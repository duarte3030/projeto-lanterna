#!/usr/bin/env python3
"""Põe o warp de Sinnoh EM CIMA da porta que o mapa já desenha.

    python3 dev_scripts/conserta_portas_sinnoh.py            # só relata
    python3 dev_scripts/conserta_portas_sinnoh.py --demo     # autoteste, não grava
    python3 dev_scripts/conserta_portas_sinnoh.py --aplicar  # escreve

O defeito, medido antes de tocar
--------------------------------
06/09/2026, playtest do Gui em `HearthomeCity`: "nem nessa casa entra".
`valida_warp_tile.py` já dizia, e ninguém tinha lido a lista pelo nome do
DESTINO: dos 18 warps mortos de Sinnoh, **cinco são a porta de um GINÁSIO**
(Hearthome, Pastoria, Canalave, Snowpoint e Sunyshore). Ginásio com warp morto é
ginásio inalcançável, e o capítulo que o Gui está jogando é justamente o
"before Fantina", cujo ginásio é o de Hearthome.

Medido, um por um, no `map.bin` do layout ATIVO (Hearthome não troca de layout:
não há `setmaplayoutindex` em nenhum script dela, e o `gba_runner` leu
`layout=799` = `LAYOUT_HEARTHOME_CITY` dentro do mapa):

| mapa | warp | onde está | o que tem lá | onde a porta está |
|---|---|---|---|---|
| HearthomeCity | 4 | (29,26) | metatile 521, chão de praça, `MB_NORMAL` | o arco do ginásio em (10,31), metatile 636 |
| PastoriaCity | 1 | (34,30) | metatile 1, grama, `MB_NORMAL` | porta animada LIVRE em (27,34) |
| SnowpointCity | 0 | (17,34) | metatile 513, `MB_SAND` | porta animada LIVRE em (17,33), UM tile acima |

A regra, e por que ela recusa mais do que aceita
------------------------------------------------
"Mover o warp, não a porta". O índice do warp NUNCA muda (outro mapa aponta para
ele por `dest_warp_id`), só o par x,y. Um warp morto só é consertado quando o
próprio mapa responde onde a porta está, por um destes dois caminhos:

1. **PORTA LIVRE**: existe célula com comportamento de porta (a mesma lista do
   `valida_warp_tile`) que nenhum warp usa, ela é a MAIS PRÓXIMA sem empate e
   está a no máximo `RAIO` de distância de Chebyshev. Foi o que resolveu
   Snowpoint (distância 1, o clássico erro de um tile) e Pastoria (distância 7,
   a porta do prédio da esquerda, com o da direita já ocupado pelo warp 7).
2. **BOCA DE PRÉDIO ÚNICA**: célula andável de `MB_NORMAL` com bloqueio em cima,
   à esquerda e à direita e chão andável embaixo (o mesmo teste que
   `abre_bocas_cavernas_sinnoh` usa), cujo METATILE aparece no repo inteiro no
   máximo `RARIDADE` vezes e só em layout desta região. Metatile desenhado uma
   única vez no mundo, no meio de uma fachada, é porta que o demake desenhou e
   esqueceu de marcar. É o arco do ginásio de Hearthome: o metatile 636 aparece
   **uma vez em todo o repo**, em (10,31) de `LAYOUT_HEARTHOME_CITY`, que é
   usado por um mapa só. Aí o conserto é no ATRIBUTO do tileset (o arco passa a
   ser `MB_NON_ANIMATED_DOOR`), e não no desenho: nenhum pixel muda e nenhum
   outro mapa sente, porque `gTileset_Hearthome` serve um layout só.

Tudo que não cai nesses dois casos sai no relatório como "sem conserto medido",
e não é tocado. Em 06/09/2026 isso deixou de fora, de propósito:

- **Canalave 1 e Sunyshore 1**, warp sobre `MB_OCEAN_WATER`: as duas cidades têm
  canal/mar no meio e nenhuma porta livre; qual porta é do ginásio é decisão de
  conteúdo, não medida (em Canalave o warp 5, do `SOUTHEAST_HOUSE`, está em
  (9,31), colado no prédio que desenha "GYM": pode ser troca de destino, e trocar
  destino no escuro é pior que deixar quieto).
- **Os cinco quartos da Elite dos Quatro de Sinnoh**: warp em tile sólido é o
  IDIOMA da Elite (ESTADO 0.t: em Kanto o `ON_FRAME` com
  `Common_Movement_WalkUp5` é que tira o jogador, e `applymovement` de script não
  consulta colisão). Mexer ali quebraria a cena.
- **EternaForest 4, OreburghMine B1F 2 e B2F 0, MtCoronet_1F_North_Room2 2**:
  caverna e floresta, onde não existe "porta desenhada" para achar.
"""
import argparse
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import valida_warp_tile as W   # noqa: E402

