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

   **ESTA CHECAGEM ERA CEGA ate 12/08/2026, e o buraco era grande.** Ela
   guardava o TEXTO da expressao de `DAILY_FLAGS_END`, e esse texto e feito de
   outras macros. Subir `MAX_TRAINERS_COUNT_EMERALD` de 2500 para 4000 muda
   `FLAGS_COUNT` de 4704 para 6200 (`flags[]` sai de 588 para 775 bytes, +187 no
   SaveBlock1) sem mudar UMA LETRA daquele texto. O script imprimiu
   "SAVE COMPATIVEL" para uma quebra de save de verdade.
   Coberto agora por `valores_de_macro()`, que resolve a cadeia no
   pre-processador de C e guarda o NUMERO.

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

6. **`mapLayoutId` (0x32 do SaveBlock1).** Irmao do item 1, e ate 22/08/2026 um
   PONTO CEGO declarado: a save guarda o NUMERO do layout, e esse numero e a
   posicao do layout dentro de `data/layouts/layouts.json` contando SO os que
   tem `border_filepath` no disco. Apagar um layout, mover um layout ou apagar
   um border.bin desloca o id de todos os seguintes, sem mudar mapa nenhum e
   sem erro de compilacao: quem estivesse parado la carrega a geometria de
   outro mapa. Coberto por `numeros_de_layout()`, com o lado velho lido do
   commit `REF_LAYOUT` enquanto a impressao gravada nao tiver a chave.

