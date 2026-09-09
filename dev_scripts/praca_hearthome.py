#!/usr/bin/env python3
"""Refino de `HearthomeCity` (tema PRAÇA E CALÇAMENTO) no `gTileset_Hearthome`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: `HearthomeCity` gasta 26,9% do chão andável a pé
(368 células de 1.368) com UM metatile, o 521, o tijolo bege do SECUNDÁRIO; o
segundo, a laje branca 545, come mais 254 (18,6%), e os três mais comuns somam
56,9%. É a cidade do Contest e da catedral, o mapa mais movimentado do cartucho,
e o chão dela são dois tapetes lisos costurados: tijolo bege nas bordas e nos
dois quarteirões do sul, laje branca no meio. Nem um banco, nem uma grade, nem
um canteiro plantado no calçamento.

O QUE FICOU DIFERENTE DAS CIDADES ANTERIORES DESTA ONDA, e é preciso dizer isto
em voz alta em vez de fingir que a prova existe: `gTileset_Hearthome` é
secundário de UM layout só, o `LAYOUT_HEARTHOME_CITY`, e de um mapa só, o
próprio `HearthomeCity` (medido nesta árvore lendo `data/layouts/layouts.json` e
todo `data/maps/*/map.json`). Portanto NÃO existe aqui a prova de "zero pixel de
diferença no mapa irmão" que Pastoria e Sunyshore puderam dar: não há mapa
irmão. A prova de que este kit não estraga desenho de terceiro é outra, e é
menos forte por construção: nenhuma cor é escrita num índice de paleta que algum
pixel VIVO deste tileset use, e nenhum tile é escrito numa vaga que alguma
entrada de algum metatile do `metatiles.bin` peça. As duas contas estão em
`vagas_pal_livres()` e `vagas_tile_livres()` e saem impressas na rodagem.

A SEGUNDA CORREÇÃO AO BRIEFING, também medida e também dita em voz alta: o
briefing desta frente afirma que "as SEIS vagas de secundário (7 a 12) estão
TODAS em uso" e que "não há vaga de paleta livre". Não é o caso. As vagas de
secundário deste tileset são SETE, de 6 a 12, e a vaga 6 está INTEIRA livre:
nenhuma das 8 entradas de nenhum dos 512 metatiles do `metatiles.bin` pinta com
ela (a contagem por vaga está em `--medir`). É nela que este kit escreve, e por
isso o `dev_scripts/compacta_paletas.py`, que o briefing autorizava como último
recurso, NÃO foi rodado: ele não era necessário e o próprio briefing avisa que
ele erra em tileset com tile compartilhado por duas paletas.

O CHÃO NOVO NÃO É IMPORTADO, E A RAZÃO É COR MEDIDA, não economia. A folha de
contato dos três pares candidatos do `Pokemon Light Platinum` (os atlas
`lp-0x286DB4-metropole-atlas.png`, `lp-0x286D24-bairro-atlas.png` e
`lp-0x286E14-mato-atlas.png`, que a frente de Jubilife já tinha desenhado) foi
olhada de novo, e o calçamento de praça do par de metrópole `0x286DB4`, que é o
único desenhado em sistema nas três, é cinza AZULADO: (136,152,184),
(112,136,160), (104,128,152), (80,88,120), (168,192,216). O chão de Hearthome
não é dessa família. A média RGB do tijolo 521 é (213,180,106) e a da laje 545 é
(236,236,236); a peça de calçamento mais próxima do hack fica a 78,0 do tijolo e
a 83,4 da laje, e o critério duro desta onda é 50. Em Jubilife esse mesmo
calçamento entrou porque LÁ a cidade já era cinza-azulada (a calçada creme é que
estava fora da família); aqui ele entraria como remendo, exatamente o defeito da
terra batida de Sandgem e da areia de Pastoria.

ENTÃO O CALÇAMENTO É NOSSO, e ele custa QUASE nada. O tijolo 521 usa TRÊS cores
((206,156,82), (214,181,107), (222,206,132)) e a laje 545 usa TRÊS
((189,189,189), (213,213,213), (255,255,255)), as seis já desenhadas neste
repositório. O vocabulário de praça sai de três operações sobre elas:

  - ESPELHO. O tijolo não é simétrico e a laje é um trançado diagonal, então
    espelhar muda o desenho de verdade: contra o original, o espelho horizontal
    do tijolo dá 37,4 de distância RGB média, o vertical 37,4 e o duplo 43,0; na
    laje dá 24,0, 30,4 e 43,4. Todos muito acima do piso de 8,0 do
    `varia_carimbo.py`. Custo: ZERO tile e ZERO cor, porque espelho é bit.
  - MOSAICO. Metatile cujos quatro quadrantes de 8x8 misturam duas famílias.
    Como cada entrada de metatile carrega a PRÓPRIA vaga de paleta, misturar um
    quadrante de laje (paleta 3 do primário) com um de granito (vaga 6 do
    secundário) é de graça.
  - GRANITO. É a ÚNICA arte nova do chão: os quatro tiles da laje escurecidos
    pelo fator 0,62, o que dá (117,117,117), (132,132,132) e (158,158,158). São
    4 tiles e 3 cores, e é com eles que a praça ganha MEIO-FIO, que é o que
    separa praça de mancha. Não é importação: é a nossa própria laje, mais
    escura.

O DESENHO. Cidade grande não tem mancha orgânica, tem figura com contorno, e
aqui são duas:

  - PRAÇA: retângulo plantado DENTRO dos campos de tijolo, com moldura de nove
    peças (quatro lados, quatro cantos e o miolo). A moldura é o meio-fio de
    granito e o miolo é o mosaico de laje e granito. Os tamanhos são tentados do
    maior para o menor, porque praça grande lê como praça e praça pequena lê
    como remendo.
  - JUNTA: fora das praças, o tijolo e a laje recebem as variantes espelhadas,
    escolhidas por hash da posição. É o que tira dos dois tapetes a cara de
    papel de parede sem gastar nada.

OS DOIS CARIMBOS. Esta é a primeira cidade da onda com DOIS: o tijolo 521 e a
laje 545, os dois com atributo 0x0000 (comportamento 0, layerType NORMAL) e os
dois inteiramente na elevação 3, sem uma célula sólida. Tratar só o 521 daria
régua de 18,6% (a laje passaria a ser o carimbo dominante), o que passa no teto
de 20% por menos de um ponto e meio e deixaria METADE do defeito de pé: o tapete
branco de 254 células continuaria liso. Com os dois, o carimbo dominante passa a
ser a grama do primário.

O MOBILIÁRIO. Seis peças, e só TRÊS vêm de fora:

  - IMPORTADAS do `Pokemon Light Platinum`, de WesleyFG, base Ruby (AXVE), md5
    7fd2c08735459d99fa23fdaa9b755486, par primário `0x286CF4` e secundário
    `0x286DB4` (o mesmo par que Jubilife usou): o BANCO (metatiles 24 e 25 do
    hack) e as duas GRADES (9 e 21). São o que uma praça precisa e o que este
    tileset não tem desenhado. A cor foi medida antes de escolher: a cor mais
    distante do banco está a 15,8 da cor mais próxima que os NOSSOS dois
    tilesets já têm, e a da grade a 24,0. É a mesma família cinza-azulada da
    catedral e dos prédios da cidade.
  - NOSSAS, de graça, levantando a camada de CIMA de metatiles que os nossos
    tilesets já desenham: o ARBUSTO REDONDO (a arte de cima do 539 do
    secundário), a MOITA LARGA (o par 30 e 31 do primário, que são o mesmo
    desenho espelhado) e a MOITA (o 14 do primário). Custo: zero tile, zero cor.
    São os canteiros de arbusto que o tema desta passada pede, e são o verde que
    a cidade já usa, não um verde de outra ROM.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHÃO NOVO é metatile com arte SÓ na camada de BAIXO e atributo IGUAL, bit a
    bit, ao do carimbo que ele substitui (0x0000 nos dois). Camada de cima em
    chão andável com layerType NORMAL desenharia ACIMA do jogador, e calçamento
    por cima do boneco é defeito, não enfeite. É por isso que as nove peças de
    laje que o tileset JÁ tem (536 a 538, 544, 546 e 552 a 554) NÃO podem ser
    usadas para plantar praça: oito delas desenham na camada de cima e por isso
    têm layerType COVERED, e trocar um 521 (NORMAL, andável) por um 537
    (COVERED, andável) muda o par (comportamento, layerType) de célula andável,
    que é justamente o que a regra 4 do `portao_planta.py` proíbe.
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chão entrada por entrada, e o atributo é comportamento ZERADO
    com layerType COVERED (0x1000), que põe as duas camadas ABAIXO do sprite.
  - CADA MÓVEL SAI EM TRÊS VERSÕES, e elas diferem SÓ na camada de baixo: uma
    pousa no tijolo, outra na laje e outra no mosaico da praça. Sem isso, banco e
    arbusto ficariam todos fora das praças, que é justamente onde mobiliário de
    praça mora.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado.
    Comportamento é id semântico: todo móvel entra com o comportamento ZERADO.

A LEI DE COLISÃO desta onda: 0 -> 1 é PERMITIDA em célula que não seja caminho,
warp, evento nem alcance de script, desde que o alcance a pé continue o mesmo;
1 -> 0 é PROIBIDA e fica em ZERO células. Elevação intacta em 100% das palavras.
Os DOIS portões de alcance rodam NA HORA, peça a peça: busca em largura a partir
de warp e objeto, e casamento de COMPONENTES conexos.

O BLOCO PRÓPRIO DESTA PASSADA É O 196, e não o 175. O
`enfeita_cidades.corredores_de_teste` pula o bloco de teste da própria rodada de
propósito, e o padrão dele é o `175_cidades_enfeitadas.json`. Para esta passada o
175 é um bloco como qualquer outro e quem tem que ficar de fora é o 196, que é
DERIVADO deste desenho. O nome é trocado ANTES da primeira chamada porque a
função guarda o resultado em cache. E o bloco que manda aqui é o T176: ele anda
por HearthomeCity com rotas medidas tile a tile pelas colunas 6, 16 e 36 e pelas
linhas 15, 16, 20, 30, 32 e 34, mais os três portões de seta e quatro portas.
Móvel sólido em qualquer uma dessas células deixa o T176 vermelho, e o
`corredores_de_teste` é justamente quem as congela.

O QUE FICOU DE FORA, com o motivo medido:

  - O CALÇAMENTO de praça do hack (metatiles 30, 31, 38, 46, 47, 54, 55, 62 e 63
    do secundário `0x286DB4`), por COR: 78,0 do nosso tijolo e 83,4 da nossa
    laje, contra o critério de 50.
  - O HIDRANTE (26, 27 e 28). Ele é o móvel de cor mais estranha à cidade: a cor
    mais distante dele está a 43,8 do que os nossos tilesets já têm, contra 15,8
    do banco e 24,0 da grade. Hidrante também é mobiliário de RUA, e o tema desta
    passada é praça.
  - O CANTEIRO DE MADEIRA do hack (40 e 41). Ele é peça de UMA camada e traz o
    calçamento cinza-azulado do hack assado dentro do próprio tile, o mesmo
    calçamento que a conta de cor acabou de reprovar. O canteiro desta praça é o
    arbusto NOSSO.
  - O VASO (294) e as COPAS (68, 104 e 295). O vaso pinta com DUAS paletas do
    hack ao mesmo tempo (a 2 e a 10) e a copa com a 2, que sozinha pede 9 cores;
    com o banco e a grade já na vaga 6, não sobrava vaga para uma terceira
    paleta do hack. Copa sem vaso é meia peça, que é a armadilha que a topiaria
    de Jubilife já pagou.
  - A FLOR VERMELHA do nosso primário (metatile 4). Ela seria o canteiro de flor
    do tema, e não entrou por medida e não por gosto: a camada de cima dela cobre
    a célula INTEIRA, com a grama assada junto, então plantada no calçamento ela
    vira um quadrado de grama com flor em cima.

Uso:
    python3 dev_scripts/praca_hearthome.py             # mede e mostra o plano
    python3 dev_scripts/praca_hearthome.py --aplicar   # tileset e mapa
    python3 dev_scripts/praca_hearthome.py --desfazer  # devolve o map.bin
    python3 dev_scripts/praca_hearthome.py --demo      # auto-teste
    python3 dev_scripts/praca_hearthome.py --autoteste # idem
    python3 dev_scripts/praca_hearthome.py --extrai    # regera o kit
    python3 dev_scripts/praca_hearthome.py --medir     # o orçamento, sem plano
    python3 dev_scripts/praca_hearthome.py --so-tileset
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

# Ver o cabeçalho: o bloco desta passada é o 196, e o 175 é um bloco de teste
# como qualquer outro. O nome é trocado ANTES da primeira chamada porque
# `corredores_de_teste` guarda o resultado em cache.
E.BLOCO_PROPRIO = "196_praca_hearthome.json"

DESTINO = f"{RAIZ}/data/tilesets/secondary/hearthome"
KIT_JSON = f"{RAIZ}/dev_scripts/praca_hearthome_kit.json"
PLANO = f"{RAIZ}/dev_scripts/praca_hearthome.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_Hearthome"
IRMAOS = ["HearthomeCity"]          # um só, e o cabeçalho diz o que isso custa
ALVO = "HearthomeCity"

# Os DOIS carimbos, com o papel de cada um no desenho.
CARIMBO_TIJOLO = 521
CARIMBO_LAJE = 545
CARIMBOS = [CARIMBO_TIJOLO, CARIMBO_LAJE]

TETO_TILES = 512
TETO_META = 512
META_LOCAL_0 = 293          # o primeiro local da faixa ALTA contígua livre
MARGEM = 2
TETO_REGUA = 20.0
FATOR_GRANITO = 0.62        # a laje escurecida, e é a única arte nova do chão
PISO_VARIA = 8.0            # o piso do `varia_carimbo.py` para duas variantes

# `gTileset_Hearthome` tem `.callback = NULL` em `src/data/tilesets/headers.h` e
# nenhuma linha em `src/tileset_anims.c`: não há vaga de tile pinada por
# animação neste tileset. A constante fica aqui para o portão continuar
# existindo se alguém pinar alguma um dia.
PINOS_ANIM = set()

# ------------------------------------------------------------------- a FONTE
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          pri=0x286CF4, sec=0x286DB4, split=(512, 512, 6),
          mapa="grupo 0 mapa 10, a metropole, 54x44")

# Paleta do hack -> vaga NOSSA. A conta está no cabeçalho: a 0 do hack (o banco)
# tem 7 cores e a 10 (a grade) tem 5, e a união delas dá 11 porque (64,72,104) é
# a mesma nas duas. Com as 3 do granito, são 14 das 15 vagas livres da vaga 6.
VAGA_NOSSA = 6
VAGAS_PAL = {0: VAGA_NOSSA, 10: VAGA_NOSSA}

# --------------------------------------------------------------- os MÓVEIS
# `grade` são os metatiles em ordem de leitura e `solidas` diz quais células
# viram SÓLIDAS. Todas as peças desta passada são sólidas por inteiro: nenhuma
# tem uma linha de cima que continue andável, porque nenhuma tem duas linhas.
#
# `fonte` diz de onde a arte vem:
#   "lp"     metatile do `Pokemon Light Platinum` (entra pelo kit)
#   "pri"    camada de CIMA de um metatile do NOSSO primário
#   "sec"    camada de CIMA de um metatile do NOSSO secundário
MOVEIS = [
    dict(nome="banco", fonte="lp", grade=[[24, 25]], solidas=[[1, 1]],
         onde="qualquer", quantos=14, espaco=5),
    dict(nome="grade", fonte="lp", grade=[[9]], solidas=[[1]],
         onde="beira", quantos=13, espaco=6),
    dict(nome="grade com poste", fonte="lp", grade=[[21]], solidas=[[1]],
         onde="beira", quantos=12, espaco=6),
    dict(nome="arbusto redondo", fonte="sec", grade=[[539]], solidas=[[1]],
         onde="qualquer", quantos=18, espaco=5),
    dict(nome="moita larga", fonte="pri", grade=[[30, 31]], solidas=[[1, 1]],
         onde="qualquer", quantos=13, espaco=6),
    dict(nome="moita", fonte="pri", grade=[[14]], solidas=[[1]],
         onde="qualquer", quantos=16, espaco=5),
]
ESPACO_ENTRE_MOVEIS = 3     # Chebyshev mínimo entre duas peças QUAISQUER

# ------------------------------------------------------------------- a PRAÇA
# Cada peça de chão é uma lista de quatro fontes de quadrante, e cada fonte é
# (família, quadrante, espelho). As famílias:
#   "tij"  o tijolo 521          "laj"  a laje 545          "gra"  o granito
PECAS_CHAO = [
    # a JUNTA do tijolo: o mesmo desenho com o bit de espelho ligado
    dict(nome="tijolo virado", espelho=("tij", "h")),
    dict(nome="tijolo deitado", espelho=("tij", "v")),
    dict(nome="tijolo girado", espelho=("tij", "hv")),
    # a JUNTA da laje
    dict(nome="laje virada", espelho=("laj", "h")),
    dict(nome="laje deitada", espelho=("laj", "v")),
    dict(nome="laje girada", espelho=("laj", "hv")),
    # o MEIO-FIO: granito na borda que dá para fora
    dict(nome="fio norte", quads=[("gra", 0), ("gra", 1), ("laj", 2), ("laj", 3)]),
    dict(nome="fio sul", quads=[("laj", 0), ("laj", 1), ("gra", 2), ("gra", 3)]),
    dict(nome="fio oeste", quads=[("gra", 0), ("laj", 1), ("gra", 2), ("laj", 3)]),
    dict(nome="fio leste", quads=[("laj", 0), ("gra", 1), ("laj", 2), ("gra", 3)]),
    dict(nome="fio NO", quads=[("gra", 0), ("gra", 1), ("gra", 2), ("laj", 3)]),
    dict(nome="fio NE", quads=[("gra", 0), ("gra", 1), ("laj", 2), ("gra", 3)]),
    dict(nome="fio SO", quads=[("gra", 0), ("laj", 1), ("gra", 2), ("gra", 3)]),
    dict(nome="fio SE", quads=[("laj", 0), ("gra", 1), ("gra", 2), ("gra", 3)]),
]

# OS TAMANHOS, e por que existe UMA figura de praça e não duas.
#
# Medido nesta árvore: o maior retângulo que cabe no campo de TIJOLO é 12 por 7,
# e o maior que cabe no campo de LAJE é 3 por 12. O campo branco desta cidade
# não é uma área, é uma REDE DE AVENIDAS de três células de largura. Pedir praça
# quadrada lá dentro devolve ZERO praça, e a saída tentada foi uma faixa de
# tijolo com meio-fio de granito correndo pelo meio da avenida, o canteiro
# central. Ela foi desenhada, plantada e CORTADA no render: no mapa inteiro os
# quatro retângulos de 3 por 9 leem como PRÉDIO, não como chão, e chão que o
# jogador acha que é parede é pior do que chão liso. O campo de laje fica com a
# junta espelhada e com o mobiliário, e a praça mora só no campo de tijolo.
# A lista vai até 4 por 3, que é a menor praça que ainda tem miolo: com o piso
# em 4 por 4 a cidade fechava com TRÊS praças, e com 4 por 3 fecha com seis, que
# é o que faz a figura aparecer nos dois quarteirões do sul E nas faixas de
# tijolo do miolo. Menor que isso não sobra miolo nenhum.
TAMANHOS_CLARA = [(9, 7), (8, 6), (7, 6), (7, 5), (6, 5), (6, 4), (5, 5),
                  (5, 4), (4, 4), (4, 3), (3, 4)]

# AS DUAS FIGURAS de praça, uma para cada carimbo.
#
# O MEDALHÃO são quatro células no centro da praça que juntas desenham um
# OCTÓGONO de granito, e ele custa ZERO metatile a mais: as quatro peças dele
# são as quatro peças de CANTO do próprio meio-fio, com o canto de miolo virado
# para FORA. A ordem é (noroeste, nordeste, sudoeste, sudeste) do bloco de 2 por
# 2, e cada uma leva a peça cujo quadrante de miolo fica no canto que dá para
# fora.
#
# A primeira versão desta passada espalhava meio-granito por hash dentro da
# praça inteira, e o render reprovou: a olho nu aquilo não lia como mosaico, lia
# como chuvisco de televisão. A segunda punha um quadrado de granito chapado no
# centro. O octógono é a terceira e é a que ficou: figura, e figura é o que
# separa praça de mancha.
FIGURAS = [
    dict(nome="praça clara", em=CARIMBO_TIJOLO, fundo="laje",
         tamanhos=TAMANHOS_CLARA,
         miolo=["laje virada", "laje deitada", "laje girada"],
         medalhao=["fio SE", "fio SO", "fio NE", "fio NO"],
         n="fio norte", s="fio sul", o="fio oeste", l="fio leste",
         no="fio NO", ne="fio NE", so="fio SO", se="fio SE"),
]
MIOLOS = sorted({n for f in FIGURAS for n in f["miolo"]})
# O medalhão só entra em praça com miolo de 4 por 4 ou mais: em praça menor ele
# encostaria na moldura e o losango viraria borrão colado no meio-fio.
MIOLO_MIN_MEDALHAO = 3
# Do maior para o menor: praça grande lê como praça, praça pequena lê como
# remendo.
TETO_PRACA = 230            # células de praça, somando moldura e miolo
FOLGA_PRACA = 1             # células de tijolo entre duas praças

# A JUNTA de cada carimbo, e ela cobre TODA célula elegível.
#
# A primeira versão desta passada deixava uma das quatro escolhas em `None`, o
# que queria dizer "deixa o carimbo", e o auto-teste reprovou com número: o piso
# novo saía em 79 pedaços de 5,9 células em média, ou seja sal e pimenta, não
# área. O motivo é que a célula deixada de fora PARTE a mancha, e a regra 8(b)
# desta onda mede exatamente isso. Sem o `None` o campo inteiro vira junta e a
# mancha volta a ser área. O desenho não perde nada: as três variantes são o
# MESMO desenho do carimbo com o bit de espelho ligado, então o campo continua
# sendo o mesmo tijolo (ou a mesma laje), só que sem a repetição exata.
JUNTA = {
    CARIMBO_TIJOLO: ["tijolo virado", "tijolo deitado", "tijolo girado"],
    CARIMBO_LAJE: ["laje virada", "laje deitada", "laje girada"],
}
# O fundo que o móvel pousa em cima, por família de célula.
FUNDO_DE = {CARIMBO_TIJOLO: "tijolo", CARIMBO_LAJE: "laje"}

N4 = E.N4


def corredor_largo(v, W, H, d):
    """As células que a suíte PODE pisar nesta cidade, por EXCESSO de verdade.

    Por que ela existe, e o preço que ela já custou nesta frente. O
    `enfeita_cidades.corredores_de_teste` simula cada roteiro com UMA convenção
    só: o primeiro toque de uma direção NOVA vira o boneco e não anda. Essa
    convenção está certa quando o jogador está PARADO, e está errada logo depois
    de uma perna SATURANTE, quando ele continua no estado de andar e o primeiro
    toque da direção nova ANDA (é a lição que o próprio T176.3 escreveu, medida
    em 6 rodadas de cada lado). A diferença de UM tile por perna muda a rota
    inteira: nesta cidade, com a convenção de virar, o T176.2 sobe a coluna 6 até
    a linha 15 e varre a linha 15; com a de andar, ele sobe até a linha 14 e
    varre a linha 14. Esta passada plantou quatro peças na linha 14, e o caso
    fechou VERMELHO com o jogador parando em (6,16), justamente porque a linha 14
    não estava congelada.

    A saída não é escolher a convenção certa, é não escolher: a simulação carrega
    um CONJUNTO de estados (x, y, para onde olha) e, a cada perna, aplica AS DUAS
    convenções a cada estado, guardando a união. O resultado é um superconjunto
    do que o motor faz, que é o lado certo para errar, porque excesso aqui custa
    enfeite a menos e falta custa caso vermelho.

    Ela é a UNIÃO com o `corredores_de_teste`, e não a substituta dele: aquele
    também trata `WARP=` no meio do roteiro e outros detalhes que esta não vê.
    """
    import glob
    import re
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_",
                                d.get("name", ALVO)).upper().replace("__", "_")
    obj = {(o["x"], o["y"]) for o in (d.get("object_events") or [])}
    warps = d.get("warp_events") or []
    passo = re.compile(r"^\d+:(UP|DOWN|LEFT|RIGHT)(?:\*(\d+))?$")
    DIR = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}
    pisadas = set()

    def anda(x, y, dirc, passos):
        dx, dy = dirc
        for _ in range(max(0, passos)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                break
            j = ny * W + nx
            if (v[j] >> 10) & 3 or (nx, ny) in obj:
                break
            ea = (v[y * W + x] >> 12) & 0xF
            eb = (v[j] >> 12) & 0xF
            if ea and eb and ea != eb:
                break
            x, y = nx, ny
            pisadas.add((x, y))
        return x, y

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
                m = passo.match(tok.strip())
                if m:
                    pernas.append((DIR[m.group(1)], int(m.group(2) or 1)))
            estados = set()
            for x0, y0 in ((warps[wid]["x"], warps[wid]["y"]),
                           (warps[wid]["x"], warps[wid]["y"] + 1)):
                if not (0 <= x0 < W and 0 <= y0 < H):
                    continue
                pisadas.add((x0, y0))
                for olhando in DIR.values():
                    estados.add((x0, y0, olhando))
            for dirc, n in pernas:
                novos = set()
                for x, y, olhando in estados:
                    # AS DUAS convenções, sempre: a de virar (perde um toque) e a
                    # de andar (não perde). Guardar as duas é o que faz esta
                    # conta ser superconjunto do que o motor faz.
                    for passos in ({n, n - 1} if olhando != dirc else {n}):
                        novos.add(anda(x, y, dirc, passos) + (dirc,))
                estados = novos
                if len(estados) > 4096:      # não deve acontecer nesta cidade
                    break
    return pisadas


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair idêntico em qualquer máquina e em qualquer versão de Python."""
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
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits DESLOCADOS três
    casas, não esticados para 0..255. Todo `.pal` desta árvore está nessa conta.
    """
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    if len(b) < 32:
        return None
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _metatile_ents(mt_id):
    """As 8 entradas de um metatile QUALQUER dos nossos dois tilesets."""
    if mt_id < 512:
        return _entradas(_tileset(PRIMARIO)["metatiles"], mt_id)
    return _entradas(_tileset(SECUNDARIO)["metatiles"], mt_id - 512)


# ------------------------------------------------------- o que está VIVO aqui
def metatiles_vivos():
    """Locais de metatile do SECUNDÁRIO que algum layout realmente usa.

    Conta o `map.bin` E a BORDA de cada layout: a borda desenha nas margens da
    tela e não aparece no `map.bin`. Sem ela, um metatile de borda seria tomado
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
    """As vagas de TILE do secundário que NENHUM metatile referencia.

    Não é "tile que só metatile morto usa": é tile que NENHUMA das oito entradas
    de NENHUM dos 512 metatiles do `metatiles.bin` pede, nem vivo nem morto.
    Escrever nelas não muda o desenho de metatile nenhum, e por isso não há
    renumeração e não há `compacta_tileset.py` nesta passada. O tile 0 fica fora.

    Os metatiles que ESTA passada grava (locais de `META_LOCAL_0` para cima)
    ficam de fora da conta, e é isso que torna a alocação idempotente: depois da
    primeira aplicação as vagas do kit voltariam a parecer ocupadas e a segunda
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
    """{vaga: [índices de cor que NENHUM pixel VIVO usa]}.

    Vivo é o pixel que algum metatile alcançável desenha: o metatile aparece no
    `map.bin` ou na borda de um dos layouts. Escrever cor nova num índice que
    nenhum pixel vivo usa não muda o desenho de nada que o jogador veja. Os
    metatiles que ESTA passada grava ficam de fora da conta, para que `--extrai`
    depois de `--aplicar` dê o mesmo kit.
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
            for v in sorted(ts["paletas"]) if v >= 6}


