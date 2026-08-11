#!/usr/bin/env python3
"""Converte a geometria de verdade das cavernas de Sinnoh, do DS para map.bin.

    python3 dev_scripts/converte_cavernas_sinnoh.py            # so relata
    python3 dev_scripts/converte_cavernas_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/converte_cavernas_sinnoh.py --demo     # autoteste

Por que este e diferente de `fecha_portas_sinnoh.py`
----------------------------------------------------
Aquele REAPROVEITA planta: casa, mart e centro Pokemon do repo com o NPC certo
por cima. Para caverna isso mentiria o mapa, entao aqui a planta e CONVERTIDA:
sai da grade 2D de 32x32 que o Platinum guarda em
`res/field/maps/data/map_data_NNN.bin`, a mesma que `demake_ds.py` ja lia.

E ela funciona para caverna justamente onde falhava para casa: **a geometria de
uma caverna E a colisao dela**. Casa tem parede, balcao, mesa e porta desenhados
no tileset, e nada disso esta na grade; labirinto de pedra e so cheio e vazio.
Medido em Wayward Cave 1F (matriz 3x2, 96x64): sai o labirinto inteiro, com os
corredores e as camaras no lugar.

O que a grade diz, tile a tile
------------------------------
u16 por tile: bit 15 = colisao, bits 0..7 = comportamento (enum TileBehavior do
pokeplatinum). Nos 24 mapas convertidos aqui aparecem 54 mil tiles, e a leitura
e esta:

- `0x08` TILE_BEHAVIOR_CAVE_FLOOR, sem colisao: chao de caverna. 4571 tiles.
- `0x00` COM colisao: rocha. 31089 tiles.
- `0x00` SEM colisao: **vazio fora do mapa**, nao chao. Na gen 4 e a area que o
  modelo 3D nem desenha, e o jogador nunca alcanca porque esta atras da rocha.
  15161 tiles. Traduzir isso como chao encheria a caverna de salao vazio, entao
  aqui vira rocha tambem. Esta e a unica regra do script que nao sai direto do
  dado: ela sai de o dado nao cobrir o caso.
- agua (`0x10`, `0x15`, `0x16`, `0x17`): poca de caverna, elevacao 1.
- qualquer outro comportamento sem colisao: chao.

Parede com duas faces, nao um bloco so
--------------------------------------
Rocha desenhada com um metatile so vira mancha chapada. Os metatiles saem
medidos dos mapas de caverna que o repo JA tem (`MtCoronet_1F_South`,
`MtCoronet_B1F`): 753 e a rocha vista de cima e 761 e a face que aparece quando
ha chao logo abaixo; 752/754 e 760/762 sao as pontas esquerda e direita. A regra
e a mesma que o mapa a mao usa: face se o tile de baixo e andavel, topo se nao,
e ponta se o vizinho lateral e andavel.

Warp
----
Coordenada de warp de caverna no Platinum e LOCAL da matriz do proprio mapa (a
matriz do dungeon comeca em 0,0, ao contrario da matriz do mundo, que e global e
nao tem offset que alinhe). Entao o warp entra na coordenada da fonte, e o tile
embaixo dele recebe o metatile de saida de caverna (519, comportamento 101) ou
de escada (575, comportamento 97), tambem medidos dos mapas de caverna do repo.

So entra o warp cujo destino existe: o mapa pai ou outra caverna desta mesma
leva. Warp para header que nao temos e descartado em vez de virar link quebrado.

Compatibilidade de save: grupo novo no FIM de `group_order`, mapa novo no fim
dele, warp novo no FIM da lista do mapa pai. Nenhum indice antigo anda.
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import demake_ds as D                # noqa: E402
import fecha_portas_sinnoh as F      # noqa: E402
import importa_npcs_sinnoh as I      # noqa: E402
import valida_mapas_sinnoh as V      # noqa: E402
import valida_warp_tile as W         # noqa: E402

PLAT = F.PLAT
APLICAR = "--aplicar" in sys.argv
GRUPO = "gMapGroup_SinnohCavernas"

# Palavras de 16 bits medidas nos mapas de caverna que o repo ja tem. Nenhuma
# foi escolhida de cabeca: ver o cabecalho.
CHAO = 0x3201        # metatile 513, colisao 0, elevacao 3, comportamento 8
AGUA = 0x10A1        # metatile 161, colisao 0, elevacao 1, MB_POND_WATER
ROCHA_TOPO = 0x6F1   # metatile 753, colisao 1, elevacao 0
ROCHA_FACE = 0x6F9   # metatile 761, a mesma rocha com chao logo abaixo
SAIDA = 0x3207       # metatile 519, comportamento 101: boca de caverna
ESCADA = 0x323F      # metatile 575, comportamento 97: escada entre andares

AGUAS = (0x10, 0x13, 0x15, 0x16, 0x17)

# Mapa nosso -> quantos warps ele ja tem. Cada caverna precisa de UM tile de
# porta livre no pai; sem ele o mapa nao teria entrada e nao e criado.


# ------------------------------------------------------------- header do DS
_HEADERS = None


def headers():
    """MAP_HEADER_X -> dict com os campos do `include/data/map_headers.h`."""
    global _HEADERS
    if _HEADERS is None:
        txt = open(os.path.join(PLAT, "include/data/map_headers.h")).read()
        _HEADERS = {}
        for nome, corpo in re.findall(r"\[(MAP_HEADER_\w+)\] = \{(.*?)\n    \}",
                                      txt, re.S):
            _HEADERS[nome] = dict(
                re.findall(r"\.(\w+)\s*=\s*([^,\n]+)", corpo))
    return _HEADERS


def grade_do_header(header):
    """(largura, altura, grade crua) juntando os pedacos de 32x32 da matriz."""
    n = int(headers()[header]["mapMatrixID"].split("_")[-1])
    m = json.load(open(os.path.join(
        PLAT, f"res/field/matrices/map_matrix_{n:03d}.json")))
    linhas = m.get("maps") or []
    if not linhas:
        return 0, 0, []
    lc, ac = len(linhas[0]), len(linhas)
    larg, alt = lc * D.LADO, ac * D.LADO
    grade = [0] * (larg * alt)
    for cy, linha in enumerate(linhas):
        for cx, nome in enumerate(linha):
            pedaco = D.grade_gen4(int(nome.split("_")[1]))
            for i, v in enumerate(pedaco):
                grade[(cy * D.LADO + i // D.LADO) * larg
                      + cx * D.LADO + i % D.LADO] = v
    return larg, alt, grade


# ------------------------------------------------------------- traducao
def traduz(larg, alt, grade):
    """Grade crua de caverna -> lista de palavras do pokeemerald."""
    def andavel(i):
        bruto = grade[i]
        if bruto & 0x8000:
            return False
        return (bruto & 0xFF) != 0x00      # 0x00 sem colisao e vazio, nao chao

    saida = []
    for y in range(alt):
        for x in range(larg):
            i = y * larg + x
            if andavel(i):
                saida.append(AGUA if (grade[i] & 0xFF) in AGUAS else CHAO)
                continue
            abaixo = y + 1 < alt and andavel(i + larg)
            base = ROCHA_FACE if abaixo else ROCHA_TOPO
            esq = x > 0 and andavel(i - 1)
            dir_ = x + 1 < larg and andavel(i + 1)
            if esq and not dir_:
                base -= 1
            elif dir_ and not esq:
                base += 1
            saida.append(base)
    return saida


def regiao_principal(pal, larg, alt):
    """Indices da MAIOR mancha andavel conexa do mapa.

    E o corpo da caverna. Tudo que fica fora dela e bolsao solto, e a boca da
    caverna da gen 4 quase sempre e um: la a passagem da entrada para a camara e
    desenhada no modelo 3D e a grade 2D nao a liga. Medido: nas tres cavernas de
    lago o tile de warp da fonte tem os QUATRO vizinhos de pedra, ou seja, o
    jogador chegaria preso.
    """
    andavel = [(p >> 10) & 3 == 0 for p in pal]
    visto, melhor = set(), []
    for ini in range(len(pal)):
        if not andavel[ini] or ini in visto:
            continue
        pilha, comp = [ini], []
        visto.add(ini)
        while pilha:
            i = pilha.pop()
            comp.append(i)
            x, y = i % larg, i // larg
            for j, ok in ((i - 1, x > 0), (i + 1, x + 1 < larg),
                          (i - larg, y > 0), (i + larg, y + 1 < alt)):
                if ok and j not in visto and andavel[j]:
                    visto.add(j)
                    pilha.append(j)
        if len(comp) > len(melhor):
            melhor = comp
    return set(melhor)


def poe_warp(regiao, larg, x, y):
    """Coordenada onde o warp pode nascer sem trancar o jogador.

    Fica onde esta se ja for parte do corpo da caverna; senao anda para o tile
    mais proximo que seja, o que mantem o lado certo da caverna sem cavar buraco
    no meio da pedra.
    """
    if y * larg + x in regiao:
        return x, y
    return min(((i % larg, i // larg) for i in regiao),
               key=lambda c: (c[0] - x) ** 2 + (c[1] - y) ** 2)


def andaveis(palavras):
    return sum(1 for p in palavras if (p >> 10) & 3 == 0)


# Chao de masmorra, na grade CRUA do DS. Os tres sao vizinhos no MESMO enum
# `TileBehavior` do pokeplatinum
# (`include/constants/field/map_tile_behaviors.h`), e a regra so contava o
# primeiro. Isso deixava de fora masmorra que nao e caverna de pedra: os cinco
# andares da Lost Tower da Route 209 e a sala do fundo do Old Chateau sao
# `OLD_CHATEAU_FLOOR`, nao `CAVE_FLOOR`, e o mapa deles esta na grade do mesmo
# jeito. Medido em 06/08/2026: Lost Tower 1F tem 123 tiles de 0x0B e ZERO de
# 0x08, e por isso era reprovada como "nao e caverna de verdade".
CHAO_MASMORRA = (0x08,   # TILE_BEHAVIOR_CAVE_FLOOR
                 0x0B,   # TILE_BEHAVIOR_OLD_CHATEAU_FLOOR
                 0x0C)   # TILE_BEHAVIOR_MOUNTAIN_FLOOR


def chao_de_caverna(grade):
    """Tiles de chao de masmorra sem colisao, na grade CRUA do DS.

    E o unico sinal que separa masmorra de verdade de mapa que so esta marcado
    MAP_TYPE_CAVE ou MAP_TYPE_INDOORS no Platinum. Contar tile andavel nao
    separa: mede o tamanho da sala, e sala pequena de verdade existe.
    """
    return sum(1 for v in grade
               if not v & 0x8000 and (v & 0xFF) in CHAO_MASMORRA)


# ------------------------------------------------------------- escrita
def nome_de_pasta(header):
    return F.nome_de_pasta(header)


def escreve_layout(pasta, header, larg, alt, palavras):
    d = f"{REPO}/data/layouts/{pasta}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/map.bin", "wb").write(struct.pack(f"<{len(palavras)}H", *palavras))
    open(f"{d}/border.bin", "wb").write(struct.pack("<4H", *([ROCHA_TOPO] * 4)))
    # o id sai do HEADER, nao do nome da pasta: separar "WaywardCave1F" em
    # palavras daria LAYOUT_WAYWARD_CAVE1_F, que nao casa com nada. Sai pelo
    # `const_do_header` para herdar o prefixo de `F.RENOMEADOS`: sem isso a
    # Victory Road de Sinnoh escreveria LAYOUT_VICTORY_ROAD_1F, que ja e de
    # Hoenn, e o build morreria com simbolo repetido.
    lid = "LAYOUT_" + F.const_do_header(header)[len("MAP_"):]
    return {
        "id": lid, "name": f"{pasta}_Layout",
        "width": larg, "height": alt,
        "primary_tileset": "gTileset_GeneralSinnoh",
        "secondary_tileset": "gTileset_CaveSinnoh",
        "border_filepath": f"data/layouts/{pasta}/border.bin",
        "blockdata_filepath": f"data/layouts/{pasta}/map.bin",
        "layout_version": "emerald",
    }


# ------------------------------------------------------------- main
def alvos():
    """(pai, header) das cavernas que faltam, na ordem da fonte."""
    heads = I.headers_do_platinum()
    por_chave = {}
    for h in heads:
        por_chave.setdefault(I.chave(h), h)
    casados = {}
    for m in I.nossos_mapas_sinnoh():
        h = I.APELIDOS.get(m) or por_chave.get(I.chave(m))
        if h in heads:
            casados[h] = m
    existentes = set(casados) | F.JA_TEMOS
    pastas = set(os.listdir(f"{REPO}/data/maps"))
    consts = set(re.findall(r'"id":\s*"(MAP_\w+)"', "".join(
        open(f"{REPO}/data/maps/{p}/map.json").read() for p in pastas
        if os.path.exists(f"{REPO}/data/maps/{p}/map.json"))))
    saida, vistos = [], set()
    for header, meu in sorted(casados.items(), key=lambda kv: kv[1]):
        pe = os.path.join(PLAT, "res/field/events", heads[header][0] + ".json")
        if not os.path.exists(pe):
            continue
        for w in json.load(open(pe)).get("warp_events", []):
            d = w["dest_header_id"]
            if d in existentes or d in vistos:
                continue
            # `mapType` e a regua GROSSA, e sozinha ela erra dos dois lados:
            # FLOAROMA_MEADOW esta marcado CAVE e e um prado, e a Lost Tower
            # esta marcada INDOORS e e masmorra. Quem decide e o chao de
            # masmorra na grade, la embaixo. Aqui so fica de fora OUTDOORS, por
            # decisao: exterior de gen 4 tem cenario DESENHADO que a grade 2D
            # nao guarda, e converter isso encheria a rua de pedra.
            if headers().get(d, {}).get("mapType") not in (
                    "MAP_TYPE_CAVE", "MAP_TYPE_INDOORS"):
                continue
            pasta = nome_de_pasta(d)
            if pasta in pastas or F.const_do_header(d) in consts:
                continue
            vistos.add(d)
            saida.append((meu, d))
    return saida


def main():
    if "--demo" in sys.argv:
        return demo()

    heads = I.headers_do_platinum()
    pend = alvos()
    convertidos = {}
    for _pai, header in pend:
        larg, alt, grade = grade_do_header(header)
        if not grade:
            continue
        pal = traduz(larg, alt, grade)
        # A grade nao e de caverna = fica de fora. Medido: FLOAROMA_MEADOW esta
        # marcado MAP_TYPE_CAVE no Platinum mas e o prado das colmeias.
        # A regra era "menos de 30 tiles andaveis", e ela reprovava as 11 salas
        # sem saida das Solaceon Ruins, que sao camaras de 10 a 13 tiles de
        # verdade: 32x32 quase todo pedra com uma sala pequena no meio e o mapa
        # como o Platinum o desenhou, nao grade vazia. Contar tile andavel media
        # o TAMANHO da sala, que nao e o que interessa.
        # A regra honesta e a que o cabecalho ja explica: masmorra e o que tem
        # chao de masmorra (`CHAO_MASMORRA`). Medido nos destinos que faltam:
        # Solaceon tem 10 a 13, Victory Road 1F tem 817, Lost Tower 84 a 123, e
        # FLOAROMA_MEADOW, CELESTIC_TOWN_CAVE, o ginasio de Hearthome, o Vista
        # Lighthouse e a sala de ranking da Jubilife TV tem ZERO, que e o que os
        # mantem de fora mesmo agora que MAP_TYPE_INDOORS passa.
        if chao_de_caverna(grade) < 8:
            continue
        convertidos[header] = (larg, alt, pal)

    # quem tem porta livre no pai entra; quem nao tem fica de fora inteiro,
    # porque caverna sem entrada e peso morto na ROM.
    livres = {}
    planos, fora = [], []
    for pai, header in pend:
        if header not in convertidos:
            fora.append((header, "grade sem chao de caverna: nao e caverna de verdade"))
            continue
        if pai not in livres:
            livres[pai] = F.portas_livres(pai)
        if not livres[pai]:
            fora.append((header, f"{pai} nao tem porta orfa para a entrada"))
            continue
        planos.append((pai, header, livres[pai].pop(0)))

    print(f"cavernas que faltam: {len(pend)}")
    print(f"geometria convertida do DS: {len(convertidos)}")
    print(f"com entrada, entram na ROM: {len(planos)}")
    for h, m in fora:
        print(f"   {h.replace('MAP_HEADER_', '')}: {m}")
    for h, (larg, alt, pal) in sorted(convertidos.items()):
        print(f"   {h.replace('MAP_HEADER_', ''):40} {larg}x{alt} "
              f"{andaveis(pal)} tiles andaveis")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        return 0

    sprites = V.sprites_utilizaveis()
    movimentos = V.constantes("include/constants/event_object_movement.h",
                              "MOVEMENT_TYPE_")
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    F.grupo_com_vaga(grupos, GRUPO)
    layouts = json.load(open(f"{REPO}/data/layouts/layouts.json"))
    modelo = json.load(open(f"{REPO}/data/maps/MtCoronet_1F_South/map.json"))
    incs = []
    conta = {"mapas": 0, "npcs": 0, "placas": 0, "textos": 0, "warps": 0}
    nossos_const = {h: F.const_do_header(h) for h in convertidos}

    for pai, header, porta in planos:
        pasta = nome_de_pasta(header)
        larg, alt, pal = convertidos[header]
        pal = list(pal)

        # --- warps: so os que tem destino de verdade
        arq = os.path.join(PLAT, "res/field/events",
                           heads[header][0] + ".json")
        fonte = json.load(open(arq)) if os.path.exists(arq) else {}
        p_pai = f"{REPO}/data/maps/{pai}/map.json"
        d_pai = json.load(open(p_pai))
        regiao = regiao_principal(pal, larg, alt)
        warps, volta_para_o_pai = [], None
        for w in fonte.get("warp_events", []):
            x, y = int(w["x"]), int(w["z"])
            if not (0 <= x < larg and 0 <= y < alt):
                continue
            d = w["dest_header_id"]
            if d in nossos_const:
                destino, saida_tile = nossos_const[d], ESCADA
            elif volta_para_o_pai is None:
                destino, saida_tile = d_pai["id"], SAIDA
            else:
                continue
            x, y = poe_warp(regiao, larg, x, y)
            if any((e["x"], e["y"]) == (x, y) for e in warps):
                continue
            pal[y * larg + x] = saida_tile
            if destino == d_pai["id"]:
                volta_para_o_pai = len(warps)
            warps.append({"x": x, "y": y, "elevation": 0,
                          "dest_map": destino, "dest_warp_id": "0"})
        if volta_para_o_pai is None:
            # nenhuma boca de caverna na fonte cai no pai: abre uma no primeiro
            # tile andavel, senao a caverna nao devolve o jogador.
            i = min(regiao)
            x, y = i % larg, i // larg
            pal[i] = SAIDA
            volta_para_o_pai = len(warps)
            warps.append({"x": x, "y": y, "elevation": 0,
                          "dest_map": d_pai["id"], "dest_warp_id": "0"})

        lay = escreve_layout(pasta, header, larg, alt, pal)
        layouts["layouts"].append(lay)
        # o cache de `fecha_portas_sinnoh` foi carregado antes deste layout
        # existir, e `conteudo_do_mapa` consulta ele para empurrar NPC que caiu
        # em tile bloqueado. Sem esta linha o mapa novo estoura em KeyError.
        F.layouts()[lay["id"]] = lay

        d = dict(modelo)
        # o modelo e MtCoronet_1F_South: as conexoes dele sao com Route207 e
        # Route208 e herdar isso emendaria a caverna nova na rota errada.
        d.pop("connections", None)
        d["id"] = F.const_do_header(header)
        d["name"] = pasta
        d["layout"] = lay["id"]
        d["warp_events"] = warps
        d["coord_events"] = []
        objs, bg, trecho = F.conteudo_do_mapa(
            header, pasta, larg, alt, sprites, movimentos, lay["id"])
        d["object_events"] = objs
        d["bg_events"] = bg
        d["origem"] = ("pokeplatinum: geometria convertida da grade 2D "
                       "(map_data), mais NPC, placa e texto")
        os.makedirs(f"{REPO}/data/maps/{pasta}", exist_ok=True)
        json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        open(f"{REPO}/data/maps/{pasta}/scripts.inc", "w").write(
            f"{pasta}_MapScripts::\n\t.byte 0\n{trecho}")
        # o grupo enche em 128 (s8 mapNum): passou disso, vai para o proximo
        grupos[F.grupo_com_vaga(grupos, GRUPO)].append(pasta)
        incs.append(f'\t.include "data/maps/{pasta}/scripts.inc"\n')

        d_pai.setdefault("warp_events", [])
        d_pai["warp_events"].append({
            "x": porta[0], "y": porta[1], "elevation": 0,
            "dest_map": d["id"], "dest_warp_id": str(volta_para_o_pai)})
        json.dump(d_pai, open(p_pai, "w"), indent=2, ensure_ascii=False)
        conta["mapas"] += 1
        conta["npcs"] += len(objs)
        conta["placas"] += len(bg)
        conta["textos"] += trecho.count(".string")
        conta["warps"] += len(warps) + 1

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    json.dump(layouts, open(f"{REPO}/data/layouts/layouts.json", "w"),
              indent=2, ensure_ascii=False)
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
    conta["voltas"] = casa_voltas()
    print(f"\naplicado: {conta['mapas']} cavernas, {conta['warps']} warps, "
          f"{conta['voltas']} voltas de escada apontadas para o degrau certo, "
          f"{conta['npcs']} NPCs, {conta['placas']} placas, "
          f"{conta['textos']} textos do Platinum")
    return 0


def _mapas_convertidos():
    """pasta -> map.json de todo mapa que ESTA ferramenta escreveu."""
    saida = {}
    for pasta in sorted(os.listdir(f"{REPO}/data/maps")):
        arq = f"{REPO}/data/maps/{pasta}/map.json"
        if not os.path.exists(arq):
            continue
        d = json.load(open(arq))
        if "geometria convertida" in (d.get("origem") or ""):
            saida[pasta] = d
    return saida


def casa_voltas():
    """Aponta cada warp de mapa convertido para o DEGRAU que devolve, nao para 0.

    O `dest_warp_id` sai "0" de fabrica aqui porque, no laco que escreve, o mapa
    do outro lado da escada ainda nao existe. So que "0" e a SAIDA da caverna:
    quem descia do 2F para o 1F era cuspido para fora do mapa inteiro, em vez de
    cair no degrau de cima do 1F. Medido em 06/08/2026 na Victory Road de Sinnoh
    e na Lost Tower: warp que existe, dispara, e leva ao lugar errado, que e a
    licao 4.1 do ESTADO por inteiro.

    A regra e a unica que nao precisa de gosto: o degrau certo do destino e o
    warp DELE que aponta de volta para mim. Warp que nao tem volta (boca de
    caverna para a rua, que cai no capacho do pai) fica como esta.

    Excecao medida em 07/08/2026, na Mt. Coronet 4F Rooms 1 and 2: quando os
    dois lados da escada estao no MESMO mapa (a sala 1 e a sala 2 dividem um
    header de 64x32), "o warp que aponta de volta para mim" inclui o proprio
    warp, e ele ganhava por ser o de indice menor. Resultado: pisar na escada
    devolvia o jogador ao tile onde ele ja estava, warp que dispara e nao leva a
    lugar nenhum. O degrau nunca e voce mesmo, entao o indice proprio sai da
    lista.
    """
    convertidos = _mapas_convertidos()
    por_id = {}
    for pasta in os.listdir(f"{REPO}/data/maps"):
        arq = f"{REPO}/data/maps/{pasta}/map.json"
        if os.path.exists(arq):
            d = json.load(open(arq))
            por_id[d["id"]] = (pasta, d)
    trocados = 0
    for pasta, d in convertidos.items():
        mudou = False
        for meu, w in enumerate(d.get("warp_events", [])):
            alvo = por_id.get(w["dest_map"])
            if not alvo:
                continue
            voltas = [i for i, v in enumerate(alvo[1].get("warp_events", []))
                      if v["dest_map"] == d["id"]
                      and not (w["dest_map"] == d["id"] and i == meu)]
            if not voltas or int(w["dest_warp_id"]) in voltas:
                continue
            w["dest_warp_id"] = str(voltas[0])
            mudou = True
            trocados += 1
        if mudou:
            json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
                      indent=2, ensure_ascii=False)
    return trocados


def demo():
    """O que a primeira versao errou, e o que prova que a caverna e de verdade."""
    # 1. `0x00` sem colisao e VAZIO, nao chao. Se virasse chao, Wayward Cave 1F
    #    passaria de labirinto para salao: sao 15 mil tiles nos 24 mapas.
    larg, alt, g = grade_do_header("MAP_HEADER_WAYWARD_CAVE_1F")
    assert (larg, alt) == (96, 64), (larg, alt)
    pal = traduz(larg, alt, g)
    vazio_sem_colisao = sum(1 for v in g if not v & 0x8000 and (v & 0xFF) == 0)
    assert vazio_sem_colisao > 1000, vazio_sem_colisao
    frac = andaveis(pal) / len(pal)
    assert 0.05 < frac < 0.45, frac       # labirinto, nem salao nem bloco macico
    # 2. a caverna tem que ser CONEXA em volta da entrada: chao solto atras da
    #    rocha seria sinal de que a leitura de colisao inverteu.
    andavel = [(p >> 10) & 3 == 0 for p in pal]
    inicio = andavel.index(True)
    pilha, visto = [inicio], {inicio}
    while pilha:
        i = pilha.pop()
        x, y = i % larg, i // larg
        for j, ok in (((i - 1), x > 0), ((i + 1), x + 1 < larg),
                      ((i - larg), y > 0), ((i + larg), y + 1 < alt)):
            if ok and j not in visto and andavel[j]:
                visto.add(j)
                pilha.append(j)
    assert len(visto) > 200, len(visto)
    # 3. parede tem face e topo: mancha de um metatile so seria sinal de que a
    #    regra de vizinho nao rodou.
    assert ROCHA_FACE in pal and ROCHA_TOPO in pal
    # 4. o metatile de saida tem comportamento de warp de verdade, lido da mesma
    #    tabela que o motor usa. Sem isso o warp existe e nunca dispara.
    prim, _ = F._atributos("gTileset_GeneralSinnoh")
    seg, _ = F._atributos("gTileset_CaveSinnoh")
    for palavra in (SAIDA, ESCADA):
        mt = palavra & 0x3FF
        tab, rel = (prim, mt) if mt < 512 else (seg, mt - 512)
        assert tab[rel] in W.COMPORTA_WARP, (hex(palavra), tab[rel])
    # 5. o nome da pasta tem que cair na mesma chave do header, senao
    #    completude.py continua contando a caverna como ausente.
    #    Quem tem nome renomeado (colisao de constante com outra regiao) casa
    #    pelo APELIDOS, e ai o par tem que estar la: e o mesmo fato, por outra
    #    porta, e sem ele o mapa entra na ROM e some da conta de completude.
    for h in ("MAP_HEADER_WAYWARD_CAVE_1F", "MAP_HEADER_VICTORY_ROAD_1F",
              "MAP_HEADER_VICTORY_ROAD_B1F", "MAP_HEADER_MT_CORONET_2F"):
        pasta = nome_de_pasta(h)
        assert (I.chave(pasta) == I.chave(h)
                or I.APELIDOS.get(pasta) == h), h
    # 6. sala PEQUENA de verdade entra, e mapa que so esta marcado
    #    MAP_TYPE_CAVE fica de fora. Foi a regra por tamanho que reprovou as 11
    #    salas sem saida das Solaceon Ruins.
    #    Lost Tower e Old Chateau entram por `OLD_CHATEAU_FLOOR`: contar so
    #    `CAVE_FLOOR` reprovava masmorra que existe na grade do mesmo jeito.
    #    Casa, ginasio e farol continuam fora, com ZERO chao de masmorra, e sao
    #    eles que provam que abrir para MAP_TYPE_INDOORS nao abriu a porteira.
    for h, entra in (("MAP_HEADER_SOLACEON_RUINS_ROOM_1_NORTHWEST_DEAD_END", True),
                     ("MAP_HEADER_ROUTE_209_LOST_TOWER_1F", True),
                     ("MAP_HEADER_OLD_CHATEAU_BACK_MIDDLE_EAST_ROOM", True),
                     ("MAP_HEADER_FLOAROMA_MEADOW", False),
                     ("MAP_HEADER_CELESTIC_TOWN_CAVE", False),
                     ("MAP_HEADER_VISTA_LIGHTHOUSE", False),
                     ("MAP_HEADER_HEARTHOME_CITY_GYM_TRAINER_ROOM_1", False)):
        _l, _a, gg = grade_do_header(h)
        assert (chao_de_caverna(gg) >= 8) is entra, (h, chao_de_caverna(gg))
    # 7. escada de mapa convertido tem que cair no DEGRAU que devolve, e nao no
    #    warp 0, que e a saida do dungeon. Com `dest_warp_id` "0" cravado, descer
    #    do 2F da Victory Road de Sinnoh cuspia o jogador na porta da Liga.
    por_id = {}
    for pasta in os.listdir(f"{REPO}/data/maps"):
        arq = f"{REPO}/data/maps/{pasta}/map.json"
        if os.path.exists(arq):
            d = json.load(open(arq))
            por_id[d["id"]] = d
    #    E o degrau nunca e o proprio warp QUANDO existe parceiro: escada com os
    #    dois lados no mesmo mapa (Mt. Coronet 4F Rooms 1 and 2) devolvia o
    #    jogador ao tile onde ele ja estava. Sem parceiro nao ha o que apontar, e
    #    e o caso da Mt. Coronet 2F, onde o outro lado da escada da fonte caiu
    #    fora do corpo andavel e foi descartado na conversao; consertar aquilo e
    #    renumerar warp de mapa que ja esta na ROM, nao e trabalho desta funcao.
    for d in _mapas_convertidos().values():
        for meu, w in enumerate(d.get("warp_events", [])):
            alvo = por_id.get(w["dest_map"])
            if not alvo:
                continue
            voltas = [i for i, v in enumerate(alvo.get("warp_events", []))
                      if v["dest_map"] == d["id"]
                      and not (w["dest_map"] == d["id"] and i == meu)]
            assert not voltas or int(w["dest_warp_id"]) in voltas, (
                d["id"], w["dest_map"], w["dest_warp_id"], voltas)
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
