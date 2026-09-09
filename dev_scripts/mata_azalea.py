#!/usr/bin/env python3
"""Refino de `AzaleaTown` (tema VILA DA MATA), sem importar um pixel de fora.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: 17,7% do chão andável a pé (103 células de 583) é UM
metatile, o 9. Azalea já entrava na onda ABAIXO do teto de 20%, então o alvo aqui
nunca foi o número: é a CARA da cidade. Azalea é a vila da FLORESTA, com a Ilex
Forest de um lado, o poço dos Slowpoke do outro e a casa do Kurt no meio, e o que
ela mostra hoje é um gramado liso do tamanho de meio mapa.

E o carimbo de verdade é MAIOR do que a régua mostra, e isso muda o desenho da
rodada. Rendendo os 1.024 metatiles do par e comparando pixel a pixel, o 9 tem
CÓPIAS EXATAS vivas no mapa: o 8 (42 células), o 0 (24) e o 188 (58). São quatro
ids diferentes para a MESMA imagem de 16x16, e a régua, que conta por id, lê
17,7% onde o olho vê 227 células de 583, ou seja 38,9% de gramado idêntico. Os
quatro existem porque o ATRIBUTO deles é diferente, e é o atributo, não o
desenho, que separa um do outro:

    metatile 9    attr 0x0007   MB_SHORT_GRASS, layerType NORMAL
    metatile 8    attr 0x0000   MB_NORMAL,      layerType NORMAL
    metatile 0    attr 0x0000   MB_NORMAL,      layerType NORMAL
    metatile 188  attr 0x1000   MB_NORMAL,      layerType COVERED

Isso é o que obriga esta passada a escrever a MESMA variante três vezes, uma por
atributo: a regra 3 da onda cobra `(comportamento, layerType)` idêntico em toda
célula que continua andável, então a variante que substitui uma célula do 9 tem
que nascer 0x0007 e a que substitui uma do 188 tem que nascer 0x1000. Não é
truque de régua: é o preço de repintar grama sem mexer no que o motor sente
debaixo do pé.

O ORÇAMENTO DESTA RODADA É ZERO, e essa é a diferença dela para Goldenrod,
Cianwood, Blackthorn e Ecruteak:

    tiles 8x8 novos   ZERO
    cores novas       ZERO
    bytes de ROM      ZERO

Nada é importado. Nada é desenhado. Tudo sai de arte que o cartucho já compilou e
que ninguém escreveu no `map.bin`, exatamente a moeda que a
`dev_scripts/atlas_metatiles.py` existe para garimpar. Medido nesta árvore, o
`gTileset_JohtoSouth` tem 640 metatiles desenhados e a cidade usa 154; o
`gTileset_AzaleaTown` tem 384 e os dois mapas do par (a cidade e a `Route33`)
usam 54, o que deixa 330 vagas de metatile mortas e 240 vagas de tile livres. As
vagas de metatile são gravadas por cima sem que o `metatiles.bin` nem o
`metatile_attributes.bin` mudem de tamanho, e o `tiles.png` não é tocado.

O QUE ENTRA, em duas frentes.

  1. GRAMA MOSQUEADA, catorze arranjos novos, e nenhum deles é escolha de gosto.
     O gramado do 9 são quatro tiles de 8x8 (394, 395, 410 e 411) sempre nos
     mesmos quadrantes, e é essa repetição de 16 em 16 pixels que o olho lê como
     tapete. Varrendo os 640 metatiles do primário, o artista deixou DOIS
     arranjos de grama pura vivos: (394, 395, 410, 411), que é o 9, e
     (620, 621, 19, 637), que é o chão da árvore do metatile 46. Cada quadrante
     desta passada só aceita tile que o artista JÁ pôs naquele quadrante em um
     desses dois, mais os quatro espelhamentos que os bits 10 e 11 da entrada de
     metatile dão de graça:

         quadrante 0   394 ou 620      quadrante 1   395 ou 621
         quadrante 2    19 ou 410      quadrante 3   411 ou 637

     São 8 opções por quadrante, 4.096 arranjos, e os catorze saem por MAIOR
     DISTÂNCIA MÍNIMA de cor aos já escolhidos. O par mais parecido do conjunto
     final fica em 3,43 de distância média por canal, muito acima do piso de
     `PISO_VARIANTE`; o auto-teste reprova qualquer par abaixo dele, porque
     variante com distância zero é variante nenhuma e enganaria a régua sem mudar
     um pixel na tela. Espelhar aqui é seguro e foi conferido em prancha antes de
     virar código: o fundo dos seis tiles é o índice 13 da paleta 0 em todos os
     256 pixels menos os pontinhos, então o espelho move os pontos e não cria
     emenda.

  2. MOBILIÁRIO DE MATA, e nenhuma peça dele é metatile novo: são ids do PRIMÁRIO
     que a cidade não usa, escritos direto no `map.bin`. Custo zero de tudo.

         árvore              46    o mesmo desenho da mata que cerca a cidade
         arbusto escuro    30+31   peça de duas células, a moita alta
         moita redonda      343
         mato baixo          56
         pedra da mata   120+122   a mesma pedra parda que a cidade ja usa
         placa de madeira    57
         cerca de madeira  242, 230, 222, 232, 233, 248, 243

     A cerca é a MESMA família que a cidade já usa: o 230 aparece cinco vezes na
     cerca ao lado do portão da Ilex. As pontas foram medidas e não supostas: o
     242 tem a metade ESQUERDA igual à grama e o poste na direita (ponta de
     início), e o 243 é o espelho disso (ponta de fim).

     Toda peça de mobiliário entra em 0x1000, ou seja comportamento zerado e
     layerType COVERED, que é o que a regra 5 da onda exige de célula
     solidificada: com NORMAL a camada de cima iria para o BG1 e desenharia
     ACIMA do boneco, que é o defeito E3 do `mapas_qa.py`.

ONDE CADA COISA CAI, e nada disso é sorteio solto. Árvore e arbusto escuro só
entram em célula que já tem pelo menos duas vizinhas SÓLIDAS, ou seja na beira da
mata: é assim que a sombra engrossa a orla em vez de virar árvore isolada no meio
do gramado. A placa só entra em célula que encosta na clareira clara (a família
189 a 207, que é a trilha da cidade), porque placa no meio do mato não se lê. A
cerca só entra em corrida horizontal de três a cinco células cujas pontas
encostam em algo sólido, que é como cerca de curral se comporta. E toda célula,
antes de virar sólida, passa por DOIS testes:

  - VÉRTICE DE CORTE (`_liga_sem`): solidificar não pode separar nenhum vizinho
    andável dos outros. Aplicado uma célula por vez sobre o mapa já modificado,
    ele garante por indução que o chão andável nunca se parte, que é o portão (b)
    do `portao_planta.py`.
  - DESVIO (`_sem_desvio`): a peça não pode alongar NENHUMA rota porta a porta em
    mais de `DESVIO_MAX` passos, medido sempre contra a matriz de distâncias do
    master, para que o desvio não vá se acumulando peça a peça. As pontas são a
    célula andável colada em cada um dos sete warps (o tile do warp de porta é
    sólido, o jogador nunca pisa nele) mais o meio da faixa andável da beira
    direita, que é por onde a conexão com a `Route33` entra.

O segundo teste existe porque a primeira versão desta passada era LEGAL e RUIM ao
mesmo tempo, e isso só apareceu andando com o boneco: ela pôs uma moita de duas
células atravessada na estrada que sai do portão da Ilex, e o `portao_planta.py`
aprovou, porque havia desvio uma linha abaixo e a cidade continuava inteira. Com
`DESVIO_MAX = 2` a moita ainda passava, porque o desvio custava exatamente dois
passos; com `DESVIO_MAX = 0` ela cai, e o preço disso foi três árvores, três
tufos de mato e uma pedra a menos, medido. Portão não é desenho.

O QUE FICOU DE FORA, e cada recusa está aqui para a próxima cidade não tentar de
novo:

  - TRILHA DE TERRA. A família de areia do primário (208 a 229, 254 a 262) tem
    canto, borda e miolo, e seria a trilha de vilarejo perfeita. Ela NÃO entra
    porque as bordas dela são 0x1000 (COVERED): elas têm grama na camada de baixo
    e a areia com recorte na de cima, e é a camada de cima que faz o dente da
    borda. Pôr uma dessas numa célula que continua andável trocaria o layerType
    NORMAL da clareira por COVERED e reprovaria a regra 3; deixar em NORMAL
    desenharia a areia por cima do boneco. Achatar as duas camadas em uma só
    exigiria tile novo, e o tile novo teria que caber numa paleta só: a areia
    mora na paleta 5 do primário e a grama na 0, e a 5 não tem os quatro verdes
    da nossa grama. Ou seja, a trilha de terra custa tile E cor, e o orçamento
    desta cidade é zero. A trilha que Azalea tem continua sendo a clareira clara
    (189 a 207), que já liga o portão da Ilex, a casa do Kurt, o Centro, o
    Mercado, o Ginásio e a Rota 33.
  - QUEBRAR A CLAREIRA. O segundo carimbo é o 198, com 59 células. Ele NÃO é
    tapete: junto com 190, 197, 199 e 206 ele forma a hachura diagonal que o
    artista desenhou para a clareira, com espelhamento e tudo. Mexer nele
    desmancharia um desenho que está certo, e depois desta passada ele fica em
    torno de 11%, longe do teto.
  - BAGA E MOITA ANDÁVEL. O 438, o 439 e o 471 são moitas de baga bonitas, mas
    o comportamento delas é 0xA1 (solo de árvore de baga), que o motor liga a
    object_event de baga. Sem o evento correspondente, elas seriam cenário com
    comportamento mentiroso, e a lente é justamente quem reprova isso.
  - PEDRA BRANCA. Os metatiles 440 e 456 são um entulho de laje clara que cabia
    no orçamento e foi POSTO no mapa antes de ser recusado no render: sobre o
    gramado verde ele lê como papel amassado, e briga com a pedra PARDA que a
    cidade já usa (120 e 122, três vezes cada, ao lado do portão da Ilex). Pedra
    de fora não é falta de vaga, é falta de coerência de material, e por isso o
    catálogo ficou com a pedra parda da própria cidade.
  - CLAREIRA DE TERRA SÓLIDA. Os 208, 210, 224 e 226 são manchas de areia
    COVERED sobre grama e caberiam no orçamento, mas mancha de terra em que o
    jogador não pode pisar é defeito de sensação, não enfeite.

Uso:
    python3 dev_scripts/mata_azalea.py            # planeja e mostra, sem gravar
    python3 dev_scripts/mata_azalea.py --aplicar  # grava tileset e map.bin
    python3 dev_scripts/mata_azalea.py --desfazer # volta o map.bin ao master
    python3 dev_scripts/mata_azalea.py --prancha  # a prancha de grama, em PNG
    python3 dev_scripts/mata_azalea.py --demo     # auto-teste (bloco T206)
"""
import collections
import itertools
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)

