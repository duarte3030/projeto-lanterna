#!/usr/bin/env python3
"""Fecha os 11 destinos que `abre_portas_extras_sinnoh.py` nao conseguiu abrir.

    python3 dev_scripts/abre_portas_teimosas_sinnoh.py            # so relata
    python3 dev_scripts/abre_portas_teimosas_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/abre_portas_teimosas_sinnoh.py --demo     # autoteste

Os dois motivos que sobraram, e o que muda aqui
-----------------------------------------------
1. **"nao tem predio sem porta"** (3 casas de Celestic, 2 de Solaceon, a casa
   leste de Sunyshore e o Ribbon Syndicate). O teste de PREDIO de
   `abre_portas_extras_sinnoh.py` exige bloco cheio, largo, longe da borda e com
   fachada de 3 tiles. Celestic e uma cratera e Resort Area e uma praia: la o
   que existe e parede de pedra, e nenhum bloco passa. Aqui o teste e o mesmo
   que abriu as bocas de caverna (`abre_bocas_cavernas_sinnoh.candidatos`):
   tile bloqueado, chao andavel logo abaixo, vizinhos de cima, esquerda e
   direita bloqueados. E o meio de uma parede, que e onde uma porta cabe, seja
   ela de casa ou de pedra.

2. **"nao e mapa de rua"** (`ETERNA_CITY_CONDOMINIUMS_2F`, os dois
   `UNUSED_*_3F` e `ROTOMS_ROOM`). Esses precisam de ESCADA dentro de um layout
   COMPARTILHADO: a planta de casa serve 74 mapas e a do
   `TeamGalacticEternaBuilding_1F` e a do Weather Institute, de HOENN. Desenhar
   nela poria escada morta em 73 casas e mudaria Hoenn. Aqui o layout e CLONADO
   antes (`abre_bocas_cavernas_sinnoh.clona_layout`) e so a copia e furada.

De onde sai a palavra de 16 bits
--------------------------------
Mesma regra de sempre, um passo mais larga: copiada de um warp que ja existe.
Quando o proprio mapa nao tem porta nenhuma para copiar (uma casa so tem o
capacho de saida, que e seta e nao dispara por cima), a palavra vem de outro
mapa que usa **o mesmo par de tilesets**, o que mantem desenho, colisao e
comportamento validos. Fora disso nao se escreve nada.

Posicao: por ancora, igual as bocas de caverna. Interior do Platinum tem
coordenada local, entao o delta entre um destino que os dois lados tem (a porta
de descida do andar, por exemplo) da a translacao.

Compatibilidade de save: layout novo e mapa novo no FIM das listas, warp novo no
FIM do mapa que ja existe.
"""
import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import abre_bocas_cavernas_sinnoh as B   # noqa: E402
import abre_portas_extras_sinnoh as A    # noqa: E402
import fecha_portas_sinnoh as F          # noqa: E402
import importa_npcs_sinnoh as I          # noqa: E402
import valida_mapas_sinnoh as V          # noqa: E402
import valida_warp_tile as W             # noqa: E402

APLICAR = "--aplicar" in sys.argv
GRUPO = A.GRUPO
PORTAS = {W._MB[n] for n in ("MB_NON_ANIMATED_DOOR", "MB_ANIMATED_DOOR")}


def palavra_ampla(mapa):
    """Palavra de porta valida neste mapa, procurada por PAR DE TILESETS.

    `abre_portas_extras_sinnoh.palavra_de_porta` so olha o proprio mapa, e uma
    casa comum nao tem porta para copiar: o unico warp dela e o capacho de
    saida, que e `MB_SOUTH_ARROW_WARP` e so dispara quem anda para o sul. Como o
    metatile e do TILESET, qualquer mapa com o mesmo par serve de fonte, e o
    desenho continua o daquela parede.
    """
    _d, lay, _w, _h, pal, comp = A._grade(mapa)
    conta = {}
    for p in pal:
        if comp(p) in PORTAS:
            conta[p] = conta.get(p, 0) + 1
    if conta:
        return max(conta, key=conta.get)
    par = (lay.get("primary_tileset"), lay.get("secondary_tileset"))
    for outro in sorted(os.listdir(f"{REPO}/data/maps")):
        if not os.path.exists(f"{REPO}/data/maps/{outro}/map.json"):
            continue
        try:
            _d2, l2, w2, _h2, p2, c2 = A._grade(outro)
        except (KeyError, FileNotFoundError, OSError):
            continue
        if (l2.get("primary_tileset"), l2.get("secondary_tileset")) != par:
            continue
        for p in p2:
            if c2(p) in PORTAS:
                return p
    return None


def planeja():
    """[(pai, header, arquetipo, (x,y), palavra)] do que da para abrir agora."""
    heads = I.headers_do_platinum()
    por_pai = {}
    for pai, header, arq in A.pendencias():
        por_pai.setdefault(pai, []).append((header, arq))
    planos, fora = [], []
    for pai, itens in sorted(por_pai.items()):
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        pal = palavra_ampla(pai)
        cands = B.candidatos(pai)
        anc = B.ancoras(pai, d, heads)
        deles = alvos_da_fonte(pai, d, heads)
        usados = set()
        for header, arq in itens:
            livres = [c for c in cands if (c[0], c[1]) not in usados]
            escolha = B.escolhe(livres, anc, deles.get(header))
            if pal is None or escolha is None:
                fora.append((header, f"{pai}: "
                             + ("nenhum tile passa no teste de parede"
                                if escolha is None else
                                "nenhum mapa do mesmo par de tilesets tem porta")))
                continue
            usados.add((escolha[0], escolha[1]))
            planos.append((pai, header, arq, (escolha[0], escolha[1]), pal))
    return planos, fora


