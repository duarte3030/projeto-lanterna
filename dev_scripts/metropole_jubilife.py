#!/usr/bin/env python3
"""Refino de `JubilifeCity` (tema METROPOLE) no `gTileset_RustboroSinnoh`, com
arte importada do `Pokemon Light Platinum`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py` em
08/09/2026: `JubilifeCity` gasta 51,4% do chao andavel a pe (839 celulas de
1.633) com UM metatile, o 699, a calcada creme quadriculada do SECUNDARIO; os
tres mais comuns somam 69,0%. E a metropole de Sinnoh, o mapa mais movimentado
do cartucho depois de Hearthome, e o chao dela e um tapete bege de meio mapa com
predio em cima. Nem um banco, nem um hidrante, nem um canteiro.

A FONTE: `Pokemon Light Platinum`, de WesleyFG, base Ruby (AXVE), md5
7fd2c08735459d99fa23fdaa9b755486, copia privada em
`fontes-mapas/romhacks/light-platinum/`, primario de exterior `0x286CF4` e
secundario `0x286DB4`, o par da METROPOLE do grupo 0 (o mapa de amostra e o
g00m10, 54x44, com praca calcada, fonte, torre de transmissao e predio de
vidro). A ROM nunca entra no repositorio: o que esta versionado e o kit
CONVERTIDO em `dev_scripts/metropole_jubilife_kit.json`, com o tile em nibble ja
reindexado para a vaga nova e a paleta em RGB. `--extrai` confere o md5 ANTES de
ler um byte e para se a copia for outra; `--aplicar` nunca abre ROM nenhuma.

POR QUE ESTE SECUNDARIO E NAO OS OUTROS DOIS TRIADOS. O condutor entregou tres
candidatos e os tres foram desenhados e olhados nesta frente (os atlas estao em
`amostras-tileset/refino/`):

  - `0x286D24` tem piso marrom-acinzentado ((168,144,120) e (144,120,104)) e
    telhado de templo: e bairro antigo, nao metropole.
  - `0x286E14` tem piso VERDE ((80,112,64), (96,136,64)): o mapa que o usa e
    cidade cortada por mato, e o inventario urbano dele e pequeno.
  - `0x286DB4` e o unico com CALCAMENTO DE PRACA desenhado em sistema (miolo de
    paralelepipedo com moldura de quatro lados e quatro cantos), mais hidrante,
    banco de praca, grade, arbusto largo e vaso com arbusto. E ele.

A COR CASA COM A CIDADE, e isso foi medido, nao suposto. A calcada creme de
Jubilife e (238,238,213)/(205,205,164); o calcamento do Light Platinum e
(136,152,184)/(112,136,160)/(104,128,152)/(80,88,120)/(168,192,216), cinza
AZULADO. Sao familias diferentes, e a saida nao foi "espalhar mancha cinza no
creme": foi olhar o resto do mapa. Os PREDIOS de Jubilife ja sao cinza-azulados
(a vaga 12 do nosso secundario e (200,200,208), (168,184,200), (144,160,176),
(120,120,128), (88,88,112), (64,72,104)) e a AVENIDA tambem ((222,230,238) e
(189,205,230)). A cor (64,72,104) e IDENTICA nos dois tilesets. Ou seja, o
calcamento importado entra na familia que a cidade ja tem, e quem estava fora
dela era justamente o tapete creme.

O DESENHO, e ele nao e mancha organica como nas vilas das rodadas anteriores.
Cidade grande nao tem mancha de terra batida: tem PRACA com contorno e PASSEIO
colado na fachada. Sao duas figuras, e as duas vem do proprio Light Platinum:

  - PRACA: retangulo de calcamento com moldura de nove pecas, e a montagem foi
    lida do MAPA do hack (o g00m10), nao adivinhada no atlas. As contagens de
    par que decidem cada lado: (38,46) na vertical 138 vezes e (46,54) 110, o
    que poe o 38 EM CIMA e o 54 EMBAIXO; (47,47) na vertical 67 e (45,45) 52,
    que sao as colunas; (46,46) 192 na horizontal e 120 na vertical, o miolo. Os
    quatro cantos (30, 31, 62, 63) foram fechados por render: das quatro
    combinacoes possiveis so uma fecha a moldura, a que poe 31 no canto noroeste,
    30 no nordeste, 63 no sudoeste e 62 no sudeste.
  - PASSEIO: faixa de UMA celula de piso liso colada na fachada dos predios,
    onde a cidade hoje tem creme. E o que liga as pracas e o que faz o quarteirao
    ler como quarteirao. Tres variantes (61, 243, 332), e nenhuma delas e copia
    pixel a pixel de outra: o 67, o 57 e o 59, que entrariam junto, foram
    CORTADOS por medida (distancia 0,0 entre eles e 3,8 contra o 61, abaixo do
    piso de 8,0 do `varia_carimbo.py`).

O ORCAMENTO, medido nesta arvore e nao herdado de brief. O
`gTileset_RustboroSinnoh` e secundario de TRES layouts (`JubilifeCity`,
`Route203`, `Route204`), layout `emerald`, teto de 512 tiles e 512 metatiles.

  tiles      512 de 512 no `tiles.png`, ZERO livres no fim do arquivo. O
             `compacta_tileset.py` liberaria 48 vagas, e ele NAO foi rodado: a
             medida direta mostra que 194 vagas ja estao livres ONDE ESTAO,
             porque NENHUMA entrada de NENHUM metatile do `metatiles.bin` aponta
             para elas (194 e o mesmo numero que o `compacta_tileset.py` chama de
             morto; o que ele ganha de novo, e o que faz o total dele cair para
             48, e so o encurtamento do arquivo, que os PINOS de animacao em
             448-451 impedem). Escrever num buraco desses nao renumera nada e nao
             encosta em metatile nenhum, nem vivo nem morto. Este kit gasta 27.
  animacao   as vagas 128-159 (agua ao vento) e 448-451 (fonte) sao escritas
             CRUAS na VRAM pelo `TilesetAnim_Rustboro` em tempo de execucao
             (conferido com `dev_scripts/pinos_anim.py`), e por isso estao fora
             da lista de vagas livres por construcao.
  paletas    as sete vagas do secundario sao 6 a 12. Contando o que os PIXELS
             usam, e so nos metatiles VIVOS (os que aparecem no `map.bin` ou na
             borda de um dos tres layouts), sobra muito mais do que a vaga 7: a
             7 esta INTEIRA livre (nenhum metatile vivo pinta com ela; os quatro
             que pintam, os locais 188, 189, 196 e 197, nao aparecem em mapa
             nenhum), a 9 tem 12 indices livres, a 8 tem 8, a 11 tem 6 e a 10
             tem 4. Escrever cor nova num indice que nenhum pixel usa nao muda o
             desenho de nada, por construcao, e o portao de render prova isso nos
             tres mapas. O `compacta_paletas.py` NAO foi usado: ele recusa
             tileset com animacao e, alem disso, o ramo de duplicacao dele erra o
             desenho (o `--autoteste` dele fecha vermelho no `gTileset_Jubilife`
             com 6.704 pixels diferentes).
  metatiles  o `metatiles.bin` tem 360 locais e o maior id que aparece nos tres
             `map.bin` e 870 (local 358). O arquivo CRESCE ate o local 396 (ids
             872 a 908, 37 metatiles), e o script recusa gravar em local cujo id
             apareca em qualquer um dos tres mapas.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHAO NOVO e metatile com arte SO na camada de BAIXO e atributo IGUAL, bit a
    bit, ao do carimbo que ele substitui (0x0000 aqui). Camada de cima em chao
    andavel com layerType NORMAL desenharia ACIMA do jogador, e calcada por cima
    do boneco e defeito, nao enfeite.
  - MOVEL e celula que vira SOLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chao entrada por entrada, e o atributo e comportamento ZERADO
    com layerType COVERED (0x1000), que poe as duas camadas ABAIXO do sprite.
  - TOPO de peca de duas celulas de altura (o arbusto do vaso) continua ANDAVEL,
    herda o atributo INTEIRO do carimbo e leva o nosso chao embaixo.
  - QUADRANTE DE BAIXO SOBE quando o de cima esta vazio (regra do
    `porto_canalave.py`), e quadrante que e CHAO DA FONTE e descartado. O chao da
    fonte e achado por EVIDENCIA: censo dos padroes de camada de baixo do tileset
    inteiro do hack, onde padrao repetido `LIMIAR_CHAO_FONTE` vezes ou mais, e
    padrao de quatro tiles iguais, e piso.
  - Nenhum id de flag, var, script, musica, treinador ou especie e importado.
    Comportamento e id semantico: todo movel entra com o comportamento ZERADO.

A LEI DE COLISAO desta onda: 0 -> 1 e PERMITIDA em celula que nao seja caminho,
warp, evento nem alcance de script, desde que o alcance a pe continue o mesmo;
1 -> 0 e PROIBIDA e fica em ZERO celulas. Elevacao intacta em 100% das palavras.
Os DOIS portoes de alcance rodam NA HORA, peca a peca: busca em largura a partir
de warp e objeto, e casamento de COMPONENTES conexos.

O BLOCO 175 NAO E PULADO. O `enfeita_cidades.corredores_de_teste` pula o proprio
bloco de teste (`175_cidades_enfeitadas`) de proposito, e para uma passada que
nao e a dele isso e um buraco: em `OreburghCity` custou o T175.4, que anda nove
celulas em linha reta e parou numa pedra nova. Aqui o nome e trocado ANTES da
primeira chamada, porque a funcao guarda o resultado em cache.

O QUE FICOU DE FORA, com o motivo:
  - a TOPIARIA do hack SOZINHA (o metatile 23). Ela entrou na primeira versao
    deste kit como peca de uma celula e o render no emulador mostrou o defeito:
    ela e METADE de uma peca. No mapa do hack o 23 aparece 8 vezes e SEMPRE com o
    22 ao lado (8 vezes com o 22 a esquerda, 6 com ele a direita), e os dois sao o
    mesmo desenho 8x8 espelhado. Sozinho, o 23 sai como uma cunha verde chapada
    no meio da calcada. Hoje ele so entra dentro do `arbusto largo`, que e o par
    (22,23). A mesma armadilha pegou o vaso: a primeira versao punha o 294 em
    cima e o 302 embaixo, e o 294 e o VASO, nao a copa. O hack usa (104,294) 5
    vezes e (68,294) 5 vezes, sempre com a copa em cima e o vaso embaixo, e e
    assim que a peca entrou.
  - a FONTE DE AGUA teal do hack (metatiles 85, 93, 109, 110 e 124 a 126). Ela e
    a peca mais bonita do tileset e foi cortada por orcamento de COR: ela pinta
    com a paleta 9 do hack, que traz doze tons novos de verde-agua, e ela sozinha
    comeria a vaga 9 inteira, que e onde mora o verde dos arbustos e o cinza dos
    bancos. Jubilife ja tem duas fontes desenhadas no proprio tileset.
  - a TORRE DE TRANSMISSAO laranja (279 e 287). Ela e alta demais para entrar
    como peca de duas celulas e, mais que isso, Jubilife JA TEM a torre dela (a
    Jubilife TV), e uma segunda torre que nao e entrada de nada e ruido.
  - o POSTE DE LUZ azul (5, 8, 11, 13 e 19): a cidade ja tem oito postes
    desenhados no `gTileset_RustboroSinnoh`, e eles aparecem no render.
  - o metatile 14 (a mudinha), unico candidato que traria a paleta 3 do hack, com
    sete cores so para ele; o arbusto largo e os dois vasos cobrem o mesmo papel.
  - os pisos 67, 57 e 59, por serem copia pixel a pixel um do outro (regra 9).

Uso:
    python3 dev_scripts/metropole_jubilife.py             # mede e mostra o plano
    python3 dev_scripts/metropole_jubilife.py --aplicar   # tileset e mapa
    python3 dev_scripts/metropole_jubilife.py --desfazer  # devolve o map.bin
    python3 dev_scripts/metropole_jubilife.py --demo      # auto-teste
    python3 dev_scripts/metropole_jubilife.py --autoteste # idem
    python3 dev_scripts/metropole_jubilife.py --extrai    # regera o kit da ROM
    python3 dev_scripts/metropole_jubilife.py --so-tileset
"""
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

