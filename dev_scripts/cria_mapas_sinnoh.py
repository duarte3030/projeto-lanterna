#!/usr/bin/env python3
"""Os mapas de Sinnoh que a fonte tem e nós não, e que não são interior de casa.

    python3 dev_scripts/cria_mapas_sinnoh.py            # só relata
    python3 dev_scripts/cria_mapas_sinnoh.py --demo     # autoteste, não grava
    python3 dev_scripts/cria_mapas_sinnoh.py --aplicar  # escreve

POR QUE UMA FERRAMENTA A MAIS, e não mais um ramo nas três que já existem
------------------------------------------------------------------------
As três de Sinnoh que criam mapa têm cada uma um recorte MEDIDO, e nenhum deles
pega estes:

- `converte_cavernas_sinnoh.py` só aceita grade com `chao_de_caverna >= 8`, e os
  quatro daqui dão ZERO (o prado de Floaroma e a fábrica do Fuego não são
  masmorra, e os nove andares do Distortion World não têm chão nenhum);
- `converte_interiores_sinnoh.py` só aceita `MAP_TYPE_INDOORS`, e o prado, a
  fábrica e os dois exteriores não são;
- `converte_moldes_sinnoh.py` reconverte mapa que JÁ existe vestindo molde, e
  aqui não existe mapa nenhum para reconverter.

Duas famílias, e a diferença entre elas é a MEDIDA, não o gosto
---------------------------------------------------------------
1. **Os quatro com grade de verdade.** Prado de Floaroma (3.044 tiles andáveis
   de 4.096), fora da Eterna Forest (664), fora do Fuego Ironworks (420) e o
   prédio do Fuego (1.348 tiles de chão liso, mais 58 de esteira). A grade 2D do
   Platinum entra INTEIRA, traduzida pelo mesmo vocabulário que o resto de
   Sinnoh já usa: `demake_ds.traduz_gen4` para exterior (grama e árvore) e
   `converte_interiores_sinnoh.traduz` para o prédio (piso, parede, mobília
   lida do comportamento do tile). Coordenada de evento entra por IDENTIDADE
   menos o canto da caixa da matriz, que é o offset que `grade_do_mapa` devolve.

2. **Os nove andares do Distortion World.** Medido em 21/08/2026 e remedido
   aqui: a grade 2D deles NÃO TEM CHÃO (95% de colisão, a maior mancha andável
   do mundo inteiro tem 10 tiles), porque o Distortion World mora no modelo 3D
   de gravidade variável. O piso é INVENÇÃO DECLARADA, igual à da sala do
   Giratina que já está na ROM desde 21/08 (`distortion_world.py`), e pela mesma
   decisão do Gui: "daria pra fazer com gravidade normal? queria o mapa", mais a
   de 22/08, "completa até ficar 100 em tudo", que aceita forma honesta com arte
   chapada. O que é da FONTE em cada andar: o TAMANHO da matriz e os tiles que a
   grade marca abertos (marcadores de pulo), por onde o corredor passa. O resto
   é corredor cavado, e está dito aqui e no `origem_geometria` de cada mapa.

Ordem, e ela importa: pai antes de filho
----------------------------------------
`FuegoIronworksBuilding` só tem porta depois que `FuegoIronworksOutside` existe,
e `FloaromaMeadowHouse` (que é interior canônico e sai pelo conversor de
interiores) só depois do prado. Por isso a lista é uma FILA, não um conjunto.

Compatibilidade de save: mapa novo entra em APPEND no fim do grupo, nunca no
meio, porque a save guarda o índice do mapa dentro do grupo. Layout novo entra
no FIM de `layouts.json` pelo mesmo motivo.
"""
import json
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import converte_cavernas_sinnoh as C        # noqa: E402
import converte_interiores_sinnoh as N      # noqa: E402
import converte_moldes_sinnoh as M          # noqa: E402
import demake_ds as D                       # noqa: E402
import fecha_portas_sinnoh as F             # noqa: E402
import importa_npcs_sinnoh as I             # noqa: E402
import valida_conectividade as VC           # noqa: E402
import valida_mapas_sinnoh as V             # noqa: E402

APLICAR = "--aplicar" in sys.argv

GRUPO_EXTERIOR = "gMapGroup_SinnohTownsRoutes"
GRUPO_CAVERNA = "gMapGroup_SinnohCavernas"
GRUPO_INTERIOR = "gMapGroup_SinnohInteriores"

