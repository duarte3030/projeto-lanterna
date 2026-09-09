#!/usr/bin/env python3
"""Refino de `SunyshoreCity` (tema ORLA), no `gTileset_Sunnyshore`, com os móveis
de cais importados do `Pokémon Light Platinum`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py` nesta
árvore em 09/09/2026: das 893 células andáveis de exterior, **356 (39,9%) são o
metatile 268**, a terra batida do `gTileset_GeneralSinnoh`, e **326 (36,5%) são o
metatile 562**, a prancha branca da passarela do `gTileset_Sunnyshore`. Os dois
juntos comem 76,4% do chão. É a cidade mais pobre das cinco que faltavam nesta
onda, e o defeito é literal: dois tapetes lisos, um marrom e um branco, do começo
ao fim.

DOIS CARIMBOS, e nenhum deles pode ser ignorado. A régua mede o DOMINANTE, então
quebrar só a terra faz a passarela assumir o posto (326 de 893 continuam sendo
36,5%) e a conta não fecha. Pior: solidificar célula tira do denominador, então
derrubar um carimbo SOBE a fração do outro. As duas famílias são tratadas juntas,
cada uma com o próprio catálogo, o próprio atributo e as próprias bolhas.

    carimbo    metatile  atributo  células  elevações
    terra           268    0x00A0      356  3 (216) e 4 (140)
    passarela       562    0x0000      326  4 (306) e 15 (20)

O ATRIBUTO 0x00A0 DA TERRA É `MB_BERRY_TREE_SOIL`, e ele NÃO é escolha desta
passada: é o que o conversor do demake carimbou nas 356 células, e o portão 4 do
`portao_planta.py` cobra `(behavior, layerType)` idêntico em toda célula que
continua andável. Portanto TODA variante de chão de terra sai com o atributo
0x00A0 bit a bit, e nenhuma constante de berry é tocada.

AS 20 CÉLULAS DE ELEVAÇÃO 15 DA PASSARELA FICAM DE FORA, e isso é decisão com
motivo escrito: elevação 15 é `ELEVATION_MULTI_LEVEL`, e em Sunyshore ela marca
exatamente os CRUZAMENTOS da passarela que o conserto de 06/09/2026 arrumou (a
seção "As passarelas de Sunyshore param de comer o sprite" do `ESTADO.md`).
Pintar um cruzamento não quebraria nenhum portão, mas mexer no que outra frente
acabou de consertar é risco sem prêmio. A terra usa as DUAS elevações dela, 3 e
4, porque as duas são chão de plateau liso (conferido célula a célula na máscara
do render): elevação ali é altura de terraço, não material.

A FONTE, e por que ela é essa. Foram medidos os secundários de TODAS as 17 ROM
hacks da pasta privada (`fontes-mapas/romhacks`), por metatile e não por paleta:
para cada tileset, quantos metatiles de CHÃO (arte só na camada de baixo, não
liso) têm cor média perto da nossa terra (155,114,114) e da nossa passarela
(207,219,234). O resultado foi o oposto do esperado e mudou o desenho:

  - PARA A PASSARELA NÃO EXISTE FONTE. Os 370 metatiles de chão a menos de 13 de
    distância da nossa prancha estão TODOS em tileset de NEVE ou de gelo (o
    `0x2D5094` e o `0x2D4E24` do FireRed, que 11 hacks herdam, o `0x2D4DDC` do
    Sword and Shield, o `0x3DFB84` do Golden Glazed). Casam de cor porque neve é
    branca, e nenhum deles é passarela. A busca foi refeita por ESTRUTURA, atrás
    de tile em faixas horizontais como o nosso 0x293, e deu na mesma neve. O
    secundário costeiro do Light Platinum, que é a fonte de orla desta onda, tem
    distância MÍNIMA de 74 até a nossa prancha: o calçadão dele é bege
    (201,193,165).
  - PARA A TERRA a fonte também não serve. O melhor candidato do Light Platinum
    (o par `0x286CF4`/`0x286D6C`, locais 16 a 23, distância 12,4) é uma FLOR
    gigante de tapete de laboratório, não chão; o filtro de "arte só na camada
    de baixo" o marcou como piso e o olho o reprovou.

Por isso a divisão desta passada é esta, e cada metade tem o motivo medido:

  - A PASSARELA é montada com tiles NOSSOS, que ali existem de verdade: a prancha
    estreita do próprio carimbo (`0x293`), a prancha LARGA (`0xE3`, uma linha a
    cada quatro em vez de a cada duas) e a chapa pontilhada (`0x116` e `0x2ED`).
    Seis metatiles novos, ZERO tile e ZERO cor.
  - A TERRA é IMPORTADA, e só quatro tiles 8x8: a terra moteada do secundário
    `0x286E8C` do mesmo hack (os tiles `0x203`, `0x204`, `0x213` e `0x214`, que
    são a camada de baixo dos metatiles 1 e 7 dele). Sete metatiles novos saem de
    arranjos e espelhos desses quatro, com distância pixel a pixel de 18,2 a 44,2
    entre eles e de 36,8 a 43,4 do carimbo.

POR QUE A TERRA NÃO PODE SER NOSSA, e este é o número que decidiu o desenho. A
primeira versão desta passada montou as variantes de terra com os tiles marrons do
nosso próprio primário (`0x108`, `0x118`, `0x1D3`, `0x1D5`, `0x1D8`, `0x1D9`,
`0x0F` e `0x1F`), e a medida reprovou: as nove composições ficaram entre 3,0 e 11,0
de distância pixel a pixel umas das outras, e o `varia_carimbo.py` documenta, com
caso concreto do `gTileset_Mauville`, que 7,7 é "invisível em jogo". Trocar chão
por chão que ninguém enxerga derruba a régua sem mudar a tela, que é exatamente o
que a trava de 8,0 existe para proibir. Terra é assim: a diferença entre duas
manchas de terra são uns poucos pixels de salpico.

E POR QUE A PRIMEIRA LISTA DE METATILES NOSSOS INTEIROS CAIU, que é o outro erro
desta passada e ele foi visto no render, não na planilha. A primeira versão usou
metatiles do nosso primário que tinham a cor certa (116, 137, 256, 258, 260, 264,
269, 273, 274, 332) e o desenho saiu com TRACINHOS VERDES espalhados pelo chão
marrom e pela passarela branca: quase todos eles são peças de TRANSIÇÃO do demake e
carregam a beirada de grama do mapa vizinho. Medido depois, pixel a pixel: de 4 a 16
pixels verdes em cada um. Contando só quem não tem UM pixel verde, o nosso primário
fica com 116 e 137 para a terra, que são lascas de estrato de penhasco e leem como
cunhas claras quando espalhadas, e nada que sirva de variante sutil.

OS MÓVEIS, do `Pokémon Light Platinum`, de WesleyFG, base Ruby (AXVE), md5
`7fd2c08735459d99fa23fdaa9b755486`. O par é o primário de exterior `0x286CF4`
com o secundário costeiro `0x286D54`, o mesmo que o `costa_sandgem.py` usou para
a praia de Sandgem, e as peças são OUTRAS: o que veio para cá é o vocabulário de
CAIS, que é o que Sunyshore pede e o demake não trouxe (conferido no atlas dos
512 metatiles do nosso secundário: não há um tambor, uma boia, um cabo de
amarração nem um poste de luz em lugar nenhum).

    boia salva-vidas   local  17   tambor de cais     local 382
    balde do pescador  local 374   cabo de amarração  local 398 (laranja)
    cabo de amarração  local 375 (azul)               poste de amarração  local 391
    guarda-sol fechado local 127   quadro de avisos   local 395
    poste do cais      local 396   pilar de corrimão  local  16
    poste de luz       locais 381 (topo) e 389 (base), bloco de duas células

O ORÇAMENTO DE PALETA fechou em DUAS vagas, e isso não foi sorte: a arte de TODOS
esses móveis mora na camada de CIMA da fonte, pintada com as paletas 0 e 1 do
hack; a camada de baixo deles é o calçadão bege do hack (paleta 9), que esta
passada JOGA FORA e substitui pelo nosso chão entrada por entrada. Medindo por
metatile VIVO (os que aparecem no `map.bin` de um dos três layouts do tileset),
as vagas 6, 7, 8, 9 e 12 do `gTileset_Sunnyshore` estão 100% livres: nenhum pixel
que chega à tela pinta com elas. A armadilha 4 do `compacta_paletas.py` (metatile
do PRIMÁRIO alcançável pintando com vaga de secundário) foi conferida e dá ZERO
aqui. Vão TRÊS: a paleta 0 do hack para a vaga 6, a paleta 1 para a vaga 7 e a
paleta 6 do outro secundário (a da terra moteada) para a vaga 8. Sobram a 9 e a 12
inteiras.

O QUE FICOU DE FORA, e por quê:

  - A PALMEIRA (locais 137, 138, 145, 146, 153 e 154 do hack) e o GUARDA-SOL
    ABERTO (109, 110, 117, 118, 125, 126). Sunyshore é a cidade do FAROL no
    leste de Sinnoh, que é região de clima frio: o demake desenhou pinheiro na
    borda oeste do mapa, e coqueiro ao lado de pinheiro não lê como orla, lê como
    erro de mapa. É a mesma razão pela qual o guarda-sol saiu de Sandgem.
  - Os BOTES do hack (locais 142, 143 e 164) e o cais sobre água (336 a 351).
    Eles pediriam solidificar célula de ÁGUA, e água em Sunyshore é a superfície
    de surf que liga a cidade à Route 223 e ao farol. Um portão de alcance DA
    ÁGUA, como o do `porto_canalave.py`, teria que entrar junto, e o prêmio é
    zero na régua (água não entra no denominador). Fica para quem quiser fazer o
    porto de Sunyshore com o cuidado que ele merece.
  - O CALÇADÃO BEGE da fonte, sempre: a camada de baixo dos móveis é o piso do
    hack e ela é achada por EVIDÊNCIA e não por constante
    decorada: todo padrão de camada de baixo que aparece em 4 ou mais metatiles
    diferentes da fonte é piso dela, e camada de baixo que repete o mesmo tile
    nos quatro quadrantes também é.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado. Só
    ARTE. Comportamento é id semântico: todo móvel entra com comportamento
    ZERADO e `layerType` COVERED (0x1000).

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHÃO NOVO é metatile com arte só na camada de BAIXO e atributo IGUAL, bit a
    bit, ao do carimbo que ele substitui (0x00A0 na terra, 0x0000 na passarela).
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO chão entrada por entrada, e o atributo é comportamento ZERADO
    com layerType COVERED (0x1000), que põe as duas camadas ABAIXO do sprite.
  - CADA PEÇA SABE SOBRE QUAL CARIMBO ELA POUSA. O tambor pousa na terra e recebe
    a camada de baixo do 268; a boia pousa na passarela e recebe a do 562. Sem
    isso a boia chegaria com um quadrado de terra em volta no meio do calçadão.
  - QUADRANTE DE BAIXO SOBE quando o de cima está vazio, que é a regra do
    `porto_canalave.py`.
  - A MANCHA É BOLHA, não sal e pimenta, e o auto-teste prova isso comparando o
    tamanho médio do pedaço conexo com o de uma sabotagem que espalha as MESMAS
    células ao acaso.
  - OS CORREDORES DA SUÍTE são congelados DUAS vezes, e a segunda é desta passada.
    O `enfeita_cidades.corredores_de_teste` simula a caminhada dos casos com a
    regra de elevação "0 é curinga e o resto exige igualdade", que é FALSA em
    Sunyshore: as passarelas têm 68 células de elevação 15
    (`ELEVATION_MULTI_LEVEL`, que mantém a elevação do jogador), e com a regra
    velha a simulação para na primeira delas. Medido: o corredor saía com 72
    células, duas peças desta passada caíam dentro da rota do T103.3, em (30,11) e
    (43,14), e o caso do rival abria VERMELHO. A `corredores_multinivel` refaz a
    conta com 0 e 15 como curingas e a união das duas é que vira gelo.

Uso:
    python3 dev_scripts/orla_sunyshore.py                  # mede e mostra o plano
    python3 dev_scripts/orla_sunyshore.py --aplicar        # escreve tileset e mapa
    python3 dev_scripts/orla_sunyshore.py --desfazer       # devolve o map.bin
    python3 dev_scripts/orla_sunyshore.py --demo           # auto-teste
    python3 dev_scripts/orla_sunyshore.py --extrai         # regera o kit da ROM
    python3 dev_scripts/orla_sunyshore.py --so-tileset     # so o tileset, sem mapa
    python3 dev_scripts/orla_sunyshore.py --prova-tiles    # o kit contra a ROM

O PLACAR desta passada, medido nesta árvore em 09/09/2026: 435 células escritas,
64 delas solidificadas, 341 de mancha; a régua cai de 39,9% para 18,3% (o carimbo
268 vai de 356 para 152 células de 829 andáveis) e o `liso3` de 81,6% para 35,5%;
38 tiles novos (vagas 416 a 453 de 512), 27 metatiles novos (locais 218 a 244) e
três vagas de paleta; +928 bytes de ROM.
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

# O `enfeita_cidades.py` PULA o próprio bloco de teste quando varre os corredores
# que a suíte anda, e a razão e circularidade: o bloco desta passada e derivado
# DO desenho, e não o contrário. Aqui o bloco próprio e o 194, e o 175 volta a
# ser um bloco como qualquer outro (ignorá-lo já custou um caso na rodada
# anterior desta onda). Medido nesta árvore: sem esta troca, os corredores do
# próprio T194 congelavam as células que o T194 existe para testar, e dois casos
# do bloco caíram sozinhos.
BLOCO_PROPRIO = "194_orla_sunyshore.json"
E.BLOCO_PROPRIO = BLOCO_PROPRIO

ALVO = "SunyshoreCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/sunnyshore"
KIT_JSON = f"{RAIZ}/dev_scripts/orla_sunyshore_kit.json"
PLANO = f"{RAIZ}/dev_scripts/orla_sunyshore.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_Sunnyshore"
# Os TRÊS layouts vivos que dividem o `gTileset_Sunnyshore`. Conferido lendo
# `data/layouts/layouts.json` e testando a existência do `map.bin` em disco.
IRMAOS = ["SunyshoreCity", "Route206", "Route223"]

TETO_TILES = 512
TETO_META = 512
TILE_LOCAL_0 = 416          # o tiles.png tem 416 tiles (128x208); sobram 96 vagas
META_LOCAL_0 = 218          # o maior local usado nos tres mapas e o 217
MARGEM = 2
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%
TETO_COR = 42.0             # distancia de cor media aceita entre chao novo e carimbo
PISO_VARIANTE = 8.0         # distancia pixel a pixel minima entre duas variantes
# Quanto uma projeção simples da posição (eixo x, y, x+y ou x-y, módulo 2 a 8)
# pode acertar a peça ALÉM do chute cego antes de a mancha virar "padrão". O
# número foi MEDIDO nesta cidade, com as bolhas desta passada, e não herdado: o
# plano de verdade chega a 5,6% (eixo y, módulo 8) e as três sabotagens de
# padrão chegam a 9,7% ((x+y) mod 6), 10,0% (x mod 8) e 15,5% (y mod 8). O corte
# de 8,0% fica entre os dois com folga dos dois lados. Ele e MAIS APERTADO que os
# 12% das passadas anteriores de propósito: aqui os grupos de bolha
# compartilham nomes, o que dilui qualquer padrão posicional, e o corte antigo
# deixaria de acusar as duas sabotagens mais fracas (medido: as duas passaram).
PISO_PADRAO = 0.08

# ------------------------------------------------------------------- a FONTE
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          pri=0x286CF4, split=(512, 512, 6))

# DOIS SECUNDÁRIOS DO MESMO PRIMÁRIO. O `0x286CF4` e o primário de exterior do
# hack, e ele aparece emparelhado com os dois secundários abaixo em mapas de
# verdade (o `0x286D54` em 8 mapas, o `0x286E8C` em 31), o que foi conferido
# lendo a tabela de layouts do inventário. Um kit só, duas leituras.
FONTES = dict(
    # o secundário COSTEIRO: e dele que vem todo o vocabulário de cais
    moveis=dict(sec=0x286D54, pal={0: 6, 1: 7}),
    # o secundário de CHÃO MOTEADO: dele vem só QUATRO tiles 8x8, que são a
    # terra granulada com que as sete variantes de chão desta cidade são
    # montadas.
    chao=dict(sec=0x286E8C, pal={6: 8}),
)

# PALETA DE ORIGEM -> VAGA NOSSA, por fonte. Três vagas ao todo: a arte dos
# móveis mora na camada de CIMA da fonte costeira, pintada com as paletas 0 e 1
# do hack, e o chão moteado usa só a paleta 6 do outro secundário.
VAGAS_PAL = {("moveis", 0): 6, ("moveis", 1): 7, ("chao", 6): 8}

# Os QUATRO tiles 8x8 de terra moteada que este kit traz do `0x286E8C`. Eles são
# a camada de baixo dos metatiles 1 e 7 daquele tileset, e as sete variantes de
# chão de terra são arranjos deles: quatro tiles pagam sete silhuetas.
TILES_CHAO_LP = [(0x203, 6), (0x204, 6), (0x213, 6), (0x214, 6)]

# Quantos metatiles DIFERENTES da fonte precisam repetir o mesmo PADRÃO de camada
# de baixo para ele ser piso dela. Mesmo corte do `costa_sandgem.py`, e conferido
# neste par: no secundário os padrões de piso aparecem 93, 31, 19, 18, 17, 15, 14,
# 13, 10 e 7 vezes e o primeiro padrão de ARTE aparece 3.
PISO_MIN = 4

CARIMBOS = dict(terra=268, passarela=562)
# Elevações que cada família aceita. A passarela recusa a 15
# (`ELEVATION_MULTI_LEVEL`), que marca os cruzamentos consertados em 06/09/2026.
ELEVACOES = dict(terra=(3, 4), passarela=(4,))

# ------------------------------------------------------------------ o CHÃO
# Cada variante e um METATILE MONTADO quadrante a quadrante, com arte SÓ na
# camada de baixo. Cada quadrante e `(fonte, tile, espelho_h)`, onde `fonte` e
# "nosso" (índice global de tile dos NOSSOS dois tilesets, que já estão na VRAM
# deste mapa e custam zero) ou "chão" (tile importado do `0x286E8C` do hack).
#
# POR QUE MONTAR EM VEZ DE COPIAR METATILE PRONTO, e a medida que decidiu isso.
# A primeira versão desta passada usou metatiles inteiros do nosso primário que
# tinham a cor certa (o 116, o 137, o 256, o 258, o 264, o 273 e o 274) e o
# render mostrou o defeito na cara: quase todos são peças de TRANSIÇÃO do demake
# e carregam a beirada VERDE da grama do mapa vizinho. Medido pixel a pixel: 8 a
# 16 pixels verdes em cada um deles, que viraram tracinhos verdes espalhados pelo
# chão marrom e pela passarela branca. Contando só quem não tem UM pixel verde,
# o nosso primário não tem variante de terra suficiente que passe no piso de 8,0
# de distância do `varia_carimbo.py`: as composicoes de terra nossa ficam entre
# 3,0 e 11,0 e o próprio `varia_carimbo.py` documenta que 7,7 e "invisível em
# jogo". Por isso a terra e IMPORTADA (quatro tiles do hack) e a passarela e
# montada com tiles NOSSOS, que ali existem de verdade: a prancha estreita do
# carimbo (0x293), a prancha LARGA (0xE3) e a chapa pontilhada (0x116, 0x2ED).
CHAO = [
    # --- TERRA, arranjos dos quatro tiles moteados do hack (distância pixel a
    # pixel entre eles: de 18,2 a 44,2; do carimbo: 36,8 a 43,4)
    dict(nome="terra de mare", sobre="terra", quads=[
        ("chao", 0x203, 0), ("chao", 0x204, 0), ("chao", 0x213, 0), ("chao", 0x214, 0)]),
    dict(nome="terra batida", sobre="terra", quads=[
        ("chao", 0x204, 0), ("chao", 0x203, 0), ("chao", 0x214, 0), ("chao", 0x213, 0)]),
    dict(nome="terra revirada", sobre="terra", quads=[
        ("chao", 0x213, 0), ("chao", 0x214, 0), ("chao", 0x203, 0), ("chao", 0x204, 0)]),
    dict(nome="terra pisada", sobre="terra", quads=[
        ("chao", 0x214, 0), ("chao", 0x213, 0), ("chao", 0x204, 0), ("chao", 0x203, 0)]),
    dict(nome="terra de mare espelhada", sobre="terra", quads=[
        ("chao", 0x203, 1), ("chao", 0x204, 1), ("chao", 0x213, 1), ("chao", 0x214, 1)]),
    dict(nome="terra grossa", sobre="terra", quads=[
        ("chao", 0x204, 0), ("chao", 0x204, 0), ("chao", 0x213, 0), ("chao", 0x213, 0)]),
    dict(nome="terra rasa", sobre="terra", quads=[
        ("chao", 0x203, 0), ("chao", 0x203, 0), ("chao", 0x214, 0), ("chao", 0x214, 0)]),
    # --- PASSARELA, tiles NOSSOS: 0x293 e a prancha estreita do carimbo, 0xE3 a
    # prancha LARGA (uma linha a cada quatro em vez de a cada duas), 0x116 e
    # 0x2ED a chapa pontilhada. Zero tile e zero cor novos.
    dict(nome="prancha larga", sobre="passarela", quads=[
        ("nosso", 0xE3, 0), ("nosso", 0xE3, 0), ("nosso", 0xE3, 0), ("nosso", 0xE3, 0)]),
    dict(nome="prancha e junta", sobre="passarela", quads=[
        ("nosso", 0x293, 0), ("nosso", 0x293, 0), ("nosso", 0xE3, 0), ("nosso", 0xE3, 0)]),
    dict(nome="junta e prancha", sobre="passarela", quads=[
        ("nosso", 0xE3, 0), ("nosso", 0xE3, 0), ("nosso", 0x293, 0), ("nosso", 0x293, 0)]),
    dict(nome="prancha alternada", sobre="passarela", quads=[
        ("nosso", 0x293, 0), ("nosso", 0xE3, 0), ("nosso", 0x293, 0), ("nosso", 0xE3, 0)]),
    dict(nome="prancha alternada b", sobre="passarela", quads=[
        ("nosso", 0xE3, 0), ("nosso", 0x293, 0), ("nosso", 0xE3, 0), ("nosso", 0x293, 0)]),
    dict(nome="chapa pontilhada", sobre="passarela", quads=[
        ("nosso", 0x293, 1), ("nosso", 0x116, 0), ("nosso", 0x116, 0), ("nosso", 0x116, 0)]),
]

# A paleta com que cada família pinta os tiles NOSSOS. E a paleta do próprio
# carimbo: a terra e a 3 do primário, a passarela e a 0.
PAL_NOSSA = dict(terra=3, passarela=0)

# ---------------------------------------------------------- os MÓVEIS do hack
MOVEIS_LP = [
    dict(nome="boia salva-vidas",     lp=17,  sobre="passarela"),
    dict(nome="cabo de amarracao",    lp=398, sobre="passarela"),
    dict(nome="poste de amarracao",   lp=391, sobre="passarela"),
    dict(nome="pilar de corrimao",    lp=16,  sobre="passarela"),
    dict(nome="tambor de cais",       lp=382, sobre="terra"),
    dict(nome="balde do pescador",    lp=374, sobre="terra"),
    dict(nome="cabo azul",            lp=375, sobre="terra"),
    dict(nome="guarda-sol fechado",   lp=127, sobre="terra"),
    dict(nome="quadro de avisos",     lp=395, sobre="terra"),
    dict(nome="poste do cais",        lp=396, sobre="terra"),
]

# BLOCOS DE DUAS CÉLULAS DE ALTURA, uma célula de largura. A linha de CIMA
# continua ANDÁVEL (a arte mora na camada de cima e o jogador passa ATRÁS dela) e
# a de BAIXO vira sólida em COVERED, que e o que faz o jogador parado ao sul
# aparecer NA FRENTE do pe do poste.
BLOCOS_LP = [
    dict(nome="poste de luz do calcadao", topo=[381], base=[389],
         sobre="passarela"),
    dict(nome="poste de luz da orla",     topo=[381], base=[389],
         sobre="terra"),
]

# O QUE A CIDADE LEVA, e quantas de cada peça.
TEMA = dict(
    # OS GRUPOS SÃO GRANDES DE PROPÓSITO. Grupo de uma peça só faz cada bolha
    # sair de uma cor única, e aí saber onde a célula está passa a adivinhar o
    # que ela e, que e o caso 11a do auto-teste.
    bolhas_terra=[
        dict(grupo=["terra de mare", "terra batida", "terra grossa",
                    "terra de mare espelhada"],               quantas=16, tam=(15, 28)),
        dict(grupo=["terra revirada", "terra pisada", "terra rasa"],
             quantas=16, tam=(14, 26)),
        dict(grupo=["terra grossa", "terra de mare espelhada",
                    "terra revirada", "terra de mare"],       quantas=16, tam=(13, 24)),
    ],
    # SEGUNDA FASE, e ela roda SÓ depois que a primeira não acha mais lugar. A
    # bolha pequena não pode disputar semente com a grande na mesma rodada: com
    # as quatro especificações juntas, medido, a regua PIOROU de 19,5% para
    # 20,6%, porque a pequena tomava as sementes boas e as grandes nasciam
    # curtas. Servida depois, ela só pega o que sobrou, que são os bolsoes de
    # oito a quinze células entre os predios.
    bolhas_terra2=[
        dict(grupo=["terra batida", "terra pisada", "terra rasa",
                    "terra de mare"],                 quantas=16, tam=(6, 14), piso=4),
    ],
    bolhas_passarela=[
        dict(grupo=["prancha larga", "prancha e junta",
                    "prancha alternada"],                     quantas=14, tam=(15, 28)),
        dict(grupo=["junta e prancha", "prancha alternada b",
                    "prancha larga"],                         quantas=14, tam=(14, 26)),
        dict(grupo=["chapa pontilhada", "prancha e junta",
                    "prancha alternada b", "junta e prancha"], quantas=14, tam=(13, 24)),
    ],
    bolhas_passarela2=[
        dict(grupo=["prancha larga", "prancha alternada",
                    "junta e prancha"],               quantas=14, tam=(6, 14), piso=4),
    ],
    moveis=[
        dict(nome="boia salva-vidas",   quantos=5, espaco=7),
        dict(nome="cabo de amarracao",  quantos=5, espaco=7),
        dict(nome="poste de amarracao", quantos=5, espaco=7),
        dict(nome="pilar de corrimao",  quantos=4, espaco=8),
        dict(nome="tambor de cais",     quantos=8, espaco=6),
        dict(nome="balde do pescador",  quantos=6, espaco=6),
        dict(nome="cabo azul",          quantos=5, espaco=7),
        dict(nome="guarda-sol fechado", quantos=5, espaco=7),
        dict(nome="quadro de avisos",   quantos=3, espaco=9),
        dict(nome="poste do cais",      quantos=3, espaco=9),
    ],
    blocos=[
        dict(nome="poste de luz do calcadao", quantos=7, espaco=6),
        dict(nome="poste de luz da orla",     quantos=8, espaco=6),
    ],
)

ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre dois moveis QUAISQUER
PISO_BOLHA = 6              # tamanho minimo de uma bolha que a regiao cortou

N4 = E.N4


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

    A pergunta nao e "o indice de tile e zero", e essa diferenca custou a
    primeira rodada desta passada: o carimbo 562 da passarela tem a camada de
    cima cheia de `0x0001`, e o tile 1 do primario nao tem um pixel aceso.
    Contar por indice diria que o carimbo desenha por cima do jogador, o que e
    falso, e o script parava sozinho.
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


def vagas_livres():
    """{vaga: [indices de cor que NENHUM pixel VIVO nosso usa]}.

    "Vivo" e a palavra que importa: o `gTileset_Sunnyshore` tem 512 metatiles e
    so 163 deles aparecem em `map.bin` de algum dos tres layouts com arquivo em
    disco. Contar os 512 daria vaga ocupada por lixo que nunca chega a tela.

    A ARMADILHA 4 do `compacta_paletas.py` (metatile do PRIMARIO alcancavel
    pintando com vaga de secundario) roda junto, porque "medi uma vez" nao e
    portao.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    usados = collections.defaultdict(set)
    vivos = set()
    for nome in IRMAOS:
        vivos |= {c & 0x3FF for c in G.grade(nome)[4]}
    for gid in sorted(x for x in vivos if x >= 512):
        local = gid - 512
        if local >= META_LOCAL_0:
            continue
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], local):
            if it == 0 or ip < 6:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        usados[ip].add(c)
    for gid in sorted(x for x in vivos if x < 512):
        for (it, fh, fv, ip) in RM.entradas_metatile(tp["metatiles"], gid):
            if it and ip >= 6:
                tile = RM.resolver_tile(tp, ts, it)
                if tile is None:
                    continue
                for linha in tile:
                    for c in linha:
                        if c:
                            usados[ip].add(c)
    return {v: [i for i in range(1, 16) if i not in usados[v]]
            for v in range(6, 13)}