PLANO = f"{RAIZ}/dev_scripts/mata_azalea.json"
DESTINO = f"{RAIZ}/data/tilesets/secondary/azalea_town"

PRIMARIO = "gTileset_JohtoSouth"
SECUNDARIO = "gTileset_AzaleaTown"
ALVO = "AzaleaTown"
# Os DOIS layouts que dividem o gTileset_AzaleaTown. A rota e a prova de nao
# regressao: ela tem que renderizar com ZERO pixel diferente.
IRMAOS = ["AzaleaTown", "Route33"]

N_META_PRI = 640          # bigPrimary de Johto, de include/fieldmap.h
N_TILES_PRI = 640
TETO_META = 384
TETO_REGUA = 20.0
PISO_VARIANTE = 2.0       # distancia RGB media minima entre duas variantes

# O gramado chapado: quatro ids, UMA imagem. O valor e o atributo de cada um, e o
# auto-teste confere os dois lados (que a imagem e a mesma e que o atributo e
# esse) contra os arquivos em disco, em vez de acreditar neste dicionario.
CHAPADO = {9: 0x0007, 8: 0x0000, 0: 0x0000, 188: 0x1000}
REFERENCIA = 9

# A clareira clara, que e a trilha da cidade. Nao e mexida; serve so para dizer
# onde a placa pode ficar.
CLAREIRA = set(range(189, 208))

