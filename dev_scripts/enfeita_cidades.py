#!/usr/bin/env python3
"""Enfeita, com tema, as cidades mais SEM GRACA das quatro regioes do cartucho 1.

Pedido do Gui no playtest (06/09/2026): "a cidade esta muito feia, e assim
mesmo?" sobre Canalave, e "as cidades sem graca do ROM hack voce podia dar uma
enfeitada tematica". Quem ESCOLHE as cidades e a regua
`dev_scripts/regua_cidades.py`; este script e o que DESENHA.

DE ONDE VEM O DESENHO. De mapa NOSSO que ja e rico e carrega o MESMO TILESET
PRIMARIO. Nada de arte nova pixel a pixel e nada de metatile inventado: o
catalogo de enfeites e EXTRAIDO, medindo, dos mapas doadores, e so entram
metatiles do PRIMARIO (id < 512), que e o unico pedaco de vocabulario que a
cidade pobre e o doador tem em comum com certeza (o secundario de cada cidade e
outro arquivo, e nem sempre tem irmao). As oito cidades de Sinnoh desta rodada
compartilham `gTileset_GeneralSinnoh` e as duas de Johto compartilham
`gTileset_JohtoNorthEast`: e por isso que a tecnica cobre as dez.
O porto de Canalave, que precisa de barco e engradado que NENHUM tileset de
Sinnoh tem, e caso a parte e mora em `dev_scripts/porto_canalave.py`.

O QUE E UM ENFEITE, medido e nao escolhido a dedo: grupo 4-conexo de metatiles
RAROS no doador (menos de KMIN ocorrencias NAQUELE mapa), retangulo cheio de ate
3x3, longe de evento e da borda, e com o anel de 8 em volta quase todo andavel.
Isso e exatamente o que o artista pos a mao: o arbusto, a arvore solta, a cerca,
a pedra, a placa, o canteiro de flor. Metatile comum e chao e parede, e nao vira
enfeite. Duas travas a mais, as duas medidas e nao supostas:

  - **SOLIDAO**: o metatile tem que cair, na maioria das vezes em que aparece,
    numa MANCHA solida de ate `MANCHA_MAX` celulas. Sem ela entram as lascas de
    PENHASCO (104, 106, 114, 116, 120, 128, 130, 136), que passam no anel quando
    a ponta do penhasco cai na areia mas so fazem sentido coladas nele: soltas
    no meio da praca viram mancha marrom.
  - **ISENTOS**: arvore, arbusto e cerca reprovam na solidao por um motivo que
    nao e defeito deles (no demake de Sinnoh eles formam a MOLDURA de todo mapa,
    entao a mancha tem centenas de celulas) e a fonte usa os tres soltos
    tambem. A lista de isencao foi conferida carimbo a carimbo, olhando o PNG.
  - **PUREZA DO ANEL, so para CANTEIRO**: quase todo o anel tem que ser O MESMO
    chao. Em FloaromaTown entrou um carimbo andavel de 2 celulas (metatiles 901
    e 2) que e o CORRIMAO de uma cerca de rota; solto no gramado ele vira uma
    barra marrom flutuando. O corrimao reprova porque o anel dele tem os POSTES
    da cerca; o canteiro de flor passa porque o anel dele e grama pura. Cobrar
    o mesmo do objeto SOLIDO esvaziava o catalogo (Blackthorn ficava com zero),
    e faz sentido: arvore e pedra moram ao lado de outras coisas por natureza.
  - **COR, no atalho de cobertura**: enfeite que troca 90% dos pixels do chao
    pode ir para um chao diferente do do doador (e o que solta a pedra na terra
    de Oreburgh), mas so se a cor bater. Medido: arbusto verde na neve de
    Snowpoint da 253 de distancia de cor, contra 29 da pedra na terra e 82 da
    arvore na grama. O limite e 150.
  - **MARGEM de 2 celulas** da borda do mapa, e no maximo 2 copias do MESMO
    carimbo por cidade: sem a primeira, Celestic ganhava objeto em (0,18); sem a
    segunda, Snowpoint ganhava dez placas iguais, porque o catalogo de neve tem
    poucos objetos e o rodizio voltava sempre nele. O teto nasceu valendo 6 e
    CONTANDO ERRADO, por `id(e)`, o que dava dois orcamentos ao mesmo desenho
    quando ele chegava pelas duas chamadas de `catalogo()`; com isso Celestic
    saiu com 9 placas iguais, Solaceon com 11 e Oreburgh com 12. O Gui viu no
    playtest, e em 07/09/2026 mandou podar: a conta passou a ser pela
    ASSINATURA do desenho e o teto caiu para 2.
  - **RETALHO DE CHAO nao e enfeite**, e por isso o quadrado de areia com borda
    de grama entrou na lista `RECUSADOS` na mesma poda. Ele nao desenha objeto,
    so troca o piso: ou cai num chao de outra cor e vira remendo (a areia na
    calcada de Eterna e no gramado de Solaceon que o Gui apontou), ou cai num
    chao da mesma cor e vira uma moldura de nada no meio da areia.

DOIS TIPOS DE ENFEITE, e eles pagam portoes diferentes:

  1. **Canteiro** (carimbo ANDAVEL: flor, mato baixo, piso de cor). Nao muda um
     bit acima dos 10 de baixo: `(antigo & 0xFC00) | novo`. Colisao, elevacao e
     comportamento saem identicos, e por isso ele nao paga portao nenhum alem da
     igualdade de comportamento.
  2. **Objeto** (carimbo SOLIDO: arvore, pedra, cerca, placa). Esse MUDA
     colisao, e por isso so cai em celula que (a) e chao liso do mapa, na
     elevacao do chao, (b) encosta em algo solido ou na borda do mapa (por isso
     "enfeite de beira": ele fica junto do predio, do muro do canal ou da
     arvore, nunca plantado no meio da praca), (c) nao e celula de evento nem
     vizinha de uma, e (d) NAO ilha ninguem. A (d) nao e promessa: `alcance()`
     faz busca em largura a partir de todos os warps e NPCs, respeitando
     elevacao, e o portao roda A CADA CARIMBO, exigindo
     `depois == antes - celulas_solidificadas`. Carimbo que fecha um beco e
     desfeito e o gerador segue; um portao no fim so saberia dizer "recusado".

MAIS TRES REGRAS DURAS:

  - Nenhum `map.json` e aberto para escrita: warp, placa, NPC e item ficam onde
    estavam, e as celulas deles mais a orla de 1 sao congeladas.
  - **Agua nao vira chao.** Celula cujo comportamento esta em `AGUA` nao e
    "andavel" para efeito de chao liso. A primeira versao contava so
    `colisao == 0`, e em Canalave o metatile mais comum "andavel" passou a ser a
    AGUA do canal (477 celulas): o gerador plantou arbusto e placa no meio do
    canal, e a regua tinha lido 35,5% de "chao liso" que era o rio.
  - Elevacao intacta: o carimbo andavel copia a elevacao da celula, e o solido
    entra com a elevacao do doador, que e 0 em todo objeto.

O QUE FOI TENTADO E DESCARTADO, com o motivo, para ninguem refazer: **espalhar
variante de piso** (trocar parte do chao liso por metatiles de comportamento
igual, escolhidos por luminancia parecida). Em `SolaceonTown` o filtro deixou
entrar os metatiles de LAVOURA do `gTileset_Celestic`, e o resultado foram
centenas de retalhos laranja jogados no gramado inteiro: a regua melhorou de
64,2% para 33,6% de chao liso e o mapa ficou PIOR. Numero de regua melhor com
desenho pior e exatamente o que a regua nao ve. Canteiro carimbado em bloco
substituiu a ideia.

IDEMPOTENCIA, e por que ela precisa de arquivo. Diferente do
`arte_mapas_pobres.py`, cujas escolhas dependem so de colisao e comportamento
(coisas que ele nao muda), aqui a escolha depende do METATILE, que e justamente
o que muda. Rodar em cima do proprio desenho daria outro desenho. Por isso o
plano guarda, em `dev_scripts/enfeita_cidades.json`, o valor ANTIGO de cada
celula escrita: na proxima rodada o script desfaz o proprio desenho em memoria,
replaneja sobre a base e escreve de novo. O mesmo arquivo e o desfazer manual,
se o Gui nao gostar.

E DESFAZER SO NO MAPA ALVO NAO BASTA, que foi o defeito da primeira versao. O
DOADOR tambem e cidade enfeitada: Eterna aprende com Oreburgh pelo caminho de
mesmo PRIMARIO, e Canalave e doadora das outras sete de Sinnoh. Lendo o doador
com o enfeite ja aplicado, o catalogo cresce a cada rodada e o desenho passa a
depender da ORDEM das cidades. Medido em 06/09/2026, com a mesma base: Oreburgh
saiu com 45, depois 51, depois 57 celulas em tres rodadas seguidas, e Eterna com
45 e depois 54. O conserto e `grade_base`, por onde passa TODA leitura de doador,
e ela desfaz pelos dois planos em disco MAIS o que a rodada corrente ja desenhou
(`registra_desenho`), senao a segunda cidade da mesma rodada aprende com a
primeira. Hoje tres rodadas seguidas dao map.bin, tileset e plano byte
identicos, e o caso 9 do `--demo` e quem cobra isso.

Uso:
    python3 dev_scripts/enfeita_cidades.py             # mede e mostra o plano
    python3 dev_scripts/enfeita_cidades.py --aplicar   # escreve os map.bin
    python3 dev_scripts/enfeita_cidades.py --desfazer  # devolve tudo a base
    python3 dev_scripts/enfeita_cidades.py --demo      # auto-teste
    python3 dev_scripts/enfeita_cidades.py --cidade X  # so uma
"""
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
import arte_ginasios_sinnoh as G   # noqa: E402  (le layout, tileset e atributo)