# Ver o cabecalho: para esta passada o bloco 175 e um bloco de teste como
# qualquer outro. O nome e trocado ANTES da primeira chamada porque
# `corredores_de_teste` guarda o resultado em cache.
E.BLOCO_PROPRIO = "<nenhum bloco e proprio desta passada>"

DESTINO = f"{RAIZ}/data/tilesets/secondary/rustboro_sinnoh"
KIT_JSON = f"{RAIZ}/dev_scripts/metropole_jubilife_kit.json"
PLANO = f"{RAIZ}/dev_scripts/metropole_jubilife.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_RustboroSinnoh"
IRMAOS = ["JubilifeCity", "Route203", "Route204"]
ALVO = "JubilifeCity"

CARIMBO = 699               # metatile do SECUNDARIO: a calcada creme da cidade
TETO_TILES = 512
TETO_META = 512
META_LOCAL_0 = 360          # o `metatiles.bin` tem 360 locais e CRESCE daqui
MARGEM = 2
TETO_REGUA = 20.0
LIMIAR_CHAO_FONTE = 4       # padrao de camada de baixo repetido tanto e piso

# As vagas de tile que a animacao escreve CRUAS na VRAM em tempo de execucao
# (`dev_scripts/pinos_anim.py gTileset_RustboroSinnoh`). Arte do kit nelas nao
# quebra build, nao muda um pixel de render estatico e so apareceria em jogo.
PINOS_ANIM = set(range(128, 160)) | set(range(448, 452))

# ------------------------------------------------------------------- a FONTE
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          pri=0x286CF4, sec=0x286DB4, split=(512, 512, 6),
          mapa="grupo 0 mapa 10, a metropole, 54x44")

# Paleta do hack -> vaga NOSSA. A conta esta no cabecalho: a 10 do hack (o
# calcamento e a grade) e a 0 (o banco e a base do vaso) cabem juntas na vaga 7,
# porque a uniao delas da 14 cores e (64,72,104) e a mesma nas duas; a 1 (o
# laranja do hidrante, 7 cores) vai para a 8, que tem 8 indices livres; a 2 (o
# verde dos arbustos, 9 cores) vai para a 9, que tem 12.
VAGAS_PAL = {10: 7, 0: 7, 1: 8, 2: 9}

# --------------------------------------------------------------------- o PISO
# `chao`: metatile da fonte cuja arte e piso (camada de baixo so). Ele entra
# INTEIRO e a camada de cima fica vazia.
PISO = [
    dict(nome="calcamento",        lp=46),
    dict(nome="calcamento norte",  lp=38),
    dict(nome="calcamento sul",    lp=54),
    dict(nome="calcamento oeste",  lp=45),
    dict(nome="calcamento leste",  lp=47),
    dict(nome="calcamento NO",     lp=31),
    dict(nome="calcamento NE",     lp=30),
    dict(nome="calcamento SO",     lp=63),
    dict(nome="calcamento SE",     lp=62),
    dict(nome="passeio",           lp=61),
]

# ESPELHO DO MIOLO, e ele custa ZERO tile e ZERO cor: e o mesmo desenho com o
# bit 0x400 (horizontal) ou 0x800 (vertical) ligado, e o proprio Light Platinum
# faz isso nos pares dele. O pave do 46 nao e simetrico, e a medida esta aqui:
# contra o original, o espelho horizontal da 10,3 de distancia RGB media, o
# vertical 16,7 e o duplo 19,2, todos acima do piso de 8,0 do
# `varia_carimbo.py`. E o que tira do miolo da praca a cara de papel de parede
# sem gastar uma vaga de tile.
ESPELHOS = [
    dict(nome="calcamento virado",  de="calcamento", eixo="h"),
    dict(nome="calcamento deitado", de="calcamento", eixo="v"),
    dict(nome="calcamento girado",  de="calcamento", eixo="hv"),
]
MIOLOS = ["calcamento", "calcamento virado", "calcamento deitado",
          "calcamento girado"]

# A PRACA: qual peca vai em cada posicao do retangulo. A montagem foi lida do
# mapa g00m10 do hack e fechada por render; ver o cabecalho.
PRACA = dict(miolo=MIOLOS, n="calcamento norte", s="calcamento sul",
             o="calcamento oeste", l="calcamento leste",
             no="calcamento NO", ne="calcamento NE",
             so="calcamento SO", se="calcamento SE")
# Tamanhos tentados, do maior para o menor: praca grande le como praca e praca
# pequena le como remendo, entao a ordem importa.
TAMANHOS = [(9, 7), (8, 6), (7, 6), (7, 5), (6, 5), (6, 4), (5, 5), (5, 4),
            (4, 4), (4, 3)]
TETO_PRACA = 430            # celulas de praca, somando moldura e miolo
FOLGA_PRACA = 1             # celulas de creme entre duas pracas

# O PASSEIO tem UMA peca so, e isso foi decidido por render e nao por economia.
# O 243 e o 332, que entrariam com ele, foram cortados: o 243 tem ARTE na camada
# de cima (piso que desenha ACIMA do jogador nao e piso) e o 332 tem um degrau
# de sombra num canto que, solto numa faixa reta de fachada, vira retalho. Os
# outros lisos do tileset (67, 57 e 59) sao copia pixel a pixel um do outro.
PASSEIO = ["passeio"]
TETO_PASSEIO = 260          # celulas de faixa de passeio colada na fachada
PASSEIO_MIN = 3             # trecho de fachada menor que isso nao vira passeio

# ------------------------------------------------------------------ os MOVEIS
# `grade` sao os metatiles da fonte em ordem de leitura e `solidas` diz quais
# celulas viram SOLIDAS. Peca de uma linha so e solida inteira; no vaso de
# arbusto a linha de CIMA continua andavel, para o jogador passar ATRAS da copa
# e aparecer NA FRENTE do vaso.
MOVEIS = [
    dict(nome="hidrante", grade=[[26]], solidas=[[1]],
         onde="beira", quantos=8, espaco=9),
    dict(nome="hidrante de esquina", grade=[[27]], solidas=[[1]],
         onde="beira", quantos=7, espaco=9),
    dict(nome="hidrante alto", grade=[[28]], solidas=[[1]],
         onde="beira", quantos=7, espaco=9),
    dict(nome="grade", grade=[[9]], solidas=[[1]],
         onde="beira", quantos=7, espaco=8),
    dict(nome="grade com poste", grade=[[21]], solidas=[[1]],
         onde="beira", quantos=6, espaco=8),
    dict(nome="arbusto largo", grade=[[22, 23]], solidas=[[1, 1]],
         onde="qualquer", quantos=8, espaco=8),
    dict(nome="banco", grade=[[24, 25]], solidas=[[1, 1]],
         onde="qualquer", quantos=7, espaco=9),
    dict(nome="vaso de arbusto", grade=[[104], [294]], solidas=[[0], [1]],
         onde="qualquer", quantos=6, espaco=10),
    dict(nome="vaso de pinheiro", grade=[[68], [294]], solidas=[[0], [1]],
         onde="qualquer", quantos=6, espaco=10),
]
ESPACO_ENTRE_MOVEIS = 3     # Chebyshev minimo entre duas pecas QUAISQUER