def granito_nosso():
    """Os quatro tiles do GRANITO e as três cores dele, medidos do nosso tileset.

    O granito é a laje 545 escurecida por `FATOR_GRANITO`. É a única arte nova de
    chão desta passada e ela não vem de ROM nenhuma: vem de multiplicar as três
    cores da nossa própria laje. Devolve (px_por_quadrante, cores_ordenadas).

    A laje entra SEM bit de espelho nas quatro entradas (medido: `0x3282`,
    `0x3281`, `0x3272`, `0x3271`, e `& 0x0C00` é zero nas quatro), então o tile
    do granito do quadrante q é o tile da laje do quadrante q, pixel a pixel.
    """
    import render_maps as RM
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    ents = _metatile_ents(CARIMBO_LAJE)[:4]
    if any(v & 0x0C00 for v in ents):
        raise SystemExit("a laje %d tem bit de espelho e o granito supõe que não"
                         % CARIMBO_LAJE)
    px, cores = {}, {}
    for q, v in enumerate(ents):
        tile = RM.resolver_tile(tp, ts, v & 0x3FF)
        pal = (tp if ((v >> 12) & 0xF) < 6 else ts)["paletas"][(v >> 12) & 0xF]
        if tile is None:
            raise SystemExit("o quadrante %d da laje não resolve" % q)
        px[q] = tile
        for linha in tile:
            for c in linha:
                if c:
                    cores[tuple(pal[c])] = None
    lista = sorted(cores)
    escuras = [tuple(min(255, int(c * FATOR_GRANITO)) for c in cor)
               for cor in lista]
    de_para = dict(zip(lista, escuras))
    saida = {}
    for q, tile in px.items():
        v = ents[q]
        pal = (tp if ((v >> 12) & 0xF) < 6 else ts)["paletas"][(v >> 12) & 0xF]
        saida[q] = [[0 if c == 0 else 1 + sorted(escuras).index(
            de_para[tuple(pal[c])]) for c in linha] for linha in tile]
    return saida, sorted(escuras)


