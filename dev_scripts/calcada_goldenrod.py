#!/usr/bin/env python3
"""A calçada de `GoldenrodCity` deixa de ser um tapete só: calçamento em losango
do Scorched Silver repintado com a NOSSA tinta, bueiro, e o mobiliário urbano
que já estava pago dentro do próprio cartucho.

O QUE ESTAVA ERRADO, medido e não lembrado. A régua de
`dev_scripts/regua_cidades.py` mede o "tapete" de chão repetido de cada cidade.
`GoldenrodCity` é a METRÓPOLE de Johto, 58x46, e marcava **26,4%**: o metatile
363 do primário `gTileset_JohtoGeneral`, o calçamento de tijolo bege, ocupava
183 das 692 células andáveis a pé. Olhando o render, esse número tem cara: a
calçada contorna TODOS os quarteirões da cidade, do Centro Pokémon à Torre de
Rádio, e não tem uma junta, um bueiro, um canteiro nem uma mudança de
calçamento em quarenta e seis linhas de mapa.

POR QUE ESTA CIDADE PEDIU UMA ESTRATÉGIA DIFERENTE DAS OUTRAS DA ONDA.
O `gTileset_Goldenrod` é o único secundário de Johto que está no TETO dos dois
lados: 384 de 384 tiles e 384 de 384 metatiles. E o orçamento de tinta é ZERO,
medido cor a cor: a menor união de um par de vagas em uso do secundário é
7+9 = 25 cores e uma vaga cabe 15, então nenhum par cabe junto e a repactuação
de paleta é impossível. Cianwood e Blackthorn puderam fundir vaga e trazer as
cores da fonte; aqui não dá, e insistir nisso mexeria em pixel de arte que já
está no mapa, o que reprova a prova de 0 pixel das rotas irmãs.

O ACHADO QUE DESTRAVOU A RODADA, e ele é uma medição de duas linhas:

    mt 363 -> entradas [(546,5),(545,5),(530,5),(529,5)] e mais nada
    paleta 5 = [.., (216,224,232), (168,184,200), (120,120,128), (88,88,112),
                (64,72,104), (230,222,164), (213,197,131), (197,172,106),
                (172,148,74), (238,230,139), (216,192,136), (208,184,104), ..]

Ou seja: a calçada inteira é do PRIMÁRIO e mora na paleta 5, que é uma das SETE
paletas do primário de Johto (`bigPrimary`), e essa paleta já traz uma rampa
bege de quatro tons dos quais a calçada usa só TRÊS (o quarto, (172,148,74), não
aparece em nenhum pixel do 363) e mais cinco tons de cinza. Um tile NOVO,
gravado no `tiles.png` do secundário e apontado com a paleta 5, sai desenhado
com essas cores sem que uma única entrada de `.pal` seja tocada. A vaga de tinta
que não existe no secundário existe, de graça e já paga, no primário. É por aí
que esta cidade paga a rodada.

O QUE ENTRA, e de onde vem cada peça.

  1. CALÇAMENTO EM LOSANGO, do `Pokémon Scorched Silver` v1.3 Complete (base
     Emerald, BPEE, md5 f7af51cecd3e170cc373fba01753053c), par de tilesets
     `0x49240C` (primário) e `0x492484` (secundário), o da metrópole densa,
     metatile local **105**. São quatro tiles e quatro tons, e os quatro tons
     são trocados posto a posto por luminância pelos quatro bege da NOSSA
     paleta 5. A regra é a mesma que fechou Blackthorn, dita na mesma frase:
     A TINTA DE CHÃO É SEMPRE A NOSSA. O desenho e a textura são da fonte, a
     cor é do cartucho.

         (240,192,96) -> (230,222,164)      (200,144,80) -> (197,172,106)
         (224,168,48) -> (213,197,131)      (192,128,56) -> (172,148,74)

     Ele vira TRÊS peças de chão sem gastar um tile a mais, porque o metatile
     guarda espelhamento nos bits 10 e 11 de cada entrada: `losango` (diagonal
     descendo para a direita), `losango espelhado` (a mesma peça em espelho
     horizontal) e `losango deitado` (espelho vertical). As três tilam sozinhas
     sem costura, porque a peça da fonte foi desenhada para tilar, e o espelho
     de um padrão sem costura continua sem costura. A distância RGB média entre
     elas foi medida e vale 26,5, 26,6 e 42,2, muito acima do piso de 8,0 desta
     onda: não são a mesma variante contada três vezes.

  2. BUEIRO, do mesmo par, metatile local **119**, por MÁSCARA: a diferença
     entre ele e o piso liso da fonte (o 108, um cinza chapado de uma cor só) é
     a tampa redonda, e só ela entra, composta em cima dos pixels da NOSSA
     calçada. Os três cinzas da tampa caem na paleta 5 quase sem mexer, e um
     deles cai EXATO:

         (128,128,136) -> (120,120,128)     (64,72,104) -> (64,72,104)  exato
         ( 96, 96,120) -> ( 88, 88,112)

  3. MOBILIÁRIO URBANO, e este NÃO É IMPORTADO: é peça que já está compilada
     dentro do `gTileset_Goldenrod` e que o mapa da cidade não usa ou usa uma
     ou duas vezes. Canteiro de flores (metatile global 828), placa (829),
     arbusto (831), duas lixeiras (1003 e 1004), máquina de rua (1005) e
     bicicleta (1006). As sete já vêm desenhadas SOBRE a calçada bege, já têm
     `layerType` COVERED e custam ZERO byte de ROM, ZERO tile e ZERO cor.

POR QUE NÃO ENTROU MAIS COISA, e isto é decisão de desenho, não falta de vaga.
Sobraram oito das dezesseis vagas de tile que a compactação abriu, e elas ficam
vazias de propósito. Três candidatos foram abertos, olhados e RECUSADOS:

  - a PRAÇA DE LAJE CINZA da fonte (locais 99 a 117, um 3x3 completo com moldura
    clara, quatro tiles só) foi montada, repintada na paleta 1 do nosso primário
    e desenhada dentro de um tapete de calçada. Ela lê como JANELA, não como
    praça: a moldura clara em volta de um cinza chapado vira um buraco no chão.
    É o mesmo defeito que a primeira versão de Blackthorn levou, e ele só
    aparece quando se olha a prancha;
  - o GRADIL DE AÇO da fonte (locais 48 a 66) é bonito na folha e some no
    recorte: a máscara de cada célula dá de 60 a 170 pixels de cinza solto, que
    na calçada lê como borrão. E a cidade já tem guarda-corpo próprio (o 793,
    usado 32 vezes), então o gradil importado seria um segundo gradil;
  - o tileset `0x492ABC`, que a tabela do briefing chama de "metrópole em
    grade", foi renderizado em atlas antes de gastar vaga, como manda a regra de
    provar que o boneco existe: ele é fachada de tijolo rosa e sebe verde, não
    tem piso de calçada nenhum, e a paleta dele não tem par no nosso. Por isso a
    fonte desta rodada é o `0x492484` e não ele.

A OUTRA MOEDA, a de graça, e por que ela não bastou sozinha. O primário
`gTileset_JohtoGeneral` tem 640 metatiles desenhados e a cidade usa 110; sobram
533 já pagos. O atlas dos 533 foi renderizado e olhado (`atlas_metatiles.py`,
bloco T202). Ele tem calçada de pedra, banco, cerca, canteiro e toldo, mas
TODOS desenhados sobre GRAMA: postos no meio da calçada bege, cada um vira um
quadrado verde. A varredura que mede isso está no auto-teste e devolveu, entre
os 533 do primário e os 58 do secundário que a cidade não usa, exatamente DOIS
metatiles cujo desenho casa a borda inteira do 363, e os dois (o 936 e o 942)
são CÓPIA PIXEL A PIXEL do 363. Usá-los derrubaria a régua sem mudar um pixel
na tela, que é a regra 8 do briefing em pessoa: eles estão na lista de proibidos
deste script e o auto-teste reprova quem os escrever.

O QUE A RÉGUA NÃO PODE ESCONDER. Derrubado o 363, o próximo tapete é o 977, o
calçamento creme da avenida, com 87 células. Ele não é mexido nesta passada (a
avenida larga e lisa é o que faz Goldenrod parecer Goldenrod) e por isso ele é o
TETO desta rodada: com as células que o mobiliário tira do denominador, o 977
fica em torno de 13%, e é ele que a régua passa a mostrar.

ONDE CADA COISA CAI, e nada disso é sorteio solto. O `esqueleto` liga as portas
da cidade pelo caminho de custo mínimo, e a `área de trilha` é ele engordado
para três de largura: é a CALÇADA DE PASSAGEM, e é ela que recebe o `losango`.
Fora da trilha, `bolhas` cresce manchas por frente de onda com ruído de hash
(nunca `random`, para o plano sair igual em qualquer máquina) e essas manchas
recebem o `losango espelhado` e o `losango deitado`, que é o pátio de calçada
dos quarteirões. O bueiro cai espaçado, sempre na trilha, que é onde bueiro
existe. O mobiliário cai FORA da trilha, encostado nos quarteirões, espaçado, e
cada peça passa pelos dois portões de ligação a pé antes de ser aceita.

AS REGRAS DURAS, e como cada uma é cumprida por construção e não por cuidado:

  - planta, warp, colisão de caminho e alcance a pé não mudam. A escrita é
    `(antigo & 0xF000) | colisão | metatile`: a ELEVAÇÃO nunca é tocada;
  - colisão 1 -> 0 é impossível aqui, porque só se escreve em célula que já era
    andável e o script só a deixa andável ou sólida;
  - LENTE: toda peça de CHÃO desta rodada tem atributo `0x0000`, byte a byte o
    mesmo do 363 (comportamento MB_NORMAL, `layerType` NORMAL). Célula que
    continua andável continua com o par (comportamento, layerType) idêntico,
    porque o atributo é literalmente o mesmo número;
  - toda peça SÓLIDA tem `layerType` COVERED (`0x1000`), que é o item 5 do
    `portao_planta.py` e o que evita o achado E3 do `mapas_qa.py`;
  - `GoldenrodCity` já tinha 14 achados E3 na linha de base (ESTADO 0.aa,
    pergunta 48), presos ao carimbo de comportamento. Esta rodada não os
    aumenta, e o auto-teste mede isso.

Uso:
    python3 dev_scripts/calcada_goldenrod.py             # mede, não escreve
    python3 dev_scripts/calcada_goldenrod.py --aplicar   # escreve tileset e mapa
    python3 dev_scripts/calcada_goldenrod.py --desfazer  # devolve o map.bin
    python3 dev_scripts/calcada_goldenrod.py --extrai    # regera o kit da ROM
    python3 dev_scripts/calcada_goldenrod.py --demo      # auto-teste

Idempotente: `--aplicar` planeja sobre a grade que ESTÁ no disco menos o que ele
mesmo gravou (o `calcada_goldenrod.json` guarda antigo e novo de cada célula), e
o tileset é reescrito em vagas FIXAS, então rodar de novo dá byte idêntico.
"""
import collections
import glob
import hashlib
import heapq
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

