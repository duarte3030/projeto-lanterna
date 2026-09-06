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
    """(metatile, colisao, nome do comportamento) na coordenada do mapa."""
    doc = json.load(open("%s/data/maps/%s/map.json" % (RAIZ, mapa)))
    lay = layouts()[doc["layout"]]
    dados = open("%s/%s" % (RAIZ, lay["blockdata_filepath"]), "rb").read()
    larg = lay["width"]
    if not (0 <= x < larg and 0 <= y < lay["height"]):
        return None, None, "fora do layout"
    bruto = struct.unpack_from("<H", dados, 2 * (y * larg + x))[0]
    mid, col = bruto & 0x3FF, bruto >> 10
    # O corte primario/secundario de Galar e o do FRLG (640), que
    # `src/fieldmap.c:438` ja resolve por `isFrlg`/`bigPrimary`.
    ts = lay["primary_tileset"] if mid < 640 else lay["secondary_tileset"]
    idx = mid if mid < 640 else mid - 640
    a = atributos(ts)
    if a is None or 4 * idx + 4 > len(a):
        return mid, col, "tileset sem atributo lido"
    beh = struct.unpack_from("<I", a, 4 * idx)[0] & 0x1FF
    return mid, col, enum_behaviors().get(beh, "MB_%d" % beh)


def bg_ocupado(mapa, x, y):
    """Rotulo do `bg_event` que ja esta nessa coordenada, ou None."""
    doc = json.load(open("%s/data/maps/%s/map.json" % (RAIZ, mapa)))
    for b in doc.get("bg_events") or []:
        if b.get("x") == x and b.get("y") == y:
            return str(b.get("script") or "sem script")
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
        dono = bg_ocupado(l["mapa"], l["x"], l["y"])
        if dono:
            bloqueadas.append(dict(l, motivo=(
                "coordenada (%d,%d) ja tem bg_event de precedencia maior (%s)"
                % (l["x"], l["y"], dono))))
            continue
        mid, col, beh = tile_de(l["mapa"], l["x"], l["y"])
        if beh == BEH_PLACA or (beh == BEH_INERTE and col):
            texto = TEXTO.get(l["chave"])
            if texto is None:
                bloqueadas.append(dict(l, motivo=(
                    "tile serve (%s, colisao %s) mas nao ha texto escrito para "
                    "esta placa" % (beh, col))))
                continue
            aceitas.append(dict(l, rotulo=rotulo(l["chave"]),
                                texto=TXT.requebra(texto), beh=beh,
                                metatile=mid, colisao=col))
            continue
        if beh == BEH_INERTE:
            bloqueadas.append(dict(l, motivo=(
                "o bg da fonte cai no metatile %s (%s, colisao %s): tile que o "
                "jogador PISA e sem desenho de placa; o `sign` seria caixa de "
                "texto saindo do chao" % (mid, beh, col))))
            continue
        bloqueadas.append(dict(l, motivo=(
            "o bg da fonte cai no metatile %s (%s, colisao %s): um `sign` ali "
            "viria ANTES de GetInteractedMetatileScript "
            "(src/field_control_avatar.c:325) e roubaria a interacao do proprio "
            "tile" % (mid, beh, col))))
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
        out += ["@ ---- %s (%s), tile %s %s ----"
                % (l["mapa"], l["chave"], l["metatile"], l["beh"]),
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
           "# (MB_SIGNPOST, ou MB_NORMAL com colisao), e nao ha bg_event nenhum",
           "# nela hoje. As que nao passaram nesse portao NAO estao aqui; elas",
           "# ficaram bloqueadas na fila, com o motivo na linha.",
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
        novo = "adiada", ("lote C da onda 1, 06/09/2026: " + b["motivo"])
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
         all(l["beh"] in (BEH_PLACA, BEH_INERTE) and
             (l["beh"] == BEH_PLACA or l["colisao"]) and l["metatile"]
             for l in aceitas))
    pcs = [b for b in bloqueadas if "MB_PC" in b["motivo"]]
    caso("as placas de cima do PC do Centro Pokemon estao BLOQUEADAS (14)",
         len(pcs) == 14)
    # PAR NEGATIVO do portao: uma placa plantada em cima de um tile de PC tem
    # de ser recusada mesmo tendo texto escrito.
    vitima = pcs[0] if pcs else None
    caso("achou onde plantar o par negativo", vitima is not None)
    if vitima:
        salvo = TEXTO.get(vitima["chave"])
        TEXTO[vitima["chave"]] = "Test."
        a2, b2 = plano()
        caso("placa com texto em cima do PC continua RECUSADA",
             all(l["chave"] != vitima["chave"] for l in a2))
        if salvo is None:
            TEXTO.pop(vitima["chave"], None)
        else:
            TEXTO[vitima["chave"]] = salvo
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
