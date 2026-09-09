#!/usr/bin/env python3
"""Refino de `MauvilleCity` (tema CIDADE ELÉTRICA E MODERNA) e de
`VerdanturfTown` (tema CAMPO FLORIDO), as DUAS cidades do `gTileset_Mauville`.

Um único secundário serve às duas, então elas são um LOTE SÓ e um kit só. Este
arquivo é o motor e a configuração de `MauvilleCity`; `campo_verdanturf.py` é a
configuração da vila e importa daqui o motor inteiro, do mesmo jeito que
`estrada_oldale.py` importa `mato_littleroot.py`. O KIT ENTRA INTEIRO NESTE
COMMIT, com as peças das duas cidades, para que o `metatiles.bin` saia igual nas
duas passadas e a segunda não precise mexer no tileset.

O QUE AS DUAS CIDADES TÊM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026:

    cidade            carimbo  células  de   andáveis    liso   liso3
    MauvilleCity            1      217   de       469   46,3%   65,0%
    VerdanturfTown        516       98   de       231   42,4%   79,7%

Em `MauvilleCity` o carimbo é o metatile 1, a grama lisa do `gTileset_General`,
e ela cobre todo o miolo entre os prédios. Só que a régua conta UM metatile e a
cidade tem DOIS tapetes: as 176 células de CALÇADA estão partidas em cinco
metatiles do primário (273, 257, 94, 264 e 266) que são variantes um do outro por
espelho, e a distância pixel a pixel entre eles vai de 3,6 a 14,7, ou seja quatro
dos dez pares ficam ABAIXO do piso de 8,0 que o `varia_carimbo.py` documenta como
invisível em jogo. Aos olhos de quem joga a rua é um tapete só de 176 células.
Derrubar só a grama deixaria a régua boa e a cidade igual, e por isso as DUAS
famílias entram.

Em `VerdanturfTown` o carimbo é o metatile 516, a relva curta do próprio
`gTileset_Mauville`, com 98 células, e o metatile 1 vem logo atrás com 60. Os
dois juntos comem 68,4% do chão, e o `liso3` de 79,7% é o mais alto das duas
cidades: a vila do ar puro é um lençol verde com quatro prédios em cima.

OS ATRIBUTOS NÃO SÃO ESCOLHA DESTA PASSADA, e são três, não um:

    família    carimbo(s)                    atributo  comportamento
    grama      1                               0x0000  MB_NORMAL
    calçada    94, 257, 264, 266, 273          0x0000  MB_NORMAL
    relva      516, 517                        0x0007  MB_SHORT_GRASS

O `portao_planta.py` cobra `(comportamento, layerType)` idêntico em toda célula
que continua andável, então TODA variante de grama e de calçada sai com 0x0000
bit a bit e TODA variante de relva sai com 0x0007 bit a bit. A relva não é
detalhe de decoração: `MB_SHORT_GRASS` é o que faz a pegada aparecer atrás do
jogador em Verdanturf, e trocar por `MB_NORMAL` não quebraria build nenhum e
apareceria só dentro do jogo.

AS VAGAS DE TILE 96 A 159 SÃO INTOCÁVEIS, e são SESSENTA E QUATRO, a maior lista
de pinos da onda. `src/tileset_anims.c` (`QueueAnimTiles_Mauville_Flowers`,
`InitTilesetAnim_Mauville`) escreve nelas em tempo de execução, com 32 destinos,
e não sabe de renumeração. Conferido com `dev_scripts/pinos_anim.py
gTileset_Mauville` ANTES de gastar qualquer vaga. Esta passada NÃO ESCREVE UM
ÚNICO TILE, então as 64 vagas ficam byte a byte onde estavam, e isso é conferido
de novo no fim: o `tiles.png` não é aberto nem para escrita.

ACHADO DE LADO, e ele decide o desenho inteiro: as vagas pinadas 96 a 159 são
justamente as FLORES. Os metatiles 520 a 535 do `gTileset_Mauville` são
[608..671] em duas paletas, ou seja os locais 96 a 159, e são eles que a
animação anima. Ver a seção "AS FLORES ANIMADAS" abaixo.

O ORÇAMENTO DESTE TILESET É O MAIS APERTADO DA ONDA, e foi remedido aqui:

    tiles      512 de 512, 472 vivos, 40 mortos, 64 deles pinados pela animação
    metatiles  510 de 512 definidos, e só 400 usados por algum dos sete layouts
    paletas    a vaga 12 é a única livre

O segundo número é o que paga a rodada, e ele não estava na tabela do briefing:
dos 510 metatiles DEFINIDOS, 110 não aparecem em `map.bin` de layout nenhum, e
mais duas vagas sobram no fim do arquivo. São 112 VAGAS DE METATILE seguras.
Conferido que as 24 constantes `METATILE_Mauville_*` de
`include/constants/metatile_labels.h` (porta, porta da Verdanturf, porta da
ciclovia, tenda de batalha, areia funda e os dezesseis blocos da Mirage Tower)
caem TODAS dentro das 400 usadas, ou seja nenhuma delas está no pool: o conjunto
dos rotulados é subconjunto do conjunto dos usados, e a conta fecha em 400 dos
dois lados.

Por causa disso esta passada gasta ZERO TILE e ZERO COR. Toda a arte nova é
ARRANJO e ESPELHO de tile que já existe, mais mobília montada com a camada de
CIMA de metatile que já existe. O tileset mais apertado da onda não precisou de
compactação nenhuma, e `compacta_tileset.py` NÃO FOI RODADO.

OS SETE LAYOUTS IRMÃOS, lidos do `data/layouts/layouts.json`, e a conferência de
`blockdata_filepath` repetido deu ZERO (nenhum layout empresta o `map.bin` de
outro aqui, ao contrário do caso de Petalburg com os quatro esboços de Kalos):

    LAYOUT_MAUVILLE_CITY               data/layouts/MauvilleCity/map.bin
    LAYOUT_VERDANTURF_TOWN             data/layouts/VerdanturfTown/map.bin
    LAYOUT_ROUTE110                    data/layouts/Route110/map.bin
    LAYOUT_ROUTE111                    data/layouts/Route111/map.bin
    LAYOUT_ROUTE117                    data/layouts/Route117/map.bin
    LAYOUT_ROUTE118                    data/layouts/Route118/map.bin
    LAYOUT_ROUTE111_NO_MIRAGE_TOWER    data/layouts/Route111_NoMirageTower/map.bin

A FONTE DE ARTE, e a REPROVAÇÃO por número. O índice do condutor
(`/tmp/claude-501/FONTES-POR-TILESET.md`) traz UM candidato para
`secondary/mauville`: o `light-platinum` no offset `0x286D6C`, fração de arte
nova 0,970, mapa de amostra g00m05 80x40. Ele NÃO ENTROU, e a razão é de medida e
não de gosto: o que a calçada de Mauville precisa não é de outra calçada, é de
VARIAÇÃO. Os cinco metatiles de calçada que a cidade usa hoje são feitos de OITO
tiles do nosso `gTileset_General` (245, 246, 261, 262, 277, 278, 293 e 294, na
vaga de paleta 1), e três desses oito têm textura de verdade: o 245 fica a 42,7
do 262 chapado, o 293 a 30,9 e o 246 a 24,6. Espelhar e rearranjar esses três
rende doze variantes entre 8,1 e 30,7 de distância pixel a pixel dos cinco
carimbos, todas com 1,3 a 23,2 de distância de cor, ou seja dentro do teto de
42,0 que Dewford fixou, e todas a custo ZERO de tile e de cor. Importar um
calçamento de fora custaria tile numa árvore com 40 vagas mortas e cor numa
árvore com UMA vaga de paleta livre, e ainda pediria borda de transição contra os
cinco carimbos, que é a lição de retalho que esta onda já pagou. REPROVADO por
orçamento e por medida, e o `CREDITS.md` NÃO É TOCADO por consequência direta.

DE ONDE VEM A ARTE, ENTÃO. De três lugares, todos NOSSOS:

  1. ARRANJO E ESPELHO do que o carimbo já usa. Os nove arranjos da grama
     (tiles 2 e 3 na vaga 2) ficam entre 12,0 e 17,3 do metatile 1 e com ZERO de
     distância de cor, que é a mesma medida que `mato_littleroot.py` registrou
     nas três cidades do `gTileset_Petalburg`. Os onze arranjos da relva (tiles
     locais 77 e 93 na vaga 2) ficam entre 23,3 e 41,3 do 516, o dobro, porque a
     relva curta tem pinta muito mais forte que a grama. Custo: ZERO tile, ZERO
     cor, uma vaga de metatile cada.
  2. METATILE QUE JÁ EXISTE E NINGUÉM USA. Quatro dos 110 metatiles órfãos do
     `gTileset_Mauville` são variante de grama pronta e passam no piso de 8,0:
     o 888 (15,4), o 890 (15,4), o 899 (33,3) e o 901 (24,1). Eles entram no
     catálogo SEM GASTAR VAGA NENHUMA, porque já estão compilados na ROM. Os
     910, 911 e 932 ficaram de fora, e o número é o motivo: os três são
     `[3,3,2,2]` e ficam a 7,7 do carimbo, abaixo do piso, além de serem cópias
     pixel a pixel um do outro.
  3. A CAMADA DE CIMA de metatile que já existe, pousada na camada de baixo do
     nosso carimbo, com comportamento ZERADO e `layerType` COVERED. É a mobília.

A MOBÍLIA, e por que ela é de BEIRA. Peça solta no meio da praça lê como erro de
mapa, então todo móvel encosta em alguma coisa pelo anel de OITO (prédio, árvore,
outra família de chão ou a borda do mapa). O tema elétrico sai daqui: poste de
luz, poste duplo, luminária, poste de braço, poste da rede, grade em três peças,
painel de avisos, canteiro de flor e máquina de bebida, cada um posto tanto na
grama quanto na CALÇADA, que é o que dá a leitura de rua de cidade e não de
gramado. Em Verdanturf a mesma máquina vira cerca de madeira, bancada de feira,
moita escura, placa e canteiro, que é o tema de feira de vila.

MÓVEL DIRETO E MÓVEL REMONTADO, e a diferença custa vaga. O metatile 4 (canteiro
de flor), o 27 (painel), o 307 (poste duplo), o 328, o 329 e o 330 (grade) e o
305 (máquina) do `gTileset_General` JÁ têm a camada de baixo `[2,3,3,2]` na vaga
2, que é EXATAMENTE a camada de baixo do metatile 1, e JÁ têm atributo 0x1000
(COVERED, comportamento zerado). Eles entram DIRETO na grama, a custo zero de
metatile. Na calçada e na relva os mesmos desenhos são REMONTADOS, porque lá a
camada de baixo tem que ser a da família, senão a peça deixa um quadrado de grama
em volta, que é a costura que a frente de Veilstone pagou para aprender.

AS FLORES ANIMADAS, e este é o achado que faz o tema de Verdanturf. Os metatiles
520 a 535 são as flores brancas e amarelas que a animação do tileset move, e o
atributo deles é 0x0000. O carimbo de Verdanturf é 0x0007. Pôr o 520 numa célula
de relva mudaria `(comportamento, layerType)` de célula ANDÁVEL e o portão 4
reprovaria na hora. A saída não é desistir: entram SEIS metatiles NOVOS que
apontam para os MESMOS tiles pinados (608 a 671, ou seja os locais 96 a 159) com
o atributo 0x0007 da relva. Referenciar tile pinado é seguro; o que é proibido é
ESCREVER nele, e esta passada não escreve tile nenhum. O resultado é canteiro de
flor que ANIMA dentro do jogo, a custo de uma vaga de metatile cada e zero tile.
Medido: as flores ficam a 96,8 e 103,5 de distância pixel a pixel do 516 e a
46,1 e 46,2 de cor, acima do teto de 42,0 do chão comum, e por isso elas são um
grupo À PARTE, com teto próprio de 50,0 e bolha pequena (2 a 5 células): são
acento de canteiro, não textura de chão. A borda da célula do 520 fica a 18,1 de
RGB da borda do 516, ou seja o fundo de relva das duas casa, e é por isso que o
acento não vira retalho.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHÃO é metatile com a camada de baixo CHEIA e atributo IGUAL, bit a bit, ao
    do carimbo da família. A camada de cima copia a de baixo quando o carimbo
    faz isso, e fica vazia quando o carimbo deixa vazia: o formato do metatile
    novo é o do velho, e não depende de o tile 0 continuar em branco.
  - MÓVEL é célula que vira SÓLIDA: arte na camada de CIMA, camada de baixo com
    o NOSSO chão entrada por entrada, atributo 0x1000 (comportamento ZERADO,
    `layerType` COVERED, as duas camadas ABAIXO do sprite).
  - MÓVEL SÓ POUSA NO CARIMBO BASE DA FAMÍLIA, e nunca numa variante já pintada.
    Móvel posto no carimbo tira uma célula do numerador E do denominador da
    régua; móvel posto em cima de mancha tira só do denominador, o que PIORA a
    conta. Por isso os móveis vêm ANTES da mancha.
  - A MANCHA É BOLHA, não sal e pimenta, e o auto-teste prova isso comparando o
    tamanho médio do pedaço conexo com o de uma sabotagem que espalha as MESMAS
    células ao acaso.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado.

O `map.json` das duas cidades fica INTOCADO: nenhum objeto novo, nenhuma placa
nova, nenhum warp mexido.

Uso:
    python3 dev_scripts/eletrica_mauville.py              # mede e mostra o plano
    python3 dev_scripts/eletrica_mauville.py --aplicar    # escreve tileset e mapa
    python3 dev_scripts/eletrica_mauville.py --desfazer   # devolve o map.bin
    python3 dev_scripts/eletrica_mauville.py --demo       # auto-teste
    python3 dev_scripts/eletrica_mauville.py --so-tileset # só o kit, sem mapa
"""
import collections
import glob
import json
import os
import re as _re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

