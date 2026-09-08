#!/usr/bin/env python3
"""G4 da obra de Galar: os 240 ids de grafico do demake -> OBJ_EVENT_GFX_* nossos.

Uso:
    python3 dev_scripts/tabela_gfx_galar.py            # imprime a tabela e as contagens
    python3 dev_scripts/tabela_gfx_galar.py --demo     # remede a fonte e confere a tabela

Molde: a TROCA_SPRITE de `valida_mapas_sinnoh.py` (id da fonte -> sprite nosso,
uma linha documentada por vez, e um autoteste que recusa destino que esta build
nao desenha).

O QUE A MEDICAO DERRUBOU (leia antes de mexer)
----------------------------------------------
O plano supunha que "os ids ate ~150 do demake tendem a ser os do FireRed base".
MEDIDO em 18/08/2026, e e FALSO:

1. A tabela viva de graficos do demake esta em 0x08EB1000 e tem 240 entradas
   (o teto do FireRed, onde comeca OBJ_EVENT_GFX_VARS). O FireRed original tem
   152. Achada por varredura estrutural (array de ponteiros cujos alvos tem
   width/height em {8,16,32,64,128}, size multiplo de 32 e os quatro ponteiros
   internos dentro da ROM) e CONFIRMADA por referencia de codigo: o literal
   0x08EB1000 aparece em 0x0805F2F4, dentro da area de codigo.
2. Cruzando essa tabela com a geometria de CADA um dos 152 graficos do
   pokefirered (largura, altura, inanimate lidos do
   src/data/object_events/object_event_graphics_info.h), casam 17 de 152, e o
   melhor deslocamento alternativo (-3 a +3) nao passa de 17. Ou seja: NAO ha
   correspondencia de id com o FireRed em nenhum alinhamento. O autor trocou o
   conjunto inteiro por arte propria (o proprio jogador virou 32x32, contra
   16x32 do FireRed).
3. Uma segunda varredura procurou uma tabela ANTIGA sobrevivente (posicao onde
   40+ entradas casassem com a geometria do FireRed): nao existe nenhuma.

Portanto o papel de cada id NAO sai de nome nenhum: foi lido do desenho. Cada
sprite usado foi renderizado da ROM (primeiro quadro, 4bpp, paleta do proprio
grafico, tabela de paletas medida em 0x0828FD30) e classificado a olho em
folha de contato. A geometria medida (16x16 / 16x32 / 32x32 / 64x64 / 128x64)
entra como CONFERENCIA: `--demo` remede a ROM e reprova se ela mudar.

AS TRES CATEGORIAS
------------------
- `pessoa`: gente. Entra no mapa, com o sprite generico mais proximo do que o
  desenho mostra (genero, idade, classe aparente). A arte e do demake e nao tem
  equivalente aqui, entao o que se preserva e o PAPEL, nunca a semelhanca.
- `placa`: o unico id de placa (162, um poste com "?"). Entra como
  OBJ_EVENT_GFX_SIGN.
- `pokemon`: a espécie MEDIDA, quando ela foi medida, com
  `OBJ_EVENT_GFX_SPECIES(X)`. Quem ainda não tem espécie medida, ou tem espécie
  medida sem desenho nosso, continua com `None` e não entra. Ver a seção
  seguinte.
- `cenario`: NÃO entra. Árvore, pedra, Poké Ball e feixe de raide são objeto que
  só existe com script: mudos, viram bloqueio permanente ou promessa falsa.

A ESPÉCIE DEIXOU DE SER CHUTE (onda 5, lote R, 06/09/2026)
----------------------------------------------------------
Até a onda 4 esta tabela dizia "bicho verde" e recusava a linha inteira, pela
lei certa da época: sprite genérico de gente mentiria a espécie (a mesma lei
de `NOMES_PROPRIOS` em `importa_npcs_sinnoh.py`). Duas coisas mudaram:

1. O motor desenha Pokémon no overworld (`OBJ_EVENT_GFX_SPECIES(X)`, definido
   em `include/constants/event_objects.h`), e o `distribui_dex.py` já põe 106
   estáticos assim. Espécie certa deixou de precisar de sprite de gente.
2. A espécie de cada gráfico foi MEDIDA, e não lida a olho. Duas evidências
   independentes, cruzadas gráfico a gráfico:
   - os 57 gráficos foram renderizados da ROM do demake (primeiro quadro, 4bpp,
     paleta do próprio gráfico pela tabela em 0x0828FD30, que tem 252 entradas)
     e OLHADOS um a um; os PNGs ficaram em `dev_scripts/onda5_gfx_galar/`;
   - os scripts da fonte dos objetos que usam cada gráfico foram desmontados, e
     o `setwildbattle` e o `playmoncry` deles dão o ID de espécie do demake, que
     `estaticos_galar.nomes_da_fonte()` traduz por NOME.
   Onde as duas discordam, vale o DESENHO, porque é ele que vai para a tela, e a
   discordância fica escrita na linha (o 201 é o caso: grito e arte de Cubchoo,
   `setwildbattle` de Sandslash).

O terceiro filtro, e o que ainda recusa 8 linhas: `SPECIES_X` existir no
`species.h` NÃO basta, porque a constante existe para toda espécie. Quem decide
se há desenho é a macro `OVERWORLD(` do `species_info`, e é ela que o `confere()`
mede. Morpeko, Zacian, Zamazenta, Meloetta, Xerneas, Shaymin e Flabébé estão
identificados e continuam com `None` por falta de arte nossa, não por dúvida.
"""
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

ROM_DEMAKE = os.path.join(os.path.dirname(RAIZ),
                          "fontes-mapas/galar-swsh/ultimate-plus-v1.2.1.2.gba")