PLANO = f"{RAIZ}/dev_scripts/enfeita_cidades.json"
PLANO_PORTO = f"{RAIZ}/dev_scripts/porto_canalave.json"

N4 = [(0, -1), (1, 0), (0, 1), (-1, 0)]
N8 = N4 + [(1, -1), (1, 1), (-1, 1), (-1, -1)]

KMIN = 25          # no doador, metatile com menos de KMIN ocorrencias e "enfeite"
FOLGA_ANEL = 0.30  # fracao maxima do anel de 8 em volta que pode ser solida
PUREZA_ANEL = 0.70  # fracao minima do anel que tem que ser o MESMO chao
BLOCO_PROPRIO = "175_cidades_enfeitadas.json"  # os casos QUE ESTA RODADA escreveu
PISO_SOLIDAO = 0.60  # fracao minima das ocorrencias que caem em mancha pequena
MANCHA_MAX = 9     # ate 9 celulas solidas coladas ainda e OBJETO, acima e parede
ORLA = 1           # celulas de folga em volta de todo evento
MARGEM = 2         # celulas de folga em relacao a borda do mapa
ESPACO = 5         # distancia minima (Chebyshev) entre dois enfeites solidos
ESPACO_CANTEIRO = 7
TETO_ENFEITE = 40  # nunca mais que isso numa cidade, por maior que ela seja
TETO_CANTEIRO = 14
TETO_POR_CARIMBO = 2  # copias do MESMO enfeite numa cidade (decisao do Gui)
FRACAO_LISO = 0.015  # metatile andavel com 1,5% ou mais das celulas e "chao liso"
TAPA_TOTAL = 0.90  # enfeite que troca 90% dos pixels do chao cabe em qualquer chao
LIMITE_COR = 150.0  # e so se a cor dele nao brigar com a do chao (verde na neve)

# Arvore, arbusto e cerca sao objeto de verdade mesmo formando a moldura do
# mapa. Conferido olhando o carimbo, um a um, no PNG do catalogo.
ISENTOS = {22, 23, 30, 31, 470, 471, 486, 487, 306, 307, 312, 313, 314, 321,
           3, 27, 226, 404, 14, 15, 37, 38, 39, 53, 54, 55, 403, 418, 4, 7}

# Metatile que PASSA em todo portao e mesmo assim fica errado no olho, porque ele
# nao e enfeite: e peca de LIGACAO, que so faz sentido presa ao que ela liga. O
# 175 e o 207 sao o DEGRAU branco de tres celulas do `gTileset_GeneralSinnoh`;
# eles passam na pureza do anel porque o anel deles e grama pura, e o resultado,
# visto no render de 06/09/2026, e uma escada flutuando no meio do gramado de
# FloaromaTown (2 pecas), de EternaCity (5) e de OreburghCity (3). Nenhum portao
# de colisao, alcance ou rota pega isso: e julgamento de desenho, e por isso a
# lista e curta, escrita a mao e com o motivo ao lado.
#
# A SEGUNDA leva entrou em 07/09/2026, pela poda que o Gui pediu na pergunta 47
# ("retalhos de chao de outra cor"). Sao os metatiles do RETALHO DE CHAO: o
# quadrado de areia com a borda arredondada de grama. Eles nao desenham objeto
# nenhum, so trocam o piso, e por isso o resultado e sempre um dos dois defeitos
# que o Gui viu no render: caem num chao de outra cor e viram remendo (areia na
# calcada de EternaCity, 83,7 de distancia de cor; areia no gramado de
# SolaceonTown, TwinleafTown, SandgemTown, FloaromaTown e EternaCity, de 97 a
# 111; areia no gramado de BlackthornCity, 99,4), ou caem no chao da MESMA cor e
# viram uma moldura de nada no meio da areia (CelesticTown, SolaceonTown e
# OreburghCity, entre 15,3 e 19,3 de distancia). Nos dois casos e peca de
# LIGACAO, igual ao degrau: ela so faz sentido presa a regiao de chao que ela
# contorna. Os ids sao lidos no PRIMARIO DO DOADOR; nos outros primarios do
# cartucho 1 os mesmos numeros sao penhasco (254 a 263 no `gTileset_GeneralSinnoh`)
# e parede de caverna (280 a 298 no `gTileset_JohtoNorthEast`), que nunca foram
# enfeite valido, entao a lista pode ser plana sem tirar nada de ninguem.
RECUSADOS = {175, 207,
             # `gTileset_GeneralSinnoh`: o retalho de areia 3x3 com borda de grama
             280, 281, 282, 288, 289, 290, 296, 297, 298,
             # `gTileset_JohtoNorthEast`: o mesmo retalho, 2x2
             254, 255, 262, 263}

