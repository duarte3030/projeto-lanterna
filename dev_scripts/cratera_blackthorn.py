#!/usr/bin/env python3
"""Refino de `BlackthornCity` (tema CRATERA), no `gTileset_Blackthorn`, com arte
importada do `Pokemon Scorched Silver`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py` em
09/09/2026: 47,6% do chao andavel a pe (385 celulas de 809) e UM metatile, o
217, a areia lisa do PRIMARIO `gTileset_JohtoNorthEast`. Blackthorn e a cidade
da cratera de vulcao do HGSS, com a Dragon's Den ao norte, e o que ela mostra e
um tapete de areia de meio mapa sem uma pedra dentro. A segunda pior de Johto.

E TEM UM SEGUNDO TAPETE, que a regua so mostra depois que o primeiro cai: o
metatile 113, a rocha da montanha, aparece 150 vezes com colisao 0 (todas na
elevacao 4, os PLATOS de topo de barranco). Enquanto o 217 e o dominante, ele
esconde o 113; derrubado o 217, o 113 vira o dominante com 150 de 809, ou seja
18,5%, e o teto da onda e 20%. Ou seja: mexer so na praca chega no maximo a
18,5%, com 1,5 ponto de folga, e QUALQUER celula solidificada come essa folga
(cada uma tira uma do denominador). Por isso esta passada refina os DOIS chaos.

O ORCAMENTO, medido nesta arvore e nao herdado de brief:

  split      todo layout de Johto e `layout_version: "johto"`, que e
             `bigPrimary`: primario de 640 tiles, 640 metatiles e 7 paletas;
             secundario de 384 tiles, 384 metatiles e 6 paletas (vagas 7 a 12).
             O id global do metatile secundario e 640 + local, NAO 512 + local.
  tiles      o `tiles.png` do `gTileset_Blackthorn` tem 80 tiles de 384, e os
             metatiles usados pelos QUATRO layouts do tileset referenciam 75
             deles. Sobram 304 vagas SEM compactar nada, e este kit gasta menos
             que isso: o `compacta_tileset.py` NAO foi rodado, para nao mexer no
             indice de tile de nenhum metatile vivo.
  metatiles  o `metatiles.bin` tem 151 metatiles (2.416 B) e o
             `metatile_attributes.bin` tem 302 B, ou seja 2 bytes por metatile.
             Os quatro layouts usam 110 locais e o maior deles e o 146. Este kit
             cresce os dois arquivos e ocupa locais a partir do 151, que nao
             existiam: nenhuma vaga viva e tocada.
  animacao   `.callback = NULL` no `gTileset_Blackthorn` (conferido em
             `src/data/tilesets/headers.h` por este script, no caso 1 do
             auto-teste). Nenhuma vaga de tile esta pinada por
             `src/tileset_anims.c`.

A VAGA DE PALETA, e ela e a conta que decide a rodada. `NUM_PALS_TOTAL` e 13
(`include/fieldmap.h`): sete vagas sao do primario (0 a 6) e SEIS do secundario
(7 a 12). As seis aparecem em metatile vivo, entao nao ha vaga livre de graca.
Medido nesta arvore, contando so os metatiles que os quatro layouts usam:

    vaga  7   7 cores, 4 tiles, e UM metatile inteiro no repo (o 657)
    vaga  8  12 cores, 17 tiles
    vaga  9  12 cores, 6 tiles
    vaga 10   9 cores, 10 tiles
    vaga 11   9 cores, 11 tiles
    vaga 12  12 cores, 20 tiles

  NENHUM tile e usado por duas vagas (zero, medido), e nenhuma das seis pinta
  tile do PRIMARIO alem da vaga 8. Ou seja, o defeito conhecido do
  `compacta_paletas.py` (tile compartilhado por duas paletas, que exige copia)
  nao se aplica aqui, e a fusao sai limpa.

  Uma paleta de BG do GBA tem 15 cores desenhaveis. Das quinze unioes de par,
  TRES cabem: 7+10 = 14, 7+11 = 14 e 10+11 = 15. Nenhum TRIO cabe (7+10+11 = 20),
  entao a rodada tem UMA vaga de paleta e nao duas.

  A FUSAO ESCOLHIDA E 7 -> 10, e ela e quase de graca: das SETE cores da vaga 7,
  DUAS ja estao em uso na vaga 10 com o RGB exato ((88,88,112) no indice 5 e
  (120,120,128) no indice 1) e QUATRO ja estao escritas em indices MORTOS da
  vaga 10, tambem com o RGB exato ((184,120,112) no 10, (216,144,128) no 11,
  (208,208,208) no 13 e (160,160,168) no 14) - indice morto e indice que
  NENHUM pixel nosso usa, e por isso escrever nele nao muda o desenho de nada.
  Sobra UMA cor para escrever de verdade, (65,74,106), que vai para o indice 9,
  tambem morto. O `.pal` da vaga 10 muda UMA linha. A vaga 7 fica livre com as
  15 cores.

A ARTE, e de onde vem. `Pokemon Scorched Silver` v1.3 Complete (base Emerald
BPEE, md5 f7af51cecd3e170cc373fba01753053c), primario `0x492964` e secundario
`0x492784`, o par da caverna de rocha avermelhada do grupo 25 (o mapa de amostra
e o g25m18, 9x15). E a fonte que o Gui chamou de "a mais moderna". O chao de
la e rocha vermelho-tijolo com pedregulho cinza e cristal, e a familia de cor
casa com o barro das paredes da cratera de Blackthorn.

A REGRA DE MONTAGEM, e a armadilha que ela resolve. A primeira versao desta
rodada importava as pecas de chao da fonte INTEIRAS, como fizeram o
`mina_oreburgh.py` e o `campo_celestic.py`. O render de teste reprovou de olho, e
o motivo esta medido: o chao da caverna do Scorched Silver e vermelho
((128,80,64), (152,104,88), (176,136,112)) e a nossa areia e palida
((213,197,131), (230,222,164), (197,172,106), (172,148,74)). Sem tile de
transicao, cada peca vira um QUADRADO de 16x16 de outra cor no meio da areia, e
isso le como tile faltando, nao como terreno.

  Entao a peca de chao desta passada e um COMPOSTO, e o fundo dela e a NOSSA
  AREIA PIXEL A PIXEL. Para cada metatile da fonte escolhe-se um metatile de
  CHAO LISO da propria fonte como referencia, e o que entra e so a MASCARA: os
  pixels em que os dois diferem. A mascara e pintada POR CIMA dos 256 pixels do
  nosso metatile 217, na CAMADA DE BAIXO, e o resultado vira tile novo. O que
  sai disso e uma pedra, uma racha ou um punhado de cascalho sobre a nossa
  areia, com a emenda invisivel por construcao: fora da mascara o pixel e
  literalmente o nosso.

  Consequencias medidas, e sao tres:
   - o quadrante SEM nenhum pixel de mascara nao vira tile novo: ele fica com a
     entrada ORIGINAL do 217 (tile 317 ou 333 do primario, paleta 5). Isso
     economiza tile e torna o fundo identico por construcao, nao por conferencia.
   - a uniao das cores de TODAS as mascaras e de OITO cores. Com as QUATRO da
     nossa areia da doze, para as quinze da vaga 7.
   - a camada de CIMA da peca de chao fica VAZIA. Camada de cima em celula
     andavel com layerType NORMAL vai para o BG1, que desenha ACIMA do sprite:
     cascalho por cima do jogador e defeito, nao enfeite.

  O PEDREGULHO e o caminho contrario e nao podia ser o mesmo: ele e MOVEL, a
  celula vira SOLIDA, e ai a arte vai na camada de CIMA (com a mascara como
  transparencia), a de baixo recebe o NOSSO 217 entrada por entrada, e o atributo
  e comportamento ZERADO com layerType COVERED (0x1000), que poe as duas camadas
  ABAIXO do sprite e faz o jogador parado ao sul aparecer NA FRENTE da pedra.

O QUE NAO CUSTOU NADA. Antes de gastar vaga, este script varre o que o repo JA
tem desenhado e nao usa:

  - CHAO DA PRACA: os metatiles 178 e 179 do primario, barro escuro, atributo
    0x0000 IGUAL ao do 217 e camada de cima VAZIA. Custam zero.
  - CHAO DO PLATO: os metatiles 107, 108, 109 e 533 do primario, a mesma rocha
    do 113 com outra mancha, atributo 0x1000 IGUAL ao do 113.
  - MOVEL: os metatiles 688, 689, 696 e 697 do SECUNDARIO, ja desenhados SOBRE a
    areia do 217, ja em COVERED e ja com comportamento zerado; e os 680 e 681,
    que sao a mesma coisa com atributo 0x0000 e por isso entram como COPIA em
    vaga nova, com o atributo trocado por 0x1000. Nenhum dos seis aparece em
    `BlackthornCity` hoje.

O QUE FICOU DE FORA, com o motivo:
  - o CHAO DE ROCHA INTEIRO da fonte (os metatiles 4, 10, 16 e 19 dela, que sao
    piso de caverna de verdade): ver a regra de montagem acima. Ele foi
    renderizado em mancha antes de ser cortado.
  - os metatiles 4 e 10 da fonte desenham os MESMOS 256 pixels, e o 6 e o 18
    tambem: cada par entrou uma vez so. O caso 6 do auto-teste reprova variante
    que e copia de outra, porque duplicar arte para engordar a conta de
    variantes e enganar a regua (regra 8 da onda).
  - os metatiles 105, 153, 186, 187, 593 e 613 do primario, que tambem sao rocha
    de montanha: a distancia RGB media deles para as quatro escolhidas fica
    entre 1,8 e 7,8, abaixo do piso de 8,0 do `varia_carimbo.py`. Sao a mesma
    pedra com outro pedregulho embaixo, e a camada de cima 242/256 opaca deles
    tapa a diferenca.
  - os metatiles 128, 129, 130 e 271 do primario, que sao areia com barro e
    teriam sido a mancha mais barata da rodada: os quatro tem atributo 0x0000
    (andavel, layerType NORMAL) com a camada de CIMA entre 130 e 242 pixels
    opacos de 256. Espalhar isso e espalhar arte que desenha ACIMA do jogador.
    Eles ja aparecem 34 vezes em `BlackthornCity` e esta passada nao mexe neles,
    mas tambem nao pinta nenhum novo.

Uso:
    python3 dev_scripts/cratera_blackthorn.py              # mede e mostra o plano
    python3 dev_scripts/cratera_blackthorn.py --aplicar
    python3 dev_scripts/cratera_blackthorn.py --desfazer
    python3 dev_scripts/cratera_blackthorn.py --demo       # auto-teste
    python3 dev_scripts/cratera_blackthorn.py --extrai     # regera o kit da ROM
    python3 dev_scripts/cratera_blackthorn.py --so-tileset # so o tileset
"""
import collections
import heapq
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

