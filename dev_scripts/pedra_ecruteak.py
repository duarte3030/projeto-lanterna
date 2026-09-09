#!/usr/bin/env python3
"""Refino de `EcruteakCity` (tema CIDADE DE PEDRA), no `gTileset_EcruteakCity`,
com um marco de pedra importado do `Pokémon GS Chronicles`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: 25,4% do chão andável a pé (301 células de 1.185) é
UM metatile, o 724. E o 724 não é uma praça: é a RUA. Rotulando o `map.bin`
célula a célula, as 301 se desenham como uma grade, quatro ruas horizontais
(linhas 27, 35, 42 e 50) e seis verticais (colunas 15, 25, 33, 34, 39, 44 e 52),
mais a alameda da ponte ao sul. Ecruteak é a cidade histórica de Johto, com a
Torre Queimada, o Teatro de Dança e dois lagos, e o que ela mostra no chão é um
xadrez de pedra IDÊNTICO em cada uma das 301 células.

O SEGUNDO CARIMBO NÃO ASSUSTA, e isso muda o tamanho da rodada. Derrubado o 724,
o dominante passa a ser o 748 com 70 células, ou seja 5,9%, muito abaixo do teto
de 20% da onda. Diferente de Blackthorn e de Cianwood, aqui NÃO há um segundo
tapete escondido: basta refinar a rua, e sobra folga para solidificar móvel sem
brigar com a régua (cada célula que vira sólida sai do denominador).

O ORÇAMENTO, medido nesta árvore e não herdado de briefing:

  split      `layout_version: "johto"`, que é `bigPrimary`: primário de 640
             tiles, 640 metatiles e 7 paletas; secundário de 384 tiles, 384
             metatiles e 6 paletas (vagas 7 a 12). O id global do metatile
             secundário é 640 + local, NÃO 512 + local.
  tiles      o `tiles.png` tem 272 tiles de 384 e sobram 112 vagas. Compactar
             NÃO abre vaga nenhuma (a conta cai no mesmo múltiplo de 16) e há 30
             vagas PINADAS porque metatiles do PRIMÁRIO `gTileset_JohtoNorthWest`
             referenciam tiles deste secundário (o 583 do primário pede os locais
             98, 99, 101 e 102). Por isso o `compacta_tileset.py` NÃO foi rodado:
             seria risco de graça.
  metatiles  o `metatiles.bin` tem 384 de 384, CHEIO, e o
             `metatile_attributes.bin` tem 768 B, ou seja 2 bytes por metatile.
             Não há vaga nova: esta passada SOBRESCREVE vagas mortas. Medido, os
             locais que NEM a cidade NEM a `Route37` usam são 74, e é só dentro
             deles que se escreve. Os 25 que só a rota usa (936 a 939, 944 a 947,
             949, 950, 952, 953, 955, 957 a 960, 963, 964, 976, 977, 984, 985,
             1016 e 1017) ficam intactos, senão a prova de 0 pixel da rota irmã
             reprova.
  paleta     ZERO vaga. As seis vagas do secundário aparecem em metatile vivo, a
             menor união de um par em uso é 10+11 = 23 cores e a vaga cabe 15:
             nenhum par cabe junto e a repactuação é impossível. Contando índice
             a índice fica ainda mais claro: das 96 entradas das seis vagas, só
             UMA está morta (o índice 15 da vaga 8). Portanto o
             `compacta_paletas.py` NÃO foi rodado (e ele tem defeito conhecido em
             tileset com tile usado por DUAS paletas, e aqui são 27), e toda arte
             que entra é reindexada para cor que JÁ existe, sem aproximar nenhuma.

O QUE O TESTE DE OLHO REPROVOU, e são duas versões inteiras que não viraram
commit. As duas estão aqui escritas porque a próxima cidade não precisa
descobrir de novo:

  1. IMPORTAR O CHÃO DO GS CHRONICLES INTEIRO. A Ecruteak do GS Chronicles
     (secundário 0x2D4B3C, primário 0x2D4A94, mapa g03m06 de 68x46) tem uma
     família de laje retangular (os metatiles 725, 607, 566, 567, 574, 575, 582,
     583, 591 e 599) que reindexa muito bem para os nossos três cinzas: a rampa
     dela é de SEIS tons ((152,160,144), (144,152,136), (144,144,136),
     (136,144,136), (128,136,128) e (112,112,120)) e cai por luminância nos
     nossos (192,192,192), (176,176,176), (160,160,160) e (128,128,136). Uma
     prancha de 14x9 células espalhando essas peças mostrou POR QUE elas não
     servem: as linhas de junta delas não são textura, são BORDA de plataforma, e
     espalhadas elas se cruzam em ângulo reto e viram um labirinto de riscos que
     não fecham. Peça de chão de fora só serve espalhada se ela for ISOTRÓPICA, e
     essa não é.
  2. MEDALHÃO E LAJE LAVRADA COMO ACENTO. O secundário de praça do mesmo hack
     (0x2D4B54) tem um medalhão redondo (metatiles 520 e 522) e lajes lavradas
     (512, 514 e 521) que reindexam bem sozinhos. Espalhados de um em um sobre o
     nosso calçamento, porém, eles não leem como pedra lavrada: leem como SÍMBOLO
     solto, um desenho escuro boiando no meio do calçamento. Acento geométrico só
     funciona em área contínua, e área contínua aqui exigiria repintar também as
     costuras 746, 748, 739 e 755, que são a borda entre a rua e o lote.

A TERCEIRA VERSÃO É A QUE ENTROU, e a regra dela é uma frase: A RUA CONTINUA
SENDO A NOSSA PEDRA, e o que muda é o ARRANJO dela. O calçamento cinza do
`gTileset_EcruteakCity` não é um desenho de 16x16: são TREZE tiles de 8x8 (os
locais 96 a 108) que o artista desenhou para trocar de quadrante. O 724 usa
(101, 102 / 98, 99) e a própria árvore já tem quatro arranjos diferentes vivos
(718, 719, 726 e 727). Esta passada escreve ONZE arranjos novos, sempre com tile
que já existe e paleta que já existe:

    custo em tile   ZERO
    custo em cor    ZERO
    custo em ROM    ZERO (o `metatiles.bin` já tem 384 entradas; sobrescrever
                    vaga morta não muda um byte de tamanho)

Os onze não são escolha de gosto. Cada quadrante só recebe tile que o artista JÁ
pôs naquele quadrante em algum metatile vivo (o canto superior esquerdo aceita
101, 103 ou 108; o superior direito 102, 100 ou 107; o inferior esquerdo 98, 106
ou 97; o inferior direito 99, 105 ou 97), o que dá 81 arranjos possíveis, e
dentro deles a escolha é gulosa por MAIOR DISTÂNCIA MÍNIMA de cor aos arranjos já
escolhidos. O menor par do conjunto final fica em 3,25 de distância média por
canal, e o auto-teste reprova qualquer par abaixo de `PISO_VARIANTE`: variante
com distância zero é variante nenhuma, e enganaria a régua sem mudar um pixel.

O MÓVEL É O QUE FAZ A CIDADE, e quase todo ele já estava desenhado e sem uso.
O truque é de montagem e não de arte: o 724 é `layerType` COVERED com a arte do
calçamento na camada de CIMA e a grama do primário na de BAIXO, invisível. Para
pôr móvel sobre a pedra basta DESCER o calçamento para a camada de baixo e usar
a de cima para a peça. Como COVERED põe as DUAS camadas abaixo do sprite
(`DrawMetatile` em `src/field_camera.c`), o jogador parado ao sul aparece na
frente da peça, que é o que a regra 3 da onda pede da base de um móvel.

  Oito peças saíram de metatiles que o repositório já tinha e que NENHUM dos dois
  mapas do tileset usava, ou que usava com outro chão embaixo:

    canteiro de flores   camada de cima do 767 (tiles 508 a 511 do primário)
    urna dourada         camada de cima do 749 (tiles 755 a 758, vaga 9)
    pedestal de pedra    camada de cima do 956 (tiles 753 e 754, vaga 9)
    banco de pedra       camada de cima do 960 (tiles 721 a 724, vaga 7)
    bebedouro            camada de cima do 963 (tiles 721 a 724, vaga 7)
    quadro de avisos     camada de cima do 943 (tiles 304, 305, 320 e 321, vaga 2)
    placa de madeira     camada de cima do 942 (tiles 364, 365, 380 e 381, vaga 1)
    arbusto (par)        camada de cima do 26 e do 27 do PRIMÁRIO (tiles 38, 39,
                         54 e 55, vaga 0)

  Nenhuma delas custa tile nem cor: são entradas de metatile apontando para tile
  que já está compilado. O que custa é a VAGA de metatile, e ela sai das 74
  mortas.

A ÚNICA ARTE IMPORTADA É O MARCO DE PEDRA, e ela entra porque é a peça que a
cidade não tinha. `Pokémon GS Chronicles` build 2.7.6 (base FireRed BPRE mas com
split de Emerald, 512/512/6), secundário 0x2D4B3C, metatiles 693 e 706: um par de
pilares de pedra de topo chanfrado, que na fonte alinha a beira de um caminho de
areia. A extração NÃO é por diferença contra o chão liso da fonte, e isso é
decisão consciente: ali o chão é areia com BORDA DE GRAMA, e a diferença traria
tufo verde junto com o pilar. A máscara é por COR: entram só os cinco tons do
objeto, e todo o resto do quadrado é o NOSSO calçamento, pixel a pixel. Os cinco
caem por luminância em cinco cores que a vaga 9 JÁ tem:

    (192,192,184) -> (192,192,192)      (56,64,72) -> (64,72,104)
    (144,144,136) -> (160,160,160)      (40,48,56) -> (64,72,104)
    (104,104,96)  -> (96,104,120)

  Nenhuma cor nova, nenhuma cor aproximada: os cinco alvos são índices vivos da
  vaga 9 e continuam com o RGB que tinham. O que cresce é o `tiles.png`, e só nos
  quadrantes em que existe pixel de pilar.

  ATRIBUTO ESCRITO À MÃO, peça por peça, e o motivo está no PRD (risco 3): o
  `metatile_attributes` do GS Chronicles tem QUATRO bytes e o nosso tem DOIS, e
  importar sem reescrever PERDE comportamento. Os dois marcos entram com
  0x1000, ou seja comportamento `MB_NORMAL` e `layerType` COVERED, que é o mesmo
  atributo do 724 que eles substituem e o que a regra 5 da onda exige de célula
  solidificada. Comportamento zerado é a escolha certa aqui porque o pilar não é
  água, não é grama alta, não é porta e não dispara script: é cenário sólido, e
  quem o torna intransponível é a COLISÃO, não o comportamento.

A LENTE, e ela é a regra que decide o desenho do móvel. A regra 3 da onda cobra
`(comportamento, layerType)` IDÊNTICO em toda célula que continua andável, e o
724 é (0x00, COVERED). Logo:

  - toda laje nova entra com atributo 0x1000, igual ao 724, e a célula continua
    andável: a lente não se mexe;
  - todo móvel de rua é de UMA célula, SÓLIDO e COVERED. Móvel de duas células
    de altura precisaria do topo ANDÁVEL em `NORMAL`, e o topo aqui é uma célula
    de rua que hoje é COVERED: trocar o `layerType` dela quebraria a regra 3. Por
    isso a lanterna suspensa dos metatiles 750 e 751, que é `NORMAL`, ficou de
    fora desta passada, e está escrito aqui para ninguém tentar de novo sem ver
    o custo.

Uso:
    python3 dev_scripts/pedra_ecruteak.py            # planeja e mostra, sem gravar
    python3 dev_scripts/pedra_ecruteak.py --aplicar  # grava tileset e map.bin
    python3 dev_scripts/pedra_ecruteak.py --desfazer # volta ao master
    python3 dev_scripts/pedra_ecruteak.py --extrai   # regera o kit a partir da ROM
    python3 dev_scripts/pedra_ecruteak.py --demo     # auto-teste (bloco T204)
"""
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")

