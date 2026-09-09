#!/usr/bin/env python3
"""Fecha os achados E3 de Johto: o jogador para de sumir dentro do cenário.

Por que existe
--------------
A lente `E3` de `dev_scripts/qa/mapas_qa.py` ("bloco preto andável": célula
ALCANÇÁVEL cujo metatile tapa o jogador por inteiro) nasceu em 06/09/2026 com o
brejo da Route 212 South e deixou **405 células de Johto abertas**. A rodada que
abriu a lente registrou a suspeita de que os 405 eram o MESMO defeito do brejo,
ou seja camada `NORMAL` que devia ser `COVERED`. Medido aqui, célula a célula,
com a arte das duas camadas na tela: **não eram**. São TRÊS defeitos diferentes,
e cada um se conserta em um lugar diferente.

    1. CAMADA, no `metatile_attributes.bin` do tileset.
       `EcruteakCity_Gym`, 46 células, metatile 811 (local 171 do
       `gTileset_EcruteakCityGym`). O ginásio de Morty é o quebra-cabeça dos
       BURACOS: 107 dos 108 warps do mapa levam de volta para a entrada, e todos
       eles ficam em cima de uma célula desse metatile. O metatile é preto puro
       nas DUAS camadas (256 px opacos em cada, os 4 quadrantes idênticos), e
       vem com tipo NORMAL: a camada de cima vai para o BG1, que é desenhado
       acima de todo sprite, e o jogador some no instante em que pisa no buraco.
       Fechar a célula não serve, porque é POR ELA que se anda: os buracos são o
       enigma. `COVERED` põe a mesma arte preta no BG2, abaixo do sprite, e o
       jogador aparece caindo no buraco em vez de evaporar.

    2. COLISÃO, no `map.bin` do mapa, em parede desenhada na camada de cima.
       `OlivineCity_Lighthouse` 29 células (o parapeito do poço do farol na
       linha 6 e o beiral da linha 17) e `Route34` 2 células (a lateral da casa
       de telhado azul). Nesses metatiles a camada de BAIXO está VAZIA e a de
       cima traz parede inteira: desenhar por cima do jogador é o certo, e o
       defeito é a célula ter vindo com colisão 0. Passá-los para `COVERED` só
       trocaria "o jogador sumiu" por "o jogador andando por dentro da parede".
       Medido: o metatile 674 do `gTileset_Lighthouse` tem 208 usos SÓLIDOS
       contra 18 andáveis, e os 641/642 do `gTileset_Goldenrod` têm 16 e 31
       sólidos contra 5 e 13. Nenhuma das 31 células tem warp, objeto, placa ou
       gatilho em cima, e nenhuma delas é passagem: as duas faixas são becos com
       célula sólida do outro lado.

    3. COLISÃO, no `map.bin`, em ENCHIMENTO preto fora da sala.
       `NewBarkTown_Lab`, 312 células, metatile 0. O layout é 40x14 e guarda
       DUAS salas: o laboratório (colunas 0 a 12, vedado) e uma segunda sala
       ligada ao warp 1, em (25,9). A segunda sala NÃO está vedada, e a partir
       dela a BFS entra no vazio preto e caminha pelas 312 células, que são
       metatile 0 com colisão 0. Aqui não há arte para consertar: o conserto é
       vedar, e o alvo é toda célula de metatile 0 do layout.

O que ele NÃO toca, e por quê
-----------------------------
`GoldenrodCity` (14 células) e `Route26` (2) são do tipo 2 e teriam o mesmo
conserto de colisão, mas os dois estão na lista `SOB_CARIMBO` do
`dev_scripts/qa/lente_carimbo.py`: mexer neles muda o carimbo de CAMINHO (bits
10 a 15) e obriga a regravar `carimbo_comportamento.json`, que é decisão de
condutor e não de executor. A trava está escrita no código, não no comentário:
`SOB_CARIMBO` é lida do próprio módulo da lente, e mapa carimbado é recusado.
Pelo mesmo motivo o `gTileset_Goldenrod` e o `gTileset_JohtoGeneral` não podem
receber conserto de CAMADA: os dois vestem mapas carimbados, e o carimbo de
COMPORTAMENTO guarda o `layerType` de cada célula.

Uso
---
    python3 dev_scripts/conserta_e3_johto.py            # só mede
    python3 dev_scripts/conserta_e3_johto.py --aplica   # grava
    python3 dev_scripts/conserta_e3_johto.py --demo     # autoteste

Idempotente: a segunda passada com `--aplica` grava 0, porque a camada já é
`COVERED` e as células já estão fechadas.
"""
import argparse
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts", "qa"))
import lente_carimbo as LC  # noqa: E402

COVERED = 1
MAPGRID_METATILE_ID_MASK = 0x03FF
MAPGRID_COLLISION_MASK = 0x0C00
MAPGRID_COLLISION_SHIFT = 10

