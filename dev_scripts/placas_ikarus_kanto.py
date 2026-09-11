#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""As 17 portas que o Ikarus desenhou em Kanto sem destino ganham placa.

    python3 dev_scripts/placas_ikarus_kanto.py            # só relata
    python3 dev_scripts/placas_ikarus_kanto.py --aplicar  # escreve
    python3 dev_scripts/placas_ikarus_kanto.py --demo     # autoteste, exit 1 se cair

De onde vêm as 17
-----------------
A troca de arte de 11/09/2026 (Ikarus' Tileset Patch FR v3.2, seção 0.ag do
ESTADO) redesenhou 109 layouts de Kanto. Em 17 blocos de célula o desenho novo
traz fachada de porta, arco de portão ou seta de saída onde o NOSSO jogo não tem
warp nenhum. A consolidação pôs as 17 na `LISTA_BRANCA` da `lente_portas.py`
para a lente voltar a morder porta nova; esta ferramenta é a onda 3, que tira as
17 de lá e põe em cada uma a placa `closed` em inglês, no molde das 31 portas de
Johto (`dev_scripts/abre_portas_johto.py`, família 5).

O QUE A MEDIÇÃO MOSTROU, e ela muda o que dá para provar no emulador
--------------------------------------------------------------------
Medido célula a célula neste HEAD (colisão do `map.bin` e censo de uso de cada
metatile em toda Kanto): das 17, só QUATRO têm célula andável encostada, e
portanto só essas quatro o jogador alcança para apertar A:

    CeruleanCity_Frlg (40,10)   porta de casa, chão andável em (40,11)
    CeruleanCity_Frlg (33,28)   porta de casa, chão andável em (33,29)
    SafariZone_West_Frlg (27,25) a própria célula é andável
    SaffronCity_Frlg (34,51)    arco sul do portão, andável, com (34,52) colado

As outras TREZE estão dentro de bloco sólido, sem UMA célula andável encostada
em nenhuma das quatro direções: o jogador nunca chega perto, e a placa fica lá
como resposta a quem chegar se algum dia o desenho abrir. Elas caem em três
famílias, todas conferidas no render e no censo de metatile:

  * A SEGUNDA FACE DO PORTÃO (Route2 5,18 e 5,46; Route6 12,0; SaffronCity 34,0;
    ViridianForest 4,2 e 6,2; OneIsland_KindleRoad 11,4). O portão de rota do
    Ikarus tem DUAS entradas desenhadas, a de cima e a de baixo, e o jogo só usa
    uma delas em cada mapa, porque a outra cai do lado de lá da emenda. Prova de
    censo: o MESMO metatile aparece com warp em outra célula do mesmo mapa
    (Route2 mt882/883 tem warp em (5,51) e (18,46); SaffronCity mt946/947 tem
    warp em (34,5); SeviiIslands123 mt1006/1007 tem warp em MtEmber_Exterior).
  * TELHADO E CHAMINÉ (Route10 8,34 e 10,34, as chaminés da usina; Route8 14,1,
    a quina do telhado). O metatile carrega `MB_NON_ANIMATED_DOOR` e o desenho
    não é porta nenhuma; nenhuma das 3 células tem warp e nenhuma outra célula
    de Kanto usa esses metatiles.
  * O CORREDOR DA SAFARI (SafariZone_Center 0,18; SafariZone_East 0,10 e 0,27).
    São a ponta cega do caminho de areia entre as áreas: 46 células usam o
    mt740, nenhuma com warp, todas com colisão 1. Quem liga as áreas é o mt979,
    que tem warp em (43,16) do Center, (48,32) do North e (40,27) do West.

Por que placa, e não conserto de metatile
-----------------------------------------
Nove dos metatiles envolvidos são COMPARTILHADOS com célula que tem warp de
verdade no mesmo mapa: mexer no `metatile_attributes.bin` deles mataria a porta
que funciona. E repintar a célula para deixar de ser porta seria desfazer o
desenho que o Gui aprovou no render (resposta 76), que é exatamente o que a
lição 0.ae proíbe. Placa é o único conserto que não mente com a arte nem com o
motor.

Save intacta
------------
`bg_event` não entra em save: não há flag, não há var, nenhum índice de
`object_events` ou de `warp_events` se mexe, e a placa entra sempre no FIM da
lista de `bg_events`.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APLICAR = "--aplicar" in sys.argv

PLACA = "Common_EventScript_PortaFechada"   # "Closed for renovations."

