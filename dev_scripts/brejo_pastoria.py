#!/usr/bin/env python3
"""Refino de `PastoriaCity` (tema BREJO, o Great Marsh do DPPt), no
`gTileset_LilycoveSinnoh`, com arte importada do `Pokémon Light Platinum`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: `PastoriaCity` gasta 36,5% do chão andável a pé
(395 células de 1.081) com o metatile 1, a grama lisa do primário, e mais 16,7%
(181 células) com o metatile 473, a clareira clara que faz o pátio das casas.
Dois tapetes chapados numa cidade de 68x60 que, no DPPt, é a cidade do PÂNTANO:
ela abre para o Great Marsh, tem o mar a sudeste e três lagoas a sudoeste, e no
render de antes nada disso aparece no chão.

DOIS CARIMBOS, como em `costa_sandgem.py`, e pela mesma razão aritmética: a
régua mede o DOMINANTE, e derrubar só o primeiro faz o segundo assumir o posto.
Pior, solidificar célula tira do denominador, então quebrar um carimbo pode
SUBIR a fração do outro. As duas famílias são tratadas juntas, cada uma com o
próprio catálogo e a própria medida antes e depois.

A ESCOLHA DA FONTE, com número, porque brejo é tema difícil de achar. Foram
triadas quatro ROM hacks com folha de contato (`ferramentas/folha_tema.py`) e
render de mapa inteiro:

  - `Pokémon Unbound`, secundários 0x2D5034 e 0x2D5004: o primeiro é RUÍNA de
    pedra com colunas, não brejo (o verde escuro da miniatura é musgo de
    parede); o segundo é floresta fechada com poças pretas. Descartados por
    conteúdo, não por cor.
  - `Pokémon GS Chronicles`, secundários 0x2D4EFC e 0x9A62CC: passarela de
    madeira sobre água, mas a água é AZUL PISCINA (o mapa g01m88) e a grama é
    (112,208,144) chapada de Johto. Descartado.
  - `Pokémon Liquid Crystal`: nenhum secundário passa o corte de arte nova.
  - `Pokémon Light Platinum`, par 0x286CF4 (primário) + 0x286FAC (secundário),
    o mapa g24m04 (46x94): ESCOLHIDO. É um brejo de verdade: chão de lama
    salpicada, poça de água parada, junco alto, samambaia, tronco caído, raiz
    exposta, passarela e CERCA de madeira, tudo desenhado sobre um verde-azulado
    da mesma família do nosso.

A CONTA DE COR que decidiu, medida nesta árvore e não herdada de brief. A nossa
grama (metatile 1) é (115,197,164) e a nossa clareira (metatile 473) tem
(164,213,197) como cor de campo. No hack:

    hack pal 7, o verde da poça:  (152,216,184) -> 17,9 da nossa clareira
                                  (128,200,160) -> 13,9 da nossa grama
    hack pal 6, o verde da lama:  ( 96,160,136) -> 50,1 da nossa grama
    hack pal 8, o tan da areia:   (207,183,135) -> 82,4 da nossa clareira

Ou seja: a paleta 7 do hack é praticamente a NOSSA cor, a 6 é a mesma família
meio tom abaixo (que é o que lama molhada é ao lado de grama), e a 8 está longe
demais para virar CHÃO. Por isso a areia do hack FICOU DE FORA do catálogo de
chão e a paleta 8 entra só nas peças de MADEIRA e no tronco, que são objeto e
não tapete: um objeto marrom sobre o verde lê como objeto, um tapete marrom no
meio do verde lê como buraco (foi assim que a terra batida caiu em
`costa_sandgem.py`).

A REPARTIÇÃO DAS DUAS FAMÍLIAS sai dessa mesma conta, e é uma decisão de
desenho que o Gui veta pelo render se não gostar:

  - a GRAMA (metatile 1, 395 células) recebe a LAMA do hack (paleta 6), porque
    grama de brejo é grama encharcada: mancha de lodo salpicado no meio do
    verde. Mais os tufos que o NOSSO primário já tem desenhados, que custam
    zero e ficam de graça na cor exata.
  - a CLAREIRA (metatile 473, 181 células) recebe a POÇA (paleta 7), porque o
    pátio pisado da cidade do pântano é onde a água fica parada, e é a paleta
    que está a 17,9 da cor dela.

O CHÃO DE GRAMA NÃO É IMPORTADO, e isso não é economia. O primário do hack tem
grama própria, mas ela é (136,184,80), um verde amarelado a 90 de distância da
nossa: numa mancha ao lado do carimbo isso é remendo. O catálogo de tufo desta
passada é todo NOSSO (cinco metatiles do `gTileset_GeneralSinnoh` com o atributo
IGUAL, bit a bit, ao do metatile 1, mais quatro espelhos horizontais deles).

O ORÇAMENTO, medido nesta árvore e não chutado:

  - PALETA. `NUM_PALS_TOTAL` é 13 (`include/fieldmap.h`): seis vagas do
    primário e SETE do secundário, da 6 à 12. Contando por metatile VIVO (os que
    algum dos TRÊS layouts vivos do tileset desenha), as vagas 7 e 10 estão
    100% livres (15 índices cada) e a vaga 6 tem 11 índices livres. A armadilha
    4 do `compacta_paletas.py` foi conferida na mão e NÃO existe aqui: ZERO
    entradas de metatile do PRIMÁRIO alcançável pintam com vaga >= 6. O kit
    pede 13 cores da paleta 6 do hack, 7 da 7 e 8 da 8, e por isso o mapa é
    hack 6 -> nossa 7, hack 7 -> nossa 10, hack 8 -> nossa 6. Nenhuma cor é
    aproximada: cada nibble é reindexado e o pixel sai idêntico ao da ROM.
  - TILE. O `tiles.png` do `gTileset_LilycoveSinnoh` é 128x256, ou seja 512 de
    512 vagas: CHEIO. Mas só 126 tiles do secundário são referenciados por
    metatile VIVO, e as outras 386 vagas são lixo morto de dumper. Esta passada
    NÃO compacta: ela escreve nas vagas mortas, em ordem crescente. Compactar
    reescreveria o índice de tile dos 392 metatiles e não ganharia nada que já
    não sobre. Metatile morto que aponta para vaga reescrita passa a desenhar
    outra coisa, e é exatamente por isso que a PROVA DE ZERO PIXEL em
    `Route212_North` e `Route212_South` é obrigatória e vale de verdade: os dois
    dividem o mesmo secundário com Pastoria.
  - METATILE. O `metatiles.bin` tem 392 de 512 entradas. Esta passada grava a
    partir do local 392, ou seja no RABO, e estende o arquivo para as 512
    entradas. O diff fica puramente ADITIVO: nenhum metatile existente muda um
    byte, o que é o que faz a prova de zero pixel dos mapas irmãos ser barata de
    acreditar.
  - ANIMAÇÃO. `gTileset_LilycoveSinnoh` declara `.callback =
    InitTilesetAnim_Lilycove` em `src/data/tilesets/headers.h`, mas essa função
    (`src/tileset_anims.c:747`) só zera o contador e põe
    `sSecondaryTilesetAnimCallback = NULL`: não há lista de VDest e portanto NÃO
    há vaga de tile pinada neste tileset. Conferido lendo a função, não a
    memória. Se houvesse, escrever numa vaga pinada estragaria água animada sem
    erro de build.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHÃO NOVO é metatile com arte só na camada de BAIXO e atributo IGUAL, bit a
    bit, ao do carimbo que ele substitui (0x0000 nos dois carimbos). Camada de
    cima em célula andável com layerType NORMAL desenha ACIMA do jogador. A
    exceção são as peças NOSSAS de tufo, que desenham em cima de propósito
    desde o jogo base (o "jogador atrás do mato"); mesmo elas pagam o portão do
    E3 do `mapas_qa.py`, que é não tapar o jogador INTEIRO.
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chão entrada por entrada, e o atributo é comportamento
    ZERADO com layerType COVERED (0x1000).
  - CADA PEÇA SABE SOBRE QUAL CARIMBO ELA POUSA. Peça que pousa na lama recebe
    a camada de baixo do metatile 1; peça que pousa na poça recebe a do 473.
  - O CHÃO DA FONTE NÃO ENTRA, e AQUI A REGRA É MAIS DURA QUE A DAS PASSADAS
    ANTERIORES, por medição. O corte por evidência do `costa_sandgem.py` ("todo
    padrão de camada de baixo que aparece em 4 ou mais metatiles é piso") supõe
    um DEGRAU no histograma, e neste tileset o degrau não existe: contando em
    quantos metatiles diferentes cada tile aparece na camada de baixo, a
    distribuição é 26, 20, 17, 15, 12, 11, 9, 9, 8, 8, 8, 7, 7, seis vezes 6
    (17 tiles), 5 (2 tiles), 4 (13 tiles), 3 (8), 2 (41) e 1 (42). Não há vale
    entre arte e piso, então QUALQUER corte numérico seria chute. A regra desta
    passada não precisa de corte: um MÓVEL que tem camada de CIMA leva SÓ a
    camada de cima, e a de baixo inteira é descartada; um móvel desenhado só na
    camada de baixo (o tronco caído do hack é assim) leva a camada de baixo
    inteira. Como o chão da fonte mora sempre na camada de baixo de metatile
    que TEM camada de cima, ele não entra por construção. O corte de 4 continua
    calculado e vale como PODA e como PORTÃO: quadrante de peça importada cujo
    tile esteja nessa lista é DESCARTADO na extração, e o caso 2 do auto-teste
    reprova se algum sobrar. Não é teoria: o metatile 38 do hack (o junco
    rasteiro) desenha um quadrante da camada de CIMA com o tile 543, que é
    exatamente o tile que a camada de baixo dele repete nos quatro quadrantes.
    Sem a poda, o junco chegaria com um quadrado opaco de chão da fonte grudado
    na perna, e foi assim que o auto-teste ficou vermelho na primeira rodada.
  - QUADRANTE DE BAIXO SOBE só quando a camada de cima está vazia INTEIRA, e
    não quadrante a quadrante. É a versão apertada da regra do
    `porto_canalave.py`, pelo motivo do parágrafo acima.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado. Só
    ARTE. Comportamento é id semântico: todo móvel entra com o comportamento
    ZERADO.

BLOCO DE DUAS CÉLULAS, generalizado. `costa_sandgem.py` só sabia bloco 2x2 (o
coqueiro). O brejo pede DUAS formas que aquele molde não desenha: o junco alto,
que é 1 célula de largura por 2 de altura, e o tronco caído, que é 2 de largura
por 1 de altura e é sólido INTEIRO (tronco não tem copa por onde passar atrás).
Aqui um bloco é um retângulo de `len(topo)+1` linhas: as linhas de `topo` (que
podem ser ZERO) continuam ANDÁVEIS com o atributo do chão, e a última linha,
`base`, vira sólida em COVERED.

O QUE FICOU DE FORA, dito na cara:

  - A AREIA e a TERRA do hack (metatiles 71 a 94 do secundário), pelo número de
    cor acima: 82,4 de distância da nossa clareira, sem nenhuma borda de
    transição desenhada. Seria o defeito nº 1 da lista do `enfeita_cidades.py`
    ("retalhos jogados no gramado").
  - A PASSARELA de madeira (metatiles 132 a 134 e 140 a 142) e a CERCA inteira
    (109, 110, 124 a 126). Passarela é estrutura LINEAR: ela só lê como
    passarela se atravessar alguma coisa, e o gerador desta onda cresce BOLHA,
    não linha. Cerca tem o mesmo problema. Sobreviveu ao corte só a ESTACA
    solta (o metatile 125), que é uma peça de uma célula e lê como poste de
    cerca do safári largado na beira do brejo.
  - O PEDREGULHO do hack (metatile 31 do secundário), porque ele pinta com a
    paleta 3 do hack, que é uma paleta do PRIMÁRIO dele: importá-la pediria uma
    quarta vaga e as três que sobram já estão pagas. No lugar dele entra o
    NOSSO metatile 224, que já é pedregulho sobre a nossa grama, em COVERED e
    com comportamento zerado, e custa ZERO.

Uso:
    python3 dev_scripts/brejo_pastoria.py                    # mede e mostra o plano
    python3 dev_scripts/brejo_pastoria.py --aplicar
    python3 dev_scripts/brejo_pastoria.py --desfazer         # devolve o map.bin
    python3 dev_scripts/brejo_pastoria.py --demo             # auto-teste
    python3 dev_scripts/brejo_pastoria.py --extrai           # regera o kit da ROM
    python3 dev_scripts/brejo_pastoria.py --so-tileset       # so o tileset
    python3 dev_scripts/brejo_pastoria.py --prova-tiles      # o kit contra a ROM
    python3 dev_scripts/brejo_pastoria.py --orcamento        # o que sobra no tileset
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

# O bloco de teste DESTA passada é derivado do desenho, e não o contrário: se
# ele entrasse na varredura de corredores, o plano mudaria depois que o bloco
# fosse escrito e a idempotência morria. Os outros blocos entram todos, o 175
# inclusive (ele não tem caso em Pastoria; quem tem são o 102, o 104 e o 186).
E.BLOCO_PROPRIO = "195_brejo_pastoria.json"

DESTINO = f"{RAIZ}/data/tilesets/secondary/lilycove_sinnoh"
KIT_JSON = f"{RAIZ}/dev_scripts/brejo_pastoria_kit.json"
PLANO = f"{RAIZ}/dev_scripts/brejo_pastoria.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_LilycoveSinnoh"
# Os TRÊS layouts vivos que dividem o `gTileset_LilycoveSinnoh`. A lista foi
# conferida nesta árvore lendo `data/layouts/layouts.json` (o tileset é
# declarado como secundário de exatamente três layouts) e testando a existência
# do `map.bin` de cada um.
IRMAOS = ["PastoriaCity", "Route212_North", "Route212_South"]

TETO_TILES = 512
TETO_META = 512
META_LOCAL_0 = 392          # o `metatiles.bin` tem 392 entradas; grava no rabo
MARGEM = 2
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%
PISO_MIN = 4                # só como PORTÃO; ver o docstring

# ------------------------------------------------------------------- a FONTE
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          pri=0x286CF4, sec=0x286FAC, split=(512, 512, 6))

# PALETA DE ORIGEM DO HACK -> VAGA NOSSA. Medido: o kit pede 13 cores da 6, 7
# da 7 e 8 da 8; as vagas 7 e 10 estão 100% livres (15 índices) e a 6 tem 11.
VAGAS_PAL = {6: 7, 7: 10, 8: 6}

CARIMBOS = dict(grama=1, clareira=473)

# ------------------------------------------------------------------ os TEMAS
# `lp` é o local do metatile no SECUNDÁRIO da fonte.
#
# CHÃO DE LAMA, importado, pousa na GRAMA. São as cinco variantes de lodo
# salpicado do brejo do hack, todas na paleta 6 e todas com a camada de cima
# vazia.
CHAO_LAMA = [
    dict(nome="lama salpicada", lp=1),
    dict(nome="lama batida",    lp=2),
    dict(nome="lama funda",     lp=7),
    dict(nome="lodo",           lp=11),
]
# SÃO SÓ QUATRO, e a lista foi FECHADA por medição e não por gosto. Os
# metatiles do secundário do hack com a camada de cima vazia e paleta 6 são 1,
# 2, 7, 11, 39, 47, 57, 58, 61, 62, 65, 66, 118, 122, 123, 130, 131, 136 e 137.
# Destes, o 39 é o BRASÃO do hack (um escudo azul com listra amarela: entrou na
# primeira lista por leitura de atlas e saiu no primeiro render de peça), o 47 e
# o 118 são retângulos azul-escuros de sombra, e todo o resto são COPAS de
# árvore desenhadas na camada de baixo. Chão de lama de verdade há quatro, e são
# estes. A distância entre os quatro vai de 14,1 a 56,2, bem acima do piso de
# 8,0 do caso 6.
# CHÃO DE POÇA, importado, pousa na CLAREIRA. Água parada e filme de musgo, na
# paleta 7 do hack, que é a que está a 17,9 da cor da clareira.
# A LISTA FOI PODADA PELO CASO 6: o 27 e o 34 têm distância 3,9 entre si (são a
# mesma borda de poça espelhada), o 16, o 18 e o 32 ficam entre 9,0 e 12,9 do 27,
# e o 10 fica a 15,9 do 24. Sobraram sete com distância mínima de 15,3 entre
# quaisquer dois.
CHAO_POCA = [
    dict(nome="poca rasa",      lp=8),
    dict(nome="poca larga",     lp=17),
    dict(nome="agua parada",    lp=19),
    dict(nome="poca funda",     lp=24),
    dict(nome="filme de musgo", lp=26),
    dict(nome="lodo na agua",   lp=25),
    dict(nome="beira de poca",  lp=33),
]
# CHÃO DE TUFO, NOSSO. Metatiles do `gTileset_GeneralSinnoh` desenhados sobre a
# camada de baixo do metatile 1, com o atributo IGUAL a ele. Custam ZERO tile,
# ZERO cor, e uma vaga de metatile só quando entram espelhados.
CHAO_TUFO_NOSSO = [
    dict(nome="moita clara",   mt=14),
    dict(nome="tufo fundo",    mt=30),
    dict(nome="tufo claro",    mt=462),
    dict(nome="tufo torto",    mt=463),
    dict(nome="moita cerrada", mt=470),
]
# VARIANTE POR ESPELHO, que não custa tile nem cor. O 14 não entra porque é
# simétrico e o espelho dele não muda um pixel (medido no caso 6 do auto-teste).
ESPELHO_TUFO = [30, 462, 463, 470]

# MÓVEIS IMPORTADOS, uma célula cada.
# UMA SAMAMBAIA SÓ, e o motivo é medida: os metatiles 12, 13, 14, 20, 21, 22,
# 28, 29 e 30 do secundário do hack desenham a MESMA samambaia (191 pixels
# opacos em todos os nove; o que muda entre eles é só o pedaço de chão da fonte
# que a camada de baixo carrega, e a regra desta passada joga esse pedaço fora).
# Importar os nove seria duplicar arte para encher catálogo, que é a regra 9
# desta onda pegando alguém em flagrante. O 36 e o 37 são, esses sim, byte a
# byte iguais entre si.
MOVEIS_LP = [
    dict(nome="samambaia",       lp=12,  sobre="grama"),
    dict(nome="junco rasteiro",  lp=38,  sobre="grama"),
    dict(nome="junco torto",     lp=40,  sobre="grama"),
    dict(nome="moita de musgo",  lp=3,   sobre="grama"),
    dict(nome="estaca de cerca", lp=125, sobre="clareira"),
    dict(nome="pedra de brejo",  lp=64,  sobre="clareira"),
]
# MÓVEIS NOSSOS: metatile do PRIMÁRIO já desenhado sobre a camada de baixo do
# carimbo e já em COVERED com comportamento zerado. Custa zero.
MOVEIS_NOSSOS = [
    dict(nome="pedregulho", mt=224, sobre="grama"),
]

# BLOCOS. Retângulo de `len(topo) + 1` linhas de `largura` células: as linhas de
# `topo` continuam ANDÁVEIS (a arte mora na camada de cima e o jogador passa
# ATRÁS dela) e a linha `base` vira sólida em COVERED. `topo` vazio é bloco
# sólido inteiro, que é o caso do tronco.
# A MOITA DE BREJO (o par 100/99 do hack, que o mapa g24m04 desenha 6 vezes em
# coluna) FOI CORTADA depois do primeiro render de peça: a arte dela mora quase
# toda na camada de BAIXO, e o que sobra na de cima são 48 e 56 pixels, ou seja
# uma lasca. Com a regra apertada desta passada ela chegaria vazia, e desenhar
# uma peça vazia é pior do que não ter peça.
BLOCOS_LP = [
    dict(nome="junco alto",   topo=[[15]], base=[23],       sobre="grama",
         faixa="agua"),
    dict(nome="raiz exposta", topo=[],     base=[53, 54],   sobre="grama"),
    dict(nome="tronco caido", topo=[],     base=[107, 108], sobre="clareira"),
]

PASTORIA = dict(
    alvo="PastoriaCity",
    # OS GRUPOS SÃO GRANDES DE PROPÓSITO: grupo de uma peça só faz cada bolha
    # sair de uma cor única, e aí saber onde a célula está passa a adivinhar o
    # que ela é (caso 11a do auto-teste).
    bolhas_grama=[
        dict(grupo=["tufo claro", "tufo claro espelhado",
                    "tufo torto", "tufo torto espelhado"],    quantas=9, tam=(16, 30)),
        dict(grupo=["lama salpicada", "lama batida", "lodo",
                    "lama funda"],                            quantas=9, tam=(16, 30)),
        dict(grupo=["tufo fundo", "tufo fundo espelhado",
                    "moita clara"],                           quantas=9, tam=(14, 26)),
        dict(grupo=["lodo", "lama funda", "lama batida",
                    "lama salpicada"],                        quantas=9, tam=(14, 26)),
        dict(grupo=["moita cerrada", "moita cerrada espelhada",
                    "tufo claro", "tufo torto espelhado"],    quantas=9, tam=(13, 24)),
    ],
    bolhas_clareira=[
        dict(grupo=["poca rasa", "poca funda", "agua parada",
                    "beira de poca"],                         quantas=9, tam=(12, 22)),
        dict(grupo=["filme de musgo", "lodo na agua",
                    "poca larga", "poca rasa"],               quantas=9, tam=(12, 22)),
    ],
    moveis=[
        dict(nome="samambaia",       quantos=6, espaco=6),
        dict(nome="junco rasteiro",  quantos=6, espaco=6),
        dict(nome="junco torto",     quantos=6, espaco=6),
        dict(nome="moita de musgo",  quantos=4, espaco=7),
        dict(nome="estaca de cerca", quantos=3, espaco=8),
        dict(nome="pedra de brejo",  quantos=3, espaco=8),
        dict(nome="pedregulho",      quantos=3, espaco=8),
    ],
    blocos=[
        dict(nome="junco alto",   quantos=6, espaco=4),
        dict(nome="raiz exposta", quantos=3, espaco=8),
        dict(nome="tronco caido", quantos=2, espaco=9),
    ],
)
TEMAS = {"PastoriaCity": PASTORIA}
ORDEM = ["PastoriaCity"]

ESPACO_ENTRE_MOVEIS = 2     # Chebyshev mínimo entre dois móveis QUAISQUER
PISO_BOLHA = 6              # tamanho mínimo de uma bolha que a região cortou
RAIO_AGUA = 8               # `faixa="agua"`: Chebyshev até a água mais perto

N4 = E.N4


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem
    que sair idêntico em qualquer máquina e em qualquer versão de Python."""
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