# O bloco desta rodada nasce DEPOIS do desenho e a partir dele, então ele não
# entra na varredura de corredor de teste. Todos os OUTROS blocos entram.
E.BLOCO_PROPRIO = "203_calcada_goldenrod.json"

DESTINO = f"{RAIZ}/data/tilesets/secondary/goldenrod"
KIT_JSON = f"{RAIZ}/dev_scripts/calcada_goldenrod_kit.json"
PLANO = f"{RAIZ}/dev_scripts/calcada_goldenrod.json"

PRIMARIO = "gTileset_JohtoGeneral"
SECUNDARIO = "gTileset_Goldenrod"
ALVO = "GoldenrodCity"
# Os TRÊS layouts que dividem o `gTileset_Goldenrod`. As duas rotas são a prova
# de não regressão: elas têm que renderizar com ZERO pixel diferente.
IRMAOS = ["GoldenrodCity", "Route34", "Route35"]

# split de Johto (bigPrimary): ver tools/mapjson/mapjson.cpp e include/fieldmap.h
N_META_PRI = 640
N_TILES_PRI = 640
N_PAL_PRI = 7
TETO_TILES = 384          # tiles do SECUNDÁRIO
TETO_META = 384           # metatiles do SECUNDÁRIO
# A compactação de `gTileset_Goldenrod` deixa 354 tiles vivos (medido:
# 384 -> 354, 30 mortos, 0 pinos). As peças novas entram a partir daí, em vaga
# FIXA, que é o que torna `--aplicar` idempotente.
TILE_LOCAL_0 = 354
MARGEM = 2
TETO_REGUA = 20.0         # o alvo desta onda: carimbo dominante <= 20%
PISO_VARIANTE = 8.0       # distância RGB média mínima entre duas variantes
ESPACO_ENTRE_MOVEIS = 3

CARIMBO = 363             # o calçamento de tijolo bege da calçada (PRIMÁRIO)
CARIMBO_AVENIDA = 977     # o calçamento creme da avenida; NÃO é mexido

# CÓPIA PIXEL A PIXEL do 363 dentro do secundário. Escrever um destes derruba a
# régua sem mudar um pixel na tela, e é exatamente o que a regra 8 do briefing
# proíbe. O auto-teste reprova quem os usar.
PROIBIDOS = (936, 942)

# Os 32 locais de metatile do secundário que NEM a cidade NEM `Route34` NEM
# `Route35` desenham. Medido nesta árvore; é a única faixa que pode ser
# sobrescrita sem quebrar rota irmã. A lista é constante de propósito: depois da
# primeira aplicação a cidade passa a usar parte dela, e recalcular pela
# ocupação faria o script escolher outra vaga na segunda rodada.
META_LIVRES = [0, 11, 40, 41, 42, 49, 54, 55, 60, 94, 141, 148, 157, 158, 179,
               180, 181, 182, 183, 190, 191, 197, 199, 218, 220, 247, 296, 302,
               323, 333, 334, 379]

# ------------------------------------------------------------------- a FONTE
SS = dict(slug="scorched-silver", hack="Pokemon Scorched Silver",
          versao="v1.3 Complete", autor="Sloo",
          creditado="RHH (pokeemerald-expansion)",
          md5="f7af51cecd3e170cc373fba01753053c", base="Emerald (BPEE)",
          pri=0x49240C, sec=0x492484, split=(512, 512, 6))

# A peça de CHÃO da fonte, inteira, com a tinta de chão trocada pela nossa.
CHAO_SS = dict(nome="losango", ss=105, pal=5)
# A peça de MÁSCARA: o que difere do piso liso da fonte, sobre a NOSSA calçada.
MOVEL_SS = dict(nome="bueiro", ss=119, ref=108, pal=5)
# Os ESPELHOS do losango, que custam zero tile: (flip_h, flip_v).
ESPELHOS = [dict(nome="losango", fh=0, fv=0),
            dict(nome="losango espelhado", fh=1, fv=0),
            dict(nome="losango deitado", fh=0, fv=1)]

# MOBILIÁRIO que JÁ ESTÁ PAGO: metatile global do `gTileset_Goldenrod`, já
# desenhado sobre a calçada bege e já em COVERED. `quantos` e `espaco` são o
# teto e o afastamento mínimo (Chebyshev) entre duas peças do mesmo tipo.
MOVEL_NOSSO = [
    dict(nome="canteiro de flores", mt=828, quantos=8, espaco=6),
    dict(nome="arbusto",            mt=831, quantos=8, espaco=6),
    dict(nome="lixeira",            mt=1003, quantos=6, espaco=7),
    dict(nome="lixeira dupla",      mt=1004, quantos=5, espaco=8),
    dict(nome="maquina de rua",     mt=1005, quantos=5, espaco=8),
    dict(nome="bicicleta",          mt=1006, quantos=5, espaco=8),
    dict(nome="placa",              mt=829, quantos=4, espaco=9),
]

# As MANCHAS de calçamento fora da trilha.
MANCHAS = [
    dict(grupo=["losango espelhado"], quantas=7, tam=(5, 11)),
    dict(grupo=["losango deitado"],   quantas=6, tam=(4, 9)),
]
CORTE_TRILHA = 55         # quanto da BORDA da trilha recebe tinta, em %
BUEIROS = dict(quantos=6, espaco=7)

N4 = E.N4
MULTI_NIVEL = 15          # ELEVATION_MULTI_LEVEL: casa com QUALQUER elevação


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair idêntico em qualquer máquina e em qualquer versão de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


# ------------------------------------------------------------ leitura do nosso
def _ler(nome):
    return open(f"{DESTINO}/{nome}", "rb").read()


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def _paletas(_c={}):
    """As 13 paletas que valem para este par, com as 7 do primário na frente."""
    if not _c:
        tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
        for v, c in ts["paletas"].items():
            if v >= N_PAL_PRI:
                _c[v] = [tuple(x) for x in c]
        for v, c in tp["paletas"].items():
            if v < N_PAL_PRI:
                _c[v] = [tuple(x) for x in c]
    return _c