KIT_JSON = f"{RAIZ}/dev_scripts/pedra_ecruteak_kit.json"
PLANO = f"{RAIZ}/dev_scripts/pedra_ecruteak.json"
DESTINO = f"{RAIZ}/data/tilesets/secondary/ecruteak_city"

PRIMARIO = "gTileset_JohtoNorthWest"
SECUNDARIO = "gTileset_EcruteakCity"
ALVO = "EcruteakCity"
# os DOIS layouts que dividem o gTileset_EcruteakCity. A rota e a prova de não
# regressao: ela tem que renderizar com ZERO pixel diferente.
IRMAOS = ["EcruteakCity", "Route37"]

N_META_PRI = 640
N_TILES_PRI = 640
TETO_TILES = 384
TETO_META = 384
TILE_LOCAL_0 = 272        # primeira vaga livre do tiles.png (272 tiles hoje)
VAGA_PEDRA = 9            # a vaga de paleta do calçamento cinza
TETO_REGUA = 20.0
PISO_VARIANTE = 3.0       # distância RGB media mínima entre duas lajes

CARIMBO = 724             # o calçamento da rua
LOTE = 714                # o calçamento marrom dos lotes

# Os TREZE tiles de calçamento cinza, e o quadrante em que o artista pos cada um.
# Sai de varrer os metatiles vivos do próprio tileset, não de gosto.
QUADRANTES = [(101, 103, 108), (102, 100, 107), (98, 106, 97), (99, 105, 97)]
LAJE_BASE = (101, 102, 98, 99)          # o arranjo do 724
LAJE_LOTE = (109, 110, 111, 112)        # o calçamento marrom do 714

