#!/usr/bin/env python3
"""Segunda passada de arte em `SnowpointCity`: MANCHA DE CHAO, VARIANTE DE
ARVORE, MOBILIA SOLIDA, BONECO DE NEVE e POSTE, no `gTileset_Snowpoint`.

POR QUE EXISTE, e por que a primeira passada nao bastou. O commit 44cb13b7b7
importou onze pecas PLANAS de neve do Golden Glazed e derrubou o carimbo
dominante de `SnowpointCity` de 87,9% para 66,8% do chao andavel a pe (regua de
`dev_scripts/regua_cidades.py`). O Gui olhou e disse que ficou pouco: a cidade
continuava um mar branco com duzentos pinheiros IGUAIS em grade. A conta explica
o olho. Aquela passada usou as onze pecas com muita economia, 168 celulas de
794, e todas encostadas no bosque, porque cada peca exigia vizinho solido; e so
sabia fazer marca de chao, porque a definicao de pronto dela proibia colisao
0 -> 1, e sem solidificar celula nao entra boneco, poste, cerca nem pedra.

A LEI MUDOU em 07/09/2026 e e ela que destrava esta passada: colisao 0 -> 1 e
PERMITIDA em celula que nao seja caminho, warp, evento nem alcance de script,
desde que o ALCANCE A PE continue o mesmo. Colisao 1 -> 0 segue proibida.

A DECISAO 56 DO GUI, que e a lei desta versao: a passada entra SEM A CALCADA DE
PEDRA. Uma versao anterior deste script (a branch `refino-neve2`) desenhava 420
celulas de calcada nove-fatias importada do Golden Glazed, e era ela que gastava
a UNICA vaga de paleta livre do tileset, a 10. O Gui olhou e cortou: Snowpoint e
uma cidade de gelo no fim do mundo, nao um centro urbano, e rua de pedra
descaracteriza. Sem a calcada, a vaga 10 volta a ficar livre, e e ela que paga o
BONECO DE NEVE que o Gui pediu pelo nome.

AS CINCO FRENTES DESTA PASSADA, em ordem de impacto medido na regua:

1. MANCHA DE CHAO, e ela sozinha e quem move a regua. As onze pecas planas da
   primeira passada (metatiles 680 a 690) tem o MESMO atributo da neve lisa
   (0x0021), sao andaveis e nao mexem em colisao: espalhar mais delas e de graca
   em orcamento e e a unica alavanca que existe depois que a calcada saiu. Elas
   entram em duas formas, e nenhuma das duas e sorteio solto:
     - a TRILHA, que e o esqueleto de custo minimo entre as portas do mapa,
       engordado para tres celulas de largura e depois DESGASTADO na borda (ver
       `desgasta_trilha` e `BORDA_TRILHA`). E o mesmo esqueleto que a versao com
       calcada usava, so que agora ele nao vira pedra: vira NEVE BATIDA, as seis
       pecas discretas do kit (683 a 688), que e o que sobra no chao onde muita
       gente pisa. A cidade ganha a leitura de "por aqui se anda" sem ganhar uma
       rua de pedra, e sem a borda reta que calcada tem e neve nao tem.
     - as MANCHAS, bolhas organicas crescidas a partir de sementes espalhadas
       pelo resto da neve, de dois grupos: gelo (689 e 690, o cristal forte) e
       banco de neve (681 e 682, a cunha branca, que so semeia encostada no
       solido porque tem borda dura de um lado). A bolha cresce por frente de
       onda com ruido, entao ela sai com contorno irregular, nao circulo nem
       xadrez. Neve batida nao faz bolha de proposito: ela e marca de quem
       passa, e fora da trilha seria pegada de ninguem.
2. VARIANTE DE ARVORE. As 193 arvores 2x2 do bosque sao o MESMO bloco
   (520,521 / 528,529), celula por celula. Duas silhuetas novas do Golden Glazed
   entram como bloco 2x2 alternativo, e a escolha por arvore e um rodizio sobre
   a lista embaralhada por posicao: nao e xadrez, nao tem periodo. Arvore troca
   por arvore e SOLIDO por SOLIDO: nenhuma dessas celulas muda de colisao, de
   elevacao nem de alcance.
3. MOBILIA SOLIDA. Placa, poste, cerca, pedra com neve e arbusto seco JA EXISTEM
   desenhados no nosso `gTileset_Snowpoint` (metatiles 515, 585, 593, 594, 577,
   516 e 517) e nenhum dos cinco mapas do tileset os usava. Custam zero tile e
   zero paleta: o que faltava era o direito de solidificar a celula. O unico
   movel de chao importado e o arbusto sob neve do Golden Glazed (metatile 25).
4. BONECO DE NEVE, do `Pokemon Scorched Silver`, tileset secundario `0x4924B4`,
   metatiles 70 (cabeca com olho, cenoura e bracos de graveto), 71 (a mesma
   cabeca com gorro vermelho) e 78 (o corpo). Foi o Gui que pediu pelo nome, e
   ele existe: o atlas dos 512 metatiles daquele secundario foi renderizado
   nesta frente e a faixa 56 a 95 olhada de perto, e o par 70 sobre 78, montado
   e ampliado, e um boneco de neve inteiro.
5. POSTE DE FERRO do proprio Golden Glazed, metatiles 159 (o capitel dourado) e
   230 (a haste com a base). Ele so entra porque SOBROU vaga de cor: ver o
   orcamento de paleta abaixo, que e a conta que decidiu.

O ORCAMENTO DE PALETA, que e a conta mais apertada da rodada e a que decide
quem entra. `NUM_PALS_TOTAL` e 13 (`include/fieldmap.h`): seis vagas sao do
primario e sete do secundario. Das sete do `gTileset_Snowpoint`, as vagas 6, 7,
8, 9, 11 e 12 ja estao em uso por metatiles vivos, e sobra UMA, a 10. Medido em
07/09/2026: compactar as seis paletas em uso nao libera nada, porque a uniao do
MELHOR par delas ja da 17 cores nao-zero e so cabem 15. Ou seja, a vaga 10 e
toda a moeda que esta passada tem.

E ela deu para os DOIS. O boneco usa 7 cores nao-zero (da paleta 1 do PRIMARIO
do Scorched Silver) e o poste usa 7 (da paleta 9 do secundario do Golden
Glazed), com DUAS iguais nas duas listas, o branco puro (255,255,255) e o cinza
azulado (98,98,123). A uniao da 12 cores nao-zero de 15, entao os dois entram na
vaga 10 SEM APROXIMAR NENHUMA COR: cada nibble e reindexado para a tabela nova e
o pixel sai identico ao da ROM. A parte do poste que usa a paleta 6 do hack nao
gasta nada, porque a nossa vaga 6 JA E a paleta 6 do Golden Glazed desde a
primeira passada.

COMO O BONECO E O POSTE SAO MONTADOS, que e onde mora a armadilha de camada. Os
dois tem duas celulas de altura e os dois vem desenhados assim na fonte:

  - a celula DE CIMA (a cabeca do boneco, o capitel do poste) continua ANDAVEL.
    A arte dela mora na camada de CIMA e so nos dois quadrantes de BAIXO; a
    camada de baixo recebe a NOSSA neve, entrada por entrada. O atributo e o do
    metatile 513 INTEIRO (0x0021), que e o que a regra 3 desta onda cobra de
    toda celula andavel. Com layerType NORMAL a camada de cima vai para o BG1,
    que desenha ACIMA do sprite: e por isso que o jogador passa ATRAS da cabeca
    do boneco, que e exatamente o que a fonte faz. Isso NAO acende o E3 do
    `mapas_qa.py`, e o motivo esta medido: o E3 so acusa camada de cima 100%
    opaca, e aqui dois dos quatro quadrantes estao vazios. O auto-teste mede
    esse numero em vez de confiar.
  - a celula DE BAIXO (o corpo do boneco, a haste do poste) vira SOLIDA, e o
    atributo dela e comportamento ZERADO com layerType COVERED (0x1000). COVERED
    poe as duas camadas ABAIXO do sprite, que e o que faz o jogador parado ao
    sul aparecer NA FRENTE do boneco. Celula solida nao entra em nenhuma das
    reguas de celula andavel, e o E3 tambem so olha celula alcancavel.

DE ONDE VEM O RESTO DA ARTE, e o que cada peca herda de quem:

  - ARVORE: metatile inteiro do Golden Glazed, paleta 6, que ja e nossa desde a
    primeira passada. O ATRIBUTO e o da NOSSA arvore que ele substitui, posicao
    por posicao (520, 521, 528 ou 529), e os quatro valem 0x0000.
  - ARBUSTO SOB NEVE: camada de baixo do nosso 513, camada de cima inteira do
    hack, atributo `attr & 0xF000`, ou seja o layerType do hack (COVERED) com o
    comportamento ZERADO, porque comportamento e id semantico e a regra 7 do PRD
    proibe importar id, so arte.
  - MANCHA: nada de novo. Sao os metatiles 680 a 690 que a primeira passada ja
    gravou, com o mesmo atributo 0x0021 da neve lisa.
  - MOBILIA NOSSA: nenhum metatile novo, so o bit de colisao da celula. A unica
    excecao e o metatile 516, a pedra com touca de neve, que esta gravado com
    comportamento 0x02, MB_TALL_GRASS, e como nenhum mapa o usava ninguem tinha
    notado; usa-lo como esta planta grama alta numa cidade de neve e o
    `mapas_qa.py` acusa D1. Trocar o atributo do 516 esta PROIBIDO (metatile
    vivo de tileset dividido por seis layouts), entao entra uma COPIA dele em
    vaga livre, com os mesmos oito tiles byte a byte, o mesmo layerType e o
    comportamento zerado.

A NEVE DO FUNDO E SEMPRE A NOSSA. Onde a fonte deixa a camada de baixo
transparente, ou pinta a neve DELA, entra a entrada do nosso metatile 513 naquele
quadrante, byte a byte. A neve do hack e achada por evidencia e nao por
constante decorada: a camada de baixo do metatile ancora e chao liso com as
quatro entradas iguais, e todo tile com os mesmos 64 nibbles daquele e neve
lisa. Sem isso a arvore importada chegava com um retangulo de neve mais clara em
volta, que foi o que o primeiro render da frente anterior mostrou.

ONDE CADA COISA CAI, e isso e julgamento com portao, nao sorteio:

  - A TRILHA nasce do esqueleto de custo minimo entre as soleiras das portas
    (ginasio, centro pokemon, loja, templo, as duas casas do norte), mais a
    entrada norte do mapa e as duas pontas do porto. O custo penaliza CURVA e
    penaliza andar COLADO no solido, entao ela sai reta e pelo MEIO do corredor.
    A ligacao e em arvore: cada porta liga ao ponto ja ligado mais perto, o que
    da cruzamento em vez de zigue-zague.
  - Movel de BEIRA (pedra, arbusto, arbusto de neve) exige vizinho solido: e o
    que encosta no bosque, como neve empilhada.
  - Movel de TRILHA (placa, poste, cerca, boneco) exige vizinho da trilha, e
    NUNCA cai em cima dela: mobiliario de rua fica na beira do caminho, e boneco
    de neve tambem, porque boneco de neve e feito por gente que passa.
  - Nenhum movel cai em evento nem na orla de 1 celula em volta dele, nem em
    celula que a suite critica ANDA (`enfeita_cidades.corredores_de_teste`, que
    ja custou sete casos de balsa em Canalave), nem em celula que o
    `enfeita_cidades.py` reservou, nem a menos de 2 celulas da borda.
  - Cada movel novo passa pelo PORTAO DE ALCANCE na hora, nao so no fim: se
    solidificar aquela celula tirar do alcance a pe qualquer celula que nao seja
    ela mesma, ou partir um pedaco de chao em dois, o movel e desfeito e o
    gerador segue.

ORDEM INTERNA, e ela tem consequencia medida na regua. Trilha (so calculada),
depois arvore, depois MOVEL, e a MANCHA por ultimo. O movel vem antes da mancha
de proposito: movel posto em neve lisa tira uma celula do numerador E do
denominador da regua, e movel posto em cima de uma mancha tira so do
denominador, o que PIORA a conta. Deixando a mancha por ultimo, todo movel cai
em neve lisa.

Idempotente: vaga de tile, de paleta e de metatile sao fixas, e o plano guarda o
valor antigo de cada celula em `dev_scripts/neve_snowpoint2.json`. Rodar duas
vezes da byte identico.

ORDEM DE RODAR: `neve_snowpoint.py` primeiro, depois `enfeita_cidades.py`, e
este por ultimo. Ele planeja sobre a grade que ESTA no disco (as duas passadas
anteriores ja desenhadas) e so encosta em celula de neve lisa nossa (o metatile
513 ou um dos onze da primeira passada, 680 a 690, que tem o mesmo 0x0021).

Uso:
    python3 dev_scripts/neve_snowpoint2.py             # mede e mostra o plano
    python3 dev_scripts/neve_snowpoint2.py --aplicar   # escreve tileset e mapa
    python3 dev_scripts/neve_snowpoint2.py --desfazer  # devolve o map.bin
    python3 dev_scripts/neve_snowpoint2.py --demo      # auto-teste
    python3 dev_scripts/neve_snowpoint2.py --autoteste # idem
    python3 dev_scripts/neve_snowpoint2.py --extrai    # regera o kit das ROMs
"""
import collections
import heapq
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402
import neve_snowpoint as N1          # noqa: E402