DESTINO = f"{RAIZ}/data/tilesets/secondary/mauville"
PLANO = f"{RAIZ}/dev_scripts/praca_mauville.json"

PRIMARIO = "gTileset_General"
SECUNDARIO = "gTileset_Mauville"

# Os SETE layouts que dividem o `gTileset_Mauville`, lidos do `layouts.json`.
# Nenhum `blockdata_filepath` se repete: são sete `map.bin` distintos.
# Lidos do `layouts.json` por `layouts_irmaos()`; a lista abaixo é só a
# documentação do que foi medido em 09/09/2026. `Route111_NoMirageTower` é
# layout SEM pasta em `data/maps/`: ele tem `map.bin` e não tem `map.json`.
IRMAOS = ["MauvilleCity", "VerdanturfTown", "Route110", "Route111",
          "Route117", "Route118", "Route111_NoMirageTower"]

TETO_TILES = 512            # NUM_TILES_IN_PRIMARY, include/fieldmap.h
TETO_META = 512             # NUM_METATILES_IN_PRIMARY, include/fieldmap.h
# As 64 vagas que `QueueAnimTiles_Mauville_Flowers` sobrescreve em tempo de
# execução. Esta passada não escreve tile nenhum, mas o portão fica de pé.
PINOS_ANIM = set(range(96, 160))
MARGEM = 1                  # células de folga em relação à borda do mapa
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%
TETO_COR = 42.0             # distância de cor média aceita entre chão novo e carimbo
# O TETO POR QUADRANTE, e ele é a regra que salvou as duas cidades do retalho.
# A média do metatile inteiro não enxerga o defeito que o olho vê primeiro: um
# quadrante de 8x8 muito mais claro (ou muito mais verde) que os outros três
# vira QUADRADO na tela, e a média de quatro quadrantes dilui isso até passar. O
# corte de 18,0 é MEDIDO e não escolhido a dedo, e ele corta exatamente duas
# famílias de defeito que a primeira versão desta passada pôs no mapa e o render
# mostrou:
#   - na CALÇADA, os tiles 245 (34,4) e 293 (23,3) são peças de CANTO do
#     autotile e trazem dez pixels da grama vizinha cada um. Usados como miolo
#     de rua eles espalham lasca verde no meio do asfalto. Ficam de fora; o 246
#     (17,0), o 261 (7,3), o 277 (2,2) e o 294 (2,2) passam, e os dois pixels de
#     verde que os três últimos têm somem no tamanho de tela.
#   - na GRAMA, os tiles 386 (61,5), 402 (59,7), 677 (26,2) e 693 (30,7) são de
#     relva CLARA, e é deles que vinham as quatro variantes prontas 888, 890,
#     899 e 901 do próprio tileset. Elas passavam na média do metatile (15,4 a
#     33,3) e desenhavam cunha pálida de 8x8 no meio do gramado.
TETO_COR_QUADRANTE = 18.0
TETO_COR_FLOR = 50.0        # o teto do grupo de ACENTO, ver o cabeçalho
PISO_VARIANTE = 8.0         # distância pixel a pixel mínima entre duas variantes
PISO_PADRAO = 0.12          # o mesmo corte de Dewford, e pela mesma razão de tamanho
ESPACO_ENTRE_MOVEIS = 2     # Chebyshev mínimo entre dois móveis QUAISQUER
PISO_BOLHA = 3
MULTI_NIVEL = 15            # ELEVATION_MULTI_LEVEL: casa com QUALQUER elevação

N4 = E.N4

# ---------------------------------------------------------------- as FAMÍLIAS
# `carimbos` são TODOS os metatiles que a família cobre (a calçada de Mauville
# está partida em cinco); `base` é o que manda na camada de baixo dos móveis e é
# o único em que móvel pousa; `attr` é o atributo que toda peça da família tem
# que repetir bit a bit; `elev` são as elevações aceitas, medidas no mapa.
FAMILIAS = {
    "grama":   dict(carimbos=[1], base=1, attr=0x0000, elev={3}),
    "calcada": dict(carimbos=[94, 257, 264, 266, 273], base=273,
                    attr=0x0000, elev={3}),
    "relva":   dict(carimbos=[516, 517], base=516, attr=0x0007, elev={3}),
}

# Os arranjos de um par de tiles [a,b,b,a]. Cada entrada é (qual, espelho), com
# `qual` em {0,1} e espelho em 0..3 (bit 1 = horizontal, bit 2 = vertical).
ARRANJOS = {
    "carimbo":   [(0, 0), (1, 0), (1, 0), (0, 0)],
    "espelhoH":  [(0, 1), (1, 1), (1, 1), (0, 1)],
    "espelhoV":  [(0, 2), (1, 2), (1, 2), (0, 2)],
    "espelhoHV": [(0, 3), (1, 3), (1, 3), (0, 3)],
    "giro":      [(1, 1), (0, 1), (0, 1), (1, 1)],
    "troca":     [(1, 0), (0, 0), (0, 0), (1, 0)],
    "misto1":    [(0, 0), (1, 1), (1, 2), (0, 3)],
    "misto2":    [(1, 3), (0, 2), (0, 1), (1, 0)],
    "misto3":    [(0, 1), (1, 0), (1, 3), (0, 2)],
    "misto4":    [(1, 2), (0, 3), (0, 0), (1, 1)],
    "faixaX":    [(0, 0), (1, 0), (0, 2), (1, 2)],
}