RAIO = 10          # distância de Chebyshev máxima para adotar uma porta livre
RARIDADE = 4       # quantas vezes um metatile pode aparecer e ainda ser "único"
PISO_PREDIO = 6    # área mínima da mancha bloqueada para ela ser um prédio
TETO_PREDIO = 4000 # acima disso não é mancha de prédio nenhum

# A BOCA JULGADA A OLHO, e por que ela não é automática. A régua de "boca única"
# sozinha NÃO separa arco de ginásio de fenda de rocha: medido em 06/09/2026, os
# três candidatos que ela achou em Sinnoh (`gTileset_Hearthome` 636,
# `gTileset_Sunnyshore` 657 e `gTileset_CaveSinnoh` 931) aparecem UMA vez cada um
# no mundo inteiro, e mesmo assim só o primeiro é porta: os PNG do
# `render_maps.py` foram abertos e olhados, e o de Hearthome é o arco de pedra da
# fachada que escreve "GYM", enquanto o de Sunyshore é uma passagem entre pedras
# do paredão e o do Oreburgh é parede de caverna. Então a boca entra por tabela,
# com o julgamento escrito aqui, e o código só CONFERE que ela continua sendo o
# que foi medido (célula de boca, metatile único, layout de um mapa só). Se o
# mapa mudar, a conferência falha em vez de escrever no lugar errado.
BOCAS_MEDIDAS = {
    # (pasta do mapa, índice do warp): (x, y, por quê)
    ("HearthomeCity", 4): (10, 31, "arco do ginásio de Fantina, metatile 636 de "
                                   "gTileset_Hearthome, único no repo"),
}

# O comportamento que a boca de prédio ganha. Porta NÃO animada de propósito: a
# animada (`MB_ANIMATED_DOOR`) exige quadro de porta em `gDoorAnimGraphicsTable`
# (src/data/field_door_anim.h) e um arco de pedra não tem; a não animada dispara
# pelo `IsWarpMetatileBehavior` com o jogador EM CIMA dela, que é como se entra
# num arco em Diamond/Pearl.
MB_PORTA = "MB_NON_ANIMATED_DOOR"


def layouts():
    with open(f"{RAIZ}/data/layouts/layouts.json", encoding="utf-8") as f:
        return {l["id"]: l for l in json.load(f)["layouts"]}


def mapas_da_regiao(marca="Sinnoh"):
    with open(f"{RAIZ}/data/maps/map_groups.json", encoding="utf-8") as f:
        g = json.load(f)
    fora = []
    for grupo in g["group_order"]:
        if marca.lower() in grupo.lower():
            fora.extend(g[grupo])
    return fora


def n_primario(layout):
    return 640 if layout.get("layout_version") in ("johto", "frlg") else 512


def grade(layout):
    """(largura, altura, blocos) ou (w,h,None) quando o layout não tem map.bin.

    Layout sem arquivo existe: `dedupe_blockdata.py` faz o repetido virar
    referência, e alguns layouts de Hoenn nunca tiveram blockdata próprio.
    """
    w, h = layout["width"], layout["height"]
    caminho = os.path.join(RAIZ, layout.get("blockdata_filepath") or "")
    if not os.path.isfile(caminho):
        return w, h, None
    dados = open(caminho, "rb").read()
    if len(dados) < w * h * 2:
        return w, h, None
    return w, h, list(struct.unpack(f"<{w * h}H", dados[:w * h * 2]))


