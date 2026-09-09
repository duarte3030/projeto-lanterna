#!/usr/bin/env python3
"""Refino de `FloaromaTown` (tema CAMPO FLORIDO, a cidade das flores de Sinnoh)
no par `gTileset_GeneralSinnoh` + `gTileset_MauvilleSinnoh`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: `FloaromaTown` tem 819 células andáveis a pé e gasta
31,4% delas (257 células) com o metatile 1, a grama lisa do primário, mais 24,2%
(198 células) com o metatile 521 e mais 23,6% (193 células) com o metatile 528.
Os três somam 79,1% do chão. Ou seja: a cidade inteira é feita de TRÊS tapetes
chapados, e dois deles são justamente os canteiros de flor, repetidos célula a
célula sem uma única variação em 391 quadrados.

TRÊS CARIMBOS, e não dois. Derrubar só o metatile 1 deixaria o 521 como
dominante com 24,2%, acima do teto de 20% da onda; derrubar 1 e 521 deixaria o
528 com 23,6%. Solidificar célula ainda TIRA do denominador, então quebrar dois
carimbos pode SUBIR a fração do terceiro. As três famílias são tratadas juntas,
cada uma com o próprio catálogo e a própria medida antes e depois.

A ARMADILHA QUE MANDA NESTA PASSADA, conferida em `src/tileset_anims.c` e não
lembrada: `gTileset_MauvilleSinnoh` declara `.callback = InitTilesetAnim_Mauville`
(`src/data/tilesets/headers.h:142`), e essa animação escreve, TODO quadro, em 64
vagas de tile do secundário. As duas listas de destino
(`gTilesetAnims_Mauville_Flower1_VDests` e `..._Flower2_VDests`,
`src/tileset_anims.c:224` e `:235`) são oito ponteiros cada, de quatro tiles
cada, a partir de `NUM_TILES_IN_PRIMARY + 96` e `+ 128`. Isso PINA as vagas 96 a
159: qualquer arte gravada ali é apagada pela animação no primeiro quadro, sem
erro de build e sem aviso. Esta passada não grava UM BYTE em `tiles.png`, então
a armadilha não chega a ser tocada; mas ela é o motivo de a arte nova ser
composta em vez de importada, e por isso está medida aqui.

E É AQUI QUE ESTÁ A DESCOBERTA QUE MUDA A RODADA: os dois carimbos de flor SÃO
essas vagas pinadas. O metatile 521 desenha os tiles 100, 101, 102 e 103 com a
paleta 8, e o 528 desenha os tiles 128, 129, 130 e 131 com a paleta 9 (lido do
`metatiles.bin`, não da memória). Ou seja, as 391 células de canteiro de
Floaroma são as duas flores ANIMADAS de Mauville, cada uma com o desenho da
flor em cima e a folhagem embaixo. Referenciar essas vagas custa ZERO e mantém
a animação; gravar nelas seria o defeito.

O QUE O `Pokémon Light Platinum` TINHA PARA OFERECER, dito com número em vez de
com adjetivo, porque a resposta foi NÃO e uma resposta dessas precisa de prova:

  - A folha de contato do hack inteiro foi montada com
    `fontes-mapas/romhacks/ferramentas/folha_tema.py` (40 secundários com
    `frac_nova >= 0.5`, três folhas), e depois os oito secundários de EXTERIOR
    verde do grupo 0 ganharam atlas de metatile cheio.
  - A GRAMA do primário do hack (`0x286CF4`, paleta 2) é (136,184,80), um verde
    amarelado. A nossa grama (metatile 1) é (115,197,164). A distância é 87,6,
    contra o critério duro de 50 desta onda (o mesmo que tirou o calçamento do
    hack de `praca_hearthome.py` e a areia de `brejo_pastoria.py`). TODA flor
    desenhada no hack está pousada nesse verde, porque no hack a flor é CHÃO;
    importar qualquer uma delas traria um retalho de outro verde no meio do
    campo, que é o defeito nº 1 da lista do `enfeita_cidades.py`.
  - Sobrou a hipótese de importar só a camada de CIMA (a regra apertada do
    `brejo_pastoria.py`). Foi medida: varrendo os treze secundários de exterior
    do hack, os metatiles com camada de cima, com o chão VERDE embaixo (75% ou
    mais de pixel verde) e com pixel de cor de flor na camada de cima são 68, e
    olhando a folha deles um a um o que existe é TELHADO, FARDO DE FENO, POSTE
    DE LUZ e TOLDO. Não há um canteiro, não há uma fileira de flor, não há
    vocabulário de jardim. A cidade das flores do Light Platinum não existe.

ENTÃO A ARTE DESTA PASSADA É DERIVADA, e a origem está dita peça a peça no
`campo_floaroma.json`. São três operações, e nenhuma delas grava um tile novo:

  - MISTURA. Cada entrada de metatile carrega a PRÓPRIA vaga de paleta e os
    PRÓPRIOS bits de espelho. Misturar o quadrante da flor rosa (tile 100,
    paleta 8) com o da flor amarela (tile 129, paleta 9) no mesmo metatile custa
    ZERO tile e ZERO cor, e o resultado é um canteiro de duas cores que continua
    ANIMADO nos dois lados, porque as duas vagas continuam sendo as pinadas.
  - ESPELHO. As flores não são simétricas (a rosa tem o miolo amarelo à
    esquerda e a branca o reflexo à direita), então espelhar troca o desenho de
    verdade. O portão do `varia_carimbo.py` cobra distância mínima de 8,0 entre
    duas variantes de chão, e o caso 6 do auto-teste mede isso peça a peça.
  - RECOLORAÇÃO EM VAGA LIVRE. Os oito tiles de flor usam só os índices 2, 3, 4,
    5, 6, 9, 10, 12 e 13 (contado tile a tile), e os DEZ quadros de animação
    (`data/tilesets/secondary/mauville/anim/flower_{1,2}/{0..4}.png`) usam
    exatamente o mesmo conjunto. Os índices 2, 3, 4, 12 e 13 são o verde e os
    5, 6, 9 e 10 são a flor. Copiando a paleta 8 para uma vaga LIVRE e trocando
    só esses quatro índices nasce um canteiro de outra cor, com o mesmo verde de
    fundo, animado, custando ZERO tile e UMA vaga de paleta. São duas: a vaga 10
    vira a PAPOULA (vermelho e laranja) e a vaga 12 vira a LAVANDA (violeta e
    lilás). As duas vagas estão 100% livres: contando por metatile VIVO nos
    QUATRO layouts que dividem este secundário, as vagas usadas são 0, 1, 2, 3,
    4, 5, 7, 8, 9 e 11, e a armadilha 4 do `compacta_paletas.py` (metatile do
    PRIMÁRIO alcançável pintando com vaga >= 6) mede ZERO entradas.

E MUITA COISA JÁ ESTAVA DESENHADA E MORTA. O `metatiles.bin` deste secundário
tem 512 entradas e só 126 delas aparecem em `map.bin` de algum dos quatro
layouts irmãos: 386 metatiles são lixo morto de dumper. Entre eles, desenhados
pixel a pixel SOBRE a nossa grama (camada de baixo idêntica, bit a bit, à do
metatile 1), estavam o canteiro com moldura de madeira (692), a jardineira
(700), a floreira comprida (691), os tocos de madeira (656, 657, 658, 697, 698),
o arbusto florido (686) e a cerca viva de três peças (904, 905, 906). Usar um
metatile morto custa ZERO: basta escrever o id no `map.bin`. O que esta passada
gasta com eles é só a vaga de metatile das versões que precisam de OUTRA camada
de baixo (a jardineira pousada no canteiro rosa, por exemplo).

O ORÇAMENTO, medido nesta árvore e não chutado:

  - TILE. `tiles.png` é 128x256, ou seja 512 de 512 vagas: CHEIO. Esta passada
    não grava nenhuma, e por isso o arquivo sai do commit sem um byte de
    diferença. As 113 vagas que metatile vivo referencia continuam intactas e as
    64 pinadas pela animação também.
  - METATILE. `metatiles.bin` tem 512 de 512 entradas: CHEIO TAMBÉM. Não há
    rabo para gravar, como havia em Pastoria. Esta passada grava nas vagas
    MORTAS, em ordem crescente, pulando toda vaga que algum dos quatro layouts
    usa e toda vaga que esta passada RESSUSCITA (metatile morto que ela escreve
    no mapa passa a ser vivo e não pode ser sobrescrito). O diff não é aditivo,
    e é exatamente por isso que a prova de ZERO PIXEL nos três mapas irmãos é
    obrigatória e vale de verdade.
  - PALETA. Duas vagas livres gravadas (10 e 12), nenhuma cor escrita em índice
    que algum pixel vivo use.

AS REGRAS DE MONTAGEM, e a armadilha que cada uma resolve:

  - CHÃO NOVO é metatile com arte só na camada de BAIXO e atributo IGUAL, bit a
    bit, ao do carimbo que ele substitui (0x0000 nos três). Camada de cima em
    célula andável com layerType NORMAL desenha ACIMA do jogador. A exceção são
    os TUFOS nossos, que desenham em cima de propósito desde o jogo base (o
    "jogador atrás do mato"); mesmo eles pagam o portão do E3 do `mapas_qa.py`,
    que é não tapar o jogador INTEIRO (256 pixels opacos).
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o chão do carimbo entrada por entrada, e o atributo é comportamento
    ZERADO com layerType COVERED (0x1000).
  - ENFEITE é a mesma montagem do móvel com atributo 0x0000: ele NÃO solidifica
    e NÃO encosta em nenhum portão de alcance. É o que deixa toco e cerca baixa
    entrarem no meio do campo sem mexer em colisão.
  - CADA PEÇA SABE SOBRE QUAIS CARIMBOS ELA POUSA, e aqui a lista é plural,
    diferente de Pastoria: os três carimbos têm o mesmo atributo e a mesma
    família de verde, então uma peça pode ser legítima em mais de um. Quem
    decide onde ela cai de fato é a especificação de bolha, não o catálogo.
  - Nenhum id de flag, var, script, música, treinador ou espécie é importado. Só
    ARTE. Comportamento é id semântico: todo móvel entra com o comportamento
    ZERADO.

A LEI DE COLISÃO desta onda: 0 -> 1 é PERMITIDA em célula que não seja caminho,
warp, evento nem alcance de script, desde que o alcance a pé continue o mesmo;
1 -> 0 é PROIBIDA e fica em ZERO células. Elevação intacta em 100% das palavras.
Os DOIS portões de alcance rodam NA HORA, peça a peça: busca em largura a partir
de warp e objeto, e casamento de COMPONENTES conexos.

O BLOCO PRÓPRIO DESTA PASSADA É O 198. O `enfeita_cidades.corredores_de_teste`
pula o bloco de teste da própria rodada de propósito, e o padrão dele é o
`175_cidades_enfeitadas.json`. O nome é trocado ANTES da primeira chamada
porque a função guarda o resultado em cache.

Uso:
    python3 dev_scripts/campo_floaroma.py                 # mede e mostra o plano
    python3 dev_scripts/campo_floaroma.py --aplicar
    python3 dev_scripts/campo_floaroma.py --desfazer      # devolve o map.bin
    python3 dev_scripts/campo_floaroma.py --demo          # auto-teste
    python3 dev_scripts/campo_floaroma.py --extrai        # regera o kit
    python3 dev_scripts/campo_floaroma.py --so-tileset    # so o tileset
    python3 dev_scripts/campo_floaroma.py --orcamento     # o que sobra no tileset
    python3 dev_scripts/campo_floaroma.py --folha saida.png   # a folha das pecas
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
# fosse escrito e a idempotência morria.
E.BLOCO_PROPRIO = "198_campo_floaroma.json"

DESTINO = f"{RAIZ}/data/tilesets/secondary/mauville_sinnoh"
KIT_JSON = f"{RAIZ}/dev_scripts/campo_floaroma_kit.json"
PLANO = f"{RAIZ}/dev_scripts/campo_floaroma.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_MauvilleSinnoh"
# Os QUATRO layouts vivos que dividem o `gTileset_MauvilleSinnoh`. A lista foi
# conferida nesta árvore lendo `data/layouts/layouts.json` e testando a
# existência do `map.bin` de cada um; cada layout tem exatamente um mapa.
IRMAOS = ["FloaromaTown", "Route205_South", "Route208", "ValleyWindworks"]

TETO_TILES = 512
TETO_META = 512
MARGEM = 2
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante abaixo de 20%

# As vagas de tile que `src/tileset_anims.c` reescreve a cada quadro. Esta
# passada REFERENCIA estas vagas (é onde a flor animada mora) e NUNCA grava
# nelas. Ver o docstring.
PINADAS = set(range(96, 160))

CARIMBOS = dict(grama=1, rosa=521, amarela=528)

# ------------------------------------------------------------------ a PALETA
# Vaga de paleta LIVRE -> (nome, {indice: cor nova}). O resto da vaga é cópia
# fiel da paleta 8, que é a das flores rosa: com isso o verde de fundo e o
# verde da folha ficam idênticos aos do carimbo e o canteiro novo não tem
# costura. Os índices trocados são exatamente os quatro que os oito tiles de
# flor e os dez quadros de animação usam para a FLOR (5 é o miolo, 6 é o tom
# pálido que as duas flores dividem, 9 é o corpo da segunda flor e 10 o da
# primeira); 11 nunca é tocado por nenhum dos dois, e por isso fica como está.
PAL_BASE = 8
PALETAS_NOVAS = {
    10: dict(nome="papoula", cores={5: (255, 255, 98), 6: (255, 222, 197),
                                    9: (255, 148, 98), 10: (222, 65, 65)}),
    12: dict(nome="lavanda", cores={5: (255, 255, 255), 6: (230, 213, 255),
                                    9: (189, 156, 246), 10: (148, 90, 205)}),
}

# Os oito tiles de flor, pelo LOCAL no secundário. `a` e `b` são as duas flores
# da linha de cima, `fe` e `fd` são a folhagem da linha de baixo.
T_ROSA = dict(a=100, b=101, fe=102, fd=103)
T_AMAR = dict(a=128, b=129, fe=130, fd=131)


def _pal_flor(qual):
    """(dicionário de tiles, vaga de paleta) da família de flor pedida."""
    return {"rosa": (T_ROSA, 8), "amarela": (T_AMAR, 9),
            "papoula": (T_ROSA, 10), "lavanda": (T_ROSA, 12)}[qual]


def q(qual, papel, h=False, v=False):
    """Uma ENTRADA de metatile apontando para um quadrante de flor.

    `qual` é a família de cor, `papel` é `a`, `b`, `fe` ou `fd`. O tile fica na
    faixa do secundário (por isso o `+ 512` na hora de escrever) e os bits de
    espelho são 0x400 (horizontal) e 0x800 (vertical).
    """
    tiles, vaga = _pal_flor(qual)
    return dict(loc=tiles[papel], pal=vaga, h=h, v=v)


# GRAMA do metatile 1: as quatro entradas da camada de baixo dele são lidas do
# `metatiles.bin` do primário e não escritas à mão, para que a peça nova siga o
# carimbo se ele mudar um dia. O quadrante de grama é SEMPRE o do metatile 1,
# mesmo numa peça que pousa no canteiro rosa ou no amarelo: os três carimbos são
# a mesma grama (os dois canteiros são a flor de Mauville desenhada sobre ela),
# e é justamente com esse quadrante que uma peça "rala" mostra o gramado por
# baixo do canteiro. Resolver o quadrante contra o carimbo de destino, e não
# contra a grama, foi um defeito real desta passada: em 09/09/2026 o "canteiro
# rosa ralo" saiu idêntico, pixel a pixel, ao próprio carimbo 521, e o caso 5 do
# auto-teste acusou com distância 0,0.
GR = ["grama0", "grama1", "grama2", "grama3"]

# ------------------------------------------------------------------- o CHÃO
# Cada peça é uma lista de QUATRO quadrantes da camada de BAIXO. String começada
# em `carimbo` é o quadrante correspondente da grama do metatile 1; dicionário é
# quadrante de flor. `sobre` é a lista de carimbos em que a peça é legítima.
CHAO = [
    # ---- sobre a GRAMA: flor SOLTA, que é o que faz um gramado virar campo
    # florido sem virar canteiro. Cada uma põe a flor num quadrante e a
    # folhagem embaixo dela, e o resto da célula continua sendo a grama do
    # carimbo, entrada por entrada.
    dict(nome="flor rosa a direita", sobre=["grama"],
         ents=[GR[0], q("rosa", "b"), GR[2], q("rosa", "fd")]),
    dict(nome="flor rosa a esquerda", sobre=["grama"],
         ents=[q("rosa", "a"), GR[1], q("rosa", "fe"), GR[3]]),
    dict(nome="flor amarela a direita", sobre=["grama"],
         ents=[GR[0], q("amarela", "b"), GR[2], q("amarela", "fd")]),
    # A MOITA é a mesma flor com a folhagem ocupando a linha de baixo inteira.
    # Ela existe porque "flor amarela a esquerda" ficaria a 7,3 de "flor rosa a
    # esquerda" (medido em 09/09/2026), abaixo do piso de 8,0 do
    # `varia_carimbo.py`: trocar SÓ a cor de uma flor de 30 pixels não move a
    # média de 256 pixels o bastante. Duas peças que só diferem na cor da flor
    # precisam diferir também na FORMA, e é isso que a moita faz.
    dict(nome="moita de flor amarela", sobre=["grama"],
         ents=[q("amarela", "a"), GR[1], q("amarela", "fe"), q("amarela", "fd")]),
    dict(nome="flor lavanda a esquerda", sobre=["grama"],
         ents=[q("lavanda", "a"), GR[1], q("lavanda", "fe"), GR[3]]),
    dict(nome="folhagem rasteira", sobre=["grama"],
         ents=[q("rosa", "fe"), q("rosa", "fd"),
               q("rosa", "fe", h=True), q("rosa", "fd", h=True)]),
    # O canteiro de PAPOULA é a única peça que serve nas duas pontas: solto no
    # gramado ele lê como um canteiro plantado, e dentro do campo rosa ele lê
    # como a faixa vermelha do canteiro. Por isso ele é um metatile SÓ, e não
    # dois iguais em famílias diferentes.
    dict(nome="canteiro papoula", sobre=["grama", "rosa"],
         ents=[q("papoula", "a"), q("papoula", "b"),
               q("papoula", "fe"), q("papoula", "fd")]),

    # ---- sobre o canteiro ROSA
    dict(nome="canteiro rosa espelhado", sobre=["rosa"],
         ents=[q("rosa", "b", h=True), q("rosa", "a", h=True),
               q("rosa", "fd", h=True), q("rosa", "fe", h=True)]),
    dict(nome="canteiro rosa denso", sobre=["rosa"],
         ents=[q("rosa", "a"), q("rosa", "b"),
               q("rosa", "a", v=True), q("rosa", "b", v=True)]),
    dict(nome="canteiro rosa e amarelo", sobre=["rosa"],
         ents=[q("rosa", "a"), q("amarela", "b"),
               q("rosa", "fe"), q("amarela", "fd")]),
    dict(nome="canteiro lavanda e rosa", sobre=["rosa"],
         ents=[q("lavanda", "a"), q("rosa", "b"),
               q("lavanda", "fe"), q("rosa", "fd")]),
    dict(nome="canteiro rosa ralo", sobre=["rosa"],
         ents=[GR[0], q("rosa", "b"), q("rosa", "fe"), q("rosa", "fd")]),

    # ---- sobre o canteiro AMARELO. A mistura aqui é a IMAGEM ESPELHADA da
    # mistura do canteiro rosa (amarelo à esquerda em vez de à direita), e isso
    # não é enfeite de simetria: `canteiro rosa e amarelo` fica a 7,3 do carimbo
    # 528 e por isso não pode servir nas duas famílias.
    dict(nome="canteiro amarelo espelhado", sobre=["amarela"],
         ents=[q("amarela", "b", h=True), q("amarela", "a", h=True),
               q("amarela", "fd", h=True), q("amarela", "fe", h=True)]),
    dict(nome="canteiro amarelo denso", sobre=["amarela"],
         ents=[q("amarela", "a"), q("amarela", "b"),
               q("amarela", "a", v=True), q("amarela", "b", v=True)]),
    dict(nome="canteiro amarelo e rosa", sobre=["amarela"],
         ents=[q("amarela", "a"), q("rosa", "b"),
               q("amarela", "fe"), q("rosa", "fd")]),
    dict(nome="canteiro lavanda", sobre=["amarela"],
         ents=[q("lavanda", "a"), q("lavanda", "b"),
               q("lavanda", "fe"), q("lavanda", "fd")]),
    dict(nome="canteiro lavanda e amarelo", sobre=["amarela"],
         ents=[q("amarela", "b", h=True), q("lavanda", "a", h=True),
               q("amarela", "fd", h=True), q("lavanda", "fe", h=True)]),
    dict(nome="canteiro amarelo ralo", sobre=["amarela"],
         ents=[q("amarela", "a"), GR[1], q("amarela", "fe"), q("amarela", "fd")]),
]

# TUFO NOSSO, de graça: metatile do PRIMÁRIO já desenhado sobre a camada de
# baixo do metatile 1, com o atributo IGUAL ao dele. Custa ZERO tile, ZERO cor e
# ZERO vaga de metatile enquanto entra como está.
TUFO_NOSSO = [
    dict(nome="moita clara",   mt=14),
    dict(nome="tufo fundo",    mt=30),
    dict(nome="tufo torto",    mt=31),
    dict(nome="tufo claro",    mt=462),
    dict(nome="tufo aberto",   mt=463),
    dict(nome="moita cerrada", mt=470),
    dict(nome="moita larga",   mt=471),
]
# VARIANTE POR ESPELHO da camada de cima do tufo: não custa tile nem cor, só a
# vaga de metatile. O caso 6 do auto-teste é quem prova que o espelho muda o
# desenho de verdade.
# SÓ DOIS, e a lista foi fechada por medição em 09/09/2026, não por gosto: o
# metatile 14 é simétrico e o espelho dele dá distância 0,0 contra o original; o
# 30 e o 31 já SÃO um par espelhado um do outro no tileset, e o 470 e o 471
# também, então espelhar qualquer um dos quatro devolve o irmão que já está no
# catálogo. Sobram o 462 e o 463.
ESPELHO_TUFO = [462, 463]

# ----------------------------------------------------------------- os MÓVEIS
# `fonte` é o metatile de onde a CAMADA DE CIMA é copiada; a de baixo é sempre
# a do carimbo em que a peça pousa. `solido` diz se a célula vira sólida
# (COVERED, 0x1000) ou continua andável (0x0000, o ENFEITE).
MOVEIS = [
    dict(nome="moita de flores",  fonte=4,   solido=True,
         sobre=["grama", "rosa", "amarela"]),
    dict(nome="canteiro com moldura", fonte=692, solido=True,
         sobre=["grama", "rosa", "amarela"]),
    dict(nome="jardineira",       fonte=700, solido=True,
         sobre=["grama", "rosa", "amarela"]),
    dict(nome="floreira comprida", fonte=691, solido=True, sobre=["grama"]),
    dict(nome="arbusto florido",  fonte=686, solido=True, sobre=["grama", "rosa"]),
    dict(nome="vaso de planta",   fonte=713, solido=True, sobre=["grama"]),
    dict(nome="toco de madeira",  fonte=656, solido=True, sobre=["grama"]),
    dict(nome="toco duplo",       fonte=657, solido=True, sobre=["grama"]),
    dict(nome="pedra do jardim",  fonte=224, solido=True, sobre=["grama"]),
    dict(nome="toco baixo",       fonte=697, solido=False, sobre=["grama"]),
    dict(nome="toco baixo torto", fonte=698, solido=False, sobre=["grama"]),
]

# BLOCO horizontal: uma fileira de `len(fontes)` células, todas sólidas. A cerca
# viva de Mauville é desenhada em três peças (esquerda, meio e direita) e só lê
# como cerca inteira; peça solta dela lê como erro de mapa.
BLOCOS = [
    dict(nome="cerca viva", fontes=[904, 905, 906], sobre="grama"),
]

FLOAROMA = dict(
    alvo="FloaromaTown",
    # OS GRUPOS SÃO GRANDES DE PROPÓSITO: grupo de uma peça só faz cada bolha
    # sair de uma cor única, e aí saber onde a célula está passa a adivinhar o
    # que ela é (caso 11a do auto-teste).
    bolhas=dict(
        grama=[
            dict(grupo=["flor rosa a direita", "flor rosa a esquerda",
                        "tufo claro", "canteiro papoula"],          quantas=18, tam=(9, 22)),
            dict(grupo=["flor amarela a direita", "moita de flor amarela",
                        "flor lavanda a esquerda", "tufo aberto"],  quantas=18, tam=(9, 22)),
            dict(grupo=["moita clara", "tufo fundo", "tufo torto",
                        "folhagem rasteira"],                       quantas=18, tam=(9, 20)),
            dict(grupo=["moita cerrada", "moita larga",
                        "tufo claro espelhado", "tufo aberto espelhado"],
                 quantas=18, tam=(9, 20)),
        ],
        rosa=[
            dict(grupo=["canteiro rosa espelhado", "canteiro rosa denso",
                        "canteiro rosa e amarelo"],                 quantas=9, tam=(12, 22)),
            dict(grupo=["canteiro papoula", "canteiro lavanda e rosa",
                        "canteiro rosa ralo"],                      quantas=9, tam=(12, 22)),
        ],
        amarela=[
            dict(grupo=["canteiro amarelo espelhado", "canteiro amarelo denso",
                        "canteiro amarelo e rosa"],                 quantas=9, tam=(12, 22)),
            dict(grupo=["canteiro lavanda", "canteiro lavanda e amarelo",
                        "canteiro amarelo ralo"],                   quantas=9, tam=(12, 22)),
        ],
    ),
    moveis=[
        dict(nome="canteiro com moldura", sobre="grama",   quantos=4, espaco=7),
        dict(nome="canteiro com moldura", sobre="rosa",    quantos=3, espaco=7),
        dict(nome="jardineira",           sobre="grama",   quantos=4, espaco=7),
        dict(nome="jardineira",           sobre="amarela", quantos=3, espaco=7),
        dict(nome="moita de flores",      sobre="rosa",    quantos=3, espaco=7),
        dict(nome="moita de flores",      sobre="amarela", quantos=3, espaco=7),
        dict(nome="floreira comprida",    sobre="grama",   quantos=3, espaco=8),
        dict(nome="arbusto florido",      sobre="grama",   quantos=4, espaco=7),
        dict(nome="arbusto florido",      sobre="rosa",    quantos=2, espaco=8),
        dict(nome="vaso de planta",       sobre="grama",   quantos=3, espaco=8),
        dict(nome="toco de madeira",      sobre="grama",   quantos=3, espaco=8),
        dict(nome="toco duplo",           sobre="grama",   quantos=3, espaco=8),
        dict(nome="pedra do jardim",      sobre="grama",   quantos=2, espaco=9),
        dict(nome="toco baixo",           sobre="grama",   quantos=4, espaco=6),
        dict(nome="toco baixo torto",     sobre="grama",   quantos=4, espaco=6),
    ],
    blocos=[
        dict(nome="cerca viva", sobre="grama", quantos=3, espaco=9),
    ],
)
TEMAS = {"FloaromaTown": FLOAROMA}
ORDEM = ["FloaromaTown"]

ESPACO_ENTRE_MOVEIS = 2     # Chebyshev mínimo entre dois móveis QUAISQUER
PISO_BOLHA = 6              # tamanho mínimo de uma bolha que a região cortou

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
    for i in (1, 0, 3, 2):
        v = quad[i]
        fora.append(0 if (v & 0x3FF) == 0 else (v ^ 0x400))
    return fora


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def _vivos(guardado=None):
    """{ids de metatile que algum dos QUATRO layouts irmãos desenha}.

    A grade do ALVO entra pela base LIMPA desta passada (o disco menos o que
    esta passada gravou), e não pelo disco: sem isso a segunda rodada reprova a
    si mesma, porque o `map.bin` já usa os ids que ela mesma escreveu.
    """
    if guardado is None:
        guardado = carrega_plano()
    vivos = set()
    for nome in IRMAOS:
        grade = (base_de(nome, guardado) if nome in TEMAS else G.grade(nome)[4])
        vivos |= {c & 0x3FF for c in grade}
    return vivos


def _metatiles_da_passada():
    """Todo metatile MORTO que esta passada escreve no `map.bin` como está.

    Ele deixa de ser morto no instante em que o mapa o usa, e por isso a vaga
    dele não pode ser reaproveitada para gravar metatile novo. Sem esta conta a
    passada se apagaria sozinha: a jardineira 700 seria reescrita como canteiro
    lavanda e o mapa desenharia lavanda onde o plano diz jardineira.
    """
    usados = {c["mt"] for c in TUFO_NOSSO}
    usados |= {m["fonte"] for m in MOVEIS}
    usados |= {f for b in BLOCOS for f in b["fontes"]}
    return usados


def orcamento(guardado=None):
    """(vagas de cor livres por vaga, vagas de METATILE mortas, vivos, arm4).

    "Vivo" é a palavra que importa duas vezes aqui. O `gTileset_MauvilleSinnoh`
    tem 512 metatiles e só 126 aparecem em `map.bin` de algum dos quatro
    layouts com arquivo em disco; o `tiles.png` tem 512 tiles e só 113 do
    secundário são referenciados por metatile vivo. Contar os 512 daria tileset
    cheio e nada a fazer.

    O portão que prova que isso é verdade não está aqui, está no render dos três
    mapas irmãos com ZERO pixel diferente.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    usados = collections.defaultdict(set)
    tiles_vivos = set()
    vivos = _vivos(guardado)
    reservados = _metatiles_da_passada()
    for gid in sorted(x for x in vivos if x >= 512):
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], gid - 512):
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
    NP = len(tp["tiles"])
    mortas_meta = [local for local in range(TETO_META)
                   if (512 + local) not in vivos
                   and (512 + local) not in reservados]
    mortas_tile = [t - NP for t in range(NP, NP + TETO_TILES)
                   if t not in tiles_vivos]
    return livres, mortas_meta, mortas_tile, sorted(vivos), arm4


