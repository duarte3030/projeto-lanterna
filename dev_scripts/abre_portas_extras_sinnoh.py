#!/usr/bin/env python3
"""Fecha o que `fecha_portas_sinnoh.py` deixou de fora por falta de porta.

    python3 dev_scripts/abre_portas_extras_sinnoh.py            # so relata
    python3 dev_scripts/abre_portas_extras_sinnoh.py --aplicar  # escreve
    python3 dev_scripts/abre_portas_extras_sinnoh.py --demo     # autoteste

O buraco que ele fecha
----------------------
`fecha_portas_sinnoh.py` so usa porta que JA existe desenhada no nosso
`map.bin`. Sobraram 39 destinos sem porta livre: 18 `POKECENTER_B1F` (o
arquetipo de centro Pokemon do repo tem uma escada so, e ela foi para o 2F) e 21
predios de cidade (a cidade tem menos porta orfa do que o Platinum tem predio).

A decisao que vale mais que o codigo: **desenhar a porta, copiando um tile que o
proprio mapa ja tem**. Nao se inventa metatile e nao se le tabela de tileset de
cabeca. O tile novo e a palavra de 16 bits COPIADA de outro warp do mesmo mapa,
entao ele nasce com o mesmo desenho, a mesma colisao, a mesma elevacao e o mesmo
comportamento de porta que o motor ja aceita. `valida_warp_tile.py` confirma
depois que o warp dispara.

Onde a porta pode ser desenhada, e onde nao pode
------------------------------------------------
- **Cidade:** so no rodape de um PREDIO SEM PORTA. Predio e um bloco conexo de
  tiles bloqueados que (a) nao encosta na borda do mapa, senao e o paredao de
  pedra que cerca a cidade, (b) tem area >= 6, senao e arvore 2x2, e (c) tem
  chao andavel logo abaixo, senao a porta nasce dentro da parede. Bloco que ja
  tem porta e pulado: predio nao ganha segunda porta.
- **Interior:** so escada, e so em layout cujos usuarios TODOS precisam dela.
  Medido: `LAYOUT_OREBURGH_CITY_POKEMON_CENTER_1F` e usado por 15 mapas e os 15
  querem um B1F, entao nenhum deles fica com escada morta. Layout compartilhado
  com mapa que nao precisa (a planta de casa, usada por 64 mapas; a do
  Weather Institute, que e de HOENN) fica de fora: a escada apareceria em mapa
  que nao tem para onde subir.

Compatibilidade de save: mapa novo entra no FIM do grupo que
`fecha_portas_sinnoh.py` criou, e warp novo entra no FIM da lista do mapa que ja
existe. Nenhum indice antigo anda.
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import fecha_portas_sinnoh as F   # noqa: E402
import importa_npcs_sinnoh as I   # noqa: E402
import valida_mapas_sinnoh as V   # noqa: E402
import valida_warp_tile as W      # noqa: E402

APLICAR = "--aplicar" in sys.argv
GRUPO = F.GRUPO_NOVO

# Escada extra dos centros Pokemon. A geometria dos quatro layouts de centro do
# repo e a mesma (medida tile a tile): a escada do 2F fica em (1,6), colada na
# parede oeste, e (13,6) e o espelho dela na parede leste, andavel e alcancavel
# pela coluna 13. Por isso a escolha e fixa e nao heuristica.
ESCADA_PC = (13, 6)
LAYOUTS_PC = {
    "LAYOUT_OREBURGH_CITY_POKEMON_CENTER_1F",
    "LAYOUT_FLOAROMA_TOWN_POKEMON_CENTER_1F",
    "LAYOUT_JUBILIFE_CITY_POKEMON_CENTER_1F",
    "LAYOUT_SANDGEM_TOWN_POKEMON_CENTER_1F",
}


# ------------------------------------------------------------------ leitura
def _grade(mapa):
    """(map.json, layout, largura, altura, palavras, comportamento)."""
    d = json.load(open(f"{REPO}/data/maps/{mapa}/map.json"))
    lay = F.layouts()[d["layout"]]
    blk = open(f"{REPO}/{lay['blockdata_filepath']}", "rb").read()
    w, h = lay["width"], lay["height"]
    prim, _ = F._atributos(lay.get("primary_tileset"))
    seg, _ = F._atributos(lay.get("secondary_tileset"))
    corte = 640 if lay.get("layout_version", "") in ("frlg", "johto") else 512
    palavras = list(struct.unpack(f"<{w * h}H", blk[:w * h * 2]))

    def comportamento(word):
        mt = word & 0x3FF
        tab, rel = (prim, mt) if mt < corte else (seg, mt - corte)
        return tab[rel] if rel < len(tab) else -1
    return d, lay, w, h, palavras, comportamento


def predios_sem_porta(mapa):
    """Rodapes onde da para desenhar porta nova. Lista de (x, y, area)."""
    _d, _lay, w, h, pal, comp = _grade(mapa)
    col = lambda x, y: (pal[y * w + x] >> 10) & 3          # noqa: E731
    porta = lambda x, y: comp(pal[y * w + x]) in W.COMPORTA_WARP  # noqa: E731
    visto = bytearray(w * h)
    saida = []
    for y0 in range(h):
        for x0 in range(w):
            if visto[y0 * w + x0] or not col(x0, y0):
                continue
            pilha, comp_tiles, borda = [(x0, y0)], [], False
            visto[y0 * w + x0] = 1
            while pilha:
                x, y = pilha.pop()
                comp_tiles.append((x, y))
                if x in (0, w - 1) or y in (0, h - 1):
                    borda = True
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not visto[ny * w + nx] \
                            and col(nx, ny):
                        visto[ny * w + nx] = 1
                        pilha.append((nx, ny))
            # borda = paredao que cerca a cidade; area < 6 = arvore 2x2
            if borda or len(comp_tiles) < 6:
                continue
            if any(porta(x, y) for x, y in comp_tiles):
                continue
            # Predio e um bloco CHEIO e largo. Sem estas tres contas o bloco
            # conexo tambem pega cerca, penhasco e a parede da cratera de
            # Celestic, e a porta nasceria no meio da pedra. Medido: a coluna
            # x=20 de CanalaveCity (uma cerca de 10 tiles de altura) passava.
            xs = [x for x, _y in comp_tiles]
            ys = [y for _x, y in comp_tiles]
            bw, bh = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
            if bw < 3 or bh < 2 or len(comp_tiles) / (bw * bh) < 0.6:
                continue
            base = [(x, y) for x, y in comp_tiles
                    if y + 1 < h and not col(x, y + 1) and not porta(x, y + 1)]
            if not base:
                continue
            ymax = max(y for _x, y in base)
            fila = sorted(x for x, y in base if y == ymax)
            # a fachada tem que ter 3 tiles seguidos: porta de 1 tile de largura
            # em cima de um toco de parede nao e predio.
            corridas, atual = [], [fila[0]]
            for x in fila[1:]:
                if x == atual[-1] + 1:
                    atual.append(x)
                else:
                    corridas.append(atual)
                    atual = [x]
            corridas.append(atual)
            corridas = [c for c in corridas if len(c) >= 3]
            if not corridas:
                continue
            maior = max(corridas, key=len)
            saida.append((maior[len(maior) // 2], ymax, len(comp_tiles)))
    return saida


def palavra_de_porta(mapa, alvo):
    """Palavra de 16 bits a copiar: a porta do mapa mais parecida com o alvo.

    "Parecida" = os vizinhos horizontais tem a mesma palavra, ou seja, e porta na
    mesma parede e no mesmo estilo de predio. Sem empate perfeito, vale a porta
    mais comum do mapa, que e o estilo dominante da cidade.
    """
    _d, _lay, w, h, pal, comp = _grade(mapa)
    ax, ay = alvo
    viz = lambda x, y: (pal[y * w + x - 1] if x else -1,     # noqa: E731
                        pal[y * w + x + 1] if x + 1 < w else -1)
    portas = [(x, y) for y in range(h) for x in range(w)
              if comp(pal[y * w + x]) in W.COMPORTA_WARP]
    if not portas:
        return None
    for x, y in portas:
        if viz(x, y) == viz(ax, ay):
            return pal[y * w + x]
    contagem = {}
    for x, y in portas:
        p = pal[y * w + x]
        contagem[p] = contagem.get(p, 0) + 1
    return max(contagem, key=contagem.get)


def mapas_do_layout(layout_id):
    """Todo map.json que aponta para este layout. O map.bin e do layout, nao do
    mapa: desenhar porta nele muda todos de uma vez."""
    saida = []
    for pasta in sorted(os.listdir(f"{REPO}/data/maps")):
        f = f"{REPO}/data/maps/{pasta}/map.json"
        if os.path.exists(f) and json.load(open(f)).get("layout") == layout_id:
            saida.append(pasta)
    return saida


def libera_tile(mapa, x, y):
    """Tira de cima de (x,y) NPC ou placa que ja estivesse la.

    Medido: `EternaCityPokecenter1F` tinha uma NPC importada exatamente em
    (13,6). Escada com gente em cima e escada que nao da para pisar, e o
    importador de NPC ja empurra por tile livre, entao aqui e a mesma conta.
    """
    p = f"{REPO}/data/maps/{mapa}/map.json"
    d = json.load(open(p))
    lay = F.layouts()[d["layout"]]
    ocupados = {(e["x"], e["y"]) for e in (d.get("object_events") or [])}
    ocupados |= {(e["x"], e["y"]) for e in (d.get("bg_events") or [])}
    ocupados.add((x, y))
    mexeu = 0
    for lista in ("object_events", "bg_events"):
        for e in d.get(lista) or []:
            if (e["x"], e["y"]) != (x, y):
                continue
            novo = I.livre(F.layouts(), d["layout"], x, y, ocupados)
            if not novo:
                continue
            e["x"], e["y"] = novo
            ocupados.add(novo)
            mexeu += 1
    if mexeu:
        json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)
    return mexeu


def grava_tile(layout_id, x, y, palavra):
    lay = F.layouts()[layout_id]
    caminho = f"{REPO}/{lay['blockdata_filepath']}"
    dados = bytearray(open(caminho, "rb").read())
    i = (y * lay["width"] + x) * 2
    struct.pack_into("<H", dados, i, palavra)
    open(caminho, "wb").write(dados)


# --------------------------------------------------------- escreve o mapa
def escreve_mapa(pasta, header, arq, dest_volta, warp_volta, grupos, incs,
                 sprites, movimentos, conta):
    """Igual ao `escreve` de fecha_portas_sinnoh: planta do arquetipo, conteudo
    do Platinum. Sem `extras`, porque nenhum destes mapas tem andar proprio."""
    base, entrada, _extras, funcional = F.ARQUETIPOS[arq]
    d = json.load(open(f"{REPO}/data/maps/{base}/map.json"))
    lay = F.layouts()[d["layout"]]
    objs, bg, trecho = F.conteudo_do_mapa(
        header, pasta, lay["width"], lay["height"], sprites, movimentos,
        d["layout"])
    if funcional:
        npc = dict(d["object_events"][0])
        npc.pop("local_id", None)
        npc["script"] = f"{pasta}_{F.ROTULO_FUNCIONAL[funcional]}"
        npc.update(F.MARCA_PLANTA)
        objs.insert(0, npc)
        trecho = F.FUNCIONAL[funcional](pasta) + trecho
    d["id"] = F.const_do_header(header)
    d["name"] = pasta
    d["object_events"] = objs
    d["bg_events"] = bg
    d["coord_events"] = []
    d["warp_events"] = [{"x": x, "y": y, "elevation": 0,
                         "dest_map": dest_volta, "dest_warp_id": str(warp_volta)}
                        for x, y in entrada]
    d["origem"] = ("pokeplatinum: NPC, placa e texto. "
                   "planta reaproveitada de " + base)
    os.makedirs(f"{REPO}/data/maps/{pasta}", exist_ok=True)
    json.dump(d, open(f"{REPO}/data/maps/{pasta}/map.json", "w"),
              indent=2, ensure_ascii=False)
    open(f"{REPO}/data/maps/{pasta}/scripts.inc", "w").write(
        f"{pasta}_MapScripts::\n\t.byte 0\n{trecho}")
    grupos[GRUPO].append(pasta)
    incs.append(f'\t.include "data/maps/{pasta}/scripts.inc"\n')
    conta["mapas"] += 1
    conta["npcs"] += len(objs)
    conta["placas"] += len(bg)
    conta["textos"] += trecho.count(".string")


# ------------------------------------------------------------------- main
def pendencias():
    """(pai, header, arquetipo) de tudo que ficou sem porta, na ordem da fonte."""
    heads = I.headers_do_platinum()
    por_chave = {}
    for h in heads:
        por_chave.setdefault(I.chave(h), h)
    casados = {}
    for m in I.nossos_mapas_sinnoh():
        h = I.APELIDOS.get(m) or por_chave.get(I.chave(m))
        if h in heads:
            casados[h] = m
    existentes = set(casados) | F.JA_TEMOS
    pastas = set(os.listdir(f"{REPO}/data/maps"))
    consts = set(re.findall(r'"id":\s*"(MAP_\w+)"', "".join(
        open(f"{REPO}/data/maps/{p}/map.json").read() for p in pastas
        if os.path.exists(f"{REPO}/data/maps/{p}/map.json"))))
    saida, vistos = [], set()
    for header, meu in sorted(casados.items(), key=lambda kv: kv[1]):
        pe = os.path.join(F.PLAT, "res/field/events", heads[header][0] + ".json")
        if not os.path.exists(pe):
            continue
        livres = len(F.portas_livres(meu))
        for w in json.load(open(pe)).get("warp_events", []):
            d = w["dest_header_id"]
            if d in existentes or d in vistos:
                continue
            a = F.arquetipo_do_header(d)
            if not a:
                continue
            pasta = F.nome_de_pasta(d)
            if pasta in pastas or F.const_do_header(d) in consts:
                continue
            if livres:            # esse o fecha_portas_sinnoh ja pega
                livres -= 1
                vistos.add(d)
                continue
            vistos.add(d)
            saida.append((meu, d, a))
    return saida


def main():
    if "--demo" in sys.argv:
        return demo()

    pend = pendencias()
    planos = []       # (pai, layout, (x,y), palavra, header, arquetipo)
    fora = []
    por_pai = {}
    for pai, header, arq in pend:
        por_pai.setdefault(pai, []).append((header, arq))

    for pai, itens in sorted(por_pai.items()):
        d, lay, _w, _h, pal, _c = _grade(pai)
        if lay["id"] in LAYOUTS_PC:
            # interior: escada espelhada, uma so, e so serve para o B1F
            alvo = ESCADA_PC
            escada = [e for e in d["warp_events"]
                      if (e["x"], e["y"]) not in
                      [t for t in F.ARQUETIPOS["pc1"][1]]]
            palavra = pal[escada[0]["y"] * lay["width"] + escada[0]["x"]] \
                if escada else None
            for header, arq in itens:
                if palavra is None or not header.endswith("POKECENTER_B1F"):
                    fora.append((pai, header, "escada indisponivel"))
                    continue
                planos.append((pai, lay["id"], alvo, palavra, header, arq))
            continue
        if d.get("map_type") not in (None, "MAP_TYPE_TOWN", "MAP_TYPE_CITY",
                                     "MAP_TYPE_ROUTE"):
            for header, arq in itens:
                fora.append((pai, header, f"{pai} nao e mapa de rua"))
            continue
        vagos = predios_sem_porta(pai)
        if not vagos:
            for header, arq in itens:
                fora.append((pai, header, f"{pai} nao tem predio sem porta"))
            continue
        # o predio do sul la vai para o predio do sul aqui: mesma regra de
        # posicao relativa de `fecha_portas_sinnoh.casa_portas`.
        for i, (header, arq) in enumerate(itens):
            if i >= len(vagos):
                fora.append((pai, header,
                             f"{pai} so tem {len(vagos)} predio(s) sem porta"))
                continue
            x, y, _a = vagos[i]
            planos.append((pai, lay["id"], (x, y), palavra_de_porta(pai, (x, y)),
                           header, arq))

    print(f"destinos sem porta: {len(pend)}")
    print(f"da para abrir agora: {len(planos)}")
    print(f"continuam de fora: {len(fora)}")
    for pai, header, motivo in fora:
        print(f"   {header.replace('MAP_HEADER_', '')}: {motivo}")
    if not APLICAR:
        print("\nnada escrito (use --aplicar)")
        for p in planos:
            print(f"   {p[0]} {p[2]} palavra {p[3]:#06x} -> "
                  f"{F.nome_de_pasta(p[4])} ({p[5]})")
        return 0

    sprites = V.sprites_utilizaveis()
    movimentos = V.constantes("include/constants/event_object_movement.h",
                              "MOVEMENT_TYPE_")
    grupos = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    grupos.setdefault(GRUPO, [])
    if GRUPO not in grupos["group_order"]:
        grupos["group_order"].append(GRUPO)
    incs = []
    conta = {"mapas": 0, "npcs": 0, "placas": 0, "textos": 0, "tiles": 0,
             "movidos": 0}
    ja_gravado = set()

    for pai, layout_id, (x, y), palavra, header, arq in planos:
        if (layout_id, x, y) not in ja_gravado:
            # o tile e do LAYOUT, entao ele muda em todo mapa que compartilha
            # ele: tem que ficar livre em todos, nao so no pai desta volta.
            for m in mapas_do_layout(layout_id):
                conta["movidos"] += libera_tile(m, x, y)
            grava_tile(layout_id, x, y, palavra)
            ja_gravado.add((layout_id, x, y))
            conta["tiles"] += 1
        p_pai = f"{REPO}/data/maps/{pai}/map.json"
        d_pai = json.load(open(p_pai))
        d_pai.setdefault("warp_events", [])
        idx = len(d_pai["warp_events"])
        d_pai["warp_events"].append({
            "x": x, "y": y, "elevation": 0,
            "dest_map": F.const_do_header(header), "dest_warp_id": "0"})
        json.dump(d_pai, open(p_pai, "w"), indent=2, ensure_ascii=False)
        escreve_mapa(F.nome_de_pasta(header), header, arq, d_pai["id"], idx,
                     grupos, incs, sprites, movimentos, conta)

    json.dump(grupos, open(f"{REPO}/data/maps/map_groups.json", "w"),
              indent=2, ensure_ascii=False)
    with open(f"{REPO}/data/event_scripts.s", "a") as f:
        f.writelines(incs)
    print(f"\naplicado: {conta['mapas']} mapas, {conta['tiles']} tiles de porta "
          f"desenhados, {conta['npcs']} NPCs, {conta['placas']} placas, "
          f"{conta['textos']} textos do Platinum, "
          f"{conta['movidos']} objetos empurrados de cima da porta")
    return 0


def demo():
    """As armadilhas que a primeira versao caiu."""
    # 1. o paredao que cerca a cidade encosta na borda e NAO pode virar porta;
    #    arvore 2x2 tem area 4 e tambem nao. Medido em CanalaveCity: 5 predios.
    v = predios_sem_porta("CanalaveCity")
    assert len(v) == 4, v
    assert all(a >= 6 for _x, _y, a in v), v
    # 2. porta nova nunca sai de metatile inventado: a palavra vem de uma porta
    #    que o proprio mapa ja tem, entao o comportamento dela ja e de warp.
    _d, _l, _w, _h, pal, comp = _grade("CanalaveCity")
    p = palavra_de_porta("CanalaveCity", (v[0][0], v[0][1]))
    assert comp(p) in W.COMPORTA_WARP, hex(p)
    # 3. o layout de centro Pokemon so pode ganhar escada porque os 15 mapas que
    #    o usam querem um B1F. Se um dia entrar um centro sem B1F, esta conta
    #    quebra e a escada tem que virar layout proprio.
    usos = [p for p in os.listdir(f"{REPO}/data/maps")
            if os.path.exists(f"{REPO}/data/maps/{p}/map.json")
            and json.load(open(f"{REPO}/data/maps/{p}/map.json")).get("layout")
            == "LAYOUT_OREBURGH_CITY_POKEMON_CENTER_1F"]
    assert len(usos) == 15, usos
    # 4. o tile da escada e do LAYOUT: quem estiver em cima dele em QUALQUER
    #    mapa que compartilha o layout tem que sair, senao a escada nasce com
    #    gente em cima. Medido: EternaCityPokecenter1F tinha NPC em (13,6).
    assert set(usos) == set(mapas_do_layout(
        "LAYOUT_OREBURGH_CITY_POKEMON_CENTER_1F"))
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