# O CHÃO NOVO, por família. `par` são os dois tiles, `pal` a vaga de paleta e
# `arr` o arranjo. Todos os números do comentário foram medidos nesta árvore.
CHAO = {
    # 12,0 a 17,3 de distância do metatile 1, e ZERO de cor: os dois tiles têm
    # a mesma paleta e o mesmo conteúdo, só mudam de lugar.
    "grama": [
        ("grama espelhada",      (2, 3), 2, "espelhoH"),
        ("grama virada",         (2, 3), 2, "espelhoV"),
        ("grama de cabeça",      (2, 3), 2, "espelhoHV"),
        ("grama girada",         (2, 3), 2, "giro"),
        ("grama trocada",        (2, 3), 2, "troca"),
        ("grama mista",          (2, 3), 2, "misto1"),
        ("grama mista dois",     (2, 3), 2, "misto2"),
        ("grama mista três",     (2, 3), 2, "misto3"),
        ("grama mista quatro",   (2, 3), 2, "misto4"),
    ],
    # DUAS PODAS, as duas medidas. (a) O 262 e o 278 sozinhos são calçada
    # CHAPADA: os onze arranjos do par deles ficam entre 1,6 e 7,2, todos abaixo
    # do piso de 8,0, e por isso o par do próprio carimbo NÃO ENTRA sozinho.
    # (b) O 245 e o 293 são peça de CANTO do autotile e trazem dez pixels de
    # grama cada um: reprovados pelo teto de quadrante (34,4 e 23,3 contra 18,0).
    # Sobram cinco tiles de miolo, e os doze arranjos abaixo saem deles, entre
    # 8,0 e 21,8 de distância pixel a pixel dos cinco carimbos.
    "calcada": [
        ("junta de calçada",     (246, 261), 1, "carimbo"),
        ("junta espelhada",      (246, 261), 1, "espelhoH"),
        ("junta girada",         (246, 261), 1, "giro"),
        ("junta mista",          (246, 261), 1, "misto1"),
        ("junta trocada",        (246, 261), 1, "troca"),
        ("junta fina",           (261, 262), 1, "carimbo"),
        ("junta fina espelhada", (261, 262), 1, "espelhoH"),
        ("junta fina girada",    (261, 262), 1, "giro"),
        ("calçada gasta",        (261, 277), 1, "espelhoV"),
        ("calçada gasta espelhada", (261, 277), 1, "espelhoHV"),
        ("calçada lisa",         (277, 278), 1, "misto1"),
        ("calçada clara",        (278, 294), 1, "misto2"),
    ],
    # 23,3 a 41,3 do 516: a relva curta tem pinta muito mais forte que a grama,
    # e o mesmo espelho que na grama rende 12 aqui rende 41.
    "relva": [
        ("relva espelhada",      (589, 605), 2, "espelhoH"),
        ("relva virada",         (589, 605), 2, "espelhoV"),
        ("relva de cabeça",      (589, 605), 2, "espelhoHV"),
        ("relva girada",         (589, 605), 2, "giro"),
        ("relva trocada",        (589, 605), 2, "troca"),
        ("relva mista",          (589, 605), 2, "misto1"),
        ("relva mista dois",     (589, 605), 2, "misto3"),
        ("relva em faixa",       (589, 605), 2, "faixaX"),
    ],
}

# CHÃO QUE JÁ EXISTE E NINGUÉM USA: entra no catálogo sem gastar vaga nenhuma.
# O portão exige que o atributo dele já seja o da família, e ele é.
# REPROVADAS, e o número é o motivo. A primeira versão desta passada trazia
# quatro variantes prontas do próprio `gTileset_Mauville` (o 888, o 890, o 899 e
# o 901), todas órfãs e todas de graça, e o render mostrou o defeito na hora:
# elas são feitas com os tiles de relva CLARA (386, 402, 677 e 693), que ficam a
# 26,2, 30,7, 59,7 e 61,5 de cor do quadrante do carimbo, e no gramado escuro de
# `MauvilleCity` viravam cunha pálida de 8x8. A média do metatile inteiro
# escondia isso (15,4 a 33,3, tudo dentro do teto de 42,0); o teto POR
# QUADRANTE, que nasceu deste render, corta as quatro. Ficaram de fora também o
# 910, o 911 e o 932, que são `[3,3,2,2]` a 7,7 do carimbo e cópia pixel a pixel
# um do outro.
CHAO_DIRETO = {"grama": [], "calcada": [], "relva": []}

# AS FLORES ANIMADAS. Metatile NOVO que aponta para os MESMOS tiles pinados dos
# metatiles 520 a 535, com o atributo 0x0007 da relva no lugar do 0x0000 deles.
# `de` é o metatile de onde a camada de baixo é copiada inteira.
FLORES = [
    ("flor branca",          520),
    ("flor branca dois",     522),
    ("flor branca três",     525),
    ("flor amarela",         528),
    ("flor amarela dois",    531),
    ("flor amarela três",    534),
]

# ------------------------------------------------------------------ os MÓVEIS
# `de` é o metatile de onde a camada de CIMA vem. `direto` significa que o
# metatile já tem a camada de baixo da família E atributo 0x1000, e por isso
# entra sem gastar vaga; o portão confere as duas coisas e não acredita na
# etiqueta.
MOVEIS = [
    dict(nome="poste de luz",       de=306),
    dict(nome="poste duplo",        de=307),
    dict(nome="luminária",          de=312),
    dict(nome="poste fino",         de=313),
    dict(nome="poste de braço",     de=314),
    dict(nome="poste da rede",      de=308),
    dict(nome="grade ponta",        de=328),
    dict(nome="grade",              de=329),
    dict(nome="grade ponta direita", de=330),
    dict(nome="painel de avisos",   de=27),
    dict(nome="canteiro de flor",   de=4),
    dict(nome="máquina de bebida",  de=305),
    dict(nome="pilar de energia",   de=792),
    dict(nome="cerca de madeira",   de=922),
    dict(nome="cerca de madeira dois", de=923),
    dict(nome="bancada de feira",   de=930),
    dict(nome="bancada de feira dois", de=931),
    dict(nome="moita escura",       de=902),
    dict(nome="placa de madeira",   de=519),
]
POR_NOME = {m["nome"]: m for m in MOVEIS}

# ------------------------------------------------------------------ as CIDADES
CIDADE_MAUVILLE = dict(
    bloco="216_eletrica_mauville.json",
    familias=["grama", "calcada"],
    # Quem entra em cada família, e quantas cópias. Peça repetida demais lê como
    # carimbo novo; peça de uma cópia só some no mapa de 40x20. Os números
    # abaixo foram fechados olhando o render.
    moveis={
        "grama": [("poste de luz", 2, 6), ("poste duplo", 2, 6),
                  ("luminária", 2, 7), ("poste de braço", 1, 7),
                  ("grade ponta", 1, 6), ("grade", 2, 5),
                  ("grade ponta direita", 1, 6), ("painel de avisos", 1, 8),
                  ("canteiro de flor", 3, 4), ("máquina de bebida", 1, 8),
                  ("moita escura", 2, 5)],
        "calcada": [("poste de luz", 2, 6), ("luminária", 1, 7),
                    ("poste fino", 1, 7), ("poste da rede", 1, 7),
                    ("pilar de energia", 1, 7), ("grade", 1, 6),
                    ("painel de avisos", 1, 8), ("máquina de bebida", 1, 8)],
    },
    bolhas={
        "grama": [
            [dict(grupo=["grama espelhada", "grama girada", "grama mista"],
                  tam=(6, 12), quantas=4),
             dict(grupo=["grama virada", "grama trocada", "grama mista dois"],
                  tam=(5, 11), quantas=4),
             dict(grupo=["grama de cabeça", "grama mista três",
                         "grama mista quatro"], tam=(5, 10), quantas=4)],
            [dict(grupo=["grama espelhada", "grama de cabeça",
                         "grama mista quatro"], tam=(3, 7), quantas=6),
             dict(grupo=["grama girada", "grama mista dois", "grama virada"],
                  tam=(3, 7), quantas=6),
             dict(grupo=["grama trocada", "grama mista três", "grama mista"],
                  tam=(2, 6), quantas=6)],
            # A TERCEIRA RODADA é de bolha miúda e existe por conta: as duas
            # primeiras deixavam 66 das 217 células de grama sem tocar e a régua
            # parava em 14,9%. Bolha de 2 a 4 células cabe nos vãos estreitos
            # entre prédio e rua, que é onde o gramado de Mauville é uma tira de
            # duas células de largura.
            [dict(grupo=["grama espelhada", "grama girada", "grama trocada"],
                  tam=(2, 4), quantas=8, piso=2),
             dict(grupo=["grama virada", "grama mista", "grama mista dois"],
                  tam=(2, 4), quantas=8, piso=2),
             dict(grupo=["grama de cabeça", "grama mista três",
                         "grama mista quatro"], tam=(2, 4), quantas=8, piso=2)],
        ],
        "calcada": [
            [dict(grupo=["junta de calçada", "junta espelhada", "junta mista"],
                  tam=(5, 10), quantas=4),
             dict(grupo=["calçada gasta", "calçada gasta espelhada",
                         "calçada clara"], tam=(4, 9), quantas=4),
             dict(grupo=["junta fina", "junta fina espelhada",
                         "junta fina girada"], tam=(4, 9), quantas=4)],
            [dict(grupo=["junta girada", "junta trocada", "calçada lisa"],
                  tam=(2, 6), quantas=7),
             dict(grupo=["junta de calçada", "calçada gasta", "junta fina"],
                  tam=(2, 5), quantas=7)],
            [dict(grupo=["junta espelhada", "junta fina girada",
                         "calçada clara"], tam=(2, 4), quantas=8, piso=2),
             dict(grupo=["junta mista", "calçada gasta espelhada",
                         "junta fina espelhada"], tam=(2, 4), quantas=8,
                  piso=2)],
        ],
    },
    piso_mancha=200,
)

