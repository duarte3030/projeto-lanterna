#!/usr/bin/env python3
"""Traz o PORTO de Slateport para o tileset de Canalave, e amarra os barcos no canal.

O Gui, no playtest de 06/09/2026, sobre `CanalaveCity`: "a cidade esta muito
feia, e assim mesmo?". Ela e, no Diamante/Perola, a cidade PORTUARIA de Sinnoh, e
o demake trouxe a geometria (o canal, as duas margens, as duas pontes) sem uma
peca sequer de porto: o `gTileset_Canalave` inteiro e calcada, telhado e agua.
Conferido metatile a metatile no atlas: nenhum barco, nenhum poste, nenhum
tambor, nenhum engradado. O `enfeita_cidades.py` nao resolve isso porque ele so
copia o que ja existe, e Canalave e o UNICO layout que usa o
`gTileset_Canalave`: nao ha mapa irmao de quem aprender.

Quem tem porto desenhado nesta ROM e HOENN: `gTileset_Slateport` guarda o bote,
o poste de luz da orla e os tambores do cais. Este script IMPORTA essas pecas
para dentro do `gTileset_Canalave` e monta metatiles novos, sem desenhar um
pixel: os tiles sao copiados byte a byte e as paletas sao copiadas inteiras.

COMO O METATILE NOVO E MONTADO, e por que ele nao pode sair torto. Metatile do
Emerald tem duas camadas de quatro tiles. Nos objetos que interessam aqui a
camada de BAIXO e o CHAO de Slateport (grama, ou a calcada branca de la) e a de
CIMA e o objeto, com fundo transparente. Entao:

  - a camada de CIMA vem inteira da fonte, so trocando o indice do tile (para a
    vaga nova dentro do Canalave) e o numero da PALETA (para a vaga nova);
  - a camada de BAIXO e SUBSTITUIDA pela do chao de Canalave: a calcada
    (metatile 521) nos objetos de terra, e a AGUA do `gTileset_GeneralSinnoh`
    (metatile 368) nos barcos. Como a agua e desenhada pelos tiles do PRIMARIO,
    e o primario tem animacao propria, o barco flutua em agua que se mexe de
    graca;
  - o COMPORTAMENTO do metatile novo e o do CHAO que entrou embaixo (0 na
    calcada, o de agua no canal), nao o da fonte. Assim nada muda de regra: a
    celula do canal continua sendo agua para o motor, so que agora com colisao.

ORCAMENTO, medido antes de escrever (nao ha "provavelmente cabe" aqui):

  - TILES: `gTileset_Canalave` usa 384 dos 512 tiles do teto de um secundario.
    O kit precisa de 33, e sobram 95. O `tiles.png` cresce de 128x192 para
    128x256, que e o tamanho maximo.
  - PALETAS: os metatiles do Canalave usam as vagas 0 a 8 (as 0 a 5 sao do
    primario). As vagas 9 a 12 estao LIVRES, e e para la que vao as paletas 7, 8
    e 9 de Slateport.
  - METATILES: o `metatiles.bin` ja tem os 512 do teto, e do local 153 (id
    global 665) em diante esta tudo em branco. O kit ocupa os locais 160 a 174,
    e o script RECUSA gravar se alguma dessas vagas estiver em uso no `map.bin`
    de Canalave.

ONDE CADA PECA ENCOSTA. Barco so em AGUA, encostado no muro do canal, e nunca
tapando o canal inteiro: o canal tem 6 celulas de largura e o barco tem 3, entao
sempre sobram 3 para quem surfa. Poste e tambor so em CALCADA de beira, colada
no muro do canal ou num predio. Os dois portoes de alcance rodam a cada peca:
o de PE (busca em largura pelos warps, respeitando elevacao) e o de AGUA (busca
em largura pela agua do canal), e os dois exigem
`depois == antes - celulas_ocupadas`.

Idempotente: as vagas de tile, de paleta e de metatile sao fixas, e o plano do
`map.bin` guarda o valor antigo de cada celula em
`dev_scripts/porto_canalave.json`, como o `enfeita_cidades.py` faz. Rodar duas
vezes da byte identico.

ORDEM: este script roda ANTES do `enfeita_cidades.py`. Ele cria metatiles que
nao estao no "chao liso", entao o outro nunca os escolhe, e o inverso nao vale.

Uso:
    python3 dev_scripts/porto_canalave.py             # mede e mostra o plano
    python3 dev_scripts/porto_canalave.py --aplicar   # escreve tileset e mapa
    python3 dev_scripts/porto_canalave.py --desfazer  # devolve o map.bin
    python3 dev_scripts/porto_canalave.py --demo      # auto-teste
"""
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