# Os quadrantes da grama: tile que o artista JA pos naquele quadrante em um
# metatile de grama pura do primario. Sai de varrer os 640, nao de gosto.
QUADRANTES = [(394, 620), (395, 621), (19, 410), (411, 637)]
ESPELHOS = [0x000, 0x400, 0x800, 0xC00]
QUANTAS_VARIANTES = 14

# Mobiliario: id de metatile do PRIMARIO que a cidade nao usa. `mata` exige beira
# de floresta, `beira` exige encostar na clareira.
# A ordem IMPORTA e nao e estetica: a peca de DUAS celulas e a cerca precisam de
# vizinhanca inteira e sao servidas primeiro; depois delas, o espacamento de 2
# celulas entre pecas ja nao deixaria par livre nenhum (medido: 1 de 6).
MOVEIS = [
    dict(nome="placa de madeira", mt=57,             quantos=3,  espaco=10, beira=True),
    dict(nome="arbusto escuro",   mt=30,   par=31,   quantos=6,  espaco=5, mata=True),
    dict(nome="arvore",           mt=46,             quantos=18, espaco=3, mata=True),
    dict(nome="pedra da mata",    mt=120,  par=122,  quantos=4,  espaco=7),
    dict(nome="moita redonda",    mt=343,            quantos=11, espaco=4),
    dict(nome="mato baixo",       mt=56,             quantos=9,  espaco=4),
]
# A cerca de madeira, a MESMA familia que a cidade ja usa no portao da Ilex.
CERCA_INICIO = 242        # metade esquerda igual a grama, poste na direita
CERCA_MEIO = [230, 222, 232, 233, 248]
CERCA_FIM = 243           # o espelho do 242
CERCAS_QUANTAS = 4
CERCA_MIN, CERCA_MAX = 3, 5

# Quantos passos a mais uma peca pode custar na pior rota porta a porta.
DESVIO_MAX = 0

N4 = [(0, -1), (1, 0), (0, 1), (-1, 0)]
N8 = [(dx, dy) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dx, dy) != (0, 0)]


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair identico em qualquer maquina e em qualquer versao de Python."""
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


def _attr_pri(_c={}):
    if not _c:
        import render_maps as RM
        caminho = os.path.join(RM.caminho_tileset(PRIMARIO), "metatile_attributes.bin")
        _c["b"] = open(caminho, "rb").read()
    return _c["b"]


def entradas_de(mid, metas_novos=None):
    """As 8 palavras de um metatile, do primario ou do secundario."""
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


def pixels_por_entradas(ents):
    """Os 256 pixels RGB de um metatile descrito por 8 palavras.

    Le do MESMO carregador do `render_maps.py`, de proposito: se a leitura
    divergir do render, o auto-teste passa a medir uma segunda verdade.
    """
    import render_maps as RM
    from PIL import Image
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    pals = {i: (tp["paletas"] if i < 7 else ts["paletas"]).get(i, [(0, 0, 0)] * 16)
            for i in range(16)}
    im = Image.new("RGB", (16, 16), (0, 0, 0))
    p = im.load()
    for cam in range(2):
        for q in range(4):
            v = ents[cam * 4 + q]
            tid = v & 0x3FF
            if cam and not tid:
                continue
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, RM.resolver_tile(tp, ts, tid),
                             pals[(v >> 12) & 0xF], bool(v & 0x400), bool(v & 0x800))
    return [[im.getpixel((x, y)) for x in range(16)] for y in range(16)]


def pixels_de(mid, metas_novos=None):
    return pixels_por_entradas(entradas_de(mid, metas_novos))


def distancia(a, b):
    """Distancia media por canal entre dois metatiles de 16x16."""
    s = 0
    for y in range(16):
        for x in range(16):
            s += abs(a[y][x][0] - b[y][x][0]) + abs(a[y][x][1] - b[y][x][1]) + \
                 abs(a[y][x][2] - b[y][x][2])
    return s / (256.0 * 3)


def blockdata_base(mapa):
    """As palavras do `map.bin` do MASTER, mesmo com a passada ja aplicada.

    Existe porque `vagas_mortas()` NAO pode olhar para o disco de hoje: depois de
    `--aplicar`, as vagas que esta passada escreveu passariam a contar como
    vivas, a segunda rodada escolheria OUTRAS vagas e deixaria as primeiras para
    tras. Idempotencia aqui nao e elegancia, e a diferenca entre rodar duas vezes
    e sujar o tileset com dezenas de metatiles orfaos.
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
    """Os locais do secundario que NEM a cidade NEM a Route33 usam.

    A `Route33` entra na conta por disciplina, nao por efeito: medido nesta
    arvore, ela divide o gTileset_AzaleaTown com a cidade e usa ZERO metatile do
    secundario (so os 30 do primario que a cidade nao usa). Ou seja, as 330 vagas
    mortas dao o mesmo numero com e sem ela, e a prova de "0 pixel na irma" que
    fechou Ecruteak e Goldenrod seria VAZIA POR CONSTRUCAO aqui. O auto-teste diz
    isso na cara em vez de anunciar uma prova que nao prova nada, e a sabotagem
    do bloco T206 passa a usar as 54 vagas que a PROPRIA cidade usa.
    """
    if not _c:
        vivos = usados_por(IRMAOS)
        _c["v"] = [m - N_META_PRI for m in range(N_META_PRI, N_META_PRI + TETO_META)
                   if m not in vivos]
    return list(_c["v"])


# ---------------------------------------------------------------- o CATALOGO
def arranjos_vivos(_c={}):
    """Os arranjos de GRAMA PURA que o artista deixou vivos no primario.

    Grama pura e metatile de UMA camada so, com os quatro tiles na familia da
    grama e na paleta 0. Varrer os 640 devolve exatamente dois, e sao eles que
    definem o que cada quadrante aceita.
    """
    if not _c:
        fam = {t for par in QUADRANTES for t in par}
        vistos = []
        for m in range(N_META_PRI):
            e = entradas_de(m)
            if any(v & 0x3FF for v in e[4:]):
                continue
            if not all((v & 0x3FF) in fam and ((v >> 12) & 0xF) == 0 for v in e[:4]):
                continue
            a = tuple(v & 0xFFF for v in e[:4])
            if a not in vistos:
                vistos.append(a)
        _c["v"] = vistos
    return list(_c["v"])


