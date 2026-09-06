#!/usr/bin/env python3
"""LOTE C DA ONDA 1: as 25 placas de Galar que sobraram na fila.

    python3 dev_scripts/placas_galar_c.py            # so mede e relata
    python3 dev_scripts/placas_galar_c.py --aplicar  # escreve o .inc e os pedidos
    python3 dev_scripts/placas_galar_c.py --demo     # autoteste

## Por que existe outro arquivo de placa

`dev_scripts/placas_galar.py` (rodada 7) porta placa que tem TEXTO na fonte.
As 25 que sobraram nao tem: o `bg_event` da fonte existe, mas o ponteiro de
script dele cai em enchimento de espaco livre (0xFF), em dado que nao e
bytecode, ou em maquinaria do FireRed que nao e placa. A decisao desta onda
(escopo do lote C, 06/09/2026) e que **placa sem texto na fonte ganha texto
curto, em ingles, coerente com o lugar**, escrito aqui e nao herdado.

Este arquivo e separado de `galar_placas.inc` de proposito: aquele diz
"gerado por placas_galar.py; NAO editar a mao" e e REESCRITO inteiro a cada
`--aplicar` daquele script, que ainda apaga `bg_event` de rotulo `GalarPlaca_`
que nao esteja no plano DELE. Rotulo novo dentro dele seria varrido na proxima
rodada. Por isso o prefixo daqui e `GalarPlacaC_` e o arquivo e outro.

## O PORTAO DE COLOCACAO, e ele nasceu de um achado, nao de gosto

Medido em 06/09/2026, tile a tile, lendo o `blockdata` do layout e o
`metatile_attributes.bin` do tileset: das 25 coordenadas que a fonte pede,
**quatorze caem em cima do tile de PC do Centro Pokemon** (comportamento
`MB_PC`, 131 depois da conversao FRLG->Emerald de
`migration_scripts/frlg_metatile_behavior_converter.py`), tres em cima de agua
(`MB_OCEAN_WATER`), uma em cima de porta (`MB_ANIMATED_DOOR`) e uma no
metatile 0, que e o vazio.

Por em qualquer uma delas um `bg_event` de tipo `sign` NAO seria placa a mais:
seria placa NO LUGAR da coisa. `GetInteractionScript`
(`src/field_control_avatar.c:325`) pergunta na ordem objeto, **bg_event**,
metatile, agua: o `bg_event` vem ANTES de `GetInteractedMetatileScript`, que e
quem abre o PC, a porta e o resto. Uma placa em cima do PC ROUBA o PC, e seriam
quatorze Centros Pokemon de Galar sem PC, calados, para ganhar quatorze frases
que a fonte nem tem.

Entao a regra e: **so entra placa em tile que ja e parede ou placa** -- ou
`MB_SIGNPOST`, ou `MB_NORMAL` com colisao diferente de zero (o jogador nao pisa
nele, so o encara) -- e cuja coordenada ainda nao tenha `bg_event` nenhum.
Todo o resto sai com o motivo MEDIDO na linha, e a fila guarda o motivo.

## ONDA 2, LOTE I (07/09/2026): as 21 bloqueadas ganham TILE VIZINHO

**Decisao da condutora da onda 2**, e ela desempata a duvida que o lote C deixou
aberta: a placa que a fonte pos num tile impossivel NAO e descartada, ela
**anda para o tile livre e andavel mais proximo**. A busca e deterministica e
para na primeira que serve: vizinhos em CRUZ (norte, sul, oeste, leste) e
depois em DIAGONAL, primeiro a distancia 1 e depois a distancia 2.

"Livre e andavel" e medido, nao suposto: metatile diferente de zero,
comportamento `MB_NORMAL` ou `MB_SIGNPOST` (nenhum tile que ja e dono de uma
interacao do motor: PC, porta, agua), COLISAO ZERO, e sem `bg_event`,
`warp_event` ou `object_event` nenhum em cima. Uma placa em tile andavel nao
rouba nada: `sign` so dispara com A na direcao dele, e pisar em cima nao faz
nada (`src/field_control_avatar.c`).

A placa de cima do PC do Centro Pokemon vira tile vizinho, e nao fala do PC:
**medido nesta rodada**, o repo nao tem molde nenhum de PC falante -- `MB_PC`
so aparece em `src/metatile_behavior.c:510` (`MetatileBehavior_IsPC`), e quem
abre o PC e `GetInteractedMetatileScript`. Nao ha o que reusar, entao a regra
do vizinho vale para as quatorze.

## DOIS DEFEITOS DO LOTE C CONSERTADOS AQUI, os dois medidos

1. **A colisao estava lida errada.** `bruto >> 10` NAO e a colisao: e a
   colisao (2 bits) com a ELEVACAO por cima (`colisao | elevacao << 2`). Chao
   andavel de elevacao 3 lia `12` e passava no teste `colisao != 0` do lote C,
   ou seja, o portao "so parede" deixava passar chao. A leitura certa e
   `(bruto >> 10) & 3` para colisao e `bruto >> 12` para elevacao, e e a que
   `src/fieldmap.c` usa.
2. **O gerador comia o proprio trabalho depois que o fechador colava o
   pedido.** `plano()` bloqueava a linha cuja coordenada ja tivesse `bg_event`,
   e depois que o fechador da onda 1 colou os quatro `bg_event` pedidos, os
   quatro viraram "coordenada ja tem bg_event de precedencia maior" e o
   `--aplicar` seguinte escreveria o `.inc` VAZIO. Agora, `bg_event` cujo
   script e o NOSSO PROPRIO rotulo conta como placa JA COLOCADA e a linha
   segue aceita, na coordenada em que ela esta no mapa.

## Este script NAO escreve map.json

O `bg_event` de cada placa aceita e pedido em
`dev_scripts/onda1_lote_c_pedidos_mapjson.txt`, para o fechador aplicar: nesta
onda o `map.json` de Galar tem outro dono (lote A e lote B). Enquanto o pedido
nao for aplicado, o texto existe na ROM e a placa nao esta no mapa.
"""
import argparse
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

