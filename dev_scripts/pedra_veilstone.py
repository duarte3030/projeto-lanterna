#!/usr/bin/env python3
"""Refino de `VeilstoneCity` (tema PEDRA TALHADA), no `gTileset_Veilstone`, com
arte importada do `Pokemon Light Platinum`.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: `VeilstoneCity` gasta 29,3% do chão andável a pé
(542 células de 1.851) com UM metatile, o 545, o tecido diagonal do calçamento;
e mais 23,1% (428 células) com o 524, o liso salpicado. Somados, DOIS metatiles
cobrem 52,4% do chão de um mapa de 66x68, o maior da leva. A cidade da pedra e
da loja de departamento é, hoje, um tapete cinza de mil células iguais entre
paredões de rocha.

AVISO QUE ESTA PASSADA TEM QUE DAR EM VOZ ALTA, e ele não é detalhe de rodapé.
O `gTileset_Veilstone` é usado por UM mapa só, o próprio `VeilstoneCity`
(medido: `grep secondary_tileset` em `data/layouts/layouts.json` devolve um
único layout com esse rótulo). Por isso NÃO EXISTE, nesta frente, a prova de
"zero pixel de diferença em mapa irmão" que as frentes de Pastoria, Sunyshore e
Oreburgh puderam dar: não há mapa irmão. Fabricar essa prova aqui seria
verdadeira por construção e não mediria nada. O que substitui a prova de irmão,
e esta sim é medida, é o portão de PLANTA (`dev_scripts/portao_planta.py`)
contra o commit de referência, mais o carimbo de comportamento
(`dev_scripts/qa/lente_carimbo.py`), que compara TODOS os mapas do cartucho e
tem que acusar mudança em VeilstoneCity e em NENHUM outro.

O ORÇAMENTO, medido nesta árvore e não herdado de brief:

  tiles      384 no `tiles.png` (128x192), 177 referenciados por algum metatile
             do secundário e o maior índice local vivo é o 373. As vagas de 384
             em diante estão livres até o teto de 512 do secundário
             (`NUM_TILES_IN_PRIMARY` 512 em `include/fieldmap.h`), ou seja 128
             vagas SEM compactar nada e sem mexer no índice de tile de nenhum
             metatile vivo. Este kit gasta 36.
  metatiles  o maior local que aparece no `map.bin` de `VeilstoneCity` é o 247
             (id 759). Os locais 248 a 511 (ids 760 a 1023) são TODOS enchimento
             do dumper e nenhum aparece no mapa: 264 vagas livres, contiguas e
             no fim. Este kit gasta 34, dos locais 248 ao 281.
  paletas    o secundário é dono das vagas 6 a 12 (`NUM_PALS_IN_PRIMARY` 6 e
             `NUM_PALS_TOTAL` 13, em `include/fieldmap.h`). A VAGA 6 DESTE
             TILESET ESTA VAZIA: as 16 cores do `palettes/06.pal` são (0,0,0) e
             NENHUM pixel de NENHUM metatile do tileset pede a vaga 6 (medido,
             zero tiles). Ou seja: há uma vaga de paleta INTEIRA de graça, e o
             `compacta_paletas.py`, que abre vaga quebrando tileset, não precisa
             ser chamado nesta frente. A vaga 8 tem só o índice 5 em uso (por um
             único metatile, o 675) e sobram 14 índices vagos nela; é lá que
             mora o poste. Nenhuma cor de índice JÁ USADO é reescrita, e o
             auto-teste tem sabotagem para isso.

A ARTE, e de onde vem cada coisa:

  CHÃO (a mancha): NENHUM pixel importado, e a razão é COR MEDIDA, não economia.
  O calçamento de pedra do `Light Platinum` que casaria de desenho (o secundário
  `0x286EEC`, a cidade de calçada do grupo 0, mapa g00m14) tem os três tons
  (168,176,176), (136,152,152) e (88,96,104), e o calçamento DESTA cidade tem
  (216,224,224), (192,200,208) e (168,184,200). A distância RGB entre as cores
  médias dos dois metatiles de piso é 85,6, muito acima do piso de ~50 que a
  lição da areia de Pastoria e da terra de Sandgem deixou: uma mancha dessas no
  meio da praça não lê como variação de calçada, lê como remendo escuro. Sem
  BORDA DE TRANSIÇÃO desenhada (que a fonte não tem para o nosso cinza), o
  retalho é garantido.
  No lugar dela, as 21 variantes de chão são ARRANJO E ESPELHO dos tiles que
  ESTE par de tilesets JÁ TEM desenhados: o tecido diagonal do próprio carimbo
  (694, 695, 710 e 711), a laje com junta (758, 759, 760, 761, 774 e 790) e o
  liso salpicado do segundo carimbo (262 e 278). É o caminho da passarela de
  Sunyshore, e ele custa ZERO tile, ZERO cor e ZERO risco de costura, porque o
  pixel é literalmente o mesmo que já está na tela ao lado.

  MÓVEL (a mobília de pedra), do `Pokemon Light Platinum` (autor WesleyFG, base
  Ruby AXVE, md5 7fd2c08735459d99fa23fdaa9b755486), de DOIS pares de tileset do
  mesmo hack:
   - `0x286E44` (primário) + `0x2870FC` (secundário), o desfiladeiro de pedra do
     grupo 8 (mapa de amostra g08m01, 48x43). Dali vem o MATACÃO 2x2 (e o
     espelho dele) e o PEDREGULHO. A escolha não foi de
     memória: a rocha desse tileset é CINZA-AZULADA, (176,184,200),
     (152,160,176), (128,128,144), (104,112,120), (96,96,96) e (80,80,88),
     exatamente a familia fria do calçamento desta cidade. A distância do tom
     claro da rocha (176,184,200) para o tom médio da nossa calçada (192,200,208)
     é 24,0, e do tom seguinte (152,160,176) para o nosso (168,184,200) é 37,8.
     A pedreira que Oreburgh usou nesta mesma onda (o `0x286E8C`) foi DESCARTADA
     aqui por essa conta: a rocha dela é quente, (184,136,128)/(152,104,96)/
     (128,80,72), e o marrom dela contra o cinza-azulado desta praça dá 102 de
     distância.
   - `0x286CF4` (primário) + `0x286EEC` (secundário), a cidade de calçada do
     grupo 0 (mapa de amostra g00m14, 40x30). Dali vem SÓ o POSTE DE RUA de duas
     células, seis cores, (48,56,88) a (184,208,224). O calçamento desse mesmo
     tileset ficou de fora pela conta de cor do paragrafo do CHÃO.

  MÓVEL NOSSO, que custa zero: a PEDRA do próprio `gTileset_GeneralSinnoh` (a
  arte da camada de cima do metatile 404, tiles 141, 142, 157 e 158 na vaga 1) e
  a MOITA FLORIDA (metatile 4, tiles 508 a 511 na vaga 2). Nenhuma das duas
  aparecia em `VeilstoneCity`. Elas entram REMONTADAS: a camada de cima é a
  delas, a de baixo é o NOSSO calçamento entrada por entrada, porque no primário
  as duas estão desenhadas sobre água e sobre grama.

COMO CADA PEÇA É MONTADA, e a armadilha que cada regra resolve:

  - CHÃO NOVO é metatile com arte SÓ na camada de BAIXO e atributo IGUAL, bit a
    bit, ao dos dois carimbos (0x0000 nos dois, medido). Camada de cima em chão
    andável com layerType NORMAL vai para o BG1 e desenha ACIMA do jogador, que
    é o defeito E3 do `mapas_qa.py`.
  - MÓVEL é célula que vira SÓLIDA: a arte vai na camada de CIMA, a de baixo
    recebe o NOSSO calçamento entrada por entrada, e o atributo é comportamento
    ZERADO com layerType COVERED (0x1000), que põe as duas camadas ABAIXO do
    sprite. Comportamento é id semântico: nenhum é importado.
  - QUADRANTE DE BAIXO SOBE quando o de cima está vazio (regra do
    `porto_canalave.py`): a coluna e a bacia do hack têm a arte na camada de
    BAIXO e a de cima vazia.
  - O CHÃO DA FONTE NÃO ENTRA, e ele é achado por EVIDÊNCIA: tile que aparece na
    camada de baixo de muitos metatiles DIFERENTES da fonte é piso dela, porque
    piso é o que se repete debaixo de tudo. `piso_min` é 20 e o número é o meio
    de um degrau medido: no `0x2870FC` o tile de piso mais usado aparece em 48
    metatiles, o segundo em 31, e o próximo tile que NÃO é piso aparece em 21.
    Quadrante uniforme nos quatro cantos também cai fora pela mesma razão.
  - ESPELHO não custa tile nem cor: o pedregulho e a coluna entram também
    espelhados (bit 0x400 ligado e as colunas trocadas), que é o que o próprio
    primário faz nos pares dele e o que o `neve_snowpoint2.py` mediu.
  - MÓVEL SÓ NO CARIMBO 545. A mancha pinta os dois carimbos (545 e 524, que têm
    o MESMO atributo 0x0000), mas a mobília só pousa no 545, e a razão é o chão
    que fica DEBAIXO dela: a camada de baixo de todo móvel é a do 545, então
    plantar um matacão numa célula de 524 deixaria uma costura de calçada em
    volta da pedra. Sobra espaço de sobra: são 542 células de 545.

O QUE FICOU DE FORA, com o motivo medido:
  - o CALÇAMENTO do `0x286EEC`, por cor: 85,6 de distância RGB (ver acima).
  - a PEDRA MIÚDA do `0x2870FC` (metatile local 70), por cor: ela é a rocha
    QUENTE do mesmo tileset, (200,152,104), (184,136,104), (160,120,88), e a
    distância dela para o nosso calçamento (192,200,208) é 114,8. Sete cores
    para plantar uma pedra marrom numa praça cinza.
  - o SEIXO (metatile local 93), porque na fonte ele tem colisão 0, ou seja é
    respingo de chão e não móvel; importá-lo como sólido poria uma pedrinha de
    oito pixels barrando o passo, que lê como bug e não como enfeite.
  - a ESCADARIA e o DEGRAU de pedra (locais 137 e 138), porque degrau é promessa
    de mudança de nível e esta passada tem elevação INTACTA em 100% das palavras
    como regra dura. Degrau desenhado sem elevação atrás dele é armadilha visual.
  - a LAJE LISA (locais 104 e 112), porque como peça solta ela é um quadrado
    cinza sem silhueta: no meio da praça não lê como móvel, lê como buraco.
  - a COLUNA (local 110) e a BACIA (local 113) do mesmo `0x2870FC`, e este corte
    foi feito DEPOIS de plantar as duas e OLHAR o render, não antes. As duas
    pintam com a paleta 5 do primário do hack, que é cinza QUENTE:
    (200,192,176), (176,176,160), (168,152,136), (152,136,136), (128,120,120) e
    (88,88,88). Contra o cinza FRIO desta cidade a conta é dura, (168,152,136)
    para o nosso (168,184,200) dá 71,6, e no render de 09/09/2026 a coluna saiu
    como uma barra bege listrada que lê como poste de MADEIRA no meio de uma
    praça de pedra, e a bacia como um banco marrom. Cortadas as duas, sobram
    nove índices livres na nossa vaga 6 para quem vier depois.
  - o BUEIRO do `0x286EEC` (local 261) e a GRADE, porque são arte de CHÃO com a
    cor do calçamento da fonte, e caem na mesma conta de 85,6 do calçamento.

Uso:
    python3 dev_scripts/pedra_veilstone.py                 # mede e mostra o plano
    python3 dev_scripts/pedra_veilstone.py --aplicar
    python3 dev_scripts/pedra_veilstone.py --desfazer      # devolve o map.bin
    python3 dev_scripts/pedra_veilstone.py --demo          # auto-teste
    python3 dev_scripts/pedra_veilstone.py --extrai        # regera o kit da ROM
    python3 dev_scripts/pedra_veilstone.py --só-tileset    # só o tileset
"""
import collections
import glob
import heapq
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

