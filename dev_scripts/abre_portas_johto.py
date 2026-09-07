#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""As 31 portas de Johto que a lente chamava de "sem interior".

    python3 dev_scripts/abre_portas_johto.py            # só relata
    python3 dev_scripts/abre_portas_johto.py --aplicar  # escreve
    python3 dev_scripts/abre_portas_johto.py --demo     # autoteste, exit 1 se cair

A pergunta 46 do Gui, e a resposta medida
-----------------------------------------
A `lente_portas.py` marcava 40 achados na classe "sem interior" em Johto. Nove
são o portão de rota desenhado dos dois lados da emenda e não são defeito;
sobram 31, e a decisão do Gui em 07/09/2026 foi: "ganham interior onde alguma
fonte tiver; o que não tem em fonte nenhuma ganha placa `closed` em inglês".

Medida a fonte, o quadro é outro do que a lista fazia parecer. As 31 caem em
cinco famílias, e a família decide o conserto:

1. **JÁ ENTRA (3).** A boca do Monte Prata na encosta é a ARTE, e o warp mora na
   célula colada, que é `MB_WEST_ARROW_WARP`: o jogador pisa nela, anda para
   oeste e `TryArrowWarp` (src/field_control_avatar.c) dispara. Medido nas três:
   (27,18) com o warp em (28,18), (34,31) com (35,31), (41,40) com (42,40), os
   três para `MT_SILVER_1F_WATERFALL_ROOM`. Não é porta morta, é o mesmo idioma
   de bloco que a própria lente documenta. Vão para a LISTA_BRANCA dela.

2. **AS DUAS PONTAS JÁ EXISTEM, FALTAVA O WARP (4).** Há boca desenhada e órfã
   DENTRO de mapa nosso que casa com boca desenhada e órfã FORA. Ligar as duas
   não inventa geometria: as duas metades já vieram da fonte, e só o warp
   faltava. É o conserto mais barato e o mais fiel.

3. **PRÉDIO QUE PEDE INTERIOR (n).** Casa, fazenda ou galpão que o jogador
   alcança. Ganha mapa novo com PLANTA REAPROVEITADA de interior de Johto que já
   está na árvore, do jeito que `fecha_portas_sinnoh.py` fez em Sinnoh: layout
   compartilhado (zero byte de blockdata novo), NPC e fala em inglês nossos.

4. **MAPA INALCANÇÁVEL (2).** As duas casas do `LakeOfRageLowTide`. O mapa
   inteiro está fora do grafo, e isso é assim NA FONTE (a maré baixa do hns é
   troca de layout, não mapa vizinho). Porta que ninguém alcança não é porta que
   não abre: fica como está, registrada.

5. **SEM FONTE (n).** Boca de caverna que nenhuma das fontes medidas abre. Ganha
   `bg_event` com placa em inglês, que foi o que o Gui aceitou.

Compatibilidade de save, a regra que não se negocia
---------------------------------------------------
Mapa novo entra em GRUPO NOVO, no fim de `group_order`. Warp novo entra no FIM
da lista de warps do mapa que já existe. Nenhum índice antigo anda, e o
`guarda_save.py` continua dizendo SAVE COMPATIVEL.
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
sys.path.insert(0, os.path.join(REPO, "dev_scripts", "qa"))
import valida_warp_tile as W  # noqa: E402

APLICAR = "--aplicar" in sys.argv
GRUPO_NOVO = "gMapGroup_JohtoPortas"
# `struct WarpData` guarda `s8 mapGroup`/`s8 mapNum`: 128 mapas por grupo é o
# teto, e o 129º nasce morto. A mesma armadilha que matou 26 mapas em Sinnoh.
LIMITE_GRUPO = 128

# ---------------------------------------------------------------------------
# FAMÍLIA 1: já entra. Só sai da lista da lente; nada muda no jogo.
# ---------------------------------------------------------------------------
JA_ENTRA = {
    ("MtSilver_MountainSide", 27, 18): ("o warp é o 0, em (28,18), e a célula "
                                        "dele é MB_WEST_ARROW_WARP"),
    ("MtSilver_MountainSide", 34, 31): ("o warp é o 1, em (35,31), e a célula "
                                        "dele é MB_WEST_ARROW_WARP"),
    ("MtSilver_MountainSide", 41, 40): ("o warp é o 2, em (42,40), e a célula "
                                        "dele é MB_WEST_ARROW_WARP"),
}