def _vivos():
    """{ids de metatile que algum dos TRÊS layouts irmãos desenha}.

    A grade dos ALVOS entra pela base LIMPA desta passada (o disco menos o que
    esta passada gravou), e não pelo disco. Sem isso a segunda rodada reprova a
    si mesma: depois de um `--aplicar` o `map.bin` de Pastoria já usa os ids
    904 a 930, e o portão "nenhum dos 3 mapas usa este metatile" dispara contra
    a própria escrita (medido em 09/09/2026: "algum dos 3 mapas usa o metatile
    904"). Os outros dois entram como estão, porque esta passada não encosta
    neles.
    """
    guardado = carrega_plano()
    vivos = set()
    for nome in IRMAOS:
        grade = (base_de(nome, guardado) if nome in TEMAS else G.grade(nome)[4])
        vivos |= {c & 0x3FF for c in grade}
    return vivos


def orcamento():
    """(vagas de cor livres por vaga, vagas de TILE mortas, metatiles vivos).

    "Vivo" é a palavra que importa duas vezes aqui. O `gTileset_LilycoveSinnoh`
    tem 392 metatiles e só 154 deles aparecem em `map.bin` de algum dos três
    layouts com arquivo em disco; o `tiles.png` tem 512 tiles e só 126 do
    secundário são referenciados por metatile vivo. Contar os 512 daria tileset
    cheio e nada a fazer; contar só os vivos dá 386 vagas de tile e as vagas de
    paleta 7 e 10 inteiras.

    O portão que prova que isso é verdade não está aqui, está no render dos dois
    mapas irmãos com ZERO pixel diferente.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    NP = len(tp["tiles"])
    n_meta_sec = len(ts["metatiles"]) // 16
    usados = collections.defaultdict(set)
    tiles_vivos = set()
    vivos = _vivos()
    for gid in sorted(x for x in vivos if x >= 512):
        local = gid - 512
        # os metatiles que ESTA passada grava (do META_LOCAL_0 para cima) são
        # ignorados de propósito, para que rodar `--extrai` depois de
        # `--aplicar` dê o mesmo kit
        if local >= min(n_meta_sec, META_LOCAL_0):
            continue
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], local):
            if it == 0:
                continue
            tiles_vivos.add(it)
            if ip < 6:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        usados[ip].add(c)
    # A ARMADILHA 4 do `compacta_paletas.py`: metatile do PRIMÁRIO alcançável
    # também pode pintar com vaga secundária. Medido aqui é ZERO, mas a conta
    # roda de qualquer jeito, porque "medi uma vez" não é portão.
    arm4 = 0
    for gid in sorted(x for x in vivos if x < 512):
        for (it, fh, fv, ip) in RM.entradas_metatile(tp["metatiles"], gid):
            if it and ip >= 6:
                arm4 += 1
                tile = RM.resolver_tile(tp, ts, it)
                if tile is None:
                    continue
                for linha in tile:
                    for c in linha:
                        if c:
                            usados[ip].add(c)
    livres = {v: [i for i in range(1, 16) if i not in usados[v]]
              for v in range(6, 13)}
    mortas = [t - NP for t in range(NP, NP + TETO_TILES)
              if t not in tiles_vivos]
    return livres, mortas, sorted(vivos), arm4


# ---------------------------------------------------------------- a EXTRACAO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb(ts, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits DESLOCADOS TRÊS
    casas, não esticados para 0..255.

    A conta importa e já foi medida duas vezes nesta obra. As duas contas dão o
    MESMO cinco-bits depois que o `gbagfx` reconverte o `.pal` para `.gbapal`,
    então a cor dentro da ROM é a mesma; o que muda é o número escrito no `.pal`
    e, com ele, o pixel de todo render de conferência. Todo `.pal` deste
    repositório está na conta de deslocar, e o `ferramentas/prova_extracao.py`,
    que é o portão da extração, também.
    """
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def _piso_da_fonte(tset):
    """Os tiles que a FONTE usa como piso, pelo corte de 4 do `costa_sandgem`.

    Aqui ele NÃO decide o que entra na peça (ver o docstring do módulo); ele é
    só o PORTÃO do caso 2 do auto-teste, que exige que nenhum tile de camada de
    cima de peça importada esteja nesta lista.
    """
    pad = collections.Counter()
    for loc in range(len(tset["meta"]) // 16):
        e = struct.unpack_from("<8H", tset["meta"], loc * 16)[:4]
        pad[tuple(v & 0x3FF for v in e)] += 1
    fora = set()
    for p, c in pad.items():
        if c >= PISO_MIN or len(set(p)) == 1:
            fora |= set(p)
    return fora


def _lista_de_pecas():
    """[(papel, dict)] com toda peça que a extração tem que ler da ROM."""
    lista = [("chao", c) for c in CHAO_LAMA + CHAO_POCA]
    lista += [("movel", m) for m in MOVEIS_LP]
    for b in BLOCOS_LP:
        for i, linha in enumerate(b["topo"]):
            for k, loc in enumerate(linha):
                lista.append(("movel", dict(
                    nome="%s topo%d %d" % (b["nome"], i, k), lp=loc)))
        for k, loc in enumerate(b["base"]):
            lista.append(("movel", dict(nome="%s base %d" % (b["nome"], k),
                                        lp=loc)))
    return lista


def extrai():
    """Regera `brejo_pastoria_kit.json` a partir da ROM privada do Light Platinum.

    Só roda na máquina que tem `fontes-mapas/romhacks/`. O que sai daqui é o
    asset CONVERTIDO (tiles em nibbles, já reindexados para a vaga de destino, e
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
    t2 = r.parse_tileset(LP["sec"])
    if t1 is None or t2 is None:
        raise SystemExit("o par 0x%X / 0x%X do hack nao abriu"
                         % (LP["pri"], LP["sec"]))
    NP = r.n_tiles_pri
    livres, mortas, _vv, _a4 = orcamento()
    pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}
    piso = _piso_da_fonte(t2)

    def ents_de(local):
        return list(struct.unpack_from("<8H", t2["meta"], local * 16))

    def px_de(idx):
        return (_nibbles(t1["tiles"], idx) if idx < NP
                else _nibbles(t2["tiles"], idx - NP))

    def branco(v):
        """A entrada aponta para um tile 8x8 SEM UM PIXEL aceso?"""
        idx = v & 0x3FF
        if not idx:
            return True
        return not any(c for linha in px_de(idx) for c in linha)

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}

    def guarda(v):
        """Registra o tile 8x8 daquela entrada e devolve a chave dele.

        A CHAVE LEVA A PALETA DE ORIGEM, e isso não é detalhe: o mesmo desenho
        8x8 pintado com duas paletas do hack tem que virar DUAS vagas nossas,
        senão a segunda apaga a primeira.
        """
        idx, ip = v & 0x3FF, (v >> 12) & 0xF
        if ip not in VAGAS_PAL:
            return None
        lado, li = ("p", idx) if idx < NP else ("s", idx - NP)
        ch = "%s:%d:%d" % (lado, li, ip)
        destino = VAGAS_PAL[ip]
        if tiles_vaga.setdefault(ch, destino) != destino:
            raise SystemExit("o tile %s foi pedido nas vagas %d e %d"
                             % (ch, tiles_vaga[ch], destino))
        tiles_px[ch] = px_de(idx)
        origem = pal[ip]
        tiles_cor.setdefault(ch, set())
        for linha in tiles_px[ch]:
            for c in linha:
                if c:
                    tiles_cor[ch].add(tuple(origem[c]))
        return ch

    pecas = []
    for papel, p in _lista_de_pecas():
        e = ents_de(p["lp"])
        baixo, cima = e[:4], e[4:]
        tem_cima = any(not branco(v) for v in cima)
        if papel == "chao":
            # o chão entra INTEIRO na camada de baixo, e a de cima fica vazia:
            # camada de cima em célula andável com layerType NORMAL desenha
            # ACIMA do jogador.
            if tem_cima:
                raise SystemExit("%s: a peca de chao %d tem camada de cima"
                                 % (p["nome"], p["lp"]))
            if len({v & 0x3FF for v in baixo}) < 2:
                raise SystemExit("%s: o metatile %d repete o mesmo tile nos "
                                 "quatro quadrantes, e por isso e chao liso da "
                                 "fonte, nao arte" % (p["nome"], p["lp"]))
            fonte = baixo
        else:
            # A REGRA APERTADA: com camada de cima, a peça é SÓ a camada de
            # cima; sem nenhuma, a peça é a camada de baixo inteira. Ver o
            # docstring do módulo: neste tileset não há corte numérico honesto
            # que separe piso de arte na camada de baixo.
            fonte = cima if tem_cima else baixo
        usadas, saida = [], []
        for q in range(4):
            v = fonte[q]
            if not (v & 0x3FF) or branco(v):
                usadas.append(None)
                saida.append(0)
                continue
            # QUADRANTE QUE É PISO DA FONTE CAI FORA, mesmo na camada de cima.
            # Não é teoria: o metatile 38 do hack (o junco rasteiro) desenha o
            # quadrante inferior esquerdo da camada de CIMA com o tile 543, que
            # é exatamente o tile que a camada de baixo dele repete nos quatro
            # quadrantes, ou seja o chão do brejo do hack. Importado inteiro, o
            # junco chegaria com um quadrado opaco de chão da fonte grudado na
            # perna. O caso 2 do auto-teste é quem cobra isso.
            if papel != "chao" and (v & 0x3FF) in piso:
                usadas.append(None)
                saida.append(0)
                continue
            ch = guarda(v)
            if ch is None:
                if papel == "chao":
                    raise SystemExit("%s: o quadrante %d usa a paleta %d, fora "
                                     "do kit" % (p["nome"], q, (v >> 12) & 0xF))
                usadas.append(None)
                saida.append(0)
                continue
            usadas.append(ch)
            saida.append(v)
        if not any(usadas):
            raise SystemExit("%s: o metatile %d nao sobrou com nenhum "
                             "quadrante de arte" % (p["nome"], p["lp"]))
        pecas.append(dict(papel=papel, nome=p["nome"], lp=p["lp"],
                          tem_cima=tem_cima, ents=saida, usadas=usadas))

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
    # é aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, só em
    # outro índice, então o pixel sai idêntico ao da ROM.
    saida_tiles = {}
    for ch, vaga in tiles_vaga.items():
        ip = int(ch.split(":")[2])
        origem = pal[ip]
        saida_tiles[ch] = [[0 if c == 0 else indice[(vaga, tuple(origem[c]))]
                            for c in linha] for linha in tiles_px[ch]]

    dados = dict(
        fonte=dict(hack=LP["hack"], autor=LP["autor"], base=LP["base"],
                   arquivo=gba, md5=md5, pri="0x%X" % LP["pri"],
                   sec="0x%X" % LP["sec"], split=list(LP["split"]),
                   n_tiles_pri=NP),
        vagas_pal={str(k): v for k, v in VAGAS_PAL.items()},
        vagas_livres={str(k): v for k, v in livres.items()},
        vagas_tile_mortas=mortas,
        paletas=paletas, tiles=saida_tiles, tiles_vaga=tiles_vaga,
        piso_da_fonte=sorted(piso), pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d pecas"
          % (os.path.relpath(KIT_JSON, RAIZ), len(saida_tiles), len(pecas)))
    for vaga, cores in sorted(por_vaga.items()):
        print("  vaga %2d: %2d cores nos indices %s"
              % (vaga, len(cores), [indice[(vaga, c)] for c in sorted(cores)]))
    return 0


# --------------------------------------------------------------- o KIT em disco
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def chao_nosso(qual):
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele)."""
    tp = _tileset(PRIMARIO)
    mt = CARIMBOS[qual]
    ents = list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))
    if any(v & 0x3FF for v in ents[4:]):
        raise SystemExit("o carimbo %d ja usa a camada de cima" % mt)
    return ents[:4], G._attrs(PRIMARIO)[mt]


