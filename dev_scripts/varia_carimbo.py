#!/usr/bin/env python3
"""QUEBRA o tapete de chao repetido de uma cidade, trocando parte das celulas do
carimbo dominante por VARIANTES intercambiaveis do mesmo par de tilesets.

O irmao que faltava. A `regua_cidades.py` MEDE o tapete (a coluna `liso`, que e
a fracao de celulas andaveis com o metatile mais comum), a `enfeita_cidades.py`
POE OBJETO em cima dele (arbusto, placa, canteiro), e ninguem QUEBRA o tapete em
si. Esta ferramenta faz so isso: nao acrescenta objeto nenhum, nao inventa
metatile, so troca o piso por outro piso que ja existe no cartucho e que a
colisao nao distingue.

O NUMERO QUE MOTIVA, medido em 06/09/2026. `SnowpointCity` e a cidade mais pobre
das quatro regioes do cartucho 1: 87,9% das celulas andaveis usam UM metatile, e
98,6% usam tres. Celula a celula no `map.bin` dela, o metatile 513 ocupa 724 das
2.312 celulas (31,3%) e mais quatro (528, 529, 520, 521, as metades das arvores
de neve) levam o total a 90%. A cidade de neve do Golden Glazed, que e o doador
da onda 1 do REFINO, usa 275 metatiles distintos em 1.600 celulas e o carimbo
mais comum dela ocupa 211 celulas, 13,2%. O alvo numerico do REFINO e esse: o
carimbo mais comum de uma cidade perto de 13%, nao de 31%.

O QUE E UMA VARIANTE, e por que cada trava existe. Achar "outro chao parecido"
por cor e facil e da errado: o par de tilesets esta cheio de PEDACO DE COISA
MAIOR que tambem e verde ou cinza. As travas abaixo foram medidas nas 58 cidades
do cartucho, e cada uma nasceu de um caso concreto que passou pela trava
anterior:

  - **MESMO (behavior, layerType)**, com as mascaras de `include/global.fieldmap.h`
    (`METATILE_ATTR_BEHAVIOR_MASK` 0x00FF, bits 0 a 7, e
    `METATILE_ATTR_LAYER_MASK` 0xF000, bits 12 a 15). Filtro duro, nunca
    dispensado, nem para variante nomeada em JSON. E ele que garante a regra 4
    da secao 4 do PRD do REFINO: encontro, grama alta, corrida, tudo depende do
    behavior, e trocar arte nao pode mudar caminho.
  - **NUNCA a duplicata pixel a pixel.** No tileset de Floaroma os metatiles 520
    a 527 sao a MESMA flor rosa oito vezes, e 528 a 535 a mesma flor amarela
    oito vezes (medido: distancia zero dentro de cada grupo). Trocar 521 por 523
    derruba a coluna `liso` da regua sem mudar UM PIXEL na tela. Isso e enganar
    a regua, nao enfeitar a cidade, e por isso distancia zero reprova.
  - **BORDA parecida** (media da distancia RGB nas quatro bordas de 16 pixels,
    limite `BORDA_MAX`). A variante vai cair no meio de um tapete do original;
    se a borda dela nao casa, aparece uma costura. E a trava que separa o piso
    de verdade da PONTA DE PENHASCO: em `gTileset_GeneralSinnoh` os metatiles
    211 e 212 sao grama com a faixa marrom do penhasco em cima, tem o mesmo
    behavior da grama e a mesma cor, e soltos no gramado viram risco marrom.
  - **INTERIOR diferente** (limite `DIST_MIN`): se o olho nao ve, a troca nao
    serve para nada. Em `gTileset_Mauville` os metatiles 910, 911 e 932 sao a
    grama do 1 com um pixel de salpico mudado (distancia 7,7): borda perfeita,
    behavior igual, e invisivel em jogo.
  - **COLISAO COMPATIVEL**: a variante tem que aparecer, em algum mapa que use
    este par de tilesets, com o MESMO valor de colisao das celulas que vamos
    trocar. Esta ferramenta preserva os bits 10 a 15 byte a byte, entao pintar
    um metatile solido numa celula andavel produz um arbusto que se atravessa.
    Foi o que quase aconteceu duas vezes: em `HearthomeCity` o metatile 542 e o
    deck de madeira COM UM ARBUSTO em cima, tem borda identica ao deck liso 521
    e passa em tudo, mas nas 94 vezes em que aparece esta sempre com colisao 1;
    em `SootopolisCity` o 721 e a pedra branca IMPASSAVEL do 729 andavel.
  - **TAPETE, e nao pedaco de padrao**: a variante tem que formar, em algum mapa
    do corpus, um bloco 2x2 homogeneo dela mesma. Sem isso entram as pecas de
    emenda: em `VeilstoneCity` o metatile 544 so aparece com o 545 a direita e o
    536 so com o 537 a direita, porque sao a coluna de transicao entre a calcada
    lisa e a calcada com desenho. Espalhados sozinhos, viram lasca.

O ESPALHAMENTO NAO E SORTEIO. Sorteio uniforme por celula produz chuvisco de
televisao, que fica pior do que o tapete liso. O plano usa ruido de valor
(lattice de `PERIODO` celulas, duas oitavas, interpolacao suave), ordena as
celulas por esse ruido e corta nas fracoes alvo: quem fica no vale do ruido vira
variante. Como o ruido e suave, o corte produz MANCHA contigua, e como a fracao
e um corte por posicao na ordem, ela sai exata. Determinismo: mesma semente,
mesmo plano, sempre.

O QUE NUNCA E TOCADO:
  - celula com warp, object_event, bg_event ou coord_event em cima. Trocar a
    arte debaixo de um warp e como o passo 6 da secao 3.3 do PRD morre na
    pratica: o mapa continua funcionando e o jogador deixa de enxergar a porta.
  - a moldura de `MARGEM` celulas na borda do mapa, que e onde moram as costuras
    de conexao entre mapas.
  - celula do carimbo que faz FRONTEIRA com outro metatile (erosao de 1 celula,
    ligavel com `--sem-erosao`). O tapete guarda a propria beirada, e a mancha
    nasce so no miolo, onde nao encosta em emenda nenhuma.

PROVA, e ela roda depois do gerador, nao dentro dele. `verifica()` compara o
`map.bin` de antes com o de depois e reprova se UMA celula tiver os bits 10 a 15
diferentes ou o par (behavior, layerType) diferente. O `--autoteste` roda a
prova positiva E a negativa: fabrica uma troca que muda o behavior (grama alta
virando chao comum) e outra que mexe na colisao, e exige que a verificacao fique
VERMELHA nas duas. Prova positiva sem par negativo nao e prova.

O CASO APLICADO, e por que foi ele. A varredura `--candidatas` sobre as 58
cidades das quatro regioes do cartucho 1 acha SETE carimbos com variante de
verdade, e nao mais que isso: o cartucho quase nao tem variante de chao
sobrando, tanto no Emerald vanilla (a grama do `gTileset_General` e UM metatile)
quanto no demake de Sinnoh (o conversor emite um piso e as emendas dele). As
cidades mais pobres da regua nao tem NENHUMA: `CelesticTown` (liso 72,1%),
`SolaceonTown` (64,3%), `OreburghCity` (61,5%) e `JubilifeCity` (51,4%) saem com
zero variante aprovada, e por isso a onda 1 do REFINO precisa IMPORTAR arte para
elas, nao rearranjar a que existe. Das sete, `SootopolisCity` e `SlateportCity`
sao Hoenn vanilla (decisao da Game Freak, e a regua nao as manda enfeitar),
`CianwoodCity` e `BlackthornCity` mexem em tileset que outra frente esta
alterando, e `FloaromaTown` so tem a flor duplicada. Sobra `VeilstoneCity`: o
carimbo 524 e a calcada lisa da cidade das lojas, 713 celulas, 38,2% do chao
andavel, e a variante 545 e a calcada COM DESENHO do mesmo `gTileset_Veilstone`,
ja usada 263 vezes no proprio mapa, com a mesma colisao e formando bloco 2x2.
Veilstone foi aplicada com `--sem-erosao`: a praca dela e recortada por predio e
escada, e a erosao de 1 celula derrubava as 697 elegiveis para 257, o que
deixava a mancha parecendo mancha de sujeira em vez de trecho de calcada. O
plano grava a escolha, e replanejar o mapa herda ela.

Uso:
    python3 dev_scripts/varia_carimbo.py --mapa VeilstoneCity        # so mede e planeja
    python3 dev_scripts/varia_carimbo.py --mapa VeilstoneCity --aplicar
    python3 dev_scripts/varia_carimbo.py --mapa VeilstoneCity --desfazer
    python3 dev_scripts/varia_carimbo.py --mapa X --variantes lista.json --aplicar
    python3 dev_scripts/varia_carimbo.py --candidatas                # varre as 58 cidades
    python3 dev_scripts/varia_carimbo.py --verificar                 # a prova, sobre o plano
    python3 dev_scripts/varia_carimbo.py --prova-negativa            # a verificacao ficando vermelha
    python3 dev_scripts/varia_carimbo.py --demo                      # = --autoteste
"""
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")