# ---------------------------------------------------------------- a EXTRACAO
def extrai():
    """Regera `campo_floaroma_kit.json`.

    Diferente das passadas anteriores desta onda, aqui NÃO há ROM de fonte: a
    triagem do `Pokémon Light Platinum` foi feita e REPROVOU (ver o docstring do
    módulo), então o kit é derivado do nosso próprio par de tilesets. O que ele
    guarda é (a) as duas paletas novas já resolvidas cor a cor, (b) o mapa de
    índices que cada tile de flor usa, que é a prova de que trocar só quatro
    índices basta, e (c) o veredito da triagem, para que ninguém precise refazer
    a medição para saber por que nada foi importado.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    livres, mortas_meta, mortas_tile, _vv, arm4 = orcamento()

    indices = {}
    for qual, tiles in (("rosa", T_ROSA), ("amarela", T_AMAR)):
        for papel, loc in sorted(tiles.items()):
            tile = RM.resolver_tile(tp, ts, len(tp["tiles"]) + loc)
            indices["%s:%s:%d" % (qual, papel, loc)] = sorted(
                {c for linha in tile for c in linha if c})
    # Os DEZ quadros de animação. Se um deles usasse um índice fora do conjunto
    # dos tiles, trocar a paleta pintaria de errado só durante a animação, que é
    # o defeito mais difícil de ver que esta passada poderia ter.
    from PIL import Image
    anim = {}
    for nome in ("flower_1", "flower_2"):
        vistos = set()
        for i in range(5):
            im = Image.open("%s/data/tilesets/secondary/mauville/anim/%s/%d.png"
                            % (RAIZ, nome, i))
            vistos |= {c for c in im.getdata() if c}
        anim[nome] = sorted(vistos)

    paletas = {}
    base = [list(c) for c in ts["paletas"][PAL_BASE]]
    for vaga, spec in sorted(PALETAS_NOVAS.items()):
        vagos = set(livres.get(vaga) or [])
        cores = [list(c) for c in base]
        for i, cor in sorted(spec["cores"].items()):
            if i not in vagos:
                raise SystemExit("a vaga %d nao tem o indice %d livre" % (vaga, i))
            cores[i] = list(cor)
        paletas[str(vaga)] = cores

    dados = dict(
        triagem=dict(
            fonte="Pokémon Light Platinum, de WesleyFG, sobre base Pokémon Ruby "
                  "(AXVE), md5 7fd2c08735459d99fa23fdaa9b755486",
            veredito="REPROVADA: nada foi importado",
            grama_do_hack=[136, 184, 80], grama_nossa=[115, 197, 164],
            distancia_de_cor=87.6, criterio_da_onda=50.0,
            pecas_de_cima_com_chao_verde=68,
            o_que_eram="telhado, fardo de feno, poste de luz e toldo; nenhum "
                       "canteiro, nenhuma fileira de flor, nenhum jardim",
            folha_de_contato="fontes-mapas/romhacks/ferramentas/folha_tema.py, "
                             "40 secundários com frac_nova >= 0,5",
        ),
        derivacao=dict(
            metodo="mistura de quadrante, espelho e recoloração em vaga de "
                   "paleta livre; ZERO tile novo",
            paleta_base=PAL_BASE,
            indices_dos_tiles=indices,
            indices_da_animacao=anim,
            vagas_pinadas=[min(PINADAS), max(PINADAS)],
        ),
        tiles_png_md5=__import__("hashlib").md5(_ler("tiles.png")).hexdigest(),
        vagas_livres={str(k): v for k, v in livres.items()},
        vagas_meta_mortas=mortas_meta,
        vagas_tile_mortas=mortas_tile,
        armadilha4=arm4,
        paletas=paletas,
    )
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1, ensure_ascii=False)
    print("kit gravado em %s: %d paletas, %d vagas de metatile mortas"
          % (os.path.relpath(KIT_JSON, RAIZ), len(paletas), len(mortas_meta)))
    for vaga, spec in sorted(PALETAS_NOVAS.items()):
        print("  vaga %2d (%s): indices %s trocados"
              % (vaga, spec["nome"], sorted(spec["cores"])))
    for nome, idx in sorted(anim.items()):
        print("  animacao %s usa os indices %s" % (nome, idx))
    return 0


def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai" % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


# --------------------------------------------------------------- o DESENHO
def chao_do_carimbo(qual):
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele)."""
    mt = CARIMBOS[qual]
    tset = _tileset(PRIMARIO) if mt < 512 else _tileset(SECUNDARIO)
    loc = mt if mt < 512 else mt - 512
    ents = list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))
    if any(v & 0x3FF for v in ents[4:]):
        raise SystemExit("o carimbo %d ja usa a camada de cima" % mt)
    attr = (G._attrs(PRIMARIO)[mt] if mt < 512
            else G._attrs(SECUNDARIO)[mt - 512])
    return ents[:4], attr