def attr_de(mt, attrs_novos=None):
    """Atributo de um metatile GLOBAL, no split de Johto (640).

    O `arte_ginasios_sinnoh.comportamento` parte o índice em 512, que é o split
    do Emerald e não serve para Johto: ele leria o metatile 616 do PRIMÁRIO como
    se fosse o local 104 do secundário.
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


def pixels_de(mt, tiles_novos=None, metas_novos=None):
    """Os 256 pixels RGB de um metatile GLOBAL, com o kit desta rodada valendo.

    `tiles_novos` é {local_no_secundario: matriz 8x8 de ÍNDICE de cor}.
    """
    import render_maps as RM
    from PIL import Image
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    pals = _paletas()
    im = Image.new("RGB", (16, 16), pals[0][0])
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
            cores = pals.get(ip)
            if cores is None:
                continue
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile, list(cores),
                             bool(v & 0x400), bool(v & 0x800))
    return list(im.get_flattened_data())


def distancia(a, b):
    return sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
               for p, q in zip(a, b)) / 256.0


def calcada_nossa():
    """(entradas, atributo, tiles) do metatile 363, o carimbo desta cidade.

    `tiles` sai como ÍNDICE de cor, não como RGB: é assim que o bueiro é
    composto, porque a tampa e a calçada moram na MESMA paleta 5 e a máscara
    entra trocando índice por índice, sem passar por RGB e sem arredondar nada.
    """
    import render_maps as RM
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    ent = entradas_de(CARIMBO)
    quads = []
    for q in range(4):
        v = ent[q]
        idx, ip = v & 0x3FF, (v >> 12) & 0xF
        if ip != CHAO_SS["pal"]:
            raise SystemExit("o metatile %d usa a paleta %d no quadrante %d e "
                             "este script foi escrito para a paleta %d"
                             % (CARIMBO, ip, q, CHAO_SS["pal"]))
        if v & 0xC00:
            raise SystemExit("o metatile %d tem espelho no quadrante %d" % (CARIMBO, q))
        tile = RM.resolver_tile(tp, ts, idx)
        quads.append([list(l) for l in tile])
    # Cuidado medido: as entradas 4 e 6 do 363 valem 0x0C00, que é o tile 0 com
    # os DOIS bits de espelho ligados. O tile 0 é o vazio, então a camada de
    # cima está vazia de verdade; quem olhar a palavra crua em vez do índice
    # (`v & 0x3FF`) conclui o contrário e para sem motivo.
    if any(ent[4 + q] & 0x3FF for q in range(4)):
        raise SystemExit("o metatile %d tem camada de cima; o bueiro presume que "
                         "ela está vazia" % CARIMBO)
    return ent, attr_de(CARIMBO), quads


def _nibbles(dados, local):
    """Um tile 8x8 de 4bpp cru da ROM, como matriz de índice de cor."""
    o = local * 32
    px = [[0] * 8 for _ in range(8)]
    if o + 32 > len(dados):
        return px
    for y in range(8):
        for x in range(0, 8, 2):
            b = dados[o + y * 4 + x // 2]
            px[y][x] = b & 0xF
            px[y][x + 1] = b >> 4
    return px


def _rgb(pal_bytes, i):
    """As 16 cores de uma vaga de paleta da ROM. A conversão de 5 para 8 bits
    neste repositório é DESLOCAR 3 CASAS, não regra de três."""
    out = []
    for k in range(16):
        v = struct.unpack_from("<H", pal_bytes, i * 32 + k * 2)[0]
        out.append(((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3))
    return out


def _luz(c):
    return 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]


def extrai():
    """Regera `calcada_goldenrod_kit.json` a partir da ROM privada.

    Só roda na máquina que tem `fontes-mapas/romhacks/`. O que sai daqui é o
    asset CONVERTIDO (tiles em índice da NOSSA paleta 5, já repintados e já
    compostos sobre a nossa calçada), nunca a ROM.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("não achei fontes-mapas/romhacks: --extrai só roda na "
                         "máquina que tem as ROMs. O kit já extraído está em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
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
        raise SystemExit("o par 0x%X / 0x%X não abriu" % (SS["pri"], SS["sec"]))
    pal = {i: _rgb(t1["pal"] if i < r.n_pal_pri else t2["pal"], i) for i in range(16)}

    def celula(loc):
        """Os 16x16 pixels RGB de um metatile da fonte, com espelho aplicado."""
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

    P = _paletas()[CHAO_SS["pal"]]
    _ent, _attr, base_idx = calcada_nossa()
    # As cores da NOSSA calçada, medidas no próprio 363 e não decoradas.
    usados_363 = sorted({base_idx[q][y][x] for q in range(4)
                         for y in range(8) for x in range(8)})
    # A RAMPA DE CHÃO DA NOSSA PALETA 5: os quatro bege em sequência de
    # luminância. Os três primeiros são os que o 363 usa; o quarto é o tom
    # escuro que a paleta já tem e que a calçada ainda não gastou, e é ele que
    # dá a junta do losango.
    rampa_nossa = [6, 7, 8, 9]
    if set(usados_363) - set(rampa_nossa):
        raise SystemExit("o 363 usa os índices %s e a rampa declarada é %s"
                         % (usados_363, rampa_nossa))

    # ------------------------------------------------ a TINTA DE CHÃO DA FONTE
    A = celula(CHAO_SS["ss"])
    rampa_fonte = sorted({A[y][x] for y in range(16) for x in range(16)},
                         key=_luz, reverse=True)
    if len(rampa_fonte) != len(rampa_nossa):
        raise SystemExit("o losango da fonte tem %d tons (%s) e a nossa rampa "
                         "tem %d; a troca só vale posto a posto"
                         % (len(rampa_fonte), rampa_fonte, len(rampa_nossa)))
    REMAP = dict(zip(rampa_fonte, rampa_nossa))
    if len({P[i] for i in REMAP.values()}) != len(REMAP):
        raise SystemExit("dois tons da fonte cairiam na MESMA cor nossa")

    tiles, pecas = {}, []
    # ------------------------------------------------------- 1. o LOSANGO
    idx_chao = [[REMAP[A[y][x]] for x in range(16)] for y in range(16)]
    for q in range(4):
        ox, oy = (q % 2) * 8, (q // 2) * 8
        tiles["losango:%d" % q] = [[idx_chao[oy + y][ox + x] for x in range(8)]
                                   for y in range(8)]
    pecas.append(dict(papel="chao", nome=CHAO_SS["nome"], ss=CHAO_SS["ss"],
                      pal=CHAO_SS["pal"], ref=None,
                      quads=["losango:%d" % q for q in range(4)],
                      pixels=256, trocados=256))

    # ------------------------------------------------------- 2. o BUEIRO
    B, R2 = celula(MOVEL_SS["ss"]), celula(MOVEL_SS["ref"])
    masc = {(x, y): B[y][x] for y in range(16) for x in range(16)
            if B[y][x] != R2[y][x]}
    if not masc:
        raise SystemExit("a máscara do metatile %d contra o %d é VAZIA"
                         % (MOVEL_SS["ss"], MOVEL_SS["ref"]))
    if len(masc) > 200:
        raise SystemExit("a máscara do %d tem %d pixels de 256: isso não é peça "
                         "sobre a calçada, é outro chão"
                         % (MOVEL_SS["ss"], len(masc)))
    tons = sorted(set(masc.values()), key=_luz, reverse=True)
    # os cinzas da NOSSA paleta 5, em luminância decrescente
    cinzas_nossos = [1, 2, 3, 4, 5]
    if len(tons) > len(cinzas_nossos):
        raise SystemExit("a tampa tem %d tons e a paleta 5 tem %d cinzas"
                         % (len(tons), len(cinzas_nossos)))
    # posto a posto pela POSIÇÃO na rampa de cinza, do mais claro para o mais
    # escuro, começando pelo cinza nosso mais próximo do tom mais claro da fonte
    inicio = min(range(len(cinzas_nossos) - len(tons) + 1),
                 key=lambda k: abs(_luz(P[cinzas_nossos[k]]) - _luz(tons[0])))
    REMAP_C = {t: cinzas_nossos[inicio + i] for i, t in enumerate(tons)}
    idx_bueiro = [[base_idx[(y // 8) * 2 + (x // 8)][y % 8][x % 8]
                   for x in range(16)] for y in range(16)]
    for (x, y), c in masc.items():
        idx_bueiro[y][x] = REMAP_C[c]
    for q in range(4):
        ox, oy = (q % 2) * 8, (q // 2) * 8
        tiles["bueiro:%d" % q] = [[idx_bueiro[oy + y][ox + x] for x in range(8)]
                                  for y in range(8)]
    pecas.append(dict(papel="chao", nome=MOVEL_SS["nome"], ss=MOVEL_SS["ss"],
                      pal=MOVEL_SS["pal"], ref=MOVEL_SS["ref"],
                      quads=["bueiro:%d" % q for q in range(4)],
                      pixels=len(masc), trocados=0))

    dados = dict(
        fonte=dict(hack=SS["hack"], versao=SS["versao"], autor=SS["autor"],
                   creditado=SS["creditado"], base=SS["base"], arquivo=gba,
                   md5=md5, pri="0x%X" % SS["pri"], sec="0x%X" % SS["sec"],
                   split=list(SS["split"])),
        paleta_alvo=CHAO_SS["pal"],
        paleta_congelada=[list(c) for c in P],
        rampa_nossa=rampa_nossa,
        rampa_da_fonte=[list(c) for c in rampa_fonte],
        remap_chao={"%d,%d,%d" % k: v for k, v in REMAP.items()},
        remap_tampa={"%d,%d,%d" % k: v for k, v in REMAP_C.items()},
        tiles=tiles, pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1, ensure_ascii=False)
    print("kit gravado em %s: %d tiles, %d peças, ZERO cor nova"
          % (os.path.relpath(KIT_JSON, RAIZ), len(tiles), len(pecas)))
    print("  a rampa de chão da fonte (%d tons): %s" % (len(rampa_fonte), rampa_fonte))
    print("  troca posto a posto: " + ", ".join(
        "%s -> %s (idx %d)" % (a, P[b], b) for a, b in REMAP.items()))
    print("  tampa do bueiro: " + ", ".join(
        "%s -> %s (idx %d)" % (a, P[b], b) for a, b in REMAP_C.items()))
    for p in pecas:
        print("    %-8s ss=%3d  %3d px de arte" % (p["nome"], p["ss"], p["pixels"]))
    return 0


# --------------------------------------------------------------- o KIT em disco
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa máquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def desenha_kit():
    """(tiles_novos, metas, attrs, carimbos), sem escrever em disco.

    `tiles_novos` = {local_no_secundario: matriz 8x8 de índice}
    `metas`       = {local_do_metatile: (8 entradas)}
    `attrs`       = {local_do_metatile: atributo}
    `carimbos`    = {"chao": [...], "movel": [...]} com o metatile GLOBAL de cada peça
    """
    dados = kit()
    P = _paletas()[dados["paleta_alvo"]]
    if [list(c) for c in P] != dados["paleta_congelada"]:
        raise SystemExit("a paleta %d da árvore não é a que o kit converteu: "
                         "esta rodada NÃO pode mexer em tinta" % dados["paleta_alvo"])
    _ent, attr_calcada, _q = calcada_nossa()
    if attr_calcada != 0:
        raise SystemExit("o atributo do %d é %04X e este script presume 0000"
                         % (CARIMBO, attr_calcada))

    tiles_novos, mapa_tile = {}, {}
    prox = TILE_LOCAL_0
    for chave in sorted(dados["tiles"]):
        tiles_novos[prox] = dados["tiles"][chave]
        mapa_tile[chave] = prox
        prox += 1
    if prox > TETO_TILES:
        raise SystemExit("o kit pede tile até a vaga %d e o teto é %d"
                         % (prox - 1, TETO_TILES))

    metas, attrs, carimbos = {}, {}, {"chao": [], "movel": []}
    vagas = list(META_LIVRES)
    por_nome = {p["nome"]: p for p in dados["pecas"]}

    def poe(ents, attr):
        if not vagas:
            raise SystemExit("acabaram as %d vagas de metatile livres"
                             % len(META_LIVRES))
        local = vagas.pop(0)
        metas[local] = tuple(ents)
        attrs[local] = attr
        return N_META_PRI + local

    # 1. o LOSANGO e os dois espelhos dele: camada de baixo com os quatro tiles
    #    novos, camada de cima VAZIA, atributo IGUAL ao do 363.
    for esp in ESPELHOS:
        p = por_nome[CHAO_SS["nome"]]
        ents = []
        ordem = list(range(4))
        if esp["fh"]:
            ordem = [1, 0, 3, 2]
        if esp["fv"]:
            ordem = [ordem[2], ordem[3], ordem[0], ordem[1]]
        for q in ordem:
            t = mapa_tile[p["quads"][q]] + N_TILES_PRI
            ents.append(t | (esp["fh"] << 10) | (esp["fv"] << 11)
                        | (p["pal"] << 12))
        ents += [0, 0, 0, 0]
        mt = poe(ents, attr_calcada)
        carimbos["chao"].append(dict(nome=esp["nome"], mt=mt))

    # 2. o BUEIRO: também chão, também atributo 0000, porque a tampa é rente ao
    #    piso e o jogador PISA nela. Com `layerType` COVERED a lente reprovaria,
    #    porque a célula continua andável e o par (comportamento, layerType)
    #    mudaria; por isso a tampa é composta na camada de BAIXO, e não posta na
    #    de cima.
    p = por_nome[MOVEL_SS["nome"]]
    ents = [(mapa_tile[p["quads"][q]] + N_TILES_PRI) | (p["pal"] << 12)
            for q in range(4)] + [0, 0, 0, 0]
    mt = poe(ents, attr_calcada)
    carimbos["chao"].append(dict(nome=MOVEL_SS["nome"], mt=mt, bueiro=True))

    # 3. o MOBILIÁRIO que já está pago entra pelo id que ele já tem: nenhuma
    #    vaga é gasta com ele.
    for m in MOVEL_NOSSO:
        a = attr_de(m["mt"])
        if (a >> 12) & 0xF != 1:
            raise SystemExit("%s (metatile %d) tem layerType %d e sólido exige "
                             "COVERED" % (m["nome"], m["mt"], (a >> 12) & 0xF))
        carimbos["movel"].append(dict(nome=m["nome"], mt=m["mt"],
                                      quantos=m["quantos"], espaco=m["espaco"]))
    return tiles_novos, metas, attrs, carimbos


# ------------------------------------------------------------ escrita do tileset
def _compacta_se_precisar():
    """Compacta `gTileset_Goldenrod` se ele ainda estiver no teto de 384 tiles.

    O secundário desta cidade é o ÚNICO da onda que precisa disso: ele está com
    384 de 384 tiles, e 30 deles são mortos (tile que veio no import da folha de
    arte e que nenhum metatile referencia). Compactar devolve 16 vagas, que é
    exatamente o orçamento de tile desta rodada.

    O gatilho é o TAMANHO do `tiles.png`, e é ele que torna `--aplicar`
    idempotente: no estado do master o arquivo tem 384 tiles e a compactação
    roda; depois desta rodada ele tem 368, a compactação NÃO roda de novo, e as
    peças voltam a ser escritas nas mesmas vagas fixas.
    """
    import compacta_tileset as CT
    from PIL import Image
    im = Image.open(f"{DESTINO}/tiles.png")
    n = (im.size[0] // 8) * (im.size[1] // 8)
    if n != TETO_TILES:
        return 0, n
    plano = CT.monta_plano(SECUNDARIO)
    # O tile 0 é pino SEMPRE (é o tile vazio e ele nunca sai do lugar); pino de
    # verdade aqui seria tile do secundário referenciado por metatile do
    # PRIMÁRIO, e `gTileset_Goldenrod` não tem nenhum. Medido: `pinos - {0}` é
    # vazio, e é essa a conta que o próprio relato do compactador imprime.
    if plano["pinos"] - {0}:
        raise SystemExit("a compactação achou pino do primário em %s: %s"
                         % (SECUNDARIO, sorted(plano["pinos"] - {0})))
    vivos = len(plano["vivos"] | plano["pinos"] | {0})
    if vivos != TILE_LOCAL_0:
        raise SystemExit("a compactação deixou %d tiles vivos e este script foi "
                         "escrito para %d" % (vivos, TILE_LOCAL_0))
    escritos = CT.escreve(plano)     # o png fecha a última linha de 16
    tiles, _p, _i, _c = CT.tiles_do_png(f"{DESTINO}/tiles.png")
    for k in range(TILE_LOCAL_0, len(tiles)):
        if any(any(l) for l in tiles[k]):
            raise SystemExit("a vaga %d ficou com tile desenhado depois da "
                             "compactação" % k)
    return n - vivos, escritos


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve `tiles.png`, `metatiles.bin` e `metatile_attributes.bin`."""
    import compacta_tileset as CT
    from PIL import Image
    mortos, _n = _compacta_se_precisar()
    tiles, paleta, info, cols = CT.tiles_do_png(f"{DESTINO}/tiles.png")
    while len(tiles) <= max(tiles_novos):
        tiles.append([[0] * 8 for _ in range(8)])
    for local, px in tiles_novos.items():
        tiles[local] = [list(l) for l in px]
    # a última linha do png tem que ficar cheia: 16 tiles por linha
    while len(tiles) % CT.COLUNAS:
        tiles.append([[0] * 8 for _ in range(8)])
    CT.grava_png(f"{DESTINO}/tiles.png", tiles, paleta, info)

    meta = bytearray(_ler("metatiles.bin"))
    if len(meta) != TETO_META * 16:
        raise SystemExit("o metatiles.bin tem %d bytes e o teto é %d"
                         % (len(meta), TETO_META * 16))
    for local, ents in metas.items():
        struct.pack_into("<8H", meta, local * 16, *ents)
    with open(f"{DESTINO}/metatiles.bin", "wb") as f:
        f.write(bytes(meta))

    at = bytearray(_ler("metatile_attributes.bin"))
    if len(at) != TETO_META * 2:
        raise SystemExit("o metatile_attributes.bin tem %d bytes e o esperado "
                         "para 2 bytes por metatile é %d" % (len(at), TETO_META * 2))
    for local, a in attrs.items():
        struct.pack_into("<H", at, local * 2, a)
    with open(f"{DESTINO}/metatile_attributes.bin", "wb") as f:
        f.write(bytes(at))
    return mortos, len(tiles)


# ------------------------------------------------------------- geometria do mapa
def esqueleto(v, W, H, d, elegivel):
    """Caminho de custo mínimo ligando as portas do mapa, em ordem de leitura.

    O custo não é só distância. Andar colado num sólido custa mais, para a
    trilha sair pelo MEIO da calçada e não raspando o prédio; virar custa mais,
    para ela sair reta como calçada de verdade; e célula que não pode receber
    tinta custa muito mais, mas não é proibida, senão o caminho não atravessa a
    soleira das portas. (A função é a mesma que fechou Blackthorn e Snowpoint.)
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
    ossos = {portas[0]}
    for p in portas[1:]:
        trecho = caminho(p, ossos)
        if trecho:
            ossos |= set(trecho)
    return ossos, portas


def area_trilha(v, W, H, d, elegivel):
    """As células de TRILHA: o esqueleto engordado para três de largura."""
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
    # risco de UMA célula de largura não lê como calçada, lê como sujeira
    while True:
        fora = {(x, y) for x, y in pav
                if not ((x, y - 1) in pav or (x, y + 1) in pav)
                or not ((x - 1, y) in pav or (x + 1, y) in pav)}
        if not fora:
            break
        pav -= fora
    return pav, portas


def bolhas(livres, spec):
    """[(nomes, {células})], manchas orgânicas crescidas por frente de onda.

    A SEMENTE não é sorteio solto: as células livres são ordenadas por um hash
    da posição e a semente só é aceita a pelo menos 4 (Chebyshev) de toda
    semente já aceita. O CRESCIMENTO é guloso com ruído: a cada passo entra a
    célula da frente de onda com o menor hash. Círculo daria mancha redonda e
    xadrez daria sal e pimenta; frente de onda com ruído dá contorno irregular.
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

    Borda reta de calçamento novo dentro de calçamento velho lê como fita
    adesiva; o corte por hash da posição é o que tira essa cara. Não há estado
    nem ordem aqui.
    """
    return {p for p in trilha
            if all((p[0] + dx, p[1] + dy) in trilha for dx, dy in N4)
            or _mistura(p[0], p[1], 0x7A17) % 100 < corte}


def peca_da_mancha(nomes, x, y):
    """Qual das peças do grupo cai nesta célula. Hash da posição, não paridade:
    paridade vira xadrez e o auto-teste reprova."""
    return nomes[_mistura(x, y, 0xA5A5 + len(nomes)) % len(nomes)]


def componentes(v, W, H):
    """{célula: rótulo} dos pedaços de chão andável ligados a pé.

    Não basta o alcance a partir dos warps: fechar um corredor com warp dos dois
    lados não tira NENHUMA célula do alcance e mesmo assim parte a cidade em
    duas. Este portão olha a LIGAÇÃO entre as células, que é o que o jogador
    sente.
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
    """Nenhum pedaço de chão se PARTIU, e nenhum se juntou a outro."""
    mau = []
    por_rotulo = collections.defaultdict(set)
    for p, rr in antes.items():
        if p not in solidificadas:
            por_rotulo[rr].add(p)
    for rr, cels in por_rotulo.items():
        if len({depois.get(p) for p in cels}) > 1:
            mau.append("o pedaço %d de chão se partiu em %d"
                       % (rr, len({depois.get(p) for p in cels})))
    juntou = collections.defaultdict(set)
    for p, rr in depois.items():
        if p in antes:
            juntou[rr].add(antes[p])
    for rr, origens in juntou.items():
        if len(origens) > 1:
            mau.append("dois pedaços de chão que eram separados se juntaram")
    return mau


def corredores_multinivel(v, W, H, d):
    """Os corredores da suíte, refeitos com a regra da ELEVAÇÃO 15.

    O `enfeita_cidades.corredores_de_teste` congela as células que a suíte anda
    dentro do mapa, mas ele PULA o bloco 175 e simula com a regra "elevação 0 é
    curinga e o resto exige igualdade", que é falsa onde há
    `ELEVATION_MULTI_LEVEL` (15). Esta versão roda a mesma simulação com a regra
    certa (0 e 15 são curingas dos dois lados) e o resultado é a UNIÃO com o que
    a função original devolve. Corredor a mais custa enfeite a menos; corredor a
    menos custa caso vermelho. (Nasceu em `orla_sunyshore.py`.)
    """
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_",
                                d.get("name", ALVO)).upper().replace("__", "_")
    obj = {(o["x"], o["y"]) for o in (d.get("object_events") or [])}
    warps = d.get("warp_events") or []
    pisadas = set()
    passo = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

    def compativel(ea, eb):
        return ea in (0, MULTI_NIVEL) or eb in (0, MULTI_NIVEL) or ea == eb

    def caminha(x, y, pernas, olhando):
        pisadas.add((x, y))
        for direcao, n in pernas:
            dx, dy = direcao
            passos = n - 1 if olhando != direcao else n
            olhando = direcao
            for _ in range(max(0, passos)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    break
                j = ny * W + nx
                if (v[j] >> 10) & 3 or (nx, ny) in obj:
                    break
                if not compativel((v[y * W + x] >> 12) & 0xF, (v[j] >> 12) & 0xF):
                    break
                x, y = nx, ny
                pisadas.add((x, y))

    for arq in sorted(glob.glob(f"{pasta}/*.json")):
        if os.path.basename(arq) == E.BLOCO_PROPRIO:
            continue
        for caso in json.load(open(arq)):
            if caso.get("warp") != nome_mapa:
                continue
            wid = int(caso.get("warp_id", 0) or 0)
            if wid >= len(warps):
                continue
            pernas = []
            for tok in (caso.get("roteiro") or "").split(","):
                m = E._LEG.match(tok.strip())
                if m:
                    pernas.append((passo[m.group(1)], int(m.group(2) or 1)))
            for x0, y0 in ((warps[wid]["x"], warps[wid]["y"]),
                           (warps[wid]["x"], warps[wid]["y"] + 1)):
                if not (0 <= x0 < W and 0 <= y0 < H):
                    continue
                for olhando in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    caminha(x0, y0, pernas, olhando)
    return pisadas


# ---------------------------------------------------------------- o PLANO
def plano_mapa(carimbos, base=None):
    """(d, L, W, H, v, escritas, contas) para `GoldenrodCity`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    AG = E.agua()
    ids_chao = {c["mt"] for c in carimbos["chao"]}
    por_nome_chao = {c["nome"]: c["mt"] for c in carimbos["chao"]}
    id_bueiro = [c["mt"] for c in carimbos["chao"] if c.get("bueiro")][0]
    familia = {CARIMBO} | ids_chao

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    elev = collections.Counter(
        (c >> 12) & 0xF for c in v
        if (c & 0x3FF) == CARIMBO and not ((c >> 10) & 3)).most_common(1)[0][0]

    elegivel = {(i % W, i // W) for i in range(W * H)
                if andavel(i) and (v[i] & 0x3FF) in familia
                and ((v[i] >> 12) & 0xF) == elev
                and (attr_de(v[i] & 0x3FF) & 0x1FF) not in AG}

    escritas = {}
    trilha, portas = area_trilha(v, W, H, d, elegivel)

    # ------------------------------------------------------------- 1. MÓVEIS
    # Eles vêm ANTES da tinta de propósito, e a razão está medida em Snowpoint:
    # móvel posto no carimbo tira uma célula do numerador E do denominador da
    # régua; móvel posto em cima de um calçamento novo tira só do denominador, o
    # que PIORA a conta.
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    gelo |= corredores_multinivel(v, W, H, d)
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))

    aplicado = list(v)
    ini = E.partidas(d, W, H, v)
    antes_alc = E.alcance(v, W, H, ini)
    antes_comp = componentes(v, W, H)
    novos_solidos, postos = [], []
    por_movel = collections.defaultdict(list)

    def nao_liga(grade, x, y):
        """Os vizinhos andáveis de (x,y) ainda se falam sem passar por (x,y)?"""
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
        """Solidifica (x,y) e devolve True se os DOIS portões deixarem."""
        i = y * W + x
        antigo = aplicado[i]
        aplicado[i] = (antigo & 0xF000) | (1 << 10) | mt_id   # ELEVAÇÃO INTACTA
        perdidas = (antes_alc - E.alcance(aplicado, W, H, ini)) \
            - set(novos_solidos) - {(x, y)}
        if perdidas or nao_liga(aplicado, x, y):
            aplicado[i] = antigo
            return False
        escritas[i] = (antigo, aplicado[i])
        novos_solidos.append((x, y))
        postos.append((x, y))
        return True

    # A ordem de varredura é a de leitura, e a escolha do móvel é por hash da
    # posição: sem hash o mapa sai com a mesma peça em fila, e com `random` o
    # plano deixaria de ser reproduzível.
    candidatas = sorted((p for p in elegivel if livre(*p)),
                        key=lambda p: _mistura(p[0], p[1], 0x1CE))
    # RODÍZIO, e não uma varredura por tipo de cada vez. Com a varredura por
    # tipo o primeiro da lista come o espaço todo e os últimos saem com ZERO
    # peça: medido, a bicicleta e a placa não entravam no mapa. No rodízio cada
    # volta põe no máximo uma peça de cada tipo, e a rua sai com os sete tipos.
    faltam = {m["nome"]: m["quantos"] for m in carimbos["movel"]}
    while any(faltam.values()):
        pos_na_volta = 0
        for m in carimbos["movel"]:
            if faltam[m["nome"]] <= 0:
                continue
            for (x, y) in candidatas:
                if not livre(x, y) or not espacado(m, x, y):
                    continue
                # móvel encostado em quarteirão lê como mobiliário de rua;
                # solto no meio da calçada lê como obstáculo largado
                if not any(not (0 <= x + dx < W and 0 <= y + dy < H)
                           or ((aplicado[(y + dy) * W + x + dx] >> 10) & 3)
                           for dx, dy in N4):
                    continue
                if tenta_solidificar(x, y, m["mt"]):
                    por_movel[m["nome"]].append((x, y))
                    faltam[m["nome"]] -= 1
                    pos_na_volta += 1
                    break
            else:
                faltam[m["nome"]] = 0
        if not pos_na_volta:
            break

    # --------------------------------------------------------- 2. a TRILHA
    # A calçada de passagem recebe o `losango`, que é o calçamento importado.
    pintadas = collections.Counter()

    def pintavel(p):
        i = p[1] * W + p[0]
        return (p in elegivel and i not in escritas
                and (aplicado[i] & 0x3FF) == CARIMBO)

    def pinta(p, mt_id):
        i = p[1] * W + p[0]
        antigo = aplicado[i]
        novo = (antigo & 0xFC00) | mt_id     # colisão e elevação INTACTAS
        aplicado[i] = novo
        escritas[i] = (antigo, novo)

    for p in sorted(desgasta(trilha, CORTE_TRILHA)):
        if pintavel(p):
            pinta(p, por_nome_chao["losango"])
            pintadas["losango"] += 1

    # --------------------------------------------------------- 3. as MANCHAS
    livres_mancha = {p for p in elegivel if pintavel(p) and p not in trilha}
    for grupo, corpo in bolhas(livres_mancha, MANCHAS):
        for p in sorted(corpo):
            if not pintavel(p):
                continue
            nome = peca_da_mancha(grupo, p[0], p[1])
            pinta(p, por_nome_chao[nome])
            pintadas[nome] += 1

    # --------------------------------------------------------- 4. os BUEIROS
    # Bueiro é da rua, então ele cai DENTRO da trilha, espaçado, e nunca em
    # célula que a suíte pisa (para o render do teste não mudar de cara).
    postos_b = []
    for p in sorted(trilha, key=lambda q: _mistura(q[0], q[1], 0xB0E1)):
        if len(postos_b) >= BUEIROS["quantos"]:
            break
        i = p[1] * W + p[0]
        if p in gelo or i in escritas:
            continue
        if (aplicado[i] & 0x3FF) not in (CARIMBO,) and i not in escritas:
            pass
        if any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) < BUEIROS["espaco"]
               for q in postos_b):
            continue
        if (aplicado[i] & 0x3FF) != CARIMBO:
            continue
        pinta(p, id_bueiro)
        pintadas["bueiro"] += 1
        postos_b.append(p)

    depois_comp = componentes(aplicado, W, H)
    contas = dict(pintadas=dict(pintadas), moveis={k: len(x) for k, x in por_movel.items()},
                  solidos=len(novos_solidos), trilha=len(trilha), portas=len(portas),
                  elegiveis=len(elegivel),
                  ligacao=ligacao_intacta(antes_comp, depois_comp, set(novos_solidos)))
    return d, L, W, H, aplicado, escritas, contas


# ------------------------------------------------------------------- a RÉGUA
def regua(v, W, H, L):
    """(liso, dominante, andáveis) com o split CERTO de Johto."""
    AG = E.agua()
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"], N_META_PRI)
    andavel = [c & 0x3FF for c in v
               if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG]
    f = collections.Counter(andavel)
    mt, n = f.most_common(1)[0]
    return round(n * 100.0 / len(andavel), 1), mt, len(andavel)


# ------------------------------------------------------------- gravar e desfazer
def carrega_plano():
    if os.path.exists(PLANO):
        return json.load(open(PLANO))
    return {}


def base_de(guardado):
    """A grade de HOJE com o que ESTE script gravou desfeito, para poder
    replanejar sobre o mesmo ponto de partida e sair byte a byte igual."""
    d, L, W, H, v = G.grade(ALVO)
    v = list(v)
    for idx, antigo, novo in guardado.get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    guardado = carrega_plano()
    base = base_de(guardado) if guardado else None
    d, L, W, H, v, escritas, contas = plano_mapa(carimbos, base)
    antes = base_de(guardado) if guardado else list(G.grade(ALVO)[4])
    liso0, mt0, n0 = regua(antes, W, H, L)
    liso1, mt1, n1 = regua(v, W, H, L)
    print("%s: %d células escritas (%d sólidas), régua %.1f%% (mt %d) -> "
          "%.1f%% (mt %d), andáveis %d -> %d"
          % (ALVO, len(escritas), contas["solidos"], liso0, mt0, liso1, mt1, n0, n1))
    print("  calçamento: " + ", ".join("%s=%d" % (k, x)
                                       for k, x in sorted(contas["pintadas"].items())))
    print("  mobiliário: " + ", ".join("%s=%d" % (k, x)
                                       for k, x in sorted(contas["moveis"].items())))
    if contas["ligacao"]:
        raise SystemExit("LIGAÇÃO A PÉ QUEBRADA: " + "; ".join(contas["ligacao"]))
    if liso1 > TETO_REGUA:
        print("  AVISO: %.1f%% ainda passa do teto de %.1f%%" % (liso1, TETO_REGUA))
    if not aplicar:
        print("  (nada foi escrito; use --aplicar)")
        return 0
    mortos, n_tiles = grava_tileset(tiles_novos, metas, attrs)
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % (W * H), *v))
    with open(PLANO, "w") as f:
        json.dump(dict(mapa=ALVO,
                       celulas=[[i, a, b] for i, (a, b) in sorted(escritas.items())]),
                  f, indent=1)
    print("  tileset: %d tiles mortos recolhidos, %d tiles no png, %d metatiles novos"
          % (mortos, n_tiles, len(metas)))
    return 0


def desfaz():
    guardado = carrega_plano()
    if not guardado:
        raise SystemExit("não há %s" % os.path.relpath(PLANO, RAIZ))
    d, L, W, H, v = G.grade(ALVO)
    v = list(v)
    n = 0
    for idx, antigo, novo in guardado["celulas"]:
        if v[idx] == novo:
            v[idx] = antigo
            n += 1
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % (W * H), *v))
    print("%s: %d células devolvidas. O TILESET não volta por aqui: use "
          "`git checkout data/tilesets/secondary/goldenrod`." % (ALVO, n))
    return 0


