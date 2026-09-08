#!/usr/bin/env python3
"""Refino de `OreburghCity` (tema MINA) e `EternaCity` (tema FLORESTA), no
`gTileset_Jubilife`, com arte importada do `Pokemon Light Platinum`.

O QUE ESTAS DUAS CIDADES TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
em 08/09/2026: `OreburghCity` gasta 61,5% do chao andavel a pe (766 celulas de
1.246) com UM metatile, o 268, que e o barro liso do primario; `EternaCity` gasta
30,0% (303 de 1.011) com o metatile 1, a grama lisa. Oreburgh e uma cidade de
minerado sem nada de mina no chao: um tapete marrom de meio mapa, com quatro
pedras soltas. Eterna e a cidade da floresta com um gramado sem um tufo.

O ORCAMENTO, medido nesta arvore e nao herdado de brief:

  tiles      384 de 512 no `tiles.png`, 308 vivos e 75 mortos. Sobram 128 vagas
             SEM compactar nada, e este kit gasta menos que isso: o
             `compacta_tileset.py` NAO foi rodado, para nao mexer no indice de
             tile de nenhum metatile vivo.
  metatiles  o maior id que aparece em `map.bin` de qualquer um dos SETE layouts
             do tileset e 897 (local 385). Os locais 387 a 511 (ids 899 a 1023)
             estao todos com enchimento do dumper e nenhum deles aparece em mapa
             nenhum: 125 vagas livres.
  paletas    as SETE vagas do secundario (6 a 12) estao ocupadas, e a ferramenta
             que deveria liberar uma REPROVA nesta arvore: `compacta_paletas.py
             gTileset_Jubilife --autoteste` fecha VERMELHO, com 6.704 pixels
             diferentes de 4.597.248 no portao de render dos sete mapas (o
             defeito aparece em porta e janela de predio de `OreburghCity` e
             `EternaCity`; os outros cinco mapas ficam identicos). Ou seja: a
             vaga que o plano da onda prometia NAO existe pelo caminho previsto.

A VAGA DE PALETA VEM DE OUTRO LUGAR, e a conta esta aqui. As vagas 6 e 7 do
`gTileset_Jubilife` sao as duas mais baratas do tileset e sao FUNDIVEIS sem
aproximar cor nenhuma:

  vaga 6   10 cores nao-zero, nos indices 1,2,3,4,5,6,11,12,13,14, em 7 tiles
  vaga 7    9 cores nao-zero, nos indices 1,2,3,4,11,12,13,14,15, em 17 tiles
  QUATRO cores sao IGUAIS nas duas e ja moram no MESMO indice: (160,160,176) no
  11, (80,80,104) no 12, (120,120,136) no 13 e (200,200,216) no 14.
  A uniao da 15 cores exatas, que e o que uma paleta de BG do GBA comporta.

E a fusao e limpa por tres medidas, nao por sorte:
  - NENHUM tile e usado com as duas vagas (intersecao vazia), entao nenhum tile
    precisa ser DUPLICADO. Foi essa duplicacao, num tileset que precisa dela, o
    caminho que o `compacta_paletas.py` erra.
  - nenhum tile do PRIMARIO e pintado com a vaga 6 nem com a 7, entao nao ha
    pixel de tile compartilhado para reindexar.
  - nenhum metatile do primario referencia tile do secundario (zero, medido),
    entao mexer no pixel de tile do secundario nao muda o primario em lugar
    nenhum.
  O remapeamento e so este: os indices 1,2,3,4 da vaga 7 viram 7,8,9,10 na vaga
  6; 11 a 15 ficam onde estao. Dezessete tiles tem os nibbles reescritos e os
  metatiles que apontavam para a vaga 7 passam a apontar para a 6. A vaga 7
  fica LIVRE, com 15 cores para gastar.

ALEM DA VAGA 7, este trabalho usa INDICE VAGO de paleta ja em uso, que e de
graca e nao mexe em pixel nenhum: uma paleta do GBA tem 15 cores desenhaveis e
as vagas do `gTileset_Jubilife` usam de 8 a 14. Escrever cor NOVA num indice que
NENHUM pixel do tileset usa nao muda o desenho de nada, por construcao, e o
portao de render prova isso nos sete mapas. Medido aqui: a vaga 11 tem os
indices 3, 4, 8, 10, 14 e 15 vagos, e e la que mora a peca importada de Eterna.

A ARTE, e de onde vem cada coisa:

  MINA (Oreburgh), do `Pokemon Light Platinum` (autor WesleyFG, base Ruby AXVE,
  md5 7fd2c08735459d99fa23fdaa9b755486), primario de exterior `0x286CF4` e
  secundario `0x286E8C`, o par da pedreira a ceu aberto do grupo 24 (o mapa de
  amostra e o g24m09, 44x80). Dali vem o CHAO de cascalho e o inventario de
  pedreira que Oreburgh nao tinha: pedra, pedregulho, pilha de minerio,
  engradado, viga de madeira e barril. O barro da pedreira do hack e da MESMA
  familia do barro de Oreburgh, e essa e a razao de ter sido escolhido entre os
  cinco secundarios triados: (184,136,128)/(152,104,96)/(128,80,72) contra os
  nossos (189,148,139)/(156,115,115)/(131,90,90).

  FLORESTA (Eterna), em duas fontes:
   - o proprio `gTileset_GeneralSinnoh`, que ja tem 75 pecas desenhadas SOBRE a
     grama do metatile 1 e seis variantes de grama com o atributo IGUAL ao dele,
     e nenhuma delas aparecia em `EternaCity`. Custam zero tile, zero cor e (as
     que precisam de comportamento zerado) uma vaga de metatile cada.
   - o `Light Platinum` outra vez, secundario `0x286FAC` (a floresta densa do
     g24m04), so pelo TRONCO CAIDO, que e a peca de mato que o nosso tileset nao
     tem em nenhuma forma. Cinco cores, nos indices vagos da vaga 11.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHAO NOVO e metatile com arte SO na camada de BAIXO e atributo IGUAL, bit a
    bit, ao do carimbo que ele substitui (0x00A0 em Oreburgh, o
    MB_BERRY_TREE_SOIL do barro; 0x0000 em Eterna). Camada de cima em chao
    andavel com layerType NORMAL desenharia ACIMA do jogador, e cascalho por
    cima do boneco e defeito, nao enfeite.
  - MOVEL e celula que vira SOLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chao entrada por entrada, e o atributo e comportamento ZERADO
    com layerType COVERED (0x1000), que e o que poe as duas camadas ABAIXO do
    sprite. Sem COVERED o BG1 tapa o jogador (o defeito E3 do `mapas_qa.py`).
  - QUADRANTE DE BAIXO SOBE quando o de cima esta vazio, que e a regra do
    `porto_canalave.py`: a fonte nem sempre desenha a peca na camada de cima.
  - O CHAO DA FONTE NAO ENTRA, e ele e achado por EVIDENCIA: sao os tiles que
    aparecem na camada de baixo dos metatiles que a propria fonte usa como piso
    (camada de cima vazia, uma paleta so). Quadrante promovido cujo tile esta
    nessa lista e DESCARTADO, e no lugar dele fica o nosso chao. Sem isso o
    engradado da pedreira chega com um tapete de barro do hack em volta.
  - Nenhum id de flag, var, script, musica, treinador ou especie e importado.
    Comportamento e id semantico: todo movel entra com o comportamento ZERADO.

O QUE FICOU DE FORA, com o motivo:
  - a BOCA DE GALERIA do hack (metatiles 11 a 13 e 19 a 21, o arco de entrada de
    tunel). Ela e linda e cabia no orcamento, e foi cortada por jogabilidade:
    `OreburghCity` ja tem a entrada de verdade da mina, e um segundo arco igual
    que nao e warp e uma armadilha para quem joga.
  - o CARRINHO e o TRILHO que o tema pedia: a pedreira do Light Platinum nao tem
    nenhum dos dois. O que ela tem no lugar e a rampa de carga (uma estrutura de
    cinco celulas com montante laranja), que exige parede de penhasco dos dois
    lados e nao cabe no chao aberto de Oreburgh.
  - a VARIACAO DE SILHUETA DE ARVORE que Snowpoint fez: `EternaCity` nao tem o
    defeito de Snowpoint. La eram 193 blocos 2x2 IDENTICOS; aqui as arvores ja
    sao dezenas de metatiles diferentes.

Uso:
    python3 dev_scripts/mina_oreburgh.py                     # mede e mostra o plano
    python3 dev_scripts/mina_oreburgh.py --aplicar           # os dois mapas
    python3 dev_scripts/mina_oreburgh.py --aplicar --mapa OreburghCity
    python3 dev_scripts/mina_oreburgh.py --desfazer          # devolve os map.bin
    python3 dev_scripts/mina_oreburgh.py --demo              # auto-teste
    python3 dev_scripts/mina_oreburgh.py --extrai            # regera o kit da ROM
    python3 dev_scripts/mina_oreburgh.py --so-tileset        # so o tileset, sem mapa
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

# O `enfeita_cidades.py` PULA o proprio bloco de teste (`175_cidades_enfeitadas`)
# quando varre os corredores que a suite anda, e faz isso com razao: aqueles
# casos foram escritos DEPOIS do desenho dele, a partir dele. Para esta passada o
# 175 e um bloco como qualquer outro, e ignora-lo custou um caso: o T175.4 anda
# do warp 7 de Oreburgh nove celulas para a direita e nove para baixo, e uma
# pedra nova no meio da perna encurtou a rota (o jogador parou em (47,27) em vez
# de (48,22)). O nome e trocado ANTES da primeira chamada porque
# `corredores_de_teste` guarda o resultado em cache.
E.BLOCO_PROPRIO = "<nenhum bloco e proprio desta passada>"

DESTINO = f"{RAIZ}/data/tilesets/secondary/jubilife"
KIT_JSON = f"{RAIZ}/dev_scripts/mina_oreburgh_kit.json"
PLANO = f"{RAIZ}/dev_scripts/mina_oreburgh.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_Jubilife"
# os SETE layouts que dividem o gTileset_Jubilife
IRMAOS = ["EternaCity", "OreburghCity", "OreburghMine_B1F", "Route205_North",
          "Route207", "Route211_West", "Route218"]

TETO_TILES = 512
TETO_META = 512
TILE_LOCAL_0 = 384          # primeira vaga livre do tiles.png (384 tiles hoje)
META_LOCAL_0 = 387          # local 387 = id 899, primeiro dos 125 livres
MARGEM = 2
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%

# ------------------------------------------------------------------ a FUSAO
FUSAO = dict(de=7, para=6)  # a vaga 7 e esvaziada dentro da 6; ver o cabecalho

# ------------------------------------------------------------------- a FONTE
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          pri=0x286CF4, split=(512, 512, 6))
SEC_MINA = 0x286E8C          # a pedreira a ceu aberto do grupo 24 (g24m09)
SEC_FLOR = 0x286FAC          # a floresta densa (g24m04)

# ------------------------------------------------------------------ os TEMAS
# `chao` : local do metatile da FONTE cuja arte e piso (camada de baixo so).
# `movel`: local do metatile da FONTE cuja arte vira peca SOLIDA de uma celula.
# `piso_min`: quantos metatiles DIFERENTES da fonte precisam usar um tile na
# camada de baixo para ele ser PISO da fonte e nunca subir para a nossa peca. O
# numero nao e chutado, e o meio do degrau medido em 08/09/2026: no `0x286E8C`
# os doze tiles de piso aparecem em 41 a 118 metatiles e o proximo tile aparece
# em 19, entao 40 fica com folga de duas vezes para os dois lados; no `0x286FAC`
# os dois tiles de piso aparecem em 26 e 28 e o proximo em 22.
MINA = dict(
    alvo="OreburghCity", sec=SEC_MINA, carimbo=268, piso_min=40,
    # a vaga 7 (livre depois da fusao) leva as paletas 6 e 10 do hack, que sao
    # as duas da pedreira e fecham em 15 cores exatas; as cinco cores escuras da
    # paleta 9, que so as pedras de basalto usam, vao para os indices vagos da
    # nossa vaga 8.
    vagas_pal={6: 7, 10: 7, 9: 8},
    chao=[
        # o metatile 7 do hack, que e o losango com UM quadrante trocado, foi
        # CORTADO desta lista: a distancia RGB media dele para o 1 e 8,7, quase
        # o piso de 8,0 que o `varia_carimbo.py` usa para recusar variante
        # invisivel, e no render lado a lado os dois sao o mesmo desenho.
        dict(nome="cascalho losango",  lp=1),
        dict(nome="areia de mina",     lp=17),
        dict(nome="laje rachada",      lp=47),
        dict(nome="areia salpicada",   lp=88),
        dict(nome="areia riscada",     lp=90),
        dict(nome="tabuado",           lp=132),
        dict(nome="cascalho amarelo",  lp=229),
        dict(nome="cascalho lascado",  lp=231),
        dict(nome="terra batida",      lp=245),
    ],
    moveis=[
        dict(nome="pedra escura",      lp=38,  quantos=8, espaco=6),
        dict(nome="pedra cinza",       lp=39,  quantos=8, espaco=6),
        dict(nome="pedra de chumbo",   lp=123, quantos=8, espaco=6),
        dict(nome="pedra clara",       lp=130, quantos=8, espaco=6),
        dict(nome="carvao",            lp=181, quantos=8, espaco=6),
        dict(nome="pedra grande",      lp=182, quantos=8, espaco=6),
        dict(nome="pedra chumbo alta", lp=238, quantos=8, espaco=6),
        dict(nome="pilha de minerio",  lp=187, quantos=6, espaco=7),
        dict(nome="minerio fino",      lp=188, quantos=6, espaco=7),
        dict(nome="minerio grosso",    lp=189, quantos=6, espaco=7),
        dict(nome="minerio partido",   lp=190, quantos=6, espaco=7),
        dict(nome="minerio miudo",     lp=191, quantos=6, espaco=7),
        dict(nome="minerio solto",     lp=179, quantos=6, espaco=7),
        dict(nome="engradado",         lp=94,  quantos=5, espaco=7),
        dict(nome="engradado escuro",  lp=101, quantos=5, espaco=7),
        dict(nome="caixote",           lp=102, quantos=5, espaco=7),
        dict(nome="viga de madeira",   lp=48,  quantos=4, espaco=9),
        dict(nome="viga deitada",      lp=57,  quantos=4, espaco=9),
        dict(nome="viga inclinada",    lp=59,  quantos=4, espaco=9),
    ],
    # PECA DE DUAS CELULAS DE ALTURA, e ela existe por desenho e por prova. Por
    # desenho: uma pedreira precisa de um matacao que se veja de longe, e o
    # matacao do hack e um bloco 2x2. Por prova: e a unica peca da rodada em que
    # a celula de CIMA continua ANDAVEL com a arte na camada de cima (o jogador
    # passa ATRAS do topo do matacao) e a de BAIXO vira solida em COVERED, que e
    # a regra 3 desta onda, e sem ela o caso 13 do auto-teste nao teria o que
    # medir.
    blocos=[
        dict(nome="matacao", topo=[45, 46], base=[53, 54], quantos=4, espaco=12),
    ],
)
FLORESTA = dict(
    alvo="EternaCity", sec=SEC_FLOR, carimbo=1, piso_min=24,
    vagas_pal={8: 11},              # so o tronco caido, nos indices vagos da 11
    chao=[],                        # o chao de Eterna e todo NOSSO (ver abaixo)
    moveis=[
        dict(nome="tronco caido",     lp=53, quantos=6, espaco=9),
        dict(nome="galho caido",      lp=54, quantos=6, espaco=9),
    ],
    blocos=[],
)
TEMAS = {"OreburghCity": MINA, "EternaCity": FLORESTA}

# CHAO NOSSO de Eterna: metatiles do PRIMARIO com o atributo IGUAL ao do
# metatile 1, arte diferente e nenhum uso em `EternaCity`. Custam ZERO.
CHAO_NOSSO_ETERNA = [
    # Os metatiles 465 e 481, que a primeira versao desta lista usava, foram
    # CORTADOS depois de olhar o render: os dois sao grama CLARA com uma costura
    # horizontal, e em mancha eles viram retangulo listrado no meio do gramado,
    # que e colcha de retalho e nao grama. O que ficou e o que tem contorno
    # organico: a grama com flor miuda e os tufos.
    dict(nome="grama florida", mt=473),
    dict(nome="tufo claro",    mt=462),
    dict(nome="tufo torto",    mt=463),
    dict(nome="moita baixa",   mt=31),
]
# VARIANTE POR ESPELHO, que nao custa tile nem cor: o tufo com a metade
# espelhada e outra silhueta na tela, e e assim que o proprio primario faz nos
# pares dele. Bit 0x400 ligado e as colunas trocadas, exatamente como o
# `neve_snowpoint2.py` fez com o pinheiro esguio.
ESPELHO_ETERNA = [
    dict(nome="tufo claro espelhado", mt=462),
    dict(nome="tufo torto espelhado", mt=463),
    dict(nome="moita espelhada",      mt=31),
]
# MOVEL NOSSO de Eterna: metatiles do PRIMARIO desenhados SOBRE a grama do 1.
# Os que ja estao em COVERED com comportamento zerado entram como estao; os
# outros entram como COPIA em vaga livre, com o comportamento ZERADO, porque
# comportamento e id semantico e mudar o atributo de metatile vivo de tileset
# compartilhado esta proibido.
MOVEL_NOSSO_ETERNA = [
    dict(nome="moita florida",  mt=4,   quantos=10, espaco=6),
    dict(nome="moita alta",     mt=14,  quantos=10, espaco=6),
    dict(nome="moita escura",   mt=30,  quantos=10, espaco=5),
    dict(nome="moita fechada",  mt=46,  quantos=10, espaco=5),
    dict(nome="pedra de mato",  mt=110, quantos=8,  espaco=6),
    dict(nome="pedra musgosa",  mt=120, quantos=8,  espaco=6),
    dict(nome="copa redonda",   mt=470, quantos=6,  espaco=8),
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


def _espelha4(quad):
    """Espelho horizontal de UMA camada: troca as colunas e liga o bit 0x400."""
    fora = []
    for q in (1, 0, 3, 2):
        v = quad[q]
        fora.append(0 if (v & 0x3FF) == 0 else (v ^ 0x400))
    return fora


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def indices_por_vaga(sec=None, pri=None):
    """{vaga: set de indices de cor que ALGUM pixel do tileset usa}.

    Conta o tile que cada entrada de metatile do secundario pede, seja ele do
    secundario ou do primario, porque o indice do pixel e do TILE e a cor vem da
    vaga da ENTRADA. Escrever cor nova num indice que nao aparece aqui nao muda
    o desenho de nada.
    """
    import render_maps as RM
    ts = sec or _tileset(SECUNDARIO)
    tp = pri or _tileset(PRIMARIO)
    fora = collections.defaultdict(set)
    for loc in range(len(ts["metatiles"]) // 16):
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], loc):
            if it == 0 or ip < 6:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        fora[ip].add(c)
    return fora


def plano_fusao():
    """O plano da fusao das vagas 6 e 7, medido no tileset que esta no disco.

    Devolve None quando a fusao JA foi aplicada (nenhum metatile aponta para a
    vaga de origem), o que e o que torna `--aplicar` idempotente.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    de, para = FUSAO["de"], FUSAO["para"]
    # Os metatiles e os tiles que ESTA passada grava ficam de fora da conta: sem
    # isso, rodar `--aplicar` duas vezes acharia a vaga 7 "em uso" outra vez (as
    # pecas da mina moram nela) e tentaria fundir de novo.
    usa = collections.defaultdict(set)
    for loc in range(min(len(ts["metatiles"]) // 16, META_LOCAL_0)):
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], loc):
            if it and it < len(tp["tiles"]) + TILE_LOCAL_0:
                usa[ip].add(it)
    if not usa[de]:
        return None
    if usa[de] & usa[para]:
        raise SystemExit("a fusao %d -> %d exige que nenhum tile seja usado nas "
                         "duas vagas, e %d sao: %s"
                         % (de, para, len(usa[de] & usa[para]),
                            sorted(usa[de] & usa[para])[:8]))
    for vaga in (de, para):
        do_pri = sorted(t for t in usa[vaga] if t < len(tp["tiles"]))
        if do_pri:
            raise SystemExit("a vaga %d pinta %d tiles do PRIMARIO (%s) e por "
                             "isso nao pode ser reindexada" % (vaga, len(do_pri),
                                                               do_pri[:6]))
    # nenhum metatile do primario pode pedir tile do secundario
    for m in range(len(tp["metatiles"]) // 16):
        for (it, fh, fv, ip) in RM.entradas_metatile(tp["metatiles"], m):
            if it >= len(tp["tiles"]):
                raise SystemExit("o metatile %d do primario pede o tile %d do "
                                 "secundario; a fusao mexeria no primario"
                                 % (m, it))
    # tile usado com uma TERCEIRA vaga tambem esta proibido
    for vaga in (de, para):
        for outra, tiles in usa.items():
            if outra in (de, para):
                continue
            if tiles & usa[vaga]:
                raise SystemExit("tile usado na vaga %d e tambem na %d"
                                 % (vaga, outra))

    def cores(vaga):
        fora = {}
        for it in sorted(usa[vaga]):
            for linha in RM.resolver_tile(tp, ts, it):
                for c in linha:
                    if c:
                        fora[c] = tuple(ts["paletas"][vaga][c])
        return fora

    c_de, c_para = cores(de), cores(para)
    nova = dict(c_para)                     # a vaga de destino nao se mexe
    remap = {}
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
        # cor que ja mora no MESMO indice fica onde esta: e o que faz o
        # remapeamento tocar so quatro dos nove indices da vaga 7.
        alvo = idx if idx in livres else livres[0]
        livres.remove(alvo)
        nova[alvo] = cor
        remap[idx] = alvo
    paleta = [list(ts["paletas"][para][0])] + \
             [list(nova.get(i, ts["paletas"][para][i])) for i in range(1, 16)]
    for i in range(1, 16):
        if i not in nova:
            paleta[i] = [0, 0, 0]
    return dict(de=de, para=para, remap={str(k): v for k, v in remap.items()},
                tiles=sorted(usa[de]), paleta=paleta,
                cores_de=len(c_de), cores_para=len(c_para), cores=len(nova))


# ---------------------------------------------------------------- a EXTRACAO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb(ts, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits deslocados TRES
    casas, nao esticados para 0..255.

    A conta importa e foi medida em 08/09/2026. As duas contas dao o MESMO
    cinco-bits depois que o `gbagfx` reconverte o `.pal` para `.gbapal`, entao a
    cor dentro da ROM e a mesma nas duas; o que muda e o numero que fica escrito
    no `.pal` e, com ele, o pixel de todo render de conferencia. Todo `.pal` do
    `gTileset_Jubilife` esta na conta de deslocar (176 = 22 << 3, 216 = 27 << 3),
    e o `ferramentas/prova_extracao.py`, que e o portao da extracao, tambem. Com
    a conta de esticar, a cor importada saia 4 a 7 pontos acima da cor da ROM em
    cada canal e a prova de "pixel identico" media 4.055 pixels diferentes de
    5.248. E a mesma conta de `render_hack.cor` e de `extrai_tileset.cor`."""
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def vagas_livres(fusao):
    """{vaga: [indices de cor que NENHUM pixel nosso usa]}.

    Os tiles e metatiles que ESTA passada grava sao ignorados de proposito, para
    que rodar `--extrai` depois de `--aplicar` de o mesmo kit.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    usados = collections.defaultdict(set)
    for loc in range(min(len(ts["metatiles"]) // 16, META_LOCAL_0)):
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], loc):
            if it == 0 or ip < 6:
                continue
            if it >= len(tp["tiles"]) + TILE_LOCAL_0:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        usados[ip].add(c)
    fora = {}
    for vaga in range(6, 13):
        if fusao and vaga == fusao["de"]:
            fora[vaga] = list(range(1, 16))         # a fusao esvazia esta vaga
            continue
        if fusao and vaga == fusao["para"]:
            continue                                # cheia depois da fusao
        fora[vaga] = [i for i in range(1, 16) if i not in usados[vaga]]
    return fora


def extrai():
    """Regera `mina_oreburgh_kit.json` a partir da ROM privada do Light Platinum.

    So roda na maquina que tem `fontes-mapas/romhacks/`. O que sai daqui e o
    asset CONVERTIDO (tiles em nibbles, ja reindexados para a vaga de destino, e
    paleta em RGB), nunca a ROM.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("nao achei fontes-mapas/romhacks: --extrai so roda na "
                         "maquina que tem as ROMs. O kit ja extraido esta em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402

    pasta = os.path.join(ferr, LP["slug"])
    gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
    caminho = os.path.join(pasta, gba)
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    if md5 != LP["md5"]:
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s"
                         % (gba, md5, LP["md5"]))
    r = Rom(caminho)
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = LP["split"]
    t1 = r.parse_tileset(LP["pri"])
    if t1 is None:
        raise SystemExit("o primario 0x%X do hack nao abriu" % LP["pri"])

    fusao = plano_fusao()
    livres = vagas_livres(fusao)

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}
    pecas, chaos = [], {}
    for nome_tema, T in sorted(TEMAS.items()):
        t2 = r.parse_tileset(T["sec"])
        if t2 is None:
            raise SystemExit("o secundario 0x%X nao abriu" % T["sec"])
        tag = "%X" % T["sec"]
        pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}

        def ents_de(local):
            return list(struct.unpack_from("<8H", t2["meta"], local * 16))

        # O CHAO DA FONTE, por evidencia e nao por constante decorada: sao os
        # tiles da camada de baixo das pecas que ESTE kit importa como piso,
        # mais todo tile com os MESMOS 64 nibbles de um deles.
        alvo_px, chao = [], set()
        for c in T["chao"]:
            for v in ents_de(c["lp"])[:4]:
                idx = v & 0x3FF
                if idx >= r.n_tiles_pri:
                    li = idx - r.n_tiles_pri
                    chao.add(li)
                    px = _nibbles(t2["tiles"], li)
                    if px not in alvo_px:
                        alvo_px.append(px)
        for k in range(len(t2["tiles"]) // 32):
            if _nibbles(t2["tiles"], k) in alvo_px:
                chao.add(k)
        # SEGUNDA ASSINATURA, e ela e que pega o piso que este kit NAO importa
        # como variante: tile que aparece na camada de baixo de muitos metatiles
        # DIFERENTES da fonte e piso dela, porque piso e o que se repete debaixo
        # de tudo. Arte de peca aparece em um ou dois.
        quantos = collections.Counter()
        n_meta = len(t2["meta"]) // 16
        for loc in range(n_meta):
            for v in {x & 0x3FF for x in struct.unpack_from("<8H", t2["meta"],
                                                            loc * 16)[:4]}:
                if v >= r.n_tiles_pri:
                    quantos[v - r.n_tiles_pri] += 1
        chao |= {k for k, n in quantos.items() if n >= T["piso_min"]}
        chaos[tag] = sorted(chao)

        def branco(v):
            """A entrada aponta para um tile 8x8 SEM UM PIXEL aceso?

            O `0x6001` que o engradado da pedreira traz na camada de cima e o
            tile 1 do primario do hack, e ele e todo transparente. Tratar isso
            como camada de cima cheia deixaria a peca VAZIA: o engradado saiu
            branco na primeira extracao desta rodada e foi assim que apareceu.
            """
            idx = v & 0x3FF
            if not idx:
                return True
            px = (_nibbles(t1["tiles"], idx) if idx < r.n_tiles_pri
                  else _nibbles(t2["tiles"], idx - r.n_tiles_pri))
            return not any(c for linha in px for c in linha)

        def guarda(v, vaga_destino):
            # A CHAVE DO TILE LEVA A PALETA DE ORIGEM, e isso nao e detalhe: o
            # engradado claro e o escuro da pedreira sao o MESMO desenho 8x8
            # pintado com as paletas 6 e 10 do hack. Com a chave sem a paleta os
            # dois viravam a mesma vaga nossa e o segundo apagava o primeiro (o
            # engradado escuro saiu igual ao claro na segunda extracao desta
            # rodada). Duas paletas de origem, duas vagas nossas.
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            lado, li = ("p", idx) if idx < r.n_tiles_pri else ("s", idx - r.n_tiles_pri)
            ch = "%s:%s:%d:%d" % (tag, lado, li, ip)
            px = _nibbles(t1["tiles"] if lado == "p" else t2["tiles"], li)
            if tiles_vaga.setdefault(ch, vaga_destino) != vaga_destino:
                raise SystemExit("o tile %s foi pedido nas vagas %d e %d"
                                 % (ch, tiles_vaga[ch], vaga_destino))
            tiles_px[ch] = px
            origem = pal[(v >> 12) & 0xF]
            tiles_cor.setdefault(ch, set())
            for linha in px:
                for c in linha:
                    if c:
                        tiles_cor[ch].add(tuple(origem[c]))
            return ch

        blocos = []
        for b in T.get("blocos") or []:
            for papel2, lst in (("topo", b["topo"]), ("base", b["base"])):
                for k, loc in enumerate(lst):
                    blocos.append(dict(nome="%s %s %d" % (b["nome"], papel2, k),
                                       lp=loc))
        for papel, lista in (("chao", T["chao"]), ("movel", T["moveis"] + blocos)):
            for p in lista:
                ents = ents_de(p["lp"])
                attr = struct.unpack_from("<H", t2["attr"], p["lp"] * 2)[0]
                baixo, cima = ents[:4], ents[4:]
                # QUADRANTE DE BAIXO SOBE quando o de cima esta vazio (regra do
                # porto_canalave.py); quadrante que e chao da fonte, ou que a
                # fonte pinta com paleta que este kit nao importa, e DESCARTADO.
                uniforme = len({v & 0x3FF for v in baixo}) == 1
                usadas = []
                for q in range(4):
                    vazio_em_cima = branco(cima[q])
                    v = baixo[q] if vazio_em_cima else cima[q]
                    de_baixo = vazio_em_cima
                    if not (v & 0x3FF):
                        usadas.append(None)
                        continue
                    ip = (v >> 12) & 0xF
                    idx = v & 0x3FF
                    li = idx - r.n_tiles_pri
                    if de_baixo and papel == "movel" and (
                            uniforme or (idx >= r.n_tiles_pri and li in chao)):
                        usadas.append(None)
                        continue
                    if ip not in T["vagas_pal"]:
                        if papel == "chao":
                            raise SystemExit("%s: o metatile %d usa a paleta %d, "
                                             "fora do kit" % (p["nome"], p["lp"], ip))
                        usadas.append(None)
                        continue
                    usadas.append(guarda(v, T["vagas_pal"][ip]))
                if papel == "chao":
                    # o chao entra INTEIRO na camada de baixo, e a de cima fica
                    # vazia: camada de cima em celula andavel com layerType
                    # NORMAL desenha ACIMA do jogador.
                    if any(v & 0x3FF for v in cima):
                        raise SystemExit("%s: a peca de chao %d tem camada de "
                                         "cima" % (p["nome"], p["lp"]))
                    if len({v & 0x3FF for v in baixo}) < 2:
                        raise SystemExit("%s: o metatile %d repete o mesmo tile "
                                         "nos quatro quadrantes, e por isso e "
                                         "chao liso da fonte, nao arte"
                                         % (p["nome"], p["lp"]))
                elif not any(usadas):
                    raise SystemExit("%s: o metatile %d nao sobrou com nenhum "
                                     "quadrante de arte" % (p["nome"], p["lp"]))
                pecas.append(dict(tema=nome_tema, papel=papel, nome=p["nome"],
                                  lp=p["lp"], tag=tag, attr=attr,
                                  ents=[(baixo[q] if branco(cima[q]) else cima[q])
                                        for q in range(4)],
                                  usadas=usadas, baixo=baixo, cima=cima))

    # -------------------------------------------------- as paletas de destino
    ts_nosso = _tileset(SECUNDARIO)
    por_vaga = collections.defaultdict(set)
    for ch, vaga in tiles_vaga.items():
        por_vaga[vaga] |= tiles_cor[ch]
    paletas, indice = {}, {}
    for vaga, cores in sorted(por_vaga.items()):
        vagos = livres.get(vaga) or []
        cores = sorted(cores)
        if len(cores) > len(vagos):
            raise SystemExit("a vaga %d tem %d indices livres (%s) e o kit pede "
                             "%d cores" % (vaga, len(vagos), vagos, len(cores)))
        base = [list(c) for c in ts_nosso["paletas"][vaga]]
        if fusao and vaga == fusao["de"]:
            base = [base[0]] + [[0, 0, 0]] * 15
        for k, c in enumerate(cores):
            base[vagos[k]] = list(c)
            indice[(vaga, c)] = vagos[k]
        paletas[str(vaga)] = base

    # REINDEXA cada nibble para a tabela nova. A cor 0 continua 0 e nenhuma cor
    # e aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, so em
    # outro indice, entao o pixel sai identico ao da ROM.
    saida_tiles = {}
    for nome_tema, T in sorted(TEMAS.items()):
        t2 = r.parse_tileset(T["sec"])
        tag = "%X" % T["sec"]
        pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}
        for p in pecas:
            if p["tag"] != tag:
                continue
            for q in range(4):
                ch = p["usadas"][q]
                if ch is None:
                    continue
                v = p["ents"][q]
                ip = int(ch.split(":")[3])
                vaga = T["vagas_pal"][ip]
                origem = pal[ip]
                px = tiles_px[ch]
                saida_tiles[ch] = [[0 if c == 0 else indice[(vaga, tuple(origem[c]))]
                                    for c in linha] for linha in px]

    dados = dict(
        fonte=dict(hack=LP["hack"], autor=LP["autor"], base=LP["base"],
                   arquivo=gba, md5=md5, pri="0x%X" % LP["pri"],
                   sec_mina="0x%X" % SEC_MINA, sec_floresta="0x%X" % SEC_FLOR,
                   split=list(LP["split"]), n_tiles_pri=r.n_tiles_pri),
        fusao=fusao, vagas_livres={str(k): v for k, v in livres.items()},
        paletas=paletas, tiles=saida_tiles, tiles_vaga=tiles_vaga,
        chao_da_fonte=chaos, pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d pecas, vagas %s"
          % (os.path.relpath(KIT_JSON, RAIZ), len(saida_tiles), len(pecas),
             {k: len(v) for k, v in por_vaga.items()}))
    for vaga, cores in sorted(por_vaga.items()):
        print("  vaga %2d: %2d cores nos indices %s"
              % (vaga, len(cores), [indice[(vaga, c)] for c in sorted(cores)]))
    return 0


# --------------------------------------------------------------- o KIT em disco
ORDEM = ["OreburghCity", "EternaCity"]   # ordem FIXA de alocacao de vaga

def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def chao_nosso(alvo):
    """As quatro entradas da camada de BAIXO do carimbo daquela cidade, mais o
    atributo dele. E o chao que todo movel pousa em cima."""
    import render_maps as RM
    tp = _tileset(PRIMARIO)
    mt = TEMAS[alvo]["carimbo"]
    ents = list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))
    if any(v & 0x3FF for v in ents[4:]):
        raise SystemExit("o carimbo %d ja usa a camada de cima" % mt)
    return ents[:4], G._attrs(PRIMARIO)[mt]


def desenha_kit(alvos=None):
    """(fusao, tiles_novos, metas, attrs, carimbos), sem escrever em disco.

    A ALOCACAO E SEMPRE A DE `ORDEM` INTEIRA, e nao a do subconjunto pedido: a
    vaga de tile e a de metatile de cada peca precisam ser as MESMAS quer o
    commit seja o de Oreburgh, o de Eterna ou os dois. Com a alocacao seguindo o
    subconjunto, aplicar so `EternaCity` reescrevia por cima das vagas de
    Oreburgh. Quem filtra por mapa e o `roda`, que so planeja e grava o
    `map.bin` dos alvos pedidos.
    """
    alvos = list(ORDEM)
    dados = kit()
    meta_jub = _ler("metatiles.bin")
    attr_jub = _ler("metatile_attributes.bin")
    ap = G._attrs(PRIMARIO)
    import render_maps as RM
    tp = _tileset(PRIMARIO)

    por_peca = {(p["tema"], p["papel"], p["nome"]): p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]
    metas, attrs = {}, {}
    proximo_meta = [META_LOCAL_0]
    carimbos = {a: dict(chao=[], moveis=[], blocos=[]) for a in ORDEM}

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
        return 512 + local

    def entrada(p, q):
        """A entrada NOSSA para o quadrante q da peca: mesmo tile, vaga nova,
        vaga de paleta nova, e os bits de espelho da fonte preservados."""
        ch = p["usadas"][q]
        if ch is None:
            return None
        v = p["ents"][q]
        alvo_pal = TEMAS[p["tema"]]["vagas_pal"][int(ch.split(":")[3])]
        return ((v & 0x0C00) | (512 + vaga(ch)) | (alvo_pal << 12))

    for alvo in alvos:
        T = TEMAS[alvo]
        base, attr_chao = chao_nosso(alvo)
        # ---------------------------------------------------------- 1. CHAO
        por_nome = {}
        for c in T["chao"]:
            p = por_peca[(alvo, "chao", c["nome"])]
            ents = [entrada(p, q) for q in range(4)]
            if any(e is None for e in ents):
                raise SystemExit("%s: quadrante vazio em peca de chao" % c["nome"])
            gid = poe(ents + [0, 0, 0, 0], attr_chao)
            por_nome[c["nome"]] = ents
            carimbos[alvo]["chao"].append(dict(nome=c["nome"], mt=gid,
                                               importado=True))
        if alvo == "EternaCity":
            # o chao de Eterna NAO gasta vaga nenhuma: sao metatiles do PRIMARIO
            # com o atributo IGUAL, bit a bit, ao do metatile 1.
            for c in CHAO_NOSSO_ETERNA:
                if ap[c["mt"]] != attr_chao:
                    raise SystemExit("o metatile %d tem atributo 0x%04X e o "
                                     "carimbo tem 0x%04X" % (c["mt"], ap[c["mt"]],
                                                             attr_chao))
                carimbos[alvo]["chao"].append(dict(nome=c["nome"], mt=c["mt"],
                                                   nosso=True))
            for c in ESPELHO_ETERNA:
                if ap[c["mt"]] != attr_chao:
                    raise SystemExit("o metatile %d tem atributo 0x%04X e o "
                                     "carimbo tem 0x%04X" % (c["mt"], ap[c["mt"]],
                                                             attr_chao))
                ents = list(struct.unpack_from("<8H", tp["metatiles"],
                                               c["mt"] * 16))
                if ents[:4] != base:
                    raise SystemExit("o metatile %d nao esta desenhado sobre a "
                                     "grama do carimbo" % c["mt"])
                gid = poe(list(base) + _espelha4(ents[4:]), attr_chao)
                carimbos[alvo]["chao"].append(dict(nome=c["nome"], mt=gid,
                                                   espelho_de=c["mt"]))
        # -------------------------------------------------------- 2. MOVEIS
        for m in T["moveis"]:
            p = por_peca[(alvo, "movel", m["nome"])]
            cima = [entrada(p, q) or 0 for q in range(4)]
            if not any(cima):
                raise SystemExit("%s: peca sem arte" % m["nome"])
            # comportamento ZERADO (regra 5: nenhum id semantico e importado) e
            # layerType COVERED, que poe as duas camadas ABAIXO do sprite.
            gid = poe(list(base) + cima, 0x1000)
            carimbos[alvo]["moveis"].append(
                dict(nome=m["nome"], mt=gid, quantos=m["quantos"],
                     espaco=m["espaco"], importado=True))
        for b in (T.get("blocos") or []):
            ids = {}
            for papel2, lst, attr_peca in (("topo", b["topo"], attr_chao),
                                           ("base", b["base"], 0x1000)):
                fora = []
                for k, _loc in enumerate(lst):
                    p = por_peca[(alvo, "movel", "%s %s %d" % (b["nome"], papel2, k))]
                    cima = [entrada(p, q) or 0 for q in range(4)]
                    if not any(cima):
                        raise SystemExit("%s: metade sem arte" % b["nome"])
                    fora.append(poe(list(base) + cima, attr_peca))
                ids[papel2] = fora
            carimbos[alvo]["blocos"].append(
                dict(nome=b["nome"], topo=ids["topo"], base=ids["base"],
                     quantos=b["quantos"], espaco=b["espaco"]))
        if alvo == "EternaCity":
            for m in MOVEL_NOSSO_ETERNA:
                ents = list(struct.unpack_from("<8H", tp["metatiles"],
                                               m["mt"] * 16))
                if ents[:4] != base:
                    raise SystemExit("o metatile %d nao esta desenhado sobre a "
                                     "grama do carimbo" % m["mt"])
                a = ap[m["mt"]]
                if a == 0x1000:
                    mt = m["mt"]        # ja e COVERED com comportamento zerado
                else:
                    mt = poe(ents, 0x1000)
                carimbos[alvo]["moveis"].append(
                    dict(nome=m["nome"], mt=mt, quantos=m["quantos"],
                         espaco=m["espaco"], importado=False, copia_de=m["mt"]))

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))
    if proximo_meta[0] > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)

    # A vaga de metatile so serve se for ENCHIMENTO do dumper ou se ja tiver
    # exatamente o que este kit escreve, e NENHUM dos sete mapas pode usar o id.
    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    usados = set()
    for nome in IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    for local, ents in metas.items():
        gid = 512 + local
        antigo = _entradas(meta_jub, local)
        if not enchimento(antigo) and antigo != ents:
            raise SystemExit("a vaga de metatile %d ja esta ocupada" % gid)
        if gid in usados and enchimento(antigo):
            raise SystemExit("algum dos sete mapas usa o metatile %d e a vaga "
                             "esta vazia" % gid)
    return plano_fusao(), tiles_novos, metas, attrs, carimbos


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
    px = novo.load()

    # ------------------------------------------------------------- a FUSAO
    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    if fusao:
        remap = {int(k): v for k, v in fusao["remap"].items()}
        for t in fusao["tiles"]:
            local = t - 512
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
    novo.save(f"{DESTINO}/tiles.png")

    for vaga, cores in sorted(dados["paletas"].items()):
        _grava_pal(int(vaga), cores)

    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


def _grava_pal(vaga, cores):
    with open(f"{DESTINO}/palettes/%02d.pal" % vaga, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))


# ------------------------------------------------------------ o ESPALHAMENTO
# A TRILHA e o esqueleto de custo minimo entre as soleiras das portas, engordado
# e desgastado na borda; as BOLHAS sao manchas organicas crescidas por frente de
# onda. As duas ideias, e o codigo delas, vem do `neve_snowpoint2.py`, que e a
# passada em que elas foram medidas e provadas.
ESPALHA = {
    "OreburghCity": dict(
        trilha=["cascalho losango", "areia de mina", "cascalho lascado"],
        bolhas=[
            dict(grupo=["laje rachada"],                    quantas=8,  tam=(5, 11)),
            dict(grupo=["cascalho amarelo"],                quantas=8,  tam=(6, 13)),
            dict(grupo=["terra batida"],                    quantas=9,  tam=(6, 13)),
            dict(grupo=["areia salpicada", "areia riscada"], quantas=10, tam=(6, 14)),
            dict(grupo=["tabuado"],                         quantas=4,  tam=(2, 4)),
        ],
        borda_trilha=75),
    "EternaCity": dict(
        trilha=["grama florida"],
        bolhas=[
            dict(grupo=["tufo claro", "tufo claro espelhado"],  quantas=4, tam=(8, 16)),
            dict(grupo=["tufo torto", "tufo torto espelhado"],  quantas=4, tam=(8, 16)),
            dict(grupo=["moita baixa", "moita espelhada"],      quantas=4, tam=(7, 14)),
            dict(grupo=["grama florida"],                       quantas=5, tam=(9, 18)),
        ],
        borda_trilha=65),
}
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


def bolhas(livres, spec, perto_solido):
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
def plano_mapa(alvo, carimbos, base=None):
    """(L, W, H, v, escritas, contas) para UM mapa."""
    T = TEMAS[alvo]
    CARIMBO = T["carimbo"]
    d, L, W, H, v0 = G.grade(alvo)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    nossos_chaos = {c["mt"] for c in carimbos[alvo]["chao"]}
    familia = {CARIMBO} | nossos_chaos
    elev = collections.Counter(
        (c >> 12) & 0xF for c in v
        if (c & 0x3FF) == CARIMBO and not ((c >> 10) & 3)).most_common(1)[0][0]

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    elegivel = {(i % W, i // W) for i in range(W * H)
                if andavel(i) and (v[i] & 0x3FF) in familia
                and ((v[i] >> 12) & 0xF) == elev
                and beh(v[i] & 0x3FF) not in AG}

    escritas = {}
    trilha, portas = area_trilha(v, W, H, d, elegivel)

    # ------------------------------------------------------------- 1. MOVEIS
    # Eles vem ANTES da mancha de proposito, e a razao esta medida em Snowpoint:
    # movel posto no carimbo tira uma celula do numerador E do denominador da
    # regua; movel posto em cima de uma mancha tira so do denominador, o que
    # PIORA a conta.
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(alvo, v, W, H, d)
    for idx, _a, _n in E.carrega_plano().get(alvo, {}).get("celulas", []):
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
        """Solidifica (x,y) e devolve True se os DOIS portoes deixarem.

        O portao roda NA HORA e nao so no fim: se solidificar esta celula tirar
        do alcance a pe qualquer OUTRA celula, ou partir um pedaco de chao em
        dois, a escrita e desfeita e o gerador segue.
        """
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

    # ------ 1a. BLOCO DE DUAS CELULAS DE ALTURA, antes da mobilia de uma
    # celula, porque ele precisa de um retangulo 2x2 inteiro e a mobilia solta
    # nao pode ter comido metade dele. A linha de CIMA continua ANDAVEL (a arte
    # dela mora na camada de cima, o jogador passa atras) e por isso nao entra
    # em `novos_solidos` nem no portao de alcance; a de BAIXO vira solida.
    conta_bloco = collections.Counter()
    por_bloco = []
    for b in carimbos[alvo].get("blocos") or []:
        for x, y in ordem_cel:
            if conta_bloco[b["nome"]] >= b["quantos"]:
                break
            cels = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if any(not livre(cx, cy) for cx, cy in cels):
                continue
            if any(max(abs(x - px), abs(y - py)) < b["espaco"] for px, py in por_bloco):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            # o matacao encosta em solido: pedra grande no meio do patio aberto
            # le como erro de mapa, e na fonte ela sempre nasce colada no barranco
            if not any(0 <= cx + dx < W and 0 <= cy + dy < H
                       and ((aplicado[(cy + dy) * W + cx + dx] >> 10) & 3)
                       for cx, cy in cels for dx, dy in N4):
                continue
            topo = [(x, y), (x + 1, y)]
            for k, (cx, cy) in enumerate(topo):
                j = cy * W + cx
                escritas[j] = (aplicado[j] & 0xFC00) | b["topo"][k]
                aplicado[j] = escritas[j]
            ok = True
            for k, (cx, cy) in enumerate([(x, y + 1), (x + 1, y + 1)]):
                if not tenta_solidificar(cx, cy, b["base"][k]):
                    ok = False
                    break
            if not ok:
                for cx, cy in cels:
                    j = cy * W + cx
                    if j in escritas and (cx, cy) not in novos_solidos:
                        del escritas[j]
                        aplicado[j] = v[j]
                for cx, cy in [(x, y + 1), (x + 1, y + 1)]:
                    if (cx, cy) in novos_solidos:
                        novos_solidos.remove((cx, cy))
                        postos.remove((cx, cy))
                        del escritas[cy * W + cx]
                        aplicado[cy * W + cx] = v[cy * W + cx]
                continue
            por_bloco += cels
            postos += topo
            conta_bloco[b["nome"]] += 1

    lista = carimbos[alvo]["moveis"]
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
    esp = ESPALHA[alvo]
    por_nome = {c["nome"]: c["mt"] for c in carimbos[alvo]["chao"]}
    conta_mancha = collections.Counter()

    def pintavel(p):
        i = p[1] * W + p[0]
        return (p in elegivel and i not in escritas
                and (aplicado[i] & 0x3FF) == CARIMBO)

    def pinta(p, nomes):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | por_nome[nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    for p in sorted(x for x in desgasta(trilha, esp["borda_trilha"]) if pintavel(x)):
        pinta(p, esp["trilha"])
    livres = {p for p in elegivel if pintavel(p)}

    def perto_solido(p):
        return any(0 <= p[0] + dx < W and 0 <= p[1] + dy < H
                   and ((aplicado[(p[1] + dy) * W + p[0] + dx] >> 10) & 3)
                   for dx, dy in N4)

    for nomes, corpo in bolhas(livres, esp["bolhas"], perto_solido):
        for p in sorted(corpo):
            pinta(p, nomes)

    # -------------------------------------------------------------- PORTOES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (alvo, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel"
                             % (alvo, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (alvo, "; ".join(queixas)))
    contas = dict(trilha=len(trilha), moveis=dict(conta_mov),
                  blocos=dict(conta_bloco), manchas=dict(conta_mancha),
                  solidos=len(novos_solidos), portas=len(portas))
    return L, W, H, v, escritas, contas


def regua(v, W, H, L, escritas=None):
    """(carimbo dominante em %, celulas andaveis a pe, id do carimbo), como a
    `regua_cidades.py` conta."""
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
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


def base_de(alvo, guardado):
    """A grade como esta no disco, so tirando o que ESTA passada escreveu.

    Sem isso a idempotencia morre, e o motivo esta no ESTADO.md: `EternaCity` e
    `OreburghCity` JA tem desenho do `enfeita_cidades.py` em cima, com plano
    proprio, e planejar sobre um mapa ja enfeitado nao volta ao mesmo lugar. A
    saida e a do `porto_canalave.py`: planejar sobre a base LIMPA desta passada
    (o disco menos o que esta passada gravou) e escrever por cima do disco.
    """
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(alvos, aplicar):
    fusao, tiles_novos, metas, attrs, carimbos = desenha_kit(alvos)
    print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d)%s"
          % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
             TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
             max(metas), 512 + min(metas), 512 + max(metas),
             "" if not fusao else "; fusao da vaga %d na %d (%d cores)"
             % (fusao["de"], fusao["para"], fusao["cores"])))
    if aplicar:
        grava_tileset(fusao, tiles_novos, metas, attrs)
    guardado = carrega_plano()
    for alvo in alvos:
        base = base_de(alvo, guardado)
        L, W, H, v, escritas, contas = plano_mapa(alvo, carimbos, base)
        a, na, ida = regua(v, W, H, L)
        b, nb, idb = regua(v, W, H, L, escritas)
        print("%s: trilha %d, mancha %d, %d celulas solidificadas, %d celulas "
              "mudadas" % (alvo, contas["trilha"],
                           sum(contas["manchas"].values()), contas["solidos"],
                           len(escritas)))
        print("  mancha: " + ", ".join("%s x%d" % kv
                                       for kv in sorted(contas["manchas"].items())))
        print("  movel:  " + ", ".join("%s x%d" % kv
                                       for kv in sorted(contas["moveis"].items())))
        if contas["blocos"]:
            print("  bloco:  " + ", ".join("%s x%d" % kv
                                           for kv in sorted(contas["blocos"].items())))
        print("  regua: carimbo %d com %.1f%% de %d celulas ANTES; carimbo %d "
              "com %.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
        if aplicar:
            saida = list(v)
            for i, val in escritas.items():
                saida[i] = val
            with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
                f.write(struct.pack("<%dH" % len(saida), *saida))
            guardado[alvo] = {"celulas": [[i, v[i], escritas[i]]
                                          for i in sorted(escritas)]}
    if aplicar:
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("aplicado")
    return 0


def desfaz(alvos):
    guardado = carrega_plano()
    for alvo in alvos:
        if alvo not in guardado:
            print("%s: nada a desfazer" % alvo)
            continue
        d, L, W, H, v = G.grade(alvo)
        v, n = list(v), 0
        for idx, antigo, novo in guardado[alvo]["celulas"]:
            if v[idx] == novo:
                v[idx] = antigo
                n += 1
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(v), *v))
        guardado.pop(alvo)
        print("%s: desfeitas %d celulas" % (alvo, n))
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    return 0


# ------------------------------------------------------------------ conferencia
def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def confere(alvos, fusao, tiles_novos, metas, attrs, carimbos, planos):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela e chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que
    tem que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida so no caminho feliz nao e regra, e prova positiva sem
    par negativo nao e prova.
    """
    mau = []
    dados = kit()
    ap = G._attrs(PRIMARIO)
    import render_maps as RM
    tp = _tileset(PRIMARIO)
    ts = _tileset(SECUNDARIO)

    def atributo(mt_id):
        """Atributo de um metatile, com o kit desta rodada valendo por cima."""
        if mt_id >= 512:
            local = mt_id - 512
            if local in attrs:
                return attrs[local]
            asec = G._attrs(SECUNDARIO)
            return asec[local] if local < len(asec) else 0
        return ap[mt_id] if mt_id < len(ap) else 0

    def entradas(mt_id):
        if mt_id >= 512 and (mt_id - 512) in metas:
            return list(metas[mt_id - 512])
        tset, loc = (tp, mt_id) if mt_id < 512 else (ts, mt_id - 512)
        return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))

    def px_de(mt_id):
        """Os 256 pixels RGB do metatile, com o kit desta rodada valendo."""
        from PIL import Image
        im = Image.new("RGB", (16, 16), tp["paletas"][0][0])
        p = im.load()
        ent = entradas(mt_id)
        for cam in (0, 1):
            for q in range(4):
                val = ent[cam * 4 + q]
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if not idx:
                    continue
                vaga = idx - len(tp["tiles"])
                if vaga in tiles_novos:
                    tile = tiles_novos[vaga]
                else:
                    tile = RM.resolver_tile(tp, ts, idx)
                if tile is None:
                    continue
                cores = (dados["paletas"].get(str(ip))
                         or (tp if ip < 6 else ts)["paletas"].get(ip))
                if cores is None:
                    continue
                RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                                 [tuple(c) for c in cores],
                                 bool(val & 0x400), bool(val & 0x800))
        return list(im.get_flattened_data())

    # ------------------------------------------------------------ 1. orcamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    livres = dados["vagas_livres"]
    for vaga, cores in sorted(dados["paletas"].items()):
        if not 6 <= int(vaga) <= 12:
            mau.append("a vaga %s nao e de secundario" % vaga)
        antigo = ts["paletas"][int(vaga)]
        vagos = set(livres.get(vaga) or [])
        for i in range(1, 16):
            if tuple(cores[i]) != tuple(antigo[i]) and i not in vagos:
                # a vaga que a fusao esvaziou pode ser reescrita inteira
                if not (fusao and int(vaga) == fusao["de"]):
                    mau.append("a vaga %s mudou a cor do indice %d, que algum "
                               "pixel nosso usa" % (vaga, i))

    # -------------------------------------------------------------- 2. a fusao
    if fusao:
        cores = [tuple(c) for c in fusao["paleta"][1:] if tuple(c) != (0, 0, 0)]
        if len(cores) > 15:
            mau.append("a fusao pede %d cores" % len(cores))
        if len(set(cores)) != len(cores):
            mau.append("a fusao gasta duas vagas com a MESMA cor")

    # -------- 3. CHAO novo: atributo identico ao do carimbo e camada de cima
    #             VAZIA (camada de cima em celula andavel NORMAL tapa o jogador)
    ids_chao, ids_movel, ids_topo, ids_base = {}, {}, {}, {}
    for alvo in alvos:
        _base, attr_chao = chao_nosso(alvo)
        for c in carimbos[alvo]["chao"]:
            ids_chao[c["mt"]] = alvo
            if atributo(c["mt"]) != attr_chao:
                mau.append("o chao %d tem atributo 0x%04X e o carimbo de %s tem "
                           "0x%04X" % (c["mt"], atributo(c["mt"]), alvo, attr_chao))
            # CAMADA DE CIMA EM CHAO ANDAVEL. Com layerType NORMAL ela vai
            # para o BG1, que desenha ACIMA do sprite. Cascalho IMPORTADO por
            # cima do jogador e defeito, e por isso toda peca de chao vinda do
            # hack entra com a camada de cima vazia. Ja o TUFO DE GRAMA nosso
            # (os metatiles 462, 463 e 31 do primario e os espelhos deles)
            # desenha em cima de proposito, que e o "jogador atras do mato" que
            # o jogo base faz desde sempre; o que ele nao pode e tapar o
            # jogador INTEIRO, que e a conta do E3 do `mapas_qa.py`.
            cima = [e for e in entradas(c["mt"])[4:] if e & 0x3FF]
            if cima and c.get("importado"):
                mau.append("o chao importado %d usa a camada de cima" % c["mt"])
            if cima and (atributo(c["mt"]) >> 12) & 0xF != 1:
                op = 0
                for e in cima:
                    vaga = (e & 0x3FF) - len(tp["tiles"])
                    op += (_opacos(tiles_novos[vaga]) if vaga in tiles_novos
                           else _opacos(RM.resolver_tile(tp, ts, e & 0x3FF)))
                if op >= 4 * 64:
                    mau.append("o chao %d tapa o jogador inteiro (E3)" % c["mt"])
        for m in carimbos[alvo]["moveis"]:
            ids_movel[m["mt"]] = alvo
        for b in carimbos[alvo].get("blocos") or []:
            for t in b["topo"]:
                ids_topo[t] = alvo
            for t in b["base"]:
                ids_base[t] = alvo

    # ------- 4. MOVEL e BASE: COVERED, comportamento zerado, e o NOSSO chao
    #            entrada por entrada na camada de baixo
    for gid, alvo in list(ids_movel.items()) + list(ids_base.items()):
        if gid < 512:
            if atributo(gid) != 0x1000:
                mau.append("o movel %d do primario nao esta em COVERED com "
                           "comportamento zerado (0x%04X)" % (gid, atributo(gid)))
            continue
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %d nao esta em COVERED" % gid)
        if a & 0xFF:
            mau.append("o movel %d importou comportamento 0x%02X da fonte"
                       % (gid, a & 0xFF))
        base, _ac = chao_nosso(alvo)
        if entradas(gid)[:4] != base:
            mau.append("o movel %d nao tem o nosso chao na camada de baixo" % gid)

    # ---- 5. TOPO de bloco: continua ANDAVEL com o atributo do chao, e a arte
    #        dele NAO pode ser 100% opaca, senao ela tapa o jogador (E3)
    for gid, alvo in ids_topo.items():
        base, attr_chao = chao_nosso(alvo)
        if atributo(gid) != attr_chao:
            mau.append("o topo de bloco %d nao herdou o atributo do chao" % gid)
        if entradas(gid)[:4] != base:
            mau.append("o topo de bloco %d nao tem o nosso chao embaixo" % gid)
        if (atributo(gid) >> 12) & 0xF != 1:
            px = 0
            for e in entradas(gid)[4:]:
                if e & 0x3FF:
                    vaga = (e & 0x3FF) - len(tp["tiles"])
                    px += (_opacos(tiles_novos[vaga]) if vaga in tiles_novos
                           else 64)
            if px >= 4 * 64:
                mau.append("o topo de bloco %d tapa o jogador inteiro (E3)" % gid)

    # ---------- 6. nenhuma variante de chao e copia pixel a pixel de outra
    for alvo in alvos:
        lista = [c["mt"] for c in carimbos[alvo]["chao"]] + [TEMAS[alvo]["carimbo"]]
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                d = sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
                        for p, q in zip(pix[a], pix[b])) / 256.0
                if d < 8.0:
                    mau.append("as variantes de chao %d e %d de %s tem distancia "
                               "%.1f, abaixo do piso de 8,0 do varia_carimbo.py: "
                               "isso e enganar a regua" % (a, b, alvo, d))

    # -------------------------------------------- 7 a 12. o plano, mapa a mapa
    for alvo in alvos:
        L, W, H, v, escritas, contas = planos[alvo]
        d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
        ev = E.eventos(d)
        CARIMBO = TEMAS[alvo]["carimbo"]
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        meus_chaos = {c["mt"] for c in carimbos[alvo]["chao"]}
        meus_moveis = {m["mt"] for m in carimbos[alvo]["moveis"]}
        meus_topos = {t for b in (carimbos[alvo].get("blocos") or []) for t in b["topo"]}
        meus_bases = {t for b in (carimbos[alvo].get("blocos") or []) for t in b["base"]}

        for i, val in escritas.items():
            x, y = i % W, i // W
            novo, velho = val & 0x3FF, v[i] & 0x3FF
            cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
            if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
                mau.append("%s: mudou ELEVACAO em (%d,%d)" % (alvo, x, y))
            if cv and not cn:
                mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                           % (alvo, x, y))
            if novo in meus_chaos or novo in meus_topos:
                if cn != cv or velho != CARIMBO:
                    mau.append("%s: chao/topo em celula errada em (%d,%d)"
                               % (alvo, x, y))
            elif novo in meus_moveis or novo in meus_bases:
                if cv or not cn:
                    mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                               % (alvo, x, y))
                if velho != CARIMBO:
                    mau.append("%s: movel fora do carimbo em (%d,%d)" % (alvo, x, y))
                if (x, y) in ev:
                    mau.append("%s: movel em cima do evento (%d,%d)" % (alvo, x, y))
            else:
                mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                           % (alvo, novo, x, y))

        # 8. (comportamento, layerType) de toda celula ANDAVEL fica igual
        for i in range(W * H):
            if (saida[i] >> 10) & 3:
                continue
            a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
            if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
                mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                           "layerType)" % (alvo, i % W, i // W))
                break

        # 9 e 10. alcance a pe e LIGACAO a pe
        ini = E.partidas(d, W, H, v)
        antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
        solid = {(i % W, i // W) for i in escritas
                 if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
        if (antes - depois) - solid:
            mau.append("%s: o alcance a pe perdeu %d celulas alem das "
                       "solidificadas: %s"
                       % (alvo, len((antes - depois) - solid),
                          sorted((antes - depois) - solid)[:6]))
        if depois - antes:
            mau.append("%s: o alcance a pe GANHOU celula" % alvo)
        mau += ["%s: %s" % (alvo, q) for q in
                ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                                solid)]

        # 11. A MANCHA NAO PODE SER ADIVINHAVEL, e o teste tem dois lados.
        #  (a) PADRAO: nenhuma projecao simples da posicao pode ADIVINHAR a peca.
        #      Medir so a paridade nao basta, e isso esta medido em Snowpoint: a
        #      conta certa e por EIXO (x, y, x+y, x-y) e por MODULO de 2 a 8,
        #      chutando dentro de cada classe de resto a peca mais comum dela,
        #      contra o chute cego da peca mais comum do mapa.
        #  (b) FORMA: mancha e BOLHA, nao sal e pimenta, e a conta e o TAMANHO
        #      MEDIO do pedaco conexo, nao quantas vizinhas cada celula tem.
        mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
                  if (val & 0x3FF) in meus_chaos}
        if len(mancha) < 120:
            mau.append("%s: so %d celulas de mancha" % (alvo, len(mancha)))
        if mancha:
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
                        mau.append("%s: saber %s mod %d adivinha a peca em %.0f%% "
                                   "das celulas contra %.0f%% do chute cego: "
                                   "virou padrao" % (alvo, rot, mod, 100 * ac,
                                                     100 * cego))
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
            if len(mancha) / pedacos < 12.0:
                mau.append("%s: a mancha media tem so %.1f celulas (%d em %d "
                           "pedacos): virou sal e pimenta, nao bolha"
                           % (alvo, len(mancha) / pedacos, len(mancha), pedacos))

        # 12. a regua tem que fechar em 20% ou menos
        b, nb, idb = regua(v, W, H, L, escritas)
        if b > TETO_REGUA:
            mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                       % (alvo, b))

        # 13. o bloco 2x2: toda BASE tem um TOPO logo acima, e as contas batem
        bases = {(i % W, i // W) for i, val in escritas.items()
                 if (val & 0x3FF) in meus_bases}
        topos = {(i % W, i // W) for i, val in escritas.items()
                 if (val & 0x3FF) in meus_topos}
        if len(bases) != len(topos):
            mau.append("%s: %d bases de bloco e %d topos" % (alvo, len(bases),
                                                             len(topos)))
        for x, y in bases:
            if (x, y - 1) not in topos:
                mau.append("%s: a base de bloco em (%d,%d) esta sem topo"
                           % (alvo, x, y))
                break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo(alvos):
    """Prova positiva e DEZ provas negativas, cada sabotagem revertida em seguida.

    "Zero diferenca" so vale depois que a comparacao mostra que sabe reprovar.
    """
    fusao, tiles_novos, metas, attrs, carimbos = desenha_kit(ORDEM)
    guardado = carrega_plano()
    planos = {}
    for alvo in ORDEM:
        planos[alvo] = plano_mapa(alvo, carimbos, base_de(alvo, guardado))

    mau = confere(ORDEM, fusao, tiles_novos, metas, attrs, carimbos, planos)
    negativas = []

    def sabota(nome, funcao, espera):
        """Roda `funcao`, que devolve os dados sabotados, e exige acusacao."""
        args = funcao()
        queixas = confere(ORDEM, *args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NAO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    def copia():
        return (dict(fusao) if fusao else None, dict(tiles_novos), dict(metas),
                dict(attrs), {k: json.loads(json.dumps(v))
                              for k, v in carimbos.items()},
                {k: (v[0], v[1], v[2], list(v[3]), dict(v[4]), v[5])
                 for k, v in planos.items()})

    alvo0 = "OreburghCity"

    # N1. colisao 1 -> 0 numa celula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[5][alvo0]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a celula ERA solida
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevacao alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[5][alvo0]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. comportamento de um metatile de CHAO sabotado
    def n3():
        a = copia()
        gid = carimbos[alvo0]["chao"][0]["mt"]
        a[3][gid - 512] = (a[3][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chao sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = carimbos[alvo0]["moveis"][0]["mt"]
        a[3][gid - 512] = a[3][gid - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no movel", n4, "nao esta em COVERED")

    # N5. base de bloco gravada SEM o topo
    def n5():
        a = copia()
        L, W, H, v, esc, ct = a[5][alvo0]
        topos = {t for b in carimbos[alvo0]["blocos"] for t in b["topo"]}
        for i in sorted(esc):
            if (esc[i] & 0x3FF) in topos:
                del esc[i]
                break
        return a
    sabota("base de bloco sem o topo", n5, "bases de bloco e")

    # N6. camada de BAIXO de um movel sabotada (chao da fonte em vez do nosso)
    def n6():
        a = copia()
        gid = carimbos[alvo0]["moveis"][0]["mt"]
        ent = list(a[2][gid - 512])
        ent[0] = ent[4]
        a[2][gid - 512] = ent
        return a
    sabota("camada de baixo sabotada", n6, "nao tem o nosso chao na camada de baixo")

    # N7. mancha escolhida por (x + y) % n, que e xadrez com periodo
    def n7():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            for alvo in ORDEM:
                a[5][alvo] = plano_mapa(alvo, carimbos, base_de(alvo, guardado))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por (x+y) % n", n7, "virou padrao")

    # N8. corredor fechado que PARTE um pedaco de chao. O portao de alcance
    #     sozinho nao pega isso quando ha warp dos dois lados, e foi assim que
    #     Snowpoint passou verde com a cidade cortada.
    def n8():
        a = copia()
        L, W, H, v, esc, ct = a[5][alvo0]
        # o ponto de articulacao e procurado na grade FINAL, a de depois do
        # desenho de verdade, senao as 121 celulas que a passada solidifica
        # aparecem como "quebra" e a busca para na primeira celula qualquer.
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
        raise SystemExit("nao achei ponto de articulacao para a sabotagem N8")
    sabota("corredor fechado", n8, "se partiu")

    # N9. duas variantes de chao IGUAIS pixel a pixel: e enganar a regua
    def n9():
        a = copia()
        lista = a[4][alvo0]["chao"]
        a[2][lista[1]["mt"] - 512] = list(a[2][lista[0]["mt"] - 512])
        return a
    sabota("variante de chao duplicada", n9, "abaixo do piso de 8,0")

    # N10. cor nova escrita num indice que os NOSSOS pixels ja usam: e o unico
    #      jeito de a vaga de indice vago estragar o desenho de quem ja estava la
    def n10():
        a = copia()
        dados = kit()
        vaga = sorted(dados["paletas"])[0]
        pal = [list(c) for c in dados["paletas"][vaga]]
        usados = [i for i in range(1, 16)
                  if i not in set(dados["vagas_livres"].get(vaga) or [])]
        if fusao and int(vaga) == fusao["de"]:
            usados = []
        if not usados:
            for vaga in sorted(dados["paletas"]):
                usados = [i for i in range(1, 16)
                          if i not in set(dados["vagas_livres"].get(vaga) or [])]
                if usados and not (fusao and int(vaga) == fusao["de"]):
                    pal = [list(c) for c in dados["paletas"][vaga]]
                    break
        pal[usados[0]] = [255, 0, 255]
        dados["paletas"][vaga] = pal
        with open(KIT_JSON + ".sab", "w") as f:
            json.dump(dados, f)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        return a
    try:
        sabota("cor nova em indice ja usado", n10, "que algum pixel nosso usa")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # ------------------------------------------------ o que esta NO DISCO
    # Sem este caso o auto-teste so confere o que ele mesmo acabou de calcular.
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.convert("P").load()

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    postas = [l for l in metas if not enchimento(_entradas(meta_disco, l))]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; o caso de DISCO "
              "nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ents in metas.items():
            if _entradas(meta_disco, local) != ents:
                mau.append("metatile %d no disco nao e o do kit" % (512 + local))
            if struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            if (vaga // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga)
        for vaga, cores in sorted(kit()["paletas"].items()):
            arq = [l.split() for l in
                   open(f"{DESTINO}/palettes/%s.pal" % vaga.zfill(2)).read().split("\n")[3:]
                   if l.strip()]
            if [[int(z) for z in c] for c in arq[:16]] != cores:
                mau.append("a paleta %s no disco nao e a do kit" % vaga)

    # ------------------------------------------------------- idempotencia
    for alvo in ORDEM:
        L, W, H, v, escritas, contas = planos[alvo]
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        volta = list(saida)
        for i in sorted(escritas):
            if volta[i] == escritas[i]:
                volta[i] = v[i]
        if volta != list(v):
            mau.append("%s: desfazer nao devolve a base" % alvo)
        _, _, _, _, esc2, _ = plano_mapa(alvo, carimbos, volta)
        if esc2 != escritas:
            mau.append("%s: segunda passada deu plano diferente" % alvo)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE")
    for alvo in ORDEM:
        L, W, H, v, escritas, contas = planos[alvo]
        a, na, ida = regua(v, W, H, L)
        b, nb, idb = regua(v, W, H, L, escritas)
        print("  %-13s %d celulas mudadas, %d solidificadas, regua %.1f%% -> %.1f%%"
              % (alvo, len(escritas), contas["solidos"], a, b))
    print("  %d tiles, %d metatiles, %d provas negativas:" % (len(tiles_novos),
                                                              len(metas),
                                                              len(negativas)))
    for nome, queixa in negativas:
        print("    %-28s -> %s" % (nome, queixa[:110]))
    return 0


def alvos_do_argv():
    alvos = list(ORDEM)
    for i, a in enumerate(sys.argv):
        if a == "--mapa":
            alvos = [sys.argv[i + 1]]
    for a in alvos:
        if a not in TEMAS:
            raise SystemExit("mapa desconhecido: %s" % a)
    return alvos


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--desfazer" in sys.argv:
        return desfaz(alvos_do_argv())
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo(alvos_do_argv())
    if "--so-tileset" in sys.argv:
        alvos = ORDEM
        for i, a in enumerate(sys.argv):
            if a == "--mapa":
                alvos = [sys.argv[i + 1]]
        f, t, m, at, c = desenha_kit(alvos)
        grava_tileset(f, t, m, at)
        print("tileset escrito: %d tiles, %d metatiles" % (len(t), len(m)))
        return 0
    return roda(alvos_do_argv(), "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