O que este script continua NAO cobrindo: qualquer estado novo que alguem
resolva salvar. Campo novo em struct de save e quebra por definicao, e a
checagem 3 pega, mas so depois de escrito.
"""
import collections
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


MACROS_DE_TAMANHO = ("FLAGS_COUNT", "VARS_COUNT", "SYSTEM_FLAGS",
                     "MAX_TRAINERS_COUNT", "NUM_FLAG_BYTES")


def valores_de_macro():
    """Resolve as macros que dimensionam o SaveBlock, como NUMERO.

    Guardar o texto da expressao nao serve: ele e feito de outras macros e nao
    muda quando elas mudam. Ver o item 2 do docstring; foi assim que 187 bytes
    de crescimento passaram batido.

    Sem compilador na maquina, devolve {"_sem_cpp": True} e o compara() avisa em
    vez de fingir que conferiu.
    """
    import subprocess
    import tempfile
    fonte = "#include \"constants/flags.h\"\n#include \"constants/opponents.h\"\n"
    fonte += "#include \"constants/vars.h\"\n"
    for i, nome in enumerate(MACROS_DE_TAMANHO):
        fonte += f"#ifdef {nome}\nint marca_{i} = {nome};\n#endif\n"
    with tempfile.NamedTemporaryFile("w", suffix=".c", delete=False) as f:
        f.write(fonte)
        caminho = f.name
    try:
        r = subprocess.run(["gcc", "-E", "-I", f"{RAIZ}/include",
                            "-I", f"{RAIZ}/include/constants", "-I", RAIZ, caminho],
                           capture_output=True, text=True, timeout=60)
    except Exception:
        return {"_sem_cpp": True}
    finally:
        os.unlink(caminho)
    if r.returncode != 0:
        return {"_sem_cpp": True}
    out = {}
    for linha in r.stdout.splitlines():
        m = re.match(r"int marca_(\d+) = (.+);\s*$", linha.strip())
        if not m:
            continue
        nome = MACROS_DE_TAMANHO[int(m.group(1))]
        expr = m.group(2)
        if not re.fullmatch(r"[0-9xXa-fA-F()+\-*/%\s]+", expr):
            continue  # sobrou identificador: nao da para avaliar com seguranca
        try:
            out[nome] = int(eval(expr, {"__builtins__": {}}, {}))
        except Exception:
            pass
    return out


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


REF_LAYOUT = "852be4632a"


def numeros_de_layout(texto, existe):
    """LAYOUT_* -> numero, REPLICANDO `generate_layouts_constants_text`.

    `SaveBlock1.mapLayoutId` (0x32) guarda esse numero, e ele nao e a posicao
    dentro de `layouts.json`: o gerador (tools/mapjson/mapjson.cpp:895) PULA,
    sem gastar numero, todo layout cujo `border_filepath` nao existe no disco.
    Medido em 22/08/2026: 2.167 entradas no JSON, 2.032 numeradas, e por isso
    apagar um border.bin desloca o id de TODO layout seguinte e manda a save
    parada la carregar outro mapa. Este era o ponto CEGO do guarda, e o achado
    e da remocao fisica dos mapas cortados, que encolhe border.bin em vez de
    apagar exatamente para nao mexer nisto.

    Fica de fora, de proposito: mapa VIVO que troca o campo `layout` de nome.
    Isso tambem muda o `mapLayoutId` dele, mas e mudanca deliberada de conteudo,
    e nao deslocamento silencioso de indice, que e o que este bloco caca.
    """
    num, i = {}, 1
    for l in json.loads(texto)["layouts"]:
        if not existe(l.get("border_filepath", "")):
            continue
        num[l["id"]] = i
        i += 1
    return num


def indices_de_layout():
    return numeros_de_layout(
        open(f"{RAIZ}/data/layouts/layouts.json", encoding="utf-8").read(),
        lambda p: os.path.exists(f"{RAIZ}/{p}"))


def layouts_do_git(ref=REF_LAYOUT):
    """Os numeros de layout COMO ERAM no commit de referencia, ou None.

    A impressao gravada e de 11/08/2026 e nao tem esta chave; sem um lado velho
    a checagem so sabe avisar. O repositorio e o lado velho: `git ls-tree` diz
    quais border.bin existiam la, que e o que decide quem gasta numero.
    """
    import subprocess
    def sai(*a):
        r = subprocess.run(a, cwd=RAIZ, capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    js = sai("git", "show", f"{ref}:data/layouts/layouts.json")
    arv = sai("git", "ls-tree", "-r", "--name-only", ref, "data/layouts/")
    if js is None or arv is None:
        return None
    tinha = set(arv.split())
    return numeros_de_layout(js, lambda p: p in tinha)


def revisao_de_layout():
    """SAVE_LAYOUT_REVISION de include/save.h, que decide se a save velha CARREGA.

    Este guarda nasceu cego para ela, e a cegueira era grande: ele lê global.h,
    flags.h, vars.h e map_groups.json, nunca save.h. Quem invalida save de
    verdade é `SECTOR_SIGNATURE`, e mexer nela apaga toda save existente do
    mundo sem mudar um byte de nenhum arquivo que este script olhava.

    Devolve None se o header não tiver a macro (build anterior ao J9, 18/08/2026).
    """
    try:
        t = open(f"{RAIZ}/include/save.h", encoding="utf-8").read()
    except OSError:
        return None
    m = re.search(r"^#define\s+SAVE_LAYOUT_REVISION\s+(\d+)", t, re.M)
    return int(m.group(1)) if m else None


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


def elf_esta_velho():
    """True se algum header mudou depois do ultimo build.

    Sem isto, `tamanho_saveblock1()` responde pelo ELF antigo e o script aprova
    uma mudanca que nem foi compilada. Foi o segundo motivo do falso verde de
    12/08/2026: eu mudei `opponents.h` e o tamanho lido continuou o da build da
    vespera.
    """
    elf = f"{RAIZ}/pokeemerald.elf"
    if not os.path.exists(elf):
        return False
    t = os.path.getmtime(elf)
    for pasta in (f"{RAIZ}/include", f"{RAIZ}/include/constants"):
        for nome in os.listdir(pasta):
            if nome.endswith(".h") and os.path.getmtime(f"{pasta}/{nome}") > t:
                return True
    return False


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


def ordinais_de_enum(header, prefixo, ate=None):
    """nome -> posicao dentro do enum, na ordem em que o arquivo declara.

    Guarda POSICAO e nao valor de proposito: entrada sem `= N` explicito herda o
    valor da anterior mais um, entao a posicao e o que realmente define o numero,
    e reordenar ou inserir no meio aparece na posicao mesmo quando ninguem
    escreveu numero nenhum.

    `ate` corta a leitura na linha do sentinela de contagem (ex. "ITEMS_COUNT").
    FALSO POSITIVO MEDIDO em 15/08/2026, e ele custou uma leva parada: sem esse
    corte, a varredura de `items.h` pegava tambem `ITEM_FIELD_ARROW` (que e
    apelido de ITEMS_COUNT, nao item) e os SETE membros de `enum ItemType`
    (ITEM_USE_MAIL e irmaos, valores 0 a 6 de OUTRO enum). Resultado: acrescentar
    UM item no fim da lista, que e a unica forma segura de acrescentar item,
    fazia o guarda gritar "INSERIDO NO MEIO" e "MOVIDO" oito vezes. Nenhum
    daqueles oito nomes e id guardado em save.
    """
    txt = open(f"{RAIZ}/include/constants/{header}").read()
    txt = re.sub(r"/\*.*?\*/", "", txt, flags=re.S)
    txt = re.sub(r"//[^\n]*", "", txt)
    if ate:
        i = txt.find(ate)
        if i != -1:
            txt = txt[:i]
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
        # `ate` so aqui: em moves.h os sentinelas MOVES_COUNT_GEN1..GEN9 ficam no
        # MEIO do enum e cortar no primeiro esconderia 700 moves. items.h tem um
        # ITEMS_COUNT so, e ele e o fim da lista de verdade.
        "items": ordinais_de_enum("items.h", "ITEM", ate="ITEMS_COUNT"),
        "moves": ordinais_de_enum("moves.h", "MOVE"),
    }


def impressao_atual():
    return {
        "mapas": indices_de_mapa(),
        "contagens": contagens(),
        "macros": valores_de_macro(),
        "structs": layout_dos_structs(),
        "layout_da_save": revisao_de_layout(),
        "sizeof_saveblock1": tamanho_saveblock1(),
        "dados": indices_de_dado(),
        "layouts": indices_de_layout(),
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

    # Macros resolvidas em numero. Impressao velha sem a chave "macros" e de
    # antes desta checagem existir: nao inventa quebra, mas avisa.
    vmac, nmac = velha.get("macros"), nova.get("macros") or {}
    if vmac is None and nmac:
        quebras.append("AVISO: impressao velha nao tem 'macros'. Ela foi gravada "
                       "antes de 12/08/2026, quando crescer FLAGS_COUNT passava "
                       "batido. Regrave assim que a janela de save permitir.")
    elif not vmac:
        pass  # impressao velha e nova sem macros: nada a comparar
    elif nmac.get("_sem_cpp") or vmac.get("_sem_cpp"):
        quebras.append("AVISO: sem gcc para resolver as macros de tamanho. "
                       "FLAGS_COUNT e MAX_TRAINERS_COUNT NAO foram conferidos "
                       "nesta rodada. Isso e cegueira, nao aprovacao.")
    else:
        for k, a in vmac.items():
            b = nmac.get(k)
            if a != b:
                quebras.append(f"MACRO DE TAMANHO MUDOU: {k} era {a}, virou {b}. "
                               f"flags[] e vars[] mudam de tamanho e empurram tudo "
                               f"que vem depois deles no SaveBlock1.")

    # `mapLayoutId` (0x32). Mesma regra dos mapas: sumir e mover reprovam,
    # entrar no FIM e livre. Impressao velha sem a chave nao inventa quebra; o
    # `main` enche esse lado com o commit REF_LAYOUT antes de chamar aqui.
    vlay = velha.get("layouts") or {}
    nlay = nova.get("layouts") or {}
    ultimo = max(vlay.values()) if vlay else -1
    for nome, pos in vlay.items():
        if nome not in nlay:
            quebras.append(f"LAYOUT APAGADO: {nome} era o mapLayoutId {pos}. "
                           f"Todo layout depois dele anda um, e save parada num "
                           f"deles carrega a geometria de outro mapa.")
        elif nlay[nome] != pos:
            quebras.append(f"LAYOUT MOVIDO: {nome} era o mapLayoutId {pos}, "
                           f"virou {nlay[nome]}. Save parada nele carrega a "
                           f"geometria de outro mapa.")
    for nome, pos in nlay.items():
        if nome not in vlay and pos <= ultimo:
            quebras.append(f"LAYOUT INSERIDO NO MEIO: {nome} entrou como "
                           f"mapLayoutId {pos}, empurrando os seguintes.")

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

    # ------------------------------------------------------------------
    # Revisao de layout, e a AMARRACAO dela com tudo que veio acima.
    #
    # Roda por ultimo de proposito: precisa da lista de quebras ja fechada.
    # Ate 18/08/2026 o guarda apenas GUARDAVA SAVE_LAYOUT_REVISION, e as duas
    # coisas nao se falavam: quem deslocasse campo do SaveBlock1 e esquecesse de
    # subir a revisao voltava a ter save velha CARREGANDO em silencio e sendo
    # lida deslocada, que e o defeito exato que esta onda gastou um bloco para
    # matar. Disciplina nao e portao; isto e.
    #
    # So conta como "deslocou" o que reinterpreta a save. Os AVISO acima
    # (impressao velha sem 'macros', falta de gcc) sao CEGUEIRA declarada, nao
    # medida de quebra, e cegueira nao pode exigir revisao nova de ninguem.
    desloca = [q for q in quebras if not q.startswith("AVISO")]

    # Invalidacao DELIBERADA. Nao e a mesma coisa que as quebras acima: aqui a
    # save antiga nao passa a ser lida errada, ela deixa de ser reconhecida, e o
    # menu principal abre em NEW GAME. E a saida digna, e mesmo assim custa o
    # progresso de quem esta jogando, entao tem que aparecer.
    vl, nl = velha.get("layout_da_save"), nova.get("layout_da_save")
    if vl is not None and nl is not None and vl != nl:
        quebras.append(f"REVISÃO DE LAYOUT DA SAVE MUDOU: SAVE_LAYOUT_REVISION "
                       f"era {vl}, virou {nl}. `SECTOR_SIGNATURE` muda junto e o "
                       f"motor deixa de reconhecer QUALQUER save gravada antes: "
                       f"os dois slots viram vazios e o jogo abre em NEW GAME. "
                       f"So suba este numero com a janela de save aberta.")
    elif vl is None and nl is not None:
        quebras.append("AVISO: impressao velha nao tem 'layout_da_save'. Ela foi "
                       "gravada antes de 18/08/2026, quando mexer em "
                       "SECTOR_SIGNATURE (o que decide se a save velha CARREGA) "
                       "passava batido. Enquanto ela nao for regravada NAO da "
                       "para saber se a revisao subiu, entao a amarracao entre "
                       "quebra de layout e revisao fica DESLIGADA nesta rodada. "
                       "Regrave assim que a janela permitir.")

    if vl is None or nl is None:
        # Falta um dos dois lados. Caso escrito e nao acidental: e o estado da
        # rodada de 18/08/2026, cuja impressao foi gravada antes do J9 e por isso
        # nao tem a chave. Sem os dois numeros a amarracao nao tem o que comparar,
        # e inventar quebra aqui reprovaria a propria onda que criou a revisao.
        # O AVISO logo acima e quem cobra a regravacao.
        pass
    elif desloca and nl <= vl:
        quebras.append(f"SAVE_LAYOUT_REVISION NAO SUBIU: o layout da save mudou "
                       f"({len(desloca)} quebra(s) acima) e a revisao continua "
                       f"{vl}. `SECTOR_SIGNATURE` fica igual, entao a save do "
                       f"layout ANTIGO continua sendo aceita e passa a ser lida "
                       f"DESLOCADA, em silencio, sem erro nenhum na tela. Suba "
                       f"SAVE_LAYOUT_REVISION em include/save.h para {vl + 1}: "
                       f"o jogador perde o progresso, mas perde SABENDO, e o "
                       f"Chapter Jump repoe. Carregar lixo calado e pior.")
    elif not desloca and nl > vl:
        quebras.append(f"AVISO: SAVE_LAYOUT_REVISION subiu de {vl} para {nl} sem "
                       f"nenhuma quebra de layout nesta impressao. Toda save do "
                       f"mundo foi invalidada e pode ter sido a toa. Confira se a "
                       f"quebra e real e simplesmente nao esta coberta por este "
                       f"guarda (motivo legitimo, e ai escreva qual); se nao for, "
                       f"volte a revisao para {vl}.")
    return quebras


def main():
    nova = impressao_atual()
    if "--gravar" in sys.argv:
        # 19/08/2026: o --gravar era escape hatch MUDO. Quem esbarrasse na trava
        # de revisao podia cala-la regravando a impressao, e a impressao passava
        # a registrar layout novo com revisao velha, que e exatamente o estado
        # em que save antiga carrega em silencio e e lida errada. Agora ele
        # recusa. --forcar existe para o caso legitimo (quebra coberta por
        # decisao escrita), e ele EXIGE que a decisao esteja escrita em algum
        # lugar, porque quem digita --forcar sem plano esta se enganando.
        if os.path.exists(IMPRESSAO) and "--forcar" not in sys.argv:
            velha_g = json.load(open(IMPRESSAO))
            quebras_g = [q for q in compara(velha_g, nova)
                         if not q.startswith("AVISO")]
            vl = velha_g.get("layout_da_save")
            nl = nova.get("layout_da_save")
            if quebras_g and vl is not None and nl is not None and nl <= vl:
                print("RECUSADO: ha quebra de layout de save e "
                      f"SAVE_LAYOUT_REVISION nao subiu (esta em {nl}).")
                for q in quebras_g:
                    print(f"  {q.splitlines()[0]}")
                print(f"Suba a revisao para {vl + 1} em include/save.h e grave "
                      "de novo, ou use --forcar se a quebra for aceita por "
                      "decisao escrita (e escreva onde).")
                return 1
        json.dump(nova, open(IMPRESSAO, "w"), indent=1, sort_keys=True)
        n = nova.get("sizeof_saveblock1")
        print(f"impressao gravada: {len(nova['mapas'])} mapas, "
              f"SaveBlock1 = {n if n else '?'} B de {TETO_SAVEBLOCK1}")
        return 0

    if not os.path.exists(IMPRESSAO):
        print("sem impressao gravada. Rode --gravar uma vez para fixar a linha de base.")
        return 0

    velha = json.load(open(IMPRESSAO))
    de_onde = "impressao"
    if "layouts" not in velha:
        velha["layouts"] = layouts_do_git()
        de_onde = f"git {REF_LAYOUT}"
        if velha["layouts"] is None:
            print(f"AVISO: sem `git show {REF_LAYOUT}:data/layouts/layouts.json` "
                  "neste clone, o mapLayoutId fica SEM lado velho. Nao conte "
                  "esta rodada como verificada.")
    quebras = compara(velha, nova)
    print(f"mapLayoutId: {len(nova['layouts'])} layouts numerados, lado velho "
          f"lido de {de_onde}")
    # I/O fica fora do compara(), que e funcao pura e tem demo em cima dela.
    if nova.get("sizeof_saveblock1") and elf_esta_velho():
        quebras.insert(0, "AVISO: o ELF e mais velho que os headers. O tamanho "
                          "abaixo e do build anterior, nao do codigo de agora. "
                          "Builde antes de acreditar nele.")
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

    # Macro de tamanho: o falso verde de 12/08/2026. O texto de
    # daily_flags_end_expr fica IGUAL quando MAX_TRAINERS_COUNT muda, entao a
    # checagem antiga nao via nada; a nova ve porque guarda o numero.
    commac = json.loads(json.dumps(base))
    commac["macros"] = {"FLAGS_COUNT": 4704, "MAX_TRAINERS_COUNT": 2500}
    assert compara(commac, commac) == [], "igual a igual nao quebra"
    subiu = json.loads(json.dumps(commac))
    subiu["macros"] = {"FLAGS_COUNT": 6200, "MAX_TRAINERS_COUNT": 4000}
    q = compara(commac, subiu)
    assert any("MACRO DE TAMANHO MUDOU" in x and "FLAGS_COUNT" in x for x in q), q
    # sem compilador o script avisa, e avisar NAO e aprovar
    cego = json.loads(json.dumps(commac)); cego["macros"] = {"_sem_cpp": True}
    assert any("cegueira" in x for x in compara(commac, cego))
    # impressao velha, gravada antes de existir a chave: avisa, nao inventa quebra
    assert any("nao tem 'macros'" in x for x in compara(base, commac))

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

    # Revisao de layout: a unica quebra que INVALIDA de proposito em vez de
    # reinterpretar. Sem esta checagem o guarda era cego para SECTOR_SIGNATURE,
    # que e exatamente o que decide se a save velha carrega.
    comrev = json.loads(json.dumps(base)); comrev["layout_da_save"] = 1
    assert compara(comrev, comrev) == [], "igual a igual nao quebra"
    subiu = json.loads(json.dumps(comrev)); subiu["layout_da_save"] = 2
    assert any("REVISÃO DE LAYOUT DA SAVE MUDOU" in x
               for x in compara(comrev, subiu)), compara(comrev, subiu)
    # impressao velha sem a chave: avisa, nao inventa quebra
    assert any("layout_da_save" in x for x in compara(base, comrev))
    assert compara(base, base) == [], "as duas sem a chave nao quebram"

    # AMARRACAO (J10): a revisao so protege se o guarda EXIGIR que ela suba.
    # Os quatro cantos, com mutacao plantada em cima de comrev (revisao 1).
    def _quebrou(d):  # muda o layout de verdade: SaveBlock1 cresce 84 B
        d = json.loads(json.dumps(d)); d["sizeof_saveblock1"] = 1084; return d

    # canto 1: layout mudou E revisao subiu = quebra deliberada, sem cobranca
    c1 = _quebrou(comrev); c1["layout_da_save"] = 2
    q = compara(comrev, c1)
    assert any("MUDOU DE TAMANHO" in x for x in q), q
    assert any("REVISÃO DE LAYOUT DA SAVE MUDOU" in x for x in q), q
    assert not any("NAO SUBIU" in x for x in q), q

    # canto 2: layout mudou e revisao NAO subiu = REPROVA. E o defeito que o J9
    # deixou aberto: sem esta linha a save velha volta a carregar lida deslocada.
    q = compara(comrev, _quebrou(comrev))
    assert any("SAVE_LAYOUT_REVISION NAO SUBIU" in x for x in q), q
    # descer a revisao e tao ruim quanto nao subir: a assinatura volta a colidir
    baixou = _quebrou(comrev); baixou["layout_da_save"] = 0
    assert any("NAO SUBIU" in x for x in compara(comrev, baixou))

    # canto 3: layout igual e revisao igual = passa calado
    assert compara(comrev, json.loads(json.dumps(comrev))) == []

    # canto 4: revisao subiu SEM quebra = avisa. Invalidar a save de todo mundo
    # a toa nao e crime, mas nao pode passar em silencio.
    so_rev = json.loads(json.dumps(comrev)); so_rev["layout_da_save"] = 2
    q = compara(comrev, so_rev)
    assert any("sem" in x and "quebra de layout" in x for x in q), q

    # a rodada de 18/08/2026: impressao velha SEM a chave e layout quebrado.
    # A amarracao tem que ficar DESLIGADA, senao ela reprova a propria onda que
    # criou a revisao. Este e o caso que o compara() trata escrito, nao por acaso.
    q = compara(base, _quebrou(comrev))
    assert any("MUDOU DE TAMANHO" in x for x in q), q
    assert not any("NAO SUBIU" in x for x in q), q
    assert any("DESLIGADA" in x for x in q), q
    # e o header de verdade tem que responder um numero
    assert isinstance(revisao_de_layout(), int), \
        "include/save.h perdeu SAVE_LAYOUT_REVISION"

    # mapLayoutId. Impressao sem a chave nao inventa quebra; sumir e mover
    # reprovam; entrar no fim e livre.
    comlay = json.loads(json.dumps(base))
    comlay["layouts"] = {"LAYOUT_A": 1, "LAYOUT_B": 2}
    assert compara(base, comlay) == [], compara(base, comlay)
    assert compara(comlay, comlay) == [], "igual a igual nao quebra"
    fim = json.loads(json.dumps(comlay)); fim["layouts"]["LAYOUT_C"] = 3
    assert compara(comlay, fim) == [], compara(comlay, fim)
    meio = json.loads(json.dumps(comlay))
    meio["layouts"] = {"LAYOUT_C": 1, "LAYOUT_A": 2, "LAYOUT_B": 3}
    q = compara(comlay, meio)
    assert any("LAYOUT MOVIDO" in x and "LAYOUT_A" in x for x in q), q
    assert any("LAYOUT INSERIDO NO MEIO" in x for x in q), q
    sem = json.loads(json.dumps(comlay)); del sem["layouts"]["LAYOUT_A"]
    assert any("LAYOUT APAGADO" in x for x in compara(comlay, sem))

    # A MUTACAO que interessa, plantada na regra de verdade: apagar o border.bin
    # de um layout do meio nao muda UMA letra do layouts.json e mesmo assim
    # desloca todo mundo depois dele. Se `numeros_de_layout` ignorasse o
    # border_filepath, este caso passaria calado.
    texto = open(f"{RAIZ}/data/layouts/layouts.json", encoding="utf-8").read()
    vivo = lambda p: os.path.exists(f"{RAIZ}/{p}")
    reais_lay = numeros_de_layout(texto, vivo)
    assert len(reais_lay) > 1000, len(reais_lay)
    # Borda EXCLUSIVA de um layout so: 4 arquivos de borda sao compartilhados
    # por mais de um layout, e escolher um deles apagaria varios de uma vez e
    # embaralharia a conta.
    usos = collections.Counter(l["border_filepath"]
                               for l in json.loads(texto)["layouts"])
    alvo = next(l["border_filepath"] for l in json.loads(texto)["layouts"]
                if usos[l["border_filepath"]] == 1 and vivo(l["border_filepath"]))
    depois = len(reais_lay) - numeros_de_layout(
        texto, vivo)[next(l["id"] for l in json.loads(texto)["layouts"]
                          if l["border_filepath"] == alvo)]
    mutante = numeros_de_layout(texto, lambda p: p != alvo and vivo(p))
    q = compara({**base, "layouts": reais_lay}, {**base, "layouts": mutante})
    assert sum("LAYOUT APAGADO" in x for x in q) == 1, q[:3]
    assert sum("LAYOUT MOVIDO" in x for x in q) == depois, \
        "apagar um border.bin tem que deslocar TODOS os layouts seguintes"

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