# ---------------------------------------------------------------- os alvos
# Cada linha traz o motivo MEDIDO, porque daqui a um mês a lista sozinha vira
# adivinhação. "local" é o índice DENTRO do tileset, não o índice no mapa.
CAMADA = (
    dict(tileset="gTileset_EcruteakCityGym", locais=(171,),
         motivo="buraco do quebra-cabeça do ginásio de Morty: preto puro nas "
                "duas camadas, e é por ele que se anda (107 warps em cima)"),
)

# Colisão por REGRA, nunca por lista de coordenadas: coordenada crava a árvore
# de hoje e mente na primeira vez que alguém mexer no mapa.
COLISAO = (
    dict(mapa="NewBarkTown_Lab", metatiles=(0,),
         motivo="enchimento preto entre as duas salas do layout 40x14; a sala "
                "do warp 1 não está vedada e a BFS entra no vazio"),
    dict(mapa="OlivineCity_Lighthouse", metatiles=(674, 936, 937, 938),
         motivo="parapeito do poço e beiral: camada de baixo vazia, camada de "
                "cima com parede inteira, e 208 usos sólidos contra 18"),
    dict(mapa="Route34", metatiles=(641, 642),
         motivo="lateral da casa de telhado azul, os mesmos metatiles de parede "
                "que Goldenrod usa sólidos 16 e 31 vezes"),
)


def layouts():
    with open(os.path.join(RAIZ, "data/layouts/layouts.json"), encoding="utf-8") as f:
        return {l["id"]: l for l in json.load(f)["layouts"]}


def layout_do_mapa(nome, tabela):
    p = os.path.join(RAIZ, "data/maps", nome, "map.json")
    with open(p, encoding="utf-8") as f:
        return tabela[json.load(f)["layout"]]


def mapas_do_tileset(rotulo, tabela):
    """Todo mapa da árvore que veste este tileset, primário ou secundário."""
    fora = set()
    base = os.path.join(RAIZ, "data/maps")
    for nome in sorted(os.listdir(base)):
        p = os.path.join(base, nome, "map.json")
        if not os.path.exists(p):
            continue
        with open(p, encoding="utf-8") as f:
            L = tabela.get(json.load(f).get("layout"))
        if not L:
            continue
        if rotulo in (L.get("primary_tileset"), L.get("secondary_tileset")):
            fora.add(nome)
    return fora


def grava_camada(rotulo, locais, aplica):
    """Marca COVERED os metatiles do tileset. Devolve quantos mudariam."""
    pasta = LC.pasta_do_tileset(rotulo)
    if not pasta:
        raise SystemExit("tileset %s sem pasta" % rotulo)
    pa = os.path.join(pasta, "metatile_attributes.bin")
    pm = os.path.join(pasta, "metatiles.bin")
    n = os.path.getsize(pm) // 16
    b = bytearray(open(pa, "rb").read())
    larg = len(b) // n if n else 2
    mudou = 0
    for i in locais:
        if larg == 4:
            v = struct.unpack_from("<I", b, i * 4)[0]
            novo = (v & ~(3 << 29)) | (COVERED << 29)
            if novo != v:
                struct.pack_into("<I", b, i * 4, novo)
                mudou += 1
        else:
            v = struct.unpack_from("<H", b, i * 2)[0]
            novo = (v & ~0xF000) | (COVERED << 12)
            if novo != v:
                struct.pack_into("<H", b, i * 2, novo)
                mudou += 1
    if mudou and aplica:
        open(pa, "wb").write(bytes(b))
    return mudou


def grava_colisao(nome, metatiles, tabela, aplica):
    """Fecha (colisão 1) toda célula do mapa cujo metatile está na lista.

    Mexe SÓ nos bits 10 e 11. O id do metatile (bits 0 a 9) e a elevação (bits
    12 a 15) saem idênticos, e é isso que a `lente_carimbo` mede.
    """
    L = layout_do_mapa(nome, tabela)
    caminho = os.path.join(RAIZ, L["blockdata_filepath"])
    W, H = L["width"], L["height"]
    b = bytearray(open(caminho, "rb").read())
    alvo = set(metatiles)
    mudou = 0
    for i in range(W * H):
        v = struct.unpack_from("<H", b, i * 2)[0]
        if (v & MAPGRID_METATILE_ID_MASK) not in alvo:
            continue
        if (v & MAPGRID_COLLISION_MASK) >> MAPGRID_COLLISION_SHIFT:
            continue
        struct.pack_into("<H", b, i * 2, v | (1 << MAPGRID_COLLISION_SHIFT))
        mudou += 1
    if mudou and aplica:
        open(caminho, "wb").write(bytes(b))
    return mudou


def eventos_em_cima(nome, metatiles, tabela):
    """Warp, objeto, placa ou gatilho em célula que o conserto vai fechar.

    Fechar célula com warp em cima cria achado A2 ("o jogador nasce dentro da
    parede"), e é a única maneira de este conserto piorar outra regra. Por isso
    ele é medido AQUI e não depois do commit.
    """
    with open(os.path.join(RAIZ, "data/maps", nome, "map.json"), encoding="utf-8") as f:
        d = json.load(f)
    L = tabela[d["layout"]]
    W, H = L["width"], L["height"]
    g = struct.unpack_from(
        "<%dH" % (W * H), open(os.path.join(RAIZ, L["blockdata_filepath"]), "rb").read(), 0)
    alvo = set(metatiles)
    fora = []
    for chave in ("warp_events", "object_events", "bg_events", "coord_events"):
        for e in d.get(chave, []):
            x, y = e.get("x"), e.get("y")
            if x is None or not (0 <= x < W and 0 <= y < H):
                continue
            v = g[y * W + x]
            if (v & MAPGRID_METATILE_ID_MASK) in alvo and not (v & MAPGRID_COLLISION_MASK):
                fora.append((chave, x, y))
    return fora