ALVO = "CanalaveCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/canalave"
FONTE = f"{RAIZ}/data/tilesets/secondary/slateport"
PLANO = f"{RAIZ}/dev_scripts/porto_canalave.json"
PLANO_ENFEITE = f"{RAIZ}/dev_scripts/enfeita_cidades.json"

TILE_LOCAL_0 = 384      # primeira vaga de tile livre no Canalave
META_LOCAL_0 = 160      # primeira vaga de metatile que o kit ocupa (id global 672)
PAL_NOVAS = {7: 9, 8: 10, 9: 11}   # paleta de Slateport -> vaga no Canalave
TETO_TILES = 512
TETO_META = 512
MARGEM = 3      # celulas de folga em relacao a borda do mapa

CHAO_CALCADA = 521      # metatile de calcada de Canalave (id global)
CHAO_AGUA = 368         # metatile de agua do GeneralSinnoh (id global, primario)

# O kit. Cada peca e um retangulo de metatiles de Slateport (ids globais do par
# General+Slateport) mais o chao que entra embaixo. Escolhidos olhando a folha de
# contato do tileset, e conferidos no mapa de origem: o bote esta em
# SlateportCity (21,35), o poste em (10,43) e os tambores em (7,45) e (11,44).
KIT = [
    dict(nome="bote atracado", chao="agua", col=1,
         fonte=[[544, 545, 546], [552, 553, 554]]),
    dict(nome="bote de proa ao contrario", chao="agua", col=1,
         fonte=[[613, 614, 615], [621, 622, 623]]),
    dict(nome="poste de luz do cais", chao="calcada", col=1, fonte=[[619]]),
    dict(nome="tambor vermelho", chao="calcada", col=1, fonte=[[547]]),
    dict(nome="tambor laranja", chao="calcada", col=1, fonte=[[555]]),
]

QUANTOS = {"bote atracado": 3, "bote de proa ao contrario": 3,
           "poste de luz do cais": 10, "tambor vermelho": 5,
           "tambor laranja": 4}
ESPACO = {"bote atracado": 8, "bote de proa ao contrario": 8,
          "poste de luz do cais": 5, "tambor vermelho": 6, "tambor laranja": 6}

N4 = E.N4