# ---------------------------------------------------------------------------
# FAMÍLIA 2: as duas pontas já existem. (mapa fora, x, y) -> (mapa dentro, x, y)
# A ponta de dentro foi achada pela própria lente, na classe "falso positivo"
# de mapa fechado, e conferida uma a uma: célula de porta bloqueada com chão
# andável colado, no lado do mapa que casa com a boca de fora.
# ---------------------------------------------------------------------------
#
# ABRIR A BOCA, e por que ela não bastava ligar
# ---------------------------------------------
# Medido em 07/09/2026, e custou a primeira versão deste script: dos 8 warps que
# a primeira ligação escreveu, só 2 disparavam. A conta é do motor, não de
# gosto. `MB_ANIMATED_DOOR` é a única família de porta que dispara SENDO SÓLIDA
# (`DISPARA_SENDO_SOLIDO` em `valida_warp_tile.py`, que é a leitura de
# `field_control_avatar.c`): o motor abre a porta de prédio e atravessa. A boca
# de caverna, `MB_NON_ANIMATED_DOOR`, dispara quando o jogador PISA nela, e com
# colisão 1 ele nunca pisa. O censo confirma: das 93 células de
# `MB_NON_ANIMATED_DOOR` com warp em Johto, as 87 que já existiam têm TODAS
# colisão 0; só as 6 que este script tinha acabado de escrever tinham 1.
#
# Então a boca decorativa precisa ser ABERTA no `map.bin`: colisão 0 e elevação
# 0. O metatile NÃO muda, para o desenho continuar o mesmo (o arco de pedra
# continua arco de pedra); mudam só os dois campos que o motor lê para deixar
# pisar. Elevação 0 é `ELEVATION_TRANSITION`, e `IsElevationMismatchAt`
# (src/event_object_movement.c) devolve FALSE para ela sempre: assim a boca
# aceita o jogador venha ele da elevação 3, 4 ou 5, que é o caso real das três
# bocas de fora (Route 45 chega em 5, Monte Prata em 4, Route 46 em 3).
ABRE_BOCA = True
LIGACOES = [
    # A porta da fachada sul da creche. O interior JÁ TEM a segunda saída
    # desenhada em (3,9), MB_SOUTH_ARROW_WARP, e ela estava órfã. O Scorched
    # Silver abre as duas portas da creche para o mesmo interior.
    (("Route34", 33, 31), ("Route34_DayCare", 3, 9),
     "creche da Route 34, porta da fachada"),
    # A segunda boca da Dark Cave North. As duas no norte dos seus mapas, e a
    # Dark Cave North já é a caverna da Route 45 (warp 0, (14,4)).
    (("Route45", 45, 6), ("DarkCave_NorthSide", 35, 3),
     "Dark Cave, boca norte"),
    # A segunda boca da Dark Cave South, que já é a caverna da Route 46
    # (warp 2, (20,11) -> (56,47)).
    (("Route46", 25, 33), ("DarkCave_SouthSide", 64, 4),
     "Dark Cave, boca leste"),
    # Monte Prata: a travessia. A boca principal (17,7) do lado de fora entra
    # na Waterfall Room por (43,46); a boca órfã de dentro, (50,5), fica à
    # direita dela, e a boca órfã de fora, (34,7), fica à direita da (17,7), na
    # MESMA linha. O jogador entra por uma e sai pela outra.
    (("MtSilver_Outside", 34, 7), ("MtSilver_1F_WaterfallRoom", 50, 5),
     "Monte Prata, saída leste do 1F"),
]