# Medidos nesta ROM, nao chutados. Ver item 1 do docstring.
TABELA_GFX = 0x08EB1000
N_GFX = 240
# Id dinamico: no FireRed 240..255 sao OBJ_EVENT_GFX_VAR_0..F, resolvidos em
# tempo de execucao por var. Sem a cena que carrega a var, nao ha grafico.
PRIMEIRO_VAR = 240

# Sprite da casa: usado quando um id aparecer no mapa e nao estiver na tabela.
# Nao deveria acontecer (o --demo cobre os 190 ids usados), e por isso ele e
# gente comum e nao um sprite chamativo: se aparecer, e um homem a mais numa
# rua, nao um crash.
PADRAO = "OBJ_EVENT_GFX_MAN"

# id da fonte -> (categoria, sprite nosso ou None, papel LIDO DO DESENHO)
#
# Categoria "pessoa"/"placa" entra no mapa; "pokemon"/"cenario" vai para o censo.
# O sprite e sempre da familia FRLG quando existe, porque os tilesets de Galar
# saem do FireRed e misturar o traco de Hoenn com o de Kanto na mesma rua salta
# aos olhos.
TABELA = {
    # --- protagonista e rivais do demake (paleta de jogador, slot 0) ---------
    0:  ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "menina protagonista de gorro (Gloria); 168 usos, o autor reusa o proprio jogador como NPC"),
    7:  ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "a mesma menina, outra pose"),
    8:  ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "a mesma menina, outra pose"),
    9:  ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "a mesma menina, outra pose"),
    12: ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_F", "a mesma menina, outra pose"),
    14: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de cabelo branco e casaco roxo"),
    15: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina de maria-chiquinha preta e laco vermelho"),
    17: ("pessoa", "OBJ_EVENT_GFX_LITTLE_BOY_FRLG", "crianca pequena, 16x16 na fonte (a unica desse tamanho que e gente)"),
    # --- gente comum de rua ------------------------------------------------
    18: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "menino louro de camisa vermelha"),
    19: ("pessoa", "OBJ_EVENT_GFX_BUG_CATCHER_FRLG", "menino de bone verde"),
    20: ("pessoa", "OBJ_EVENT_GFX_MAN", "homem de bone branco e roupa escura"),
    21: ("pessoa", "OBJ_EVENT_GFX_WORKER_M", "homem de uniforme escuro e bone marrom"),
    22: ("pessoa", "OBJ_EVENT_GFX_BEAUTY_FRLG", "moca loura de casaco; 212 usos, o rosto mais comum da regiao"),
    23: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de cabelo castanho"),
    24: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina de cabelo claro e roupa vermelha"),
    25: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "menino de bone preto e camisa verde"),
    26: ("pessoa", "OBJ_EVENT_GFX_MAN", "homem moreno de camisa vermelha"),
    27: ("pessoa", "OBJ_EVENT_GFX_WOMAN_1_FRLG", "moca de avental rosa"),
    28: ("pessoa", "OBJ_EVENT_GFX_WOMAN_2_FRLG", "mulher de cabelo castanho e vestido vermelho"),
    29: ("pessoa", "OBJ_EVENT_GFX_WOMAN_3_FRLG", "mulher de cabelo roxo e vestido branco"),
    30: ("pessoa", "OBJ_EVENT_GFX_GENTLEMAN_FRLG", "homem de terno escuro"),
    31: ("pessoa", "OBJ_EVENT_GFX_OLD_WOMAN_FRLG", "senhora de cabelo lilas e vestido azul"),
    32: ("pessoa", "OBJ_EVENT_GFX_BALDING_MAN", "senhor careca"),
    33: ("pessoa", "OBJ_EVENT_GFX_FISHER", "pessoa de chapeu preto largo e macacao"),
    34: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina de rosa com touca de orelhas"),
    35: ("pessoa", "OBJ_EVENT_GFX_OLD_WOMAN_FRLG", "senhora de cabelo branco e roupa rosa"),
    36: ("pessoa", "OBJ_EVENT_GFX_WOMAN_2_FRLG", "mulher de coque e camisa amarela"),
    37: ("pessoa", "OBJ_EVENT_GFX_WOMAN_3_FRLG", "mulher morena de coque"),
    38: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "menino ruivo de camisa verde"),
    39: ("pessoa", "OBJ_EVENT_GFX_WORKER_M", "pessoa de bone verde e uniforme; 105 usos"),
    40: ("pessoa", "OBJ_EVENT_GFX_WORKER_F", "par feminino do 39, mesmo uniforme; 106 usos"),
    41: ("pessoa", "OBJ_EVENT_GFX_MAN", "homem moreno de camisa azul; 101 usos"),
    42: ("pessoa", "OBJ_EVENT_GFX_WOMAN_2_FRLG", "mulher de coque e roupa vermelha; 100 usos"),
    43: ("pessoa", "OBJ_EVENT_GFX_BEAUTY_FRLG", "moca loura de roupa branca"),
    44: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "menino de bone preto e camisa vermelha"),
    46: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina loura de vestido azul"),
    47: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de camisa azul"),
    48: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina loura de bone azul"),
    49: ("pessoa", "OBJ_EVENT_GFX_ROCKET_M", "punk de moicano e roupa preta (Team Yell)"),
    50: ("pessoa", "OBJ_EVENT_GFX_ROCKET_F", "punk de cabelo rosa (Team Yell)"),
    51: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de camisa azul escura"),
    52: ("pessoa", "OBJ_EVENT_GFX_BUG_CATCHER_FRLG", "crianca de bone azul"),
    53: ("pessoa", "OBJ_EVENT_GFX_WORKER_M", "homem de chapeu escuro e macacao laranja (mineiro)"),
    54: ("pessoa", "OBJ_EVENT_GFX_FISHER", "homem de bandana"),
    55: ("pessoa", "OBJ_EVENT_GFX_SCIENTIST", "pessoa de jaleco branco e oculos"),
    56: ("pessoa", "OBJ_EVENT_GFX_YOUNGSTER_FRLG", "crianca de bone azul e camisa laranja"),
    57: ("pessoa", "OBJ_EVENT_GFX_BUG_CATCHER_FRLG", "crianca de bone amarelo"),
    58: ("pessoa", "OBJ_EVENT_GFX_POKE_MANIAC_FRLG", "crianca de cabelo cinza"),
    60: ("pessoa", "OBJ_EVENT_GFX_POLICEMAN", "pessoa de bone azul e uniforme; 208 usos, o segundo rosto mais comum"),
    61: ("pessoa", "OBJ_EVENT_GFX_BLACK_BELT_FRLG", "pessoa morena de bone e roupa azul"),
    62: ("pessoa", "OBJ_EVENT_GFX_CAPTAIN", "pessoa de quepe e uniforme branco"),
    64: ("pessoa", "OBJ_EVENT_GFX_NURSE_FRLG", "moca de cabelo rosa e touca (enfermeira)"),
    65: ("pessoa", "OBJ_EVENT_GFX_WORKER_M", "guarda de bone e uniforme"),
    66: ("pessoa", "OBJ_EVENT_GFX_MAN", "homem de cabelo escuro"),
    67: ("pessoa", "OBJ_EVENT_GFX_WOMAN_1_FRLG", "mulher de cabelo castanho"),
    68: ("pessoa", "OBJ_EVENT_GFX_WOMAN_2_FRLG", "moca de vestido vermelho; 142 usos"),
    69: ("pessoa", "OBJ_EVENT_GFX_PICNICKER_FRLG", "menina de bone vermelho; 77 usos"),
    71: ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_M", "pessoa morena de cabelo roxo e roupa dourada"),
    72: ("pessoa", "OBJ_EVENT_GFX_COOLTRAINER_M", "pessoa de cabelo roxo agachada; 61 usos"),
    73: ("pessoa", "OBJ_EVENT_GFX_SCIENTIST", "pessoa de jaleco e cabelo castanho"),
    75: ("pessoa", "OBJ_EVENT_GFX_ROCKER", "pessoa de cabelo preto e branco e roupa escura"),
    77: ("pessoa", "OBJ_EVENT_GFX_PICNICKER_FRLG", "menina ruiva de maria-chiquinha"),
    78: ("pessoa", "OBJ_EVENT_GFX_GENTLEMAN_FRLG", "homem de terno claro"),
    79: ("pessoa", "OBJ_EVENT_GFX_OLD_WOMAN_FRLG", "senhora de cabelo branco e vestido"),
    80: ("pessoa", "OBJ_EVENT_GFX_CAMPER_FRLG", "pessoa de chapeu de palha e roupa de campo"),
    81: ("pessoa", "OBJ_EVENT_GFX_SWIMMER_F_LAND", "moca morena de cabelo azul e roupa de banho"),
    82: ("pessoa", "OBJ_EVENT_GFX_POKE_MANIAC_FRLG", "crianca de cabelo branco e camisa laranja"),
    83: ("pessoa", "OBJ_EVENT_GFX_ROCKER", "pessoa de cabelo preto e roupa escura"),
    84: ("pessoa", "OBJ_EVENT_GFX_WOMAN_3_FRLG", "pessoa de chapeu azul e quimono"),
    85: ("pessoa", "OBJ_EVENT_GFX_OLD_MAN_1", "pessoa de cabelo branco e roupa branca"),
    86: ("pessoa", "OBJ_EVENT_GFX_BLACK_BELT_FRLG", "pessoa de cabelo laranja e roupa escura"),
    87: ("pessoa", "OBJ_EVENT_GFX_OLD_MAN_2", "senhor de cabelo branco, oculos e jaleco"),
    88: ("pessoa", "OBJ_EVENT_GFX_WOMAN_1_FRLG", "mulher de cabelo roxo e blusa vermelha"),
    89: ("pessoa", "OBJ_EVENT_GFX_BEAUTY_FRLG", "moca de cabelo claro comprido"),
    90: ("pessoa", "OBJ_EVENT_GFX_WOMAN_3_FRLG", "pessoa morena de cabelo preto"),
    191: ("pessoa", "OBJ_EVENT_GFX_LASS_FRLG", "menina ruiva, 16x32 na fonte"),
    197: ("pessoa", "OBJ_EVENT_GFX_BOY", "menino de cabelo azul, 16x32 na fonte"),
    207: ("pessoa", "OBJ_EVENT_GFX_CHANNELER", "figura encapuzada cinza; o CHANNELER e a unica tunica que temos"),
    223: ("pessoa", "OBJ_EVENT_GFX_SCIENTIST", "pessoa de oculos e cabelo azul"),
    225: ("pessoa", "OBJ_EVENT_GFX_PICNICKER_FRLG", "moca de chapeu branco"),
    229: ("pessoa", "OBJ_EVENT_GFX_OLD_MAN_LYING_DOWN", "pessoa DEITADA no chao; casa em papel e em tamanho (32x32 nos dois lados)"),
    # --- placa --------------------------------------------------------------
    162: ("placa", "OBJ_EVENT_GFX_SIGN", "poste com uma placa de '?'; 29 usos"),
    # --- Pokemon: nao entram (especie desconhecida, e sprite generico mente) --
    16:  ("pokemon", None, "quadrupede pequeno de orelha grande, 16x32; 103 usos"),
    45:  ("pokemon", None, "vulto escuro"),
    59:  ("pokemon", None, "mariposa branca"),
    63: ("pokemon", "OBJ_EVENT_GFX_SPECIES(PYROAR)",
         "Pyroar; 9 objetos deste gfx dao `setwildbattle` e `playmoncry` Pyroar (id 967) na fonte, e o desenho e o leao de juba vermelha e dourada"),
    70: ("pokemon", "OBJ_EVENT_GFX_SPECIES(GOGOAT)",
         "Gogoat; 8 `setwildbattle`/`playmoncry` Gogoat (id 826), e o desenho e o bode de manto de folhas"),
    74: ("pokemon", "OBJ_EVENT_GFX_SPECIES(PIDGEOT)",
         "Pidgeot; 4 `setwildbattle`/`playmoncry` Pidgeot (id 18), e o desenho e a ave dourada de crista vermelha e amarela"),
    93:  ("pokemon", None, "passaro laranja"),
    94:  ("pokemon", None, "dragao escuro"),
    98:  ("pokemon", None, "morcego roxo"),
    99: ("pokemon", "OBJ_EVENT_GFX_SPECIES(BULBASAUR)",
         "Bulbasaur; objeto UNICO, sem script, no g01m34 (Galar_IsleOfArmor02, o Dojo do Mestre), ao lado do Squirtle do gfx 100 e do Kubfu do gfx 221: sao os presentes da Ilha da Armadura. Desenho verde claro de bulbo verde escuro e olho vermelho. Confianca MEDIA: nao ha script para confirmar"),
    100: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SQUIRTLE)",
         "Squirtle; objeto UNICO, sem script, no mesmo g01m34 do Bulbasaur do gfx 99. Desenho azul redondo com o plastrao amarelo embaixo e olho vermelho. Confianca MEDIA: nao ha script para confirmar"),
    101: ("pokemon", None, "cogumelo rosa"),
    103: ("pokemon", None, "cristal verde"),
    106: ("pokemon", None, "cabeca amarela"),
    107: ("pokemon", "OBJ_EVENT_GFX_SPECIES(REGIROCK)",
         "Regirock; o desenho e o golem de pedra bege com a face de pontos alaranjados. Os 2 objetos deste gfx batalham um Regirock (id 401) e um Regice (id 402): a fonte poe a arte de Regirock nos dois, e por isso a linha fica com a especie que o DESENHO mostra. Confianca MEDIA"),
    109: ("pokemon", "OBJ_EVENT_GFX_SPECIES(GLASTRIER)",
         "Glastrier; 2 `setwildbattle` Glastrier (id 1188), nos mapas Galar_CrownTundra08 e 15, que sao a casa dele. Desenho branco de elmo de gelo azul. Confianca MEDIA: a silhueta 32x32 nao fecha sozinha"),
    110: ("pokemon", "OBJ_EVENT_GFX_SPECIES(ZIGZAGOON_GALAR)",
         "Zigzagoon de Galar; 45 `setwildbattle` do id 1226, que esta no bloco de FORMAS REGIONAIS do demake (1210 a 1240) e nao no id base 288, e o desenho e preto e branco, nao marrom"),
    111: ("pokemon", "OBJ_EVENT_GFX_SPECIES(YAMPER)",
         "Yamper; 66 `setwildbattle` e 70 `playmoncry` Yamper (id 1128); 38 objetos no total"),
    112: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SILICOBRA)",
         "Silicobra; 53 `setwildbattle`/`playmoncry` Silicobra (id 1153), e o desenho e a cobra de areia de olho verde"),
    113: ("pokemon", None, "aranha roxa"),
    114: ("pokemon", None, "raposa escura"),
    115: ("pokemon", "OBJ_EVENT_GFX_SPECIES(ARROKUDA)",
         "Arrokuda; 18 `setwildbattle`/`playmoncry` Arrokuda (id 1160), e o desenho e o peixe marrom de focinho branco"),
    116: ("pokemon", "OBJ_EVENT_GFX_SPECIES(ROOKIDEE)",
         "Rookidee; 45 `setwildbattle` e 47 `playmoncry` Rookidee (id 1126), e o desenho e o passarinho azul de bico amarelo"),
    117: ("pokemon", None, "bola preta"),
    118: ("pokemon", "OBJ_EVENT_GFX_SPECIES(HOUNDOUR)",
         "Houndour; 51 `setwildbattle`/`playmoncry` Houndour (id 228)"),
    119: ("pokemon", "OBJ_EVENT_GFX_SPECIES(CHEWTLE)",
         "Chewtle; 48 `setwildbattle`/`playmoncry` Chewtle (id 1157), e o desenho e o cagado verde-agua de chifre laranja"),
    120: ("pokemon", "OBJ_EVENT_GFX_SPECIES(APPLIN)",
         "Applin; 69 `setwildbattle` e 70 `playmoncry` Applin (id 1163), e o desenho e a maca vermelha de folhas verdes"),
    121: ("pokemon", "OBJ_EVENT_GFX_SPECIES(FARFETCHD_GALAR)",
         "Farfetch'd de Galar; 27 `setwildbattle`/`playmoncry` do id 1217, que esta no bloco de formas regionais do demake, e o desenho e o pato marrom com o alho-poro nas costas. Os 4 Rockruff que dividem este gfx sao objetos de outro papel no mesmo script"),
    122: ("pokemon", "OBJ_EVENT_GFX_SPECIES(MEOWTH_GALAR)",
         "Meowth de Galar; 24 `setwildbattle`/`playmoncry` do id 1212, do bloco de formas regionais, e o desenho e CINZA de olho amarelo, nao o amarelo de Kanto"),
    123: ("pokemon", "OBJ_EVENT_GFX_SPECIES(STUNFISK_GALAR)",
         "Stunfisk de Galar; 47 `setwildbattle`/`playmoncry` do id 1233, do bloco de formas regionais, e o desenho e verde escuro, nao o marrom e amarelo de Unova"),
    124: ("pokemon", "OBJ_EVENT_GFX_SPECIES(WOOLOO)",
         "Wooloo; 45 `setwildbattle` e 49 `playmoncry` Wooloo (id 1123), e o desenho e a ovelha de la branca e cara preta. E o gfx de POKEMON mais usado da regiao, 54 usos"),
    125: ("pokemon", "OBJ_EVENT_GFX_SPECIES(IMPIDIMP)",
         "Impidimp; 54 `setwildbattle`/`playmoncry` Impidimp (id 1168), e o desenho e o diabinho rosa de chifres escuros"),
    126: ("pokemon", None,
         "Morpeko; 29 `setwildbattle` e 32 `playmoncry` Morpeko (id 1175), e o desenho e o hamster metade amarelo metade preto. RECUSADO por FALTA DE ARTE NOSSA: SPECIES_MORPEKO nao tem `OVERWORLD(` no species_info, entao OBJ_EVENT_GFX_SPECIES(MORPEKO) nao desenharia nada"),
    127: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SNOM)",
         "Snom; 29 `setwildbattle`/`playmoncry` Snom (id 1170), e o desenho e a larva branca de casca azul-gelo"),
    128: ("pokemon", "OBJ_EVENT_GFX_SPECIES(DARUMAKA_GALAR)",
         "Darumaka de Galar; 62 `setwildbattle`/`playmoncry` do id 1229, do bloco de formas regionais, e o desenho e branco e azul, nao o vermelho de Unova"),
    129: ("pokemon", "OBJ_EVENT_GFX_SPECIES(FALINKS)",
         "Falinks; 49 `setwildbattle`/`playmoncry` Falinks (id 1177), e o desenho e a tropa de seis soldados alaranjados enfileirados"),
    130: ("pokemon", "OBJ_EVENT_GFX_SPECIES(COPPERAJAH)",
         "Copperajah; 58 `setwildbattle`/`playmoncry` Copperajah (id 1180), e o desenho e o elefante de cobre esverdeado com placas alaranjadas"),
    131: ("pokemon", "OBJ_EVENT_GFX_SPECIES(CLOBBOPUS)",
         "Clobbopus; 54 `setwildbattle`/`playmoncry` Clobbopus (id 1171), e o desenho e o polvo creme de faixa laranja"),
    132: ("pokemon", None, "passaro azul"),
    133: ("pokemon", "OBJ_EVENT_GFX_SPECIES(DREEPY)",
         "Dreepy; 90 `setwildbattle`/`playmoncry` Dreepy (id 1185), e o desenho e o dragaozinho verde-acinzentado de aletas rosa. E o gfx com mais scripts de encontro da regiao"),
    134: ("pokemon", "OBJ_EVENT_GFX_SPECIES(DURALUDON)",
         "Duraludon; 25 `setwildbattle`/`playmoncry` Duraludon (id 1184), e o desenho e a torre de metal branca e azul de olho amarelo"),
    135: ("pokemon", "OBJ_EVENT_GFX_SPECIES(YAMASK_GALAR)",
         "Yamask de Galar; 63 `setwildbattle`/`playmoncry` do id 1232, do bloco de formas regionais, e o desenho carrega a lapide, nao a mascara dourada de Unova"),
    136: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SNOVER)",
         "Snover; 79 `setwildbattle`/`playmoncry` Snover (id 512), e o desenho e o pinheirinho branco de base marrom. 63 usos, o segundo gfx de Pokemon mais usado"),
    137: ("pokemon", None, "peixe-serra azul; 72 usos"),
    138: ("pokemon", None, "passaro azul e branco"),
    139: ("pokemon", "OBJ_EVENT_GFX_SPECIES(ROCKRUFF)",
         "Rockruff; 21 `setwildbattle`/`playmoncry` Rockruff (id 961), e o desenho e o cachorro marrom de colar de pedras e olho azul"),
    140: ("pokemon", None, "baleia azul 64x64; 40 usos"),
    141: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SLOWPOKE_GALAR)",
         "Slowpoke de Galar; 3 `setwildbattle` do id 1215, do bloco de formas regionais, e o desenho tem a espiral AMARELA na cabeca, que e a marca da forma de Galar"),
    142: ("pokemon", None,
         "Zacian; 1 `setwildbattle`/`playmoncry` Zacian (id 1186), e o desenho e o lobo azul de crista vermelha. RECUSADO por FALTA DE ARTE NOSSA: SPECIES_ZACIAN nao tem `OVERWORLD(` no species_info"),
    143: ("pokemon", None,
         "Zamazenta; o `setwildbattle` do objeto diz Zamazenta (id 1187) e o desenho e o lobo VERMELHO de crista azul, o par do 142; o `playmoncry` do mesmo script diz Zacian, e essa e divergencia da propria fonte. RECUSADO por FALTA DE ARTE NOSSA: SPECIES_ZAMAZENTA nao tem `OVERWORLD(`"),
    144: ("pokemon", "OBJ_EVENT_GFX_SPECIES(CALYREX)",
         "Calyrex; 1 `setwildbattle` Calyrex (id 1190), e o desenho e a coroa verde-escura sobre o corpo branco"),
    # CORRIGIDO em 06/09/2026 (onda 4, lote P). Dizia "morcego rosa 64x64", e
    # essa linha era a unica duvida do pedido de taxi da onda 3. Medido na ROM:
    # 64x64, `oam` 0x83A3720 e tabela de subsprite 0x83A38D0 IGUAIS as do 232
    # (o Corviknight preto), 690 pixels opacos em cada um e 97,1% da mascara de
    # transparencia coincidindo pixel a pixel. Os dados de tile sao outros
    # (0x9017A1C contra 0x8F71360), entao sao DUAS ARTES do mesmo passaro e nao
    # um alias: o 145 e a versao PRATA.
    145: ("pokemon", None, "Corviknight prata 64x64; 32 usos; par do 232"),
    146: ("pokemon", None, "aranha azul e rosa 64x64"),
    147: ("pokemon", None, "morcego bege; 83 usos"),
    153: ("pokemon", "OBJ_EVENT_GFX_SPECIES(GROOKEY)",
         "Grookey; o desenho e o macaco verde de tufo de folhas e focinho marrom, e ele e o primeiro do TRIO de iniciais 153/154/155 (Grookey, Scorbunny, Sobble), os tres com o mesmo molde de arte e ids seguidos. O script do objeto e um `givemon` por var, entao a especie sai do desenho e da posicao no trio"),
    154: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SCORBUNNY)",
         "Scorbunny; o coelho branco de orelhas em chama laranja, o do meio do trio de iniciais 153/154/155. LINHA CORRIGIDA na onda 5 (dizia so 'coelho branco'): a arte foi renderizada e olhada junto com as duas vizinhas"),
    155: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SOBBLE)",
         "Sobble; o lagarto azul de barbatana amarela na cabeca, o terceiro do trio de iniciais 153/154/155"),
    157: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SKWOVET)",
         "Skwovet; 12 `setwildbattle`/`playmoncry` Skwovet (id 1121), e o desenho e o esquilo cinza de rabo enorme e bochecha laranja"),
    158: ("pokemon", None,
         "Meloetta; 1 `setwildbattle`/`playmoncry` Meloetta (id 731), e o desenho e a forma Aria, de cabelo verde e vestido branco. RECUSADO por FALTA DE ARTE NOSSA: SPECIES_MELOETTA nao tem `OVERWORLD(` no species_info"),
    160: ("pokemon", "OBJ_EVENT_GFX_SPECIES(DRAMPA)",
         "Drampa; 3 `setwildbattle`/`playmoncry` Drampa (id 1013), e o desenho e o dragao branco de juba e bigode verde-agua"),
    168: ("pokemon", None, "passaro amarelo"),
    169: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SKWOVET)",
         "Skwovet; ARTE IDENTICA a do gfx 157 (o PNG renderizado dos dois bate byte a byte, md5 06a65903390ff014aed3f260042c1e50), e os 6 scripts deste gfx tambem dizem Skwovet"),
    170: ("pokemon", None,
         "Meloetta; ARTE IDENTICA a do gfx 158 (md5 fef708696796fe0d9d5e65804bab3cae nos dois PNGs). Os 2 objetos deste gfx nao tem script. RECUSADO pelo mesmo motivo do 158: SPECIES_MELOETTA nao tem `OVERWORLD(`"),
    173: ("pokemon", "OBJ_EVENT_GFX_SPECIES(PALOSSAND)",
         "Palossand; 10 `setwildbattle`/`playmoncry` Palossand (id 1000), e o desenho e o castelo de areia alaranjado"),
    176: ("pokemon", "OBJ_EVENT_GFX_SPECIES(MAMOSWINE)",
         "Mamoswine; 23 `setwildbattle`/`playmoncry` Mamoswine (id 526), e o desenho e o mamute marrom de presas brancas; 24 usos"),
    177: ("pokemon", "OBJ_EVENT_GFX_SPECIES(TAPU_KOKO)",
         "Tapu Koko; o desenho e o corpo preto com as duas conchas amarelas abertas e o olho azul, que e o Koko e nao o Bulu. Os 2 objetos deste gfx, os dois no Galar_IsleOfArmor05, batalham um Tapu Koko (id 1002) e um Tapu Bulu (id 1004), entao a especie sai do DESENHO. Confianca MEDIA"),
    179: ("pokemon", None, "coelho cinza 64x64"),
    180: ("pokemon", None, "vulto alado preto 64x64"),
    181: ("pokemon", None,
         "Xerneas; o desenho e o cervo azul de galhada dourada com as pontas coloridas. Os 3 objetos deste gfx batalham Xerneas (id 824), Dialga e Kyogre, e a arte e a de Xerneas. RECUSADO por FALTA DE ARTE NOSSA: SPECIES_XERNEAS nao tem `OVERWORLD(`"),
    182: ("pokemon", None, "dragao laranja"),
    183: ("pokemon", "OBJ_EVENT_GFX_SPECIES(GROUDON)",
         "Groudon; 1 `setwildbattle`/`playmoncry` Groudon (id 405) no Galar_GalarMine01, e o desenho 64x64 e o quadrupede vermelho de placa cinza no rosto"),
    185: ("pokemon", None, "fantasma rosa"),
    190: ("pokemon", None,
         "Shaymin, forma Terrestre; o desenho e o ourico verde com os TUFOS ROSA dos dois lados da cabeca, que e o Shaymin e nao o Celebi. Os 2 objetos deste gfx batalham um Shaymin (id 545) e um Celebi (id 251). RECUSADO por FALTA DE ARTE NOSSA: SPECIES_SHAYMIN nao tem `OVERWORLD(`"),
    198: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SCRAGGY)",
         "Scraggy; 6 `setwildbattle`/`playmoncry` Scraggy (id 645), e o desenho e o lagarto amarelo de crista vermelha"),
    199: ("pokemon", "OBJ_EVENT_GFX_SPECIES(TAILLOW)",
         "Taillow; 6 `setwildbattle`/`playmoncry` Taillow (id 276), e o desenho e a andorinha azul de rosto vermelho"),
    200: ("pokemon", "OBJ_EVENT_GFX_SPECIES(TRAPINCH)",
         "Trapinch; 5 `setwildbattle`/`playmoncry` Trapinch (id 328), e o desenho e a cabeca laranja de mandibula enorme"),
    201: ("pokemon", "OBJ_EVENT_GFX_SPECIES(CUBCHOO)",
         "Cubchoo; 7 `playmoncry` Cubchoo (id 613) e o desenho e o ursinho AZUL de orelha redonda. O `setwildbattle` do mesmo script diz Sandslash (id 28), o marrom de Kanto, e nem a arte nem o grito batem com ele: e divergencia da propria fonte, e aqui vale o desenho"),
    202: ("pokemon", None,
         "Flabebe; 12 `setwildbattle`/`playmoncry` Flabebe (id 777), e o desenho e a fadinha branca segurando a flor amarela; 13 usos. RECUSADO por FALTA DE ARTE NOSSA: SPECIES_FLABEBE nao tem `OVERWORLD(` no species_info"),
    209: ("pokemon", "OBJ_EVENT_GFX_SPECIES(TRUBBISH)",
         "Trubbish; 8 `playmoncry` e 4 `setwildbattle` Trubbish (id 653), e o desenho e o saco de lixo verde de dois nos no alto"),
    221: ("pokemon", "OBJ_EVENT_GFX_SPECIES(KUBFU)",
         "Kubfu; o objeto do g01m34 (o Dojo do Mestre) toca `playmoncry` Kubfu (id 1183), e os outros 3 objetos deste gfx estao no g38m01, g38m05 e g38m08, as torres da Ilha da Armadura, que e onde o Kubfu acompanha o jogador. Confianca MEDIA: um grito so"),
    224: ("pokemon", "OBJ_EVENT_GFX_SPECIES(MUDSDALE)",
         "Mudsdale; 14 `setwildbattle` e 15 `playmoncry` Mudsdale (id 984), e o desenho e o cavalo de carga marrom de crina escura"),
    227: ("pokemon", None, "inseto laranja"),
    228: ("pokemon", None, "inseto amarelo"),
    230: ("pokemon", None, "cacto verde"),
    231: ("pokemon", "OBJ_EVENT_GFX_SPECIES(SNORLAX)",
         "Snorlax dormindo; 64x64, sem script em nenhum dos 5 objetos. O desenho e inconfundivel: barriga creme, corpo azul-petroleo e boca aberta de costas no chao"),
    # "corvo de armadura" ate 06/09/2026: e o Corviknight, e o par PRETO do 145.
    232: ("pokemon", None, "Corviknight preto 64x64; 30 usos; par do 145"),
    233: ("pokemon", None, "passaro lendario vermelho e dourado 64x64"),
    234: ("pokemon", None, "lendario branco e azul 64x64"),
    235: ("pokemon", None, "serpente de metal 64x64; 38 usos"),
    237: ("pokemon", None, "lendario roxo alado 64x64"),
    # --- cenario e objeto de script: nao entram -----------------------------
    91:  ("cenario", None, "feixe de luz de covil de raide, 64x64; 45 usos. Sem a cena de raide e um poste luminoso solido"),
    92:  ("cenario", None, "Poke Ball no chao, 16x16; 74 usos. Item VISIVEL: qual item e so o script sabe, e Poke Ball que nao se pega e promessa falsa"),
    95:  ("cenario", None, "muda de arvore; 17 usos. Obstaculo de campo"),
    97:  ("cenario", None, "pedra redonda 16x16, o unico grafico marcado inanimate na fonte"),
    105: ("cenario", None, "arvore frutifera 64x64; 23 usos. Sem script vira parede permanente"),
    108: ("cenario", None, "trem 64x64"),
    148: ("cenario", None, "monte de pedras 64x64; 155 usos. Obstaculo de Rock Smash sem Rock Smash e caverna trancada para sempre"),
    149: ("cenario", None, "estrela escura no chao 64x64; 27 usos. Marca de covil da Wild Area"),
    150: ("cenario", None, "caixa vermelha 16x16; 56 usos"),
    151: ("cenario", None, "estacao de trem 128x64, o unico grafico desse tamanho"),
    161: ("cenario", None, "caixa de presente"),
    193: ("cenario", None, "anel dourado sobre fundo vermelho, 16x32"),
    196: ("cenario", None, "cristal branco, 16x32"),
    203: ("cenario", None, "marca de X, 16x32"),
    204: ("cenario", None, "marca de X, 16x32"),
    208: ("cenario", None, "Poke Ball 16x16; 20 usos. Mesmo motivo do 92"),
    239: ("cenario", None, "letreiro escrito PIERS, 64x64"),
}