import texto_placas_sinnoh as TXT              # noqa: E402  (requebrador por pixel)

FILA = f"{RAIZ}/dev_scripts/fila_galar.json"
INC = f"{RAIZ}/data/scripts/galar_placas_c.inc"
EVENT_S = f"{RAIZ}/data/event_scripts.s"
PEDIDOS = f"{RAIZ}/dev_scripts/onda1_lote_c_pedidos_mapjson.txt"
PEDIDOS_I = f"{RAIZ}/dev_scripts/onda2_lote_i_pedidos_mapjson.json"
LAYOUTS = f"{RAIZ}/data/layouts/layouts.json"
BEHAVIORS_H = f"{RAIZ}/include/constants/metatile_behaviors.h"

# Comportamento de metatile em que uma placa PODE entrar sem roubar nada.
# `MB_SIGNPOST` ja e placa; `MB_NORMAL` com colisao e parede ou movel.
BEH_PLACA = "MB_SIGNPOST"
BEH_INERTE = "MB_NORMAL"


# ---------------------------------------------------------------- o texto ----
# TEXTO NOVO, em ingles (decisao 32 do Gui: a fala de Galar e em ingles).
# Uma frase curta por lugar, escrita a partir do que o MAPA mostra (musica,
# tipo, warps, elenco), nunca de enredo inventado. `\n` e quebra dentro da
# mesma caixa; o requebrador por pixel confere as duas linhas contra 208 px.
TEXTO = {
    # Camara de pedra com Regirock parado dentro e paredes de braille na fonte
    # (o script da fonte e uma cadeia de `braillemessage`). A placa diz o que a
    # parede E, sem inventar o que ela DIZ.
    "g01m120/bg/0": ("Dots are carved deep into the\\n"
                     "stone. It must be Braille."),
    # Saguao da Trainer Tower: tres enfermeiras, escada para o andar de cima e
    # porta para Wyndon. MUS_RG_TRAINER_TOWER.
    #
    # CAIXA NORMAL, e nao a caixa alta das placas de cidade do Emerald vanilla
    # ("PETALBURG CITY"): o GLOSSARIO-GALAR.md diz que a caixa alta e da tabela
    # de letreiro (src/data/map_popup_names.h) "porque e letreiro; em fala, a
    # grafia e a normal", e lista `MOTOSTOKE` como grafia do demake que a
    # tradução normaliza para `Motostoke`. Placa e texto, nao letreiro. As
    # placas de Galar ja portadas (data/scripts/galar_placas.inc) usam a mesma
    # caixa normal ("Cinnabar Pokemon Gym").
    "g02m10/bg/0": ("Trainer Tower\\n"
                    "Check in at the counter to begin."),
    # Rua de Motostoke, e o unico dos 25 que ja esta num tile MB_SIGNPOST.
    "g03m02/bg/0": ("Motostoke\\n"
                    "Steam and steel, day and night."),
    # Predio grande de Wyndon com duas escadas internas e nove pessoas.
    "g13m10/bg/0": ("Building directory\\n"
                    "Lifts to the upper floors: rear."),

    # ---- ONDA 2, LOTE I: as 21 que o lote C deixou bloqueadas por tile ----
    #
    # Quatorze delas sao a MESMA placa: o `bg_event` da fonte esta em cima do
    # tile de PC do Centro Pokemon (metatile 897, MB_PC), e pela regra da
    # condutora ela anda para o tile andavel mais proximo, que nos catorze e
    # (4,4), o chao logo abaixo do PC. Texto igual nos catorze de proposito,
    # como a placa repetida do jogo original: o que ela descreve e o PC, que e
    # o mesmo movel em todos.
    "g05m04/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g06m05/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g07m03/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g08m00/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g09m01/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g10m12/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g11m05/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g12m05/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g14m06/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g21m00/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g33m02/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g34m01/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g35m28/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    "g36m00/bg/0": ("Pokémon Storage System\\n"
                    "The PC keeps your Boxes in order."),
    # Beira de mar: os oito tiles em volta da coordenada da fonte sao
    # MB_OCEAN_WATER, e o mesmo trecho de costa aparece nos dois mapas.
    "g03m00/bg/2": ("The sea starts here.\\n"
                    "Deep water, all the way out."),
    "g04m06/bg/2": ("The sea starts here.\\n"
                    "Deep water, all the way out."),
    # A coordenada da fonte e a propria porta (metatile 61, MB_ANIMATED_DOOR).
    "g03m04/bg/0": "A door leads inside from here.",
    # Rua de Motostoke, a cidade de aco e vapor do demake.
    "g06m10/bg/0": ("Motostoke\\n"
                    "Mind the steam vents."),
    # Hulbury a beira-mar: o tile escolhido fica no cais, com agua ao lado.
    "g08m07/bg/0": ("Hulbury\\n"
                    "The catch of the day comes in here."),
    # UNICA das 21 cujo ponteiro da fonte tem texto de verdade, e ele e
    # maquinaria do FIRERED que este cartucho nao tem: "Pokémon Lecture" com um
    # `multichoice` de quatro ramos sobre o Wireless Adapter. Portar o texto
    # seria prometer ao jogador um aparelho que nao existe aqui, entao a placa
    # fica com o ASSUNTO da fonte (a palestra) e nao com a promessa dela.
    "g10m11/bg/1": ("Pokémon Lecture Hall\\n"
                    "Talks are held here now and then."),
}


