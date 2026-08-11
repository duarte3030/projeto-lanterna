#!/usr/bin/env python3
"""Impede mudanca que INVALIDA save file de quem ja esta jogando.

Uso:
    python3 dev_scripts/guarda_save.py            # confere contra a impressao gravada
    python3 dev_scripts/guarda_save.py --gravar   # grava a impressao atual (so quando a quebra for aceita)

Por que existe
--------------
O Gui joga 50 horas e acha um bug. A gente conserta, ele atualiza a ROM, e a
save tem que continuar valendo. Em pokeemerald nao existe versionamento de save
nem migracao: o SaveBlock e despejado cru na flash. Entao qualquer INDICE que a
save guarda vira uma promessa permanente.

O que quebra uma save, em ordem de facilidade de errar:

1. **Posicao do jogador.** A save guarda `location.mapGroup` e `location.mapNum`,
   que sao INDICES, nao nomes. Apagar ou reordenar mapa no meio de um grupo
   desloca todos os seguintes, e a save volta em outro lugar. Inserir grupo no
   meio de `group_order` desloca grupos inteiros.
   Regra: mapa novo so no FIM do grupo, grupo novo so no FIM de `group_order`.

2. **FLAGS_COUNT e VARS_COUNT.** `flags[]` e `vars[]` moram dentro do
   SaveBlock1, e `flags[]` esta em 0x1270 (`include/global.h`). Crescer o
   numero de flags empurra TUDO que vem depois. Por isso flag nova sai do pool
   `FLAG_UNUSED_*`, que ja esta dentro da contagem, e nunca de numero novo.

3. **Layout dos structs de save.** Trocar ordem de campo em SaveBlock1/2/3
   reinterpreta a save inteira. So append, e so em espaco que ja existe.

4. **Teto de tamanho.** SaveBlock1 ocupa os setores 1 a 4, ou seja
   4 x 3968 = 15872 bytes. Passar disso nao da erro de compilacao obvio, da save
   corrompida.

5. **Indice de especie, item e move.** A save guarda o NUMERO deles dentro do
   Pokemon e da bag. Reordenar `SPECIES_*`, `ITEM_*` ou `MOVE_*` reinterpreta o
   time inteiro do jogador, sem mexer em mapa nem em SaveBlock, entao nenhuma
   das quatro checagens acima enxerga. Coberto desde 11/08/2026 por
   `indices_de_dado()`, que guarda a POSICAO de cada nome dentro do enum:
   acrescentar no FIM e livre, mover ou inserir no meio reprova.

O que este script continua NAO cobrindo: qualquer estado novo que alguem
resolva salvar. Campo novo em struct de save e quebra por definicao, e a
checagem 3 pega, mas so depois de escrito.
"""
import hashlib
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMPRESSAO = f"{RAIZ}/dev_scripts/save_impressao.json"
TETO_SAVEBLOCK1 = 4 * 3968


def indices_de_mapa():
    """nome do mapa -> (indice do grupo, indice dentro do grupo)."""
    g = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    saida = {}
    for gi, grp in enumerate(g["group_order"]):
        for mi, m in enumerate(g.get(grp, [])):
            saida[m] = [gi, mi]
    return saida


def contagens():
    """Numeros que definem o tamanho dos arrays dentro do SaveBlock."""
    out = {}
    flags = open(f"{RAIZ}/include/constants/flags.h").read()
    # FLAGS_COUNT = DAILY_FLAGS_END + 1: pegamos o ultimo numero literal atribuido
    m = re.findall(r"#define\s+DAILY_FLAGS_END\s+\(?([^\n]+)", flags)
    out["daily_flags_end_expr"] = m[-1].strip() if m else "?"
    out["n_flag_unused"] = flags.count("FLAG_UNUSED")
    varsh = open(f"{RAIZ}/include/constants/vars.h").read()
    out["vars_start_end"] = re.findall(r"#define\s+VARS_(?:START|END)\s+(\S+)", varsh)
    out["n_var_unused"] = varsh.count("VAR_UNUSED")
    return out


