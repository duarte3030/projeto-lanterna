#!/usr/bin/env python3
"""G2+G3 da obra de Galar: os 438 mapas do demake viram layout + header + porta.

Uso:
    python3 dev_scripts/mundo_galar.py --demo       # autoteste, nao grava nada
    python3 dev_scripts/mundo_galar.py --conferir   # simula tudo e imprime o censo
    python3 dev_scripts/mundo_galar.py --gravar     # grava (idempotente)

O que ele faz, e o que NAO faz
------------------------------
Faz (G2): alocador de grupo (de-para gravado em `dev_scripts/galar_mundo.json`),
`data/layouts/Galar_*/{map.bin,border.bin}` + entrada em `layouts.json` com
`layout_version: "frlg"`, `data/maps/Galar_*/{map.json,scripts.inc}` com musica,
MAPSEC, clima e tipo traduzidos, as MAPSEC novas e os `.include` do
`event_scripts.s`.

Faz (G3): warps limpos, conexoes, RENOMEACAO dos mapas da secao-balde pelo grafo
e heal location por cidade com Pokecenter. Ver os itens 7 a 10 abaixo.

NAO faz: objeto, coord, bg. Isso e G4, por decisao da condutora
(PLANO-OBRAS-GALAR.md, bloco G4). Esses arrays saem VAZIOS de proposito.

De onde sai cada numero (nada foi escolhido de cabeca)
-----------------------------------------------------
1. GEOMETRIA: `fontes-mapas/galar-swsh/extraidos-ultimate/blockdata/gNNmMM.bin`
   cru, formato u16 FRLG, que e o mesmo que o nosso motor le quando o layout
   esta marcado "frlg". Conferido byte a byte: tamanho == w*h*2 nos 438.
   Border sai do `complemento.json` (bytes + borderWidth/borderHeight), tambem
   conferido contra bw*bh*2 nos 438.

2. TILESETS: o par primario/secundario de cada mapa e o par EXATO da fonte,
   traduzido pelo censo do G1 (`dev_scripts/galar_tilesets.json`). Par nao se
   troca. Tres excecoes MEDIDAS, e so tres:
     - g10m07 usa como secundario o unico tileset que o G1 nao converteu
       (0x02D4F8C, LZ77 anomalo). O blockdata dele tem metatile MAXIMO 94, ou
       seja NENHUM metatile de faixa secundaria (>= 640): o secundario e
       decorativo. Recebe SUBSTITUTO_SECUNDARIO e o mapa fica visualmente
       completo.
     - g42m03 e g42m09 usam galar_00 nos DOIS slots. galar_00 foi registrado
       como primario (.isSecondary = FALSE) pelo G1, entao nao pode ser
       pareado como secundario. Os dois mapas tem 1 metatile distinto (4 e 1
       blocos), ambos de faixa primaria, logo o secundario e irrelevante:
       recebem SUBSTITUTO_SECUNDARIO_G00.

3. MUSICA: MEDIDA, nao proposta. O demake e FireRed, e os 344 mapas de Kanto
   que ja estao no repo dao a tabela de conversao de graca: cruzando (MAPSEC,
   largura, altura) entre `mapas.json` e `data/maps/*_Frlg/map.json` sai
   `nosso_valor_de_MUS = id_da_fonte + 212`, com 138 mapas casados, 21 ids de
   musica distintos e ZERO contradicao. Por isso a tabela abaixo e uma
   identidade, nao um chute por papel. A unica excecao e o id 264 (ver
   MUSICA_FORA_DO_BLOCO).

4. CLIMA e TIPO: os enums de FRLG e de Emerald sao o mesmo enum (os dois
   descendem de Ruby), entao o valor cru vira o nome pelo indice.

5. CENA DE BATALHA: os apelidos de FRLG ja existem em include/constants/
   map_types.h (INDOOR_1, INDOOR_2, LORELEI, BRUNO, AGATHA, LANCE, LINK), todos
   valendo MAP_BATTLE_SCENE_NORMAL. So o 1 (GYM) muda de verdade.

6. `cave` e `andar` da fonte sao 0 nos 438 (medido), entao requires_flash=false
   e floor_number some. (E por isso que a renomeacao do item 9 NAO pode derivar
   andar de nada: o campo existe e e zero nos 438.)

7. WARPS (G3): entram os 1.473 que a triagem do G0 aprovou
   (`galar_sujeira.json`), na ORDEM DA FONTE, e a ponta traduzida pelo de-para.
   Como os 674 warps sujos nao entram, o indice de warp muda de lugar: o
   `dest_warp_id` de cada warp e reindexado para a posicao do warp de chegada na
   lista LIMPA do mapa de destino, e um warp que aponta para indice que nao
   existe la e recusado.
   DESVIO CONSCIENTE da letra do plano, medido: dos 1.473, 226 nao tem destino
   representavel (188 apontam para mapa vanilla do FireRed fora dos 438, 38
   apontam para um indice de warp que nao existe no destino). Apagar a LINHA
   deles do map.json renumeraria os warps do mapa e derrubaria 328 warps BONS
   que apontam para indices altos de mapas-cruzamento (medido: 1.473 -> 910 por
   cascata). Entao a linha fica, apontando para SI MESMA (porta que abre no
   proprio lugar, inerte e sem crash), o link nao existe, e cada um dos 226 vai
   para o censo como pendencia de conteudo. Funcionais: 1.247.

8. CONEXOES (G3): as do `complemento.json`, direcao traduzida pelo
   `asm/macros/map.inc` (1=down, 2=up, 3=left, 4=right, conferido no
   `.equiv connection_*`, nao de cabeca). Direcao 0 (CONNECTION_NONE) e alvo
   fora dos 438 nao viram conexao e vao para o censo.

9. RENOMEACAO (G3): o autor jogou 172 mapas na secao 88 (Postwick), que por
   isso virou balde no G2 e deu nomes mentirosos (`Galar_PostwickNN` para casa
   de Motostoke). Com o grafo de warps + conexoes montado, cada mapa do balde
   recebe a identidade de quem ele LIGA: voto por peso de aresta entre os
   vizinhos que NAO sao do balde, UMA rodada so. Uma rodada e regra, nao
   preguica: propagar identidade atraves do proprio balde contamina (medido: com
   propagacao, Postwick12 - que e a propria Postwick, vizinha da Rota 1 - virava
   "Turffield" por causa de 60 salas de raide que penduram num predio de
   Turffield). Empate e mapa sem vizinho ficam Postwick, com nota no censo.
   O nome sai identidade + papel (Indoor/Cave pelo map_type) + numero na ordem
   da fonte; grupo e indice de mapa NAO mudam (o alocador roda depois e so
   depende da ordem da lista e do map_type, que a renomeacao nao toca).

10. HEAL LOCATIONS (G3, decisao 10): o Pokecenter do demake e achado por
    IMPRESSAO DE LAYOUT, nao por nome: 15x10 (a mesma dimensao do
    LAYOUT_POKEMON_CENTER_1F_FRLG que o repo ja tem), blockdata identico entre
    todos, (7,4) andavel e (7,3) parede logo acima (o balcao). Sao 15 mapas
    assim nos 438, um por cidade. Recebe heal location o que tem warp de
    chegada (ou seja, o que da para entrar): uma por cidade identificavel, em
    (7,4), que e o proprio DEFAULT_POKEMON_CENTER_X/Y do motor. `respawn_npc`
    fica de fora de proposito: a enfermeira e NPC, e NPC e G4.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import shutil
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(os.path.dirname(RAIZ), "fontes-mapas/galar-swsh/extraidos-ultimate")
CENSO = f"{RAIZ}/dev_scripts/galar_mundo.json"
CENSO_TILESETS = f"{RAIZ}/dev_scripts/galar_tilesets.json"
HEAL_JSON = f"{RAIZ}/src/data/heal_locations.json"

GRUPO_NOVO = "gMapGroup_Galar"
TETO_GRUPO = 128          # mapNum e s8 no motor: 0..127
TETO_GRUPOS = 128         # mapGroup e s8 no motor: 0..127
# Grupo que nao recebe append: gMapGroup_IndoorDynamic guarda os mapas
# especiais (MAP_DYNAMIC e irmaos) e nao e deposito.
GRUPOS_PROIBIDOS = {"gMapGroup_IndoorDynamic"}

# Deslocamento MEDIDO entre o id de musica do FireRed e o valor do nosso MUS_*.
# Ver item 3 do docstring. `--demo` remede e falha se mudar.
DESLOCAMENTO_MUSICA = 212
# Id 264 e uma musica do FireRed ANTERIOR ao bloco que o repo importou como
# MUS_RG_* (o bloco comeca no id 272 = MUS_RG_FOLLOW_ME). Nos 7 mapas de FR que
# a usam ela e o tema da Safari Zone, e o port de Kanto deste repo a trocou por
# MUS_EVOLUTION, que e um jingle e nao serve de fundo. Os DOIS mapas de Galar
# que a usam sao campo aberto da Wild Area, entao ela vai para o tema que o
# resto da Wild Area ja usa. Esta e a UNICA escolha por papel deste bloco.
MUSICA_FORA_DO_BLOCO = {264: "MUS_RG_ROUTE1"}

SUBSTITUTO_SECUNDARIO = "gTileset_Galar31"      # o mais pareado com galar_11 (79 mapas)
SUBSTITUTO_SECUNDARIO_G00 = "gTileset_Galar32"  # o mais pareado com galar_00 (26 mapas)

CLIMA = ["WEATHER_NONE", "WEATHER_SUNNY_CLOUDS", "WEATHER_SUNNY", "WEATHER_RAIN",
         "WEATHER_SNOW", "WEATHER_RAIN_THUNDERSTORM", "WEATHER_FOG_HORIZONTAL",
         "WEATHER_VOLCANIC_ASH", "WEATHER_SANDSTORM", "WEATHER_FOG_DIAGONAL",
         "WEATHER_UNDERWATER", "WEATHER_SHADE", "WEATHER_DROUGHT",
         "WEATHER_DOWNPOUR", "WEATHER_UNDERWATER_BUBBLES", "WEATHER_ABNORMAL"]
TIPO = ["MAP_TYPE_NONE", "MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE",
        "MAP_TYPE_UNDERGROUND", "MAP_TYPE_UNDERWATER", "MAP_TYPE_OCEAN_ROUTE",
        "MAP_TYPE_UNKNOWN", "MAP_TYPE_INDOOR", "MAP_TYPE_SECRET_BASE"]
BATALHA = ["MAP_BATTLE_SCENE_NORMAL", "MAP_BATTLE_SCENE_GYM",
           "MAP_BATTLE_SCENE_INDOOR_1", "MAP_BATTLE_SCENE_INDOOR_2",
           "MAP_BATTLE_SCENE_LORELEI", "MAP_BATTLE_SCENE_BRUNO",
           "MAP_BATTLE_SCENE_AGATHA", "MAP_BATTLE_SCENE_LANCE",
           "MAP_BATTLE_SCENE_LINK"]
# (cycling, escaping, running, show_map_name) por tipo de mapa, copiado da
# MAIORIA dos 344 mapas de FRLG que ja estao no repo (medido, nao inventado).
BANDEIRAS = {
    "MAP_TYPE_NONE":        (False, False, False, False),
    "MAP_TYPE_TOWN":        (True, False, True, True),
    "MAP_TYPE_CITY":        (True, False, True, True),
    "MAP_TYPE_ROUTE":       (True, False, True, True),
    "MAP_TYPE_UNDERGROUND": (True, True, True, True),
    "MAP_TYPE_INDOOR":      (False, False, False, False),
}
EXTERIOR = {"MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE"}

# As 6 MAPSEC REAIS de Galar. Sao 6 e nao 44 por uma medida dura: o enum ja tem
# 216 entradas e MAPSEC e u8 que divide o espaco de valores com METLOC_SPECIAL_EGG
# (0xFD), entao so cabem 36 entradas NOVAS antes de MAPSEC_NONE bater em 253 e o
# valor virar lixo. 44 nao cabe. As 44 secoes de Galar continuam existindo pelo
# nome, como #define, exatamente como Johto, Sinnoh e Unova ja fazem (ver o
# comentario do proprio region_map_sections.constants.json.txt).
MAPSEC_REAIS = [
    ("MAPSEC_GALAR_SOUTH", "GALAR SOUTH"),
    ("MAPSEC_GALAR_CENTRAL", "GALAR CENTRAL"),
    ("MAPSEC_GALAR_NORTH", "GALAR NORTH"),
    ("MAPSEC_GALAR_ISLE_OF_ARMOR", "ISLE OF ARMOR"),
    ("MAPSEC_GALAR_CROWN_TUNDRA", "CROWN TUNDRA"),
    ("MAPSEC_GALAR_OTHER", "GALAR"),
]

S, C, N, A, T, O = ("MAPSEC_GALAR_SOUTH", "MAPSEC_GALAR_CENTRAL", "MAPSEC_GALAR_NORTH",
                    "MAPSEC_GALAR_ISLE_OF_ARMOR", "MAPSEC_GALAR_CROWN_TUNDRA",
                    "MAPSEC_GALAR_OTHER")

# id da secao na fonte -> (apelido curto usado no nome do mapa, MAPSEC real, nota)
# Nome canonico de Galar quando o autor errou; nota em toda correcao.
SECOES = {
    88:  ("Postwick", S, ""),
    89:  ("Wedgehurst", S, ""),
    90:  ("Motostoke", C, ""),
    91:  ("Turffield", C, ""),
    92:  ("Hulbury", C, ""),
    93:  ("Hammerlocke", N, "a fonte escreve 'Hammmelock'; canonico de Galar e Hammerlocke"),
    94:  ("StowOnSide", C, "a fonte escreve 'Stow On Side'; canonico e Stow-on-Side"),
    95:  ("Ballonlea", N, ""),
    96:  ("Circhester", N, ""),
    97:  ("Wyndon", N, ""),
    98:  ("Spikemuth", N, ""),
    101: ("Route01", S, "a fonte escreve 'Rota 1' (portugues do autor)"),
    102: ("Route02", S, "a fonte escreve 'Rota 2'"),
    103: ("Route03", S, "a fonte escreve 'Rota 3'"),
    104: ("Route04", C, "a fonte escreve 'Rota 4'"),
    105: ("Route05", C, "a fonte escreve 'Rota 5'"),
    106: ("Route06", C, "a fonte escreve 'Rota 6'"),
    107: ("Route07", N, "a fonte escreve 'Rota 7'"),
    108: ("Route08", N, "a fonte escreve 'Rota 8'"),
    109: ("Route09", N, "a fonte escreve 'Rota 9'"),
    110: ("Route10", N, "a fonte escreve 'Rota 10'"),
    116: ("Route16", C, "slot de mapsec do FireRed reaproveitado; Galar nao tem Rota 16"),
    120: ("DynamaxAdventure", T, "Max Lair, que na fonte canonica fica na Crown Tundra"),
    121: ("NewmoonIsland", O, "slot de mapsec de fora de Galar reaproveitado pelo autor"),
    122: ("Underwater", O, "slot do FireRed reaproveitado"),
    123: ("WildArea", C, "primeiro dos DOIS ids que o autor chama de Wild Area"),
    124: ("IceDreamCave", T, "nome do autor, sem equivalente canonico; agrupado na Crown Tundra pelo tema"),
    126: ("SlumberingWeald", S, "a fonte escreve 'Slumbering area'; canonico e Slumbering Weald"),
    127: ("GalarMine", C, ""),
    131: ("WarmUpTunnel", A, "a fonte escreve 'Warm up tunnel'; canonico e Warm-Up Tunnel (Isle of Armor)"),
    132: ("CourageousCavern", A, "a fonte escreve 'Coageous Cavern'; canonico e Courageous Cavern (Isle of Armor)"),
    136: ("WildArea", C, "SEGUNDO id de Wild Area; funde no mesmo MAPSEC_GALAR_WILD_AREA, e por isso as secoes sao 44 e nao 45"),
    138: ("BrawlersCave", A, "canonico e Brawlers' Cave (Isle of Armor)"),
    140: ("RoseTower", N, ""),
    143: ("IsleOfArmor", A, ""),
    149: ("SixIsland", O, "slot do FireRed reaproveitado"),
    176: ("GlimwoodTangle", N, ""),
    179: ("TrainerTower", O, "slot do FireRed reaproveitado"),
    181: ("LostCave", O, "slot do FireRed reaproveitado"),
    183: ("AlteringCave", O, "slot do FireRed reaproveitado"),
    186: ("TanobyKey", O, "slot do FireRed reaproveitado"),
    189: ("LiptooChamber", O, "slot do FireRed reaproveitado"),
    192: ("ScufibChamber", O, "slot do FireRed reaproveitado"),
    193: ("RixyChamber", O, "slot do FireRed reaproveitado"),
    195: ("CrownTundra", T, ""),
}


# ------------------------------------------------------------------ G3 ------
# Secao que o autor usou de balde (172 dos 438 mapas caem nela). Ver item 9.
SECAO_BALDE = 88
# Papel do mapa no nome novo, pelo map_type. Exterior nao ganha papel: a
# identidade ja e o lugar. `andar` nao entra porque e 0 nos 438 (item 6).
PAPEL = {"MAP_TYPE_INDOOR": "Indoor", "MAP_TYPE_UNDERGROUND": "Cave"}
# Conferido em asm/macros/map.inc (.equiv connection_down, CONNECTION_SOUTH ...)
# contra o enum Connection de include/constants/global.h.
DIRECAO = {1: "down", 2: "up", 3: "left", 4: "right"}
# Impressao do Pokecenter do demake (item 10). Dimensao igual a do
# LAYOUT_POKEMON_CENTER_1F_FRLG que o repo ja tem; (7,4) e o
# DEFAULT_POKEMON_CENTER_X/Y de src/data/heal_locations.json.txt.
PC_DIM = (15, 10)
PC_CURA = (7, 4)
PC_BALCAO = (7, 3)


def snake(nome):
    """Postwick -> POSTWICK; StowOnSide -> STOW_ON_SIDE; Route01 -> ROUTE01."""
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", nome)
    return s.upper()


def apelido_mapsec(slug):
    return "MAPSEC_GALAR_" + snake(slug)


# ---------------------------------------------------------------- leitura ----

def le_fonte():
    mapas = json.load(open(f"{FONTE}/mapas.json"))
    comp = json.load(open(f"{FONTE}/complemento.json"))
    tset = json.load(open(CENSO_TILESETS))
    de_para_ts = {int(k, 16): v for k, v in tset["de_para"].items()}
    nao_conv = {int(x["endereco"], 16) for x in tset["nao_convertidos"]}
    validos = []
    for grupo in mapas:
        for i, m in enumerate(grupo["mapas"]):
            nome = "g%02dm%02d" % (grupo["grupo"], i)
            caminho = f"{FONTE}/blockdata/{nome}.bin"
            if not os.path.exists(caminho):
                continue
            validos.append((nome, grupo["grupo"], i, m, comp[nome]))
    return validos, de_para_ts, nao_conv


def resolve(validos, de_para_ts, nao_conv):
    """Um dicionario por mapa, com tudo ja traduzido para nome do repo."""
    contador = collections.Counter()
    saida = []
    for nome, gsrc, isrc, m, c in validos:
        sec = SECOES[m["secao_mapa"]]
        slug = sec[0]
        contador[slug] += 1
        base = "Galar_%s%02d" % (slug, contador[slug])
        idmapa = "MAP_GALAR_%s_%02d" % (snake(slug), contador[slug])
        idlayout = "LAYOUT_GALAR_%s_%02d" % (snake(slug), contador[slug])

        t1, t2 = m["layout"]["tileset1"], m["layout"]["tileset2"]
        notas_ts = ""
        primario = de_para_ts[t1]["rotulo"]
        if t2 in nao_conv:
            secundario = SUBSTITUTO_SECUNDARIO
            notas_ts = ("secundario 0x%07X nao foi convertido pelo G1 (LZ77 anomalo); "
                        "o blockdata deste mapa nao usa metatile de faixa secundaria, "
                        "entao entra %s no lugar" % (t2, secundario))
        elif de_para_ts[t2]["papel"] != "secundario":
            secundario = SUBSTITUTO_SECUNDARIO_G00
            notas_ts = ("a fonte pareia %s nos DOIS slots; ele foi registrado como "
                        "primario pelo G1 e o mapa tem 1 metatile distinto de faixa "
                        "primaria, entao entra %s no lugar"
                        % (de_para_ts[t2]["nome"], secundario))
        else:
            secundario = de_para_ts[t2]["rotulo"]

        mus = m["music"]
        if mus == 0:
            musica = "MUS_NONE"
        elif mus in MUSICA_FORA_DO_BLOCO:
            musica = MUSICA_FORA_DO_BLOCO[mus]
        else:
            musica = None  # resolvido em nome_musica(), que precisa do songs.h
        tipo = TIPO[m["tipo"]]
        saida.append({
            "fonte": nome, "fonte_grupo": gsrc, "fonte_indice": isrc,
            "nome": base, "id_mapa": idmapa, "id_layout": idlayout,
            "w": m["layout"]["w"], "h": m["layout"]["h"],
            "border_w": c["border"]["borderWidth"], "border_h": c["border"]["borderHeight"],
            "border_bytes": c["border"]["bytes"],
            "primary_tileset": primario, "secondary_tileset": secundario,
            "nota_tileset": notas_ts,
            "music_fonte": mus, "music": musica,
            "secao_fonte": m["secao_mapa"], "slug_secao": slug,
            "region_map_section": apelido_mapsec(slug),
            "weather": CLIMA[m["clima"]], "map_type": tipo,
            "battle_scene": BATALHA[m["batalha"]],
            "map_script_ptr": c.get("map_script_ptr"),
            "conexoes_na_fonte": len(c.get("conexoes") or []),
        })
    return saida


# --------------------------------------------------- G3: topologia do mundo --

def topologia(validos):
    """Warps limpos e conexoes validas, em chave da FONTE (nada de nome ainda).

    Devolve:
      limpos[fonte]  -> lista dos indices de warp que a triagem aprovou
      pos[fonte]     -> indice cru do warp -> posicao dele na lista limpa
      warp[fonte]    -> lista de (posicao, warp cru, destino ou None, motivo)
      conex[fonte]   -> lista de (direcao, offset, destino) validas
      pend_conex     -> lista de conexoes recusadas, com motivo
      arestas[fonte] -> Counter de vizinho -> peso (grafo NAO dirigido)
    """
    doc = json.load(open(f"{FONTE}/galar_sujeira.json"))
    sujos = collections.defaultdict(set)
    for r in doc["reprovados"]:
        sujos[(r["mapa"], r["tipo"])].add(r["i"])

    bruto = {n: (m.get("warps") or [], c.get("conexoes") or [])
             for n, g, i, m, c in validos}
    chave = {(g, i): n for n, g, i, m, c in validos}

    limpos = {n: [j for j in range(len(bruto[n][0])) if j not in sujos[(n, "warps")]]
              for n in bruto}
    pos = {n: {j: p for p, j in enumerate(limpos[n])} for n in limpos}

    warp, conex, pend_conex = {}, {}, []
    arestas = collections.defaultdict(collections.Counter)
    for n in sorted(bruto):
        linhas = []
        for p, j in enumerate(limpos[n]):
            w = bruto[n][0][j]
            d = chave.get((w["grupo"], w["mapa"]))
            if d is None:
                motivo = ("destino %d.%d nao esta nos 438: e mapa vanilla do FireRed "
                          "que o demake nao redesenhou" % (w["grupo"], w["mapa"]))
            elif w["warp_id"] not in pos[d]:
                motivo = ("warp de chegada %d nao existe em %s, que tem %d warps limpos"
                          % (w["warp_id"], d, len(pos[d])))
            else:
                motivo = None
            linhas.append((p, w, d if not motivo else None, motivo))
            # A ARESTA vale mesmo quando o indice de chegada esta quebrado: o
            # que o grafo de identidade (item 9) precisa saber e que a porta
            # deste mapa da NAQUELE mapa, e isso o destino ja diz.
            if d is not None and d != n:
                arestas[n][d] += 1
                arestas[d][n] += 1
        warp[n] = linhas

        validas = []
        for cx in bruto[n][1]:
            d = chave.get((cx["grupo"], cx["mapa"]))
            if cx["direcao"] not in DIRECAO:
                motivo = "direcao %d (CONNECTION_NONE): conexao morta na fonte" % cx["direcao"]
            elif d is None:
                motivo = ("destino %d.%d nao esta nos 438: e mapa vanilla do FireRed "
                          "que o demake nao redesenhou" % (cx["grupo"], cx["mapa"]))
            else:
                motivo = None
            if motivo:
                pend_conex.append({"mapa_fonte": n, "direcao": cx["direcao"],
                                   "offset": cx["offset"], "motivo": motivo})
                continue
            validas.append((cx["direcao"], cx["offset"], d))
            if d != n:
                arestas[n][d] += 1
                arestas[d][n] += 1
        conex[n] = validas
    return limpos, pos, warp, conex, pend_conex, arestas


def renomeia(mapas, arestas):
    """Da nome de verdade aos mapas da secao-balde, pelo grafo. Ver item 9.

    Grupo e indice NAO mudam: o alocador roda depois desta funcao e so olha a
    ordem da lista e o map_type, e nenhum dos dois e tocado aqui.
    """
    por_fonte = {m["fonte"]: m for m in mapas}
    balde = [m for m in mapas if m["secao_fonte"] == SECAO_BALDE]
    fora = {m["fonte"]: m["slug_secao"] for m in mapas if m["secao_fonte"] != SECAO_BALDE}

    # contador de cada familia de nome ja em uso pelos mapas de fora do balde
    usados = collections.Counter()
    for m in mapas:
        if m["secao_fonte"] != SECAO_BALDE:
            usados[m["slug_secao"]] += 1

    decisao = {}
    for m in balde:
        votos = collections.Counter()
        for viz, peso in arestas[m["fonte"]].items():
            if viz in fora:
                votos[fora[viz]] += peso
        ranking = votos.most_common()
        if not ranking:
            decisao[m["fonte"]] = (None, "nenhum warp nem conexao limpa liga este mapa a "
                                         "um mapa de secao conhecida", {})
        elif len(ranking) > 1 and ranking[0][1] == ranking[1][1]:
            decisao[m["fonte"]] = (None, "empate no grafo entre %s" %
                                   ", ".join("%s(%d)" % r for r in ranking[:3]), dict(votos))
        else:
            decisao[m["fonte"]] = (ranking[0][0], "", dict(votos))

    renomeados = {}
    for m in balde:  # ordem da fonte, que e a ordem da lista `mapas`
        ident, nota, votos = decisao[m["fonte"]]
        if ident is None:
            m["nota_nome"] = "nome de balde mantido: " + nota
            m["voto_nome"] = votos
            continue
        familia = ident + PAPEL.get(m["map_type"], "")
        usados[familia] += 1
        velho = m["nome"]
        m["nome_no_g2"] = velho
        m["slug_secao"] = familia
        m["nome"] = "Galar_%s%02d" % (familia, usados[familia])
        m["id_mapa"] = "MAP_GALAR_%s_%02d" % (snake(familia), usados[familia])
        m["id_layout"] = "LAYOUT_GALAR_%s_%02d" % (snake(familia), usados[familia])
        m["nota_nome"] = ("renomeado no G3: o grafo liga este mapa a %s (votos %s); "
                          "papel %s pelo map_type" % (ident, votos, m["map_type"]))
        m["voto_nome"] = votos
        renomeados[velho] = m["nome"]
    return renomeados, decisao


def costura(mapas, limpos, pos, warp, conex):
    """Transforma a topologia em warp_events e connections, ja com os nomes finais."""
    por_fonte = {m["fonte"]: m for m in mapas}
    pend_warp = []
    for m in mapas:
        eventos = []
        for p, w, d, motivo in warp[m["fonte"]]:
            if motivo:
                # porta inerte: aponta para si mesma para NAO renumerar os warps
                # do mapa (ver item 7). Sem link, e com pendencia no censo.
                destino, chegada = m["id_mapa"], p
                pend_warp.append({
                    "mapa_fonte": m["fonte"], "mapa": m["nome"], "warp": p,
                    "x": w["x"], "y": w["y"],
                    "destino_fonte": "g%02dm%02d" % (w["grupo"], w["mapa"]),
                    "warp_id_fonte": w["warp_id"], "motivo": motivo,
                })
            else:
                destino, chegada = por_fonte[d]["id_mapa"], pos[d][w["warp_id"]]
            eventos.append({"x": w["x"], "y": w["y"], "elevation": 0,
                            "dest_map": destino, "dest_warp_id": str(chegada)})
        m["warp_events"] = eventos
        m["connections"] = [{"map": por_fonte[d]["id_mapa"], "offset": off,
                             "direction": DIRECAO[dire]}
                            for dire, off, d in conex[m["fonte"]]]
    return pend_warp


def acha_pokecenters(mapas, arestas):
    """Os Pokecenter do demake, pela impressao de layout. Ver item 10."""
    grupos = collections.defaultdict(list)
    for m in mapas:
        if (m["w"], m["h"]) != PC_DIM:
            continue
        b = open(f"{FONTE}/blockdata/{m['fonte']}.bin", "rb").read()
        grupos[hashlib.md5(b).hexdigest()].append(m)
    achados = []
    for md5, lista in grupos.items():
        if len(lista) < 10:
            continue
        b = open(f"{FONTE}/blockdata/{lista[0]['fonte']}.bin", "rb").read()
        v = struct.unpack("<%dH" % (len(b) // 2), b)
        colisao = lambda x, y: (v[y * PC_DIM[0] + x] >> 10) & 3
        if colisao(*PC_CURA) == 0 and colisao(*PC_BALCAO) != 0:
            achados.append((md5, lista))
    if len(achados) != 1:
        raise SystemExit("impressao de Pokecenter nao e unica: %d clusters" % len(achados))
    return achados[0][1]


def heal_locations(mapas, arestas):
    """Uma heal location por cidade com Pokecenter em que da para entrar."""
    novas, ignorados = [], []
    vistos = set()
    # Cidade com mais de um Centro fica com o MAIS LIGADO (desempate: ordem da
    # fonte), que e o que tem mais porta chegando nele.
    for m in sorted(acha_pokecenters(mapas, arestas),
                    key=lambda m: (-len(arestas[m["fonte"]]), m["fonte"])):
        if not arestas[m["fonte"]]:
            ignorados.append((m["nome"], "nenhum warp limpo chega neste Centro; "
                                         "cidade nao identificavel pelo grafo"))
            continue
        slug = m["slug_secao"]
        if slug in vistos:
            ignorados.append((m["nome"], "%s ja tem heal location" % slug))
            continue
        vistos.add(slug)
        novas.append({"id": "HEAL_LOCATION_GALAR_" + snake(slug),
                      "map": m["id_mapa"], "x": PC_CURA[0], "y": PC_CURA[1],
                      "respawn_map": m["id_mapa"]})
    return novas, ignorados


def escreve_heal(novas, gravar):
    doc = json.load(open(HEAL_JSON))
    doc["heal_locations"] = [h for h in doc["heal_locations"]
                             if not h["id"].startswith("HEAL_LOCATION_GALAR_")]
    doc["heal_locations"].extend(novas)     # APPEND: nenhum indice antigo se mexe
    if gravar:
        with open(HEAL_JSON, "w") as f:
            json.dump(doc, f, indent=2)
            f.write("\n")
    return len(doc["heal_locations"])


def tabela_musica():
    """id da fonte -> nome do nosso MUS_*, pelo deslocamento medido."""
    valor_para_nome = {}
    for linha in open(f"{RAIZ}/include/constants/songs.h"):
        m = re.match(r"#define\s+(MUS_[A-Z0-9_]+)\s+(\d+)", linha)
        if m:
            valor_para_nome.setdefault(int(m.group(2)), m.group(1))
    return valor_para_nome


def aplica_musica(mapas):
    valor_para_nome = tabela_musica()
    faltando = set()
    for m in mapas:
        if m["music"]:
            continue
        alvo = valor_para_nome.get(m["music_fonte"] + DESLOCAMENTO_MUSICA)
        if not alvo:
            faltando.add(m["music_fonte"])
            alvo = "MUS_NONE"
        m["music"] = alvo
    return faltando


# --------------------------------------------------------------- alocador ----

def aloca(mapas):
    """Distribui os mapas em APPEND. Nenhum indice existente muda.

    Regra, nesta ordem:
      1. o grupo livre (o 128o e ultimo que o motor aceita, porque mapGroup e s8)
         nasce como gMapGroup_Galar e recebe os EXTERIORES (town/city/route),
         que sao os mapas que o Gui vai querer achar pelo nome;
      2. o resto empacota em grupos que ja existem, na ordem de quem tem mais
         vaga (desempate: ordem de group_order), respeitando o teto de 128.
    """
    grupos = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    ordem = list(grupos["group_order"])
    if len(ordem) >= TETO_GRUPOS and GRUPO_NOVO not in ordem:
        raise SystemExit("sem grupo livre: group_order ja tem %d de %d" % (len(ordem), TETO_GRUPOS))

    # ponto de partida limpo: tira qualquer Galar de uma rodada anterior
    for g in ordem:
        grupos[g] = [n for n in grupos[g] if not n.startswith("Galar_")]
    if GRUPO_NOVO not in ordem:
        ordem.append(GRUPO_NOVO)
        grupos["group_order"] = ordem
    grupos[GRUPO_NOVO] = []

    exteriores = [m for m in mapas if m["map_type"] in EXTERIOR]
    resto = [m for m in mapas if m["map_type"] not in EXTERIOR]
    if len(exteriores) > TETO_GRUPO:
        raise SystemExit("exteriores (%d) nao cabem no grupo livre" % len(exteriores))

    destino = {}
    for m in exteriores:
        destino[m["nome"]] = GRUPO_NOVO

    candidatos = [(TETO_GRUPO - len(grupos[g]), -i, g)
                  for i, g in enumerate(ordem)
                  if g != GRUPO_NOVO and g not in GRUPOS_PROIBIDOS]
    candidatos.sort(reverse=True)
    fila = [(g, vaga) for vaga, _, g in candidatos if vaga > 0]

    it = iter(resto)
    atual = None
    for m in it:
        while atual is None or usados >= atual[1]:
            if not fila:
                raise SystemExit("acabou vaga em grupo existente")
            atual, usados = fila.pop(0), 0
        destino[m["nome"]] = atual[0]
        usados += 1

    for m in mapas:
        g = destino[m["nome"]]
        grupos[g].append(m["nome"])
        m["grupo"] = g
        m["grupo_indice_no_grupo"] = len(grupos[g]) - 1
        m["grupo_indice"] = ordem.index(g)

    for g in ordem:
        if len(grupos[g]) > TETO_GRUPO:
            raise SystemExit("grupo %s estourou o teto (%d)" % (g, len(grupos[g])))
    return grupos, ordem


# ----------------------------------------------------------------- gravar ----

def escreve_layouts(mapas, gravar):
    caminho = f"{RAIZ}/data/layouts/layouts.json"
    doc = json.load(open(caminho))
    doc["layouts"] = [x for x in doc["layouts"]
                      if not str(x.get("id", "")).startswith("LAYOUT_GALAR_")]
    for m in mapas:
        pasta = f"{RAIZ}/data/layouts/{m['nome']}"
        if gravar:
            os.makedirs(pasta, exist_ok=True)
            with open(f"{pasta}/map.bin", "wb") as f:
                f.write(open(f"{FONTE}/blockdata/{m['fonte']}.bin", "rb").read())
            with open(f"{pasta}/border.bin", "wb") as f:
                f.write(bytes.fromhex(m["border_bytes"]))
        doc["layouts"].append({
            "id": m["id_layout"],
            "name": m["nome"] + "_Layout",
            "width": m["w"], "height": m["h"],
            "border_width": m["border_w"], "border_height": m["border_h"],
            "primary_tileset": m["primary_tileset"],
            "secondary_tileset": m["secondary_tileset"],
            "border_filepath": f"data/layouts/{m['nome']}/border.bin",
            "blockdata_filepath": f"data/layouts/{m['nome']}/map.bin",
            "layout_version": "frlg",
        })
    if gravar:
        with open(caminho, "w") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")
    return len(doc["layouts"])


def escreve_mapas(mapas, gravar):
    for m in mapas:
        ciclo, fuga, corrida, nome_na_tela = BANDEIRAS[m["map_type"]]
        nota_nome = (" " + m["nota_nome"]) if m.get("nota_nome") else ""
        doc = {
            "id": m["id_mapa"],
            "name": m["nome"],
            "layout": m["id_layout"],
            "music": m["music"],
            "region_map_section": m["region_map_section"],
            "requires_flash": False,
            "weather": m["weather"],
            "map_type": m["map_type"],
            "allow_cycling": ciclo,
            "allow_escaping": fuga,
            "allow_running": corrida,
            "show_map_name": nome_na_tela,
            "battle_scene": m["battle_scene"],
            "connections": m["connections"],
            "object_events": [],
            "warp_events": m["warp_events"],
            "coord_events": [],
            "bg_events": [],
            "origem": ("demake Sword and Shield Ultimate Plus v1.2.1.2 (FireRed), mapa %s. "
                       "Gerado por dev_scripts/mundo_galar.py; nao editar a mao. "
                       "object_events, coord_events e bg_events vazios de proposito: "
                       "o G4 (NPCs e itens) ainda nao rodou.%s" % (m["fonte"], nota_nome)),
        }
        if not gravar:
            continue
        pasta = f"{RAIZ}/data/maps/{m['nome']}"
        os.makedirs(pasta, exist_ok=True)
        with open(f"{pasta}/map.json", "w") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")
        with open(f"{pasta}/scripts.inc", "w") as f:
            f.write("@ Gerado por dev_scripts/mundo_galar.py (G2). Sem cena: o ponteiro de\n"
                    "@ map script da fonte (%s) esta anotado no censo para a fase de conteudo.\n\n"
                    % (m["map_script_ptr"] or "nenhum"))
            f.write("%s_MapScripts::\n\t.byte 0\n" % m["nome"])


def limpa_orfaos(mapas, gravar):
    """Pasta de mapa/layout de uma rodada ANTERIOR que nao existe mais nesta.

    Existe por causa da renomeacao: `data/maps/Galar_Postwick13/` continuaria em
    disco depois que o mapa virou `Galar_Wedgehurst12`, e pasta orfa de mapa e
    lixo que o `mapjson` ainda enxerga. (Licao LEVA_DONA do S8: gerador que so
    escreve, e nunca apaga, mente na segunda rodada.)
    """
    vivos = {m["nome"] for m in mapas}
    orfas = []
    for base in ("data/maps", "data/layouts"):
        for nome in sorted(os.listdir(f"{RAIZ}/{base}")):
            if nome.startswith("Galar_") and nome not in vivos:
                orfas.append(f"{base}/{nome}")
    if gravar:
        for o in orfas:
            shutil.rmtree(f"{RAIZ}/{o}")
    return orfas


def escreve_grupos(grupos, gravar):
    if gravar:
        with open(f"{RAIZ}/data/maps/map_groups.json", "w") as f:
            json.dump(grupos, f, indent=2, ensure_ascii=False)
            f.write("\n")


def escreve_mapsecs(gravar):
    caminho = f"{RAIZ}/src/data/region_map/region_map_sections.json"
    doc = json.load(open(caminho))
    doc["map_sections"] = [x for x in doc["map_sections"]
                           if not str(x.get("id", "")).startswith("MAPSEC_GALAR_")]
    for ident, nome in MAPSEC_REAIS:
        doc["map_sections"].append({"id": ident, "name": nome,
                                    "x": 0, "y": 0, "width": 1, "height": 1})
    if gravar:
        with open(caminho, "w") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")

    tpl = f"{RAIZ}/src/data/region_map/region_map_sections.constants.json.txt"
    txt = open(tpl).read()
    txt = re.sub(r"\n// Apelidos de MAPSEC de Galar\..*?(?=\n#endif)", "", txt, flags=re.S)
    apelidos = []
    vistos = set()
    for sid in sorted(SECOES):
        slug, real, _ = SECOES[sid]
        nome = apelido_mapsec(slug)
        if nome in vistos:
            continue
        vistos.add(nome)
        if nome == real:
            continue  # IsleOfArmor e CrownTundra ja SAO MAPSEC reais; nao se apelidam
        apelidos.append("#define %s %s" % (nome, real))
    bloco = ("\n// Apelidos de MAPSEC de Galar. Sao 44 nomes para 6 MAPSEC reais pela\n"
             "// mesma razao de Johto, Sinnoh e Unova acima: MAPSEC e u8 e divide o espaco\n"
             "// de valores com METLOC_SPECIAL_EGG (0xFD). Com 216 entradas ja gastas, so\n"
             "// cabiam 36 novas; as 44 secoes de Galar viram apelido de regiao.\n"
             + "\n".join(apelidos) + "\n")
    txt = txt.replace("\n#endif // GUARD_CONSTANTS_REGION_MAP_SECTIONS_H",
                      bloco + "\n#endif // GUARD_CONSTANTS_REGION_MAP_SECTIONS_H")
    if gravar:
        open(tpl, "w").write(txt)
    return len(apelidos)


def escreve_includes(mapas, gravar):
    caminho = f"{RAIZ}/data/event_scripts.s"
    linhas = [l for l in open(caminho).read().splitlines()
              if not l.strip().startswith('.include "data/maps/Galar_')]
    for m in mapas:
        linhas.append('\t.include "data/maps/%s/scripts.inc"' % m["nome"])
    if gravar:
        open(caminho, "w").write("\n".join(linhas) + "\n")


def escreve_censo(mapas, grupos, gravar, g3=None):
    porgrupo = collections.Counter(m["grupo"] for m in mapas)
    g3 = g3 or {}
    doc = {
        "gerado_por": "dev_scripts/mundo_galar.py",
        "fonte": "fontes-mapas/galar-swsh/extraidos-ultimate",
        "n_mapas": len(mapas),
        "grupo_novo": GRUPO_NOVO,
        "mapas_por_grupo": dict(sorted(porgrupo.items(), key=lambda x: -x[1])),
        "mapsecs_reais": [a for a, _ in MAPSEC_REAIS],
        "deslocamento_musica_medido": DESLOCAMENTO_MUSICA,
        "musica_fora_do_bloco": {str(k): v for k, v in MUSICA_FORA_DO_BLOCO.items()},
        "de_para": {m["fonte"]: {
            "mapa": m["id_mapa"], "nome": m["nome"], "layout": m["id_layout"],
            "grupo": m["grupo"], "grupo_indice": m["grupo_indice"],
            "indice_no_grupo": m["grupo_indice_no_grupo"],
            "fonte_grupo": m["fonte_grupo"], "fonte_indice": m["fonte_indice"],
            "w": m["w"], "h": m["h"],
            "primary_tileset": m["primary_tileset"],
            "secondary_tileset": m["secondary_tileset"],
            "nota_tileset": m["nota_tileset"],
            "music_fonte": m["music_fonte"], "music": m["music"],
            "secao_fonte": m["secao_fonte"],
            "region_map_section": m["region_map_section"],
            "map_script_ptr": m["map_script_ptr"],
            "conexoes_na_fonte": m["conexoes_na_fonte"],
            "warps": len(m["warp_events"]),
            "conexoes": len(m["connections"]),
            "nome_no_g2": m.get("nome_no_g2"),
            "nota_nome": m.get("nota_nome", ""),
        } for m in mapas},
        **g3,
        "secoes": {str(k): {"slug": v[0], "mapsec_real": v[1],
                            "apelido": apelido_mapsec(v[0]), "nota": v[2]}
                   for k, v in sorted(SECOES.items())},
    }
    if gravar:
        with open(CENSO, "w") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return doc


# ------------------------------------------------------------------ demo ----

def demo():
    """Autoteste: tudo que este script AFIRMA, medido de novo."""
    validos, ts, nao_conv = le_fonte()
    assert len(validos) == 438, len(validos)

    # 1. geometria bate com a dimensao declarada, nos 438
    for nome, _, _, m, c in validos:
        tam = os.path.getsize(f"{FONTE}/blockdata/{nome}.bin")
        assert tam == m["layout"]["w"] * m["layout"]["h"] * 2, nome
        assert len(c["border"]["bytes"]) // 2 == c["border"]["borderWidth"] * c["border"]["borderHeight"] * 2, nome

    # 2. deslocamento de musica: remedido do zero contra os mapas de Kanto
    import glob
    lay = {x["id"]: x for x in json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    val = {}
    for linha in open(f"{RAIZ}/include/constants/songs.h"):
        mm = re.match(r"#define\s+(MUS_[A-Z0-9_]+)\s+(\d+)", linha)
        if mm:
            val[mm.group(1)] = int(mm.group(2))
    nossos = collections.defaultdict(set)
    for p in glob.glob(f"{RAIZ}/data/maps/*_Frlg/map.json"):
        d = json.load(open(p))
        L = lay.get(d["layout"])
        if L:
            nossos[(d["region_map_section"], L["width"], L["height"])].add(val.get(d["music"]))
    secname = {}
    for x in json.load(open(f"{RAIZ}/src/data/region_map/region_map_sections.json"))["map_sections"]:
        if "name" in x:
            secname[re.sub(r"[^A-Z0-9]", "", x["name"].replace("。", ".").upper())] = x["id"]
    fonte_todos = json.load(open(f"{FONTE}/mapas.json"))
    votos = collections.Counter()
    for g in fonte_todos:
        for i, m in enumerate(g["mapas"]):
            if "music" not in m or m.get("invalido"):
                continue
            if os.path.exists(f"{FONTE}/blockdata/g%02dm%02d.bin" % (g["grupo"], i)):
                continue
            sid = secname.get(re.sub(r"[^A-Z0-9]", "", (m.get("nome_secao") or "").replace("。", ".").upper()))
            k = (sid, m["layout"]["w"], m["layout"]["h"])
            if sid and k in nossos and len(nossos[k]) == 1:
                v = next(iter(nossos[k]))
                if v:
                    votos[v - m["music"]] += 1
    assert len(votos) == 1 and DESLOCAMENTO_MUSICA in votos, votos.most_common(5)
    assert votos[DESLOCAMENTO_MUSICA] >= 100, votos[DESLOCAMENTO_MUSICA]

    # 3. os tres mapas degenerados sao mesmo degenerados
    for nome in ("g42m03", "g42m09", "g10m07"):
        b = open(f"{FONTE}/blockdata/{nome}.bin", "rb").read()
        v = struct.unpack("<%dH" % (len(b) // 2), b)
        assert max(x & 0x3FF for x in v) < 640, nome  # nenhum metatile de faixa secundaria

    # 4. as secoes cobrem tudo, e sao 44 apelidos
    usados = {m["secao_mapa"] for _, _, _, m, _ in validos}
    assert usados <= set(SECOES), usados - set(SECOES)
    assert len({apelido_mapsec(v[0]) for v in SECOES.values()}) == 44

    # 5. MAPSEC cabe no u8 depois do que vamos acrescentar
    txt = open(f"{RAIZ}/include/constants/region_map_sections.h").read()
    atuais = [l.strip().rstrip(",") for l in txt.split("enum {")[1].split("};")[0].strip().splitlines() if l.strip()]
    novos = len([a for a, _ in MAPSEC_REAIS if a not in atuais])
    assert atuais.index("MAPSEC_NONE") + novos <= 0xFC, "MAPSEC_NONE passaria de 252"

    # 6. a resolucao inteira roda e a alocacao respeita os tetos
    mapas = resolve(validos, ts, nao_conv)
    faltando = aplica_musica(mapas)
    assert not faltando, faltando
    antes = {m["fonte"]: m["nome"] for m in mapas}

    # 7. a direcao de conexao sai do repo, nao da memoria
    macro = open(f"{RAIZ}/asm/macros/map.inc").read()
    for valor, palavra in DIRECAO.items():
        alvo = {1: "SOUTH", 2: "NORTH", 3: "WEST", 4: "EAST"}[valor]
        assert ".equiv connection_%s, CONNECTION_%s" % (palavra, alvo) in macro, palavra
    enum = open(f"{RAIZ}/include/constants/global.h").read().split("enum Connection")[1]
    ordem_enum = re.findall(r"CONNECTION_([A-Z]+)", enum.split("};")[0])
    assert ordem_enum[:5] == ["INVALID", "NONE", "SOUTH", "NORTH", "WEST"], ordem_enum

    # 8. a topologia bate com os totais do censo de sujeira
    suj = json.load(open(f"{FONTE}/galar_sujeira.json"))
    limpos, pos, warp, conex, pend_conex, arestas = topologia(validos)
    assert sum(len(v) for v in limpos.values()) == suj["totais_limpos"]["warps"], "warps limpos"

    # 9. renomeacao: grupo e indice ficam intactos, e nome/id continuam unicos
    renomeia(mapas, arestas)
    grupos, ordem = aloca(mapas)
    assert len(ordem) <= TETO_GRUPOS
    assert all(len(grupos[g]) <= TETO_GRUPO for g in ordem)
    assert len({m["id_mapa"] for m in mapas}) == 438
    assert len({m["nome"] for m in mapas}) == 438
    assert len({m["id_layout"] for m in mapas}) == 438
    padrao = json.load(open(CENSO))["de_para"]
    for m in mapas:                       # o de-para gravado e a testemunha
        c = padrao.get(m["fonte"])
        if c:
            assert (c["grupo"], c["indice_no_grupo"]) == (m["grupo"], m["grupo_indice_no_grupo"]), \
                "%s mudou de lugar: %s -> %s" % (m["fonte"], (c["grupo"], c["indice_no_grupo"]),
                                                 (m["grupo"], m["grupo_indice_no_grupo"]))
    assert all(m["secao_fonte"] == SECAO_BALDE for m in mapas if m["nome"] != antes[m["fonte"]])

    # 10. warps: todo destino existe, e a ponta cai DENTRO do mapa de chegada
    pend = costura(mapas, limpos, pos, warp, conex)
    porid = {m["id_mapa"]: m for m in mapas}
    for m in mapas:
        for w in m["warp_events"]:
            d = porid[w["dest_map"]]
            i = int(w["dest_warp_id"])
            assert 0 <= i < len(d["warp_events"]), "%s: warp %d fora de %s" % (m["nome"], i, d["nome"])
            chega = d["warp_events"][i]
            assert 0 <= chega["x"] < d["w"] and 0 <= chega["y"] < d["h"], \
                "%s: chegada (%d,%d) fora de %s (%dx%d)" % (m["nome"], chega["x"], chega["y"],
                                                            d["nome"], d["w"], d["h"])
            assert 0 <= w["x"] < m["w"] and 0 <= w["y"] < m["h"], m["nome"]
    inertes = {(p["mapa"], p["warp"]) for p in pend}
    for m in mapas:                        # porta inerte aponta para si mesma
        for i, w in enumerate(m["warp_events"]):
            if (m["nome"], i) in inertes:
                assert w["dest_map"] == m["id_mapa"] and int(w["dest_warp_id"]) == i, m["nome"]

    # 11. heal location: (7,4) e chao e (7,3) e parede nos 15 Pokecenter
    pcs = acha_pokecenters(mapas, arestas)
    for m in pcs:
        b = open(f"{FONTE}/blockdata/{m['fonte']}.bin", "rb").read()
        v = struct.unpack("<%dH" % (len(b) // 2), b)
        assert (v[PC_CURA[1] * PC_DIM[0] + PC_CURA[0]] >> 10) & 3 == 0, m["nome"]
        assert (v[PC_BALCAO[1] * PC_DIM[0] + PC_BALCAO[0]] >> 10) & 3 != 0, m["nome"]
    lay = {x["id"]: x for x in json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    pc_frlg = lay["LAYOUT_POKEMON_CENTER_1F_FRLG"]
    assert (pc_frlg["width"], pc_frlg["height"]) == PC_DIM, "PC_DIM nao e a do FRLG do repo"
    novas, _fora = heal_locations(mapas, arestas)
    ja = {h["id"] for h in json.load(open(HEAL_JSON))["heal_locations"]
          if not h["id"].startswith("HEAL_LOCATION_GALAR_")}
    assert not (ja & {h["id"] for h in novas}), "heal location de Galar colide com uma existente"

    print("demo: 11 checagens passaram, 438 mapas resolvidos, %d warps, %d conexoes, "
          "%d renomeados, %d heal locations"
          % (sum(len(m["warp_events"]) for m in mapas),
             sum(len(m["connections"]) for m in mapas),
             sum(1 for m in mapas if m["nome"] != antes[m["fonte"]]), len(novas)))


# ------------------------------------------------------------------ main ----

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true")
    p.add_argument("--conferir", action="store_true")
    p.add_argument("--gravar", action="store_true")
    a = p.parse_args()
    if a.demo:
        return demo()

    validos, ts, nao_conv = le_fonte()
    mapas = resolve(validos, ts, nao_conv)
    faltando = aplica_musica(mapas)
    if faltando:
        raise SystemExit("musica sem alvo: %s" % sorted(faltando))

    limpos, pos, warp, conex, pend_conex, arestas = topologia(validos)
    renomeados, decisao = renomeia(mapas, arestas)
    grupos, ordem = aloca(mapas)
    pend_warp = costura(mapas, limpos, pos, warp, conex)
    novas_curas, curas_fora = heal_locations(mapas, arestas)

    n_warps = sum(len(m["warp_events"]) for m in mapas)
    n_conex = sum(len(m["connections"]) for m in mapas)
    g3 = {
        "warps_gravados": n_warps,
        "warps_funcionais": n_warps - len(pend_warp),
        "warps_inertes": len(pend_warp),
        "conexoes_gravadas": n_conex,
        "renomeados": renomeados,
        "balde_sem_nome": {f: n for f, (i, n, _v) in sorted(decisao.items()) if i is None},
        "heal_locations": novas_curas,
        "heal_locations_fora": [{"mapa": k, "motivo": v} for k, v in curas_fora],
        "pendencias_warp": pend_warp,
        "pendencias_conexao": pend_conex,
    }

    n_layouts = escreve_layouts(mapas, a.gravar)
    escreve_mapas(mapas, a.gravar)
    escreve_grupos(grupos, a.gravar)
    n_apelidos = escreve_mapsecs(a.gravar)
    escreve_includes(mapas, a.gravar)
    n_cura = escreve_heal(novas_curas, a.gravar)
    orfas = limpa_orfaos(mapas, a.gravar)
    censo = escreve_censo(mapas, grupos, a.gravar, g3)

    print("%d mapas, %d layouts na tabela, %d apelidos de MAPSEC, %d grupos"
          % (len(mapas), n_layouts, n_apelidos, len(ordem)))
    print("-- G3 --")
    print("  warps gravados      %5d  (%d funcionais, %d inertes com pendencia)"
          % (n_warps, n_warps - len(pend_warp), len(pend_warp)))
    print("  conexoes gravadas   %5d  (%d recusadas)" % (n_conex, len(pend_conex)))
    print("  mapas renomeados    %5d  de %d na secao-balde"
          % (len(renomeados), sum(1 for m in mapas if m["secao_fonte"] == SECAO_BALDE)))
    print("  heal locations      %5d  (tabela fica com %d)" % (len(novas_curas), n_cura))
    print("  pastas orfas        %5d" % len(orfas))
    motivos = collections.Counter(
        "destino fora dos 438 (mapa vanilla do FireRed)" if "nao esta nos 438" in p["motivo"]
        else "warp de chegada nao existe no destino" for p in pend_warp)
    for k, v in motivos.most_common():
        print("    pendencia: %-46s %4d" % (k, v))
    print("-- mapas por grupo --")
    for g, n in censo["mapas_por_grupo"].items():
        print("  %-40s %3d  (grupo fica com %d/%d)" % (g, n, len(grupos[g]), TETO_GRUPO))
    if a.conferir:
        print("-- renomeacao (amostra) --")
        for velho, novo in list(renomeados.items())[:10]:
            print("  %-24s -> %s" % (velho, novo))
        print("-- heal locations --")
        for h in novas_curas:
            print("  %-40s %s" % (h["id"], h["map"]))
    if not a.gravar:
        print("(nada gravado; use --gravar)")


if __name__ == "__main__":
    main()