# O bloco de teste DESTA rodada é o único que o varredor de corredores pula: os
# casos dele foram escritos DEPOIS do desenho e a partir dele, então tratá-los
# como corredor a preservar seria circular. Todos os outros blocos valem, e
# valem inteiros: o 171, o 125 e o 102 andam dentro de VeilstoneCity.
E.BLOCO_PROPRIO = "197_pedra_veilstone.json"

ALVO = "VeilstoneCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/veilstone"
KIT_JSON = f"{RAIZ}/dev_scripts/pedra_veilstone_kit.json"
PLANO = f"{RAIZ}/dev_scripts/pedra_veilstone.json"

PRIMARIO = "gTileset_GeneralSinnoh"
SECUNDARIO = "gTileset_Veilstone"
# O `gTileset_Veilstone` é de UM mapa só. A lista existe para o portão de vaga
# de metatile e para deixar o fato escrito onde o código o usa.
IRMAOS = [ALVO]

TETO_TILES = 512            # NUM_TILES_IN_PRIMARY, include/fieldmap.h
TETO_META = 512             # NUM_METATILES_IN_PRIMARY, include/fieldmap.h
TILE_LOCAL_0 = 384          # primeira vaga livre do tiles.png (384 tiles hoje)
META_LOCAL_0 = 248          # local 248 = id 760, o primeiro dos 264 livres
MARGEM = 2
TETO_REGUA = 20.0           # o alvo desta onda: carimbo dominante <= 20%
MULTI_NIVEL = 15            # ELEVATION_MULTI_LEVEL: casa com QUALQUER elevacao

CARIMBO = 545               # o tecido diagonal, 542 celulas (29,3%)
CARIMBO2 = 524              # o liso salpicado, 428 celulas (23,1%)

# ------------------------------------------------------------------- as FONTES
LP = dict(slug="light-platinum", hack="Pokemon Light Platinum", autor="WesleyFG",
          md5="7fd2c08735459d99fa23fdaa9b755486", base="Ruby (AXVE)",
          split=(512, 512, 6))
# par 1: o desfiladeiro de pedra do grupo 8 (g08m01, 48x43)
PAR_ROCHA = dict(tag="2870FC", pri=0x286E44, sec=0x2870FC, piso_min=20)
# par 2: a cidade de calçada do grupo 0 (g00m14, 40x30)
PAR_RUA = dict(tag="286EEC", pri=0x286CF4, sec=0x286EEC, piso_min=20)
PARES = {PAR_ROCHA["tag"]: PAR_ROCHA, PAR_RUA["tag"]: PAR_RUA}

# Para onde vai cada paleta da fonte. A rocha do desfiladeiro mora na paleta 7
# do secundário do hack e são SEIS cores; elas vão para a nossa vaga 6, que
# estava inteira vazia, e sobram nove índices nela. O poste vai para os índices
# vagos da vaga 8, que tinha catorze.
# A paleta 5 do primário daquele par, a da coluna e da bacia, foi CORTADA depois
# do render (ver "o que ficou de fora" no cabeçalho): ela é cinza QUENTE.
VAGAS_PAL = {"2870FC": {7: 6}, "286EEC": {0: 8}}

# ------------------------------------------------------------- as PEÇAS da ROM
MOVEIS_LP = [
    dict(nome="pedregulho", par="2870FC", lp=84, quantos=14, espaco=6),
]
# Espelho horizontal do que já foi importado: custa UMA vaga de metatile e
# ZERO tile e ZERO cor, e muda a silhueta na tela.
ESPELHOS_LP = [
    dict(nome="pedregulho espelhado", de="pedregulho",      quantos=13, espaco=6),
]
# Blocos de DUAS células de altura: a de cima continua ANDÁVEL (a arte mora na
# camada de cima e o jogador passa ATRÁS) e a de baixo vira SÓLIDA em COVERED.
# Os pares não são escolha de atlas: foram lidos do MAPA do hack. No g08m01 o
# par vertical (77,85) aparece 21 vezes e o (78,86) outras 21, e o par
# horizontal (85,86) aparece 27; no g00m14 o poste aparece como (262 em cima,
# 270 embaixo).
BLOCOS_LP = [
    dict(nome="matacao", par="2870FC", topo=[77, 78], base=[85, 86],
         quantos=6, espaco=11),
    dict(nome="poste de rua", par="286EEC", topo=[262], base=[270],
         quantos=11, espaco=9),
]
# Bloco ESPELHADO: custa uma vaga de metatile por metade e ZERO tile e ZERO cor.
# O espelho de um bloco de duas colunas não é só espelhar cada metade: as duas
# metades TROCAM DE LADO também, senão o matacão sai com as duas faces
# iluminadas para dentro.
ESPELHOS_BLOCOS = [
    dict(nome="matacao espelhado", de="matacao", quantos=6, espaco=10),
]
# ---------------------------------------------------------- as PEÇAS que já são nossas
# Metatiles do PRIMÁRIO cuja arte da camada de CIMA é reaproveitada, remontada
# sobre o NOSSO calçamento. Nenhum deles aparece em `VeilstoneCity` hoje.
MOVEIS_NOSSOS = [
    dict(nome="pedra do demake", mt=404, quantos=14, espaco=6),
    dict(nome="moita florida",   mt=4,   quantos=12, espaco=7),
]
ESPELHOS_NOSSOS = [
    dict(nome="pedra do demake espelhada", de="pedra do demake", quantos=13,
         espaco=6),
]