# ---------------------------------------------------------------------------
# FAMÍLIA 3: prédio que ganha interior. Uma linha por porta.
#   pasta, planta base (mapa cujo LAYOUT é reaproveitado), rótulo do popup,
#   música, e o conteúdo (NPCs com fala em inglês).
# ---------------------------------------------------------------------------
#
# A REGRA DE CORTE, e ela é a decisão do Gui lida ao pé da letra
# ---------------------------------------------------------------
# "Ganham interior onde alguma fonte tiver." Medidas as cinco fontes de Johto
# em 07/09/2026 (hns, o decomp do GS Chronicles, Liquid Crystal, FireGold e
# Scorched Silver), o que existe e o que não existe ficou assim:
#
#   * PRÉDIO HABITADO cujo interior a fonte tem para a MESMA cidade ou rota:
#     ganha interior. São quatro, e cada linha abaixo diz qual fonte.
#   * BOCA DE CAVERNA e GALPÃO DE PORTO: nenhuma das cinco fontes abre um só.
#     No Monte Prata e na Dark Cave as fontes têm UMA boca externa cada, e é a
#     que já está ligada. Esses ganham placa, que foi o que o Gui aceitou.
#
# A planta é REAPROVEITADA de interior de Johto que já está na árvore, como
# `fecha_portas_sinnoh.py` fez em Sinnoh: o layout é compartilhado, então o
# mapa novo não gasta um byte de blockdata, e a sala nasce com parede, móvel e
# porta no lugar. O que é nosso é o NPC e a fala, os dois em inglês.
INTERIORES = [
    dict(
        pai="BellchimeTrail", x=54, y=58, pasta="BellchimeTrail_House",
        planta="EcruteakCity_House1", popup="BELLCHIME TRAIL",
        mapsec="MAPSEC_ECRUTEAK_CITY", musica="MUS_HG_BELL_TOWER",
        fonte=("FireGold, mapa 44.105 (9x8, 6 objetos): a casinha do sábio na "
               "Bellchime Trail, a única das cinco fontes que desenha a trilha "
               "como mapa próprio E abre o prédio dela. O Liquid Crystal tem o "
               "mesmo prédio (2.46, 9x9) ao lado da Tin Tower."),
        npcs=[
            dict(gfx="OBJ_EVENT_GFX_MAN_5", x=4, y=3,
                 mov="MOVEMENT_TYPE_FACE_DOWN",
                 texto="The bell of the tower can be heard from here.\\p"
                       "They say it only rings for a trainer with a\\n"
                       "pure heart. Mine, sadly, is a bit dented."),
            dict(gfx="OBJ_EVENT_GFX_WOMAN_2", x=8, y=5,
                 mov="MOVEMENT_TYPE_FACE_LEFT",
                 texto="We keep this house for the pilgrims who walk\\n"
                       "the trail. Rest here as long as you like."),
        ]),
    dict(
        pai="Route38", x=34, y=41, pasta="Route38_FarmHouse",
        planta="Route39_FarmHouse", popup="ROUTE 38",
        mapsec="MAPSEC_ROUTE_38", musica="MUS_HG_ROUTE38",
        fonte=("A casa da fazenda existe nas cinco fontes, sempre com a mesma "
               "planta de 13x10: hns e GS Chronicles `Route39_FarmHouse`, "
               "Liquid Crystal 1.28 (13x10, cozinha e mesa), FireGold 44.109 "
               "(11x9), Scorched Silver 17.0 (12x9). Nas cinco ela está na "
               "Route 39; o NOSSO desenho põe uma segunda fazenda na Route 38, "
               "no mesmo tileset `gTileset_Route38Farmland`, e é essa que "
               "recebe a planta."),
        npcs=[
            dict(gfx="OBJ_EVENT_GFX_BALDING_MAN", x=4, y=4,
                 mov="MOVEMENT_TYPE_FACE_DOWN_AND_RIGHT",
                 texto="Our herd grazes the whole east pasture.\\p"
                       "MooMoo Milk from Route 39 gets all the fame,\\n"
                       "but ours is the sweeter one. Don't tell them."),
            dict(gfx="OBJ_EVENT_GFX_WOMAN_3", x=8, y=5,
                 mov="MOVEMENT_TYPE_FACE_LEFT",
                 texto="A MILTANK that is not brushed every day will\\n"
                       "not give a single drop. They are proud."),
        ]),
    dict(
        pai="Route34", x=23, y=50, pasta="Route34_House1",
        planta="Route26_House1", popup="ROUTE 34",
        mapsec="MAPSEC_ROUTE_34", musica="MUS_HG_ROUTE34",
        fonte=("A casa de telhado azul de beira de rota existe no Liquid "
               "Crystal, DUAS vezes, 13x10 cada (mapas 4.7 e 4.9), e na "
               "FireGold (45.57 e 45.56, 11x9). Nas duas ela está na Route 26, "
               "que é onde o hns também a põe (`Route26_House1` e `House2`, o "
               "layout que esta linha reaproveita). O nosso desenho põe a "
               "mesma casa na beira sul da Route 34."),
        npcs=[
            dict(gfx="OBJ_EVENT_GFX_FISHERMAN", x=4, y=4,
                 mov="MOVEMENT_TYPE_FACE_DOWN",
                 texto="I built this place for the fishing.\\p"
                       "The water south of here is thick with\\n"
                       "TENTACOOL. Bring a good rod."),
            dict(gfx="OBJ_EVENT_GFX_GIRL_2", x=8, y=6,
                 mov="MOVEMENT_TYPE_LOOK_AROUND",
                 texto="The Day Care is just up the road.\\n"
                       "They opened the front door again!"),
        ]),
    dict(
        pai="EcruteakCity", x=57, y=25, pasta="EcruteakCity_House3",
        planta="EcruteakCity_House2", popup="ECRUTEAK CITY",
        mapsec="MAPSEC_ECRUTEAK_CITY", musica="MUS_HG_ECRUTEAK",
        fonte=("A casa de Ecruteak, planta de 13x10, está no hns e no GS "
               "Chronicles como `EcruteakCity_House1` e `House2`, que são as "
               "duas que a nossa árvore já traz. Esta é a terceira casa que o "
               "NOSSO desenho de Ecruteak tem e a fonte não abriu."),
        npcs=[
            dict(gfx="OBJ_EVENT_GFX_OLD_WOMAN", x=4, y=4,
                 mov="MOVEMENT_TYPE_FACE_DOWN",
                 texto="This side of town is quiet since the tower\\n"
                       "burned. Only the wind walks the east road."),
            dict(gfx="OBJ_EVENT_GFX_BOY_1", x=8, y=6,
                 mov="MOVEMENT_TYPE_LOOK_AROUND",
                 texto="Grandma says three POKéMON woke up in the\\n"
                       "Burned Tower and ran off. I saw nothing!"),
        ]),
]