# Palavra de árvore usada como borda de mapa de rua, a mesma de
# `converte_moldes_sinnoh.ARVORE_TOPO`.
BORDA_EXTERIOR = M.ARVORE_TOPO

# (header, pai da entrada). O pai é o mapa NOSSO por onde o jogador chega; ele
# sai da fonte, e não de gosto: o prado de Floaroma tem quatro warps para
# FLOAROMA_TOWN, o prédio do Fuego tem um para o pátio, e os dois exteriores
# são vizinhos de matriz do mapa citado (a fonte os liga andando, e andar entre
# mapas não existe neste motor: vira porta, declarada).
FILA = [
    ("MAP_HEADER_FLOAROMA_MEADOW", "FloaromaTown", "exterior"),
    ("MAP_HEADER_ETERNA_FOREST_OUTSIDE", "EternaForest", "exterior"),
    ("MAP_HEADER_FUEGO_IRONWORKS_OUTSIDE", "Route205_North", "exterior"),
    ("MAP_HEADER_FUEGO_IRONWORKS_BUILDING", "FuegoIronworksOutside", "predio"),
]

# Os nove andares que faltam, na ordem em que se desce. A sala do Giratina já
# está na ROM (`DistortionWorld`), e é o fundo da corrente.
DW = ["MAP_HEADER_DISTORTION_WORLD_1F",
      "MAP_HEADER_DISTORTION_WORLD_B1F",
      "MAP_HEADER_DISTORTION_WORLD_B2F",
      "MAP_HEADER_DISTORTION_WORLD_B3F",
      "MAP_HEADER_DISTORTION_WORLD_B4F",
      "MAP_HEADER_DISTORTION_WORLD_B5F",
      "MAP_HEADER_DISTORTION_WORLD_B6F",
      "MAP_HEADER_DISTORTION_WORLD_B7F"]
DW_TURNBACK = "MAP_HEADER_DISTORTION_WORLD_TURNBACK_CAVE_ROOM"
DW_GIRATINA = "DistortionWorld"          # a sala do Giratina, já na ROM

CHAO_FONTE = 0x0008     # TILE_BEHAVIOR_CAVE_FLOOR na grade CRUA do DS


# --------------------------------------------------------------- geometria
def _abertos(grade):
    """Índices que a grade da FONTE deixa abertos (sem o bit 15 de colisão)."""
    return [i for i, v in enumerate(grade) if not v & 0x8000]