# ------------------------------------------------------------ as VARIANTES de CHÃO
# Cada variante é um metatile novo com arte SÓ na camada de baixo, montado com
# tiles que os nossos dois tilesets JÁ têm. `base` diz sobre qual carimbo ela
# pode ser pintada: "545" é o tecido diagonal, "524" o liso salpicado e "ambos"
# as que são 100% laje e casam com os dois.
# A ENTRADA é (tile, espelho), com espelho em 0..3: bit 1 = horizontal (0x400),
# bit 2 = vertical (0x800). A vaga de paleta é sempre a 12, a do calçamento.
PAL_CHAO = 12
VARIANTES = [
    ("laje inteira",     "ambos", [(758, 0), (758, 1), (758, 2), (758, 3)]),
    ("laje girada",      "ambos", [(758, 3), (758, 2), (758, 1), (758, 0)]),
    ("laje dupla",       "ambos", [(759, 0), (759, 1), (759, 2), (759, 3)]),
    ("laje larga",       "ambos", [(774, 0), (774, 1), (774, 2), (774, 3)]),
    ("laje estreita",    "ambos", [(790, 0), (790, 1), (790, 2), (790, 3)]),
    ("laje canto",       "ambos", [(761, 0), (761, 1), (761, 2), (761, 3)]),
    ("laje miolo",       "ambos", [(760, 0), (760, 1), (760, 2), (760, 3)]),
    ("junta cruzada",    "ambos", [(758, 0), (759, 1), (759, 2), (758, 3)]),
    ("junta dupla",      "ambos", [(760, 0), (761, 1), (761, 2), (760, 3)]),
    ("meia laje norte",  "545",   [(758, 0), (758, 1), (695, 0), (694, 0)]),
    ("meia laje sul",    "545",   [(711, 0), (710, 0), (758, 2), (758, 3)]),
    ("meia laje oeste",  "545",   [(758, 0), (710, 0), (758, 2), (694, 0)]),
    ("meia laje leste",  "545",   [(711, 0), (758, 1), (695, 0), (758, 3)]),
    ("laje e tecido",    "545",   [(774, 0), (710, 0), (695, 0), (774, 3)]),
    ("tecido e laje",    "545",   [(711, 0), (790, 1), (790, 2), (694, 0)]),
    ("tecido e liso",    "545",   [(711, 0), (710, 0), (278, 0), (262, 0)]),
    ("liso com laje",    "524",   [(262, 0), (278, 0), (758, 2), (758, 3)]),
    ("liso com junta",   "524",   [(758, 0), (758, 1), (278, 0), (262, 0)]),
    ("liso e tecido",    "524",   [(262, 0), (278, 0), (695, 0), (694, 0)]),
    ("liso com canto",   "524",   [(262, 0), (761, 1), (278, 0), (262, 0)]),
    ("liso rachado",     "524",   [(790, 0), (278, 0), (278, 0), (790, 3)]),
]

# ------------------------------------------------------------ o ESPALHAMENTO
# A TRILHA é o esqueleto de custo mínimo entre as soleiras das portas, engordado
# e desgastado na borda; as BOLHAS são manchas orgânicas crescidas por frente de
# onda. As duas ideias vêm do `neve_snowpoint2.py`.
ESPALHA = dict(
    trilha=["laje inteira", "laje girada", "laje dupla"],
    # A ORDEM DESTA LISTA IMPORTA e não é enfeite: a bolha é gulosa e a primeira
    # que passa toma a célula. Na primeira montagem os quatro últimos grupos
    # ficaram com ZERO células (metatile novo que ninguém usa é vaga gasta à
    # toa), e a correção foi intercalar os grupos do carimbo 545 com os do 524 e
    # pôr na frente quem ficou sem nada.
    bolhas=[
        dict(grupo=["meia laje norte", "meia laje sul"],      quantas=5, tam=(6, 13)),
        dict(grupo=["laje e tecido", "tecido e laje"],        quantas=5, tam=(6, 13)),
        dict(grupo=["liso com canto", "liso rachado"],        quantas=5, tam=(7, 15)),
        dict(grupo=["meia laje oeste", "meia laje leste"],    quantas=5, tam=(6, 13)),
        dict(grupo=["laje larga", "laje estreita"],           quantas=5, tam=(7, 15)),
        dict(grupo=["liso com laje", "liso com junta"],       quantas=5, tam=(7, 15)),
        dict(grupo=["laje canto", "laje miolo"],              quantas=5, tam=(7, 15)),
        dict(grupo=["junta cruzada", "junta dupla"],          quantas=5, tam=(6, 13)),
        dict(grupo=["tecido e liso"],                         quantas=4, tam=(4, 9)),
        dict(grupo=["liso e tecido"],                         quantas=4, tam=(4, 9)),
    ],
    borda_trilha=72)
ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre dois moveis QUAISQUER

N4 = E.N4
PISO_DISTANCIA = 8.0        # o piso do `varia_carimbo.py` para variante visivel


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