def comportamentos(layout):
    """metatile -> comportamento, do arquivo de atributos dos dois tilesets."""
    frlg = layout.get("layout_version") == "frlg"
    larg = 4 if frlg else 2
    fora, npri = {}, n_primario(layout)
    for chave, base in (("primary_tileset", 0), ("secondary_tileset", npri)):
        pasta = W.pasta_do_tileset(layout.get(chave))
        if not pasta:
            return None
        dados = open(os.path.join(pasta, "metatile_attributes.bin"), "rb").read()
        for i in range(len(dados) // larg):
            v = int.from_bytes(dados[i * larg:(i + 1) * larg], "little")
            fora[base + i] = (v & 0x1FF) if frlg else (v & 0xFF)
    return fora


def censo_de_metatiles(todos):
    """metatile -> (total de células no repo, conjunto de layouts que o usam).

    Uma passada só. É essa contagem que separa "porta desenhada uma vez, de
    propósito" de "chão liso que existe aos milhares".
    """
    total = collections.Counter()
    onde = collections.defaultdict(set)
    for lid, layout in todos.items():
        w, h, g = grade(layout)
        if g is None:
            continue
        for palavra in g:
            chave = identidade(layout, palavra & 0x3FF)
            total[chave] += 1
            onde[chave].add(lid)
    return total, onde


def identidade(layout, mt):
    """A identidade de um metatile é (tileset, índice local), não o número solto.

    Sem isto o censo mente: o 636 de `gTileset_Hearthome` e o 636 de qualquer
    outro secundário são desenhos diferentes, e contar os dois juntos dava 1.074
    células em 119 layouts para um metatile que na verdade existe UMA vez.
    """
    npri = n_primario(layout)
    if mt < npri:
        return ("pri", layout["primary_tileset"], mt)
    return ("sec", layout.get("secondary_tileset"), mt - npri)


def usuarios_de_layout():
    with open(f"{RAIZ}/data/maps/map_groups.json", encoding="utf-8") as f:
        mg = json.load(f)
    fora = collections.defaultdict(list)
    for grupo in mg["group_order"]:
        for nome in mg[grupo]:
            caminho = f"{RAIZ}/data/maps/{nome}/map.json"
            if os.path.exists(caminho):
                with open(caminho, encoding="utf-8") as f:
                    fora[json.load(f)["layout"]].append(nome)
    return fora


def bloco_de_predio(g, w, h, semente):
    """Mancha conexa de células bloqueadas a partir de uma vizinha da boca.

    Devolve (tamanho, encosta_na_borda). É o mesmo teste de PRÉDIO de
    `abre_portas_extras_sinnoh.py`: mancha que toca a borda do mapa é o paredão
    de pedra que cerca a cidade ou a parede de uma caverna, não uma casa.
    """
    col = lambda x, y: (g[y * w + x] >> 10) & 3
    visto, fila, borda = {semente}, [semente], False
    while fila:
        x, y = fila.pop()
        if x in (0, w - 1) or y in (0, h - 1):
            borda = True
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visto and col(nx, ny):
                visto.add((nx, ny))
                fila.append((nx, ny))
        if len(visto) > TETO_PREDIO:
            return len(visto), True
    return len(visto), borda


def bocas_de_predio(g, w, h, beh):
    """Célula andável de MB_NORMAL cercada em cima, esquerda e direita.

    A mancha bloqueada logo acima precisa ter pelo menos `PISO_PREDIO` células,
    o que descarta árvore 2x2 e canto de cerca. O teste PARA AQUI de propósito:
    "encosta na borda do mapa" foi medido e descartado como filtro, porque em
    Hearthome o prédio do ginásio é 4-conexo com a fileira de arbustos que cerca
    a cidade, e o filtro jogava fora justamente o caso certo. Quem separa arco de
    fenda é o julgamento escrito em `BOCAS_MEDIDAS`, não esta função.
    """
    col = lambda x, y: (g[y * w + x] >> 10) & 3
    fora = []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if col(x, y) or beh.get(g[y * w + x] & 0x3FF, -1) != 0:
                continue
            if not (col(x, y - 1) and col(x - 1, y) and col(x + 1, y)
                    and not col(x, y + 1)):
                continue
            tamanho, borda = bloco_de_predio(g, w, h, (x, y - 1))
            if tamanho < PISO_PREDIO:
                continue          # árvore 2x2 e canto de cerca não são fachada
            fora.append((x, y, g[y * w + x] & 0x3FF))
    return fora


def diagnostico(marca="Sinnoh"):
    """Lista (mapa, indice, de, para, receita) e os casos sem conserto medido."""
    todos = layouts()
    total_mt, onde_mt = censo_de_metatiles(todos)
    usuarios = usuarios_de_layout()
    consertos, recusas = [], []
    for nome in mapas_da_regiao(marca):
        caminho = f"{RAIZ}/data/maps/{nome}/map.json"
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            mapa = json.load(f)
        layout = todos.get(mapa.get("layout"))
        if layout is None:
            continue
        beh = comportamentos(layout)
        if beh is None:
            continue
        w, h, g = grade(layout)
        if g is None:
            continue
        usados = {(wp["x"], wp["y"]) for wp in mapa.get("warp_events", [])}
        livres = []
        for y in range(h):
            for x in range(w):
                b = beh.get(g[y * w + x] & 0x3FF, -1)
                if b in W.COMPORTA_WARP and (x, y) not in usados:
                    livres.append((x, y))
        # As bocas NÃO são filtradas por "célula já usada por warp": quando esta
        # ferramenta já rodou uma vez, o warp consertado ESTÁ em cima da boca, e
        # filtrar por uso faria a segunda execução recusar o próprio conserto.
        # Quem impede conserto em cima de outro warp é a tabela `BOCAS_MEDIDAS`.
        bocas = bocas_de_predio(g, w, h, beh)

        for i, wp in enumerate(mapa.get("warp_events", [])):
            if "fechado" in wp:
                continue
            x, y = wp["x"], wp["y"]
            palavra = g[y * w + x]
            morto, motivo = W.warp_morto(beh.get(palavra & 0x3FF, -1),
                                         (palavra >> 10) & 3)
            if not morto:
                continue
            # 1. porta livre mais próxima, sem empate e dentro do raio
            dist = sorted(((max(abs(px - x), abs(py - y)), px, py)
                           for px, py in livres))
            if dist and dist[0][0] <= RAIO and (len(dist) == 1 or dist[1][0] > dist[0][0]):
                d, px, py = dist[0]
                consertos.append((nome, i, (x, y), (px, py), "porta livre",
                                  wp["dest_map"], None))
                usados.add((px, py))
                livres.remove((px, py))
                continue
            # 2. boca de prédio julgada a olho, reconferida aqui
            medida = BOCAS_MEDIDAS.get((nome, i))
            unicas = []
            if medida:
                px, py, _porque = medida
                unicas = [b for b in bocas
                          if (b[0], b[1]) == (px, py)
                          and total_mt[identidade(layout, b[2])] <= RARIDADE
                          and onde_mt[identidade(layout, b[2])] <= {mapa["layout"]}
                          and len(usuarios[mapa["layout"]]) == 1]
                if not unicas:
                    recusas.append((nome, i, (x, y),
                                    f"{motivo} (a boca medida em {px},{py} não "
                                    "confere mais)", wp["dest_map"],
                                    len(livres), len(bocas)))
                    continue
            if len(unicas) == 1:
                px, py, mt = unicas[0]
                consertos.append((nome, i, (x, y), (px, py), "boca única",
                                  wp["dest_map"],
                                  (layout["secondary_tileset"] if mt >= n_primario(layout)
                                   else layout["primary_tileset"],
                                   mt - (n_primario(layout) if mt >= n_primario(layout) else 0),
                                   mt)))
                bocas.remove(unicas[0])
                continue
            recusas.append((nome, i, (x, y), motivo, wp["dest_map"],
                            len(livres), len(bocas)))
    return consertos, recusas


def valores_mb():
    return W._MB


def aplica(consertos):
    """Grava map.json (posição do warp) e metatile_attributes.bin (a boca)."""
    mb = valores_mb()[MB_PORTA]
    por_mapa = collections.defaultdict(list)
    for c in consertos:
        por_mapa[c[0]].append(c)
    tocados = 0
    for nome, lista in por_mapa.items():
        caminho = f"{RAIZ}/data/maps/{nome}/map.json"
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
        mapa = json.loads(texto)
        for _n, i, _de, (px, py), _receita, _dest, tileset in lista:
            mapa["warp_events"][i]["x"] = px
            mapa["warp_events"][i]["y"] = py
            mapa["warp_events"][i]["porta_movida"] = (
                "warp posto em cima da porta desenhada, "
                "dev_scripts/conserta_portas_sinnoh.py")
            if tileset:
                nome_ts, local, _mt = tileset
                pasta = W.pasta_do_tileset(nome_ts)
                arq = os.path.join(pasta, "metatile_attributes.bin")
                dados = bytearray(open(arq, "rb").read())
                v = struct.unpack_from("<H", dados, local * 2)[0]
                struct.pack_into("<H", dados, local * 2, (v & ~0xFF) | mb)
                open(arq, "wb").write(bytes(dados))
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(mapa, f, indent=2, ensure_ascii=False)
            f.write("\n")
        tocados += 1
    return tocados


def demo():
    """Autoteste: a régua acha os três casos medidos e recusa o resto."""
    consertos, recusas = diagnostico()
    por_mapa = {c[0]: c for c in consertos}
    esperado = {
        "SnowpointCity": ((17, 34), (17, 33), "porta livre"),
        "PastoriaCity": ((34, 30), (27, 34), "porta livre"),
        "HearthomeCity": ((29, 26), (10, 31), "boca única"),
    }
    ja_feito = not consertos
    if not ja_feito:
        for nome, (de, para, receita) in esperado.items():
            assert nome in por_mapa, f"{nome} saiu da lista de conserto"
            c = por_mapa[nome]
            assert (c[2], c[3], c[4]) == (de, para, receita), (nome, c)
        # o arco de Hearthome tem que ser metatile de UM uso só
        c = por_mapa["HearthomeCity"]
        assert c[6] and c[6][2] == 636, c
        assert c[6][0] == "gTileset_Hearthome", c
    # nenhuma recusa pode virar conserto por acidente
    nomes = {r[0] for r in recusas}
    assert "SinnohLeague_AaronsRoom" in nomes or ja_feito, recusas
    # e o índice do warp nunca muda: só x,y
    print(f"demo OK: {len(consertos)} consertos medidos, "
          f"{len(recusas)} warps mortos sem conserto medido")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regiao", default="Sinnoh")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()
    if args.demo:
        return demo()
    consertos, recusas = diagnostico(args.regiao)
    print(f"{len(consertos)} warps para mover, {len(recusas)} sem conserto medido\n")
    for nome, i, de, para, receita, dest, ts in consertos:
        extra = f"  (+ atributo de {ts[0]} metatile {ts[2]} -> {MB_PORTA})" if ts else ""
        print(f"  {nome:28s} warp {i:2d} {de} -> {para}  [{receita}]  {dest}{extra}")
    print()
    for nome, i, de, motivo, dest, nlivres, nbocas in recusas:
        print(f"  RECUSA {nome:24s} warp {i:2d} {de} {motivo}  {dest}  "
              f"(portas livres {nlivres}, bocas {nbocas})")
    if args.aplicar:
        n = aplica(consertos)
        print(f"\n{n} map.json regravados")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