# (mapa, x, y, alcançável, o que o desenho é)
PLACAS = [
    ("CeruleanCity_Frlg", 40, 10, True,
     "porta de casa sem interior; chão andável em (40,11)"),
    ("CeruleanCity_Frlg", 33, 28, True,
     "porta de casa sem interior; chão andável em (33,29)"),
    ("OneIsland_KindleRoad_Frlg", 11, 4, False,
     "seta do portão da Kindle Road, face sem uso; o mt1006 com warp está em "
     "MtEmber_Exterior (28,48)"),
    ("Route10_Frlg", 8, 34, False,
     "chaminé do telhado da usina; o mt783 não tem warp em célula nenhuma"),
    ("Route10_Frlg", 10, 34, False,
     "chaminé do telhado da usina; o mt783 não tem warp em célula nenhuma"),
    ("Route2_Frlg", 5, 18, False,
     "face sul do portão norte da Viridian Forest; o mt882 com warp está em "
     "(5,51) e (18,46)"),
    ("Route2_Frlg", 5, 46, False,
     "face norte do portão sul da Viridian Forest; o mt842 com warp está em "
     "(5,13) e (18,41)"),
    ("Route6_Frlg", 12, 0, False,
     "telhado do portão norte da Route 6, do lado de lá da emenda com Saffron"),
    ("Route8_Frlg", 14, 1, False,
     "quina do telhado da casa; o mt794 não tem warp em célula nenhuma"),
    ("SafariZone_Center_Frlg", 0, 18, False,
     "ponta cega do corredor de areia; quem liga as áreas é o mt979 em (43,16)"),
    ("SafariZone_East_Frlg", 0, 10, False,
     "ponta cega do corredor de areia; o mt740 não tem warp em célula nenhuma"),
    ("SafariZone_East_Frlg", 0, 27, False,
     "ponta cega do corredor de areia; o mt740 não tem warp em célula nenhuma"),
    ("SafariZone_West_Frlg", 27, 25, True,
     "abertura no penhasco com o mt979 e sem warp; a célula é andável"),
    ("SaffronCity_Frlg", 34, 0, False,
     "telhado do portão norte de Saffron, do lado de lá da emenda com a Route 5"),
    ("SaffronCity_Frlg", 34, 51, True,
     "arco sul do portão de Saffron; andável, com (34,52) colado"),
    ("ViridianForest_Frlg", 4, 2, False,
     "telhado do portão norte da floresta, do lado de lá da emenda"),
    ("ViridianForest_Frlg", 6, 2, False,
     "telhado do portão norte da floresta, do lado de lá da emenda"),
]

LENTE = os.path.join(REPO, "dev_scripts", "qa", "lente_portas.py")
MARCA = "Porta do Ikarus sem destino, placa closed pendente da onda 3 de Kanto."


def caminho(nome):
    return os.path.join(REPO, "data", "maps", nome, "map.json")


def escreve_placas():
    """Põe a placa no FIM de bg_events. Devolve quantas entraram."""
    postas = 0
    por_mapa = {}
    for nome, x, y, _alc, motivo in PLACAS:
        por_mapa.setdefault(nome, []).append((x, y, motivo))
    for nome, itens in sorted(por_mapa.items()):
        cam = caminho(nome)
        with open(cam, encoding="utf-8") as f:
            d = json.load(f)
        d.setdefault("bg_events", [])
        mudou = False
        for x, y, motivo in itens:
            if any(b.get("x") == x and b.get("y") == y
                   and b.get("script") == PLACA for b in d["bg_events"]):
                continue
            d["bg_events"].append({
                "type": "sign", "x": x, "y": y, "elevation": 0,
                "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                "script": PLACA,
                "origem": "porta do Ikarus sem destino (onda 3 de Kanto): " + motivo,
            })
            postas += 1
            mudou = True
        if mudou and APLICAR:
            with open(cam, "w", encoding="utf-8") as f:
                json.dump(d, f, indent=2, ensure_ascii=False)
                f.write("\n")
    return postas


