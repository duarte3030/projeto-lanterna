#!/usr/bin/env python3
"""Liga os NPCs de Unova que entraram mudos e que no BW3G tem FUNCAO.

Medido em 05/08/2026, contra `data/maps/Unova_*/map.json`:

    147 objetos com `"script": "0"`
     96 deles estao com script 0 NO PROPRIO BW3G, ou seja, sao mudos la tambem
     51 tem script na fonte, e nenhum deles e dialogo: sao mecanica

Esse e o achado que muda a tarefa. Nao ha fala de NPC para portar; o importador
original ja levou todo `jumptextfaceplayer` / `writetext` que existia. O que
sobrou sao 51 objetos que fazem alguma coisa, e "alguma coisa" e o que este
script liga, sempre no comando que este repo JA TEM:

| familia            | n  | como entra                                      |
|--------------------|----|-------------------------------------------------|
| loja especializada |  6 | `pokemart` com a lista de data/items/marts.asm  |
| arvore de fruta    | 13 | a baga de data/items/fruit_trees.asm, uma vez,  |
|                    |    | com uma flag por arvore                         |
| fossil da Relic    |  2 | `giveitem` + a flag no proprio objeto, que e o  |
|                    |    | `disappear` do gen 2                            |
| vendedor de ficha  |  2 | o balconista de MauvilleCity_GameCorner         |
| avaliador de nome  |  1 | o de SlateportCity_NameRatersHouse              |
| apagador de golpe  |  1 | o de LilycoveCity_MoveDeletersHouse             |

Fica de fora, e sai no relatorio: 17 trocas de Pokemon (precisam de entrada em
`gIngameTrades`, que e tabela, nao script), 2 do Day Care (o Day Care do gen 3 e
um par de scripts de ON_TRANSITION com LOCALID, nao um NPC solto), 3 de sala de
link, 4 de decoracao e 1 casa de batalha que depende de var de enredo.

Duas trocas honestas, marcadas no codigo gerado: as bagas do gen 2 viram a baga
de gen 3 de mesmo efeito (PSNCUREBERRY -> PECHA, e assim por diante), e a arvore
da a fruta UMA vez em vez de reencher, porque reencher e o sistema de plantio do
gen 3, que e outra mecanica.

Faixa de flag: 0x4C3 a 0x4EE, o que sobrou da faixa desta frente depois das
grutas (`importa_placas_unova.py`).

Uso:
    python3 dev_scripts/importa_npcs_unova.py            # so relata
    python3 dev_scripts/importa_npcs_unova.py --aplica   # escreve

Idempotente: so mexe em objeto que ainda esta com `"script": "0"`.

Compatibilidade de save: nao acrescenta nem reordena objeto nenhum, so troca o
campo `script` (e, no fossil, o campo `flag`) de objeto que ja existe. Indice de
objeto, de mapa e de warp ficam iguais.
"""
import json
import os
import re
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
os.chdir(REPO)

import importa_unova as iu  # noqa: E402

APLICA = "--aplica" in sys.argv
BW3G = iu.BW3G

FLAG_BASE = 0x4C3   # depois das 15 grutas de importa_placas_unova.py
FLAG_TETO = 0x4EE

# Baga do gen 2 -> baga do gen 3 de MESMO EFEITO. Nao ha escolha aqui, e a
# tabela canonica de conversao: cada uma cura o mesmo estado.
BAGA = {
    "BERRY": "ITEM_ORAN_BERRY",             # cura 10 PS
    "GOLD_BERRY": "ITEM_SITRUS_BERRY",      # cura 30 PS
    "PSNCUREBERRY": "ITEM_PECHA_BERRY",     # veneno
    "PRZCUREBERRY": "ITEM_CHERI_BERRY",     # paralisia
    "MINT_BERRY": "ITEM_CHESTO_BERRY",      # sono
    "ICE_BERRY": "ITEM_RAWST_BERRY",        # queimadura
    "BURNT_BERRY": "ITEM_ASPEAR_BERRY",     # congelamento
    "BITTER_BERRY": "ITEM_PERSIM_BERRY",    # confusao
}

# TM que o BW3G vende e que este build (so os 50 de Hoenn) nao tem. Mesma regra
# do ITEM_TROCA de importa_unova.py: o mais proximo em tipo e papel.
TM_TROCA = {
    "TM_BULLDOZE": "ITEM_TM_DIG",              # Terra, fisico
    "TM_THUNDER_WAVE": "ITEM_TM_SHOCK_WAVE",   # Eletrico; Hoenn nao tem o de status
}