ALVO = "SnowpointCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/snowpoint"
KIT_JSON = f"{RAIZ}/dev_scripts/neve_snowpoint2_kit.json"
PLANO = f"{RAIZ}/dev_scripts/neve_snowpoint2.json"

IRMAOS = N1.IRMAOS          # os cinco layouts que dividem o gTileset_Snowpoint
CHAO = N1.CHAO              # 513, a neve lisa
KIT1 = list(range(680, 691))  # os onze metatiles planos da primeira passada
TETO_TILES = 512
TETO_META = 512
MARGEM = 2

TILE_LOCAL_0 = 238          # primeira vaga de tile livre depois da 1a passada
META_LOCAL_0 = 179          # primeira vaga de metatile livre (id global 691)
PAL_NOVA = 10               # unica vaga de paleta livre do gTileset_Snowpoint
PAL_MATA = 6                # a paleta da 1a passada, ja nossa (= a 6 do GG)

# As duas fontes. `pals` diz que paleta de origem vira o que aqui dentro:
# a 6 do Golden Glazed ja e a nossa vaga 6; tudo o mais vai para a vaga 10.
FONTES = {
    "gg": dict(slug="golden-glazed", ts1=0x3DF704, ts2=0x3DF7AC,
               hack="Pokemon Golden Glazed",
               mapa="grupo 0 mapa 0 (a cidade de neve)",
               ancora_neve=12, pals={PAL_MATA: PAL_MATA, 9: PAL_NOVA}),
    "ss": dict(slug="scorched-silver", ts1=0x49240C, ts2=0x4924B4,
               hack="Pokemon Scorched Silver",
               mapa="grupo 0 mapa 11 (um dos 9 mapas que usam este par)",
               ancora_neve=None, pals={1: PAL_NOVA}),
}

# ------------------------------------------------------------------- o KIT
# ARVORE: bloco 2x2 do hack que substitui o nosso (520,521 / 528,529). Onde o
# hack so tem a METADE ESQUERDA desenhada, a direita e a mesma arte com o bit
# de espelho horizontal ligado, que e o que o proprio hack faz nos pares 5/6,
# 13/14 e 77/78 e nao custa tile novo.
ARVORES = [
    dict(nome="pinheiro copado", gg=[(13, 0), (14, 0), (21, 0), (22, 0)]),
    dict(nome="pinheiro esguio", gg=[(133, 0), (133, 1), (141, 0), (141, 1)]),
]
NOSSA_ARVORE = [520, 521, 528, 529]     # ordem de leitura do bloco 2x2

# MOVEL DE CHAO IMPORTADO: uma celula so. `sobre_nossa_neve` troca a camada de
# baixo do hack pela do nosso 513.
MOVEIS_GG = [
    dict(nome="arbusto sob neve", gg=25, espelha=False),
    dict(nome="arbusto sob neve espelhado", gg=25, espelha=True),
]

# MOVEL DE DUAS CELULAS: a de baixo e solida, a de cima continua andavel. Ver o
# cabecalho, secao "COMO O BONECO E O POSTE SAO MONTADOS".
TORRES = [
    dict(nome="boneco de neve", fonte="ss", topo=70, base=78,
         onde="trilha", quantos=3, espaco=9),
    dict(nome="boneco de neve de gorro", fonte="ss", topo=71, base=78,
         onde="trilha", quantos=2, espaco=9),
    dict(nome="poste de ferro", fonte="gg", topo=159, base=230,
         onde="trilha", quantos=8, espaco=5),
]

# MOVEL NOSSO: metatile que JA existe no gTileset_Snowpoint e que nenhum dos
# cinco mapas usava. Custa zero tile, zero paleta e zero metatile novo.
#   `onde`: "beira"   = precisa de vizinho SOLIDO (encosta no bosque)
#           "trilha"  = precisa de vizinho da trilha (mobiliario de caminho)
# O metatile 547 foi TIRADO desta lista depois de olhar o render: ele nao e um
# pedregulho solto, e um pedaco de PAREDE de barranco, e sozinho na neve vira um
# retangulo marrom chapado.
MOVEIS_NOSSOS = [
    dict(nome="pedra com neve",      mt=516, onde="beira",  quantos=16, espaco=4),
    dict(nome="arbusto seco",        mt=517, onde="beira",  quantos=16, espaco=4),
    dict(nome="placa de madeira",    mt=515, onde="trilha", quantos=6,  espaco=8),
    dict(nome="poste",               mt=585, onde="trilha", quantos=10, espaco=4),
    dict(nome="poste baixo",         mt=593, onde="trilha", quantos=8,  espaco=4),
    dict(nome="cerca",               mt=594, onde="trilha", quantos=8,  espaco=4),
    dict(nome="cerca de canto",      mt=577, onde="trilha", quantos=6,  espaco=4),
]
TETO_MOVEIS = 110
ESPACO_ENTRE_MOVEIS = 2     # Chebyshev minimo entre dois moveis QUAISQUER