def cava(grade, larg, alt, pontos, raio=1):
    """Abre chão de caverna num corredor que liga `pontos` na ordem dada.

    Só troca VAZIO por chão: tile que a fonte já deixou aberto continua como
    está, e por isso o corredor passa exatamente por cima dos marcadores dela.
    O caminho é em L (vertical e depois horizontal), que é o menor traçado que
    não precisa de heurística nenhuma.
    """
    grade = list(grade)

    def pinta(x, y):
        for dy in range(-raio, raio + 1):
            for dx in range(-raio, raio + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < larg and 0 <= ny < alt:
                    grade[ny * larg + nx] = CHAO_FONTE

    for (x0, y0), (x1, y1) in zip(pontos, pontos[1:]):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            pinta(x0, y)
        for x in range(min(x0, x1), max(x0, x1) + 1):
            pinta(x, y1)
    for x, y in pontos:
        pinta(x, y)
    return grade


def planta_dw(header):
    """(larg, alt, palavras, entrada, saida) de um andar do Distortion World.

    A entrada e a saída são os dois marcadores mais distantes que a FONTE deixou
    abertos naquele andar (empate desfeito pela ordem de leitura, que é
    determinística). Quando o andar não tem dois, o que falta cai no canto do
    corpo do mapa: continua sendo a matriz da fonte que dá o tamanho.
    """
    larg, alt, grade, _off = M.grade_do_mapa(header)
    # MARCADOR não é "tile sem o bit de colisão": a grade do DS tem milhares de
    # tiles com comportamento 0x00 e colisão 0, que é o VAZIO atrás da parede e
    # não chão (é a mesma regra que `converte_cavernas_sinnoh.traduz` usa). O
    # marcador é o que sobra depois dela: os pares de pulo e, no B3F, o mar.
    base = C.traduz(larg, alt, grade)
    pontos = [(i % larg, i // larg) for i, p in enumerate(base)
              if (p >> 10) & 3 == 0]
    if len(pontos) >= 2:
        entrada, saida = pontos[0], pontos[-1]
    elif pontos:
        entrada = pontos[0]
        saida = (larg - 1 - entrada[0], alt - 1 - entrada[1])
    else:
        entrada, saida = (larg // 4, alt // 4), (3 * larg // 4, 3 * alt // 4)
    # O corredor visita os marcadores um a um SÓ quando eles são poucos, que é o
    # caso de oito dos nove andares (1 a 152 tiles). No B3F eles são 2.822, o mar
    # inteiro, e visitá-los abriria o mapa todo: 4.096 de 4.096 andáveis, ou seja
    # uma quadra vazia de 64x64 no lugar de um andar. Lá o corredor é só o L
    # entre a escada de cima e a de baixo, e o mar da fonte fica como está.
    caminho = ([entrada] + pontos + [saida] if len(pontos) <= 64
               else [entrada, saida])
    grade = cava(grade, larg, alt, caminho)
    return larg, alt, C.traduz(larg, alt, grade), entrada, saida


# --------------------------------------------------------------- escrita
def _layouts_json():
    return json.load(open(f"{REPO}/data/layouts/layouts.json"))


def registra_layout(lay):
    """Layout novo no FIM de layouts.json. Índice que anda quebra save."""
    d = _layouts_json()
    if any(l.get("id") == lay["id"] for l in d["layouts"]):
        return
    nomes = {l.get("name") for l in d["layouts"]}
    assert lay["name"] not in nomes, lay["name"]
    d["layouts"].append(lay)
    json.dump(d, open(f"{REPO}/data/layouts/layouts.json", "w"),
              indent=2, ensure_ascii=False)
    open(f"{REPO}/data/layouts/layouts.json", "a").write("\n")
    F.layouts()[lay["id"]] = lay


def escreve_layout(pasta, header, larg, alt, palavras, caverna):
    d = f"{REPO}/data/layouts/{pasta}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/map.bin", "wb").write(
        struct.pack(f"<{len(palavras)}H", *palavras))
    borda = C.ROCHA_TOPO if caverna else BORDA_EXTERIOR
    open(f"{d}/border.bin", "wb").write(struct.pack("<4H", *([borda] * 4)))
    return {
        "id": "LAYOUT_" + F.const_do_header(header)[len("MAP_"):],
        "name": f"{pasta}_Layout",
        "width": larg, "height": alt,
        "primary_tileset": "gTileset_GeneralSinnoh",
        "secondary_tileset": ("gTileset_CaveSinnoh" if caverna
                              else "gTileset_PetalburgSinnoh"),
        "border_filepath": f"data/layouts/{pasta}/border.bin",
        "blockdata_filepath": f"data/layouts/{pasta}/map.bin",
        "layout_version": "emerald",
    }


def grava_mapa(pasta, d, trecho, grupo, incs, grupos):
    os.makedirs(f"{REPO}/data/maps/{pasta}", exist_ok=True)
    json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
              indent=2, ensure_ascii=False)
    open(f"{REPO}/data/maps/{pasta}/scripts.inc", "w").write(
        f"{pasta}_MapScripts::\n\t.byte 0\n{trecho}")
    grupos[F.grupo_com_vaga(grupos, grupo)].append(pasta)
    incs.append(f'\t.include "data/maps/{pasta}/scripts.inc"\n')


MODELO_EXTERIOR = {
    "music": "MUS_ROUTE110", "region_map_section": "MAPSEC_SINNOH_WEST",
    "requires_flash": False, "weather": "WEATHER_SUNNY",
    "map_type": "MAP_TYPE_ROUTE", "allow_cycling": True,
    "allow_escaping": False, "allow_running": True, "show_map_name": True,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
}
MODELO_CAVERNA = {
    "music": "MUS_ABNORMAL_WEATHER", "region_map_section": "MAPSEC_SINNOH_NORTH",
    "requires_flash": False, "weather": "WEATHER_NONE",
    "map_type": "MAP_TYPE_UNDERGROUND", "allow_cycling": False,
    "allow_escaping": False, "allow_running": False, "show_map_name": False,
    "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
}


# --------------------------------------------------------------- os quatro
def plano_quatro(header, tipo):
    """(larg, alt, palavras, offset, caverna) de um dos quatro com grade."""
    if tipo == "predio":
        larg, alt, grade = N.recorta(header)
        return larg, alt, N.traduz(larg, alt, grade), (0, 0), "predio"
    larg, alt, grade, off = M.grade_do_mapa(header)
    return larg, alt, D.traduz_gen4(grade, larg), off, "exterior"


def aplica_quatro(grupos, incs, sprites, movimentos, desenhadas, relato):
    for header, pai0, tipo in FILA:
        pasta = F.nome_de_pasta(header)
        if os.path.exists(f"{REPO}/data/maps/{pasta}/map.json"):
            relato.append(f"{pasta}: já existe, nada a fazer")
            continue
        if not os.path.exists(f"{REPO}/data/maps/{pai0}/map.json"):
            relato.append(f"{pasta}: PULADO, o pai {pai0} não existe")
            continue
        larg, alt, pal, off, familia = plano_quatro(header, tipo)
        pal = list(pal)
        regiao = C.regiao_principal(pal, larg, alt)
        if not regiao:
            relato.append(f"{pasta}: PULADO, a grade não tem corpo andável")
            continue
        predio = familia == "predio"

        porta = N.abre_porta(pai0, desenhadas)
        if porta is None:
            relato.append(f"{pasta}: PULADO, {pai0} não tem porta órfã nem "
                          f"parede onde desenhar uma")
            continue
        p_pai = f"{REPO}/data/maps/{pai0}/map.json"
        d_pai = json.load(open(p_pai))

        # warps: os da fonte que têm destino de verdade, mais a volta ao pai
        warps, volta = [], None
        fonte = _eventos(header)
        for w in fonte.get("warp_events") or []:
            x, y = int(w["x"]) - off[0], int(w["z"]) - off[1]
            if not (0 <= x < larg and 0 <= y < alt):
                continue
            alvo = _nosso_id(w["dest_header_id"])
            if alvo is None:
                continue
            x, y = C.poe_warp(regiao, larg, x, y)
            if any((e["x"], e["y"]) == (x, y) for e in warps):
                continue
            if alvo == d_pai["id"]:
                if volta is not None:
                    continue
                volta = len(warps)
            pal[y * larg + x] = _tile_de_warp(predio, alvo, (x, y),
                                              (larg, alt), pal)
            warps.append({"x": x, "y": y, "elevation": 0,
                          "dest_map": alvo, "dest_warp_id": "0"})
        if volta is None:
            i = min(regiao)
            x, y = i % larg, i // larg
            pal[i] = _tile_de_warp(predio, d_pai["id"], (x, y), (larg, alt), pal)
            volta = len(warps)
            warps.append({"x": x, "y": y, "elevation": 0,
                          "dest_map": d_pai["id"], "dest_warp_id": "0"})

        lay = escreve_layout(pasta, header, larg, alt, pal, predio)
        if predio:
            lay["primary_tileset"], lay["secondary_tileset"] = (
                N.PRIMARIO, N.SECUNDARIO)
            open(f"{REPO}/data/layouts/{pasta}/border.bin", "wb").write(
                struct.pack("<4H", *([N.PAREDE_TOPO] * 4)))
        registra_layout(lay)

        d = dict(MODELO_CAVERNA if predio else MODELO_EXTERIOR)
        d["id"] = F.const_do_header(header)
        d["name"] = pasta
        d["layout"] = lay["id"]
        d["connections"] = 0
        d["warp_events"] = warps
        d["coord_events"] = []
        if predio:
            d["map_type"] = "MAP_TYPE_INDOOR"
        objs, bg, trecho = F.conteudo_do_mapa(
            header, pasta, larg, alt, sprites, movimentos, lay["id"], off)
        d["object_events"] = objs
        d["bg_events"] = bg
        d["origem"] = ("pokeplatinum: geometria convertida da grade 2D "
                       "(map_data), mais NPC, placa e texto")
        d["origem_geometria"] = (
            f"cria_mapas_sinnoh.py: grade 2D do Platinum ({header}), "
            f"{larg}x{alt}, offset {off}. Mapa que a fonte tem e nós não "
            f"tínhamos")
        grava_mapa(pasta, d, trecho, GRUPO_INTERIOR if predio
                   else GRUPO_EXTERIOR, incs, grupos)

        d_pai.setdefault("warp_events", [])
        d_pai["warp_events"].append({
            "x": porta[0], "y": porta[1], "elevation": 0,
            "dest_map": d["id"], "dest_warp_id": str(volta),
            "origem": (f"entrada inventada: a fonte liga {pasta} a {pai0} "
                       f"andando pela matriz do mundo, e andar entre mapas não "
                       f"existe neste motor. Decisão de 22/08/2026")
            if not (fonte.get("warp_events") or []) else "fonte"})
        json.dump(d_pai, open(p_pai, "w"), indent=2, ensure_ascii=False)
        relato.append(f"{pasta}: {larg}x{alt}, {len(warps)} warps, "
                      f"{len(objs)} objetos, {len(bg)} placas, "
                      f"arte {M.arte(pal)}")


def _tile_de_warp(fechado, dest, pos, tamanho, pal):
    if fechado:
        return N.ESCADA
    p = M.tile_de_warp(False, dest, pos, tamanho, pal)
    return M.PORTA if p is None else p


def _eventos(header):
    arq = os.path.join(F.PLAT, "res/field/events",
                       I.headers_do_platinum()[header][0] + ".json")
    return json.load(open(arq)) if os.path.exists(arq) else {}


_IDS = None


def _nosso_id(header):
    """MAP_* do nosso mapa que casa com o header da fonte, ou None."""
    global _IDS
    if _IDS is None:
        _IDS = {}
        heads = I.headers_do_platinum()
        por_chave = {}
        for h in heads:
            por_chave.setdefault(I.chave(h), h)
        for m in I.nossos_mapas_sinnoh():
            h = I.APELIDOS.get(m) or por_chave.get(I.chave(m))
            if h in heads:
                _IDS.setdefault(h, json.load(
                    open(f"{REPO}/data/maps/{m}/map.json"))["id"])
    return _IDS.get(header)


# --------------------------------------------- os nove do Distortion World
def aplica_dw(grupos, incs, relato):
    """Cria os oito andares mais a sala da Turnback, e emenda a corrente.

    A corrente é 1F -> B1F -> ... -> B7F -> sala do Giratina, mais a sala da
    Turnback pendurada no 1F, que é como a fonte a liga. Cada andar tem DOIS
    warps: o de subir e o de descer, e por isso ninguém nasce de mão única.
    """
    ordem = DW + [DW_TURNBACK]
    plantas, novos = {}, []
    for h in ordem:
        pasta = F.nome_de_pasta(h)
        if os.path.exists(f"{REPO}/data/maps/{pasta}/map.json"):
            relato.append(f"{pasta}: já existe, nada a fazer")
            continue
        plantas[h] = planta_dw(h)
        novos.append(h)
    if not novos:
        return

    giratina = json.load(open(f"{REPO}/data/maps/{DW_GIRATINA}/map.json"))
    # quem é o vizinho de cima e de baixo de cada andar
    corrente = [h for h in DW if h in plantas]
    ids = {h: F.const_do_header(h) for h in plantas}

    for h in novos:
        pasta = F.nome_de_pasta(h)
        larg, alt, pal, entrada, saida = plantas[h]
        pal = list(pal)
        regiao = C.regiao_principal(pal, larg, alt)
        warps = []

        def poe(pos, destino):
            x, y = C.poe_warp(regiao, larg, *pos)
            if any((w["x"], w["y"]) == (x, y) for w in warps):
                return
            pal[y * larg + x] = C.ESCADA
            warps.append({"x": x, "y": y, "elevation": 0,
                          "dest_map": destino, "dest_warp_id": "0"})

        if h == DW_TURNBACK:
            poe(entrada, ids[DW[0]] if DW[0] in ids else
                _nosso_id(DW[0]) or ids[corrente[0]])
        else:
            i = corrente.index(h)
            acima = (_saida_do_mt_coronet() if i == 0
                     else ids[corrente[i - 1]])
            abaixo = (ids[corrente[i + 1]] if i + 1 < len(corrente)
                      else giratina["id"])
            poe(entrada, acima)
            poe(saida, abaixo)
            if i == 0 and DW_TURNBACK in plantas:
                # a sala da Turnback pendura no 1F, como na fonte
                livre = sorted(regiao)[len(regiao) // 2]
                poe((livre % larg, livre // larg), ids[DW_TURNBACK])

        lay = escreve_layout(pasta, h, larg, alt, pal, True)
        registra_layout(lay)
        d = dict(MODELO_CAVERNA)
        d["id"] = ids[h]
        d["name"] = pasta
        d["layout"] = lay["id"]
        d["connections"] = 0
        d["warp_events"] = warps
        d["object_events"] = []
        d["bg_events"] = []
        d["coord_events"] = []
        d["origem_geometria"] = (
            f"cria_mapas_sinnoh.py: a grade 2D do Platinum ({h}) tem "
            f"{len(_abertos(M.grade_do_mapa(h)[2]))} tiles abertos e NENHUM "
            f"chão, porque o Distortion World mora no modelo 3D de gravidade "
            f"variável. O tamanho {larg}x{alt} e os tiles por onde o corredor "
            f"passa são da fonte; o PISO é invenção declarada, decisão do Gui "
            f"em 21/08/2026 (o mapa) e 22/08/2026 (completar até 100)")
        grava_mapa(pasta, d, "", GRUPO_CAVERNA, incs, grupos)
        relato.append(f"{pasta}: {larg}x{alt}, {len(warps)} warps, "
                      f"arte {M.arte(pal)}")

    # a sala do Giratina ganha a escada de subida para o B7F
    ultimo = ids.get(corrente[-1]) if corrente else None
    if ultimo and not any(w["dest_map"] == ultimo
                          for w in giratina.get("warp_events") or []):
        lay = F.layouts()[giratina["layout"]]
        blk = bytearray(open(f"{REPO}/{lay['blockdata_filepath']}", "rb").read())
        larg = lay["width"]
        pal = [blk[i] | (blk[i + 1] << 8) for i in range(0, len(blk), 2)]
        regiao = C.regiao_principal(pal, larg, lay["height"])
        i = max(regiao)
        x, y = i % larg, i // larg
        struct.pack_into("<H", blk, i * 2, C.ESCADA)
        open(f"{REPO}/{lay['blockdata_filepath']}", "wb").write(bytes(blk))
        giratina.setdefault("warp_events", []).append({
            "x": x, "y": y, "elevation": 0, "dest_map": ultimo,
            "dest_warp_id": "1",
            "origem": "escada de volta para o B7F, aberta em 22/08/2026"})
        json.dump(giratina,
                  open(f"{REPO}/data/maps/{DW_GIRATINA}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        relato.append(f"{DW_GIRATINA}: escada nova para {ultimo} em ({x},{y})")


def _saida_do_mt_coronet():
    """Destino do warp de saída do 1F: o que a FONTE manda, se existir aqui."""
    for w in _eventos(DW[0]).get("warp_events") or []:
        alvo = _nosso_id(w["dest_header_id"])
        if alvo:
            return alvo
    return _nosso_id("MAP_HEADER_SPEAR_PILLAR") or "MAP_SPEAR_PILLAR"


# ------------------------------------------------- simetria dos warps
# O warp N do andar X tem que levar ao warp PAR do andar X±1, e esse par tem que
# devolver ao N. Até 22/08/2026 todo `dest_warp_id` da corrente era "0" (é o que
# `poe` escreve na criação, porque nessa hora o mapa de destino ainda nem tem
# warp), e quem subia caía sempre no PRIMEIRO warp do andar de cima, que é a
# escada de subida DELE e não o par. Ninguém ficava preso, mas o tile de chegada
# era o errado. O conserto mora aqui, e não numa ferramenta à parte, porque o
# `--aplicar` não recria mapa que já existe: sem este passo o defeito ficaria
# congelado nos nove andares para sempre.


def pares(warps_por_mapa):
    """{(mapa, i): "j"} do warp PAR de cada warp que tem volta.

    O par do i-ésimo warp de A para B é o i-ésimo warp de B para A. Escrito
    assim ele é simétrico POR CONSTRUÇÃO (o mesmo `zip` produz (A,i)->j e
    (B,j)->i) e determinístico quando há mais de um warp entre o mesmo par de
    mapas. Warp cujo destino não volta fica de FORA: só entra quem tem par de
    verdade, e o que sobra é dito em voz alta em `simetriza`.
    """
    idx = {}
    for a, ws in warps_por_mapa.items():
        for i, w in enumerate(ws):
            idx.setdefault((a, w.get("dest_map")), []).append(i)
    saida = {}
    for (a, b), meus in idx.items():
        for i, j in zip(meus, idx.get((b, a)) or []):
            saida[(a, i)] = str(j)
    return saida


def assimetricos(warps_por_mapa, familia):
    """(mapa, i, tem, devia) de todo warp da `familia` apontado para o índice
    errado. Lista vazia quer dizer corrente simétrica."""
    p = pares(warps_por_mapa)
    ruins = []
    for m in familia:
        for i, w in enumerate(warps_por_mapa.get(m) or []):
            devia = p.get((m, i))
            if devia is not None and str(w.get("dest_warp_id")) != devia:
                ruins.append((m, i, str(w.get("dest_warp_id")), devia))
    return ruins


def familia_dw():
    """Os MAP_* da corrente: os nove andares novos mais a sala do Giratina."""
    ids = [F.const_do_header(h) for h in DW + [DW_TURNBACK]]
    p = f"{REPO}/data/maps/{DW_GIRATINA}/map.json"
    if os.path.exists(p):
        ids.append(json.load(open(p))["id"])
    return ids


def _warps_do_repo():
    """(mapas do repo, {MAP_*: lista de warps}). Leitura, não escreve nada."""
    mapas = VC.carrega()
    return mapas, {k: (v["dados"].get("warp_events") or [])
                   for k, v in mapas.items()}


def simetriza(relato):
    """Reescreve só `dest_warp_id` dos mapas da corrente. Idempotente.

    Não toca em `map.bin`, não cria warp e não reordena a lista: a save guarda
    a POSIÇÃO do jogador, mas os casos gravados da suíte entram por ÍNDICE de
    warp, então mover um warp de lugar invalidaria caso verde.
    """
    mapas, ws = _warps_do_repo()
    familia = [m for m in familia_dw() if m in mapas]
    por_mapa = {}
    for m, i, tem, devia in assimetricos(ws, familia):
        por_mapa.setdefault(m, []).append((i, tem, devia))
    for m, itens in por_mapa.items():
        d = mapas[m]["dados"]
        for i, _tem, devia in itens:
            d["warp_events"][i]["dest_warp_id"] = devia
        json.dump(d, open(f"{REPO}/data/maps/{mapas[m]['dir']}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        relato.append(f"{mapas[m]['dir']}: " + ", ".join(
            f"warp {i} {tem}->{devia}" for i, tem, devia in itens))
    p = pares(ws)
    for m in familia:
        for i, w in enumerate(ws[m]):
            if (m, i) not in p:
                relato.append(f"{mapas[m]['dir']}: warp {i} para "
                              f"{w['dest_map']} NÃO tem par (o destino não "
                              f"volta), fica em {w['dest_warp_id']}")
    if not por_mapa:
        relato.append("simetria: nada a mudar, a corrente já é simétrica")
    return sum(len(v) for v in por_mapa.values())


# --------------------------------------------------------------- relatório
def relatorio():
    print(f"{'mapa':34s} {'tamanho':>9s} {'KB':>6s} {'andáveis':>9s}  fonte")
    for header, pai, tipo in FILA:
        pasta = F.nome_de_pasta(header)
        larg, alt, pal, off, _f = plano_quatro(header, tipo)
        marca = "JÁ EXISTE" if os.path.exists(
            f"{REPO}/data/maps/{pasta}/map.json") else f"entra por {pai}"
        print(f"{pasta:34s} {larg}x{alt:<6d} {larg*alt*2/1024:6.1f} "
              f"{C.andaveis(pal):9d}  {marca}")
    for h in DW + [DW_TURNBACK]:
        pasta = F.nome_de_pasta(h)
        larg, alt, pal, _e, _s = planta_dw(h)
        marca = "JÁ EXISTE" if os.path.exists(
            f"{REPO}/data/maps/{pasta}/map.json") else "corredor cavado"
        print(f"{pasta:34s} {larg}x{alt:<6d} {larg*alt*2/1024:6.1f} "
              f"{C.andaveis(pal):9d}  {marca}")
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    if not APLICAR:
        relatorio()
        print("\nnada escrito (use --aplicar)")
        return 0

    sprites = V.sprites_utilizaveis()
    movimentos = V.constantes("include/constants/event_object_movement.h",
                              "MOVEMENT_TYPE_")
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    for g in (GRUPO_EXTERIOR, GRUPO_CAVERNA, GRUPO_INTERIOR):
        F.grupo_com_vaga(grupos, g)
    incs, desenhadas, relato = [], {}, []
    aplica_quatro(grupos, incs, sprites, movimentos, desenhadas, relato)
    aplica_dw(grupos, incs, relato)
    simetriza(relato)
    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
    voltas = C.casa_voltas()
    for l in relato:
        print("  ", l)
    print(f"\naplicado: {len(incs)} mapas novos, {voltas} voltas de escada "
          f"apontadas para o degrau certo")
    return 0


# --------------------------------------------------------------- autoteste
def demo():
    """O que prova que o mapa novo é mapa, e não máscara de colisão."""
    # 1. os quatro com grade têm corpo andável de verdade, e ele é a MAIOR
    #    mancha: mapa cujo corpo principal é minúsculo é grade vazia.
    for header, _pai, tipo in FILA:
        larg, alt, pal, _off, _f = plano_quatro(header, tipo)
        regiao = C.regiao_principal(pal, larg, alt)
        assert len(regiao) >= 30, (header, len(regiao))
        assert C.andaveis(pal) >= 100, (header, C.andaveis(pal))

    # 2. o corredor do Distortion World LIGA a entrada à saída. É o portão que
    #    separa "cavei chão" de "cavei dois buracos sem passagem entre eles".
    for h in DW + [DW_TURNBACK]:
        larg, alt, pal, entrada, saida = planta_dw(h)
        regiao = C.regiao_principal(pal, larg, alt)
        assert entrada[1] * larg + entrada[0] in regiao, (h, "entrada")
        assert saida[1] * larg + saida[0] in regiao, (h, "saída")

    # 3. `cava` é IDEMPOTENTE e só ABRE: rodar duas vezes dá a mesma grade, e
    #    nenhum tile que a fonte deixou aberto vira parede.
    larg, alt, grade, _o = M.grade_do_mapa(DW[1])
    a = cava(grade, larg, alt, [(5, 5), (20, 20)])
    b = cava(a, larg, alt, [(5, 5), (20, 20)])
    assert a == b
    for i, v in enumerate(grade):
        if not v & 0x8000:
            assert not a[i] & 0x8000, i

    # 4. a mutação plantada TEM que ser pega: um corredor que não sai do lugar
    #    deixa entrada e saída em manchas diferentes.
    larg, alt, grade, _o = M.grade_do_mapa(DW[2])
    ruim = cava(grade, larg, alt, [(2, 2)])
    ruim = cava(ruim, larg, alt, [(60, 60)])
    pal = C.traduz(larg, alt, ruim)
    reg = C.regiao_principal(pal, larg, alt)
    assert not (2 * larg + 2 in reg and 60 * larg + 60 in reg), \
        "a mutação de corredor partido passou despercebida"

    # 5. o tile debaixo de todo warp de exterior tem comportamento de warp, lido
    #    da tabela do tileset e não do número decorado.
    for p in (M.PORTA,) + tuple(M.SETA.values()):
        c = M.comportamento(p & 0x3FF, "gTileset_GeneralSinnoh",
                            "gTileset_PetalburgSinnoh")
        assert "WARP" in c or "DOOR" in c, (hex(p), c)

    # 6. nenhum alvo desta ferramenta pode estar FORA do escopo: a régua é a
    #    mesma que mede, `completude.CORTES_DO_GUI`.
    import completude as CP
    rx, _d = CP.cortes_da_regiao("Sinnoh")
    for h in [x[0] for x in FILA] + DW + [DW_TURNBACK]:
        assert not (rx and rx.search(h)), h

    # 7. a corrente do Distortion World é SIMÉTRICA no disco: o warp N do
    #    andar X leva ao par no andar X±1, e esse par devolve ao N. Olha o
    #    disco de propósito, porque o invariante é do repo e não do plano: o
    #    `--aplicar` não recria mapa que já existe, então plano verde com disco
    #    torto seria mentira (foi o defeito dos dois `--demo` de 22/08/2026).
    mapas, ws = _warps_do_repo()
    familia = [m for m in familia_dw() if m in mapas]
    assert familia, "a corrente do Distortion World não está no disco"
    assert not assimetricos(ws, familia), assimetricos(ws, familia)

    # 8. a mutação plantada TEM que reprovar: um par assimétrico, escrito à
    #    mão no primeiro warp com par da corrente, e só na cópia em memória.
    alvo = next((m, i) for m in familia for i in range(len(ws[m]))
                if (m, i) in pares(ws))
    torto = {k: [dict(w) for w in v] for k, v in ws.items()}
    w = torto[alvo[0]][alvo[1]]
    w["dest_warp_id"] = str(int(w["dest_warp_id"]) + 1)
    assert assimetricos(torto, familia), \
        "a mutação de par assimétrico passou despercebida"

    # 9. `pares` é simétrico por construção: se (A,i) aponta para j, (B,j)
    #    aponta de volta para i. É o que separa "consertei um lado" de
    #    "consertei o par".
    p = pares(ws)
    for (a, i), j in p.items():
        b = ws[a][i]["dest_map"]
        assert p.get((b, int(j))) == str(i), (a, i, b, j)

    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