CIDADE_VERDANTURF = dict(
    bloco="217_campo_verdanturf.json",
    familias=["relva", "grama"],
    moveis={
        "relva": [("cerca de madeira", 2, 5), ("cerca de madeira dois", 2, 5),
                  ("bancada de feira", 1, 6), ("bancada de feira dois", 1, 6),
                  ("moita escura", 2, 5), ("placa de madeira", 1, 7),
                  ("canteiro de flor", 2, 5), ("poste fino", 1, 7)],
        "grama": [("moita escura", 2, 5), ("canteiro de flor", 2, 5),
                  ("cerca de madeira", 1, 6), ("placa de madeira", 1, 7)],
    },
    bolhas={
        "relva": [
            [dict(grupo=["relva espelhada", "relva girada", "relva mista"],
                  tam=(5, 10), quantas=4),
             dict(grupo=["relva virada", "relva trocada", "relva mista dois"],
                  tam=(4, 9), quantas=4),
             dict(grupo=["relva de cabeça", "relva em faixa"],
                  tam=(4, 8), quantas=3)],
            [dict(grupo=["flor branca", "flor branca dois", "flor branca três"],
                  tam=(2, 5), quantas=3, piso=1),
             dict(grupo=["flor amarela", "flor amarela dois",
                         "flor amarela três"], tam=(2, 5), quantas=3, piso=1)],
            [dict(grupo=["relva espelhada", "relva mista dois",
                         "relva em faixa"], tam=(2, 5), quantas=5),
             dict(grupo=["relva girada", "relva trocada", "relva de cabeça"],
                  tam=(2, 5), quantas=5)],
        ],
        "grama": [
            [dict(grupo=["grama espelhada", "grama girada", "grama mista"],
                  tam=(4, 8), quantas=3),
             dict(grupo=["grama virada", "grama trocada", "grama mista quatro"],
                  tam=(3, 7), quantas=3),
             dict(grupo=["grama de cabeça", "grama mista dois",
                         "grama mista três"], tam=(3, 7), quantas=3)],
        ],
    },
    piso_mancha=90,
)

CIDADES = {"MauvilleCity": CIDADE_MAUVILLE,
           "VerdanturfTown": CIDADE_VERDANTURF}

# A posição de cada família numa ordem FIXA. Ver o comentário da semente em
# `plano_mapa`: `hash()` de texto é salgado por processo e não serve para
# semente de plano que precisa sair igual em toda máquina.
ORDEM_FAMILIA = {q: i for i, q in enumerate(FAMILIAS)}


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


def _entradas(bin_meta, local):
    return list(struct.unpack_from("<8H", bin_meta, local * 16))


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def ents_nossas(mt_id, tp=None, ts=None):
    """As oito entradas de um metatile NOSSO, pelo id global."""
    tp = tp or _tileset(PRIMARIO)
    ts = ts or _tileset(SECUNDARIO)
    tset, loc = (tp, mt_id) if mt_id < 512 else (ts, mt_id - 512)
    return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))


def attr_nosso(mt_id):
    if mt_id < 512:
        return G._attrs(PRIMARIO)[mt_id]
    return G._attrs(SECUNDARIO)[mt_id - 512]


def arte_em_cima(ents, tp=None, ts=None):
    """A camada de CIMA destas entradas acende ALGUM pixel?

    A pergunta não é "o índice de tile é zero": o tile 1 do primário existe e não
    tem um pixel aceso, e contar por índice diria que um chão chapado desenha por
    cima do jogador.
    """
    import render_maps as RM
    tp = tp or _tileset(PRIMARIO)
    ts = ts or _tileset(SECUNDARIO)
    for v in ents[4:]:
        idx = v & 0x3FF
        if not idx:
            continue
        tile = RM.resolver_tile(tp, ts, idx)
        if tile is None:
            continue
        if any(c for linha in tile for c in linha):
            return True
    return False


def px_metatile(ents, tp, ts):
    """Os 256 pixels RGB de um metatile descrito por oito entradas."""
    import render_maps as RM
    from PIL import Image
    im = Image.new("RGB", (16, 16), (0, 0, 0))
    p = im.load()
    for cam in (0, 1):
        for q in range(4):
            val = ents[cam * 4 + q]
            idx, ip = val & 0x3FF, (val >> 12) & 0xF
            if not idx:
                continue
            tile = RM.resolver_tile(tp, ts, idx)
            if tile is None:
                continue
            cores = (tp if ip < 6 else ts)["paletas"].get(ip)
            if cores is None:
                continue
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                             [tuple(c) for c in cores],
                             bool(val & 0x400), bool(val & 0x800))
    return list(im.get_flattened_data())


def _dist_pixels(a, b):
    return sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
               for p, q in zip(a, b)) / 256.0


def _cor_media(px):
    return tuple(sum(c[k] for c in px) / 256.0 for k in range(3))


