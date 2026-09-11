#!/usr/bin/env python3
"""Devolve a MECÂNICA que a arte do Ikarus apagou em Kanto, sem desfazer a arte.

Uso:
    python3 dev_scripts/conserta_ikarus_kanto.py --contra /caminho/arvore-antes
    python3 dev_scripts/conserta_ikarus_kanto.py --contra ... --aplicar
    python3 dev_scripts/conserta_ikarus_kanto.py --demo

POR QUE ESTE ARQUIVO EXISTE
---------------------------
Em 11/09/2026 Kanto inteira trocou de arte para o "Ikarus' Tileset Patch v3.2":
`gTileset_General_Frlg`, 24 secundários e 101 `map.bin`. A onda 1 do QA mediu que
warp, NPC e conexão continuavam de pé, e a onda 2 mediu o que ninguém tinha
medido: o COMPORTAMENTO de metatile, célula a célula, contra a árvore de antes
(`8212542e4a`).

O resultado, e ele NÃO é bug nosso. Contando comportamento célula a célula nos
187 mapas de Kanto, antes e depois da troca:

    MB_FAST_WATER            2.831 -> 1        MB_MOUNTAIN_TOP  1.119 ->  210
    MB_CYCLING_ROAD_PULL_DOWN 2.041 -> 25      MB_SAND          1.491 ->  291
    MB_CYCLING_ROAD_WATER      751 -> 0        MB_POND_WATER      635 ->    4
    MB_NORTHWARD_CURRENT       142 -> 0        MB_ROCK_STAIRS     358 ->   81
    MB_SOUTHWARD_CURRENT        45 -> 0        MB_MT_PYRE_HOLE     31 ->   23

A mesma conta rodada na ROM do próprio Ikarus contra a FireRed limpa dá os
mesmos zeros: o patch publicado é que apaga a Cycling Road e o quebra-cabeça das
Seafoam. A importação copiou isso com fidelidade. A seção 1.2 do
METODO-COPIA-CIDADES.md diz "jogo inteiro nosso: warps, NPCs, gatilhos, placas,
scripts, conexões, encontros"; mecânica de mapa é jogo, não arte, então o
veredito do condutor foi RESTAURAR.

AS DUAS FERRAMENTAS, e quando cada uma vale
-------------------------------------------
1. **Comportamento mora no METATILE.** Onde o metatile for EXCLUSIVO da mecânica,
   devolver o comportamento a ele conserta o mapa inteiro e não vaza. É o caso da
   Cycling Road: a estrada que o Ikarus desenhou na Route 17 são os metatiles
   672, 673 e 674 do secundário `celadon_city_frlg` (índices locais 32, 33 e 34),
   317 células cada, e eles NÃO aparecem em nenhum dos outros quatro mapas que
   dividem esse secundário (CeladonCity, Route7, Route16, Route18: medido, zero
   células). Aqui é `--route17`.

2. **Onde o metatile é compartilhado, o conserto é no `map.bin`, célula a
   célula.** É o caso das Seafoam: o Ikarus repintou cada célula de corrente com
   água comum (o metatile 473 do primário, que é oceano em Kanto inteira), então
   devolver comportamento ao 473 inundaria a região de correntes. Mas o tileset
   NOVO ainda tem os metatiles certos, com o comportamento certo e com a arte
   redesenhada pelo autor (780 a 806 = corrente, 646 = buraco, 795/796 = queda,
   715 e 848/849 = água rápida). Então a célula volta a apontar para o metatile
   que ela apontava ANTES, e quem desenha continua sendo o Ikarus. Aqui é
   `--seafoam`.

O QUE ELE PRESERVA, de propósito
---------------------------------
- **Os bits 10 a 15 do `map.bin` são os do IKARUS**, não os de antes: colisão e
  elevação são caminho, e o caminho novo é o que a arte nova pede. Só o id do
  metatile (bits 0 a 9) volta. Medido nas 256 células que este script repinta:
  253 já tinham colisão e elevação idênticas às de antes, e as 3 que diferem
  (elevação 1 -> 0) ficam como o Ikarus deixou.
- **Nada de `map.json`**: warp, objeto e gatilho não são assunto desta
  ferramenta. Quem mexe em warp é `porta_ikarus_kanto.py`.
- **Nada de mapa fora da lista.** `--seafoam` só toca os cinco mapas das Seafoam
  Islands, e a lista está escrita aqui, não deduzida por regra larga. As outras
  perdas medidas acima (areia, topo de montanha, escada de pedra, água rápida das
  Sevii) NÃO entram: elas caem em mapas que o Ikarus REDESENHOU, e repintar lá
  seria discutir desenho, não devolver mecânica.

A ARMADILHA QUE ESTA FERRAMENTA NÃO CAI
----------------------------------------
Repintar célula por "o comportamento sumiu" sem olhar o que o autor pôs no lugar
é como consertar a Route 17 inteira: das 2.041 células que tinham
`MB_CYCLING_ROAD_PULL_DOWN`, só 951 são estrada no desenho novo. As outras 1.090
viraram grama, mata, cerca e um lago, porque o Ikarus REDESENHOU a rota. Pintar
asfalto nelas para fazer o número bater destruiria o desenho. Por isso a Route 17
é consertada pelo TILESET (as 951 que são estrada de verdade) e o resto é
relatado, não pintado.
"""
import argparse
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import atributos_metatile as A  # noqa: E402

