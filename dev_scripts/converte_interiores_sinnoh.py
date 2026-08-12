#!/usr/bin/env python3
"""Converte a geometria de verdade dos INTERIORES de Sinnoh, do DS para map.bin.

    python3 dev_scripts/converte_interiores_sinnoh.py            # so relata
    python3 dev_scripts/converte_interiores_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/converte_interiores_sinnoh.py --demo     # autoteste

O que a fonte guarda de mobilia, e onde
---------------------------------------
A hipotese do PRD (bloco B1.a) era que mobilia de gen 4 e modelo 3D que a grade
2D nao carrega. **Medido em 12/08/2026: e meia verdade, e a metade util esta na
grade.** O `res/field/maps/data/map_data_NNN.bin` do pokeplatinum e

    u32 tamanho_da_permissao | u32 tamanho_da_lista_de_objetos |
    u32 tamanho_do_modelo    | u32 tamanho_do_bdhc
    + grade de permissao 32x32 (u16 por tile)
    + lista de objetos (48 B cada: id de modelo u32, x/y/z fx32, rotacao, escala)
    + NSBMD do mapa inteiro + BDHC

A lista de objetos so tem PROP com modelo proprio (porta de ginasio, elevador),
e o resto da mobilia esta desenhado dentro do NSBMD do mapa, irrecuperavel como
peca. **So que a grade de permissao carrega o COMPORTAMENTO do tile**, e o enum
`TileBehavior` do Platinum tem `TABLE`, `PC`, `TV`, `BOOKSHELF_1/2`,
`SMALL_BOOKSHELF_1/2`, `MART_SHELF_1/2/3`, `TRASH_CAN`, `TOWN_MAP`. Ou seja: a
pegada da mobilia, tile a tile, com o TIPO dela junto. E o que falta e so a arte,
que o GBA tem no tileset dele.

Melhor ainda, e isto foi medido e nao suposto: **os dois enums estao alinhados
em numero** na faixa de interior, porque a Game Freak manteve a tabela entre as
geracoes. Platinum 128 TABLE = GBA `MB_COUNTER`; 131 PC = `MB_PC`; 133 TOWN_MAP
= `MB_REGION_MAP`; 134 TV = `MB_TELEVISION`; 224 = `MB_PICTURE_BOOK_SHELF`;
225 = `MB_BOOKSHELF`; 226 = `MB_POKEMON_CENTER_BOOKSHELF`; 229 = `MB_SHOP_SHELF`;
101 = `MB_SOUTH_ARROW_WARP`; 105 = `MB_ANIMATED_DOOR`; 106/107 = escada rolante.
A tabela abaixo continua escrita a mao, porque o alinhamento e coincidencia util
e nao contrato, e porque 128 (mesa) virar balcao e escolha, nao identidade.

Onde a grade acaba, e o corte
-----------------------------
A grade e sempre 32x32 mesmo quando o quarto tem 17x12: o resto e area que o
modelo 3D nem desenha. O corte sai do bounding box dos tiles COM COLISAO, que e
a casca do quarto. Medido nos 14 destinos desta leva: o bounding box comeca em
(0,0) em todos, entao **coordenada de NPC da fonte cai no mesmo lugar depois do
corte** e o importador de NPC de Sinnoh serve sem offset.

Ao contrario da caverna, aqui `0x00 sem colisao` DENTRO do corte E chao: numa
caverna aquilo era vazio atras da pedra, num quarto e o piso. E por isso que
`converte_cavernas_sinnoh.chao_de_caverna` da ZERO nestes mapas e os reprovava.

De onde saem as palavras de 16 bits
-----------------------------------
Nenhuma foi escolhida de cabeca. Todas foram lidas do `map.bin` de mapas que o
repo JA tem (`LAYOUT_HOUSE1` e `LAYOUT_HOUSE3`, par `Building` +
`GenericBuilding`) e conferidas no desenho, renderizando o atlas de metatiles do
tileset com `dev_scripts/render_maps.py`. O piso e o tapete de 9 pecas
(565..583) que a HOUSE1 usa, com canto e borda; a parede e o par 517/525 (topo e
a base com rodape); o capacho e 520/521; a escada e 523.

O que NAO entra de proposito
----------------------------
- `MB_REGION_MAP`, `MB_SHOP_SHELF` e lata de lixo nao existem no par
  `Building` + `GenericBuilding`: cairiam noutro tileset e trocar o tileset do
  mapa por causa de um movel e trocar o quarto inteiro. Fica parede, e a lista
  sai no relatorio. (`MB_PC` entrou depois, em 12/08: ele mora no PRIMARIO
  `gTileset_Building`, que todo interior carrega, e apareceu em 8 tiles assim
  que o Battle Frontier destravou as salas do Frontier.)
- Ponta esquerda e direita de parede: os unicos metatiles com esse desenho
  (522 e 524) carregam `MB_COUNTER`. Parede que o jogador "usa" e defeito, entao
  parede aqui so tem topo e base.

Compatibilidade de save: grupo novo no FIM de `group_order`, mapa novo no fim
dele, warp novo no FIM da lista do mapa que ja existe. Nenhum indice antigo anda.
`dest_warp_id` nunca fica cravado em "0": quem fecha e `casa_voltas()` do
conversor de caverna, a mesma funcao e pela mesma licao (as 69 escadas de
06/08/2026).
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import abre_bocas_cavernas_sinnoh as B      # noqa: E402
import abre_portas_extras_sinnoh as A       # noqa: E402
import abre_portas_teimosas_sinnoh as T     # noqa: E402
import converte_cavernas_sinnoh as C        # noqa: E402
import fecha_portas_sinnoh as F             # noqa: E402
import importa_npcs_sinnoh as I             # noqa: E402
import valida_mapas_sinnoh as V             # noqa: E402
import valida_warp_tile as W                # noqa: E402

PLAT = F.PLAT
APLICAR = "--aplicar" in sys.argv
GRUPO = "gMapGroup_SinnohInteriores"
PRIMARIO, SECUNDARIO = "gTileset_Building", "gTileset_GenericBuilding"

# ------------------------------------------------------------- vocabulario
# Piso: tapete de 9 pecas da LAYOUT_HOUSE1 (metatiles 565..583), elevacao 3,
# colisao 0. A peca sai da forma do quarto: canto onde faltam dois vizinhos,
# borda onde falta um, miolo onde nao falta nenhum. E o mesmo desenho que o mapa
# a mao usa, e e a unica coisa desta tabela que depende da geometria.
PISO = ((0x3235, 0x3236, 0x3237),
        (0x323D, 0x323E, 0x323F),
        (0x3245, 0x3246, 0x3247))

PAREDE_TOPO = 0x0605   # metatile 517, colisao 1: parede vista de frente
PAREDE_BASE = 0x060D   # metatile 525, a mesma parede com o rodape, chao abaixo
CAPACHO = (0x0208, 0x0209)   # 520/521, MB_SOUTH_ARROW_WARP: saida para o sul
ESCADA = 0x020B              # 523, MB_NON_ANIMATED_DOOR: dispara de qualquer lado

# Comportamento do Platinum -> colunas (palavra de cima, palavra de baixo) do
# movel no GBA. Coluna se repete quando o movel da fonte e mais largo que o do
# tileset. Todas medidas em LAYOUT_HOUSE3, tile a tile.
MOBILIA = {
    128: [(0x0602, 0x060A)],                    # TABLE      -> MB_COUNTER
    # PC: metatile 4 e 5 do PRIMARIO `gTileset_Building`, que e o mesmo em todo
    # interior e nao depende do secundario. Sao duas telas inteiras num tile so
    # (conferido no atlas), entao a peca de cima e parede comum, igual a TV.
    131: [(PAREDE_TOPO, 0x0404), (PAREDE_TOPO, 0x0405)],
    134: [(0x0616, 0x061E)],                    # TV         -> MB_TELEVISION
    224: [(0x0615, 0x06A1)],                    # SMALL_BOOKSHELF_1
    225: [(0x06A6, 0x06AE), (0x06A7, 0x06AF)],  # BOOKSHELF_1, duas colunas
    226: [(0x06A6, 0x06AE), (0x06A7, 0x06AF)],  # BOOKSHELF_2, mesmo desenho
    234: [(0x0615, 0x06A1)],                    # SMALL_BOOKSHELF_2
}

# Comportamento do Platinum que e tile de WARP. O capacho so dispara para quem
# anda para o SUL (`IsArrowWarpMetatileBehavior`), entao ele so serve para a
# porta que a fonte marcou como saida ao sul; todo o resto vira escada, que
# dispara de qualquer lado.
WARP_SUL = 101                                   # WARP_ENTRANCE_SOUTH
WARPS = {98, 99, 100, 101, 103, 105, 106, 107, 108, 109, 110, 111, 94, 95}

# Mapa da fonte que esta ferramenta NAO cria, com o motivo escrito.
NAO_CRIAR = {
    # Caverna de pedra: cair no par Building+GenericBuilding sairia com parede
    # de casa e tapete de sala. Ela e do conversor de caverna, que hoje a reprova
    # por ter ZERO chao de masmorra na grade; consertar aquilo e trabalho de la.
    "MAP_HEADER_CELESTIC_TOWN_CAVE": "caverna, tileset errado aqui",
    # Decisao 17 do Gui, confirmada em 12/08/2026: os NPCs de Wi-Fi e Union Room
    # foram ESCONDIDOS porque os sistemas de link nao existem nesta ROM. Criar a
    # sala seria um quarto sem funcao, e ainda por cima com dono arbitrario (18
    # centros Pokemon apontam para ela na fonte e so um pode receber a volta).
    # Reabre se link um dia entrar.
    "MAP_HEADER_UNION_ROOM": ("decisao 17, sistemas de link nao existem; "
                              "reabre se link um dia entrar"),
}


# ------------------------------------------------------------- leitura
def recorta(header):
    """(largura, altura, grade recortada) do quarto dentro da grade 32x32.

    O corte e o bounding box dos tiles COM COLISAO, que e a casca do quarto.
    Fora dela a grade e area que o modelo 3D nem desenha, e traduzir aquilo como
    chao daria um salao vazio em volta do quarto.
    """
    larg, alt, grade = C.grade_do_header(header)
    if not grade:
        return 0, 0, []
    bloq = [i for i, v in enumerate(grade) if v & 0x8000]
    if not bloq:
        return 0, 0, []
    xs = [i % larg for i in bloq]
    ys = [i // larg for i in bloq]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    w, h = x1 - x0 + 1, y1 - y0 + 1
    corte = [grade[(y0 + y) * larg + x0 + x] for y in range(h) for x in range(w)]
    return w, h, corte


def eh_interior(grade):
    """A grade tem quarto de verdade: casca fechada e chao dentro dela.

    Sem isto entraria mapa cuja grade e so a marca de saida (`WIFI_PLAZA` e
    `UNKNOWN_561` tem ZERO tile com colisao) e mapa de rua, que o filtro de
    `mapType` ja tira antes.
    """
    return sum(1 for v in grade if not v & 0x8000) >= 8


# ------------------------------------------------------------- traducao
def blocos(w, h, comp, bloqueado):
    """(x0, y0) do canto de cada mancha conexa de mobilia do MESMO tipo.

    A coluna e a linha do movel no GBA saem da posicao dentro da mancha: e o que
    faz a estante 2x2 da fonte sair com a coluna esquerda e a direita certas em
    vez de duas metades esquerdas.
    """
    canto = {}
    visto = set()
    for i in range(w * h):
        if i in visto or not bloqueado(i) or comp(i) not in MOBILIA:
            continue
        pilha, comp_tiles = [i], []
        visto.add(i)
        while pilha:
            j = pilha.pop()
            comp_tiles.append(j)
            x, y = j % w, j // w
            for k, ok in ((j - 1, x > 0), (j + 1, x + 1 < w),
                          (j - w, y > 0), (j + w, y + 1 < h)):
                if ok and k not in visto and bloqueado(k) and comp(k) == comp(i):
                    visto.add(k)
                    pilha.append(k)
        x0 = min(j % w for j in comp_tiles)
        y0 = min(j // w for j in comp_tiles)
        for j in comp_tiles:
            canto[j] = (x0, y0)
    return canto


def traduz(w, h, grade):
    """Grade recortada de interior -> lista de palavras do pokeemerald."""
    def bloqueado(i):
        return bool(grade[i] & 0x8000)

    def comp(i):
        return grade[i] & 0xFF

    def andavel(x, y):
        return 0 <= x < w and 0 <= y < h and not bloqueado(y * w + x)

    canto = blocos(w, h, comp, bloqueado)
    saida = []
    for y in range(h):
        for x in range(w):
            i = y * w + x
            if not bloqueado(i):
                lin = 0 if not andavel(x, y - 1) else (
                    2 if not andavel(x, y + 1) else 1)
                col = 0 if not andavel(x - 1, y) else (
                    2 if not andavel(x + 1, y) else 1)
                saida.append(PISO[lin][col])
                continue
            b = comp(i)
            if b in WARPS:
                # Porta de gen 4 e tile BLOQUEADO com comportamento `DOOR`: o
                # jogador anda contra ela e o motor do DS abre. No GBA a porta e
                # tile ANDAVEL com comportamento de warp, que o jogador pisa.
                # Sem esta linha a porta virava parede, o warp era empurrado por
                # `poe_warp` para o chao mais proximo, e a coordenada da fonte
                # ficava dentro da pedra: foi o `--demo` do
                # `abre_bocas_cavernas_sinnoh` que pegou, conferindo justamente
                # isso nos mapas convertidos.
                saida.append(palavra_de_warp(b, x))
                continue
            if b in MOBILIA:
                x0, y0 = canto[i]
                colunas = MOBILIA[b]
                cima, baixo = colunas[(x - x0) % len(colunas)]
                # topo enquanto houver mais movel embaixo; a peca que carrega o
                # comportamento e sempre a de BAIXO, que e como o GBA desenha.
                mesmo_abaixo = (y + 1 < h and bloqueado(i + w)
                                and comp(i + w) == b)
                saida.append(cima if mesmo_abaixo else baixo)
                continue
            saida.append(PAREDE_BASE if andavel(x, y + 1) else PAREDE_TOPO)
    return saida


def _corte(lay):
    """Onde acaba o tileset primario. NAO e o tamanho da tabela dele.

    `gTileset_Building` tem OITO metatiles no arquivo e e primario de quase todo
    interior; o motor continua cortando em 512. Usar o tamanho da tabela como
    corte manda o metatile 516 para o primario e a leitura devolve -1.
    """
    return 640 if lay.get("layout_version", "") in ("frlg", "johto") else 512


def comportamento(lay, palavra):
    """Comportamento do metatile de uma palavra, na tabela que o motor usa."""
    prim, _ = F._atributos(lay["primary_tileset"])
    seg, _ = F._atributos(lay["secondary_tileset"])
    corte = _corte(lay)
    mt = palavra & 0x3FF
    tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
    return tab[rel] if rel < len(tab) else -1


def palavra_do_tileset(pai, x, y):
    """Palavra de porta lida da tabela de ATRIBUTOS do tileset do mapa.

    Ultimo recurso, depois de `abre_portas_teimosas_sinnoh.palavra_ampla`, que so
    copia warp que algum mapa ja desenhou. Medido: `gTileset_Pasos` (portarias,
    Iron Island, a propria antecamara de Sinnoh) e `gTileset_MossdeepGym` nao tem
    metatile de porta NENHUM, entao nao ha o que copiar e a copia devolve None.

    A seta escolhida e a do NORTE porque o teste de parede de
    `abre_bocas_cavernas_sinnoh.candidatos` so aceita tile com chao andavel logo
    ABAIXO: o jogador chega andando para cima, e `IsArrowWarpMetatileBehavior`
    casa comportamento com direcao. Colisao e elevacao vem do chao de baixo, que
    e de onde o jogador vem; elevacao escolhida de cabeca poe a porta noutra
    camada e ela fica inalcancavel com validador estatico verde.
    """
    d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
    lay = F.layouts()[d["layout"]]
    prim, _ = F._atributos(lay["primary_tileset"])
    seg, _ = F._atributos(lay["secondary_tileset"])
    corte = _corte(lay)
    alvo = W._MB["MB_NORTH_ARROW_WARP"]
    escolha = None
    for i, b in enumerate(prim[:corte]):
        if b == alvo:
            escolha = i
            break
    if escolha is None:
        for i, b in enumerate(seg):
            if b == alvo:
                escolha = corte + i
                break
    if escolha is None:
        return None
    blk = open(f"{REPO}/{lay['blockdata_filepath']}", "rb").read()
    abaixo = struct.unpack_from("<H", blk, ((y + 1) * lay["width"] + x) * 2)[0]
    return escolha | (abaixo & 0xF000)      # elevacao do chao, colisao 0


def regiao_principal(pal, w, h):
    return C.regiao_principal(pal, w, h)


def palavra_de_warp(b, x):
    """Tile que o warp pisa. Capacho so para a saida ao sul da fonte."""
    if b == WARP_SUL:
        return CAPACHO[x % 2]
    return ESCADA


# ------------------------------------------------------------- fila
def _consts_existentes():
    pastas = set(os.listdir(f"{REPO}/data/maps"))
    consts = set(re.findall(r'"id":\s*"(MAP_\w+)"', "".join(
        open(f"{REPO}/data/maps/{p}/map.json").read() for p in pastas
        if os.path.exists(f"{REPO}/data/maps/{p}/map.json"))))
    return pastas, consts


def _casados(heads):
    por_chave = {}
    for h in heads:
        por_chave.setdefault(I.chave(h), h)
    casados = {}
    for m in I.nossos_mapas_sinnoh():
        h = I.APELIDOS.get(m) or por_chave.get(I.chave(m))
        if h in heads:
            casados[h] = m
    return casados


_DEST = {}


def destinos(header, heads):
    if header not in _DEST:
        arq = os.path.join(PLAT, "res/field/events", heads[header][0] + ".json")
        _DEST[header] = (json.load(open(arq)).get("warp_events", [])
                         if os.path.exists(arq) else [])
    return _DEST[header]


def fila():
    """[(pai, header)] dos interiores alcancaveis, na ordem em que abrem.

    "Alcancavel" e literal: o pai ja esta na ROM, ou entrou nesta mesma leva. E
    a mesma regra do conversor de caverna, so que rodada em laco ate parar de
    render, porque o ginasio DP de Hearthome e uma cadeia (sala do lider ->
    elevador -> mais seis salas) e o fecho so aparece iterando.
    """
    heads = I.headers_do_platinum()
    casados = _casados(heads)
    existentes = set(casados) | F.JA_TEMOS
    pastas, consts = _consts_existentes()
    H = C.headers()

    def serve(d):
        if d in existentes or d in NAO_CRIAR:
            return False
        if H.get(d, {}).get("mapType") != "MAP_TYPE_INDOORS":
            return False
        if F.nome_de_pasta(d) in pastas or F.const_do_header(d) in consts:
            return False
        w, h, g = recorta(d)
        return bool(g) and eh_interior(g)

    saida, vistos = [], set()
    # primeira volta: pai que ja esta na ROM. `NAO_FURAR` e decisao registrada
    # (furar a parede da Elite dos Quatro cria segunda saida sem o bloqueio de
    # vitoria), e ela vale aqui igual.
    for header, meu in sorted(casados.items(), key=lambda kv: kv[1]):
        if meu in A.NAO_FURAR:
            continue
        for wp in destinos(header, heads):
            d = wp["dest_header_id"]
            if d in vistos or not serve(d):
                continue
            vistos.add(d)
            saida.append((meu, d))
    # voltas seguintes: pai que entrou agora
    mudou = True
    while mudou:
        mudou = False
        for _pai, header in list(saida):
            for wp in destinos(header, heads):
                d = wp["dest_header_id"]
                if d in vistos or not serve(d):
                    continue
                vistos.add(d)
                saida.append((F.nome_de_pasta(header), d))
                mudou = True
    return saida


# ------------------------------------------------------------- porta no pai
def abre_porta(pai, desenhadas):
    """(x, y) de um tile de porta no mapa pai, desenhando um se preciso.

    Primeiro a porta ORFA que ja existe (`fecha_portas_sinnoh.portas_livres`).
    Sem ela, desenha, com a mesma regra das bocas de caverna: meio de parede com
    chao logo abaixo, e a palavra COPIADA de um warp que ja existe no par de
    tilesets. Layout compartilhado e clonado antes, senao a porta nova apareceria
    nas 64 casas que usam a planta.
    """
    d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
    ja = desenhadas.setdefault(pai, set())
    livres = [p for p in F.portas_livres(pai, d) if p not in ja]
    if livres:
        ja.add(livres[0])
        return livres[0]
    cand = [(x, y) for x, y, _p, _a in B.candidatos(pai) if (x, y) not in ja]
    if not cand:
        return None
    x, y = cand[0]
    palavra = T.palavra_ampla(pai) or palavra_do_tileset(pai, x, y)
    if palavra is None:
        return None
    if len(A.mapas_do_layout(d["layout"])) > 1:
        B.clona_layout(pai, d)
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
    A.libera_tile(pai, x, y)
    A.grava_tile(d["layout"], x, y, palavra)
    ja.add((x, y))
    return x, y


def pais_possiveis(header, heads, casados, primeiro):
    """Mapas nossos que servem de entrada para `header`, o mais fiel primeiro.

    Existe porque o pai que a fonte indica nem sempre PODE receber porta: o
    tileset do nosso `HearthomeCity_Gym` e o `gTileset_MossdeepGym`, que nao tem
    metatile de porta nenhum (so `MB_MOSSDEEP_GYM_WARP`, que e o painel da
    patinacao e tem comportamento proprio no motor). Desenhar porta ali nao e
    "desenhar a porta que faltava", e inventar mecanica.

    A alternativa nao e escolhida a esmo: vale qualquer mapa que a FONTE liga a
    este, nos dois sentidos. A sala de treinador 1 do ginasio de Hearthome leva a
    sala 2 no Platinum, entao entrar por ela e andar o mesmo corredor ao
    contrario, e nao um atalho inventado.
    """
    saida = [primeiro]
    vizinhos = set()
    for wp in destinos(header, heads):
        vizinhos.add(wp["dest_header_id"])
    for h in heads:
        if any(wp["dest_header_id"] == header for wp in destinos(h, heads)):
            vizinhos.add(h)
    for h in sorted(vizinhos):
        meu = casados.get(h)
        if meu and meu not in saida and meu not in A.NAO_FURAR:
            saida.append(meu)
    return saida


# ------------------------------------------------------------- escrita
def escreve_layout(pasta, header, w, h, palavras):
    d = f"{REPO}/data/layouts/{pasta}"
    os.makedirs(d, exist_ok=True)
    open(f"{d}/map.bin", "wb").write(struct.pack(f"<{len(palavras)}H", *palavras))
    open(f"{d}/border.bin", "wb").write(struct.pack("<4H", *([PAREDE_TOPO] * 4)))
    lid = "LAYOUT_" + F.const_do_header(header)[len("MAP_"):]
    return {
        "id": lid, "name": f"{pasta}_Layout",
        "width": w, "height": h,
        "primary_tileset": PRIMARIO, "secondary_tileset": SECUNDARIO,
        "border_filepath": f"data/layouts/{pasta}/border.bin",
        "blockdata_filepath": f"data/layouts/{pasta}/map.bin",
        "layout_version": "emerald",
    }


def registra_layout(lay):
    """Poe o layout novo no FIM de layouts.json, RELENDO o arquivo antes.

    Sem a releitura, `abre_porta` clona um layout no meio do laco (a planta de
    casa serve 64 mapas e nao pode ser furada), grava o clone em layouts.json, e
    o dump final desta ferramenta o apagava por escrever uma copia carregada
    antes do clone existir. Medido em 12/08/2026: o `HearthomeCityGymLeaderRoom`
    ficou apontando para `LAYOUT_HEARTHOMECITYGYMLEADERROOM`, que nao estava em
    lugar nenhum, e o mapa PAI (que ja estava na ROM) morria junto.
    """
    arq = f"{REPO}/data/layouts/layouts.json"
    todos = json.load(open(arq))
    todos["layouts"].append(lay)
    json.dump(todos, open(arq, "w"), indent=2, ensure_ascii=False)
    F.layouts()[lay["id"]] = lay


def distintos(palavras):
    return len({p & 0x3FF for p in palavras})


def sem_traducao(grade):
    """Comportamento de movel que a fonte tem e este tileset nao desenha."""
    fora = {}
    for v in grade:
        if not v & 0x8000:
            continue
        b = v & 0xFF
        if b and b not in MOBILIA and b not in WARPS:
            fora[b] = fora.get(b, 0) + 1
    return fora


def main():
    if "--demo" in sys.argv:
        return demo()

    heads = I.headers_do_platinum()
    casados = _casados(heads)
    pend = fila()
    print(f"interiores alcancaveis que faltam: {len(pend)}")
    perdidos = {}
    for _pai, header in pend:
        w, h, g = recorta(header)
        pal = traduz(w, h, g)
        for b, n in sem_traducao(g).items():
            perdidos[b] = perdidos.get(b, 0) + n
        print(f"   {header.replace('MAP_HEADER_', ''):44} {w}x{h} "
              f"{C.andaveis(pal):4} andaveis, {distintos(pal):3} metatiles")
    if perdidos:
        print("comportamento de movel sem metatile neste tileset (vira parede):")
        for b, n in sorted(perdidos.items()):
            print(f"   {b} ({W.NOME.get(b, '?')}): {n} tiles")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        return 0

    sprites = V.sprites_utilizaveis()
    movimentos = V.constantes("include/constants/event_object_movement.h",
                              "MOVEMENT_TYPE_")
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    F.grupo_com_vaga(grupos, GRUPO)
    modelo = json.load(open(f"{REPO}/data/maps/HearthomeCityGymTrainerRoom2/map.json"))
    incs, desenhadas = [], {}
    conta = {"mapas": 0, "npcs": 0, "placas": 0, "textos": 0, "warps": 0,
             "portas": 0}
    # constante de todo mapa que o warp pode alcancar: os que ja estao na ROM e
    # os desta leva. Warp para fora dessa lista e descartado em vez de virar
    # link quebrado, que e a regra do conversor de caverna.
    # Destino que um warp NOVO pode ter: so mapa DESTA leva, mais o pai, que
    # ganha o warp de volta logo abaixo. Mapa que ja estava na ROM fica de fora
    # de proposito: ele nao tem warp de volta para ca, e `casa_voltas()` nao teria
    # o que apontar, entao o `dest_warp_id` ficaria "0" e o jogador cairia no
    # warp 0 do outro lado, que e a SAIDA dele. E a licao das 69 escadas de
    # 06/08/2026, e ela reapareceu aqui em 12/08: a sala de treinador 1 do
    # ginasio de Hearthome nascia com warp para o ginasio caindo na porta da rua.
    nossos = {header: F.const_do_header(header) for _p, header in pend}

    for pai0, header in pend:
        # o pai pode JA ter o warp para este filho, quando ele proprio nasceu
        # nesta leva com a lista de warps da fonte (o elevador do ginasio DP
        # aponta para as seis salas antes de qualquer uma existir). Nesse caso a
        # entrada e aquela, e desenhar outra porta so poria uma segunda escada ao
        # lado da primeira, para o mesmo lugar.
        pai, porta = pai0, None
        arq_pai = f"{REPO}/data/maps/{pai0}/map.json"
        const = F.const_do_header(header)
        if os.path.exists(arq_pai) and any(
                wp["dest_map"] == const
                for wp in json.load(open(arq_pai)).get("warp_events", [])):
            porta = "ja tem"
        for pai in ([] if porta else
                    pais_possiveis(header, heads, casados, pai0)):
            if not os.path.exists(f"{REPO}/data/maps/{pai}/map.json"):
                continue
            porta = abre_porta(pai, desenhadas)
            if porta is not None:
                break
        if porta is None:
            print(f"   PULADO {header.replace('MAP_HEADER_', '')}: nenhum vizinho "
                  f"da fonte tem porta orfa nem parede/tileset onde desenhar uma")
            continue
        if pai != pai0:
            print(f"   {header.replace('MAP_HEADER_', '')}: entra por {pai} "
                  f"(o pai da fonte, {pai0}, nao aceita porta)")
        conta["portas"] += 1
        pasta = F.nome_de_pasta(header)
        w, h, g = recorta(header)
        pal = traduz(w, h, g)
        regiao = regiao_principal(pal, w, h)

        p_pai = f"{REPO}/data/maps/{pai}/map.json"
        d_pai = json.load(open(p_pai))
        warps, volta = [], None
        for wp in destinos(header, heads):
            x, y = int(wp["x"]), int(wp["z"])
            if not (0 <= x < w and 0 <= y < h):
                continue
            d = wp["dest_header_id"]
            if d in nossos and nossos[d] != d_pai["id"]:
                destino = nossos[d]
            elif volta is None:
                destino = d_pai["id"]
            else:
                continue
            b = g[y * w + x] & 0xFF
            x, y = C.poe_warp(regiao, w, x, y)
            if any((e["x"], e["y"]) == (x, y) for e in warps):
                continue
            pal[y * w + x] = palavra_de_warp(b, x)
            if destino == d_pai["id"]:
                volta = len(warps)
            warps.append({"x": x, "y": y, "elevation": 0,
                          "dest_map": destino, "dest_warp_id": "0"})
        if volta is None:
            # nenhum warp da fonte cai no pai: abre a volta no tile andavel mais
            # ao norte do corpo do quarto, senao o quarto nao devolve o jogador.
            i = min(regiao)
            pal[i] = ESCADA
            volta = len(warps)
            warps.append({"x": i % w, "y": i // w, "elevation": 0,
                          "dest_map": d_pai["id"], "dest_warp_id": "0"})

        lay = escreve_layout(pasta, header, w, h, pal)
        registra_layout(lay)

        d = dict(modelo)
        d.pop("connections", None)
        d["id"] = F.const_do_header(header)
        d["name"] = pasta
        d["layout"] = lay["id"]
        d["warp_events"] = warps
        d["coord_events"] = []
        objs, bg, trecho = F.conteudo_do_mapa(
            header, pasta, w, h, sprites, movimentos, lay["id"])
        d["object_events"] = objs
        d["bg_events"] = bg
        d["origem"] = ("pokeplatinum: geometria convertida da grade 2D "
                       "(map_data) com mobilia, mais NPC, placa e texto")
        os.makedirs(f"{REPO}/data/maps/{pasta}", exist_ok=True)
        json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
                  indent=2, ensure_ascii=False)
        open(f"{REPO}/data/maps/{pasta}/scripts.inc", "w").write(
            f"{pasta}_MapScripts::\n\t.byte 0\n{trecho}")
        grupos[F.grupo_com_vaga(grupos, GRUPO)].append(pasta)
        incs.append(f'\t.include "data/maps/{pasta}/scripts.inc"\n')

        if porta != "ja tem":
            d_pai.setdefault("warp_events", [])
            d_pai["warp_events"].append({
                "x": porta[0], "y": porta[1], "elevation": 0,
                "dest_map": d["id"], "dest_warp_id": str(volta)})
            json.dump(d_pai, open(p_pai, "w"), indent=2, ensure_ascii=False)
            conta["warps"] += 1
        conta["mapas"] += 1
        conta["npcs"] += len(objs)
        conta["placas"] += len(bg)
        conta["textos"] += trecho.count(".string")
        conta["warps"] += len(warps)

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
    voltas = C.casa_voltas()
    print(f"\naplicado: {conta['mapas']} interiores, {conta['warps']} warps, "
          f"{voltas} voltas apontadas para o degrau certo, "
          f"{conta['npcs']} NPCs, {conta['placas']} placas, "
          f"{conta['textos']} textos do Platinum")
    return 0


# ------------------------------------------------------------- autoteste
def demo():
    """O que prova que o quarto e de verdade, e nao mascara de colisao."""
    prim, _ = F._atributos(PRIMARIO)
    seg, _ = F._atributos(SECUNDARIO)

    def comportamento(palavra):
        mt = palavra & 0x3FF
        tab, rel = (prim, mt) if mt < 512 else (seg, mt - 512)
        return tab[rel] if rel < len(tab) else -1

    # 1. o alinhamento dos dois enums e o coracao da tabela: se o GBA mudar de
    #    numero, o movel vira outro movel calado. Cada linha da MOBILIA tem que
    #    cair no comportamento de MESMO numero do Platinum.
    for plat, colunas in MOBILIA.items():
        # 226 e 234 sao a segunda estante grande e a segunda pequena da fonte, e
        # o tileset do GBA so tem um desenho de cada tamanho: elas caem de
        # proposito no mesmo metatile da primeira.
        esperado = {226: 225, 234: 224}.get(plat, plat)
        for _cima, baixo in colunas:
            assert comportamento(baixo) == esperado, (plat, hex(baixo),
                                                      comportamento(baixo))
    # 2. o tile que o warp pisa tem que disparar de verdade, lido da mesma tabela
    #    que o motor usa. Sem isso o warp existe e nunca dispara (licao 4.1).
    for palavra in CAPACHO + (ESCADA,):
        assert comportamento(palavra) in W.COMPORTA_WARP, hex(palavra)
    # 3. piso anda, parede e movel nao. Colisao invertida daria quarto solido.
    for linha in PISO:
        for p in linha:
            assert (p >> 10) & 3 == 0, hex(p)
    for p in (PAREDE_TOPO, PAREDE_BASE):
        assert (p >> 10) & 3 != 0, hex(p)
    for colunas in MOBILIA.values():
        for cima, baixo in colunas:
            assert (cima >> 10) & 3 != 0 and (baixo >> 10) & 3 != 0

    # 4. o corte: a grade e 32x32 e o quarto nao. Sem o corte, a sala de
    #    treinador do ginasio de Hearthome sairia com 1024 tiles em vez de 204,
    #    e o resto seria salao vazio que o Platinum nem desenha.
    w, h, g = recorta("MAP_HEADER_HEARTHOME_CITY_GYM_TRAINER_ROOM_1")
    assert (w, h) == (17, 12), (w, h)
    pal = traduz(w, h, g)
    assert len(pal) == w * h
    #    e o corte comeca em (0,0), que e o que deixa a coordenada de NPC da
    #    fonte cair no mesmo tile depois de recortado.
    larg, _alt, cru = C.grade_do_header("MAP_HEADER_HEARTHOME_CITY_GYM_TRAINER_ROOM_1")
    assert cru[0] == g[0] and cru[1] == g[1]

    # 5. mobilia: a grade CARREGA o movel, e a traducao tem que por o metatile
    #    certo na pegada certa. Iron Island House tem uma TV 2x2 na fonte.
    w2, h2, g2 = recorta("MAP_HEADER_IRON_ISLAND_HOUSE")
    tv = [i for i, v in enumerate(g2) if v & 0x8000 and (v & 0xFF) == 134]
    assert len(tv) == 4, len(tv)         # 2x2 de TILE_BEHAVIOR_TV
    pal2 = traduz(w2, h2, g2)
    baixo = [i for i in tv if not (i + w2 < len(g2) and g2[i + w2] & 0x8000
                                   and (g2[i + w2] & 0xFF) == 134)]
    assert all(comportamento(pal2[i]) == 134 for i in baixo), "TV sem MB_TELEVISION"
    assert all(comportamento(pal2[i]) == 0 for i in tv if i not in baixo)

    # 6. MUTACAO PLANTADA: trocar o movel na FONTE tem que trocar o metatile na
    #    saida, e so nele. Tabela morta (ou movel lido do lugar errado) passa nos
    #    testes de cima e reprova aqui.
    mutante = list(g2)
    for i in tv:
        mutante[i] = (mutante[i] & ~0xFF) | 225      # TV vira estante
    pal3 = traduz(w2, h2, mutante)
    assert all(comportamento(pal3[i]) == 225 for i in baixo), "mutacao nao pegou"
    iguais = sum(1 for a, b in zip(pal2, pal3) if a == b)
    assert iguais == len(pal2) - len(tv), (iguais, len(pal2), len(tv))

    # 7. o quarto nao e mascara de duas cores: o piso sai com canto e borda, que
    #    e a diferenca entre planta e mancha. Menos de 8 metatiles distintos num
    #    quarto de 17x12 significa que o tapete de 9 pecas nao rodou.
    assert distintos(pal) >= 8, distintos(pal)
    assert PISO[0][0] in pal and PISO[1][1] in pal and PISO[2][2] in pal

    # 7b. a porta da fonte tem que virar tile ANDAVEL que dispara. No Platinum
    #     ela e tile BLOQUEADO com comportamento `DOOR`, e traduzir a colisao ao
    #     pe da letra a transformava em parede: o warp era empurrado para o chao
    #     vizinho e a coordenada da fonte caia dentro da pedra.
    portas = [i for i, v in enumerate(g) if v & 0x8000 and (v & 0xFF) in WARPS]
    assert portas, "a sala de treinador tem porta na fonte"
    for i in portas:
        assert (pal[i] >> 10) & 3 == 0, i
        assert comportamento(pal[i]) in W.COMPORTA_WARP, i

    # 8. o quarto tem que ser andavel de ponta a ponta a partir da porta: chao
    #    solto atras da parede seria sinal de colisao invertida.
    regiao = regiao_principal(pal, w, h)
    assert len(regiao) > 40, len(regiao)

    # 9. nome de pasta tem que cair na mesma chave do header, senao
    #    completude.py continua contando o mapa como ausente depois de criado.
    for hh in ("MAP_HEADER_HEARTHOME_CITY_GYM_TRAINER_ROOM_1",
               "MAP_HEADER_IRON_ISLAND_HOUSE", "MAP_HEADER_UNION_ROOM"):
        pasta = F.nome_de_pasta(hh)
        assert I.chave(pasta) == I.chave(hh) or I.APELIDOS.get(pasta) == hh, hh

    # 10. IDEMPOTENCIA: o que ja esta na ROM nao volta para a fila.
    heads = I.headers_do_platinum()
    casados = _casados(heads)
    pend = fila()
    assert not (set(h for _p, h in pend) & set(casados)), "fila repete mapa"
    assert len(set(h for _p, h in pend)) == len(pend), "fila repete header"

    # 11. o que a fonte tem de movel e este tileset nao desenha some CALADO se
    #     ninguem contar. Aqui a conta existe e o main a imprime.
    fora = sem_traducao(g2)
    assert isinstance(fora, dict)

    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