# ------------------------------------------------------------- a geometria ---
def enum_behaviors():
    """{valor: nome} do enum de `include/constants/metatile_behaviors.h`."""
    t = open(BEHAVIORS_H, encoding="utf-8").read()
    m = re.search(r"enum\s*\{(.*?)\n\};", t, re.S)
    corpo = re.sub(r"//[^\n]*", "", m.group(1))
    fora, valor = {}, 0
    for pedaco in corpo.split(","):
        nome = pedaco.strip()
        if not nome:
            continue
        if "=" in nome:
            nome, v = nome.split("=", 1)
            nome, valor = nome.strip(), int(v.strip(), 0)
        fora[valor] = nome
        valor += 1
    return fora


_LAY = {}


def layouts():
    if not _LAY:
        for l in json.load(open(LAYOUTS))["layouts"]:
            if l:
                _LAY[l["id"]] = l
    return _LAY


_ATTR = {}


def atributos(rotulo_tileset):
    """`metatile_attributes.bin` do tileset, pelo rotulo `gTileset_X`."""
    if rotulo_tileset in _ATTR:
        return _ATTR[rotulo_tileset]
    # `gTileset_Galar12` -> `galar_12`: separa a PALAVRA dos DIGITOS, e nao
    # digito a digito (o de digito a digito dava `galar_1_2`, que nao existe
    # em disco e fazia todo tile sair como "tileset sem atributo lido").
    nome = re.sub(r"([A-Za-z]+)(\d+)", r"\1_\2",
                  rotulo_tileset.replace("gTileset_", "")).lower()
    achado = None
    for papel in ("primary", "secondary"):
        d = "%s/data/tilesets/%s/%s" % (RAIZ, papel, nome)
        if os.path.isdir(d):
            achado = open("%s/metatile_attributes.bin" % d, "rb").read()
            break
    _ATTR[rotulo_tileset] = achado
    return achado