def vagas_livres():
    """{vaga: [índices de cor que NENHUM pixel nosso usa]}.

    Conta o tile que cada entrada de metatile do secundário pede, seja ele do
    secundário ou do primário, porque o índice do pixel é do TILE e a cor vem da
    vaga da ENTRADA. Escrever cor nova num índice que não aparece aqui não muda
    o desenho de nada, e o auto-teste tem sabotagem que prova que a conferência
    sabe reprovar quando um índice USADO é reescrito.

    Os metatiles que ESTA passada grava (local >= META_LOCAL_0) ficam de fora de
    propósito, para que rodar `--extrai` depois de `--aplicar` de o mesmo kit.
    """
    import render_maps as RM
    ts, tp = _tileset(SECUNDARIO), _tileset(PRIMARIO)
    usados = collections.defaultdict(set)
    for loc in range(min(len(ts["metatiles"]) // 16, META_LOCAL_0)):
        for (it, fh, fv, ip) in RM.entradas_metatile(ts["metatiles"], loc):
            if it == 0 or ip < 6:
                continue
            tile = RM.resolver_tile(tp, ts, it)
            if tile is None:
                continue
            for linha in tile:
                for c in linha:
                    if c:
                        usados[ip].add(c)
    return {v: [i for i in range(1, 16) if i not in usados[v]] for v in range(6, 13)}


# ---------------------------------------------------------------- a EXTRAÇÃO
def _nibbles(dados, local):
    """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
    b = dados[local * 32:local * 32 + 32]
    return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
             for x in range(8)] for y in range(8)]


def _rgb(ts, i):
    """BGR555 do GBA para o RGB888 que o repo usa: cinco bits deslocados TRÊS
    casas, não esticados para 0..255.

    A conta importa e já foi medida em 08/09/2026 pela frente da mina: as duas
    contas dão o MESMO cinco-bits depois que o `gbagfx` reconverte o `.pal` para
    `.gbapal`, então a cor dentro da ROM é a mesma; o que muda é o número
    escrito no `.pal` e, com ele, o pixel de todo render de conferência. Todo
    `.pal` deste repositório está na conta de deslocar."""
    c = struct.unpack_from("<16H", ts["pal"], i * 32)
    return [[((v >> s) & 0x1F) << 3 for s in (0, 5, 10)] for v in c]


def extrai():
    """Regera `pedra_veilstone_kit.json` a partir da ROM privada do Light Platinum.

    Só roda na máquina que tem `fontes-mapas/romhacks/`. O que sai daqui é o
    asset CONVERTIDO (tiles em nibbles, já reindexados para a vaga de destino, e
    paleta em RGB), nunca a ROM, nem em parte nem em dump.
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
        raise SystemExit("a ROM em %s tem md5 %s e o kit foi feito com %s"
                         % (gba, md5, LP["md5"]))
    r = Rom(caminho)
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = LP["split"]
    livres = vagas_livres()

    tiles_px, tiles_vaga, tiles_cor = {}, {}, {}
    pecas, chaos = [], {}

    # todas as peças, achatadas, com o par a que pertencem
    lista = [(m["par"], "movel", m["nome"], m["lp"]) for m in MOVEIS_LP]
    for b in BLOCOS_LP:
        for papel2, locs in (("topo", b["topo"]), ("base", b["base"])):
            for k, loc in enumerate(locs):
                lista.append((b["par"], "movel",
                              "%s %s %d" % (b["nome"], papel2, k), loc))

    for tag in sorted(PARES):
        P = PARES[tag]
        t1 = r.parse_tileset(P["pri"])
        t2 = r.parse_tileset(P["sec"])
        if t1 is None or t2 is None:
            raise SystemExit("o par 0x%X/0x%X do hack não abriu"
                             % (P["pri"], P["sec"]))
        pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}

        # O CHÃO DA FONTE, por evidência e não por constante decorada: tile que
        # aparece na camada de baixo de muitos metatiles DIFERENTES da fonte é
        # piso dela, porque piso é o que se repete debaixo de tudo. Arte de peça
        # aparece em um ou dois.
        quantos = collections.Counter()
        for loc in range(len(t2["meta"]) // 16):
            for v in {x & 0x3FF for x in struct.unpack_from("<8H", t2["meta"],
                                                            loc * 16)[:4]}:
                if v >= r.n_tiles_pri:
                    quantos[v - r.n_tiles_pri] += 1
        chao = {k for k, n in quantos.items() if n >= P["piso_min"]}
        chaos[tag] = sorted(chao)

        def branco(v, t1=t1, t2=t2):
            """A entrada aponta para um tile 8x8 SEM UM PIXEL aceso?

            Tratar tile todo transparente como camada de cima cheia deixaria a
            peça VAZIA; foi assim que o engradado da pedreira saiu branco na
            primeira extração da frente da mina.
            """
            idx = v & 0x3FF
            if not idx:
                return True
            px = (_nibbles(t1["tiles"], idx) if idx < r.n_tiles_pri
                  else _nibbles(t2["tiles"], idx - r.n_tiles_pri))
            return not any(c for linha in px for c in linha)

        def guarda(v, vaga_destino, tag=tag, t1=t1, t2=t2, pal=pal):
            """A CHAVE DO TILE LEVA A PALETA DE ORIGEM. Sem isso, o MESMO
            desenho 8x8 pintado com duas paletas da fonte viraria uma vaga só e
            o segundo apagaria o primeiro."""
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            lado, li = ("p", idx) if idx < r.n_tiles_pri else ("s", idx - r.n_tiles_pri)
            ch = "%s:%s:%d:%d" % (tag, lado, li, ip)
            px = _nibbles(t1["tiles"] if lado == "p" else t2["tiles"], li)
            if tiles_vaga.setdefault(ch, vaga_destino) != vaga_destino:
                raise SystemExit("o tile %s foi pedido nas vagas %d e %d"
                                 % (ch, tiles_vaga[ch], vaga_destino))
            tiles_px[ch] = px
            origem = pal[ip]
            tiles_cor.setdefault(ch, set())
            for linha in px:
                for c in linha:
                    if c:
                        tiles_cor[ch].add(tuple(origem[c]))
            return ch

        for (par, papel, nome, loc) in lista:
            if par != tag:
                continue
            ents = list(struct.unpack_from("<8H", t2["meta"], loc * 16))
            attr = struct.unpack_from("<H", t2["attr"], loc * 2)[0]
            baixo, cima = ents[:4], ents[4:]
            uniforme = len({v & 0x3FF for v in baixo}) == 1
            usadas = []
            for q in range(4):
                vazio_em_cima = branco(cima[q])
                v = baixo[q] if vazio_em_cima else cima[q]
                de_baixo = vazio_em_cima
                if not (v & 0x3FF):
                    usadas.append(None)
                    continue
                ip, idx = (v >> 12) & 0xF, v & 0x3FF
                li = idx - r.n_tiles_pri
                if de_baixo and (uniforme or (idx >= r.n_tiles_pri and li in chao)):
                    usadas.append(None)          # e chao da fonte, nao sobe
                    continue
                if ip not in VAGAS_PAL[tag]:
                    usadas.append(None)
                    continue
                usadas.append(guarda(v, VAGAS_PAL[tag][ip]))
            if not any(usadas):
                raise SystemExit("%s: o metatile %d do par %s não sobrou com "
                                 "nenhum quadrante de arte" % (nome, loc, tag))
            pecas.append(dict(papel=papel, nome=nome, lp=loc, tag=tag, attr=attr,
                              ents=[(baixo[q] if branco(cima[q]) else cima[q])
                                    for q in range(4)],
                              usadas=usadas, baixo=baixo, cima=cima))

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

    # REINDEXA cada nibble para a tabela nova. A cor 0 continua 0 e NENHUMA cor
    # é aproximada: a tabela de destino tem as MESMAS cores RGB da fonte, só em
    # outro índice, então o pixel sai idêntico ao da ROM.
    saida_tiles = {}
    for tag in sorted(PARES):
        P = PARES[tag]
        t1, t2 = r.parse_tileset(P["pri"]), r.parse_tileset(P["sec"])
        pal = {i: _rgb(t1 if i < 6 else t2, i) for i in range(16)}
        for p in pecas:
            if p["tag"] != tag:
                continue
            for q in range(4):
                ch = p["usadas"][q]
                if ch is None:
                    continue
                ip = int(ch.split(":")[3])
                vaga = VAGAS_PAL[tag][ip]
                origem = pal[ip]
                saida_tiles[ch] = [[0 if c == 0 else indice[(vaga, tuple(origem[c]))]
                                    for c in linha] for linha in tiles_px[ch]]

    dados = dict(
        fonte=dict(hack=LP["hack"], autor=LP["autor"], base=LP["base"],
                   arquivo=gba, md5=md5, split=list(LP["split"]),
                   n_tiles_pri=r.n_tiles_pri,
                   pares={t: dict(pri="0x%X" % PARES[t]["pri"],
                                  sec="0x%X" % PARES[t]["sec"],
                                  piso_min=PARES[t]["piso_min"])
                          for t in sorted(PARES)}),
        vagas_livres={str(k): v for k, v in livres.items()},
        paletas=paletas, tiles=saida_tiles, tiles_vaga=tiles_vaga,
        chao_da_fonte=chaos, pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d peças"
          % (os.path.relpath(KIT_JSON, RAIZ), len(saida_tiles), len(pecas)))
    for vaga, cores in sorted(por_vaga.items()):
        print("  vaga %2d: %2d cores nos índices %s"
              % (vaga, len(cores), [indice[(vaga, c)] for c in sorted(cores)]))
    for tag, ch in sorted(chaos.items()):
        print("  chão da fonte %s: %d tiles" % (tag, len(ch)))
    return 0


# --------------------------------------------------------------- o KIT em disco
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa máquina com a ROM"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def chao_nosso():
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele).

    É o calçamento que todo móvel pousa em cima, e o atributo que toda variante
    de chão tem que repetir bit a bit.
    """
    ts = _tileset(SECUNDARIO)
    ents = list(struct.unpack_from("<8H", ts["metatiles"], (CARIMBO - 512) * 16))
    cima = [v for v in ents[4:] if v & 0x3FF]
    if cima:
        import render_maps as RM
        tp = _tileset(PRIMARIO)
        for v in cima:
            t = RM.resolver_tile(tp, ts, v & 0x3FF)
            if t and any(c for linha in t for c in linha):
                raise SystemExit("o carimbo %d tem arte na camada de cima"
                                 % CARIMBO)
    return ents[:4], G._attrs(SECUNDARIO)[CARIMBO - 512]


def desenha_kit():
    """(tiles_novos, metas, attrs, carimbos), sem escrever em disco."""
    dados = kit()
    meta_disco = _ler("metatiles.bin")
    ap = G._attrs(PRIMARIO)
    tp = _tileset(PRIMARIO)
    base, attr_chao = chao_nosso()

    por_peca = {(p["papel"], p["nome"]): p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]
    metas, attrs = {}, {}
    proximo_meta = [META_LOCAL_0]
    carimbos = dict(chao=[], moveis=[], blocos=[])

    def vaga(chave):
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco não tem o tile %s" % chave)
            mapa_tile[chave] = proximo[0]
            tiles_novos[proximo[0]] = dados["tiles"][chave]
            proximo[0] += 1
        return mapa_tile[chave]

    def poe(ents, attr):
        local = proximo_meta[0]
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
        alvo_pal = VAGAS_PAL[p["tag"]][int(ch.split(":")[3])]
        return ((v & 0x0C00) | (512 + vaga(ch)) | (alvo_pal << 12))

    # ------------------------------------------------------------ 1. CHÃO
    for (nome, sobre, quads) in VARIANTES:
        ents = [(PAL_CHAO << 12) | (f << 10) | t for (t, f) in quads]
        gid = poe(ents + [0, 0, 0, 0], attr_chao)
        carimbos["chao"].append(dict(nome=nome, mt=gid, sobre=sobre, nosso=True))

    # ---------------------------------------------------------- 2. MÓVEIS
    por_nome = {}
    for m in MOVEIS_LP:
        p = por_peca[("movel", m["nome"])]
        cima = [entrada(p, q) or 0 for q in range(4)]
        if not any(cima):
            raise SystemExit("%s: peça sem arte" % m["nome"])
        # comportamento ZERADO (nenhum id semântico é importado) e layerType
        # COVERED, que põe as duas camadas ABAIXO do sprite.
        gid = poe(list(base) + cima, 0x1000)
        por_nome[m["nome"]] = cima
        carimbos["moveis"].append(dict(nome=m["nome"], mt=gid, quantos=m["quantos"],
                                       espaco=m["espaco"], importado=True))
    for m in ESPELHOS_LP:
        gid = poe(list(base) + _espelha4(por_nome[m["de"]]), 0x1000)
        carimbos["moveis"].append(dict(nome=m["nome"], mt=gid, quantos=m["quantos"],
                                       espaco=m["espaco"], importado=True,
                                       espelho_de=m["de"]))
    for m in MOVEIS_NOSSOS:
        ents = list(struct.unpack_from("<8H", tp["metatiles"], m["mt"] * 16))
        cima = list(ents[4:])
        if not any(v & 0x3FF for v in cima):
            raise SystemExit("o metatile %d não tem arte na camada de cima"
                             % m["mt"])
        gid = poe(list(base) + cima, 0x1000)
        por_nome[m["nome"]] = cima
        carimbos["moveis"].append(dict(nome=m["nome"], mt=gid, quantos=m["quantos"],
                                       espaco=m["espaco"], importado=False,
                                       copia_de=m["mt"]))
    for m in ESPELHOS_NOSSOS:
        gid = poe(list(base) + _espelha4(por_nome[m["de"]]), 0x1000)
        carimbos["moveis"].append(dict(nome=m["nome"], mt=gid, quantos=m["quantos"],
                                       espaco=m["espaco"], importado=False,
                                       espelho_de=m["de"]))

    # ---------------------------------------------------------- 3. BLOCOS
    por_bloco_ents = {}
    for b in BLOCOS_LP:
        ids = {}
        for papel2, locs, attr_peca in (("topo", b["topo"], attr_chao),
                                        ("base", b["base"], 0x1000)):
            fora = []
            for k, _loc in enumerate(locs):
                p = por_peca[("movel", "%s %s %d" % (b["nome"], papel2, k))]
                cima = [entrada(p, q) or 0 for q in range(4)]
                if not any(cima):
                    raise SystemExit("%s: metade sem arte" % b["nome"])
                fora.append(poe(list(base) + cima, attr_peca))
            ids[papel2] = fora
        carimbos["blocos"].append(dict(nome=b["nome"], topo=ids["topo"],
                                       base=ids["base"], quantos=b["quantos"],
                                       espaco=b["espaco"], largura=len(b["topo"])))
        por_bloco_ents[b["nome"]] = {papel2: [list(metas[g - 512]) for g in ids[papel2]]
                                     for papel2 in ("topo", "base")}
    for b in ESPELHOS_BLOCOS:
        fonte = por_bloco_ents[b["de"]]
        ids = {}
        for papel2, attr_peca in (("topo", attr_chao), ("base", 0x1000)):
            fora = []
            for ents in reversed(fonte[papel2]):      # as metades trocam de lado
                fora.append(poe(list(base) + _espelha4(ents[4:]), attr_peca))
            ids[papel2] = fora
        carimbos["blocos"].append(dict(nome=b["nome"], topo=ids["topo"],
                                       base=ids["base"], quantos=b["quantos"],
                                       espaco=b["espaco"], largura=len(ids["topo"]),
                                       espelho_de=b["de"]))

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))
    if proximo_meta[0] > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)

    # A vaga de metatile só serve se for ENCHIMENTO do dumper ou se já tiver
    # exatamente o que este kit escreve, e o mapa não pode usar o id.
    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    usados = set()
    for nome in IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    for local, ents in metas.items():
        gid = 512 + local
        antigo = _entradas(meta_disco, local)
        if not enchimento(antigo) and antigo != ents:
            raise SystemExit("a vaga de metatile %d já está ocupada" % gid)
        if gid in usados and enchimento(antigo):
            raise SystemExit("o mapa usa o metatile %d e a vaga está vazia" % gid)
    return tiles_novos, metas, attrs, carimbos


def grava_tileset(tiles_novos, metas, attrs):
    """Escreve tiles.png, palettes/*.pal, metatiles.bin e metatile_attributes.bin.

    Idempotente: as vagas de tile, de paleta e de metatile são FIXAS.
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


# ------------------------------------------------------ os CORREDORES da suite
def corredores_multinivel(v, W, H, d):
    """Os corredores da suite, refeitos com a regra da ELEVAÇÃO 15.

    O `enfeita_cidades.corredores_de_teste` simula a caminhada da suite com a
    regra "elevação 0 é curinga e o resto exige igualdade". Essa regra é uma
    APROXIMAÇÃO do `MapGridGetElevationAt`: a elevação 15
    (`ELEVATION_MULTI_LEVEL`) também casa com qualquer vizinho, e foi a
    diferença entre verde e vermelho na frente da orla de Sunyshore. Nesta
    cidade não há NENHUMA célula de elevação 15 (medido: o histograma de
    elevação de `VeilstoneCity` tem 0, 1, 3, 4 e 5 e mais nada), então aqui as
    duas simulações coincidem. A função existe assim mesmo porque a UNIÃO nunca
    é pior: corredor a mais custa enfeite a menos, corredor a menos custa caso
    vermelho, e no dia em que alguém puser passarela nesta cidade a rede já
    está armada.
    """
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_",
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


# ------------------------------------------------------------ o ESPALHAMENTO
def esqueleto(v, W, H, d, elegivel):
    """Caminho de custo mínimo ligando as portas do mapa, em ordem de leitura.

    O custo não é só distância. Andar colado num sólido custa mais, para a
    trilha sair pelo MEIO do corredor e não raspando o prédio; virar custa mais,
    para ela sair reta como caminho batido de verdade; e célula que não pode
    receber mancha custa muito mais, mas não é proibida, senão o caminho não
    atravessa a soleira das portas.
    """
    def andavel(i):
        return not ((v[i] >> 10) & 3)

    def perto_de_solido(x, y):
        return sum(1 for dx, dy in N4
                   if not (0 <= x + dx < W and 0 <= y + dy < H)
                   or ((v[(y + dy) * W + x + dx] >> 10) & 3))

    def custo(x, y):
        c = 1.0 + 2.0 * perto_de_solido(x, y)
        if (x, y) not in elegivel:
            c += 12.0
        return c

    def caminho(ini, fim):
        """Dijkstra com estado (célula, direção), para poder cobrar a curva."""
        alvo = set(fim)
        dist, pai = {}, {}
        fila = [(0.0, ini[0], ini[1], 0, 0)]
        while fila:
            g, x, y, dx0, dy0 = heapq.heappop(fila)
            if (x, y, dx0, dy0) in dist:
                continue
            dist[(x, y, dx0, dy0)] = g
            if (x, y) in alvo and (dx0, dy0) != (0, 0):
                saida, no = [], (x, y, dx0, dy0)
                while no in pai:
                    saida.append((no[0], no[1]))
                    no = pai[no]
                saida.append((no[0], no[1]))
                return saida
            for dx, dy in N4:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H) or not andavel(ny * W + nx):
                    continue
                curva = 9.0 if (dx0, dy0) != (0, 0) and (dx, dy) != (dx0, dy0) else 0.0
                no = (nx, ny, dx, dy)
                if no in dist:
                    continue
                pai[no] = (x, y, dx0, dy0)
                heapq.heappush(fila, (g + custo(nx, ny) + curva, nx, ny, dx, dy))
        return []

    portas = []
    for w in (d.get("warp_events") or []):
        x, y = w["x"], w["y"]
        for dx, dy in ((0, 1), (0, 0), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and andavel(ny * W + nx):
                portas.append((nx, ny))
                break
    chao = sorted(elegivel)
    if chao:
        ymin, ymax = min(y for _, y in chao), max(y for _, y in chao)
        for alvo_y in (ymin, ymax):
            faixa = [p for p in chao if abs(p[1] - alvo_y) <= 1]
            if faixa:
                xs = sorted({p[0] for p in faixa})
                xe = min(xs, key=lambda x: abs(x - W // 2))
                portas.append(min((p for p in faixa if p[0] == xe),
                                  key=lambda p: abs(p[1] - alvo_y)))
    if not portas:
        return set(), []
    # LIGAÇÃO EM ÁRVORE, não em fila: cada porta nova se liga ao ponto já ligado
    # mais perto, o que dá uma rede com cruzamento em vez de zigue-zague.
    ossos = {portas[0]}
    for p in portas[1:]:
        trecho = caminho(p, ossos)
        if trecho:
            ossos |= set(trecho)
    return ossos, portas


def area_trilha(v, W, H, d, elegivel):
    """As células de TRILHA: o esqueleto engordado para três de largura."""
    ossos, portas = esqueleto(v, W, H, d, elegivel)
    pav = set()
    for x, y in ossos:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                p = (x + dx, y + dy)
                if p in elegivel:
                    pav.add(p)
    while True:
        entra = {p for p in elegivel if p not in pav
                 and sum(1 for dx, dy in N4 if (p[0] + dx, p[1] + dy) in pav) >= 3}
        if not entra:
            break
        pav |= entra
    # risco de UMA célula de largura não lê como caminho, lê como sujeira
    while True:
        fora = {(x, y) for x, y in pav
                if not ((x, y - 1) in pav or (x, y + 1) in pav)
                or not ((x - 1, y) in pav or (x + 1, y) in pav)}
        if not fora:
            break
        pav -= fora
    return pav, portas


def bolhas(livres, spec):
    """[(nomes, {células})], bolhas orgânicas crescidas por frente de onda.

    A SEMENTE não é sorteio solto: as células livres são ordenadas por um hash da
    posição e a semente só é aceita a pelo menos 4 (Chebyshev) de toda semente já
    aceita. O CRESCIMENTO é guloso com ruído: a cada passo entra a célula da
    frente de onda com o menor hash. Círculo daria bolha redonda e xadrez daria
    sal e pimenta; frente de onda com ruído dá contorno irregular.
    """
    ordem = sorted(livres, key=lambda p: _mistura(p[0], p[1], 0x5EED))
    tomadas, saida, sementes = set(), [], []
    for esp in spec:
        feitas = 0
        for p in ordem:
            if feitas >= esp["quantas"]:
                break
            if p in tomadas or p not in livres:
                continue
            if any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) < 4 for q in sementes):
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
            if len(corpo) < lo:
                continue
            tomadas |= corpo
            sementes.append(p)
            saida.append((esp["grupo"], corpo))
            feitas += 1
    return saida


def desgasta(trilha, corte):
    """A trilha que vai receber tinta: miolo inteiro e parte da borda.

    Borda reta em calçada de cidade grande existe, mas borda reta de MANCHA não;
    o corte por hash da posição é o que tira a cara de fita adesiva. Não há
    estado nem ordem aqui.
    """
    return {p for p in trilha
            if all((p[0] + dx, p[1] + dy) in trilha for dx, dy in N4)
            or _mistura(p[0], p[1], 0x7A17) % 100 < corte}


def peca_da_mancha(nomes, x, y):
    """Qual das peças do grupo cai nesta célula. Hash da posição, não paridade:
    paridade vira xadrez e o auto-teste reprova."""
    return nomes[_mistura(x, y, 0xA5A5 + len(nomes)) % len(nomes)]


# ----------------------------------------------------------- ligação a pé
def componentes(v, W, H):
    """{célula: rótulo} dos pedaços de chão andável ligados a pé.

    POR QUE NÃO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda é
    alcançável a partir de algum ponto de partida", e ponto de partida ali é
    warp OU objeto: fechar um corredor com warp dos dois lados não tira NENHUMA
    célula do alcance e mesmo assim parte a cidade em duas. Em `SnowpointCity`
    isso passou VERDE numa sabotagem, e é por isso que este segundo portão
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
def plano_mapa(carimbos, base=None):
    """(L, W, H, v, escritas, contas) para `VeilstoneCity`."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    _base_ent, attr_chao = chao_nosso()

    # Os DOIS carimbos têm o MESMO atributo, e isso é conferido aqui e não
    # suposto: sem isso, pintar um em cima do outro mudaria (comportamento,
    # layerType) de célula andável, que é o item 4 do portão de planta.
    asec = G._attrs(SECUNDARIO)
    if asec[CARIMBO2 - 512] != attr_chao:
        raise SystemExit("o carimbo %d tem atributo 0x%04X e o %d tem 0x%04X"
                         % (CARIMBO2, asec[CARIMBO2 - 512], CARIMBO, attr_chao))

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    # ELEGIVEL não filtra elevação, e isso é decisão medida. Esta cidade é a de
    # mais patamar do demake: o carimbo 545 aparece nas elevações 3 (352
    # células), 4 (189) e 5 (1), e o 524 nas elevações 4 (309) e 3 (119).
    # Filtrar pela elevação MAIS COMUM, como a frente da mina fez, jogaria fora
    # 40% do chão a enfeitar. O que protege o corredor não é a elevação da
    # mancha (a mancha não muda colisão nem elevação), e sim o portão de alcance
    # e o de componentes, que rodam com a regra de elevação dos dois lados.
    elegivel = {}
    for i in range(W * H):
        mt = v[i] & 0x3FF
        if not andavel(i) or mt not in (CARIMBO, CARIMBO2):
            continue
        if beh(mt) in AG:
            continue
        elegivel[(i % W, i // W)] = mt
    so545 = {p for p, mt in elegivel.items() if mt == CARIMBO}

    escritas = {}
    trilha, portas = area_trilha(v, W, H, d, set(elegivel))

    # ------------------------------------------------------------- 1. MÓVEIS
    # Eles vêm ANTES da mancha de propósito, e a razão está medida em Snowpoint:
    # móvel posto no carimbo tira uma célula do numerador E do denominador da
    # régua; móvel posto em cima de uma mancha tira só do denominador, o que
    # PIORA a conta.
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    gelo |= corredores_multinivel(v, W, H, d)
    # As células que o `enfeita_cidades.py` já escreveu nesta cidade ficam
    # CONGELADAS: aquele desenho tem plano próprio e reescrevê-lo por cima
    # quebraria o `--desfazer` dele. Aqui a lista sai VAZIA (o
    # `enfeita_cidades.json` cobre onze cidades e `VeilstoneCity` não é uma
    # delas), e a linha fica assim mesmo porque o dia em que alguém enfeitar
    # esta cidade por aquele caminho, este gerador já respeita.
    # NÃO é o plano DESTA passada que entra aqui: congelar o próprio desenho
    # anterior faria o gerador dar plano diferente depois de `--aplicar`, e a
    # idempotência já é garantida pelo `base_de`, que devolve a grade limpa.
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
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

    def livre(x, y):
        """A célula pode receber MÓVEL? Só o carimbo 545, e nunca a trilha.

        O móvel só pousa no 545 porque a camada de BAIXO de todo móvel é a do
        545: pousar num 524 deixaria costura de calçada em volta da peça.
        """
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas or (x, y) not in so545:
            return False
        if (x, y) in trilha:
            return False
        return (aplicado[i] & 0x3FF) == CARIMBO

    def espacado(m, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < m["espaco"]
                       for px, py in por_movel[m["nome"]])

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portões deixarem.

        O portão roda NA HORA e não só no fim: se solidificar esta célula tirar
        do alcance a pé qualquer OUTRA célula, ou partir um pedaço de chão em
        dois, a escrita é desfeita e o gerador segue.
        """
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

    # ------ 1a. BLOCOS, antes da mobília de uma célula, porque eles precisam de
    # um retângulo inteiro e a mobília solta não pode ter comido metade dele. A
    # linha de CIMA continua ANDÁVEL (a arte dela mora na camada de cima, o
    # jogador passa atrás) e por isso não entra em `novos_solidos` nem no portão
    # de alcance; a de BAIXO vira sólida.
    conta_bloco = collections.Counter()
    # O `espaco` de bloco é contado POR NOME e não contra todos os blocos já
    # postos, ao contrário do que a frente da mina fez. A razão é medida: com a
    # conta global, o matacão espelhado ficava com ZERO copias no mapa, porque o
    # matacão e o poste já tinham tomado todo ponto a 10 células ou mais de
    # distância, e um metatile que ninguém usa é vaga gasta à toa. O que impede
    # duas peças de encostarem uma na outra continua sendo o
    # `ESPACO_ENTRE_MOVEIS`, que vale contra TODAS as peças já postas.
    por_bloco = collections.defaultdict(list)
    for b in carimbos["blocos"]:
        larg = b["largura"]
        for x, y in ordem_cel:
            if conta_bloco[b["nome"]] >= b["quantos"]:
                break
            topo = [(x + k, y) for k in range(larg)]
            base_c = [(x + k, y + 1) for k in range(larg)]
            cels = topo + base_c
            if any(not livre(cx, cy) for cx, cy in cels):
                continue
            if any(max(abs(x - px), abs(y - py)) < b["espaco"]
                   for px, py in por_bloco[b["nome"]]):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            for k, (cx, cy) in enumerate(topo):
                j = cy * W + cx
                escritas[j] = (aplicado[j] & 0xFC00) | b["topo"][k]
                aplicado[j] = escritas[j]
            ok = True
            for k, (cx, cy) in enumerate(base_c):
                if not tenta_solidificar(cx, cy, b["base"][k]):
                    ok = False
                    break
            if not ok:
                for cx, cy in cels:
                    j = cy * W + cx
                    if j in escritas and (cx, cy) not in novos_solidos:
                        del escritas[j]
                        aplicado[j] = v[j]
                for cx, cy in base_c:
                    if (cx, cy) in novos_solidos:
                        novos_solidos.remove((cx, cy))
                        postos.remove((cx, cy))
                        del escritas[cy * W + cx]
                        aplicado[cy * W + cx] = v[cy * W + cx]
                continue
            por_bloco[b["nome"]] += cels
            postos += topo
            conta_bloco[b["nome"]] += 1

    lista = carimbos["moveis"]
    for x, y in ordem_cel:
        giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
        for k in range(len(lista)):
            m = lista[(giro + k) % len(lista)]
            if conta_mov[m["nome"]] >= m["quantos"]:
                continue
            if not livre(x, y) or not espacado(m, x, y):
                continue
            # móvel de cidade encosta em alguma coisa: ou num sólido, ou na
            # trilha. Peça solta no meio do vazio lê como erro de mapa.
            perto = any(0 <= x + dx < W and 0 <= y + dy < H
                        and (((aplicado[(y + dy) * W + x + dx] >> 10) & 3)
                             or (x + dx, y + dy) in trilha)
                        for dx, dy in N4)
            if not perto:
                continue
            if not tenta_solidificar(x, y, m["mt"]):
                continue
            por_movel[m["nome"]].append((x, y))
            conta_mov[m["nome"]] += 1
            break

    # ------------------------------------------------------------- 2. MANCHA
    por_nome = {c["nome"]: c for c in carimbos["chao"]}
    conta_mancha = collections.Counter()

    def pintavel(p, nomes):
        """A célula pode receber ALGUMA das peças do grupo?

        A regra do SOBRE é o que impede costura: variante de tecido só entra em
        célula de tecido, variante de liso só em célula de liso, e a laje
        inteira entra nos dois.
        """
        i = p[1] * W + p[0]
        if p not in elegivel or i in escritas:
            return False
        mt = aplicado[i] & 0x3FF
        if mt not in (CARIMBO, CARIMBO2):
            return False
        rot = "545" if mt == CARIMBO else "524"
        return any(por_nome[n]["sobre"] in ("ambos", rot) for n in nomes)

    def pinta(p, nomes):
        i = p[1] * W + p[0]
        mt = aplicado[i] & 0x3FF
        rot = "545" if mt == CARIMBO else "524"
        cabem = [n for n in nomes if por_nome[n]["sobre"] in ("ambos", rot)]
        nome = peca_da_mancha(cabem, p[0], p[1])
        escritas[i] = (aplicado[i] & 0xFC00) | por_nome[nome]["mt"]
        aplicado[i] = escritas[i]
        conta_mancha[nome] += 1

    trilha_nomes = ESPALHA["trilha"]
    for p in sorted(x for x in desgasta(trilha, ESPALHA["borda_trilha"])
                    if pintavel(x, trilha_nomes)):
        pinta(p, trilha_nomes)

    for esp in ESPALHA["bolhas"]:
        livres = {p for p in elegivel if pintavel(p, esp["grupo"])}
        for nomes, corpo in bolhas(livres, [esp]):
            for p in sorted(corpo):
                if pintavel(p, nomes):
                    pinta(p, nomes)

    # -------------------------------------------------------------- PORTÕES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d células ficariam inalcançáveis, ex.: %s"
                         % (ALVO, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcançável"
                             % (ALVO, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (ALVO, "; ".join(queixas)))
    contas = dict(trilha=len(trilha), moveis=dict(conta_mov),
                  blocos=dict(conta_bloco), manchas=dict(conta_mancha),
                  solidos=len(novos_solidos), portas=len(portas),
                  elegiveis=len(elegivel))
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
    """A grade como está no disco, só tirando o que ESTA passada escreveu.

    Sem isso a idempotência morre: planejar sobre um mapa já desenhado por esta
    passada não volta ao mesmo lugar. A saída é a do `porto_canalave.py`.
    """
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    print("kit: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d)"
          % (len(tiles_novos), min(tiles_novos), max(tiles_novos), TETO_TILES,
             TETO_TILES - max(tiles_novos) - 1, len(metas), min(metas),
             max(metas), 512 + min(metas), 512 + max(metas)))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base_de(guardado))
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("%s: %d células elegíveis, trilha %d, mancha %d, %d solidificadas, "
          "%d células mudadas" % (ALVO, contas["elegiveis"], contas["trilha"],
                                  sum(contas["manchas"].values()),
                                  contas["solidos"], len(escritas)))
    print("  mancha: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["manchas"].items())))
    print("  móvel:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    print("  bloco:  " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["blocos"].items())))
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
def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def confere(tiles_novos, metas, attrs, carimbos, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela é chamada várias vezes pelo auto-teste: uma com o plano de verdade, que
    tem que sair sem queixa, e uma por sabotagem, que tem que sair com a queixa
    certa. Regra conferida só no caminho feliz não é regra, e prova positiva sem
    par negativo não é prova.
    """
    mau = []
    dados = kit()
    ap = G._attrs(PRIMARIO)
    asec = G._attrs(SECUNDARIO)
    import render_maps as RM
    tp = _tileset(PRIMARIO)
    ts = _tileset(SECUNDARIO)
    _base_ent, attr_chao = chao_nosso()

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
        return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))

    def px_de(mt_id):
        """Os 256 pixels RGB do metatile, com o kit desta rodada valendo."""
        from PIL import Image
        im = Image.new("RGB", (16, 16), tp["paletas"][0][0])
        p = im.load()
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
                RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                                 [tuple(c) for c in cores],
                                 bool(val & 0x400), bool(val & 0x800))
        return list(im.get_flattened_data())

    # ------------------------------------------------------------ 1. orçamento
    if tiles_novos and max(tiles_novos) >= TETO_TILES:
        mau.append("estoura o teto de %d tiles" % TETO_TILES)
    if metas and max(metas) >= TETO_META:
        mau.append("estoura o teto de %d metatiles" % TETO_META)
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

    # -------- 2. CHÃO novo: atributo idêntico ao do carimbo e camada de cima
    #             VAZIA (camada de cima em célula andável NORMAL tapa o jogador)
    ids_chao = {c["mt"]: c for c in carimbos["chao"]}
    ids_movel = {m["mt"] for m in carimbos["moveis"]}
    ids_topo = {t for b in carimbos["blocos"] for t in b["topo"]}
    ids_base = {t for b in carimbos["blocos"] for t in b["base"]}
    for gid, c in ids_chao.items():
        if atributo(gid) != attr_chao:
            mau.append("o chão %d tem atributo 0x%04X e o carimbo tem 0x%04X"
                       % (gid, atributo(gid), attr_chao))
        if any(e & 0x3FF for e in entradas(gid)[4:]):
            mau.append("o chão %d usa a camada de cima" % gid)
        if c["sobre"] not in ("ambos", "545", "524"):
            mau.append("o chão %d tem `sobre` inválido" % gid)

    # ------- 3. MÓVEL e BASE: COVERED, comportamento zerado, e o NOSSO chão
    #            entrada por entrada na camada de baixo
    for gid in sorted(ids_movel | ids_base):
        a = atributo(gid)
        if (a >> 12) & 0xF != 1:
            mau.append("o móvel %d não está em COVERED" % gid)
        if a & 0xFF:
            mau.append("o móvel %d importou comportamento 0x%02X da fonte"
                       % (gid, a & 0xFF))
        if entradas(gid)[:4] != _base_ent:
            mau.append("o móvel %d não tem o nosso chão na camada de baixo" % gid)
        if not any(e & 0x3FF for e in entradas(gid)[4:]):
            mau.append("o móvel %d não tem arte na camada de cima" % gid)

    # ---- 4. TOPO de bloco: continua ANDÁVEL com o atributo do chão, e a arte
    #        dele NÃO pode ser 100% opaca, senão ela tapa o jogador (E3)
    for gid in sorted(ids_topo):
        if atributo(gid) != attr_chao:
            mau.append("o topo de bloco %d não herdou o atributo do chão" % gid)
        if entradas(gid)[:4] != _base_ent:
            mau.append("o topo de bloco %d não tem o nosso chão embaixo" % gid)
        opac = 0
        for e in entradas(gid)[4:]:
            if e & 0x3FF:
                vaga = (e & 0x3FF) - len(tp["tiles"])
                opac += (_opacos(tiles_novos[vaga]) if vaga in tiles_novos
                         else _opacos(RM.resolver_tile(tp, ts, e & 0x3FF)))
        if opac >= 4 * 64:
            mau.append("o topo de bloco %d tapa o jogador inteiro (E3)" % gid)

    # ---------- 5. nenhuma variante de chão é cópia de outra nem do carimbo
    lista = sorted(ids_chao) + [CARIMBO, CARIMBO2]
    pix = {mt: px_de(mt) for mt in lista}
    for i, a in enumerate(lista):
        for b in lista[i + 1:]:
            dd = sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
                     for p, q in zip(pix[a], pix[b])) / 256.0
            if dd < PISO_DISTANCIA:
                mau.append("as variantes de chão %d e %d têm distância %.1f, "
                           "abaixo do piso de %.1f do varia_carimbo.py: isso é "
                           "enganar a régua" % (a, b, dd, PISO_DISTANCIA))

    # -------------------------------------------- 6 a 12. o plano, no mapa
    L, W, H, v, escritas, contas = plano
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVAÇÃO em (%d,%d)" % (ALVO, x, y))
        if cv and not cn:
            mau.append("%s: colisão 1 -> 0 em (%d,%d), que segue proibida"
                       % (ALVO, x, y))
        if novo in ids_chao:
            if cn != cv or velho not in (CARIMBO, CARIMBO2):
                mau.append("%s: chão em célula errada em (%d,%d)" % (ALVO, x, y))
            rot = "545" if velho == CARIMBO else "524"
            if ids_chao[novo]["sobre"] not in ("ambos", rot):
                mau.append("%s: a variante %d, que é do carimbo %s, foi pintada "
                           "no carimbo %d em (%d,%d)"
                           % (ALVO, novo, ids_chao[novo]["sobre"], velho, x, y))
        elif novo in ids_topo:
            if cn != cv or velho != CARIMBO:
                mau.append("%s: topo de bloco em célula errada em (%d,%d)"
                           % (ALVO, x, y))
        elif novo in ids_movel or novo in ids_base:
            if cv or not cn:
                mau.append("%s: móvel em (%d,%d) não é solidificação 0 -> 1"
                           % (ALVO, x, y))
            if velho != CARIMBO:
                mau.append("%s: móvel fora do carimbo %d em (%d,%d)"
                           % (ALVO, CARIMBO, x, y))
            if (x, y) in ev:
                mau.append("%s: móvel em cima do evento (%d,%d)" % (ALVO, x, y))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) é de fora do kit"
                       % (ALVO, novo, x, y))

    # 7. (comportamento, layerType) de toda célula ANDÁVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: célula andável (%d,%d) mudou (comportamento, "
                       "layerType)" % (ALVO, i % W, i // W))
            break

    # 8 e 9. alcance a pé e LIGAÇÃO a pé
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
            ligacao_intacta(componentes(v, W, H), componentes(saida, W, H), solid)]

    # 10. A MANCHA NÃO PODE SER ADIVINHÁVEL, e o teste tem dois lados.
    #  (a) PADRÃO: nenhuma projeção simples da posição pode ADIVINHAR a peça.
    #  (b) FORMA: mancha é BOLHA, não sal e pimenta, e a conta é o TAMANHO
    #      MÉDIO do pedaço conexo, não quantas vizinhas cada célula tem.
    mancha = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
              if (val & 0x3FF) in ids_chao}
    if len(mancha) < 400:
        mau.append("%s: só %d células de mancha" % (ALVO, len(mancha)))
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
                    mau.append("%s: saber %s mod %d adivinha a peça em %.0f%% das "
                               "células contra %.0f%% do chute cego: virou padrão"
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
            mau.append("%s: a mancha média tem só %.1f células (%d em %d pedaços): "
                       "virou sal e pimenta, não bolha"
                       % (ALVO, len(mancha) / pedacos, len(mancha), pedacos))

    # 11. a régua tem que fechar em 20% ou menos
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("%s: a régua ainda marca %.1f%% de carimbo dominante"
                   % (ALVO, b))

    # 12. os blocos: toda BASE tem um TOPO logo acima, e as contas batem
    bases = {(i % W, i // W) for i, val in escritas.items()
             if (val & 0x3FF) in ids_base}
    topos = {(i % W, i // W) for i, val in escritas.items()
             if (val & 0x3FF) in ids_topo}
    if len(bases) != len(topos):
        mau.append("%s: %d bases de bloco e %d topos" % (ALVO, len(bases),
                                                         len(topos)))
    for x, y in sorted(bases):
        if (x, y - 1) not in topos:
            mau.append("%s: a base de bloco em (%d,%d) está sem topo" % (ALVO, x, y))
            break
    return mau


# ------------------------------------------------------------------ auto-teste
def demo():
    """Prova positiva e DEZ provas negativas, cada sabotagem revertida em seguida.

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
                 plano[5]))

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = confere(*args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NÃO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    # N1. colisão 1 -> 0 numa célula de mancha
    def n1():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a celula ERA solida
        return a
    sabota("colisão 1 -> 0", n1, "colisão 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevação alterada", n2, "mudou ELEVAÇÃO")

    # N3. comportamento de um metatile de CHÃO sabotado
    def n3():
        a = copia()
        gid = carimbos["chao"][0]["mt"]
        a[2][gid - 512] = (a[2][gid - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chão sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        gid = carimbos["moveis"][0]["mt"]
        a[2][gid - 512] = a[2][gid - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no móvel", n4, "não está em COVERED")

    # N5. base de bloco gravada SEM o topo
    def n5():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        topos = {t for b in carimbos["blocos"] for t in b["topo"]}
        for i in sorted(esc):
            if (esc[i] & 0x3FF) in topos:
                del esc[i]
                break
        return a
    sabota("base de bloco sem o topo", n5, "bases de bloco e")

    # N6. camada de BAIXO de um móvel sabotada (arte no lugar do nosso chão)
    def n6():
        a = copia()
        gid = carimbos["moveis"][0]["mt"]
        ent = list(a[1][gid - 512])
        ent[0] = ent[4]
        a[1][gid - 512] = ent
        return a
    sabota("camada de baixo sabotada", n6, "não tem o nosso chão na camada de baixo")

    # N7. mancha escolhida por (x + y) % n, que é xadrez com período
    def n7():
        a = copia()
        original = globals()["peca_da_mancha"]
        globals()["peca_da_mancha"] = lambda nomes, x, y: nomes[(x + y) % len(nomes)]
        try:
            a = (dict(tiles_novos), dict(metas), dict(attrs),
                 json.loads(json.dumps(carimbos)),
                 plano_mapa(carimbos, base_de(guardado)))
        finally:
            globals()["peca_da_mancha"] = original
        return a
    sabota("mancha por (x+y) % n", n7, "virou padrão")

    # N8. corredor fechado que PARTE um pedaço de chão. O portão de alcance
    #     sozinho não pega isso quando há warp dos dois lados, e foi assim que
    #     Snowpoint passou verde com a cidade cortada.
    def n8():
        a = copia()
        L, W, H, v, esc, ct = a[4]
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

    # N9. duas variantes de chão IGUAIS pixel a pixel: é enganar a régua
    def n9():
        a = copia()
        lst = a[3]["chao"]
        a[1][lst[1]["mt"] - 512] = list(a[1][lst[0]["mt"] - 512])
        return a
    sabota("variante de chão duplicada", n9, "abaixo do piso de")

    # N10. variante do carimbo 524 pintada em célula do carimbo 545. E o erro
    #      que produz costura de calçada, e nenhum outro portão o pega: colisão,
    #      elevação, atributo e alcance ficam todos certos.
    def n10():
        a = copia()
        L, W, H, v, esc, ct = a[4]
        so524 = {c["mt"] for c in carimbos["chao"] if c["sobre"] == "524"}
        alvo = min(so524)
        for i in sorted(esc):
            if v[i] & 0x3FF == CARIMBO and (esc[i] & 0x3FF) in \
                    {c["mt"] for c in carimbos["chao"]}:
                esc[i] = (esc[i] & 0xFC00) | alvo
                return a
        raise SystemExit("não achei célula de 545 pintada para a sabotagem N10")
    sabota("variante do 524 no carimbo 545", n10, "foi pintada no carimbo")

    # N11. cor nova escrita num índice que os NOSSOS pixels já usam: é o único
    #      jeito de a vaga de índice vago estragar o desenho de quem já estava lá
    def n11():
        a = copia()
        dados = kit()
        alvo_vaga = None
        for vaga in sorted(dados["paletas"]):
            usados = [i for i in range(1, 16)
                      if i not in set(dados["vagas_livres"].get(vaga) or [])]
            if usados:
                alvo_vaga, alvo_idx = vaga, usados[0]
                break
        if alvo_vaga is None:
            raise SystemExit("nenhuma vaga do kit tem índice já usado")
        pal = [list(c) for c in dados["paletas"][alvo_vaga]]
        pal[alvo_idx] = [255, 0, 255]
        dados["paletas"][alvo_vaga] = pal
        with open(KIT_JSON + ".sab", "w") as f:
            json.dump(dados, f)
        os.replace(KIT_JSON, KIT_JSON + ".bak")
        os.replace(KIT_JSON + ".sab", KIT_JSON)
        return a
    try:
        sabota("cor nova em índice já usado", n11, "que algum pixel nosso usa")
    finally:
        if os.path.exists(KIT_JSON + ".bak"):
            os.replace(KIT_JSON + ".bak", KIT_JSON)

    # ------------------------------------------------ o que está NO DISCO
    # Sem este caso o auto-teste só confere o que ele mesmo acabou de calcular.
    from PIL import Image
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.load()

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    postas = [l for l in metas if not enchimento(_entradas(meta_disco, l))]
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
        for vaga, tile in tiles_novos.items():
            if (vaga // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d não cabe no tiles.png" % vaga)
                continue
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco não é o do kit" % vaga)
        for vaga, cores in sorted(kit()["paletas"].items()):
            arq = [l.split() for l in
                   open(f"{DESTINO}/palettes/%s.pal" % vaga.zfill(2)).read().split("\n")[3:]
                   if l.strip()]
            if [[int(z) for z in c] for c in arq[:16]] != cores:
                mau.append("a paleta %s no disco não é a do kit" % vaga)

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
        mau.append("%s: desfazer não devolve a base" % ALVO)
    _, _, _, _, esc2, _ = plano_mapa(carimbos, volta)
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
    print("  %s: %d células mudadas, %d solidificadas, régua %.1f%% (mt %d) -> "
          "%.1f%% (mt %d)" % (ALVO, len(escritas), contas["solidos"], a, ida,
                              b, idb))
    print("  %d tiles, %d metatiles, %d provas negativas:"
          % (len(tiles_novos), len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-32s -> %s" % (nome, queixa[:100]))
    return 0


def main():
    if "--extrai" in sys.argv:
        return extrai()
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