def layout_dos_structs():
    """Hash do texto das structs de save. Muda o texto, muda o layout."""
    g = open(f"{RAIZ}/include/global.h").read()
    saida = {}
    for nome in ("SaveBlock1", "SaveBlock2", "SaveBlock3"):
        m = re.search(r"struct\s+%s\s*\{(.*?)\n\};" % nome, g, re.S)
        corpo = m.group(1) if m else ""
        # ignora comentario de offset e espaco, que mudam sem mudar layout
        limpo = re.sub(r"/\*.*?\*/", "", corpo)
        limpo = re.sub(r"//[^\n]*", "", limpo)
        limpo = re.sub(r"\s+", " ", limpo).strip()
        saida[nome] = hashlib.sha256(limpo.encode()).hexdigest()[:16]
    return saida


def tamanho_saveblock1():
    """Le do ELF, se existir. Devolve None se ainda nao buildou."""
    import subprocess
    elf = f"{RAIZ}/pokeemerald.elf"
    if not os.path.exists(elf):
        return None
    dka = os.environ.get("DEVKITARM", "")
    nm = f"{dka}/bin/arm-none-eabi-nm" if dka else "nm"
    if not os.path.exists(nm):
        nm = "nm"
    try:
        r = subprocess.run([nm, "-S", elf], capture_output=True, text=True, timeout=60)
    except Exception:
        return None
    for linha in r.stdout.splitlines():
        p = linha.split()
        if len(p) >= 4 and p[-1] == "gSaveblock1":
            return int(p[1], 16)
    return None


def ordinais_de_enum(header, prefixo):
    """nome -> posicao dentro do enum, na ordem em que o arquivo declara.

    Guarda POSICAO e nao valor de proposito: entrada sem `= N` explicito herda o
    valor da anterior mais um, entao a posicao e o que realmente define o numero,
    e reordenar ou inserir no meio aparece na posicao mesmo quando ninguem
    escreveu numero nenhum.
    """
    txt = open(f"{RAIZ}/include/constants/{header}").read()
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r"//[^\n]*", "", txt)
    nomes = re.findall(r"^\s*(%s_[A-Z0-9_]+)\s*(?:=[^,\n]+)?,\s*$" % prefixo,
                       txt, re.M)
    return {n: i for i, n in enumerate(nomes)}


def indices_de_dado():
    """Especie, item e move: o que o Pokemon salvo guarda como INDICE.

    O buraco que este bloco fecha estava declarado no topo deste arquivo: a save
    guarda especie, item segurado, move e item da bag como NUMERO. Reordenar
    qualquer um desses enums reinterpreta o time inteiro do jogador, e nenhuma
    das outras checagens enxerga isso, porque nem o SaveBlock nem os mapas mudam.
    """
    return {
        "species": ordinais_de_enum("species.h", "SPECIES"),
        "items": ordinais_de_enum("items.h", "ITEM"),
        "moves": ordinais_de_enum("moves.h", "MOVE"),
    }


def impressao_atual():
    return {
        "mapas": indices_de_mapa(),
        "contagens": contagens(),
        "structs": layout_dos_structs(),
        "sizeof_saveblock1": tamanho_saveblock1(),
        "dados": indices_de_dado(),
    }