# As dez cidades, o tema de cada uma e de quem ela aprende. O tema e o do jogo de
# origem, nao invencao: Canalave e cidade PORTUARIA no Diamante/Perola, Oreburgh
# e cidade de MINA, Snowpoint e a cidade da NEVE, Celestic e a vila das RUINAS,
# Solaceon e RURAL, Floaroma e das FLORES, Eterna e a da floresta antiga,
# Cianwood e o porto rochoso de Johto e Blackthorn a cidade dos DRAGOES.
#
# Hearthome, Sunyshore e Pastoria ficaram FORA da lista de alvos desta rodada
# porque outros agentes estavam editando o `map.bin` dos tres no mesmo dia. Como
# DOADORES eles sao so leitura, e por isso continuam aqui.
TEMAS = {
    "CanalaveCity":   "porto: cais, engradado, barco e poste",
    "CelesticTown":   "ruinas: pedra, cerca e mato antigo",
    "SnowpointCity":  "neve: arvore carregada e cerca no gelo",
    "SolaceonTown":   "rural: canteiro, cerca e mato de pasto",
    "OreburghCity":   "mina: pedra solta, cerca e placa",
    "JubilifeCity":   "cidade grande: canteiro, cerca e placa",
    "TwinleafTown":   "vila natal: horta, cerca e flor",
    "SandgemTown":    "praia e laboratorio: canteiro, pedra e cerca",
    "BlackthornCity": "cidade dos dragoes: pedra, cerca e mato",
    "EternaCity":     "floresta antiga: arvore, canteiro e pedra",
    "FloaromaTown":   "flores: canteiro, cerca e arbusto",
}

# Medida e NAO servida, com o motivo, para ninguem tentar de novo achando que
# esqueceram: `CianwoodCity` e a 8a mais sem graca e ficou de fora. Os quatro
# irmaos de par dela (Route47, Route41, Route44, Route48) nao guardam UM objeto
# solto, e o chao dela (metatile 113, a areia de praia de Johto) nao aparece
# embaixo de nenhum enfeite dos mapas de mesmo primario: dos 31 carimbos que o
# catalogo achou, nenhum passa em `chao`/`tapa` sem ficar com borda de grama ou
# de terra na areia. Servir Cianwood exige importar peca de outro tileset, como
# o `porto_canalave.py` faz, e isso e obra de outra rodada.
NAO_SERVIDAS = {"CianwoodCity": "sem carimbo compativel com a areia de praia"}


# ------------------------------------------------------------- comportamentos
def _ordem_comportamentos(_c={}):
    """{nome: valor} lido do header. O enum ja mudou de tamanho nesta arvore."""
    if _c:
        return _c
    texto = open(f"{RAIZ}/include/constants/metatile_behaviors.h").read()
    corpo = texto[texto.index("MB_NORMAL"):]
    i = 0
    for m in re.finditer(r"^\s*(MB_[A-Z0-9_]+)\s*(?:=\s*(0x[0-9A-Fa-f]+|\d+))?\s*,",
                         corpo, re.M):
        if m.group(2):
            i = int(m.group(2), 0)
        _c[m.group(1)] = i
        i += 1
    return _c


def _valores(nomes):
    ordem = _ordem_comportamentos()
    falta = [n for n in nomes if n not in ordem]
    if falta:
        raise SystemExit("comportamento sumiu do header: %s" % falta)
    return {ordem[n] for n in nomes}


def chao_banal(_c={}):
    """Comportamentos que um OBJETO SOLIDO pode cobrir sem apagar mecanica.

    Fica de fora tudo que faz alguma coisa: `MB_TALL_GRASS` e `MB_LONG_GRASS`
    (encontro selvagem), gelo, esteira, porta, seta de warp, mola. Ficam de
    dentro os cinco que sao so chao. `MB_BERRY_TREE_SOIL` entra com motivo
    medido: ele so vale alguma coisa embaixo de um objeto de arvore de berry, e
    os 90 `BERRY_SOIL` de Sinnoh foram CORTADOS da ROM (ESTADO 0.s), entao as
    777 celulas de terra de Oreburgh sao chao inerte. O gerador confere isso
    mapa a mapa antes de usar (`sem_berry`).
    """
    if not _c:
        _c["set"] = _valores(["MB_NORMAL", "MB_SAND", "MB_DEEP_SAND",
                              "MB_FOOTPRINTS", "MB_SHORT_GRASS",
                              "MB_BERRY_TREE_SOIL"])
    return _c["set"]


def agua(_c={}):
    """Comportamentos de metatile em que o jogador NAO anda a pe (surfa).

    Lido do proprio `include/constants/metatile_behaviors.h` em vez de decorado:
    o enum ja mudou de tamanho nesta arvore, e numero cravado aqui envelheceria
    calado. So entram os que exigem Surf; `MB_PUDDLE` e `MB_SHALLOW_WATER` sao
    agua de andar e ficam de fora de proposito.
    """
    if _c:
        return _c["set"]
    _c["set"] = _valores(
        ["MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER",
         "MB_WATERFALL", "MB_SOOTOPOLIS_DEEP_WATER", "MB_OCEAN_WATER",
         "MB_UNUSED_SOOTOPOLIS_DEEP_WATER", "MB_NO_SURFACING",
         "MB_UNUSED_SOOTOPOLIS_DEEP_WATER_2", "MB_SEAWEED",
         "MB_SEAWEED_NO_SURFACING", "MB_FAST_WATER", "MB_CYCLING_ROAD_WATER"])
    return _c["set"]


# ------------------------------------------------------------------ utilidades
# Mapas que OUTROS agentes estavam editando em 06/09/2026. Nao entram como
# doador para o desenho nao depender de trabalho ainda nao commitado.
EM_OBRA = {"HearthomeCity", "SunyshoreCity", "PastoriaCity", "Mahoganytown"}


def doadores_de(alvo, quantos=6, so_primario=False, _c={}):
    """Mapas de rua com o MESMO PAR de tilesets, do maior para o menor.

    O par inteiro, e nao so o primario: com o secundario igual o carimbo pode
    usar TODO o vocabulario, e, mais importante, ele foi desenhado sobre o MESMO
    chao. Aprender so pelo primario punha arbusto de GRAMA verde na neve de
    Snowpoint, porque a camada de baixo do metatile 486 e grama e o mapa de
    Snowpoint e branco (medido, olhando o PNG, em 06/09/2026).
    """
    if (alvo, so_primario) in _c:
        return _c[(alvo, so_primario)]
    L0 = _layouts()[json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))["layout"]]
    par, achados = (L0["primary_tileset"], L0["secondary_tileset"]), []
    for nome in sorted(os.listdir(f"{RAIZ}/data/maps")):
        p = f"{RAIZ}/data/maps/{nome}/map.json"
        if not os.path.isfile(p) or nome == alvo or nome in EM_OBRA:
            continue
        j = json.load(open(p))
        if j.get("map_type") not in ("MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE"):
            continue
        L = _layouts().get(j["layout"])
        if not L:
            continue
        if so_primario:
            if L["primary_tileset"] == par[0] and L["secondary_tileset"] != par[1]:
                achados.append((L["width"] * L["height"], nome))
        elif (L["primary_tileset"], L["secondary_tileset"]) == par:
            achados.append((L["width"] * L["height"], nome))
    achados.sort(reverse=True)
    _c[(alvo, so_primario)] = [n for _, n in achados[:quantos]]
    return _c[(alvo, so_primario)]


def _layouts(_c={}):
    if not _c:
        d = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
        _c.update({l["id"]: l for l in d["layouts"] if l.get("id")})
    return _c


def grade(nome):
    return G.grade(nome)


def _desenhos(_c={}):
    """{mapa: {celula: (antigo, novo)}} de TUDO que esta ferramenta ja desenhou.

    Comeca nos dois planos em disco (o desta rodada anterior e o do porto) e vai
    CRESCENDO durante a rodada, por `registra_desenho`. As duas fontes importam:
    sem o disco, a segunda rodada aprende com o desenho da primeira; sem o
    registro em memoria, a segunda CIDADE da mesma rodada aprende com o desenho
    da primeira, que `roda` acabou de gravar em disco.
    """
    if _c:
        return _c["m"]
    m = {}
    for arq in (PLANO, PLANO_PORTO):
        if not os.path.exists(arq):
            continue
        for nome, reg in json.load(open(arq)).items():
            m.setdefault(nome, {}).update({i: (a, n) for i, a, n in reg["celulas"]})
    _c["m"] = m
    return m