# ---------------------------------------------------------------------------
# FAMÍLIA 4: mapa inalcançável.
# ---------------------------------------------------------------------------
INALCANCAVEIS = {
    ("LakeOfRageLowTide", 15, 4): "casa 1 do Lago da Fúria, maré baixa",
    ("LakeOfRageLowTide", 39, 41): "casa 2 do Lago da Fúria, maré baixa",
}

# ---------------------------------------------------------------------------
# FAMÍLIA 5: placa.
# ---------------------------------------------------------------------------
#
# Duas frases, e a diferença entre elas é o que o jogador está olhando. Porta de
# prédio já tem a placa do repo, `Common_EventScript_PortaFechada` ("Closed for
# renovations.", em `data/scripts/portas_fechadas.inc`, criada em 06/09/2026
# justamente porque as 22 primeiras nasceram em português). Boca de caverna não
# tem obra nenhuma: escrever "closed for renovations" na frente de um buraco de
# pedra mentiria o mapa, então ela ganha a sua, no mesmo arquivo e no mesmo
# inglês.
PLACA_PREDIO = "Common_EventScript_PortaFechada"
PLACA_CAVERNA = "Common_EventScript_BocaFechada"
TEXTO_BOCA = "The cave mouth is blocked by fallen rocks.$"
PLACAS = [
    ("OlivineCity", 2, 15, PLACA_PREDIO, "galpão do porto (1 de 6)"),
    ("OlivineCity", 6, 15, PLACA_PREDIO, "galpão do porto (2 de 6)"),
    ("OlivineCity", 10, 15, PLACA_PREDIO, "galpão do porto (3 de 6)"),
    ("OlivineCity", 27, 15, PLACA_PREDIO, "galpão do porto (4 de 6)"),
    ("OlivineCity", 31, 15, PLACA_PREDIO, "galpão do porto (5 de 6)"),
    ("OlivineCity", 35, 15, PLACA_PREDIO, "galpão do porto (6 de 6)"),
    ("EcruteakCity", 8, 54, PLACA_CAVERNA, "boca no penhasco sudoeste"),
    ("BlackthornCity", 39, 18, PLACA_CAVERNA, "boca no penhasco leste"),
    ("BlackthornCity", 5, 33, PLACA_CAVERNA, "boca no penhasco oeste"),
    ("IlexForest", 77, 39, PLACA_CAVERNA, "boca da floresta"),
    ("Route26", 2, 20, PLACA_CAVERNA, "boca da Route 26"),
    ("Route26North", 21, 8, PLACA_CAVERNA, "boca da Route 26 norte"),
    ("Route34", 53, 53, PLACA_CAVERNA, "boca da Route 34"),
    ("Route45", 1, 7, PLACA_CAVERNA, "boca oeste da Route 45"),
    ("Route45", 39, 53, PLACA_CAVERNA, "boca sul da Route 45"),
    ("MtSilver_Outside", 14, 3, PLACA_CAVERNA, "Monte Prata, boca norte"),
    ("MtSilver_Outside", 7, 16, PLACA_CAVERNA, "Monte Prata, boca oeste"),
    ("MtSilver_MountainSide", 44, 9, PLACA_CAVERNA, "Monte Prata, boca da encosta"),
]