# ------------------------------------------------------------------ a MANCHA
# Os tres grupos de peca plana da primeira passada, por leitura de arte. Foram
# renderizados um a um sobre neve lisa antes de dividir, e a divisao segue o que
# a imagem mostra, nao o nome que o kit anterior deu:
#   batida  as seis marcas discretas, riscos brancos curtos: e o que fica no
#           chao onde muita gente pisa, e e a unica que serve para cobrir area
#           grande sem virar poluicao.
#   gelo    o cristal forte, a peca mais chamativa das onze: bolha pequena.
#   banco   a cunha branca de borda dura, que so fecha o desenho quando tem
#           solido de um lado; por isso ela SO semeia encostada no bosque.
GRUPOS_MANCHA = {
    "batida": [683, 684, 685, 686, 687, 688],
    "gelo":   [689, 690],
    "banco":  [681, 682],
}
# QUANTAS BOLHAS DE CADA GRUPO, e o tamanho alvo de cada uma (min, max). So
# GELO e BANCO fazem bolha, e as duas razoes sao diferentes:
#
#   - `batida` nao faz, e isso e desenho e nao economia: neve batida e a marca
#     de quem PASSA, entao ela pertence a trilha e a mais nada. Bolha de neve
#     batida no meio do bosque, longe de qualquer porta, seria pegada de
#     ninguem. A primeira versao desta lista tinha 10 bolhas de `batida` no fim
#     e elas puseram ZERO celula no mapa, porque nao sobrava espaco livre com a
#     folga de semente exigida; a linha saiu em vez de ficar de enfeite.
#   - a ORDEM importa e tem consequencia medida: com `batida` na FRENTE, as
#     bolhas dela comiam o chao livre e sobravam 3 celulas de gelo e 4 de banco
#     no mapa inteiro, ou seja as duas pecas mais bonitas do kit ficavam
#     invisiveis. Gelo e banco sao os escassos e por isso servem primeiro.
BOLHAS = [
    dict(grupo="gelo",   quantas=10, tam=(3, 7)),
    dict(grupo="banco",  quantas=12, tam=(4, 9)),
]
# A TRILHA PINTADA NAO E O RETANGULO INTEIRO. O esqueleto dilatado da uma fita
# de tres celulas de largura com borda reta, e borda reta em neve nao existe: o
# miolo entra sempre e a BORDA entra so em parte, sorteada pelo hash da posicao.
# O que sai e uma trilha de uma a tres celulas com contorno irregular, que e o
# que pisada de gente faz na neve, e que ainda deixa neve lisa respirando ao
# lado. Em porcento das celulas de borda.
BORDA_TRILHA = 80
TETO_REGUA = 25.0           # o alvo do Gui: carimbo dominante <= 25%

N4 = E.N4
DIAG = {"no": (-1, -1), "nl": (1, -1), "so": (-1, 1), "sl": (1, 1)}


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem
    que sair identico em qualquer maquina e em qualquer versao de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