# ---------------------------------------------------------------- a EXTRAÇÃO
def extrai():
    """Regera `praca_hearthome_kit.json`.

    O que vem da ROM privada do hack são SÓ os tiles do banco e das duas grades;
    o granito é calculado do nosso próprio tileset. O que sai daqui é o asset
    CONVERTIDO (tiles em nibbles, já reindexados para a vaga de destino, e paleta
    em RGB), nunca a ROM.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("não achei fontes-mapas/romhacks: --extrai só roda na "
                         "máquina que tem as ROMs. O kit já extraído está em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402

    pasta = os.path.join(ferr, LP["slug"])
    gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
    caminho = os.path.join(pasta, gba)
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    if md5 != LP["md5"]:
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s: não "
                         "leio um byte de uma cópia diferente"
                         % (gba, md5, LP["md5"]))
    r = Rom(caminho)
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = LP["split"]
    t1 = r.parse_tileset(LP["pri"])
    t2 = r.parse_tileset(LP["sec"])
    if t1 is None or t2 is None:
        raise SystemExit("o par 0x%X/0x%X do hack não abriu"
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

        Tile transparente na camada de cima é entrada morta do dumper, e tratar
        isso como camada de cima cheia deixaria a peça vazia.
        """
        if not (v & 0x3FF):
            return True
        t = px_de(v)
        return t is None or not any(c for linha in t for c in linha)

    # O CHÃO DA FONTE, por EVIDÊNCIA e não por constante decorada: censo dos
    # padrões de camada de baixo do tileset inteiro do hack. Padrão repetido é
    # piso; padrão de arte aparece uma ou duas vezes. Quatro tiles IGUAIS
    # também é piso.
    censo = collections.Counter()
    for i in range(n_meta):
        censo[tuple(x & 0x3FF for x in ents_de(i)[:4])] += 1
    chao = set()
    for pat, k in censo.items():
        if k >= 4 or len({x for x in pat}) == 1:
            chao |= {x for x in pat if x}
    censo_top = [[list(p), k] for p, k in censo.most_common(8)]

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}
    pecas = []

    def guarda(v):
        """Registra o tile de uma entrada e devolve a chave dele.

        A CHAVE LEVA A PALETA DE ORIGEM: o mesmo desenho 8x8 pintado com duas
        paletas do hack são duas vagas nossas, senão a segunda apaga a primeira.
        """
        idx, ip = v & 0x3FF, (v >> 12) & 0xF
        if ip not in VAGAS_PAL:
            raise SystemExit("a paleta %d do hack não está no mapa de vagas" % ip)
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

    quero = []
    for mv in MOVEIS:
        if mv["fonte"] != "lp":
            continue
        for li, linha in enumerate(mv["grade"]):
            for ci, lp in enumerate(linha):
                quero.append(("movel", "%s %d %d" % (mv["nome"], li, ci), lp))

    for papel, nome, local in quero:
        if local >= n_meta:
            raise SystemExit("%s: o metatile %d não existe no tileset"
                             % (nome, local))
        ents = ents_de(local)
        attr = struct.unpack_from("<H", t2["attr"], local * 2)[0]
        baixo, cima = ents[:4], ents[4:]
        uniforme = len({v & 0x3FF for v in baixo}) == 1
        usadas, escolhidas = [], []
        for q in range(4):
            vazio_em_cima = branco(cima[q])
            v = baixo[q] if vazio_em_cima else cima[q]
            escolhidas.append(v)
            if not (v & 0x3FF):
                usadas.append(None)
                continue
            idx = v & 0x3FF
            li = idx - npri
            if vazio_em_cima and (uniforme or (idx >= npri and li in chao)):
                usadas.append(None)          # é o chão da fonte: fica de fora
                continue
            usadas.append(guarda(v))
        if not any(usadas):
            raise SystemExit("%s: o metatile %d não sobrou com nenhum quadrante "
                             "de arte" % (nome, local))
        pecas.append(dict(papel=papel, nome=nome, lp=local, attr=attr,
                          ents=escolhidas, usadas=usadas,
                          baixo=baixo, cima=cima))

    # ------------------------------------------- o GRANITO, que é NOSSO
    gpx, gcores = granito_nosso()
    for q, tile in gpx.items():
        ch = "granito:%d" % q
        tiles_px[ch] = tile
        tiles_vaga[ch] = VAGA_NOSSA
        tiles_cor[ch] = {tuple(c) for c in gcores}

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
            raise SystemExit("a vaga %d tem %d índices livres (%s) e o kit pede "
                             "%d cores" % (vaga, len(vagos), vagos, len(cores)))
        base = [list(c) for c in ts_nosso["paletas"][vaga]]
        for k, c in enumerate(cores):
            base[vagos[k]] = list(c)
            indice[(vaga, c)] = vagos[k]
        paletas[str(vaga)] = base

    # REINDEXA cada nibble para a tabela nova. A cor 0 continua 0 e nenhuma cor
    # é aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, só em
    # outro índice, então o pixel sai idêntico.
    saida_tiles = {}
    for ch, px in sorted(tiles_px.items()):
        if ch.startswith("granito:"):
            ordem = sorted({tuple(c) for c in gcores})
            saida_tiles[ch] = [[0 if c == 0
                                else indice[(VAGA_NOSSA, ordem[c - 1])]
                                for c in linha] for linha in px]
            continue
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
        granito=dict(fator=FATOR_GRANITO, cores=[list(c) for c in gcores],
                     de="o metatile %d deste repositório" % CARIMBO_LAJE),
        vagas_livres={str(k): v for k, v in livres.items()},
        vagas_pal={str(k): v for k, v in VAGAS_PAL.items()},
        paletas=paletas, tiles=saida_tiles, tiles_vaga=tiles_vaga,
        chao_da_fonte=sorted(chao), censo_chao=censo_top, pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d peças importadas, granito com %d cores"
          % (os.path.relpath(KIT_JSON, RAIZ), len(saida_tiles), len(pecas),
             len(gcores)))
    for vaga, cores in sorted(por_vaga.items()):
        print("  vaga %2d: %2d cores nos índices %s (de %d livres)"
              % (vaga, len(cores), [indice[(vaga, c)] for c in sorted(cores)],
                 len(livres.get(vaga) or [])))
    return 0