def limpa_lista_branca():
    """Tira da LISTA_BRANCA da lente as 17 linhas da onda 3. Devolve quantas."""
    with open(LENTE, encoding="utf-8") as f:
        texto = f.read()
    tiradas = 0
    for nome, x, y, _alc, _motivo in PLACAS:
        alvo = (f'    ("{nome}", {x}, {y}):\n'
                f'        "{MARCA}",\n')
        if alvo in texto:
            texto = texto.replace(alvo, "", 1)
            tiradas += 1
    # O comentário de bloco das 17 sai junto: sem linha nenhuma embaixo dele,
    # ele passaria a descrever o vazio.
    if tiradas:
        inicio = texto.find(
            "    # --- Kanto, Ikarus' Tileset Patch v3.2: 17 portas DESENHADAS")
        if inicio >= 0:
            fim = texto.find("}", inicio)
            novo = (
                "    # --- Kanto, Ikarus' Tileset Patch v3.2 -------------------\n"
                "    # As 17 portas que o autor desenhou sem destino NÃO moram\n"
                "    # mais aqui: a onda 3 de Kanto (11/09/2026) pôs em cada uma\n"
                "    # a placa `closed` do molde de Johto, e a lente as conta na\n"
                "    # classe \"placa\", que é medida no `map.json` e não em lista.\n"
                "    # Ver `dev_scripts/placas_ikarus_kanto.py`.\n")
            texto = texto[:inicio] + novo + texto[fim:]
    if APLICAR and tiradas:
        with open(LENTE, "w", encoding="utf-8") as f:
            f.write(texto)
    return tiradas


def demo():
    """Autoteste: o que esta ferramenta promete, conferido no HEAD."""
    falhas = []
    sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
    sys.path.insert(0, os.path.join(REPO, "dev_scripts", "qa"))
    import struct
    import valida_warp_tile as vwt

    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]
        if "id" in l}
    cache = {}

    def grade(nome):
        if nome in cache:
            return cache[nome]
        d = json.load(open(caminho(nome), encoding="utf-8"))
        lay = layouts[d["layout"]]
        blk = open(os.path.join(REPO, lay["blockdata_filepath"]), "rb").read()
        w, h = lay["width"], lay["height"]
        cel = {}
        for y in range(h):
            for x in range(w):
                b = struct.unpack("<H", blk[(y * w + x) * 2:(y * w + x) * 2 + 2])[0]
                cel[(x, y)] = (b & 0x3FF, (b >> 10) & 3)
        cache[nome] = (d, cel, w, h)
        return cache[nome]

    # 1. cada célula da lista existe, e o comportamento dela é de porta
    for nome, x, y, alc, _m in PLACAS:
        d, cel, w, h = grade(nome)
        if (x, y) not in cel:
            falhas.append(f"{nome} ({x},{y}) fora da grade {w}x{h}")
            continue
        # 2. a alcançabilidade declarada bate com o map.bin
        viz = [(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
        andavel = (cel[(x, y)][1] == 0
                   or any(cel.get(v) and cel[v][1] == 0 for v in viz))
        if andavel != alc:
            falhas.append(f"{nome} ({x},{y}): alcançável declarado {alc}, "
                          f"medido {andavel}")
        # 3. a célula não tem warp (se tivesse, placa seria mentira)
        if any(wv.get("x") == x and wv.get("y") == y
               for wv in d.get("warp_events", [])):
            falhas.append(f"{nome} ({x},{y}) TEM warp: placa não cabe")

    # 4. a placa existe no arquivo de scripts comuns
    inc = open(os.path.join(REPO, "data/scripts/portas_fechadas.inc"),
               encoding="utf-8").read()
    if f"{PLACA}::" not in inc:
        falhas.append(f"{PLACA} não está em data/scripts/portas_fechadas.inc")

    # 5. nenhuma flag e nenhuma var novas
    for nome, x, y, _a, _m in PLACAS:
        d, _c, _w, _h = grade(nome)
        for b in d.get("bg_events", []):
            if b.get("script") == PLACA and "flag" in b:
                falhas.append(f"{nome} ({x},{y}): placa com flag")

    if falhas:
        for f_ in falhas:
            print("FALHA:", f_)
        return 1
    print(f"demo OK: {len(PLACAS)} placas, "
          f"{sum(1 for p in PLACAS if p[3])} alcançáveis, "
          f"{sum(1 for p in PLACAS if not p[3])} em bloco sólido")
    return 0


def main():
    if "--demo" in sys.argv:
        sys.exit(demo())
    postas = escreve_placas()
    tiradas = limpa_lista_branca()
    print(f"placas a pôr: {postas}; linhas a tirar da LISTA_BRANCA: {tiradas}")
    if not APLICAR:
        print("(nada escrito; use --aplicar)")


if __name__ == "__main__":
    main()