def variantes(_c={}):
    """Os catorze arranjos novos, por MAIOR DISTANCIA MINIMA aos ja escolhidos.

    O espaco nao e livre: cada quadrante so aceita tile que o artista ja pos
    NAQUELE quadrante, mais os quatro espelhamentos. Escolher os quatro tiles por
    distancia sozinha produziria mosaico picado, e a prancha de
    `--prancha` e onde isso foi olhado antes de virar codigo.
    """
    if _c:
        return list(_c["v"])
    opcoes = [[t | f for t in par for f in ESPELHOS] for par in QUADRANTES]
    vivos = arranjos_vivos()
    px = {}

    def P(a):
        if a not in px:
            px[a] = pixels_por_entradas(list(a) + [0, 0, 0, 0])
        return px[a]

    alvo = [P(a) for a in vivos]
    escolhidos = []
    cands = [c for c in itertools.product(*opcoes) if c not in vivos]
    while len(escolhidos) < QUANTAS_VARIANTES:
        melhor = None
        for c in cands:
            if c in escolhidos:
                continue
            dm = min(distancia(P(c), a) for a in alvo)
            if melhor is None or dm > melhor[0] + 1e-9:
                melhor = (dm, c)
        escolhidos.append(melhor[1])
        alvo.append(P(melhor[1]))
    _c["v"] = escolhidos
    return list(escolhidos)


def catalogo(_c={}):
    """Tudo que esta passada escreve no TILESET, com a vaga de cada peca.

    So ha uma coisa a escrever: as variantes de grama, uma vez por ATRIBUTO. As
    vagas saem de `vagas_mortas()` em ordem crescente, o que torna a alocacao
    deterministica e conferivel.
    """
    if _c:
        return _c
    fila = iter(sorted(vagas_mortas()))
    sabores = []
    for a in sorted(set(CHAPADO.values())):
        sabores.append(a)
    novos = {}
    for attr in sabores:
        for k, arr in enumerate(variantes()):
            local = next(fila)
            novos[local] = dict(local=local, attr=attr, arranjo=list(arr),
                                entradas=list(arr) + [0, 0, 0, 0],
                                nome="grama %02d attr 0x%04X" % (k + 1, attr))
    _c.update(novos=novos, sabores=sabores)
    return _c


def variantes_por_attr(attr):
    c = catalogo()
    return [p["local"] + N_META_PRI for p in c["novos"].values() if p["attr"] == attr]


# --------------------------------------------------------- gravar o TILESET
def grava_tileset():
    """Escreve metatiles.bin e metatile_attributes.bin. O tiles.png NAO e tocado.

    Os dois binarios NAO mudam de tamanho: o `metatiles.bin` ja tem as 384
    entradas e esta passada so reescreve vaga morta.
    """
    c = catalogo()
    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    n0, a0 = len(meta), len(attr)
    mortas = set(vagas_mortas())
    for p in c["novos"].values():
        if p["local"] not in mortas:
            raise SystemExit("a vaga %d nao esta morta: escrever nela quebraria "
                             "a Route33" % (p["local"] + N_META_PRI))
        for i, v in enumerate(p["entradas"]):
            struct.pack_into("<H", meta, p["local"] * 16 + i * 2, v)
        struct.pack_into("<H", attr, p["local"] * 2, p["attr"])
    if len(meta) != n0 or len(attr) != a0:
        raise SystemExit("os binarios de metatile mudaram de tamanho")
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------- o PLANO do mapa
def grade(mapa):
    L, d = layout_de(mapa)
    W, H = L["width"], L["height"]
    v = blockdata_base(mapa)
    return v, W, H, L, d


def eventos(d):
    """Toda celula que carrega evento: warp, objeto, placa ou gatilho."""
    s = set()
    for chave in ("object_events", "warp_events", "bg_events", "coord_events"):
        for e in d.get(chave) or []:
            s.add((e["x"], e["y"]))
    return s


def andavel(v, i):
    return ((v[i] >> 10) & 3) == 0


def componentes(v, W, H):
    """Rotulo de componente conexo do chao andavel, com a regra de elevacao do
    `enfeita_cidades.py` (elevacao 0 e curinga)."""
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


def _liga_sem(v, W, H, celulas):
    """True se solidificar `celulas` NAO separa nenhum vizinho andavel delas dos
    outros. E o teste de vertice de corte, e ele e o portao do espalhamento: sem
    ele, uma peca no meio de um corredor de uma celula fecha a cidade."""
    viz = []
    for i in celulas:
        x, y = i % W, i // W
        for dx, dy in N4:
            a, b = x + dx, y + dy
            j = b * W + a
            if 0 <= a < W and 0 <= b < H and j not in celulas and andavel(v, j):
                viz.append(j)
    if len(viz) <= 1:
        return True
    guarda = [v[i] for i in celulas]
    for i in celulas:
        v[i] = (v[i] & ~(3 << 10)) | (1 << 10)
    rot, _ = componentes(v, W, H)
    for i, g in zip(celulas, guarda):
        v[i] = g
    return len({rot[j] for j in viz}) == 1


def distancias(v, W, H, ini):
    """Distancia em passos de `ini` a toda celula andavel, com a regra de
    elevacao do `enfeita_cidades.py`. Celula inalcancavel fica em None."""
    d = [None] * (W * H)
    if not andavel(v, ini):
        return d
    d[ini] = 0
    fila = collections.deque([ini])
    while fila:
        j = fila.popleft()
        x, y = j % W, j // W
        ej = (v[j] >> 12) & 0xF
        for dx, dy in N4:
            a, b = x + dx, y + dy
            if not (0 <= a < W and 0 <= b < H):
                continue
            k = b * W + a
            if d[k] is not None or not andavel(v, k):
                continue
            ek = (v[k] >> 12) & 0xF
            if ej and ek and ej != ek:
                continue
            d[k] = d[j] + 1
            fila.append(k)
    return d