N4 = E.N4


def papel_de(mv, li, ci):
    """O papel de uma celula de movel, e ele decide de quem e a camada de baixo.

      `topo`   celula que continua ANDAVEL: a camada de baixo e o NOSSO chao.
      `movel`  celula SOLIDA da primeira linha da peca. Objeto de uma celula de
               altura pousa NO chao, entao a camada de baixo tambem e a nossa.
      `base`   celula SOLIDA que nao e a primeira linha; ai a camada de baixo da
               fonte pode ser ARTE de verdade, e o filtro de chao da fonte
               continua valendo tile a tile.
    """
    if not mv["solidas"][li][ci]:
        return "topo"
    return "movel" if li == 0 else "base"


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair identico em qualquer maquina e em qualquer versao de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


def _ler(nome):
    return open(f"{DESTINO}/{nome}", "rb").read()


def _entradas(bin_meta, local):
    return list(struct.unpack_from("<8H", bin_meta, local * 16))


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def _espelha4(quad, eixo):
    """Espelho de uma camada de 4 quadrantes. 'h' troca as colunas e liga 0x400,
    'v' troca as linhas e liga 0x800."""
    fora = list(quad)
    if "h" in eixo:
        fora = [0 if (fora[q] & 0x3FF) == 0 else (fora[q] ^ 0x400)
                for q in (1, 0, 3, 2)]
    if "v" in eixo:
        fora = [0 if (fora[q] & 0x3FF) == 0 else (fora[q] ^ 0x800)
                for q in (2, 3, 0, 1)]
    return fora