# Ids que a fonte usa e que nao tem entrada na tabela de graficos do demake.
# 255 e OBJ_EVENT_GFX_VAR_F: grafico dinamico, so existe depois que uma cena
# escreve a var. Sem cena, nao ha o que desenhar.
DINAMICOS = {255: "grafico dinamico (VAR_F); so a cena que escreve a var sabe o que e"}


def traduz(gid):
    """(sprite, categoria, papel). sprite None = nao entra no mapa."""
    if gid in TABELA:
        cat, sprite, papel = TABELA[gid]
        return sprite, cat, papel
    if gid >= PRIMEIRO_VAR:
        return None, "dinamico", DINAMICOS.get(gid, "grafico dinamico por var")
    return PADRAO, "pessoa", "id sem linha na tabela; sprite padrao da casa"


# ------------------------------------------------------------------ medicao --

def mede_rom():
    """(id -> (w, h, inanimate)) lido da tabela viva da ROM do demake."""
    rom = open(ROM_DEMAKE, "rb").read()
    base = 0x08000000
    fora = {}
    for i in range(N_GFX):
        p = struct.unpack_from("<I", rom, TABELA_GFX - base + 4 * i)[0]
        o = p - base
        fora[i] = (struct.unpack_from("<h", rom, o + 8)[0],
                   struct.unpack_from("<h", rom, o + 10)[0],
                   bool((rom[o + 12] >> 6) & 1))
    return fora