# ---------------------------------------------------------------- a EXTRAÇÃO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb(ts, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits DESLOCADOS TRES
    casas, nao esticados para 0..255. Todo `.pal` deste repositorio esta nessa
    conta, e o `ferramentas/prova_extracao.py` tambem."""
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def _piso_da_fonte(tset):
    """Os tiles que a FONTE usa como piso, por evidencia e nao por decoreba.

    Duas assinaturas: (a) padrao de camada de baixo que aparece em PISO_MIN
    metatiles diferentes ou mais; (b) camada de baixo que repete o MESMO tile nos
    quatro quadrantes.
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


def extrai():
    """Regera `orla_sunyshore_kit.json` a partir da ROM privada do Light Platinum.

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
    tsec = {}
    for nome, f in FONTES.items():
        tsec[nome] = r.parse_tileset(f["sec"])
        if tsec[nome] is None:
            raise SystemExit("o par 0x%X / 0x%X do hack nao abriu"
                             % (LP["pri"], f["sec"]))
    if t1 is None:
        raise SystemExit("o primario 0x%X do hack nao abriu" % LP["pri"])
    NP = r.n_tiles_pri
    livres = vagas_livres()
    # A paleta de origem depende da FONTE: as vagas 0 a 5 são do primário, que e
    # o mesmo para as duas, e da 6 em diante são do secundário de cada uma.
    pal = {nome: {i: _rgb(t1 if i < 6 else tsec[nome], i) for i in range(16)}
           for nome in FONTES}
    piso = {nome: _piso_da_fonte(tsec[nome]) for nome in FONTES}

    def px_de(idx, fonte):
        return (_nibbles(t1["tiles"], idx) if idx < NP
                else _nibbles(tsec[fonte]["tiles"], idx - NP))

    def branco(v, fonte):
        """A entrada aponta para um tile 8x8 SEM UM PIXEL aceso? O tile 1 do
        primario do hack e todo transparente, e tratar isso como camada de cima
        cheia deixaria metade da peca VAZIA."""
        idx = v & 0x3FF
        if not idx:
            return True
        return not any(c for linha in px_de(idx, fonte) for c in linha)

    def eh_piso(v, fonte):
        return (v & 0x3FF) in piso[fonte]

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}

    def guarda(idx, ip, fonte):
        """Registra o tile 8x8 e devolve a chave dele.

        A CHAVE LEVA A FONTE E A PALETA DE ORIGEM: o mesmo indice 8x8 em dois
        secundarios diferentes e outro desenho, e o mesmo desenho pintado com
        duas paletas do hack tem que virar DUAS vagas nossas, senao a segunda
        apaga a primeira.
        """
        if (fonte, ip) not in VAGAS_PAL:
            return None
        ch = "%s:%d:%d" % (fonte, idx, ip)
        destino = VAGAS_PAL[(fonte, ip)]
        if tiles_vaga.setdefault(ch, destino) != destino:
            raise SystemExit("o tile %s foi pedido nas vagas %d e %d"
                             % (ch, tiles_vaga[ch], destino))
        tiles_px[ch] = px_de(idx, fonte)
        origem = pal[fonte][ip]
        tiles_cor.setdefault(ch, set())
        for linha in tiles_px[ch]:
            for c in linha:
                if c:
                    tiles_cor[ch].add(tuple(origem[c]))
        return ch

    # ---- os quatro tiles de CHÃO, pedidos por índice e não por metatile: o que
    # esta passada quer daquele tileset e a TEXTURA, e ela é remontada aqui.
    for idx, ip in TILES_CHAO_LP:
        if guarda(idx, ip, "chao") is None:
            raise SystemExit("o tile de chao 0x%X pede a paleta %d, fora do plano"
                             % (idx, ip))

    lista = [dict(nome=m["nome"], lp=m["lp"]) for m in MOVEIS_LP]
    for b in BLOCOS_LP:
        for papel, lst in (("topo", b["topo"]), ("base", b["base"])):
            for k, loc in enumerate(lst):
                lista.append(dict(nome="%s %s %d" % (b["nome"], papel, k), lp=loc))
    vistos = {}
    pecas = []
    for p in lista:
        # duas peças podem apontar para o MESMO local da fonte (os dois postes de
        # luz vem do mesmo desenho); o kit guarda uma entrada por NOME, e o
        # conteúdo sai igual porque a alocacao de tile e por chave.
        ents = list(struct.unpack_from("<8H", tsec["moveis"]["meta"], p["lp"] * 16))
        baixo, cima = ents[:4], ents[4:]
        # QUADRANTE DE BAIXO SOBE quando o de cima está vazio; quadrante promovido
        # que e PISO da fonte, ou que a fonte pinta com paleta fora do kit, e
        # DESCARTADO e recebe o NOSSO chão.
        usadas, saida = [], []
        for q in range(4):
            de_baixo = branco(cima[q], "moveis")
            v = baixo[q] if de_baixo else cima[q]
            if not (v & 0x3FF) or (de_baixo and eh_piso(v, "moveis")):
                usadas.append(None)
                saida.append(0)
                continue
            ch = guarda(v & 0x3FF, (v >> 12) & 0xF, "moveis")
            usadas.append(ch)
            saida.append(v if ch is not None else 0)
        if not any(usadas):
            raise SystemExit("%s: o metatile %d nao sobrou com nenhum quadrante "
                             "de arte" % (p["nome"], p["lp"]))
        pecas.append(dict(papel="movel", nome=p["nome"], lp=p["lp"],
                          ents=saida, usadas=usadas))
        vistos[p["nome"]] = p["lp"]

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

    # REINDEXA cada nibble para a tabela nova. A cor 0 continua 0 e nenhuma cor e
    # aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, só em
    # outro índice, entao o pixel sai idêntico ao da ROM.
    saida_tiles = {}
    for ch, vaga in tiles_vaga.items():
        fonte, _idx, ip = ch.split(":")
        origem = pal[fonte][int(ip)]
        saida_tiles[ch] = [[0 if c == 0 else indice[(vaga, tuple(origem[c]))]
                            for c in linha] for linha in tiles_px[ch]]

    dados = dict(
        fonte=dict(hack=LP["hack"], autor=LP["autor"], base=LP["base"],
                   arquivo=gba, md5=md5, pri="0x%X" % LP["pri"],
                   secs={k: "0x%X" % v["sec"] for k, v in FONTES.items()},
                   split=list(LP["split"]), n_tiles_pri=NP),
        vagas_pal={"%s:%d" % k: v for k, v in VAGAS_PAL.items()},
        vagas_livres={str(k): v for k, v in livres.items()},
        paletas=paletas, tiles=saida_tiles, tiles_vaga=tiles_vaga,
        piso_da_fonte={k: sorted(v) for k, v in piso.items()}, pecas=pecas)
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
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele).

    E o chao que todo movel pousa em cima e que toda peca de topo herda.
    """
    mt = CARIMBOS[qual]
    ents = ents_nossas(mt)
    if arte_em_cima(ents):
        raise SystemExit("o carimbo %d desenha na camada de cima" % mt)
    return ents[:4], attr_nosso(mt)