def compara(velha, nova):
    """Devolve lista de quebras. Lista vazia = save continua valendo."""
    quebras = []

    vm, nm_ = velha["mapas"], nova["mapas"]
    for nome, idx in vm.items():
        if nome not in nm_:
            quebras.append(f"MAPA APAGADO: {nome} ocupava {idx}. "
                           f"Save parada nele volta em lugar errado.")
        elif nm_[nome] != idx:
            quebras.append(f"MAPA MOVIDO: {nome} era {idx}, virou {nm_[nome]}. "
                           f"Save parada nele volta em lugar errado.")
    # mapa novo so pode ter entrado DEPOIS do ultimo indice de cada grupo
    for nome, (gi, mi) in nm_.items():
        if nome in vm:
            continue
        antigos = [b for a, b in vm.items() if b[0] == gi]
        if antigos and mi <= max(b[1] for b in antigos):
            quebras.append(f"MAPA INSERIDO NO MEIO: {nome} entrou em {[gi, mi]}, "
                           f"empurrando os seguintes. Acrescente no FIM do grupo.")

    if velha["contagens"] != nova["contagens"]:
        for k in velha["contagens"]:
            a, b = velha["contagens"][k], nova["contagens"].get(k)
            if a != b and not k.startswith("n_"):
                quebras.append(f"CONTAGEM MUDOU: {k} era {a}, virou {b}. "
                               f"flags[] e vars[] mudam de tamanho e empurram o SaveBlock.")

    for k, v in velha["structs"].items():
        if nova["structs"].get(k) != v:
            quebras.append(f"STRUCT MUDOU: {k} teve o corpo alterado. "
                           f"A save inteira e reinterpretada. So append, e so em espaco existente.")

    # Tamanho do SaveBlock1: QUALQUER mudanca quebra save, nao so estourar o teto.
    # A primeira versao so olhava o teto, e por isso disse "SAVE COMPATIVEL" depois
    # de eu crescer FLAGS_COUNT e levar o bloco de 15764 para 15848 B. Eu sabia que
    # tinha quebrado e a ferramenta disse que nao. Notica boa e suspeita ate provar
    # que e real.
    v, n = velha.get("sizeof_saveblock1"), nova.get("sizeof_saveblock1")
    if v and n and v != n:
        quebras.append(f"SAVEBLOCK1 MUDOU DE TAMANHO: {v} B -> {n} B. "
                       f"Tudo que vem depois do campo que cresceu muda de lugar, "
                       f"e save antiga passa a ser lida errada.")
    if n and n > TETO_SAVEBLOCK1:
        quebras.append(f"SAVEBLOCK1 ESTOUROU: {n} B > {TETO_SAVEBLOCK1} B "
                       f"(setores 1 a 4). Save corrompe sem erro de compilacao.")

    # Especie, item e move: a save guarda o NUMERO deles dentro do Pokemon.
    # Impressao velha sem a chave "dados" e de antes desta checagem existir, e
    # nao tem contra o que comparar: nao inventa quebra.
    for tipo, vd in (velha.get("dados") or {}).items():
        nd = (nova.get("dados") or {}).get(tipo, {})
        ultimo = max(vd.values()) if vd else -1
        for nome, pos in vd.items():
            if nome not in nd:
                quebras.append(f"{tipo.upper()} APAGADO: {nome} ocupava {pos}. "
                               f"Pokemon salvo com ele vira outra coisa.")
            elif nd[nome] != pos:
                quebras.append(f"{tipo.upper()} MOVIDO: {nome} era {pos}, virou "
                               f"{nd[nome]}. O time salvo inteiro e reinterpretado.")
        for nome, pos in nd.items():
            if nome not in vd and pos <= ultimo:
                quebras.append(f"{tipo.upper()} INSERIDO NO MEIO: {nome} entrou em "
                               f"{pos}, empurrando os seguintes. Acrescente no FIM.")
    return quebras


def main():
    nova = impressao_atual()
    if "--gravar" in sys.argv:
        json.dump(nova, open(IMPRESSAO, "w"), indent=1, sort_keys=True)
        n = nova.get("sizeof_saveblock1")
        print(f"impressao gravada: {len(nova['mapas'])} mapas, "
              f"SaveBlock1 = {n if n else '?'} B de {TETO_SAVEBLOCK1}")
        return 0

    if not os.path.exists(IMPRESSAO):
        print("sem impressao gravada. Rode --gravar uma vez para fixar a linha de base.")
        return 0

    velha = json.load(open(IMPRESSAO))
    quebras = compara(velha, nova)
    novos = len(set(nova["mapas"]) - set(velha["mapas"]))
    n = nova.get("sizeof_saveblock1")
    print(f"mapas: {len(velha['mapas'])} -> {len(nova['mapas'])} ({novos} novos)")
    print(f"SaveBlock1: {n if n else '?'} B de {TETO_SAVEBLOCK1} "
          f"({100*n/TETO_SAVEBLOCK1:.1f}%)" if n else "SaveBlock1: nao buildado")
    if not quebras:
        print("\nSAVE COMPATIVEL: nenhuma mudanca invalida save existente.")
        return 0
    print(f"\n{len(quebras)} QUEBRA(S) DE SAVE:")
    for q in quebras:
        print(f"  {q}")
    print("\nSe a quebra for aceita de proposito, rode --gravar. Senao, conserte.")
    return 1