def alvos_da_fonte(pai, d, heads):
    """header do destino -> (x, z) do warp dele no Platinum."""
    ph = B.header_do_mapa(pai, d, heads)
    if not ph:
        return {}
    pe = os.path.join(B.C.PLAT, "res/field/events", heads[ph][0] + ".json")
    if not os.path.exists(pe):
        return {}
    saida = {}
    for w in json.load(open(pe)).get("warp_events", []):
        saida.setdefault(w["dest_header_id"], (int(w["x"]), int(w["z"])))
    return saida


def main():
    if "--demo" in sys.argv:
        return demo()
    planos, fora = planeja()
    print(f"destinos que sobraram: {len(planos) + len(fora)}")
    print(f"da para abrir agora: {len(planos)}")
    for header, m in fora:
        print(f"   {header.replace('MAP_HEADER_', '')}: {m}")
    for pai, header, arq, (x, y), p in planos:
        print(f"   {pai:32} ({x:3},{y:3}) 0x{p:04X} -> "
              f"{header.replace('MAP_HEADER_', '')} ({arq})")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        return 0

    sprites = V.sprites_utilizaveis()
    movimentos = V.constantes("include/constants/event_object_movement.h",
                              "MOVEMENT_TYPE_")
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    F.grupo_com_vaga(grupos, GRUPO)
    incs = []
    conta = {"mapas": 0, "npcs": 0, "placas": 0, "textos": 0, "clones": 0,
             "movidos": 0}
    for pai, header, arq, (x, y), palavra in planos:
        d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
        if len(A.mapas_do_layout(d["layout"])) > 1:
            B.clona_layout(pai, d)
            d = json.load(open(f"{REPO}/data/maps/{pai}/map.json"))
            conta["clones"] += 1
        conta["movidos"] += A.libera_tile(pai, x, y)
        A.grava_tile(d["layout"], x, y, palavra)
        p_pai = f"{REPO}/data/maps/{pai}/map.json"
        d_pai = json.load(open(p_pai))
        d_pai.setdefault("warp_events", [])
        idx = len(d_pai["warp_events"])
        d_pai["warp_events"].append({
            "x": x, "y": y, "elevation": 0,
            "dest_map": F.const_do_header(header), "dest_warp_id": "0"})
        json.dump(d_pai, open(p_pai, "w"), indent=2, ensure_ascii=False)
        A.escreve_mapa(F.nome_de_pasta(header), header, arq, d_pai["id"], idx,
                       grupos, incs, sprites, movimentos, conta)

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
    print(f"\naplicado: {conta['mapas']} mapas, {conta['clones']} layouts "
          f"clonados, {conta['npcs']} NPCs, {conta['placas']} placas, "
          f"{conta['textos']} textos do Platinum, "
          f"{conta['movidos']} objetos empurrados de cima da porta")
    return 0


def demo():
    """O que prova que a porta nasce em parede, e viva."""
    # 1. Celestic e uma cratera: o teste de PREDIO nao acha nada, e o de parede
    #    acha. Se os dois achassem o mesmo, este script nao precisaria existir.
    assert not A.predios_sem_porta("CelesticTown")
    assert B.candidatos("CelesticTown")
    # 2. o tile escolhido esta bloqueado hoje e tem chao logo abaixo.
    for mapa in ("CelesticTown", "ResortArea", "SunyshoreCity"):
        _d, _l, w, _h, pal, _c = A._grade(mapa)
        for x, y, _p, _a in B.candidatos(mapa)[:40]:
            assert (pal[y * w + x] >> 10) & 3, (mapa, x, y)
            assert not ((pal[(y + 1) * w + x] >> 10) & 3), (mapa, x, y)
    # 3. a palavra escrita dispara de verdade, lida da mesma tabela do motor.
    #    A casa de Eterna e o caso que forcou a busca por par de tilesets: o
    #    unico warp dela e o capacho de saida, que e seta.
    for mapa in ("CelesticTown", "EternaCityCondominiums1F",
                 "TeamGalacticEternaBuilding_1F"):
        p = palavra_ampla(mapa)
        _d, _l, _w, _h, _pal, comp = A._grade(mapa)
        assert p is not None and comp(p) in W.COMPORTA_WARP, (mapa, p)
    # 4. layout compartilhado nunca e furado: furar o original poria escada
    #    morta em casa que nao sobe, e no caso do Weather Institute mudaria
    #    HOENN. Quem ganha escada ganha antes uma COPIA `_PROPRIO`.
    #    A versao anterior cravava "EternaCityCondominiums1F usa layout
    #    compartilhado" e envelheceu calada, porque a copia dele foi feita nesse
    #    dia e o mapa passou a ser dono do proprio layout (licao 4.11). O fato
    #    permanente e este: toda copia `_PROPRIO` tem UM dono so.
    for mapa in ("EternaCityCondominiums1F", "TeamGalacticEternaBuilding_1F"):
        d = json.load(open(f"{REPO}/data/maps/{mapa}/map.json"))
        assert A.mapas_do_layout(d["layout"]) == [mapa], (mapa, d["layout"])
    #    E o layout de Hoenn que o predio da Galactica usava continua LA,
    #    intocado: se a copia tivesse sido feita errado, o Weather Institute
    #    teria ganhado uma escada no meio da sala.
    donos = A.mapas_do_layout("LAYOUT_ROUTE119_WEATHER_INSTITUTE_1F")
    assert donos and all(not m.startswith(("Eterna", "TeamGalactic"))
                         for m in donos), donos
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