def _locais_livres():
    """Os locais de metatile em que esta passada pode gravar, em ordem. O portao
    de verdade (nenhum dos tres mapas usa o id) roda depois, no `desenha_kit`."""
    return list(range(META_LOCAL_0, TETO_META))


def px_metatile(ents, tp, ts, tiles_novos=None, paletas=None):
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
            cores = None
            if paletas:
                cores = paletas.get(str(ip))
            if cores is None:
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


def desenha_kit():
    """(tiles_novos, metas, attrs, catalogo), sem escrever em disco."""
    dados = kit()
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)

    por_peca = {p["nome"]: p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]
    metas, attrs = {}, {}
    vagas_meta = _locais_livres()
    proximo_meta = [0]
    catalogo = dict(chao={}, moveis={}, blocos={}, sobre={})

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            mapa_tile[chave] = proximo[0]
            tiles_novos[proximo[0]] = dados["tiles"][chave]
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
        """A entrada NOSSA para o quadrante q da peca: mesmo tile, vaga nova,
        vaga de paleta nova, e os bits de espelho da fonte preservados."""
        ch = p["usadas"][q]
        if ch is None:
            return None
        v = p["ents"][q]
        fonte, _idx, ip = ch.split(":")
        alvo_pal = VAGAS_PAL[(fonte, int(ip))]
        return ((v & 0x0C00) | (512 + vaga(ch)) | (alvo_pal << 12))

    def quadrante(qd, qual):
        """A entrada de 16 bits de um quadrante de chao.

        `("nosso", tile, fh)` aponta para um tile que JA esta na VRAM deste mapa
        e usa a paleta do proprio carimbo; `("chao", tile, fh)` aponta para um
        tile importado, que ganha vaga nova e a vaga de paleta do kit.
        """
        origem, idx, fh = qd
        if origem == "nosso":
            return (0x400 if fh else 0) | idx | (PAL_NOSSA[qual] << 12)
        ch = "%s:%d:%d" % (origem, idx, dict(TILES_CHAO_LP)[idx])
        alvo_pal = VAGAS_PAL[(origem, dict(TILES_CHAO_LP)[idx])]
        return (0x400 if fh else 0) | (512 + vaga(ch)) | (alvo_pal << 12)

    BASE = {}
    for qual in CARIMBOS:
        BASE[qual] = chao_nosso(qual)

    # ------------------------------------------------------ 1. CHÃO
    px_carimbo = {q: px_metatile(ents_nossas(CARIMBOS[q], tp, ts), tp, ts)
                  for q in CARIMBOS}
    for c in CHAO:
        qual = c["sobre"]
        _base, attr_carimbo = BASE[qual]
        ents = [quadrante(qd, qual) for qd in c["quads"]] + [0, 0, 0, 0]
        d = _dist_cor(_cor_media(px_metatile(ents, tp, ts, tiles_novos,
                                             dados["paletas"])),
                      _cor_media(px_carimbo[qual]))
        if d > TETO_COR:
            raise SystemExit("o chao %s esta a %.1f de cor do carimbo de %s, "
                             "acima do teto de %.1f"
                             % (c["nome"], d, qual, TETO_COR))
        catalogo["chao"][c["nome"]] = poe(ents, attr_carimbo)
        catalogo["sobre"][c["nome"]] = qual

    # ---------------------------------------------------- 2. MÓVEIS de 1 célula
    for m in MOVEIS_LP:
        p = por_peca[m["nome"]]
        cima = [entrada(p, q) or 0 for q in range(4)]
        if not any(cima):
            raise SystemExit("%s: peca sem arte" % m["nome"])
        base, _a = BASE[m["sobre"]]
        # comportamento ZERADO (nenhum id semantico e importado) e layerType
        # COVERED, que poe as duas camadas ABAIXO do sprite.
        catalogo["moveis"][m["nome"]] = poe(list(base) + cima, 0x1000)
        catalogo["sobre"][m["nome"]] = m["sobre"]

    # ------------------------------------------------- 3. BLOCOS de 2 células
    for b in BLOCOS_LP:
        base, attr_base = BASE[b["sobre"]]
        ids = {}
        for papel, lst, attr_peca in (("topo", b["topo"], attr_base),
                                      ("base", b["base"], 0x1000)):
            fora = []
            for k, _loc in enumerate(lst):
                p = por_peca["%s %s %d" % (b["nome"], papel, k)]
                cima = [entrada(p, q) or 0 for q in range(4)]
                if not any(cima):
                    raise SystemExit("%s: metade sem arte" % b["nome"])
                fora.append(poe(list(base) + cima, attr_peca))
            ids[papel] = fora
        catalogo["blocos"][b["nome"]] = dict(topo=ids["topo"], base=ids["base"])
        catalogo["sobre"][b["nome"]] = b["sobre"]

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))

    # A vaga de metatile só serve se NENHUM dos três mapas vivos usar o id. A
    # grade do ALVO entra pela base LIMPA desta passada, e não pelo disco: depois
    # de um `--aplicar` o disco já tem os ids que este kit acabou de escrever, e
    # o portão reprovaria a si mesmo na segunda rodada.
    guardado = carrega_plano()
    usados = set()
    for nome in IRMAOS:
        grade = base_de(nome, guardado) if nome == ALVO else G.grade(nome)[4]
        usados |= {c & 0x3FF for c in grade}
    for local in metas:
        if 512 + local in usados:
            raise SystemExit("algum dos tres mapas usa o metatile %d"
                             % (512 + local))
    return tiles_novos, metas, attrs, catalogo


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    Idempotente: as vagas de tile, de paleta e de metatile sao FIXAS.

    A ARMADILHA DO `Image.convert("P")`: numa imagem que JA e "P" ele devolve uma
    COPIA e nao converte, e uma frente desta onda gravou metatiles e NENHUM tile
    por causa disso. Aqui a imagem nova nasce em "P" e recebe a paleta da antiga.
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
    for v, tile in tiles_novos.items():
        x0, y0 = (v % cols) * 8, (v // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    novo.save(f"{DESTINO}/tiles.png")

    for vaga, cores in sorted(dados["paletas"].items()):
        _grava_pal(int(vaga), cores)

    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
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
                # ACEITA A BOLHA CURTA quando foi a REGIÃO que acabou, e não a
                # vontade de crescer: a passarela tem bracos de três células de
                # largura e exigir o tamanho cheio deixaria o braco liso.
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

    POR QUE ESTA FUNCAO EXISTE, e ela nasceu de um caso VERMELHO desta passada,
    nao de zelo. O `enfeita_cidades.corredores_de_teste` congela as celulas que
    a suite anda dentro do mapa, e ele simula a caminhada com a regra de
    elevacao do resto daquele arquivo: elevacao 0 e curinga e o resto exige
    igualdade. Em Sunyshore essa regra e FALSA, e a diferenca nao e teorica: as
    passarelas da cidade tem 68 celulas de ELEVACAO 15 (`ELEVATION_MULTI_LEVEL`,
    que MANTEM a elevacao do jogador em vez de exigir igualdade), e sao elas que
    ligam a praca da linha 7 ao resto. Com a regra de igualdade, a simulacao
    PARA na primeira celula 15 e o corredor sai curto: medido, 72 celulas, e sem
    a rota do T103.3 depois da coluna 27. Duas pecas desta passada cairam la
    dentro, em (30,11) e (43,14), e o T103.3 abriu VERMELHO com a cena do rival
    inalcancavel.

    Aqui a mesma simulacao roda com a regra certa (0 e 15 sao curingas dos dois
    lados), e o resultado e a UNIAO com o que a funcao original ja devolve: onde
    a original anda mais, ela vale; onde esta anda mais, esta vale. Corredor a
    mais custa enfeite a menos; corredor a menos custa caso vermelho.
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
    em duas.
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
    """(L, W, H, v, escritas, contas) para `SunyshoreCity`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()

    # As duas FAMÍLIAS de chão. Uma célula só e elegivel se ainda for o carimbo
    # puro, se estiver numa das elevações que a família aceita e se não for agua
    # para o motor.
    fam = {}
    for qual, mt in CARIMBOS.items():
        fam[qual] = {(i % W, i // W) for i in range(W * H)
                     if not ((v[i] >> 10) & 3) and (v[i] & 0x3FF) == mt
                     and ((v[i] >> 12) & 0xF) in ELEVACOES[qual]
                     and beh(v[i] & 0x3FF) not in AG}

    escritas = {}
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    gelo |= corredores_multinivel(v, W, H, d)
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

    # ------ 1. BLOCO DE DUAS CÉLULAS, antes da mobilia de uma célula, porque ele
    # precisa das duas células inteiras e a mobilia solta não pode ter comido
    # metade dele. A linha de CIMA continua ANDÁVEL; a de BAIXO vira sólida.
    conta_bloco = collections.Counter()
    por_bloco = []
    for b in TEMA["blocos"]:
        info = catalogo["blocos"][b["nome"]]
        qual = catalogo["sobre"][b["nome"]]
        larg = len(info["topo"])
        for x, y in ordem_cel:
            if conta_bloco[b["nome"]] >= b["quantos"]:
                break
            cels = [(x + i, y) for i in range(larg)] + \
                   [(x + i, y + 1) for i in range(larg)]
            if any(not livre(cx, cy, qual) for cx, cy in cels):
                continue
            if any(max(abs(x - px), abs(y - py)) < b["espaco"]
                   for px, py in por_bloco):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            topo = [(x + i, y) for i in range(larg)]
            for k, (cx, cy) in enumerate(topo):
                j = cy * W + cx
                escritas[j] = (aplicado[j] & 0xFC00) | info["topo"][k]
                aplicado[j] = escritas[j]
            ok = True
            for k, (cx, cy) in enumerate([(x + i, y + 1) for i in range(larg)]):
                if not tenta_solidificar(cx, cy, info["base"][k]):
                    ok = False
                    break
            if not ok:
                for cx, cy in cels:
                    j = cy * W + cx
                    if j in escritas and (cx, cy) not in novos_solidos:
                        del escritas[j]
                        aplicado[j] = v[j]
                for cx, cy in [(x + i, y + 1) for i in range(larg)]:
                    if (cx, cy) in novos_solidos:
                        novos_solidos.remove((cx, cy))
                        postos.remove((cx, cy))
                        del escritas[cy * W + cx]
                        aplicado[cy * W + cx] = v[cy * W + cx]
                continue
            por_bloco += cels
            postos += topo
            conta_bloco[b["nome"]] += 1

    # ------ 2. MÓVEIS de uma célula. Eles vem ANTES da mancha de propósito:
    # móvel posto no carimbo tira uma célula do numerador E do denominador da
    # regua; móvel posto em cima de uma mancha tira só do denominador, o que
    # PIORA a conta.
    lista = TEMA["moveis"]
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            m = lista[(giro + k) % len(lista)]
            if conta_mov[m["nome"]] >= m["quantos"]:
                continue
            qual = catalogo["sobre"][m["nome"]]
            if not livre(x, y, qual) or not espacado(m["nome"], m["espaco"], x, y):
                continue
            # móvel de cidade encosta em alguma coisa: ou num sólido, ou na OUTRA
            # família de chão. Peça solta no meio do vazio le como erro de mapa.
            outra = "passarela" if qual == "terra" else "terra"
            perto = any(0 <= x + dx < W and 0 <= y + dy < H
                        and (((aplicado[(y + dy) * W + x + dx] >> 10) & 3)
                             or (x + dx, y + dy) in fam[outra])
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

    for qual, chave, semente in (("terra", "bolhas_terra", 0x5EED),
                                 ("passarela", "bolhas_passarela", 0xB0A7),
                                 ("terra", "bolhas_terra2", 0x5EED ^ 0x1234),
                                 ("passarela", "bolhas_passarela2", 0xB0A7 ^ 0x1234)):
        livres = {p for p in fam[qual] if pintavel(p, qual)}
        for nomes, corpo in bolhas(livres, TEMA[chave], semente):
            for p in sorted(corpo):
                pinta(p, nomes)

    # -------------------------------------------------------------- PORTÕES
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
    contas = dict(moveis=dict(conta_mov), blocos=dict(conta_bloco),
                  manchas=dict(conta_mancha), solidos=len(novos_solidos),
                  terra=len(fam["terra"]), passarela=len(fam["passarela"]))
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
    ao mesmo lugar. A saida e a do `porto_canalave.py`: planejar sobre a base
    LIMPA desta passada e escrever por cima do disco.
    """
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    if tiles_novos:
        print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
              "novos (locais %d a %d, ids %d a %d)"
              % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
                 TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
                 max(metas), 512 + min(metas), 512 + max(metas)))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    base = base_de(ALVO, guardado)
    L, W, H, v, escritas, contas = plano_mapa(catalogo, base)
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("%s: %d celulas de mancha, %d solidificadas, %d mudadas "
          "(familia terra %d, passarela %d)"
          % (ALVO, sum(contas["manchas"].values()), contas["solidos"],
             len(escritas), contas["terra"], contas["passarela"]))
    print("  mancha: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["manchas"].items())))
    print("  movel:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    if contas["blocos"]:
        print("  bloco:  " + ", ".join("%s x%d" % kv
                                       for kv in sorted(contas["blocos"].items())))
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
def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def confere(tiles_novos, metas, attrs, catalogo, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela e chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que tem
    que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa certa.
    Regra conferida so no caminho feliz nao e regra.
    """
    mau = []
    dados = kit()
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
        return px_metatile(entradas(mt_id), tp, ts, tiles_novos, dados["paletas"])

    # ------------------------------------------------------------ 1. orçamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if tiles_novos and min(tiles_novos) < TILE_LOCAL_0:
        mau.append("o kit grava tile abaixo da primeira vaga livre (%d)"
                   % TILE_LOCAL_0)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    if metas and min(metas) < META_LOCAL_0:
        mau.append("o kit grava metatile abaixo da primeira vaga livre (%d)"
                   % META_LOCAL_0)
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

    # ---------- 2. o kit não pode importar paleta de origem fora de VAGAS_PAL
    for ch in dados["tiles"]:
        fonte, _idx, ip = ch.split(":")
        if (fonte, int(ip)) not in VAGAS_PAL:
            mau.append("o kit importou a paleta %s da fonte %s, fora do plano"
                       % (ip, fonte))

    # ---------- 3. CHÃO novo: atributo idêntico ao do carimbo, camada de cima
    # VAZIA e cor a menos de TETO_COR do carimbo
    px_carimbo = {q: px_de(CARIMBOS[q]) for q in CARIMBOS}
    for nome, gid in catalogo["chao"].items():
        qual = catalogo["sobre"][nome]
        _b, attr_chao = chao_nosso(qual)
        if atributo(gid) != attr_chao:
            mau.append("o chao %s (%d) tem atributo 0x%04X e o carimbo de %s tem "
                       "0x%04X" % (nome, gid, atributo(gid), qual, attr_chao))
        if arte_em_cima(entradas(gid), tp, ts):
            mau.append("o chao %s (%d) usa a camada de cima, e em celula andavel "
                       "NORMAL isso desenha ACIMA do jogador" % (nome, gid))
        dc = _dist_cor(_cor_media(px_de(gid)), _cor_media(px_carimbo[qual]))
        if dc > TETO_COR:
            mau.append("o chao %s (%d) esta a %.1f de cor do carimbo de %s, "
                       "acima do teto de %.1f" % (nome, gid, dc, qual, TETO_COR))

    # ---------- 4. MÓVEL e BASE: COVERED, comportamento zerado, e o NOSSO chão
    # entrada por entrada na camada de baixo
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

    # ---------- 5. TOPO de bloco: continua ANDÁVEL com o atributo do chão, tem o
    # nosso chão embaixo e a arte dele NÃO pode ser 100% opaca
    for nome, info in catalogo["blocos"].items():
        qual = catalogo["sobre"][nome]
        base, attr_chao = chao_nosso(qual)
        for gid in info["topo"]:
            if atributo(gid) != attr_chao:
                mau.append("o topo de bloco %s (%d) nao herdou o atributo do chao"
                           % (nome, gid))
            if entradas(gid)[:4] != base:
                mau.append("o topo de bloco %s (%d) nao tem o nosso chao embaixo"
                           % (nome, gid))
            op = 0
            for e in entradas(gid)[4:]:
                if e & 0x3FF:
                    vaga = (e & 0x3FF) - len(tp["tiles"])
                    op += (_opacos(tiles_novos[vaga]) if vaga in tiles_novos
                           else _opacos(RM.resolver_tile(tp, ts, e & 0x3FF)))
            if op >= 4 * 64:
                mau.append("o topo de bloco %s (%d) tapa o jogador inteiro (E3)"
                           % (nome, gid))

    # ---------- 6. nenhuma variante de chão e copia pixel a pixel de outra
    for qual in CARIMBOS:
        lista = [g for n, g in catalogo["chao"].items()
                 if catalogo["sobre"][n] == qual] + [CARIMBOS[qual]]
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                dd = _dist_pixels(pix[a], pix[b])
                if dd < PISO_VARIANTE:
                    mau.append("as variantes de chao %d e %d de %s tem distancia "
                               "%.1f, abaixo do piso de %.1f do varia_carimbo.py:"
                               " isso e enganar a regua"
                               % (a, b, qual, dd, PISO_VARIANTE))

    # ---------------------------------------------- 7 a 13. o plano, célula a célula
    L, W, H, v, escritas, contas = plano
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    meus_chaos = {catalogo["chao"][n]: n for n in catalogo["chao"]}
    meus_moveis = {catalogo["moveis"][n]: n for n in catalogo["moveis"]}
    meus_topos = {t: n for n, b in catalogo["blocos"].items() for t in b["topo"]}
    meus_bases = {t: n for n, b in catalogo["blocos"].items() for t in b["base"]}

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVACAO em (%d,%d)" % (ALVO, x, y))
        if cv and not cn:
            mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                       % (ALVO, x, y))
        if novo in meus_chaos or novo in meus_topos:
            nome = meus_chaos.get(novo) or meus_topos.get(novo)
            if cn != cv or velho != CARIMBOS[catalogo["sobre"][nome]]:
                mau.append("%s: chao/topo em celula errada em (%d,%d)"
                           % (ALVO, x, y))
        elif novo in meus_moveis or novo in meus_bases:
            nome = meus_moveis.get(novo) or meus_bases.get(novo)
            if cv or not cn:
                mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                           % (ALVO, x, y))
            if velho != CARIMBOS[catalogo["sobre"][nome]]:
                mau.append("%s: movel fora do carimbo em (%d,%d)" % (ALVO, x, y))
            if (x, y) in ev:
                mau.append("%s: movel em cima do evento (%d,%d)" % (ALVO, x, y))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                       % (ALVO, novo, x, y))
        # a passarela não encosta na elevação 15, que e o cruzamento consertado
        if (v[i] >> 12) & 0xF not in ELEVACOES[
                "terra" if velho == CARIMBOS["terra"] else "passarela"]:
            mau.append("%s: (%d,%d) tem elevacao fora da lista da familia"
                       % (ALVO, x, y))

    # 8. (comportamento, layerType) de toda célula ANDÁVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                       "layerType)" % (ALVO, i % W, i // W))
            break

    # 9 e 10. alcance a pe e LIGACAO a pe
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

    # 11. A MANCHA NÃO PODE SER ADIVINHAVEL, e o teste tem dois lados.
    # (a) PADRÃO: nenhuma projeção simples da posição pode ADIVINHAR a peça.
    # (b) FORMA: mancha e BOLHA, não sal e pimenta, e a conta e o TAMANHO MÉDIO
    # do pedaco conexo.
    mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
              if (val & 0x3FF) in meus_chaos}
    if len(mancha) < 300:
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
        if len(mancha) / pedacos < 12.0:
            mau.append("%s: a mancha media tem so %.1f celulas (%d em %d "
                       "pedacos): virou sal e pimenta, nao bolha"
                       % (ALVO, len(mancha) / pedacos, len(mancha), pedacos))

    # 12. a regua tem que fechar em 20% ou menos
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                   % (ALVO, b))

    # 13. o bloco de duas células: toda BASE tem um TOPO logo acima
    bases = {(i % W, i // W) for i, val in escritas.items()
             if (val & 0x3FF) in meus_bases}
    topos = {(i % W, i // W) for i, val in escritas.items()
             if (val & 0x3FF) in meus_topos}
    if len(bases) != len(topos):
        mau.append("%s: %d bases de bloco e %d topos" % (ALVO, len(bases),
                                                         len(topos)))
    for x, y in bases:
        if (x, y - 1) not in topos:
            mau.append("%s: a base de bloco em (%d,%d) esta sem topo" % (ALVO, x, y))
            break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferenca" so vale depois que a comparacao mostra que sabe reprovar.
    """
    tiles_novos, metas, attrs, catalogo = desenha_kit()
    guardado = carrega_plano()
    plano = plano_mapa(catalogo, base_de(ALVO, guardado))

    ts_do_disco = _tileset(SECUNDARIO)
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
        return (dict(tiles_novos), dict(metas), dict(attrs),
                json.loads(json.dumps(catalogo)),
                (L, W, H, list(v), dict(esc), ct))

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
        gid = a[3]["chao"]["terra de mare"]
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

    # N5. base de bloco gravada SEM o topo
    def n5():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        topos = {t for b in catalogo["blocos"].values() for t in b["topo"]}
        for i in sorted(esc):
            if (esc[i] & 0x3FF) in topos:
                del esc[i]
                break
        return a
    sabota("base de bloco sem o topo", n5, "bases de bloco e")

    # N6. camada de BAIXO de um móvel sabotada (chão da fonte em vez do nosso)
    def n6():
        a = copia()
        gid = a[3]["moveis"][MOVEIS_LP[0]["nome"]]
        ent = list(a[1][gid - 512])
        ent[0] = ent[4]
        a[1][gid - 512] = ent
        return a
    sabota("camada de baixo sabotada", n6, "nao tem o nosso chao de")

    # N7. o móvel da PASSARELA pousando na camada de baixo da TERRA. E a
    # sabotagem que só existe porque esta passada tem DOIS carimbos.
    def n7():
        a = copia()
        gid = a[3]["moveis"]["boia salva-vidas"]
        base_t, _ = chao_nosso("terra")
        a[1][gid - 512] = list(base_t) + list(a[1][gid - 512])[4:]
        return a
    sabota("movel de passarela com chao de terra", n7,
           "nao tem o nosso chao de passarela")

    # N8. mancha escolhida por (x + y) % n, que e xadrez com período
    def n8():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            a = (a[0], a[1], a[2], a[3],
                 plano_mapa(catalogo, base_de(ALVO, guardado)))
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
            a = (a[0], a[1], a[2], a[3],
                 plano_mapa(catalogo, base_de(ALVO, guardado)))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por x % n", n9, "virou padrao")

    # N9b. mancha escolhida por y % n, que e a mais forte das três sabotagens de
    # padrão (medida: 15,5% acima do chute cego).
    def n9b():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[y % len(nomes)]
        try:
            a = (a[0], a[1], a[2], a[3],
                 plano_mapa(catalogo, base_de(ALVO, guardado)))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por y % n", n9b, "virou padrao")

    # N10. a mancha espalhada AO ACASO com as MESMAS células: o teste de FORMA
    # tem que reprovar sal e pimenta que passa em todos os outros.
    def n10():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        meus = set(catalogo["chao"].values())
        cels = [i for i in esc if (esc[i] & 0x3FF) in meus]
        fam = collections.defaultdict(list)
        for i in cels:
            fam["terra" if (v[i] & 0x3FF) == CARIMBOS["terra"]
                else "passarela"].append(i)
        for qual, idxs in fam.items():
            # todas as células do carimbo que não estão escritas viram candidatas
            livres = [i for i in range(W * H)
                      if (v[i] & 0x3FF) == CARIMBOS[qual] and not ((v[i] >> 10) & 3)
                      and i not in esc]
            livres.sort(key=lambda i: _mistura(i, 0xDEAD))
            valores = [esc[i] & 0x3FF for i in idxs]
            for i in idxs:
                del esc[i]
            for k, val in enumerate(valores):
                if k < len(livres):
                    esc[livres[k]] = (v[livres[k]] & 0xFC00) | val
        return a
    sabota("mancha espalhada ao acaso", n10, "sal e pimenta")

    # N11. duas variantes de chão IGUAIS pixel a pixel: e enganar a regua
    def n11():
        a = copia()
        gid_a = a[3]["chao"]["terra de mare"]
        gid_b = a[3]["chao"]["terra batida"]
        a[1][gid_b - 512] = list(a[1][gid_a - 512])
        return a
    sabota("variante de chao duplicada", n11, "abaixo do piso de")

    # N12. cor nova escrita num índice que os NOSSOS pixels já usam. As vagas que
    # este kit usa (6 e 7) estão 100% livres, entao a sabotagem precisa
    # declarar uma vaga que TEM índice ocupado, que e a 10 ou a 11.
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

    # N13. gravar numa vaga de metatile que os mapas VIVOS usam
    def n13():
        a = copia()
        a[1][100] = list(a[1][min(a[1])])
        a[2][100] = 0x1000
        a[3]["chao"]["terra de mare"] = 512 + 100
        return a
    sabota("grava em vaga de metatile viva", n13, "abaixo da primeira vaga livre")

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
    print("  %-14s %d celulas mudadas, %d solidificadas, regua %.1f%% -> %.1f%%"
          % (ALVO, len(escritas), contas["solidos"], a, b))
    print("  %d tiles, %d metatiles, %d provas negativas:"
          % (len(tiles_novos), len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-34s -> %s" % (nome, queixa[:96]))
    return 0


# ------------------------------------------------- prova de TILE contra a ROM
def prova_tiles():
    """Cada tile do kit, DEPOIS de reindexado, contra o tile da ROM: zero pixel.

    Reindexar nibble e a unica coisa que este kit faz com o desenho da fonte, e e
    exatamente onde um erro passaria despercebido: a arte continuaria parecendo
    arte, com as cores trocadas de lugar.
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
    t1 = r.parse_tileset(LP["pri"])
    tsec = {k: r.parse_tileset(f["sec"]) for k, f in FONTES.items()}
    NP = r.n_tiles_pri
    pal = {k: {i: _rgb(t1 if i < 6 else tsec[k], i) for i in range(16)}
           for k in FONTES}
    dados = kit()
    n, dif = 0, 0
    for ch, px_kit in dados["tiles"].items():
        fonte, idx, ip = ch.split(":")
        idx, ip = int(idx), int(ip)
        crus = (_nibbles(t1["tiles"], idx) if idx < NP
                else _nibbles(tsec[fonte]["tiles"], idx - NP))
        vaga = dados["tiles_vaga"][ch]
        cores_nossas = dados["paletas"][str(vaga)]
        for y in range(8):
            for x in range(8):
                n += 1
                a = tuple(pal[fonte][ip][crus[y][x]]) if crus[y][x] else None
                b = (tuple(cores_nossas[px_kit[y][x]]) if px_kit[y][x] else None)
                if a != b:
                    dif += 1
                    if dif == 1:
                        print("  primeiro: tile %s (%d,%d) rom=%s kit=%s"
                              % (ch, x, y, a, b))
    print("tiles do kit contra a ROM: %d pixels, %d diferentes" % (n, dif))
    # a conta tem que saber REPROVAR
    ch0 = sorted(dados["tiles"])[0]
    fonte0, idx0, ip0 = ch0.split(":")
    idx0, ip0 = int(idx0), int(ip0)
    salvo = [linha[:] for linha in dados["tiles"][ch0]]
    dados["tiles"][ch0][0][0] = (salvo[0][0] + 1) % 16
    crus = (_nibbles(t1["tiles"], idx0) if idx0 < NP
            else _nibbles(tsec[fonte0]["tiles"], idx0 - NP))
    cores_nossas = dados["paletas"][str(dados["tiles_vaga"][ch0])]
    ruim = 0
    for y in range(8):
        for x in range(8):
            a = tuple(pal[fonte0][ip0][crus[y][x]]) if crus[y][x] else None
            b = (tuple(cores_nossas[dados["tiles"][ch0][y][x]])
                 if dados["tiles"][ch0][y][x] else None)
            if a != b:
                ruim += 1
    print("com UM nibble trocado no kit: %d pixels diferentes (tem que ser > 0)"
          % ruim)
    return 0 if dif == 0 and ruim > 0 else 1


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--prova-tiles" in sys.argv:
        return prova_tiles()
    if "--desfazer" in sys.argv:
        return desfaz()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--so-tileset" in sys.argv:
        t, m, at, c = desenha_kit()
        grava_tileset(t, m, at)
        print("tileset escrito: %d tiles, %d metatiles" % (len(t), len(m)))
        return 0
    return roda("--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