# ------------------------------------------------------------------- a FONTE
GSC = dict(slug="gs-chronicles", hack="Pokemon GS Chronicles", versao="build 2.7.6 (19/06/2024)",
           autor="Overlord Kaktus / G0LD",
           creditado="RHH (Rom Hacking Hideout) e o pokemonHnS, que o proprio "
                     "README do hack manda creditar",
           md5="d50d50b2ed8e462882aa5f30cb056a41",
           base="FireRed (BPRE) com split de Emerald",
           pri=0x2D4A94, sec=0x2D4B3C, split=(512, 512, 6),
           mapa_amostra="grupo 3, mapa 6 (68x46), a Ecruteak do hack")
# Os metatiles do hack de onde sai o marco, e as cinco cores do objeto.
MARCOS = [dict(nome="marco de pedra", gsc=693),
          dict(nome="marco de pedra gasto", gsc=706)]
COR_DO_MARCO = {(192, 192, 184): 3, (144, 144, 136): 2, (104, 104, 96): 8,
                (56, 64, 72): 7, (40, 48, 56): 7}

# ---------------------------------------------------- o que já e NOSSO
# Cada móvel e a camada de CIMA de um metatile que já existe, montada sobre o
# nosso calçamento. `par` marca peca de duas células (esquerda e direita).
MOVEIS = [
    dict(nome="canteiro de flores", doador=767, quantos=8, espaco=4),
    dict(nome="arbusto",            doador=26, par=27, quantos=4, espaco=6),
    dict(nome="urna dourada",       doador=749, quantos=4, espaco=6),
    dict(nome="pedestal de pedra",  doador=956, quantos=3, espaco=7),
    dict(nome="banco de pedra",     doador=960, quantos=3, espaco=7),
    dict(nome="bebedouro",          doador=963, quantos=2, espaco=9),
    dict(nome="quadro de avisos",   doador=943, quantos=2, espaco=9),
    dict(nome="placa de madeira",   doador=942, quantos=3, espaco=8),
]
# Os mesmos móveis, montados sobre o calçamento MARROM do lote.
MOVEIS_LOTE = [
    dict(nome="canteiro no lote", doador=767, quantos=5, espaco=4),
    dict(nome="arbusto no lote",  doador=26, par=27, quantos=3, espaco=5),
    dict(nome="urna no lote",     doador=749, quantos=2, espaco=6),
    dict(nome="banco no lote",    doador=960, quantos=2, espaco=6),
]
MOVEIS_IMPORTADOS = [
    dict(nome="marco de pedra",       gsc=693, quantos=4, espaco=6),
    dict(nome="marco de pedra gasto", gsc=706, quantos=3, espaco=7),
]

N4 = [(0, -1), (1, 0), (0, 1), (-1, 0)]
N8 = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dx, dy) != (0, 0)]


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair idêntico em qualquer máquina e em qualquer versão de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


# ------------------------------------------------------------ leitura do nosso
def _layouts(_c={}):
    if not _c:
        d = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
        _c.update({l["id"]: l for l in d["layouts"] if l.get("id")})
    return _c


def layout_de(mapa):
    d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json"))
    return _layouts()[d["layout"]], d


def _tileset(rotulo, _c={}):
    if rotulo not in _c:
        import render_maps as RM
        _c[rotulo] = RM.carregar_tileset(rotulo)
    return _c[rotulo]


def _ler(nome):
    return open(f"{DESTINO}/{nome}", "rb").read()


def paleta(vaga, _c={}):
    """As 16 cores de uma vaga do secundário, lidas do `.pal` em disco."""
    if vaga not in _c:
        linhas = open(f"{DESTINO}/palettes/%02d.pal" % vaga).read().splitlines()[3:19]
        _c[vaga] = [tuple(int(v) for v in l.split()) for l in linhas]
    return _c[vaga]