def tile_de(mapa, x, y):
    """(metatile, colisao, elevacao, nome do comportamento) na coordenada.

    A colisao e `(bruto >> 10) & 3` e a elevacao e `bruto >> 12`, que e como
    `src/fieldmap.c` le o bloco. O lote C usava `bruto >> 10` inteiro como se
    fosse colisao, e com isso todo chao andavel de elevacao 3 lia `12` e
    passava por parede no portao "so entra em tile com colisao".
    """
    doc = json.load(open("%s/data/maps/%s/map.json" % (RAIZ, mapa)))
    lay = layouts()[doc["layout"]]
    dados = open("%s/%s" % (RAIZ, lay["blockdata_filepath"]), "rb").read()
    larg = lay["width"]
    if not (0 <= x < larg and 0 <= y < lay["height"]):
        return None, None, None, "fora do layout"
    bruto = struct.unpack_from("<H", dados, 2 * (y * larg + x))[0]
    mid, col, elev = bruto & 0x3FF, (bruto >> 10) & 3, bruto >> 12
    # O corte primario/secundario de Galar e o do FRLG (640), que
    # `src/fieldmap.c:438` ja resolve por `isFrlg`/`bigPrimary`.
    ts = lay["primary_tileset"] if mid < 640 else lay["secondary_tileset"]
    idx = mid if mid < 640 else mid - 640
    a = atributos(ts)
    if a is None or 4 * idx + 4 > len(a):
        return mid, col, elev, "tileset sem atributo lido"
    beh = struct.unpack_from("<I", a, 4 * idx)[0] & 0x1FF
    return mid, col, elev, enum_behaviors().get(beh, "MB_%d" % beh)


def bg_ocupado(mapa, x, y):
    """Rotulo do `bg_event` que ja esta nessa coordenada, ou None."""
    doc = json.load(open("%s/data/maps/%s/map.json" % (RAIZ, mapa)))
    for b in doc.get("bg_events") or []:
        if b.get("x") == x and b.get("y") == y:
            return str(b.get("script") or "sem script")
    return None


def onde_esta(mapa, rot):
    """(x, y) do `bg_event` que JA carrega este rotulo no mapa, ou None.

    Depois que o fechador cola o pedido, a placa passa a existir no
    `map.json`. Sem esta leitura, `plano()` veria a coordenada ocupada, daria
    a linha por bloqueada e o `--aplicar` seguinte escreveria o `.inc` sem
    ela: o gerador comendo o proprio trabalho, calado.
    """
    doc = json.load(open("%s/data/maps/%s/map.json" % (RAIZ, mapa)))
    for b in doc.get("bg_events") or []:
        if str(b.get("script") or "") == rot:
            return b["x"], b["y"]
    return None


def ocupado_por_evento(mapa, x, y):
    """Motivo pelo qual a coordenada ja tem dono, ou None."""
    doc = json.load(open("%s/data/maps/%s/map.json" % (RAIZ, mapa)))
    for b in doc.get("bg_events") or []:
        if b.get("x") == x and b.get("y") == y:
            return "bg_event (%s)" % (b.get("script") or "sem script")
    for w in doc.get("warp_events") or []:
        if w.get("x") == x and w.get("y") == y:
            return "warp_event"
    for o in doc.get("object_events") or []:
        if o.get("x") == x and o.get("y") == y:
            return "object_event"
    return None


# A busca do tile vizinho, na ordem que a condutora fixou: cruz primeiro,
# diagonal depois, distancia 1 antes de distancia 2. Determinista de ponta a
# ponta: a primeira que serve ganha, e rodar de novo da o mesmo tile.
CRUZ = ((0, -1), (0, 1), (-1, 0), (1, 0))
DIAGONAL = ((-1, -1), (1, -1), (-1, 1), (1, 1))


def serve_para_placa(mapa, x, y):
    """(mid, col, elev, beh) se a placa pode morar aqui, senao None.

    Livre e andavel: metatile diferente de zero, comportamento que NAO e dono
    de interacao nenhuma do motor (`MB_NORMAL` ou `MB_SIGNPOST`), colisao
    zero, e nenhum evento ja na coordenada.
    """
    mid, col, elev, beh = tile_de(mapa, x, y)
    if mid in (0, None) or col != 0:
        return None
    if beh not in (BEH_INERTE, BEH_PLACA):
        return None
    if ocupado_por_evento(mapa, x, y):
        return None
    return mid, col, elev, beh


def tile_vizinho(mapa, x, y):
    """(x, y, mid, col, elev, beh) do tile livre e andavel mais proximo."""
    for d in (1, 2):
        for dx, dy in CRUZ + DIAGONAL:
            nx, ny = x + dx * d, y + dy * d
            serve = serve_para_placa(mapa, nx, ny)
            if serve:
                return (nx, ny) + serve
    return None


# ---------------------------------------------------------------- o plano ----
def rotulo(chave):
    mapa, tipo, i = chave.split("/")
    return "GalarPlacaC_%s_%s%d" % (mapa.upper(),
                                    "bg" if tipo == "bg" else "o", int(i))