# Os cinco mapas das Seafoam Islands. Escritos a mão, e não achados por regra,
# porque o critério que os separa do resto de Kanto é de JOGO (o quebra-cabeça
# de corrente e buraco que leva ao Articuno), não de medida.
SEAFOAM = [
    "SeafoamIslands_1F_Frlg", "SeafoamIslands_B1F_Frlg", "SeafoamIslands_B2F_Frlg",
    "SeafoamIslands_B3F_Frlg", "SeafoamIslands_B4F_Frlg",
]

# Os comportamentos que são MECÂNICA de quebra-cabeça, e cuja perda o
# `--seafoam` desfaz. Água comum e chão comum ficam de fora de propósito: trocar
# um oceano do Ikarus por outro oceano nosso não devolve mecânica nenhuma e só
# mexeria em desenho.
#
# `MB_SHALLOW_WATER` ficou de FORA depois de medido: são 4 células nas Seafoam
# (duas na B3F, duas na B4F), o Ikarus pintou oceano nelas, e os metatiles de
# antes (824, 825, 827, 828) NÃO carregam mais esse comportamento no tileset
# novo. Ou seja, não há para onde repintar sem chutar, e água rasa não é peça do
# quebra-cabeça do Articuno: quem carrega o jogador é a CORRENTE, quem abre o
# caminho é o BURACO.
MECANICA = {
    "MB_NORTHWARD_CURRENT", "MB_SOUTHWARD_CURRENT", "MB_EASTWARD_CURRENT",
    "MB_WESTWARD_CURRENT", "MB_FAST_WATER", "MB_WATERFALL", "MB_MT_PYRE_HOLE",
}

# A estrada que o Ikarus desenhou na Route 17, e o comportamento que ela perdeu.
# Os três índices locais saem de contar célula a célula o `map.bin` novo, não de
# olhar o atlas: são os únicos metatiles do secundário que aparecem SÓ na
# Route 17, com 317 células cada.
ROUTE17_TILESET = "gTileset_CeladonCity"
ROUTE17_LOCAIS = (32, 33, 34)          # metatiles 672, 673 e 674
ROUTE17_BEHAVIOR = "MB_CYCLING_ROAD_PULL_DOWN"


# --------------------------------------------------------------- leitura crua
def comportamentos(raiz):
    """MB_* -> número, do enum de include/constants/metatile_behaviors.h."""
    import re
    texto = open(os.path.join(raiz, "include/constants/metatile_behaviors.h")).read()
    corpo = texto[texto.index("{") + 1:texto.rindex("}")]
    valor, tabela = 0, {}
    for item in corpo.split(","):
        item = re.sub(r"/\*.*?\*/", "", re.sub(r"//.*", "", item), flags=re.S).strip()
        if not item:
            continue
        if "=" in item:
            nome, _, bruto = item.partition("=")
            nome, valor = nome.strip(), int(bruto.strip(), 0)
        else:
            nome = item
        tabela[nome] = valor
        valor += 1
    return tabela