# ---------------------------------------------------------------- a CONFERÊNCIA
def _git_show(ref, caminho):
    import subprocess
    return subprocess.run(["git", "-C", RAIZ, "show", "%s:%s" % (ref, caminho)],
                          stdout=subprocess.PIPE, check=True).stdout


def _tileset_do_ref(ref):
    """(tiles, metatiles, attrs) do `gTileset_Goldenrod` no commit de referência."""
    import io
    from PIL import Image
    rel = os.path.relpath(DESTINO, RAIZ)
    png = Image.open(io.BytesIO(_git_show(ref, rel + "/tiles.png")))
    if png.mode != "P":
        png = png.convert("P")
    W, H = png.size
    px = png.load()
    cols = W // 8
    tiles = [[[px[(i % cols) * 8 + x, (i // cols) * 8 + y] for x in range(8)]
              for y in range(8)] for i in range((W // 8) * (H // 8))]
    return (tiles, _git_show(ref, rel + "/metatiles.bin"),
            _git_show(ref, rel + "/metatile_attributes.bin"))


def _px_com(tiles_pri, tiles_sec, meta_sec, mt, pals):
    """Os 256 pixels RGB de um metatile GLOBAL, com um secundário arbitrário."""
    import render_maps as RM
    from PIL import Image
    tp = _tileset(PRIMARIO)
    im = Image.new("RGB", (16, 16), pals[0][0])
    p = im.load()
    if mt >= N_META_PRI:
        local = mt - N_META_PRI
        ent = list(struct.unpack_from("<8H", meta_sec, local * 16))
    else:
        ent = list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))
    for cam in (0, 1):
        for q in range(4):
            v = ent[cam * 4 + q]
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            if not idx:
                continue
            tile = (tiles_pri[idx] if idx < N_TILES_PRI
                    else (tiles_sec[idx - N_TILES_PRI]
                          if idx - N_TILES_PRI < len(tiles_sec) else None))
            if tile is None or ip not in pals:
                continue
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile, list(pals[ip]),
                             bool(v & 0x400), bool(v & 0x800))
    return list(im.get_flattened_data())


def _attr_com(a_sec, mt):
    """O atributo de um metatile GLOBAL lendo o `metatile_attributes.bin` DADO.

    Existe para que a mesma conta sirva para o arquivo de hoje e para o do
    commit de referência, e para que o auto-teste possa sabotar o arquivo e
    provar que o portão acusa.
    """
    ap = G._attrs(PRIMARIO)
    if mt < N_META_PRI:
        return ap[mt] if mt < len(ap) else 0
    local = mt - N_META_PRI
    return struct.unpack_from("<H", a_sec, local * 2)[0] \
        if local * 2 + 2 <= len(a_sec) else 0


def defeitos_de_planta(antigo, v, W, H, at_velho, at_novo):
    """As regras duras 1, 3, 4, 5 e 8 do briefing, célula a célula.

    Função PURA de propósito: `confere` a chama com o que está em disco e o
    auto-teste a chama com grades sabotadas, e as duas passam pelo mesmo código.
    """
    mau = []
    for i in range(W * H):
        a, b = antigo[i], v[i]
        if (a >> 12) != (b >> 12):
            mau.append("elevação mudou em (%d,%d)" % (i % W, i // W))
        ca, cb = (a >> 10) & 3, (b >> 10) & 3
        if ca and not cb:
            mau.append("colisão 1 -> 0 em (%d,%d)" % (i % W, i // W))
        if a == b:
            continue
        if (b & 0x3FF) in PROIBIDOS:
            mau.append("o metatile %d é CÓPIA PIXEL A PIXEL do %d e foi escrito "
                       "em (%d,%d)" % (b & 0x3FF, CARIMBO, i % W, i // W))
        if cb:
            if ((_attr_com(at_novo, b & 0x3FF) >> 12) & 0xF) != 1:
                mau.append("a célula sólida (%d,%d) não é COVERED" % (i % W, i // W))
        else:
            la = _attr_com(at_velho, a & 0x3FF)
            lb = _attr_com(at_novo, b & 0x3FF)
            if (la & 0x1FF, (la >> 12) & 0xF) != (lb & 0x1FF, (lb >> 12) & 0xF):
                mau.append("a lente mudou na célula andável (%d,%d): %04X -> %04X"
                           % (i % W, i // W, la, lb))
    return mau


def confere(ref="HEAD"):
    """Prova, contra o commit de referência, tudo o que o briefing cobra."""
    d, L, W, H, v = G.grade(ALVO)
    antigo = list(struct.unpack("<%dH" % (W * H),
                                _git_show(ref, L["blockdata_filepath"])))
    if len(antigo) != len(v):
        return ["o map.bin mudou de tamanho"]
    at_novo = _ler("metatile_attributes.bin")
    _t0, _m0, at_velho = _tileset_do_ref(ref)
    mau = defeitos_de_planta(antigo, list(v), W, H, at_velho, at_novo)

    def attr(a_sec, mt):
        return _attr_com(a_sec, mt)

    # os mapas IRMÃOS: nenhum metatile que eles desenham pode ter mudado um pixel
    pals = _paletas()
    from PIL import Image
    tp = _tileset(PRIMARIO)
    tiles_pri = tp["tiles"]
    tiles_v, meta_v, _a = _tileset_do_ref(ref)
    ts = _tileset(SECUNDARIO)
    tiles_n, meta_n = ts["tiles"], ts["metatiles"]
    layouts = {l["id"]: l for l in json.load(
        open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"] if l.get("id")}
    for irmao in IRMAOS:
        if irmao == ALVO:
            continue
        Li = layouts[json.load(open(f"{RAIZ}/data/maps/{irmao}/map.json"))["layout"]]
        b = open(f"{RAIZ}/{Li['blockdata_filepath']}", "rb").read()
        if b != _git_show(ref, Li["blockdata_filepath"]):
            mau.append("o map.bin de %s foi tocado" % irmao)
        usados = {struct.unpack_from("<H", b, k)[0] & 0x3FF
                  for k in range(0, len(b), 2)}
        for mt in sorted(usados):
            if _px_com(tiles_pri, tiles_v, meta_v, mt, pals) != \
                    _px_com(tiles_pri, tiles_n, meta_n, mt, pals):
                mau.append("%s: o metatile %d mudou de pixel" % (irmao, mt))
            if attr(at_velho, mt) != attr(at_novo, mt):
                mau.append("%s: o atributo do metatile %d mudou" % (irmao, mt))

    # As paletas do secundário não podem ter mudado uma COR. A comparação é
    # feita sobre as cores lidas, não sobre os bytes do arquivo: o
    # `.gitattributes` deste repositório declara `*.pal text eol=crlf`, então o
    # que está no índice tem LF e o que está no disco tem CRLF, e comparar byte
    # a byte acusaria as dezesseis paletas como mudadas todo dia.
    def _cores_pal(dados):
        linhas = dados.decode("latin-1").replace("\r\n", "\n").split("\n")
        return [l.strip() for l in linhas[3:] if l.strip()]

    rel = os.path.relpath(DESTINO, RAIZ)
    for k in range(16):
        nome = "%s/palettes/%02d.pal" % (rel, k)
        if _cores_pal(open(f"{RAIZ}/{nome}", "rb").read()) != \
                _cores_pal(_git_show(ref, nome)):
            mau.append("a paleta %02d do secundário mudou; esta rodada tem ZERO "
                       "orçamento de tinta" % k)

    # as variantes de calçamento têm que ser variantes de VERDADE
    _tn, _mm, _aa, carimbos = desenha_kit()
    ids = [c["mt"] for c in carimbos["chao"]]
    px = {mt: pixels_de(mt) for mt in ids + [CARIMBO]}
    for a in range(len(ids)):
        for b2 in range(a + 1, len(ids)):
            dd = distancia(px[ids[a]], px[ids[b2]])
            if dd < PISO_VARIANTE:
                mau.append("os metatiles %d e %d distam %.2f, abaixo do piso %.1f"
                           % (ids[a], ids[b2], dd, PISO_VARIANTE))
        if distancia(px[ids[a]], px[CARIMBO]) < PISO_VARIANTE:
            mau.append("o metatile %d é igual demais ao carimbo %d"
                       % (ids[a], CARIMBO))
    return mau


# ------------------------------------------------------------------ auto-teste
def _casa_borda(a, b):
    """Quantos por cento da BORDA de 16x16 de dois metatiles coincidem."""
    pa, pb = pixels_de(a), pixels_de(b)
    ring = [(x, 0) for x in range(16)] + [(x, 15) for x in range(16)] \
        + [(0, y) for y in range(1, 15)] + [(15, y) for y in range(1, 15)]
    ig = sum(1 for x, y in ring if pa[y * 16 + x] == pb[y * 16 + x])
    return ig * 100.0 / len(ring)


def demo():
    """Os casos que esta rodada precisou fechar, e as sabotagens que ela acusa."""
    mau = []
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    ids_chao = [c["mt"] for c in carimbos["chao"]]

    # 1. ORÇAMENTO. O kit cabe nas 16 vagas que a compactação abre e nas 32 vagas
    #    de metatile que nem Route34 nem Route35 usam.
    if len(tiles_novos) > TETO_TILES - TILE_LOCAL_0:
        mau.append("o kit pede %d tiles e a compactação abre %d"
                   % (len(tiles_novos), TETO_TILES - TILE_LOCAL_0))
    if len(metas) > len(META_LIVRES):
        mau.append("o kit pede %d metatiles e há %d vagas livres"
                   % (len(metas), len(META_LIVRES)))

    # 2. AS 32 VAGAS SÃO MESMO LIVRES. Este é o caso que evita quebrar rota
    #    irmã: `Route34` e `Route35` desenham 26 dos 58 metatiles que a CIDADE
    #    não usa, e sobrescrever um deles estragaria a rota calado.
    layouts = {l["id"]: l for l in json.load(
        open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"] if l.get("id")}
    usados = set()
    for nome in IRMAOS:
        Li = layouts[json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))["layout"]]
        b = open(f"{RAIZ}/{Li['blockdata_filepath']}", "rb").read()
        for k in range(0, len(b), 2):
            usados.add(struct.unpack_from("<H", b, k)[0] & 0x3FF)
    invadidos = [l for l in metas if N_META_PRI + l in usados]
    if invadidos:
        # depois de aplicado, a CIDADE passa a usar as vagas; o caso só vale
        # contra as ROTAS, que são a prova
        rotas = set()
        for nome in IRMAOS:
            if nome == ALVO:
                continue
            Li = layouts[json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))["layout"]]
            b = open(f"{RAIZ}/{Li['blockdata_filepath']}", "rb").read()
            for k in range(0, len(b), 2):
                rotas.add(struct.unpack_from("<H", b, k)[0] & 0x3FF)
        invadidos = [l for l in metas if N_META_PRI + l in rotas]
        if invadidos:
            mau.append("as vagas %s são desenhadas por Route34 ou Route35"
                       % sorted(invadidos))

    # 3. A LENTE DAS PEÇAS DE CHÃO. Toda peça andável tem que ter o atributo
    #    IDÊNTICO ao do 363, senão a célula que continua andável muda de lente e
    #    o `portao_planta.py` reprova.
    a363 = attr_de(CARIMBO)
    for c in carimbos["chao"]:
        a = attrs[c["mt"] - N_META_PRI]
        if a != a363:
            mau.append("a peça de chão %s tem atributo %04X e o 363 tem %04X"
                       % (c["nome"], a, a363))
    for c in carimbos["movel"]:
        a = attr_de(c["mt"])
        if ((a >> 12) & 0xF) != 1:
            mau.append("o móvel %s não é COVERED" % c["nome"])

    # 4. NENHUMA COR NOVA. Todo pixel dos tiles novos aponta para um índice que a
    #    paleta 5 já tinha, e o `.pal` em disco não é tocado por este script.
    P = _paletas()[CHAO_SS["pal"]]
    for local, px in tiles_novos.items():
        for l in px:
            for c in l:
                if not (0 <= c < len(P)):
                    mau.append("o tile %d usa o índice %d, fora da paleta" % (local, c))

    # 5. AS VARIANTES SÃO VARIANTES. Duas peças com distância RGB zero são uma
    #    peça só, e usar cópia para derrubar a régua é a regra 8 do briefing.
    px = {mt: pixels_de(mt) for mt in ids_chao + [CARIMBO]}
    for i in range(len(ids_chao)):
        for j in range(i + 1, len(ids_chao)):
            dd = distancia(px[ids_chao[i]], px[ids_chao[j]])
            if dd < PISO_VARIANTE:
                mau.append("as peças %d e %d distam %.2f (piso %.1f)"
                           % (ids_chao[i], ids_chao[j], dd, PISO_VARIANTE))

    # 6. A SABOTAGEM QUE ESTA CIDADE PRECISOU ACHAR, e ela é real: o secundário
    #    tem DOIS metatiles (936 e 942) que são cópia PIXEL A PIXEL do 363.
    #    Escrever um deles derrubaria a régua sem mudar um pixel na tela. O caso
    #    prova que eles existem, que são idênticos, e que o `confere` acusa.
    for mt in PROIBIDOS:
        if distancia(pixels_de(mt), px[CARIMBO]) != 0.0:
            mau.append("o metatile %d deixou de ser cópia do %d: a lista de "
                       "proibidos precisa ser remedida" % (mt, CARIMBO))

    # 7. O ESPELHO É ESPELHO DE VERDADE. A peça espelhada tem que ser a imagem
    #    refletida da original, pixel a pixel, senão as entradas de flip estão
    #    montadas erradas e o calçamento sai com costura.
    por_nome = {c["nome"]: c["mt"] for c in carimbos["chao"]}
    base = pixels_de(por_nome["losango"])
    esp = pixels_de(por_nome["losango espelhado"])
    dei = pixels_de(por_nome["losango deitado"])
    for y in range(16):
        for x in range(16):
            if base[y * 16 + x] != esp[y * 16 + (15 - x)]:
                mau.append("o `losango espelhado` não é o espelho horizontal do "
                           "`losango` em (%d,%d)" % (x, y))
                break
            if base[y * 16 + x] != dei[(15 - y) * 16 + x]:
                mau.append("o `losango deitado` não é o espelho vertical do "
                           "`losango` em (%d,%d)" % (x, y))
                break
        else:
            continue
        break

    # 8. O CALÇAMENTO TILA SEM COSTURA. A coluna 15 de uma peça e a coluna 0 da
    #    peça ao lado têm que fechar o desenho: o teste é que a peça repetida
    #    2x2 não crie borda que não existe dentro dela. Medimos pela DERIVADA:
    #    a variação média na junta não pode ser maior que a variação média
    #    dentro da peça.
    for nome in ("losango", "losango espelhado", "losango deitado"):
        p = pixels_de(por_nome[nome])
        def dvar(a, b):
            return sum(abs(a[k] - b[k]) for k in range(3))
        junta = sum(dvar(p[y * 16 + 15], p[y * 16 + 0]) for y in range(16)) / 16.0
        dentro = sum(dvar(p[y * 16 + x], p[y * 16 + x + 1])
                     for y in range(16) for x in range(15)) / (16 * 15.0)
        if junta > dentro * 3 + 1:
            mau.append("%s: a junta vertical varia %.1f e o miolo %.1f: tem "
                       "costura" % (nome, junta, dentro))

    # 9. O PLANO É DETERMINISTA. Duas montagens seguidas dão a mesma escrita, e
    #    é isso que faz `--aplicar` sair byte a byte igual duas vezes. O plano
    #    parte SEMPRE da grade do master (a de hoje menos o que este script já
    #    gravou), senão o auto-teste mediria coisa diferente antes e depois de
    #    aplicar.
    base = base_de(carrega_plano())
    _d, L0, W0, H0, v1, e1, c1 = plano_mapa(carimbos, base)
    _d, _L, _W, _H, _v2, e2, _c2 = plano_mapa(carimbos, base)
    if e1 != e2:
        mau.append("o plano do mapa não é determinista")

    # 10. O PLANO NÃO MEXE EM ELEVAÇÃO, NÃO ABRE PASSAGEM E NÃO PARTE A CIDADE.
    at_novo = _ler("metatile_attributes.bin")
    for i, (a, b) in e1.items():
        if (a >> 12) != (b >> 12):
            mau.append("o plano mexeu na elevação de (%d,%d)" % (i % W0, i // W0))
        if ((a >> 10) & 3) and not ((b >> 10) & 3):
            mau.append("o plano abriu passagem em (%d,%d)" % (i % W0, i // W0))
    if c1["ligacao"]:
        mau.append("o plano parte a cidade: " + "; ".join(c1["ligacao"]))
    mau += defeitos_de_planta(base, v1, W0, H0, at_novo, at_novo)

    # 11. A RÉGUA CHEGA NO TETO DA ONDA, e o dominante NOVO é o calçamento creme
    #     da avenida, que esta rodada não mexe.
    liso, mt, n = regua(v1, W0, H0, L0)
    if liso > TETO_REGUA:
        mau.append("a régua planejada é %.1f%% e o teto é %.1f%%" % (liso, TETO_REGUA))

    # ---------------------------------------------------------- as SABOTAGENS
    # Daqui para baixo o auto-teste ESTRAGA o resultado de propósito e exige que
    # o portão acuse. Caso que não é sabotado não prova portão, prova desenho.
    def sabota(nome, v_sab, at_sab, espera):
        achados = defeitos_de_planta(base, v_sab, W0, H0, at_novo, at_sab)
        if not any(espera in x for x in achados):
            mau.append("SABOTAGEM %s passou: esperava um achado com %r, veio %s"
                       % (nome, espera, achados[:3] or "nada"))

    # 12. Escrever no mapa um dos DOIS metatiles que são cópia pixel a pixel do
    #     363. Ele derrubaria a régua sem mudar um pixel na tela, que é a regra
    #     8 do briefing. Sem este caso, a tentação existe e passa calada.
    alvo = sorted(e1)[0]
    v_sab = list(v1)
    v_sab[alvo] = (v_sab[alvo] & 0xFC00) | PROIBIDOS[0]
    sabota("12 (cópia do carimbo)", v_sab, at_novo, "CÓPIA PIXEL A PIXEL")

    # 13. Dar `layerType` COVERED a uma peça de CHÃO. A célula continua andável,
    #     então a lente muda e o `portao_planta.py` reprovaria. Foi este caso
    #     que decidiu pôr a tampa do bueiro na camada de BAIXO em vez da de cima.
    at_sab = bytearray(at_novo)
    struct.pack_into("<H", at_sab, (ids_chao[0] - N_META_PRI) * 2, 0x1000)
    sabota("13 (chão em COVERED)", v1, bytes(at_sab), "a lente mudou")

    # 14. Dar `layerType` NORMAL a um MÓVEL. Com NORMAL a camada de cima vai para
    #     o BG1 e desenha ACIMA do boneco: é o achado E3 do `mapas_qa.py`, e
    #     `GoldenrodCity` já tem 14 deles na linha de base, que esta rodada não
    #     pode aumentar.
    solidos = [i for i, (a, b) in e1.items() if (b >> 10) & 3]
    if not solidos:
        mau.append("a sabotagem 14 não achou célula sólida para estragar")
    else:
        mt_movel = v1[solidos[0]] & 0x3FF
        at_sab = bytearray(at_novo)
        struct.pack_into("<H", at_sab, (mt_movel - N_META_PRI) * 2, 0x0000)
        sabota("14 (móvel em NORMAL)", v1, bytes(at_sab), "não é COVERED")

    # 15. Abrir passagem onde havia parede (colisão 1 -> 0). É a regra 1 do
    #     briefing, a única que é proibida SEMPRE e nos dois sentidos de leitura.
    parede = next(i for i in range(W0 * H0) if (base[i] >> 10) & 3)
    v_sab = list(v1)
    v_sab[parede] = base[parede] & 0xF3FF
    sabota("15 (passagem nova)", v_sab, at_novo, "colisão 1 -> 0")

    # 16. Mexer na ELEVAÇÃO de uma célula. Ela tem que ficar intacta em 100% das
    #     palavras, sem exceção.
    v_sab = list(v1)
    v_sab[alvo] = (v_sab[alvo] & 0x0FFF) | (((v_sab[alvo] >> 12) ^ 1) << 12)
    sabota("16 (elevação)", v_sab, at_novo, "elevação mudou")

    # 17. Fechar um corredor de UMA célula de largura. O portão de alcance passa
    #     verde quando há warp dos dois lados (foi o que aconteceu em Snowpoint);
    #     quem acusa é o portão de COMPONENTES, e é ele que este caso exercita.
    antes_c = componentes(base, W0, H0)
    achou_gargalo = False
    for i in range(W0 * H0):
        if (base[i] >> 10) & 3:
            continue
        x, y = i % W0, i // W0
        v_sab = list(base)
        v_sab[i] = (base[i] & 0xF000) | (1 << 10) | (base[i] & 0x3FF)
        if ligacao_intacta(antes_c, componentes(v_sab, W0, H0), {(x, y)}):
            achou_gargalo = True
            break
    if not achou_gargalo:
        mau.append("SABOTAGEM 17 não achou nenhum gargalo no mapa: o portão de "
                   "componentes não está provando nada")

    if mau:
        print("DEMO VERMELHA")
        for x in mau:
            print("  -", x)
        return 1
    print("DEMO VERDE: %d tiles, %d metatiles novos, %d peças de chão, "
          "%d móveis, régua planejada %.1f%%, 17 casos (6 sabotagens)"
          % (len(tiles_novos), len(metas), len(carimbos["chao"]),
             len(carimbos["movel"]), liso))
    return 0


def main():
    a = sys.argv[1:]
    if "--extrai" in a:
        return extrai()
    if "--demo" in a:
        return demo()
    if "--desfazer" in a:
        return desfaz()
    if "--confere" in a:
        ref = "HEAD"
        for i, x in enumerate(a):
            if x == "--ref" and i + 1 < len(a):
                ref = a[i + 1]
        mau = confere(ref)
        if mau:
            print("CONFERÊNCIA VERMELHA contra %s" % ref)
            for x in mau:
                print("  -", x)
            return 1
        print("CONFERÊNCIA VERDE contra %s" % ref)
        return 0
    return roda("--aplicar" in a)


if __name__ == "__main__":
    sys.exit(main())