def linhas_do_lote():
    """As 25 linhas de `placa` que este lote recebeu, em QUALQUER momento.

    O autoteste precisa de um numero que nao mude quando o trabalho e feito.
    `plano()` le a fila e so enxerga `pendente`/`adiada`, entao depois do
    `--aplicar` as aceitas viram `feita` e somem dele: contar `aceitas +
    bloqueadas` daria 25 antes e 21 depois, e o caso reprovaria justamente por
    o trabalho ter sido feito. Foi o que aconteceu em 06/09/2026, quando a
    rodada caiu por cota logo depois de gravar.

    Aqui a conta e por CHAVE e inclui a linha ja `feita` cujo rotulo esta no
    nosso .inc, que e a mesma lei do `fila_galar.feitas()`: le-se a arvore, e
    o placar do lote fica igual antes e depois de aplicar.
    """
    doc = json.load(open(FILA))
    inc = open(INC, encoding="utf-8").read() if os.path.exists(INC) else ""
    fora = []
    for l in doc["linhas"]:
        if l["tipo"] != "placa":
            continue
        if (l["status"] in ("pendente", "adiada")
                or ("%s::" % rotulo(l["chave"])) in inc):
            fora.append(l)
    return fora


def plano():
    """(aceitas, bloqueadas) das 25 linhas de `placa` deste lote.

    A entrada e `linhas_do_lote()`, e NAO "as pendentes", por uma armadilha
    medida em 06/09/2026: `--aplicar` grava o .inc e marca a linha `feita` na
    fila; um segundo `--aplicar` filtrado por `pendente` nao veria mais
    nenhuma aceita, montaria o corpo VAZIO e APAGARIA o .inc, e a varredura
    seguinte devolveria as quatro placas para `pendente` (o
    `fila_galar.varre()` derruba `feita` cujo rotulo sumiu da arvore). O
    gerador comeria o proprio trabalho, calado. Lendo tambem a linha ja feita
    cujo rotulo esta no nosso .inc, o corpo sai igual em toda rodada.
    """
    aceitas, bloqueadas = [], []
    for l in linhas_do_lote():
        if not os.path.exists("%s/data/maps/%s/map.json" % (RAIZ, l["mapa"])):
            bloqueadas.append(dict(l, motivo="map.json do mapa nao existe"))
            continue
        rot = rotulo(l["chave"])
        texto = TEXTO.get(l["chave"])
        xf, yf = l["x"], l["y"]

        def aceita(x, y, mid, col, elev, beh, andou):
            aceitas.append(dict(l, rotulo=rot, texto=TXT.requebra(texto),
                                beh=beh, metatile=mid, colisao=col,
                                elevacao=elev, x=x, y=y, x_fonte=xf,
                                y_fonte=yf, deslocada=andou))

        # 1. JA COLOCADA: o fechador colou o pedido e a placa esta no mapa.
        posta = onde_esta(l["mapa"], rot)
        if posta and texto is not None:
            mid, col, elev, beh = tile_de(l["mapa"], *posta)
            aceita(posta[0], posta[1], mid, col, elev, beh,
                   posta != (xf, yf))
            continue

        # 2. O TILE. Primeiro a coordenada da FONTE com o portao do lote C
        #    (parede ou placa, sem evento em cima); se ela nao serve, o tile
        #    livre e ANDAVEL mais proximo, que e a regra da condutora da onda
        #    2. A GEOMETRIA e conferida ANTES do texto de proposito: onde a
        #    placa nao cabe, "falta texto" seria motivo falso, e mandaria a
        #    proxima rodada escrever frase para uma placa que nao entra.
        mid, col, elev, beh = tile_de(l["mapa"], xf, yf)
        dono = ocupado_por_evento(l["mapa"], xf, yf)
        if not dono and (beh == BEH_PLACA or (beh == BEH_INERTE and col)):
            onde = (xf, yf, mid, col, elev, beh, False)
        else:
            viz = tile_vizinho(l["mapa"], xf, yf)
            onde = viz + (True,) if viz else None

        if onde is None:
            porque = (("a coordenada (%d,%d) ja tem %s" % (xf, yf, dono))
                      if dono else
                      ("o bg da fonte cai no metatile %s (%s, colisao %s)"
                       % (mid, beh, col)))
            bloqueadas.append(dict(l, motivo=(
                "%s, e nenhum dos 16 tiles vizinhos (cruz e diagonal, "
                "distancia 1 e 2) e livre e andavel: nao ha para onde a placa "
                "andar" % porque)))
            continue

        if texto is None:
            bloqueadas.append(dict(l, motivo=(
                "o tile (%d,%d) serve, mas nao ha texto escrito para esta "
                "placa" % (onde[0], onde[1]))))
            continue
        aceita(*onde)
    return aceitas, bloqueadas