PLANO = f"{RAIZ}/dev_scripts/varia_carimbo.json"

# Mascaras de include/global.fieldmap.h, e nao de memoria.
BEHAVIOR_MASK = 0x00FF          # METATILE_ATTR_BEHAVIOR_MASK, bits 0 a 7
LAYER_MASK = 0xF000             # METATILE_ATTR_LAYER_MASK, bits 12 a 15
LAYER_SHIFT = 12
ID_MASK = 0x03FF                # MAPGRID_METATILE_ID_MASK, bits 0 a 9
ALTO_MASK = 0xFC00              # colisao (10-11) + elevacao (12-15)

MB_TALL_GRASS = 2               # include/constants/metatile_behaviors.h

# Limiares. Todos medidos nas 58 cidades do cartucho 1, nenhum chutado.
PISO_CARIMBO = 5.0              # % de celulas para um metatile ser "carimbo dominante"
BORDA_MAX = 26.0                # distancia RGB media nas bordas
DIST_MIN = 8.0                  # distancia RGB media no metatile inteiro
MARGEM = 2                      # moldura intocada, em celulas
PERIODO = 6                     # celulas por celula do lattice de ruido
FRACAO_ORIGINAL = 0.60          # quanto do carimbo continua sendo o original
SEMENTE = 20260906