# O bloco de teste desta rodada nasce DEPOIS do desenho e a partir dele, entao
# ele nao entra na varredura de corredor: pular o proprio bloco e o que o
# `enfeita_cidades.py` ja faz com o dele. Todos os OUTROS blocos entram.
E.BLOCO_PROPRIO = "201_cratera_blackthorn.json"

DESTINO = f"{RAIZ}/data/tilesets/secondary/blackthorn"
KIT_JSON = f"{RAIZ}/dev_scripts/cratera_blackthorn_kit.json"
PLANO = f"{RAIZ}/dev_scripts/cratera_blackthorn.json"

PRIMARIO = "gTileset_JohtoNorthEast"
SECUNDARIO = "gTileset_Blackthorn"
ALVO = "BlackthornCity"
# os QUATRO layouts que dividem o gTileset_Blackthorn. Os tres irmaos sao a
# prova de nao regressao: eles tem que renderizar com ZERO pixel diferente.
IRMAOS = ["BlackthornCity", "Route26", "Route45", "MtSilver_MountainSide"]

# split de Johto (bigPrimary), ver tools/mapjson/mapjson.cpp e include/fieldmap.h
N_META_PRI = 640
N_TILES_PRI = 640
N_PAL_PRI = 7
TETO_TILES = 384          # tiles do SECUNDARIO
TETO_META = 384           # metatiles do SECUNDARIO
TILE_LOCAL_0 = 80         # primeira vaga livre do tiles.png (80 tiles hoje)
META_LOCAL_0 = 151        # primeiro local livre do metatiles.bin (151 hoje)
MARGEM = 2
TETO_REGUA = 20.0         # o alvo desta onda: carimbo dominante <= 20%
PISO_VARIANTE = 8.0       # distancia RGB media minima entre duas variantes

CARIMBO = 217             # a areia lisa da praca (primario)
CARIMBO_PLATO = 113       # a rocha da montanha (primario), andavel na elevacao 4

# ------------------------------------------------------------------ a FUSAO
FUSAO = dict(de=7, para=10)   # a vaga 7 e esvaziada dentro da 10; ver o cabecalho

# ------------------------------------------------------------------- a FONTE
SS = dict(slug="scorched-silver", hack="Pokemon Scorched Silver", versao="v1.3 Complete",
          autor="Sloo", creditado="RHH (pokeemerald-expansion)",
          md5="f7af51cecd3e170cc373fba01753053c", base="Emerald (BPEE)",
          pri=0x492964, sec=0x492784, split=(512, 512, 6))

# CHAO IMPORTADO: as pecas de PISO da fonte, com a tinta de chao trocada pela
# NOSSA (ver REMAP_CHAO abaixo). Elas entram INTEIRAS, na camada de baixo, e a
# de cima fica vazia.
CHAO_SS = [
    dict(nome="cascalho claro",  ss=4),
    dict(nome="cascalho escuro", ss=16),
    dict(nome="terra batida",    ss=6),
    dict(nome="terra riscada",   ss=17),
    dict(nome="terra ondulada",  ss=19),
    dict(nome="seixo redondo",   ss=1),
    dict(nome="seixo grande",    ss=3),
    dict(nome="laje solta",      ss=13),
    dict(nome="laje partida",    ss=15),
]
# MOVEL IMPORTADO: a celula vira SOLIDA e a arte vai na camada de CIMA, tirada
# por MASCARA (a diferenca entre o metatile do pedregulho e o do chao liso da
# fonte). O fundo e o NOSSO 217.
MOVEL_SS = [
    dict(nome="pedregulho",       ss=14, ref=4, quantos=10, espaco=7),
    dict(nome="monte de minerio", ss=40, ref=4, quantos=8,  espaco=8),
    dict(nome="minerio miudo",    ss=42, ref=4, quantos=8,  espaco=8),
    dict(nome="pilar de rocha",   ss=51, ref=4, quantos=4,  espaco=10),
]
# OS DOIS METATILES DE CHAO LISO DA FONTE, e eles nao sao escolha de gosto: o 10
# aparece 192 vezes nos mapas do hack que usam este tileset, e o 16 e o par
# escuro dele. Deles saem, por MEDIDA, as quatro cores de tinta de chao da fonte
# (as nao-cinza, ou seja aquelas em que R, G e B nao sao iguais).
PISO_DA_FONTE = [10, 16]
# ---------------------------------------------------- o que ja e NOSSO
# CHAO DA PRACA, do PRIMARIO, com atributo IGUAL ao do 217 e camada de cima VAZIA.
CHAO_NOSSO = [
    dict(nome="barro batido", mt=178),
    dict(nome="barro fundo",  mt=179),
]
# CHAO DO PLATO, do PRIMARIO, com atributo IGUAL ao do 113 (0x1000, COVERED).
CHAO_PLATO = [
    dict(nome="rocha riscada",  mt=107),
    dict(nome="rocha manchada", mt=109),
    dict(nome="rocha lascada",  mt=187),
]
# MOVEL NOSSO, do SECUNDARIO, ja desenhado SOBRE a areia do 217. Os que ja estao
# em COVERED com comportamento zerado entram como estao; os outros entram como
# COPIA em vaga livre, com o atributo trocado.
MOVEL_NOSSO = [
    dict(nome="rocha esquerda", mt=696, quantos=6, espaco=7),
    dict(nome="rocha direita",  mt=697, quantos=6, espaco=7),
    dict(nome="galho seco",     mt=688, quantos=5, espaco=8),
    dict(nome="tronco seco",    mt=689, quantos=5, espaco=8),
    dict(nome="pedra pontuda",  mt=680, quantos=6, espaco=7),
    dict(nome="pedra torta",    mt=681, quantos=6, espaco=7),
]

N4 = E.N4


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem
    que sair identico em qualquer maquina e em qualquer versao de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


# ------------------------------------------------------------ leitura do nosso
def _ler(nome):
    return open(f"{DESTINO}/{nome}", "rb").read()


def _entradas(bin_meta, local):
    return list(struct.unpack_from("<8H", bin_meta, local * 16))


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def attr_de(mt, attrs_novos=None):
    """Atributo de um metatile GLOBAL, no split de Johto (640), com o kit valendo.

    O `arte_ginasios_sinnoh.comportamento` parte o indice em 512, que e o split
    do Emerald, e por isso NAO serve para Johto: ele leria o metatile 616 do
    PRIMARIO como se fosse o local 104 do secundario. Medido nesta arvore: com o
    split errado a `regua_cidades.py` conta 809 celulas andaveis em
    `BlackthornCity` e com o certo conta 805, porque os metatiles 616 e 617 sao
    agua do primario e escapam do filtro. A diferenca e de quatro celulas e nao
    muda o veredito, mas quem decide onde a tinta cai aqui e esta funcao.
    """
    ap, asec = G._attrs(PRIMARIO), G._attrs(SECUNDARIO)
    if mt < N_META_PRI:
        return ap[mt] if mt < len(ap) else 0
    local = mt - N_META_PRI
    if attrs_novos and local in attrs_novos:
        return attrs_novos[local]
    return asec[local] if local < len(asec) else 0


def entradas_de(mt, metas_novos=None):
    """As 8 entradas de um metatile GLOBAL, com o kit desta rodada valendo."""
    if mt >= N_META_PRI:
        local = mt - N_META_PRI
        if metas_novos and local in metas_novos:
            return list(metas_novos[local])
        ts = _tileset(SECUNDARIO)
        if local * 16 + 16 > len(ts["metatiles"]):
            return [0] * 8
        return list(struct.unpack_from("<8H", ts["metatiles"], local * 16))
    tp = _tileset(PRIMARIO)
    return list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))


def pixels_de(mt, tiles_novos=None, metas_novos=None, paletas_novas=None):
    """Os 256 pixels RGB de um metatile GLOBAL, com o kit desta rodada valendo."""
    import render_maps as RM
    from PIL import Image
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    im = Image.new("RGB", (16, 16), tp["paletas"][0][0])
    p = im.load()
    ent = entradas_de(mt, metas_novos)
    for cam in (0, 1):
        for q in range(4):
            v = ent[cam * 4 + q]
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            if not idx:
                continue
            local = idx - N_TILES_PRI
            if tiles_novos and local in tiles_novos:
                tile = tiles_novos[local]
            else:
                tile = RM.resolver_tile(tp, ts, idx)
            if tile is None:
                continue
            cores = None
            if paletas_novas and str(ip) in paletas_novas:
                cores = [tuple(c) for c in paletas_novas[str(ip)]]
            if cores is None:
                cores = (tp if ip < N_PAL_PRI else ts)["paletas"].get(ip)
            if cores is None:
                continue
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                             [tuple(c) for c in cores],
                             bool(v & 0x400), bool(v & 0x800))
    return list(im.get_flattened_data())


def distancia(a, b):
    return sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
               for p, q in zip(a, b)) / 256.0


