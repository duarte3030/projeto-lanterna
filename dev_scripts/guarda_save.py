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

O que este script NAO cobre: indice de especie, item e move dentro do Pokemon
salvo. Se um dia alguem reordenar `SPECIES_*`, nenhuma save sobrevive, e isso
precisa de outra checagem.
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


def impressao_atual():
    return {
        "mapas": indices_de_mapa(),
        "contagens": contagens(),
        "structs": layout_dos_structs(),
        "sizeof_saveblock1": tamanho_saveblock1(),
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

    n = nova.get("sizeof_saveblock1")
    if n and n > TETO_SAVEBLOCK1:
        quebras.append(f"SAVEBLOCK1 ESTOUROU: {n} B > {TETO_SAVEBLOCK1} B "
                       f"(setores 1 a 4). Save corrompe sem erro de compilacao.")
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
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