# --------------------------------------------------------------- o KIT em disco
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa máquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def chao_nosso(carimbo):
    """As quatro entradas da camada de BAIXO de um carimbo, mais o atributo dele.

    É o chão que todo móvel pousa em cima. Os dois carimbos desta cidade são do
    SECUNDÁRIO e os dois têm atributo 0x0000.
    """
    ts = _tileset(SECUNDARIO)
    local = carimbo - 512
    ents = _entradas(ts["metatiles"], local)
    for v in ents[4:]:
        if v & 0x3FF:
            import render_maps as RM
            t = RM.resolver_tile(_tileset(PRIMARIO), ts, v & 0x3FF)
            if t and any(c for linha in t for c in linha):
                raise SystemExit("o carimbo %d já usa a camada de cima" % carimbo)
    attr = G._attrs(SECUNDARIO)[local]
    if attr & 0xFF:
        raise SystemExit("o carimbo %d tem comportamento 0x%02X e esta rodada "
                         "supõe chão normal" % (carimbo, attr & 0xFF))
    if attr & 0xF000:
        raise SystemExit("o carimbo %d não é layerType NORMAL" % carimbo)
    return ents[:4], attr


def desenha_kit():
    """(tiles_novos, metas, attrs, carimbos) sem escrever nada em lugar nenhum.

    `tiles_novos` é {vaga: nibbles}, e as vagas saem da lista de buracos do
    `tiles.png` em ordem crescente, que é fixa enquanto ninguém mexer nos
    metatiles antigos.
    """
    dados = kit()
    base_tij, attr_tij = chao_nosso(CARIMBO_TIJOLO)
    base_laj, attr_laj = chao_nosso(CARIMBO_LAJE)
    if attr_tij != attr_laj:
        raise SystemExit("os dois carimbos têm atributos diferentes (0x%04X e "
                         "0x%04X) e o plano supõe um só" % (attr_tij, attr_laj))
    attr_chao = attr_tij
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
                raise SystemExit("o kit em disco não tem o tile %s" % chave)
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

    # ------------------------------------------------------- as FAMÍLIAS de chão
    FAM = {"tij": list(base_tij), "laj": list(base_laj),
           "gra": [((512 + vaga("granito:%d" % q)) | (VAGA_NOSSA << 12))
                   for q in range(4)]}

    entradas_chao = {}
    for c in PECAS_CHAO:
        if "espelho" in c:
            fam, eixo = c["espelho"]
            ents = _espelha4(FAM[fam], eixo)
        else:
            ents = [FAM[f][q] for f, q in c["quads"]]
        if any(not (e & 0x3FF) for e in ents):
            raise SystemExit("%s: quadrante vazio em peça de chão" % c["nome"])
        entradas_chao[c["nome"]] = ents
        gid = poe(list(ents) + [0, 0, 0, 0], attr_chao)
        carimbos["chao"].append(dict(nome=c["nome"], mt=gid))

    # ---------------------------------------------------------------- MÓVEIS
    # Três fundos, e a razão está no cabeçalho: sem eles o mobiliário ficaria
    # todo fora das praças.
    # Dois fundos, e não três: móvel plantado no miolo da praça pousa na LAJE,
    # que é o piso que aquela célula tem ali de qualquer jeito.
    FUNDOS = {"tijolo": list(base_tij), "laje": list(base_laj)}

    def arte_de(mv, lp):
        """As quatro entradas da camada de CIMA da célula, já na NOSSA vaga.

        Para peça IMPORTADA, o tile vem do kit e a vaga de paleta é a nossa.
        Para peça NOSSA, a arte é a camada de cima de um metatile que os nossos
        tilesets já desenham, e ela entra como está: o índice de tile e a vaga de
        paleta continuam valendo, porque o primário deste layout é o mesmo.
        """
        if mv["fonte"] == "lp":
            p = por_peca[("movel", lp)]
            fora = []
            for q in range(4):
                ch = p["usadas"][q]
                if ch is None:
                    fora.append(0)
                    continue
                v = p["ents"][q]
                alvo = VAGAS_PAL[int(ch.split(":")[2])]
                fora.append((v & 0x0C00) | (512 + vaga(ch)) | (alvo << 12))
            return fora
        ents = _metatile_ents(lp)
        cima = ents[4:]
        if not any(v & 0x3FF for v in cima):
            raise SystemExit("o metatile %d não tem camada de cima para levantar"
                             % lp)
        return list(cima)

    feito = {}
    for mv in MOVEIS:
        grades = {}
        for fundo, ents_fundo in sorted(FUNDOS.items()):
            grade = []
            for li, linha in enumerate(mv["grade"]):
                saida = []
                for ci, lp in enumerate(linha):
                    chave_mt = (mv["fonte"], lp, fundo)
                    if chave_mt in feito:
                        saida.append(feito[chave_mt])
                        continue
                    nome_peca = "%s %d %d" % (mv["nome"], li, ci)
                    cima = arte_de(mv, lp if mv["fonte"] != "lp" else nome_peca)
                    if not any(cima):
                        raise SystemExit("%s: célula sem arte" % mv["nome"])
                    # comportamento ZERADO (nenhum id semântico é importado) e
                    # layerType COVERED, que põe as duas camadas ABAIXO do sprite
                    feito[chave_mt] = poe(list(ents_fundo) + list(cima), 0x1000)
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
        raise SystemExit("o kit caiu em vaga de PINO de animação: %s"
                         % sorted(set(tiles_novos) & PINOS_ANIM))

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    _loc_vivos, usados = metatiles_vivos()
    n_disco = len(meta_disco) // 16
    for local, ents in metas.items():
        gid = 512 + local
        nosso = (local < n_disco and _entradas(meta_disco, local) == ents)
        if gid in usados and not nosso:
            raise SystemExit("o mapa já usa o metatile %d" % gid)
        if local < n_disco and not nosso:
            antigo = _entradas(meta_disco, local)
            if not enchimento(antigo):
                raise SystemExit("a vaga de metatile %d já está ocupada" % gid)
    return tiles_novos, metas, attrs, carimbos