def pastas_de_tileset(raiz):
    """gTileset_X -> pasta do tileset, pelo INCBIN de src/data/tilesets/metatiles.h.

    A mesma leitura do `valida_warp_tile.py`, e pelo mesmo motivo: o nome da
    pasta NÃO sai do símbolo (`gTileset_Route38Farmland` mora em
    `secondary/route_38_farmland`), e `dedupe_assets.py` troca tileset repetido
    por `ASSET_ALIAS`, que some de uma varredura ingênua.
    """
    import re
    mt = open(os.path.join(raiz, "src/data/tilesets/metatiles.h")).read()
    sym = dict(re.findall(
        r'gMetatiles_(\w+)\[\]\s*=\s*INCBIN_U16\("(data/tilesets/\w+/\w+)/metatiles\.bin"\)', mt))
    for apelido, canonico in re.findall(
            r'gMetatiles_(\w+)\[[^\]]*\]\s*ASSET_ALIAS\(gMetatiles_(\w+)\)', mt):
        sym.setdefault(apelido, canonico)
    for _ in range(len(sym)):
        mudou = False
        for k, v in sym.items():
            if not v.startswith("data/") and v in sym:
                sym[k], mudou = sym[v], True
        if not mudou:
            break
    hdr = open(os.path.join(raiz, "src/data/tilesets/headers.h")).read()
    fora = {}
    for nome, corpo in re.findall(
            r'const struct Tileset gTileset_(\w+)\s*=\s*\{(.*?)\};', hdr, re.S):
        m = re.search(r'\.metatiles\s*=\s*gMetatiles_(\w+)', corpo)
        if m and m.group(1) in sym:
            fora["gTileset_" + nome] = os.path.join(raiz, sym[m.group(1)])
    return fora