def item(nome):
    if nome in BAGA:
        return BAGA[nome]
    if nome in TM_TROCA:
        return TM_TROCA[nome]
    i = iu.ITEM_TROCA.get(nome, "ITEM_" + nome)
    return i if i in iu.ITENS_DO_BUILD else None


def le_marts():
    """MART_X -> [ITEM_...]. A lista do gen 2 e `db N` seguido de N itens."""
    s = open(f"{BW3G}/data/items/marts.asm").read()
    rotulos = re.findall(r"^\s*dw (\w+)", s, re.M)
    consts = re.findall(r"^\s*const (MART_\w+)",
                        open(f"{BW3G}/constants/mart_constants.asm").read(), re.M)
    saida = {}
    for i, rot in enumerate(rotulos):
        m = re.search(rf"^{rot}:\n(.*?)\n\s*db -1", s, re.M | re.S)
        if not m or i >= len(consts):
            continue
        itens = [item(x) for x in re.findall(r"db (\w+)", m.group(1))[1:]]
        saida[consts[i]] = [x for x in itens if x]
    return saida


def le_fruit_trees():
    """FRUITTREE_X -> ITEM_.... A ordem da tabela segue a das constantes, e a
    primeira constante e o zero reservado, que nao tem linha na tabela."""
    s = open(f"{BW3G}/data/items/fruit_trees.asm").read()
    consts = re.findall(r"^\s*const (FRUITTREE_\w+)",
                        open(f"{BW3G}/constants/script_constants.asm").read(), re.M)
    itens = re.findall(r"^\s*db (\w+)", s, re.M)
    return {c: item(n) for c, n in zip(consts, itens)}


def corpo_de(asm, rotulo):
    m = re.search(rf"^{re.escape(rotulo)}:+\s*$", asm, re.M)
    if not m:
        return ""
    out = []
    for ln in asm[m.end():].splitlines():
        if re.match(r"^\w+:", ln):
            break
        out.append(ln)
    return "\n".join(out)


MARTS = le_marts()
FRUTAS = le_fruit_trees()

# Scripts que ja existem neste repo e fazem exatamente o que o do gen 2 fazia.
REUSO = {
    "NameRater": "SlateportCity_NameRatersHouse_EventScript_NameRater",
    "MoveDeletion": "LilycoveCity_MoveDeletersHouse_EventScript_MoveDeleter",
    "gamecornercoinvendor": "MauvilleCity_GameCorner_EventScript_CoinsClerk",
}

grupos = iu.le_grupos()
idx = iu.indice_asm()
motivos = Counter()
recusados = []
plano = []      # (nome, {(x,y): (script, flag_ou_None)}, trecho)
aliases = []
proxima = [FLAG_BASE]


def nova_flag(apelido):
    n = proxima[0]
    if n > FLAG_TETO:
        raise SystemExit("faixa de flag 0x4C3-0x4EE estourou")
    proxima[0] += 1
    aliases.append(f"#define FLAG_UNOVA_{apelido:<29} FLAG_UNUSED_0x{n:03X}")
    return f"FLAG_UNOVA_{apelido}"


