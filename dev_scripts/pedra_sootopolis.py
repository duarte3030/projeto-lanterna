#!/usr/bin/env python3
"""Refino de `SootopolisCity` (tema CRATERA E ÁGUA), no `gTileset_Sootopolis`,
com arte NOVA desenhada aqui e ZERO peça importada de ROM hack.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py` nesta
árvore em 09/09/2026: das 908 células andáveis a pé, **607 (66,9%) são o metatile
729**, a pedra branca do terraço, e ela cobre a cratera inteira. É o terceiro pior
carimbo de Hoenn e o defeito é literal: a cidade do Wallace é um caminho de pedra
chapada serpenteando entre paredões, sem uma junta, uma rachadura ou uma poça em
908 células.

A PLANTA DE SOOTOPOLIS NÃO É PRAÇA, É LABIRINTO, e isso muda o desenho inteiro.
Medido varrendo o `map.bin`: o terraço branco anda em faixas de 2 a 6 células
entre paredões sólidos, nunca num pátio aberto. Bolha grande não cabe, e enfeite
plantado no meio do caminho tranca gente. Por isso as bolhas desta passada são
curtas (2 a 9 células) e os móveis são poucos, todos de beira e todos conferidos
célula a célula pelos dois portões de ligação a pé.

A ÁGUA É SURF E NÃO É TOCADA, e isso é medido e não prometido. As 640 células de
comportamento de água do lago (a elevação 1 do meio da cratera) são filtradas
para fora do catálogo por `enfeita_cidades.agua()` antes de qualquer conta, e o
`confere` cobra que o CONJUNTO de células de água seja idêntico byte a byte antes
e depois. Esta passada escreve só nos 10 bits baixos (metatile) e no bit de
colisão de célula de TERRA, nunca nos 4 bits de elevação e nunca numa célula de
água: o alcance de Surf sai igual por construção, e o portão prova.

AS VAGAS DE TILE 240 A 335 SÃO INTOCÁVEIS, E SÃO NOVENTA E SEIS. Medido com
`dev_scripts/pinos_anim.py gTileset_Sootopolis`: `src/tileset_anims.c`
(`QueueAnimTiles_Sootopolis_StormyWater`) copia 96 tiles de água agitada para
`NUM_TILES_IN_PRIMARY + 240` em tempo de execução e não sabe de renumeração.
Escrever ali não quebra o build, não muda um pixel do render estático e só
aparece dentro do jogo. Esta passada não escreve NENHUMA delas: os tiles novos
começam na vaga 336, que é a primeira depois do fim do `tiles.png` de hoje, e o
`confere` tem um portão que reprova qualquer vaga entre 240 e 335. Conferido
DEPOIS de aplicar: as 96 vagas continuam byte a byte iguais às de antes.

O TILESET É DE UM MAPA SÓ, e a prova de "0 pixel no mapa irmão" NÃO EXISTE AQUI.
Conferido em `data/layouts/layouts.json`: `gTileset_Sootopolis` é secundário de
UM layout (`LAYOUT_SOOTOPOLIS_CITY`) e de UM mapa (`SootopolisCity`). Fabricar
uma prova de irmão seria inventar evidência vazia. No lugar dela entram as DUAS
contas diretas que o `praca_hearthome.py` usou:

  1. NENHUMA COR É ESCRITA. Esta passada não muda um byte de `palettes/*.pal`.
     Toda a arte nova é pintada com a vaga de paleta 7, que é a do próprio
     carimbo, e só com índices que a paleta 7 JÁ TEM. Logo não existe pixel vivo
     que mude de cor, e o portão `confere` compara os treze arquivos de paleta
     do disco com os do kit e reprova se um byte se mexer.
  2. NENHUM TILE É ESCRITO EM VAGA QUE ALGUM METATILE PEÇA. Medido varrendo os
     254 metatiles do `gTileset_Sootopolis`: o maior tile LOCAL que algum deles
     referencia é o 327, e o `tiles.png` tem 336. Os tiles novos vão de 336 para
     cima, e o portão reprova qualquer vaga abaixo de 336.

A FONTE DE ARTE, e as DUAS REPROVAÇÕES por número. O índice do condutor
(`/tmp/claude-501/FONTES-POR-TILESET.md`) dá dois candidatos para
`secondary/sootopolis`, e os dois foram extraídos e OLHADOS nesta rodada, com o
`extrai_tileset.py` e o `render_hack.py`:

  - `light-platinum` `0x286E2C` (fração de arte nova 0,947), o secundário da
    cidade g00m07 do Pokémon Light Platinum. É uma cidade RIBEIRINHA moderna:
    calçamento de pedra azul-acinzentada, casas de telhado azul-chumbo, chafariz,
    banco e poste. Medindo a cor média de cada metatile que usa arte do
    secundário do hack contra a cor média do nosso carimbo 729 ((236,4; 236,4;
    227,4) na paleta 7), o CALÇAMENTO dele, que é a única peça de chão do tema,
    fica a **59,2, 67,5, 75,8, 78,6 e 79,0** de distância RGB, muito acima do
    corte de ~50 que Hearthome fixou. Os dois únicos metatiles do hack que PASSAM
    no corte são o local 359 (30,1) e o local 283 (42,0), e olhando os dois
    ampliados eles são um pedaço de PAREDE com uma faixa laranja e um pedaço de
    TELHADO vermelho: nem chão, nem móvel, nem nada que caiba numa cratera de
    calcário branco. REPROVADO.
  - `golden-glazed` `0x3DF83C` (0,943), o secundário da cidade g00m07 do Pokémon
    Golden Glazed. É uma cidade de CÂNION, chão vermelho-tijolo e paredão
    marrom. O metatile mais próximo do nosso carimbo está a **74,6** e o segundo
    a 97,1. Não há um único metatile abaixo do corte. REPROVADO.

Reprovar com o número na mão vale mais do que importar peça que não casa, e é o
mesmo caminho que `praca_hearthome.py` tomou. Consequência direta: **o
`CREDITS.md` não é tocado nesta passada**, porque não há asset importado a
creditar.

DE ONDE VEM A ARTE, ENTÃO. De dois lugares, os dois nossos:

  - REARRANJO E ESPELHO do próprio carimbo. O 729 é `[98, 99, 114, 115]` do
    `gTileset_General` pintado com a vaga de paleta 7, e os quatro são mancha
    clara ASSIMÉTRICA: girar, espelhar e trocar os quadrantes de lugar move de
    13,8 a 26,4 pixel a pixel, tudo acima do piso de 8,0 que o `varia_carimbo.py`
    documenta como "invisível em jogo". Custo: ZERO tile, ZERO cor, uma vaga de
    metatile cada.
    ACHADO DE LADO, e ele CORTOU quatro variantes da primeira lista: os tiles 70,
    75, 82 e 83 do `gTileset_General` são cópia PIXEL A PIXEL dos 98, 99, 114 e
    115. Um metatile feito deles marca 0,0 de distância do carimbo, ou seja seria
    trocar o carimbo por ele mesmo e ver a régua cair sem um pixel mudar na tela.
    Fora.
  - ARTE NOVA DESENHADA AQUI, e ela é o que dá o tema. Cada peça é o carimbo (ou
    um rearranjo dele) com uma máscara de detalhe por cima, desenhada em texto no
    próprio arquivo e pintada SÓ com índices que a paleta 7 já tem: o 13
    (172,172,156) e o 14 (148,148,123) para junta, rachadura e musgo seco; o 12
    (205,205,189) para desgaste e cascalho; o 5 (131,131,139) para poça de água;
    o 3 (189,148,139) e o 4 (156,115,115) para o líquen avermelhado, que é a cor
    da rocha vulcânica que a própria cidade já tem na beira do lago. Nenhuma cor
    nova, nenhum índice novo.

AS TRÊS PEÇAS QUE FORAM CORTADAS DEPOIS DO RENDER, e as três pelo olho e não pelo
número:

  - RESPINGO (quadradinhos azuis espalhados). No número passava; ampliado, os
    quadrados de 2x2 na cor 5 leem como ladrilho azul solto, não como água que
    espirrou. Poça sim, respingo não.
  - RISCO (barras horizontais de 6 pixels). Lê como escada deitada ou como
    tábua, e não como arranhão em pedra.
  - LASCA (bolha escura no meio da célula). Sozinha no meio do caminho lê como
    buraco, e buraco no chão de uma cidade é erro de mapa.

E DOIS METATILES DE MÓVEL FORAM CORTADOS pelo mesmo defeito que Dewford já tinha
medido: o 508 e o 509 do `gTileset_General` ("mato de duna") desenham a METADE DE
BAIXO de um arbusto que mora na célula de cima, então soltos no chão viram um
borrão verde grudado na borda superior. No lugar deles entram o 510 e o 511, que
são touceira ancorada embaixo e fecham sozinhos.

AS REGRAS DE MONTAGEM:

  - CHÃO é metatile com o atributo do carimbo bit a bit (`0x1000`, comportamento
    zerado com `layerType` COVERED) e com a camada de cima DUPLICANDO a de baixo,
    que é como o 729 é montado. Em COVERED a camada de baixo vai para o BG3 e a
    de cima para o BG2, as duas ABAIXO do sprite: pedra em cima de pedra dá o
    mesmo pixel, e copiar a estrutura do carimbo deixa o metatile novo do MESMO
    formato que o velho.
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chão de pedra entrada por entrada, e o atributo é
    comportamento ZERADO com `layerType` COVERED (`0x1000`).
  - MÓVEL ENCOSTA EM ALGUMA COISA (sólido, água ou borda do mapa). Pedra solta no
    meio da passarela lê como erro de mapa, e num caminho de 2 células de largura
    ela ainda por cima estreita a passagem.
  - QUADRANTE DE BAIXO SOBE quando o de cima está vazio (a regra do
    `porto_canalave.py`).
  - A MANCHA É BOLHA, não sal e pimenta, e o auto-teste prova isso comparando o
    tamanho médio do pedaço conexo com o de uma sabotagem que espalha as MESMAS
    células ao acaso.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado. E
    nenhuma ARTE de fora, tampouco.

Uso:
    python3 dev_scripts/pedra_sootopolis.py               # mede e mostra o plano
    python3 dev_scripts/pedra_sootopolis.py --aplicar     # escreve tileset e mapa
    python3 dev_scripts/pedra_sootopolis.py --desfazer    # devolve o map.bin
    python3 dev_scripts/pedra_sootopolis.py --demo        # auto-teste
    python3 dev_scripts/pedra_sootopolis.py --so-tileset  # só o tileset, sem mapa
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

# O `enfeita_cidades.py` PULA o proprio bloco de teste quando varre os corredores
# que a suite anda, e a razao e circularidade: o bloco desta passada e derivado DO
# desenho, e nao o contrario. Aqui o bloco proprio e o 214.
BLOCO_PROPRIO = "214_pedra_sootopolis.json"
E.BLOCO_PROPRIO = BLOCO_PROPRIO

ALVO = "SootopolisCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/sootopolis"
PLANO = f"{RAIZ}/dev_scripts/pedra_sootopolis.json"

PRIMARIO = "gTileset_General"
SECUNDARIO = "gTileset_Sootopolis"
# O `gTileset_Sootopolis` e secundario de UM layout e de UM mapa. Conferido em
# `data/layouts/layouts.json`: nao existe mapa irmao, e por isso a prova de
# "0 pixel no irmao" nao aparece nesta passada (ver o cabecalho).
IRMAOS = ["SootopolisCity"]

TETO_TILES = 512
TETO_META = 512
TILE_LOCAL_0 = 336          # o `tiles.png` tem 336 tiles; o maior PEDIDO e o 327
META_LOCAL_0 = 254          # o mapa usa os locais 0 a 253
# A AGUA AGITADA. `QueueAnimTiles_Sootopolis_StormyWater` escreve 96 tiles a
# partir de `NUM_TILES_IN_PRIMARY + 240`. NUNCA escrever aqui.
PINOS_ANIM = set(range(240, 336))
MARGEM = 1                  # celulas de folga em relacao a borda do mapa
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%
TETO_COR = 36.0             # distancia de cor media aceita entre chao novo e carimbo
PISO_VARIANTE = 8.0         # distancia pixel a pixel minima entre duas variantes
# Quanto uma projecao simples da posicao pode acertar a peca ALEM do chute cego
# antes de a mancha virar "padrao". Aqui cabe o corte de 8,0% de Sunyshore, e nao
# os 12,0% que Dewford precisou: Dewford tinha menos de 110 celulas de mancha num
# mapa 20x20 e o ruido amostral sozinho passava de 8%; aqui a mancha tem mais de
# quatrocentas celulas num mapa 60x60, e cada classe de "x mod 7" tem dezenas.
PISO_PADRAO = 0.08
PISO_MANCHA = 380           # abaixo disso a passada nao fez o servico
ESPACO_ENTRE_MOVEIS = 3     # Chebyshev minimo entre dois moveis QUAISQUER
PISO_BOLHA = 2              # tamanho minimo de uma bolha que a regiao cortou

N4 = E.N4

CARIMBO = 729               # a pedra branca do terraco
ELEVACOES = {3}             # o terraco inteiro esta na elevacao 3
PAL_PEDRA = 7               # a vaga de paleta que o carimbo 729 usa
ATTR_CARIMBO = 0x1000       # comportamento 0, layerType COVERED

# Os quatro tiles do carimbo, na ordem dos quadrantes.
BASE_TILES = [98, 99, 114, 115]

# Os indices de cor da vaga 7 que esta passada usa, e o que cada um e de verdade
# (lido de `palettes/07.pal`):
#   9  (246,246,246) branco puro        10 (246,246,238) branco quente, a base
#   11 (222,222,213) sombra clara       12 (205,205,189) sombra media
#   13 (172,172,156) junta              14 (148,148,123) junta funda, musgo seco
#   3  (189,148,139) liquen claro        4 (156,115,115) liquen escuro
#   5  (131,131,139) agua parada         6 ( 98, 98,123) agua funda
COD = {" ": None, ".": 10, ":": 11, "=": 12, "-": 13, "#": 14, "*": 9,
       "r": 3, "R": 4, "b": 5, "B": 6}


# ------------------------------------------------------------ arranjos de base
def _q(t, fh=0, fv=0):
    return (t, fh, fv)


# O carimbo, e os rearranjos dele. `_esp` espelha o 16x16 INTEIRO: troca os
# quadrantes de lugar E liga o bit de espelho de cada um, que e o que faz o
# espelho ser do desenho e nao de cada pedaco.
CAR = [_q(98), _q(99), _q(114), _q(115)]


def _esp_h(quads):
    a, b, c, d = quads
    return [(b[0], 1 - b[1], b[2]), (a[0], 1 - a[1], a[2]),
            (d[0], 1 - d[1], d[2]), (c[0], 1 - c[1], c[2])]


def _esp_v(quads):
    a, b, c, d = quads
    return [(c[0], c[1], 1 - c[2]), (d[0], d[1], 1 - d[2]),
            (a[0], a[1], 1 - a[2]), (b[0], b[1], 1 - b[2])]


VIR = _esp_h(CAR)                       # a pedra virada
CAB = _esp_v(CAR)                       # a pedra de cabeca para baixo
GIR = _esp_h(_esp_v(CAR))               # a pedra girada meia volta
TRO = [_q(114), _q(115), _q(98), _q(99)]        # os quadrantes trocados
CRU = [_q(99), _q(98, 1), _q(115, 0, 1), _q(114, 1, 1)]

# Os quatro tiles quase lisos do primario que passam na cor (73 a 1,0; 53 a 1,3;
# 52 a 1,5; 72 a 3,5) e que juntos leem como laje polida.
LIS = [_q(73), _q(53, 1), _q(52, 0, 1), _q(72, 1, 1)]
LIS2 = [_q(52), _q(98, 1), _q(72, 0, 1), _q(114, 1, 1)]

ARRANJOS = dict(CAR=CAR, VIR=VIR, CAB=CAB, GIR=GIR, TRO=TRO, CRU=CRU,
                LIS=LIS, LIS2=LIS2)

# ------------------------------------------------------------------- o DETALHE
# Cada mascara e 16 linhas de 16 caracteres. Espaco = nao mexe, o resto e indice
# da paleta 7 pelo dicionario COD. O tile do quadrante so vira tile NOVO se a
# mascara encostar nele; quadrante intocado continua apontando para o tile do
# primario, de graca.
DETALHES = {
    "junta de laje": ("CAR", [
        "               :",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "               -",
        "::::::::::::::::",
        "----------------"]),
    "junta travada": ("VIR", [
        "       :       :",
        "       -       -",
        "       -       -",
        "       -       -",
        "       -       -",
        "       -       -",
        "::::::::::::::::",
        "----------------",
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
        "                ",
        "                "]),
    "rachadura": ("CAR", [
        "    -           ",
        "    -=          ",
        "     -          ",
        "     -=         ",
        "      -         ",
        "      #-        ",
        "       -        ",
        "       -=       ",
        "        -       ",
        "        -=      ",
        "         -      ",
        "         #-     ",
        "          -     ",
        "          -=    ",
        "           -    ",
        "           -    "]),
    "rachadura ramificada": ("CAR", [
        "                ",
        "          -     ",
        "         -=     ",
        "         -      ",
        "        -       ",
        "    -----       ",
        "   -=   -       ",
        "  -=     --     ",
        " -=        -    ",
        "                ",
        "                ",
        "      --        ",
        "     -==-       ",
        "    -=  -       ",
        "   -     -      ",
        "          -     "]),
    "pedra gasta": ("CAR", [
        "                ",
        "    ::====:     ",
        "   :=======:    ",
        "  :=========:   ",
        "  :==-----==:   ",
        "   :=------=:   ",
        "    :=====:     ",
        "      :::       ",
        "                ",
        "         :::    ",
        "       ::====:  ",
        "      :==---=:  ",
        "      :=----=:  ",
        "       ::===:   ",
        "         ::     ",
        "                "]),
    # O CASCALHO NASCEU COMO TELA DE MOSQUITEIRO. A primeira versao era um campo
    # denso de pares de pixels espalhados, e no render ele parou de ler como
    # pedra lascada e passou a ler como malha: e o mesmo defeito que o
    # `praia_dewford.py` mediu no tile 356 do primario. O de agora tem OITO
    # lascas de dois a quatro pixels, longe umas das outras, com nucleo na cor 13
    # e sombra na 12.
    "cascalho": ("CAR", [
        "                ",
        "    #-          ",
        "    -=          ",
        "                ",
        "          --    ",
        "          -=    ",
        "  #-            ",
        "  -=       ##-  ",
        "        --  -=  ",
        "        -=      ",
        "                ",
        "    ##-      -  ",
        "    -=      #-  ",
        "             =  ",
        "  --            ",
        "  -=      --    "]),
    "poca de agua": ("CAR", [
        "                ",
        "      ::::      ",
        "     :bbbb:     ",
        "    :bbbbbb:    ",
        "    :bbBBbb:    ",
        "     :bbbb:     ",
        "      ::::      ",
        "                ",
        "                ",
        "                ",
        "          ::    ",
        "         :bb:   ",
        "         :bb:   ",
        "          ::    ",
        "                ",
        "                "]),
    # O LIQUEN COM TRES BOLHAS virava fileira de confete vermelho quando duas
    # celulas vizinhas caiam na mesma peca. Ficaram DUAS bolhas, uma delas so com
    # a cor clara (3), e o nucleo escuro (4) apareceu so na maior.
    "liquen": ("CAR", [
        "                ",
        "                ",
        "     rrr        ",
        "    rrRRr       ",
        "    rRRRr       ",
        "     rRrr       ",
        "      rr        ",
        "                ",
        "                ",
        "                ",
        "                ",
        "           rr   ",
        "          rrr   ",
        "           rr   ",
        "                ",
        "                "]),
    "musgo seco": ("VIR", [
        "                ",
        "                ",
        "      ---       ",
        "     -###-      ",
        "     -###-      ",
        "      ---       ",
        "                ",
        "                ",
        "          --    ",
        "         -##-   ",
        "         -##-   ",
        "          --    ",
        "    --          ",
        "   -##-         ",
        "    --          ",
        "                "]),
    # O VEIO NASCEU FRACO e o portao 5 pegou. A primeira versao era uma linha de
    # dois pixels na cor 12 e ficava a 6,3 pixel a pixel da "pedra de cabeca",
    # abaixo do piso de 8,0: seria trocar o carimbo por ele mesmo e ver a regua
    # cair sem mudar a tela. O veio de agora tem nucleo na cor 13, sombra na 12 e
    # atravessa a celula inteira nas duas diagonais.
    # O VEIO PRECISOU DE DOIS CONSERTOS. O primeiro foi de FORCA: ele era uma
    # linha de dois pixels na cor 12 e ficava a 6,3 pixel a pixel da "pedra de
    # cabeca", abaixo do piso de 8,0, ou seja seria derrubar a regua sem mudar a
    # tela. O segundo foi de EMENDA: com o veio indo de canto a canto, duas
    # celulas vizinhas emendavam a diagonal e o terraco ganhava riscos de vinte
    # celulas de comprimento, que leem como rabisco e nao como pedra. O de agora
    # PARA a duas colunas da borda dos dois lados, entao cada veio fecha dentro
    # da propria celula.
    "veio de pedra": ("GIR", [
        "                ",
        "                ",
        "   -=           ",
        "    ==-=        ",
        "      ==-=      ",
        "        ==-=    ",
        "          ==-   ",
        "            =   ",
        "                ",
        "                ",
        "             -  ",
        "           =-=  ",
        "         =-=    ",
        "       =-=      ",
        "      ==        ",
        "                "]),
    "junta rachada": ("TRO", [
        "               :",
        "               -",
        "         -     -",
        "         -=    -",
        "          -    -",
        "          -=   -",
        "           -   -",
        "           -=  -",
        "            -  -",
        "            -= -",
        "             - -",
        "             -=-",
        "              --",
        "               -",
        "::::::::::::::::",
        "----------------"]),
    "pedra manchada": ("CAB", [
        "                ",
        "        ::::    ",
        "      ::====:   ",
        "     :==--==:   ",
        "     :=----=:   ",
        "     :==--==:   ",
        "      ::==:     ",
        "        ::      ",
        "                ",
        "   ::::         ",
        "  ::===:        ",
        "  :=---:        ",
        "   ::=:         ",
        "                ",
        "                ",
        "                "]),
}

# AS ORIENTACOES. Espelhar o 16x16 pronto e de graca (o mesmo tile com o bit de
# espelho ligado) e multiplica o catalogo sem custar tile nem cor. So entra a
# orientacao que fica a PISO_VARIANTE ou mais de toda outra peca, e o portao 6 do
# `confere` mede isso de novo sobre o que sair.
# AS QUATRO ORIENTACOES DE TODA PECA DE MOTIVO SOLTO, e isso e conserto de um
# defeito que so o render mostrou. Sootopolis anda em corredores de uma e duas
# celulas de largura, e numa faixa de UMA celula a bolha e uma LINHA RETA: com
# duas orientacoes, a mesma poca caia na mesma altura em celulas seguidas e o
# corredor ganhava um pontilhado azul que le como pegada, nao como agua parada. O
# espelho e de graca (mesmo tile com o bit de espelho ligado, ZERO tile novo), e
# com quatro posicoes de motivo o pontilhado some. As pecas de LINHA (junta,
# veio, rachadura) nao tem esse problema, porque a linha delas ja atravessa a
# celula, e algumas nem admitem espelho sem virar a duplicata da outra.
ORIENTACOES = {
    "junta de laje": ["", "h"],
    "junta travada": ["", "v"],
    "rachadura": ["", "h", "v", "hv"],
    "rachadura ramificada": ["", "h", "v", "hv"],
    "pedra gasta": ["", "h", "v", "hv"],
    "cascalho": ["", "h", "v", "hv"],
    "poca de agua": ["", "h", "v", "hv"],
    "liquen": ["", "h", "v", "hv"],
    "musgo seco": ["", "h", "v", "hv"],
    "veio de pedra": ["", "h"],
    "junta rachada": ["", "h"],
    "pedra manchada": ["", "h", "v", "hv"],
}

# O CHAO SEM DETALHE: rearranjo puro do carimbo, custo ZERO tile.
CHAO_LIMPO = [
    dict(nome="pedra virada", arranjo="VIR"),
    dict(nome="pedra de cabeca", arranjo="CAB"),
    dict(nome="pedra girada", arranjo="GIR"),
    dict(nome="pedra trocada", arranjo="TRO"),
    dict(nome="pedra cruzada", arranjo="CRU"),
    dict(nome="pedra polida", arranjo="LIS"),
    dict(nome="pedra polida mista", arranjo="LIS2"),
]

# ---------------------------------------------------------------- os MÓVEIS
# Metatile do NOSSO par de tilesets cuja camada de CIMA e levantada sobre a nossa
# pedra. Custa ZERO tile, ZERO cor e uma vaga de metatile cada.
# TODA PECA ENTRA POUCAS VEZES, e isso e conta e nao gosto: os caminhos de
# Sootopolis tem 2 a 6 celulas de largura e cada peca posta mata o anel de tres
# em volta dela, entao repetir a mesma peca comeria o lugar das outras.
MOVEIS = [
    dict(nome="pedra azulada",      mt=315, quantos=2, espaco=8),
    dict(nome="pedra azulada larga", mt=316, quantos=2, espaco=8),
    dict(nome="matacao rosado",     mt=504, quantos=2, espaco=8),
    dict(nome="matacao rosado alto", mt=505, quantos=2, espaco=8),
    dict(nome="pedregulho",         mt=226, quantos=2, espaco=8),
    dict(nome="touceira",           mt=510, quantos=2, espaco=7),
    dict(nome="touceira virada",    mt=511, quantos=2, espaco=7),
    dict(nome="planta de fresta",   mt=735, quantos=3, espaco=6),
    dict(nome="poste de pedra",     mt=313, quantos=1, espaco=9),
    dict(nome="mureta de pedra",    mt=733, quantos=1, espaco=9),
]

# AS BOLHAS. Grupo grande de proposito: bolha de uma peca so faz cada mancha sair
# de uma cor unica, e ai saber onde a celula esta passa a adivinhar a peca, que e
# o que o caso 11 do auto-teste proibe. As tres passadas de bolha sao de tamanho
# decrescente: a primeira pega as faixas largas, a segunda o que sobrou e a
# terceira os cotocos de duas e tres celulas que o labirinto deixa.
TEMA = dict(
    bolhas1=[
        dict(grupo=["junta de laje", "junta de laje h", "junta travada",
                    "junta travada v"], tam=(5, 9), quantas=12),
        dict(grupo=["rachadura", "rachadura h", "rachadura v",
                    "rachadura hv"], tam=(4, 8), quantas=12),
        dict(grupo=["pedra gasta", "pedra gasta h", "pedra gasta v",
                    "pedra gasta hv", "pedra manchada", "pedra manchada h",
                    "pedra manchada v", "pedra manchada hv"],
             tam=(4, 8), quantas=12),
        dict(grupo=["cascalho", "cascalho h", "cascalho v", "cascalho hv",
                    "veio de pedra", "veio de pedra h"], tam=(4, 8), quantas=12),
        dict(grupo=["pedra virada", "pedra girada", "pedra trocada",
                    "pedra cruzada"], tam=(5, 9), quantas=12),
    ],
    bolhas2=[
        dict(grupo=["musgo seco", "musgo seco h", "musgo seco v",
                    "musgo seco hv", "liquen", "liquen h", "liquen v",
                    "liquen hv"], tam=(3, 6), quantas=12),
        dict(grupo=["poca de agua", "poca de agua h", "poca de agua v",
                    "poca de agua hv", "pedra de cabeca"], tam=(3, 6),
             quantas=12),
        dict(grupo=["rachadura ramificada", "rachadura ramificada h",
                    "rachadura ramificada v", "rachadura ramificada hv",
                    "junta rachada", "junta rachada h"], tam=(3, 7), quantas=12),
        dict(grupo=["pedra polida", "pedra polida mista", "pedra virada"],
             tam=(3, 7), quantas=12),
        dict(grupo=["junta de laje", "junta travada v", "cascalho h",
                    "cascalho v", "pedra manchada", "pedra manchada hv"],
             tam=(3, 7), quantas=12),
    ],
    bolhas3=[
        dict(grupo=["pedra girada", "pedra trocada", "veio de pedra",
                    "musgo seco", "musgo seco hv"], tam=(2, 5), quantas=16,
             piso=2),
        dict(grupo=["rachadura h", "cascalho", "cascalho hv", "pedra gasta",
                    "pedra gasta v", "liquen h", "liquen v"], tam=(2, 5),
             quantas=16, piso=2),
        dict(grupo=["junta de laje h", "pedra polida", "pedra cruzada",
                    "poca de agua", "poca de agua h"], tam=(2, 5), quantas=16,
             piso=2),
        dict(grupo=["junta rachada", "pedra manchada h", "pedra manchada v",
                    "pedra de cabeca", "rachadura v"], tam=(2, 5), quantas=16,
             piso=2),
    ],
)


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair identico em qualquer maquina e em qualquer versao de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


# ------------------------------------------------------------ leitura do nosso
def _ler(nome):
    return open(f"{DESTINO}/{nome}", "rb").read()


def _entradas(bin_meta, local):
    """As oito entradas de um metatile do arquivo, ou None se ele nem existe.

    Devolver None em vez de estourar importa: o `--demo` roda ANTES do primeiro
    `--aplicar`, quando o `metatiles.bin` do disco ainda tem 254 metatiles e o
    kit pergunta pelo 254.
    """
    if (local + 1) * 16 > len(bin_meta):
        return None
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

    A pergunta nao e "o indice de tile e zero": o tile 1 do primario existe e nao
    tem um pixel aceso, e contar por indice diria que um chao chapado desenha por
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


def tiles_pedidos():
    """Os tiles LOCAIS que algum metatile ANTERIOR a esta passada referencia.

    E a segunda das duas contas diretas que substituem a prova de mapa irmao:
    tile novo so pode cair em vaga que ninguem pede. Medido nesta arvore: o maior
    e o 327, e o `tiles.png` tem 336.

    O CORTE EM `META_LOCAL_0` NAO E DETALHE, e a falta dele quebrou a
    idempotencia na primeira versao: depois de um `--aplicar`, os metatiles que
    ESTA passada escreveu (locais 254 em diante) ja apontam para as vagas 336 em
    diante, e sem o corte o portao acusava o proprio kit de invadir vaga pedida,
    na segunda rodada. O que o portao quer saber e sobre o tileset ANTIGO.
    """
    import render_maps as RM
    ts = _tileset(SECUNDARIO)
    pedidos = set()
    for loc in range(min(META_LOCAL_0, len(ts["metatiles"]) // 16)):
        for (it, _fh, _fv, _ip) in RM.entradas_metatile(ts["metatiles"], loc):
            if it >= 512:
                pedidos.add(it - 512)
    return pedidos


# ------------------------------------------------------------------- o DESENHO
def _tile(t, fh=0, fv=0, tp=None, ts=None):
    """Os 8x8 indices de cor de um tile NOSSO, ja espelhado."""
    import render_maps as RM
    tp = tp or _tileset(PRIMARIO)
    ts = ts or _tileset(SECUNDARIO)
    g = [linha[:] for linha in RM.resolver_tile(tp, ts, t)]
    if fh:
        g = [linha[::-1] for linha in g]
    if fv:
        g = g[::-1]
    return g


def grade16(quads, tp=None, ts=None):
    """Os 16x16 indices de cor de um arranjo de quatro quadrantes."""
    g = [[0] * 16 for _ in range(16)]
    for k, (t, fh, fv) in enumerate(quads):
        tl = _tile(t, fh, fv, tp, ts)
        qx, qy = k % 2, k // 2
        for y in range(8):
            for x in range(8):
                g[qy * 8 + y][qx * 8 + x] = tl[y][x]
    return g


def pinta(g, mascara):
    """A grade com a mascara de detalhe por cima."""
    fora = [linha[:] for linha in g]
    if len(mascara) != 16 or any(len(l) != 16 for l in mascara):
        raise SystemExit("mascara de detalhe nao e 16x16")
    for y, linha in enumerate(mascara):
        for x, ch in enumerate(linha):
            if ch not in COD:
                raise SystemExit("caractere %r fora do dicionario COD" % ch)
            if COD[ch] is not None:
                fora[y][x] = COD[ch]
    return fora


def espelha16(g, como):
    fora = [linha[:] for linha in g]
    if "h" in como:
        fora = [linha[::-1] for linha in fora]
    if "v" in como:
        fora = fora[::-1]
    return fora


def _quadrantes(g):
    """Os quatro 8x8 de uma grade 16x16, na ordem dos quadrantes."""
    return [[[g[(k // 2) * 8 + y][(k % 2) * 8 + x] for x in range(8)]
             for y in range(8)] for k in range(4)]


def _flips(tile):
    """As quatro leituras de um 8x8: (fh, fv, conteudo)."""
    for fh in (0, 1):
        for fv in (0, 1):
            g = [linha[::-1] for linha in tile] if fh else [l[:] for l in tile]
            if fv:
                g = g[::-1]
            yield fh, fv, g


# ------------------------------------------------------------------- as CONTAS
def px_metatile(ents, tp, ts, tiles_novos=None):
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
            vaga = idx - len(tp["tiles"])
            if tiles_novos and vaga in tiles_novos:
                tile = tiles_novos[vaga]
            else:
                tile = RM.resolver_tile(tp, ts, idx)
            if tile is None:
                continue
            cores = (tp if ip < 6 else ts)["paletas"].get(ip)
            if cores is None:
                continue
            RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                             [tuple(c) for c in cores],
                             bool(val & 0x400), bool(val & 0x800))
    return list(im.getdata())


def _dist_pixels(a, b):
    return sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
               for p, q in zip(a, b)) / 256.0


def _cor_media(px):
    return tuple(sum(c[k] for c in px) / 256.0 for k in range(3))


def _dist_cor(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


# ---------------------------------------------------------------------- o KIT
def _locais_livres():
    return list(range(META_LOCAL_0, TETO_META))


def _vagas_de_tile():
    """As vagas de TILE livres, em ordem, PULANDO os 96 pinos da agua agitada."""
    return [v for v in range(TILE_LOCAL_0, TETO_TILES) if v not in PINOS_ANIM]


def desenha_kit():
    """(tiles_novos, metas, attrs, catalogo), sem escrever em disco."""
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    n_pri = len(tp["tiles"])

    tiles_novos = {}
    vagas_tile = _vagas_de_tile()
    metas, attrs = {}, {}
    vagas_meta = _locais_livres()
    proximo_meta = [0]
    catalogo = dict(chao={}, moveis={})

    # Os tiles do primario que PODEM ser reusados: os que esta passada ja conhece
    # por nome mais qualquer um do primario. Reusar de graca e sempre melhor que
    # gastar vaga, e o espelho e de graca tambem.
    conhecidos = []
    for t in sorted(set(BASE_TILES + [52, 53, 72, 73])):
        conhecidos.append((t, _tile(t, 0, 0, tp, ts)))

    def acha_tile(alvo):
        """(indice global, fh, fv) de um 8x8, reusando o que ja existe."""
        for t, base in conhecidos:
            for fh, fv, g in _flips(base):
                if g == alvo:
                    return t, fh, fv
        for vaga, base in tiles_novos.items():
            for fh, fv, g in _flips(base):
                if g == alvo:
                    return n_pri + vaga, fh, fv
        if len(tiles_novos) >= len(vagas_tile):
            raise SystemExit("acabaram as vagas de tile livres")
        vaga = vagas_tile[len(tiles_novos)]
        tiles_novos[vaga] = [linha[:] for linha in alvo]
        return n_pri + vaga, 0, 0

    def poe(ents, attr):
        if proximo_meta[0] >= len(vagas_meta):
            raise SystemExit("acabaram as vagas de metatile livres")
        local = vagas_meta[proximo_meta[0]]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return 512 + local

    def entradas_de(g):
        """As quatro entradas de 16 bits da camada de baixo de uma grade 16x16."""
        fora = []
        for tile in _quadrantes(g):
            idx, fh, fv = acha_tile(tile)
            fora.append(((0x400 if fh else 0) | (0x800 if fv else 0) | idx
                         | (PAL_PEDRA << 12)))
        return fora

    # O CARIMBO DUPLICA a camada de baixo na de cima, e isso NAO e enfeite: em
    # `METATILE_LAYER_TYPE_COVERED` a camada de baixo vai para o BG3 e a de cima
    # para o BG2, as duas ABAIXO do sprite. Pedra em cima de pedra da o mesmo
    # pixel, e as variantes copiam a estrutura do carimbo em vez de deixar a
    # camada de cima vazia, porque assim o metatile novo e do MESMO formato que o
    # velho e nao depende de o tile 0 do primario continuar em branco.
    ents_car = ents_nossas(CARIMBO, tp, ts)
    if ents_car[4:] != ents_car[:4]:
        raise SystemExit("o carimbo nao duplica a camada de baixo: %s"
                         % [hex(x) for x in ents_car])
    if attr_nosso(CARIMBO) != ATTR_CARIMBO:
        raise SystemExit("o carimbo tem atributo 0x%04X e nao 0x%04X"
                         % (attr_nosso(CARIMBO), ATTR_CARIMBO))
    px_carimbo = px_metatile(ents_car, tp, ts)

    # ------------------------------------------------------- 1. CHÃO sem detalhe
    for c in CHAO_LIMPO:
        g = grade16(ARRANJOS[c["arranjo"]], tp, ts)
        quads = entradas_de(g)
        catalogo["chao"][c["nome"]] = poe(quads + list(quads), ATTR_CARIMBO)

    # -------------------------------------------------------- 2. CHÃO com detalhe
    for nome, (arranjo, mascara) in DETALHES.items():
        base = pinta(grade16(ARRANJOS[arranjo], tp, ts), mascara)
        for como in ORIENTACOES[nome]:
            g = espelha16(base, como)
            quads = entradas_de(g)
            rotulo = nome if not como else "%s %s" % (nome, como)
            catalogo["chao"][rotulo] = poe(quads + list(quads), ATTR_CARIMBO)

    # -------------------------------------------- 3. MÓVEIS de uma célula, NOSSOS
    base_pedra = ents_car[:4]
    for m in MOVEIS:
        e = ents_nossas(m["mt"], tp, ts)
        cima = list(e[4:])
        # QUADRANTE DE BAIXO SOBE quando o de cima esta vazio.
        if not arte_em_cima(e, tp, ts):
            cima = list(e[:4])
        if not any(v & 0x3FF for v in cima):
            raise SystemExit("%s: o metatile %d nao tem arte" % (m["nome"],
                                                                m["mt"]))
        catalogo["moveis"][m["nome"]] = poe(list(base_pedra) + cima, ATTR_CARIMBO)

    # ------------------------------------------------------------- os PORTÕES
    for nome, gid in catalogo["chao"].items():
        d = _dist_cor(_cor_media(px_metatile(metas[gid - 512], tp, ts,
                                             tiles_novos)),
                      _cor_media(px_carimbo))
        if d > TETO_COR:
            raise SystemExit("o chao %s esta a %.1f de cor do carimbo, acima do "
                             "teto de %.1f" % (nome, d, TETO_COR))
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles" % TETO_TILES)
    for vaga in tiles_novos:
        if vaga in PINOS_ANIM:
            raise SystemExit("o kit grava na vaga de tile %d, que e pino da agua "
                             "agitada" % vaga)
    pedidos = tiles_pedidos()
    for vaga in tiles_novos:
        if vaga in pedidos:
            raise SystemExit("o kit grava na vaga de tile %d, que algum metatile "
                             "do tileset ja pede" % vaga)
    # A vaga de metatile so serve se o mapa nao usar o id. A grade do ALVO entra
    # pela base LIMPA desta passada, e nao pelo disco: depois de um `--aplicar` o
    # disco ja tem os ids que este kit acabou de escrever, e o portao reprovaria a
    # si mesmo na segunda rodada.
    guardado = carrega_plano()
    usados = set()
    for nome in IRMAOS:
        grade = base_de(nome, guardado) if nome == ALVO else G.grade(nome)[4]
        usados |= {c & 0x3FF for c in grade}
    for local in metas:
        if 512 + local in usados:
            raise SystemExit("o mapa usa o metatile %d" % (512 + local))
    return tiles_novos, metas, attrs, catalogo


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, metatiles.bin e metatile_attributes.bin.

    NENHUMA PALETA E ESCRITA, e isso e a regra e nao um esquecimento: toda a arte
    desta passada e pintada com indices que a vaga 7 ja tem.

    Idempotente: as vagas de tile e de metatile sao FIXAS.

    A ARMADILHA DO `Image.convert("P")`: numa imagem que JA e "P" ele devolve uma
    COPIA e nao converte, e uma frente desta onda gravou metatiles e NENHUM tile
    por causa disso. Aqui a imagem nova nasce em "P" e recebe a paleta da antiga.
    """
    from PIL import Image
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    alvo = max((max(tiles_novos) + 1) if tiles_novos else 0,
               (antigo.size[1] // 8) * cols)
    linhas = (alvo + cols - 1) // cols
    novo = Image.new("P", (antigo.size[0], linhas * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    px = novo.load()
    for v, tile in tiles_novos.items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    novo.save(f"{DESTINO}/tiles.png")

    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    falta = (max(metas) + 1) * 16 - len(meta) if metas else 0
    if falta > 0:
        meta += bytes(falta)
        attr += bytes((max(metas) + 1) * 2 - len(attr))
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------ o ESPALHAMENTO
def bolhas(livres, spec, semente=0x5EED):
    """[(nomes, {celulas})], bolhas organicas crescidas por frente de onda.

    A SEMENTE nao e sorteio solto: as celulas livres sao ordenadas por um hash da
    posicao e a semente so e aceita a pelo menos 2 (Chebyshev) de toda semente ja
    aceita. O CRESCIMENTO e guloso com ruido: a cada passo entra a celula da
    frente de onda com o menor hash. Circulo daria bolha redonda e xadrez daria
    sal e pimenta; frente de onda com ruido da contorno irregular.

    A ORDEM E POR RODADA, e nao por especificacao inteira: servindo UMA bolha por
    especificacao a cada rodada, o que falta no fim e o excedente de todo mundo, e
    nao a lista inteira de quem estava no fim da fila.
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
                # ACEITA A BOLHA CURTA quando foi a REGIAO que acabou, e nao a
                # vontade de crescer. Em Sootopolis isso e a regra e nao a
                # excecao: o terraco anda em faixas de 2 a 6 celulas, e exigir
                # tamanho cheio deixaria o labirinto inteiro liso.
                if len(corpo) < lo and (frente or len(corpo) < esp.get("piso", PISO_BOLHA)):
                    continue
                achou = (p, corpo)
                break
            if achou is None:
                feitas[k] = esp["quantas"]     # nao ha mais lugar para esta
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


MULTI_NIVEL = 15        # ELEVATION_MULTI_LEVEL: casa com QUALQUER elevacao


def corredores_multinivel(v, W, H, d):
    """Os corredores da suite, refeitos com a regra da ELEVACAO 15.

    O `enfeita_cidades.corredores_de_teste` congela as celulas que a suite anda
    dentro do mapa e simula a caminhada com a regra "elevacao 0 e curinga e o
    resto exige igualdade". Essa regra ignora a elevacao 15
    (`ELEVATION_MULTI_LEVEL`), que MANTEM a elevacao do jogador. As elevacoes de
    Sootopolis sao 0, 1 e 3 (medido), entao aqui as duas contas coincidem, e e por
    isso mesmo que as DUAS rodam: a uniao e barata e nao depende de a medida
    continuar valendo depois que outra frente mexer no mapa.
    """
    import glob
    import re as _re
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = "MAP_" + _re.sub(r"(?<!^)(?=[A-Z])", "_",
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
        if os.path.basename(arq) == BLOCO_PROPRIO:
            continue   # o bloco desta rodada e derivado DO desenho, nao o contrario
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


def peca_da_mancha(nomes, x, y):
    """Qual das pecas do grupo cai nesta celula. Hash da posicao, nao paridade:
    paridade vira xadrez e o auto-teste reprova."""
    return nomes[_mistura(x, y, 0xA5A5 + len(nomes)) % len(nomes)]


# ----------------------------------------------------------- ligacao a pe
def componentes(v, W, H):
    """{celula: rotulo} dos pedacos de chao andavel ligados a pe.

    POR QUE NAO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda e
    alcancavel a partir de algum ponto de partida", e fechar um corredor com warp
    dos dois lados nao tira NENHUMA celula do alcance e mesmo assim parte a cidade
    em duas. Em Sootopolis, que tem treze warps, isso e o portao que importa.
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
def plano_mapa(catalogo, base=None):
    """(L, W, H, v, escritas, contas) para `SootopolisCity`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    # A FAMILIA de chao. Uma celula so e elegivel se ainda for o carimbo puro, se
    # estiver na elevacao 3 e se nao for AGUA para o motor. O filtro de agua e o
    # que protege o lago: nenhuma celula de superficie de Surf entra no catalogo.
    fam = {(i % W, i // W) for i in range(W * H)
           if not ((v[i] >> 10) & 3) and (v[i] & 0x3FF) == CARIMBO
           and ((v[i] >> 12) & 0xF) in ELEVACOES
           and beh(v[i] & 0x3FF) not in AG}

    escritas = {}
    # DOIS GELOS, e a diferenca custou metade da regua em Dewford. O
    # `enfeita_cidades.congelado` devolve a celula de todo evento MAIS um anel de
    # uma celula em volta, e isso existe para o objeto SOLIDO: peca nova encostada
    # numa porta ou num NPC tranca gente. Repintar o CHAO nao tranca nada: a
    # colisao, a elevacao e o par (comportamento, layerType) continuam identicos
    # por construcao.
    #
    # `gelo_solido` (evento + anel + corredor da suite) manda no MOVEL.
    # `gelo` (so o corredor da suite e o que ESTA passada ja escreveu) manda na
    # MANCHA.
    ev, halo = E.congelado(d)
    gelo = E.corredores_de_teste(ALVO, v, W, H, d)
    gelo |= corredores_multinivel(v, W, H, d)
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))
    gelo_solido = gelo | halo

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
        if (x, y) in gelo_solido or i in escritas or (x, y) not in fam:
            return False
        return (aplicado[i] & 0x3FF) == CARIMBO

    def espacado(nome, esp, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < esp
                       for px, py in por_movel[nome])

    def encostado(x, y):
        """MOVEL DE CRATERA ENCOSTA EM ALGUMA COISA: num solido, na agua ou na
        borda do mapa. Pedra solta no meio da passarela le como erro de mapa.

        O ANEL E O DE OITO, e nao o de quatro: a peca encostada na DIAGONAL de um
        paredao continua encostada aos olhos de quem joga.
        """
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if not dx and not dy:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    return True      # a borda do mapa tambem e encosto
                j = ny * W + nx
                if (aplicado[j] >> 10) & 3:
                    return True
                if beh(aplicado[j] & 0x3FF) in AG:
                    return True
        return False

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portoes deixarem. O portao
        roda NA HORA e nao so no fim."""
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

    # ------ 1. MOVEIS de uma celula. Eles vem ANTES da mancha de proposito:
    # movel posto no carimbo tira uma celula do numerador E do denominador da
    # regua; movel posto em cima de uma mancha tira so do denominador, o que
    # PIORA a conta.
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(MOVEIS)
        for k in range(len(MOVEIS)):
            m = MOVEIS[(giro + k) % len(MOVEIS)]
            if conta_mov[m["nome"]] >= m["quantos"]:
                continue
            if not livre(x, y) or not espacado(m["nome"], m["espaco"], x, y):
                continue
            if not encostado(x, y):
                continue
            if not tenta_solidificar(x, y, catalogo["moveis"][m["nome"]]):
                continue
            por_movel[m["nome"]].append((x, y))
            conta_mov[m["nome"]] += 1
            break

    # ------------------------------------------------------------- 2. MANCHA
    conta_mancha = collections.Counter()

    def pintavel(p):
        i = p[1] * W + p[0]
        return (p in fam and i not in escritas and p not in gelo
                and (aplicado[i] & 0x3FF) == CARIMBO)

    def poe_mancha(p, nomes):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | catalogo["chao"][nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    for chave, semente in (("bolhas1", 0x5EED), ("bolhas2", 0xB0A7),
                           ("bolhas3", 0x5EED ^ 0x1234)):
        livres = {p for p in fam if pintavel(p)}
        for nomes, corpo in bolhas(livres, TEMA[chave], semente):
            for p in sorted(corpo):
                poe_mancha(p, nomes)

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
    contas = dict(moveis=dict(conta_mov), manchas=dict(conta_mancha),
                  solidos=len(novos_solidos), pedra=len(fam))
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

    Sem isso a idempotencia morre: planejar sobre um mapa ja desenhado nao volta
    ao mesmo lugar.
    """
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar, so_tileset=False):
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    if tiles_novos:
        print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
              "novos (locais %d a %d, ids %d a %d)"
              % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
                 TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
                 max(metas), 512 + min(metas), 512 + max(metas)))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
        if so_tileset:
            print("so o tileset")
            return 0
    guardado = carrega_plano()
    base = base_de(ALVO, guardado)
    L, W, H, v, escritas, contas = plano_mapa(catalogo, base)
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("%s: %d celulas de mancha, %d solidificadas, %d mudadas (o carimbo "
          "tinha %d celulas)"
          % (ALVO, sum(contas["manchas"].values()), contas["solidos"],
             len(escritas), contas["pedra"]))
    print("  mancha: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["manchas"].items())))
    print("  movel:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    print("  regua: carimbo %d com %.1f%% de %d celulas ANTES; carimbo %d com "
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


# ------------------------------------------------------------------ conferência
def confere(tiles_novos, metas, attrs, catalogo, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela e chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que tem
    que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa certa.
    Regra conferida so no caminho feliz nao e regra.
    """
    mau = []
    import render_maps as RM
    tp = _tileset(PRIMARIO)
    ts = _tileset(SECUNDARIO)
    ap = G._attrs(PRIMARIO)
    asec = G._attrs(SECUNDARIO)

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
        return px_metatile(entradas(mt_id), tp, ts, tiles_novos)

    def opacos_de_cima(gid):
        op = 0
        for e in entradas(gid)[4:]:
            if e & 0x3FF:
                vaga = (e & 0x3FF) - len(tp["tiles"])
                if vaga in tiles_novos:
                    op += _opacos(tiles_novos[vaga])
                else:
                    t = RM.resolver_tile(tp, ts, e & 0x3FF)
                    op += _opacos(t) if t else 0
        return op

    # ------------------------------------------------------------ 1. orçamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if tiles_novos and min(tiles_novos) < TILE_LOCAL_0:
        mau.append("o kit grava tile abaixo da primeira vaga livre (%d)"
                   % TILE_LOCAL_0)
    if set(tiles_novos) & PINOS_ANIM:
        mau.append("o kit grava na vaga de tile pinada pela agua agitada")
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    if metas and min(metas) < META_LOCAL_0:
        mau.append("o kit grava metatile abaixo da primeira vaga livre (%d)"
                   % META_LOCAL_0)

    # ---------- 2. as DUAS contas diretas que substituem a prova de mapa irmao.
    # (a) nenhum tile novo cai em vaga que algum metatile do tileset ja pede;
    # (b) nenhuma cor e escrita, ou seja nenhum pixel VIVO muda de cor.
    pedidos = tiles_pedidos()
    for vaga in tiles_novos:
        if vaga in pedidos:
            mau.append("o tile novo da vaga %d cai numa vaga que algum metatile "
                       "do tileset ja pede" % vaga)
    for ip in range(13):
        arq = f"{DESTINO}/palettes/%02d.pal" % ip
        if not os.path.exists(arq):
            continue
        linhas = [l.split() for l in open(arq).read().split("\n")[3:] if l.strip()]
        disco = [tuple(int(z) for z in c) for c in linhas[:16]]
        atual = [tuple(c) for c in ts["paletas"].get(ip, disco)]
        if disco != atual:
            mau.append("a paleta %d do disco nao e a que o render le" % ip)
    for gid in sorted(set(catalogo["chao"].values())
                      | set(catalogo["moveis"].values())):
        for e in entradas(gid):
            if (e & 0x3FF) and ((e >> 12) & 0xF) not in (PAL_PEDRA,) \
               and gid not in catalogo["moveis"].values():
                mau.append("o chao %d pinta com a vaga de paleta %d, e esta "
                           "passada so pinta com a %d"
                           % (gid, (e >> 12) & 0xF, PAL_PEDRA))
                break

    # ---------- 3. CHÃO: atributo idêntico ao do carimbo, camada de cima
    # DUPLICANDO a de baixo (como o carimbo faz) e cor a menos de TETO_COR
    px_carimbo = px_de(CARIMBO)
    for nome, gid in catalogo["chao"].items():
        if atributo(gid) != ATTR_CARIMBO:
            mau.append("o chao %s (%d) tem atributo 0x%04X e o carimbo tem "
                       "0x%04X" % (nome, gid, atributo(gid), ATTR_CARIMBO))
        e = entradas(gid)
        if e[4:] != e[:4]:
            mau.append("o chao %s (%d) nao duplica a camada de baixo na de cima, "
                       "como o carimbo faz" % (nome, gid))
        if opacos_de_cima(gid) != 4 * 64:
            mau.append("o chao %s (%d) tem camada com buraco: o BG3 apareceria"
                       % (nome, gid))
        dc = _dist_cor(_cor_media(px_de(gid)), _cor_media(px_carimbo))
        if dc > TETO_COR:
            mau.append("o chao %s (%d) esta a %.1f de cor do carimbo, acima do "
                       "teto de %.1f" % (nome, gid, dc, TETO_COR))

    # ---------- 4. MÓVEL: COVERED, comportamento zerado, e o NOSSO chão entrada
    # por entrada na camada de baixo
    base_pedra = ents_nossas(CARIMBO, tp, ts)[:4]
    for nome, gid in catalogo["moveis"].items():
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o movel %s (%d) nao esta em COVERED" % (nome, gid))
        if a & 0xFF:
            mau.append("o movel %s (%d) importou comportamento 0x%02X"
                       % (nome, gid, a & 0xFF))
        if entradas(gid)[:4] != list(base_pedra):
            mau.append("o movel %s (%d) nao tem o nosso chao de pedra na camada "
                       "de baixo" % (nome, gid))
        if opacos_de_cima(gid) == 0:
            mau.append("o movel %s (%d) esta sem arte em cima" % (nome, gid))

    # ---------- 5. nenhuma variante de chão e copia pixel a pixel de outra
    lista = list(catalogo["chao"].values()) + [CARIMBO]
    pix = {mt: px_de(mt) for mt in lista}
    for i, a in enumerate(lista):
        for b in lista[i + 1:]:
            dd = _dist_pixels(pix[a], pix[b])
            if dd < PISO_VARIANTE:
                mau.append("as variantes de chao %d e %d tem distancia %.1f, "
                           "abaixo do piso de %.1f do varia_carimbo.py: isso e "
                           "enganar a regua" % (a, b, dd, PISO_VARIANTE))

    # ---------------------------------------- 6 a 12. o plano, célula a célula
    L, W, H, v, escritas, contas = plano
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    meus_chaos = {g: n for n, g in catalogo["chao"].items()}
    meus_moveis = {g: n for n, g in catalogo["moveis"].items()}

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVACAO em (%d,%d)" % (ALVO, x, y))
        if cv and not cn:
            mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                       % (ALVO, x, y))
        if novo in meus_chaos:
            if cn != cv or velho != CARIMBO:
                mau.append("%s: chao em celula errada em (%d,%d)" % (ALVO, x, y))
        elif novo in meus_moveis:
            if cv or not cn:
                mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                           % (ALVO, x, y))
            if velho != CARIMBO:
                mau.append("%s: movel fora do carimbo em (%d,%d)" % (ALVO, x, y))
            if (x, y) in ev:
                mau.append("%s: movel em cima do evento (%d,%d)" % (ALVO, x, y))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                       % (ALVO, novo, x, y))
        if (v[i] >> 12) & 0xF not in ELEVACOES:
            mau.append("%s: (%d,%d) tem elevacao fora da lista da familia"
                       % (ALVO, x, y))

    # 7. (comportamento, layerType) de toda célula ANDÁVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                       "layerType)" % (ALVO, i % W, i // W))
            break

    # 8 e 9. alcance a pe e LIGACAO a pe
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
            ligacao_intacta(componentes(v, W, H), componentes(saida, W, H), solid)]

    # 10. O LAGO: nenhuma celula de AGUA foi escrita, e o conjunto de celulas de
    # agua e IDENTICO antes e depois. E este o portao que garante que o alcance
    # de Surf nao mudou.
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    def agua_de(grade):
        return {(i % W, i // W) for i in range(W * H)
                if beh(grade[i] & 0x3FF) in AG}
    if agua_de(v) != agua_de(saida):
        mau.append("%s: o conjunto de celulas de AGUA mudou, e com ele o alcance "
                   "de Surf" % ALVO)

    # 11. A MANCHA NÃO PODE SER ADIVINHAVEL, e o teste tem dois lados.
    # (a) PADRAO: nenhuma projecao simples da posicao pode ADIVINHAR a peca.
    # (b) FORMA: mancha e BOLHA, nao sal e pimenta, e a conta e o TAMANHO MEDIO
    # do pedaco conexo.
    mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
              if (val & 0x3FF) in meus_chaos}
    if len(mancha) < PISO_MANCHA:
        mau.append("%s: so %d celulas de mancha" % (ALVO, len(mancha)))
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
                    mau.append("%s: saber %s mod %d adivinha a peca em %.0f%% das "
                               "celulas contra %.0f%% do chute cego: virou padrao"
                               % (ALVO, rot, mod, 100 * ac, 100 * cego))
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
        if len(mancha) / pedacos < 4.0:
            mau.append("%s: a mancha media tem so %.1f celulas (%d em %d "
                       "pedacos): virou sal e pimenta, nao bolha"
                       % (ALVO, len(mancha) / pedacos, len(mancha), pedacos))

    # 12. a regua tem que fechar em 20% ou menos
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                   % (ALVO, b))
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferenca" so vale depois que a comparacao mostra que sabe reprovar.
    """
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    guardado = carrega_plano()
    plano = plano_mapa(catalogo, base_de(ALVO, guardado))

    mau = confere(tiles_novos, metas, attrs, catalogo, plano)
    negativas = []

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = confere(*args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NAO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    def copia():
        L, W, H, v, esc, ct = plano
        return (dict(tiles_novos), {k: list(x) for k, x in metas.items()},
                dict(attrs), json.loads(json.dumps(catalogo)),
                (L, W, H, list(v), dict(esc), ct))

    algum_chao = sorted(catalogo["chao"])[0]
    outro_chao = sorted(catalogo["chao"])[1]
    algum_movel = MOVEIS[0]["nome"]

    # N1. colisão 1 -> 0 numa célula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a celula ERA solida
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. atributo de um metatile de CHÃO sabotado
    def n3():
        a = copia()
        gid = a[3]["chao"][algum_chao]
        a[2][gid - 512] = (a[2][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chao sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = a[3]["moveis"][algum_movel]
        a[2][gid - 512] = a[2][gid - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no movel", n4, "nao esta em COVERED")

    # N5. comportamento inventado num móvel
    def n5():
        a = copia()
        gid = a[3]["moveis"][MOVEIS[1]["nome"]]
        a[2][gid - 512] = a[2][gid - 512] | 0x02
        return a
    sabota("comportamento inventado", n5, "importou comportamento")

    # N6. móvel SEM o nosso chão embaixo
    def n6():
        a = copia()
        gid = a[3]["moveis"][algum_movel]
        e = list(a[1][gid - 512])
        e[0] = 0x5000 | 300
        a[1][gid - 512] = e
        return a
    sabota("chao trocado no movel", n6, "nao tem o nosso chao")

    # N7. um chão com BURACO na camada: em COVERED o BG3 apareceria
    def n7():
        a = copia()
        gid = a[3]["chao"][algum_chao]
        e = list(a[1][gid - 512])
        e[0] = 0
        e[4] = 0
        a[1][gid - 512] = e
        return a
    sabota("chao com buraco", n7, "camada com buraco")

    # N8. célula andável com (comportamento, layerType) trocado
    def n8():
        a = copia()
        gid = a[3]["chao"][outro_chao]
        a[2][gid - 512] = 0x0021          # NORMAL onde o carimbo e COVERED
        return a
    sabota("layerType de chao trocado", n8, "mudou (comportamento")

    # N9. um móvel plantado em cima de célula de EVENTO
    def n9():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
        gid = a[3]["moveis"][algum_movel]
        for x, y in sorted(E.eventos(d)):
            i = y * W + x
            if (v[i] & 0x3FF) == CARIMBO and not ((v[i] >> 10) & 3):
                esc[i] = (v[i] & 0xF000) | (1 << 10) | gid
                return a
        raise SystemExit("nao ha evento em cima do carimbo para sabotar")
    sabota("movel em cima de evento", n9, "em cima do evento")

    # N10. a mancha espalhada AO ACASO, com as mesmas células
    def n10():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        meus = set(catalogo["chao"].values())
        cels = [i for i in esc if (esc[i] & 0x3FF) in meus]
        livres = [i for i in range(W * H)
                  if (v[i] & 0x3FF) == CARIMBO and not ((v[i] >> 10) & 3)
                  and i not in esc]
        livres.sort(key=lambda i: _mistura(i, 0xDEAD))
        valores = [esc[i] & 0x3FF for i in cels]
        for i in cels:
            del esc[i]
        for k, val in enumerate(valores):
            if k < len(livres):
                esc[livres[k]] = (v[livres[k]] & 0xFC00) | val
        return a
    sabota("mancha espalhada ao acaso", n10, "sal e pimenta")

    # N11. duas variantes de chão IGUAIS pixel a pixel: e enganar a regua
    def n11():
        a = copia()
        gid_a = a[3]["chao"][algum_chao]
        gid_b = a[3]["chao"][outro_chao]
        a[1][gid_b - 512] = list(a[1][gid_a - 512])
        return a
    sabota("variante de chao duplicada", n11, "abaixo do piso de")

    # N12. gravar numa vaga de metatile que o mapa usa
    def n12():
        a = copia()
        a[1][100] = list(a[1][min(a[1])])
        a[2][100] = ATTR_CARIMBO
        a[3]["chao"][algum_chao] = 512 + 100
        return a
    sabota("grava em vaga de metatile viva", n12, "abaixo da primeira vaga livre")

    # N13. gravar tile numa das 96 vagas pinadas pela agua agitada
    def n13():
        a = copia()
        a[0][240] = [[0] * 8 for _ in range(8)]
        return a
    sabota("tile na vaga da agua agitada", n13, "pinada pela agua agitada")

    # N14. gravar tile numa vaga que algum metatile do tileset JA PEDE. E a
    # segunda das duas contas diretas que substituem a prova de mapa irmao, e ela
    # so vale se souber reprovar.
    def n14():
        a = copia()
        pedidos = sorted(tiles_pedidos())
        a[0][pedidos[-1]] = [[0] * 8 for _ in range(8)]
        return a
    sabota("tile em vaga que um metatile pede", n14, "ja pede")

    # N15. mexer numa celula de AGUA: o alcance de Surf mudaria
    def n15():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        AG = E.agua()
        gid = a[3]["chao"][algum_chao]
        for i in range(W * H):
            if beh(v[i] & 0x3FF) in AG:
                esc[i] = (v[i] & 0xFC00) | gid
                return a
        raise SystemExit("o mapa nao tem celula de agua para sabotar")
    sabota("celula de agua trocada", n15, "alcance de Surf")

    # ------------------------------------------------ o que está NO DISCO
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.load()

    postas = [l for l in metas if _entradas(meta_disco, l) == metas[l]]
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
            if (local + 1) * 2 > len(attr_disco) or \
               struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            if (vaga // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga)

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
        mau.append("%s: desfazer nao devolve a base" % ALVO)
    _, _, _, _, esc2, _ = plano_mapa(catalogo, volta)
    if esc2 != escritas:
        mau.append("%s: segunda passada deu plano diferente" % ALVO)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE")
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("  %-16s %d celulas mudadas, %d solidificadas, regua %.1f%% -> %.1f%%"
          % (ALVO, len(escritas), contas["solidos"], a, b))
    print("  %d tiles, %d metatiles, %d provas negativas:"
          % (len(tiles_novos), len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-36s -> %s" % (nome, queixa[:92]))
    return 0


def main():
    if "--desfazer" in sys.argv:
        return desfaz()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    return roda("--aplicar" in sys.argv or "--so-tileset" in sys.argv,
                "--so-tileset" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