def _grava_pal(vaga, cores):
    with open(f"{DESTINO}/palettes/%02d.pal" % vaga, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.
    """
    from PIL import Image
    dados = kit()
    antigo = Image.open(f"{DESTINO}/tiles.png")
    if antigo.mode != "P":
        raise SystemExit("o tiles.png não está paletizado (modo %s)" % antigo.mode)
    # `Image.convert("P")` numa imagem que JÁ é "P" devolve uma CÓPIA, e escrever
    # nela não muda o arquivo que se salva depois. Aqui o `load()` é da PRÓPRIA
    # imagem que vai ser salva.
    antigo.load()
    cols = antigo.size[0] // 8
    px = antigo.load()
    for v, tile in tiles_novos.items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        if y0 + 8 > antigo.size[1]:
            raise SystemExit("a vaga de tile %d não cabe no tiles.png" % v)
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
def pracas(elegivel, tomadas, teto, tamanhos):
    """[(canto, largura, altura)] das praças, em ordem determinista.

    Retângulo cheio de células elegíveis e livres, com `FOLGA_PRACA` células de
    tijolo em volta para duas molduras nunca se encostarem.
    """
    saida, usadas, total = [], set(tomadas), 0
    for larg, alt in tamanhos:
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


def peca_da_praca(fig, x0, y0, larg, alt, x, y):
    """Qual peça do calçamento vai nesta célula da praça.

    A moldura é o meio-fio; o centro, quando a praça tem miolo de pelo menos
    `MIOLO_MIN_MEDALHAO` por `MIOLO_MIN_MEDALHAO`, ganha o LOSANGO de granito; o
    resto do miolo é a laje espelhada, escolhida por hash da posição.
    """
    n, s = y == y0, y == y0 + alt - 1
    o, l = x == x0, x == x0 + larg - 1
    if n and o:
        return fig["no"], False
    if n and l:
        return fig["ne"], False
    if s and o:
        return fig["so"], False
    if s and l:
        return fig["se"], False
    if n:
        return fig["n"], False
    if s:
        return fig["s"], False
    if o:
        return fig["o"], False
    if l:
        return fig["l"], False
    if min(larg, alt) - 2 >= MIOLO_MIN_MEDALHAO:  # o miolo cabe o octógono
        cx, cy = x0 + larg // 2, y0 + alt // 2
        for k, p in enumerate(((cx - 1, cy - 1), (cx, cy - 1),
                               (cx - 1, cy), (cx, cy))):
            if (x, y) == p:
                return fig["medalhao"][k], True
    return peca_da_lista(fig["miolo"], x, y), True


def peca_da_lista(nomes, x, y):
    """Qual das peças do grupo cai nesta célula. Hash da posição, não paridade:
    paridade vira xadrez e o auto-teste reprova."""
    return nomes[_mistura(x, y, 0xA5A5 + len(nomes)) % len(nomes)]


# ----------------------------------------------------------- ligação a pé
def componentes(v, W, H):
    """{célula: rótulo} dos pedaços de chão andável ligados a pé.

    POR QUE NÃO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda é
    alcançável a partir de algum ponto de partida", e ponto de partida ali é
    warp OU objeto: fechar um corredor com warp dos dois lados não tira NENHUMA
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
        vistos = {depois.get(p) for p in cels}
        if len(vistos) > 1:
            mau.append("o pedaço %d de chão se partiu em %d" % (rr, len(vistos)))
    juntou = collections.defaultdict(set)
    for p, rr in depois.items():
        if p in antes:
            juntou[rr].add(antes[p])
    for rr, origens in juntou.items():
        if len(origens) > 1:
            mau.append("dois pedaços de chão que eram separados se juntaram")
    return mau


# ---------------------------------------------------------------- o PLANO
def plano_mapa(carimbos, base=None):
    """(L, W, H, v, escritas, contas) de `HearthomeCity`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    elev = {}
    for c in CARIMBOS:
        conta = collections.Counter((x >> 12) & 0xF for x in v
                                    if (x & 0x3FF) == c and not ((x >> 10) & 3))
        if not conta:
            raise SystemExit("o carimbo %d não aparece andável no mapa" % c)
        elev[c] = conta.most_common(1)[0][0]

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    elegivel = {}
    for c in CARIMBOS:
        elegivel[c] = {(i % W, i // W) for i in range(W * H)
                       if andavel(i) and (v[i] & 0x3FF) == c
                       and ((v[i] >> 12) & 0xF) == elev[c]
                       and beh(v[i] & 0x3FF) not in AG
                       and MARGEM <= i % W < W - MARGEM
                       and MARGEM <= i // W < H - MARGEM}
    todas = set().union(*elegivel.values())

    escritas = {}
    # ------------------------------------------------------ 1. o PISO, no papel
    # As praças e as juntas são decididas ANTES dos móveis e escritas DEPOIS
    # deles: com os móveis primeiro, nenhum retângulo de praça sobrevive inteiro.
    plano_piso, miolo, moldura = {}, {}, set()
    lista_pracas, n_praca = [], 0
    for fig in FIGURAS:
        lista, n = pracas(elegivel[fig["em"]], set(), TETO_PRACA,
                          fig["tamanhos"])
        n_praca += n
        for x0, y0, larg, alt in lista:
            lista_pracas.append([fig["nome"], x0, y0, larg, alt])
            for j in range(alt):
                for i in range(larg):
                    p = (x0 + i, y0 + j)
                    nome, dentro = peca_da_praca(fig, x0, y0, larg, alt,
                                                 p[0], p[1])
                    plano_piso[p] = nome
                    if dentro:
                        miolo[p] = fig["fundo"]
                    else:
                        moldura.add(p)
    for c in CARIMBOS:
        for p in sorted(elegivel[c]):
            if p in plano_piso:
                continue
            plano_piso[p] = peca_da_lista(JUNTA[c], p[0], p[1])

    # ------------------------------------------------------------- 2. MÓVEIS
    # Eles vêm antes de o piso ser ESCRITO de propósito: móvel posto no carimbo
    # tira uma célula do numerador E do denominador da régua; móvel posto em cima
    # de uma peça nova tira só do denominador, o que PIORA a conta. MOLDURA fica
    # proibida, porque móvel em cima dela quebra o contorno da praça.
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    gelo |= corredor_largo(v, W, H, d)
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))
    proibido = set(moldura)

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

    def livre(x, y):
        i = y * W + x
        if (x, y) in gelo or i in escritas or (x, y) not in todas:
            return False
        if (x, y) in proibido:
            return False
        return (aplicado[i] & 0x3FF) in CARIMBOS

    def solido(x, y):
        return 0 <= x < W and 0 <= y < H and ((aplicado[y * W + x] >> 10) & 3)

    def encosto_ok(onde, cels):
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

    def fundo_de(p):
        if p in miolo:
            return miolo[p]
        return FUNDO_DE[aplicado[p[1] * W + p[0]] & 0x3FF]

    def tenta_peca(mv, x0, y0):
        """Escreve a peça inteira e devolve o fundo se os DOIS portões deixarem.

        O portão roda NA HORA e não só no fim: se solidificar as células desta
        peça tirar do alcance a pé qualquer OUTRA célula, ou partir um pedaço de
        chão em dois, a escrita é desfeita e o gerador segue.
        """
        pontos = [(x0 + ci, y0 + li)
                  for li, linha in enumerate(mv["grades"]["tijolo"])
                  for ci, _g in enumerate(linha)]
        if any(not livre(x, y) for x, y in pontos):
            return False
        # FUNDO COERENTE: as células de uma peça têm que estar todas no mesmo
        # chão, senão meio banco pousa no tijolo e meio na laje.
        fundos = {fundo_de(p) for p in pontos}
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
            # ELEVAÇÃO PRESERVADA (bits 12 a 15); a colisão só LIGA, nunca desliga
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

    # ------------------------------------------------------ 3. o PISO, escrito
    por_nome = {c["nome"]: c["mt"] for c in carimbos["chao"]}
    conta_chao = collections.Counter()

    def pintavel(p):
        """A célula pode receber CHÃO novo?

        `gelo` NÃO entra aqui, e não entra de propósito: chão novo não mexe em
        colisão, não mexe em elevação e não mexe em (comportamento, layerType),
        então pintar a célula onde mora uma placa ou por onde a suíte anda não
        muda nada para o jogo, só troca o desenho do piso.
        """
        i = p[1] * W + p[0]
        return (p in todas and i not in escritas
                and (aplicado[i] & 0x3FF) in CARIMBOS)

    for p in sorted(plano_piso):
        if pintavel(p):
            i = p[1] * W + p[0]
            escritas[i] = (aplicado[i] & 0xFC00) | por_nome[plano_piso[p]]
            aplicado[i] = escritas[i]
            conta_chao[plano_piso[p]] += 1

    # -------------------------------------------------------------- PORTÕES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d células ficariam inalcançáveis, ex.: %s"
                         % (ALVO, len(perdidas), sorted(perdidas)[:6]))
    if depois - antes_alc:
        raise SystemExit("%s: o alcance a pé GANHOU célula" % ALVO)
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcançável"
                             % (ALVO, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (ALVO, "; ".join(queixas)))

    contas = dict(pracas=len(lista_pracas), celulas_praca=n_praca,
                  por_figura=dict(collections.Counter(f[0] for f in lista_pracas)),
                  moveis=dict(conta_mov), chao=dict(conta_chao),
                  fundos=dict(conta_fundo), solidos=len(novos_solidos),
                  postas=postas, lista_pracas=lista_pracas,
                  elegiveis={str(c): len(elegivel[c]) for c in CARIMBOS})
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


def base_de(guardado):
    """A grade como está no disco, só tirando o que ESTA passada escreveu."""
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def medir():
    """O orçamento desta cidade, sem plano nenhum. É o que o cabeçalho afirma."""
    loc_vivos, _usados = metatiles_vivos()
    livres = sorted(set(range(512)) - loc_vivos)
    alta = []
    for i in range(511, -1, -1):
        if i in loc_vivos:
            break
        alta.append(i)
    ts = _tileset(SECUNDARIO)
    print("%s é secundário de %d layout(s) e de %d mapa(s): %s"
          % (SECUNDARIO, len(IRMAOS), len(IRMAOS), ", ".join(IRMAOS)))
    print("metatiles: %d vivos, %d livres; faixa alta contígua %d a 511 (%d)"
          % (len(loc_vivos), len(livres), min(alta) if alta else -1, len(alta)))
    print("  primeiros livres: %s" % livres[:8])
    buracos = vagas_tile_livres()
    print("tiles: %d no tiles.png, %d buracos livres, teto %d"
          % (len(ts["tiles"]), len(buracos), TETO_TILES))
    for vaga, ind in sorted(vagas_pal_livres().items()):
        print("  vaga de paleta %2d: %2d índices que nenhum pixel vivo usa %s"
              % (vaga, len(ind), ind))
    gpx, gcores = granito_nosso()
    print("granito (fator %.2f): %s" % (FATOR_GRANITO, gcores))
    return 0


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
        print("  vaga %s: %d cores novas em índice que nenhum pixel vivo usava"
              % (vaga, n))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)

    guardado = carrega_plano()
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base_de(guardado))
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("\n%s: %d praças (%d células), %d células solidificadas, %d células "
          "mudadas" % (ALVO, contas["pracas"], contas["celulas_praca"],
                       contas["solidos"], len(escritas)))
    print("  chão:  " + ", ".join("%s x%d" % kv
                                  for kv in sorted(contas["chao"].items())))
    print("  móvel: " + ", ".join("%s x%d" % kv
                                  for kv in sorted(contas["moveis"].items())))
    print("  fundo: " + ", ".join("%s x%d" % kv
                                  for kv in sorted(contas["fundos"].items())))
    print("  régua: carimbo %d com %.1f%% de %d células ANTES; carimbo %d com "
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
    print("%s: desfeitas %d células" % (ALVO, n))
    return 0


# ------------------------------------------------------------------ conferência
def ids_topo_de(carimbos):
    """Os metatiles de célula ANDÁVEL de peça. Nesta passada não existe nenhum:
    todas as peças são de uma linha e sólidas por inteiro. A função continua
    aqui porque o portão que a usa tem que continuar existindo."""
    return [g for mv in carimbos["moveis"] for grade in mv["grades"].values()
            for li, linha in enumerate(grade)
            for ci, g in enumerate(linha) if not mv["solidas"][li][ci]]


def confere(tiles_novos, metas, attrs, carimbos, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela é chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que
    tem que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida só no caminho feliz não é regra.
    """
    import render_maps as RM
    from PIL import Image
    mau = []
    dados = kit()
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    base_tij, attr_chao = chao_nosso(CARIMBO_TIJOLO)
    base_laj, _al = chao_nosso(CARIMBO_LAJE)
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

    # ------------------------------------------------------------ 1. orçamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    if set(tiles_novos) & PINOS_ANIM:
        mau.append("o kit ocupa vaga de PINO de animação: %s"
                   % sorted(set(tiles_novos) & PINOS_ANIM))
    livres = dados["vagas_livres"]
    for vaga, cores in sorted(dados["paletas"].items()):
        if not 6 <= int(vaga) <= 12:
            mau.append("a vaga %s não é de secundário" % vaga)
        antigo = ts["paletas"][int(vaga)]
        vagos = set(livres.get(vaga) or [])
        for i in range(1, 16):
            if tuple(cores[i]) != tuple(antigo[i]) and i not in vagos:
                mau.append("a vaga %s mudou a cor do índice %d, que algum pixel "
                           "nosso usa" % (vaga, i))
        nz = [tuple(c) for c in cores[1:] if tuple(c) != (0, 0, 0)]
        if len(nz) > 15:
            mau.append("a vaga %s tem %d cores não-zero" % (vaga, len(nz)))

    # ------ 2. CHÃO novo: atributo IGUAL ao do carimbo e camada de cima VAZIA
    ids_chao = [c["mt"] for c in carimbos["chao"]]
    for c in carimbos["chao"]:
        if atributo(c["mt"]) != attr_chao:
            mau.append("o chão %d tem atributo 0x%04X e o carimbo tem 0x%04X"
                       % (c["mt"], atributo(c["mt"]), attr_chao))
        if any(e & 0x3FF for e in entradas(c["mt"])[4:]):
            mau.append("o chão %d usa a camada de cima, que com layerType "
                       "NORMAL desenha ACIMA do jogador" % c["mt"])

    # ------ 3. MÓVEL: COVERED, comportamento zerado, e o NOSSO chão embaixo
    fundos = {"tijolo": tuple(base_tij), "laje": tuple(base_laj)}
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
            mau.append("o móvel %d (%s) não está em COVERED" % (gid, nome))
        if a & 0xFF:
            mau.append("o móvel %d importou comportamento 0x%02X da fonte"
                       % (gid, a & 0xFF))
        if tuple(entradas(gid)[:4]) != fundos[fundo]:
            mau.append("o móvel %d não tem o nosso chão na camada de baixo" % gid)
    for gid, (nome, fundo) in sorted(ids_topo.items()):
        if atributo(gid) != attr_chao:
            mau.append("o topo %d (%s) não herdou o atributo do carimbo"
                       % (gid, nome))
        if tuple(entradas(gid)[:4]) != fundos[fundo]:
            mau.append("o topo %d não tem o nosso chão na camada de baixo" % gid)
        if sum(opac(e) for e in entradas(gid)[4:]) >= 4 * 64:
            mau.append("o topo %d tapa o jogador inteiro (E3)" % gid)

    # ------ 4. nenhuma variante de chão é cópia pixel a pixel de outra, NEM de
    #        um chão que a cidade JÁ desenha. A segunda metade é mais dura que a
    #        de Jubilife de propósito: aqui existem nove peças de laje prontas no
    #        tileset (536 a 538, 544 a 546, 552 a 554), e clonar uma delas numa
    #        vaga nova dividiria a contagem da régua sem mudar um pixel na tela.
    JA_DESENHA = [512, 513, 514, 520, 521, 522, 535, 536, 537, 538, 544, 545,
                  546, 551, 552, 553, 554]
    lista = ids_chao + JA_DESENHA
    pix = {mt: px_de(mt) for mt in lista}
    for i, a in enumerate(lista):
        for b in lista[i + 1:]:
            if a in JA_DESENHA and b in JA_DESENHA:
                continue        # o que já estava no tileset não é conta minha
            dd = sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
                     for p, q in zip(pix[a], pix[b])) / 256.0
            if dd < PISO_VARIA:
                mau.append("as variantes de chão %d e %d têm distância %.1f, "
                           "abaixo do piso de %.1f do varia_carimbo.py: isso é "
                           "enganar a régua" % (a, b, dd, PISO_VARIA))

    # ------------------------------------------------ 5 a 11. o plano do mapa
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
            mau.append("%s: mudou ELEVAÇÃO em (%d,%d)" % (ALVO, x, y))
        if cv and not cn:
            mau.append("%s: colisão 1 -> 0 em (%d,%d), que segue proibida"
                       % (ALVO, x, y))
        if velho not in CARIMBOS:
            mau.append("%s: peça escrita fora do carimbo em (%d,%d)"
                       % (ALVO, x, y))
        if novo in meus_chaos or novo in ids_topo:
            if cn != cv:
                mau.append("%s: chão ou topo mudou colisão em (%d,%d)"
                           % (ALVO, x, y))
        elif novo in ids_solido:
            if cv or not cn:
                mau.append("%s: móvel em (%d,%d) não é solidificação 0 -> 1"
                           % (ALVO, x, y))
            if (x, y) in ev:
                mau.append("%s: móvel em cima do evento (%d,%d)" % (ALVO, x, y))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) é de fora do kit"
                       % (ALVO, novo, x, y))

    # 6. (comportamento, layerType) de toda célula ANDÁVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: célula andável (%d,%d) mudou (comportamento, "
                       "layerType)" % (ALVO, i % W, i // W))
            break

    # 7. os DOIS portões de alcance
    ini = E.partidas(d, W, H, v)
    antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
    solid = {(i % W, i // W) for i in escritas
             if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
    if (antes - depois) - solid:
        mau.append("%s: o alcance a pé perdeu %d células além das solidificadas: "
                   "%s" % (ALVO, len((antes - depois) - solid),
                           sorted((antes - depois) - solid)[:6]))
    if depois - antes:
        mau.append("%s: o alcance a pé GANHOU célula" % ALVO)
    mau += ["%s: %s" % (ALVO, q) for q in
            ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                            solid)]

    # 8. O PISO NOVO NÃO PODE SER ADIVINHÁVEL, e o teste tem dois lados.
    #  (a) PADRÃO: nenhuma projeção simples da posição pode ADIVINHAR a peça. A
    #      conta é por EIXO (x, y, x+y, x-y) e por MÓDULO de 2 a 8. O piso não é
    #      o chute cego cru: as MESMAS posições recebem rótulo por um hash
    #      independente (três sementes de controle) e o maior ganho que o acaso
    #      produz ali é o que a distribuição de verdade tem direito de ter, mais
    #      a margem de 12 pontos.
    #  (b) FORMA: o piso novo tem que ser ÁREA, não sal e pimenta.
    mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
              if (val & 0x3FF) in meus_chaos}
    if len(mancha) < 400:
        mau.append("%s: só %d células de piso novo" % (ALVO, len(mancha)))
    # O medalhão fica FORA desta conta de propósito: ele é figura desenhada, com
    # posição fixa no centro da praça, e não escolha por hash. A regra 8(a) mede
    # se o HASH virou padrão, e medir o medalhão com ela seria acusar o desenho
    # de ser desenho.
    ids_miolo = {c["mt"] for c in carimbos["chao"] if c["nome"] in MIOLOS}
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
            mau.append("%s: saber %s mod %d adivinha a peça em %.0f%% das "
                       "células contra %.0f%% do chute cego (ganho de %.2f "
                       "contra o piso de acaso %.2f): virou padrão"
                       % (ALVO, rot, mod, 100 * (ganho + cego), 100 * cego,
                          ganho, piso))
    if mancha:
        # A célula que virou MÓVEL é ponte, não barreira, e isto não é o portão
        # sendo afrouxado para passar: um banco plantado no meio da praça é um
        # BURACO no calçamento, não um pedaço de calçamento solto. Com o móvel
        # contado como barreira, esta cidade fechava com 550 células em 46
        # pedaços (11,96 de média, um centésimo abaixo do piso) e o que estava
        # sendo medido eram as 72 peças de mobiliário, não a forma do piso. O
        # portão continua com dentes: a célula que ficou com o CARIMBO, que é a
        # que de fato parte a mancha, continua sendo barreira, e foi ela que
        # reprovou a primeira versão desta passada com 5,9 de média.
        ponte = {(i % W, i // W) for i in escritas
                 if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
        anda = set(mancha) | ponte
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
                    if rr in anda and rr not in vistos:
                        vistos.add(rr)
                        pilha.append(rr)
        if len(mancha) / pedacos < 12.0:
            mau.append("%s: o piso novo tem pedaço médio de só %.1f células "
                       "(%d em %d pedaços): virou sal e pimenta, não área"
                       % (ALVO, len(mancha) / pedacos, len(mancha), pedacos))

    # 9. a régua tem que fechar
    b, _nb, _idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("%s: a régua ainda marca %.1f%% de carimbo dominante"
                   % (ALVO, b))

    # 10. PEÇA INTEIRA NO MAPA: cada peça anotada no plano está no mapa com
    #     TODAS as células dela, e nenhuma célula de peça está fora de uma peça
    #     anotada. A conta NÃO pode ser por metatile, porque metatile de peça é
    #     COMPARTILHADO entre as três versões de fundo.
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
                    mau.append("%s: a peça %s em (%d,%d) devia ter o metatile "
                               "%d em (%d,%d) e tem %d"
                               % (ALVO, nome, x0, y0, gid, x, y, saida[j] & 0x3FF))
                if bool(mv["solidas"][li][ci]) != bool((saida[j] >> 10) & 3):
                    mau.append("%s: a célula (%d,%d) da peça %s tem a colisão "
                               "errada" % (ALVO, x, y, nome))
    de_peca = set(ids_solido) | set(ids_topo)
    for i, val in escritas.items():
        if (val & 0x3FF) in de_peca and (i % W, i // W) not in cobertas:
            mau.append("%s: a célula (%d,%d) tem metatile de peça (%d) e não "
                       "pertence a peça nenhuma do plano"
                       % (ALVO, i % W, i // W, val & 0x3FF))
            break

    # 11. NENHUM MÓVEL EM CORREDOR DA SUÍTE. O T176 anda por esta cidade com
    #     pernas SATURANTES medidas tile a tile, e peça nova numa delas encurta a
    #     perna sem quebrar portão de arquivo nenhum.
    corredor = E.corredores_de_teste(ALVO, v, W, H, d) | corredor_largo(v, W, H, d)
    for x, y in sorted(solid):
        if (x, y) in corredor:
            mau.append("%s: móvel sólido em (%d,%d), que é corredor de caso da "
                       "suíte" % (ALVO, x, y))
            break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferença" só vale depois que a comparação mostra que sabe reprovar.
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
            mau.append("SABOTAGEM NÃO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    W = plano[1]

    # N1. colisão 1 -> 0 numa célula de piso. A célula tem que ser de CHÃO e não
    #     a primeira escrita qualquer: se cair num móvel, o que a conferência
    #     acusa é "não é solidificação 0 -> 1", que é outra regra, e a prova
    #     negativa desta aqui não teria acontecido.
    ids_chao_demo = {c["mt"] for c in carimbos["chao"]}

    def n1():
        a = copia()
        _L, _W, _H, v, esc, _ct = a[4]
        i = sorted(j for j in esc if (esc[j] & 0x3FF) in ids_chao_demo)[0]
        v[i] = v[i] | (1 << 10)          # a célula ERA sólida
        return a
    sabota("colisão 1 -> 0", n1, "colisão 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        _L, _W, _H, v, esc, _ct = a[4]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | ((((v[i] >> 12) + 1) & 0xF) << 12)
        return a
    sabota("elevação alterada", n2, "mudou ELEVAÇÃO")

    # N3. comportamento importado num metatile de CHÃO
    def n3():
        a = copia()
        gid = carimbos["chao"][0]["mt"]
        a[2][gid - 512] = (a[2][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chão sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = sorted(g for mv in carimbos["moveis"]
                     for grade in mv["grades"].values()
                     for li, linha in enumerate(grade)
                     for ci, g in enumerate(linha) if mv["solidas"][li][ci])[0]
        a[2][gid - 512] = a[2][gid - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no móvel", n4, "não está em COVERED")

    # N5. peça de chão com a camada de cima ligada: piso que desenha ACIMA do
    #     jogador não é piso, e é por isso que as nove peças de laje que o
    #     tileset já tem não podiam ser usadas para plantar praça
    def n5():
        a = copia()
        gid = carimbos["chao"][0]["mt"]
        ent = list(a[1][gid - 512])
        ent[4] = ent[0]
        a[1][gid - 512] = ent
        return a
    sabota("chão com camada de cima", n5, "usa a camada de cima")

    # N6. camada de BAIXO de um móvel sabotada (a arte no lugar do nosso chão)
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

    # N7. peça escolhida por (x + y) % n, que é xadrez com período
    def n7():
        original = globals()["peca_da_lista"]
        globals()["peca_da_lista"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            a = (dict(tiles_novos), dict(metas), dict(attrs),
                 json.loads(json.dumps(carimbos)),
                 plano_mapa(carimbos, base_de(guardado)))
        finally:
            globals()["peca_da_lista"] = original
        return a
    sabota("piso por (x+y) % n", n7, "virou padrão")

    # N8. corredor fechado que PARTE um pedaço de chão. O portão de alcance
    #     sozinho não pega isso quando há warp dos dois lados.
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
        raise SystemExit("não achei ponto de articulação para a sabotagem N8")
    sabota("corredor fechado", n8, "se partiu")

    # N9. uma variante de chão CLONADA de uma peça que a cidade já desenha: é
    #     enganar a régua sem mudar um pixel na tela, e é a tentação desta
    #     cidade, porque as nove peças de laje já existem prontas
    def n9():
        a = copia()
        alvo = [c["mt"] for c in a[3]["chao"]
                if c["nome"] == "laje virada"][0]
        a[1][alvo - 512] = _metatile_ents(CARIMBO_LAJE)
        return a
    sabota("chão clonado do que a cidade já desenha", n9, "abaixo do piso de")

    # N10. cor nova escrita num índice que os NOSSOS pixels já usam
    def n10():
        a = copia()
        dados = kit()
        # A vaga 6 está INTEIRA livre, então sabotar dentro dela não prova nada.
        # A sabotagem entra por uma vaga que TENHA índice ocupado, escrevendo cor
        # nova justamente nele, que é o único jeito de a escrita estragar o
        # desenho de quem já estava lá.
        for vaga, livres_da in sorted(dados["vagas_livres"].items()):
            usados = [i for i in range(1, 16) if i not in set(livres_da)]
            if not usados:
                continue
            pal = [list(c) for c in _tileset(SECUNDARIO)["paletas"][int(vaga)]]
            pal[usados[0]] = [255, 0, 255]
            dados["paletas"][vaga] = pal
            break
        with open(KIT_JSON + ".sab", "w") as f:
            json.dump(dados, f)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        return a
    try:
        sabota("cor nova em índice já usado", n10, "que algum pixel nosso usa")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # N11. móvel sólido plantado num corredor do T176
    def n11():
        a = copia()
        _L, _W, _H, v, esc, ct = a[4]
        H = plano[2]
        d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
        corredor = E.corredores_de_teste(ALVO, v, W, H, d) | corredor_largo(v, W, H, d)
        gid = ct["postas"][0]
        mv = [m for m in carimbos["moveis"] if m["nome"] == gid[0]][0]
        alvo_mt = mv["grades"][gid[1]][0][0]
        for (x, y) in sorted(corredor):
            i = y * W + x
            if i in esc or ((v[i] >> 10) & 3):
                continue
            esc[i] = (v[i] & 0xF000) | (1 << 10) | alvo_mt
            ct["postas"].append([gid[0], gid[1], x, y])
            return a
        raise SystemExit("não achei célula de corredor livre para a sabotagem N11")
    sabota("móvel em corredor da suíte", n11, "corredor de caso da suíte")

    # ------------------------------------------------ o que está NO DISCO
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    png.load()
    pxd = png.load()
    n_disco = len(meta_disco) // 16
    postas = [l for l in metas
              if l < n_disco and _entradas(meta_disco, l) == metas[l]]
    if not postas:
        print("aviso: o kit ainda não foi aplicado no tileset; o caso de DISCO "
              "não roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit está pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ents in metas.items():
            if local >= n_disco or _entradas(meta_disco, local) != ents:
                mau.append("metatile %d no disco não é o do kit" % (512 + local))
            elif struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco não é o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if y0 + 8 > png.size[1]:
                mau.append("a vaga de tile %d não cabe no tiles.png" % vaga)
                continue
            if [[pxd[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco não é o do kit" % vaga)
        for vaga, cores in sorted(kit()["paletas"].items()):
            arq = [l.split() for l in
                   open(f"{DESTINO}/palettes/%s.pal" % vaga.zfill(2)).read().split("\n")[3:]
                   if l.strip()]
            if [[int(z) for z in c] for c in arq[:16]] != cores:
                mau.append("a paleta %s no disco não é a do kit" % vaga)

    # ------------------------------------------------------- idempotência
    _L, _W, _H, v, escritas, _ct = plano
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    volta = list(saida)
    for i in sorted(escritas):
        if volta[i] == escritas[i]:
            volta[i] = v[i]
    if volta != list(v):
        mau.append("%s: desfazer não devolve a base" % ALVO)
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
    print("DEMO VERDE: %d tiles, %d metatiles, %d células mudadas, %d "
          "solidificadas, régua %.1f%% -> %.1f%%"
          % (len(tiles_novos), len(metas), len(escritas), contas["solidos"],
             a, b))
    print("  %d provas negativas:" % len(negativas))
    for nome, queixa in negativas:
        print("    %-38s -> %s" % (nome, queixa[:100]))
    return 0


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--medir" in sys.argv:
        return medir()
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
