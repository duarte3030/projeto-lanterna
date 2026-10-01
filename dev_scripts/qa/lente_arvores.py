#!/usr/bin/env python3
"""Lente da ÁRVORE ANDÁVEL: a arte do Blazing e a colisão do Emerald EX discordam.

POR QUE ELA EXISTE
------------------
Playtest de 30/09/2026 (fila de bugs 3): em Lavaridge o Gui andou EM CIMA de uma
árvore florida, na ponta esquerda da fileira de baixo do bosque ao sul do
caminho do Centro Pokémon. Causa medida na árvore e no emulador:

* A planta de Hoenn é a do Emerald EX (seção 0.ap do ESTADO), escrita com a
  SEMÂNTICA do vanilla: o metatile 542/543 do secundário `lavaridge` é um
  canteiro de flores com a pontinha (tile 0x0CC) da copa de baixo, e o EX o
  deixa ANDÁVEL acima da árvore de duas células (copa 470/471, tronco 486/487).
* A arte por cima é a do Blazing Emerald v1.6 (0.af), e o Blazing redesenhou o
  MESMO índice: no nosso tileset o 542/543 tem a copa (tiles 0x13B, 0x15C,
  0x14B) e as flores ficam em cima dela. Na tela é o topo florido de uma árvore
  de três células. Andável, vira "andar em cima da árvore".
* O mesmo desencontro, ao contrário, no primário: o vanilla (e o EX) usa o
  478/479 como TRONCO com a ponta da copa de baixo, bloqueado; o Blazing
  redefiniu o 478/479 como grama com mudinhas (175 usos andáveis e 0 bloqueados
  nos mapas do próprio Blazing). Na tela, uma faixa de grama em que não se pisa,
  e a fileira de árvores de cima fica sem tronco.

O `de-para` da frente Hoenn EX (`depara_metatiles_ex.py`) só traduz o que o EX
REDEFINIU em relação ao vanilla; o que o BLAZING redefiniu ficou de fora, porque
os dois lados (EX e vanilla) concordam entre si.

O QUE ELA MEDE
--------------
Todo mapa vivo (túmulo de Unova e Galar fora) cujo layout usa um dos dois
primários medidos: `gTileset_General` (a Hoenn que recebeu a arte do Blazing
por cima do EX, e os mapas de Sinnoh que herdaram esse primário, como o
`ValorLakefront`) e `gTileset_GeneralSinnoh` (estendida em 01/10/2026, depois
que a frente bugs3-teto achou troncos atravessáveis em Canalave e na Route 203).

    A1  árvore andável: célula com colisão 0 cujo metatile é, na NOSSA arte,
        copa ou tronco de árvore (tabela ARVORE abaixo).
    A2  parede de mudinha: célula com colisão diferente de 0 cujo metatile é,
        na NOSSA arte, grama andável redesenhada pelo Blazing (tabela GRAMA).

As duas tabelas não são chute: cada índice foi conferido no render do layout,
no uso dentro da ROM do Blazing (contagem de células andáveis e bloqueadas
quando o Blazing usa aquele índice) e, para o 542/543 e o 478/479, no emulador
(T361).

O QUE ELA NÃO MEDE
------------------
Desenho fora das duas tabelas. A varredura completa (todo metatile que o
Blazing redefiniu contra todo uso do EX) foi rodada em 30/09/2026 e as outras
classes que ela levantou eram iguais no EX (as escadas das casas de árvore de
Fortree e da Route 120, decorativas e bloqueadas no próprio EX), borda de mapa
inalcançável, ou desencontro de ARTE sem mudança de caminho (o Route 126). O `ValorLakefront`
(Sinnoh, primário General) tinha o mesmo 478/479 em 1072 células e foi
consertado junto em 01/10/2026.

USO
---
    python3 dev_scripts/qa/lente_arvores.py           # varre e imprime
    python3 dev_scripts/qa/lente_arvores.py --demo    # autoteste com mutação
"""
import glob
import json
import os
import shutil
import struct
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

import comum  # noqa: E402

PRIMARIO = "gTileset_General"
PRIMARIO_SINNOH = "gTileset_GeneralSinnoh"
PRIMARIOS = (PRIMARIO, PRIMARIO_SINNOH)

# Metatile cuja arte, no nosso tileset, é copa ou tronco de árvore.
# Primário: 468-471 copa, 476/477 tronco com a ponta da copa de baixo, 484-487
# tronco (o Blazing os usa bloqueados em mais de 80% das células).
# Lavaridge: 542/543 é o topo florido da árvore (playtest de 30/09/2026).
# Sinnoh (primário `gTileset_GeneralSinnoh`): 468-471 topo e 476-479 e 486/487
# base do pinheiro de duas células. Medido em 01/10/2026 em todos os layouts
# desse primário: 46.002 células bloqueadas contra 16 andáveis, e as 16 eram o
# defeito (Canalave x=3, y 4 a 7; Route 203 linhas 11 e 13, achados pela
# frente bugs3-teto). O 484/485 NÃO entra: nesse primário ele é outra arte,
# andável em 24 de 27 células.
ARVORE = {
    PRIMARIO: {468, 469, 470, 471, 476, 477, 484, 485, 486, 487},
    PRIMARIO_SINNOH: {468, 469, 470, 471, 476, 477, 478, 479, 486, 487},
    "gTileset_Lavaridge": {542, 543},
}

