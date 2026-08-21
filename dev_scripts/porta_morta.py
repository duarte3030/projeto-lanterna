#!/usr/bin/env python3
"""Warp com comportamento de porta em cima de tile SOLIDO: acha e conserta.

    python3 dev_scripts/porta_morta.py            # censo, nao escreve
    python3 dev_scripts/porta_morta.py --demo     # autoteste, nao escreve
    python3 dev_scripts/porta_morta.py --aplicar  # escreve

O DEFEITO, medido em 21/08/2026
-------------------------------
`valida_warp_tile.py` conferia so o COMPORTAMENTO do metatile debaixo do warp.
Falta metade: quase todo caminho de warp do motor exige que o jogador ESTEJA no
tile (`TryStartWarpEventScript` -> `IsWarpMetatileBehavior` sobre a posicao
dele; `TryArrowWarp` e as escadas diagonais idem). Tile com COLISAO nunca e
pisado, entao comportamento certo em tile solido e warp morto.

A UNICA excecao e a porta ANIMADA: `TryDoorWarp` olha o tile da FRENTE quando o
jogador anda para o norte, e por isso a porta de casa de Hoenn e solida de
proposito em centenas de mapas legitimos. Ela so aceita `MB_ANIMATED_DOOR`.

Sonda no emulador que fechou o diagnostico: parado em (26,2) da `RavagedPath`,
ao lado do warp de (26,1), `UP*6` nao move o jogador e `DOWN*6` seguido de
`UP*8` tambem nao. O warp existia, apontava para o mapa certo, tinha o indice
certo dos dois lados e simplesmente nunca disparava.

O CONSERTO E UM BIT, e nao um metatile novo
-------------------------------------------
O tile ja E porta: o que sobra e a colisao. Zerar os dois bits de colisao da
palavra do `map.bin` deixa a arte, a elevacao e o comportamento exatamente como
estavam. Trocar o metatile mudaria o desenho do mapa sem precisar.

Elevacao fica como esta, inclusive quando e 0: `ELEVATION_TRANSITION` e o valor
normal de tile de porta, e os proprios `warp_events` destes mapas declaram
`elevation: 0`.

O QUE NAO E CONSERTADO, e por que
---------------------------------
Ver `RECUSADOS`. Em resumo: ginasio nao se mexe (o buraco do EcruteakCity_Gym e
quebra-cabeca, nao porta), porta ANIMADA solida e o padrao legitimo do motor, e
warp que so duplica um irmao que JA funciona nao esta trancando ninguem.
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import valida_warp_tile as V   # noqa: E402

REPO = V.RAIZ

# Recusa por MAPA, com o motivo medido. Nunca uma lista muda.
RECUSADOS = {
    "EcruteakCity_Gym": (
        "ginasio, fora de qualquer fronteira desta rodada, e os quatro warps "
        "sao MB_MT_PYRE_HOLE apontando para o PROPRIO mapa: e o quebra-cabeca "
        "de buraco no chao, nao porta emperrada. Zerar a colisao mudaria o "
        "enigma"),
    "Galar_Hammerlocke21": (
        "o warp 14 aponta para o proprio MAP_GALAR_HAMMERLOCKE_21. Warp que "
        "volta para onde ja se esta nao tranca ninguem, e Galar ainda esta em "
        "fase de conteudo: sem saber a cena, zerar colisao e chute"),
    "Galar_CrownTundra14": (
        "o metatile 774 aqui e MB_ANIMATED_DOOR e nao MB_NON_ANIMATED_DOOR "
        "(lido com o corte de 640 do layout_version frlg, que e o certo para "
        "Galar). Porta animada solida e o jeito CERTO do motor: TryDoorWarp le "
        "o tile da frente. Nao ha defeito aqui"),
    "SSAnne_Exterior_Frlg": (
        "os warps 0 e 4, em (31,5) e (33,5), sao gemeos do warp 2 de (32,5), "
        "que e o metatile 767 com COLISAO 0 e funciona. Os tres vao para o "
        "MAP_VERMILION_CITY e a passarela abaixo, em y=6, e andavel: o mapa "
        "nao esta trancado. Zerar a colisao poria o jogador em cima do casco "
        "do navio para consertar nada"),
}


def _layouts():
    return {l["id"]: l for l in json.load(
        open(f"{REPO}/data/layouts/layouts.json"))["layouts"]}


def censo():
    """[(mapa, i, x, y, metatile, comportamento, veredito, motivo)] do repo todo.

    A lista SAI da medida, sempre. Nao ha nome de mapa escrito a mao aqui: o que
    e escrito a mao e so a RECUSA, que e decisao e por isso vem com motivo.
    """
    layouts = _layouts()
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    cache, linhas = {}, []

    def atributos(ts):
        if ts not in cache:
            cache[ts] = V.tabela_de_atributos(ts)
        return cache[ts]

    for grp in grupos["group_order"]:
        for m in grupos.get(grp, []):
            p = f"{REPO}/data/maps/{m}/map.json"
            if not os.path.exists(p):
                continue
            d = json.load(open(p))
            warps = d.get("warp_events") or []
            lay = layouts.get(d.get("layout"))
            if not warps or not lay:
                continue
            bp = f"{REPO}/{lay.get('blockdata_filepath', '')}"
            if not os.path.exists(bp):
                continue
            blk = open(bp, "rb").read()
            w, h = lay["width"], lay["height"]
            prim, _ = atributos(lay.get("primary_tileset"))
            seg, _ = atributos(lay.get("secondary_tileset"))
            if prim is None or seg is None:
                continue
            # O corte primario/secundario e a CONSTANTE do motor, nunca o
            # tamanho do arquivo: 640 no ramo frlg/johto, 512 no resto. Ler
            # errado aqui foi o que fez o primeiro censo desta rodada dizer que
            # o SSAnne e o Galar_CrownTundra14 eram o mesmo defeito dos de
            # Sinnoh, e eles nao sao.
            corte = 640 if lay.get("layout_version", "") in ("frlg", "johto") else 512
            for i, wp in enumerate(warps):
                x, y = wp.get("x", 0), wp.get("y", 0)
                idx = (y * w + x) * 2
                if not (0 <= x < w and 0 <= y < h and idx + 2 <= len(blk)):
                    continue
                pal = struct.unpack("<H", blk[idx:idx + 2])[0]
                mt, col = pal & 0x3FF, (pal >> 10) & 3
                tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
                if rel >= len(tab) or not col:
                    continue
                c = tab[rel]
                if c not in V.COMPORTA_WARP or c in V.DISPARA_SENDO_SOLIDO:
                    continue
                motivo = RECUSADOS.get(m)
                linhas.append((m, i, x, y, mt, V.NOME.get(c, c),
                               "recusado" if motivo else "consertar", motivo))
    return linhas


def aplica():
    """Zera os dois bits de colisao dos alvos. Idempotente por natureza."""
    feitos, layouts = [], _layouts()
    for m, i, x, y, mt, mb, veredito, _motivo in censo():
        if veredito != "consertar":
            continue
        d = json.load(open(f"{REPO}/data/maps/{m}/map.json"))
        lay = layouts[d["layout"]]
        caminho = f"{REPO}/{lay['blockdata_filepath']}"
        b = bytearray(open(caminho, "rb").read())
        j = (y * lay["width"] + x) * 2
        antes = b[j] | (b[j + 1] << 8)
        depois = antes & ~(3 << 10)
        b[j], b[j + 1] = depois & 0xFF, depois >> 8
        open(caminho, "wb").write(bytes(b))
        feitos.append((m, i, x, y, mt, mb, antes, depois))
    return feitos


def imprime_censo():
    linhas = censo()
    print(f"{'mapa':30s} {'w':>3s} {'x,y':>9s} {'tile':>5s}  comportamento")
    for m, i, x, y, mt, mb, veredito, motivo in linhas:
        marca = " " if veredito == "consertar" else "R"
        print(f"{marca} {m:28s} {i:3d} {f'{x},{y}':>9s} {mt:5d}  {mb}")
        if motivo:
            print(f"      recusado: {motivo}")
    print(f"\n{sum(1 for l in linhas if l[6] == 'consertar')} a consertar, "
          f"{sum(1 for l in linhas if l[6] == 'recusado')} recusados com motivo")
    return 0


def demo():
    """Autoteste com mutacao plantada: o que quebra tem que ser PEGO."""
    # 1. A REGRA, que e do motor e nao minha. Porta animada solida dispara;
    #    porta nao animada solida nao. Mutacao plantada: inverter isso faria
    #    centenas de mapas legitimos de Hoenn virarem defeito.
    assert V.warp_morto(V._MB["MB_ANIMATED_DOOR"], 1)[0] is False
    assert V.warp_morto(V._MB["MB_NON_ANIMATED_DOOR"], 1)[0] is True
    assert V.warp_morto(V._MB["MB_NON_ANIMATED_DOOR"], 0)[0] is False
    assert V.warp_morto(V._MB["MB_NORMAL"], 0)[0] is True

    # 2. O corte de 640 do ramo frlg NAO e detalhe: com 512 o metatile 774 do
    #    Galar_CrownTundra14 le como porta NAO animada e o script "consertaria"
    #    um mapa que esta certo. Mutacao plantada, e ela ja aconteceu de
    #    verdade no primeiro censo desta rodada.
    lay = _layouts()[json.load(open(
        f"{REPO}/data/maps/Galar_CrownTundra14/map.json"))["layout"]]
    assert lay.get("layout_version") == "frlg", lay.get("layout_version")
    seg, _ = V.tabela_de_atributos(lay["secondary_tileset"])
    assert V.NOME.get(seg[774 - 640]) == "MB_ANIMATED_DOOR"

    # 3. O conserto e UM BIT: a arte e a elevacao nao podem andar.
    antes = 0x0706
    depois = antes & ~(3 << 10)
    assert depois & 0x3FF == antes & 0x3FF          # mesmo metatile
    assert (depois >> 12) & 0xF == (antes >> 12) & 0xF   # mesma elevacao
    assert (depois >> 10) & 3 == 0

    # 4. Toda recusa tem motivo escrito, e todo mapa recusado aparece mesmo no
    #    censo (recusa que nao e medida e so uma lista que envelhece calada).
    linhas = censo()
    assert all(l[7] for l in linhas if l[6] == "recusado")
    vistos = {l[0] for l in linhas}
    # Dois recusados NAO chegam ao censo, e isso e afirmacao e nao esquecimento:
    # o Galar_CrownTundra14 porque a porta dele e animada (item 2), e o SSAnne
    # porque o tile de (31,5) nem porta e. Cada um e provado onde mora.
    FORA_DO_CENSO = ("Galar_CrownTundra14", "SSAnne_Exterior_Frlg")
    for m in RECUSADOS:
        if m in FORA_DO_CENSO:
            assert m not in vistos, f"{m} entrou no censo: a recusa mudou de motivo"
            continue
        assert m in vistos, f"{m} esta em RECUSADOS e sumiu da medida"

    # 4.b O SSAnne nao esta trancado, e isso e MEDIDO e nao suposto: dos tres
    #     warps que vao para Vermilion, o do meio tem colisao ZERO, e a linha
    #     de baixo e andavel. Se um dia essa passagem fechar, a recusa cai.
    d = json.load(open(f"{REPO}/data/maps/SSAnne_Exterior_Frlg/map.json"))
    lay = _layouts()[d["layout"]]
    blk = open(f"{REPO}/{lay['blockdata_filepath']}", "rb").read()

    def palavra(x, y, _w=lay["width"]):
        i = (y * _w + x) * 2
        return blk[i] | (blk[i + 1] << 8)
    vivos = [w for w in d["warp_events"] if w["dest_map"] == "MAP_VERMILION_CITY"
             and not ((palavra(w["x"], w["y"]) >> 10) & 3)]
    assert vivos, "o SSAnne perdeu a passagem viva: a recusa nao vale mais"
    assert not (palavra(vivos[0]["x"], vivos[0]["y"] + 1) >> 10) & 3

    # 5. Depois de aplicado nao sobra alvo, e o que sobra e so recusa. Isto so
    #    vale depois do `--aplicar`, e por isso e condicional em vez de mentira.
    if not any(l[6] == "consertar" for l in linhas):
        assert {l[0] for l in linhas} <= set(RECUSADOS), linhas

    print("demo ok")
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--aplicar" in sys.argv:
        feitos = aplica()
        for m, i, x, y, mt, mb, antes, depois in feitos:
            print(f"{m:28s} warp{i} ({x},{y}) tile {mt} {mb}: "
                  f"0x{antes:04X} -> 0x{depois:04X}")
        print(f"\n{len(feitos)} portas destravadas")
        return 0
    return imprime_censo()


if __name__ == "__main__":
    sys.exit(main())