def registra_desenho(nome, celulas):
    m = _desenhos()
    m.setdefault(nome, {}).update({i: (a, n) for i, a, n in celulas})


def grade_base(nome):
    """A grade do DOADOR sem enfeite nenhum, nem deste script nem do porto.

    So serve para DOADOR. O mapa ALVO continua entrando por `grade`, com o
    desfazer restrito ao plano DESTE script (`base_de`): usar esta funcao no alvo
    apagaria o porto de Canalave, porque `roda` grava a grade inteira e o porto
    teria sido desfeito junto. Custou um render: a Canalave saiu sem um barco.

    DOADOR TAMBEM E CIDADE ENFEITADA, e foi por isso que a primeira versao nao
    era idempotente de verdade. `EternaCity` aprende com `OreburghCity` pelo
    caminho de mesmo PRIMARIO, e ler o doador com o enfeite JA aplicado faz o
    catalogo da segunda depender da ordem em que a primeira rodou. Medido em
    06/09/2026: rodando o gerador tres vezes seguidas sobre a MESMA base,
    Oreburgh saiu com 45, depois 51, depois 57 celulas, e Eterna com 45 e depois
    54, sempre crescendo, porque cada rodada aprendia com o enfeite da anterior.
    O portao de igualdade byte a byte pegou; o `--demo` de antes nao, porque ele
    so olhava o mapa alvo.

    Todo doador passa por aqui, e o `PLANO_PORTO` entra junto porque Canalave e
    doador de mesmo primario das outras sete cidades de Sinnoh.
    """
    d, L, W, H, v = G.grade(nome)
    reg = _desenhos().get(nome)
    if reg:
        v = list(v)
        for idx, (antigo, novo) in reg.items():
            if v[idx] == novo:
                v[idx] = antigo
    return d, L, W, H, v


def eventos(d):
    return {(o["x"], o["y"])
            for k in ("object_events", "warp_events", "bg_events", "coord_events")
            for o in (d.get(k) or [])}


def congelado(d):
    ev = eventos(d)
    fora = set()
    for x, y in ev:
        for dx in range(-ORLA, ORLA + 1):
            for dy in range(-ORLA, ORLA + 1):
                fora.add((x + dx, y + dy))
    return ev, fora


_LEG = re.compile(r"^(?:\d+:)?(UP|DOWN|LEFT|RIGHT)(?:\*(\d+))?$")


def corredores_de_teste(alvo, v, W, H, d, _c={}):
    """Celulas que algum caso da SUITE ja anda dentro deste mapa.

    Enfeite solido nao pode cair numa delas, e o motivo e medido: os casos do
    `testa_critico.py` andam por PERNAS SATURANTES ("vinte DOWN"), e uma perna
    saturante nao para onde o autor escreveu, para no primeiro obstaculo. Um
    barril novo no meio do caminho encurta a perna e o caso quebra sem que nada
    tenha ficado inalcancavel: em 06/09/2026 o poste de (19,39) de Canalave
    derrubou SETE casos de balsa de uma vez (T8.5, T10.1 e T86.8 a T86.12), que
    descem a coluna 19 inteira ate a linha 52 antes de virar.

    A varredura le so as pernas de DIRECAO do roteiro (A, B, NADA, R+START e
    menu sao ignorados) e simula sobre a grade BASE, a de antes do desenho. Ela
    e uma APROXIMACAO POR EXCESSO de proposito: caso que entra no mapa por um
    `WARP=` no meio do roteiro nao e simulado, e caso cujo roteiro passa por
    menu anda mais do que andaria de verdade. Excesso aqui custa enfeite a
    menos, e falta custaria caso vermelho.
    """
    if alvo in _c:
        return _c[alvo]
    import glob
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = None
    grupos = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    # MAP_X do nome da pasta: o proprio `map.json` guarda o nome do mapa
    nome_mapa = "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_",
                                d.get("name", alvo)).upper().replace("__", "_")
    obj = {(o["x"], o["y"]) for o in (d.get("object_events") or [])}
    warps = d.get("warp_events") or []
    pisadas = set()

    def caminha(x, y, pernas, olhando):
        """Anda as pernas a partir de (x,y), gastando um aperto para VIRAR.

        A primeira tecla de uma direcao NOVA so vira o boneco (licao T121.1 da
        suite), e ignorar isso nao e detalhe: sem a virada a simulacao anda um
        tile a mais na primeira perna, a segunda perna comeca noutro lugar e o
        caminho inteiro diverge. Foi assim que o corredor de TwinleafTown saiu
        errado e tres casos (T100.1, T100.3 e T100.4) quebraram com o enfeite de
        (2,10), que a varredura nao tinha marcado.
        """
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
                ea = (v[y * W + x] >> 12) & 0xF
                eb = (v[j] >> 12) & 0xF
                if ea and eb and ea != eb:
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
                m = _LEG.match(tok.strip())
                if m:
                    pernas.append(({"UP": (0, -1), "DOWN": (0, 1),
                                    "LEFT": (-1, 0), "RIGHT": (1, 0)}[m.group(1)],
                                   int(m.group(2) or 1)))
            # O warp de debug nao promete NEM onde o jogador olha NEM em que
            # tile ele pousa, entao entram as QUATRO direcoes iniciais e as DUAS
            # hipoteses de pouso (o proprio tile do warp e o de baixo dele), e o
            # corredor e a uniao de tudo. A segunda hipotese nao e teoria: o
            # T94.1 quebrou por ela em 06/09/2026. O warp 2 de CelesticTown esta
            # em (2,15), que e a PORTA e nao da passo nenhum, entao simular so
            # dali dava um corredor de 23 celulas e uma cidade quase toda livre
            # para enfeitar; na ROM o jogador pousa em (2,16) e anda ate (16,10),
            # e um carimbo novo o parou em (6,15).
            for x0, y0 in ((warps[wid]["x"], warps[wid]["y"]),
                           (warps[wid]["x"], warps[wid]["y"] + 1)):
                if not (0 <= x0 < W and 0 <= y0 < H):
                    continue
                for olhando in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    caminha(x0, y0, pernas, olhando)
    _c[alvo] = pisadas
    return pisadas


def alcance(v, W, H, ini):
    """Celulas andaveis alcancaveis a pe, respeitando elevacao.

    Duas elevacoes diferentes e ambas nao-nulas nao se ligam
    (`IsElevationMismatchAt`): sem isso a busca atravessaria a agua do canal de
    Canalave (elevacao 1) e daria a outra margem por alcancada.
    """
    vis = set(p for p in ini)
    fila = collections.deque(vis)
    while fila:
        x, y = fila.popleft()
        ea = (v[y * W + x] >> 12) & 0xF
        for dx, dy in N4:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in vis:
                continue
            j = ny * W + nx
            if (v[j] >> 10) & 3:
                continue
            eb = (v[j] >> 12) & 0xF
            if ea and eb and ea != eb:
                continue
            vis.add((nx, ny))
            fila.append((nx, ny))
    return vis


def partidas(d, W, H, v):
    p = [(w["x"], w["y"]) for w in (d.get("warp_events") or [])]
    p += [(o["x"], o["y"]) for o in (d.get("object_events") or [])]
    return [(x, y) for x, y in p
            if 0 <= x < W and 0 <= y < H and not ((v[y * W + x] >> 10) & 3)]