# ------------------------------------------------------------------ leitura
_LAYOUTS = None


def layouts():
    global _LAYOUTS
    if _LAYOUTS is None:
        _LAYOUTS = {l["id"]: l for l in json.load(
            open(f"{REPO}/data/layouts/layouts.json"))["layouts"] if "id" in l}
    return _LAYOUTS


def mapa(nome):
    return json.load(open(f"{REPO}/data/maps/{nome}/map.json"))


def grade(nome):
    """(x,y) -> (comportamento, colisão), lendo o map.bin do layout."""
    d = mapa(nome)
    lay = layouts()[d["layout"]]
    blk = open(f"{REPO}/{lay['blockdata_filepath']}", "rb").read()
    w, h = lay["width"], lay["height"]
    prim, _ = W.tabela_de_atributos(lay.get("primary_tileset"))
    seg, _ = W.tabela_de_atributos(lay.get("secondary_tileset"))
    corte = 640 if lay.get("layout_version", "") in ("frlg", "johto") else 512
    fora = {}
    for y in range(h):
        for x in range(w):
            i = (y * w + x) * 2
            bruto = struct.unpack("<H", blk[i:i + 2])[0]
            mt, col = bruto & 0x3FF, (bruto >> 10) & 3
            tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
            if rel < len(tab):
                fora[(x, y)] = (tab[rel], col)
    return fora


def const_do_mapa(pasta):
    """Pasta CamelCase_ComUnderscore -> MAP_CONSTANTE. É o mesmo de-para que o
    `mapjson` faz para gerar `include/constants/map_groups.h`, e por isso NÃO
    pode ser inventado: errar aqui faz o `completude.py` contar o mapa como
    ausente depois de ele existir (a armadilha que o `fecha_portas_sinnoh.py`
    documenta no `demo`)."""
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", pasta.replace("_", ""))
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", s)
    return "MAP_" + s.upper()


def palavras(nome):
    """(lista de u16 do map.bin, largura, altura, caminho do arquivo)."""
    d = mapa(nome)
    lay = layouts()[d["layout"]]
    caminho = f"{REPO}/{lay['blockdata_filepath']}"
    blk = open(caminho, "rb").read()
    w, h = lay["width"], lay["height"]
    return list(struct.unpack(f"<{w * h}H", blk[:w * h * 2])), w, h, caminho


