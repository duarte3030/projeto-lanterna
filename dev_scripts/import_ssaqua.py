#!/usr/bin/env python3
"""Traz o navio S.S. Aqua do hns para dentro da ROM, com texto, NPC e travessia.

Uso:
    python3 dev_scripts/import_ssaqua.py            # aplica
    python3 dev_scripts/import_ssaqua.py --demo     # so os autotestes

POR QUE ISSO EXISTE
-------------------
Os 11 mapas `SSAqua_*` eram o unico conteudo de Johto de verdade que ainda
faltava (`dev_scripts/completude.py --detalhe Johto`). O `dev_scripts/import_johto.py`
lista `SSAqua_` em `JOHTO_DUNGEONS_PREFIXES`, mas procura o prefixo dentro de
`gMapGroup_Dungeons` do hns, e no hns o navio mora em `gMapGroup_SpecialArea`:
os 11 mapas nunca casaram e cairam calados.

O QUE **NAO** VEM DO HNS, DE PROPOSITO
--------------------------------------
O `SSAqua_1F_EventScript_LeaveBoat` do hns e um monte de 90 `setflag`/`clearflag`
de enredo de Kanto (o "FLAGHEAP"): no hns, desembarcar em Vermilion **e** o
gatilho que liga a segunda metade do jogo. Aqui Kanto e a PRIMEIRA regiao e ja
esta ligada; copiar aquilo zeraria progresso do jogador. Fica so a parte de
navegacao. Idem `IsPokecenterChallengeActivated`, `special` que so existe no hns.

A TRAVESSIA
-----------
Antes: o marinheiro de Olivine dava `warpsilent MAP_VERMILION_CITY` e o de
Vermilion dava `warpsilent MAP_OLIVINE_CITY_PORT_INSIDE`. Um teleporte.

Agora os dois embarcam em `MAP_SSAQUA_1F`, e o marinheiro da porta (29,2)
desembarca no outro lado. Quem manda o sentido e `FLAG_SSAQUA_RUMO_KANTO`, posta
no embarque. A porta (29,1) e `MAP_DYNAMIC`: `setdynamicwarp` no embarque a
aponta para o porto de origem, entao sair pela porta e desistir da viagem, nao
teleportar de graca. Os pontos de desembarque sao **os mesmos** de antes
(MAP_VERMILION_CITY 15,10 e MAP_OLIVINE_CITY_PORT_INSIDE 8,17), para nao
invalidar os roteiros ja provados de T10.3 e da cadeia cronologica.

FAIXAS
------
Flags 0x8E5..0x8E9 (faixa exclusiva desta frente: 0x8E5 a 0x900).
Var: uma so, VAR_SSAQUA_STATE, para o enredo do avo e da neta, que usa
`map_script_2` e `coord_event` (os dois exigem var, flag nao serve).
Treinadores: ids no fim da faixa de Johto (2274..2599), acervo proprio.
"""
import importlib.util
import json
import os
import re
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HNS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns"

MAPAS = ["SSAqua_1F", "SSAqua_B1F", "SSAqua_CaptainsRoom", "SSAqua_PlayersRoom",
         "SSAqua_RoomNW", "SSAqua_RoomNE", "SSAqua_RoomNNE", "SSAqua_RoomSSW",
         "SSAqua_RoomSSE", "SSAqua_RoomSE", "SSAqua_RoomSW"]

GRUPO = "gMapGroup_Dungeons_Johto"   # grupo de Johto que ja existe; entra no FIM

MARCA_PARTY = "=== ACERVO JOHTO S.S. AQUA (import_ssaqua.py) ==="
SENT_INI = "// >>> treinadores do S.S. Aqua (gerado) >>>"
SENT_FIM = "// <<< treinadores do S.S. Aqua (gerado) <<<"

# Faixa de nivel do hns medida por importa_treinadores_johto.py na mesma fonte
# (ele imprime "nivel: origem hns 7..45 -> 45..100"). Cravada aqui de proposito:
# se o S.S. Aqua entrasse na conta com faixa propria, os marinheiros dele
# cairiam num lugar relativo diferente do resto de Johto.
ORIGEM_NIVEL = (7, 45)