def demo():
    """Confere que cada modo de quebra e mesmo detectado."""
    base = {"mapas": {"A": [0, 0], "B": [0, 1]},
            "contagens": {"daily_flags_end_expr": "X"},
            "structs": {"SaveBlock1": "abc"},
            "sizeof_saveblock1": 1000}
    assert compara(base, base) == [], "igual a igual nao quebra"

    # apagar mapa do meio: B some
    sem_b = json.loads(json.dumps(base)); del sem_b["mapas"]["B"]
    assert any("APAGADO" in q for q in compara(base, sem_b))

    # inserir no meio: C entra no indice 0 e empurra
    meio = json.loads(json.dumps(base)); meio["mapas"] = {"C": [0, 0], "A": [0, 1], "B": [0, 2]}
    q = compara(base, meio)
    assert any("MOVIDO" in x for x in q), q

    # acrescentar no FIM e legitimo, nao quebra
    fim = json.loads(json.dumps(base)); fim["mapas"]["C"] = [0, 2]
    assert compara(base, fim) == [], compara(base, fim)

    # struct mudou
    st = json.loads(json.dumps(base)); st["structs"]["SaveBlock1"] = "zzz"
    assert any("STRUCT" in x for x in compara(base, st))

    # estourou o teto
    gr = json.loads(json.dumps(base)); gr["sizeof_saveblock1"] = TETO_SAVEBLOCK1 + 1
    assert any("ESTOUROU" in x for x in compara(base, gr))

    # crescer SEM estourar o teto tambem quebra: foi o caso que passou batido
    cresceu = json.loads(json.dumps(base)); cresceu["sizeof_saveblock1"] = 1084
    assert any("MUDOU DE TAMANHO" in x for x in compara(base, cresceu)), \
        "crescer dentro do teto continua invalidando save"

    # Especie, item e move. Impressao sem a chave "dados" e anterior a esta
    # checagem: nao pode inventar quebra em quem gravou antes.
    assert compara(base, json.loads(json.dumps(base))) == []

    comdados = json.loads(json.dumps(base))
    comdados["dados"] = {"species": {"SPECIES_NONE": 0, "SPECIES_BULBASAUR": 1,
                                     "SPECIES_IVYSAUR": 2}}
    assert compara(comdados, comdados) == [], "igual a igual nao quebra"

    # acrescentar no FIM e legitimo: e assim que treinador e item novo entram
    apend = json.loads(json.dumps(comdados))
    apend["dados"]["species"]["SPECIES_VENUSAUR"] = 3
    assert compara(comdados, apend) == [], compara(comdados, apend)

    # inserir no MEIO empurra todo mundo depois: o time salvo vira outra coisa
    ins = {"species": {"SPECIES_NONE": 0, "SPECIES_NOVO": 1,
                       "SPECIES_BULBASAUR": 2, "SPECIES_IVYSAUR": 3}}
    q = compara(comdados, {**comdados, "dados": ins})
    assert any("MOVIDO" in x for x in q), q
    assert any("INSERIDO NO MEIO" in x for x in q), q

    # apagar do meio
    ap = {"species": {"SPECIES_NONE": 0, "SPECIES_IVYSAUR": 2}}
    assert any("APAGADO" in x for x in compara(comdados, {**comdados, "dados": ap}))

    # a leitura de verdade do header tem que achar as tres tabelas e comecar em NONE
    reais = indices_de_dado()
    for tipo, prefixo in (("species", "SPECIES"), ("items", "ITEM"), ("moves", "MOVE")):
        assert len(reais[tipo]) > 300, (tipo, len(reais[tipo]))
        assert reais[tipo][f"{prefixo}_NONE"] == 0, tipo
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