def _dist_cor(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def _quadrantes(px):
    """As quatro cores médias, uma por quadrante de 8x8 dos 256 pixels."""
    out = []
    for qy in (0, 8):
        for qx in (0, 8):
            p = [px[(qy + y) * 16 + qx + x] for y in range(8) for x in range(8)]
            out.append(tuple(sum(c[k] for c in p) / 64.0 for k in range(3)))
    return out


def pior_quadrante(ents, refs, tp, ts):
    """A MAIOR distância de cor entre um quadrante desta peça e o quadrante mais
    parecido dos carimbos de referência.

    É esta conta, e não a média do metatile, que enxerga o quadrado de 8x8. Ver
    o comentário de `TETO_COR_QUADRANTE`.
    """
    meus = _quadrantes(px_metatile(ents, tp, ts))
    deles = [q for r in refs for q in _quadrantes(r)]
    return max(min(_dist_cor(m, d) for d in deles) for m in meus)


# ---------------------------------------------------------------------- o KIT
def layouts_irmaos(_c={}):
    """[(id do layout, caminho do map.bin)] de TODO layout que usa este
    secundário, lido do `layouts.json` e não de lista escrita à mão.

    SÃO SETE LAYOUTS E SEIS MAPAS. `Route111_NoMirageTower` é layout sem pasta
    em `data/maps/`, ou seja tem `map.bin` próprio e nenhum `map.json`: quem
    varrer os irmãos por `data/maps/<nome>/map.json` (que é o que
    `arte_ginasios_sinnoh.grade` faz) PERDE esse layout calado e acha vaga de
    metatile livre que não está livre. A varredura aqui é pelo arquivo de
    blocos, direto.

    Conferido: nenhum `blockdata_filepath` se repete nos sete, ou seja não há o
    caso dos quatro esboços de Kalos que emprestam o `map.bin` de Petalburg.
    """
    if _c:
        return list(_c["v"])
    lay = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
    v = [(L["id"], L["blockdata_filepath"]) for L in lay["layouts"]
         if L.get("secondary_tileset") == SECUNDARIO]
    repetidos = [c for c, n in collections.Counter(x[1] for x in v).items()
                 if n > 1]
    if repetidos:
        raise SystemExit("layouts irmãos com blockdata repetido: %s" % repetidos)
    _c["v"] = v
    return list(v)


def blocos(caminho):
    b = open(f"{RAIZ}/{caminho}", "rb").read()
    return list(struct.unpack_from("<%dH" % (len(b) // 2), b, 0))


def locais_livres(_c={}):
    """As vagas de metatile em que esta passada pode gravar, em ordem.

    Uma vaga só serve se NENHUM dos sete layouts irmãos escrever o id dela em
    `map.bin`. Metatile DEFINIDO e não usado é vaga: ele ocupa espaço no
    `metatiles.bin` mas não chega à tela de mapa nenhum, e sobrescrevê-lo não
    move um pixel em lugar nenhum. As 24 constantes `METATILE_Mauville_*` são
    conferidas à parte, e todas caem dentro das usadas.
    """
    if _c:
        return list(_c["v"])
    # A grade das DUAS cidades entra pela BASE desta passada, e não pelo disco.
    # Sem isso a idempotência morre: depois de um `--aplicar` o `map.bin` já tem
    # os ids que este kit acabou de escrever, o portão os declara "usados por um
    # irmão" e a segunda rodada fica sem vaga nenhuma. É o mesmo cuidado que o
    # `praia_dewford.py` toma com `base_de`.
    guardado = carrega_plano()
    usados = set()
    for _id, caminho in layouts_irmaos():
        cidade = None
        for nome in CIDADES:
            if caminho == "data/layouts/%s/map.bin" % nome:
                cidade = nome
        grade = base_de(cidade, guardado) if cidade else blocos(caminho)
        usados |= {c & 0x3FF for c in grade if (c & 0x3FF) >= 512}
    rotulados = set()
    txt = open(f"{RAIZ}/include/constants/metatile_labels.h").read()
    corpo = txt.split("// gTileset_Mauville\n")
    if len(corpo) > 1:
        corpo = corpo[1].split("// gTileset_MauvilleGym")[0]
        for m in _re.finditer(r"#define\s+METATILE_Mauville_\w+\s+(0x[0-9A-Fa-f]+)",
                              corpo):
            rotulados.add(int(m.group(1), 16))
    # AS FONTES DA ARTE TAMBÉM SÃO RESERVA, e este portão nasceu de um bug de
    # verdade nesta rodada. Oito das dezenove peças de mobília e as seis flores
    # vêm de metatile do PRÓPRIO `gTileset_Mauville` (o 519, o 792, o 902, o
    # 903, o 922, o 923, o 930, o 931 e os 520 a 535), e esses metatiles são
    # ÓRFÃOS: nenhum dos sete mapas os usa, que é justamente por que eles
    # estavam na lista de vagas livres. Sem esta reserva o kit gravava por cima
    # da própria fonte, e a segunda rodada montava a placa de madeira lendo o
    # metatile que a primeira tinha acabado de trocar por uma variante de grama.
    # Dentro de UMA rodada nada aparecia, porque `desenha_kit` lê tudo antes de
    # `grava_tileset` escrever qualquer coisa: o defeito só aparecia na rodada
    # seguinte, e foi a contagem de metatiles caindo de 55 para 54 que o
    # denunciou.
    fontes = {m["de"] for m in MOVEIS} | {de for _n, de in FLORES}
    for _q, lista in CHAO_DIRETO.items():
        fontes |= {mt for _n, mt in lista}
    reserva = {g - 512 for g in usados | rotulados | {f for f in fontes
                                                      if f >= 512}}
    n = len(_ler("metatiles.bin")) // 16
    v = [i for i in range(max(n, 0)) if i not in reserva]
    v += [i for i in range(n, TETO_META)]
    _c["v"] = v
    _c["rotulados"] = sorted(rotulados)
    _c["usados"] = sorted(usados)
    return list(v)


def base_da_familia(qual, tp=None, ts=None):
    """(as quatro entradas da camada de BAIXO do carimbo base, o atributo)."""
    mt = FAMILIAS[qual]["base"]
    ents = ents_nossas(mt, tp, ts)
    return ents[:4], attr_nosso(mt)


def desenha_kit():
    """(metas, attrs, catalogo) sem escrever em disco.

    `metas` é {local: [8 entradas]} e `attrs` {local: atributo}, só com locais
    NOVOS. `catalogo` descreve as peças por família e por nome.
    """
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    metas, attrs = {}, {}
    vagas = locais_livres()
    prox = [0]
    catalogo = dict(chao={}, moveis={}, sobre={})

    def poe(ents, attr):
        if prox[0] >= len(vagas):
            raise SystemExit("acabaram as vagas de metatile livres")
        local = vagas[prox[0]]
        metas[local] = list(ents)
        attrs[local] = attr
        prox[0] += 1
        return 512 + local

    for qual, fam in FAMILIAS.items():
        catalogo["chao"][qual] = {}
        catalogo["moveis"][qual] = {}
    px_carimbo = {q: {m: px_metatile(ents_nossas(m, tp, ts), tp, ts)
                      for m in FAMILIAS[q]["carimbos"]} for q in FAMILIAS}

    # ------------------------------------------------------------- 1. o CHÃO
    for qual, lista in CHAO.items():
        fam = FAMILIAS[qual]
        modelo = ents_nossas(fam["base"], tp, ts)
        copia_cima = modelo[4:] == modelo[:4]
        for nome, (a, b), pal, arr in lista:
            par = (a, b)
            quads = [(pal << 12) | (f << 10) | par[k]
                     for (k, f) in ARRANJOS[arr]]
            ents = quads + (list(quads) if copia_cima else [0, 0, 0, 0])
            d = min(_dist_cor(_cor_media(px_metatile(ents, tp, ts)),
                              _cor_media(p)) for p in px_carimbo[qual].values())
            if d > TETO_COR:
                raise SystemExit("o chão %s está a %.1f de cor do carimbo de %s, "
                                 "acima do teto de %.1f" % (nome, d, qual,
                                                            TETO_COR))
            q = pior_quadrante(ents, list(px_carimbo[qual].values()), tp, ts)
            if q > TETO_COR_QUADRANTE:
                raise SystemExit("o chão %s tem um QUADRANTE a %.1f de cor do "
                                 "carimbo de %s, acima do teto de %.1f: isso "
                                 "vira quadrado de 8x8 na tela"
                                 % (nome, q, qual, TETO_COR_QUADRANTE))
            catalogo["chao"][qual][nome] = poe(ents, fam["attr"])
            catalogo["sobre"][nome] = qual

    # CHÃO DIRETO: metatile que já existe. Não gasta vaga; o portão confere que
    # o atributo dele já é o da família.
    for qual, lista in CHAO_DIRETO.items():
        for nome, mt_id in lista:
            if attr_nosso(mt_id) != FAMILIAS[qual]["attr"]:
                raise SystemExit("o chão direto %s (%d) tem atributo 0x%04X e a "
                                 "família %s pede 0x%04X"
                                 % (nome, mt_id, attr_nosso(mt_id), qual,
                                    FAMILIAS[qual]["attr"]))
            q = pior_quadrante(ents_nossas(mt_id, tp, ts),
                               list(px_carimbo[qual].values()), tp, ts)
            if q > TETO_COR_QUADRANTE:
                raise SystemExit("o chão direto %s (%d) tem um QUADRANTE a %.1f "
                                 "de cor do carimbo de %s, acima do teto de %.1f"
                                 % (nome, mt_id, q, qual, TETO_COR_QUADRANTE))
            catalogo["chao"][qual][nome] = mt_id
            catalogo["sobre"][nome] = qual

    # ---------------------------------------------------- 2. as FLORES da relva
    for nome, de in FLORES:
        ents = list(ents_nossas(de, tp, ts))
        if any(v & 0x3FF for v in ents[4:]):
            raise SystemExit("a flor %s vem do metatile %d, que tem arte na "
                             "camada de cima" % (nome, de))
        d = min(_dist_cor(_cor_media(px_metatile(ents, tp, ts)),
                          _cor_media(p)) for p in px_carimbo["relva"].values())
        if d > TETO_COR_FLOR:
            raise SystemExit("a flor %s está a %.1f de cor da relva, acima do "
                             "teto de acento de %.1f" % (nome, d, TETO_COR_FLOR))
        catalogo["chao"]["relva"][nome] = poe(ents, FAMILIAS["relva"]["attr"])
        catalogo["sobre"][nome] = "relva"

    # ------------------------------------------------------------ 3. os MÓVEIS
    # Só entram os pares (família, peça) que ALGUMA das duas cidades pede. Montar
    # as dezenove peças nas três famílias custaria 57 vagas de metatile num
    # tileset que só tem 112; montar o que é usado custa 29, das quais nove são
    # DIRETAS e não gastam vaga nenhuma.
    pedidos = collections.defaultdict(set)
    for _c, cid in CIDADES.items():
        for qual, lista in cid["moveis"].items():
            for nome, _q, _e in lista:
                pedidos[qual].add(nome)
    for qual, fam in FAMILIAS.items():
        base, _a = base_da_familia(qual, tp, ts)
        for m in [x for x in MOVEIS if x["nome"] in pedidos[qual]]:
            e = ents_nossas(m["de"], tp, ts)
            cima = list(e[4:])
            # QUADRANTE DE BAIXO SOBE quando o de cima está vazio, que é a regra
            # do `porto_canalave.py`.
            if not arte_em_cima(e, tp, ts):
                cima = list(e[:4])
            if not any(v & 0x3FF for v in cima):
                raise SystemExit("%s: o metatile %d não tem arte"
                                 % (m["nome"], m["de"]))
            # DIRETO só quando o metatile de origem JÁ tem a camada de baixo
            # desta família E já é COVERED com comportamento zerado.
            if e[:4] == list(base) and attr_nosso(m["de"]) == 0x1000 \
                    and cima == list(e[4:]):
                catalogo["moveis"][qual][m["nome"]] = m["de"]
            else:
                catalogo["moveis"][qual][m["nome"]] = poe(list(base) + cima,
                                                          0x1000)

    if metas and max(metas) >= TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)
    return metas, attrs, catalogo


def grava_tileset(metas, attrs):
    """CRESCE `metatiles.bin` e `metatile_attributes.bin` do secundário.

    O `tiles.png` e os `.pal` NÃO SÃO ABERTOS, nem para leitura: esta passada
    gasta zero tile e zero cor, e as 64 vagas pinadas pela animação das flores
    ficam byte a byte onde estavam por construção.
    """
    if not metas:
        return
    alvo = max(metas) + 1
    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    meta += bytes(max(0, alvo * 16 - len(meta)))
    attr += bytes(max(0, alvo * 2 - len(attr)))
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------ o ESPALHAMENTO
def bolhas(livres, spec, semente=0x5EED):
    """[(nomes, {células})], bolhas orgânicas crescidas por frente de onda.

    A SEMENTE não é sorteio solto: as células livres são ordenadas por um hash da
    posição e a semente só é aceita a pelo menos 2 (Chebyshev) de toda semente já
    aceita. O CRESCIMENTO é guloso com ruído: a cada passo entra a célula da
    frente de onda com o menor hash. Círculo daria bolha redonda e xadrez daria
    sal e pimenta; frente de onda com ruído dá contorno irregular.
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
                # vontade de crescer.
                if len(corpo) < lo and (frente or
                                        len(corpo) < esp.get("piso", PISO_BOLHA)):
                    continue
                achou = (p, corpo)
                break
            if achou is None:
                feitas[k] = esp["quantas"]
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


# ------------------------------------------------------ os CORREDORES da suite
def corredores_multinivel(alvo, v, W, H, d, bloco):
    """Os corredores da suite, refeitos com a regra da ELEVAÇÃO 15.

    O `enfeita_cidades.corredores_de_teste` simula a caminhada da suite com a
    regra "elevação 0 é curinga e o resto exige igualdade". Essa regra é uma
    APROXIMAÇÃO do `MapGridGetElevationAt`: a elevação 15
    (`ELEVATION_MULTI_LEVEL`) também casa com qualquer vizinho. Medido nesta
    árvore: `MauvilleCity` tem elevações 0, 1 e 3 e `VerdanturfTown` tem 0 e 3,
    ou seja hoje as duas contas coincidem nas duas cidades. As DUAS rodam mesmo
    assim, porque a união é barata e não depende de a medida continuar valendo
    depois que outra frente mexer no mapa.
    """
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = "MAP_" + _re.sub(r"(?<!^)(?=[A-Z])", "_",
                                 d.get("name", alvo)).upper().replace("__", "_")
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
                if not compativel((v[y * W + x] >> 12) & 0xF,
                                  (v[j] >> 12) & 0xF):
                    break
                x, y = nx, ny
                pisadas.add((x, y))

    for arq in sorted(glob.glob(f"{pasta}/*.json")):
        if os.path.basename(arq) == bloco:
            continue   # o bloco desta rodada é derivado DO desenho
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


# ----------------------------------------------------------- ligação a pé
def componentes(v, W, H):
    """{célula: rótulo} dos pedaços de chão andável ligados a pé.

    POR QUE NÃO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda é
    alcançável a partir de algum ponto de partida", e fechar um corredor com warp
    dos dois lados não tira NENHUMA célula do alcance e mesmo assim parte a
    cidade em duas.
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


# ---------------------------------------------------------------- o PLANO
def plano_mapa(alvo, cid, catalogo, base=None):
    """(L, W, H, v, escritas, contas) para uma das duas cidades."""
    d, L, W, H, v0 = G.grade(alvo)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    # As famílias desta cidade. Uma célula só é elegível se ainda for um dos
    # carimbos da família, se estiver numa das elevações que a família aceita e
    # se não for ÁGUA para o motor.
    fam, base_fam = {}, {}
    for qual in cid["familias"]:
        f = FAMILIAS[qual]
        alvos = set(f["carimbos"])
        fam[qual] = {(i % W, i // W) for i in range(W * H)
                     if not ((v[i] >> 10) & 3) and (v[i] & 0x3FF) in alvos
                     and ((v[i] >> 12) & 0xF) in f["elev"]
                     and beh(v[i] & 0x3FF) not in AG}
        base_fam[qual] = {p for p in fam[qual]
                          if (v[p[1] * W + p[0]] & 0x3FF) == f["base"]}

    escritas = {}
    # DOIS GELOS. `gelo_solido` (evento + anel + corredor da suite) manda no
    # MÓVEL, porque peça nova encostada numa porta ou num NPC tranca gente.
    # `gelo` (só o corredor da suite e o que ESTA passada já escreveu) manda na
    # MANCHA: repintar o CHÃO não tranca nada, porque a colisão, a elevação e o
    # par (comportamento, layerType) continuam idênticos por construção.
    _ev, halo = E.congelado(d)
    E.BLOCO_PROPRIO = cid["bloco"]
    gelo = E.corredores_de_teste(alvo, v, W, H, d)
    gelo |= corredores_multinivel(alvo, v, W, H, d, cid["bloco"])
    for idx, _a, _n in E.carrega_plano().get(alvo, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))
    gelo_solido = gelo | halo

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

    def livre(qual, x, y):
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo_solido or i in escritas or (x, y) not in base_fam[qual]:
            return False
        return (aplicado[i] & 0x3FF) == FAMILIAS[qual]["base"]

    def espacado(nome, esp, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < esp
                       for px, py in por_movel[nome])

    def encostado(x, y, qual):
        """MÓVEL É DE BEIRA: encosta num sólido, na água, numa célula de outra
        família ou na borda do mapa. O anel é o de OITO e não o de quatro: a peça
        encostada na diagonal de um prédio continua encostada aos olhos de quem
        joga, e o de quatro derruba o número de lugares candidatos pela metade.
        """
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx and not dy:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    return True
                j = ny * W + nx
                if (aplicado[j] >> 10) & 3:
                    return True
                if beh(aplicado[j] & 0x3FF) in AG:
                    return True
                for outra in cid["familias"]:
                    if outra != qual and (nx, ny) in fam[outra]:
                        return True
        return False

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portões deixarem. O portão
        roda NA HORA e não só no fim."""
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
                       key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF,
                                      p))

    # ------ 1. MÓVEIS. Eles vêm ANTES da mancha de propósito: móvel posto no
    # carimbo tira uma célula do numerador E do denominador da régua; móvel posto
    # em cima de uma mancha tira só do denominador, o que PIORA a conta.
    lista = [(qual, nome, quantos, esp)
             for qual in cid["familias"]
             for (nome, quantos, esp) in cid["moveis"].get(qual, [])]
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % max(1, len(lista))
        for k in range(len(lista)):
            qual, nome, quantos, esp = lista[(giro + k) % len(lista)]
            chave = (qual, nome)
            if conta_mov[chave] >= quantos:
                continue
            if not livre(qual, x, y) or not espacado(chave, esp, x, y):
                continue
            if not encostado(x, y, qual):
                continue
            if not tenta_solidificar(x, y, catalogo["moveis"][qual][nome]):
                continue
            por_movel[chave].append((x, y))
            conta_mov[chave] += 1
            break

    # ------------------------------------------------------------- 2. MANCHA
    conta_mancha = collections.Counter()

    def pintavel(p, qual):
        i = p[1] * W + p[0]
        return (p in fam[qual] and i not in escritas and p not in gelo
                and (aplicado[i] & 0x3FF) in set(FAMILIAS[qual]["carimbos"]))

    def pinta(p, nomes, qual):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | catalogo["chao"][qual][nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    for qual in cid["familias"]:
        for rodada, spec in enumerate(cid["bolhas"].get(qual, [])):
            livres = {p for p in fam[qual] if pintavel(p, qual)}
            # A SEMENTE NÃO PODE USAR `hash()` DE TEXTO. O `hash` de `str` do
            # CPython é salgado por processo (`PYTHONHASHSEED`), e a primeira
            # versão desta linha usava `hash(qual)`: o mesmo comando dava 300,
            # 306 e 323 células escritas em três rodadas seguidas, e o
            # auto-teste de idempotência não pegava porque as duas passadas da
            # MESMA rodada usam a mesma salga. A semente aqui é a POSIÇÃO da
            # família na lista fixa, que é a mesma em qualquer máquina.
            semente = _mistura(0x5EED, ORDEM_FAMILIA[qual], rodada)
            for nomes, corpo in bolhas(livres, spec, semente):
                for p in sorted(corpo):
                    pinta(p, nomes, qual)

    # -------------------------------------------------------------- PORTÕES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d células ficariam inalcançáveis, ex.: %s"
                         % (alvo, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcançável"
                             % (alvo, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (alvo, "; ".join(queixas)))
    contas = dict(moveis={"%s/%s" % k: n for k, n in conta_mov.items()},
                  manchas=dict(conta_mancha), solidos=len(novos_solidos),
                  familias={q: len(fam[q]) for q in fam})
    return L, W, H, v, escritas, contas


def comportamento_com_kit(L, attrs):
    """`beh(metatile)` que conhece o kit AINDA NÃO GRAVADO no disco.

    Sem isto a conta erra em silêncio, e ela errou de verdade nesta rodada: as
    vagas de metatile que esta passada reaproveita são metatiles ÓRFÃOS que
    continuam com o atributo velho no `metatile_attributes.bin`, e alguns desses
    atributos velhos são de ÁGUA. Enquanto o kit não é aplicado, perguntar o
    comportamento ao disco devolve "água" para uma célula de relva recém
    pintada, e aí a régua tira a célula do denominador e o portão da água acusa
    mudança que não existe. A resposta certa vem do kit, e do disco só o que o
    kit não escreve.
    """
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])

    def com_kit(mt_id):
        if mt_id >= 512 and (mt_id - 512) in (attrs or {}):
            return attrs[mt_id - 512] & 0xFF
        return beh(mt_id)
    return com_kit


def regua(v, W, H, L, escritas=None, attrs=None):
    """(carimbo dominante em %, células andáveis a pé, id do carimbo), como a
    `regua_cidades.py` conta."""
    beh = comportamento_com_kit(L, attrs)
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
    """A grade como está no disco, só tirando o que ESTA passada escreveu."""
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(alvo, cid, aplicar):
    metas, attrs, catalogo = desenha_kit()
    if metas:
        print("kit: 0 tiles novos, 0 cores novas, %d metatiles novos "
              "(locais %d a %d, ids %d a %d), %d vagas de metatile livres sobram"
              % (len(metas), min(metas), max(metas), 512 + min(metas),
                 512 + max(metas), len(locais_livres()) - len(metas)))
    if aplicar:
        grava_tileset(metas, attrs)
    guardado = carrega_plano()
    base = base_de(alvo, guardado)
    L, W, H, v, escritas, contas = plano_mapa(alvo, cid, catalogo, base)
    a, na, ida = regua(v, W, H, L, None, attrs)
    b, nb, idb = regua(v, W, H, L, escritas, attrs)
    print("%s: %d células de mancha, %d solidificadas, %d mudadas (%s)"
          % (alvo, sum(contas["manchas"].values()), contas["solidos"],
             len(escritas),
             ", ".join("%s %d" % kv for kv in sorted(contas["familias"].items()))))
    print("  mancha: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["manchas"].items())))
    print("  móvel:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    print("  régua: carimbo %d com %.1f%% de %d células ANTES; carimbo %d com "
          "%.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    conta = collections.Counter(c & 0x3FF for c in saida if not ((c >> 10) & 3))
    print("  os cinco mais comuns depois: " +
          ", ".join("%d x%d" % kv for kv in conta.most_common(5)))
    if aplicar:
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(saida), *saida))
        guardado[alvo] = {"celulas": [[i, v[i], escritas[i]]
                                      for i in sorted(escritas)]}
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("aplicado")
    return 0


def desfaz(alvo):
    guardado = carrega_plano()
    if alvo not in guardado:
        print("%s: nada a desfazer" % alvo)
        return 0
    d, L, W, H, v = G.grade(alvo)
    v, n = list(v), 0
    for idx, antigo, novo in guardado[alvo]["celulas"]:
        if v[idx] == novo:
            v[idx] = antigo
            n += 1
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(v), *v))
    guardado.pop(alvo)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("%s: desfeitas %d células" % (alvo, n))
    return 0


# ------------------------------------------------------------------ conferência
def confere(alvo, cid, metas, attrs, catalogo, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela é chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que tem
    que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida só no caminho feliz não é regra.
    """
    mau = []
    import render_maps as RM
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    ap, asec = G._attrs(PRIMARIO), G._attrs(SECUNDARIO)

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
        return ents_nossas(mt_id, tp, ts)

    def px_de(mt_id):
        return px_metatile(entradas(mt_id), tp, ts)

    def opacos_de(gid, cam):
        op = 0
        for e in entradas(gid)[cam * 4:cam * 4 + 4]:
            if e & 0x3FF:
                t = RM.resolver_tile(tp, ts, e & 0x3FF)
                op += _opacos(t) if t else 0
        return op

    # ------------------------------------------------------------ 1. orçamento
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    seguras = set(locais_livres())
    for local in metas:
        if local not in seguras:
            mau.append("o kit grava na vaga de metatile %d, que algum dos sete "
                       "layouts irmãos usa ou que um METATILE_Mauville_* rotula"
                       % (512 + local))
    # ESTA PASSADA NÃO ESCREVE TILE NENHUM. O portão dos pinos fica de pé mesmo
    # assim: se um dia alguém acrescentar tile aqui, a regra reprova sozinha.
    for local, ents in metas.items():
        for v in ents:
            idx = v & 0x3FF
            if idx and idx >= 512 and (idx - 512) in PINOS_ANIM:
                # referenciar tile pinado é PERMITIDO (as flores fazem isso e
                # é para isso que a animação existe); ESCREVER nele é que não é.
                pass

    # ---------- 2. CHÃO: atributo idêntico ao da família, camada de baixo CHEIA
    # e cor a menos do teto contra o carimbo mais próximo
    for qual in FAMILIAS:
        fam = FAMILIAS[qual]
        pcs = [px_de(m) for m in fam["carimbos"]]
        modelo = entradas(fam["base"])
        copia_cima = modelo[4:] == modelo[:4]
        flores = {n for n, _ in FLORES}
        for nome, gid in catalogo["chao"].get(qual, {}).items():
            if atributo(gid) != fam["attr"]:
                mau.append("o chão %s (%d) tem atributo 0x%04X e a família %s "
                           "tem 0x%04X" % (nome, gid, atributo(gid), qual,
                                           fam["attr"]))
            if opacos_de(gid, 0) != 4 * 64:
                mau.append("o chão %s (%d) tem camada de baixo com buraco"
                           % (nome, gid))
            e = entradas(gid)
            if gid in (512 + l for l in metas) and nome not in flores:
                if copia_cima and e[4:] != e[:4]:
                    mau.append("o chão %s (%d) não copia a camada de baixo na "
                               "de cima, como o carimbo de %s faz"
                               % (nome, gid, qual))
            teto = TETO_COR_FLOR if nome in flores else TETO_COR
            dc = min(_dist_cor(_cor_media(px_de(gid)), _cor_media(p))
                     for p in pcs)
            if dc > teto:
                mau.append("o chão %s (%d) está a %.1f de cor do carimbo de %s, "
                           "acima do teto de %.1f" % (nome, gid, dc, qual, teto))
            # O TETO POR QUADRANTE não vale para a FLOR, e a isenção é medida:
            # os quadrantes dela ficam de 34,1 a 72,6 do carimbo de relva porque
            # a flor é um DESENHO em cima do chão, não uma textura de chão. Ela
            # é acento de canteiro, entra em bolha de 2 a 5 células e nunca
            # cobre praça inteira; o que sustenta o acento é a BORDA da célula
            # continuar casando com a relva, e ela casa a 18,1 de RGB.
            if nome not in flores:
                pq = pior_quadrante(entradas(gid), pcs, tp, ts)
                if pq > TETO_COR_QUADRANTE:
                    mau.append("o chão %s (%d) tem um QUADRANTE a %.1f de cor do "
                               "carimbo de %s, acima do teto de %.1f: isso vira "
                               "quadrado de 8x8 na tela"
                               % (nome, gid, pq, qual, TETO_COR_QUADRANTE))

    # ---------- 3. MÓVEL: COVERED, comportamento zerado, e o NOSSO chão entrada
    # por entrada na camada de baixo
    for qual in FAMILIAS:
        base, _a = base_da_familia(qual, tp, ts)
        for nome, gid in catalogo["moveis"].get(qual, {}).items():
            a = atributo(gid)
            if (a >> 12) & 0xF != 1:
                mau.append("o móvel %s/%s (%d) não está em COVERED"
                           % (qual, nome, gid))
            if a & 0xFF:
                mau.append("o móvel %s/%s (%d) tem comportamento 0x%02X"
                           % (qual, nome, gid, a & 0xFF))
            if entradas(gid)[:4] != list(base):
                mau.append("o móvel %s/%s (%d) não tem o nosso chão de %s na "
                           "camada de baixo" % (qual, nome, gid, qual))
            if opacos_de(gid, 1) == 0:
                mau.append("o móvel %s/%s (%d) está sem arte em cima"
                           % (qual, nome, gid))

    # ---------- 4. nenhuma variante de chão é cópia pixel a pixel de outra
    #
    # DUAS ISENÇÕES, e as duas são medidas e escritas, não silêncio:
    #
    # (a) CARIMBO CONTRA CARIMBO fica de fora. Os cinco metatiles de calçada de
    #     `MauvilleCity` (94, 257, 264, 266 e 273) já vêm do Emerald a 3,6, 4,9,
    #     6,4 e 8,4 um do outro, ou seja quatro dos dez pares já nascem abaixo do
    #     piso. Isso é o DEFEITO que esta passada existe para consertar, e não
    #     algo que ela criou: cobrar o piso entre eles reprovaria o mapa de
    #     origem. O que a regra tem que proibir é peça NOVA que copie alguém, e é
    #     isso que o par (novo, qualquer) continua cobrando.
    #
    # (b) FLOR CONTRA FLOR fica de fora, e a razão está em `src/tileset_anims.c`.
    #     `TilesetAnim_Mauville` chama `QueueAnimTiles_Mauville_Flowers` com
    #     `timer_mod` de 0 a 7 e o corpo faz `timer_div -= timer_mod` antes de
    #     escolher o quadro: as OITO cópias da flor mostram quadros DEFASADOS ao
    #     mesmo tempo, e é isso que faz o canteiro balançar fora de compasso. No
    #     `tiles.png` parado as oito vagas guardam o mesmo desenho, então a
    #     distância estática entre duas flores é 0,0 e sempre será. O que
    #     substitui o piso aqui é outro portão, mais forte: as seis flores têm
    #     que vir de SEIS metatiles de origem diferentes, ou seja de seis vagas
    #     de destino diferentes da animação, senão duas delas mostrariam o MESMO
    #     quadro em jogo e aí sim seriam cópia.
    flores = {n for n, _ in FLORES}
    de_flor = [de for _n, de in FLORES]
    if len(set(de_flor)) != len(de_flor):
        mau.append("duas flores vêm do mesmo metatile de origem, e por isso "
                   "mostrariam o mesmo quadro da animação")
    for qual in FAMILIAS:
        nomes = catalogo["chao"].get(qual, {})
        lista = list(nomes.values()) + list(FAMILIAS[qual]["carimbos"])
        de_nome = {g: n for n, g in nomes.items()}
        carimbos = set(FAMILIAS[qual]["carimbos"])
        pix = {m: px_de(m) for m in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                if a in carimbos and b in carimbos:
                    continue
                if de_nome.get(a) in flores and de_nome.get(b) in flores:
                    continue
                dd = _dist_pixels(pix[a], pix[b])
                if dd < PISO_VARIANTE:
                    mau.append("as variantes de chão %d e %d de %s têm distância "
                               "%.1f, abaixo do piso de %.1f do varia_carimbo.py:"
                               " isso é enganar a régua"
                               % (a, b, qual, dd, PISO_VARIANTE))

    # ---------------------------------------- 5 em diante: o plano, célula a célula
    L, W, H, v, escritas, contas = plano
    d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    meus_chaos, meus_moveis = {}, {}
    for qual in cid["familias"]:
        for n, g in catalogo["chao"].get(qual, {}).items():
            meus_chaos[g] = (qual, n)
        for n, g in catalogo["moveis"].get(qual, {}).items():
            meus_moveis.setdefault(g, (qual, n))

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVAÇÃO em (%d,%d)" % (alvo, x, y))
        if cv and not cn:
            mau.append("%s: colisão 1 -> 0 em (%d,%d), que segue proibida"
                       % (alvo, x, y))
        if novo in meus_chaos:
            qual, _n = meus_chaos[novo]
            if cn != cv or velho not in FAMILIAS[qual]["carimbos"]:
                mau.append("%s: chão em célula errada em (%d,%d)" % (alvo, x, y))
        elif novo in meus_moveis:
            qual, _n = meus_moveis[novo]
            if cv or not cn:
                mau.append("%s: móvel em (%d,%d) não é solidificação 0 -> 1"
                           % (alvo, x, y))
            if velho != FAMILIAS[qual]["base"]:
                mau.append("%s: móvel fora do carimbo base em (%d,%d)"
                           % (alvo, x, y))
            if (x, y) in ev:
                mau.append("%s: móvel em cima do evento (%d,%d)" % (alvo, x, y))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                       % (alvo, novo, x, y))
        for qual in cid["familias"]:
            if velho in FAMILIAS[qual]["carimbos"] \
                    and (v[i] >> 12) & 0xF not in FAMILIAS[qual]["elev"]:
                mau.append("%s: (%d,%d) tem elevação fora da lista da família %s"
                           % (alvo, x, y, qual))

    # 6. (comportamento, layerType) de toda célula ANDÁVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: célula andável (%d,%d) mudou (comportamento, "
                       "layerType)" % (alvo, i % W, i // W))
            break

    # 7 e 8. alcance a pé e LIGAÇÃO a pé
    ini = E.partidas(d, W, H, v)
    antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
    solid = {(i % W, i // W) for i in escritas
             if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
    if (antes - depois) - solid:
        mau.append("%s: o alcance a pé perdeu %d células além das solidificadas: "
                   "%s" % (alvo, len((antes - depois) - solid),
                           sorted((antes - depois) - solid)[:6]))
    if depois - antes:
        mau.append("%s: o alcance a pé GANHOU célula" % alvo)
    mau += ["%s: %s" % (alvo, q) for q in
            ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                            solid)]

    # 9. a ÁGUA não é tocada: o conjunto de células de água é idêntico. Nenhuma
    # das duas cidades tem célula de água hoje (medido: zero nas duas), e o
    # portão fica de pé para o dia em que alguém acrescentar uma.
    beh = comportamento_com_kit(L, attrs)
    AG = E.agua()

    def agua_de(grade):
        return {(i % W, i // W) for i in range(W * H)
                if beh(grade[i] & 0x3FF) in AG}
    if agua_de(v) != agua_de(saida):
        mau.append("%s: o conjunto de células de ÁGUA mudou" % alvo)

    # 10. A MANCHA NÃO PODE SER ADIVINHÁVEL, e o teste tem dois lados: PADRÃO
    # (nenhuma projeção simples da posição adivinha a peça) e FORMA (mancha é
    # BOLHA, e a conta é o tamanho médio do pedaço conexo).
    mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
              if (val & 0x3FF) in meus_chaos}
    if len(mancha) < cid["piso_mancha"]:
        mau.append("%s: só %d células de mancha, abaixo do piso de %d"
                   % (alvo, len(mancha), cid["piso_mancha"]))
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
                if ac - cego > PISO_PADRAO:
                    mau.append("%s: saber %s mod %d adivinha a peça em %.0f%% "
                               "das células contra %.0f%% do chute cego: virou "
                               "padrão" % (alvo, rot, mod, 100 * ac, 100 * cego))
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
        if len(mancha) / pedacos < 5.0:
            mau.append("%s: a mancha média tem só %.1f células (%d em %d "
                       "pedaços): virou sal e pimenta, não bolha"
                       % (alvo, len(mancha) / pedacos, len(mancha), pedacos))

    # 11. a régua tem que fechar em 20% ou menos
    b, nb, idb = regua(v, W, H, L, escritas, attrs)
    if b > TETO_REGUA:
        mau.append("%s: a régua ainda marca %.1f%% de carimbo dominante"
                   % (alvo, b))
    return mau


# ------------------------------------------------------------------ auto-teste
def demo(alvo, cid):
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferença" só vale depois que a comparação mostra que sabe reprovar.
    """
    metas, attrs, catalogo = desenha_kit()
    guardado = carrega_plano()
    plano = plano_mapa(alvo, cid, catalogo, base_de(alvo, guardado))
    mau = confere(alvo, cid, metas, attrs, catalogo, plano)
    negativas = []

    def copia():
        L, W, H, v, esc, ct = plano
        return (alvo, cid, dict(metas), dict(attrs),
                json.loads(json.dumps(catalogo)),
                (L, W, H, list(v), dict(esc), ct))

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = confere(*args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NÃO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    fam0 = cid["familias"][0]
    # Os NOVOS primeiro: as sabotagens de atributo e de arte só fazem sentido em
    # peça que ESTA passada escreve. Chão e móvel DIRETOS (metatile que já
    # existia) entram no fim da lista.
    chao0 = sorted(catalogo["chao"][fam0],
                   key=lambda n: (catalogo["chao"][fam0][n] - 512 not in metas, n))
    mov0 = sorted(catalogo["moveis"][fam0],
                  key=lambda n: (catalogo["moveis"][fam0][n] - 512 not in metas, n))

    # N1. colisão 1 -> 0 numa célula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[5]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)
        return a
    sabota("colisão 1 -> 0", n1, "colisão 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[5]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevação alterada", n2, "mudou ELEVAÇÃO")

    # N3. comportamento de um metatile de CHÃO sabotado
    def n3():
        a = copia()
        gid = a[4]["chao"][fam0][chao0[0]]
        a[3][gid - 512] = (a[3][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("comportamento de chão sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        for nome in mov0:
            gid = a[4]["moveis"][fam0][nome]
            if gid - 512 in a[3]:
                a[3][gid - 512] = a[3][gid - 512] & 0x0FFF
                return a
        raise SystemExit("não há móvel remontado em %s para sabotar" % fam0)
    sabota("layerType NORMAL no móvel", n4, "não está em COVERED")

    # N5. comportamento não zerado num móvel
    def n5():
        a = copia()
        for nome in mov0:
            gid = a[4]["moveis"][fam0][nome]
            if gid - 512 in a[3]:
                a[3][gid - 512] = a[3][gid - 512] | 0x02
                return a
        raise SystemExit("não há móvel remontado em %s para sabotar" % fam0)
    sabota("comportamento no móvel", n5, "tem comportamento")

    # N6. móvel SEM o nosso chão embaixo: sobraria a camada de baixo da origem
    def n6():
        a = copia()
        for nome in mov0:
            gid = a[4]["moveis"][fam0][nome]
            if gid - 512 in a[2]:
                e = list(a[2][gid - 512])
                e[0] = 0x5000 | 300
                a[2][gid - 512] = e
                return a
        raise SystemExit("não há móvel remontado em %s para sabotar" % fam0)
    sabota("chão errado no móvel", n6, "não tem o nosso chão")

    # N7. chão com buraco na camada de baixo: em NORMAL o BG3 é lixo
    def n7():
        a = copia()
        for nome in chao0:
            gid = a[4]["chao"][fam0][nome]
            if gid - 512 in a[2]:
                e = list(a[2][gid - 512])
                e[0] = 0
                a[2][gid - 512] = e
                return a
        raise SystemExit("não há chão novo em %s para sabotar" % fam0)
    sabota("chão com buraco embaixo", n7, "camada de baixo com buraco")

    # N8. célula andável com (comportamento, layerType) trocado
    def n8():
        a = copia()
        for nome in chao0:
            gid = a[4]["chao"][fam0][nome]
            if gid - 512 in a[3]:
                a[3][gid - 512] = 0x0002
                return a
        raise SystemExit("não há chão novo em %s para sabotar" % fam0)
    sabota("layerType de chão trocado", n8, "mudou (comportamento")

    # N9. um móvel plantado em cima de célula de EVENTO
    def n9():
        a = copia()
        L, W, H, v, esc, ct = a[5]
        d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
        gid = a[4]["moveis"][fam0][mov0[0]]
        for x, y in sorted(E.eventos(d)):
            i = y * W + x
            if (v[i] & 0x3FF) == FAMILIAS[fam0]["base"] and not ((v[i] >> 10) & 3):
                esc[i] = (v[i] & 0xF000) | (1 << 10) | gid
                return a
        raise SystemExit("não há evento em cima do carimbo para sabotar")
    sabota("móvel em cima de evento", n9, "em cima do evento")

    # N10. a mancha espalhada AO ACASO, com as mesmas células
    def n10():
        a = copia()
        L, W, H, v, esc, ct = a[5]
        meus = {g for qual in cid["familias"]
                for g in catalogo["chao"][qual].values()}
        cels = [i for i in esc if (esc[i] & 0x3FF) in meus]
        por_fam = collections.defaultdict(list)
        for i in cels:
            for qual in cid["familias"]:
                if (v[i] & 0x3FF) in FAMILIAS[qual]["carimbos"]:
                    por_fam[qual].append(i)
                    break
        for qual, idxs in por_fam.items():
            livres = [i for i in range(W * H)
                      if (v[i] & 0x3FF) in FAMILIAS[qual]["carimbos"]
                      and not ((v[i] >> 10) & 3) and i not in esc]
            livres.sort(key=lambda i: _mistura(i, 0xDEAD))
            valores = [esc[i] & 0x3FF for i in idxs]
            for i in idxs:
                del esc[i]
            for k, val in enumerate(valores):
                if k < len(livres):
                    esc[livres[k]] = (v[livres[k]] & 0xFC00) | val
        return a
    sabota("mancha espalhada ao acaso", n10, "sal e pimenta")

    # N11. duas variantes de chão IGUAIS pixel a pixel: é enganar a régua
    def n11():
        a = copia()
        # As FLORES ficam de fora: elas são isentas do piso de propósito (ver a
        # regra 4), então copiar uma na outra não teria o que acusar. A
        # sabotagem tem que cair em peça que o piso realmente cobra.
        flor = {n for n, _ in FLORES}
        novos = [n for n in chao0
                 if a[4]["chao"][fam0][n] - 512 in a[2] and n not in flor]
        ga = a[4]["chao"][fam0][novos[0]]
        gb = a[4]["chao"][fam0][novos[1]]
        a[2][gb - 512] = list(a[2][ga - 512])
        return a
    sabota("variante de chão duplicada", n11, "abaixo do piso de")

    # N12. gravar numa vaga de metatile que algum dos sete layouts usa
    def n12():
        a = copia()
        vivos = sorted({(c & 0x3FF) - 512
                        for c in blocos("data/layouts/Route110/map.bin")
                        if (c & 0x3FF) >= 512})
        alvo_local = vivos[0]
        a[2][alvo_local] = list(a[2][min(a[2])])
        a[3][alvo_local] = 0x1000
        a[4]["chao"][fam0][chao0[0]] = 512 + alvo_local
        return a
    sabota("grava em vaga de metatile viva", n12, "layouts irmãos usa")

    # ------------------------------------------------ o que está NO DISCO
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    postas = [l for l in metas if _entradas(meta_disco, l) == metas[l]]
    if not postas:
        print("aviso: o kit ainda não foi aplicado no tileset; o caso de DISCO "
              "não roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit está pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ents in metas.items():
            if _entradas(meta_disco, local) != ents:
                mau.append("metatile %d no disco não é o do kit" % (512 + local))
            if struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco não é o do kit"
                           % (512 + local))

    # ------------------------------------------------------- idempotência
    L, W, H, v, escritas, contas = plano
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    volta = list(saida)
    for i in sorted(escritas):
        if volta[i] == escritas[i]:
            volta[i] = v[i]
    if volta != list(v):
        mau.append("%s: desfazer não devolve a base" % alvo)
    _, _, _, _, esc2, _ = plano_mapa(alvo, cid, catalogo, volta)
    if esc2 != escritas:
        mau.append("%s: segunda passada deu plano diferente" % alvo)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE")
    a, na, ida = regua(v, W, H, L, None, attrs)
    b, nb, idb = regua(v, W, H, L, escritas, attrs)
    print("  %-15s %d células mudadas, %d solidificadas, régua %.1f%% -> %.1f%%"
          % (alvo, len(escritas), contas["solidos"], a, b))
    print("  0 tiles, 0 cores, %d metatiles novos, %d provas negativas:"
          % (len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-32s -> %s" % (nome, queixa[:92]))
    return 0


ALVO = "MauvilleCity"
CIDADE = CIDADE_MAUVILLE


def main():
    if "--desfazer" in sys.argv:
        return desfaz(ALVO)
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo(ALVO, CIDADE)
    if "--so-tileset" in sys.argv:
        m, at, _c = desenha_kit()
        grava_tileset(m, at)
        print("tileset escrito: 0 tiles, %d metatiles" % len(m))
        return 0
    return roda(ALVO, CIDADE, "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