def portas(v, W, H, d):
    """As pontas das rotas que o jogador faz de verdade: a celula andavel colada
    em cada warp, mais o meio da faixa andavel da beira direita, que e por onde a
    conexao com a `Route33` entra."""
    fora = []
    for e in d.get("warp_events") or []:
        x, y = e["x"], e["y"]
        # o warp de porta e SOLIDO (colisao 1): a ponta e a celula ao lado dele
        for dx, dy in [(0, 0), (0, 1), (0, -1), (1, 0), (-1, 0)]:
            a, b = x + dx, y + dy
            if 0 <= a < W and 0 <= b < H and andavel(v, b * W + a):
                fora.append(b * W + a)
                break
    beira = [y * W + (W - 1) for y in range(H) if andavel(v, y * W + (W - 1))]
    if beira:
        fora.append(beira[len(beira) // 2])
    return fora


def matriz(v, W, H, pontas):
    """A distancia porta a porta, em passos. None quando nao ha caminho."""
    fora = {}
    for p in pontas:
        d = distancias(v, W, H, p)
        for q in pontas:
            if q != p:
                fora[(p, q)] = d[q]
    return fora


def plano_mapa():
    """A lista de (indice, palavra_antes, palavra_depois) desta passada."""
    c = catalogo()
    base, W, H, L, d = grade(ALVO)
    v = list(base)
    ev = eventos(d)
    perto_de_warp = set()
    for e in d.get("warp_events") or []:
        for dx, dy in N8 + [(0, 0)]:
            perto_de_warp.add((e["x"] + dx, e["y"] + dy))
    perto_de_objeto = set()
    for e in d.get("object_events") or []:
        for dx, dy in N4 + [(0, 0)]:
            perto_de_objeto.add((e["x"] + dx, e["y"] + dy))
    # AS PORTAS e a distancia porta a porta ANTES de qualquer peca. Toda peca,
    # depois de passar pelo teste de vertice de corte, ainda tem que provar que
    # nao alonga NENHUMA rota porta a porta em mais de `DESVIO_MAX` passos, e a
    # comparacao e sempre contra esta matriz do master, para que o desvio nao va
    # se acumulando peca a peca.
    #
    # Este teste existe porque a primeira versao desta passada era LEGAL e
    # RUIM ao mesmo tempo: ela pos uma moita de duas celulas atravessada na
    # estrada que sai do portao da Ilex (o jogador saia da floresta e batia o
    # nariz) e passou em todos os portoes, porque havia desvio uma linha abaixo e
    # a cidade continuava inteira. Portao nao e desenho.
    pontas = portas(base, W, H, d)
    m0 = matriz(base, W, H, pontas)

    escritas = {}

    def _sem_desvio(v, celulas):
        """True se solidificar `celulas` nao alonga nenhuma rota porta a porta em
        mais de DESVIO_MAX passos em relacao ao master."""
        guarda = [v[i] for i in celulas]
        for i in celulas:
            v[i] = (v[i] & ~(3 << 10)) | (1 << 10)
        m = matriz(v, W, H, pontas)
        for i, g in zip(celulas, guarda):
            v[i] = g
        for par, antes in m0.items():
            depois = m.get(par)
            if antes is None:
                continue
            if depois is None or depois - antes > DESVIO_MAX:
                return False
        return True

    def solido(i):
        return not andavel(v, i)

    def vizinhos_solidos(i):
        x, y = i % W, i // W
        n = 0
        for dx, dy in N8:
            a, b = x + dx, y + dy
            if not (0 <= a < W and 0 <= b < H) or not andavel(v, b * W + a):
                n += 1
        return n

    def encosta_clareira(i):
        x, y = i % W, i // W
        for dx, dy in N4:
            a, b = x + dx, y + dy
            if 0 <= a < W and 0 <= b < H and (v[b * W + a] & 0x3FF) in CLAREIRA:
                return True
        return False

    def elegivel(i):
        x, y = i % W, i // W
        if (v[i] & 0x3FF) not in CHAPADO or not andavel(v, i):
            return False
        if (x, y) in ev or (x, y) in perto_de_warp or (x, y) in perto_de_objeto:
            return False

        # celula de beira de mapa nunca recebe peca: a conexao com a Route33
        # entra por la e o portao mede alcance, nao intencao.
        if x < 1 or y < 1 or x + 1 >= W or y + 1 >= H:
            return False
        return vizinhos_solidos(i) <= 3

    def marca(i, mt):
        p = (v[i] & ~0x3FF) | mt
        p = (p & ~(3 << 10)) | (1 << 10)
        escritas[i] = p
        v[i] = p

    postos, colocados = [], []

    # ---------------------------------------------------------------- a CERCA
    corridas = []
    for y in range(1, H - 1):
        x = 1
        while x < W - 1:
            fim = x
            while fim < W - 1 and elegivel(y * W + fim):
                fim += 1
            larg = fim - x
            if larg >= CERCA_MIN:
                for n in range(min(larg, CERCA_MAX), CERCA_MIN - 1, -1):
                    for x0 in range(x, fim - n + 1):
                        cel = [y * W + x0 + k for k in range(n)]
                        # a corrida tem que ENCOSTAR em algo solido dos dois
                        # lados: cerca solta no meio do gramado le como muro.
                        esq = x0 - 1 >= 0 and solido(y * W + x0 - 1)
                        dir_ = x0 + n < W and solido(y * W + x0 + n)
                        if esq or dir_:
                            corridas.append((cel, esq, dir_))
                    break
            x = max(fim, x + 1)
    corridas.sort(key=lambda c: _mistura(c[0][0], len(c[0]), 0xC0FFEE))
    posto = 0
    for cel, esq, dir_ in corridas:
        if posto >= CERCAS_QUANTAS:
            break
        if any(not elegivel(i) for i in cel):
            continue
        x0, y0 = cel[0] % W, cel[0] // W
        if any(max(abs(x0 - a), abs(y0 - b)) < 4 for a, b, _ in postos):
            continue
        if not _liga_sem(v, W, H, cel) or not _sem_desvio(v, cel):
            continue
        for k, i in enumerate(cel):
            if k == 0:
                mt = CERCA_INICIO
            elif k == len(cel) - 1:
                mt = CERCA_FIM
            else:
                mt = CERCA_MEIO[_mistura(i, 0xFE) % len(CERCA_MEIO)]
            marca(i, mt)
            postos.append((i % W, i // W, "cerca de madeira"))
        colocados.append(("cerca de madeira (%d celulas)" % len(cel), x0, y0))
        posto += 1
    cercas_postas = posto

    # ----------------------------------------------------------- o MOBILIARIO
    for peca in MOVEIS:
        alvo = peca["quantos"]
        cands = sorted((i for i in range(W * H) if elegivel(i)),
                       key=lambda i: _mistura(i, peca["mt"], 0x1234))
        posto = 0
        for i in cands:
            if posto >= alvo:
                break
            x, y = i % W, i // W
            if peca.get("mata") and vizinhos_solidos(i) < 2:
                continue
            if peca.get("beira") and not encosta_clareira(i):
                continue
            if any(max(abs(x - a), abs(y - b)) < peca["espaco"]
                   for a, b, n in postos if n == peca["nome"]):
                continue
            if any(max(abs(x - a), abs(y - b)) < 2 for a, b, _ in postos):
                continue
            celulas = [i]
            if peca.get("par"):
                j = i + 1
                if x + 1 >= W or not elegivel(j):
                    continue
                celulas.append(j)
            if not _liga_sem(v, W, H, celulas) or not _sem_desvio(v, celulas):
                continue
            for k, mt in zip(celulas, [peca["mt"]] + ([peca["par"]] if peca.get("par") else [])):
                marca(k, mt)
                postos.append((k % W, k // W, peca["nome"]))
            colocados.append((peca["nome"], x, y))
            posto += 1
        peca["postos"] = posto

    # -------------------------------------------------------- a GRAMA MOSQUEADA
    pools = {}
    for mt, attr in CHAPADO.items():
        pools[mt] = [mt] + variantes_por_attr(attr)
    repintadas = 0
    for i in range(W * H):
        mt = v[i] & 0x3FF
        if mt not in CHAPADO or not andavel(v, i):
            continue
        pool = pools[mt]
        novo = pool[_mistura(i % W, i // W, 0x9E37) % len(pool)]
        if novo != mt:
            escritas[i] = (v[i] & ~0x3FF) | novo
            v[i] = escritas[i]
            repintadas += 1
    return base, v, escritas, colocados, repintadas, cercas_postas, W, H


# ---------------------------------------------------------------- a REGUA
def regua(v, W, H):
    """As mesmas contas de `dev_scripts/regua_cidades.py`, em memoria.

    Fica aqui para o auto-teste medir o plano ANTES de gravar; quem manda no
    numero do relatorio continua sendo a regua do repositorio, rodada em disco.
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
    base, v, escritas, colocados, repintadas, cercas, W, H = plano_mapa()
    antes = regua(base, W, H)
    depois = regua(v, W, H)
    print("AzaleaTown  liso %.1f%% (mt %d, %d andaveis) -> %.1f%% (mt %d, %d andaveis)"
          % (antes["liso"], antes["chao"], antes["andaveis"],
             depois["liso"], depois["chao"], depois["andaveis"]))
    print("            liso3 %.1f%% -> %.1f%%" % (antes["liso3"], depois["liso3"]))
    solidas = sum(1 for k in escritas
                  if ((escritas[k] >> 10) & 3) and not ((base[k] >> 10) & 3))
    print("  variantes de grama: %d arranjos x %d atributos = %d vagas mortas escritas"
          % (QUANTAS_VARIANTES, len(c["sabores"]), len(c["novos"])))
    print("  celulas repintadas: %d   celulas solidificadas: %d   tiles novos: 0   cores novas: 0"
          % (repintadas, solidas))
    for m in MOVEIS:
        print("    %-20s mt %3d  %d de %d" % (m["nome"], m["mt"], m.get("postos", 0),
                                              m["quantos"]))
    print("    %-20s        %d de %d" % ("cerca de madeira", cercas, CERCAS_QUANTAS))
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
                       colocados=colocados, repintadas=repintadas,
                       variantes=[dict(local=p["local"], attr=p["attr"],
                                       arranjo=p["arranjo"])
                                  for p in c["novos"].values()]), f, indent=1)
    print("  gravado: map.bin, metatiles.bin, metatile_attributes.bin "
          "(o tiles.png NAO foi tocado)")
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
          "checkout em data/tilesets/secondary/azalea_town." % n)
    return 0


def prancha(saida=None):
    """A prancha de grama: as variantes espalhadas por hash, para o olho julgar."""
    from PIL import Image
    saida = saida or "/tmp/prancha_grama_azalea.png"
    todos = [tuple(a) for a in arranjos_vivos()] + variantes()
    W, H = 24, 16
    big = Image.new("RGB", (W * 16, H * 16))
    cache = {}
    for y in range(H):
        for x in range(W):
            a = todos[_mistura(x, y, 0x9E37) % len(todos)]
            if a not in cache:
                im = Image.new("RGB", (16, 16))
                p = im.load()
                px = pixels_por_entradas(list(a) + [0, 0, 0, 0])
                for yy in range(16):
                    for xx in range(16):
                        p[xx, yy] = px[yy][xx]
                cache[a] = im
            big.paste(cache[a], (x * 16, y * 16))
    big.resize((W * 16 * 3, H * 16 * 3), Image.NEAREST).save(saida)
    print("prancha em", saida)
    return 0


# ------------------------------------------------------------------ auto-teste
def demo():
    """Auto-teste do bloco T206. Nao checa beleza: checa que o script sabe
    REPROVAR. Varios casos sao SABOTAGEM: se ela passar, a prova nao vale."""
    from PIL import Image
    falhas = []

    def caso(n, cond, msg):
        print(f"  T206.{n} {'ok  ' if cond else 'FALHA'} {msg}")
        if not cond:
            falhas.append(n)

    c = catalogo()

    # 1. o split de Johto lido dos arquivos, nao decorado
    n_meta = len(_ler("metatiles.bin")) // 16
    larg = len(_ler("metatile_attributes.bin")) // n_meta
    caso(1, n_meta == TETO_META and larg == 2,
         "o gTileset_AzaleaTown tem %d metatiles e atributo de %d byte(s)"
         % (n_meta, larg))

    # 2. o CARIMBO de verdade: os quatro ids do gramado sao a MESMA imagem
    ref = pixels_de(REFERENCIA)
    iguais = all(distancia(ref, pixels_de(m)) == 0.0 for m in CHAPADO)
    caso(2, iguais,
         "os metatiles %s tem distancia 0 entre si: sao quatro ids para uma "
         "imagem so" % sorted(CHAPADO))

    # 3. e o ATRIBUTO de cada um e o que este script afirma, lido do disco
    ok = all(attr_de(m) == a for m, a in CHAPADO.items())
    caso(3, ok, "os atributos lidos em disco batem com %s"
         % {m: "0x%04X" % a for m, a in sorted(CHAPADO.items())})

    # 4. so vaga MORTA e escrita, e morta e "nem a cidade nem a Route33 usam"
    mortas = set(vagas_mortas())
    escritas = set(c["novos"])
    caso(4, escritas <= mortas and len(mortas) == 330,
         "as %d vagas escritas estao entre as %d mortas" % (len(escritas), len(mortas)))

    # 5. SABOTAGEM: vaga que a CIDADE usa nao pode passar por morta.
    #    A sabotagem tinha que ser a da rota irma (o caso das cidades anteriores
    #    desta onda), mas aqui ela seria VAZIA POR CONSTRUCAO e isso esta medido:
    #    a `Route33` divide o gTileset_AzaleaTown com a cidade e nao usa NENHUM
    #    metatile do secundario, so os do primario. Prova vazia nao vale, entao
    #    quem faz o papel de sabotagem e o proprio mapa da cidade.
    da_cidade = {m - N_META_PRI for m in usados_por([ALVO]) if m >= N_META_PRI}
    caso(5, da_cidade and not (da_cidade & mortas) and len(da_cidade) == 54,
         "as %d vagas que a cidade usa ficam fora das mortas (a Route33 usa "
         "ZERO metatile do secundario, entao a prova da irma seria vazia)"
         % len(da_cidade))

    # 5b. e o outro lado do mesmo risco: se algum metatile do PRIMARIO apontasse
    #     para tile do secundario, escrever aqui poderia respingar em quem usa o
    #     gTileset_JohtoSouth com OUTRO secundario. Medido: nenhum aponta, e esta
    #     passada nao toca no tiles.png de qualquer forma.
    pinados = {v & 0x3FF for m in range(N_META_PRI)
               for v in entradas_de(m) if (v & 0x3FF) >= N_TILES_PRI}
    caso(51, not pinados,
         "nenhum dos %d metatiles do primario referencia tile do secundario"
         % N_META_PRI)

    # 6. o espaco de arranjo sai do ARTISTA, nao de gosto
    vivos = arranjos_vivos()
    caso(6, len(vivos) == 2 and tuple(vivos[0]) == (394, 395, 410, 411),
         "o primario tem %d arranjos de grama pura vivos, e o primeiro e o do "
         "metatile 9" % len(vivos))

    # 7. nenhuma variante repete outra: distancia RGB >= PISO_VARIANTE
    px = {}
    for k, a in enumerate(variantes()):
        px["v%02d" % k] = pixels_por_entradas(list(a) + [0, 0, 0, 0])
    for k, a in enumerate(vivos):
        px["artista%d" % k] = pixels_por_entradas(list(a) + [0, 0, 0, 0])
    pior = min((distancia(px[a], px[b]), a, b)
               for a, b in itertools.combinations(sorted(px), 2))
    caso(7, pior[0] >= PISO_VARIANTE,
         "o par mais parecido de grama esta a %.2f (piso %.1f): %s x %s"
         % (pior[0], PISO_VARIANTE, pior[1], pior[2]))

    # 8. SABOTAGEM: uma copia do 9 tem que cair no piso do caso 7
    copia = distancia(px["artista0"],
                      pixels_por_entradas(list(vivos[0]) + [0, 0, 0, 0]))
    caso(8, copia == 0.0 and copia < PISO_VARIANTE,
         "uma copia do arranjo do 9 mede distancia %.2f e cairia no piso" % copia)

    # 9. a LENTE: cada variante nasce com o atributo do gramado que ela substitui
    ok = True
    for p in c["novos"].values():
        if p["attr"] not in set(CHAPADO.values()):
            ok = False
        if any(v & 0x3FF for v in p["entradas"][4:]):
            ok = False       # variante e de UMA camada so
    caso(9, ok and sorted(set(p["attr"] for p in c["novos"].values()))
         == sorted(set(CHAPADO.values())),
         "as %d variantes cobrem os atributos %s e nenhuma usa camada de cima"
         % (len(c["novos"]), sorted("0x%04X" % a for a in set(CHAPADO.values()))))

    # 10. mobiliario solidificado tem que ser COVERED, nunca NORMAL
    todos_moveis = [m["mt"] for m in MOVEIS] + [m["par"] for m in MOVEIS if m.get("par")]
    todos_moveis += [CERCA_INICIO, CERCA_FIM] + CERCA_MEIO
    ok = all((attr_de(m) >> 12) == 1 for m in todos_moveis)
    caso(10, ok, "os %d metatiles de mobiliario estao todos em layerType COVERED"
         % len(todos_moveis))

    # 11. SABOTAGEM: 0x0000 e NORMAL e nao passaria no caso 10
    caso(11, (0x0000 >> 12) != 1,
         "0x0000 e NORMAL (camada de cima no BG1, acima do boneco) e reprovaria "
         "no caso 10")

    # 12. as PONTAS da cerca foram MEDIDAS, nao supostas
    g = pixels_de(REFERENCIA)
    ini, fim = pixels_de(CERCA_INICIO), pixels_de(CERCA_FIM)
    esq_ini = sum(1 for y in range(16) for x in range(8) if ini[y][x] != g[y][x])
    dir_fim = sum(1 for y in range(16) for x in range(8, 16) if fim[y][x] != g[y][x])
    caso(12, esq_ini == 0 and dir_fim == 0,
         "o %d tem a metade esquerda igual a grama (ponta de inicio) e o %d a "
         "direita (ponta de fim)" % (CERCA_INICIO, CERCA_FIM))

    # 13. ZERO tile novo e ZERO cor nova: o tiles.png nao e nem aberto para
    #     escrita, e toda entrada nova aponta para tile que ja existe
    im = Image.open(f"{DESTINO}/tiles.png")
    n_tiles = (im.size[0] // 8) * (im.size[1] // 8)
    fora = [v & 0x3FF for p in c["novos"].values() for v in p["entradas"][:4]
            if (v & 0x3FF) >= N_TILES_PRI]
    pals = {(v >> 12) & 0xF for p in c["novos"].values() for v in p["entradas"][:4]}
    caso(13, not fora and pals == {0} and n_tiles == 144,
         "as %d variantes so usam tile do primario na paleta 0; o tiles.png "
         "continua com %d tiles" % (len(c["novos"]), n_tiles))

    # 14. a planta: colisao 1 -> 0 em zero celulas, elevacao intacta
    base, v, escritas, colocados, repintadas, cercas, W, H = plano_mapa()
    abre = sum(1 for i in range(W * H) if ((base[i] >> 10) & 3) and not ((v[i] >> 10) & 3))
    elev = sum(1 for i in range(W * H) if ((base[i] >> 12) & 0xF) != ((v[i] >> 12) & 0xF))
    caso(14, abre == 0 and elev == 0,
         "colisao 1->0 em %d celulas e elevacao mudada em %d" % (abre, elev))

    # 15. a LIGACAO a pe: nenhum componente do chao andavel se parte nem se junta
    r0, n0 = componentes(base, W, H)
    r1, n1 = componentes(v, W, H)
    solidas = {i for i in range(W * H) if andavel(base, i) and not andavel(v, i)}
    par = {}
    ok = True
    for i in range(W * H):
        if not andavel(base, i) or i in solidas:
            continue
        if r0[i] in par and par[r0[i]] != r1[i]:
            ok = False
        par[r0[i]] = r1[i]
    caso(15, ok and len(set(par.values())) == len(par),
         "os %d componentes de antes viraram %d depois, sem partir nem juntar "
         "(%d celulas solidificadas)" % (n0, n1, len(solidas)))

    # 16. SABOTAGEM: solidificar uma celula de corredor tem que ser REPROVADO
    #     pelo teste de vertice de corte que o espalhamento usa
    v2 = list(base)
    corte = None
    for i in range(W * H):
        if andavel(v2, i) and not _liga_sem(v2, W, H, [i]):
            corte = i
            break
    caso(16, corte is not None,
         "existe celula de corte no mapa (%s) e o `_liga_sem` a reprova"
         % (str(None) if corte is None else str((corte % W, corte // W))))

    # 17. celula de EVENTO nunca vira solida
    _, d = layout_de(ALVO)
    ev = eventos(d)
    mau = [(i % W, i // W) for i in escritas
           if (i % W, i // W) in ev and ((escritas[i] >> 10) & 3)
           and not ((base[i] >> 10) & 3)]
    caso(17, not mau, "nenhuma das %d celulas de evento virou solida" % len(ev))

    # 18. a REGUA cai e o carimbo novo nao e o antigo
    a, dp = regua(base, W, H), regua(v, W, H)
    caso(18, dp["liso"] <= TETO_REGUA and dp["liso"] < a["liso"] and dp["chao"] != a["chao"],
         "liso %.1f%% (mt %d) -> %.1f%% (mt %d), teto %.1f%%"
         % (a["liso"], a["chao"], dp["liso"], dp["chao"], TETO_REGUA))

    # 19. IDEMPOTENCIA: rodar duas vezes da o mesmo plano
    base2, v2b, escritas2, _, _, _, _, _ = plano_mapa()
    caso(19, escritas == escritas2 and base == base2,
         "o plano e deterministico: as %d escritas saem iguais na segunda "
         "chamada" % len(escritas))

    # 20. o DESVIO: nenhuma rota porta a porta ficou mais longa
    pontas = portas(base, W, H, d)
    m0, m1 = matriz(base, W, H, pontas), matriz(v, W, H, pontas)
    piores = [(m1[k], m0[k]) for k in m0
              if m0[k] is not None and (m1[k] is None or m1[k] > m0[k])]
    caso(20, not piores,
         "as %d rotas porta a porta (7 warps mais a beira da Route33) tem a "
         "MESMA distancia de antes" % len(m0))

    # 21. SABOTAGEM: a moita atravessada na estrada da Ilex, que a primeira
    #     versao desta passada pos e o portao aprovou, alonga uma rota e por isso
    #     e reprovada aqui. Sem este caso, o teste de desvio nao vale nada.
    v3 = list(base)
    for cel in (16 * W + 10, 16 * W + 11):
        v3[cel] = (v3[cel] & ~(3 << 10)) | (1 << 10)
    m3 = matriz(v3, W, H, pontas)
    pior = max((m3[k] - m0[k]) for k in m0 if m0[k] is not None and m3[k] is not None)
    caso(21, pior > DESVIO_MAX,
         "solidificar (10,16) e (11,16) alonga a pior rota em %d passo(s), acima "
         "de DESVIO_MAX = %d" % (pior, DESVIO_MAX))

    print("  T206: %d casos, %d falha(s)" % (22, len(falhas)))
    return 1 if falhas else 0


def main():
    a = sys.argv[1:]
    if "--demo" in a:
        return demo()
    if "--desfazer" in a:
        return desfaz()
    if "--prancha" in a:
        i = a.index("--prancha")
        return prancha(a[i + 1] if len(a) > i + 1 else None)
    return roda("--aplicar" in a)


if __name__ == "__main__":
    sys.exit(main())