class Arvore:
    """Uma árvore do repo, lida como dado: layouts, blockdata e atributos."""

    def __init__(self, raiz):
        self.raiz = raiz
        self.layouts = {l["id"]: l for l in json.load(
            open(os.path.join(raiz, "data/layouts/layouts.json"), encoding="utf-8"))["layouts"]}
        self.pastas = pastas_de_tileset(raiz)
        self.mb = comportamentos(raiz)
        self.nome_mb = {v: k for k, v in self.mb.items()}
        self._attr = {}

    def layout_do_mapa(self, mapa):
        d = json.load(open(os.path.join(self.raiz, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))
        return self.layouts[d["layout"]]

    def atributos(self, tileset, versao):
        if tileset in self._attr:
            return self._attr[tileset]
        pasta = self.pastas.get(tileset)
        if not pasta:
            self._attr[tileset] = []
            return []
        cru = open(os.path.join(pasta, "metatile_attributes.bin"), "rb").read()
        self._attr[tileset] = A.palavras(cru, versao)
        return self._attr[tileset]

    def grade(self, layout):
        """(células cruas, largura, altura). Célula = a palavra do `map.bin`."""
        bruto = open(os.path.join(self.raiz, layout["blockdata_filepath"]), "rb").read()
        w, h = layout["width"], layout["height"]
        return [struct.unpack_from("<H", bruto, i * 2)[0] for i in range(w * h)], w, h

    def behavior(self, layout, metatile):
        versao = layout.get("layout_version") or "emerald"
        p = A.perfil(versao)
        pri = self.atributos(layout.get("primary_tileset"), versao)
        sec = self.atributos(layout.get("secondary_tileset"), versao)
        tab, rel = (pri, metatile) if metatile < p["corte"] else (sec, metatile - p["corte"])
        if rel >= len(tab):
            return None
        return A.par(tab[rel], versao)[0]


# ------------------------------------------------------------------- seafoam
def planeja_seafoam(agora, antes):
    """[(mapa, x, y, metatile_velho, metatile_novo, comportamento_perdido)]."""
    plano = []
    for mapa in SEAFOAM:
        la, lb = agora.layout_do_mapa(mapa), antes.layout_do_mapa(mapa)
        ca, w, h = agora.grade(la)
        cb, wb, hb = antes.grade(lb)
        if (w, h) != (wb, hb):
            raise SystemExit(f"{mapa} mudou de tamanho ({w}x{h} contra {wb}x{hb}); "
                             "repintar célula a célula deixou de fazer sentido")
        for i, (pa, pb) in enumerate(zip(ca, cb)):
            mt_a, mt_b = pa & 0x3FF, pb & 0x3FF
            b_a, b_b = agora.behavior(la, mt_a), antes.behavior(lb, mt_b)
            nome_b = antes.nome_mb.get(b_b)
            if nome_b not in MECANICA or b_a == b_b:
                continue
            # A trava que evita repintar no escuro: o metatile de antes tem que
            # existir no tileset de AGORA e ainda carregar o comportamento certo.
            if agora.behavior(la, mt_b) != b_b:
                raise SystemExit(
                    f"{mapa} ({i % w},{i // w}): o metatile {mt_b} não tem mais "
                    f"{nome_b} no tileset novo; repintar seria chute")
            plano.append((mapa, i % w, i // w, mt_a, mt_b, nome_b))
    return plano


def aplica_seafoam(agora, plano):
    """Grava o plano nos `map.bin`, preservando os bits 10 a 15 do Ikarus."""
    por_mapa = collections.defaultdict(list)
    for mapa, x, y, _velho, novo, _b in plano:
        por_mapa[mapa].append((x, y, novo))
    total = 0
    for mapa, itens in sorted(por_mapa.items()):
        lay = agora.layout_do_mapa(mapa)
        caminho = os.path.join(agora.raiz, lay["blockdata_filepath"])
        dados = bytearray(open(caminho, "rb").read())
        w = lay["width"]
        for x, y, novo in itens:
            off = (y * w + x) * 2
            palavra = struct.unpack_from("<H", dados, off)[0]
            struct.pack_into("<H", dados, off, (palavra & ~0x3FF) | (novo & 0x3FF))
            total += 1
        open(caminho, "wb").write(bytes(dados))
    return total


# ------------------------------------------------------------------ route 17
def planeja_route17(agora):
    """[(índice local, comportamento de agora)] dos metatiles da estrada."""
    lay = agora.layout_do_mapa("Route17_Frlg")
    if lay.get("secondary_tileset") != ROUTE17_TILESET:
        raise SystemExit(f"Route17 deixou de usar {ROUTE17_TILESET}")
    versao = lay.get("layout_version") or "emerald"
    p = A.perfil(versao)
    sec = agora.atributos(ROUTE17_TILESET, versao)
    fora = []
    for local in ROUTE17_LOCAIS:
        beh, _lt = A.par(sec[local], versao)
        fora.append((local, local + p["corte"], agora.nome_mb.get(beh, beh)))
    return fora


def exclusividade_route17(agora):
    """Quantas células cada metatile da estrada tem, mapa a mapa do secundário.

    A trava do item 1 do cabeçalho: se algum mapa FORA da Route 17 usar um
    desses três, devolver comportamento a eles vazaria para lá.
    """
    grupos = json.load(open(os.path.join(agora.raiz, "data/maps/map_groups.json"),
                            encoding="utf-8"))
    censo = collections.Counter()
    for gn in grupos["group_order"]:
        if "frlg" not in gn.lower():
            continue
        for mapa in grupos.get(gn, []):
            p = os.path.join(agora.raiz, "data/maps", mapa, "map.json")
            if not os.path.exists(p):
                continue
            d = json.load(open(p, encoding="utf-8"))
            lay = agora.layouts.get(d.get("layout"))
            if not lay or lay.get("secondary_tileset") != ROUTE17_TILESET:
                continue
            celulas, _w, _h = agora.grade(lay)
            corte = A.perfil(lay.get("layout_version") or "emerald")["corte"]
            for pal in celulas:
                mt = pal & 0x3FF
                if mt - corte in ROUTE17_LOCAIS:
                    censo[(mapa, mt)] += 1
    return censo


def aplica_route17(agora):
    versao = agora.layout_do_mapa("Route17_Frlg").get("layout_version") or "emerald"
    p = A.perfil(versao)
    pasta = agora.pastas[ROUTE17_TILESET]
    caminho = os.path.join(pasta, "metatile_attributes.bin")
    dados = bytearray(open(caminho, "rb").read())
    alvo = agora.mb[ROUTE17_BEHAVIOR]
    mudou = 0
    for local in ROUTE17_LOCAIS:
        off = local * p["largura"]
        palavra = struct.unpack_from("<I" if p["largura"] == 4 else "<H", dados, off)[0]
        novo = (palavra & ~p["mask_beh"]) | ((alvo << p["shift_beh"]) & p["mask_beh"])
        if novo != palavra:
            struct.pack_into("<I" if p["largura"] == 4 else "<H", dados, off, novo)
            mudou += 1
    if mudou:
        open(caminho, "wb").write(bytes(dados))
    return mudou


# ------------------------------------------------------------------ autoteste
def demo():
    """O portão: as duas travas mordem, e a máscara de escrita não vaza."""
    # (1) a escrita do comportamento só mexe nos bits do comportamento
    p = A.perfil("frlg")
    palavra = 0x41000108              # layerType 2, bits soltos, comportamento 0x108
    alvo = 0x0B
    novo = (palavra & ~p["mask_beh"]) | ((alvo << p["shift_beh"]) & p["mask_beh"])
    assert novo == 0x4100000B, hex(novo)
    assert A.par(novo, "frlg") == (0x0B, 2), A.par(novo, "frlg")

    # (2) a repintura do map.bin só mexe nos bits 0 a 9
    palavra = 0x3D6E                  # metatile 0x36E, colisão e elevação em cima
    repintado = (palavra & ~0x3FF) | (0x286 & 0x3FF)
    assert repintado & 0x3FF == 0x286 and repintado >> 10 == palavra >> 10

    # (3) a lista de mecânica não pode virar "tudo": água e chão comuns ficam de
    #     fora, senão o `--seafoam` repintaria oceano do Ikarus por oceano nosso
    assert "MB_OCEAN_WATER" not in MECANICA and "MB_CAVE" not in MECANICA
    assert "MB_MT_PYRE_HOLE" in MECANICA and "MB_NORTHWARD_CURRENT" in MECANICA

    # (4) os três metatiles da estrada existem e são do secundário da Celadon
    agora = Arvore(RAIZ)
    lay = agora.layout_do_mapa("Route17_Frlg")
    assert lay.get("secondary_tileset") == ROUTE17_TILESET
    sec = agora.atributos(ROUTE17_TILESET, lay.get("layout_version") or "emerald")
    assert len(sec) > max(ROUTE17_LOCAIS), f"o secundário encolheu para {len(sec)}"
    print("demo ok")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contra", help="árvore de ANTES da troca de arte (8212542e4a)")
    ap.add_argument("--seafoam", action="store_true")
    ap.add_argument("--route17", action="store_true")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()
    if not (a.seafoam or a.route17):
        a.seafoam = a.route17 = True

    agora = Arvore(RAIZ)

    if a.route17:
        censo = exclusividade_route17(agora)
        fora = {m for (m, _mt) in censo if m != "Route17_Frlg"}
        print("== Route 17: a estrada do Ikarus")
        for (mapa, mt), n in sorted(censo.items()):
            print(f"   {mapa:<24s} metatile {mt}: {n} células")
        if fora:
            raise SystemExit(f"os metatiles da estrada vazaram para {sorted(fora)}; "
                             "devolver comportamento a eles estragaria aqueles mapas")
        for local, mid, beh in planeja_route17(agora):
            print(f"   metatile {mid} (local {local}): {beh} -> {ROUTE17_BEHAVIOR}")
        if a.aplicar:
            print(f"   {aplica_route17(agora)} metatiles regravados")

    if a.seafoam:
        if not a.contra:
            raise SystemExit("--seafoam precisa de --contra <árvore de antes>")
        antes = Arvore(a.contra)
        plano = planeja_seafoam(agora, antes)
        print(f"== Seafoam Islands: {len(plano)} células com mecânica apagada")
        por = collections.Counter((m, b) for m, _x, _y, _v, _n, b in plano)
        for (mapa, beh), n in sorted(por.items()):
            print(f"   {mapa:<28s} {beh:<24s} {n} células")
        if a.aplicar:
            print(f"   {aplica_seafoam(agora, plano)} células repintadas")

    if not a.aplicar:
        print("\n(só medindo; use --aplicar para gravar)")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