def tiles_png(_c={}):
    """(pixels indexados do tiles.png, colunas). Índice de paleta, não cor."""
    if not _c:
        from PIL import Image
        im = Image.open(f"{DESTINO}/tiles.png")
        px = im.load()
        cols = im.size[0] // 8
        n = cols * (im.size[1] // 8)
        _c["grade"] = [[[px[(t % cols) * 8 + x, (t // cols) * 8 + y] for x in range(8)]
                        for y in range(8)] for t in range(n)]
        _c["cols"] = cols
    return _c["grade"], _c["cols"]


def _attr_pri(_c={}):
    if not _c:
        import render_maps as RM
        caminho = os.path.join(RM.caminho_tileset(PRIMARIO), "metatile_attributes.bin")
        _c["b"] = open(caminho, "rb").read()
    return _c["b"]


def entradas_de(mid, metas_novos=None):
    """As 8 palavras de um metatile, do primário ou do secundário."""
    if metas_novos and mid >= N_META_PRI and (mid - N_META_PRI) in metas_novos:
        return list(metas_novos[mid - N_META_PRI])
    if mid < N_META_PRI:
        return list(struct.unpack_from("<8H", _tileset(PRIMARIO)["metatiles"], mid * 16))
    return list(struct.unpack_from("<8H", _ler("metatiles.bin"), (mid - N_META_PRI) * 16))


def attr_de(mid, attrs_novos=None):
    if attrs_novos and mid >= N_META_PRI and (mid - N_META_PRI) in attrs_novos:
        return attrs_novos[mid - N_META_PRI]
    if mid < N_META_PRI:
        return struct.unpack_from("<H", _attr_pri(), mid * 2)[0]
    return struct.unpack_from("<H", _ler("metatile_attributes.bin"), (mid - N_META_PRI) * 2)[0]


def pixels_de(mid, tiles_novos=None, metas_novos=None):
    """Os 256 pixels RGB de um metatile, com as duas camadas compostas.

    Le do MESMO carregador do `render_maps.py`, de proposito: se a leitura
    divergir do render, o auto-teste passa a medir uma segunda verdade.
    """
    import render_maps as RM
    from PIL import Image
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    pals = {i: (tp["paletas"] if i < 7 else ts["paletas"]).get(i, [(0, 0, 0)] * 16)
            for i in range(16)}
    ents = entradas_de(mid, metas_novos)
    im = Image.new("RGB", (16, 16), (0, 0, 0))
    p = im.load()
    for cam in range(2):
        for q in range(4):
            v = ents[cam * 4 + q]
            tid = v & 0x3FF
            if cam and not tid:
                continue
            if tiles_novos is not None and tid >= N_TILES_PRI and (tid - N_TILES_PRI) in tiles_novos:
                tile = tiles_novos[tid - N_TILES_PRI]
            else:
                tile = RM.resolver_tile(tp, ts, tid)
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                             pals[(v >> 12) & 0xF], bool(v & 0x400), bool(v & 0x800))
    return [[im.getpixel((x, y)) for x in range(16)] for y in range(16)]


def distancia(a, b):
    """Distancia media por canal entre dois metatiles de 16x16."""
    s = 0
    for y in range(16):
        for x in range(16):
            s += abs(a[y][x][0] - b[y][x][0]) + abs(a[y][x][1] - b[y][x][1]) + \
                 abs(a[y][x][2] - b[y][x][2])
    return s / (256.0 * 3)


def blockdata_base(mapa):
    """As palavras do `map.bin` do MASTER, mesmo com a passada já aplicada.

    Existe porque `vagas_mortas()` NAO pode olhar para o disco de hoje: depois de
    `--aplicar`, as vagas que esta passada escreveu passariam a contar como
    vivas, a segunda rodada escolheria OUTRAS vagas e deixaria as primeiras para
    tras. Idempotencia aqui não e elegancia, e a diferença entre rodar duas vezes
    e sujar o tileset com trinta metatiles órfãos.
    """
    L, _ = layout_de(mapa)
    b = open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read()
    v = list(struct.unpack_from("<%dH" % (len(b) // 2), b, 0))
    if mapa == ALVO and os.path.isfile(PLANO):
        for i, antes, depois in json.load(open(PLANO))["escritas"]:
            if v[i] == depois:
                v[i] = antes
    return v


def usados_por(mapas):
    """Todo metatile que aparece no map.bin (base) ou no border.bin dos mapas."""
    s = set()
    for m in mapas:
        L, _ = layout_de(m)
        s.update(w & 0x3FF for w in blockdata_base(m))
        b = open(f"{RAIZ}/{L['border_filepath']}", "rb").read()
        for i in range(0, len(b) - 1, 2):
            s.add(struct.unpack_from("<H", b, i)[0] & 0x3FF)
    return s


def vagas_mortas(_c={}):
    """Os locais do secundário que NEM a cidade NEM a rota irmã usam.

    Sobrescrever qualquer outro quebraria a prova de 0 pixel da `Route37`, e a
    diferença entre "a cidade não usa" e "ninguém usa" e exatamente a armadilha
    que o guia da onda registra.
    """
    if not _c:
        vivos = usados_por(IRMAOS)
        _c["v"] = [m - N_META_PRI for m in range(N_META_PRI, N_META_PRI + TETO_META)
                   if m not in vivos]
    return list(_c["v"])


# ---------------------------------------------------------------- a EXTRACAO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO."""
    b = dados[local * 32:local * 32 + 32]
    if len(b) < 32:
        return [[0] * 8 for _ in range(8)]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb_gba(pal_bytes, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits deslocados TRES
    casas, não esticados para 0..255. Todo `.pal` deste tileset esta nessa
    conta (192 = 24 << 3, 104 = 13 << 3)."""
    c = struct.unpack_from("<16H", pal_bytes, i * 32)
    return [tuple(((v >> s) & 0x1F) << 3 for s in (0, 5, 10)) for v in c]


def extrai():
    """Regera `pedra_ecruteak_kit.json` a partir da ROM privada.

    So roda na máquina que tem `fontes-mapas/romhacks/`. O que sai daqui e a
    MASCARA convertida (índice da nossa vaga 9, com -1 onde o pixel e nosso),
    nunca a ROM nem pedaco dela.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("nao achei fontes-mapas/romhacks: --extrai so roda na "
                         "maquina que tem as ROMs. O kit ja extraido esta em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402

    pasta = os.path.join(ferr, GSC["slug"])
    gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
    caminho = os.path.join(pasta, gba)
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    if md5 != GSC["md5"]:
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s"
                         % (gba, md5, GSC["md5"]))
    r = Rom(caminho)
    # O split e o de EMERALD mesmo a base sendo FireRed: e a armadilha da seção
    # 3.1 do PRD, e ler com 640/640/7 devolve metatile fora de lugar.
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = GSC["split"]
    t1, t2 = r.parse_tileset(GSC["pri"]), r.parse_tileset(GSC["sec"])
    if t1 is None or t2 is None:
        raise SystemExit("o par 0x%X / 0x%X nao abriu" % (GSC["pri"], GSC["sec"]))
    largura_attr = len(t2["attr"]) // (len(t2["meta"]) // 16)
    pal = {i: _rgb_gba(t1["pal"] if i < 6 else t2["pal"], i) for i in range(16)}

    def celula(loc):
        """Os 16x16 pixels RGB de um metatile da fonte, com flip aplicado."""
        fora = [[None] * 16 for _ in range(16)]
        ents = struct.unpack_from("<8H", t2["meta"], loc * 16)
        for cam in range(2):
            for q in range(4):
                v = ents[cam * 4 + q]
                tid = v & 0x3FF
                if cam and not tid:
                    continue
                px = (_nibbles(t2["tiles"], tid - r.n_tiles_pri)
                      if tid >= r.n_tiles_pri else _nibbles(t1["tiles"], tid))
                if v & 0x400:
                    px = [list(reversed(l)) for l in px]
                if v & 0x800:
                    px = list(reversed(px))
                cores = pal[(v >> 12) & 0xF]
                for y in range(8):
                    for x in range(8):
                        c = px[y][x]
                        if c or cam == 0:
                            fora[(q // 2) * 8 + y][(q % 2) * 8 + x] = cores[c]
        return fora

    nossas = paleta(VAGA_PEDRA)
    for cor, idx in COR_DO_MARCO.items():
        if idx >= len(nossas):
            raise SystemExit("indice %d fora da vaga %d" % (idx, VAGA_PEDRA))
    pecas = []
    for m in MARCOS:
        A = celula(m["gsc"] - GSC["split"][0])
        masc = [[COR_DO_MARCO.get(A[y][x], -1) for x in range(16)] for y in range(16)]
        n = sum(1 for l in masc for v in l if v >= 0)
        if n < 40:
            raise SystemExit("%s: so %d pixels de objeto, a mascara por cor nao "
                             "pegou o pilar" % (m["nome"], n))
        pecas.append(dict(nome=m["nome"], gsc=m["gsc"], pixels=n, mascara=masc,
                          cores_da_fonte=sorted({str(A[y][x]) for y in range(16)
                                                 for x in range(16)
                                                 if A[y][x] in COR_DO_MARCO})))
    kit = dict(
        fonte=dict(hack=GSC["hack"], versao=GSC["versao"], autor=GSC["autor"],
                   creditado=GSC["creditado"], md5=GSC["md5"], base=GSC["base"],
                   primario="0x%X" % GSC["pri"], secundario="0x%X" % GSC["sec"],
                   split=list(GSC["split"]), largura_do_atributo=largura_attr,
                   mapa_amostra=GSC["mapa_amostra"]),
        remap={str(k): v for k, v in COR_DO_MARCO.items()},
        vaga=VAGA_PEDRA,
        paleta=[list(c) for c in nossas],
        pecas=pecas,
    )
    with open(KIT_JSON, "w") as f:
        json.dump(kit, f, indent=1, sort_keys=True)
    print("kit gravado em", os.path.relpath(KIT_JSON, RAIZ))
    print("  atributo da fonte: %d bytes (o nosso e 2, entao o comportamento foi "
          "reescrito a mao)" % largura_attr)
    for p in pecas:
        print("  %-24s %3d pixels de objeto" % (p["nome"], p["pixels"]))
    return 0


def kit(_c={}):
    if not _c:
        if not os.path.isfile(KIT_JSON):
            raise SystemExit("falta %s: rode --extrai na maquina que tem as ROMs"
                             % os.path.relpath(KIT_JSON, RAIZ))
        _c.update(json.load(open(KIT_JSON)))
    return _c


# --------------------------------------------------------------- o CATALOGO
def _pal(v):
    return (v >> 12) & 0xF


def _laje_entradas(arranjo, vaga=VAGA_PEDRA):
    """As quatro palavras da camada de CIMA de uma laje: tile local + vaga."""
    return [(N_TILES_PRI + t) | (vaga << 12) for t in arranjo]


def base_do_724(_c={}):
    """A camada de BAIXO do 724, que e grama do primário e nenhum pixel dela
    aparece: o calçamento da camada de cima e opaco nos 256 pixels."""
    if not _c:
        e = entradas_de(CARIMBO)
        if any(v & 0x3FF for v in e[4:]) is False:
            raise SystemExit("o 724 nao tem camada de cima; a leitura esta errada")
        _c["e"] = e[:4]
    return list(_c["e"])


def arranjo_do(mid):
    """O arranjo de tiles da camada de CIMA, se o metatile for laje pura."""
    e = entradas_de(mid)
    if e[:4] != base_do_724():
        return None
    fora = []
    for v in e[4:]:
        t = (v & 0x3FF) - N_TILES_PRI
        if v & 0xC00 or _pal(v) != VAGA_PEDRA or not (94 <= t <= 108):
            return None
        fora.append(t)
    return tuple(fora)


def lajes_novas(quantas=11):
    """Os arranjos novos de calçamento, escolhidos por MAIOR DISTANCIA MINIMA.

    O espaco de busca não e livre: cada quadrante só aceita tile que o artista já
    pos NAQUELE quadrante em algum metatile do tileset (`QUADRANTES`). Isso e o
    que faz a emenda fechar; escolher os quatro tiles por distância sozinha
    produz um mosaico picado, e isso foi visto em prancha antes de virar codigo.
    """
    import itertools
    # A referência sai só dos metatiles VIVOS (os que a cidade ou a rota usam).
    # Varrer as 384 vagas tornaria a escolha dependente do que esta passada já
    # escreveu nas vagas mortas, e a segunda rodada daria outro conjunto.
    ref = {a for m in sorted(usados_por(IRMAOS)) if m >= N_META_PRI
           for a in [arranjo_do(m)] if a}
    px = {}

    def P(a):
        if a not in px:
            px[a] = pixels_de(CARIMBO, metas_novos={
                CARIMBO - N_META_PRI: base_do_724() + _laje_entradas(a)})
        return px[a]

    escolhidos, alvo = [], [P(a) for a in sorted(ref)]
    cands = [c for c in itertools.product(*QUADRANTES) if c not in ref]
    while len(escolhidos) < quantas:
        melhor = None
        for c in cands:
            if c in escolhidos:
                continue
            dm = min(distancia(P(c), a) for a in alvo)
            if melhor is None or dm > melhor[0] + 1e-9:
                melhor = (dm, c)
        escolhidos.append(melhor[1])
        alvo.append(P(melhor[1]))
    return escolhidos


def catalogo(_c={}):
    """Tudo que esta passada escreve no tileset, com a vaga de cada peca.

    A alocacao e deterministica: as vagas saem de `vagas_mortas()` em ordem
    crescente, tirando as três que DOAM arte (749, 767 e 956), que precisam
    continuar inteiras para o próximo que ler este script.
    """
    if _c:
        return _c
    doadores = {749, 767, 956}
    pool = [v for v in sorted(vagas_mortas())
            if (v + N_META_PRI) not in doadores]
    fila = iter(pool)
    lajes, moveis, tiles_novos = [], [], {}
    base = base_do_724()
    for i, arr in enumerate(lajes_novas()):
        lajes.append(dict(nome="laje %d" % (i + 1), local=next(fila),
                          entradas=base + _laje_entradas(arr),
                          attr=attr_de(CARIMBO), arranjo=list(arr)))
    base_rua = _laje_entradas(LAJE_BASE)
    base_lote = _laje_entradas(LAJE_LOTE)

    def monta(spec, chao, sufixo):
        fora = []
        for m in spec:
            topo = entradas_de(m["doador"])[4:]
            local = next(fila)
            peca = dict(nome=m["nome"], local=local, entradas=chao + list(topo),
                        attr=0x1000, doador=m["doador"], quantos=m["quantos"],
                        espaco=m["espaco"], solido=True, sufixo=sufixo)
            if m.get("par"):
                peca["par_local"] = next(fila)
                peca["par_entradas"] = chao + list(entradas_de(m["par"])[4:])
                peca["par_doador"] = m["par"]
            fora.append(peca)
        return fora

    moveis += monta(MOVEIS, base_rua, "rua")
    moveis += monta(MOVEIS_LOTE, base_lote, "lote")

    # ------------------------------------------------------ o marco IMPORTADO
    dados = kit()
    por_nome = {p["nome"]: p for p in dados["pecas"]}
    grade, _cols = tiles_png()
    vaga_tile = TILE_LOCAL_0
    for m in MOVEIS_IMPORTADOS:
        p = por_nome[m["nome"]]
        masc = p["mascara"]
        topo = []
        for q in range(4):
            ox, oy = (q % 2) * 8, (q // 2) * 8
            bloco = [[masc[oy + y][ox + x] for x in range(8)] for y in range(8)]
            if all(v < 0 for l in bloco for v in l):
                topo.append(0)          # quadrante sem pilar: camada de cima vazia
                continue
            tiles_novos[vaga_tile] = [[max(v, 0) for v in l] for l in bloco]
            topo.append((N_TILES_PRI + vaga_tile) | (VAGA_PEDRA << 12))
            vaga_tile += 1
        moveis.append(dict(nome=m["nome"], local=next(fila),
                           entradas=base_rua + topo, attr=0x1000,
                           doador=None, gsc=m["gsc"], quantos=m["quantos"],
                           espaco=m["espaco"], solido=True, sufixo="rua"))
    _c.update(lajes=lajes, moveis=moveis, tiles_novos=tiles_novos,
              vaga_tile_fim=vaga_tile)
    return _c


# --------------------------------------------------------- gravar o TILESET
def grava_tileset():
    """Escreve tiles.png, metatiles.bin e metatile_attributes.bin.

    Os DOIS binarios NAO mudam de tamanho: o `metatiles.bin` já tem as 384
    entradas e esta passada só reescreve vaga morta. O `tiles.png` cresce, e só
    ele, porque os oito tiles do marco importado não existiam.
    """
    from PIL import Image
    c = catalogo()
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    fim = max(c["vaga_tile_fim"], (antigo.size[1] // 8) * cols)
    if fim > TETO_TILES:
        raise SystemExit("o tiles.png passaria de %d tiles" % TETO_TILES)
    linhas = (fim + cols - 1) // cols
    novo = Image.new("P", (antigo.size[0], linhas * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    # O tiles.png do master carrega um bloco tRNS. Reescrever o arquivo SEM ele
    # não muda um pixel mas suja o diff, e o Pillow só o regrava se a chave for
    # passada no save.
    trns = antigo.info.get("transparency")
    px = novo.load()
    for v, tile in c["tiles_novos"].items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    if trns is None:
        novo.save(f"{DESTINO}/tiles.png")
    else:
        novo.save(f"{DESTINO}/tiles.png", transparency=trns)

    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    n0, a0 = len(meta), len(attr)
    mortas = set(vagas_mortas())
    for peca in c["lajes"] + c["moveis"]:
        alvos = [(peca["local"], peca["entradas"])]
        if peca.get("par_local") is not None:
            alvos.append((peca["par_local"], peca["par_entradas"]))
        for local, ents in alvos:
            if local not in mortas:
                raise SystemExit("a vaga %d nao esta morta: escrever nela "
                                 "quebraria a Route37" % (local + N_META_PRI))
            for i, v in enumerate(ents):
                struct.pack_into("<H", meta, local * 16 + i * 2, v)
            struct.pack_into("<H", attr, local * 2, peca["attr"])
    if len(meta) != n0 or len(attr) != a0:
        raise SystemExit("os binarios de metatile mudaram de tamanho")
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------- o PLANO do mapa
def grade(mapa):
    L, d = layout_de(mapa)
    W, H = L["width"], L["height"]
    b = open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read()
    v = list(struct.unpack_from("<%dH" % (W * H), b, 0))
    return v, W, H, L, d


def eventos(d):
    """Toda célula que carrega evento: warp, objeto, placa ou gatilho."""
    s = set()
    for chave in ("object_events", "warp_events", "bg_events", "coord_events"):
        for e in d.get(chave) or []:
            s.add((e["x"], e["y"]))
    return s


def andavel(v, i):
    return ((v[i] >> 10) & 3) == 0


def componentes(v, W, H):
    """Rotulo de componente conexo do chão andável, com a regra de elevação do
    `enfeita_cidades.py` (elevação 0 e curinga)."""
    rot = [-1] * (W * H)
    n = 0
    for i in range(W * H):
        if not andavel(v, i) or rot[i] >= 0:
            continue
        pilha, rot[i] = [i], n
        while pilha:
            j = pilha.pop()
            x, y = j % W, j // W
            ej = (v[j] >> 12) & 0xF
            for dx, dy in N4:
                a, b = x + dx, y + dy
                if not (0 <= a < W and 0 <= b < H):
                    continue
                k = b * W + a
                if rot[k] >= 0 or not andavel(v, k):
                    continue
                ek = (v[k] >> 12) & 0xF
                if ej and ek and ej != ek:
                    continue
                rot[k] = n
                pilha.append(k)
        n += 1
    return rot, n


def _liga_sem(v, W, H, i):
    """True se solidificar a célula i NAO separa nenhum vizinho andável dela dos
    outros. E o teste de vértice de corte, e ele e o portao do espalhamento: sem
    ele, uma peca no meio de um corredor de uma célula fecha a cidade."""
    x, y = i % W, i // W
    viz = []
    for dx, dy in N4:
        a, b = x + dx, y + dy
        if 0 <= a < W and 0 <= b < H and andavel(v, b * W + a):
            viz.append(b * W + a)
    if len(viz) <= 1:
        return True
    guarda = v[i]
    v[i] = (v[i] & ~(3 << 10)) | (1 << 10)
    rot, _ = componentes(v, W, H)
    v[i] = guarda
    return len({rot[j] for j in viz}) == 1


def plano_mapa():
    """A lista de (índice, palavra_antes, palavra_depois) desta passada."""
    c = catalogo()
    v, W, H, L, d = grade(ALVO)
    base = base_do_plano(v)
    v = list(base)
    ev = eventos(d)
    perto_de_warp = set()
    for e in d.get("warp_events") or []:
        for dx, dy in N4 + [(0, 0)]:
            perto_de_warp.add((e["x"] + dx, e["y"] + dy))

    # ------------------------------------------------------------ o CALCAMENTO
    lajes = [CARIMBO] + [l["local"] + N_META_PRI for l in c["lajes"]]
    escritas = {}
    for i in range(W * H):
        if (v[i] & 0x3FF) != CARIMBO:
            continue
        x, y = i % W, i // W
        novo = lajes[_mistura(x, y, 0x9E37) % len(lajes)]
        if novo != CARIMBO:
            escritas[i] = (v[i] & ~0x3FF) | novo
            v[i] = escritas[i]

    # --------------------------------------------------------------- o MOVEL
    def elegivel(i, chao):
        x, y = i % W, i // W
        if (v[i] & 0x3FF) not in chao or not andavel(v, i):
            return False
        if (x, y) in ev or (x, y) in perto_de_warp:
            return False
        livres = 0
        for dx, dy in N8:
            a, b = x + dx, y + dy
            if 0 <= a < W and 0 <= b < H and andavel(v, b * W + a):
                livres += 1
        return livres >= 5

    def encostado(i):
        x, y = i % W, i // W
        for dx, dy in N4:
            a, b = x + dx, y + dy
            if not (0 <= a < W and 0 <= b < H):
                return True
            if not andavel(v, b * W + a):
                return True
        return False

    chao_de = {"rua": set(lajes), "lote": {LOTE}}
    postos, colocados = [], []
    for peca in c["moveis"]:
        chao = chao_de[peca["sufixo"]]
        alvo = peca["quantos"]
        # Movel de rua encosta na PAREDE. Ordenar por "tem vizinho sólido" antes
        # do sorteio tira a peca do meio da calcada, que e onde ela lia como
        # confete: banco, placa e canteiro moram na beira, não no eixo.
        cands = sorted((i for i in range(W * H) if elegivel(i, chao)),
                       key=lambda i: (0 if encostado(i) else 1,
                                      _mistura(i, peca["local"], 0x1234)))
        posto = 0
        for i in cands:
            if posto >= alvo:
                break
            x, y = i % W, i // W
            if any(max(abs(x - a), abs(y - b)) < peca["espaco"]
                   for a, b, n in postos if n == peca["nome"]):
                continue
            if any(max(abs(x - a), abs(y - b)) < 2 for a, b, _ in postos):
                continue
            celulas = [i]
            if peca.get("par_local") is not None:
                j = i + 1
                if x + 1 >= W or not elegivel(j, chao):
                    continue
                celulas.append(j)
            if not all(_liga_sem(v, W, H, k) for k in celulas):
                continue
            ok = True
            for k, local in zip(celulas, [peca["local"]] + ([peca["par_local"]]
                                if peca.get("par_local") is not None else [])):
                pal = (v[k] & ~0x3FF) | (local + N_META_PRI)
                pal = (pal & ~(3 << 10)) | (1 << 10)     # a célula vira SOLIDA
                escritas[k] = pal
                v[k] = pal
            if ok:
                for k in celulas:
                    postos.append((k % W, k // W, peca["nome"]))
                colocados.append((peca["nome"], x, y))
                posto += 1
        peca["postos"] = posto
    return base, v, escritas, colocados, W, H


def base_do_plano(v):
    """O `map.bin` do MASTER, mesmo que o disco já esteja com a passada aplicada.

    Sem isto o plano seria calculado em cima de si mesmo e a segunda rodada
    espalharia móvel sobre móvel.
    """
    if os.path.isfile(PLANO):
        g = json.load(open(PLANO))
        b = list(v)
        for i, antes, depois in g["escritas"]:
            if b[i] == depois:
                b[i] = antes
        return b
    return list(v)


# ---------------------------------------------------------------- a REGUA
def regua(v, W, H, metas_novos=None):
    """As mesmas contas de `dev_scripts/regua_cidades.py`, em memória.

    Fica aqui para o auto-teste medir o plano ANTES de gravar; quem manda no
    número do relatorio continua sendo a régua do repositorio, rodada em disco.
    """
    import arte_ginasios_sinnoh as G
    import enfeita_cidades as E
    beh = G.comportamento(PRIMARIO, SECUNDARIO, N_META_PRI)
    agua = E.agua()
    mt = [c & 0x3FF for c in v]
    dentro = [mt[i] for i in range(W * H) if andavel(v, i) and beh(mt[i]) not in agua]
    f = collections.Counter(dentro)
    top = f.most_common(1)[0]
    return dict(andaveis=len(dentro), distintos=len(set(mt)),
                liso=round(top[1] * 100.0 / len(dentro), 1), chao=top[0],
                liso3=round(sum(n for _, n in f.most_common(3)) * 100.0 / len(dentro), 1))


# --------------------------------------------------------------------- rodagem
def roda(aplicar):
    c = catalogo()
    base, v, escritas, colocados, W, H = plano_mapa()
    antes = regua(base, W, H)
    depois = regua(v, W, H)
    print("EcruteakCity  liso %.1f%% (mt %d, %d andaveis) -> %.1f%% (mt %d, %d andaveis)"
          % (antes["liso"], antes["chao"], antes["andaveis"],
             depois["liso"], depois["chao"], depois["andaveis"]))
    solidas = sum(1 for k in escritas
                  if ((escritas[k] >> 10) & 3) and not ((base[k] >> 10) & 3))
    print("  lajes novas: %d   moveis: %d pecas em %d celulas solidificadas   "
          "tiles novos: %d" % (len(c["lajes"]), len(colocados), solidas,
                               len(c["tiles_novos"])))
    for m in c["moveis"]:
        print("    %-22s vaga %4d  %d de %d" % (m["nome"], m["local"] + N_META_PRI,
                                                m.get("postos", 0), m["quantos"]))
    if depois["liso"] > TETO_REGUA:
        raise SystemExit("o carimbo ficou em %.1f%%, acima do teto de %.1f%%"
                         % (depois["liso"], TETO_REGUA))
    if not aplicar:
        print("  (nada gravado; use --aplicar)")
        return 0
    grava_tileset()
    L, _ = layout_de(ALVO)
    b = bytearray(open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read())
    for i, palavra in escritas.items():
        struct.pack_into("<H", b, i * 2, palavra)
    open(f"{RAIZ}/{L['blockdata_filepath']}", "wb").write(bytes(b))
    with open(PLANO, "w") as f:
        json.dump(dict(mapa=ALVO, antes=antes, depois=depois,
                       escritas=sorted([i, base[i], escritas[i]] for i in escritas),
                       colocados=colocados,
                       lajes=[dict(nome=l["nome"], local=l["local"],
                                   arranjo=l["arranjo"]) for l in c["lajes"]],
                       moveis=[dict(nome=m["nome"], local=m["local"],
                                    par_local=m.get("par_local"),
                                    doador=m.get("doador"), gsc=m.get("gsc"),
                                    postos=m.get("postos", 0)) for m in c["moveis"]],
                       tiles_novos=sorted(c["tiles_novos"])), f, indent=1)
    print("  gravado: map.bin, metatiles.bin, metatile_attributes.bin, tiles.png")
    return 0


def desfaz():
    if not os.path.isfile(PLANO):
        raise SystemExit("nao ha plano gravado")
    g = json.load(open(PLANO))
    L, _ = layout_de(ALVO)
    b = bytearray(open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read())
    n = 0
    for i, antes, depois in g["escritas"]:
        if struct.unpack_from("<H", b, i * 2)[0] == depois:
            struct.pack_into("<H", b, i * 2, antes)
            n += 1
    open(f"{RAIZ}/{L['blockdata_filepath']}", "wb").write(bytes(b))
    print("map.bin: %d celulas voltaram. O tileset NAO volta sozinho: use git "
          "checkout em data/tilesets/secondary/ecruteak_city." % n)
    return 0


# ------------------------------------------------------------------ conferencia
def confere():
    """O que o commit afirma, medido de novo contra os arquivos em disco."""
    falhas = []

    def caso(n, cond, msg):
        print(f"  T204.{n} {'ok  ' if cond else 'FALHA'} {msg}")
        if not cond:
            falhas.append(n)
    return caso, falhas


def demo():
    """Auto-teste do bloco T204. Nao checa beleza: checa que o script sabe
    REPROVAR. Cada caso par e uma SABOTAGEM: se ela passar, a prova não vale."""
    import itertools
    from PIL import Image
    caso, falhas = confere()
    c = catalogo()

    # 1. o split de Johto lido dos arquivos, não decorado
    n_meta = len(_ler("metatiles.bin")) // 16
    larg = len(_ler("metatile_attributes.bin")) // n_meta
    caso(1, n_meta == TETO_META and larg == 2,
         "o gTileset_EcruteakCity tem %d metatiles e atributo de %d byte(s)" % (n_meta, larg))

    # 2. só vaga MORTA e escrita, e morta e "nem a cidade nem a Route37 usam"
    mortas = set(vagas_mortas())
    escritas = {p["local"] for p in c["lajes"] + c["moveis"]}
    escritas |= {p["par_local"] for p in c["moveis"] if p.get("par_local") is not None}
    caso(2, escritas <= mortas and len(mortas) == 74,
         "as %d vagas escritas estao entre as %d mortas" % (len(escritas), len(mortas)))

    # 3. SABOTAGEM: uma vaga que só a Route37 usa não pode passar por morta
    so_rota = usados_por(["Route37"]) - usados_por([ALVO])
    so_rota = {m - N_META_PRI for m in so_rota if m >= N_META_PRI}
    caso(3, so_rota and not (so_rota & mortas),
         "as %d vagas que SO a Route37 usa (936, 944, 952, 964, ...) ficam fora "
         "das mortas" % len(so_rota))

    # 4. nenhuma laje nova repete outra: distância RGB >= PISO_VARIANTE
    base = base_do_724()
    pix = {}
    for p in c["lajes"]:
        pix[p["nome"]] = pixels_de(CARIMBO, metas_novos={CARIMBO - N_META_PRI: p["entradas"]})
    pix["724"] = pixels_de(CARIMBO)
    pior = min(((distancia(pix[a], pix[b]), a, b)
                for a, b in itertools.combinations(sorted(pix), 2)))
    caso(4, pior[0] >= PISO_VARIANTE,
         "o par mais parecido de laje esta a %.2f (piso %.1f): %s x %s"
         % (pior[0], PISO_VARIANTE, pior[1], pior[2]))

    # 5. SABOTAGEM: duas lajes IGUAIS tem que reprovar o caso 4
    igual = distancia(pix["724"], pixels_de(CARIMBO,
                      metas_novos={CARIMBO - N_META_PRI: base + _laje_entradas(LAJE_BASE)}))
    caso(5, igual == 0.0 and igual < PISO_VARIANTE,
         "uma copia do 724 mede distancia %.2f e cairia no piso" % igual)

    # 6. a lente: laje andável mantem (comportamento, layerType) do 724
    a724 = attr_de(CARIMBO)
    caso(6, all(p["attr"] == a724 for p in c["lajes"]) and (a724 >> 12) == 1,
         "as %d lajes entram com o atributo 0x%04X do 724 (COVERED)"
         % (len(c["lajes"]), a724))

    # 7. móvel solidificado tem que ser COVERED, nunca NORMAL
    caso(7, all((p["attr"] >> 12) == 1 and (p["attr"] & 0xFF) == 0 for p in c["moveis"]),
         "os %d moveis entram em 0x1000: comportamento zerado e COVERED"
         % len(c["moveis"]))

    # 8. SABOTAGEM: um móvel em NORMAL seria o defeito E3 do mapas_qa
    caso(8, (0x0000 >> 12) != 1,
         "0x0000 e NORMAL (camada de cima no BG1, acima do boneco) e nao passaria no caso 7")

    # 9. o kit importado: atributo da fonte tem 4 bytes e o comportamento foi
    #    reescrito a mao
    k = kit()
    caso(9, k["fonte"]["largura_do_atributo"] == 4 and k["fonte"]["md5"] == GSC["md5"],
         "o kit veio de atributo de %d bytes (md5 %s), e por isso o comportamento "
         "dos dois marcos foi escrito a mao"
         % (k["fonte"]["largura_do_atributo"], k["fonte"]["md5"][:8]))

    # 10. toda cor da máscara importada JA existe na vaga 9, sem aproximar nada
    nossas = paleta(VAGA_PEDRA)
    idx = {v for p in k["pecas"] for l in p["mascara"] for v in l if v >= 0}
    caso(10, idx and all(0 <= i < 16 for i in idx) and
         [list(x) for x in nossas] == k["paleta"],
         "a mascara usa os indices %s da vaga %d, e o .pal em disco e o mesmo do kit"
         % (sorted(idx), VAGA_PEDRA))

    # 11. SABOTAGEM: cor da fonte fora do remap tem que virar -1 (transparente),
    #     nunca a cor mais parecida
    cru = {tuple(eval(s)) for p in k["pecas"] for s in p["cores_da_fonte"]}
    caso(11, cru <= set(COR_DO_MARCO) and len(cru) >= 4,
         "as %d cores de objeto da fonte estao todas no remap; o resto do quadrado "
         "ficou -1 e recebe o NOSSO pixel" % len(cru))

    # 12. o tiles.png só cresce, e os tiles vivos ficam intactos
    im = Image.open(f"{DESTINO}/tiles.png")
    n_tiles = (im.size[0] // 8) * (im.size[1] // 8)
    caso(12, n_tiles <= TETO_TILES and min(c["tiles_novos"], default=TILE_LOCAL_0) >= TILE_LOCAL_0,
         "o tiles.png tem %d tiles de %d e os %d novos comecam no %d"
         % (n_tiles, TETO_TILES, len(c["tiles_novos"]), TILE_LOCAL_0))

    # 13. a planta: colisão 1 -> 0 em zero células, elevação intacta
    v, W, H, L, d = grade(ALVO)
    b = base_do_plano(v)
    abre = sum(1 for i in range(W * H) if ((b[i] >> 10) & 3) and not ((v[i] >> 10) & 3))
    elev = sum(1 for i in range(W * H) if ((b[i] >> 12) & 0xF) != ((v[i] >> 12) & 0xF))
    caso(13, abre == 0 and elev == 0,
         "colisao 1->0 em %d celulas e elevacao mudada em %d" % (abre, elev))

    # 14. SABOTAGEM: a ligação a pe. Solidificar uma célula de corredor tem que
    #     ser recusada por `_liga_sem`
    corredor = None
    for i in range(W * H):
        if not andavel(v, i):
            continue
        if not _liga_sem(v, W, H, i):
            corredor = i
            break
    caso(14, corredor is not None,
         "existe pelo menos uma celula de corte no mapa (a %s) e `_liga_sem` a recusa"
         % (corredor and (corredor % W, corredor // W),))

    # 15. nenhum móvel caiu em célula de evento nem colado em warp
    ev = eventos(d)
    postos = {(x, y) for _, x, y in json.load(open(PLANO))["colocados"]} \
        if os.path.isfile(PLANO) else set()
    caso(15, postos and not (postos & ev),
         "as %d pecas colocadas nao pisam em nenhum dos %d eventos do mapa"
         % (len(postos), len(ev)))

    # 16. a régua chegou onde a onda pede
    r = regua(v, W, H)
    caso(16, r["liso"] <= TETO_REGUA,
         "o carimbo dominante ficou em %.1f%% (metatile %d), teto %.1f%%"
         % (r["liso"], r["chao"], TETO_REGUA))

    print("DEMO VERDE" if not falhas else "DEMO VERMELHA nos casos %s" % falhas)
    return 1 if falhas else 0


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--desfazer" in sys.argv:
        return desfaz()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
