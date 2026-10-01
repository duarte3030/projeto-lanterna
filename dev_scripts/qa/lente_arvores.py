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
Só os mapas de `REGION_HOENN` com primário `gTileset_General` (a Hoenn que
recebeu a arte do Blazing por cima do EX).

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
inalcançável, ou desencontro de ARTE sem mudança de caminho (o Route 126). Fora
de Hoenn, o `ValorLakefront` (Sinnoh, primário General) tem o mesmo 478/479 e
fica fora desta lente (região de outra frente) e foi relatado ao condutor
da fila de bugs 3.

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

# Metatile cuja arte, no nosso tileset, é copa ou tronco de árvore.
# Primário: 468-471 copa, 476/477 tronco com a ponta da copa de baixo, 484-487
# tronco (o Blazing os usa bloqueados em mais de 80% das células).
# Lavaridge: 542/543 é o topo florido da árvore (playtest de 30/09/2026).
ARVORE = {
    PRIMARIO: {468, 469, 470, 471, 476, 477, 484, 485, 486, 487},
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
    """Layouts de Hoenn com o primário do Blazing, com o nome de um mapa que os usa."""
    lays = _layouts(raiz)
    vistos = {}
    for f in sorted(glob.glob(os.path.join(raiz, "data/maps/*/map.json"))):
        with open(f, encoding="utf-8") as fh:
            m = json.load(fh)
        if m.get("region") != "REGION_HOENN":
            continue
        L = lays.get(m.get("layout"))
        if not L or L.get("primary_tileset") != PRIMARIO:
            continue
        vistos.setdefault(L["id"], (L, m["name"]))
    return list(vistos.values())


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
    sec = L.get("secondary_tileset")
    tab = PRIMARIO if mt < 512 else sec
    if colisao == 0 and mt in ARVORE.get(tab, ()):
        return "A1"
    if colisao != 0 and mt in GRAMA.get(tab, ()):
        return "A2"
    return None


def varre(raiz=None):
    raiz = raiz or comum.RAIZ
    achados, censo = [], dict(layouts=0, mudos=0)
    for L, mapa in alvos(raiz):
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
                    regra=regra, classe="provável", regiao="Hoenn", mapa=mapa,
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
    if censo["layouts"] < 50:
        falso(f"só {censo['layouts']} layouts de Hoenn medidos: a seleção quebrou")
    if base:
        falso("%d achado(s) na árvore: %s" % (len(base), ", ".join(
            sorted({f"{a['mapa']} ({a['x']},{a['y']})" for a in base}))[:300]))

    lav = [L for L, m in alvos(raiz) if m == "LavaridgeTown"]
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