def _rgb(ts, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits DESLOCADOS tres
    casas, nao esticados para 0..255.

    A conta importa e ja custou uma rodada nesta pesquisa. As duas contas dao o
    MESMO cinco-bits depois que o `gbagfx` reconverte o `.pal` para `.gbapal`,
    entao a cor dentro da ROM e a mesma; o que muda e o numero escrito no `.pal`
    e, com ele, o pixel de todo render de conferencia. Todo `.pal` do
    `gTileset_RustboroSinnoh` esta na conta de deslocar (216 = 27 << 3,
    184 = 23 << 3), e o `ferramentas/prova_extracao.py` tambem.
    """
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


# ------------------------------------------------------- o que esta VIVO aqui
def metatiles_vivos():
    """Locais de metatile do SECUNDARIO que algum dos tres layouts realmente usa.

    Conta o `map.bin` E a BORDA de cada layout: a borda desenha nas margens da
    tela e nao aparece no `map.bin`. Sem ela, um metatile de borda seria tomado
    por morto e a paleta dele poderia ser reescrita.
    """
    usados = set()
    for nome in IRMAOS:
        d, L, W, H, v = G.grade(nome)
        usados |= {c & 0x3FF for c in v}
        borda = L.get("border_filepath")
        if borda and os.path.exists(f"{RAIZ}/{borda}"):
            b = open(f"{RAIZ}/{borda}", "rb").read()
            usados |= {x & 0x3FF for x in
                       struct.unpack_from("<%dH" % (len(b) // 2), b, 0)}
    return {m - 512 for m in usados if m >= 512}, usados


def vagas_tile_livres():
    """As vagas de TILE do secundario que NENHUM metatile referencia.

    Nao e "tile que so metatile morto usa": e tile que NENHUMA das oito entradas
    de NENHUM dos 360 metatiles do `metatiles.bin` pede, nem vivo nem morto.
    Escrever nelas nao muda o desenho de metatile nenhum, e por isso nao ha
    renumeracao e nao ha `compacta_tileset.py` nesta passada. O tile 0 e os
    pinos de animacao ficam fora.

    Os metatiles que ESTA passada grava (locais de `META_LOCAL_0` para cima)
    ficam de fora da conta, e e isso que torna a alocacao idempotente: depois da
    primeira aplicacao as vagas do kit voltariam a parecer ocupadas e a segunda
    rodada escolheria outras.
    """
    ts = _tileset(SECUNDARIO)
    meta = ts["metatiles"]
    pedidos = set()
    for loc in range(min(len(meta) // 16, META_LOCAL_0)):
        for v in _entradas(meta, loc):
            idx = v & 0x3FF
            if idx >= 512:
                pedidos.add(idx - 512)
    return [i for i in range(len(ts["tiles"]))
            if i and i not in pedidos and i not in PINOS_ANIM]


def vagas_pal_livres():
    """{vaga: [indices de cor que NENHUM pixel VIVO usa]}.

    Vivo e o pixel que algum metatile alcancavel desenha: o metatile aparece no
    `map.bin` ou na borda de um dos tres layouts. Escrever cor nova num indice
    que nenhum pixel vivo usa nao muda o desenho de nada que o jogador veja, e
    o portao de render dos tres mapas prova isso. Os metatiles que ESTA passada
    grava ficam de fora da conta, para que `--extrai` depois de `--aplicar` de o
    mesmo kit.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    loc_vivos, _ = metatiles_vivos()
    usados = collections.defaultdict(set)
    for loc in sorted(loc_vivos):
        if loc >= META_LOCAL_0:
            continue
        for (it, _fh, _fv, ip) in RM.entradas_metatile(ts["metatiles"], loc):
            if it == 0 or ip < 6:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        usados[ip].add(c)
    return {v: [i for i in range(1, 16) if i not in usados[v]]
            for v in range(6, 13)}


# ---------------------------------------------------------------- a EXTRACAO
def extrai():
    """Regera `metropole_jubilife_kit.json` a partir da ROM privada do hack.

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
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s: nao "
                         "leio um byte de uma copia diferente"
                         % (gba, md5, LP["md5"]))
    r = Rom(caminho)
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = LP["split"]
    t1 = r.parse_tileset(LP["pri"])
    t2 = r.parse_tileset(LP["sec"])
    if t1 is None or t2 is None:
        raise SystemExit("o par 0x%X/0x%X do hack nao abriu"
                         % (LP["pri"], LP["sec"]))
    npri = r.n_tiles_pri
    pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}
    n_meta = len(t2["meta"]) // 16
    livres = vagas_pal_livres()

    def ents_de(local):
        return list(struct.unpack_from("<8H", t2["meta"], local * 16))

    def px_de(v):
        idx = v & 0x3FF
        return (_nibbles(t1["tiles"], idx) if idx < npri
                else _nibbles(t2["tiles"], idx - npri))

    def branco(v):
        """A entrada aponta para um tile 8x8 SEM UM PIXEL aceso?

        O `0x0800` que as pecas de calcamento trazem na camada de cima e o tile 0
        com espelho vertical, e ele e todo transparente. Tratar isso como camada
        de cima cheia deixaria a peca vazia.
        """
        if not (v & 0x3FF):
            return True
        return not any(c for linha in px_de(v) for c in linha)

    # O CHAO DA FONTE, por EVIDENCIA e nao por constante decorada: censo dos
    # padroes de camada de baixo do tileset inteiro do hack. Padrao repetido e
    # piso; padrao de arte aparece uma ou duas vezes. Quatro tiles IGUAIS
    # tambem e piso, que e a assinatura que o `neve_snowpoint2.py` ja usava.
    censo = collections.Counter()
    for i in range(n_meta):
        censo[tuple(x & 0x3FF for x in ents_de(i)[:4])] += 1
    chao = set()
    for pat, k in censo.items():
        if k >= LIMIAR_CHAO_FONTE or len({x for x in pat}) == 1:
            chao |= {x for x in pat if x}
    censo_top = [[list(p), k] for p, k in censo.most_common(8)]

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}
    pecas = []

    def guarda(v):
        """Registra o tile de uma entrada e devolve a chave dele.

        A CHAVE LEVA A PALETA DE ORIGEM: o mesmo desenho 8x8 pintado com duas
        paletas do hack sao duas vagas nossas, senao a segunda apaga a primeira.
        """
        idx, ip = v & 0x3FF, (v >> 12) & 0xF
        if ip not in VAGAS_PAL:
            raise SystemExit("a paleta %d do hack nao esta no mapa de vagas" % ip)
        lado, li = ("p", idx) if idx < npri else ("s", idx - npri)
        ch = "%s:%d:%d" % (lado, li, ip)
        destino = VAGAS_PAL[ip]
        if tiles_vaga.setdefault(ch, destino) != destino:
            raise SystemExit("o tile %s foi pedido nas vagas %d e %d"
                             % (ch, tiles_vaga[ch], destino))
        tiles_px[ch] = px_de(v)
        origem = pal[ip]
        tiles_cor.setdefault(ch, set())
        for linha in tiles_px[ch]:
            for c in linha:
                if c:
                    tiles_cor[ch].add(tuple(origem[c]))
        return ch

    quero = [("chao", p["nome"], p["lp"]) for p in PISO]
    for mv in MOVEIS:
        for li, linha in enumerate(mv["grade"]):
            for ci, lp in enumerate(linha):
                quero.append((papel_de(mv, li, ci),
                              "%s %d %d" % (mv["nome"], li, ci), lp))

    for papel, nome, local in quero:
        if local >= n_meta:
            raise SystemExit("%s: o metatile %d nao existe no tileset" % (nome, local))
        ents = ents_de(local)
        attr = struct.unpack_from("<H", t2["attr"], local * 2)[0]
        baixo, cima = ents[:4], ents[4:]
        uniforme = len({v & 0x3FF for v in baixo}) == 1
        usadas, escolhidas = [], []
        for q in range(4):
            vazio_em_cima = branco(cima[q])
            v = baixo[q] if vazio_em_cima else cima[q]
            escolhidas.append(v)
            if papel == "chao":
                if not (v & 0x3FF):
                    raise SystemExit("%s: quadrante vazio em peca de chao" % nome)
                usadas.append(guarda(v))
                continue
            if not (v & 0x3FF):
                usadas.append(None)
                continue
            idx = v & 0x3FF
            li = idx - npri
            if vazio_em_cima and papel in ("movel", "topo") and (
                    uniforme or (idx >= npri and li in chao)):
                usadas.append(None)          # e o chao da fonte: fica de fora
                continue
            if vazio_em_cima and papel == "base" and idx >= npri and li in chao:
                usadas.append(None)
                continue
            usadas.append(guarda(v))
        if papel == "chao":
            # "Tem camada de cima" e ter PIXEL ACESO nela. Cinco das nove pecas
            # de calcamento trazem o tile 1 do primario do hack, ou o tile 0 com
            # espelho, na camada de cima, e os dois sao 100% transparentes: sao
            # entrada morta do dumper, e tratar isso como camada de cima cheia
            # deixaria metade do calcamento de fora.
            if any(not branco(v) for v in cima):
                raise SystemExit("%s: a peca de chao %d tem camada de cima"
                                 % (nome, local))
        elif not any(usadas):
            raise SystemExit("%s: o metatile %d nao sobrou com nenhum quadrante "
                             "de arte" % (nome, local))
        pecas.append(dict(papel=papel, nome=nome, lp=local, attr=attr,
                          ents=escolhidas, usadas=usadas,
                          baixo=baixo, cima=cima))

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
        for k, c in enumerate(cores):
            base[vagos[k]] = list(c)
            indice[(vaga, c)] = vagos[k]
        paletas[str(vaga)] = base

    # REINDEXA cada nibble para a tabela nova. A cor 0 continua 0 e nenhuma cor
    # e aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, so em
    # outro indice, entao o pixel sai identico ao da ROM.
    saida_tiles = {}
    for ch, px in sorted(tiles_px.items()):
        ip = int(ch.split(":")[2])
        vaga = VAGAS_PAL[ip]
        origem = pal[ip]
        saida_tiles[ch] = [[0 if c == 0 else indice[(vaga, tuple(origem[c]))]
                            for c in linha] for linha in px]

    dados = dict(
        fonte=dict(hack=LP["hack"], autor=LP["autor"], base=LP["base"],
                   arquivo=gba, md5=md5, pri="0x%X" % LP["pri"],
                   sec="0x%X" % LP["sec"], mapa=LP["mapa"],
                   split=list(LP["split"]), n_tiles_pri=npri),
        vagas_livres={str(k): v for k, v in livres.items()},
        vagas_pal={str(k): v for k, v in VAGAS_PAL.items()},
        paletas=paletas, tiles=saida_tiles, tiles_vaga=tiles_vaga,
        chao_da_fonte=sorted(chao), censo_chao=censo_top, pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d pecas"
          % (os.path.relpath(KIT_JSON, RAIZ), len(saida_tiles), len(pecas)))
    for vaga, cores in sorted(por_vaga.items()):
        print("  vaga %2d: %2d cores nos indices %s (de %d livres)"
              % (vaga, len(cores), [indice[(vaga, c)] for c in sorted(cores)],
                 len(livres.get(vaga) or [])))
    print("  chao da fonte: %d tiles; padroes mais repetidos: %s"
          % (len(chao), ", ".join("%s x%d" % ([hex(z) for z in p], k)
                                  for p, k in censo_top[:3])))
    return 0


# --------------------------------------------------------------- o KIT em disco
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def chao_nosso():
    """As quatro entradas da camada de BAIXO do carimbo, mais o atributo dele.

    E o chao que todo movel pousa em cima e o que toda peca de duas celulas leva
    embaixo. O carimbo de Jubilife e do SECUNDARIO, nao do primario: o metatile
    699 e o local 187 do `gTileset_RustboroSinnoh`.
    """
    ts = _tileset(SECUNDARIO)
    local = CARIMBO - 512
    ents = _entradas(ts["metatiles"], local)
    if any(v & 0x3FF for v in ents[4:]):
        raise SystemExit("o carimbo %d ja usa a camada de cima" % CARIMBO)
    attr = G._attrs(SECUNDARIO)[local]
    if attr & 0xFF:
        raise SystemExit("o carimbo %d tem comportamento 0x%02X e esta rodada "
                         "supoe chao normal" % (CARIMBO, attr & 0xFF))
    return ents[:4], attr


def desenha_kit():
    """(tiles_novos, metas, attrs, carimbos) sem escrever nada em lugar nenhum.

    `tiles_novos` e {vaga: nibbles}, e as vagas saem da lista de buracos do
    `tiles.png` em ordem crescente, que e fixa enquanto ninguem mexer nos 360
    metatiles antigos.
    """
    dados = kit()
    base, attr_chao = chao_nosso()
    meta_disco = _ler("metatiles.bin")
    por_peca = {(p["papel"], p["nome"]): p for p in dados["pecas"]}
    buracos = vagas_tile_livres()
    tiles_novos, mapa_tile, usadas_ordem = {}, {}, []
    metas, attrs = {}, {}
    proximo_meta = [META_LOCAL_0]
    carimbos = {"chao": [], "moveis": []}

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            if len(usadas_ordem) >= len(buracos):
                raise SystemExit("acabaram as %d vagas de tile livres"
                                 % len(buracos))
            mapa_tile[chave] = buracos[len(usadas_ordem)]
            usadas_ordem.append(chave)
            tiles_novos[mapa_tile[chave]] = dados["tiles"][chave]
        return mapa_tile[chave]

    def poe(ents, attr):
        local = proximo_meta[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return 512 + local

    def entrada(p, q):
        """A entrada NOSSA para o quadrante q: mesmo tile, vaga nova, vaga de
        paleta nova, e os bits de espelho da fonte preservados."""
        ch = p["usadas"][q]
        if ch is None:
            return None
        v = p["ents"][q]
        alvo_pal = VAGAS_PAL[int(ch.split(":")[2])]
        return ((v & 0x0C00) | (512 + vaga(ch)) | (alvo_pal << 12))

    # ------------------------------------------------------------------ CHAO
    entradas_chao = {}
    for c in PISO:
        p = por_peca[("chao", c["nome"])]
        ents = [entrada(p, q) for q in range(4)]
        if any(e is None for e in ents):
            raise SystemExit("%s: quadrante vazio em peca de chao" % c["nome"])
        entradas_chao[c["nome"]] = ents
        gid = poe(ents + [0, 0, 0, 0], attr_chao)
        carimbos["chao"].append(dict(nome=c["nome"], mt=gid, lp=c["lp"]))
    for c in ESPELHOS:
        ents = _espelha4(entradas_chao[c["de"]], c["eixo"])
        gid = poe(ents + [0, 0, 0, 0], attr_chao)
        carimbos["chao"].append(dict(nome=c["nome"], mt=gid,
                                     espelho_de=c["de"], eixo=c["eixo"]))

    # ---------------------------------------------------------------- MOVEIS
    # CADA MOVEL SAI EM DUAS VERSOES, e elas diferem SO na camada de baixo: uma
    # pousa na calcada creme (o carimbo) e outra no calcamento da praca. Sem a
    # segunda, banco, hidrante e vaso ficariam todos fora das pracas, que e
    # justamente onde mobiliario urbano mora; com ela, o fundo do movel e sempre
    # o piso que aquela celula teria, e nunca o chao da FONTE. O fundo de praca
    # e o `calcamento` sem espelho: os vizinhos podem ser espelhados, e a junta
    # do pave nao casa em um ou dois pixels, o que a olho nu nao aparece porque
    # o movel cobre o miolo do quadrado.
    FUNDOS = {"carimbo": list(base), "calcada": list(entradas_chao["calcamento"])}
    feito = {}
    for mv in MOVEIS:
        grades = {}
        for fundo, ents_fundo in sorted(FUNDOS.items()):
            grade = []
            for li, linha in enumerate(mv["grade"]):
                saida = []
                for ci, lp in enumerate(linha):
                    papel = papel_de(mv, li, ci)
                    # o MESMO metatile da fonte no MESMO papel e com o MESMO
                    # fundo e uma vaga so: o vaso 294 e a base dos dois vasos.
                    chave_mt = (papel, lp, fundo)
                    if chave_mt in feito:
                        saida.append(feito[chave_mt])
                        continue
                    p = por_peca[(papel, "%s %d %d" % (mv["nome"], li, ci))]
                    cima = [entrada(p, q) or 0 for q in range(4)]
                    if not any(cima):
                        raise SystemExit("%s: celula sem arte" % mv["nome"])
                    # comportamento ZERADO (regra 5: nenhum id semantico e
                    # importado) e layerType COVERED nas solidas; a celula que
                    # continua andavel herda o atributo INTEIRO do carimbo.
                    solida = bool(mv["solidas"][li][ci])
                    feito[chave_mt] = poe(list(ents_fundo) + cima,
                                          0x1000 if solida else attr_chao)
                    saida.append(feito[chave_mt])
                grade.append(saida)
            grades[fundo] = grade
        carimbos["moveis"].append(dict(nome=mv["nome"], grades=grades,
                                       solidas=mv["solidas"], onde=mv["onde"],
                                       quantos=mv["quantos"],
                                       espaco=mv["espaco"]))

    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles" % TETO_TILES)
    if proximo_meta[0] > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)
    if set(tiles_novos) & PINOS_ANIM:
        raise SystemExit("o kit caiu em vaga de PINO de animacao: %s"
                         % sorted(set(tiles_novos) & PINOS_ANIM))

    # A vaga de metatile so serve se estiver ALEM do fim do arquivo, se for
    # ENCHIMENTO do dumper, ou se ja tiver o que este kit escreve (rodar duas
    # vezes), e NENHUM dos tres mapas pode usar o id.
    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    _loc_vivos, usados = metatiles_vivos()
    n_disco = len(meta_disco) // 16
    for local, ents in metas.items():
        gid = 512 + local
        # A vaga so serve se estiver ALEM do fim do arquivo, se for ENCHIMENTO do
        # dumper, ou se ja tiver exatamente o que este kit escreve. Este ultimo
        # caso e o de rodar duas vezes: depois de `--aplicar` o mapa passa a usar
        # os ids do kit, e sem esta ressalva a segunda rodada acusaria a si
        # mesma.
        nosso = (local < n_disco and _entradas(meta_disco, local) == ents)
        if gid in usados and not nosso:
            raise SystemExit("algum dos tres mapas ja usa o metatile %d" % gid)
        if local < n_disco and not nosso:
            antigo = _entradas(meta_disco, local)
            if not enchimento(antigo):
                raise SystemExit("a vaga de metatile %d ja esta ocupada" % gid)
    return tiles_novos, metas, attrs, carimbos


def _grava_pal(vaga, cores):
    with open(f"{DESTINO}/palettes/%02d.pal" % vaga, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    Os dois `.bin` CRESCEM: o `metatiles.bin` desta pasta tem 360 locais e o kit
    mora a partir do 360. O que entra no meio, se sobrar buraco, e o padrao de
    ENCHIMENTO do dumper (as oito entradas iguais a 1), que e o que o resto do
    repositorio usa como vaga vazia.
    """
    from PIL import Image
    dados = kit()
    antigo = Image.open(f"{DESTINO}/tiles.png")
    if antigo.mode != "P":
        raise SystemExit("o tiles.png nao esta paletizado (modo %s)" % antigo.mode)
    # `Image.convert("P")` numa imagem que JA e "P" devolve uma COPIA, e escrever
    # nela nao muda o arquivo que se salva depois. Foi assim que a primeira
    # aplicacao desta passada gravou os 37 metatiles e NENHUM dos 29 tiles: no
    # render, praca e passeio sairam azul-marinho, porque os metatiles novos
    # apontavam para o lixo que estava naquelas vagas. Aqui o `load()` e da
    # PROPRIA imagem que vai ser salva.
    antigo.load()
    cols = antigo.size[0] // 8
    px = antigo.load()
    for v, tile in tiles_novos.items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        if y0 + 8 > antigo.size[1]:
            raise SystemExit("a vaga de tile %d nao cabe no tiles.png" % v)
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    antigo.save(f"{DESTINO}/tiles.png")

    for vaga, cores in sorted(dados["paletas"].items()):
        _grava_pal(int(vaga), cores)

    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    alvo = (max(metas) + 1) if metas else len(meta) // 16
    while len(meta) // 16 < alvo:
        meta += struct.pack("<8H", *([1] * 8))
    while len(attr) // 2 < alvo:
        attr += struct.pack("<H", 0)
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------ o ESPALHAMENTO
def pracas(elegivel, tomadas, teto):
    """[(canto, largura, altura)] das pracas, em ordem determinista.

    Retangulo cheio de celulas elegiveis e livres, com `FOLGA_PRACA` celulas de
    creme em volta para duas molduras nunca se encostarem. Os tamanhos sao
    tentados do MAIOR para o menor, porque praca grande le como praca e praca
    pequena le como remendo; dentro de cada tamanho a ordem das posicoes e um
    hash da posicao, que nao tem periodo e nao depende de x nem de y sozinhos.
    """
    saida, usadas, total = [], set(tomadas), 0
    for larg, alt in TAMANHOS:
        cand = sorted(elegivel, key=lambda p: (_mistura(p[0], p[1], 0x9A17), p))
        for x0, y0 in cand:
            if total + larg * alt > teto:
                continue
            cels = [(x0 + i, y0 + j) for j in range(alt) for i in range(larg)]
            if any(p not in elegivel or p in usadas for p in cels):
                continue
            volta = [(x0 + i, y0 + j)
                     for j in range(-FOLGA_PRACA, alt + FOLGA_PRACA)
                     for i in range(-FOLGA_PRACA, larg + FOLGA_PRACA)]
            if any(p in usadas for p in volta):
                continue
            usadas |= set(volta)
            saida.append((x0, y0, larg, alt))
            total += larg * alt
    return saida, total


def peca_da_praca(x0, y0, larg, alt, x, y):
    """Qual peca do calcamento vai nesta celula da praca."""
    n, s = y == y0, y == y0 + alt - 1
    o, l = x == x0, x == x0 + larg - 1
    if n and o:
        return PRACA["no"]
    if n and l:
        return PRACA["ne"]
    if s and o:
        return PRACA["so"]
    if s and l:
        return PRACA["se"]
    if n:
        return PRACA["n"]
    if s:
        return PRACA["s"]
    if o:
        return PRACA["o"]
    if l:
        return PRACA["l"]
    return peca_da_lista(PRACA["miolo"], x, y)


def faixa_de_passeio(elegivel, tomadas, v, W, H, teto):
    """As celulas de PASSEIO: creme colado na fachada, em trechos contiguos.

    Passeio de cidade e faixa, nao pontilhado, entao a escolha e por TRECHO: as
    celulas que encostam num solido sao agrupadas em pedacos 4-conexos, os
    pedacos menores que `PASSEIO_MIN` sao descartados (risco de uma celula solta
    le como sujeira) e os que ficam entram inteiros, do maior para o menor, ate
    o teto.
    """
    def solido(x, y):
        return not (0 <= x < W and 0 <= y < H) or ((v[y * W + x] >> 10) & 3)

    beira = {p for p in elegivel if p not in tomadas
             and any(solido(p[0] + dx, p[1] + dy) for dx, dy in N4)}
    vistos, pedacos = set(), []
    for p in sorted(beira):
        if p in vistos:
            continue
        pilha, corpo = [p], {p}
        vistos.add(p)
        while pilha:
            q = pilha.pop()
            for dx, dy in N4:
                rr = (q[0] + dx, q[1] + dy)
                if rr in beira and rr not in vistos:
                    vistos.add(rr)
                    corpo.add(rr)
                    pilha.append(rr)
        if len(corpo) >= PASSEIO_MIN:
            pedacos.append(corpo)
    pedacos.sort(key=lambda c: (-len(c), sorted(c)[0]))
    saida, total = [], 0
    for corpo in pedacos:
        if total + len(corpo) > teto:
            continue
        saida.append(corpo)
        total += len(corpo)
    return saida, total


def peca_da_lista(nomes, x, y):
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
    existe.
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
        vistos = {depois.get(p) for p in cels}
        if len(vistos) > 1:
            mau.append("o pedaco %d de chao se partiu em %d" % (rr, len(vistos)))
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
    """(L, W, H, v, escritas, contas) de `JubilifeCity`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    # ELEVACAO: a do carimbo, e ela e filtro porque a mesma calcada aparece em
    # mais de uma elevacao num mapa de cidade com escada. A elevacao de cada
    # celula continua preservada bit a bit na escrita.
    elev = collections.Counter(
        (c >> 12) & 0xF for c in v
        if (c & 0x3FF) == CARIMBO and not ((c >> 10) & 3)).most_common(1)[0][0]

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    elegivel = {(i % W, i // W) for i in range(W * H)
                if andavel(i) and (v[i] & 0x3FF) == CARIMBO
                and ((v[i] >> 12) & 0xF) == elev
                and beh(v[i] & 0x3FF) not in AG
                and MARGEM <= i % W < W - MARGEM
                and MARGEM <= i // W < H - MARGEM}

    escritas = {}
    # ------------------------------------------------------- 1. o PISO, no papel
    # As pracas e o passeio sao decididos ANTES dos moveis e escritos DEPOIS
    # deles. A ordem importa e foi medida nesta frente: com os moveis primeiro,
    # as 63 pecas espalhadas caiam uma a cada treze celulas de creme e nenhum
    # retangulo de praca sobrevivia inteiro (a primeira versao fechou com UMA
    # praca de 4x3 e a regua parou em 31,2%). Decidindo o piso primeiro, o movel
    # sabe em que chao esta pousando e escolhe a versao de fundo certa.
    lista_pracas, n_praca = pracas(elegivel, set(), TETO_PRACA)
    plano_piso, miolo, moldura = {}, set(), set()
    for x0, y0, larg, alt in lista_pracas:
        for j in range(alt):
            for i in range(larg):
                p = (x0 + i, y0 + j)
                nome = peca_da_praca(x0, y0, larg, alt, p[0], p[1])
                plano_piso[p] = nome
                (miolo if nome in PRACA["miolo"] else moldura).add(p)
    resto = {p for p in elegivel if p not in plano_piso}
    trechos, n_passeio = faixa_de_passeio(resto, set(), v, W, H, TETO_PASSEIO)
    passeio_cels = set()
    for corpo in trechos:
        for p in corpo:
            plano_piso[p] = peca_da_lista(PASSEIO, p[0], p[1])
            passeio_cels.add(p)

    # ------------------------------------------------------------- 2. MOVEIS
    # Eles vem antes de o piso ser ESCRITO de proposito, e a razao esta medida em
    # Snowpoint: movel posto no carimbo tira uma celula do numerador E do
    # denominador da regua; movel posto em cima de uma peca nova tira so do
    # denominador, o que PIORA a conta. MOLDURA e PASSEIO ficam proibidos: movel
    # em cima da moldura quebra o contorno da praca, e movel no passeio tapa a
    # faixa de uma celula que e a leitura de calcada.
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    # o que o `enfeita_cidades.py` ja desenhou nesta cidade fica de fora, mas SO
    # a celula: movel encostado em enfeite e cidade cheia, nao cidade errada.
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))
    proibido = moldura | passeio_cels

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
        if (x, y) in gelo or i in escritas or (x, y) not in elegivel:
            return False
        if (x, y) in proibido:
            return False
        return (aplicado[i] & 0x3FF) == CARIMBO

    def solido(x, y):
        return 0 <= x < W and 0 <= y < H and ((aplicado[y * W + x] >> 10) & 3)

    def encosto_ok(onde, cels):
        # Movel de cidade encosta em alguma coisa: peca solta no meio da praca
        # vazia le como erro de mapa.
        if onde == "beira":
            return any(solido(x + dx, y + dy) for x, y in cels for dx, dy in N4)
        return True

    def espacado(mv, cels):
        for x, y in cels:
            if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
                   for px, py in postos):
                return False
            if any(max(abs(x - px), abs(y - py)) < mv["espaco"]
                   for px, py in por_movel[mv["nome"]]):
                return False
        return True

    def tenta_peca(mv, x0, y0):
        """Escreve a peca inteira e devolve True se os DOIS portoes deixarem.

        O portao roda NA HORA e nao so no fim: se solidificar as celulas desta
        peca tirar do alcance a pe qualquer OUTRA celula, ou partir um pedaco de
        chao em dois, a escrita e desfeita e o gerador segue.
        """
        pontos = [(x0 + ci, y0 + li)
                  for li, linha in enumerate(mv["grades"]["carimbo"])
                  for ci, _g in enumerate(linha)]
        if any(not livre(x, y) for x, y in pontos):
            return False
        # FUNDO COERENTE: as celulas de uma peca tem que estar todas no mesmo
        # chao, senao meio banco pousa no creme e meio no calcamento.
        fundos = {"calcada" if p in miolo else "carimbo" for p in pontos}
        if len(fundos) > 1:
            return False
        fundo = fundos.pop()
        grade = mv["grades"][fundo]
        cels = [(x0 + ci, y0 + li, gid, bool(mv["solidas"][li][ci]))
                for li, linha in enumerate(grade)
                for ci, gid in enumerate(linha)]
        if not encosto_ok(mv["onde"], pontos) or not espacado(mv, pontos):
            return False
        guarda = {}
        novas = []
        for x, y, gid, sol in cels:
            i = y * W + x
            guarda[i] = aplicado[i]
            # ELEVACAO PRESERVADA (bits 12 a 15); a colisao so LIGA, nunca desliga
            aplicado[i] = ((aplicado[i] & 0xF000)
                           | ((1 << 10) if sol else (aplicado[i] & 0x0C00))
                           | gid)
            if sol:
                novas.append((x, y))
        perdidas = (antes_alc - E.alcance(aplicado, W, H, ini)) \
            - set(novos_solidos) - set(novas)
        partiu = any(nao_liga(aplicado, x, y) for x, y in novas)
        if perdidas or partiu:
            for i, val in guarda.items():
                aplicado[i] = val
            return False
        for i in guarda:
            escritas[i] = aplicado[i]
        novos_solidos.extend(novas)
        postos.extend(pontos)
        for p in pontos:
            plano_piso.pop(p, None)
        return fundo

    ordem_cel = sorted(((x, y) for y in range(H) for x in range(W)),
                       key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF, p))
    lista = carimbos["moveis"]
    postas, conta_fundo = [], collections.Counter()
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            mv = lista[(giro + k) % len(lista)]
            if conta_mov[mv["nome"]] >= mv["quantos"]:
                continue
            fundo = tenta_peca(mv, x, y)
            if fundo:
                por_movel[mv["nome"]].append((x, y))
                conta_mov[mv["nome"]] += 1
                conta_fundo[fundo] += 1
                postas.append([mv["nome"], fundo, x, y])
                break

    # ------------------------------------------------------- 3. o PISO, escrito
    por_nome = {c["nome"]: c["mt"] for c in carimbos["chao"]}
    conta_chao = collections.Counter()

    def pintavel(p):
        """A celula pode receber CHAO novo?

        `gelo` NAO entra aqui, e nao entra de proposito: chao novo nao mexe em
        colisao, nao mexe em elevacao e nao mexe em (comportamento, layerType),
        entao pintar a celula onde mora uma placa ou por onde a suite anda nao
        muda nada para o jogo, so troca o desenho do piso.
        """
        i = p[1] * W + p[0]
        return (p in elegivel and i not in escritas
                and (aplicado[i] & 0x3FF) == CARIMBO)

    for p in sorted(plano_piso):
        if pintavel(p):
            i = p[1] * W + p[0]
            escritas[i] = (aplicado[i] & 0xFC00) | por_nome[plano_piso[p]]
            aplicado[i] = escritas[i]
            conta_chao[plano_piso[p]] += 1

    # -------------------------------------------------------------- PORTOES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (ALVO, len(perdidas), sorted(perdidas)[:6]))
    if depois - antes_alc:
        raise SystemExit("%s: o alcance a pe GANHOU celula" % ALVO)
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel"
                             % (ALVO, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (ALVO, "; ".join(queixas)))

    contas = dict(pracas=len(lista_pracas), celulas_praca=n_praca,
                  passeio=n_passeio, trechos=len(trechos),
                  moveis=dict(conta_mov), chao=dict(conta_chao),
                  fundos=dict(conta_fundo), solidos=len(novos_solidos),
                  postas=postas, lista_pracas=lista_pracas)
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


def base_de(guardado):
    """A grade como esta no disco, so tirando o que ESTA passada escreveu.

    Sem isso a idempotencia morre: `JubilifeCity` JA tem desenho do
    `enfeita_cidades.py` em cima, com plano proprio, e planejar sobre um mapa ja
    enfeitado nao volta ao mesmo lugar. A saida e a do `porto_canalave.py`:
    planejar sobre a base LIMPA desta passada (o disco menos o que esta passada
    gravou) e escrever por cima do disco.
    """
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    dados = kit()
    print("kit: %d tiles novos nos buracos %s%s de %d, %d metatiles novos "
          "(locais %d a %d, ids %d a %d)"
          % (len(tiles_novos), sorted(tiles_novos)[:6],
             " ..." if len(tiles_novos) > 6 else "", TETO_TILES,
             len(metas), min(metas), max(metas), 512 + min(metas),
             512 + max(metas)))
    for vaga, cores in sorted(dados["paletas"].items()):
        antigos = _tileset(SECUNDARIO)["paletas"][int(vaga)]
        n = sum(1 for i in range(1, 16) if list(cores[i]) != list(antigos[i]))
        print("  vaga %s: %d cores novas em indice que nenhum pixel vivo usava"
              % (vaga, n))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)

    guardado = carrega_plano()
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base_de(guardado))
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("\n%s: %d pracas (%d celulas), %d trechos de passeio (%d celulas), "
          "%d celulas solidificadas, %d celulas mudadas"
          % (ALVO, contas["pracas"], contas["celulas_praca"], contas["trechos"],
             contas["passeio"], contas["solidos"], len(escritas)))
    print("  chao:  " + ", ".join("%s x%d" % kv
                                  for kv in sorted(contas["chao"].items())))
    print("  movel: " + ", ".join("%s x%d" % kv
                                  for kv in sorted(contas["moveis"].items())))
    print("  regua: carimbo %d com %.1f%% de %d celulas ANTES; carimbo %d com "
          "%.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
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
def confere(tiles_novos, metas, attrs, carimbos, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela e chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que
    tem que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida so no caminho feliz nao e regra, e prova positiva sem
    par negativo nao e prova.
    """
    import render_maps as RM
    from PIL import Image
    mau = []
    dados = kit()
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    base, attr_chao = chao_nosso()
    asec = G._attrs(SECUNDARIO)
    ap = G._attrs(PRIMARIO)

    def atributo(mt_id):
        if mt_id >= 512:
            local = mt_id - 512
            if local in attrs:
                return attrs[local]
            return asec[local] if local < len(asec) else 0
        return ap[mt_id] if mt_id < len(ap) else 0

    def entradas(mt_id):
        if mt_id >= 512 and (mt_id - 512) in metas:
            return list(metas[mt_id - 512])
        tset, loc = (tp, mt_id) if mt_id < 512 else (ts, mt_id - 512)
        return _entradas(tset["metatiles"], loc)

    def opac(val):
        idx = val & 0x3FF
        if idx == 0:
            return 0
        vaga = idx - len(tp["tiles"])
        if vaga in tiles_novos:
            return _opacos(tiles_novos[vaga])
        t = RM.resolver_tile(tp, ts, idx)
        return _opacos(t) if t else 64

    def px_de(mt_id):
        """Os 256 pixels RGB do metatile, com o kit desta rodada valendo."""
        im = Image.new("RGB", (16, 16), tuple(tp["paletas"][0][0]))
        pxi = im.load()
        ent = entradas(mt_id)
        for cam in (0, 1):
            for q in range(4):
                val = ent[cam * 4 + q]
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if not idx:
                    continue
                vaga = idx - len(tp["tiles"])
                tile = (tiles_novos[vaga] if vaga in tiles_novos
                        else RM.resolver_tile(tp, ts, idx))
                if tile is None:
                    continue
                cores = (dados["paletas"].get(str(ip))
                         or (tp if ip < 6 else ts)["paletas"].get(ip))
                if cores is None:
                    continue
                RM.desenhar_tile(pxi, (q % 2) * 8, (q // 2) * 8, tile,
                                 [tuple(c) for c in cores],
                                 bool(val & 0x400), bool(val & 0x800))
        return [pxi[x, y] for y in range(16) for x in range(16)]

    # ------------------------------------------------------------ 1. orcamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    if set(tiles_novos) & PINOS_ANIM:
        mau.append("o kit ocupa vaga de PINO de animacao: %s"
                   % sorted(set(tiles_novos) & PINOS_ANIM))
    livres = dados["vagas_livres"]
    for vaga, cores in sorted(dados["paletas"].items()):
        if not 6 <= int(vaga) <= 12:
            mau.append("a vaga %s nao e de secundario" % vaga)
        antigo = ts["paletas"][int(vaga)]
        vagos = set(livres.get(vaga) or [])
        for i in range(1, 16):
            if tuple(cores[i]) != tuple(antigo[i]) and i not in vagos:
                mau.append("a vaga %s mudou a cor do indice %d, que algum pixel "
                           "nosso usa" % (vaga, i))
        nz = [tuple(c) for c in cores[1:] if tuple(c) != (0, 0, 0)]
        if len(nz) > 15:
            mau.append("a vaga %s tem %d cores nao-zero" % (vaga, len(nz)))

    # ------ 2. CHAO novo: atributo IGUAL ao do carimbo e camada de cima VAZIA
    ids_chao = [c["mt"] for c in carimbos["chao"]]
    for c in carimbos["chao"]:
        if atributo(c["mt"]) != attr_chao:
            mau.append("o chao %d tem atributo 0x%04X e o carimbo tem 0x%04X"
                       % (c["mt"], atributo(c["mt"]), attr_chao))
        if any(e & 0x3FF for e in entradas(c["mt"])[4:]):
            mau.append("o chao %d usa a camada de cima, que com layerType "
                       "NORMAL desenha ACIMA do jogador" % c["mt"])

    # ------ 3. MOVEL e BASE: COVERED, comportamento zerado, e o NOSSO chao
    fundos = {"carimbo": tuple(base)}
    for c in carimbos["chao"]:
        if c["nome"] == "calcamento":
            fundos["calcada"] = tuple(entradas(c["mt"])[:4])
    ids_solido, ids_topo = {}, {}
    for mv in carimbos["moveis"]:
        for fundo, grade in sorted(mv["grades"].items()):
            for li, linha in enumerate(grade):
                for ci, gid in enumerate(linha):
                    if mv["solidas"][li][ci]:
                        ids_solido[gid] = (mv["nome"], fundo)
                    else:
                        ids_topo[gid] = (mv["nome"], fundo)
    for gid, (nome, fundo) in sorted(ids_solido.items()):
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %d (%s) nao esta em COVERED" % (gid, nome))
        if a & 0xFF:
            mau.append("o movel %d importou comportamento 0x%02X da fonte"
                       % (gid, a & 0xFF))
        if tuple(entradas(gid)[:4]) != fundos[fundo]:
            mau.append("o movel %d nao tem o nosso chao na camada de baixo" % gid)
    # ------ 4. TOPO de peca: continua ANDAVEL, herda o atributo do carimbo e
    #           nao pode tapar o jogador inteiro (o defeito E3 do mapas_qa.py)
    for gid, (nome, fundo) in sorted(ids_topo.items()):
        if atributo(gid) != attr_chao:
            mau.append("o topo %d (%s) nao herdou o atributo do carimbo"
                       % (gid, nome))
        if tuple(entradas(gid)[:4]) != fundos[fundo]:
            mau.append("o topo %d nao tem o nosso chao na camada de baixo" % gid)
        if sum(opac(e) for e in entradas(gid)[4:]) >= 4 * 64:
            mau.append("o topo %d tapa o jogador inteiro (E3)" % gid)

    # ------ 5. nenhuma variante de chao e copia pixel a pixel de outra
    lista = ids_chao + [CARIMBO]
    pix = {mt: px_de(mt) for mt in lista}
    for i, a in enumerate(lista):
        for b in lista[i + 1:]:
            dd = sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
                     for p, q in zip(pix[a], pix[b])) / 256.0
            if dd < 8.0:
                mau.append("as variantes de chao %d e %d tem distancia %.1f, "
                           "abaixo do piso de 8,0 do varia_carimbo.py: isso e "
                           "enganar a regua" % (a, b, dd))

    # ------------------------------------------------ 6 a 11. o plano do mapa
    L, W, H, v, escritas, contas = plano
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    meus_chaos = set(ids_chao)

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVACAO em (%d,%d)" % (ALVO, x, y))
        if cv and not cn:
            mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                       % (ALVO, x, y))
        if velho != CARIMBO:
            mau.append("%s: peca escrita fora do carimbo em (%d,%d)" % (ALVO, x, y))
        if novo in meus_chaos or novo in ids_topo:
            if cn != cv:
                mau.append("%s: chao ou topo mudou colisao em (%d,%d)"
                           % (ALVO, x, y))
        elif novo in ids_solido:
            if cv or not cn:
                mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                           % (ALVO, x, y))
            if (x, y) in ev:
                mau.append("%s: movel em cima do evento (%d,%d)" % (ALVO, x, y))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                       % (ALVO, novo, x, y))

    # 7. (comportamento, layerType) de toda celula ANDAVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                       "layerType)" % (ALVO, i % W, i // W))
            break

    # 8. os DOIS portoes de alcance
    ini = E.partidas(d, W, H, v)
    antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
    solid = {(i % W, i // W) for i in escritas
             if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
    if (antes - depois) - solid:
        mau.append("%s: o alcance a pe perdeu %d celulas alem das solidificadas: "
                   "%s" % (ALVO, len((antes - depois) - solid),
                           sorted((antes - depois) - solid)[:6]))
    if depois - antes:
        mau.append("%s: o alcance a pe GANHOU celula" % ALVO)
    mau += ["%s: %s" % (ALVO, q) for q in
            ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                            solid)]

    # 9. O PISO NOVO NAO PODE SER ADIVINHAVEL, e o teste tem dois lados.
    #  (a) PADRAO: nenhuma projecao simples da posicao pode ADIVINHAR a peca. A
    #      conta e por EIXO (x, y, x+y, x-y) e por MODULO de 2 a 8, chutando
    #      dentro de cada classe de resto a peca mais comum dela, contra o chute
    #      cego da peca mais comum do mapa. O corte de 12 pontos vem do
    #      `neve_snowpoint2.py`, calibrado la com folga de duas vezes.
    #  (b) FORMA: o piso novo tem que ser AREA, nao sal e pimenta, e a conta e o
    #      TAMANHO MEDIO do pedaco conexo.
    mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
              if (val & 0x3FF) in meus_chaos}
    if len(mancha) < 400:
        mau.append("%s: so %d celulas de piso novo" % (ALVO, len(mancha)))
    # O teste de PADRAO roda sobre o MIOLO da praca, e nao sobre todo o piso
    # novo, e a razao esta medida: o passeio tem uma peca so e ocupa metade das
    # celulas, entao ele sozinho poe o chute cego em 49% e afoga qualquer ganho
    # de projecao. Com a sabotagem de `(x+y) % n` ligada, o teste sobre o piso
    # inteiro fechou VERDE; sobre o miolo, que e onde a escolha por hash
    # realmente acontece, ele acusa. Medir a decisao, nao a media.
    #      E o piso do teste nao e o chute cego cru: com 79 celulas de miolo e
    #      quatro variantes, qualquer particao em oito classes acerta 41% por
    #      ACASO contra 28% do chute cego, e o teste cru fechava vermelho no
    #      caminho feliz. O piso e medido: as MESMAS posicoes recebem rotulo por
    #      um hash independente (tres sementes de controle) e o maior ganho que
    #      o acaso produz ali e o que a distribuicao de verdade tem direito de
    #      ter, mais a margem de 12 pontos.
    ids_miolo = {c["mt"] for c in carimbos["chao"] if c["nome"] in PRACA["miolo"]}
    so_miolo = {p: m for p, m in mancha.items() if m in ids_miolo}
    if so_miolo:
        EIXOS = (("x", lambda p: p[0]), ("y", lambda p: p[1]),
                 ("x+y", lambda p: p[0] + p[1]),
                 ("x-y", lambda p: p[0] - p[1]))

        def melhor_ganho(rotulos):
            tot = len(rotulos)
            cego = collections.Counter(rotulos.values()).most_common(1)[0][1] / tot
            melhor = (0.0, "", 0, cego)
            for rot, eixo in EIXOS:
                for mod in range(2, 9):
                    tab = collections.defaultdict(collections.Counter)
                    for p, mt_id in rotulos.items():
                        tab[eixo(p) % mod][mt_id] += 1
                    ac = sum(c.most_common(1)[0][1] for c in tab.values()) / tot
                    if ac - cego > melhor[0]:
                        melhor = (ac - cego, rot, mod, cego)
            return melhor

        alvos = sorted(ids_miolo)
        piso = 0.0
        for semente in (0x1111, 0x2222, 0x3333):
            ctrl = {p: alvos[_mistura(p[0], p[1], semente) % len(alvos)]
                    for p in so_miolo}
            piso = max(piso, melhor_ganho(ctrl)[0])
        ganho, rot, mod, cego = melhor_ganho(so_miolo)
        if ganho > piso + 0.12:
            mau.append("%s: saber %s mod %d adivinha a peca em %.0f%% das "
                       "celulas contra %.0f%% do chute cego (ganho de %.2f "
                       "contra o piso de acaso %.2f): virou padrao"
                       % (ALVO, rot, mod, 100 * (ganho + cego), 100 * cego,
                          ganho, piso))
    if mancha:
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
            mau.append("%s: o piso novo tem pedaco medio de so %.1f celulas "
                       "(%d em %d pedacos): virou sal e pimenta, nao area"
                       % (ALVO, len(mancha) / pedacos, len(mancha), pedacos))

    # 10. a regua tem que fechar
    b, _nb, _idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                   % (ALVO, b))

    # 11. PECA INTEIRA NO MAPA: cada peca anotada no plano esta no mapa com
    #     TODAS as celulas dela, e nenhuma celula de peca esta fora de uma peca
    #     anotada. A conta NAO pode ser por metatile, porque metatile de peca e
    #     COMPARTILHADO entre as duas versoes de fundo.
    por_nome = {m["nome"]: m for m in carimbos["moveis"]}
    cobertas = set()
    for nome, fundo, x0, y0 in contas["postas"]:
        mv = por_nome[nome]
        for li, linha in enumerate(mv["grades"][fundo]):
            for ci, gid in enumerate(linha):
                x, y = x0 + ci, y0 + li
                cobertas.add((x, y))
                j = y * W + x
                if (saida[j] & 0x3FF) != gid:
                    mau.append("%s: a peca %s em (%d,%d) devia ter o metatile "
                               "%d em (%d,%d) e tem %d"
                               % (ALVO, nome, x0, y0, gid, x, y, saida[j] & 0x3FF))
                if bool(mv["solidas"][li][ci]) != bool((saida[j] >> 10) & 3):
                    mau.append("%s: a celula (%d,%d) da peca %s tem a colisao "
                               "errada" % (ALVO, x, y, nome))
    de_peca = set(ids_solido) | set(ids_topo)
    for i, val in escritas.items():
        if (val & 0x3FF) in de_peca and (i % W, i // W) not in cobertas:
            mau.append("%s: a celula (%d,%d) tem metatile de peca (%d) e nao "
                       "pertence a peca nenhuma do plano"
                       % (ALVO, i % W, i // W, val & 0x3FF))
            break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e DEZ provas negativas, cada sabotagem revertida em seguida.

    "Zero diferenca" so vale depois que a comparacao mostra que sabe reprovar.
    """
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    guardado = carrega_plano()
    plano = plano_mapa(carimbos, base_de(guardado))
    mau = confere(tiles_novos, metas, attrs, carimbos, plano)
    negativas = []

    def copia():
        return (dict(tiles_novos), dict(metas), dict(attrs),
                json.loads(json.dumps(carimbos)),
                (plano[0], plano[1], plano[2], list(plano[3]), dict(plano[4]),
                 json.loads(json.dumps(plano[5]))))

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = confere(*args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NAO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    W = plano[1]

    # N1. colisao 1 -> 0 numa celula de piso
    def n1():
        a = copia()
        _L, _W, _H, v, esc, _ct = a[4]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a celula ERA solida
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevacao alterada
    def n2():
        a = copia()
        _L, _W, _H, v, esc, _ct = a[4]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | ((((v[i] >> 12) + 1) & 0xF) << 12)
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. comportamento da fonte importado num metatile de CHAO
    def n3():
        a = copia()
        gid = carimbos["chao"][0]["mt"]
        a[2][gid - 512] = (a[2][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chao sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = sorted(g for mv in carimbos["moveis"]
                     for grade in mv["grades"].values()
                     for li, linha in enumerate(grade)
                     for ci, g in enumerate(linha) if mv["solidas"][li][ci])[0]
        a[2][gid - 512] = a[2][gid - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no movel", n4, "nao esta em COVERED")

    # N5. peca de chao com a camada de cima ligada: piso que desenha ACIMA do
    #     jogador nao e piso, e foi por isso que o metatile 243 do hack ficou de
    #     fora do kit
    def n5():
        a = copia()
        gid = carimbos["chao"][0]["mt"]
        ent = list(a[1][gid - 512])
        ent[4] = ent[0]
        a[1][gid - 512] = ent
        return a
    sabota("chao com camada de cima", n5, "usa a camada de cima")

    # N6. camada de BAIXO de um movel sabotada (chao da fonte no lugar do nosso)
    def n6():
        a = copia()
        gid = sorted(ids for mv in carimbos["moveis"]
                     for grade in mv["grades"].values()
                     for linha in grade for ids in linha)[0]
        ent = list(a[1][gid - 512])
        ent[0] = ent[4]
        a[1][gid - 512] = ent
        return a
    sabota("camada de baixo sabotada", n6, "camada de baixo")

    # N7. peca escolhida por (x + y) % n, que e xadrez com periodo
    def n7():
        a = copia()
        original = globals()["peca_da_lista"]
        globals()["peca_da_lista"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            a = (dict(tiles_novos), dict(metas), dict(attrs),
                 json.loads(json.dumps(carimbos)),
                 plano_mapa(carimbos, base_de(guardado)))
        finally:
            globals()["peca_da_lista"] = original
        return a
    sabota("piso por (x+y) % n", n7, "virou padrao")

    # N8. corredor fechado que PARTE um pedaco de chao. O portao de alcance
    #     sozinho nao pega isso quando ha warp dos dois lados, e foi assim que
    #     Snowpoint passou verde com a cidade cortada.
    def n8():
        a = copia()
        _L, _W, _H, v, esc, _ct = a[4]
        H = plano[2]
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
        lista = a[3]["chao"]
        a[1][lista[1]["mt"] - 512] = list(a[1][lista[0]["mt"] - 512])
        return a
    sabota("variante de chao duplicada", n9, "abaixo do piso de 8,0")

    # N10. topo de peca com a camada de cima 100% opaca: ele tapa o jogador
    def n10():
        a = copia()
        gid = sorted(ids_topo_de(carimbos))[0]
        ent = list(a[1][gid - 512])
        cheio = a[1][carimbos["chao"][0]["mt"] - 512][0]
        a[1][gid - 512] = ent[:4] + [cheio] * 4
        return a
    sabota("topo de peca 100% opaco", n10, "tapa o jogador inteiro")

    # N11. cor nova escrita num indice que os NOSSOS pixels ja usam: e o unico
    #      jeito de a vaga de indice vago estragar o desenho de quem ja estava la
    def n11():
        a = copia()
        dados = kit()
        for vaga in sorted(dados["paletas"]):
            usados = [i for i in range(1, 16)
                      if i not in set(dados["vagas_livres"].get(vaga) or [])]
            if usados:
                pal = [list(c) for c in dados["paletas"][vaga]]
                pal[usados[0]] = [255, 0, 255]
                dados["paletas"][vaga] = pal
                break
        with open(KIT_JSON + ".sab", "w") as f:
            json.dump(dados, f)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        return a
    try:
        sabota("cor nova em indice ja usado", n11, "que algum pixel nosso usa")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # ------------------------------------------------ o que esta NO DISCO
    # Sem este caso o auto-teste so confere o que ele mesmo acabou de calcular em
    # memoria: sabotar o atributo, o tile ou a cor DIRETO NO DISCO deixaria todos
    # os casos anteriores verdes.
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    pxd = png.convert("P").load()
    n_disco = len(meta_disco) // 16
    postas = [l for l in metas
              if l < n_disco and _entradas(meta_disco, l) == metas[l]]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; o caso de DISCO "
              "nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ents in metas.items():
            if local >= n_disco or _entradas(meta_disco, local) != ents:
                mau.append("metatile %d no disco nao e o do kit" % (512 + local))
            elif struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if y0 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
            if [[pxd[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga)
        for vaga, cores in sorted(kit()["paletas"].items()):
            arq = [l.split() for l in
                   open(f"{DESTINO}/palettes/%s.pal" % vaga.zfill(2)).read().split("\n")[3:]
                   if l.strip()]
            if [[int(z) for z in c] for c in arq[:16]] != cores:
                mau.append("a paleta %s no disco nao e a do kit" % vaga)

    # ------------------------------------------------------- idempotencia
    _L, _W, _H, v, escritas, _ct = plano
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    volta = list(saida)
    for i in sorted(escritas):
        if volta[i] == escritas[i]:
            volta[i] = v[i]
    if volta != list(v):
        mau.append("%s: desfazer nao devolve a base" % ALVO)
    _l, _w, _h, _v, esc2, _c2 = plano_mapa(carimbos, volta)
    if esc2 != escritas:
        mau.append("%s: segunda passada deu plano diferente" % ALVO)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    L, W, H, v, escritas, contas = plano
    a, _na, _ida = regua(v, W, H, L)
    b, _nb, _idb = regua(v, W, H, L, escritas)
    print("DEMO VERDE: %d tiles, %d metatiles, %d celulas mudadas, %d "
          "solidificadas, regua %.1f%% -> %.1f%%"
          % (len(tiles_novos), len(metas), len(escritas), contas["solidos"],
             a, b))
    print("  %d provas negativas:" % len(negativas))
    for nome, queixa in negativas:
        print("    %-28s -> %s" % (nome, queixa[:110]))
    return 0


def ids_topo_de(carimbos):
    """Os metatiles de celula ANDAVEL de peca (o topo do vaso de arbusto)."""
    return [g for mv in carimbos["moveis"] for grade in mv["grades"].values()
            for li, linha in enumerate(grade)
            for ci, g in enumerate(linha) if not mv["solidas"][li][ci]]



def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--desfazer" in sys.argv:
        return desfaz()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--so-tileset" in sys.argv:
        t, m, at, _c = desenha_kit()
        grava_tileset(t, m, at)
        print("tileset escrito: %d tiles, %d metatiles" % (len(t), len(m)))
        return 0
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