def demo():
    """Autoteste: os dois gravadores mexem SÓ no campo que prometem."""
    ruim = 0

    def falso(msg):
        nonlocal ruim
        ruim = 1
        print("  conserta_e3_johto DEMO: " + msg)

    # 1. a escrita de camada de 16 bits preserva o comportamento (bits 0 a 7)
    for v in (0x0000, 0x2008, 0x3011, 0xF0FF):
        novo = (v & ~0xF000) | (COVERED << 12)
        if (novo & 0x0FFF) != (v & 0x0FFF):
            falso("a escrita de camada sujou o comportamento de 0x%04X" % v)
        if (novo >> 12) != COVERED:
            falso("a camada de 0x%04X não virou COVERED" % v)

    # 2. a escrita de colisão preserva metatile e elevação
    for v in (0x0000, 0x028B, 0x3FFF & ~MAPGRID_COLLISION_MASK, 0xF2C1):
        novo = v | (1 << MAPGRID_COLLISION_SHIFT)
        if (novo & MAPGRID_METATILE_ID_MASK) != (v & MAPGRID_METATILE_ID_MASK):
            falso("a escrita de colisão mexeu no metatile de 0x%04X" % v)
        if (novo & 0xF000) != (v & 0xF000):
            falso("a escrita de colisão mexeu na elevação de 0x%04X" % v)
        if not (novo & MAPGRID_COLLISION_MASK):
            falso("a célula 0x%04X não ficou sólida" % v)

    # 3. a trava do carimbo é de verdade: nenhum alvo pode encostar em mapa
    #    carimbado, nem pelo mapa nem pelo tileset que ele veste.
    tabela = layouts()
    carimbados = set(LC.SOB_CARIMBO)
    for a in COLISAO:
        if a["mapa"] in carimbados:
            falso("o mapa %s está SOB_CARIMBO e é alvo de colisão" % a["mapa"])
    for a in CAMADA:
        sujos = sorted(mapas_do_tileset(a["tileset"], tabela) & carimbados)
        if sujos:
            falso("o tileset %s veste mapa carimbado: %s"
                  % (a["tileset"], ", ".join(sujos)))

    # 4. os alvos ainda existem na árvore: lista que aponta para o vazio é
    #    conserto que passou a mentir sem ninguém notar.
    for a in CAMADA:
        pasta = LC.pasta_do_tileset(a["tileset"])
        if not pasta or not os.path.exists(os.path.join(pasta, "metatile_attributes.bin")):
            falso("o tileset %s sumiu da árvore" % a["tileset"])
            continue
        n = os.path.getsize(os.path.join(pasta, "metatiles.bin")) // 16
        for i in a["locais"]:
            if i >= n:
                falso("o metatile %d não existe em %s" % (i, a["tileset"]))
    for a in COLISAO:
        if not os.path.exists(os.path.join(RAIZ, "data/maps", a["mapa"], "map.json")):
            falso("o mapa %s sumiu da árvore" % a["mapa"])

    if not ruim:
        print("demo ok")
    return ruim


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        return demo()

    tabela = layouts()
    carimbados = set(LC.SOB_CARIMBO)
    total = 0

    for alvo in CAMADA:
        sujos = sorted(mapas_do_tileset(alvo["tileset"], tabela) & carimbados)
        if sujos:
            raise SystemExit("RECUSADO: %s veste mapa carimbado (%s); mudar a "
                             "camada obriga a regravar o carimbo"
                             % (alvo["tileset"], ", ".join(sujos)))
        n = grava_camada(alvo["tileset"], alvo["locais"], a.aplica)
        total += n
        print("camada  %-28s %s -> COVERED: %d entradas  (%s)"
              % (alvo["tileset"], list(alvo["locais"]), n, alvo["motivo"]))

    for alvo in COLISAO:
        if alvo["mapa"] in carimbados:
            raise SystemExit("RECUSADO: %s está SOB_CARIMBO" % alvo["mapa"])
        maus = eventos_em_cima(alvo["mapa"], alvo["metatiles"], tabela)
        if maus:
            raise SystemExit("RECUSADO: %s tem evento em célula que seria "
                             "fechada: %s" % (alvo["mapa"], maus))
        n = grava_colisao(alvo["mapa"], alvo["metatiles"], tabela, a.aplica)
        total += n
        print("colisão %-28s metatiles %s: %d células  (%s)"
              % (alvo["mapa"], list(alvo["metatiles"]), n, alvo["motivo"]))

    print("\n%d escritas%s" % (total, "" if a.aplica else " (só medindo; use --aplica)"))
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