FLAGS = {
    "FLAG_HIDE_SSAQUA_1F_GRANDPA": "FLAG_UNUSED_0x8E5",
    "FLAG_HIDE_SSAQUA_SAILOR": "FLAG_UNUSED_0x8E6",
    "FLAG_HIDE_SSAQUA_CAPTAINS_ROOM_GRANDDAUGHTER": "FLAG_UNUSED_0x8E7",
    "FLAG_HIDE_SSAQUA_ROOM_SSE_GRANDDAUGHTER": "FLAG_UNUSED_0x8E8",
    "FLAG_SSAQUA_RUMO_KANTO": "FLAG_UNUSED_0x8E9",
}
VAR_ALIAS = ("VAR_SSAQUA_STATE", "VAR_UNUSED_0x40FF")

# --------------------------------------------------------------------------
# O bloco de navegacao que substitui o FLAGHEAP do hns em SSAqua_1F.
# Os textos citados aqui sao os do hns; so o `Olivine` foi espelhado a partir do
# `Vermilion` que ja vinha pronto, porque a balsa daqui vai nos dois sentidos.
# --------------------------------------------------------------------------
NAVEGACAO_1F = """SSAqua_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SSAqua_1F_OnTransition
	.byte 0

@ Primeira vez a bordo. As quatro flags e o valor 1 sao os mesmos de
@ `OlivinePort_EventScript_Sailor_MaidenVoyage` do hns, e a ordem importa:
@ o avo tem que estar VISIVEL (flag apagada) ja quando o mapa carrega, porque
@ `SSAqua_1F_Trigger_Grandpa` faz `applymovement` nele. Com ele escondido o
@ objeto nao existe, o `waitmovement 0` nunca volta e o jogo trava de pe no
@ corredor. Medido no emulador em 05/08/2026, nao deduzido.
@ Numa save antiga toda flag vale 0, entao a inicializacao tem que ser em jogo,
@ e o VAR_SSAQUA_STATE >= 1 impede que ela repita depois que o enredo andou.
SSAqua_1F_OnTransition::
	goto_if_ge VAR_SSAQUA_STATE, 1, SSAqua_1F_OnTransition_Fim
	clearflag FLAG_HIDE_SSAQUA_1F_GRANDPA
	setflag FLAG_HIDE_SSAQUA_ROOM_SSE_GRANDDAUGHTER
	clearflag FLAG_HIDE_SSAQUA_SAILOR
	clearflag FLAG_HIDE_SSAQUA_CAPTAINS_ROOM_GRANDDAUGHTER
	setvar VAR_SSAQUA_STATE, 1
SSAqua_1F_OnTransition_Fim::
	end

SSAqua_1F_EventScript_DoorSailor::
	lock
	faceplayer
	goto_if_set FLAG_SSAQUA_RUMO_KANTO, SSAqua_1F_EventScript_DoorSailorVermilion
	msgbox SSAqua_1F_Text_SailorDoorArrivedOlivine, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, TRUE, SSAqua_1F_EventScript_LeaveBoatOlivine
	goto SSAqua_1F_EventScript_StayAboard

SSAqua_1F_EventScript_DoorSailorVermilion::
	msgbox SSAqua_1F_Text_SailorDoorArrived, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, TRUE, SSAqua_1F_EventScript_LeaveBoatVermilion
	goto SSAqua_1F_EventScript_StayAboard

SSAqua_1F_EventScript_StayAboard::
	msgbox SSAqua_1F_Text_Sailor1_ToVermilion, MSGBOX_DEFAULT
	closemessage
	release
	end

SSAqua_1F_EventScript_LeaveBoatVermilion::
	closemessage
	warp MAP_VERMILION_CITY, 15, 10
	waitstate
	release
	end

SSAqua_1F_EventScript_LeaveBoatOlivine::
	closemessage
	warp MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	waitstate
	release
	end

SSAqua_1F_Text_SailorDoorArrivedOlivine:
	.string "We have arrived in OLIVINE CITY.\\n"
	.string "Would you like to disembark?$"
"""


def le(p):
    return open(p, encoding="utf-8", errors="replace").read()


def _modulo(nome, arquivo):
    spec = importlib.util.spec_from_file_location(
        nome, os.path.join(RAIZ, "dev_scripts", arquivo))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# 1. limpeza dos scripts do hns
# --------------------------------------------------------------------------

def corta_bloco(texto, rotulo):
    """Remove o bloco `rotulo::` inteiro, ate o proximo rotulo de primeira coluna."""
    m = re.search(rf"^{re.escape(rotulo)}::[^\n]*\n", texto, re.M)
    if not m:
        return texto
    prox = re.search(r"^\w+:{1,2}", texto[m.end():], re.M)
    fim = m.end() + (prox.start() if prox else len(texto) - m.end())
    return texto[:m.start()] + texto[fim:]


