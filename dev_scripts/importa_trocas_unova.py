#!/usr/bin/env python3
"""Liga as 9 trocas de Pokemon de Unova, com os dados e o texto do BW3G.

Por que este script existe
--------------------------
`importa_npcs_unova.py` recusou de proposito os NPCs de casa de troca: no gen 2
a troca e o comando `trade NPC_TRADE_X`, que le uma TABELA
(`data/events/npc_trades.asm`), e tabela nao e script. Aqui a tabela do BW3G
vira entrada em `sIngameTrades` (`src/data/trade.h`), que e a mesma mecanica de
troca em jogo que este repo ja tem para Hoenn e para Kanto, e o NPC passa a
chamar o roteiro de troca do vanilla (`EventScript_DoInGameTrade` e companhia).

Nada e inventado: especie pedida, especie oferecida, apelido, item segurado,
numero e nome do OT e o texto dos quatro conjuntos de dialogo saem todos da
fonte. As duas unicas conversoes de formato, ambas registradas no relatorio:

1. **DV de gen 2 vira IV de gen 3**, `IV = DV * 2` (0 a 15 vira 0 a 30). O gen 2
   tem UM stat Especial, entao o mesmo DV alimenta SpAtk e SpDef.
2. **Item de gen 2 vira o item de gen 3 de mesmo efeito**: BERRY (cura 10 PS)
   vira ORAN, GOLD_BERRY (30 PS) vira SITRUS, MYSTERYBERRY (PP) vira LEPPA. Os
   outros cinco existem com o mesmo nome nesta build.

O sexo do OT sai do SPRITE do proprio NPC na fonte (`SPRITE_TWIN`,
`SPRITE_POKEFAN_F` e `SPRITE_COOLTRAINER_F` sao mulher; `SPRITE_YOUNGSTER`,
`SPRITE_FISHER` e `SPRITE_BUG_CATCHER` sao homem). O gen 3 exige `otGender` e a
tabela do gen 2 nao tem esse campo, entao o sprite e a evidencia mais proxima
que a fonte da. A primeira versao deste script usava o conjunto de dialogo, e
errava: a dona da casa estranha se chama REGINA, tem `SPRITE_POKEFAN_F` e caia
como homem porque o conjunto dela e o CREEPY, que nao e de mulher.

Custo
-----
9 flags, da faixa desta frente (0x4D2 a 0x4DA), uma por troca, porque o motor
precisa lembrar que aquela troca ja foi feita (e o que o `EVENT_` do gen 2
fazia). **Zero var**, zero objeto novo, zero mapa novo: so o campo `script` de
objeto que ja existe muda, entao indice de save nenhum se mexe.

Uso:
    python3 dev_scripts/importa_trocas_unova.py            # so relata
    python3 dev_scripts/importa_trocas_unova.py --aplica   # escreve
    python3 dev_scripts/importa_trocas_unova.py --demo     # autoteste

Idempotente: pula NPC que ja aponta para o script de troca, e reescreve os
blocos gerados entre marcadores em vez de duplicar.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
os.chdir(REPO)

import importa_unova as iu  # noqa: E402  (reusa BW3G, indice_asm, le_eventos, limpa)

APLICA = "--aplica" in sys.argv
DEMO = "--demo" in sys.argv
BW3G = iu.BW3G

FLAG_BASE = 0x4D2          # faixa exclusiva desta frente: 0x4D2 a 0x4EE
FLAG_TETO = 0x4EE

MARCA_INI = "    // >>> trocas de Unova (dev_scripts/importa_trocas_unova.py) >>>"
MARCA_FIM = "    // <<< trocas de Unova <<<"

# Item de gen 2 -> item desta build, por EFEITO. As tres bagas nao existem aqui
# com o mesmo nome; as outras cinco sim.
ITEM = {
    "BERRY": "ITEM_ORAN_BERRY",            # cura 10 PS
    "GOLD_BERRY": "ITEM_SITRUS_BERRY",     # cura 30 PS
    "MYSTERYBERRY": "ITEM_LEPPA_BERRY",    # devolve PP
}

# Conjunto de dialogo do gen 2 -> indice na tabela TradeTexts. A ordem e a das
# constantes de constants/npc_trade_constants.asm, e o texto 1 ("I collect
# #MON.") confirma que o primeiro e o COLLECTOR.
DIALOGSET = {
    "TRADE_DIALOGSET_COLLECTOR": 1,
    "TRADE_DIALOGSET_HAPPY": 2,
    "TRADE_DIALOGSET_CREEPY": 3,
    "TRADE_DIALOGSET_GIRL": 4,
}

# Sprite do NPC na fonte -> sexo do OT. So os sprites que as nove casas de troca
# usam de verdade; sprite fora desta lista cai em MALE e sai no relatorio.
SEXO_DO_SPRITE = {
    "SPRITE_TWIN": "FEMALE", "SPRITE_POKEFAN_F": "FEMALE",
    "SPRITE_COOLTRAINER_F": "FEMALE", "SPRITE_LASS": "FEMALE",
    "SPRITE_YOUNGSTER": "MALE", "SPRITE_FISHER": "MALE",
    "SPRITE_BUG_CATCHER": "MALE", "SPRITE_COOLTRAINER_M": "MALE",
}
DIALOGOS = ["Intro", "Cancel", "Wrong", "Complete", "After"]


# ------------------------------------------------------------------ a fonte

def le_tabela():
    """As entradas de data/events/npc_trades.asm, na ordem das constantes."""
    asm = open(f"{BW3G}/data/events/npc_trades.asm", encoding="utf-8").read()
    linhas = []
    for ln in asm.splitlines():
        m = re.match(r"\s*npctrade\s+(.+)$", ln)
        if not m or "MACRO" in ln:
            continue
        campos = [c.strip() for c in re.split(r",(?![^\"]*\"\s*,)", m.group(1))]
        if len(campos) != 10:
            campos = [c.strip() for c in m.group(1).split(",")]
        linhas.append(campos)
    nomes = []
    cst = open(f"{BW3G}/constants/npc_trade_constants.asm", encoding="utf-8").read()
    dentro = False
    for ln in cst.splitlines():
        if "NPCTrades indexes" in ln:
            dentro = True
            continue
        if dentro:
            m = re.match(r"\s*const\s+(NPC_TRADE_\w+)", ln)
            if m:
                nomes.append(m.group(1))
            elif "NUM_NPC_TRADES" in ln:
                break
    assert len(nomes) == len(linhas), f"{len(nomes)} constantes, {len(linhas)} linhas"
    return dict(zip(nomes, linhas))


def le_textos_de_troca():
    """(indice do conjunto, dialogo) -> lista de partes ja em formato .string."""
    eng = open(f"{BW3G}/engine/events/npc_trade.asm", encoding="utf-8").read()
    # TradeIntroText1 -> UnknownText_0x...
    ponteiro = {}
    # entre o rotulo e o `text_far` costuma haver uma linha de comentario com a
    # frase inteira; aceitar so a linha seguinte perdia 17 dos 20 textos
    for m in re.finditer(r"^Trade(\w+?)Text(\d):\s*\n(?:\s*;.*\n)*\s*text_far\s+(\w+)",
                         eng, re.M):
        ponteiro[(m.group(1), int(m.group(2)))] = m.group(3)
    corpos = {}
    for f in sorted(os.listdir(f"{BW3G}/data/text")):
        if f.endswith(".asm"):
            corpos.update(le_texto_far(f"{BW3G}/data/text/{f}"))
    saida = {}
    for (dialogo, n), rot in ponteiro.items():
        if rot in corpos:
            saida[(dialogo, n)] = corpos[rot]
    return saida


def le_texto_far(caminho):
    """rotulo -> partes, aceitando text_ram (que o le_textos de importa_unova corta).

    O texto de troca so existe com `text_ram wStringBuffer1`, que e o nome do
    POKéMON pedido, no meio da frase. Cortar ali (o que o leitor generico faz)
    entregaria "Do you have" sem dizer o que. Aqui os dois buffers viram
    {STR_VAR_1} e {STR_VAR_2}, que e exatamente o que GetInGameTradeSpeciesInfo
    escreve em gStringVar1 e gStringVar2 (src/trade.c:4545).
    """
    saida, rotulo, partes = {}, None, None
    for ln in open(caminho, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\n")
        m = re.match(r"^(\w+):+\s*$", ln)
        if m:
            if rotulo and partes:
                saida[rotulo] = partes
            rotulo, partes = m.group(1), None
            continue
        m = re.match(r'^\s*(text|line|next|cont|para)\s+"([^"]*)"', ln)
        if m:
            if partes is None:
                if m.group(1) != "text":
                    rotulo = None
                    continue
                partes = []
            partes.append(iu.JUNTA[m.group(1)] + iu.limpa(m.group(2)))
            continue
        m = re.match(r"^\s*text_ram\s+w(StringBuffer\d|MonOrItemNameBuffer)", ln)
        if m:
            # wStringBuffer1 e wMonOrItemNameBuffer guardam os dois o nome do
            # POKéMON PEDIDO (GetTradeMonNames copia de um para o outro,
            # engine/events/npc_trade.asm:345); wStringBuffer2 e o oferecido
            var = "{STR_VAR_2}" if m.group(1) == "StringBuffer2" else "{STR_VAR_1}"
            if partes is None:
                # ha texto que COMECA pelo nome ("'s cute, but I don't have it")
                partes = [var]
            else:
                partes[-1] += var
            continue
        if re.match(r"^\s*(done|prompt|text_end)\s*$", ln):
            if rotulo and partes:
                saida[rotulo] = partes
            rotulo, partes = None, None
            continue
    if rotulo and partes:
        saida[rotulo] = partes
    return saida


def acha_npcs():
    """NPC_TRADE_X -> (mapa aqui, x, y, texto de 'ainda sem POKéMON' ou None).

    O NPC de Humilau so troca depois que o jogador tem um POKéMON
    (`checkevent EVENT_GOT_A_POKEMON_FROM_ELM`), e diz outro texto antes disso.
    Esse portao vem junto, senao a troca do inicio do jogo fica sem sentido; em
    gen 3 quem guarda o mesmo fato e FLAG_SYS_POKEMON_GET.
    """
    saida = {}
    for f in sorted(os.listdir(f"{BW3G}/maps")):
        if not f.endswith(".asm"):
            continue
        asm = open(f"{BW3G}/maps/{f}", encoding="utf-8", errors="replace").read()
        rotulos = [(mm.start(), mm.group(1)) for mm in re.finditer(r"^(\w+):\s*$", asm, re.M)]
        for i, (pos, rot) in enumerate(rotulos):
            fim = rotulos[i + 1][0] if i + 1 < len(rotulos) else len(asm)
            corpo = asm[pos:fim]
            mt = re.search(r"^\s*trade\s+(NPC_TRADE_\w+)", corpo, re.M)
            if not mt:
                continue
            troca = mt.group(1)
            mo = re.search(rf"^\s*object_event\s+(-?\d+),\s*(-?\d+),\s*(\w+),.*\b{rot}\b",
                           asm, re.M)
            if not mo:
                continue
            sem_pokemon = None
            if "EVENT_GOT_A_POKEMON_FROM_ELM" in corpo:
                mw = re.search(r"^\s*writetext\s+(\w+)", corpo, re.M)
                sem_pokemon = mw.group(1) if mw else None
            mm = re.search(r"^(\w+)_MapEvents:", asm, re.M)
            saida[troca] = (iu.PREFIXO + mm.group(1), int(mo.group(1)),
                            int(mo.group(2)), sem_pokemon, mo.group(3))
    return saida


# ------------------------------------------------------------------ o destino

def ivs_de(dv_ad, dv_ss):
    """DV de gen 2 (dois bytes) -> os seis IV de gen 3, IV = DV * 2."""
    atk, dfn = dv_ad >> 4, dv_ad & 0xF
    spd, spc = dv_ss >> 4, dv_ss & 0xF
    hp = ((atk & 1) << 3) | ((dfn & 1) << 2) | ((spd & 1) << 1) | (spc & 1)
    return [hp * 2, atk * 2, dfn * 2, spd * 2, spc * 2, spc * 2]


def sufixo(nome_troca):
    return nome_troca[len("NPC_TRADE_"):]


def bloco_c(troca, campos, const, sexo):
    _dialog, pedido, oferecido, apelido, dv1, dv2, item, otid, otnome, _g = campos
    ivs = ivs_de(int(dv1.strip("$"), 16), int(dv2.strip("$"), 16))
    item3 = ITEM.get(item, "ITEM_" + item)
    return f"""    [{const}] =
    {{
        .nickname = _("{apelido.strip('"').replace('@', '')}"),
        .species = SPECIES_{oferecido},
        .ivs = {{{', '.join(str(v) for v in ivs)}}},
        .abilityNum = 0,
        .otId = {int(otid)},
        .conditions = {{5, 5, 5, 5, 5}},
        .personality = 0x{int(dv1.strip('$'), 16) << 8 | int(dv2.strip('$'), 16):08x},
        .heldItem = {item3},
        .mailNum = MAIL_NONE,
        .otName = _("{otnome.strip('"').replace('@', '')}"),
        .otGender = {sexo},
        .sheen = 10,
        .requestedSpecies = SPECIES_{pedido}
    }},
"""


def bloco_script(mapa, const, flag, n_set, sem_pokemon=None):
    r = f"{mapa}_EventScript_Troca"
    t = f"Unova_Text_Troca{n_set}"
    portao, extra = "", ""
    if sem_pokemon:
        # o mesmo portao do gen 2 (EVENT_GOT_A_POKEMON_FROM_ELM), com o texto
        # que o importador original ja trouxe para este mapa
        portao = f"\tgoto_if_unset FLAG_SYS_POKEMON_GET, {r}SemPokemon\n"
        extra = (f"\n{r}SemPokemon::\n"
                 f"\tmsgbox {mapa}_Text_{sem_pokemon}\n"
                 f"\trelease\n\tend\n")
    return f"""
@ troca de Pokemon do BW3G, no molde de Route2_House_Frlg (vanilla)
{r}::
	lock
	faceplayer
{portao}	setvar VAR_0x8008, {const}
	call EventScript_GetInGameTradeSpeciesInfo
	goto_if_set {flag}, {r}Feita
	msgbox {t}Intro, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, {r}Nao
	call EventScript_ChooseMonForInGameTrade
	goto_if_ge VAR_0x8004, PARTY_SIZE, {r}Nao
	call EventScript_GetInGameTradeSpecies
	goto_if_ne VAR_RESULT, VAR_0x8009, {r}Errada
	call EventScript_DoInGameTrade
	msgbox {t}Complete
	setflag {flag}
	release
	end

{r}Nao::
	msgbox {t}Cancel
	release
	end

{r}Errada::
	msgbox {t}Wrong
	release
	end

{r}Feita::
	msgbox {t}After
	release
	end
{extra}"""


def emite_texto(rotulo, partes):
    linhas = [f"{rotulo}::"]
    for i, p in enumerate(partes):
        fim = "$" if i == len(partes) - 1 else ""
        linhas.append(f'\t.string "{p}{fim}"')
    return "\n".join(linhas) + "\n"


# ---------------------------------------------------------------- autoteste

def demo():
    """Prova a forma, nao a contagem: cada afirmacao le a fonte de novo."""
    tab = le_tabela()
    assert len(tab) == 9, f"a fonte tem {len(tab)} trocas, esperava 9"
    txt = le_textos_de_troca()
    faltando = [(d, n) for n in (1, 2, 3, 4) for d in DIALOGOS if (d, n) not in txt]
    assert not faltando, f"texto de troca que nao resolveu: {faltando}"
    # o texto de intro TEM que citar os dois nomes, senao o text_ram foi cortado
    for n in (1, 2, 3, 4):
        junto = "".join(txt[("Intro", n)])
        assert "{STR_VAR_1}" in junto and "{STR_VAR_2}" in junto, \
            f"intro {n} sem os dois nomes: {junto!r}"
    # texto que comeca com apostrofo e nome de POKéMON perdido: o conjunto 4
    # abre com `text_ram` antes de qualquer `text`, e a primeira versao deste
    # script cuspia "'s cute, but I don't have it"
    for chave, partes in txt.items():
        assert not partes[0].lstrip("\\nlp").startswith("'"), \
            f"{chave} comeca com apostrofo: perdeu o text_ram da frente"
    # DV -> IV: o teto do gen 2 tem que virar o teto util do gen 3
    assert ivs_de(0xFF, 0xFF) == [30, 30, 30, 30, 30, 30]
    assert ivs_de(0x00, 0x00) == [0, 0, 0, 0, 0, 0]
    npcs = acha_npcs()
    assert len(npcs) == 9, f"{len(npcs)} NPCs de troca achados na fonte, esperava 9"
    for troca in tab:
        assert troca in npcs, f"{troca} nao tem NPC em mapa nenhum"
        sprite = npcs[troca][4]
        assert sprite in SEXO_DO_SPRITE, \
            f"{troca}: sprite {sprite} sem sexo na tabela"
    # a ultima entrada do vanilla fecha sem virgula: emendar sem por uma nao
    # compila, e o `make` deste repo nao roda aqui para acusar
    c = open(f"{REPO}/src/data/trade.h", encoding="utf-8").read()
    i = c.index("static const struct InGameTrade sIngameTrades[] =")
    corpo = c[i:c.index("\n};", i)]
    if MARCA_INI in corpo:
        assert re.search(r"\},\s*\n\s*// >>> trocas de Unova", corpo), \
            "a entrada de Unova entrou colada na anterior, sem virgula"
    # flag: a faixa desta frente tem que caber as 9
    assert FLAG_BASE + len(tab) - 1 <= FLAG_TETO
    print(f"demo OK: {len(tab)} trocas, {len(npcs)} NPCs, 4 conjuntos de dialogo, "
          f"flags {FLAG_BASE:#x} a {FLAG_BASE + len(tab) - 1:#x}")


# ------------------------------------------------------------------ trabalho

def main():
    tab = le_tabela()
    txt = le_textos_de_troca()
    npcs = acha_npcs()

    entradas_c, constantes, flags_novas, por_mapa = [], [], [], {}
    fora = []
    for i, (troca, campos) in enumerate(tab.items()):
        alvo = npcs.get(troca)
        if not alvo:
            fora.append(f"{troca}: nenhum NPC na fonte")
            continue
        mapa, x, y, sem_pokemon, sprite = alvo
        if not os.path.isdir(f"{REPO}/data/maps/{mapa}"):
            fora.append(f"{troca}: {mapa} nao esta na ROM")
            continue
        const = "INGAME_TRADE_UNOVA_" + sufixo(troca)
        flag = "FLAG_UNOVA_TROCA_" + sufixo(troca)
        n_set = DIALOGSET[campos[0]]
        if sprite not in SEXO_DO_SPRITE:
            fora.append(f"{troca}: sprite {sprite} fora da tabela de sexo, "
                        f"o OT vai como MALE")
        sexo = SEXO_DO_SPRITE.get(sprite, "MALE")
        constantes.append(f"    {const},")
        flags_novas.append((flag, FLAG_BASE + len(flags_novas)))
        entradas_c.append(bloco_c(troca, campos, const, sexo))
        por_mapa.setdefault(mapa, []).append((x, y, const, flag, n_set, sem_pokemon))

    if flags_novas and flags_novas[-1][1] > FLAG_TETO:
        sys.exit(f"ERRO: a faixa 0x{FLAG_BASE:X}-0x{FLAG_TETO:X} nao cabe "
                 f"{len(flags_novas)} flags")

    ligados, ja_ligados = 0, 0
    trechos_por_mapa = {}
    for mapa, itens in por_mapa.items():
        cam = f"{REPO}/data/maps/{mapa}/map.json"
        j = json.load(open(cam))
        trechos = []
        for x, y, const, flag, n_set, sem_pokemon in itens:
            alvo = next((o for o in j["object_events"] if o["x"] == x and o["y"] == y), None)
            if alvo is None:
                fora.append(f"{mapa}: nenhum objeto em ({x},{y})")
                continue
            rot = f"{mapa}_EventScript_Troca"
            atual = str(alvo.get("script", "0"))
            if atual == rot:
                ja_ligados += 1
                continue
            # so tomo objeto mudo ou objeto que o proprio importador gerou como
            # NPC de fala (`_EventScript_NpcN`), que e o caso de Humilau: la o
            # texto de "ainda sem POKéMON" tinha virado a fala inteira do NPC
            if atual not in ("0", "", "NULL") and \
                    not re.fullmatch(rf"{mapa}_EventScript_Npc\d+", atual):
                fora.append(f"{mapa} ({x},{y}): o objeto ja fala "
                            f"({atual}), nao vou trocar")
                continue
            alvo["script"] = rot
            trechos.append(bloco_script(mapa, const, flag, n_set, sem_pokemon))
            ligados += 1
        if trechos:
            trechos_por_mapa[mapa] = (cam, j, trechos)

    # os quatro conjuntos de texto sao globais e saem UMA vez, no primeiro mapa
    compartilhado = ""
    if trechos_por_mapa:
        usados = sorted({i[4] for itens in por_mapa.values() for i in itens})
        for n in usados:
            for d in DIALOGOS:
                compartilhado += "\n" + emite_texto(f"Unova_Text_Troca{n}{d}", txt[(d, n)])

    print(f"trocas na fonte: {len(tab)}   NPCs ligados: {ligados}   "
          f"ja ligados: {ja_ligados}")
    print(f"flags: {len(flags_novas)} "
          f"({flags_novas[0][1]:#x} a {flags_novas[-1][1]:#x})" if flags_novas else "flags: 0")
    for f in fora:
        print("   fora:", f)

    if not APLICA:
        print("\n(nada escrito; rode com --aplica)")
        return

    primeiro = True
    for mapa, (cam, j, trechos) in trechos_por_mapa.items():
        with open(cam, "w", encoding="utf-8") as f:
            json.dump(j, f, indent=2, ensure_ascii=False)
            f.write("\n")
        add = "".join(trechos) + (compartilhado if primeiro else "")
        primeiro = False
        with open(f"{REPO}/data/maps/{mapa}/scripts.inc", "a", encoding="utf-8") as f:
            f.write(add)

    # include/constants/trade.h: as constantes entram no FIM do enum, que e o que
    # mantem o indice das trocas que ja existem
    cam = f"{REPO}/include/constants/trade.h"
    h = open(cam, encoding="utf-8").read()
    if MARCA_INI not in h:
        bloco = MARCA_INI + "\n" + "\n".join(constantes) + "\n" + MARCA_FIM + "\n"
        h = re.sub(r"(\n    INGAME_TRADE_SEEL,\n)", r"\1" + bloco, h, count=1)
        open(cam, "w", encoding="utf-8").write(h)

    # src/data/trade.h: as entradas entram no fim de sIngameTrades
    cam = f"{REPO}/src/data/trade.h"
    c = open(cam, encoding="utf-8").read()
    if MARCA_INI not in c:
        i = c.index("static const struct InGameTrade sIngameTrades[] =")
        fim = c.index("\n};", i)
        # a ultima entrada do vanilla fecha com `}` SEM virgula; emendar a
        # primeira de Unova ali sem por a virgula nao compila
        antes = c[:fim].rstrip()
        if antes.endswith("}"):
            antes += ","
        c = antes + "\n" + MARCA_INI + "\n" + "".join(entradas_c) + MARCA_FIM + c[fim:]
        open(cam, "w", encoding="utf-8").write(c)

    # include/constants/flags.h: os apelidos, no fim do bloco de Unova
    cam = f"{REPO}/include/constants/flags.h"
    fl = open(cam, encoding="utf-8").read()
    if "FLAG_UNOVA_TROCA_" not in fl:
        larg = 40
        bloco = ("\n// Trocas de Pokemon de Unova (dev_scripts/importa_trocas_unova.py)\n"
                 + "".join(f"#define {n:<{larg}} FLAG_UNUSED_0x{v:03X}\n"
                           for n, v in flags_novas))
        alvo = "#define FLAG_UNOVA_ARVORE_VILLAGE_BRIDGE         FLAG_UNUSED_0x4D1\n"
        fl = fl.replace(alvo, alvo + bloco, 1)
        open(cam, "w", encoding="utf-8").write(fl)

    print("escrito.")


if __name__ == "__main__":
    if DEMO:
        demo()
    else:
        main()