# ------------------------------------------------------------------ a FUSAO
def indices_usados():
    """{vaga: set de indices de cor que ALGUM pixel NOSSO usa}.

    So conta os metatiles que existiam ANTES desta passada (local < META_LOCAL_0)
    e os tiles que existiam antes (local < TILE_LOCAL_0), para que rodar
    `--aplicar` duas vezes de a mesma conta.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    fora = collections.defaultdict(set)
    n = min(len(ts["metatiles"]) // 16, META_LOCAL_0)
    for loc in range(n):
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], loc):
            if it == 0 or ip < N_PAL_PRI:
                continue
            if it >= N_TILES_PRI + TILE_LOCAL_0:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        fora[ip].add(c)
    return fora


def vivos_do_primario(_c={}):
    """Metatiles que ALGUM layout do `gTileset_JohtoNorthEast` usa de verdade."""
    if _c:
        return _c["set"]
    lay = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]
    fora = set()
    for l in lay:
        if l.get("primary_tileset") != PRIMARIO:
            continue
        b = open(f"{RAIZ}/{l['blockdata_filepath']}", "rb").read()
        n = l["width"] * l["height"]
        fora |= {c & 0x3FF for c in struct.unpack_from("<%dH" % n, b, 0)}
    _c["set"] = {m for m in fora if m < N_META_PRI}
    return _c["set"]


def plano_fusao():
    """O plano da fusao 7 -> 10, medido no tileset que esta no disco.

    Devolve None quando a fusao JA foi aplicada (nenhum metatile antigo aponta
    para a vaga de origem), que e o que torna `--aplicar` idempotente.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    de, para = FUSAO["de"], FUSAO["para"]
    usa = collections.defaultdict(set)
    n = min(len(ts["metatiles"]) // 16, META_LOCAL_0)
    for loc in range(n):
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], loc):
            if it:
                usa[ip].add(it)
    if not usa[de]:
        return None
    if usa[de] & usa[para]:
        raise SystemExit("a fusao %d -> %d exige que nenhum tile seja usado nas "
                         "duas vagas, e %d sao: %s"
                         % (de, para, len(usa[de] & usa[para]),
                            sorted(usa[de] & usa[para])[:8]))
    for vaga in (de, para):
        do_pri = sorted(t for t in usa[vaga] if t < N_TILES_PRI)
        if do_pri:
            raise SystemExit("a vaga %d pinta %d tiles do PRIMARIO (%s) e por "
                             "isso nao pode ser reindexada"
                             % (vaga, len(do_pri), do_pri[:6]))
    # Nenhum metatile VIVO do primario pode pedir tile do secundario, senao
    # reindexar pixel de tile do secundario mudaria o desenho do primario, que
    # serve 31 layouts. Medido nesta arvore: das 5.120 entradas do
    # `gTileset_JohtoNorthEast` so DUAS pedem tile do secundario (as duas do
    # metatile 588, tiles 812 e 813 com a paleta 10), e o 588 nao aparece em
    # `map.bin` de NENHUM dos 31 layouts que usam este primario. Ele e
    # enchimento do dumper: os tiles 812 e 813 seriam os locais 172 e 173 do
    # secundario, e o `gTileset_Blackthorn` tem 80. Por isso a conferencia olha
    # metatile VIVO, e nao todos.
    for m in vivos_do_primario():
        for (it, fh, fv, ip) in RM.entradas_metatile(tp["metatiles"], m):
            if it >= N_TILES_PRI:
                raise SystemExit("o metatile VIVO %d do primario pede o tile %d "
                                 "do secundario; a fusao mexeria no primario"
                                 % (m, it))
    for vaga in (de, para):
        for outra, tiles in usa.items():
            if outra in (de, para) or not tiles:
                continue
            if tiles & usa[vaga]:
                raise SystemExit("tile usado na vaga %d e tambem na %d"
                                 % (vaga, outra))

    def cores(vaga):
        fora = {}
        for it in sorted(usa[vaga]):
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        fora[c] = tuple(ts["paletas"][vaga][c])
        return fora

    c_de, c_para = cores(de), cores(para)
    nova = dict(c_para)                     # a vaga de destino nao se mexe
    remap, escritas = {}, []
    livres = [i for i in range(1, 16) if i not in nova]
    for idx in sorted(c_de):
        cor = c_de[idx]
        igual = [i for i, v in nova.items() if v == cor]
        if igual:
            remap[idx] = igual[0]
            continue
        if not livres:
            raise SystemExit("a uniao das vagas %d e %d passa de 15 cores"
                             % (de, para))
        # PREFERE o indice morto que JA guarda esta cor exata: e o que faz o
        # `.pal` da vaga 10 mudar uma linha so em vez de cinco.
        ja = [i for i in livres if tuple(ts["paletas"][para][i]) == cor]
        alvo = ja[0] if ja else (idx if idx in livres else livres[0])
        livres.remove(alvo)
        nova[alvo] = cor
        remap[idx] = alvo
        if not ja:
            escritas.append([alvo, list(cor)])
    paleta = [list(ts["paletas"][para][0])]
    for i in range(1, 16):
        paleta.append(list(nova[i]) if i in nova else [0, 0, 0])
    return dict(de=de, para=para, remap={str(k): v for k, v in remap.items()},
                tiles=sorted(usa[de]), paleta=paleta, escritas=escritas,
                cores_de=len(c_de), cores_para=len(c_para), cores=len(nova))


# ---------------------------------------------------------------- a EXTRACAO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb(pal_bytes, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits deslocados TRES
    casas, nao esticados para 0..255.

    A conta importa: as duas contas dao o MESMO cinco-bits depois que o `gbagfx`
    reconverte o `.pal` para `.gbapal`, entao a cor dentro da ROM e a mesma nas
    duas; o que muda e o numero que fica escrito no `.pal` e, com ele, o pixel de
    todo render de conferencia. Todo `.pal` do `gTileset_Blackthorn` esta na
    conta de deslocar (por exemplo 208 = 26 << 3, 112 = 14 << 3), e o
    `ferramentas/prova_extracao.py`, que e o portao da extracao, tambem.
    """
    c = struct.unpack_from("<16H", pal_bytes, i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def areia_nossa():
    """(entradas da camada de baixo do 217, atributo do 217, 256 pixels RGB)."""
    import render_maps as RM
    from PIL import Image
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    ent = list(struct.unpack_from("<8H", tp["metatiles"], CARIMBO * 16))
    if any(v & 0x3FF for v in ent[4:]):
        raise SystemExit("o carimbo %d ja usa a camada de cima" % CARIMBO)
    im = Image.new("RGB", (16, 16), tp["paletas"][0][0])
    p = im.load()
    for q in range(4):
        v = ent[q]
        RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8,
                         RM.resolver_tile(tp, ts, v & 0x3FF),
                         tp["paletas"][(v >> 12) & 0xF],
                         bool(v & 0x400), bool(v & 0x800))
    px = [[im.getpixel((x, y)) for x in range(16)] for y in range(16)]
    return ent[:4], G._attrs(PRIMARIO)[CARIMBO], px


def extrai():
    """Regera `cratera_blackthorn_kit.json` a partir da ROM privada.

    So roda na maquina que tem `fontes-mapas/romhacks/`. O que sai daqui e o
    asset CONVERTIDO (tiles em nibbles, ja compostos sobre a nossa areia e ja
    reindexados para a vaga 7), nunca a ROM.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("nao achei fontes-mapas/romhacks: --extrai so roda na "
                         "maquina que tem as ROMs. O kit ja extraido esta em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402

    pasta = os.path.join(ferr, SS["slug"])
    gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
    caminho = os.path.join(pasta, gba)
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    if md5 != SS["md5"]:
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s"
                         % (gba, md5, SS["md5"]))
    r = Rom(caminho)
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = SS["split"]
    t1, t2 = r.parse_tileset(SS["pri"]), r.parse_tileset(SS["sec"])
    if t1 is None or t2 is None:
        raise SystemExit("o par 0x%X / 0x%X nao abriu" % (SS["pri"], SS["sec"]))
    pal = {i: _rgb(t1["pal"] if i < r.n_pal_pri else t2["pal"], i)
           for i in range(16)}

    def celula(loc):
        """Os 16x16 pixels RGB de um metatile da fonte, com flip aplicado."""
        fora = [[None] * 16 for _ in range(16)]
        ents = struct.unpack_from("<8H", t2["meta"], loc * 16)
        for cam in range(2):
            for q in range(4):
                v = ents[cam * 4 + q]
                tid = v & 0x3FF
                if not tid and cam:
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
                            fora[(q // 2) * 8 + y][(q % 2) * 8 + x] = tuple(cores[c])
        return fora

    _ents, _attr, areia = areia_nossa()
    cores_areia = []
    for y in range(16):
        for x in range(16):
            if areia[y][x] not in cores_areia:
                cores_areia.append(areia[y][x])

    # ------------------------------------------------ a TINTA DE CHAO DA FONTE
    # Ela sai por MEDIDA e nao por constante decorada: sao as cores NAO-CINZA
    # (aquelas em que R, G e B nao sao os tres iguais) dos DOIS metatiles de chao
    # liso da fonte. O 10 e o piso que os mapas do hack usam 192 vezes, o 16 e o
    # par escuro dele; juntos eles dao a rampa inteira do chao daquela caverna.
    # Cinza nao entra porque cinza ali e pedregulho, e pedregulho e detalhe, nao
    # e tinta de chao.
    rampa = []
    for loc in PISO_DA_FONTE:
        A = celula(loc)
        for y in range(16):
            for x in range(16):
                c = A[y][x]
                if c is None or (c[0] == c[1] == c[2]):
                    continue
                if c not in rampa:
                    rampa.append(c)

    def luz(c):
        return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

    rampa.sort(key=luz, reverse=True)
    nossa = sorted(cores_areia, key=luz, reverse=True)
    if len(rampa) != len(nossa):
        raise SystemExit("a rampa de chao da fonte tem %d tons (%s) e a nossa "
                         "areia tem %d (%s); a troca so vale posto a posto"
                         % (len(rampa), rampa, len(nossa), nossa))
    REMAP = dict(zip(rampa, nossa))
    if len(set(REMAP.values())) != len(REMAP):
        raise SystemExit("duas cores de chao da fonte cairiam na MESMA cor nossa")

    # ------------------------------------------------------------- as PECAS
    pecas, desenhos = [], {}
    for p in CHAO_SS:
        A = celula(p["ss"])
        img = [[REMAP.get(A[y][x], A[y][x]) for x in range(16)] for y in range(16)]
        sobrou = sorted({A[y][x] for y in range(16) for x in range(16)
                         if A[y][x] in REMAP and img[y][x] not in nossa})
        if sobrou:
            raise SystemExit("%s: sobrou tinta de chao da fonte" % p["nome"])
        desenhos[p["nome"]] = img
        pecas.append(dict(papel="chao", nome=p["nome"], ss=p["ss"], ref=None,
                          pixels=256,
                          trocados=sum(1 for y in range(16) for x in range(16)
                                       if A[y][x] in REMAP)))
    for p in MOVEL_SS:
        A, B = celula(p["ss"]), celula(p["ref"])
        m = {(x, y): A[y][x] for y in range(16) for x in range(16)
             if A[y][x] != B[y][x]}
        if not m:
            raise SystemExit("%s: a mascara do metatile %d contra o %d e VAZIA"
                             % (p["nome"], p["ss"], p["ref"]))
        if len(m) > 150:
            raise SystemExit("%s: a mascara do metatile %d contra o %d tem %d "
                             "pixels de 256; acima de 150 nao e peca sobre a "
                             "areia, e outro chao"
                             % (p["nome"], p["ss"], p["ref"], len(m)))
        # a mascara do movel nao pode trazer tinta de chao da fonte junto: o
        # fundo dele e a NOSSA areia e uma borda vermelha do hack apareceria.
        img = [[m.get((x, y)) for x in range(16)] for y in range(16)]
        desenhos[p["nome"]] = img
        pecas.append(dict(papel="movel", nome=p["nome"], ss=p["ss"],
                          ref=p["ref"], pixels=len(m), trocados=0))

    # ------------------------------------------------- a PALETA da vaga 7
    # As cores da NOSSA areia primeiro, porque elas sao a tinta de chao de toda
    # peca; depois as da fonte que sobraram, em ordem.
    resto = sorted({c for img in desenhos.values() for l in img for c in l
                    if c is not None and c not in cores_areia})
    tabela = list(cores_areia) + resto
    if len(tabela) > 15:
        raise SystemExit("a vaga %d cabe 15 cores e o kit pede %d: %s"
                         % (FUSAO["de"], len(tabela), tabela))
    indice = {c: i + 1 for i, c in enumerate(tabela)}
    paleta7 = [[0, 0, 0]] + [list(c) for c in tabela] + \
              [[0, 0, 0]] * (15 - len(tabela))

    # -------------------------------------------------------- os TILES
    tiles = {}
    for p in pecas:
        img = desenhos[p["nome"]]
        qs = []
        for q in range(4):
            ox, oy = (q % 2) * 8, (q // 2) * 8
            if p["papel"] == "movel" and not any(
                    img[oy + y][ox + x] is not None
                    for y in range(8) for x in range(8)):
                qs.append(None)
                continue
            chave = "%s:%d:%d" % (p["papel"], p["ss"], q)
            tiles[chave] = [[0 if img[oy + y][ox + x] is None
                             else indice[img[oy + y][ox + x]]
                             for x in range(8)] for y in range(8)]
            qs.append(chave)
        p["quads"] = qs

    dados = dict(
        fonte=dict(hack=SS["hack"], versao=SS["versao"], autor=SS["autor"],
                   creditado=SS["creditado"], base=SS["base"], arquivo=gba,
                   md5=md5, pri="0x%X" % SS["pri"], sec="0x%X" % SS["sec"],
                   split=list(SS["split"]), piso=PISO_DA_FONTE),
        vaga=FUSAO["de"], paleta=paleta7,
        cores_areia=[list(c) for c in cores_areia],
        rampa_da_fonte=[list(c) for c in rampa],
        remap={"%d,%d,%d" % k: list(v) for k, v in REMAP.items()},
        cores_da_fonte=[list(c) for c in resto],
        tiles=tiles, pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d pecas, %d cores na vaga %d"
          % (os.path.relpath(KIT_JSON, RAIZ), len(tiles), len(pecas),
             len(tabela), FUSAO["de"]))
    print("  a nossa areia (%d tons): %s" % (len(cores_areia), nossa))
    print("  a rampa de chao da fonte (%d tons): %s" % (len(rampa), rampa))
    print("  troca posto a posto: " + ", ".join("%s -> %s" % (a, b)
                                                for a, b in REMAP.items()))
    print("  cores da fonte que ficam (%d): %s" % (len(resto), resto))
    for p in pecas:
        print("    %-6s %-16s ss=%3d  %3d px de arte, %d tinta de chao trocada"
              % (p["papel"], p["nome"], p["ss"], p["pixels"], p["trocados"]))
    return 0


# --------------------------------------------------------------- o KIT em disco
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def desenha_kit():
    """(fusao, tiles_novos, metas, attrs, carimbos), sem escrever em disco."""
    dados = kit()
    ap = G._attrs(PRIMARIO)
    asec = G._attrs(SECUNDARIO)
    meta_bt = _ler("metatiles.bin")
    base, attr_areia, _px = areia_nossa()
    attr_plato = ap[CARIMBO_PLATO]

    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]
    metas, attrs = {}, {}
    proximo_meta = [META_LOCAL_0]
    carimbos = dict(chao=[], plato=[], moveis=[])

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            mapa_tile[chave] = proximo[0]
            tiles_novos[proximo[0]] = dados["tiles"][chave]
            proximo[0] += 1
        return mapa_tile[chave]

    def poe(ents, attr):
        local = proximo_meta[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return N_META_PRI + local

    por_nome = {p["nome"]: p for p in dados["pecas"]}

    # ------------------------------------------------------ 1. CHAO importado
    for c in CHAO_SS:
        p = por_nome[c["nome"]]
        baixo = []
        for q in range(4):
            ch = p["quads"][q]
            if ch is None:
                baixo.append(base[q])          # a entrada ORIGINAL do 217
            else:
                baixo.append((N_TILES_PRI + vaga(ch)) | (dados["vaga"] << 12))
        gid = poe(baixo + [0, 0, 0, 0], attr_areia)
        carimbos["chao"].append(dict(nome=c["nome"], mt=gid, importado=True,
                                     pixels=p["pixels"]))
    # ------------------------------------------------------ 2. CHAO nosso
    for c in CHAO_NOSSO:
        if ap[c["mt"]] != attr_areia:
            raise SystemExit("o metatile %d tem atributo 0x%04X e o carimbo tem "
                             "0x%04X" % (c["mt"], ap[c["mt"]], attr_areia))
        carimbos["chao"].append(dict(nome=c["nome"], mt=c["mt"], importado=False))
    # ------------------------------------------------------ 3. CHAO do plato
    for c in CHAO_PLATO:
        if ap[c["mt"]] != attr_plato:
            raise SystemExit("o metatile %d tem atributo 0x%04X e o carimbo do "
                             "plato tem 0x%04X" % (c["mt"], ap[c["mt"]], attr_plato))
        carimbos["plato"].append(dict(nome=c["nome"], mt=c["mt"]))
    # ------------------------------------------------------ 4. MOVEL importado
    for m in MOVEL_SS:
        p = por_nome[m["nome"]]
        cima = []
        for q in range(4):
            ch = p["quads"][q]
            cima.append(0 if ch is None
                        else (N_TILES_PRI + vaga(ch)) | (dados["vaga"] << 12))
        if not any(cima):
            raise SystemExit("%s: peca sem arte" % m["nome"])
        # comportamento ZERADO (regra 7 da onda: nenhum id semantico e importado)
        # e layerType COVERED, que poe as duas camadas ABAIXO do sprite.
        gid = poe(list(base) + cima, 0x1000)
        carimbos["moveis"].append(dict(nome=m["nome"], mt=gid, importado=True,
                                       quantos=m["quantos"], espaco=m["espaco"]))
    # ------------------------------------------------------ 5. MOVEL nosso
    for m in MOVEL_NOSSO:
        local = m["mt"] - N_META_PRI
        if local < 0 or local >= len(asec):
            raise SystemExit("o movel %d nao e do secundario" % m["mt"])
        ents = _entradas(meta_bt, local)
        if ents[:4] != base:
            raise SystemExit("o metatile %d nao esta desenhado sobre a areia do "
                             "carimbo" % m["mt"])
        if asec[local] == 0x1000:
            mt = m["mt"]                        # ja e COVERED e comportamento 0
            copia = None
        else:
            mt = poe(ents, 0x1000)              # COPIA com o atributo trocado
            copia = m["mt"]
        carimbos["moveis"].append(dict(nome=m["nome"], mt=mt, importado=False,
                                       copia_de=copia, quantos=m["quantos"],
                                       espaco=m["espaco"]))

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))
    if proximo_meta[0] > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles (%d)"
                         % (TETO_META, proximo_meta[0]))

    # As vagas de metatile so servem se NENHUM dos quatro layouts usar o id, e se
    # a vaga estiver alem do fim do arquivo ou com exatamente o que este kit grava.
    usados = set()
    for nome in IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    n_disco = len(meta_bt) // 16
    for local, ents in metas.items():
        gid = N_META_PRI + local
        if local >= n_disco:
            continue                      # a vaga nem existia no arquivo
        antigo = _entradas(meta_bt, local)
        if antigo == ents:
            continue                      # ja e o que este kit grava (idempotencia)
        if gid in usados:
            raise SystemExit("algum dos quatro layouts ja usa o metatile %d e a "
                             "vaga nao tem o desenho deste kit" % gid)
        if not (len(set(antigo)) == 1 and antigo[0] <= 2):
            raise SystemExit("a vaga de metatile %d ja esta ocupada" % gid)
    return plano_fusao(), tiles_novos, metas, attrs, carimbos


