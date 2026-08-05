#!/usr/bin/env python3
"""Porta os 8 ginásios de Johto do hns para este repo.

Uso:
    python3 dev_scripts/porta_ginasios_johto.py ../fontes-mapas/hns

Reescreve, para cada ginásio, `data/maps/<Mapa>/scripts.inc` e a lista
`object_events` de `data/maps/<Mapa>/map.json`. Não toca em layout, warp,
connections nem em nenhum arquivo compartilhado fora de map_event_ids.h.

O que vem do hns tal e qual: posição, direção, raio de visão, e TODO o texto.
O que é adaptado de propósito:

- Sprite. Líder de Johto não tem gráfico nesta build, e GYM_GUY, ROCKER,
  CHANNELER, COOLTRAINER_M/F, OLD_MAN_1/2 só existem dentro de `#if IS_FRLG`,
  onde o id aponta para o vazio e reinicia a ROM. Cada troca é conferida contra
  object_event_graphics_info_pointers.h FORA do ramo FRLG.
- Enredo do líder. O hns amarra cada líder a `VAR_<CIDADE>_STATE`, a
  `FLAG_BADGE0N_GET` de Hoenn e a `VAR_NUM_BADGES`. Aqui o ginásio é chapado no
  padrão de Sinnoh: fala, batalha, fala, `setflag FLAG_INSIGNIA_JOHTO_N`. Zero
  var gasta, e as insígnias de Hoenn ficam intactas.
- Pokémon de enfeite (`OBJ_EVENT_GFX_MON_BASE+SPECIES_*`) são descartados.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Sprite do hns -> sprite que ESTA build desenha. Conferido contra a tabela de
# ponteiros, fora de `#if IS_FRLG`, pela função valida_sprites() abaixo.
SUBST_SPRITE = {
    "OBJ_EVENT_GFX_FALKNER": "OBJ_EVENT_GFX_WINONA",
    "OBJ_EVENT_GFX_BUGSY": "OBJ_EVENT_GFX_NINJA_BOY",
    "OBJ_EVENT_GFX_WHITNEY": "OBJ_EVENT_GFX_LASS",
    "OBJ_EVENT_GFX_MORTY": "OBJ_EVENT_GFX_PHOEBE",
    "OBJ_EVENT_GFX_JASMINE": "OBJ_EVENT_GFX_ROXANNE",
    "OBJ_EVENT_GFX_CHUCK": "OBJ_EVENT_GFX_BRAWLY",
    "OBJ_EVENT_GFX_PRYCE": "OBJ_EVENT_GFX_GLACIA",
    "OBJ_EVENT_GFX_CLAIR": "OBJ_EVENT_GFX_LIZA",
    "OBJ_EVENT_GFX_GYM_GUY": "OBJ_EVENT_GFX_OLD_MAN",
    "OBJ_EVENT_GFX_ROCKER": "OBJ_EVENT_GFX_CAMPER",
    "OBJ_EVENT_GFX_CHANNELER": "OBJ_EVENT_GFX_HEX_MANIAC",
    "OBJ_EVENT_GFX_SAGE": "OBJ_EVENT_GFX_EXPERT_M",
    "OBJ_EVENT_GFX_COOLTRAINER_M": "OBJ_EVENT_GFX_EXPERT_M",
    "OBJ_EVENT_GFX_COOLTRAINER_F": "OBJ_EVENT_GFX_EXPERT_F",
    "OBJ_EVENT_GFX_OLD_MAN_1": "OBJ_EVENT_GFX_OLD_MAN",
    "OBJ_EVENT_GFX_OLD_MAN_2": "OBJ_EVENT_GFX_MAN_2",
}

# hns -> nosso, igual ao de dev_scripts/import_johto_gym_trainers.py.
TRAINER = {
    "TRAINER_ROD": "TRAINER_JOHTO_BIRD_KEEPER_ROD",
    "TRAINER_ABE": "TRAINER_JOHTO_BIRD_KEEPER_ABE",
    "TRAINER_FALKNER_1": "TRAINER_JOHTO_LEADER_FALKNER",
    "TRAINER_AL": "TRAINER_JOHTO_BUG_CATCHER_AL",
    "TRAINER_JOSH": "TRAINER_JOHTO_BUG_CATCHER_JOSH",
    "TRAINER_BENNY": "TRAINER_JOHTO_BUG_CATCHER_BENNY",
    "TRAINER_AMY_AND_MAY": "TRAINER_JOHTO_TWINS_AMY_AND_MAY",
    "TRAINER_BUGSY_1": "TRAINER_JOHTO_LEADER_BUGSY",
    "TRAINER_CARRIE": "TRAINER_JOHTO_LASS_CARRIE",
    "TRAINER_BRIDGET": "TRAINER_JOHTO_LASS_BRIDGET",
    "TRAINER_VICTORIA": "TRAINER_JOHTO_BEAUTY_VICTORIA",
    "TRAINER_SAMANTHA": "TRAINER_JOHTO_BEAUTY_SAMANTHA",
    "TRAINER_WHITNEY_1": "TRAINER_JOHTO_LEADER_WHITNEY",
    "TRAINER_JEFFREY": "TRAINER_JOHTO_SAGE_JEFFREY",
    "TRAINER_PING": "TRAINER_JOHTO_SAGE_PING",
    "TRAINER_MARTHA": "TRAINER_JOHTO_MEDIUM_MARTHA",
    "TRAINER_GRACE": "TRAINER_JOHTO_MEDIUM_GRACE",
    "TRAINER_MORTY_1": "TRAINER_JOHTO_LEADER_MORTY",
    "TRAINER_JASMINE_1": "TRAINER_JOHTO_LEADER_JASMINE",
    "TRAINER_YOSHI": "TRAINER_JOHTO_BLACK_BELT_YOSHI",
    "TRAINER_LAO": "TRAINER_JOHTO_BLACK_BELT_LAO",
    "TRAINER_NOB": "TRAINER_JOHTO_BLACK_BELT_NOB",
    "TRAINER_LUNG": "TRAINER_JOHTO_BLACK_BELT_LUNG",
    "TRAINER_CHUCK_1": "TRAINER_JOHTO_LEADER_CHUCK",
    "TRAINER_RONALD": "TRAINER_JOHTO_GENTLEMAN_RONALD",
    "TRAINER_BRAD": "TRAINER_JOHTO_SKIER_BRAD",
    "TRAINER_DOUGLAS": "TRAINER_JOHTO_BOARDER_DOUGLAS",
    "TRAINER_ROXANNE": "TRAINER_JOHTO_SKIER_ROXANNE",
    "TRAINER_CLARISSA": "TRAINER_JOHTO_SKIER_CLARISSA",
    "TRAINER_PRYCE_1": "TRAINER_JOHTO_LEADER_PRYCE",
    "TRAINER_CODY": "TRAINER_JOHTO_COOLTRAINER_CODY",
    "TRAINER_FRAN": "TRAINER_JOHTO_COOLTRAINER_FRAN",
    "TRAINER_PAUL": "TRAINER_JOHTO_COOLTRAINER_PAUL",
    "TRAINER_MIKE": "TRAINER_JOHTO_COOLTRAINER_MIKE",
    "TRAINER_LOLA": "TRAINER_JOHTO_COOLTRAINER_LOLA",
    "TRAINER_CLAIR_1": "TRAINER_JOHTO_LEADER_CLAIR",
}

# Um ginásio por entrada. `lider` e `guia` citam rótulos de texto do hns; o resto
# dos treinadores é lido direto do scripts.inc de lá.
GINASIOS = [
    dict(
        mapa="VioletCity_Gym", hns="VioletCity_Gym", flag="FLAG_INSIGNIA_JOHTO_1",
        cidade="VIOLET CITY", curto="VIOLET",
        lider=dict(nome="Falkner", npc="Falkner", trainer="TRAINER_FALKNER_1",
                   intro="VioletGym_Text_Falkner_Intro",
                   derrota="VioletGym_Text_Falkner_WinLoss",
                   insignia="VioletGym_Text_Falkner_BadgeExplain",
                   depois="VioletGym_Text_Falkner_AfterFight"),
        guia=dict(npc="GymGuy", antes="VioletGym_Text_GymGuide_Intro",
                  depois="VioletGym_Text_GymGuide_Win"),
    ),
    dict(
        mapa="AzaleaTown_Gym", hns="AzaleaTown_Gym", flag="FLAG_INSIGNIA_JOHTO_2", teias=True,
        cidade="AZALEA TOWN", curto="AZALEA",
        lider=dict(nome="Bugsy", npc="Bugsy", trainer="TRAINER_BUGSY_1",
                   intro="AzaleaTown_Gym_Text_BugsyIntro",
                   derrota="AzaleaTown_Gym_Text_BugsyBeaten",
                   insignia="AzaleaTown_Gym_Text_HiveBadgeSpeech",
                   depois="AzaleaTown_Gym_Text_BugsyAdvice"),
        guia=dict(npc="GymGuy", antes="AzaleaTown_Gym_Text_GymGuide",
                  depois="AzaleaTown_Gym_Text_GymGuideWin"),
    ),
    dict(
        mapa="GoldenrodCity_Gym", hns="GoldenrodCity_Gym", flag="FLAG_INSIGNIA_JOHTO_3",
        cidade="GOLDENROD CITY", curto="GOLDENROD",
        lider=dict(nome="Whitney", npc="Whitney", trainer="TRAINER_WHITNEY_1",
                   intro="GoldenrodCity_Gym_Text_WhitneyBefore",
                   derrota="GoldenrodCity_Gym_Text_WhitneyShouldntBeSoSerious",
                   insignia="GoldenrodCity_Gym_Text_WhitneyPlainBadge",
                   depois="GoldenrodCity_Gym_Text_WhitneyGoodCry"),
        guia=dict(npc="Gym_Guy", antes="GoldenrodCity_Gym_Text_GymGuide",
                  depois="GoldenrodCity_Gym_Text_GymGuideWin"),
    ),
    dict(
        mapa="EcruteakCity_Gym", hns="EcruteakCity_Gym", flag="FLAG_INSIGNIA_JOHTO_4",
        cidade="ECRUTEAK CITY", curto="ECRUTEAK",
        lider=dict(nome="Morty", npc="Morty", trainer="TRAINER_MORTY_1",
                   intro="MortyIntroText", derrota="MortyWinLossText",
                   insignia="MortyText_FogBadgeSpeech", depois="MortyFightDoneText"),
        guia=dict(npc="GymGuy", antes="EcruteakCity_GymGuideText",
                  depois="EcruteakCity_GymGuideWinText"),
    ),
    dict(
        mapa="OlivineCity_Gym", hns="OlivineCity_Gym", flag="FLAG_INSIGNIA_JOHTO_5",
        cidade="OLIVINE CITY", curto="OLIVINE",
        lider=dict(nome="Jasmine", npc="Jasmine", trainer="TRAINER_JASMINE_1",
                   intro="OlivineCity_Gym_Text_JasmineSteelTypeIntro",
                   derrota="OlivineCity_Gym_Text_JasmineBetterTrainer",
                   insignia="OlivineCity_Gym_Text_JasmineBadgeSpeech",
                   depois="OlivineCity_Gym_Text_JasmineGoodLuck"),
        guia=dict(npc="GymGuide", antes="OlivineCity_Gym_Text_GymGuideText",
                  depois="OlivineCity_Gym_Text_GymGuideWinText"),
        conversa=[dict(npc="Lass", texto="OlivineCity_Gym_Text_Lass"),
                  dict(npc="Gent", texto="OlivineCity_Gym_Text_Gent")],
    ),
    dict(
        mapa="CianwoodGym", hns="CianwoodGym", flag="FLAG_INSIGNIA_JOHTO_6",
        cidade="CIANWOOD CITY", curto="CIANWOOD",
        lider=dict(nome="Chuck", npc="Chuck", trainer="TRAINER_CHUCK_1",
                   intro="CianwoodGym_Text_ChuckIntro1",
                   derrota="CianwoodGym_Text_ChuckIntro2",
                   insignia="CianwoodGym_Text_ChuckBadgeSpeech",
                   depois="CianwoodGym_Text_ChuckAfter"),
    ),
    dict(
        mapa="MahoganyTown_Gym", hns="MahoganyTown_Gym", flag="FLAG_INSIGNIA_JOHTO_7",
        cidade="MAHOGANY TOWN", curto="MAHOGANY",
        lider=dict(nome="Pryce", npc="Pryce", trainer="TRAINER_PRYCE_1",
                   intro="MahoganyTown_Gym_Text_PryceIntro",
                   derrota="MahoganyTown_Gym_Text_PryceImpressed",
                   insignia="MahoganyTown_Gym_Text_GlacierBadgeSpeech",
                   depois="MahoganyTown_Gym_Text_CherishPokemon"),
        guia=dict(npc="GymGuy", antes="MahoganyTown_Gym_Text_Guide",
                  depois="MahoganyTown_Gym_Text_GuideWin"),
    ),
    dict(
        mapa="BlackthornCity_Gym", hns="BlackthornCity_Gym", flag="FLAG_INSIGNIA_JOHTO_8", pontes=True,
        cidade="BLACKTHORN CITY", curto="BLACKTHORN",
        lider=dict(nome="Clair", npc="Clair", trainer="TRAINER_CLAIR_1",
                   intro="BlackthornGym_Text_ClairIntroText",
                   derrota="BlackthornGym_Text_ClairWinText",
                   insignia="BlackthornGym_Text_ClairText_GoToDragonsDen",
                   depois="BlackthornGym_Text_ClairText_League"),
        guia=dict(npc="GymGuy", antes="BlackthornGym_Text_GuideText",
                  depois="BlackthornGym_Text_GuideWinText"),
    ),
]


# ponytail: UMA var, decidida pelo Gui em 05/08/2026, para recuperar o
# quebra-cabeca das pontes de Blackthorn. Registrada em SINNOH-PADRAO.md.
VAR_PONTES = "VAR_BLACKTHORN_GYM_STATE"


def le(caminho):
    return open(caminho, encoding="utf-8", errors="replace").read()


def sprites_desenhaveis():
    """Mesma leitura que valida_mapas_sinnoh.py: só o que fica FORA de IS_FRLG."""
    caminho = os.path.join(
        REPO, "src/data/object_events/object_event_graphics_info_pointers.h")
    fora, profundidade, dentro, nivel = set(), 0, False, 0
    for linha in open(caminho):
        s = linha.strip()
        if s.startswith("#if"):
            profundidade += 1
            if "IS_FRLG" in s and not s.startswith("#if !"):
                dentro, nivel = True, profundidade
        elif s.startswith("#endif"):
            if dentro and profundidade == nivel:
                dentro = False
            profundidade -= 1
        achado = re.search(r"\[(OBJ_EVENT_GFX_[A-Z0-9_]+)\]", s)
        if achado and not dentro:
            fora.add(achado.group(1))
    return fora


def textos_do_hns(fonte):
    """rotulo -> corpo inteiro do bloco `.string`, já com o `$` final."""
    saida = {}
    for m in re.finditer(
        r"^(\w+):\s*\n((?:\s*\.string\s+\"[^\n]*\"\s*\n)+)", fonte, re.M
    ):
        saida[m.group(1)] = m.group(2).rstrip("\n")
    return saida


def treinadores_do_hns(fonte):
    """Lista de dicts: script do hns, treinador, textos de visto/vencido/depois."""
    saida = []
    padrao = re.compile(
        r"^(\w+)::[^\n]*\n"
        r"\s*trainerbattle_(single|double)\s+(TRAINER_\w+),?\s+([\w]+),\s*([\w]+)"
        r"(?:,\s*[\w]+)?[^\n]*\n"
        r"(?:\s*(?!msgbox)[^\n]*\n)*?"     # special, delay e afins do hns: ignorados
        r"\s*msgbox\s+(\w+),",
        re.M,
    )
    for m in padrao.finditer(fonte):
        saida.append(dict(script=m.group(1), tipo=m.group(2), trainer=m.group(3),
                          visto=m.group(4), vencido=m.group(5), depois=m.group(6)))
    return saida


def limpa(txt):
    """Normaliza a indentação (o hns mistura tab e espaço) e o que não existe aqui."""
    linhas = ["\t" + l.strip() for l in txt.split("\n") if l.strip()]
    return "\n".join(linhas).replace("{RIVAL}", "your rival")


# Comandos que sobrevivem ao corte nos gatilhos de teia de Azalea: só o que move
# o JOGADOR. As linhas de Ariados (addobject, applymovement do bicho, flag de
# esconder) caem fora porque o sprite de Pokémon andante não é confiável nesta
# build, e a travessia não depende dele.
OPS_GATILHO = ("lock", "release", "end", "waitmovement", "delay", "playse",
               "turnobject OBJ_EVENT_ID_PLAYER", "applymovement OBJ_EVENT_ID_PLAYER")

MOV_LOCAL = {
    "Common_Movement_JumpUp1": ("JumpUp", ["jump_up"]),
    "Common_Movement_JumpDown1": ("JumpDown", ["jump_down"]),
}


def gatilhos_azalea(fonte, pre, hns_json):
    """Porta as 12 teias de Azalea como movimento forçado do jogador.

    Sem elas o ginásio é intransponível: o layout tem parede inteira em y=38,
    y=28, y=22 e y=12, e no hns quem atravessa o jogador é a cena do Ariados.
    Custo aqui: zero flag e zero var persistente (VAR_TEMP_0 é rascunho).
    """
    linhas, coord, movimentos = [], [], {}
    for c in hns_json.get("coord_events", []):
        nome = c["script"].split("_EventScript_")[-1]
        m = re.search(rf"^{re.escape(c['script'])}::(.*?)\n\tend", fonte, re.S | re.M)
        if not m:
            continue
        corpo = []
        for ln in m.group(1).split("\n"):
            t = ln.strip()
            if not t or t.startswith("@"):
                continue
            if not any(t.startswith(op) for op in OPS_GATILHO):
                continue
            achado = re.search(r"applymovement OBJ_EVENT_ID_PLAYER, (\w+)", t)
            if achado:
                rot = achado.group(1)
                if rot in MOV_LOCAL:
                    novo = f"{pre}_Movement_{MOV_LOCAL[rot][0]}"
                    movimentos[novo] = MOV_LOCAL[rot][1]
                else:
                    novo = pre + "_Movement_" + rot.split("_Movement_")[-1]
                    passos = re.search(rf"^{re.escape(rot)}:\n((?:\t\w+\n)+)", fonte, re.S | re.M)
                    movimentos[novo] = [p.strip() for p in passos.group(1).split("\n")
                                        if p.strip() and p.strip() != "step_end"]
                t = t.replace(rot, novo)
            corpo.append("\t" + t)
        linhas.append(f"{pre}_EventScript_{nome}::")
        linhas += corpo
        linhas.append("\tend")
        linhas.append("")
        coord.append({"type": "trigger", "x": c["x"], "y": c["y"],
                      "elevation": c.get("elevation", 0), "var": "VAR_TEMP_0",
                      "var_value": "0", "script": f"{pre}_EventScript_{nome}"})
    for nome, passos in movimentos.items():
        linhas.append(f"{nome}:")
        linhas += ["\t" + p for p in passos]
        linhas.append("\tstep_end")
        linhas.append("")
    return linhas, coord


def pontes_blackthorn(fonte, pre, piso, hns_json):
    """Reconstrói o quebra-cabeça das quatro pontes de Blackthorn.

    ponytail: a primeira versão acendia as quatro pontes de uma vez no ON_LOAD,
    para não gastar var. O Gui decidiu em 05/08/2026 gastar UMA var e recuperar
    o quebra-cabeça original, então aqui a estrutura é a mesma do hns: quatro
    estados cumulativos em VAR_BLACKTHORN_GYM_STATE, cada gatilho acende a ponte
    seguinte, e o ON_LOAD reconstrói o que já foi aceso quando o jogador volta ao
    mapa.

    O id de metatile do hns (0x35A) NÃO serve: o tileset foi trocado no import,
    então usa-se o piso andável mais comum DESTE layout. Consequência conhecida e
    aceita: a ponte funciona mas tem cara de chão comum, e só melhora com trabalho
    de tileset, que é outra tarefa.
    """
    # Cada BuildBridgeN do hns vira um bloco próprio, preservando o agrupamento:
    # sem isso as quatro pontes voltariam a acender juntas.
    blocos = {}
    for m in re.finditer(
            r"^(\w*BuildBridge(\d)\w*)::\n((?:\ttry\w+.*\n|\tsetmetatile .*\n)+)",
            fonte, re.M):
        n = int(m.group(2))
        blocos[n] = [
            f"\tsetmetatile {a}, {b}, {piso}, {c}"
            for a, b, c in re.findall(r"setmetatile (\d+), (\d+), 0x[0-9A-Fa-f]+, (\w+)",
                                      m.group(3))
        ]
    if not blocos:  # o hns mudou de forma: cai no comportamento antigo, tudo de uma vez
        linhas = [f"{pre}_EventScript_Pontes::"]
        for m in re.finditer(r"setmetatile (\d+), (\d+), 0x[0-9A-Fa-f]+, (\w+)", fonte):
            linhas.append(f"\tsetmetatile {m.group(1)}, {m.group(2)}, {piso}, {m.group(3)}")
        return linhas + ["\tend", ""], []

    ordem = sorted(blocos)
    linhas = []
    # ON_LOAD: reconstrói cumulativamente o estado já alcançado
    linhas.append(f"{pre}_EventScript_Pontes::")
    for n in ordem:
        linhas.append(f"\tcall_if_ge {VAR_PONTES}, {n}, {pre}_EventScript_Ponte{n}")
    linhas += ["\tend", ""]
    for n in ordem:
        linhas.append(f"{pre}_EventScript_Ponte{n}::")
        linhas += blocos[n]
        linhas += ["\treturn", ""]
    # gatilhos: acende a ponte, redesenha e avança o estado
    for n in ordem:
        linhas.append(f"{pre}_EventScript_AcendePonte{n}::")
        linhas += [f"\tcall {pre}_EventScript_Ponte{n}",
                   "\tspecial DrawWholeMapView",
                   f"\tsetvar {VAR_PONTES}, {n}",
                   "\tend", ""]
    # coord_events vindos do hns, remapeados para os rótulos locais
    coord = []
    for c in hns_json.get("coord_events", []):
        achado = re.search(r"Bridge(\d)", c.get("script", ""))
        if not achado:
            continue
        n = int(achado.group(1))
        coord.append({"type": "trigger", "x": c["x"], "y": c["y"],
                      "elevation": c.get("elevation", 0), "var": VAR_PONTES,
                      "var_value": str(n - 1),
                      "script": f"{pre}_EventScript_AcendePonte{n}"})
    return linhas, coord


def piso_mais_comum(layout_id):
    import struct
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    L = layouts[layout_id]
    b = open(os.path.join(REPO, L["blockdata_filepath"]), "rb").read()
    contagem = {}
    for i in range(L["width"] * L["height"]):
        v = struct.unpack("<H", b[i * 2:i * 2 + 2])[0]
        if (v >> 10) & 3 == 0:
            contagem[v & 0x3FF] = contagem.get(v & 0x3FF, 0) + 1
    return max(contagem, key=contagem.get)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    hns_raiz = os.path.abspath(sys.argv[1])
    desenhaveis = sprites_desenhaveis()

    ruins = sorted(v for v in SUBST_SPRITE.values() if v not in desenhaveis)
    if ruins:
        sys.exit("ABORTADO: SUBST_SPRITE aponta para sprite sem gráfico: " + ", ".join(ruins))

    localids = []
    resumo = []

    for g in GINASIOS:
        mapa, pre = g["mapa"], g["mapa"]
        hns_dir = os.path.join(hns_raiz, "data/maps", g["hns"])
        fonte = le(os.path.join(hns_dir, "scripts.inc"))
        textos = textos_do_hns(fonte)
        hns_json = json.load(open(os.path.join(hns_dir, "map.json")))

        batalhas = {t["script"]: t for t in treinadores_do_hns(fonte)}
        usados = {}          # rotulo nosso -> corpo do texto
        linhas = []
        objetos = []
        prefixo_local = "LOCALID_" + re.sub(r"(?<!^)(?=[A-Z])", "_", mapa).upper()
        prefixo_local = prefixo_local.replace("__", "_")
        locais = []

        def texto(rotulo_hns, nome_nosso, fallback):
            """Registra um texto do hns sob nome nosso. Sem o texto, usa fallback."""
            corpo = textos.get(rotulo_hns)
            rotulo = f"{pre}_Text_{nome_nosso}"
            if corpo is None:
                corpo = '\t.string "' + fallback + '$"'
                resumo.append(f"{mapa}: texto {rotulo_hns} nao achado, usando fallback")
            usados[rotulo] = limpa(corpo)
            return rotulo

        # --- objetos, na ordem do hns ---
        for obj in hns_json["object_events"]:
            gfx = obj["graphics_id"]
            if "MON_BASE" in gfx:
                continue  # enfeite: descartado de propósito
            script = obj.get("script")
            gfx = SUBST_SPRITE.get(gfx, gfx)
            if gfx not in desenhaveis:
                resumo.append(f"{mapa}: sprite {obj['graphics_id']} sem gráfico, virou MAN_1")
                gfx = "OBJ_EVENT_GFX_MAN_1"

            if script in (None, "NULL", "0"):
                continue
            if script in ("EventScript_StrengthBoulder", "EventScript_RockSmash") \
                    and g["mapa"] == "CianwoodGym":
                # ponytail: as pedras de Cianwood foram REMOVIDAS por decisao do
                # Gui em 05/08/2026. Fieis ao HGSS, elas prendem para sempre quem
                # chegar sem Strength, e em Johto o Strength vem do proprio Chuck,
                # que fica atras delas. Softlock nao e fidelidade.
                continue
            if script in ("EventScript_StrengthBoulder", "EventScript_RockSmash"):
                # pedra do ginásio de Cianwood: script global, já existe em
                # data/scripts/field_move_scripts.inc
                novo_script = script
                nome = "Boulder" if "Strength" in script else "Rock"
            else:
                nome = re.sub(r".*EventScript_", "", script)
                novo_script = f"{pre}_EventScript_{nome}"

            local = f"{prefixo_local}_{re.sub(r'(?<!^)(?=[A-Z])', '_', nome).upper()}"
            local = re.sub(r"_+", "_", local)
            if local in [l[0] for l in locais]:
                n = 2
                while f"{local}_{n}" in [l[0] for l in locais]:
                    n += 1
                local = f"{local}_{n}"
            locais.append((local, len(locais) + 1))

            objetos.append({
                "local_id": local,
                "graphics_id": gfx,
                "x": obj["x"], "y": obj["y"],
                "elevation": obj.get("elevation", 0),
                "movement_type": obj.get("movement_type", "MOVEMENT_TYPE_FACE_DOWN"),
                "movement_range_x": obj.get("movement_range_x", 0),
                "movement_range_y": obj.get("movement_range_y", 0),
                "trainer_type": obj.get("trainer_type", "TRAINER_TYPE_NONE"),
                "trainer_sight_or_berry_tree_id": obj.get("trainer_sight_or_berry_tree_id", "0"),
                "script": novo_script,
                "flag": "0",
            })

        localids.append((mapa, [o["local_id"] for o in objetos]))

        # --- cabeçalho ---
        linhas.append(f"@ Ginasio de {g['cidade']}, portado de fontes-mapas/hns por")
        linhas.append("@ dev_scripts/porta_ginasios_johto.py. Nao editar a mao: rode o script.")
        linhas.append("@ ponytail: o enredo de var do hns foi cortado. Aqui o ginasio e fala,")
        linhas.append(f"@ batalha, fala e {g['flag']}. Zero var gasta.")
        linhas.append("")
        linhas.append(f"{pre}_MapScripts::")
        if g.get("pontes"):
            linhas.append(f"\tmap_script MAP_SCRIPT_ON_LOAD, {pre}_EventScript_Pontes")
        linhas.append("\t.byte 0")
        linhas.append("")

        coord_events = []
        if g.get("pontes"):
            extra, coord_events = pontes_blackthorn(
                fonte, pre,
                piso_mais_comum(json.load(open(
                    os.path.join(REPO, "data/maps", mapa, "map.json")))["layout"]),
                hns_json)
            linhas += extra
        if g.get("teias"):
            extra, coord_events = gatilhos_azalea(fonte, pre, hns_json)
            linhas += extra

        # --- treinadores comuns ---
        n_portados = 0
        for obj in objetos:
            nome = obj["script"].split("_EventScript_")[-1]
            hns_script = next((s for s in batalhas
                               if s.endswith("_EventScript_" + nome)), None)
            if not hns_script:
                continue
            b = batalhas[hns_script]
            novo_tr = TRAINER.get(b["trainer"])
            if not novo_tr:
                resumo.append(f"{mapa}: treinador {b['trainer']} sem constante nossa")
                continue
            t_visto = texto(b["visto"], nome + "Seen", "Let's battle!")
            t_vencido = texto(b["vencido"], nome + "Beaten", "I lost!")
            t_depois = texto(b["depois"], nome + "After", "Good battle.")
            linhas.append(f"{obj['script']}::")
            if b["tipo"] == "double":
                t_poucos = f"{pre}_Text_{nome}NotEnoughMons"
                usados[t_poucos] = ('\t.string "You need two POKéMON to battle\\n"\n'
                                    '\t.string "the two of us!$"')
                linhas.append(
                    f"\ttrainerbattle_double {novo_tr}, {t_visto}, {t_vencido}, {t_poucos}")
            else:
                linhas.append(f"\ttrainerbattle_single {novo_tr}, {t_visto}, {t_vencido}")
            linhas.append(f"\tmsgbox {t_depois}, MSGBOX_AUTOCLOSE")
            linhas.append("\tend")
            linhas.append("")
            n_portados += 1

        # --- líder ---
        L = g["lider"]
        obj_lider = next((o for o in objetos
                          if o["script"].endswith("_EventScript_" + L["npc"])), None)
        if obj_lider is None:
            sys.exit(f"{mapa}: nao achei o objeto do lider {L['npc']}")
        novo_tr = TRAINER[L["trainer"]]
        t_intro = texto(L["intro"], L["nome"] + "Intro", "I am the GYM LEADER!")
        t_derrota = texto(L["derrota"], L["nome"] + "Defeat", "You are strong.")
        t_insignia = texto(L["insignia"], L["nome"] + "Badge", "Take this BADGE.")
        t_depois = texto(L["depois"], L["nome"] + "Post", "Come back anytime.")
        linhas += [
            f"{obj_lider['script']}::",
            "\tlock",
            "\tfaceplayer",
            f"\tgoto_if_set {g['flag']}, {pre}_EventScript_{L['nome']}Derrotado",
            f"\tmsgbox {t_intro}, MSGBOX_DEFAULT",
            f"\ttrainerbattle_no_intro {novo_tr}, {t_derrota}",
            "\tcall Common_EventScript_PlayGymBadgeFanfare",
            f"\tmsgbox {t_insignia}, MSGBOX_DEFAULT",
            f"\tsetflag {g['flag']}",
            "\tclosemessage",
            "\trelease",
            "\tend",
            "",
            f"{pre}_EventScript_{L['nome']}Derrotado::",
            f"\tmsgbox {t_depois}, MSGBOX_DEFAULT",
            "\tclosemessage",
            "\trelease",
            "\tend",
            "",
        ]

        # --- guia e conversa solta ---
        if g.get("guia"):
            G = g["guia"]
            obj_guia = next((o for o in objetos
                             if o["script"].endswith("_EventScript_" + G["npc"])), None)
            if obj_guia:
                t_a = texto(G["antes"], "GuideBefore", "The LEADER is tough!")
                t_d = texto(G["depois"], "GuideAfter", "Nice battle!")
                linhas += [
                    f"{obj_guia['script']}::",
                    "\tlock",
                    "\tfaceplayer",
                    f"\tgoto_if_set {g['flag']}, {pre}_EventScript_GuideAfter",
                    f"\tmsgbox {t_a}, MSGBOX_DEFAULT",
                    "\trelease",
                    "\tend",
                    "",
                    f"{pre}_EventScript_GuideAfter::",
                    f"\tmsgbox {t_d}, MSGBOX_DEFAULT",
                    "\trelease",
                    "\tend",
                    "",
                ]

        for c in g.get("conversa", []):
            obj_c = next((o for o in objetos
                          if o["script"].endswith("_EventScript_" + c["npc"])), None)
            if obj_c:
                t = texto(c["texto"], c["npc"], "Hello!")
                linhas += [f"{obj_c['script']}::", f"\tmsgbox {t}, MSGBOX_NPC", "\tend", ""]

        # --- placas ---
        bg = []
        for b in hns_json.get("bg_events", []):
            bg.append({
                "type": "sign", "x": b["x"], "y": b["y"], "elevation": b.get("elevation", 0),
                "player_facing_dir": b.get("player_facing_dir", "BG_EVENT_PLAYER_FACING_ANY"),
                "script": f"{pre}_EventScript_Statue",
            })
        if bg:
            usados[f"{pre}_Text_Statue"] = (
                f'\t.string "{g["cidade"]} POKéMON GYM\\n"\n'
                f'\t.string "Leader: {g["lider"]["nome"].upper()}$"')
            usados[f"{pre}_Text_StatueCertified"] = (
                f'\t.string "{g["cidade"]} POKéMON GYM\\p"\n'
                f'\t.string "{g["lider"]["nome"].upper()}\'S CERTIFIED TRAINERS:\\n"\n'
                '\t.string "{PLAYER}$"')
            linhas += [
                f"{pre}_EventScript_Statue::",
                f"\tgoto_if_set {g['flag']}, {pre}_EventScript_StatueCertified",
                f"\tmsgbox {pre}_Text_Statue, MSGBOX_SIGN",
                "\tend",
                "",
                f"{pre}_EventScript_StatueCertified::",
                f"\tmsgbox {pre}_Text_StatueCertified, MSGBOX_SIGN",
                "\tend",
                "",
            ]

        # --- textos ---
        for rotulo, corpo in usados.items():
            linhas.append(f"{rotulo}:")
            linhas.append(corpo)
            linhas.append("")

        destino = os.path.join(REPO, "data/maps", mapa)
        open(os.path.join(destino, "scripts.inc"), "w", encoding="utf-8").write(
            "\n".join(linhas).rstrip("\n") + "\n")

        caminho_json = os.path.join(destino, "map.json")
        d = json.load(open(caminho_json))
        d["object_events"] = objetos
        d["bg_events"] = bg
        d["coord_events"] = coord_events
        json.dump(d, open(caminho_json, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

        resumo.append(f"{mapa}: {len(objetos)} objetos, {n_portados} treinadores + 1 lider")

    # --- LOCALIDs ---
    bloco = ["", "// ponytail: ginasios de Johto, gerados por dev_scripts/porta_ginasios_johto.py"]
    for mapa, ids in localids:
        bloco.append("")
        bloco.append(f"// MAP_{re.sub(r'(?<!^)(?=[A-Z])', '_', mapa).upper().replace('__', '_')}")
        for i, nome in enumerate(ids, 1):
            bloco.append(f"#define {nome} {i}")
    marca = "// ponytail: ginasios de Johto"
    caminho = os.path.join(REPO, "include/constants/map_event_ids.h")
    texto_h = le(caminho)
    if marca in texto_h:
        texto_h = texto_h[:texto_h.index(marca)].rstrip("\n") + "\n"
        texto_h += "\n#endif // GUARD_CONSTANTS_MAP_EVENT_IDS_H\n"
    texto_h = texto_h.replace(
        "#endif // GUARD_CONSTANTS_MAP_EVENT_IDS_H",
        "\n".join(bloco).strip("\n") + "\n\n#endif // GUARD_CONSTANTS_MAP_EVENT_IDS_H")
    open(caminho, "w", encoding="utf-8").write(texto_h)

    for r in resumo:
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