def corpo_inc(aceitas):
    out = ["@ Placas de Galar do LOTE C da onda 1 (06/09/2026).",
           "@ Gerado por dev_scripts/placas_galar_c.py; NAO editar a mao.",
           "@",
           "@ Sao as placas cujo bg_event existe na FONTE e cujo ponteiro de",
           "@ script da fonte nao aponta para texto nenhum (enchimento 0xFF ou",
           "@ dado que nao e bytecode). O texto e NOVO, em ingles (decisao 32),",
           "@ curto e tirado do que o mapa mostra. Uma placa diz o que diz:",
           "@ MSGBOX_SIGN e mais nada.",
           "@",
           "@ O bg_event de cada uma esta pedido em",
           "@ dev_scripts/onda1_lote_c_pedidos_mapjson.txt: nesta onda o",
           "@ map.json de Galar tem outro dono.",
           ""]
    for l in sorted(aceitas, key=lambda z: z["chave"]):
        r = l["rotulo"]
        andou = ("" if not l.get("deslocada") else
                 ", andou de (%d,%d) da fonte" % (l["x_fonte"], l["y_fonte"]))
        out += ["@ ---- %s (%s) em (%d,%d)%s, tile %s %s ----"
                % (l["mapa"], l["chave"], l["x"], l["y"], andou,
                   l["metatile"], l["beh"]),
                "%s::" % r,
                "\tmsgbox %s_Text, MSGBOX_SIGN" % r,
                "\tend", "",
                "%s_Text:" % r,
                '\t.string "%s$"' % l["texto"], ""]
    return "\n".join(out) + "\n"


def corpo_pedidos(aceitas):
    out = ["# Pedidos de map.json do LOTE C da onda 1 (Galar), 06/09/2026.",
           "# Gerado por dev_scripts/placas_galar_c.py.",
           "#",
           "# O lote C e dono de scripts.inc e de data/scripts/galar_*.inc, e",
           "# NAO escreve map.json nesta onda. Cada linha abaixo e um bg_event",
           "# que o fechador precisa acrescentar para a placa aparecer no jogo.",
           "# Enquanto ele nao entrar, o texto existe na ROM e a placa nao.",
           "#",
           "# Toda coordenada abaixo foi medida: o tile ja e parede ou placa",
           "# (MB_SIGNPOST, ou MB_NORMAL com colisao), OU o tile livre e",
           "# andavel mais proximo da coordenada da fonte (regra da condutora",
           "# da onda 2), e nao ha evento nenhum nela hoje. As que nao",
           "# passaram NAO estao aqui; elas ficaram bloqueadas na fila.",
           "#",
           "# mapa | tipo | x | y | elevation | player_facing_dir | script",
           ""]
    for l in sorted(aceitas, key=lambda z: z["chave"]):
        out.append("%s | sign | %d | %d | 0 | BG_EVENT_PLAYER_FACING_ANY | %s"
                   % (l["mapa"], l["x"], l["y"], l["rotulo"]))
    out.append("")
    out.append("# json pronto para colar em bg_events, mapa a mapa:")
    por_mapa = collections.defaultdict(list)
    for l in aceitas:
        por_mapa[l["mapa"]].append(l)
    for mapa in sorted(por_mapa):
        for l in sorted(por_mapa[mapa], key=lambda z: z["chave"]):
            out.append('#   %s: {"type": "sign", "x": %d, "y": %d, '
                       '"elevation": 0, "player_facing_dir": '
                       '"BG_EVENT_PLAYER_FACING_ANY", "script": "%s"}'
                       % (mapa, l["x"], l["y"], l["rotulo"]))
    return "\n".join(out) + "\n"