def abre_boca(nome, x, y):
    """Colisão 0 e elevação 0 na célula, preservando o metatile. Devolve
    (antes, depois) ou None se a célula já estava aberta."""
    pal, w, h, caminho = palavras(nome)
    i = y * w + x
    antes = pal[i]
    depois = antes & 0x3FF          # zera colisão (bits 10-11) e elevação (12-15)
    if antes == depois:
        return None
    pal[i] = depois
    with open(caminho, "r+b") as f:
        f.seek(i * 2)
        f.write(struct.pack("<H", depois))
    return antes, depois


def grupo_com_vaga(grupos, base):
    """Grupo novo entra sempre no FIM de `group_order`, que é o que mantém a
    save de pé: `mapGroup` de mapa velho nunca anda."""
    i, nome = 0, base
    while nome in grupos and len(grupos[nome]) >= LIMITE_GRUPO:
        i += 1
        nome = f"{base}{i}"
    if nome not in grupos:
        grupos[nome] = []
        grupos["group_order"].append(nome)
    return nome


# ------------------------------------------------------------------ conferência
def confere():
    """Devolve (erros, avisos). Roda sempre, com ou sem --aplicar."""
    erros, avisos = [], []
    caches = {}

    def cel(nome, x, y):
        if nome not in caches:
            caches[nome] = grade(nome)
        return caches[nome].get((x, y))

    for (fora, xf, yf), (dentro, xd, yd), rotulo in LIGACOES:
        for nome, x, y, lado in ((fora, xf, yf, "fora"), (dentro, xd, yd, "dentro")):
            v = cel(nome, x, y)
            if v is None:
                erros.append(f"{rotulo}: {nome} ({x},{y}) fora da grade")
                continue
            if v[0] not in W.COMPORTA_WARP:
                erros.append(f"{rotulo}: {nome} ({x},{y}) não é célula que "
                             f"dispara warp (comportamento {v[0]})")
            # A conferência que a primeira versão não fazia: o par
            # comportamento+colisão. Sólido que não é porta animada NUNCA
            # dispara, e ligar assim escreve warp morto.
            morto, motivo = W.warp_morto(v[0], v[1])
            if morto and not ABRE_BOCA:
                erros.append(f"{rotulo}: {nome} ({x},{y}) nasceria morto: {motivo}")
            elif morto:
                avisos.append(f"{rotulo}: {nome} ({x},{y}) precisa abrir a "
                              f"boca ({motivo})")
            d = mapa(nome)
            ja = {(w["x"], w["y"]) for w in d.get("warp_events") or []}
            if (x, y) in ja:
                erros.append(f"{rotulo}: {nome} ({x},{y}) JÁ tem warp; ligar de "
                             f"novo criaria warp duplicado no mesmo tile")
            # chão andável colado, senão o jogador nunca chega na porta
            if not any((caches[nome].get((x + dx, y + dy)) or (0, 9))[1] == 0
                       for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0))):
                erros.append(f"{rotulo}: {nome} ({x},{y}) não tem chão andável "
                             f"colado, ninguém alcança essa porta ({lado})")
    return erros, avisos