# Metatile cuja arte, no nosso tileset, é chão andável que o Blazing redesenhou
# sobre um índice que no vanilla era tronco (478/479: 175 e 42 células andáveis
# no Blazing, 0 e 1 bloqueadas).
GRAMA = {
    PRIMARIO: {478, 479},
}


def _layouts(raiz):
    with open(os.path.join(raiz, "data/layouts/layouts.json"), encoding="utf-8") as f:
        return {L["id"]: L for L in json.load(f)["layouts"] if "id" in L}


def alvos(raiz):
    """Layouts com um dos dois primários medidos, com o nome de um mapa que os usa.

    Túmulo de mapa cortado (`cortado_por`, Unova e Galar) fica de fora.
    """
    lays = _layouts(raiz)
    vistos = {}
    for f in sorted(glob.glob(os.path.join(raiz, "data/maps/*/map.json"))):
        with open(f, encoding="utf-8") as fh:
            m = json.load(fh)
        if m.get("cortado_por"):
            continue
        L = lays.get(m.get("layout"))
        if not L or L.get("primary_tileset") not in PRIMARIOS:
            continue
        vistos.setdefault(L["id"], (L, m["name"], m.get("region")))
    return [(L, nome) for L, nome, _r in vistos.values()], {
        L["id"]: r for L, _n, r in vistos.values()}


def celulas(raiz, L):
    caminho = os.path.join(raiz, L["blockdata_filepath"])
    if not os.path.exists(caminho):
        return None
    d = open(caminho, "rb").read()
    w, h = L["width"], L["height"]
    if len(d) != 2 * w * h:
        return None
    return w, list(struct.unpack("<%dH" % (w * h), d))


def classifica(L, mt, colisao):
    tab = L.get("primary_tileset") if mt < 512 else L.get("secondary_tileset")
    if colisao == 0 and mt in ARVORE.get(tab, ()):
        return "A1"
    if colisao != 0 and mt in GRAMA.get(tab, ()):
        return "A2"
    return None


def varre(raiz=None):
    raiz = raiz or comum.RAIZ
    achados, censo = [], dict(layouts=0, mudos=0)
    lista, regioes = alvos(raiz)
    for L, mapa in lista:
        c = celulas(raiz, L)
        if c is None:
            censo["mudos"] += 1
            continue
        censo["layouts"] += 1
        w, v = c
        for i, x in enumerate(v):
            regra = classifica(L, x & 0x3FF, (x >> 10) & 3)
            if regra:
                achados.append(dict(
                    regra=regra, classe="provável",
                    regiao=("Hoenn" if regioes.get(L["id"]) == "REGION_HOENN"
                            or L.get("primary_tileset") == PRIMARIO else "Sinnoh"),
                    mapa=mapa,
                    layout=L["name"], x=i % w, y=i // w, metatile=x & 0x3FF,
                    detalhe=("árvore andável" if regra == "A1"
                             else "grama do Blazing com colisão")))
    return achados, censo


def demo():
    """Mutação plantada numa cópia de Lavaridge: as duas regras têm de morder."""
    ruim = 0

    def falso(msg):
        nonlocal ruim
        ruim = 1
        print(f"  lente_arvores DEMO: {msg}")

    raiz = comum.RAIZ
    base, censo = varre(raiz)
    if censo["layouts"] < 300:
        falso(f"só {censo['layouts']} layouts medidos: a seleção quebrou")
    if base:
        falso("%d achado(s) na árvore: %s" % (len(base), ", ".join(
            sorted({f"{a['mapa']} ({a['x']},{a['y']})" for a in base}))[:300]))

    lav = [L for L, m in alvos(raiz)[0] if m == "LavaridgeTown"]
    if not lav:
        falso("LavaridgeTown sumiu dos alvos")
        return 1
    L = lav[0]
    tmp = tempfile.mkdtemp(prefix="lente_arvores_")
    try:
        os.makedirs(os.path.join(tmp, "data/layouts"))
        os.makedirs(os.path.join(tmp, "data/maps/LavaridgeTown"))
        shutil.copy(os.path.join(raiz, "data/maps/LavaridgeTown/map.json"),
                    os.path.join(tmp, "data/maps/LavaridgeTown/map.json"))
        L2 = dict(L, blockdata_filepath="mut.bin")
        json.dump({"layouts": [L2]}, open(os.path.join(tmp, "data/layouts/layouts.json"), "w"))
        w, v = celulas(raiz, L)
        # (8,26) é a célula do playtest: topo florido volta a ser andável.
        v[26 * w + 8] = 543 | (3 << 12)
        # (9,26): tronco vira a grama de mudinha do Blazing, ainda bloqueada.
        v[26 * w + 9] = 478 | (1 << 10)
        open(os.path.join(tmp, "mut.bin"), "wb").write(struct.pack("<%dH" % len(v), *v))
        mut, _ = varre(tmp)
        regras = {(a["regra"], a["x"], a["y"]) for a in mut}
        if ("A1", 8, 26) not in regras:
            falso("o topo florido andável em (8,26) passou batido")
        if ("A2", 9, 26) not in regras:
            falso("a mudinha bloqueada em (9,26) passou batido")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if not ruim:
        print("demo ok")
    return ruim


def main():
    if "--demo" in sys.argv:
        return demo()
    achados, censo = varre()
    print("layouts %(layouts)d, mudos %(mudos)d" % censo)
    for a in achados:
        print("  %-3s %-24s (%d,%d) metatile %d: %s" % (
            a["regra"], a["mapa"], a["x"], a["y"], a["metatile"], a["detalhe"]))
    print("%d achado(s)" % len(achados))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