def _grava_pal(vaga, cores):
    with open(f"{DESTINO}/palettes/%02d.pal" % vaga, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))


def grava_tileset(fusao, tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    Idempotente: a fusao so e aplicada quando `plano_fusao()` ainda a encontra
    por fazer, e as vagas de tile, de paleta e de metatile sao FIXAS.
    """
    from PIL import Image
    dados = kit()
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    alvo = max(TILE_LOCAL_0 + len(tiles_novos), (antigo.size[1] // 8) * cols)
    linhas = (alvo + cols - 1) // cols
    novo = Image.new("P", (antigo.size[0], linhas * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    # O tiles.png do master carrega um bloco tRNS de 16 bytes 0xFF (opaco em
    # todos os indices). Ele nao muda um pixel e 170 dos 219 tilesets do repo
    # nem o tem, mas reescrever o arquivo SEM ele e ruido no diff: o Pillow so
    # regrava o bloco quando a chave `transparency` vai no save.
    trns = antigo.info.get("transparency")
    px = novo.load()

    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    # ------------------------------------------------------------- a FUSAO
    if fusao:
        remap = {int(k): v for k, v in fusao["remap"].items()}
        for t in fusao["tiles"]:
            local = t - N_TILES_PRI
            x0, y0 = (local % cols) * 8, (local // cols) * 8
            for y in range(8):
                for x in range(8):
                    c = px[x0 + x, y0 + y]
                    if c:
                        px[x0 + x, y0 + y] = remap.get(c, c)
        for local in range(len(meta) // 16):
            for i in range(8):
                v = struct.unpack_from("<H", meta, local * 16 + i * 2)[0]
                if (v & 0x3FF) and ((v >> 12) & 0xF) == fusao["de"]:
                    v = (v & 0x0FFF) | (fusao["para"] << 12)
                    struct.pack_into("<H", meta, local * 16 + i * 2, v)
        _grava_pal(fusao["para"], fusao["paleta"])

    for v, tile in tiles_novos.items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    if trns is None:
        novo.save(f"{DESTINO}/tiles.png")
    else:
        novo.save(f"{DESTINO}/tiles.png", transparency=trns)
    _grava_pal(dados["vaga"], dados["paleta"])

    # os dois binarios CRESCEM: os locais a partir do 151 nao existiam
    fim = max(metas) + 1 if metas else 0
    if fim * 16 > len(meta):
        meta += bytes(fim * 16 - len(meta))
    if fim * 2 > len(attr):
        attr += bytes(fim * 2 - len(attr))
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------ o ESPALHAMENTO
# A TRILHA e o esqueleto de custo minimo entre as soleiras das portas, engordado
# e desgastado na borda; as BOLHAS sao manchas organicas crescidas por frente de
# onda. As duas ideias, e o codigo delas, vem do `neve_snowpoint2.py` e do
# `mina_oreburgh.py`, que sao as passadas em que foram medidas e provadas.
ESPALHA = dict(
    trilha=["cascalho claro", "cascalho escuro"],
    borda_trilha=48,
    bolhas=[
        dict(grupo=["barro batido", "barro fundo"],       quantas=3, tam=(6, 12)),
        dict(grupo=["terra ondulada"],                    quantas=3, tam=(5, 11)),
        dict(grupo=["seixo redondo", "seixo grande"],     quantas=3, tam=(5, 11)),
        dict(grupo=["terra batida", "terra riscada"],     quantas=3, tam=(5, 11)),
        dict(grupo=["laje solta", "laje partida"],        quantas=3, tam=(5, 10)),
        dict(grupo=["barro fundo", "barro batido"],       quantas=2, tam=(4, 9)),
        dict(grupo=["terra riscada", "terra ondulada"],   quantas=2, tam=(4, 9)),
        dict(grupo=["cascalho escuro"],                   quantas=2, tam=(4, 8)),
        dict(grupo=["laje partida", "seixo grande"],      quantas=2, tam=(4, 8)),
    ],
)
# O PLATO nao tem porta nem caminho: e topo de barranco. So bolha.
ESPALHA_PLATO = dict(
    bolhas=[
        dict(grupo=["rocha riscada", "rocha lascada"],  quantas=4, tam=(8, 18)),
        dict(grupo=["rocha manchada", "rocha riscada"], quantas=4, tam=(7, 16)),
        dict(grupo=["rocha lascada", "rocha manchada"], quantas=4, tam=(7, 16)),
    ],
)
ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre dois moveis QUAISQUER


def esqueleto(v, W, H, d, elegivel):
    """Caminho de custo minimo ligando as portas do mapa, em ordem de leitura.

    O custo nao e so distancia. Andar colado num solido custa mais, para a
    trilha sair pelo MEIO do corredor e nao raspando o predio; virar custa mais,
    para ela sair reta como caminho batido de verdade; e celula que nao pode
    receber mancha custa muito mais, mas nao e proibida, senao o caminho nao
    atravessa a soleira das portas.
    """
    def andavel(i):
        return not ((v[i] >> 10) & 3)

    def perto_de_solido(x, y):
        return sum(1 for dx, dy in N4
                   if not (0 <= x + dx < W and 0 <= y + dy < H)
                   or ((v[(y + dy) * W + x + dx] >> 10) & 3))

    def custo(x, y):
        c = 1.0 + 2.0 * perto_de_solido(x, y)
        if (x, y) not in elegivel:
            c += 12.0
        return c

    def caminho(ini, fim):
        """Dijkstra com estado (celula, direcao), para poder cobrar a curva."""
        alvo = set(fim)
        dist, pai = {}, {}
        fila = [(0.0, ini[0], ini[1], 0, 0)]
        while fila:
            g, x, y, dx0, dy0 = heapq.heappop(fila)
            if (x, y, dx0, dy0) in dist:
                continue
            dist[(x, y, dx0, dy0)] = g
            if (x, y) in alvo and (dx0, dy0) != (0, 0):
                saida, no = [], (x, y, dx0, dy0)
                while no in pai:
                    saida.append((no[0], no[1]))
                    no = pai[no]
                saida.append((no[0], no[1]))
                return saida
            for dx, dy in N4:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H) or not andavel(ny * W + nx):
                    continue
                ea = (v[y * W + x] >> 12) & 0xF
                eb = (v[ny * W + nx] >> 12) & 0xF
                if ea and eb and ea != eb:
                    continue
                curva = 9.0 if (dx0, dy0) != (0, 0) and (dx, dy) != (dx0, dy0) else 0.0
                no = (nx, ny, dx, dy)
                if no in dist:
                    continue
                pai[no] = (x, y, dx0, dy0)
                heapq.heappush(fila, (g + custo(nx, ny) + curva, nx, ny, dx, dy))
        return []

    portas = []
    for w in (d.get("warp_events") or []):
        x, y = w["x"], w["y"]
        for dx, dy in ((0, 1), (0, 0), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and andavel(ny * W + nx):
                portas.append((nx, ny))
                break
    chao = sorted(elegivel)
    if chao:
        ymin, ymax = min(y for _, y in chao), max(y for _, y in chao)
        for alvo_y in (ymin, ymax):
            faixa = [p for p in chao if abs(p[1] - alvo_y) <= 1]
            if faixa:
                xs = sorted({p[0] for p in faixa})
                xe = min(xs, key=lambda x: abs(x - W // 2))
                portas.append(min((p for p in faixa if p[0] == xe),
                                  key=lambda p: abs(p[1] - alvo_y)))
    if not portas:
        return set(), []
    # LIGACAO EM ARVORE, nao em fila: cada porta nova se liga ao ponto ja ligado
    # mais perto, o que da uma rede com cruzamento em vez de zigue-zague.
    ossos = {portas[0]}
    for p in portas[1:]:
        trecho = caminho(p, ossos)
        if trecho:
            ossos |= set(trecho)
    return ossos, portas


def area_trilha(v, W, H, d, elegivel):
    """As celulas de TRILHA: o esqueleto engordado para tres de largura."""
    ossos, portas = esqueleto(v, W, H, d, elegivel)
    pav = set()
    for x, y in ossos:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                p = (x + dx, y + dy)
                if p in elegivel:
                    pav.add(p)
    while True:
        entra = {p for p in elegivel if p not in pav
                 and sum(1 for dx, dy in N4 if (p[0] + dx, p[1] + dy) in pav) >= 3}
        if not entra:
            break
        pav |= entra
    # risco de UMA celula de largura nao le como caminho, le como sujeira
    while True:
        fora = {(x, y) for x, y in pav
                if not ((x, y - 1) in pav or (x, y + 1) in pav)
                or not ((x - 1, y) in pav or (x + 1, y) in pav)}
        if not fora:
            break
        pav -= fora
    return pav, portas


def bolhas(livres, spec):
    """[(nomes, {celulas})], bolhas organicas crescidas por frente de onda.

    A SEMENTE nao e sorteio solto: as celulas livres sao ordenadas por um hash da
    posicao e a semente so e aceita a pelo menos 4 (Chebyshev) de toda semente ja
    aceita. O CRESCIMENTO e guloso com ruido: a cada passo entra a celula da
    frente de onda com o menor hash. Circulo daria bolha redonda e xadrez daria
    sal e pimenta; frente de onda com ruido da contorno irregular.
    """
    ordem = sorted(livres, key=lambda p: _mistura(p[0], p[1], 0x5EED))
    tomadas, saida, sementes = set(), [], []
    for esp in spec:
        feitas = 0
        for p in ordem:
            if feitas >= esp["quantas"]:
                break
            if p in tomadas:
                continue
            if any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) < 4 for q in sementes):
                continue
            lo, hi = esp["tam"]
            alvo = lo + _mistura(p[0], p[1], 0xB10B) % (hi - lo + 1)
            corpo, frente = {p}, set()
            for dx, dy in N4:
                q = (p[0] + dx, p[1] + dy)
                if q in livres and q not in tomadas:
                    frente.add(q)
            while len(corpo) < alvo and frente:
                q = min(frente, key=lambda r: _mistura(r[0], r[1], 0xC0FFEE))
                frente.discard(q)
                corpo.add(q)
                for dx, dy in N4:
                    rr = (q[0] + dx, q[1] + dy)
                    if rr in livres and rr not in tomadas and rr not in corpo:
                        frente.add(rr)
            if len(corpo) < lo:
                continue
            tomadas |= corpo
            sementes.append(p)
            saida.append((esp["grupo"], corpo))
            feitas += 1
    return saida


def desgasta(trilha, corte):
    """A trilha que vai receber tinta: miolo inteiro e parte da borda.

    Borda reta em chao batido nao existe; o corte por hash da posicao e o que
    tira a cara de fita adesiva. Nao ha estado nem ordem aqui.
    """
    return {p for p in trilha
            if all((p[0] + dx, p[1] + dy) in trilha for dx, dy in N4)
            or _mistura(p[0], p[1], 0x7A17) % 100 < corte}


def peca_da_mancha(nomes, x, y):
    """Qual das pecas do grupo cai nesta celula. Hash da posicao, nao paridade:
    paridade vira xadrez e o auto-teste reprova."""
    return nomes[_mistura(x, y, 0xA5A5 + len(nomes)) % len(nomes)]


# ----------------------------------------------------------- ligacao a pe
def componentes(v, W, H):
    """{celula: rotulo} dos pedacos de chao andavel ligados a pe.

    POR QUE NAO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda e
    alcancavel a partir de algum ponto de partida", e ponto de partida ali e
    warp OU objeto: fechar um corredor com warp dos dois lados nao tira NENHUMA
    celula do alcance e mesmo assim parte a cidade em duas. Em `SnowpointCity`
    isso passou VERDE numa sabotagem, e e por isso que este segundo portao
    existe. Ele olha a LIGACAO entre as celulas, que e o que o jogador sente.
    """
    rot, prox = {}, 0
    for y in range(H):
        for x in range(W):
            if (v[y * W + x] >> 10) & 3 or (x, y) in rot:
                continue
            fila, prox = [(x, y)], prox + 1
            rot[(x, y)] = prox
            while fila:
                cx, cy = fila.pop()
                ea = (v[cy * W + cx] >> 12) & 0xF
                for dx, dy in N4:
                    nx, ny = cx + dx, cy + dy
                    if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in rot:
                        continue
                    j = ny * W + nx
                    if (v[j] >> 10) & 3:
                        continue
                    eb = (v[j] >> 12) & 0xF
                    if ea and eb and ea != eb:
                        continue
                    rot[(nx, ny)] = prox
                    fila.append((nx, ny))
    return rot


def ligacao_intacta(antes, depois, solidificadas):
    """Nenhum pedaco de chao se PARTIU, e nenhum se juntou a outro."""
    mau = []
    por_rotulo = collections.defaultdict(set)
    for p, rr in antes.items():
        if p not in solidificadas:
            por_rotulo[rr].add(p)
    for rr, cels in por_rotulo.items():
        if len({depois.get(p) for p in cels}) > 1:
            mau.append("o pedaco %d de chao se partiu em %d"
                       % (rr, len({depois.get(p) for p in cels})))
    juntou = collections.defaultdict(set)
    for p, rr in depois.items():
        if p in antes:
            juntou[rr].add(antes[p])
    for rr, origens in juntou.items():
        if len(origens) > 1:
            mau.append("dois pedacos de chao que eram separados se juntaram")
    return mau


# ---------------------------------------------------------------- o PLANO
def plano_mapa(carimbos, base=None):
    """(L, W, H, v, escritas, contas) para `BlackthornCity`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    AG = E.agua()
    ids_chao = {c["mt"] for c in carimbos["chao"]}
    ids_plato = {c["mt"] for c in carimbos["plato"]}
    familia = {CARIMBO} | ids_chao
    familia_plato = {CARIMBO_PLATO} | ids_plato

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    elev = collections.Counter(
        (c >> 12) & 0xF for c in v
        if (c & 0x3FF) == CARIMBO and not ((c >> 10) & 3)).most_common(1)[0][0]
    elev_p = collections.Counter(
        (c >> 12) & 0xF for c in v
        if (c & 0x3FF) == CARIMBO_PLATO and not ((c >> 10) & 3)).most_common(1)[0][0]

    elegivel = {(i % W, i // W) for i in range(W * H)
                if andavel(i) and (v[i] & 0x3FF) in familia
                and ((v[i] >> 12) & 0xF) == elev
                and (attr_de(v[i] & 0x3FF) & 0x1FF) not in AG}
    elegivel_p = {(i % W, i // W) for i in range(W * H)
                  if andavel(i) and (v[i] & 0x3FF) in familia_plato
                  and ((v[i] >> 12) & 0xF) == elev_p
                  and (attr_de(v[i] & 0x3FF) & 0x1FF) not in AG}

    escritas = {}
    trilha, portas = area_trilha(v, W, H, d, elegivel)

    # ------------------------------------------------------------- 1. MOVEIS
    # Eles vem ANTES da mancha de proposito, e a razao esta medida em Snowpoint:
    # movel posto no carimbo tira uma celula do numerador E do denominador da
    # regua; movel posto em cima de uma mancha tira so do denominador, o que
    # PIORA a conta.
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))

    aplicado = list(v)
    ini = E.partidas(d, W, H, v)
    antes_alc = E.alcance(v, W, H, ini)
    novos_solidos, postos = [], []
    conta_mov = collections.Counter()
    por_movel = collections.defaultdict(list)

    def nao_liga(grade, x, y):
        """Os vizinhos andaveis de (x,y) ainda se falam sem passar por (x,y)?"""
        viz = [(x + dx, y + dy) for dx, dy in N4
               if 0 <= x + dx < W and 0 <= y + dy < H
               and not ((grade[(y + dy) * W + x + dx] >> 10) & 3)]
        if len(viz) < 2:
            return False
        vistos, fila, falta = {viz[0]}, [viz[0]], set(viz[1:])
        while fila and falta:
            cx, cy = fila.pop()
            ea = (grade[cy * W + cx] >> 12) & 0xF
            for dx, dy in N4:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in vistos:
                    continue
                j = ny * W + nx
                if (grade[j] >> 10) & 3:
                    continue
                eb = (grade[j] >> 12) & 0xF
                if ea and eb and ea != eb:
                    continue
                vistos.add((nx, ny))
                falta.discard((nx, ny))
                fila.append((nx, ny))
        return bool(falta)

    def livre(x, y):
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas or (x, y) not in elegivel:
            return False
        if (x, y) in trilha:
            return False
        return (aplicado[i] & 0x3FF) == CARIMBO

    def espacado(m, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < m["espaco"]
                       for px, py in por_movel[m["nome"]])

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portoes deixarem."""
        i = y * W + x
        antigo = aplicado[i]
        aplicado[i] = (antigo & 0xF000) | (1 << 10) | mt_id   # elevacao INTACTA
        perdidas = (antes_alc - E.alcance(aplicado, W, H, ini)) \
            - set(novos_solidos) - {(x, y)}
        if perdidas or nao_liga(aplicado, x, y):
            aplicado[i] = antigo
            return False
        escritas[i] = aplicado[i]
        novos_solidos.append((x, y))
        postos.append((x, y))
        return True

    ordem_cel = sorted(((x, y) for y in range(H) for x in range(W)),
                       key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF, p))

    lista = carimbos["moveis"]
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            m = lista[(giro + k) % len(lista)]
            if conta_mov[m["nome"]] >= m["quantos"]:
                continue
            if not livre(x, y) or not espacado(m, x, y):
                continue
            # movel de cidade encosta em alguma coisa: ou num solido, ou na
            # trilha. Peca solta no meio do vazio le como erro de mapa.
            perto = any(0 <= x + dx < W and 0 <= y + dy < H
                        and (((aplicado[(y + dy) * W + x + dx] >> 10) & 3)
                             or (x + dx, y + dy) in trilha)
                        for dx, dy in N4)
            if not perto:
                continue
            if not tenta_solidificar(x, y, m["mt"]):
                continue
            por_movel[m["nome"]].append((x, y))
            conta_mov[m["nome"]] += 1
            break

    # ------------------------------------------------------------- 2. MANCHA
    por_nome = {c["nome"]: c["mt"] for c in carimbos["chao"]}
    por_nome_p = {c["nome"]: c["mt"] for c in carimbos["plato"]}
    conta_mancha = collections.Counter()

    def pintavel(p, alvo_mt):
        i = p[1] * W + p[0]
        return i not in escritas and (aplicado[i] & 0x3FF) == alvo_mt

    def pinta(p, nomes, tabela):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | tabela[nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    for p in sorted(x for x in desgasta(trilha, ESPALHA["borda_trilha"])
                    if x in elegivel and pintavel(x, CARIMBO)):
        pinta(p, ESPALHA["trilha"], por_nome)
    livres = {p for p in elegivel if pintavel(p, CARIMBO)}
    for nomes, corpo in bolhas(livres, ESPALHA["bolhas"]):
        for p in sorted(corpo):
            pinta(p, nomes, por_nome)

    # ------------------------------------------------------- 3. MANCHA do PLATO
    livres_p = {p for p in elegivel_p if pintavel(p, CARIMBO_PLATO)}
    conta_plato = collections.Counter()

    def pinta_p(p, nomes):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | por_nome_p[nome]
        aplicado[i] = escritas[i]
        conta_plato[nome] += 1

    for nomes, corpo in bolhas(livres_p, ESPALHA_PLATO["bolhas"]):
        for p in sorted(corpo):
            pinta_p(p, nomes)

    # -------------------------------------------------------------- PORTOES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (ALVO, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel"
                             % (ALVO, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (ALVO, "; ".join(queixas)))
    contas = dict(trilha=len(trilha), moveis=dict(conta_mov),
                  manchas=dict(conta_mancha), plato=dict(conta_plato),
                  solidos=len(novos_solidos), portas=len(portas),
                  elegivel=len(elegivel), elegivel_plato=len(elegivel_p))
    return L, W, H, v, escritas, contas


def regua(v, W, H, L, escritas=None, split_certo=False):
    """(carimbo dominante em %, celulas andaveis a pe, id do carimbo).

    Por padrao conta EXATAMENTE como a `regua_cidades.py`, que resolve o
    comportamento com `arte_ginasios_sinnoh.comportamento`, ou seja com o split
    do Emerald (512). `split_certo=True` refaz a conta com o split de Johto
    (640), que e o certo; a diferenca esta medida no cabecalho de `attr_de`.
    """
    AG = E.agua()
    if split_certo:
        def beh(mt):
            return attr_de(mt) & 0x1FF
    else:
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    cel = list(v)
    for i, val in (escritas or {}).items():
        cel[i] = val
    and_ = [c & 0x3FF for c in cel
            if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG]
    top = collections.Counter(and_).most_common(1)[0]
    return 100.0 * top[1] / len(and_), len(and_), top[0]


# --------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(guardado):
    """A grade como esta no disco, so tirando o que ESTA passada escreveu.

    Sem isso a idempotencia morre: planejar sobre um mapa que ja recebeu esta
    passada nao volta ao mesmo lugar.
    """
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    fusao, tiles_novos, metas, attrs, carimbos = desenha_kit()
    print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d)%s"
          % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
             TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
             max(metas), N_META_PRI + min(metas), N_META_PRI + max(metas),
             "" if not fusao else "; fusao da vaga %d na %d (%d cores, %d "
             "escrita(s) de verdade)" % (fusao["de"], fusao["para"],
                                         fusao["cores"], len(fusao["escritas"]))))
    if aplicar:
        grava_tileset(fusao, tiles_novos, metas, attrs)
    guardado = carrega_plano()
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base_de(guardado))
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    ac, nac, _ = regua(v, W, H, L, None, True)
    bc, nbc, idbc = regua(v, W, H, L, escritas, True)
    print("%s: trilha %d, mancha %d, plato %d, %d celulas solidificadas, %d "
          "celulas mudadas de %d"
          % (ALVO, contas["trilha"], sum(contas["manchas"].values()),
             sum(contas["plato"].values()), contas["solidos"], len(escritas), W * H))
    print("  mancha: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["manchas"].items())))
    print("  plato:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["plato"].items())))
    print("  movel:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    print("  regua (como a regua_cidades.py conta): carimbo %d com %.1f%% de %d "
          "ANTES; carimbo %d com %.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
    print("  regua (split de Johto, o certo):       %.1f%% de %d ANTES; "
          "carimbo %d com %.1f%% de %d DEPOIS" % (ac, nac, idbc, bc, nbc))
    if aplicar:
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(saida), *saida))
        guardado[ALVO] = {"celulas": [[i, v[i], escritas[i]]
                                      for i in sorted(escritas)]}
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("aplicado")
    return 0


def desfaz():
    guardado = carrega_plano()
    if ALVO not in guardado:
        print("%s: nada a desfazer" % ALVO)
        return 0
    d, L, W, H, v = G.grade(ALVO)
    v, n = list(v), 0
    for idx, antigo, novo in guardado[ALVO]["celulas"]:
        if v[idx] == novo:
            v[idx] = antigo
            n += 1
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(v), *v))
    guardado.pop(ALVO)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("%s: desfeitas %d celulas" % (ALVO, n))
    return 0


# ------------------------------------------------------------------ conferencia
def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def confere(fusao, tiles_novos, metas, attrs, carimbos, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela e chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que
    tem que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida so no caminho feliz nao e regra, e prova positiva sem
    par negativo nao e prova.
    """
    mau = []
    dados = kit()
    ap = G._attrs(PRIMARIO)
    ts = _tileset(SECUNDARIO)
    base, attr_areia, areia_px = areia_nossa()
    attr_plato = ap[CARIMBO_PLATO]
    pal_novas = {str(dados["vaga"]): dados["paleta"]}
    if fusao:
        pal_novas[str(fusao["para"])] = fusao["paleta"]

    def atributo(mt):
        return attr_de(mt, attrs)

    def entradas(mt):
        return entradas_de(mt, metas)

    def px_de(mt):
        return pixels_de(mt, tiles_novos, metas, pal_novas)

    # ------------------------------------------------------------ 1. orcamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles do secundario" % TETO_TILES)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles do secundario" % TETO_META)
    cab = open(f"{RAIZ}/src/data/tilesets/headers.h").read()
    i = cab.find("const struct Tileset %s =" % SECUNDARIO)
    if i < 0 or ".callback = NULL," not in cab[i:i + 400]:
        mau.append("o %s deixou de ter .callback = NULL: alguma vaga de tile "
                   "pode estar pinada por animacao e a renumeracao nao vale mais"
                   % SECUNDARIO)

    # -------------------------------------------------------------- 2. a fusao
    if fusao:
        cores = [tuple(c) for c in fusao["paleta"][1:] if tuple(c) != (0, 0, 0)]
        if len(cores) > 15:
            mau.append("a fusao pede %d cores" % len(cores))
        if len(set(cores)) != len(cores):
            mau.append("a fusao gasta duas vagas com a MESMA cor")
        # A PROVA de que a fusao nao muda um pixel: para todo indice remapeado,
        # a cor no indice de DESTINO e a MESMA cor do indice de ORIGEM.
        for k, alvo in fusao["remap"].items():
            origem = tuple(ts["paletas"][fusao["de"]][int(k)])
            destino = tuple(fusao["paleta"][alvo])
            if origem != destino:
                mau.append("a fusao aproxima cor: o indice %s da vaga %d e %s e "
                           "o indice %d da vaga %d ficou %s"
                           % (k, fusao["de"], origem, alvo, fusao["para"], destino))
        # e nenhum indice VIVO da vaga de destino se mexeu
        usados = indices_usados()
        for idx in usados.get(fusao["para"], ()):
            if tuple(fusao["paleta"][idx]) != tuple(ts["paletas"][fusao["para"]][idx]):
                mau.append("a fusao mudou a cor do indice %d da vaga %d, que "
                           "algum pixel nosso usa" % (idx, fusao["para"]))

    # ------------------------------- 3. a vaga do kit e a que a fusao esvaziou
    if int(dados["vaga"]) != FUSAO["de"]:
        mau.append("o kit pinta na vaga %s, que nao e a que a fusao esvazia"
                   % dados["vaga"])
    cores_kit = [tuple(c) for c in dados["paleta"][1:] if tuple(c) != (0, 0, 0)]
    if len(cores_kit) > 15:
        mau.append("a vaga do kit pede %d cores" % len(cores_kit))
    if len(set(cores_kit)) != len(cores_kit):
        mau.append("a vaga do kit gasta dois indices com a MESMA cor")
    # as QUATRO cores da nossa areia tem que estar la, senao o fundo composto
    # nao pode ser a nossa areia
    da_areia = {areia_px[y][x] for y in range(16) for x in range(16)}
    falta = [c for c in da_areia if list(c) not in [list(x) for x in dados["paleta"]]]
    if falta:
        mau.append("a vaga do kit nao tem %d cor(es) da nossa areia: %s"
                   % (len(falta), falta[:4]))

    # ---------------------- 4. CHAO: atributo do carimbo e camada de cima VAZIA
    ids_chao = {c["mt"]: c for c in carimbos["chao"]}
    ids_plato = {c["mt"]: c for c in carimbos["plato"]}
    ids_movel = {m["mt"]: m for m in carimbos["moveis"]}
    for gid, c in ids_chao.items():
        if atributo(gid) != attr_areia:
            mau.append("o chao %d tem atributo 0x%04X e o carimbo tem 0x%04X"
                       % (gid, atributo(gid), attr_areia))
        if any(e & 0x3FF for e in entradas(gid)[4:]):
            mau.append("o chao %d usa a camada de cima, que com layerType NORMAL "
                       "desenha ACIMA do jogador" % gid)
    for gid, c in ids_plato.items():
        if atributo(gid) != attr_plato:
            mau.append("o chao de plato %d tem atributo 0x%04X e o 113 tem 0x%04X"
                       % (gid, atributo(gid), attr_plato))

    # ------- 5. A TINTA DE CHAO E SEMPRE A NOSSA. Nenhuma cor da rampa de chao
    #            da fonte pode sobreviver em peca de chao, e a troca tem que ser
    #            posto a posto (injetiva e na mesma ordem de luminancia).
    def luz(c):
        return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

    rampa = [tuple(c) for c in dados["rampa_da_fonte"]]
    nossa = [tuple(c) for c in dados["cores_areia"]]
    remap = {tuple(int(z) for z in k.split(",")): tuple(v)
             for k, v in dados["remap"].items()}
    if sorted(remap) != sorted(rampa):
        mau.append("o remap do kit nao cobre a rampa de chao da fonte")
    if len(set(remap.values())) != len(remap):
        mau.append("duas cores de chao da fonte caem na MESMA cor nossa")
    if set(remap.values()) - set(nossa):
        mau.append("o remap manda cor de chao da fonte para fora da nossa areia")
    ordem_f = sorted(remap, key=luz, reverse=True)
    if [remap[c] for c in ordem_f] != sorted(remap.values(), key=luz, reverse=True):
        mau.append("a troca de tinta de chao nao respeita a ordem de luminancia")
    proibidas = set(rampa)
    for gid, c in ids_chao.items():
        if not c.get("importado"):
            continue
        p = px_de(gid)
        sobrou = {q for q in p if q in proibidas}
        if sobrou:
            mau.append("o chao %d ainda pinta com tinta de chao da fonte (%s): "
                       "a areia nao e a nossa" % (gid, sorted(sobrou)[:3]))

    # ------- 6. MOVEL: COVERED, comportamento zerado, e o NOSSO chao embaixo
    for gid, m in ids_movel.items():
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %d nao esta em COVERED (0x%04X)" % (gid, a))
        if a & 0xFF:
            mau.append("o movel %d importou comportamento 0x%02X da fonte"
                       % (gid, a & 0xFF))
        if entradas(gid)[:4] != base:
            mau.append("o movel %d nao tem a nossa areia na camada de baixo" % gid)
        if not any(e & 0x3FF for e in entradas(gid)[4:]):
            mau.append("o movel %d nao tem arte na camada de cima" % gid)

    # ---------- 6b. A COR DA PECA DE CHAO. Esta guarda nasceu de um defeito que
    #                so o render mostrou, duas vezes seguidas nesta rodada: os
    #                metatiles 533, 593 e 613 do primario sao a MESMA rocha de
    #                montanha do 113, passavam em todos os outros portoes, e cada
    #                um carrega 14 pixels de AGUA no topo (sao pecas de beira de
    #                lago): espalhados pelo plato eles viraram riscos AZUIS no
    #                meio do barranco. Trocados por eles, o 153 passou de novo e
    #                virou risco AMARELO, porque carrega 14 pixels do topo de uma
    #                cerca clara; e o 105 carrega 14 pixels da grama
    #                (115,205,164). Sao TRES regras, e cada uma pega um dos tres:
    #                  fria  : B > R + 8            (agua)
    #                  verde : G > R + 24           (grama)
    #                  clara : luminancia acima da MAIS CLARA do carimbo (o chao
    #                          e o que reflete a luz da cena; peca de chao pode
    #                          ter sombra mais escura, nunca brilho mais claro)
    def luz2(c):
        return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]

    for rotulo, alvos, carimbo_id in (("praca", ids_chao, CARIMBO),
                                      ("plato", ids_plato, CARIMBO_PLATO)):
        teto = max(luz2(c) for c in set(px_de(carimbo_id)))
        for gid in alvos:
            cs = set(px_de(gid))
            ruins = [c for c in cs if c[2] > c[0] + 8 or c[1] > c[0] + 24
                     or luz2(c) > teto]
            if ruins:
                mau.append("a peca de %s %d usa %d cor(es) que o carimbo %d nao "
                           "admite %s: e agua, grama ou brilho de outra peca"
                           % (rotulo, gid, len(ruins), carimbo_id,
                              sorted(ruins)[:3]))

    # ---------- 7. nenhuma variante e copia pixel a pixel de outra, por familia
    for rotulo, lista in (("praca", sorted(ids_chao) + [CARIMBO]),
                          ("plato", sorted(ids_plato) + [CARIMBO_PLATO]),
                          ("movel", sorted(ids_movel))):
        pix = {mt: px_de(mt) for mt in lista}
        for k, a in enumerate(lista):
            for b in lista[k + 1:]:
                dd = distancia(pix[a], pix[b])
                if dd < PISO_VARIANTE:
                    mau.append("as variantes de %s %d e %d tem distancia %.1f, "
                               "abaixo do piso de %.1f do varia_carimbo.py: isso "
                               "e enganar a regua"
                               % (rotulo, a, b, dd, PISO_VARIANTE))

    # -------------------------------------------- 8 a 13. o plano, celula a celula
    L, W, H, v, escritas, contas = plano
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    meus_chaos = set(ids_chao)
    meus_platos = set(ids_plato)
    meus_moveis = set(ids_movel)

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("mudou ELEVACAO em (%d,%d)" % (x, y))
        if cv and not cn:
            mau.append("colisao 1 -> 0 em (%d,%d), que segue proibida" % (x, y))
        if novo in meus_chaos:
            if cn != cv or velho != CARIMBO:
                mau.append("chao da praca em celula errada em (%d,%d)" % (x, y))
        elif novo in meus_platos:
            if cn != cv or velho != CARIMBO_PLATO:
                mau.append("chao de plato em celula errada em (%d,%d)" % (x, y))
        elif novo in meus_moveis:
            if cv or not cn:
                mau.append("movel em (%d,%d) nao e solidificacao 0 -> 1" % (x, y))
            if velho != CARIMBO:
                mau.append("movel fora do carimbo em (%d,%d)" % (x, y))
            if (x, y) in ev:
                mau.append("movel em cima do evento (%d,%d)" % (x, y))
        else:
            mau.append("metatile %d escrito em (%d,%d) e de fora do kit"
                       % (novo, x, y))

    # 9. (comportamento, layerType) de toda celula ANDAVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("celula andavel (%d,%d) mudou (comportamento, layerType)"
                       % (i % W, i // W))
            break

    # 10. alcance a pe e LIGACAO a pe
    ini = E.partidas(d, W, H, v)
    antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
    solid = {(i % W, i // W) for i in escritas
             if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
    if (antes - depois) - solid:
        mau.append("o alcance a pe perdeu %d celulas alem das solidificadas: %s"
                   % (len((antes - depois) - solid),
                      sorted((antes - depois) - solid)[:6]))
    if depois - antes:
        mau.append("o alcance a pe GANHOU celula")
    mau += ligacao_intacta(componentes(v, W, H), componentes(saida, W, H), solid)

    # 11. A MANCHA NAO PODE SER ADIVINHAVEL, e o teste tem dois lados.
    def componente_media(alvo_mt, ids):
        """Tamanho medio do pedaco CONEXO do terreno elegivel daquela familia.

        E ele que da o piso de forma da mancha, e nao um numero decorado: o
        plato de `BlackthornCity` sao 150 celulas em NOVE pedacos separados
        (media 16,7) e a praca sao 385 em nove (media 42,8). Cobrar 12 celulas
        de mancha media nos dois seria cobrar do plato uma bolha maior do que o
        terreno dele comporta.
        """
        fam = {alvo_mt} | set(ids)
        cel = {(i % W, i // W) for i in range(W * H)
               if not ((v[i] >> 10) & 3) and (v[i] & 0x3FF) in fam}
        vis, n = set(), 0
        for p in sorted(cel):
            if p in vis:
                continue
            n += 1
            pilha = [p]
            vis.add(p)
            while pilha:
                q = pilha.pop()
                for dx, dy in N4:
                    rr = (q[0] + dx, q[1] + dy)
                    if rr in cel and rr not in vis:
                        vis.add(rr)
                        pilha.append(rr)
        return (len(cel) / n if n else 0.0), len(cel)

    for rotulo, conjunto, minimo, carimbo_id in (
            ("praca", meus_chaos, 200, CARIMBO),
            ("plato", meus_platos, 60, CARIMBO_PLATO)):
        mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
                  if (val & 0x3FF) in conjunto}
        if len(mancha) < minimo:
            mau.append("so %d celulas de mancha na %s (minimo %d)"
                       % (len(mancha), rotulo, minimo))
        if not mancha:
            continue
        tot = len(mancha)
        cego = collections.Counter(mancha.values()).most_common(1)[0][1] / tot
        for rot, eixo in (("x", lambda p: p[0]), ("y", lambda p: p[1]),
                          ("x+y", lambda p: p[0] + p[1]),
                          ("x-y", lambda p: p[0] - p[1])):
            for mod in range(2, 9):
                tab = collections.defaultdict(collections.Counter)
                for p, mt_id in mancha.items():
                    tab[eixo(p) % mod][mt_id] += 1
                ac = sum(c.most_common(1)[0][1] for c in tab.values()) / tot
                if ac - cego > 0.12:
                    mau.append("na %s, saber %s mod %d adivinha a peca em %.0f%% "
                               "das celulas contra %.0f%% do chute cego: virou "
                               "padrao" % (rotulo, rot, mod, 100 * ac, 100 * cego))
        vistos, pedacos = set(), 0
        for p in sorted(mancha):
            if p in vistos:
                continue
            pedacos += 1
            pilha = [p]
            vistos.add(p)
            while pilha:
                q = pilha.pop()
                for dx, dy in N4:
                    rr = (q[0] + dx, q[1] + dy)
                    if rr in mancha and rr not in vistos:
                        vistos.add(rr)
                        pilha.append(rr)
        terreno, n_terreno = componente_media(carimbo_id, conjunto)
        # O PISO DE FORMA e o do molde (o `neve_snowpoint2.py` calibrou 12 com
        # a mancha boa em 17,05 celulas por pedaco contra 8,32 na versao
        # espalhada), mas ele DESCE quando o terreno e mais picado que isso: o
        # plato desta cidade sao 150 celulas em nove pedacos separados, e cobrar
        # bolha de 12 la seria cobrar bolha maior que o terreno.
        piso_forma = min(12.0, 0.55 * terreno)
        if len(mancha) / pedacos < piso_forma:
            mau.append("na %s a mancha media tem so %.1f celulas (%d em %d "
                       "pedacos) contra o piso de %.1f (o terreno tem %d celulas "
                       "em pedacos de %.1f): virou sal e pimenta, nao bolha"
                       % (rotulo, len(mancha) / pedacos, len(mancha), pedacos,
                          piso_forma, n_terreno, terreno))

    # 12. a regua tem que fechar em 20% ou menos, na conta da regua_cidades.py
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("a regua ainda marca %.1f%% de carimbo dominante (metatile %d)"
                   % (b, idb))
    bc, _n, _i = regua(v, W, H, L, escritas, True)
    if bc > TETO_REGUA:
        mau.append("com o split certo a regua marca %.1f%%" % bc)
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e DOZE provas negativas, cada sabotagem revertida em seguida.

    "Zero diferenca" so vale depois que a comparacao mostra que sabe reprovar.
    """
    fusao, tiles_novos, metas, attrs, carimbos = desenha_kit()
    guardado = carrega_plano()
    plano = plano_mapa(carimbos, base_de(guardado))
    mau = confere(fusao, tiles_novos, metas, attrs, carimbos, plano)
    negativas, pulados = [], []

    def copia():
        return (json.loads(json.dumps(fusao)) if fusao else None,
                {k: [list(l) for l in v] for k, v in tiles_novos.items()},
                {k: list(v) for k, v in metas.items()}, dict(attrs),
                json.loads(json.dumps(carimbos)),
                (plano[0], plano[1], plano[2], list(plano[3]), dict(plano[4]),
                 plano[5]))

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = confere(*args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NAO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    # N1. colisao 1 -> 0 numa celula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[5]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a celula ERA solida
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevacao alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[5]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. comportamento IMPORTADO num metatile de chao
    def n3():
        a = copia()
        gid = [c["mt"] for c in carimbos["chao"] if c.get("importado")][0]
        a[3][gid - N_META_PRI] = (a[3][gid - N_META_PRI] & 0xFF00) | 0x02
        return a
    sabota("behavior de chao sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = [m["mt"] for m in carimbos["moveis"] if m.get("importado")][0]
        a[3][gid - N_META_PRI] = a[3][gid - N_META_PRI] & 0x0FFF
        return a
    sabota("layerType NORMAL no movel", n4, "nao esta em COVERED")

    # N5. camada de CIMA numa peca de chao andavel (tapa o jogador)
    def n5():
        a = copia()
        gid = [c["mt"] for c in carimbos["chao"] if c.get("importado")][0]
        ent = list(a[2][gid - N_META_PRI])
        ent[4] = ent[0]
        a[2][gid - N_META_PRI] = ent
        return a
    sabota("chao com camada de cima", n5, "usa a camada de cima")

    # N6. A TINTA DE CHAO DA FONTE VOLTA. O kit em DISCO ganha, num indice
    #     morto da vaga 7, uma das quatro cores da rampa de chao do hack, e o
    #     primeiro tile de chao passa a pintar com ela. E a sabotagem que guarda
    #     a regra "a tinta de chao e sempre a nossa" por construcao: sem ela, a
    #     peca de chao chegaria com a areia vermelha da caverna do Scorched
    #     Silver em volta e o portao de cor nao teria o que medir.
    def n6():
        a = copia()
        dados = kit()
        pal = [list(c) for c in dados["paleta"]]
        livre = [i for i in range(1, 16) if pal[i] == [0, 0, 0]][0]
        pal[livre] = list(dados["rampa_da_fonte"][0])
        dados["paleta"] = pal
        chave = sorted(k for k in dados["tiles"] if k.startswith("chao:"))[0]
        t = [list(l) for l in dados["tiles"][chave]]
        t[0][0] = livre
        dados["tiles"][chave] = t
        with open(KIT_JSON + ".sab", "w") as fp:
            json.dump(dados, fp)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        # os tiles precisam ser RELIDOS do kit sabotado, senao a conferencia
        # renderiza o desenho bom e nao tem o que acusar
        _f, tiles_sab, _m, _at, _c = desenha_kit()
        return (a[0], tiles_sab, a[2], a[3], a[4], a[5])
    try:
        sabota("tinta de chao da fonte de volta", n6,
               "ainda pinta com tinta de chao da fonte")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # N7. camada de baixo do movel sabotada (nao e mais a nossa areia)
    def n7():
        a = copia()
        gid = [m["mt"] for m in carimbos["moveis"] if m.get("importado")][0]
        ent = list(a[2][gid - N_META_PRI])
        ent[0] = ent[4]
        a[2][gid - N_META_PRI] = ent
        return a
    sabota("camada de baixo do movel", n7, "nao tem a nossa areia na camada de baixo")

    # N8. a fusao APROXIMANDO cor em vez de mover o indice
    def n8():
        a = copia()
        alvo = list(a[0]["remap"].values())[0]
        a[0]["paleta"][alvo] = [255, 0, 255]
        return a
    if fusao:
        sabota("fusao aproximando cor", n8, "a fusao aproxima cor")
    else:
        pulados.append("fusao aproximando cor")

    # N9. a fusao mexendo num indice VIVO da vaga de destino
    def n9():
        a = copia()
        usados = indices_usados()
        idx = sorted(usados[FUSAO["para"]])[0]
        a[0]["paleta"][idx] = [255, 0, 255]
        return a
    if fusao:
        sabota("fusao mexendo em indice vivo", n9, "que algum pixel nosso usa")
    else:
        pulados.append("fusao mexendo em indice vivo")

    # N10. mancha escolhida por (x + y) % n, que e xadrez com periodo
    def n10():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            a = (a[0], a[1], a[2], a[3], a[4],
                 plano_mapa(carimbos, base_de(guardado)))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por (x+y) % n", n10, "virou padrao")

    # N11. corredor fechado que PARTE um pedaco de chao. O portao de alcance
    #      sozinho nao pega isso quando ha warp dos dois lados, e foi assim que
    #      Snowpoint passou verde com a cidade cortada.
    def n11():
        a = copia()
        L, W, H, v, esc, ct = a[5]
        final = list(v)
        for j, val in esc.items():
            final[j] = val
        antes = componentes(final, W, H)
        for y in range(H):
            for x in range(W):
                i = y * W + x
                if (final[i] >> 10) & 3:
                    continue
                teste = list(final)
                teste[i] = (final[i] & 0xF000) | (1 << 10) | (final[i] & 0x3FF)
                if ligacao_intacta(antes, componentes(teste, W, H), {(x, y)}):
                    esc[i] = teste[i]
                    return a
        raise SystemExit("nao achei ponto de articulacao para a sabotagem N11")
    sabota("corredor fechado", n11, "se partiu")

    # N12. duas variantes de chao IGUAIS pixel a pixel: e enganar a regua
    def n12():
        a = copia()
        imp = [c["mt"] for c in carimbos["chao"] if c.get("importado")]
        a[2][imp[1] - N_META_PRI] = list(a[2][imp[0] - N_META_PRI])
        return a
    sabota("variante de chao duplicada", n12, "abaixo do piso")

    # N13. metatile de FORA do kit escrito no mapa
    def n13():
        a = copia()
        L, W, H, v, esc, ct = a[5]
        i = sorted(esc)[len(esc) // 2]
        esc[i] = (esc[i] & 0xFC00) | 999
        return a
    sabota("metatile de fora do kit", n13, "e de fora do kit")

    # ------------------------------------------------ o que esta NO DISCO
    # Sem este caso o auto-teste so confere o que ele mesmo acabou de calcular.
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.convert("P").load()
    n_disco = len(meta_disco) // 16
    postas = [l for l in metas if l < n_disco
              and _entradas(meta_disco, l) == metas[l]]
    if not postas:
        pulados.append("o que esta NO DISCO (o kit ainda nao foi aplicado)")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ents in metas.items():
            if local >= n_disco or _entradas(meta_disco, local) != ents:
                mau.append("metatile %d no disco nao e o do kit"
                           % (N_META_PRI + local))
            elif struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (N_META_PRI + local))
        for vaga_t, tile in tiles_novos.items():
            if (vaga_t // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga_t)
                continue
            x0, y0 = (vaga_t % cols) * 8, (vaga_t // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga_t)
        arq = [l.split() for l in
               open(f"{DESTINO}/palettes/%02d.pal" % int(kit()["vaga"])).read()
               .split("\n")[3:] if l.strip()]
        if [[int(z) for z in c] for c in arq[:16]] != kit()["paleta"]:
            mau.append("a paleta %s no disco nao e a do kit" % kit()["vaga"])

    # ------------------------------------------------------- idempotencia
    L, W, H, v, escritas, contas = plano
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    volta = list(saida)
    for i in sorted(escritas):
        if volta[i] == escritas[i]:
            volta[i] = v[i]
    if volta != list(v):
        mau.append("desfazer nao devolve a base")
    _, _, _, _, esc2, _ = plano_mapa(carimbos, volta)
    if esc2 != escritas:
        mau.append("segunda passada deu plano diferente")

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE")
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("  %s: %d celulas mudadas, %d solidificadas, regua %.1f%% (mt %d) -> "
          "%.1f%% (mt %d)" % (ALVO, len(escritas), contas["solidos"], a, ida, b, idb))
    print("  %d tiles, %d metatiles, %d provas negativas:"
          % (len(tiles_novos), len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-30s -> %s" % (nome, queixa[:100]))
    if pulados:
        print("  casos PULADOS nesta rodada (rode o --demo dos dois lados do "
              "--aplicar para exercitar todos):")
        for nome in pulados:
            print("    %s" % nome)
    return 0


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--desfazer" in sys.argv:
        return desfaz()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--so-tileset" in sys.argv:
        f, t, m, at, c = desenha_kit()
        grava_tileset(f, t, m, at)
        print("tileset escrito: %d tiles, %d metatiles" % (len(t), len(m)))
        return 0
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