# --------------------------------------------------------------------- leitura
def _tiles_png(caminho):
    from PIL import Image
    img = Image.open(caminho)
    if img.mode != "P":
        raise SystemExit(f"{caminho} nao e PNG indexado")
    W, H = img.size
    px = img.load()
    cols = W // 8
    tiles = [[[px[(i % cols) * 8 + x, (i // cols) * 8 + y] for x in range(8)]
              for y in range(8)]
             for i in range((W // 8) * (H // 8))]
    return tiles, img.getpalette(), cols


def _entradas(bin_meta, local):
    return [struct.unpack_from("<H", bin_meta, local * 16 + i * 2)[0] for i in range(8)]


def _monta(valor, tile, pal):
    return (valor & 0x0C00) | (tile & 0x3FF) | ((pal & 0xF) << 12)


# ----------------------------------------------------------------- importacao
def desenha_kit():
    """(tiles_novos, metatiles_novos, atributos, carimbos) sem escrever nada.

    `tiles_novos` e {vaga_local_no_canalave: tile 8x8}; `metatiles_novos` e
    {vaga_local: [8 entradas]}; `carimbos` e o que o passo do mapa carimba.
    """
    meta_fonte = open(f"{FONTE}/metatiles.bin", "rb").read()
    attr_fonte = open(f"{FONTE}/metatile_attributes.bin", "rb").read()
    meta_can = open(f"{DESTINO}/metatiles.bin", "rb").read()
    meta_pri = open(f"{RAIZ}/data/tilesets/primary/general_sinnoh/metatiles.bin", "rb").read()
    attr_pri = open(f"{RAIZ}/data/tilesets/primary/general_sinnoh/metatile_attributes.bin",
                    "rb").read()
    tiles_fonte, _pal, _c = _tiles_png(f"{FONTE}/tiles.png")

    chao = {
        "calcada": (_entradas(meta_can, CHAO_CALCADA - 512)[:4],
                    struct.unpack_from("<H", open(f"{DESTINO}/metatile_attributes.bin", "rb").read(),
                                       (CHAO_CALCADA - 512) * 2)[0]),
        "agua": (_entradas(meta_pri, CHAO_AGUA)[:4],
                 struct.unpack_from("<H", attr_pri, CHAO_AGUA * 2)[0]),
    }

    tiles_novos, mapa_tile = {}, {}
    metas, attrs, carimbos = {}, {}, []
    proximo_tile = TILE_LOCAL_0
    proximo_meta = META_LOCAL_0

    for peca in KIT:
        base_baixo, attr_chao = chao[peca["chao"]]
        linhas = []
        for linha in peca["fonte"]:
            saida = []
            for mt in linha:
                ent = _entradas(meta_fonte, mt - 512)
                attr_src = struct.unpack_from("<H", attr_fonte, (mt - 512) * 2)[0]
                cima = []
                for valor in ent[4:]:
                    idx, pal = valor & 0x3FF, (valor >> 12) & 0xF
                    if idx == 0 and pal == 0:
                        cima.append(0)
                        continue
                    if idx < 512:
                        raise SystemExit(
                            "%s: o metatile %d usa tile do PRIMARIO de Hoenn (%d), "
                            "que nao existe em Sinnoh" % (peca["nome"], mt, idx))
                    if pal not in PAL_NOVAS:
                        raise SystemExit("%s: paleta %d de Slateport sem vaga"
                                         % (peca["nome"], pal))
                    if idx not in mapa_tile:
                        mapa_tile[idx] = proximo_tile
                        tiles_novos[proximo_tile] = tiles_fonte[idx - 512]
                        proximo_tile += 1
                    cima.append(_monta(valor, 512 + mapa_tile[idx], PAL_NOVAS[pal]))
                metas[proximo_meta] = list(base_baixo) + cima
                # comportamento do CHAO, camada da FONTE: a celula continua com a
                # regra do chao que entrou embaixo, e o desenho fica igual ao de
                # Slateport.
                # As mascaras sao as do EMERALD, lidas de `include/global.fieldmap.h`
                # e nao decoradas: comportamento e 0x00FF (bits 0-7) e tipo de
                # camada e 0xF000 (bits 12-15). O `& 0x1FF` que o
                # `arte_ginasios_sinnoh.comportamento` usa da o mesmo numero
                # nestes tilesets, mas aqui a conta ESCREVE atributo, e escrever
                # com mascara larga sujaria o bit 8.
                attrs[proximo_meta] = (attr_src & 0xF000) | (attr_chao & 0x00FF)
                saida.append(512 + proximo_meta)
                proximo_meta += 1
            linhas.append(saida)
        carimbos.append(dict(nome=peca["nome"], chao=peca["chao"], col=peca["col"],
                             ids=linhas, w=len(linhas[0]), h=len(linhas)))

    if proximo_tile > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)" % (TETO_TILES, proximo_tile))
    if proximo_meta > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)
    # vaga de metatile tem que estar em BRANCO e fora de uso no mapa
    # A vaga so pode ser usada se ela e ENCHIMENTO ou se ja tem exatamente o
    # que este kit escreve (caso de rodar duas vezes).
    #
    # "Em branco" nao serve como teste: as vagas livres do `metatiles.bin` de
    # Canalave nao sao zero, sao o padrao de enchimento que o dumper deixou
    # (as oito entradas iguais a 1, ou as oito iguais a 2, que e o tile 1 ou 2
    # na paleta 0 repetido). Medido no HEAD: local 160 = [1]*8, local 161 =
    # [2]*8. O que importa de verdade e o mapa nao usar o id.
    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    usados = {c & 0x3FF for c in G.grade(ALVO)[4]}
    for local, entradas in metas.items():
        gid = 512 + local
        antigo = _entradas(meta_can, local)
        if not enchimento(antigo) and antigo != entradas:
            raise SystemExit("vaga de metatile %d ja esta ocupada por outra coisa" % gid)
        if gid in usados and enchimento(antigo):
            raise SystemExit("o mapa usa o metatile %d e a vaga esta vazia" % gid)
    return tiles_novos, metas, attrs, carimbos


def grava_tileset(tiles_novos, metas, attrs):
    from PIL import Image
    # 1. tiles.png cresce para 512 tiles (128x256), guardando os 384 que ja tem
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    novo = Image.new("P", (antigo.size[0], (TETO_TILES // cols) * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    px = novo.load()
    for vaga, tile in tiles_novos.items():
        x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    novo.save(f"{DESTINO}/tiles.png")

    # 2. paletas: copia inteiras para as vagas livres
    for de, para in sorted(PAL_NOVAS.items()):
        with open(f"{FONTE}/palettes/%02d.pal" % de) as f:
            texto = f.read()
        with open(f"{DESTINO}/palettes/%02d.pal" % para, "w") as f:
            f.write(texto)

    # 3. metatiles e atributos, nas vagas fixas
    meta = bytearray(open(f"{DESTINO}/metatiles.bin", "rb").read())
    attr = bytearray(open(f"{DESTINO}/metatile_attributes.bin", "rb").read())
    for local, entradas in metas.items():
        for i, valor in enumerate(entradas):
            struct.pack_into("<H", meta, local * 16 + i * 2, valor)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ---------------------------------------------------------------- passo do mapa
def agua_alcance(v, W, H, AG, beh):
    """Componente de agua ligada as bordas do mapa e as pontes: quem surfa chega."""
    molhada = [i for i in range(W * H)
               if not ((v[i] >> 10) & 3) and beh(v[i] & 0x3FF) in AG]
    ini = [i for i in molhada
           if i % W in (0, W - 1) or i // W in (0, H - 1)
           or any(0 <= (i % W) + dx < W and 0 <= (i // W) + dy < H
                  and not ((v[(i // W + dy) * W + (i % W) + dx] >> 10) & 3)
                  and beh(v[(i // W + dy) * W + (i % W) + dx] & 0x3FF) not in AG
                  for dx, dy in N4)]
    vis, fila = set(ini), collections.deque(ini)
    molhada = set(molhada)
    while fila:
        i = fila.popleft()
        x, y = i % W, i // W
        for dx, dy in N4:
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H:
                j = ny * W + nx
                if j in molhada and j not in vis:
                    vis.add(j)
                    fila.append(j)
    return vis


def plano_mapa(carimbos, base=None):
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG, BANAL = E.agua(), E.chao_banal()
    ev, gelo = E.congelado(d)
    # Corredor de teste: perna saturante de caso da suite nao pode ganhar
    # obstaculo novo. Em 06/09/2026 o poste de (19,39) derrubou os SETE casos de
    # balsa que descem a coluna 19 de Canalave inteira.
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    aplicado = list(v)
    escritas, ocupadas = {}, []

    ini_pe = E.partidas(d, W, H, v)
    pe_antes = E.alcance(v, W, H, ini_pe)
    agua_antes = agua_alcance(v, W, H, AG, beh)

    freq = collections.Counter(
        v[i] & 0x3FF for i in range(W * H)
        if not ((v[i] >> 10) & 3) and beh(v[i] & 0x3FF) not in AG)
    n_and = sum(freq.values())
    chao = freq.most_common(1)[0][0]
    elev_chao = collections.Counter((c >> 12) & 0xF for c in v
                                    if (c & 0x3FF) == chao).most_common(1)[0][0]
    liso = {mt for mt, n in freq.items() if n >= max(8, E.FRACAO_LISO * n_and)}

    postos = collections.defaultdict(list)

    def cabe(car, x, y):
        # MARGEM: peca colada na borda do mapa aparece cortada pela metade na
        # tela e, no caso do bote, fica boiando na parte do canal que o jogador
        # nunca ve de perto. Medido na primeira passada: tres botes nasceram na
        # linha 0.
        if x < MARGEM or y < MARGEM:
            return False
        if x + car["w"] > W - MARGEM or y + car["h"] > H - MARGEM:
            return False
        if any(max(abs(x - px), abs(y - py)) < ESPACO[car["nome"]]
               for px, py in postos[car["nome"]]) or \
           any(max(abs(x - px), abs(y - py)) < 3
               for nome in postos for px, py in postos[nome]):
            return False
        pes = [(x + dx, y + dy) for dy in range(car["h"]) for dx in range(car["w"])]
        encosta = False
        for cx, cy in pes:
            i = cy * W + cx
            if (cx, cy) in gelo or ((aplicado[i] >> 10) & 3):
                return False
            mt, b = aplicado[i] & 0x3FF, beh(aplicado[i] & 0x3FF)
            if car["chao"] == "agua":
                if b not in AG:
                    return False
            else:
                if mt not in liso or b not in BANAL:
                    return False
                if ((aplicado[i] >> 12) & 0xF) != elev_chao:
                    return False
            for dx, dy in N4:
                nx, ny = cx + dx, cy + dy
                # so encosta em SOLIDO de verdade: a borda do mapa nao conta,
                # senao o bote atraca no nada.
                if 0 <= nx < W and 0 <= ny < H and (nx, ny) not in pes \
                   and ((aplicado[ny * W + nx] >> 10) & 3):
                    encosta = True
        return encosta

    ordem = sorted(((x, y) for y in range(H) for x in range(W)),
                   key=lambda p: ((p[1] * 2654435761 + p[0] * 40503) & 0xFFFF, p))
    for x, y in ordem:
        for car in carimbos:
            if len(postos[car["nome"]]) >= QUANTOS[car["nome"]]:
                continue
            if not cabe(car, x, y):
                continue
            posto = []
            for dy in range(car["h"]):
                for dx in range(car["w"]):
                    j = (y + dy) * W + x + dx
                    posto.append((j, aplicado[j],
                                  (car["col"] << 10) | car["ids"][dy][dx],
                                  (x + dx, y + dy)))
            for j, _velho, novo, _c in posto:
                aplicado[j] = novo
            marcadas = ocupadas + [c for _, _, _, c in posto]
            idx_marcadas = {c[1] * W + c[0] for c in marcadas}
            ruim = (pe_antes - E.alcance(aplicado, W, H, ini_pe)) - set(marcadas)
            ruim2 = (agua_antes - agua_alcance(aplicado, W, H, AG, beh)) - idx_marcadas
            if ruim or ruim2:
                for j, velho, _novo, _c in posto:
                    aplicado[j] = velho
                continue
            for j, _velho, novo, cel in posto:
                escritas[j] = novo
                ocupadas.append(cel)
            postos[car["nome"]].append((x, y))
            break
    return L, W, H, v, escritas, {k: len(v2) for k, v2 in postos.items()}


# ---------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def _enfeite():
    """O plano do `enfeita_cidades.py`, que desenha nesta MESMA Canalave."""
    if not os.path.exists(PLANO_ENFEITE):
        return {}
    return json.load(open(PLANO_ENFEITE))


def base_de(guardado):
    """A grade sem enfeite NENHUM: nem o porto daqui, nem o do outro script.

    Desfazer so o porto nao bastava. Rodando porto e `enfeita_cidades.py` em
    sequencia duas vezes, na segunda o porto planejava sobre um mapa que ja
    tinha os enfeites do outro script, e um poste de luz saiu de (9,18) para
    (9,20): plano diferente com a mesma base, ou seja, nao idempotente. Medido
    em 06/09/2026.
    """
    v = list(G.grade(ALVO)[4])
    for reg in (guardado, _enfeite()):
        for idx, antigo, novo in reg.get(ALVO, {}).get("celulas", []):
            if v[idx] == novo:
                v[idx] = antigo
    return v


def grade_atual_sem_porto(guardado):
    """A grade COMO ESTA no disco, so tirando o porto velho.

    O plano sai da base limpa (ordem nao importa), mas a ESCRITA vai por cima do
    disco, senao gravar o porto apagaria o desenho do `enfeita_cidades.py`.
    """
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    print("kit do porto: %d tiles novos (vagas %d a %d de %d), %d metatiles novos "
          "(locais %d a %d), paletas %s"
          % (len(tiles_novos), TILE_LOCAL_0, TILE_LOCAL_0 + len(tiles_novos) - 1,
             TETO_TILES, len(metas), min(metas), max(metas),
             ", ".join("%d->%d" % kv for kv in sorted(PAL_NOVAS.items()))))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base_de(guardado))
    print("no mapa: " + ", ".join("%s x%d" % (k, n) for k, n in contas.items())
          + " | %d celulas" % len(escritas))
    if aplicar:
        saida = grade_atual_sem_porto(guardado)
        pisado = {i for reg in [_enfeite().get(ALVO, {})]
                  for i, a, n in reg.get("celulas", []) if i in escritas and a != n}
        if pisado:
            print("AVISO: %d celulas do porto caem em cima de enfeite; rode "
                  "enfeita_cidades.py depois" % len(pisado))
        for i, val in escritas.items():
            saida[i] = val
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(saida), *saida))
        guardado[ALVO] = {"celulas": [[i, v[i], escritas[i]] for i in sorted(escritas)]}
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("aplicado")
    return escritas


def desfaz():
    guardado = carrega_plano()
    if ALVO not in guardado:
        print("nada a desfazer")
        return 0
    d, L, W, H, v = G.grade(ALVO)
    v, n = list(v), 0
    for idx, antigo, novo in guardado[ALVO]["celulas"]:
        if v[idx] == novo:
            v[idx] = antigo
            n += 1
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(v), *v))
    guardado.pop(ALVO)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("desfeito %d celulas do porto" % n)
    return 0


def demo():
    mau = []
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    # 1. orcamento
    if TILE_LOCAL_0 + len(tiles_novos) > TETO_TILES:
        mau.append("estoura o teto de tiles")
    if max(metas) >= TETO_META:
        mau.append("estoura o teto de metatiles")
    for de, para in PAL_NOVAS.items():
        if para < 9 or para > 12:
            mau.append("paleta %d fora da faixa livre 9-12" % para)
    # 2. as vagas de paleta escolhidas estao mesmo livres no Canalave de HOJE
    meta_can = open(f"{DESTINO}/metatiles.bin", "rb").read()
    usadas = set()
    for local in range(len(meta_can) // 16):
        if local in metas:
            continue
        for valor in _entradas(meta_can, local):
            usadas.add((valor >> 12) & 0xF)
    for para in PAL_NOVAS.values():
        if para in usadas:
            mau.append("paleta %d ja e usada por outro metatile do Canalave" % para)
    # 3. comportamento: barco continua com o comportamento da AGUA, e peca de
    #    terra com o da calcada. E o que garante que nenhuma regra mudou.
    attr_pri = open(f"{RAIZ}/data/tilesets/primary/general_sinnoh/metatile_attributes.bin",
                    "rb").read()
    beh_agua = struct.unpack_from("<H", attr_pri, CHAO_AGUA * 2)[0] & 0x1FF
    attr_can = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()
    beh_calc = struct.unpack_from("<H", attr_can, (CHAO_CALCADA - 512) * 2)[0] & 0x1FF
    for car in carimbos:
        esperado = beh_agua if car["chao"] == "agua" else beh_calc
        for linha in car["ids"]:
            for gid in linha:
                if (attrs[gid - 512] & 0x1FF) != esperado:
                    mau.append("%s: comportamento %d, esperado %d"
                               % (car["nome"], attrs[gid - 512] & 0x1FF, esperado))
    # 4. plano do mapa: nada em evento, barco so em agua, peca de terra so em
    #    calcada, e o canal continua passavel para quem surfa
    guardado = carrega_plano()
    base = base_de(guardado)
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base)
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    ev = E.eventos(d)
    for i in escritas:
        if (i % W, i // W) in ev:
            mau.append("escreveu no evento (%d,%d)" % (i % W, i // W))
    aguas = {gid for car in carimbos if car["chao"] == "agua"
             for linha in car["ids"] for gid in linha}
    for i, val in escritas.items():
        molhado = beh(v[i] & 0x3FF) in AG
        if molhado != ((val & 0x3FF) in aguas):
            mau.append("peca no chao errado em (%d,%d)" % (i % W, i // W))
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    ocupadas = {i for i in escritas}
    if (agua_alcance(v, W, H, AG, beh) - agua_alcance(saida, W, H, AG, beh)) - ocupadas:
        mau.append("o canal deixou de ser passavel para quem surfa")
    ini = E.partidas(d, W, H, v)
    if (E.alcance(v, W, H, ini) - E.alcance(saida, W, H, ini)) - {
            (i % W, i // W) for i in escritas}:
        mau.append("alguem ficou inalcancavel a pe")
    # 5. idempotente
    base2 = list(saida)
    for i in sorted(escritas):
        if base2[i] == escritas[i]:
            base2[i] = v[i]
    if base2 != list(v):
        mau.append("desfazer nao devolve a base")
    _, _, _, _, escritas2, _ = plano_mapa(carimbos, base2)
    if escritas2 != escritas:
        mau.append("segunda passada deu plano diferente")
    # 6. tem que sobrar canal para surfar: pelo menos 3 celulas de largura em
    #    cada linha em que um barco entrou
    if sum(contas.values()) < 8:
        mau.append("so %d pecas no porto" % sum(contas.values()))
    if mau:
        print("DEMO VERMELHA")
        for x in mau:
            print("  -", x)
        return 1
    print("DEMO VERDE: %d tiles, %d metatiles, %d pecas, 6 casos"
          % (len(tiles_novos), len(metas), sum(contas.values())))
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--desfazer" in sys.argv:
        return desfaz()
    roda("--aplicar" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