# --------------------------------------------------------------- leitura crua
def _layouts(_c={}):
    if not _c:
        d = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
        _c.update({l["id"]: l for l in d["layouts"] if l.get("id")})
    return _c


def _pastas_tileset():
    import arte_ginasios_sinnoh as G
    return G._pastas_tileset()


def atributos(label, _c={}):
    if label not in _c:
        b = open(f"{RAIZ}/{_pastas_tileset()[label]}/metatile_attributes.bin", "rb").read()
        _c[label] = [struct.unpack_from("<H", b, i * 2)[0] for i in range(len(b) // 2)]
    return _c[label]


def chave(pri, sec):
    """metatile -> (behavior, layerType), ou None se o metatile nao existe."""
    ap, asec = atributos(pri), atributos(sec)

    def f(mt):
        t, i = (ap, mt) if mt < 512 else (asec, mt - 512)
        if not (0 <= i < len(t)):
            return None
        a = t[i]
        return (a & BEHAVIOR_MASK, (a & LAYER_MASK) >> LAYER_SHIFT)
    return f


def imagens(pri, sec, _c={}):
    """{metatile: [256 tuplas RGB]}, reusando render_maps.py em vez de reimplementar 4bpp."""
    if (pri, sec) in _c:
        return _c[(pri, sec)]
    import render_maps as RM
    from PIL import Image
    tp, ts = RM.carregar_tileset(pri), RM.carregar_tileset(sec)
    fundo = tp["paletas"][0][0]
    out = {}
    for base, tset in ((0, tp), (512, ts)):
        for i in range(len(tset["metatiles"]) // 16):
            img = Image.new("RGB", (16, 16), fundo)
            px = img.load()
            for k, (it, fh, fv, ip) in enumerate(RM.entradas_metatile(tset["metatiles"], i)):
                t = RM.resolver_tile(tp, ts, it)
                if t is None:
                    continue
                cores = (tp if ip < 6 else ts)["paletas"].get(ip)
                if cores is None:
                    continue
                RM.desenhar_tile(px, (k % 4 % 2) * 8, (k % 4 // 2) * 8, t, cores, fh, fv)
            out[base + i] = [px[x, y] for y in range(16) for x in range(16)]
    _c[(pri, sec)] = out
    return out


def grade(mapa):
    d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json"))
    L = _layouts()[d["layout"]]
    W, H = L["width"], L["height"]
    b = open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read()
    return d, L, W, H, list(struct.unpack_from("<%dH" % (W * H), b, 0))


def grava(L, v):
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(v), *v))


# ---------------------------------------------------------------- distancias
def _media(a, b, indices):
    s = 0.0
    for i in indices:
        p, q = a[i], b[i]
        s += ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2) ** 0.5
    return s / len(indices)


_TODOS = list(range(256))
_BORDAS = [[i for i in range(16)], [240 + i for i in range(16)],
           [y * 16 for y in range(16)], [y * 16 + 15 for y in range(16)]]


def distancia(a, b):
    return _media(a, b, _TODOS)


def borda(a, b):
    return max(_media(a, b, ind) for ind in _BORDAS)


# ------------------------------------------------------------------- o corpus
def corpus(pri, sec, _c={}):
    """Todo (W, H, celulas) de mapa que usa ESTE par de tilesets.

    A evidencia de colisao e a de tapete 2x2 nao podem sair do ar: elas saem de
    onde o proprio cartucho ja usou aquele metatile.
    """
    if (pri, sec) in _c:
        return _c[(pri, sec)]
    saida = []
    for L in _layouts().values():
        if L.get("primary_tileset") != pri or L.get("secondary_tileset") != sec:
            continue
        caminho = f"{RAIZ}/{L['blockdata_filepath']}"
        if not os.path.exists(caminho):
            continue
        W, H = L["width"], L["height"]
        b = open(caminho, "rb").read()
        n = min(W * H, len(b) // 2)
        if n != W * H:
            continue
        saida.append((W, H, list(struct.unpack_from("<%dH" % n, b, 0))))
    _c[(pri, sec)] = saida
    return saida


def _colisoes_vistas(pri, sec, mt, _c={}):
    """{colisao: quantas vezes} com que o metatile aparece no corpus."""
    ch = (pri, sec, mt)
    if ch not in _c:
        c = collections.Counter()
        for _, _, v in corpus(pri, sec):
            for w in v:
                if (w & ID_MASK) == mt:
                    c[(w >> 10) & 3] += 1
        _c[ch] = c
    return _c[ch]


def _e_tapete(pri, sec, mt, _c={}):
    """True se o metatile forma um bloco 2x2 homogeneo em algum mapa do corpus."""
    ch = (pri, sec, mt)
    if ch not in _c:
        achou = False
        for W, H, v in corpus(pri, sec):
            for y in range(H - 1):
                base = y * W
                for x in range(W - 1):
                    i = base + x
                    if ((v[i] & ID_MASK) == mt and (v[i + 1] & ID_MASK) == mt
                            and (v[i + W] & ID_MASK) == mt
                            and (v[i + W + 1] & ID_MASK) == mt):
                        achou = True
                        break
                if achou:
                    break
            if achou:
                break
        _c[ch] = achou
    return _c[ch]


# ---------------------------------------------------------------- as travas
def variantes(pri, sec, carimbo, colisoes_alvo, nomeadas=None):
    """[(metatile, borda, distancia, colisoes_que_aceita)] aprovadas, e as recusas.

    `colisoes_alvo` e o conjunto de valores de colisao das celulas candidatas. A
    trava de colisao e por CELULA, nao por carimbo: uma variante que so foi
    vista com colisao 0 continua valendo, e o plano so a usa nas celulas de
    colisao 0. Em `VeilstoneCity` isso importa: das 713 celulas do carimbo 524,
    seis tem colisao 1 (calcada debaixo de um canto de predio), e cobrar da
    variante que ela tambem sirva para essas seis matava a variacao das outras
    707. `nomeadas` (lista vinda de JSON) pula so as travas que dependem do
    corpus, porque arte importada na onda 1 ainda nao foi usada em lugar nenhum;
    o filtro duro de (behavior, layerType), a duplicata e a borda continuam
    valendo para ela.
    """
    f, IM = chave(pri, sec), imagens(pri, sec)
    alvo = f(carimbo)
    boas, recusas = [], {}
    universo = list(nomeadas) if nomeadas else sorted(IM)
    for o in universo:
        if o == carimbo:
            continue
        if o not in IM or f(o) is None:
            recusas[o] = "nao existe neste par de tilesets"
            continue
        if f(o) != alvo:
            recusas[o] = "behavior/layer %s != %s" % (f(o), alvo)
            continue
        d = distancia(IM[carimbo], IM[o])
        if d < 1e-9:
            recusas[o] = "duplicata pixel a pixel: enganaria a regua sem mudar a tela"
            continue
        if d < DIST_MIN:
            recusas[o] = "interior quase igual (%.1f < %.1f)" % (d, DIST_MIN)
            continue
        b = borda(IM[carimbo], IM[o])
        if b > BORDA_MAX:
            recusas[o] = "borda nao casa (%.1f > %.1f)" % (b, BORDA_MAX)
            continue
        aceita = set(colisoes_alvo)
        if not nomeadas:
            vistas = _colisoes_vistas(pri, sec, o)
            if not vistas:
                recusas[o] = "nunca usado no corpus deste par"
                continue
            aceita = set(colisoes_alvo) & set(vistas)
            if not aceita:
                recusas[o] = ("nunca visto com a colisao das celulas alvo %s (visto com %s)"
                              % (sorted(colisoes_alvo), sorted(vistas)))
                continue
            if not _e_tapete(pri, sec, o):
                recusas[o] = "nao forma bloco 2x2 de si mesmo: e peca de emenda"
                continue
        boas.append((o, round(b, 1), round(d, 1), sorted(aceita)))
    boas.sort(key=lambda t: (t[1], -t[2]))
    return boas, recusas


# ---------------------------------------------------------------- o ruido
def _hash(x, y, semente):
    n = (x * 374761393 + y * 668265263 + semente * 362437) & 0xFFFFFFFF
    n ^= n >> 13
    n = (n * 1274126177) & 0xFFFFFFFF
    n ^= n >> 16
    return n / 4294967296.0


def _suave(t):
    return t * t * (3 - 2 * t)


def _octava(x, y, periodo, semente):
    gx, gy = x // periodo, y // periodo
    fx, fy = _suave((x % periodo) / periodo), _suave((y % periodo) / periodo)
    a = _hash(gx, gy, semente)
    b = _hash(gx + 1, gy, semente)
    c = _hash(gx, gy + 1, semente)
    d = _hash(gx + 1, gy + 1, semente)
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def ruido(x, y, semente=SEMENTE, periodo=PERIODO):
    """Ruido de valor em [0,1), suave, deterministico. Duas oitavas."""
    return (2 * _octava(x, y, periodo, semente)
            + _octava(x, y, max(2, periodo // 2), semente + 7919)) / 3.0


# ---------------------------------------------------------------- o plano
def eventos(d):
    saida = set()
    for k in ("warp_events", "object_events", "bg_events", "coord_events"):
        for e in d.get(k) or []:
            if "x" in e and "y" in e:
                saida.add((e["x"], e["y"]))
    return saida


def fracoes(n, original=FRACAO_ORIGINAL):
    """Fracao alvo de cada variante: o resto de `original`, repartido por 1/(i+1)."""
    if n <= 0:
        return []
    pesos = [1.0 / (i + 1) for i in range(n)]
    total = sum(pesos)
    return [(1.0 - original) * p / total for p in pesos]


def carimbos(v, piso=PISO_CARIMBO):
    """[(metatile, celulas, %)] acima do piso de ocorrencia, do mais comum ao menos."""
    freq = collections.Counter(w & ID_MASK for w in v)
    tot = len(v)
    return [(mt, n, 100.0 * n / tot) for mt, n in freq.most_common()
            if 100.0 * n / tot >= piso]


def plano(mapa, base=None, semente=SEMENTE, nomeadas=None, erosao=True,
          piso=PISO_CARIMBO, quantos=1):
    """{indice: palavra_nova}, mais o relatorio do que foi decidido."""
    d, L, W, H, v = grade(mapa)
    if base is not None:
        v = list(base)
    pri, sec = L["primary_tileset"], L["secondary_tileset"]
    proibidas = eventos(d)
    escritas, relato = {}, []
    for carimbo, n, pct in carimbos(v, piso)[:quantos]:
        celulas = []
        for i, w in enumerate(v):
            if (w & ID_MASK) != carimbo:
                continue
            x, y = i % W, i // W
            if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
                continue
            if (x, y) in proibidas:
                continue
            if erosao and any((v[i + dx + dy * W] & ID_MASK) != carimbo
                              for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                continue
            celulas.append(i)
        colisoes_alvo = {(v[i] >> 10) & 3 for i in celulas}
        boas, recusas = variantes(pri, sec, carimbo, colisoes_alvo, nomeadas)
        relato.append({"carimbo": carimbo, "celulas_no_mapa": n, "pct": round(pct, 1),
                       "elegiveis": len(celulas), "variantes": boas,
                       "recusas": len(recusas)})
        if not boas or not celulas:
            continue
        fr = fracoes(len(boas))
        ordem = sorted(celulas, key=lambda i: (ruido(i % W, i // W, semente), i))
        inicio = 0
        for (mt, _, _, colis), f in zip(boas, fr):
            fim = inicio + int(round(f * len(ordem)))
            for i in ordem[inicio:fim]:
                if ((v[i] >> 10) & 3) in colis:
                    escritas[i] = (v[i] & ALTO_MASK) | mt
            inicio = fim
    return L, W, H, v, escritas, relato


# ---------------------------------------------------------------- a regua
def _agua():
    import enfeita_cidades
    return enfeita_cidades.agua()


def regua(v, pri, sec):
    """(liso, liso3, distintos), as tres colunas de regua_cidades.py."""
    f = chave(pri, sec)
    AG = _agua()
    andavel = [w & ID_MASK for w in v
               if not ((w >> 10) & 3) and (f(w & ID_MASK) or (0, 0))[0] not in AG]
    freq = collections.Counter(andavel)
    tot = len(andavel) or 1
    top = freq.most_common(3)
    return (round(100.0 * top[0][1] / tot, 1),
            round(100.0 * sum(n for _, n in top) / tot, 1),
            len({w & ID_MASK for w in v}))


# ---------------------------------------------------------------- a prova 1
def verifica(antes, depois, pri, sec):
    """[] se a troca preservou tudo. Caminho, e nao arte: bits 10 a 15 e (behavior, layer).

    Verificacao independente do gerador: recebe dois vetores de palavras e nao
    sabe nada de plano, de ruido nem de variante.
    """
    falhas = []
    if len(antes) != len(depois):
        return ["tamanho do map.bin mudou: %d -> %d" % (len(antes), len(depois))]
    f = chave(pri, sec)
    for i, (a, b) in enumerate(zip(antes, depois)):
        if (a & ALTO_MASK) != (b & ALTO_MASK):
            falhas.append("celula %d: bits 10-15 %04X -> %04X" % (i, a & ALTO_MASK, b & ALTO_MASK))
            continue
        ka, kb = f(a & ID_MASK), f(b & ID_MASK)
        if ka != kb:
            falhas.append("celula %d: metatile %d -> %d muda (behavior, layer) %s -> %s"
                          % (i, a & ID_MASK, b & ID_MASK, ka, kb))
    return falhas


# ------------------------------------------------------------ plano em disco
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(mapa, guardado):
    """O `map.bin` SEM a variacao desta ferramenta, para replanejar por cima."""
    _, _, _, _, v = grade(mapa)
    reg = guardado.get(mapa)
    if not reg:
        return v
    v = list(v)
    for i, antigo, novo in reg["celulas"]:
        if v[i] == novo:
            v[i] = antigo
    return v


def desfaz(mapas):
    guardado = carrega_plano()
    for mapa in mapas:
        if mapa not in guardado:
            print("nada a desfazer em", mapa)
            continue
        _, L, _, _, v = grade(mapa)
        v, n = list(v), 0
        for i, antigo, novo in guardado[mapa]["celulas"]:
            if v[i] == novo:
                v[i] = antigo
                n += 1
        grava(L, v)
        print("desfeito %-16s %d celulas" % (mapa, n))
        guardado.pop(mapa)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    return 0


def roda(mapa, aplicar=False, semente=None, nomeadas=None, erosao=None, quantos=1):
    """Replanejar um mapa ja variado herda a semente e a erosao GRAVADAS no plano.

    Sem isso a ferramenta seria uma armadilha: quem rodasse de novo sem repetir
    os mesmos parametros da linha de comando trocaria o desenho calado.
    """
    guardado = carrega_plano()
    anterior = guardado.get(mapa) or {}
    if semente is None:
        semente = anterior.get("semente", SEMENTE)
    if erosao is None:
        erosao = anterior.get("erosao", True)
    base = base_de(mapa, guardado)
    L, W, H, v, escritas, relato = plano(mapa, base, semente, nomeadas, erosao,
                                         quantos=quantos)
    pri, sec = L["primary_tileset"], L["secondary_tileset"]
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    a1, a3, ad = regua(v, pri, sec)
    d1, d3, dd = regua(saida, pri, sec)
    print("%s  %dx%d  %s + %s" % (mapa, W, H, pri, sec))
    for r in relato:
        print("  carimbo %4d: %d celulas (%.1f%%), %d elegiveis, %d variantes %s, %d recusas"
              % (r["carimbo"], r["celulas_no_mapa"], r["pct"], r["elegiveis"],
                 len(r["variantes"]), [x[0] for x in r["variantes"]], r["recusas"]))
    print("  %d celulas trocadas" % len(escritas))
    print("  regua  liso %.1f%% -> %.1f%% | liso3 %.1f%% -> %.1f%% | distintos %d -> %d"
          % (a1, d1, a3, d3, ad, dd))
    falhas = verifica(v, saida, pri, sec)
    print("  prova da preservacao: %s"
          % ("VERDE, %d celulas conferidas" % len(v) if not falhas
             else "VERMELHA, %d falhas: %s" % (len(falhas), falhas[:3])))
    if falhas:
        raise SystemExit("plano reprovado, nada foi gravado")
    if aplicar and escritas:
        guardado[mapa] = {
            "semente": semente, "erosao": erosao,
            "variantes": {str(r["carimbo"]): [x[0] for x in r["variantes"]] for r in relato},
            "celulas": [[i, v[i], escritas[i]] for i in sorted(escritas)]}
        grava(L, saida)
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("  gravado; plano em", os.path.relpath(PLANO, RAIZ))
    return relato, (a1, a3, ad), (d1, d3, dd), escritas


def verificar_plano():
    """A prova 1 sobre o que esta EM DISCO agora, sem confiar no gerador."""
    guardado = carrega_plano()
    if not guardado:
        print("plano vazio: nada gravado por esta ferramenta")
        return 0
    ruim = 0
    for mapa, reg in guardado.items():
        _, L, _, _, agora = grade(mapa)
        antes = list(agora)
        for i, antigo, novo in reg["celulas"]:
            if antes[i] == novo:
                antes[i] = antigo
        falhas = verifica(antes, agora, L["primary_tileset"], L["secondary_tileset"])
        print("%-18s %s" % (mapa, "VERDE, %d celulas" % len(agora) if not falhas
                            else "VERMELHA %d falhas: %s" % (len(falhas), falhas[:3])))
        ruim += len(falhas)
    return 1 if ruim else 0


# ---------------------------------------------------------------- candidatas
def candidatas(piso=PISO_CARIMBO):
    """Varre as cidades da regua e diz quais tem variante sobrando de verdade."""
    import regua_cidades as R
    dentro, _ = R.cidades()
    achados = []
    for regiao, nome in dentro:
        try:
            d, L, W, H, v = grade(nome)
            pri, sec = L["primary_tileset"], L["secondary_tileset"]
            imagens(pri, sec)
        except Exception as e:
            print("  (pulado %s: %s)" % (nome, e))
            continue
        for carimbo, n, pct in carimbos(v, piso)[:3]:
            colisoes = {(w >> 10) & 3 for w in v if (w & ID_MASK) == carimbo}
            boas, _ = variantes(pri, sec, carimbo, colisoes)
            if boas:
                l1, l3, dist = regua(v, pri, sec)
                achados.append((regiao, nome, l1, carimbo, n, round(pct, 1), boas))
    achados.sort(key=lambda t: -t[2])
    for regiao, nome, l1, carimbo, n, pct, boas in achados:
        print("%-7s %-18s liso=%5.1f%%  carimbo %4d (%d cel, %.1f%%) -> %s"
              % (regiao, nome, l1, carimbo, n, pct, boas))
    if not achados:
        print("nenhuma cidade tem variante intercambiavel sobrando")
    return achados


# ---------------------------------------------------------------- autoteste
def demo():
    """Os casos que esta ferramenta existe para acertar, e os que ela tem que reprovar."""
    mau = []
    mapa = "VeilstoneCity"
    d, L, W, H, v = grade(mapa)
    pri, sec = L["primary_tileset"], L["secondary_tileset"]
    f = chave(pri, sec)

    # 1. As mascaras sao as do global.fieldmap.h, e nao as do FRLG.
    if (BEHAVIOR_MASK, LAYER_MASK, LAYER_SHIFT) != (0x00FF, 0xF000, 12):
        mau.append("mascaras diferentes das de include/global.fieldmap.h")

    # 2. PROVA POSITIVA: o plano do mapa alvo preserva tudo. A base e o `map.bin`
    #    SEM a variacao ja gravada, senao o autoteste mediria o proprio efeito.
    partida = base_de(mapa, carrega_plano())
    _, _, _, base, escritas, relato = plano(mapa, base=partida, semente=SEMENTE)
    saida = list(base)
    for i, val in escritas.items():
        saida[i] = val
    if not escritas:
        mau.append("%s: plano vazio, a ferramenta nao mexeu em nada" % mapa)
    falhas = verifica(base, saida, pri, sec)
    if falhas:
        mau.append("prova da preservacao vermelha no caso bom: %s" % falhas[:2])

    # 3. PROVA NEGATIVA A: grama alta virando chao comum tem que REPROVAR.
    #    Sem par negativo, a prova positiva nao vale nada.
    alta = [mt for mt in imagens(pri, sec) if (f(mt) or (0, 0))[0] == MB_TALL_GRASS]
    comum = [mt for mt in imagens(pri, sec) if (f(mt) or (9, 9))[0] == 0]
    if alta and comum:
        sujo = list(base)
        sujo[0] = (base[0] & ALTO_MASK) | comum[0]
        limpo = list(base)
        limpo[0] = (base[0] & ALTO_MASK) | alta[0]
        if not verifica(limpo, sujo, pri, sec):
            mau.append("verifica() aceitou grama alta (%d) virando chao comum (%d)"
                       % (alta[0], comum[0]))
    else:
        mau.append("nao achei grama alta e chao comum no par %s/%s" % (pri, sec))

    # 4. PROVA NEGATIVA B: mexer na colisao tem que REPROVAR.
    sujo = list(base)
    sujo[5] = base[5] ^ 0x0400
    if not verifica(base, sujo, pri, sec):
        mau.append("verifica() aceitou mudanca no bit 10 (colisao)")
    sujo = list(base)
    sujo[7] = base[7] ^ 0x1000
    if not verifica(base, sujo, pri, sec):
        mau.append("verifica() aceitou mudanca no bit 12 (elevacao)")

    # 5. As travas de variante pegam os casos que ja passaram por elas.
    #    5a. duplicata pixel a pixel da flor de Floaroma.
    try:
        boas, rec = variantes("gTileset_GeneralSinnoh", "gTileset_MauvilleSinnoh",
                              521, {0})
        if any(t[0] in (522, 523, 524, 525, 526, 527) for t in boas):
            mau.append("duplicata pixel a pixel da flor de Floaroma foi aprovada")
        if 523 not in rec or "duplicata" not in rec[523]:
            mau.append("a flor 523 nao foi recusada por duplicata: %s" % rec.get(523))
    except Exception as e:
        mau.append("nao consegui medir Floaroma: %s" % e)
    #    5b. o arbusto solido de Hearthome nao pode virar chao andavel.
    try:
        boas, rec = variantes("gTileset_GeneralSinnoh", "gTileset_Hearthome", 521, {0})
        if any(t[0] == 542 for t in boas):
            mau.append("o arbusto solido 542 de Hearthome foi aprovado para celula andavel")
        if 542 not in rec or "colisao" not in rec[542]:
            mau.append("542 recusado pelo motivo errado: %s" % rec.get(542))
    except Exception as e:
        mau.append("nao consegui medir Hearthome: %s" % e)
    #    5c. a peca de emenda 544 de Veilstone nao e tapete.
    boas, rec = variantes(pri, sec, 524, {0})
    if any(t[0] == 544 for t in boas):
        mau.append("a peca de emenda 544 de Veilstone foi aprovada")
    if not boas:
        mau.append("Veilstone perdeu todas as variantes do carimbo 524")

    # 6. Evento e moldura ficam intactos, sempre.
    proib = eventos(d)
    for i in escritas:
        x, y = i % W, i // W
        if (x, y) in proib:
            mau.append("celula (%d,%d) tem evento em cima e foi trocada" % (x, y))
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            mau.append("celula (%d,%d) esta na moldura e foi trocada" % (x, y))

    # 7. Deterministico e reversivel: mesma semente, mesmo plano; e desfazer o
    #    resultado devolve a base byte a byte, que e o que `base_de` faz antes de
    #    replanejar por cima de um mapa ja variado.
    _, _, _, _, outra, _ = plano(mapa, base=partida, semente=SEMENTE)
    if outra != escritas:
        mau.append("mesma semente deu plano diferente")
    volta = list(saida)
    for i, val in escritas.items():
        if volta[i] == val:
            volta[i] = base[i]
    if volta != base:
        mau.append("desfazer o plano nao devolve a base byte a byte")
    _, _, _, _, terceira, _ = plano(mapa, base=volta, semente=SEMENTE)
    if terceira != escritas:
        mau.append("replanejar sobre a base desfeita nao devolve o mesmo plano")

    # 8. Mancha, e nao chuvisco: a maioria das celulas trocadas tem VIZINHA
    #    trocada. Sorteio uniforme com 40% daria ~40% por vizinho; exigimos que
    #    pelo menos 3 de cada 4 celulas trocadas tenham companhia ao lado.
    if escritas:
        trocadas = set(escritas)
        com_companhia = sum(
            1 for i in trocadas
            if any((i + dx + dy * W) in trocadas for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))))
        if com_companhia < 0.75 * len(trocadas):
            mau.append("espalhamento virou chuvisco: so %d de %d celulas tem vizinha trocada"
                       % (com_companhia, len(trocadas)))

    # 9. A regua tem que enxergar a melhora.
    # A coluna `liso` tem que cair. `distintos` NAO precisa subir: em Veilstone a
    # variante 545 ja era usada no mapa, entao o vocabulario nao cresce, so a
    # repeticao cai. Cobrar as duas coisas reprovaria o caso certo.
    a1, a3, ad = regua(base, pri, sec)
    d1, d3, dd = regua(saida, pri, sec)
    if d1 >= a1 or dd < ad:
        mau.append("regua nao melhorou: liso %.1f->%.1f, distintos %d->%d" % (a1, d1, ad, dd))

    if mau:
        print("AUTOTESTE VERMELHO")
        for x in mau:
            print("  -", x)
        return 1
    print("AUTOTESTE VERDE: 9 casos, %d celulas trocadas em %s, liso %.1f%% -> %.1f%%"
          % (len(escritas), mapa, a1, d1))
    return 0


def prova_negativa(mapa="VeilstoneCity"):
    """Mostra a verificacao SAINDO VERMELHA quando ela tem que sair.

    Prova positiva sem par negativo nao e prova: se `verifica()` estivesse
    quebrada e aprovasse tudo, a prova positiva passaria do mesmo jeito.
    """
    _, L, _, _, v = grade(mapa)
    pri, sec = L["primary_tileset"], L["secondary_tileset"]
    f = chave(pri, sec)
    base = base_de(mapa, carrega_plano())
    alta = sorted(mt for mt in imagens(pri, sec) if (f(mt) or (0, 0))[0] == MB_TALL_GRASS)
    comum = sorted(mt for mt in imagens(pri, sec) if (f(mt) or (9, 9))[0] == 0)
    casos = []
    limpo = list(base)
    limpo[0] = (base[0] & ALTO_MASK) | alta[0]
    sujo = list(base)
    sujo[0] = (base[0] & ALTO_MASK) | comum[0]
    casos.append(("grama alta %d virando chao comum %d" % (alta[0], comum[0]), limpo, sujo))
    sujo = list(base)
    sujo[5] = base[5] ^ 0x0400
    casos.append(("bit 10 (colisao) invertido na celula 5", base, sujo))
    sujo = list(base)
    sujo[7] = base[7] ^ 0x1000
    casos.append(("bit 12 (elevacao) invertido na celula 7", base, sujo))
    bom = list(base)
    for i, val in plano(mapa, base=base)[4].items():
        bom[i] = val
    casos.append(("o plano de verdade desta ferramenta", base, bom))
    ruim = 0
    for nome, antes, depois in casos:
        falhas = verifica(antes, depois, pri, sec)
        print("%-46s %s" % (nome, "VERMELHA: %s" % falhas[0] if falhas else "VERDE"))
        if nome.startswith("o plano") and falhas:
            ruim += 1
        if not nome.startswith("o plano") and not falhas:
            ruim += 1
    print("prova negativa %s" % ("REPROVADA" if ruim else "OK: as tres fabricadas ficaram "
                                 "vermelhas e so a troca legitima ficou verde"))
    return 1 if ruim else 0


def main():
    a = sys.argv
    if "--demo" in a or "--autoteste" in a:
        return demo()
    if "--prova-negativa" in a:
        return prova_negativa(a[a.index("--mapa") + 1] if "--mapa" in a else "VeilstoneCity")
    if "--candidatas" in a:
        candidatas()
        return 0
    if "--verificar" in a:
        return verificar_plano()
    mapa = a[a.index("--mapa") + 1] if "--mapa" in a else None
    if "--desfazer" in a:
        return desfaz([mapa] if mapa else list(carrega_plano()))
    if not mapa:
        print(__doc__)
        return 2
    nomeadas = None
    if "--variantes" in a:
        d = json.load(open(a[a.index("--variantes") + 1]))
        nomeadas = d[mapa] if isinstance(d, dict) and mapa in d else d
    semente = int(a[a.index("--semente") + 1]) if "--semente" in a else None
    quantos = int(a[a.index("--carimbos") + 1]) if "--carimbos" in a else 1
    erosao = False if "--sem-erosao" in a else (True if "--com-erosao" in a else None)
    roda(mapa, "--aplicar" in a, semente, nomeadas, erosao, quantos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