def desenha_kit(guardado=None):
    """(metas, attrs, catalogo), sem escrever em disco."""
    dados = kit()
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    NP = len(tp["tiles"])
    ap = G._attrs(PRIMARIO)
    asec = G._attrs(SECUNDARIO)

    BASE = {qual: chao_do_carimbo(qual) for qual in CARIMBOS}
    metas, attrs = {}, {}
    vagas_meta = list(dados["vagas_meta_mortas"])
    proximo = [0]
    catalogo = dict(chao={}, moveis={}, blocos={}, sobre={}, solido={})

    def poe(ents, attr):
        if proximo[0] >= len(vagas_meta):
            raise SystemExit("acabaram as vagas de metatile mortas")
        local = vagas_meta[proximo[0]]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo[0] += 1
        return 512 + local

    def entrada(spec, qual_base):
        """Traduz um quadrante do catálogo em entrada de metatile."""
        if isinstance(spec, str):
            return BASE["grama"][0][int(spec[-1])]
        loc = spec["loc"]
        return ((spec["pal"] << 12)
                | (0x400 if spec["h"] else 0) | (0x800 if spec["v"] else 0)
                | (NP + loc))

    def cima_de(mt):
        tset, loc = (tp, mt) if mt < 512 else (ts, mt - 512)
        return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))[4:]

    # ------------------------------------------------------ 1. CHAO DERIVADO
    for c in CHAO:
        ents = [entrada(x, c["sobre"][0]) for x in c["ents"]]
        gid = poe(ents + [0, 0, 0, 0], BASE[c["sobre"][0]][1])
        catalogo["chao"][c["nome"]] = gid
        catalogo["sobre"][c["nome"]] = list(c["sobre"])

    # ------------------------------------------------------ 2. TUFO NOSSO
    base_grama, attr_grama = BASE["grama"]
    for c in TUFO_NOSSO:
        if ap[c["mt"]] != attr_grama:
            raise SystemExit("o metatile %d tem atributo 0x%04X e o carimbo de "
                             "grama tem 0x%04X" % (c["mt"], ap[c["mt"]], attr_grama))
        ents = list(struct.unpack_from("<8H", tp["metatiles"], c["mt"] * 16))
        if ents[:4] != base_grama:
            raise SystemExit("o metatile %d nao esta desenhado sobre a grama do "
                             "carimbo" % c["mt"])
        catalogo["chao"][c["nome"]] = c["mt"]
        catalogo["sobre"][c["nome"]] = ["grama"]
    por_mt = {c["mt"]: c["nome"] for c in TUFO_NOSSO}
    for mt in ESPELHO_TUFO:
        ents = list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))
        nome = por_mt[mt] + (" espelhada" if por_mt[mt].startswith("moita")
                             else " espelhado")
        gid = poe(list(base_grama) + _espelha4(ents[4:]), attr_grama)
        catalogo["chao"][nome] = gid
        catalogo["sobre"][nome] = ["grama"]

    # ------------------------------------------------------ 3. MOVEIS
    for m in MOVEIS:
        cima = cima_de(m["fonte"])
        if not any(v & 0x3FF for v in cima):
            raise SystemExit("%s: o metatile %d nao tem camada de cima"
                             % (m["nome"], m["fonte"]))
        for qual in m["sobre"]:
            base, attr_chao = BASE[qual]
            # comportamento ZERADO (nenhum id semântico é importado); COVERED
            # quando a peça solidifica, e o atributo do chão quando ela é só
            # enfeite e a célula continua andável.
            attr = 0x1000 if m["solido"] else attr_chao
            gid = poe(list(base) + list(cima), attr)
            catalogo["moveis"]["%s|%s" % (m["nome"], qual)] = gid
            catalogo["sobre"]["%s|%s" % (m["nome"], qual)] = [qual]
            catalogo["solido"]["%s|%s" % (m["nome"], qual)] = m["solido"]

    # ------------------------------------------------------ 4. BLOCOS
    for b in BLOCOS:
        base, _a = BASE[b["sobre"]]
        ids = []
        for fonte in b["fontes"]:
            cima = cima_de(fonte)
            if not any(v & 0x3FF for v in cima):
                raise SystemExit("%s: o metatile %d nao tem camada de cima"
                                 % (b["nome"], fonte))
            ids.append(poe(list(base) + list(cima), 0x1000))
        catalogo["blocos"][b["nome"]] = ids
        catalogo["sobre"][b["nome"]] = [b["sobre"]]

    # A vaga de metatile só serve se NENHUM dos quatro mapas usar o id e se esta
    # passada não estiver escrevendo o mapa com ele.
    vivos = _vivos(guardado)
    reservados = _metatiles_da_passada()
    for local in metas:
        if 512 + local in vivos:
            raise SystemExit("algum dos 4 mapas usa o metatile %d" % (512 + local))
        if 512 + local in reservados:
            raise SystemExit("o metatile %d e usado como esta por esta passada"
                             % (512 + local))
    # Nenhum tile novo: a passada não pode ter pedido vaga pinada para gravar.
    return metas, attrs, catalogo