for _, mapas in grupos:
    for camel, const, w, h, tileset, amb, land, mus in mapas:
        nome = iu.PREFIXO + camel
        dir_mapa = f"{REPO}/data/maps/{nome}"
        p = idx.get(camel)
        if not os.path.isdir(dir_mapa) or not p:
            continue
        asm = open(p, encoding="utf-8", errors="replace").read()
        ev = iu.le_eventos(asm, camel)
        nosso = json.load(open(f"{dir_mapa}/map.json"))
        mudos = {(o["x"], o["y"]) for o in nosso["object_events"]
                 if o.get("script") == "0"}
        if not mudos:
            continue

        troca, trechos = {}, []
        for o in ev["obj"]:
            xy = (o["x"], o["y"])
            if xy not in mudos or o["script"] in ("0", "-1"):
                continue
            corpo = corpo_de(asm, o["script"])

            m = re.search(r"pokemart\s+\w+,\s*(MART_\w+)", corpo)
            if m and MARTS.get(m.group(1)):
                rot = f"{nome}_EventScript_Loja{len(trechos)}"
                lista = MARTS[m.group(1)]
                trechos.append(
                    f"\n@ {m.group(1)} do BW3G (data/items/marts.asm)\n"
                    f"{rot}::\n\tlock\n\tfaceplayer\n"
                    f"\tmessage gText_HowMayIServeYou\n\twaitmessage\n"
                    f"\tpokemart {rot}_Itens\n"
                    f"\tmsgbox gText_PleaseComeAgain, MSGBOX_DEFAULT\n"
                    f"\trelease\n\tend\n\n\t.align 2\n{rot}_Itens:\n"
                    + "".join(f"\t.2byte {x}\n" for x in lista)
                    + "\tpokemartlistend\n")
                troca[xy] = (rot, None)
                motivos["loja especializada"] += 1
                continue

            m = re.search(r"fruittree\s+(FRUITTREE_\w+)", corpo)
            if m and FRUTAS.get(m.group(1)):
                flag = nova_flag("ARVORE_" + m.group(1).replace("FRUITTREE_", ""))
                rot = f"{nome}_EventScript_Arvore"
                trechos.append(
                    f"\n@ {m.group(1)} do BW3G. ponytail: no gen 2 a arvore reenche;\n"
                    f"@ aqui a fruta sai uma vez, porque replantio e outra mecanica.\n"
                    f"{rot}::\n\tlock\n"
                    f"\tgoto_if_set {flag}, Unova_EventScript_GrutaVazia\n"
                    f"\tgiveitem {FRUTAS[m.group(1)]}\n"
                    f"\tsetflag {flag}\n\trelease\n\tend\n")
                troca[xy] = (rot, None)
                motivos["arvore de fruta"] += 1
                continue

            m = re.search(r"verbosegiveitem\s+(\w+)", corpo)
            if m and item(m.group(1)):
                flag = nova_flag("ITEM_" + o["script"].replace("Script", "").upper())
                rot = f"{nome}_EventScript_{o['script'].replace('Script', '')}"
                trechos.append(
                    f"\n@ {o['script']} do BW3G: o `disappear` de la vira a flag do\n"
                    f"@ proprio objeto, que e o que esconde o sprite depois de pegar.\n"
                    f"{rot}::\n\tlock\n\tgiveitem {item(m.group(1))}\n"
                    f"\tsetflag {flag}\n\tremoveobject VAR_LAST_TALKED\n"
                    f"\trelease\n\tend\n")
                troca[xy] = (rot, flag)
                motivos["fossil"] += 1
                continue

            alvo = next((v for k, v in REUSO.items() if k in corpo), None)
            if alvo:
                troca[xy] = (alvo, None)
                motivos["reaproveitado: " + alvo.split("_EventScript_")[1]] += 1
                continue

            motivos["sem regra"] += 1
            recusados.append(f"{nome}/{o['script']}")

        if troca:
            cab = ("\n@ NPCs ligados a partir do BW3G por "
                   "dev_scripts/importa_npcs_unova.py\n")
            plano.append((nome, troca, cab + "".join(trechos) if trechos else ""))

total = sum(len(t) for _, t, _ in plano)
print(f"mapas tocados: {len(plano)}   NPCs ligados: {total}")
for k, v in motivos.most_common():
    print(f"  {v:4d}  {k}")
print(f"flags gastas: {len(aliases)} "
      f"(0x{FLAG_BASE:03X} a 0x{proxima[0] - 1:03X})")
if recusados:
    print(f"\nsem regra: {len(recusados)}")
    for r in sorted(set(recusados))[:10]:
        print("   ", r)

if not APLICA:
    print("\n(nada escrito; rode com --aplica)")
    sys.exit(0)

for nome, troca, trecho in plano:
    p = f"{REPO}/data/maps/{nome}/map.json"
    d = json.load(open(p))
    for o in d["object_events"]:
        alvo = troca.get((o["x"], o["y"]))
        if alvo and o.get("script") == "0":
            o["script"] = alvo[0]
            if alvo[1]:
                o["flag"] = alvo[1]
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if trecho:
        with open(f"{REPO}/data/maps/{nome}/scripts.inc", "a",
                  encoding="utf-8") as f:
            f.write(trecho)

if aliases:
    p = f"{REPO}/include/constants/flags.h"
    s = open(p).read()
    if "FLAG_UNOVA_ARVORE_" not in s:
        alvo = "// Grutas escondidas de Unova"
        bloco = ("// Arvores de fruta e fosseis de Unova "
                 "(dev_scripts/importa_npcs_unova.py).\n"
                 "// Faixa 0x4C3 a 0x4EE, o resto da faixa reservada a essa frente.\n"
                 + "\n".join(aliases) + "\n\n")
        s = s.replace(alvo, bloco + alvo, 1)
        open(p, "w").write(s)

print(f"escrito: {total} NPCs em {len(plano)} mapas, {len(aliases)} flags")