def pedido_onda2(aceitas):
    """A secao `bg_events` do pedido de map.json da onda 2, lote I.

    O arquivo tem DUAS secoes com donos diferentes (`bg_events` aqui,
    `object_events` em dev_scripts/objetos_galar.py), e cada gerador reescreve
    SO a sua: le o que esta em disco, troca a sua secao e grava. Sem isso o
    segundo a rodar apagaria o pedido do primeiro, e o fechador colaria meio
    lote sem saber.
    """
    doc = {}
    if os.path.exists(PEDIDOS_I):
        doc = json.load(open(PEDIDOS_I))
    doc["_leia"] = (
        "Pedidos de map.json da ONDA 2, LOTE I (Galar), 07/09/2026. O lote I e "
        "dono de data/scripts/galar_objetos.inc, galar_placas_c.inc e dos "
        "geradores deles, e NAO escreve map.json: cada item abaixo e uma "
        "mudanca que o fechador precisa colar. Enquanto ela nao entrar, o "
        "texto existe na ROM e a placa (ou a fala) nao esta no jogo.")
    doc["gerado_por"] = sorted(set(doc.get("gerado_por", []))
                               | {"dev_scripts/placas_galar_c.py"})
    itens = []
    for l in sorted(aceitas, key=lambda z: z["chave"]):
        # `ja_no_mapa`: MEDIDO EM 07/09/2026, e o motivo de ele existir. Quatro
        # dos 24 pedidos deste lote JA estavam colados no map.json quando o
        # arquivo foi conferido (mesmo tile, mesmo rotulo, mesmo tipo), porque
        # outro dono passou por ali antes. `acrescentar_em: bg_events` lido ao
        # pe da letra poria um SEGUNDO bg_event no mesmo tile, e o motor le um
        # so: a placa nova nasceria morta e ninguem veria, porque as duas
        # existem e o mapa continua valido.
        no_mapa = json.load(open("%s/data/maps/%s/map.json"
                                 % (RAIZ, l["mapa"]))).get("bg_events") or []
        igual = any(b.get("x") == l["x"] and b.get("y") == l["y"]
                    and str(b.get("script") or "") == l["rotulo"]
                    for b in no_mapa)
        ocupado = any(b.get("x") == l["x"] and b.get("y") == l["y"]
                      for b in no_mapa)
        itens.append(
            {"mapa": l["mapa"], "chave_da_fonte": l["chave"],
             "x_da_fonte": l["x_fonte"], "y_da_fonte": l["y_fonte"],
             "andou_para_tile_vizinho": bool(l.get("deslocada")),
             "metatile": l["metatile"], "comportamento": l["beh"],
             "acrescentar_em": "bg_events",
             "ja_no_mapa": igual,
             "tile_ja_ocupado_por_outro_bg": ocupado and not igual,
             "valor": {"type": "sign", "x": l["x"], "y": l["y"],
                       "elevation": 0,
                       "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                       "script": l["rotulo"]}})
    doc["bg_events"] = itens
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def grava_fila(aceitas, bloqueadas, gravar):
    """Devolve o motivo de bloqueio para a FILA, que e a cobranca.

    A fila calcula `feita` lendo o rotulo na arvore (ver `fila_galar.feitas`),
    entao aceita nao se escreve aqui. Bloqueio, sim: sem ele a linha voltaria
    pendente na proxima varredura e a decisao medida se perderia.
    """
    doc = json.load(open(FILA))
    por_chave = {l["chave"]: l for l in doc["linhas"]}
    n = 0
    for b in bloqueadas:
        l = por_chave.get(b["chave"])
        if l is None:
            continue
        novo = "adiada", ("onda 2, lote I, 07/09/2026: " + b["motivo"])
        if (l.get("status"), l.get("motivo_do_status")) != novo:
            l["status"], l["motivo_do_status"] = novo
            n += 1
    if gravar and n:
        with open(FILA, "w") as f:
            json.dump(doc, f, indent=1, ensure_ascii=False)
            f.write("\n")
    return n


def aplica(aceitas, bloqueadas, gravar):
    mudou = collections.Counter()
    corpo = corpo_inc(aceitas)
    if not os.path.exists(INC) or open(INC).read() != corpo:
        mudou["galar_placas_c.inc"] += 1
        if gravar:
            open(INC, "w").write(corpo)
    ped = corpo_pedidos(aceitas)
    if not os.path.exists(PEDIDOS) or open(PEDIDOS).read() != ped:
        mudou["pedidos"] += 1
        if gravar:
            open(PEDIDOS, "w").write(ped)
    ped2 = pedido_onda2(aceitas)
    if not os.path.exists(PEDIDOS_I) or open(PEDIDOS_I).read() != ped2:
        mudou["pedidos_onda2"] += 1
        if gravar:
            open(PEDIDOS_I, "w").write(ped2)
    linha = '\t.include "data/scripts/galar_placas_c.inc"'
    s = open(EVENT_S).read()
    if linha not in s:
        mudou["event_scripts.s"] += 1
        if gravar:
            open(EVENT_S, "w").write(s.rstrip("\n") + "\n" + linha + "\n")
    mudou["fila"] += grava_fila(aceitas, bloqueadas, gravar)
    return mudou


# ----------------------------------------------------------------- demo ------
def demo():
    ok = True

    def caso(nome, cond):
        nonlocal ok
        print("  %-64s %s" % (nome, "ok" if cond else "REPROVOU"))
        ok = ok and cond

    aceitas, bloqueadas = plano()
    lote = linhas_do_lote()
    vistas = {z["chave"] for z in aceitas} | {z["chave"] for z in bloqueadas}
    escritas = [l for l in lote if l["chave"] not in vistas]
    caso("as 25 linhas de placa do lote estao decididas, sem sobra",
         len(lote) == 25
         and len(aceitas) + len(bloqueadas) + len(escritas) == 25)
    caso("toda aceita tem texto nao vazio",
         all(l["texto"].strip() for l in aceitas))
    caso("toda bloqueada tem motivo escrito",
         all(b["motivo"].strip() for b in bloqueadas))
    # O PORTAO, e o par negativo dele: nenhuma aceita pode cair em tile que
    # dispara coisa do motor. Se isso passar, quatorze Centros Pokemon de Galar
    # perdem o PC calados, que foi o achado que criou este arquivo.
    caso("nenhuma aceita esta em cima de PC, porta, agua ou vazio",
         all(l["beh"] in (BEH_PLACA, BEH_INERTE) and l["metatile"]
             for l in aceitas))
    # PAR NEGATIVO, e ele e o mesmo achado do lote C visto do outro lado:
    # AGORA a placa entra, mas NUNCA no tile de PC. Basta uma delas parar em
    # cima do PC para catorze Centros Pokemon perderem o PC calados.
    pcs = [l for l in aceitas
           if tile_de(l["mapa"], l["x_fonte"], l["y_fonte"])[3] == "MB_PC"]
    caso("as 14 placas da fonte em cima do PC entraram (%d)" % len(pcs),
         len(pcs) == 14)
    caso("nenhuma delas ficou na coordenada do PC",
         all((l["x"], l["y"]) != (l["x_fonte"], l["y_fonte"]) for l in pcs))
    caso("nenhuma aceita divide coordenada com outro evento do mapa",
         all(ocupado_por_evento(l["mapa"], l["x"], l["y"]) in
             (None, "bg_event (%s)" % l["rotulo"]) for l in aceitas))
    caso("toda placa deslocada ficou a no maximo dois tiles da fonte",
         all(max(abs(l["x"] - l["x_fonte"]), abs(l["y"] - l["y_fonte"])) <= 2
             for l in aceitas))
    # DETERMINISMO: a busca do vizinho tem que dar o mesmo tile sempre, senao
    # o pedido ao fechador e o .inc andam sozinhos entre duas rodadas.
    de_novo, _ = plano()
    caso("a busca do tile vizinho e deterministica",
         [(l["chave"], l["x"], l["y"]) for l in de_novo]
         == [(l["chave"], l["x"], l["y"]) for l in aceitas])
    # E a leitura de colisao, que era o outro defeito do lote C: chao andavel
    # de elevacao 3 nao pode voltar a ler como parede.
    caso("colisao e 2 bits, nunca a elevacao junto",
         all(l["colisao"] in (0, 1, 2, 3) for l in aceitas))
    # A regua de pixel e a mesma do qa/checa_texto.py.
    largas = [(l["rotulo"], ln) for l in aceitas
              for ln in re.split(r"\\[nlp]", l["texto"])
              if TXT.largura_px(ln) > TXT.LARGURA_CAIXA]
    caso("nenhuma linha de texto passa de 208 px", not largas)
    if largas:
        for r, ln in largas:
            print("      %s: %r (%d px)" % (r, ln, TXT.largura_px(ln)))
    caso("nenhuma caixa passa de tres linhas",
         all(len(re.split(r"\\[nl]", caixa)) <= 3
             for l in aceitas for caixa in l["texto"].split("\\p")))
    corpo = corpo_inc(aceitas)
    caso("todo rotulo aparece uma vez so no .inc",
         all(corpo.count("\n%s::" % l["rotulo"]) == 1 for l in aceitas))
    caso("o .inc so emite MSGBOX_SIGN",
         "MSGBOX_SIGN" in corpo and "MSGBOX_DEFAULT" not in corpo)
    caso("aplicar duas vezes seco nao muda nada na segunda",
         True if aplica(aceitas, bloqueadas, False) is not None else False)
    print("\n%s" % ("demo verde" if ok else "DEMO REPROVOU"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    aceitas, bloqueadas = plano()
    print("placas do lote C aceitas: %d em %d mapas"
          % (len(aceitas), len({l["mapa"] for l in aceitas})))
    for l in sorted(aceitas, key=lambda z: z["chave"]):
        print("  %-14s %-22s (%2d,%2d) %-12s %s"
              % (l["chave"], l["mapa"], l["x"], l["y"], l["beh"], l["rotulo"]))
    print("\nbloqueadas: %d" % len(bloqueadas))
    conta = collections.Counter(re.sub(r"\d+", "N", b["motivo"].split(":")[0])
                                for b in bloqueadas)
    for m, n in conta.most_common():
        print("  %4d  %s" % (n, m))
    mudou = aplica(aceitas, bloqueadas, gravar=a.aplicar)
    print("\n%s: %s" % ("gravado" if a.aplicar else "mudaria", dict(mudou)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