def desenha_kit():
    """(tiles_novos, metas, attrs, catalogo), sem escrever em disco."""
    dados = kit()
    ap = G._attrs(PRIMARIO)
    tp = _tileset(PRIMARIO)
    NP = len(tp["tiles"])

    por_peca = {(p["papel"], p["nome"]): p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    vagas_tile = list(dados["vagas_tile_mortas"])
    proximo = [0]
    metas, attrs = {}, {}
    vagas_meta = list(range(META_LOCAL_0, TETO_META))
    proximo_meta = [0]
    catalogo = dict(chao={}, moveis={}, blocos={}, sobre={})

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            if proximo[0] >= len(vagas_tile):
                raise SystemExit("acabaram as vagas de tile mortas")
            mapa_tile[chave] = vagas_tile[proximo[0]]
            tiles_novos[vagas_tile[proximo[0]]] = dados["tiles"][chave]
            proximo[0] += 1
        return mapa_tile[chave]

    def poe(ents, attr):
        if proximo_meta[0] >= len(vagas_meta):
            raise SystemExit("acabaram as vagas de metatile livres")
        local = vagas_meta[proximo_meta[0]]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return 512 + local

    def entrada(p, q):
        """A entrada NOSSA para o quadrante q da peça: mesmo tile, vaga nova,
        vaga de paleta nova, e os bits de espelho da fonte preservados."""
        ch = p["usadas"][q]
        if ch is None:
            return None
        v = p["ents"][q]
        alvo_pal = VAGAS_PAL[int(ch.split(":")[2])]
        return ((v & 0x0C00) | (NP + vaga(ch)) | (alvo_pal << 12))

    base_grama, attr_grama = chao_nosso("grama")
    base_clareira, attr_clareira = chao_nosso("clareira")
    BASE = dict(grama=(base_grama, attr_grama),
                clareira=(base_clareira, attr_clareira))

    # ------------------------------------------------------ 1. CHAO IMPORTADO
    for c, qual in ([(c, "grama") for c in CHAO_LAMA]
                    + [(c, "clareira") for c in CHAO_POCA]):
        p = por_peca[("chao", c["nome"])]
        ents = [entrada(p, q) for q in range(4)]
        if any(e is None for e in ents):
            raise SystemExit("%s: quadrante vazio em peca de chao" % c["nome"])
        gid = poe(ents + [0, 0, 0, 0], BASE[qual][1])
        catalogo["chao"][c["nome"]] = gid
        catalogo["sobre"][c["nome"]] = qual

    # ------------------------------------------------------ 2. CHAO NOSSO
    for c in CHAO_TUFO_NOSSO:
        if ap[c["mt"]] != attr_grama:
            raise SystemExit("o metatile %d tem atributo 0x%04X e o carimbo de "
                             "grama tem 0x%04X" % (c["mt"], ap[c["mt"]], attr_grama))
        ents = list(struct.unpack_from("<8H", tp["metatiles"], c["mt"] * 16))
        if ents[:4] != base_grama:
            raise SystemExit("o metatile %d nao esta desenhado sobre a grama do "
                             "carimbo" % c["mt"])
        catalogo["chao"][c["nome"]] = c["mt"]
        catalogo["sobre"][c["nome"]] = "grama"
    por_mt = {c["mt"]: c["nome"] for c in CHAO_TUFO_NOSSO}
    for mt in ESPELHO_TUFO:
        ents = list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))
        nome = por_mt[mt] + (" espelhada" if por_mt[mt].startswith("moita")
                             else " espelhado")
        gid = poe(list(base_grama) + _espelha4(ents[4:]), attr_grama)
        catalogo["chao"][nome] = gid
        catalogo["sobre"][nome] = "grama"

    # ---------------------------------------------------- 3. MOVEIS de 1 celula
    for m in MOVEIS_LP:
        p = por_peca[("movel", m["nome"])]
        cima = [entrada(p, q) or 0 for q in range(4)]
        if not any(cima):
            raise SystemExit("%s: peca sem arte" % m["nome"])
        base, _a = BASE[m["sobre"]]
        # comportamento ZERADO (nenhum id semântico é importado) e layerType
        # COVERED, que põe as duas camadas ABAIXO do sprite.
        gid = poe(list(base) + cima, 0x1000)
        catalogo["moveis"][m["nome"]] = gid
        catalogo["sobre"][m["nome"]] = m["sobre"]
    for m in MOVEIS_NOSSOS:
        base, _a = BASE[m["sobre"]]
        ents = list(struct.unpack_from("<8H", tp["metatiles"], m["mt"] * 16))
        if ents[:4] != base:
            raise SystemExit("o metatile %d nao esta desenhado sobre o carimbo "
                             "de %s" % (m["mt"], m["sobre"]))
        if ap[m["mt"]] != 0x1000:
            raise SystemExit("o metatile %d nao esta em COVERED com "
                             "comportamento zerado (0x%04X)"
                             % (m["mt"], ap[m["mt"]]))
        catalogo["moveis"][m["nome"]] = m["mt"]
        catalogo["sobre"][m["nome"]] = m["sobre"]

    # ------------------------------------------------- 4. BLOCOS de N celulas
    for b in BLOCOS_LP:
        base, attr_base = BASE[b["sobre"]]
        topos = []
        for i, linha in enumerate(b["topo"]):
            fora = []
            for k, _loc in enumerate(linha):
                p = por_peca[("movel", "%s topo%d %d" % (b["nome"], i, k))]
                cima = [entrada(p, q) or 0 for q in range(4)]
                if not any(cima):
                    raise SystemExit("%s: metade sem arte" % b["nome"])
                fora.append(poe(list(base) + cima, attr_base))
            topos.append(fora)
        bases = []
        for k, _loc in enumerate(b["base"]):
            p = por_peca[("movel", "%s base %d" % (b["nome"], k))]
            cima = [entrada(p, q) or 0 for q in range(4)]
            if not any(cima):
                raise SystemExit("%s: metade sem arte" % b["nome"])
            bases.append(poe(list(base) + cima, 0x1000))
        catalogo["blocos"][b["nome"]] = dict(topo=topos, base=bases)
        catalogo["sobre"][b["nome"]] = b["sobre"]

    # A vaga de metatile só serve se NENHUM dos três mapas vivos usar o id.
    usados = _vivos()
    for local in metas:
        if 512 + local in usados:
            raise SystemExit("algum dos 3 mapas usa o metatile %d" % (512 + local))
    # A vaga de TILE só serve se nenhum metatile VIVO a referenciar.
    mortas = set(dados["vagas_tile_mortas"])
    for v in tiles_novos:
        if v not in mortas:
            raise SystemExit("a vaga de tile %d nao esta na lista de mortas" % v)
    return tiles_novos, metas, attrs, catalogo


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    Idempotente: as vagas de tile, de paleta e de metatile são FIXAS.
    """
    from PIL import Image
    dados = kit()
    # ARMADILHA JÁ PAGA POR OUTRA FRENTE: `Image.convert("P")` numa imagem que
    # JÁ é "P" devolve uma CÓPIA e não converte, e uma frente desta onda gravou
    # metatiles e NENHUM tile por causa disso. Aqui a imagem é aberta e escrita
    # direto, sem conversão nenhuma, e o auto-teste relê o PNG do disco.
    im = Image.open(f"{DESTINO}/tiles.png")
    if im.mode != "P":
        raise SystemExit("o tiles.png nao esta em modo P (esta em %s)" % im.mode)
    im = im.copy()
    cols = im.size[0] // 8
    px = im.load()
    for v, tile in tiles_novos.items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        if y0 + 8 > im.size[1]:
            raise SystemExit("a vaga de tile %d nao cabe no tiles.png" % v)
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    im.save(f"{DESTINO}/tiles.png")

    for vaga, cores in sorted(dados["paletas"].items()):
        _grava_pal(int(vaga), cores)

    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    # O arquivo tem 392 entradas e esta passada grava a partir da 392: estender
    # com ZERO é o que torna o diff puramente aditivo.
    if len(meta) < TETO_META * 16:
        meta += bytes(TETO_META * 16 - len(meta))
    if len(attr) < TETO_META * 2:
        attr += bytes(TETO_META * 2 - len(attr))
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
def bolhas(livres, spec, semente=0x5EED):
    """[(nomes, {celulas})], bolhas orgânicas crescidas por frente de onda.

    A SEMENTE não é sorteio solto: as células livres são ordenadas por um hash
    da posição e a semente só é aceita a pelo menos 2 (Chebyshev) de toda
    semente já aceita. O CRESCIMENTO é guloso com ruído: a cada passo entra a
    célula da frente de onda com o menor hash. Círculo daria bolha redonda e
    xadrez daria sal e pimenta; frente de onda com ruído dá contorno irregular.

    A ORDEM É POR RODADA, e não por especificação inteira: servindo UMA bolha
    por especificação a cada rodada, o que falta no fim é o excedente de todo
    mundo, e não a lista inteira de quem estava no fim da fila.
    """
    ordem = sorted(livres, key=lambda p: _mistura(p[0], p[1], semente))
    tomadas, saida, sementes = set(), [], []
    feitas = [0] * len(spec)
    while True:
        andou = False
        for k, esp in enumerate(spec):
            if feitas[k] >= esp["quantas"]:
                continue
            achou = None
            for p in ordem:
                if p in tomadas:
                    continue
                if any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) < 2
                       for q in sementes):
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
                # ACEITA A BOLHA CURTA quando foi a REGIÃO que acabou, e não a
                # vontade de crescer. O piso absoluto de PISO_BOLHA existe para
                # que "mancha" continue querendo dizer mancha.
                if len(corpo) < lo and (frente or len(corpo) < PISO_BOLHA):
                    continue
                achou = (p, corpo)
                break
            if achou is None:
                feitas[k] = esp["quantas"]     # não há mais lugar para esta
                continue
            p, corpo = achou
            tomadas |= corpo
            sementes.append(p)
            saida.append((esp["grupo"], corpo))
            feitas[k] += 1
            andou = True
        if not andou:
            break
    return saida


def peca_da_mancha(nomes, x, y):
    """Qual das peças do grupo cai nesta célula. Hash da posição, não paridade:
    paridade vira xadrez e o auto-teste reprova."""
    return nomes[_mistura(x, y, 0xA5A5 + len(nomes)) % len(nomes)]


# ----------------------------------------------------------- ligacao a pe
def componentes(v, W, H):
    """{celula: rotulo} dos pedaços de chão andável ligados a pé.

    POR QUE NÃO BASTA O `enfeita_cidades.alcance`: aquele mede "quem ainda é
    alcançável a partir de algum ponto de partida", e ponto de partida ali é
    warp OU objeto; fechar um corredor com warp dos dois lados não tira NENHUMA
    célula do alcance e mesmo assim parte a cidade em duas.
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
def plano_mapa(alvo, catalogo, base=None):
    """(L, W, H, v, escritas, contas) para UM mapa."""
    T = TEMAS[alvo]
    d, L, W, H, v0 = G.grade(alvo)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    # As duas FAMÍLIAS de chão. Uma célula só é elegível se ainda for o carimbo
    # puro, se estiver na elevação dominante daquele carimbo e se não for água
    # para o motor.
    fam, elev = {}, {}
    for qual, mt in CARIMBOS.items():
        alvos = [c for c in v if (c & 0x3FF) == mt and not ((c >> 10) & 3)]
        if not alvos:
            elev[qual] = None
            fam[qual] = set()
            continue
        elev[qual] = collections.Counter((c >> 12) & 0xF
                                         for c in alvos).most_common(1)[0][0]
        fam[qual] = {(i % W, i // W) for i in range(W * H)
                     if not ((v[i] >> 10) & 3) and (v[i] & 0x3FF) == mt
                     and ((v[i] >> 12) & 0xF) == elev[qual]
                     and beh(v[i] & 0x3FF) not in AG}

    # A FAIXA DE ÁGUA, para o junco: célula a até RAIO_AGUA (Chebyshev) de
    # alguma célula que o motor trata como água. Junco não nasce no meio do
    # quintal; ele nasce na beira da lagoa e na beira do mar, e Pastoria tem os
    # dois. A conta é feita sobre a grade BASE.
    agua = [(i % W, i // W) for i in range(W * H) if beh(v[i] & 0x3FF) in AG]
    perto_agua = set()
    for ax, ay in agua:
        for dx in range(-RAIO_AGUA, RAIO_AGUA + 1):
            for dy in range(-RAIO_AGUA, RAIO_AGUA + 1):
                perto_agua.add((ax + dx, ay + dy))

    escritas = {}
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

    def livre(x, y, qual):
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas or (x, y) not in fam[qual]:
            return False
        return (aplicado[i] & 0x3FF) == CARIMBOS[qual]

    def espacado(nome, esp, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < esp
                       for px, py in por_movel[nome])

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portões deixarem.

        O portão roda NA HORA e não só no fim: se solidificar esta célula tirar
        do alcance a pé qualquer OUTRA célula, ou partir um pedaço de chão em
        dois, a escrita é desfeita e o gerador segue.
        """
        i = y * W + x
        antigo = aplicado[i]
        aplicado[i] = (antigo & 0xF000) | (1 << 10) | mt_id   # elevação INTACTA
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

    # ------ 1. BLOCOS, antes da mobília de uma célula, porque cada um precisa
    # de um retângulo inteiro e a mobília solta não pode ter comido metade dele.
    # As linhas de `topo` continuam ANDÁVEIS e por isso não entram em
    # `novos_solidos` nem no portão de alcance; a linha de baixo vira sólida.
    conta_bloco = collections.Counter()
    por_bloco = []
    for b in T["blocos"]:
        info = catalogo["blocos"][b["nome"]]
        qual = catalogo["sobre"][b["nome"]]
        larg = len(info["base"])
        alt = len(info["topo"]) + 1
        for x, y in ordem_cel:
            if conta_bloco[b["nome"]] >= b["quantos"]:
                break
            cels = [(x + dx, y + dy) for dy in range(alt) for dx in range(larg)]
            if any(not (0 <= cx < W and 0 <= cy < H) for cx, cy in cels):
                continue
            if b.get("faixa") == "agua" and not all(c in perto_agua for c in cels):
                continue
            if any(not livre(cx, cy, qual) for cx, cy in cels):
                continue
            if any(max(abs(x - px), abs(y - py)) < b["espaco"]
                   for px, py in por_bloco):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            topo_cels = []
            for i_lin, linha_ids in enumerate(info["topo"]):
                for k in range(larg):
                    cx, cy = x + k, y + i_lin
                    j = cy * W + cx
                    escritas[j] = (aplicado[j] & 0xFC00) | linha_ids[k]
                    aplicado[j] = escritas[j]
                    topo_cels.append((cx, cy))
            ok = True
            feitas = []
            for k in range(larg):
                cx, cy = x + k, y + alt - 1
                if not tenta_solidificar(cx, cy, info["base"][k]):
                    ok = False
                    break
                feitas.append((cx, cy))
            if not ok:
                for cx, cy in topo_cels:
                    j = cy * W + cx
                    del escritas[j]
                    aplicado[j] = v[j]
                for cx, cy in feitas:
                    novos_solidos.remove((cx, cy))
                    postos.remove((cx, cy))
                    del escritas[cy * W + cx]
                    aplicado[cy * W + cx] = v[cy * W + cx]
                continue
            por_bloco += cels
            postos += topo_cels
            conta_bloco[b["nome"]] += 1

    # ------ 2. MÓVEIS de uma célula. Eles vêm ANTES da mancha de propósito, e a
    # razão está medida em Snowpoint: móvel posto no carimbo tira uma célula do
    # numerador E do denominador da régua; móvel posto em cima de uma mancha
    # tira só do denominador, o que PIORA a conta.
    lista = T["moveis"]
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            m = lista[(giro + k) % len(lista)]
            if conta_mov[m["nome"]] >= m["quantos"]:
                continue
            qual = catalogo["sobre"][m["nome"]]
            if not livre(x, y, qual) or not espacado(m["nome"], m["espaco"], x, y):
                continue
            # MÓVEL DE CIDADE ENCOSTA EM ALGUMA COISA: ou num sólido, ou na
            # BEIRA da própria família. Peça solta no meio do vazio lê como erro
            # de mapa.
            #
            # A primeira versão pedia "sólido OU a OUTRA família", e ela deixou
            # a CLAREIRA com ZERO móveis, medido: nenhuma das 126 células livres
            # de clareira faz fronteira com uma célula de grama pura. O motivo
            # está no desenho do demake: entre o metatile 473 e o metatile 1 há
            # SEMPRE uma fileira de metatiles de transição (o 464, o 465, o 466,
            # o 472, o 474, o 481 e o 482), então as duas famílias nunca se
            # tocam. A regra passou a ser "sólido ou beira da própria família",
            # que é a mesma ideia sem a suposição errada.
            perto = any(not (0 <= x + dx < W and 0 <= y + dy < H)
                        or ((aplicado[(y + dy) * W + x + dx] >> 10) & 3)
                        or (x + dx, y + dy) not in fam[qual]
                        for dx, dy in N4)
            if not perto:
                continue
            if not tenta_solidificar(x, y, catalogo["moveis"][m["nome"]]):
                continue
            por_movel[m["nome"]].append((x, y))
            conta_mov[m["nome"]] += 1
            break

    # ------------------------------------------------------------- 3. MANCHA
    conta_mancha = collections.Counter()

    def pintavel(p, qual):
        i = p[1] * W + p[0]
        return (p in fam[qual] and i not in escritas and p not in gelo
                and (aplicado[i] & 0x3FF) == CARIMBOS[qual])

    def pinta(p, nomes):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | catalogo["chao"][nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    for qual, chave_bolhas in (("grama", "bolhas_grama"),
                               ("clareira", "bolhas_clareira")):
        livres = {p for p in fam[qual] if pintavel(p, qual)}
        for nomes, corpo in bolhas(livres, T[chave_bolhas],
                                   0x5EED if qual == "grama" else 0xB0A7):
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
    contas = dict(moveis=dict(conta_mov), blocos=dict(conta_bloco),
                  manchas=dict(conta_mancha), solidos=len(novos_solidos),
                  grama=len(fam["grama"]), clareira=len(fam["clareira"]),
                  perto_agua=len(perto_agua & fam["grama"]))
    return L, W, H, v, escritas, contas


def regua(v, W, H, L, escritas=None):
    """(carimbo dominante em %, células andáveis a pé, id do carimbo), como a
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
    """A grade como está no disco, só tirando o que ESTA passada escreveu.

    Sem isso a idempotência morre: planejar sobre um mapa já desenhado não volta
    ao mesmo lugar.
    """
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(alvos, aplicar):
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    print("kit: %d tiles novos (vagas mortas %d a %d), %d metatiles novos "
          "(locais %d a %d, ids %d a %d)"
          % (len(tiles_novos), min(tiles_novos), max(tiles_novos), len(metas),
             min(metas), max(metas), 512 + min(metas), 512 + max(metas)))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    for alvo in alvos:
        base = base_de(alvo, guardado)
        L, W, H, v, escritas, contas = plano_mapa(alvo, catalogo, base)
        a, na, ida = regua(v, W, H, L)
        b, nb, idb = regua(v, W, H, L, escritas)
        print("%s: %d celulas de mancha, %d solidificadas, %d mudadas "
              "(familia grama %d, clareira %d, grama perto de agua %d)"
              % (alvo, sum(contas["manchas"].values()), contas["solidos"],
                 len(escritas), contas["grama"], contas["clareira"],
                 contas["perto_agua"]))
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


def confere(alvos, tiles_novos, metas, attrs, catalogo, planos):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela é chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que
    tem que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida só no caminho feliz não é regra, e prova positiva sem
    par negativo não é prova.
    """
    mau = []
    dados = kit()
    ap = G._attrs(PRIMARIO)
    import render_maps as RM
    tp = _tileset(PRIMARIO)
    ts = _tileset(SECUNDARIO)
    NP = len(tp["tiles"])
    asec = G._attrs(SECUNDARIO)

    def atributo(mt_id):
        """Atributo de um metatile, com o kit desta rodada valendo por cima."""
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
        if loc * 16 + 16 > len(tset["metatiles"]):
            return [0] * 8
        return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))

    def px_de(mt_id):
        """Os 256 pixels RGB do metatile, com o kit desta rodada valendo."""
        from PIL import Image
        im = Image.new("RGB", (16, 16), tuple(tp["paletas"][0][0]))
        p = im.load()
        ent = entradas(mt_id)
        for cam in (0, 1):
            for q in range(4):
                val = ent[cam * 4 + q]
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if not idx:
                    continue
                vaga = idx - NP
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
        return list(im.getdata())

    # ------------------------------------------------------------ 1. orcamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    mortas = set(dados["vagas_tile_mortas"])
    for v in tiles_novos:
        if v not in mortas:
            mau.append("a vaga de tile %d nao esta na lista de vagas mortas "
                       "e algum metatile vivo desenha com ela" % v)
    for local in metas:
        if local < META_LOCAL_0:
            mau.append("o metatile %d fica ABAIXO do rabo do arquivo e "
                       "sobrescreveria metatile que ja existe" % (512 + local))
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

    # ---------- 2. o kit não pode importar paleta de origem fora de VAGAS_PAL,
    #             e nenhum tile de camada de CIMA de peça importada pode estar
    #             na lista de piso da fonte
    piso = set(dados["piso_da_fonte"])
    for ch in dados["tiles"]:
        ip = int(ch.split(":")[2])
        if ip not in VAGAS_PAL:
            mau.append("o kit importou a paleta %d da fonte, fora do plano" % ip)
    for p in dados["pecas"]:
        if p["papel"] == "chao" or not p["tem_cima"]:
            continue
        for v in p["ents"]:
            if (v & 0x3FF) and (v & 0x3FF) in piso:
                mau.append("a peca %s importou na camada de cima o tile %d, "
                           "que e piso da fonte" % (p["nome"], v & 0x3FF))

    # -------- 3. CHAO novo: atributo idêntico ao do carimbo em que ele pousa e,
    #             quando importado, camada de cima VAZIA
    importados = {c["nome"] for c in CHAO_LAMA + CHAO_POCA}
    for nome, gid in catalogo["chao"].items():
        qual = catalogo["sobre"][nome]
        _b, attr_chao = chao_nosso(qual)
        if atributo(gid) != attr_chao:
            mau.append("o chao %s (%d) tem atributo 0x%04X e o carimbo de %s tem "
                       "0x%04X" % (nome, gid, atributo(gid), qual, attr_chao))
        cima = [e for e in entradas(gid)[4:] if e & 0x3FF]
        if cima and nome in importados:
            mau.append("o chao importado %s (%d) usa a camada de cima"
                       % (nome, gid))
        # CAMADA DE CIMA EM CHAO ANDAVEL. Com layerType NORMAL ela vai para o
        # BG1, que desenha ACIMA do sprite. O tufo nosso desenha em cima de
        # propósito, que é o "jogador atrás do mato" do jogo base; o que ele não
        # pode é tapar o jogador INTEIRO (defeito E3 do `mapas_qa.py`).
        if cima and (atributo(gid) >> 12) & 0xF != 1:
            op = 0
            for e in cima:
                vaga = (e & 0x3FF) - NP
                t = (tiles_novos[vaga] if vaga in tiles_novos
                     else RM.resolver_tile(tp, ts, e & 0x3FF))
                op += _opacos(t) if t else 64
            if op >= 4 * 64:
                mau.append("o chao %s (%d) tapa o jogador inteiro (E3)"
                           % (nome, gid))

    # ------- 4. MOVEL e BASE de bloco: COVERED, comportamento zerado, e o NOSSO
    #            chão entrada por entrada na camada de baixo
    ids_base = {}
    for nome, info in catalogo["blocos"].items():
        for gid in info["base"]:
            ids_base[gid] = nome
    for gid, nome in list((g, n) for n, g in catalogo["moveis"].items()) \
            + list(ids_base.items()):
        qual = catalogo["sobre"][nome]
        base, _ac = chao_nosso(qual)
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %s (%d) nao esta em COVERED" % (nome, gid))
        if a & 0xFF:
            mau.append("o movel %s (%d) importou comportamento 0x%02X da fonte"
                       % (nome, gid, a & 0xFF))
        if entradas(gid)[:4] != base:
            mau.append("o movel %s (%d) nao tem o nosso chao de %s na camada de "
                       "baixo" % (nome, gid, qual))

    # ---- 5. TOPO de bloco: continua ANDÁVEL com o atributo do chão, e a arte
    #        dele NÃO pode ser 100% opaca, senão ela tapa o jogador (E3)
    for nome, info in catalogo["blocos"].items():
        qual = catalogo["sobre"][nome]
        base, attr_chao = chao_nosso(qual)
        for linha in info["topo"]:
            for gid in linha:
                if atributo(gid) != attr_chao:
                    mau.append("o topo de bloco %s (%d) nao herdou o atributo "
                               "do chao" % (nome, gid))
                if entradas(gid)[:4] != base:
                    mau.append("o topo de bloco %s (%d) nao tem o nosso chao "
                               "embaixo" % (nome, gid))
                px = 0
                for e in entradas(gid)[4:]:
                    if e & 0x3FF:
                        vaga = (e & 0x3FF) - NP
                        px += (_opacos(tiles_novos[vaga]) if vaga in tiles_novos
                               else 64)
                if px >= 4 * 64:
                    mau.append("o topo de bloco %s (%d) tapa o jogador inteiro "
                               "(E3)" % (nome, gid))

    # ---------- 6. nenhuma variante de chão é cópia pixel a pixel de outra
    for qual in ("grama", "clareira"):
        lista = [g for n, g in catalogo["chao"].items()
                 if catalogo["sobre"][n] == qual] + [CARIMBOS[qual]]
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                dd = sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
                         for p, q in zip(pix[a], pix[b])) / 256.0
                if dd < 8.0:
                    mau.append("as variantes de chao %d e %d de %s tem distancia "
                               "%.1f, abaixo do piso de 8,0 do varia_carimbo.py: "
                               "isso e enganar a regua" % (a, b, qual, dd))

    # -------------------------------------------- 7 a 13. o plano, mapa a mapa
    for alvo in alvos:
        L, W, H, v, escritas, contas = planos[alvo]
        d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
        ev = E.eventos(d)
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        meus_chaos = {catalogo["chao"][n]: n for n in catalogo["chao"]}
        meus_moveis = {catalogo["moveis"][n]: n for n in catalogo["moveis"]}
        meus_topos = {t: n for n, b in catalogo["blocos"].items()
                      for linha in b["topo"] for t in linha}
        meus_bases = {t: n for n, b in catalogo["blocos"].items()
                      for t in b["base"]}

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
                nome = meus_chaos.get(novo) or meus_topos.get(novo)
                if cn != cv or velho != CARIMBOS[catalogo["sobre"][nome]]:
                    mau.append("%s: chao/topo em celula errada em (%d,%d)"
                               % (alvo, x, y))
            elif novo in meus_moveis or novo in meus_bases:
                nome = meus_moveis.get(novo) or meus_bases.get(novo)
                if cv or not cn:
                    mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                               % (alvo, x, y))
                if velho != CARIMBOS[catalogo["sobre"][nome]]:
                    mau.append("%s: movel fora do carimbo em (%d,%d)" % (alvo, x, y))
                if (x, y) in ev:
                    mau.append("%s: movel em cima do evento (%d,%d)" % (alvo, x, y))
            else:
                mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                           % (alvo, novo, x, y))

        # 8. (comportamento, layerType) de toda célula ANDÁVEL fica igual
        for i in range(W * H):
            if (saida[i] >> 10) & 3:
                continue
            a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
            if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
                mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                           "layerType)" % (alvo, i % W, i // W))
                break

        # 9 e 10. alcance a pé e LIGACAO a pé
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

        # 10b. NENHUMA célula que a suíte já anda pode ter virado sólida. O
        # `corredores_de_teste` já congela isso no gerador; aqui a conta é
        # refeita FORA dele, porque foi assim que sete casos de balsa caíram em
        # Canalave.
        corr = E.corredores_de_teste(alvo, v, W, H, d)
        if solid & corr:
            mau.append("%s: %d celulas de corredor da suite viraram solidas: %s"
                       % (alvo, len(solid & corr), sorted(solid & corr)[:6]))

        # 11. A MANCHA NÃO PODE SER ADIVINHÁVEL, e o teste tem dois lados.
        #  (a) PADRÃO: nenhuma projeção simples da posição pode ADIVINHAR a peça.
        #  (b) FORMA: mancha é BOLHA, não sal e pimenta, e a conta é o TAMANHO
        #      MÉDIO do pedaço conexo.
        mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
                  if (val & 0x3FF) in meus_chaos}
        if len(mancha) < 200:
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

        # 12. a régua tem que fechar em 20% ou menos
        b, nb, idb = regua(v, W, H, L, escritas)
        if b > TETO_REGUA:
            mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                       % (alvo, b))

        # 13. o bloco: toda BASE tem o retângulo inteiro escrito, e as contas
        #     batem linha por linha
        for nome, info in catalogo["blocos"].items():
            larg = len(info["base"])
            alt = len(info["topo"]) + 1
            bases = sorted((i % W, i // W) for i, val in escritas.items()
                           if (val & 0x3FF) in info["base"])
            if len(bases) % larg:
                mau.append("%s: o bloco %s tem %d celulas de base, que nao e "
                           "multiplo de %d" % (alvo, nome, len(bases), larg))
            cantos = [(x, y) for x, y in bases
                      if (escritas.get(y * W + x, 0) & 0x3FF) == info["base"][0]]
            for x, y in cantos:
                for k in range(larg):
                    j = y * W + x + k
                    if (escritas.get(j, 0) & 0x3FF) != info["base"][k]:
                        mau.append("%s: a base do bloco %s em (%d,%d) esta "
                                   "incompleta" % (alvo, nome, x, y))
                        break
                for i_lin, linha_ids in enumerate(info["topo"]):
                    for k in range(larg):
                        j = (y - alt + 1 + i_lin) * W + x + k
                        if (escritas.get(j, 0) & 0x3FF) != linha_ids[k]:
                            mau.append("%s: o bloco %s em (%d,%d) esta sem a "
                                       "linha de topo %d"
                                       % (alvo, nome, x, y, i_lin))
                            break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo(alvos):
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferença" só vale depois que a comparação mostra que sabe reprovar.
    """
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    guardado = carrega_plano()
    planos = {}
    for alvo in ORDEM:
        planos[alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))

    ts_do_disco = _tileset(SECUNDARIO)
    mau = confere(ORDEM, tiles_novos, metas, attrs, catalogo, planos)
    negativas = []

    def sabota(nome, funcao, espera):
        """Roda `funcao`, que devolve os dados sabotados, e exige acusação."""
        args = funcao()
        queixas = confere(ORDEM, *args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NAO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    def copia():
        return (dict(tiles_novos), dict(metas), dict(attrs),
                json.loads(json.dumps(catalogo)),
                {k: (v[0], v[1], v[2], list(v[3]), dict(v[4]), v[5])
                 for k, v in planos.items()})

    alvo0 = "PastoriaCity"

    # N1. colisão 1 -> 0 numa célula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a célula ERA sólida
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. comportamento de um metatile de CHAO importado sabotado
    def n3():
        a = copia()
        gid = a[3]["chao"][CHAO_LAMA[0]["nome"]]
        a[2][gid - 512] = (a[2][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chao sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = a[3]["moveis"][MOVEIS_LP[0]["nome"]]
        a[2][gid - 512] = a[2][gid - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no movel", n4, "nao esta em COVERED")

    # N5. bloco gravado SEM a linha de topo
    def n5():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
        topos = {t for b in catalogo["blocos"].values()
                 for linha in b["topo"] for t in linha}
        for i in sorted(esc):
            if (esc[i] & 0x3FF) in topos:
                del esc[i]
                break
        return a
    sabota("bloco sem a linha de topo", n5, "sem a linha de topo")

    # N6. camada de BAIXO de um móvel sabotada (chão da fonte em vez do nosso)
    def n6():
        a = copia()
        gid = a[3]["moveis"][MOVEIS_LP[0]["nome"]]
        ent = list(a[1][gid - 512])
        ent[0] = ent[4]
        a[1][gid - 512] = ent
        return a
    sabota("camada de baixo sabotada", n6, "nao tem o nosso chao de")

    # N7. a peça de CLAREIRA pousando na camada de baixo da GRAMA. É a sabotagem
    #     que só existe porque esta passada tem DOIS carimbos.
    def n7():
        a = copia()
        gid = a[3]["blocos"]["tronco caido"]["base"][0]
        base_g, _ = chao_nosso("grama")
        a[1][gid - 512] = list(base_g) + list(a[1][gid - 512])[4:]
        return a
    sabota("movel de clareira com chao de grama", n7,
           "nao tem o nosso chao de clareira")

    # N8. mancha escolhida por (x + y) % n, que é xadrez com período
    def n8():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            for alvo in ORDEM:
                a[4][alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por (x+y) % n", n8, "virou padrao")

    # N9. mancha escolhida por x % n
    def n9():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[x % len(nomes)]
        try:
            for alvo in ORDEM:
                a[4][alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por x % n", n9, "virou padrao")

    # N10. corredor fechado que PARTE um pedaço de chão. O portão de alcance
    #      sozinho não pega isso quando há warp dos dois lados.
    def n10():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
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
        raise SystemExit("nao achei ponto de articulacao para a sabotagem N10")
    sabota("corredor fechado", n10, "se partiu")

    # N11. duas variantes de chão IGUAIS pixel a pixel: é enganar a régua
    def n11():
        a = copia()
        nomes = [c["nome"] for c in CHAO_POCA]
        a[1][a[3]["chao"][nomes[1]] - 512] = list(a[1][a[3]["chao"][nomes[0]] - 512])
        return a
    sabota("variante de chao duplicada", n11, "abaixo do piso de 8,0")

    # N12. cor nova escrita num índice que os NOSSOS pixels já usam. As vagas 7
    #      e 10 estão 100% livres, então a sabotagem precisa da vaga que TEM
    #      índice ocupado; o kit é reescrito no disco declarando essa vaga com
    #      um índice em uso trocado.
    def n12():
        a = copia()
        dados = kit()
        alvo_vaga = None
        for vaga in range(6, 13):
            livres_v = set(dados["vagas_livres"].get(str(vaga)) or [])
            usados = [i for i in range(1, 16) if i not in livres_v]
            if usados:
                alvo_vaga, idx = str(vaga), usados[0]
                break
        if alvo_vaga is None:
            raise SystemExit("nao ha vaga com indice em uso para sabotar")
        pal = [list(c) for c in ts_do_disco["paletas"][int(alvo_vaga)]]
        pal[idx] = [255, 0, 255]
        dados["paletas"][alvo_vaga] = pal
        with open(KIT_JSON + ".sab", "w") as f:
            json.dump(dados, f)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        return a
    try:
        sabota("cor nova em indice ja usado", n12, "que algum pixel nosso usa")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # N13. gravar numa vaga de tile VIVA, ou seja em cima de um tile que algum
    #      metatile vivo dos três mapas irmãos desenha. É a sabotagem própria
    #      desta passada, que escreve em tileset CHEIO.
    def n13():
        a = copia()
        dados = kit()
        mortas = set(dados["vagas_tile_mortas"])
        viva = next(v for v in range(TETO_TILES) if v not in mortas)
        a[0][viva] = a[0][min(a[0])]
        return a
    sabota("grava em vaga de tile viva", n13, "nao esta na lista de vagas mortas")

    # N14. gravar num metatile ABAIXO do rabo, ou seja em cima de um metatile
    #      que o `metatiles.bin` já define.
    def n14():
        a = copia()
        a[1][0] = list(a[1][min(a[1])])
        a[2][0] = 0x1000
        return a
    sabota("grava em metatile ja definido", n14, "fica ABAIXO do rabo")

    # N15. móvel plantado numa célula que a suíte anda. É o defeito que derrubou
    #      sete casos de balsa em Canalave, e o único que este auto-teste
    #      poderia deixar passar porque o gerador é quem congela o corredor.
    def n15():
        a = copia()
        L, W, H, v, esc, ct = a[4][alvo0]
        d = json.load(open(f"{RAIZ}/data/maps/{alvo0}/map.json"))
        corr = E.corredores_de_teste(alvo0, v, W, H, d)
        gid = catalogo["moveis"][MOVEIS_NOSSOS[0]["nome"]]
        for x, y in sorted(corr):
            i = y * W + x
            if i in esc or (v[i] >> 10) & 3:
                continue
            if (v[i] & 0x3FF) != CARIMBOS["grama"]:
                continue
            esc[i] = (v[i] & 0xF000) | (1 << 10) | gid
            return a
        raise SystemExit("nao achei celula de corredor para a sabotagem N15")
    sabota("movel no corredor da suite", n15, "celulas de corredor da suite")

    # ------------------------------------------------ o que está NO DISCO
    # Sem este caso o auto-teste só confere o que ele mesmo acabou de calcular.
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.load()

    postas = [l for l in metas
              if (l + 1) * 16 <= len(meta_disco)
              and _entradas(meta_disco, l) == metas[l]]
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
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if y0 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
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
        _, _, _, _, esc2, _ = plano_mapa(alvo, catalogo, volta)
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
        print("    %-34s -> %s" % (nome, queixa[:100]))
    return 0


# ------------------------------------------------- prova de TILE contra a ROM
def prova_tiles():
    """Cada tile do kit, DEPOIS de reindexado, contra o tile da ROM: zero pixel.

    Reindexar nibble é a única coisa que este kit faz com o desenho da fonte, e é
    exatamente onde um erro passaria despercebido: a arte continuaria parecendo
    arte, com as cores trocadas de lugar. A conta é direta: para cada tile do
    kit, o pixel (x,y) tem que ter a MESMA COR RGB que o pixel (x,y) do tile
    correspondente da ROM, lido com a paleta de origem dele.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("--prova-tiles so roda na maquina que tem as ROMs")
    sys.path.insert(0, f"{ferr}/ferramentas")
    from gbamap import Rom  # noqa: E402
    p = os.path.join(ferr, LP["slug"])
    gba = [f for f in sorted(os.listdir(p)) if f.lower().endswith(".gba")][0]
    r = Rom(os.path.join(p, gba))
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = LP["split"]
    t1, t2 = r.parse_tileset(LP["pri"]), r.parse_tileset(LP["sec"])
    pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}
    dados = kit()
    n, dif = 0, 0
    for ch, px_kit in dados["tiles"].items():
        lado, li, ip = ch.split(":")
        li, ip = int(li), int(ip)
        crus = _nibbles((t1 if lado == "p" else t2)["tiles"], li)
        vaga = dados["tiles_vaga"][ch]
        cores_nossas = dados["paletas"][str(vaga)]
        for y in range(8):
            for x in range(8):
                n += 1
                a = tuple(pal[ip][crus[y][x]]) if crus[y][x] else None
                b = (tuple(cores_nossas[px_kit[y][x]]) if px_kit[y][x] else None)
                if a != b:
                    dif += 1
                    if dif == 1:
                        print("  primeiro: tile %s (%d,%d) rom=%s kit=%s"
                              % (ch, x, y, a, b))
    print("tiles do kit contra a ROM: %d pixels, %d diferentes" % (n, dif))
    # a conta tem que saber REPROVAR
    ch0 = sorted(dados["tiles"])[0]
    salvo = [linha[:] for linha in dados["tiles"][ch0]]
    dados["tiles"][ch0][0][0] = (salvo[0][0] + 1) % 16
    ruim = 0
    crus = _nibbles((t1 if ch0.split(":")[0] == "p" else t2)["tiles"],
                    int(ch0.split(":")[1]))
    ip = int(ch0.split(":")[2])
    cores_nossas = dados["paletas"][str(dados["tiles_vaga"][ch0])]
    for y in range(8):
        for x in range(8):
            a = tuple(pal[ip][crus[y][x]]) if crus[y][x] else None
            b = (tuple(cores_nossas[dados["tiles"][ch0][y][x]])
                 if dados["tiles"][ch0][y][x] else None)
            if a != b:
                ruim += 1
    print("com UM nibble trocado no kit: %d pixels diferentes (tem que ser > 0)"
          % ruim)
    return 0 if dif == 0 and ruim > 0 else 1


def mostra_orcamento():
    livres, mortas, vivos, arm4 = orcamento()
    ts = _tileset(SECUNDARIO)
    print("%s: %d metatiles no arquivo, %d vivos nos 3 layouts irmaos"
          % (SECUNDARIO, len(ts["metatiles"]) // 16,
             len([x for x in vivos if x >= 512])))
    print("armadilha 4 do compacta_paletas (metatile PRIMARIO vivo pintando com "
          "vaga >= 6): %d entradas" % arm4)
    print("vagas de TILE mortas: %d de %d" % (len(mortas), TETO_TILES))
    for v in range(6, 13):
        print("  vaga de cor %2d: %2d indices livres %s"
              % (v, len(livres[v]), livres[v]))
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
    if "--orcamento" in sys.argv:
        return mostra_orcamento()
    if "--extrai" in sys.argv:
        return extrai()
    if "--prova-tiles" in sys.argv:
        return prova_tiles()
    if "--desfazer" in sys.argv:
        return desfaz(alvos_do_argv())
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo(alvos_do_argv())
    if "--so-tileset" in sys.argv:
        t, m, at, c = desenha_kit()
        grava_tileset(t, m, at)
        print("tileset escrito: %d tiles, %d metatiles" % (len(t), len(m)))
        return 0
    return roda(alvos_do_argv(), "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