def renomeia_treinadores(texto, mapa_nomes):
    """TRAINER_X -> TRAINER_JOHTO_X, e poe a virgula que o hns as vezes omite."""
    for velho, novo in sorted(mapa_nomes.items(), key=lambda kv: -len(kv[0])):
        texto = re.sub(rf"\b{velho}\b", novo, texto)
    return re.sub(r"(trainerbattle_(?:single|double)\s+TRAINER_\w+)\s+(?=\w)",
                  r"\1, ", texto)


# O hns numera os movimentos comuns de um passo (`...WalkDown1`); aqui eles se
# chamam `...WalkDown`. Conferido corpo a corpo: os dois sao `walk_down`+`step_end`.
MOVIMENTO = {
    "Common_Movement_WalkDown1": "Common_Movement_WalkDown",
    "Common_Movement_WalkRight1": "Common_Movement_WalkRight",
    "Common_Movement_WalkLeft1": "Common_Movement_WalkLeft",
    "Common_Movement_WalkUp1": "Common_Movement_WalkUp",
}


def limpa_scripts(mapa, texto, mapa_nomes):
    texto = renomeia_treinadores(texto, mapa_nomes)
    for velho, novo in MOVIMENTO.items():
        texto = re.sub(rf"\b{velho}\b", novo, texto)

    if mapa == "SSAqua_1F":
        # Fora o FLAGHEAP de Kanto, o aviso de chegada por VAR e o menu de porta
        # do hns; entra a navegacao de balsa dos dois sentidos.
        for r in ("SSAqua_1F_MapScripts", "SSAqua_1F_OnFrame",
                  "SSAqua_1F_EventScript_Arrived", "SSAqua_1F_EventScript_DoorSailor",
                  "SSAqua_1F_EventScript_DoorSailorArrived",
                  "SSAqua_1F_EventScript_LeaveBoat"):
            texto = corta_bloco(texto, r)
        texto = NAVEGACAO_1F + "\n" + texto.lstrip("\n")

    if mapa == "SSAqua_PlayersRoom":
        # `IsPokecenterChallengeActivated` nao existe nesta build.
        texto = corta_bloco(texto, "SSAquaRooms_EventScript_Bed")
        texto = corta_bloco(texto, "SSAquaRooms_EventScript_Bed_PokecenterChallenge")
        texto = texto.replace(
            "SSAqua_PlayersRoom_MapScripts::\n\t.byte 0\n",
            "SSAqua_PlayersRoom_MapScripts::\n\t.byte 0\n\n"
            "SSAquaRooms_EventScript_Bed::\n"
            "\tlockall\n"
            "\tmsgbox SSAquaRooms_Text_TakeRestOnBed, MSGBOX_DEFAULT\n"
            "\tclosemessage\n"
            "\tcall Common_EventScript_OutOfCenterPartyHeal\n"
            "\treleaseall\n"
            "\tend\n", 1)
        texto = re.sub(
            r"SSAquaRooms_Text_TakeRestOnBed_PokecenterChallenge:\n(?:\t\.string[^\n]*\n)+",
            "", texto)
    return texto


# --------------------------------------------------------------------------
# 2. treinadores
# --------------------------------------------------------------------------

def treinadores_dos_scripts(textos):
    nomes = set()
    for t in textos.values():
        nomes |= set(re.findall(r"trainerbattle_\w+\s+(TRAINER_\w+)", t))
    return sorted(nomes)