# ------------------------------------------------------------------- cobertura
def _pixels(pri, sec, _c={}):
    """{metatile: [(r,g,b) x 256]}, o desenho de cada metatile do par."""
    if (pri, sec) in _c:
        return _c[(pri, sec)]
    import render_maps as RM
    from PIL import Image
    tp, ts = RM.carregar_tileset(pri), RM.carregar_tileset(sec)
    fundo = tp["paletas"][0][0]
    out = {}
    for base, tset in ((0, tp), (512, ts)):
        for i in range(len(tset["metatiles"]) // 16):
            img = Image.new("RGB", (16, 16), fundo)
            px = img.load()
            for camada in (0, 1):
                for q in range(4):
                    it, fh, fv, ip = RM.entradas_metatile(tset["metatiles"], i)[camada * 4 + q]
                    t = RM.resolver_tile(tp, ts, it)
                    if t is None:
                        continue
                    cores = (tp if ip < 6 else ts)["paletas"].get(ip)
                    if cores is None:
                        continue
                    RM.desenhar_tile(px, (q % 2) * 8, (q // 2) * 8, t, cores, fh, fv)
            out[base + i] = [px[x, y] for y in range(16) for x in range(16)]
    _c[(pri, sec)] = out
    return out


def cor_media(pri, sec, mt, _c={}):
    """(r, g, b) medio do metatile, para comparar enfeite com chao."""
    chave = (pri, sec, mt)
    if chave not in _c:
        px = _pixels(pri, sec).get(mt)
        _c[chave] = (0.0, 0.0, 0.0) if not px else tuple(
            sum(p[k] for p in px) / 256.0 for k in range(3))
    return _c[chave]


def distancia_cor(pri, sec, a, b):
    ca, cb = cor_media(pri, sec, a), cor_media(pri, sec, b)
    return sum((ca[i] - cb[i]) ** 2 for i in range(3)) ** 0.5


def cobertura(pri, sec, mt, chao):
    """Fracao dos 256 pixels do metatile que NAO sao o chao do doador.

    Serve para separar o enfeite que TAPA a celula inteira (pedra, arvore do
    meio, tronco) do que so pinta um pedaco e deixa o chao aparecer nos cantos
    (arbusto, cerca, flor). O primeiro pode ir para qualquer chao; o segundo so
    para um chao igual ao do doador, senao vira mancha de grama verde na neve
    de Snowpoint.
    """
    p = _pixels(pri, sec)
    a, b = p.get(mt), p.get(chao)
    if not a or not b:
        return 0.0
    return sum(1 for i in range(256) if a[i] != b[i]) / 256.0


# -------------------------------------------------------------------- catalogo
def assinatura_crua(w, h, solido, cel):
    """O que faz DOIS carimbos serem 'o mesmo enfeite' aos olhos do jogador."""
    return (w, h, solido, tuple((c[0], c[1], c[2]) for c in cel))


def assinatura(e):
    return assinatura_crua(e["w"], e["h"], e["solido"], e["cel"])


def _solidao(primario, doadores, _c={}):
    """{metatile: fracao das ocorrencias que caem em MANCHA solida pequena}."""
    chave = (primario, tuple(doadores))
    if chave in _c:
        return _c[chave]
    total, pequeno = collections.Counter(), collections.Counter()
    for nome in doadores:
        if not os.path.isfile(f"{RAIZ}/data/maps/{nome}/map.json"):
            continue
        d, L, W, H, v = grade_base(nome)
        if L["primary_tileset"] != primario:
            continue
        duro = [bool((c >> 10) & 3) for c in v]
        visto = [False] * (W * H)
        for y0 in range(H):
            for x0 in range(W):
                i0 = y0 * W + x0
                if not duro[i0] or visto[i0]:
                    continue
                comp, fila = [i0], [(x0, y0)]
                visto[i0] = True
                while fila:
                    x, y = fila.pop()
                    for dx, dy in N4:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < W and 0 <= ny < H:
                            j = ny * W + nx
                            if duro[j] and not visto[j]:
                                visto[j] = True
                                comp.append(j)
                                fila.append((nx, ny))
                for j in comp:
                    mt = v[j] & 0x3FF
                    total[mt] += 1
                    if len(comp) <= MANCHA_MAX:
                        pequeno[mt] += 1
    _c[chave] = {mt: pequeno[mt] / total[mt] for mt in total}
    return _c[chave]


def catalogo(primario, doadores, so_primario=False, _c={}):
    """Enfeites aprendidos dos doadores. Cada um traz `solido` True ou False."""
    chave = (primario, tuple(doadores), so_primario)
    if chave in _c:
        return _c[chave]
    solto = _solidao(primario, doadores)
    achados, vistos = [], set()
    for nome in doadores:
        if not os.path.isfile(f"{RAIZ}/data/maps/{nome}/map.json"):
            continue
        d, L, W, H, v = grade_base(nome)
        if L["primary_tileset"] != primario:
            continue
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        ev, _ = congelado(d)
        freq = collections.Counter(c & 0x3FF for c in v)
        raro = {(x, y) for y in range(1, H - 1) for x in range(1, W - 1)
                if freq[v[y * W + x] & 0x3FF] < KMIN and (x, y) not in ev
                and not (so_primario and (v[y * W + x] & 0x3FF) >= 512)}
        visto = set()
        for p0 in sorted(raro):
            if p0 in visto:
                continue
            grupo, fila = {p0}, [p0]
            visto.add(p0)
            while fila:
                x, y = fila.pop()
                for dx, dy in N4:
                    n = (x + dx, y + dy)
                    if n in raro and n not in visto:
                        visto.add(n)
                        grupo.add(n)
                        fila.append(n)
            xs, ys = [p[0] for p in grupo], [p[1] for p in grupo]
            w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
            if w > 3 or h > 3 or w * h != len(grupo):
                continue
            x0, y0 = min(xs), min(ys)
            cel = [(x - x0, y - y0, v[y * W + x] & 0x3FF,
                    (v[y * W + x] >> 10) & 3, (v[y * W + x] >> 12) & 0xF)
                   for x, y in sorted(grupo, key=lambda p: (p[1], p[0]))]
            solido = all(c[3] for c in cel)
            if not solido and any(c[3] for c in cel):
                continue   # meio solido, meio andavel: nao da para carimbar
            if any(beh(c[2]) != beh(cel[0][2]) for c in cel):
                continue
            anel = {(x + dx, y + dy) for x, y in grupo for dx, dy in N8} - grupo
            duro = sum(1 for p in anel
                       if not (0 <= p[0] < W and 0 <= p[1] < H)
                       or ((v[p[1] * W + p[0]] >> 10) & 3))
            if duro > FOLGA_ANEL * len(anel):
                continue
            # o CHAO do doador embaixo do enfeite: o metatile mais comum do
            # anel. So se ele existir no chao liso do alvo o carimbo entra, e e
            # essa linha que impede arbusto de grama na neve.
            chao_anel = collections.Counter(
                v[p[1] * W + p[0]] & 0x3FF for p in anel
                if 0 <= p[0] < W and 0 <= p[1] < H
                and not ((v[p[1] * W + p[0]] >> 10) & 3)).most_common(1)
            if not chao_anel:
                continue
            # PUREZA do anel: quase todo o anel tem que ser O MESMO chao. O
            # teste de "anel quase todo andavel" nao basta, e o defeito e
            # visivel: em FloaromaTown entrou um carimbo andavel de 2 celulas
            # (metatiles 901 e 2) que e o CORRIMAO de uma cerca de rota, e solto
            # no gramado ele vira uma barra marrom flutuando. O corrimao reprova
            # aqui porque o anel dele tem os POSTES da cerca; o canteiro de flor
            # passa porque o anel dele e grama pura.
            # So para CANTEIRO. O objeto SOLIDO (arvore, pedra, arbusto) mora
            # ao lado de outras coisas por natureza, e cobrar pureza dele
            # esvaziava o catalogo: BlackthornCity ficava com ZERO objeto e
            # JubilifeCity com seis num mapa de 70x64.
            anel_dentro = [p for p in anel if 0 <= p[0] < W and 0 <= p[1] < H]
            if not solido:
                if not anel_dentro or sum(
                        1 for p in anel_dentro
                        if (v[p[1] * W + p[0]] & 0x3FF) == chao_anel[0][0]) \
                        < PUREZA_ANEL * len(anel_dentro):
                    continue
            if solido and any(solto.get(c[2], 0.0) < PISO_SOLIDAO for c in cel) \
               and not all(c[2] in ISENTOS for c in cel):
                continue
            if any(c[2] in RECUSADOS for c in cel):
                continue
            marca = assinatura_crua(w, h, solido, cel)
            if marca in vistos:
                continue
            vistos.add(marca)
            piso_doador = chao_anel[0][0]
            tapa = min(cobertura(L["primary_tileset"], L["secondary_tileset"],
                                 c[2], piso_doador) for c in cel)
            achados.append({"w": w, "h": h, "solido": solido, "cel": cel,
                            "beh": beh(cel[0][2]), "chao": piso_doador,
                            "tapa": tapa, "doador": nome})
    achados.sort(key=lambda e: (len(e["cel"]), e["cel"][0][2]))
    _c[chave] = achados
    return achados


def liso_de(v, W, H, beh, _c={}):
    """O conjunto de chao liso de uma grade, do mesmo jeito que `plano` calcula."""
    AG = agua()
    freq = collections.Counter(
        v[i] & 0x3FF for i in range(W * H)
        if not ((v[i] >> 10) & 3) and beh(v[i] & 0x3FF) not in AG)
    n = sum(freq.values()) or 1
    return {mt for mt, c in freq.items() if c >= max(8, FRACAO_LISO * n)}


def catalogo_de(alvo, L):
    """O catalogo do alvo: primeiro os irmaos de PAR, e o primario como reserva.

    SEGUNDA FONTE, so quando a primeira nao da objeto: Snowpoint, Blackthorn e
    Cianwood tem irmao de par (as rotas em volta), mas nenhuma delas guarda
    objeto solto e o catalogo sai so com canteiro. Nesse caso entram os mapas de
    mesmo PRIMARIO, e ai o carimbo so pode usar metatile do primario (o
    secundario deles e outro arquivo, e o mesmo id desenha outra coisa) e ainda
    precisa passar em `chao`/`tapa`, que e quem impede arbusto de grama na neve.
    """
    cat = list(catalogo(L["primary_tileset"], doadores_de(alvo)))
    if sum(1 for e in cat if e["solido"]) < 3:
        cat += [e for e in catalogo(L["primary_tileset"],
                                    doadores_de(alvo, so_primario=True),
                                    so_primario=True) if e["solido"]]
    cat.sort(key=lambda e: (len(e["cel"]), e["cel"][0][2]))
    return cat


# ----------------------------------------------------------------------- plano
def plano(alvo, base=None):
    """(L, W, H, v_base, escritas, n_objetos, n_canteiros)."""
    d, L, W, H, v0 = grade(alvo)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG, BANAL = agua(), chao_banal()
    # `MB_BERRY_TREE_SOIL` so entra em mapa SEM arvore de berry: se algum dia
    # voltar objeto de berry, o chao dele deixa de ser inerte.
    if any("BERRY_TREE" in (o.get("graphics_id") or "")
           for o in (d.get("object_events") or [])):
        BANAL = BANAL - _valores(["MB_BERRY_TREE_SOIL"])
    ev, gelo = congelado(d)
    gelo |= corredores_de_teste(alvo, v, W, H, d)
    escritas, aplicado = {}, list(v)

    # chao liso: andavel a pe (colisao 0 e comportamento fora da agua)
    freq = collections.Counter(
        v[i] & 0x3FF for i in range(W * H)
        if not ((v[i] >> 10) & 3) and beh(v[i] & 0x3FF) not in AG)
    if not freq:
        raise SystemExit("%s: nenhuma celula andavel a pe" % alvo)
    n_and = sum(freq.values())
    chao = freq.most_common(1)[0][0]
    elev_chao = collections.Counter(
        (c >> 12) & 0xF for c in v if (c & 0x3FF) == chao).most_common(1)[0][0]
    liso = liso_de(v, W, H, beh)

    cat = catalogo_de(alvo, L)
    ini = partidas(d, W, H, v)
    antes = alcance(v, W, H, ini)
    postos = []

    def cabe(e, x, y):
        # MARGEM: enfeite colado na borda do mapa aparece cortado na tela e cai
        # na moldura de arvore que o jogador nunca pisa. Medido: sem ela,
        # CelesticTown ganhava um objeto em (0,18) e SolaceonTown em (19,0).
        if x < MARGEM or y < MARGEM:
            return False
        if x + e["w"] > W - MARGEM or y + e["h"] > H - MARGEM:
            return False
        # ATALHO DE COBERTURA: enfeite que tapa a celula inteira pode ir para um
        # chao diferente do do doador, MAS so se a cor bater. Sem a segunda
        # metade, o arbusto verde 486 (que tapa 100% dos pixels) caia na NEVE de
        # Snowpoint: medido, 253 de distancia de cor contra 29 da pedra na terra
        # de Oreburgh e 82 da arvore na grama de Celestic.
        if e["chao"] not in liso:
            if e["tapa"] < TAPA_TOTAL:
                return False
            if any(distancia_cor(L["primary_tileset"], L["secondary_tileset"],
                                 c[2], aplicado[(y + c[1]) * W + x + c[0]] & 0x3FF)
                   > LIMITE_COR for c in e["cel"]):
                return False
        folga = ESPACO if e["solido"] else ESPACO_CANTEIRO
        if any(max(abs(x - px), abs(y - py)) < folga for px, py, _ in postos):
            return False
        pes = [(x + c[0], y + c[1]) for c in e["cel"]]
        for (cx, cy) in pes:
            i = cy * W + cx
            if (cx, cy) in gelo:
                return False
            if (aplicado[i] & 0x3FF) not in liso:
                return False
            if (aplicado[i] >> 10) & 3:
                return False
            if ((aplicado[i] >> 12) & 0xF) != elev_chao:
                return False
            atual = beh(aplicado[i] & 0x3FF)
            if e["solido"]:
                if atual not in BANAL:
                    return False
            elif atual != e["beh"]:
                return False
        if not e["solido"]:
            return True
        # de BEIRA: alguma celula do carimbo encosta em algo SOLIDO de verdade.
        # A borda do mapa nao conta, senao o objeto atraca no nada.
        for cx, cy in pes:
            for dx, dy in N4:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in pes \
                   and ((aplicado[ny * W + nx] >> 10) & 3):
                    return True
        return False

    # varredura ESPALHADA: em ordem de leitura todo enfeite se amontoa no canto
    # de cima. A ordem aqui e um embaralhamento determinista da posicao, e o
    # carimbo gira a cada posto para o mapa nao ganhar quinze copias do mesmo.
    ordem = sorted(((x, y) for y in range(H) for x in range(W)),
                   key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF, p))
    por_carimbo = collections.Counter()
    solidos = [e for e in cat if e["solido"]]
    canteiros = [e for e in cat if not e["solido"]]
    novos_solidos = []
    contas = {"solido": 0, "canteiro": 0}
    tetos = {"solido": max(6, min(TETO_ENFEITE, (W * H) // 110)),
             "canteiro": max(3, min(TETO_CANTEIRO, (W * H) // 260))}
    for x, y in ordem:
        for tipo, lista in (("solido", solidos), ("canteiro", canteiros)):
            if not lista or contas[tipo] >= tetos[tipo]:
                continue
            for t in range(len(lista)):
                e = lista[(contas[tipo] + t) % len(lista)]
                # TETO POR CARIMBO: sem ele Snowpoint ganhava dez copias da
                # MESMA placa, porque o catalogo de neve tem poucos objetos e o
                # rodizio voltava sempre nele. Dez placas iguais nao e
                # decoracao, e repeticao.
                #
                # A conta era por `id(e)`, e ISSO NAO SEGURAVA NADA quando o
                # mesmo desenho chegava por dois caminhos: `catalogo_de` soma
                # duas chamadas de `catalogo()`, cada uma com o proprio `vistos`,
                # entao a placa 3 entrava como DOIS objetos Python diferentes e
                # ganhava dois orcamentos. Medido no plano de 06/09/2026, com o
                # teto valendo 6: CelesticTown ficou com 9 copias da placa,
                # SolaceonTown com 11 e OreburghCity com 12. E foi exatamente
                # isso que o Gui viu no playtest. A chave agora e a ASSINATURA
                # do desenho (forma mais metatiles), que e o que o jogador ve.
                if por_carimbo[assinatura(e)] >= TETO_POR_CARIMBO:
                    continue
                if not cabe(e, x, y):
                    continue
                posto = []
                for dx, dy, mt, col, elev in e["cel"]:
                    j = (y + dy) * W + x + dx
                    novo = ((elev << 12) | (col << 10) | mt) if e["solido"] \
                        else ((aplicado[j] & 0xFC00) | mt)
                    posto.append((j, aplicado[j], novo, (x + dx, y + dy)))
                if e["solido"]:
                    for j, _velho, novo, _c in posto:
                        aplicado[j] = novo
                    marcados = novos_solidos + [c for _, _, _, c in posto]
                    # PORTAO POR CARIMBO, e nao so no fim: em CelesticTown um
                    # objeto tapava a boca de um beco de 3 celulas. Conferir
                    # aqui deixa o gerador DESISTIR daquele carimbo e seguir.
                    if (antes - alcance(aplicado, W, H, ini)) - set(marcados):
                        for j, velho, _novo, _c in posto:
                            aplicado[j] = velho
                        continue
                    novos_solidos += [c for _, _, _, c in posto]
                else:
                    for j, _velho, novo, _c in posto:
                        aplicado[j] = novo
                for j, _velho, novo, _c in posto:
                    escritas[j] = novo
                postos.append((x, y, tipo))
                por_carimbo[assinatura(e)] += 1
                contas[tipo] += 1
                break

    depois = alcance(aplicado, W, H, ini)
    perdidas = antes - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d celulas ficariam inalcancaveis, ex.: %s"
                         % (alvo, len(perdidas), sorted(perdidas)[:6]))
    for x, y in eventos(d):
        if (x, y) in antes and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcancavel" % (alvo, x, y))
    return L, W, H, v, escritas, contas["solido"], contas["canteiro"]


# ------------------------------------------------------------- leitura/escrita
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(alvo, guardado):
    """O `map.bin` SEM o desenho desta ferramenta, para replanejar sobre ele."""
    d, L, W, H, v = grade(alvo)
    reg = guardado.get(alvo)
    if not reg:
        return v
    v = list(v)
    for idx, antigo, novo in reg["celulas"]:
        if v[idx] == novo:
            v[idx] = antigo
    return v


def distintos(v):
    return len({c & 0x3FF for c in v})


def _liso(v, beh):
    AG = agua()
    f = collections.Counter(c & 0x3FF for c in v
                            if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG)
    n = sum(f.values())
    return 100.0 * f.most_common(1)[0][1] / n if n else 0.0


def grava(alvo, L, saida):
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(saida), *saida))


def desfaz(alvos):
    guardado = carrega_plano()
    for alvo in alvos:
        if alvo not in guardado:
            continue
        d, L, W, H, v = grade(alvo)
        v = list(v)
        n = 0
        for idx, antigo, novo in guardado[alvo]["celulas"]:
            if v[idx] == novo:
                v[idx] = antigo
                n += 1
        grava(alvo, L, v)
        print("desfeito %-16s %d celulas" % (alvo, n))
        guardado.pop(alvo)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    return 0


def roda(alvos, aplicar):
    guardado = carrega_plano()
    for alvo in alvos:
        base = base_de(alvo, guardado)
        L, W, H, v, escritas, n_obj, n_can = plano(alvo, base)
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        print("%-16s %-38s %2d objetos, %2d canteiros, %4d celulas | "
              "liso %.1f%% -> %.1f%% | distintos %d -> %d"
              % (alvo, TEMAS[alvo][:38], n_obj, n_can, len(escritas),
                 _liso(v, beh), _liso(saida, beh), distintos(v), distintos(saida)))
        guardado[alvo] = {"tema": TEMAS[alvo],
                          "celulas": [[i, v[i], escritas[i]] for i in sorted(escritas)]}
        registra_desenho(alvo, guardado[alvo]["celulas"])
        if aplicar:
            grava(alvo, L, saida)
    if aplicar:
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("plano gravado em", os.path.relpath(PLANO, RAIZ))
    return guardado


def rotas_intactas():
    """Todo caso da suite que entra numa cidade enfeitada tem que TERMINAR NO
    MESMO TILE antes e depois do desenho.

    O congelamento de `corredores_de_teste` e uma promessa de entrada ("nao
    carimbe aqui"); este e o cobrador de SAIDA, e ele mede a coisa que importa,
    que e o destino da perna saturante. Vale para as ONZE cidades, e nao so para
    as cinco do resto do `--demo`, porque e conta de grade e nao custa emulador.
    """
    import glob
    mau = []
    for alvo in TEMAS:
        d, L, W, H, v = grade(alvo)
        base = base_de(alvo, carrega_plano())
        for reg in (json.load(open(PLANO_PORTO)) if os.path.exists(PLANO_PORTO) else {},):
            for i, a, n in reg.get(alvo, {}).get("celulas", []):
                if base[i] == n:
                    base[i] = a
        obj = {(o["x"], o["y"]) for o in (d.get("object_events") or [])}
        warps = d.get("warp_events") or []
        nome_mapa = "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_",
                                    d.get("name", alvo)).upper().replace("__", "_")

        def anda(grade_, x, y, pernas, olhando):
            for direcao, k in pernas:
                dx, dy = direcao
                passos = k - 1 if olhando != direcao else k
                olhando = direcao
                for _ in range(max(0, passos)):
                    nx, ny = x + dx, y + dy
                    if not (0 <= nx < W and 0 <= ny < H):
                        break
                    j = ny * W + nx
                    if (grade_[j] >> 10) & 3 or (nx, ny) in obj:
                        break
                    ea = (grade_[y * W + x] >> 12) & 0xF
                    eb = (grade_[j] >> 12) & 0xF
                    if ea and eb and ea != eb:
                        break
                    x, y = nx, ny
            return (x, y)

        for arq in sorted(glob.glob(f"{RAIZ}/dev_scripts/testes_criticos/*.json")):
            if os.path.basename(arq) == BLOCO_PROPRIO:
                continue
            for caso in json.load(open(arq)):
                if caso.get("warp") != nome_mapa:
                    continue
                wid = int(caso.get("warp_id", 0) or 0)
                if wid >= len(warps):
                    continue
                pernas = []
                for tok in (caso.get("roteiro") or "").split(","):
                    m = _LEG.match(tok.strip())
                    if m:
                        pernas.append(({"UP": (0, -1), "DOWN": (0, 1),
                                        "LEFT": (-1, 0), "RIGHT": (1, 0)}[m.group(1)],
                                       int(m.group(2) or 1)))
                if not pernas:
                    continue
                w = warps[wid]
                for p in ((w["x"], w["y"]), (w["x"], w["y"] + 1)):
                    if not (0 <= p[0] < W and 0 <= p[1] < H):
                        continue
                    for olhando in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                        antes = anda(base, p[0], p[1], pernas, olhando)
                        depois = anda(v, p[0], p[1], pernas, olhando)
                        if antes != depois:
                            mau.append("%s: o caso %s parava em %s e passou a "
                                       "parar em %s (pouso %s)"
                                       % (alvo, caso["id"], antes, depois, p))
    return sorted(set(mau))


def demo():
    mau = []
    alvos = ["CanalaveCity", "CelesticTown", "SolaceonTown", "BlackthornCity",
             "SnowpointCity"]
    guardado = carrega_plano()
    AG = agua()
    for alvo in alvos:
        base = base_de(alvo, guardado)
        L, W, H, v, escritas, n_obj, n_can = plano(alvo, base)
        beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
        d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
        ev = eventos(d)
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val

        # 1. nenhuma celula de evento (nem a orla) foi escrita
        for i in escritas:
            if (i % W, i // W) in ev:
                mau.append("%s: escreveu no evento (%d,%d)" % (alvo, i % W, i // W))

        # 2. canteiro nao mexe nos 6 bits de cima, e mantem o comportamento
        for i, val in escritas.items():
            if (val & 0xFC00) == (v[i] & 0xFC00):
                if beh(val & 0x3FF) != beh(v[i] & 0x3FF):
                    mau.append("%s: comportamento mudou sem mudar colisao em %d"
                               % (alvo, i))

        # 3. nada foi escrito na AGUA: era o defeito da primeira versao
        for i in escritas:
            if beh(v[i] & 0x3FF) in AG:
                mau.append("%s: carimbou na agua em (%d,%d)" % (alvo, i % W, i // W))

        # 4. quem virou solido era andavel, e nenhum warp/NPC ficou ilhado
        #    (o `plano` ja levanta se ilhar; aqui so se cobra que ele checou)
        ini = partidas(d, W, H, v)
        if (alcance(v, W, H, ini) - alcance(saida, W, H, ini)) - {
                (i % W, i // W) for i, val in escritas.items()
                if ((val >> 10) & 3) and not ((v[i] >> 10) & 3)}:
            mau.append("%s: alguem ficou inalcancavel" % alvo)

        # 5. idempotente: desfazer devolve a base, e replanejar da o MESMO plano
        base2 = list(saida)
        for idx in sorted(escritas):
            if base2[idx] == escritas[idx]:
                base2[idx] = v[idx]
        if base2 != list(v):
            mau.append("%s: desfazer nao devolve a base" % alvo)
        _, _, _, _, escritas2, _, _ = plano(alvo, base2)
        if escritas2 != escritas:
            mau.append("%s: segunda passada deu plano diferente (%d vs %d)"
                       % (alvo, len(escritas2), len(escritas)))

        # 6. a rodada tem que ADICIONAR desenho, e nunca tirar vocabulario
        if distintos(saida) < distintos(v):
            mau.append("%s: vocabulario encolheu (%d -> %d)"
                       % (alvo, distintos(v), distintos(saida)))
        # O piso era 5, e ele nasceu quando o teto por carimbo era 6: bastava um
        # carimbo servir para a cidade passar. Com o teto em 2 (a poda que o Gui
        # pediu em 07/09/2026) o piso passa a ser o proprio teto, porque
        # BlackthornCity tem UMA assinatura util no catalogo e sai com 2. O que
        # este caso ainda cobra e o que ele sempre cobrou de verdade: que o
        # gerador nao tenha parado de desenhar calado.
        if n_obj + n_can < TETO_POR_CARIMBO:
            mau.append("%s: so %d enfeites" % (alvo, n_obj + n_can))

        # 7. o catalogo tem que ter objeto solido, senao a cidade so ganha
        #    canteiro e o portao de alcance nunca e exercitado
        cat = catalogo_de(alvo, L)
        if not any(e["solido"] for e in cat):
            mau.append("%s: catalogo sem nenhum objeto solido" % alvo)

        # 8. REGRA DE BEIRA, cobrada na saida e nao na intencao: toda celula que
        #    virou solida tem que encostar em algo que JA era solido ou em outra
        #    celula do mesmo carimbo. E o que impede o barril plantado no meio da
        #    praca, e e verificavel de fora do gerador.
        virou = {(i % W, i // W) for i, val in escritas.items()
                 if ((val >> 10) & 3) and not ((v[i] >> 10) & 3)}
        for x, y in virou:
            encosta = False
            for dx, dy in N4:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    continue
                if ((v[ny * W + nx] >> 10) & 3) or (nx, ny) in virou:
                    encosta = True
            if not encosta:
                mau.append("%s: objeto solto no meio do chao em (%d,%d)" % (alvo, x, y))

        # 9. DOADOR ENTRA SEM ENFEITE, e este caso e o que faltava: o caso 5 so
        #    olha o mapa alvo, entao ele ficava VERDE com o gerador nao sendo
        #    idempotente. Cidade enfeitada tambem e doadora (Eterna aprende com
        #    Oreburgh pelo caminho de mesmo primario), e ler o doador ja
        #    desenhado fazia o catalogo crescer a cada rodada: medido em
        #    06/09/2026, Oreburgh saiu com 45, 51 e 57 celulas em tres rodadas
        #    seguidas sobre a MESMA base. Aqui se cobra o contrario: nenhuma
        #    celula de enfeite de doador nenhum chega ao catalogo.
        for nome in doadores_de(alvo) + doadores_de(alvo, so_primario=True):
            reg = _desenhos().get(nome)
            if not reg:
                continue
            vb = grade_base(nome)[4]
            sujo = [i for i, (a, n) in reg.items() if a != n and vb[i] == n]
            if sujo:
                mau.append("%s: doador %s entrou com %d celulas de enfeite"
                           % (alvo, nome, len(sujo)))

    # 10. NENHUM caso da suite muda de destino por causa do desenho. O caso 9 do
    #     `corredores_de_teste` promete "nao carimbo no caminho"; este mede o
    #     resultado. Ele nasceu de um vermelho de verdade: o T94.1 quebrou em
    #     06/09/2026 porque o corredor simulava so a partir do TILE DO WARP, e o
    #     warp 2 de CelesticTown e uma PORTA que nao anda; na ROM o jogador
    #     pousa um tile ao sul e atravessa a cidade inteira.
    mau += rotas_intactas()

    if mau:
        print("DEMO VERMELHA")
        for x in mau:
            print("  -", x)
        return 1
    print("DEMO VERDE: %d cidades, 9 casos cada, mais o caso 10 nas %d cidades"
          % (len(alvos), len(TEMAS)))
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    alvos = list(TEMAS)
    if "--cidade" in sys.argv:
        alvos = [sys.argv[sys.argv.index("--cidade") + 1]]
    if "--desfazer" in sys.argv:
        return desfaz(alvos)
    roda(alvos, "--aplicar" in sys.argv)
    for nome, motivo in sorted(NAO_SERVIDAS.items()):
        print("%-16s MEDIDA E NAO SERVIDA: %s" % (nome, motivo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