def sprites_desenhaveis():
    import valida_mapas_sinnoh as V
    return V.sprites_utilizaveis()


ESPECIE = re.compile(r"^OBJ_EVENT_GFX_SPECIES\(([A-Z0-9_]+)\)$")


def especies_desenhaveis():
    """Espécies que esta build desenha no overworld.

    `OBJ_EVENT_GFX_SPECIES(X)` vale `SPECIES_X + OBJ_EVENT_MON`, e a constante
    existe para TODA espécie: quem decide se há desenho é a macro `OVERWORLD(`
    do `species_info`. Espécie sem ela vira objeto sem gráfico no mapa, que é
    exatamente a armadilha que `sprites_utilizaveis()` documenta para os
    sprites de gente. Por isso a conferência é a mesma que o `censo_dex.py`
    já usa para decidir quem pode ser encontro estático.
    """
    import censo_dex
    return censo_dex.com_overworld()


def confere(gids_usados=None):
    """Autoteste. Devolve lista de problemas (vazia = tudo certo)."""
    problemas = []
    desenhaveis = sprites_desenhaveis()
    com_ow = None
    nossas = None
    for gid, (cat, sprite, _) in sorted(TABELA.items()):
        if cat in ("pessoa", "placa"):
            if not sprite:
                problemas.append("id %d e %s e nao tem sprite" % (gid, cat))
            elif sprite not in desenhaveis:
                problemas.append("id %d aponta para %s, que esta build nao desenha"
                                 % (gid, sprite))
        elif cat == "pokemon" and sprite is not None:
            # Destino de espécie: mede species.h e a macro OVERWORLD(, nunca a
            # tabela de ponteiros de gente, onde ele nunca vai aparecer.
            m = ESPECIE.match(sprite)
            if not m:
                problemas.append("id %d e pokemon e o sprite %r nao e "
                                 "OBJ_EVENT_GFX_SPECIES(...)" % (gid, sprite))
                continue
            if com_ow is None:
                com_ow = especies_desenhaveis()
                nossas = set(re.findall(
                    r"\bSPECIES_[A-Z0-9_]+\b",
                    open(os.path.join(RAIZ,
                                      "include/constants/species.h")).read()))
            nome = "SPECIES_" + m.group(1)
            if nome not in nossas:
                problemas.append("id %d aponta para %s, que nao existe no "
                                 "nosso species.h" % (gid, nome))
            elif nome not in com_ow:
                problemas.append("id %d aponta para %s, que nao tem OVERWORLD( "
                                 "no species_info: nao ha o que desenhar"
                                 % (gid, nome))
        elif sprite is not None:
            problemas.append("id %d e %s e nao devia ter sprite" % (gid, cat))
    if PADRAO not in desenhaveis:
        problemas.append("o sprite padrao %s nao e desenhavel" % PADRAO)

    if os.path.exists(ROM_DEMAKE):
        medido = mede_rom()
        for gid in sorted(TABELA):
            if gid not in medido:
                problemas.append("id %d nao existe na tabela da ROM" % gid)
        # A tabela viva tem 240 entradas: se a ROM mudar de versao e ela
        # encolher, o numero abaixo muda e o caso morre aqui, nao no jogo.
        if len(medido) != N_GFX:
            problemas.append("tabela da ROM tem %d entradas, esperado %d"
                             % (len(medido), N_GFX))
    else:
        problemas.append("ROM do demake nao encontrada em %s" % ROM_DEMAKE)

    if gids_usados:
        faltando = sorted(g for g in gids_usados
                          if g not in TABELA and g < PRIMEIRO_VAR)
        if faltando:
            problemas.append("ids usados sem linha na tabela: %s" % faltando)
    return problemas


def main():
    demo = "--demo" in sys.argv
    problemas = confere()
    cats = {}
    for gid, (cat, sprite, _) in TABELA.items():
        cats.setdefault(cat, []).append(gid)
    print("tabela de gfx de Galar: %d ids classificados de %d na tabela da ROM"
          % (len(TABELA), N_GFX))
    for cat in ("pessoa", "placa", "pokemon", "cenario"):
        ids = cats.get(cat, [])
        print("  %-8s %3d ids" % (cat, len(ids)))
    destinos = sorted({s for c, s, _ in TABELA.values() if s})
    print("  sprites nossos usados: %d (%s)" % (len(destinos), ", ".join(
        d.replace("OBJ_EVENT_GFX_", "") for d in destinos)))
    if problemas:
        print("\nPROBLEMAS:")
        for p in problemas:
            print("  -", p)
        return 1
    print("\nautoteste: OK")
    if demo:
        medido = mede_rom()
        print("geometria medida na ROM (amostra):")
        for gid in (0, 17, 92, 148, 151, 162, 229):
            print("   id %3d %s  %s" % (gid, medido[gid], TABELA[gid][2][:60]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