def grava_tileset(metas, attrs):
    """Escreve palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    `tiles.png` NÃO é tocado: esta passada não cria um tile sequer, e é isso que
    torna a prova de zero pixel dos três mapas irmãos barata de acreditar.
    Idempotente: as vagas de paleta e de metatile são FIXAS.
    """
    dados = kit()
    for vaga, cores in sorted(dados["paletas"].items()):
        _grava_pal(int(vaga), cores)
    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
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
                if any(max(abs(p[0] - s[0]), abs(p[1] - s[1])) < 2
                       for s in sementes):
                    continue
                lo, hi = esp["tam"]
                alvo = lo + _mistura(p[0], p[1], 0xB10B) % (hi - lo + 1)
                corpo, frente = {p}, set()
                for dx, dy in N4:
                    r = (p[0] + dx, p[1] + dy)
                    if r in livres and r not in tomadas:
                        frente.add(r)
                while len(corpo) < alvo and frente:
                    r = min(frente, key=lambda z: _mistura(z[0], z[1], 0xC0FFEE))
                    frente.discard(r)
                    corpo.add(r)
                    for dx, dy in N4:
                        z = (r[0] + dx, r[1] + dy)
                        if z in livres and z not in tomadas and z not in corpo:
                            frente.add(z)
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
    for p, r in antes.items():
        if p not in solidificadas:
            por_rotulo[r].add(p)
    for r, cels in por_rotulo.items():
        if len({depois.get(p) for p in cels}) > 1:
            mau.append("o pedaco %d de chao se partiu em %d"
                       % (r, len({depois.get(p) for p in cels})))
    juntou = collections.defaultdict(set)
    for p, r in depois.items():
        if p in antes:
            juntou[r].add(antes[p])
    for r, origens in juntou.items():
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

    # As TRÊS famílias de chão. Uma célula só é elegível se ainda for o carimbo
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

    escritas = {}
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(alvo, v, W, H, d)
    # DOIS GELOS, e a diferença é a razão de o campo de Floaroma ficar inteiro
    # em vez de listrado. O `corredores_de_teste` congela as células que a suíte
    # já anda, e o próprio docstring dele diz o que ele protege: "enfeite SÓLIDO
    # não pode cair numa delas", porque perna saturante para no primeiro
    # obstáculo. Trocar o CHÃO de uma dessas células não é obstáculo: o
    # (comportamento, layerType) continua idêntico bit a bit, a colisão continua
    # 0 e a perna anda exatamente o mesmo tanto. O mesmo vale para a orla de uma
    # célula em volta de cada evento: ela existe para não fechar a saída de um
    # NPC, e chão não fecha nada. Medido em 09/09/2026 nesta árvore: com o gelo
    # único, 86 das 257 células de grama ficavam de fora, e 18 delas são a
    # coluna 4 inteira, que corta o campo rosa de cima a baixo e deixaria uma
    # listra de carimbo puro atravessando o mapa. O que continua congelado para
    # o chão é a célula do EVENTO em si (porta, placa e NPC pousam nela).
    gelo_chao = set(ev)
    for idx, _a, _n in E.carrega_plano().get(alvo, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))
        gelo_chao.add((idx % W, idx // W))

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

    def espacado(chave, esp, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < esp
                       for px, py in por_movel[chave])

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

    def poe_enfeite(x, y, mt_id):
        """Enfeite não muda colisão: a célula continua andável."""
        i = y * W + x
        escritas[i] = (aplicado[i] & 0xFC00) | mt_id
        aplicado[i] = escritas[i]
        postos.append((x, y))
        return True

    ordem_cel = sorted(((x, y) for y in range(H) for x in range(W)),
                       key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF, p))

    # ------ 1. BLOCOS, antes da mobília de uma célula, porque cada um precisa
    # de uma fileira inteira e a mobília solta não pode ter comido metade dela.
    conta_bloco = collections.Counter()
    por_bloco = []
    for b in T["blocos"]:
        ids = catalogo["blocos"][b["nome"]]
        qual = b["sobre"]
        larg = len(ids)
        for x, y in ordem_cel:
            if conta_bloco[b["nome"]] >= b["quantos"]:
                break
            cels = [(x + k, y) for k in range(larg)]
            if any(not (0 <= cx < W) for cx, cy in cels):
                continue
            if any(not livre(cx, cy, qual) for cx, cy in cels):
                continue
            if any(max(abs(x - px), abs(y - py)) < b["espaco"]
                   for px, py in por_bloco):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            ok, feitas = True, []
            for k in range(larg):
                cx, cy = x + k, y
                if not tenta_solidificar(cx, cy, ids[k]):
                    ok = False
                    break
                feitas.append((cx, cy))
            if not ok:
                for cx, cy in feitas:
                    novos_solidos.remove((cx, cy))
                    postos.remove((cx, cy))
                    del escritas[cy * W + cx]
                    aplicado[cy * W + cx] = v[cy * W + cx]
                continue
            por_bloco += cels
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
            chave = "%s|%s" % (m["nome"], m["sobre"])
            if conta_mov[chave] >= m["quantos"]:
                continue
            qual = m["sobre"]
            if not livre(x, y, qual) or not espacado(chave, m["espaco"], x, y):
                continue
            # MÓVEL DE CIDADE ENCOSTA EM ALGUMA COISA: ou num sólido, ou na
            # BEIRA da própria família. Peça solta no meio do vazio lê como erro
            # de mapa.
            perto = any(not (0 <= x + dx < W and 0 <= y + dy < H)
                        or ((aplicado[(y + dy) * W + x + dx] >> 10) & 3)
                        or (x + dx, y + dy) not in fam[qual]
                        for dx, dy in N4)
            if not perto:
                continue
            gid = catalogo["moveis"][chave]
            if catalogo["solido"][chave]:
                if not tenta_solidificar(x, y, gid):
                    continue
            else:
                poe_enfeite(x, y, gid)
            por_movel[chave].append((x, y))
            conta_mov[chave] += 1
            break

    # ------------------------------------------------------------- 3. MANCHA
    conta_mancha = collections.Counter()

    def pintavel(p, qual):
        i = p[1] * W + p[0]
        if p[0] < MARGEM or p[1] < MARGEM or p[0] >= W - MARGEM or p[1] >= H - MARGEM:
            return False
        return (p in fam[qual] and i not in escritas and p not in gelo_chao
                and (aplicado[i] & 0x3FF) == CARIMBOS[qual])

    def pinta(p, nomes):
        i = p[1] * W + p[0]
        nome = peca_da_mancha(nomes, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | catalogo["chao"][nome]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    sementes = dict(grama=0x5EED, rosa=0xB0A7, amarela=0xF10A)
    for qual in ("grama", "rosa", "amarela"):
        pool = {p for p in fam[qual] if pintavel(p, qual)}
        for nomes, corpo in bolhas(pool, T["bolhas"][qual], sementes[qual]):
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
                  familias={k: len(s) for k, s in fam.items()})
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
    guardado = carrega_plano()
    metas, attrs, catalogo = desenha_kit(guardado)
    print("kit: %d metatiles novos em vaga MORTA (locais %d a %d, ids %d a %d), "
          "%d tiles novos" % (len(metas), min(metas), max(metas),
                              512 + min(metas), 512 + max(metas), 0))
    if aplicar:
        grava_tileset(metas, attrs)
    for alvo in alvos:
        base = base_de(alvo, guardado)
        L, W, H, v, escritas, contas = plano_mapa(alvo, catalogo, base)
        a, na, ida = regua(v, W, H, L)
        b, nb, idb = regua(v, W, H, L, escritas)
        print("%s: %d celulas de mancha, %d solidificadas, %d mudadas "
              "(familias %s)"
              % (alvo, sum(contas["manchas"].values()), contas["solidos"],
                 len(escritas), contas["familias"]))
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


def confere(alvos, metas, attrs, catalogo, planos):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela é chamada DUAS vezes pelo auto-teste: uma com o plano de verdade, que
    tem que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida só no caminho feliz não é regra, e prova positiva sem
    par negativo não é prova.
    """
    mau = []
    dados = kit()
    import render_maps as RM
    from PIL import Image
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    NP = len(tp["tiles"])
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
        tset, loc = (tp, mt_id) if mt_id < 512 else (ts, mt_id - 512)
        if loc * 16 + 16 > len(tset["metatiles"]):
            return [0] * 8
        return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))

    def px_de(mt_id):
        """Os 256 pixels RGB do metatile, com o kit desta rodada valendo."""
        im = Image.new("RGB", (16, 16), tuple(tp["paletas"][0][0]))
        p = im.load()
        for cam in (0, 1):
            for qd in range(4):
                val = entradas(mt_id)[cam * 4 + qd]
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if not idx:
                    continue
                tile = RM.resolver_tile(tp, ts, idx)
                if tile is None:
                    continue
                cores = (dados["paletas"].get(str(ip))
                         or (tp if ip < 6 else ts)["paletas"].get(ip))
                if cores is None:
                    continue
                RM.desenhar_tile(p, (qd % 2) * 8, (qd // 2) * 8, tile,
                                 [tuple(c) for c in cores],
                                 bool(val & 0x400), bool(val & 0x800))
        return list(im.getdata())

    # ------------------------------------------------------------ 1. orcamento
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
    mortas = set(dados["vagas_meta_mortas"])
    for local in metas:
        if local not in mortas:
            mau.append("o metatile %d nao esta na lista de vagas MORTAS: algum "
                       "mapa irmao usa esse id ou esta passada o escreve como "
                       "esta" % (512 + local))
    # AS VAGAS PINADAS. Esta passada REFERENCIA de propósito as vagas que
    # `src/tileset_anims.c` reescreve (é lá que a flor animada mora), e o que ela
    # não pode fazer é referenciar uma vaga pinada que não seja uma das oito de
    # flor: qualquer outra desenharia a flor de Mauville no lugar do que o atlas
    # mostra, e só em tempo de execução.
    flores = {T_ROSA[k] for k in T_ROSA} | {T_AMAR[k] for k in T_AMAR}
    for local, ents in metas.items():
        for val in ents:
            idx = val & 0x3FF
            if idx < NP:
                continue
            vaga = idx - NP
            if vaga in PINADAS and vaga not in flores:
                mau.append("o metatile %d usa a vaga de tile %d, que a animacao "
                           "reescreve e nao e tile de flor" % (512 + local, vaga))
    # E o `tiles.png` tem que sair do commit sem um byte de diferença. O md5 foi
    # gravado no kit no `--extrai` e é conferido contra o disco aqui: é o portão
    # que prova, sem depender de render, que nenhuma vaga de tile foi tocada.
    import hashlib
    md5_disco = hashlib.md5(_ler("tiles.png")).hexdigest()
    if md5_disco != dados["tiles_png_md5"]:
        mau.append("o tiles.png mudou (md5 %s no disco, %s no kit): esta passada "
                   "nao pode gravar tile" % (md5_disco, dados["tiles_png_md5"]))
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

    # ---- 2. a paleta derivada só pode ter trocado os índices da FLOR, e cada
    #        um deles tem que estar na lista de índices que os tiles e os DEZ
    #        quadros de animação usam. Índice de VERDE trocado descosturaria o
    #        canteiro do resto do campo, calado.
    verdes = {2, 3, 4, 12, 13}
    base_pal = ts["paletas"][PAL_BASE]
    for vaga, cores in sorted(dados["paletas"].items()):
        plano_da_vaga = PALETAS_NOVAS.get(int(vaga))
        if plano_da_vaga is None:
            mau.append("a vaga %s nao esta no plano de paletas desta passada"
                       % vaga)
            continue
        for i in range(16):
            if tuple(cores[i]) == tuple(base_pal[i]):
                continue
            if i in verdes:
                mau.append("a vaga %s trocou o indice %d, que e VERDE de fundo"
                           % (vaga, i))
            if i not in plano_da_vaga["cores"]:
                mau.append("a vaga %s trocou o indice %d, fora do plano"
                           % (vaga, i))

    # ------ 3. CHAO novo: atributo idêntico ao do carimbo em que ele pousa e,
    #           quando derivado, camada de cima VAZIA
    derivados = {c["nome"] for c in CHAO}
    for nome, gid in catalogo["chao"].items():
        quais = catalogo["sobre"][nome]
        for qual in quais:
            _b, attr_chao = chao_do_carimbo(qual)
            if atributo(gid) != attr_chao:
                mau.append("o chao %s (%d) tem atributo 0x%04X e o carimbo de %s "
                           "tem 0x%04X" % (nome, gid, atributo(gid), qual, attr_chao))
        cima = [e for e in entradas(gid)[4:] if e & 0x3FF]
        if cima and nome in derivados:
            mau.append("o chao derivado %s (%d) usa a camada de cima" % (nome, gid))
        # CAMADA DE CIMA EM CHAO ANDAVEL. Com layerType NORMAL ela vai para o
        # BG1, que desenha ACIMA do sprite. O tufo nosso desenha em cima de
        # propósito, que é o "jogador atrás do mato" do jogo base; o que ele não
        # pode é tapar o jogador INTEIRO (defeito E3 do `mapas_qa.py`).
        if cima and ((atributo(gid) >> 12) & 0xF) != 1:
            op = 0
            for e in cima:
                t = RM.resolver_tile(tp, ts, e & 0x3FF)
                op += _opacos(t) if t else 64
            if op >= 4 * 64:
                mau.append("o chao %s (%d) tapa o jogador inteiro (E3)"
                           % (nome, gid))

    # ------- 4. MOVEL e BLOCO: comportamento zerado, COVERED quando solidifica,
    #            e o NOSSO chão entrada por entrada na camada de baixo
    ids_bloco = {}
    for nome, ids in catalogo["blocos"].items():
        for gid in ids:
            ids_bloco[gid] = nome
    for chave, gid in list(catalogo["moveis"].items()) + \
            [(n, g) for g, n in ids_bloco.items()]:
        qual = catalogo["sobre"][chave][0]
        base, attr_chao = chao_do_carimbo(qual)
        a = atributo(gid)
        solido = catalogo["solido"].get(chave, True)
        if solido and ((a >> 12) & 0xF) != 1:
            mau.append("o movel %s (%d) nao esta em COVERED" % (chave, gid))
        if not solido and a != attr_chao:
            mau.append("o enfeite %s (%d) nao herdou o atributo do chao"
                       % (chave, gid))
        if a & 0xFF:
            mau.append("o movel %s (%d) importou comportamento 0x%02X da fonte"
                       % (chave, gid, a & 0xFF))
        if entradas(gid)[:4] != base:
            mau.append("o movel %s (%d) nao tem o nosso chao de %s na camada de "
                       "baixo" % (chave, gid, qual))
        if not solido:
            op = 0
            for e in entradas(gid)[4:]:
                if e & 0x3FF:
                    t = RM.resolver_tile(tp, ts, e & 0x3FF)
                    op += _opacos(t) if t else 64
            if op >= 4 * 64:
                mau.append("o enfeite %s (%d) tapa o jogador inteiro (E3)"
                           % (chave, gid))

    # ---------- 5. nenhuma variante de chão é cópia pixel a pixel de outra
    for qual in CARIMBOS:
        lista = [g for n, g in catalogo["chao"].items()
                 if qual in catalogo["sobre"][n]] + [CARIMBOS[qual]]
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                dd = sum(sum((x - y) ** 2 for x, y in zip(p, r)) ** 0.5
                         for p, r in zip(pix[a], pix[b])) / 256.0
                if dd < 8.0:
                    mau.append("as variantes de chao %d e %d de %s tem distancia "
                               "%.1f, abaixo do piso de 8,0 do varia_carimbo.py: "
                               "isso e enganar a regua" % (a, b, qual, dd))
    return mau + confere_mapas(alvos, metas, attrs, catalogo, planos, atributo)


def confere_mapas(alvos, metas, attrs, catalogo, planos, atributo):
    """Os portões que olham para o MAPA, e não para o tileset."""
    mau = []
    for alvo in alvos:
        L, W, H, v, escritas, contas = planos[alvo]
        d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
        ev = E.eventos(d)
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        meus_chaos = {g: n for n, g in catalogo["chao"].items()}
        meus_moveis = {g: n for n, g in catalogo["moveis"].items()}
        meus_blocos = {g: n for n, ids in catalogo["blocos"].items() for g in ids}

        for i, val in escritas.items():
            x, y = i % W, i // W
            novo, velho = val & 0x3FF, v[i] & 0x3FF
            cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
            if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
                mau.append("%s: mudou ELEVACAO em (%d,%d)" % (alvo, x, y))
            if cv and not cn:
                mau.append("%s: colisao 1 -> 0 em (%d,%d), que segue proibida"
                           % (alvo, x, y))
            nome = meus_chaos.get(novo) or meus_moveis.get(novo) or meus_blocos.get(novo)
            if nome is None:
                mau.append("%s: metatile %d escrito em (%d,%d) e de fora do kit"
                           % (alvo, novo, x, y))
                continue
            quais = {CARIMBOS[qq] for qq in catalogo["sobre"][nome]}
            if velho not in quais:
                mau.append("%s: a peca %s caiu em (%d,%d), que era o metatile %d "
                           "e nao um carimbo dela" % (alvo, nome, x, y, velho))
            solido = catalogo["solido"].get(nome)
            if novo in meus_chaos or solido is False:
                if cn != cv:
                    mau.append("%s: chao/enfeite mudou colisao em (%d,%d)"
                               % (alvo, x, y))
            else:
                if cv or not cn:
                    mau.append("%s: movel em (%d,%d) nao e solidificacao 0 -> 1"
                               % (alvo, x, y))
                if (x, y) in ev:
                    mau.append("%s: movel em cima do evento (%d,%d)" % (alvo, x, y))

        # (comportamento, layerType) de toda célula ANDÁVEL fica igual
        for i in range(W * H):
            if (saida[i] >> 10) & 3:
                continue
            a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
            if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
                mau.append("%s: celula andavel (%d,%d) mudou (comportamento, "
                           "layerType)" % (alvo, i % W, i // W))
                break

        # alcance a pé e LIGACAO a pé
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
        mau += ["%s: %s" % (alvo, qx) for qx in
                ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                                solid)]

        # NENHUMA célula que a suíte já anda pode ter virado sólida. O
        # `corredores_de_teste` já congela isso no gerador; aqui a conta é
        # refeita FORA dele, porque foi assim que sete casos de balsa caíram em
        # Canalave.
        corr = E.corredores_de_teste(alvo, v, W, H, d)
        if solid & corr:
            mau.append("%s: %d celulas de corredor da suite viraram solidas: %s"
                       % (alvo, len(solid & corr), sorted(solid & corr)[:6]))

        # A MANCHA NÃO PODE SER ADIVINHÁVEL, e o teste tem dois lados.
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
                    r = pilha.pop()
                    for dx, dy in N4:
                        z = (r[0] + dx, r[1] + dy)
                        if z in mancha and z not in vistos:
                            vistos.add(z)
                            pilha.append(z)
            if len(mancha) / pedacos < 12.0:
                mau.append("%s: a mancha media tem so %.1f celulas (%d em %d "
                           "pedacos): virou sal e pimenta, nao bolha"
                           % (alvo, len(mancha) / pedacos, len(mancha), pedacos))

        # a régua tem que fechar ABAIXO de 20%
        b, nb, idb = regua(v, W, H, L, escritas)
        if b >= TETO_REGUA:
            mau.append("%s: a regua ainda marca %.1f%% de carimbo dominante"
                       % (alvo, b))

        # o BLOCO: toda fileira sai inteira, nunca pela metade
        for nome, ids in catalogo["blocos"].items():
            larg = len(ids)
            cantos = [(i % W, i // W) for i, val in escritas.items()
                      if (val & 0x3FF) == ids[0]]
            for x, y in cantos:
                for k in range(larg):
                    j = y * W + x + k
                    if (escritas.get(j, 0) & 0x3FF) != ids[k]:
                        mau.append("%s: a fileira do bloco %s em (%d,%d) esta "
                                   "incompleta" % (alvo, nome, x, y))
                        break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo(alvos):
    """Prova positiva e as provas NEGATIVAS, cada sabotagem revertida em seguida.

    "Zero diferença" só vale depois que a comparação mostra que sabe reprovar.
    """
    guardado = carrega_plano()
    metas, attrs, catalogo = desenha_kit(guardado)
    planos = {}
    for alvo in ORDEM:
        planos[alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))

    ts_do_disco = _tileset(SECUNDARIO)
    mau = confere(ORDEM, metas, attrs, catalogo, planos)
    negativas = []

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = confere(ORDEM, *args)
        pega = [qx for qx in queixas if espera in qx]
        if not pega:
            mau.append("SABOTAGEM NAO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    def copia():
        return (dict(metas), dict(attrs),
                json.loads(json.dumps(catalogo)),
                {k: (v[0], v[1], v[2], list(v[3]), dict(v[4]), v[5])
                 for k, v in planos.items()})

    alvo0 = "FloaromaTown"

    # N1. colisão 1 -> 0 numa célula de MANCHA, e mancha não é detalhe: numa
    #     célula de móvel a mesma sabotagem sai acusada por outra regra ("móvel
    #     em (x,y) não é solidificação 0 -> 1"), e o caso passaria a provar a
    #     regra errada.
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[3][alvo0]
        i = next(j for j in sorted(esc) if not ((esc[j] >> 10) & 3))
        v[i] = v[i] | (1 << 10)
        return a
    sabota("colisao 1 -> 0", n1, "colisao 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[3][alvo0]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevacao alterada", n2, "mudou ELEVACAO")

    # N3. comportamento de um metatile de CHAO derivado sabotado
    def n3():
        a = copia()
        gid = a[2]["chao"][CHAO[0]["nome"]]
        a[1][gid - 512] = (a[1][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chao sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = a[2]["moveis"]["canteiro com moldura|grama"]
        a[1][gid - 512] = a[1][gid - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no movel", n4, "nao esta em COVERED")

    # N5. camada de BAIXO de um móvel sabotada (chão de outro carimbo)
    def n5():
        a = copia()
        gid = a[2]["moveis"]["canteiro com moldura|rosa"]
        base_g, _x = chao_do_carimbo("grama")
        a[0][gid - 512] = list(base_g) + list(a[0][gid - 512])[4:]
        return a
    sabota("movel de rosa com chao de grama", n5, "nao tem o nosso chao de rosa")

    # N6. bloco gravado pela metade
    def n6():
        a = copia()
        L, W, H, v, esc, ct = a[3][alvo0]
        ids = catalogo["blocos"]["cerca viva"]
        for i in sorted(esc):
            if (esc[i] & 0x3FF) == ids[1]:
                del esc[i]
                break
        return a
    sabota("bloco pela metade", n6, "esta incompleta")

    # N7. mancha escolhida por (x + y) % n, que é xadrez com período
    def n7():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            for alvo in ORDEM:
                a[3][alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por (x+y) % n", n7, "virou padrao")

    # N8. mancha escolhida por x % n
    def n8():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[x % len(nomes)]
        try:
            for alvo in ORDEM:
                a[3][alvo] = plano_mapa(alvo, catalogo, base_de(alvo, guardado))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por x % n", n8, "virou padrao")

    # N9. corredor fechado que PARTE um pedaço de chão. O portão de alcance
    #     sozinho não pega isso quando há warp dos dois lados.
    def n9():
        a = copia()
        L, W, H, v, esc, ct = a[3][alvo0]
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
        raise SystemExit("nao achei ponto de articulacao para a sabotagem N9")
    sabota("corredor fechado", n9, "se partiu")

    # N10. duas variantes de chão IGUAIS pixel a pixel: é enganar a régua
    def n10():
        a = copia()
        g1 = a[2]["chao"][CHAO[7]["nome"]]
        g2 = a[2]["chao"][CHAO[8]["nome"]]
        a[0][g2 - 512] = list(a[0][g1 - 512])
        return a
    sabota("variante de chao duplicada", n10, "abaixo do piso de 8,0")

    # N11. cor nova escrita num índice que os NOSSOS pixels já usam. As duas
    #      vagas que esta passada grava estão 100% livres, então a sabotagem
    #      PRECISA declarar uma vaga que não é do plano: ela pega a primeira
    #      vaga de 6 a 12 que tenha índice em uso (a 7, medida nesta árvore) e
    #      manda o kit gravar cor nela.
    def n11():
        a = copia()
        dados = kit()
        alvo_vaga, idx = None, None
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
        sabota("cor nova em indice ja usado", n11, "que algum pixel nosso usa")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # N12. a paleta derivada trocando um índice de VERDE. Este é o defeito
    #      SILENCIOSO desta passada: o canteiro continuaria animado e bonito, e
    #      só o verde de fundo dele ficaria diferente do resto do campo.
    def n12():
        a = copia()
        dados = kit()
        vaga = sorted(dados["paletas"])[0]
        pal = [list(c) for c in dados["paletas"][vaga]]
        pal[13] = [255, 0, 255]
        dados["paletas"][vaga] = pal
        with open(KIT_JSON + ".sab", "w") as f:
            json.dump(dados, f)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        return a
    try:
        sabota("verde de fundo trocado", n12, "que e VERDE de fundo")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # N13. gravar numa vaga de metatile VIVA, ou seja em cima de um metatile que
    #      algum dos quatro mapas irmãos desenha. É a sabotagem própria desta
    #      passada, que escreve em `metatiles.bin` CHEIO.
    def n13():
        a = copia()
        dados = kit()
        mortas = set(dados["vagas_meta_mortas"])
        viva = next(x for x in range(TETO_META) if x not in mortas)
        a[0][viva] = list(a[0][min(a[0])])
        a[1][viva] = 0x1000
        return a
    sabota("grava em metatile vivo", n13, "nao esta na lista de vagas MORTAS")

    # N14. móvel plantado numa célula que a suíte anda. É o defeito que derrubou
    #      sete casos de balsa em Canalave.
    def n14():
        a = copia()
        L, W, H, v, esc, ct = a[3][alvo0]
        d = json.load(open(f"{RAIZ}/data/maps/{alvo0}/map.json"))
        corr = E.corredores_de_teste(alvo0, v, W, H, d)
        gid = catalogo["moveis"]["pedra do jardim|grama"]
        for x, y in sorted(corr):
            i = y * W + x
            if i in esc or (v[i] >> 10) & 3:
                continue
            if (v[i] & 0x3FF) != CARIMBOS["grama"]:
                continue
            esc[i] = (v[i] & 0xF000) | (1 << 10) | gid
            return a
        raise SystemExit("nao achei celula de corredor para a sabotagem N14")
    sabota("movel no corredor da suite", n14, "celulas de corredor da suite")

    # N15. metatile novo apontando para uma vaga PINADA que não é de flor. Sem
    #      este caso, a armadilha central desta passada não teria par negativo.
    def n15():
        a = copia()
        gid = a[2]["chao"][CHAO[0]["nome"]]
        ents = list(a[0][gid - 512])
        ents[0] = (8 << 12) | (len(_tileset(PRIMARIO)["tiles"]) + 110)
        a[0][gid - 512] = ents
        return a
    sabota("vaga pinada que nao e flor", n15, "que a animacao reescreve")

    # ------------------------------------------------ o que está NO DISCO
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
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
    print("  0 tiles, %d metatiles, %d provas negativas:"
          % (len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-34s -> %s" % (nome, queixa[:100]))
    return 0


def folha(saida):
    """Desenha o catálogo inteiro num PNG, para decidir OLHANDO e não por nome."""
    import render_maps as RM
    from PIL import Image, ImageDraw
    dados = kit()
    guardado = carrega_plano()
    metas, attrs, catalogo = desenha_kit(guardado)
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    itens = [("carimbo %d" % CARIMBOS[k], CARIMBOS[k]) for k in
             ("grama", "rosa", "amarela")]
    itens += sorted(catalogo["chao"].items(), key=lambda kv: kv[0])
    itens += sorted(catalogo["moveis"].items(), key=lambda kv: kv[0])
    itens += [(n, g) for n, ids in sorted(catalogo["blocos"].items()) for g in ids]
    cols, CELL, esc = 8, 16, 6
    linhas = (len(itens) + cols - 1) // cols
    im = Image.new("RGB", (cols * (CELL + 2), linhas * (CELL + 2 + 9)), (20, 20, 20))
    px = im.load()
    for k, (nome, gid) in enumerate(itens):
        ox, oy = (k % cols) * (CELL + 2) + 1, (k // cols) * (CELL + 2 + 9) + 1
        if gid >= 512 and (gid - 512) in metas:
            ents = metas[gid - 512]
        else:
            tset, loc = (tp, gid) if gid < 512 else (ts, gid - 512)
            ents = list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))
        for cam in range(2):
            for qd in range(4):
                val = ents[cam * 4 + qd]
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if not idx:
                    continue
                tile = RM.resolver_tile(tp, ts, idx)
                if tile is None:
                    continue
                cores = (dados["paletas"].get(str(ip))
                         or (tp if ip < 6 else ts)["paletas"].get(ip))
                RM.desenhar_tile(px, ox + (qd % 2) * 8, oy + (qd // 2) * 8, tile,
                                 [tuple(c) for c in cores],
                                 bool(val & 0x400), bool(val & 0x800))
    im = im.resize((im.size[0] * esc, im.size[1] * esc), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for k, (nome, gid) in enumerate(itens):
        d.text(((k % cols) * (CELL + 2) * esc + 2,
                ((k // cols) * (CELL + 2 + 9) + CELL + 2) * esc - 4),
               ("%s %d" % (nome, gid))[:26], fill=(255, 255, 0))
    im.save(saida)
    print("%s  %dx%d  %d pecas" % (saida, im.size[0], im.size[1], len(itens)))
    return 0


def mostra_orcamento():
    livres, mortas_meta, mortas_tile, vivos, arm4 = orcamento()
    print("%s: %d metatiles no arquivo, %d vivos nos 4 layouts irmaos"
          % (SECUNDARIO, len(_ler("metatiles.bin")) // 16,
             len([x for x in vivos if x >= 512])))
    print("armadilha 4 do compacta_paletas (metatile PRIMARIO vivo pintando com "
          "vaga >= 6): %d entradas" % arm4)
    print("vagas de METATILE mortas: %d de %d" % (len(mortas_meta), TETO_META))
    print("vagas de TILE mortas: %d de %d (%d delas PINADAS pela animacao e "
          "proibidas)" % (len(mortas_tile), TETO_TILES,
                          len([t for t in mortas_tile if t in PINADAS])))
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
    if "--folha" in sys.argv:
        return folha(sys.argv[sys.argv.index("--folha") + 1])
    if "--desfazer" in sys.argv:
        return desfaz(alvos_do_argv())
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo(alvos_do_argv())
    if "--so-tileset" in sys.argv:
        m, at, c = desenha_kit()
        grava_tileset(m, at)
        print("tileset escrito: %d metatiles, 0 tiles" % len(m))
        return 0
    return roda(alvos_do_argv(), "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