# ------------------------------------------------------------------ extracao
def extrai():
    """Regera `neve_snowpoint2_kit.json` a partir das ROMs privadas dos hacks.

    So roda na maquina que tem `fontes-mapas/romhacks/`. O que sai daqui e o
    asset convertido (tiles em nibbles, ja reindexados para a paleta nova, e a
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

    def nibbles(dados, local):
        """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
        b = dados[local * 32:local * 32 + 32]
        return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
                 for x in range(8)] for y in range(8)]

    def rgb(ts, i):
        c = struct.unpack_from("<16H", ts["pal"], i * 32)
        return [[((v >> s) & 0x1F) * 255 // 31 for s in (0, 5, 10)] for v in c]

    # o que cada fonte precisa entregar
    quero = {"gg": [], "ss": []}
    for a in ARVORES:
        quero["gg"] += [("arvore", g) for g, _e in a["gg"]]
    quero["gg"] += [("movel", m["gg"]) for m in MOVEIS_GG]
    for t in TORRES:
        quero[t["fonte"]] += [("topo", t["topo"]), ("base", t["base"])]

    abertas, pecas, neve = {}, [], {}
    # (fonte, lado, local) -> paleta de origem
    tiles_pal, tiles_px = {}, {}
    for chave, F in FONTES.items():
        if not quero[chave]:
            continue
        pasta = os.path.join(ferr, F["slug"])
        gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
        caminho = os.path.join(pasta, gba)
        r = Rom(caminho)
        t1, t2 = r.parse_tileset(F["ts1"]), r.parse_tileset(F["ts2"])
        npri = r.n_tiles_pri
        abertas[chave] = dict(
            hack=F["hack"], arquivo=gba,
            md5=hashlib.md5(open(caminho, "rb").read()).hexdigest(),
            ts1="0x%X" % F["ts1"], ts2="0x%X" % F["ts2"], mapa=F["mapa"],
            n_tiles_pri=npri)

        # A NEVE LISA DA FONTE, achada por evidencia e nao por constante
        # decorada: a camada de baixo do metatile ancora e chao liso com as
        # quatro entradas iguais, e todo tile com os MESMOS 64 nibbles daquele
        # tambem e neve lisa. Quem estiver nesta lista nao entra no nosso
        # tileset: no lugar dele vai a neve do NOSSO metatile 513, senao a
        # arvore importada chega com um retangulo de neve mais clara em volta.
        neve[chave] = []
        if F["ancora_neve"] is not None:
            baixo = list(struct.unpack_from("<8H", t2["meta"],
                                            F["ancora_neve"] * 16))[:4]
            if len({x & 0x3FF for x in baixo}) != 1:
                raise SystemExit("o metatile %d de %s deixou de ser chao liso; a "
                                 "deteccao da neve da fonte precisa de outra "
                                 "ancora" % (F["ancora_neve"], chave))
            ref = (baixo[0] & 0x3FF) - npri
            alvo_px = nibbles(t2["tiles"], ref)
            neve[chave] = sorted(k for k in range(len(t2["tiles"]) // 32)
                                 if nibbles(t2["tiles"], k) == alvo_px)

        vistos = set()
        for papel, local in quero[chave]:
            if (chave, local) in vistos:
                continue
            vistos.add((chave, local))
            ents = list(struct.unpack_from("<8H", t2["meta"], local * 16))
            chao_embaixo = _baixo_e_chao(papel, ents)
            for k, val in enumerate(ents):
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if idx == 0:
                    continue
                # a camada de BAIXO nao entra no kit quando ela e so chao da
                # fonte: no lugar dela vai a do nosso metatile 513.
                if k < 4 and chao_embaixo:
                    continue
                if ip not in F["pals"]:
                    raise SystemExit("%s: metatile %d usa a paleta %d, e o kit so "
                                     "importa %s" % (chave, local, ip,
                                                     sorted(F["pals"])))
                lado, li = ("p", idx) if idx < npri else ("s", idx - npri)
                if k < 4 and (lado == "s" and li in neve[chave]):
                    continue
                ch = "%s:%s:%d" % (chave, lado, li)
                if tiles_pal.setdefault(ch, ip) != ip:
                    raise SystemExit("o tile %s aparece com duas paletas de "
                                     "origem, %d e %d"
                                     % (ch, tiles_pal[ch], ip))
                tiles_px[ch] = nibbles(t1["tiles"] if lado == "p" else t2["tiles"], li)
            pecas.append(dict(papel=papel, fonte=chave, gg=local, ents=ents,
                              attr=struct.unpack_from("<H", t2["attr"],
                                                      local * 2)[0]))
        abertas[chave]["paletas"] = {str(i): rgb(t1 if i < 6 else t2, i)
                                     for i in sorted(set(F["pals"]))}

    # ------------------------------------------------- a paleta nova, vaga 10
    # Uniao das cores NAO-ZERO realmente usadas pelos tiles que vao apontar para
    # a vaga 10. Cor igual nas duas fontes conta UMA vez: e isso que faz o
    # boneco e o poste caberem juntos. Nada e aproximado; se estourar 15, para.
    usadas = []
    for ch, ip in sorted(tiles_pal.items()):
        fonte = ch.split(":")[0]
        if FONTES[fonte]["pals"][ip] != PAL_NOVA:
            continue
        origem = abertas[fonte]["paletas"][str(ip)]
        for linha in tiles_px[ch]:
            for c in linha:
                if c and origem[c] not in usadas:
                    usadas.append(origem[c])
    usadas.sort()
    if len(usadas) > 15:
        raise SystemExit("a vaga %d precisaria de %d cores nao-zero e so cabem "
                         "15: %s" % (PAL_NOVA, len(usadas), usadas))
    nova = [[0, 0, 0]] + usadas + [[0, 0, 0]] * (15 - len(usadas))
    indice = {tuple(c): i + 1 for i, c in enumerate(usadas)}

    # reindexa cada tile da vaga 10 para a tabela nova; a cor 0 continua 0.
    saida_tiles = {}
    for ch, px in sorted(tiles_px.items()):
        fonte, ip = ch.split(":")[0], tiles_pal[ch]
        if FONTES[fonte]["pals"][ip] == PAL_NOVA:
            origem = abertas[fonte]["paletas"][str(ip)]
            px = [[0 if c == 0 else indice[tuple(origem[c])] for c in linha]
                  for linha in px]
        saida_tiles[ch] = px

    dados = dict(fontes=abertas, paleta={str(PAL_NOVA): nova},
                 cores_usadas=len(usadas), tiles=saida_tiles,
                 tiles_paleta=tiles_pal, neve_da_fonte=neve, pecas=pecas)
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, %d cores nao-zero na vaga %d, %d pecas, "
          "%d fontes" % (os.path.relpath(KIT_JSON, RAIZ), len(saida_tiles),
                         len(usadas), PAL_NOVA, len(pecas), len(abertas)))
    return 0


# --------------------------------------------------------------------- leitura
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com as ROMs"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def _entradas(bin_meta, local):
    return list(struct.unpack_from("<8H", bin_meta, local * 16))


def _espelha4(quad):
    """Espelho horizontal de uma camada: troca as colunas e liga o bit 0x400."""
    fora = []
    for q in (1, 0, 3, 2):
        v = quad[q]
        fora.append(0 if (v & 0x3FF) == 0 else (v ^ 0x400))
    return fora


def _opacos(px):
    return sum(1 for linha in px for c in linha if c)


def _baixo_e_chao(papel, ents):
    """A camada de BAIXO desta peca e so CHAO da fonte, e por isso sai inteira?

    Duas assinaturas, e as duas sao de evidencia, nao de nome de metatile:

      - `topo` e `movel` pousam no chao por construcao: a arte deles mora toda
        na camada de cima.
      - qualquer peca cuja camada de baixo repete o MESMO tile nos quatro
        quadrantes. Repetir um 8x8 quatro vezes e o que chao faz e o que arte
        nao faz, e e essa assinatura que separa o CORPO do boneco (quatro copias
        do tile de neve do Scorched Silver, que nao pode entrar no nosso
        tileset) da BASE do poste (quatro tiles diferentes, que sao a haste
        desenhada e tem que entrar).

    Sem isso o corpo do boneco trazia junto o tile de neve do OUTRO hack, que
    gasta vaga, gasta cor na paleta 10 e aparece nos ombros arredondados, onde a
    camada de cima e transparente.
    """
    return papel in ("topo", "movel") or len({e & 0x3FF for e in ents[:4]}) == 1


# ------------------------------------------------------------------ importacao
def desenha_kit():
    """(tiles_novos, metas, attrs, carimbos), sem escrever nada em lugar nenhum.

    `carimbos` sai como dicionario: `arvores` (blocos 2x2), `moveis` (de uma
    celula) e `torres` (de duas).
    """
    dados = kit()
    meta_snow = open(f"{DESTINO}/metatiles.bin", "rb").read()
    attr_snow = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()

    chao_ents = _entradas(meta_snow, CHAO - 512)
    attr_chao = struct.unpack_from("<H", attr_snow, (CHAO - 512) * 2)[0]
    if chao_ents[4:] != [0, 0, 0, 0]:
        raise SystemExit("o metatile %d ja usa a camada de cima" % CHAO)

    por_peca = {}
    for p in dados["pecas"]:
        por_peca.setdefault((p["fonte"], p["gg"]), p)

    tiles_novos, mapa_tile = {}, {}
    proximo = [TILE_LOCAL_0]

    def vaga(chave):
        """Vaga NOSSA para um tile da fonte, criada na primeira vez que aparece."""
        if chave not in mapa_tile:
            if chave not in dados["tiles"]:
                raise SystemExit("o kit em disco nao tem o tile %s" % chave)
            mapa_tile[chave] = proximo[0]
            tiles_novos[proximo[0]] = dados["tiles"][chave]
            proximo[0] += 1
        return mapa_tile[chave]

    def traduz(fonte, v, quadrante=None):
        """Entrada da fonte -> entrada nossa: mesmo tile, vaga nova, paleta nova.

        `quadrante` so vem preenchido para as quatro entradas da camada de
        BAIXO. Ali valem duas trocas, e as duas existem pelo mesmo motivo: a
        neve do fundo tem que ser a NOSSA.

          - tile 0 e transparente nas duas camadas (`render_maps.desenhar_tile`
            pula a cor 0), entao no fundo ele mostra o BACKDROP do BG, que aqui
            e azul-escuro. Trocando pela entrada do nosso 513, a peca importada
            pousa na nossa neve em vez de num buraco.
          - o tile de neve lisa DA FONTE e branco puro e a nossa neve e azulada
            com salpico: deixar o da fonte desenha um retangulo mais claro em
            volta da peca importada.
        """
        npri = dados["fontes"][fonte]["n_tiles_pri"]
        neve = set(dados["neve_da_fonte"].get(fonte) or [])
        pals = FONTES[fonte]["pals"]
        idx, ip = v & 0x3FF, (v >> 12) & 0xF
        if quadrante is not None and (idx == 0 or (idx >= npri
                                                   and (idx - npri) in neve)):
            return chao_ents[quadrante]
        if idx == 0:
            return 0
        if ip not in pals:
            if quadrante is not None:
                return chao_ents[quadrante]
            raise SystemExit("%s: entrada com paleta %d, fora do kit"
                             % (fonte, ip))
        lado, li = ("p", idx) if idx < npri else ("s", idx - npri)
        return ((v & 0x0C00) | (512 + vaga("%s:%s:%d" % (fonte, lado, li)))
                | (pals[ip] << 12))

    metas, attrs = {}, {}
    carimbos = {"arvores": [], "moveis": [], "torres": []}
    proximo_meta = [META_LOCAL_0]

    def poe(ents, attr):
        local = proximo_meta[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo_meta[0] += 1
        return 512 + local

    def importa(fonte, gg, papel, espelha=False):
        """As oito entradas do metatile `gg` da fonte, ja traduzidas.

        O espelho e aplicado ANTES da traducao, nas entradas CRUAS. Se fosse
        depois, ele viraria tambem a neve NOSSA que entra no lugar da neve da
        fonte (e a nossa neve e um desenho de 2x2 tiles em que cada quadrante
        tem o seu). Quando `_baixo_e_chao` diz que a camada de baixo e so chao
        da fonte, ela sai inteira e no lugar entra a do nosso 513.
        """
        ents = por_peca[(fonte, gg)]["ents"]
        if espelha:
            ents = _espelha4(ents[:4]) + _espelha4(ents[4:])
        baixo = (list(chao_ents[:4]) if _baixo_e_chao(papel, ents)
                 else [traduz(fonte, v, q) for q, v in enumerate(ents[:4])])
        return baixo + [traduz(fonte, v) for v in ents[4:]]

    # 1. ARVORE: metatile inteiro do hack, atributo da NOSSA arvore da posicao.
    for arv in ARVORES:
        ids = []
        for pos, (gg, esp) in enumerate(arv["gg"]):
            nosso = NOSSA_ARVORE[pos]
            a = struct.unpack_from("<H", attr_snow, (nosso - 512) * 2)[0]
            ids.append(poe(importa("gg", gg, "arvore", bool(esp)), a))
        carimbos["arvores"].append(dict(nome=arv["nome"], ids=ids))

    # 2. MOVEL DE CHAO IMPORTADO: camada de baixo do NOSSO 513, de cima do hack.
    for m in MOVEIS_GG:
        p = por_peca[("gg", m["gg"])]
        ents = _espelha4(p["ents"][4:]) if m["espelha"] else p["ents"][4:]
        cima = [traduz("gg", v) for v in ents]
        if all(x == 0 for x in cima):
            raise SystemExit("%s: o metatile %d do hack nao desenha nada em cima"
                             % (m["nome"], m["gg"]))
        # comportamento ZERADO de proposito: comportamento e id semantico e a
        # regra 7 do PRD proibe importar id do hack, so arte. O layerType e o do
        # hack (COVERED), que e o que poe o jogador NA FRENTE do arbusto.
        gid = poe(list(chao_ents[:4]) + cima, p["attr"] & 0xF000)
        carimbos["moveis"].append(dict(nome=m["nome"], mt=gid, onde="beira",
                                       quantos=12, espaco=5, importado=True))

    # 3. TORRE (boneco e poste): a de cima ANDAVEL com o atributo do 513, a de
    #    baixo SOLIDA com layerType COVERED e comportamento zerado.
    for t in TORRES:
        topo = poe(importa(t["fonte"], t["topo"], "topo"), attr_chao)
        base = poe(importa(t["fonte"], t["base"], "base"), 0x1000)
        carimbos["torres"].append(dict(nome=t["nome"], topo=topo, base=base,
                                       onde=t["onde"], quantos=t["quantos"],
                                       espaco=t["espaco"]))

    # 4. MOVEL NOSSO: em regra nada de novo no tileset, so o direito de usar.
    #    A excecao e o metatile cujo COMPORTAMENTO nao e MB_NORMAL nem o da
    #    propria neve. O 516 (a pedra com touca de neve) esta gravado como 0x02,
    #    MB_TALL_GRASS, e nenhum mapa o usava, entao ninguem tinha notado; usa-lo
    #    como esta planta grama alta numa cidade de neve e o `mapas_qa.py` acusa
    #    D1. Trocar o atributo do 516 esta PROIBIDO (metatile vivo de tileset
    #    compartilhado por seis layouts), entao entra uma COPIA dele em vaga
    #    livre, com os mesmos oito tiles byte a byte e o comportamento zerado.
    for m in MOVEIS_NOSSOS:
        local = m["mt"] - 512
        ents = _entradas(meta_snow, local)
        if len(set(ents)) == 1 and ents[0] <= 2:
            raise SystemExit("o metatile %d esta vazio no disco" % m["mt"])
        a = struct.unpack_from("<H", attr_snow, local * 2)[0]
        estranho = (a & 0xFF) not in (0x00, attr_chao & 0xFF)
        mt = poe(list(ents), a & 0xF000) if estranho else m["mt"]
        carimbos["moveis"].append(dict(nome=m["nome"], mt=mt, onde=m["onde"],
                                       quantos=m["quantos"], espaco=m["espaco"],
                                       importado=False, copia_de=m["mt"]))

    if proximo[0] > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo[0]))
    if proximo_meta[0] > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)

    # A vaga de metatile so serve se for ENCHIMENTO do dumper (as oito entradas
    # iguais e baixas) ou se ja tiver exatamente o que este kit escreve (rodar
    # duas vezes), e NENHUM dos cinco mapas do tileset pode usar o id.
    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    usados = set()
    for nome in IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    for local, ents in metas.items():
        gid = 512 + local
        antigo = _entradas(meta_snow, local)
        if not enchimento(antigo) and antigo != ents:
            raise SystemExit("vaga de metatile %d ja esta ocupada por outra coisa"
                             % gid)
        if gid in usados and enchimento(antigo):
            raise SystemExit("algum dos cinco mapas usa o metatile %d e a vaga "
                             "esta vazia" % gid)

    # A vaga de paleta tem que estar livre em TODO metatile que nao seja do kit.
    for local in range(len(meta_snow) // 16):
        if local in metas:
            continue
        for v in _entradas(meta_snow, local):
            if (v & 0x3FF) and ((v >> 12) & 0xF) == PAL_NOVA:
                raise SystemExit("a paleta %d ja e usada pelo metatile %d"
                                 % (PAL_NOVA, 512 + local))
    return tiles_novos, metas, attrs, carimbos


def grava_tileset(tiles_novos, metas, attrs):
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

    cores = dados["paleta"][str(PAL_NOVA)]
    with open(f"{DESTINO}/palettes/%02d.pal" % PAL_NOVA, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))

    meta = bytearray(open(f"{DESTINO}/metatiles.bin", "rb").read())
    attr = bytearray(open(f"{DESTINO}/metatile_attributes.bin", "rb").read())
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------------------- a trilha
def esqueleto(v, W, H, d, elegivel):
    """Caminho de custo minimo ligando as portas do mapa, em ordem de leitura.

    O custo nao e so distancia. Andar colado num solido custa mais, para a
    trilha sair pelo MEIO do corredor e nao raspando o bosque; virar custa mais,
    para ela sair reta como caminho batido de verdade; e celula que nao pode
    receber mancha custa muito mais, mas nao e proibida, senao o caminho nao
    atravessa a soleira das portas nem os pedacos de chao que nao sao neve lisa
    nossa.
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
        """Dijkstra com estado (celula, direcao), para poder cobrar a curva."""
        alvo = set(fim)
        dist = {}
        fila = [(0.0, ini[0], ini[1], 0, 0)]
        pai = {}
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
                if not (0 <= nx < W and 0 <= ny < H):
                    continue
                if not andavel(ny * W + nx):
                    continue
                # A CURVA E CARA de proposito: com pouca multa o caminho de
                # custo minimo desce em escada e a trilha dilatada sai com dente
                # de serra. Com multa alta ele anda reto ate o corredor acabar.
                curva = 9.0 if (dx0, dy0) != (0, 0) and (dx, dy) != (dx0, dy0) else 0.0
                no = (nx, ny, dx, dy)
                if no in dist:
                    continue
                pai[no] = (x, y, dx0, dy0)
                heapq.heappush(fila, (g + custo(nx, ny) + curva, nx, ny, dx, dy))
        return []

    # As soleiras: a celula andavel logo abaixo de cada porta, que e onde o
    # jogador pousa. Mais a entrada norte do mapa e as duas pontas do porto.
    portas = []
    for w in (d.get("warp_events") or []):
        x, y = w["x"], w["y"]
        for dx, dy in ((0, 1), (0, 0), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and andavel(ny * W + nx):
                portas.append((nx, ny))
                break
    chao = sorted(p for p in elegivel)
    if chao:
        ymin, ymax = min(y for _, y in chao), max(y for _, y in chao)
        for alvo_y, quantos in ((ymin, 1), (ymax, 2)):
            faixa = [p for p in chao if abs(p[1] - alvo_y) <= 1]
            if not faixa:
                continue
            xs = sorted({p[0] for p in faixa})
            escolhas = [xs[len(xs) // 4], xs[3 * len(xs) // 4]][:quantos] \
                if quantos > 1 else [min(xs, key=lambda x: abs(x - W // 2))]
            for xe in escolhas:
                portas.append(min((p for p in faixa if p[0] == xe),
                                  key=lambda p: abs(p[1] - alvo_y)))
    # LIGACAO EM ARVORE, nao em fila: ligar porta 0 a 1, 1 a 2 e assim por
    # diante daria um zigue-zague que atravessa a cidade inteira toda vez. Aqui
    # cada porta nova se liga a QUALQUER ponto ja ligado, que e o caminho mais
    # curto que serve, e o resultado e uma rede com cruzamento.
    ossos = set([portas[0]])
    for p in portas[1:]:
        trecho = caminho(p, ossos)
        if not trecho:
            continue
        ossos |= set(trecho)
    return ossos, portas


def area_trilha(v, W, H, d, elegivel):
    """As celulas de TRILHA: o esqueleto engordado para tres de largura.

    A versao com calcada abria a rua para cinco celulas onde sobrava espaco e
    punha uma praca 5x3 em cada soleira, porque calcada de pedra e desenho de
    cidade e cidade tem largo. Neve batida nao: ela e marca de pisada, e marca
    de pisada nao tem praca. Ficou so a dilatacao de Chebyshev 1, mais a limpeza
    de faixa de uma celula, que aqui existe por leitura de arte e nao por falta
    de peca: risco de uma celula de largura no meio da neve nao le como caminho,
    le como sujeira.
    """
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
    while True:
        fora = {(x, y) for x, y in pav
                if not ((x, y - 1) in pav or (x, y + 1) in pav)
                or not ((x - 1, y) in pav or (x + 1, y) in pav)}
        if not fora:
            break
        pav -= fora
    return pav, portas


# ---------------------------------------------------------------- as manchas
def bolhas(livres, W, H, perto_solido):
    """[(grupo, {celulas})], bolhas organicas crescidas por frente de onda.

    A SEMENTE nao e sorteio solto: as celulas livres sao ordenadas por um hash
    da posicao e a semente so e aceita se estiver a pelo menos 4 (Chebyshev) de
    toda semente ja aceita, o que espalha as bolhas pelo mapa em vez de deixa-las
    grudadas. A bolha do grupo `banco` so semeia ENCOSTADA no solido, porque a
    peca dela tem borda dura de um lado e sozinha no meio do campo nao fecha.

    O CRESCIMENTO e guloso com ruido: a cada passo entra a celula da frente de
    onda com o menor hash. Circulo daria bolha redonda e xadrez daria sal e
    pimenta; frente de onda com ruido da contorno irregular, que e o que neve
    de verdade faz.
    """
    ordem = sorted(livres, key=lambda p: _mistura(p[0], p[1], 0x5EED))
    tomadas, saida, sementes = set(), [], []
    for spec in BOLHAS:
        feitas = 0
        for p in ordem:
            if feitas >= spec["quantas"]:
                break
            if p in tomadas:
                continue
            if any(max(abs(p[0] - q[0]), abs(p[1] - q[1])) < 4 for q in sementes):
                continue
            if spec["grupo"] == "banco" and not perto_solido(p):
                continue
            lo, hi = spec["tam"]
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
                    r = (q[0] + dx, q[1] + dy)
                    if r in livres and r not in tomadas and r not in corpo:
                        frente.add(r)
            if len(corpo) < lo:
                continue
            tomadas |= corpo
            sementes.append(p)
            saida.append((spec["grupo"], corpo))
            feitas += 1
    return saida


def desgasta_trilha(trilha):
    """A trilha que vai receber tinta: miolo inteiro e parte da borda.

    Miolo e a celula com as quatro vizinhas de N4 tambem na trilha. A borda
    passa por um hash da posicao, e o corte e o `BORDA_TRILHA`. Nao ha estado
    nem ordem aqui: a mesma celula da a mesma resposta em qualquer maquina.
    """
    return {p for p in trilha
            if all((p[0] + dx, p[1] + dy) in trilha for dx, dy in N4)
            or _mistura(p[0], p[1], 0x7A17) % 100 < BORDA_TRILHA}


def peca_da_mancha(grupo, x, y):
    """Qual das pecas do grupo cai nesta celula.

    Hash da posicao, nao paridade: paridade vira xadrez e o auto-teste reprova
    (caso 11). O hash tambem nao tem periodo, porque nao e funcao de x nem de y
    sozinhos.
    """
    lista = GRUPOS_MANCHA[grupo]
    return lista[_mistura(x, y, 0xA5A5 + len(lista)) % len(lista)]


# ---------------------------------------------------------------- plano do mapa
def plano_mapa(carimbos, base=None):
    """(L, W, H, v, escritas, contas)."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    elev_chao = collections.Counter(
        (c >> 12) & 0xF for c in v
        if (c & 0x3FF) == CHAO and not ((c >> 10) & 3)).most_common(1)[0][0]

    nossa_neve = {CHAO} | set(KIT1)

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    elegivel = {(i % W, i // W) for i in range(W * H)
                if andavel(i) and (v[i] & 0x3FF) in nossa_neve
                and ((v[i] >> 12) & 0xF) == elev_chao
                and beh(v[i] & 0x3FF) not in AG}

    escritas = {}

    # ------------------------------------------------------- 1. a trilha (so
    #    calculada; quem a pinta e a etapa 4, e quem a usa como encosto e a 3)
    trilha, portas = area_trilha(v, W, H, d, elegivel)

    # ------------------------------------------------------------- 2. arvores
    def mt(x, y):
        return v[y * W + x] & 0x3FF if 0 <= x < W and 0 <= y < H else -1

    blocos = [(x, y) for y in range(H - 1) for x in range(W - 1)
              if [mt(x, y), mt(x + 1, y), mt(x, y + 1), mt(x + 1, y + 1)]
              == NOSSA_ARVORE]
    # rodizio sobre a lista EMBARALHADA por posicao: nao e xadrez e nao tem
    # periodo, e mesmo assim a conta de cada variante fica equilibrada.
    ordem = sorted(blocos, key=lambda p: (((p[0] * 2654435761) ^ (p[1] * 40503))
                                          * 2246822519) & 0xFFFFFFFF)
    conta_arv = collections.Counter()
    # 3 em cada 7 continuam a nossa arvore: variedade nao e trocar tudo.
    roda = [None, ARVORES[0]["nome"], None, ARVORES[1]["nome"], None,
            ARVORES[0]["nome"], ARVORES[1]["nome"]]
    por_nome = {a["nome"]: a for a in carimbos["arvores"]}
    for k, (x, y) in enumerate(ordem):
        nome = roda[k % len(roda)]
        if nome is None:
            conta_arv["a nossa"] += 1
            continue
        ids = por_nome[nome]["ids"]
        for pos, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
            j = (y + dy) * W + x + dx
            escritas[j] = (v[j] & 0xFC00) | ids[pos]
        conta_arv[nome] += 1

    # -------------------------------------------------------------- 3. moveis
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    # O que o `enfeita_cidades.py` desenhou nesta cidade fica de fora, mas SO a
    # celula: aqui nao vale a orla de 1 que o `neve_snowpoint.py` usa, porque
    # aquilo era para dois carimbos de CHAO nao se encostarem, e movel encostado
    # em enfeite e cidade cheia, nao cidade errada.
    for idx, _a, _n in E.carrega_plano().get(ALVO, {}).get("celulas", []):
        gelo.add((idx % W, idx // W))

    aplicado = list(v)
    for i, val in escritas.items():
        aplicado[i] = val
    ini = E.partidas(d, W, H, v)
    antes = E.alcance(v, W, H, ini)
    novos_solidos, postos = [], []
    conta_mov = collections.Counter()
    por_movel = collections.defaultdict(list)

    def solido(x, y):
        return 0 <= x < W and 0 <= y < H and ((aplicado[y * W + x] >> 10) & 3)

    def nao_liga(grade, x, y):
        """Os vizinhos andaveis de (x,y) ainda se falam sem passar por (x,y)?

        E o teste de ponto de articulacao, e ele existe porque o portao de
        alcance sozinho nao pega corredor com warp dos dois lados (ver
        `componentes`). A busca comeca no primeiro vizinho andavel e tem que
        chegar em todos os outros.
        """
        viz = [(x + dx, y + dy) for dx, dy in N4
               if 0 <= x + dx < W and 0 <= y + dy < H
               and not ((grade[(y + dy) * W + x + dx] >> 10) & 3)]
        if len(viz) < 2:
            return False
        vistos = {viz[0]}
        fila = [viz[0]]
        falta = set(viz[1:])
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

    def livre(x, y, so_chao):
        """A celula esta liberada para receber peca desta passada?"""
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas or (x, y) not in elegivel:
            return False
        if (x, y) in trilha:
            return False
        # Vale a neve lisa (513) e tambem as onze pecas planas da primeira
        # passada (680 a 690): as tres coisas tem o mesmo atributo 0x0021 e o
        # mesmo papel de chao, e boa parte das celulas de BEIRA da cidade e da
        # primeira passada, que foi justamente atras de encosto de solido.
        if (aplicado[i] & 0x3FF) not in nossa_neve:
            return False
        if so_chao and (aplicado[i] & 0x3FF) != CHAO:
            return False
        return True

    def encosto_ok(onde, x, y):
        if onde == "beira":
            return any(solido(x + dx, y + dy) for dx, dy in N4)
        return any((x + dx, y + dy) in trilha for dx, dy in N4)

    def espacado(m, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
               for px, py in postos):
            return False
        return not any(max(abs(x - px), abs(y - py)) < m["espaco"]
                       for px, py in por_movel[m["nome"]])

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os dois portoes deixarem.

        O portao roda NA HORA e nao so no fim: se solidificar esta celula tirar
        do alcance a pe qualquer OUTRA celula, ou partir um pedaco de chao em
        dois, a escrita e desfeita e o gerador segue, como faz o
        `enfeita_cidades.py`.
        """
        i = y * W + x
        antigo = aplicado[i]
        # elevacao PRESERVADA (bits 12 a 15), colisao ligada, metatile novo.
        aplicado[i] = (antigo & 0xF000) | (1 << 10) | mt_id
        perdidas = (antes - E.alcance(aplicado, W, H, ini)) \
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

    # 3a. TORRES (boneco de neve e poste), primeiro, porque elas precisam de um
    #     PAR vertical de celulas boas e a mobilia de uma celula so nao pode ter
    #     comido o par antes. A de cima continua andavel: e por isso que ela nao
    #     entra em `novos_solidos` nem passa pelo portao de alcance.
    conta_torre = collections.Counter()
    por_torre = collections.defaultdict(list)
    for t in carimbos["torres"]:
        for x, y in ordem_cel:
            if conta_torre[t["nome"]] >= t["quantos"]:
                break
            if not livre(x, y, True) or not livre(x, y - 1, False):
                continue
            if not encosto_ok(t["onde"], x, y):
                continue
            if not espacado(t, x, y):
                continue
            # nenhuma torre encosta em outra torre, nem da mesma nem de outro
            # tipo: duas torres coladas viram uma parede, nao dois enfeites.
            if any(max(abs(x - px), abs(y - py)) < 3
                   for lista in por_torre.values() for px, py in lista):
                continue
            j = (y - 1) * W + x
            escritas[j] = (v[j] & 0xFC00) | t["topo"]
            aplicado[j] = escritas[j]
            if not tenta_solidificar(x, y, t["base"]):
                del escritas[j]
                aplicado[j] = v[j]
                continue
            por_torre[t["nome"]].append((x, y))
            por_movel[t["nome"]].append((x, y))
            conta_torre[t["nome"]] += 1

    # 3b. MOBILIA de uma celula. DUAS VARREDURAS, e a ordem tem consequencia
    #     medida. Na primeira o movel so entra em neve lisa 513, que e o carimbo
    #     que este trabalho existe para quebrar; na segunda ele aceita tambem as
    #     pecas planas da primeira passada. Com uma varredura so, o movel comia
    #     peca da primeira passada antes de comer carimbo e a regua PIORAVA: o
    #     denominador caia e o numerador nao.
    lista = carimbos["moveis"]
    for so_chao in (True, False):
        for x, y in ordem_cel:
            if sum(conta_mov.values()) >= TETO_MOVEIS:
                break
            giro = ((x * 73856093) ^ (y * 19349663)) % len(lista)
            for k in range(len(lista)):
                m = lista[(giro + k) % len(lista)]
                if conta_mov[m["nome"]] >= m["quantos"]:
                    continue
                if not livre(x, y, so_chao) or not encosto_ok(m["onde"], x, y):
                    continue
                if not espacado(m, x, y):
                    continue
                if not tenta_solidificar(x, y, m["mt"]):
                    continue
                por_movel[m["nome"]].append((x, y))
                conta_mov[m["nome"]] += 1
                break

    # -------------------------------------------------------------- 4. manchas
    # A trilha vira NEVE BATIDA e as bolhas caem no que sobrou. Mancha so pisa
    # em neve lisa 513: as pecas da primeira passada ficam onde estao, porque
    # elas ja foram postas com encosto e regravar por cima trocaria arte boa por
    # arte sorteada, e porque trocar 680..690 por 680..690 nao mexe na regua.
    def perto_solido(p):
        return any(solido(p[0] + dx, p[1] + dy) for dx, dy in N4)

    conta_mancha = collections.Counter()

    def pinta(p, grupo):
        i = p[1] * W + p[0]
        escritas[i] = (aplicado[i] & 0xFC00) | peca_da_mancha(grupo, p[0], p[1])
        aplicado[i] = escritas[i]
        conta_mancha[grupo] += 1

    def pintavel(p):
        i = p[1] * W + p[0]
        return (p in elegivel and i not in escritas
                and (aplicado[i] & 0x3FF) == CHAO)

    for p in sorted(x for x in desgasta_trilha(trilha) if pintavel(x)):
        pinta(p, "batida")
    livres = {p for p in elegivel if pintavel(p)}
    for grupo, corpo in bolhas(livres, W, H, perto_solido):
        for p in sorted(corpo):
            pinta(p, grupo)

    # ------------------------------------------------------------- os portoes
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (ALVO, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel"
                             % (ALVO, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (ALVO, "; ".join(queixas)))
    contas = dict(trilha=len(trilha), arvores=dict(conta_arv),
                  moveis=dict(conta_mov), torres=dict(conta_torre),
                  manchas=dict(conta_mancha), solidos=len(novos_solidos),
                  portas=portas)
    return L, W, H, v, escritas, contas


# ----------------------------------------------------------- ligacao a pe
def componentes(v, W, H):
    """{celula: rotulo} dos pedacos de chao andavel ligados a pe.

    POR QUE NAO BASTA O `enfeita_cidades.alcance`. Aquele mede "quem ainda e
    alcancavel a partir de algum ponto de partida", e ponto de partida ali e
    warp OU objeto. Snowpoint tem warp dos DOIS lados do corredor de duas
    celulas da linha 14 (as casas do norte de um lado, a cidade do outro):
    fechar o corredor inteiro nao tira NENHUMA celula do alcance, porque cada
    metade continua alcancavel a partir do proprio warp, e mesmo assim o
    jogador que entra pela cidade nao chega mais nas casas. Medido em
    07/09/2026, com uma sabotagem que o portao antigo deixou passar VERDE.
    Este aqui olha a LIGACAO entre as celulas, que e o que o jogador sente.
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
    """Nenhum pedaco de chao se PARTIU, e nenhum se juntou a outro.

    Devolve a lista de queixas, vazia quando esta tudo bem.
    """
    mau = []
    por_rotulo = collections.defaultdict(set)
    for p, r in antes.items():
        if p not in solidificadas:
            por_rotulo[r].add(p)
    for r, cels in por_rotulo.items():
        vistos = {depois.get(p) for p in cels}
        if len(vistos) > 1:
            mau.append("o pedaco %d de chao se partiu em %d" % (r, len(vistos)))
    juntou = collections.defaultdict(set)
    for p, r in depois.items():
        if p in antes:
            juntou[r].add(antes[p])
    for r, origens in juntou.items():
        if len(origens) > 1:
            mau.append("dois pedacos de chao que eram separados se juntaram")
    return mau


# ------------------------------------------------------------------ regua
def regua(v, W, H, L, escritas=None):
    """(carimbo dominante, celulas andaveis a pe, id do carimbo) como a regua."""
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    cel = list(v)
    for i, val in (escritas or {}).items():
        cel[i] = val
    and_ = [c & 0x3FF for c in cel
            if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG]
    top = collections.Counter(and_).most_common(1)[0]
    return 100.0 * top[1] / len(and_), len(and_), top[0]


# ---------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(guardado):
    """A grade como esta no disco, so tirando o que ESTA passada escreveu."""
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    print("kit 2: %d tiles novos (vagas %d a %d de %d, sobram %d), %d metatiles "
          "novos (locais %d a %d, ids %d a %d), paleta %d com %d cores nao-zero"
          % (len(tiles_novos), TILE_LOCAL_0, TILE_LOCAL_0 + len(tiles_novos) - 1,
             TETO_TILES, TETO_TILES - TILE_LOCAL_0 - len(tiles_novos),
             len(metas), min(metas), max(metas), 512 + min(metas),
             512 + max(metas), PAL_NOVA, kit()["cores_usadas"]))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    base = base_de(guardado)
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base)
    print("trilha: %d celulas | arvores: %s"
          % (contas["trilha"],
             ", ".join("%s x%d" % kv for kv in sorted(contas["arvores"].items()))))
    print("  manchas: %d em %s"
          % (sum(contas["manchas"].values()),
             ", ".join("%s x%d" % kv for kv in sorted(contas["manchas"].items()))))
    print("  torres: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["torres"].items())))
    print("  moveis: " + ", ".join("%s x%d" % kv
                                   for kv in sorted(contas["moveis"].items())))
    print("  celulas solidificadas: %d" % contas["solidos"])
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("regua (chao andavel a pe): carimbo %d com %.1f%% de %d celulas ANTES; "
          "carimbo %d com %.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
    print("celulas do mapa mudadas: %d" % len(escritas))
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
    return escritas


def desfaz():
    guardado = carrega_plano()
    if ALVO not in guardado:
        print("nada a desfazer")
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
    print("desfeitas %d celulas" % n)
    return 0


# ------------------------------------------------------------------ auto-teste
def demo():
    mau = []
    dados = kit()
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    meta_snow = open(f"{DESTINO}/metatiles.bin", "rb").read()
    attr_snow = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()
    attr_chao = struct.unpack_from("<H", attr_snow, (CHAO - 512) * 2)[0]
    chao_ents = _entradas(meta_snow, CHAO - 512)
    ids_arvore = {i for a in carimbos["arvores"] for i in a["ids"]}
    ids_movel_novo = {m["mt"] for m in carimbos["moveis"] if m["importado"]}
    ids_topo = {t["topo"] for t in carimbos["torres"]}
    ids_base = {t["base"] for t in carimbos["torres"]}
    ids_mancha = {i for lst in GRUPOS_MANCHA.values() for i in lst}

    # 1. orcamento de tile, metatile e paleta
    if TILE_LOCAL_0 + len(tiles_novos) > TETO_TILES:
        mau.append("estoura o teto de tiles")
    if max(metas) >= TETO_META:
        mau.append("estoura o teto de metatiles")
    if not 6 <= PAL_NOVA <= 12:
        mau.append("paleta %d nao e vaga de secundario" % PAL_NOVA)
    cores = dados["paleta"][str(PAL_NOVA)]
    nz = [c for c in cores[1:] if c != [0, 0, 0]]
    if len(nz) > 15:
        mau.append("a vaga %d tem %d cores nao-zero" % (PAL_NOVA, len(nz)))
    if len({tuple(c) for c in nz}) != len(nz):
        mau.append("a vaga %d gasta duas vagas com a MESMA cor" % PAL_NOVA)

    # 2. A CALCADA NAO ENTRA (decisao 56 do Gui). O teste e por construcao e nao
    #    por nome: nenhuma peca do kit pode vir da paleta 11 do Golden Glazed,
    #    que era a da calcada, e nenhum metatile novo pode ser ANDAVEL sem ser
    #    topo de torre.
    for ch, ip in dados["tiles_paleta"].items():
        if ch.startswith("gg:") and ip == 11:
            mau.append("o tile %s vem da paleta 11 do Golden Glazed, que era a "
                       "da calcada" % ch)
    for local, a in attrs.items():
        gid = 512 + local
        if a == attr_chao and gid not in ids_topo:
            mau.append("o metatile %d e andavel com o atributo do chao e nao e "
                       "topo de torre" % gid)

    # 3. a arvore herda o atributo da NOSSA arvore da posicao
    for a in carimbos["arvores"]:
        for pos, gid in enumerate(a["ids"]):
            esperado = struct.unpack_from("<H", attr_snow,
                                          (NOSSA_ARVORE[pos] - 512) * 2)[0]
            if attrs[gid - 512] != esperado:
                mau.append("%s: metatile %d com atributo 0x%04X, esperado 0x%04X"
                           % (a["nome"], gid, attrs[gid - 512], esperado))

    # 4. o movel importado pisa na NOSSA neve e nao importa comportamento
    for gid in ids_movel_novo | ids_topo:
        ent = metas[gid - 512]
        if ent[:4] != chao_ents[:4]:
            mau.append("metatile %d nao tem a neve de Snowpoint embaixo" % gid)
    for gid in ids_movel_novo | ids_topo | ids_base:
        if attrs[gid - 512] & 0xFF and attrs[gid - 512] != attr_chao:
            mau.append("metatile %d importou comportamento 0x%02X da fonte"
                       % (gid, attrs[gid - 512] & 0xFF))

    # 5. O TOPO DE TORRE E ANDAVEL E NAO PODE TAPAR O JOGADOR. A conta e a do E3
    #    do `mapas_qa.py` (camada de cima 100% opaca em metatile NORMAL ou
    #    SPLIT), feita nos pixels de verdade e nao no desenho de memoria, mas
    #    ela e MAIS DURA que a de la de proposito, e a diferenca esta medida:
    #    o E3 perdoa camada de cima opaca quando a de baixo desenha um chao
    #    DIFERENTE, porque isso e passagem por baixo de ponte ou de copa. Aqui a
    #    camada de baixo e sempre a nossa neve, entao o topo de torre se
    #    encaixaria na excecao e o E3 passaria verde: medido em 07/09/2026, com
    #    uma sabotagem que encheu a camada de cima do topo com tile opaco e
    #    deixou o `mapas_qa.py` acusando ZERO em SnowpointCity. Cabeca de boneco
    #    nao e ponte, e quem anda atras dela tem que continuar aparecendo.
    for gid in ids_topo:
        ent = metas[gid - 512]
        if (attrs[gid - 512] >> 12) & 0xF == 1:
            continue                        # COVERED nunca tapa
        px = 0
        for e in ent[4:]:
            if e & 0x3FF:
                vaga = (e & 0x3FF) - 512
                px += _opacos(tiles_novos[vaga]) if vaga in tiles_novos else 64
        if px >= 4 * 64:
            mau.append("o topo %d tapa o jogador inteiro (E3)" % gid)

    # 6. a base de torre e SOLIDA e por isso nao entra em regra de celula
    #    andavel; o que ela nao pode e ficar com layerType NORMAL, senao a arte
    #    dela desenha por cima do jogador parado ao sul.
    for gid in ids_base:
        if (attrs[gid - 512] >> 12) & 0xF != 1:
            mau.append("a base %d nao esta em COVERED" % gid)

    # 7. paleta: so a 6 (a da primeira passada), a 10 (a que este kit traz) e as
    #    que o NOSSO metatile 513 ja usava, que sao as que entram junto com a
    #    neve nossa substituida na camada de baixo.
    pals_ok = {PAL_MATA, PAL_NOVA} | {(x >> 12) & 0xF for x in chao_ents if x & 0x3FF}
    for local, ent in metas.items():
        for x in ent:
            if (x & 0x3FF) and ((x >> 12) & 0xF) not in pals_ok:
                mau.append("metatile %d aponta para a paleta %d, que nao e do kit"
                           % (512 + local, (x >> 12) & 0xF))

    # 8. o plano do mapa, celula por celula
    guardado = carrega_plano()
    base = base_de(guardado)
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base)
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val

    for i, val in escritas.items():
        x, y = i % W, i // W
        mt_novo, mt_velho = val & 0x3FF, v[i] & 0x3FF
        col_novo, col_velho = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("mudou ELEVACAO em (%d,%d)" % (x, y))
        if col_velho and not col_novo:
            mau.append("colisao 1 -> 0 em (%d,%d), que segue proibida" % (x, y))
        if mt_novo in ids_mancha:
            if col_novo != col_velho or mt_velho != CHAO:
                mau.append("mancha em celula errada em (%d,%d)" % (x, y))
        elif mt_novo in ids_topo:
            if col_novo != col_velho or mt_velho not in ({CHAO} | set(KIT1)):
                mau.append("topo de torre em celula errada em (%d,%d)" % (x, y))
        elif mt_novo in ids_arvore:
            if not col_velho or not col_novo:
                mau.append("arvore trocada em celula nao solida em (%d,%d)" % (x, y))
        else:
            if col_velho or not col_novo:
                mau.append("movel em (%d,%d) nao e solidificacao 0 -> 1" % (x, y))
            if mt_velho not in ({CHAO} | set(KIT1)):
                mau.append("movel fora da nossa neve lisa em (%d,%d)" % (x, y))
            if (x, y) in ev:
                mau.append("movel em cima do evento (%d,%d)" % (x, y))

    # 9. (comportamento, layerType) de toda celula ANDAVEL fica igual
    ap = G._attrs(L["primary_tileset"])
    asec = G._attrs(L["secondary_tileset"])

    def atributo(mt_id):
        """Atributo de um metatile, com o kit desta rodada valendo por cima.

        O kit pode ainda nao estar no disco (primeira rodada antes do
        `--aplicar`), e nesse caso o valor certo e o que o `desenha_kit` acabou
        de montar, nao o enchimento do dumper que esta no arquivo.
        """
        if mt_id >= 512:
            local = mt_id - 512
            if local in attrs:
                return attrs[local]
            return asec[local] if local < len(asec) else 0
        return ap[mt_id] if mt_id < len(ap) else 0

    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("celula andavel (%d,%d) mudou (comportamento, layerType)"
                       % (i % W, i // W))
            break

    # 10. alcance a pe: perde SO as celulas que viraram solidas, e ganha nenhuma
    ini = E.partidas(d, W, H, v)
    antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
    solidificadas = {(i % W, i // W) for i in escritas
                     if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
    # A igualdade nao e "o mesmo conjunto": movel novo TIRA do alcance a celula
    # que ele ocupa, e e isso que a lei nova de 07/09/2026 permite. O que nao
    # pode e perder QUALQUER OUTRA celula, nem ganhar nenhuma. (Parte das
    # celulas solidificadas ja nao estava no alcance porque e bolsao fechado
    # dentro do bosque, entao a inclusao e num sentido so.)
    if (antes - depois) - solidificadas:
        mau.append("o alcance a pe perdeu %d celulas alem das solidificadas: %s"
                   % (len((antes - depois) - solidificadas),
                      sorted((antes - depois) - solidificadas)[:6]))
    if depois - antes:
        mau.append("o alcance a pe GANHOU celula, e nenhuma peca abre passagem")
    # 10b. LIGACAO a pe: nenhum pedaco de chao se partiu nem se juntou a outro.
    #      Este e o caso que pega o corredor com warp dos dois lados, que o 10
    #      sozinho deixa passar verde (ver o comentario de `componentes`).
    mau += ligacao_intacta(componentes(v, W, H), componentes(saida, W, H),
                           solidificadas)

    # 11. A MANCHA NAO PODE SER ADIVINHAVEL, e o teste tem dois lados.
    #     (a) PADRAO: nenhuma projecao simples da posicao pode ADIVINHAR a peca.
    #         Medir so a PARIDADE nao basta e isso esta medido: uma sabotagem que
    #         trocou o hash por `(x + y) % len(lista)` passou VERDE numa regra de
    #         paridade, porque com seis pecas no grupo `batida` a paridade de x+y
    #         so estreita o palpite de seis para tres, ou seja 33%, abaixo de
    #         qualquer piso razoavel, e mesmo assim o mapa fica listrado na
    #         diagonal com periodo 6. A conta certa e por EIXO (x, y, x+y, x-y) e
    #         por MODULO de 2 a 8: dentro de cada classe de resto chuta-se a peca
    #         mais comum daquela classe, e o acerto e comparado com o de chutar a
    #         peca mais comum do mapa inteiro. Hash bom nao melhora o palpite;
    #         padrao periodico melhora muito. Medido em 07/09/2026: chute cego
    #         14,4%, melhor projecao 19,9% (ganho de 5,6 pontos), e a sabotagem
    #         de `(x + y) % 6` da ganho de 85,6. O corte de 12 pontos fica no
    #         meio, com folga de duas vezes para os dois lados.
    #     (b) FORMA: mancha tem que ser BOLHA, nao sal e pimenta. A conta e o
    #         TAMANHO MEDIO do pedaco conexo (N4), e nao "quantas vizinhas cada
    #         celula tem", porque a segunda nao sabe reprovar: espalhar metade
    #         das celulas da trilha ao acaso ainda deixa 76% delas com duas
    #         vizinhas, contra 84,5% do desenho de verdade, e passa. O tamanho
    #         medio do pedaco separa: 17,05 celulas por pedaco no desenho de
    #         verdade (341 celulas em 20 pedacos) contra 8,32 na versao
    #         espalhada (308 em 37). O corte fica em 12.
    mancha_em = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
                 if (val & 0x3FF) in ids_mancha}
    if len(mancha_em) < 200:
        mau.append("so %d celulas de mancha, e a regua nao fecha com menos"
                   % len(mancha_em))
    if mancha_em:
        tot = len(mancha_em)
        cego = collections.Counter(mancha_em.values()).most_common(1)[0][1] / tot
        for rotulo, eixo in (("x", lambda p: p[0]), ("y", lambda p: p[1]),
                             ("x+y", lambda p: p[0] + p[1]),
                             ("x-y", lambda p: p[0] - p[1])):
            for mod in range(2, 9):
                tabela = collections.defaultdict(collections.Counter)
                for p, mt_id in mancha_em.items():
                    tabela[eixo(p) % mod][mt_id] += 1
                ac = sum(c.most_common(1)[0][1] for c in tabela.values()) / tot
                if ac - cego > 0.12:
                    mau.append("saber %s mod %d adivinha a peca de mancha em "
                               "%.0f%% das celulas contra %.0f%% do chute cego: "
                               "virou padrao" % (rotulo, mod, 100 * ac, 100 * cego))
    if mancha_em:
        vistos_m, pedacos = set(), 0
        for p in sorted(mancha_em):
            if p in vistos_m:
                continue
            pedacos += 1
            pilha = [p]
            vistos_m.add(p)
            while pilha:
                q = pilha.pop()
                for dx, dy in N4:
                    r = (q[0] + dx, q[1] + dy)
                    if r in mancha_em and r not in vistos_m:
                        vistos_m.add(r)
                        pilha.append(r)
        if len(mancha_em) / pedacos < 12.0:
            mau.append("a mancha media tem so %.1f celulas (%d celulas em %d "
                       "pedacos): virou sal e pimenta, nao bolha"
                       % (len(mancha_em) / pedacos, len(mancha_em), pedacos))

    # 12. variedade de arvore: tres silhuetas e distribuicao SEM periodo
    trocadas = sum(n for k, n in contas["arvores"].items() if k != "a nossa")
    if len([k for k in contas["arvores"] if k != "a nossa"]) < 2:
        mau.append("menos de duas variantes de arvore entraram")
    if trocadas < 60:
        mau.append("so %d arvores trocadas" % trocadas)
    de_id = {i: a["nome"] for a in carimbos["arvores"] for i in a["ids"]}
    bloco_de = {}
    for i, val in escritas.items():
        nome = de_id.get(val & 0x3FF)
        if nome is None:
            continue
        x, y = i % W, i // W
        if (val & 0x3FF) == [a for a in carimbos["arvores"]
                             if a["nome"] == nome][0]["ids"][0]:
            bloco_de[(x, y)] = nome
    # E O CANTO DO BLOCO que interessa, nao a celula: cada bloco escreve quatro
    # celulas, duas de cada paridade, entao contar celula da sempre 50/50 e o
    # caso nunca reprova. E a conta certa nao e "os blocos estao numa paridade
    # so" (a mata e uma grade alinhada, isso e verdade sempre): e "saber a
    # paridade JA DIZ qual variante caiu ali".
    for rotulo, chave in (("(x+y)", lambda p: (p[0] + p[1]) % 2),
                          ("x", lambda p: (p[0] // 2) % 2),
                          ("y", lambda p: (p[1] // 2) % 2),
                          ("x+y do bloco", lambda p: (p[0] // 2 + p[1] // 2) % 2)):
        tabela = collections.defaultdict(collections.Counter)
        for p, nome in bloco_de.items():
            tabela[chave(p)][nome] += 1
        acertos = sum(c.most_common(1)[0][1] for c in tabela.values())
        total = sum(sum(c.values()) for c in tabela.values())
        if total and len(set(bloco_de.values())) > 1 and acertos / total > 0.8:
            mau.append("a paridade de %s adivinha a variante de arvore em %d de "
                       "%d blocos: virou xadrez" % (rotulo, acertos, total))

    # 13. as torres: quantas, e sempre com o topo LOGO ACIMA da base
    n_boneco = sum(n for k, n in contas["torres"].items() if "boneco" in k)
    if not 4 <= n_boneco <= 6:
        mau.append("%d bonecos de neve, e o Gui pediu de 4 a 6" % n_boneco)
    bases = {(i % W, i // W) for i, val in escritas.items()
             if (val & 0x3FF) in ids_base}
    topos = {(i % W, i // W) for i, val in escritas.items()
             if (val & 0x3FF) in ids_topo}
    if len(bases) != len(topos):
        mau.append("%d bases de torre e %d topos" % (len(bases), len(topos)))
    for x, y in bases:
        if (x, y - 1) not in topos:
            mau.append("a base de torre em (%d,%d) esta sem topo" % (x, y))
            break

    # 14. idempotente
    base2 = list(saida)
    for i in sorted(escritas):
        if base2[i] == escritas[i]:
            base2[i] = v[i]
    if base2 != list(v):
        mau.append("desfazer nao devolve a base")
    _, _, _, _, escritas2, _ = plano_mapa(carimbos, base2)
    if escritas2 != escritas:
        mau.append("segunda passada deu plano diferente")

    # 15. o trabalho tem que valer a pena: a regua precisa cair para 25% ou menos
    a, na, _ = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > TETO_REGUA:
        mau.append("a regua ainda marca %.1f%% de carimbo dominante" % b)

    # 16. O QUE ESTA NO DISCO e o que o kit manda. Sem este caso o auto-teste so
    #     confere o que ele mesmo acabou de calcular em memoria: foi a licao da
    #     quinta sabotagem de 44cb13b7b7, em que sabotar o atributo e um tile
    #     DIRETO NO DISCO deixava os casos anteriores verdes.
    from PIL import Image
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.convert("P").load()

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    postas = [l for l in metas if not enchimento(_entradas(meta_snow, l))]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; caso 16 nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ent in metas.items():
            if _entradas(meta_snow, local) != ent:
                mau.append("metatile %d no disco nao e o do kit" % (512 + local))
            if struct.unpack_from("<H", attr_snow, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            if (vaga // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga)
        pal = [l.split() for l in
               open(f"{DESTINO}/palettes/%02d.pal" % PAL_NOVA).read().split("\n")[3:]
               if l.strip()]
        if [[int(z) for z in c] for c in pal[:16]] != cores:
            mau.append("a paleta %d no disco nao e a do kit" % PAL_NOVA)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE: %d tiles, %d metatiles, %d cores na vaga %d, %d celulas "
          "de mancha, %d arvores trocadas, %d celulas solidas, %d bonecos, "
          "regua de %.1f%% para %.1f%%, 16 casos"
          % (len(tiles_novos), len(metas), len(nz), PAL_NOVA, len(mancha_em),
             trocadas, contas["solidos"], n_boneco, a, b))
    return 0


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--desfazer" in sys.argv:
        return desfaz()
    roda("--aplicar" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