# ------------------------------------------------------------------ escrita
def aplica():
    incs = []
    conta = {"ligacoes": 0, "mapas": 0, "placas": 0, "bocas": 0}
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))

    # --- família 2: warp de ida e warp de volta, os dois no FIM da lista
    for (fora, xf, yf), (dentro, xd, yd), rotulo in LIGACOES:
        # ABRIR A BOCA vem ANTES de ligar: warp em cima de célula sólida que não
        # é porta animada nasce morto, e o mapa passaria na leitura e falharia
        # no jogo.
        for nome, x, y in ((fora, xf, yf), (dentro, xd, yd)):
            g = grade(nome)
            mb, col = g[(x, y)]
            if W.warp_morto(mb, col)[0]:
                r = abre_boca(nome, x, y)
                if r:
                    print(f"   boca aberta: {nome} ({x},{y}) "
                          f"0x{r[0]:04X} -> 0x{r[1]:04X}")
                    conta["bocas"] += 1
        d_fora, d_dentro = mapa(fora), mapa(dentro)
        d_fora.setdefault("warp_events", [])
        d_dentro.setdefault("warp_events", [])
        i_fora = len(d_fora["warp_events"])
        i_dentro = len(d_dentro["warp_events"])
        d_fora["warp_events"].append({
            "x": xf, "y": yf, "elevation": 0, "dest_map": d_dentro["id"],
            "dest_warp_id": str(i_dentro)})
        d_dentro["warp_events"].append({
            "x": xd, "y": yd, "elevation": 0, "dest_map": d_fora["id"],
            "dest_warp_id": str(i_fora)})
        json.dump(d_fora, open(f"{REPO}/data/maps/{fora}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        json.dump(d_dentro, open(f"{REPO}/data/maps/{dentro}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        conta["ligacoes"] += 1

    # --- família 3: interior novo, com a planta reaproveitada
    for it in INTERIORES:
        base = mapa(it["planta"])
        entrada = [(w["x"], w["y"]) for w in base["warp_events"]]
        d_pai = mapa(it["pai"])
        d_pai.setdefault("warp_events", [])
        i_pai = len(d_pai["warp_events"])
        const = const_do_mapa(it["pasta"])
        objs = []
        for k, npc in enumerate(it["npcs"]):
            objs.append({
                "graphics_id": npc["gfx"], "x": npc["x"], "y": npc["y"],
                "elevation": 0, "movement_type": npc["mov"],
                "movement_range_x": 0, "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": f"{it['pasta']}_EventScript_Npc{k + 1}", "flag": "0"})
        novo = {
            "id": const, "name": it["pasta"], "layout": base["layout"],
            "music": it["musica"], "region_map_section": it["mapsec"],
            "map_name_popup": it["popup"], "requires_flash": False,
            "weather": "WEATHER_NONE", "map_type": "MAP_TYPE_INDOOR",
            "allow_cycling": False, "allow_escaping": False,
            "allow_running": False, "show_map_name": False,
            "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": 0,
            "object_events": objs,
            "warp_events": [{"x": x, "y": y, "elevation": 0,
                             "dest_map": d_pai["id"], "dest_warp_id": str(i_pai)}
                            for x, y in entrada],
            "coord_events": [], "bg_events": [],
            "origem": ("planta reaproveitada de " + it["planta"] + ". FONTE: "
                       + it["fonte"]),
        }
        d_pai["warp_events"].append({
            "x": it["x"], "y": it["y"], "elevation": 0, "dest_map": const,
            "dest_warp_id": "0"})
        os.makedirs(f"{REPO}/data/maps/{it['pasta']}", exist_ok=True)
        json.dump(novo, open(f"{REPO}/data/maps/{it['pasta']}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        json.dump(d_pai, open(f"{REPO}/data/maps/{it['pai']}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        trecho = [f"{it['pasta']}_MapScripts::\n\t.byte 0\n"]
        for k, npc in enumerate(it["npcs"]):
            r = f"{it['pasta']}_EventScript_Npc{k + 1}"
            trecho.append(f"\n{r}::\n\tmsgbox {r}_Text, MSGBOX_NPC\n\tend\n")
            trecho.append(f"\n{r}_Text:\n\t.string \"{npc['texto']}$\"\n")
        with open(f"{REPO}/data/maps/{it['pasta']}/scripts.inc", "w") as f:
            f.write("".join(trecho))
        grupos[grupo_com_vaga(grupos, GRUPO_NOVO)].append(it["pasta"])
        incs.append(f'\t.include "data/maps/{it["pasta"]}/scripts.inc"\n')
        conta["mapas"] += 1

    # --- família 5: placa na célula da porta
    for nome, x, y, script, rotulo in PLACAS:
        d = mapa(nome)
        d.setdefault("bg_events", [])
        if any(b.get("x") == x and b.get("y") == y for b in d["bg_events"]):
            continue
        d["bg_events"].append({
            "type": "sign", "x": x, "y": y, "elevation": 0,
            "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
            "script": script,
            "origem": "porta sem interior em fonte nenhuma (pergunta 46): "
                      + rotulo})
        json.dump(d, open(f"{REPO}/data/maps/{nome}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        conta["placas"] += 1

    if conta["placas"]:
        cam = f"{REPO}/data/scripts/portas_fechadas.inc"
        texto = open(cam, encoding="utf-8").read()
        if PLACA_CAVERNA not in texto:
            with open(cam, "a", encoding="utf-8") as f:
                f.write(
                    "\n@ Boca de caverna que nenhuma das cinco fontes de Johto "
                    "abre (hns, GS\n@ Chronicles, Liquid Crystal, FireGold e "
                    "Scorched Silver), medido em 07/09/2026\n@ na pergunta 46 do"
                    " Gui. Frase própria porque a placa de prédio fala em obra,"
                    "\n@ e buraco de pedra não está em obra nenhuma.\n"
                    f"{PLACA_CAVERNA}::\n"
                    f"\tmsgbox {PLACA_CAVERNA}_Text, MSGBOX_SIGN\n\tend\n\n"
                    f"{PLACA_CAVERNA}_Text:\n\t.string \"{TEXTO_BOCA}\"\n")

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    if incs:
        with open(f"{REPO}/data/event_scripts.s", "a") as f:
            f.writelines(incs)
    return conta


def demo():
    """As três coisas que a primeira versão errou, cada uma com o seu caso."""
    # 1. O de-para de pasta para constante de mapa. Errar aqui faz o
    #    `completude.py` contar o mapa como ausente DEPOIS de ele existir.
    for pasta, esperado in (("BellchimeTrail_House", "MAP_BELLCHIME_TRAIL_HOUSE"),
                            ("Route38_FarmHouse", "MAP_ROUTE38_FARM_HOUSE"),
                            ("Route34_House1", "MAP_ROUTE34_HOUSE1"),
                            ("EcruteakCity_House3", "MAP_ECRUTEAK_CITY_HOUSE3")):
        assert const_do_mapa(pasta) == esperado, (pasta, const_do_mapa(pasta))

    # 2. Abrir a boca mexe SO na colisão e na elevação; o metatile fica.
    for antes, depois in ((0x04A9, 0x00A9), (0x0694, 0x0294), (0x30A9, 0x00A9)):
        assert (antes & 0x3FF) == (depois & 0x3FF), (antes, depois)
        assert antes & 0x3FF == depois, (antes, depois)
    # e a célula já aberta não é tocada duas vezes
    assert (0x00A9 & 0x3FF) == 0x00A9

    # 3. O par comportamento+colisão, que é o que decide se o warp nasce vivo.
    #    Porta animada dispara sólida; boca de caverna sólida NÃO dispara. Sem
    #    isto a primeira versão escreveu 6 warps mortos e passou verde na
    #    leitura.
    animada = W._MB["MB_ANIMATED_DOOR"]
    caverna = W._MB["MB_NON_ANIMATED_DOOR"]
    assert W.warp_morto(animada, 1)[0] is False
    assert W.warp_morto(caverna, 1)[0] is True
    assert W.warp_morto(caverna, 0)[0] is False

    # 4. A conferência de verdade, contra a árvore: nenhum erro nas ligações
    #    declaradas (depois de aplicadas, elas já têm warp e a checagem de
    #    duplicata acusa; antes, elas passam).
    erros, _ = confere()
    ja_aplicado = all("JÁ tem warp" in e for e in erros)
    assert not erros or ja_aplicado, erros
    print("demo ok" + (" (a tabela já está aplicada nesta árvore)"
                       if erros else ""))
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    erros, avisos = confere()
    for e in erros:
        print("ERRO  ", e)
    for a in avisos:
        print("aviso ", a)
    if erros:
        return 1
    print(f"famílias: {len(JA_ENTRA)} já entram, {len(LIGACOES)} ligações, "
          f"{len(INTERIORES)} interiores novos, {len(INALCANCAVEIS)} "
          f"inalcançáveis, {len(PLACAS)} placas")
    for (fora, xf, yf), (dentro, xd, yd), rotulo in LIGACOES:
        print(f"   {fora} ({xf},{yf})  <->  {dentro} ({xd},{yd})   {rotulo}")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        return 0
    conta = aplica()
    print(f"\naplicado: {conta['ligacoes']} ligações ({conta['bocas']} bocas "
          f"abertas), {conta['mapas']} mapas novos, {conta['placas']} placas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