def escreve_treinadores(nomes, it):
    """Gera os blocos .party e os #define. Devolve {nome_nosso: id}."""
    curva = _modulo("curva", "curva_de_nivel.py")
    fonte_times = it.times_do_hns(HNS)
    ctx = {
        "species": it.constantes("include/constants/species.h", "SPECIES_"),
        "moves": it.constantes("include/constants/moves.h", "MOVE_"),
        "itens": it.constantes("include/constants/items.h", "ITEM_"),
        "classes": it.constantes("include/constants/trainers.h", "TRAINER_CLASS_"),
        "pics": it.constantes("include/constants/trainers.h", "TRAINER_PIC_"),
    }
    avisos = []

    def resolve(valor, tabela, existentes, rotulo):
        for tent in (tabela.get(valor), valor, (valor or "") + "_FRLG"):
            if tent and tent in existentes:
                return tent
        avisos.append(f"{rotulo}: {valor} sem equivalente nesta build")
        return None

    party = le(it.PARTY)
    header = le(it.HEADER)
    anterior = party.split(f"/*{MARCA_PARTY}")[0]
    ids_atuais = {n: int(v) for n, v in re.findall(
        r"^#define (TRAINER_[A-Z0-9_]+)\s+(\d+)\s*$", header, re.M)}
    # os nossos do acervo anterior nao contam como colisao numa re-execucao
    ja = set(re.findall(r"^=== (TRAINER_[A-Z0-9_]+) ===", anterior, re.M))

    meu = {n: "TRAINER_JOHTO_" + n[len("TRAINER_"):] for n in nomes}
    colide = [m for m in meu.values() if m in ja]
    if colide:
        sys.exit("ABORTADO: nome ja existe fora deste acervo: " + ", ".join(colide))

    lo, hi = it.FAIXA
    ocupados = {i for n, i in ids_atuais.items() if n in ja}
    livres = [i for i in range(lo, hi + 1) if i not in ocupados]
    if len(meu) > len(livres):
        sys.exit(f"ABORTADO: {len(meu)} treinadores nao cabem em {lo}..{hi}")
    novos = {meu[n]: livres[i] for i, n in enumerate(nomes)}

    linhas = []
    for tr in nomes:
        t = fonte_times.get(tr)
        if not t or not t["mons"]:
            sys.exit(f"ABORTADO: {tr} sem time no hns. Time nao se inventa.")
        classe = resolve(t["class"], it.CLASSE, ctx["classes"], f"classe de {tr}")
        pic = resolve(t["pic"], it.PIC, ctx["pics"], f"pic de {tr}")
        if not pic:
            sys.exit(f"ABORTADO: {tr} sem pic utilizavel")
        L = [f"=== {meu[tr]} ===", f"Name: {t['name'].title()}"]
        if classe:
            L.append(f"Class: {classe}")
        L.append(f"Pic: {pic}")
        itens_ok = [i for i in t["items"] if i != "ITEM_NONE" and i in ctx["itens"]]
        if itens_ok:
            L.append("Items: " + " / ".join(itens_ok))
        L.append("Double Battle: " + ("Yes" if t["double"] else "No"))
        macro = t["macro"] or "NO_ITEM_DEFAULT_MOVES"
        for mon in t["mons"]:
            if mon["species"] not in ctx["species"]:
                avisos.append(f"{tr}: especie {mon['species']} nao existe aqui")
                continue
            cabeca = mon["species"]
            if macro.startswith("ITEM_") and mon["item"] and \
                    mon["item"] != "ITEM_NONE" and mon["item"] in ctx["itens"]:
                cabeca += f" @ {mon['item']}"
            nivel = curva.transforma(int(mon["lvl"] or 5), ORIGEM_NIVEL,
                                     curva.ALVO["Johto"])
            v = min(31, int(mon["iv"] or 0) * 31 // 255)
            L += ["", cabeca, f"Level: {nivel}",
                  f"IVs: {v} HP / {v} Atk / {v} Def / {v} SpA / {v} SpD / {v} Spe"]
            if macro.endswith("CUSTOM_MOVES"):
                for mv in mon["moves"]:
                    mv = it.RENOMEIA_MOVE.get(mv, mv)
                    if mv == "MOVE_NONE":
                        continue
                    if mv not in ctx["moves"]:
                        avisos.append(f"{tr}: golpe {mv} nao existe aqui")
                        continue
                    L.append(f"- {mv}")
        linhas += L + [""]

    antes_n = len(re.findall(r"^=== TRAINER_", party, re.M))
    saida = it.troca_acervo(party, linhas, MARCA_PARTY)
    depois_n = len(re.findall(r"^=== TRAINER_", saida, re.M))
    if depois_n < antes_n:
        sys.exit(f"ABORTADO: trainers.party cairia de {antes_n} para {depois_n}")
    open(it.PARTY, "w", encoding="utf-8").write(saida)

    bloco = "\n".join([SENT_INI]
                      + [f"#define {n:<52} {i}" for n, i in novos.items()]
                      + [SENT_FIM])
    if SENT_INI in header:
        header = re.sub(re.escape(SENT_INI) + r".*?" + re.escape(SENT_FIM),
                        bloco, header, flags=re.S)
    else:
        alvo = "// <<< treinadores de rota de Johto (gerado) <<<"
        header = header.replace(alvo, alvo + "\n\n" + bloco, 1)
    open(it.HEADER, "w", encoding="utf-8").write(header)

    for a in sorted(set(avisos)):
        print("  AVISO:", a)
    return novos, meu


# --------------------------------------------------------------------------
# 3. constantes novas
# --------------------------------------------------------------------------

def apensa(arquivo, sentinela, bloco):
    p = os.path.join(RAIZ, arquivo)
    txt = le(p)
    if sentinela in txt:
        txt = re.sub(re.escape(sentinela) + r".*?" + re.escape(sentinela.replace(">>>", "<<<")),
                     bloco, txt, flags=re.S)
    else:
        txt = txt.rstrip("\n") + "\n\n" + bloco + "\n"
    open(p, "w", encoding="utf-8").write(txt)


def constantes_novas():
    ini = "// >>> S.S. Aqua (dev_scripts/import_ssaqua.py) >>>"
    fim = "// <<< S.S. Aqua (dev_scripts/import_ssaqua.py) <<<"

    flags = le(os.path.join(RAIZ, "include/constants/flags.h"))
    for alvo in FLAGS.values():
        if f"#define {alvo} " not in flags:
            sys.exit(f"ABORTADO: {alvo} nao existe em flags.h")
    apensa("include/constants/flags.h", ini,
           "\n".join([ini] + [f"#define {n:<48} {v}" for n, v in FLAGS.items()] + [fim]))

    nome, alvo = VAR_ALIAS
    # o proprio bloco desta ferramenta sai da conta, senao re-executar aborta
    vars_h = re.sub(re.escape(ini) + r".*?" + re.escape(fim), "",
                    le(os.path.join(RAIZ, "include/constants/vars.h")), flags=re.S)
    usos = re.findall(rf"\b{alvo}\b", vars_h)
    if len(usos) != 1:
        sys.exit(f"ABORTADO: {alvo} ja tem apelido em vars.h ({len(usos)} usos)")
    apensa("include/constants/vars.h", ini,
           "\n".join([ini, f"#define {nome:<48} {alvo}", fim]))

    apensa("include/constants/songs.h", ini,
           "\n".join([ini, "#define MUS_HG_SS_AQUA MUS_ABANDONED_SHIP", fim]))

    # MAPSEC_SS_AQUA nao entra: `include/constants/region_map_sections.h` e
    # GERADO (esta no .gitignore), entao qualquer #define escrito la some no
    # `make clean` seguinte. O navio usa o MAPSEC do porto de onde ele zarpa.


# --------------------------------------------------------------------------

def main():
    it = _modulo("it", "importa_treinadores_johto.py")
    pg = _modulo("pg", "porta_ginasios_johto.py")
    desenhaveis = pg.sprites_desenhaveis()

    # --- ler o hns ---
    scripts = {m: le(f"{HNS}/data/maps/{m}/scripts.inc") for m in MAPAS}
    jsons = {m: json.load(open(f"{HNS}/data/maps/{m}/map.json")) for m in MAPAS}

    nomes_hns = treinadores_dos_scripts(scripts)
    print(f"treinadores citados pelos scripts do navio: {len(nomes_hns)}")
    novos, meu = escreve_treinadores(nomes_hns, it)

    # --- scripts.inc e map.json ---
    for m in MAPAS:
        destino = os.path.join(RAIZ, "data/maps", m)
        os.makedirs(destino, exist_ok=True)
        open(f"{destino}/scripts.inc", "w", encoding="utf-8").write(
            limpa_scripts(m, scripts[m], meu))

        d = jsons[m]
        d["region_map_section"] = "MAPSEC_OLIVINE_CITY"
        for o in d.get("object_events", []):
            gfx = it.SPRITE.get(o["graphics_id"], o["graphics_id"])
            if gfx not in desenhaveis:
                print(f"  AVISO: {m}: sprite {o['graphics_id']} sem grafico, virou MAN_1")
                gfx = "OBJ_EVENT_GFX_MAN_1"
            o["graphics_id"] = gfx
        if m == "SSAqua_1F":
            # a porta do cais volta para o porto de onde o jogador embarcou
            w = d["warp_events"][0]
            assert (w["x"], w["y"]) == (29, 1), w
            w["dest_map"], w["dest_warp_id"] = "MAP_DYNAMIC", "WARP_ID_DYNAMIC"
        json.dump(d, open(f"{destino}/map.json", "w", encoding="utf-8"),
                  indent=2, ensure_ascii=False)

    # --- layouts ---
    hl = {l["id"]: l for l in json.load(
        open(f"{HNS}/data/layouts/layouts.json"))["layouts"]}
    nosso = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
    tem = {l["id"] for l in nosso["layouts"]}
    for m in MAPAS:
        lid = jsons[m]["layout"]
        L = dict(hl[lid])
        for chave in ("border_filepath", "blockdata_filepath"):
            src, dst = f"{HNS}/{L[chave]}", f"{RAIZ}/{L[chave]}"
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
        if lid not in tem:
            nosso["layouts"].append(L)
            tem.add(lid)
    json.dump(nosso, open(f"{RAIZ}/data/layouts/layouts.json", "w",
                          encoding="utf-8"), indent=2)

    # --- map_groups: SEMPRE no fim do grupo, save do Gui em jogo ---
    grupos = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    ja_reg = {x for g in grupos["group_order"] for x in grupos.get(g, [])}
    for m in MAPAS:
        if m not in ja_reg:
            grupos[GRUPO].append(m)
    json.dump(grupos, open(f"{RAIZ}/data/maps/map_groups.json", "w",
                           encoding="utf-8"), indent=2)

    # --- event_scripts.s ---
    p = os.path.join(RAIZ, "data/event_scripts.s")
    txt = le(p)
    faltam = [m for m in MAPAS if f'"data/maps/{m}/scripts.inc"' not in txt]
    if faltam:
        txt = txt.rstrip("\n") + "\n" + "".join(
            f'\t.include "data/maps/{m}/scripts.inc"\n' for m in faltam)
        open(p, "w", encoding="utf-8").write(txt)

    constantes_novas()

    print(f"mapas registrados no fim de {GRUPO}: {len(MAPAS)}")
    print(f"treinadores: {len(novos)}, ids {min(novos.values())}..{max(novos.values())}")
    print("agora rode: python3 dev_scripts/importa_tilesets_johto.py")
    return 0


def demo():
    """Os tres jeitos de este script estragar coisa alheia, virados em teste."""
    # 1. corta_bloco pega o bloco inteiro e para no proximo rotulo, nao no fim.
    t = "A::\n\tx\n\ty\n\nB::\n\tz\n"
    assert corta_bloco(t, "A") == "B::\n\tz\n", repr(corta_bloco(t, "A"))
    assert corta_bloco(t, "C") == t

    # 2. o FLAGHEAP de Kanto some, e o resto do arquivo do hns NAO some junto.
    fonte = le(f"{HNS}/data/maps/SSAqua_1F/scripts.inc")
    saida = limpa_scripts("SSAqua_1F", fonte, {})
    assert "FLAG_HIDE_COPYCAT_CLEFAIRY_DOLL" not in saida
    assert "VAR_KANTO_ROCKET_STORY_STATE" not in saida
    assert "SSAqua_1F_Text_Grandpa:" in saida, "texto do avo foi junto"
    assert "SSAqua_1F_Trigger_Grandpa::" in saida
    assert "FLAG_SSAQUA_RUMO_KANTO" in saida

    # 3. o hns escreve trainerbattle SEM virgula depois do id; o gas daqui quer.
    r = renomeia_treinadores("\ttrainerbattle_single TRAINER_WAI A, B\n",
                             {"TRAINER_WAI": "TRAINER_JOHTO_WAI"})
    assert r == "\ttrainerbattle_single TRAINER_JOHTO_WAI, A, B\n", repr(r)
    r2 = renomeia_treinadores("\ttrainerbattle_single TRAINER_WAI, A, B\n",
                              {"TRAINER_WAI": "TRAINER_JOHTO_WAI"})
    assert r2 == "\ttrainerbattle_single TRAINER_JOHTO_WAI, A, B\n", repr(r2)

    # 4. as flags desta frente sao SO da faixa exclusiva 0x8E5..0x900.
    for alvo in FLAGS.values():
        n = int(alvo.split("_0x")[1], 16)
        assert 0x8E5 <= n <= 0x900, alvo

    # 5. o quarto do jogador nao pode citar special que nao existe aqui.
    quarto = limpa_scripts("SSAqua_PlayersRoom",
                           le(f"{HNS}/data/maps/SSAqua_PlayersRoom/scripts.inc"), {})
    assert "IsPokecenterChallengeActivated" not in quarto
    assert "SSAquaRooms_EventScript_Bed::" in quarto
    assert "SSAquaRooms_Text_TakeRestOnBed:" in quarto
    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
