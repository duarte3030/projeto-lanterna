#!/usr/bin/env python3
"""Importa o KIT DE NEVE do Golden Glazed para o `gTileset_Snowpoint` e quebra o
carimbo dominante de `SnowpointCity`.

A medida que motiva o trabalho, e ela e da regua da onda 0 do PRD-REFINO
(`amostras-tileset/refino/recon-cidades.tsv`): entre as 22 cidades exteriores do
cartucho 1, `SnowpointCity` e a MAIS POBRE. 87,9% do chao andavel dela e "chao
liso" e UM SO metatile, o 513, responde por 65,1% das 1.073 celulas andaveis. O
render de antes mostra o que a conta diz: um mar de neve branca, sem uma marca,
sem um banco de neve, sem um monte encostado no pe das arvores.

O que este script NAO e, e isso vem da secao 0.2 e da regra 4 do PRD: nao e
redesenho de planta, nao e troca de tileset e nao encosta em colisao, elevacao,
warp, evento nem comportamento. Ele so acrescenta VOCABULARIO DE CHAO ao
`gTileset_Snowpoint`, em vaga livre, e reescreve os 10 bits de indice de metatile
de um punhado de celulas que hoje sao todas o mesmo 513.

DE ONDE VEM A ARTE, e por que ela e legitima. Do `Pokemon Golden Glazed` (base
Emerald, o mesmo motor deste repo), par de tilesets `0x3DF704` (primario) e
`0x3DF7AC` (secundario), que e a CIDADE DE NEVE do hack. A escolha do par nao foi
adivinhada: o atlas rotulado da recon
(`amostras-tileset/refino/atlas-gg-neve-rotulado.png`) foi conferido metatile a
metatile contra os atlas regerados de todos os pares do hack, e so esse bateu
(277 de 288 metatiles identicos pixel a pixel; os 11 restantes sao metatiles
vazios, em que o atlas salvo pinta o fundo com 20,20,20 e o regerado com
24,24,24). O par ja tinha passado pela prova da onda 0 e passou de novo nesta
frente: `render_hack` direto da ROM contra `render_maps.py` a partir do tileset
extraido, ZERO pixel diferente de 409.600. Credito em `CREDITS.md`, que e a
regra 2 do PRD.

A ROM e privada e nunca entra no repo (regra 1). O que entra e o ASSET
CONVERTIDO: `dev_scripts/neve_snowpoint_kit.json` guarda, para cada peca, os
tiles 8x8 ja em nibbles e a paleta ja em RGB. `--extrai` regenera esse arquivo a
partir da ROM (so roda na maquina que tem `fontes-mapas/`); `--aplicar` nunca
abre a ROM.

COMO O METATILE NOVO E MONTADO, e por que nada muda de regra. Metatile do Emerald
tem duas camadas de quatro tiles. O metatile 513 (a neve lisa de Snowpoint) usa
so a camada de BAIXO: as quatro entradas de cima dele sao zero. Entao:

  - a camada de BAIXO do metatile novo e a do 513, entrada por entrada, byte a
    byte. A neve continua sendo a NOSSA neve, com a nossa paleta 9;
  - a camada de CIMA vem inteira do Golden Glazed, so trocando o indice do tile
    para a vaga nova dentro do Snowpoint. O numero da paleta nao muda porque a
    paleta 6 do secundario do hack cai na vaga 6 do nosso, que estava livre;
  - o ATRIBUTO do metatile novo e o do 513 INTEIRO (0x0021), nao so o
    comportamento. O `porto_canalave.py` herda o `layerType` da fonte
    (`attr_src & 0xF000`); aqui isso seria errado, porque o portao desta frente
    cobra `(comportamento, layerType)` identico celula a celula, e o layerType
    da fonte nem sempre e o nosso. Copiando o atributo inteiro, comportamento e
    layerType saem identicos por construcao, e ainda assim a verificacao roda.

COLISAO: NENHUMA CELULA MUDA DE COLISAO, e essa e a diferenca de desenho para o
`porto_canalave.py`. La o bote SOLIDIFICA agua (colisao 0 -> 1). Aqui a definicao
de pronto da frente exige os bits 10 a 15 de TODAS as palavras do `map.bin`
identicos antes e depois, em 100%, entao toda peca deste kit e PLANA: marca de
neve, banco de neve, crista, muda no pe da mata. Peca com volume (arbusto, pedra,
boneco de neve, cerca, poste, banco) so poderia entrar em celula que JA e solida,
e as unicas celulas solidas de neve lisa que existem em Snowpoint sao as 24 do
telhado do ginasio (13..20, 2..4) mais duas em (20..21, 24): telhado de predio
nao ganha arbusto. Por isso o kit ficou so com chao, que e exatamente o que o
alvo do trabalho pede, porque o carimbo dominante e do CHAO.

ORCAMENTO, medido antes de escrever (`compacta_tileset.py` e a leitura direta das
pastas), nao "provavelmente cabe":

  - TILES: o `gTileset_Snowpoint` usa 224 dos 512 tiles de um secundario, e
    sobram 288 vagas. O kit gasta 14, nas vagas 224 a 237, e o `tiles.png`
    cresce de 128x112 para 128x128. Sobram 274.
  - PALETAS: os 300 metatiles do tileset usam as vagas 0, 1, 3, 5, 7, 8, 9, 11 e
    12. As vagas 6, 10, 13, 14 e 15 estao LIVRES. O kit usa UMA, a 6, e la entra
    a paleta 6 do secundario do Golden Glazed inteira.
  - METATILES: o `metatiles.bin` tem 300 locais (ids 512 a 811) e os cinco mapas
    que usam este tileset (`SnowpointCity`, `AcuityLakefront`, `LakeAcuity`,
    `Route216`, `Route217`) usam 147 deles, o maior sendo o local 167. Os locais
    168 a 299 estao livres E sao enchimento do dumper. O kit ocupa 168 a 178, e o
    script RECUSA gravar se algum desses ids aparecer em `map.bin` de qualquer um
    dos cinco.

ONDE CADA PECA ENCOSTA, e isso e julgamento, nao sorteio. Neve nao cai igual em
todo lugar: ela EMPILHA contra o que barra o vento. Entao cada peca declara um
`encosto`, e o plano so a aceita na celula certa:

  - `N` (banco de neve, beirada, muda de pinheiro): a arte ocupa a fileira de
    CIMA do metatile, e por isso a celula precisa de vizinho SOLIDO ao norte. E o
    monte que se forma no pe da mata e na parede do predio. Em Snowpoint ha 87
    celulas assim.
  - `W` e `L` (crista de neve): a arte ocupa uma COLUNA, e a celula precisa de
    solido do lado correspondente. A versao do leste e a mesma arte com o bit de
    espelho horizontal ligado, que e o que o proprio Golden Glazed faz nos pares
    5/6 e 77/78: nao custa tile novo.
  - `-` (rastro de neve): peca solta, de campo aberto, com espacamento grande
    para nao virar sarampo.

Nenhuma peca cai em evento nem na orla de 1 celula em volta dele (`congelado`),
nem a menos de 2 celulas da borda do mapa, nem em celula que o
`enfeita_cidades.py` ja reservou no plano dele.

Idempotente: vaga de tile, de paleta e de metatile sao fixas, e o plano guarda o
valor antigo de cada celula em `dev_scripts/neve_snowpoint.json`. Rodar duas
vezes da byte identico.

ORDEM: este script roda ANTES do `enfeita_cidades.py`, como o `porto_canalave.py`.
Ele planeja sobre a base limpa (sem enfeite nenhum, nem o dele) e escreve por
cima do disco, para nao apagar o desenho do outro.

Uso:
    python3 dev_scripts/neve_snowpoint.py             # mede e mostra o plano
    python3 dev_scripts/neve_snowpoint.py --aplicar   # escreve tileset e mapa
    python3 dev_scripts/neve_snowpoint.py --desfazer  # devolve o map.bin
    python3 dev_scripts/neve_snowpoint.py --demo      # auto-teste
    python3 dev_scripts/neve_snowpoint.py --autoteste # idem
    python3 dev_scripts/neve_snowpoint.py --extrai    # regera o kit a partir da ROM
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

ALVO = "SnowpointCity"
DESTINO = f"{RAIZ}/data/tilesets/secondary/snowpoint"
KIT_JSON = f"{RAIZ}/dev_scripts/neve_snowpoint_kit.json"
PLANO = f"{RAIZ}/dev_scripts/neve_snowpoint.json"
PLANO_ENFEITE = f"{RAIZ}/dev_scripts/enfeita_cidades.json"

# os cinco layouts que compartilham o gTileset_Snowpoint
IRMAOS = ["SnowpointCity", "AcuityLakefront", "LakeAcuity", "Route216", "Route217"]

TILE_LOCAL_0 = 224      # primeira vaga de tile livre no Snowpoint
META_LOCAL_0 = 168      # primeira vaga de metatile livre (id global 680)
PAL_NOVA = 6            # vaga de paleta livre que recebe a paleta 6 do hack
TETO_TILES = 512
TETO_META = 512
MARGEM = 2              # celulas de folga em relacao a borda do mapa

CHAO = 513              # o carimbo dominante: a neve lisa de Snowpoint

# A fonte, para o `--extrai` e para o rastro.
FONTE = dict(slug="golden-glazed", ts1=0x3DF704, ts2=0x3DF7AC,
             hack="Pokemon Golden Glazed", mapa="grupo 0 mapa 0 (a cidade de neve)")

# O KIT. `gg` e o indice LOCAL do metatile no secundario do Golden Glazed;
# `espelha` liga o bit de espelho horizontal em cima da arte da fonte (o proprio
# hack faz isso nos pares 5/6 e 77/78, entao nao custa tile novo); `encosto` diz
# de que lado a celula precisa ter solido; `quantos` e o teto de copias e
# `espaco` a distancia minima (Chebyshev) entre duas copias da MESMA peca.
KIT = [
    dict(nome="muda de pinheiro",           gg=12, espelha=False, encosto="N",
         quantos=6,  espaco=8),
    dict(nome="banco de neve largo",        gg=77, espelha=False, encosto="N",
         quantos=22, espaco=2),
    dict(nome="banco de neve espelhado",    gg=78, espelha=False, encosto="N",
         quantos=22, espaco=2),
    dict(nome="beirada de neve",            gg=70, espelha=False, encosto="N",
         quantos=18, espaco=2),
    dict(nome="beirada de neve curta",      gg=69, espelha=False, encosto="N",
         quantos=16, espaco=2),
    dict(nome="beirada de neve no canto",   gg=71, espelha=False, encosto="N",
         quantos=16, espaco=2),
    dict(nome="pingo de neve",              gg=76, espelha=False, encosto="N",
         quantos=16, espaco=2),
    dict(nome="crista de neve",             gg=79, espelha=False, encosto="W",
         quantos=34, espaco=2),
    dict(nome="crista de neve espelhada",   gg=79, espelha=True,  encosto="L",
         quantos=34, espaco=2),
    dict(nome="rastro de neve",             gg=5,  espelha=False, encosto="-",
         quantos=10, espaco=8),
    dict(nome="rastro de neve espelhado",   gg=6,  espelha=False, encosto="-",
         quantos=10, espaco=8),
]

VIZINHO = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "L": (1, 0)}
N4 = E.N4


# ------------------------------------------------------------------ extracao
def extrai():
    """Regera `neve_snowpoint_kit.json` a partir da ROM privada do hack.

    So roda na maquina que tem `fontes-mapas/romhacks/`. O que sai daqui e o
    asset convertido (tiles em nibbles e paleta em RGB), nunca a ROM.
    """
    ferr = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks"
    if not os.path.isdir(ferr):
        raise SystemExit("nao achei fontes-mapas/romhacks: --extrai so roda na "
                         "maquina que tem as ROMs. O kit ja extraido esta em "
                         + os.path.relpath(KIT_JSON, RAIZ))
    sys.path.insert(0, f"{ferr}/ferramentas")
    import hashlib
    from gbamap import Rom  # noqa: E402
    pasta = os.path.join(ferr, FONTE["slug"])
    gba = [f for f in sorted(os.listdir(pasta)) if f.lower().endswith(".gba")][0]
    caminho = os.path.join(pasta, gba)
    md5 = hashlib.md5(open(caminho, "rb").read()).hexdigest()
    r = Rom(caminho)
    t2 = r.parse_tileset(FONTE["ts2"])
    meta, pal, tiles = t2["meta"], t2["pal"], t2["tiles"]

    def entradas(local):
        return list(struct.unpack_from("<8H", meta, local * 16))

    def tile_nibbles(local):
        """8 linhas de 8 nibbles, o pixel PAR no nibble BAIXO (ver extrai_tileset)."""
        b = tiles[local * 32:local * 32 + 32]
        return [[(b[y * 4 + (x >> 1)] >> (0 if x % 2 == 0 else 4)) & 0xF
                 for x in range(8)] for y in range(8)]

    precisa, pecas = {}, []
    for peca in KIT:
        cima = entradas(peca["gg"])[4:]
        for v in cima:
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            if idx == 0:
                continue
            if idx < r.n_tiles_pri:
                raise SystemExit("%s: usa tile do PRIMARIO do hack (%d)"
                                 % (peca["nome"], idx))
            if ip != PAL_NOVA:
                raise SystemExit("%s: paleta %d, e o kit so importa a %d"
                                 % (peca["nome"], ip, PAL_NOVA))
            precisa[idx - r.n_tiles_pri] = True
        pecas.append(dict(nome=peca["nome"], gg=peca["gg"], cima=cima))

    cores = struct.unpack_from("<16H", pal, PAL_NOVA * 32)
    dados = dict(
        fonte=dict(hack=FONTE["hack"], arquivo=gba, md5=md5,
                   ts1="0x%X" % FONTE["ts1"], ts2="0x%X" % FONTE["ts2"],
                   mapa=FONTE["mapa"], n_tiles_pri=r.n_tiles_pri),
        paleta={str(PAL_NOVA): [[((c >> s) & 0x1F) * 255 // 31
                                 for s in (0, 5, 10)] for c in cores]},
        tiles={str(k): tile_nibbles(k) for k in sorted(precisa)},
        pecas=pecas,
    )
    with open(KIT_JSON, "w") as f:
        json.dump(dados, f, indent=1)
    print("kit gravado em %s: %d tiles, 1 paleta, %d pecas"
          % (os.path.relpath(KIT_JSON, RAIZ), len(dados["tiles"]), len(pecas)))


# --------------------------------------------------------------------- leitura
def kit():
    if not os.path.exists(KIT_JSON):
        raise SystemExit("falta %s; rode --extrai numa maquina com as ROMs"
                         % os.path.relpath(KIT_JSON, RAIZ))
    return json.load(open(KIT_JSON))


def _entradas(bin_meta, local):
    return [struct.unpack_from("<H", bin_meta, local * 16 + i * 2)[0] for i in range(8)]


def _espelha4(cima):
    """Espelho horizontal do metatile: troca as colunas e liga o bit 0x400."""
    fora = []
    for q in (1, 0, 3, 2):
        v = cima[q]
        fora.append(0 if (v & 0x3FF) == 0 and v == 0 else (v ^ 0x400))
    return fora


# ------------------------------------------------------------------ importacao
def desenha_kit():
    """(tiles_novos, metatiles_novos, atributos, carimbos), sem escrever nada."""
    dados = kit()
    n_pri = dados["fonte"]["n_tiles_pri"]
    meta_snow = open(f"{DESTINO}/metatiles.bin", "rb").read()
    attr_snow = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()

    base_baixo = _entradas(meta_snow, CHAO - 512)[:4]
    attr_chao = struct.unpack_from("<H", attr_snow, (CHAO - 512) * 2)[0]
    if _entradas(meta_snow, CHAO - 512)[4:] != [0, 0, 0, 0]:
        raise SystemExit("o metatile %d ja usa a camada de cima; o kit precisa "
                         "dela livre" % CHAO)

    por_gg = {p["gg"]: p for p in dados["pecas"]}
    tiles_novos, mapa_tile = {}, {}
    metas, attrs, carimbos = {}, {}, []
    proximo_tile = TILE_LOCAL_0
    proximo_meta = META_LOCAL_0

    for peca in KIT:
        fonte = por_gg.get(peca["gg"])
        if fonte is None:
            raise SystemExit("o kit em disco nao tem o metatile %d do hack"
                             % peca["gg"])
        cima = []
        for v in fonte["cima"]:
            idx, ip = v & 0x3FF, (v >> 12) & 0xF
            if idx == 0:
                cima.append(0)
                continue
            local_fonte = idx - n_pri
            if local_fonte not in mapa_tile:
                if str(local_fonte) not in dados["tiles"]:
                    raise SystemExit("o kit em disco nao tem o tile %d"
                                     % local_fonte)
                mapa_tile[local_fonte] = proximo_tile
                tiles_novos[proximo_tile] = dados["tiles"][str(local_fonte)]
                proximo_tile += 1
            novo = 512 + mapa_tile[local_fonte]
            cima.append((v & 0x0C00) | novo | (PAL_NOVA << 12))
        if peca["espelha"]:
            cima = _espelha4(cima)
        metas[proximo_meta] = list(base_baixo) + cima
        # atributo INTEIRO do chao: comportamento E layerType identicos ao 513.
        attrs[proximo_meta] = attr_chao
        carimbos.append(dict(nome=peca["nome"], id=512 + proximo_meta,
                             encosto=peca["encosto"], quantos=peca["quantos"],
                             espaco=peca["espaco"], gg=peca["gg"],
                             espelha=peca["espelha"]))
        proximo_meta += 1

    if proximo_tile > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles (%d)"
                         % (TETO_TILES, proximo_tile))
    if proximo_meta > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)

    # A vaga de metatile so serve se for ENCHIMENTO do dumper (as oito entradas
    # iguais e baixas) ou se ja tiver exatamente o que este kit escreve (caso de
    # rodar duas vezes), e nenhum dos CINCO mapas do tileset pode usar o id.
    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    usados = set()
    for nome in IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    for local, entradas in metas.items():
        gid = 512 + local
        antigo = _entradas(meta_snow, local)
        if not enchimento(antigo) and antigo != entradas:
            raise SystemExit("vaga de metatile %d ja esta ocupada por outra coisa"
                             % gid)
        if gid in usados and enchimento(antigo):
            raise SystemExit("algum dos cinco mapas usa o metatile %d e a vaga "
                             "esta vazia" % gid)

    # A vaga de paleta tem que estar livre em TODOS os metatiles do tileset que
    # nao sejam do kit.
    for local in range(len(meta_snow) // 16):
        if local in metas:
            continue
        for valor in _entradas(meta_snow, local):
            if (valor >> 12) & 0xF == PAL_NOVA:
                raise SystemExit("a paleta %d ja e usada pelo metatile %d"
                                 % (PAL_NOVA, 512 + local))
    return tiles_novos, metas, attrs, carimbos


def grava_tileset(tiles_novos, metas, attrs):
    from PIL import Image
    dados = kit()
    # 1. tiles.png cresce so o que precisa, em multiplo de linha de 16 tiles
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    alvo_tiles = max(TILE_LOCAL_0 + len(tiles_novos), (antigo.size[1] // 8) * cols)
    linhas = (alvo_tiles + cols - 1) // cols
    novo = Image.new("P", (antigo.size[0], linhas * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    px = novo.load()
    for vaga, tile in tiles_novos.items():
        x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = tile[y][x]
    novo.save(f"{DESTINO}/tiles.png")

    # 2. paleta: a do hack inteira na vaga livre, em JASC-PAL
    cores = dados["paleta"][str(PAL_NOVA)]
    with open(f"{DESTINO}/palettes/%02d.pal" % PAL_NOVA, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n16\n")
        for r, g, b in cores:
            f.write("%d %d %d\n" % (r, g, b))

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
def plano_mapa(carimbos, base=None):
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    _ev, gelo = E.congelado(d)
    # o que o enfeita_cidades.py ja reservou nesta cidade fica fora, com orla de
    # 1: assim os dois scripts nunca disputam a mesma celula.
    for idx, _a, _n in _enfeite().get(ALVO, {}).get("celulas", []):
        x, y = idx % W, idx // W
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                gelo.add((x + dx, y + dy))

    def solido(x, y):
        return 0 <= x < W and 0 <= y < H and ((v[y * W + x] >> 10) & 3)

    escritas = {}
    postos = collections.defaultdict(list)

    def cabe(car, x, y):
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas:
            return False
        # SO o carimbo dominante: e ele que este trabalho existe para quebrar, e
        # so ele garante que o atributo antigo e o 0x0021 que o kit copia.
        if (v[i] & 0x3FF) != CHAO or ((v[i] >> 10) & 3):
            return False
        if car["encosto"] != "-":
            dx, dy = VIZINHO[car["encosto"]]
            if not solido(x + dx, y + dy):
                return False
        else:
            # rastro e peca de campo aberto: nada solido em volta
            if any(solido(x + dx, y + dy) for dx, dy in N4):
                return False
        if any(max(abs(x - px), abs(y - py)) < car["espaco"]
               for px, py in postos[car["nome"]]):
            return False
        return True

    ordem = sorted(((x, y) for y in range(H) for x in range(W)),
                   key=lambda p: ((p[1] * 2654435761 + p[0] * 40503) & 0xFFFF, p))
    for x, y in ordem:
        # rodizio: a peca da vez comeca num ponto que depende da celula, senao a
        # primeira da lista come todas as vagas de encosto e as ultimas ficam em
        # zero (medido: `beirada no canto` e `pingo de neve` sairam x0).
        giro = ((x * 73856093) ^ (y * 19349663)) % len(carimbos)
        for k in range(len(carimbos)):
            car = carimbos[(giro + k) % len(carimbos)]
            if len(postos[car["nome"]]) >= car["quantos"]:
                continue
            if not cabe(car, x, y):
                continue
            i = y * W + x
            escritas[i] = (v[i] & 0xFC00) | car["id"]
            postos[car["nome"]].append((x, y))
            break
    return L, W, H, v, escritas, {k: len(p) for k, p in postos.items()}


# ---------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def _enfeite():
    """O plano do `enfeita_cidades.py`, que desenha nesta MESMA Snowpoint."""
    if not os.path.exists(PLANO_ENFEITE):
        return {}
    return json.load(open(PLANO_ENFEITE))


def base_de(guardado):
    """A grade sem enfeite NENHUM: nem a neve daqui, nem o do outro script."""
    v = list(G.grade(ALVO)[4])
    for reg in (guardado, _enfeite()):
        for idx, antigo, novo in reg.get(ALVO, {}).get("celulas", []):
            if v[idx] == novo:
                v[idx] = antigo
    return v


def grade_atual_sem_neve(guardado):
    """A grade COMO ESTA no disco, so tirando a neve velha desta frente."""
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    print("kit de neve: %d tiles novos (vagas %d a %d de %d, sobram %d), "
          "%d metatiles novos (locais %d a %d, ids %d a %d), paleta %d"
          % (len(tiles_novos), TILE_LOCAL_0, TILE_LOCAL_0 + len(tiles_novos) - 1,
             TETO_TILES, TETO_TILES - TILE_LOCAL_0 - len(tiles_novos),
             len(metas), min(metas), max(metas), 512 + min(metas), 512 + max(metas),
             PAL_NOVA))
    if aplicar:
        grava_tileset(tiles_novos, metas, attrs)
    guardado = carrega_plano()
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base_de(guardado))
    print("no mapa: " + ", ".join("%s x%d" % (k, n) for k, n in contas.items())
          + " | %d celulas" % len(escritas))
    antes = collections.Counter(c & 0x3FF for c in v if not ((c >> 10) & 3))
    n_and = sum(antes.values())
    print("carimbo dominante %d: %d/%d = %.1f%% antes, %.1f%% depois"
          % (CHAO, antes[CHAO], n_and, 100.0 * antes[CHAO] / n_and,
             100.0 * (antes[CHAO] - len(escritas)) / n_and))
    if aplicar:
        saida = grade_atual_sem_neve(guardado)
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
    print("desfeitas %d celulas de neve" % n)
    return 0


def demo():
    mau = []
    tiles_novos, metas, attrs, carimbos = desenha_kit()
    meta_snow = open(f"{DESTINO}/metatiles.bin", "rb").read()
    attr_snow = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()
    attr_chao = struct.unpack_from("<H", attr_snow, (CHAO - 512) * 2)[0]
    base_baixo = _entradas(meta_snow, CHAO - 512)[:4]

    # 1. orcamento
    if TILE_LOCAL_0 + len(tiles_novos) > TETO_TILES:
        mau.append("estoura o teto de tiles")
    if max(metas) >= TETO_META:
        mau.append("estoura o teto de metatiles")
    if PAL_NOVA < 6 or PAL_NOVA > 15:
        mau.append("paleta %d nao e do lado secundario" % PAL_NOVA)

    # 2. camada de BAIXO e a nossa neve, entrada por entrada
    for local, ent in metas.items():
        if ent[:4] != base_baixo:
            mau.append("metatile %d nao tem a neve de Snowpoint embaixo" % (512 + local))
        if all((x & 0x3FF) == 0 for x in ent[4:]):
            mau.append("metatile %d nao desenha nada em cima" % (512 + local))

    # 3. atributo INTEIRO igual ao do chao: comportamento E layerType
    for local, a in attrs.items():
        if a != attr_chao:
            mau.append("metatile %d: atributo 0x%04X, esperado 0x%04X"
                       % (512 + local, a, attr_chao))

    # 4. plano do mapa: so no carimbo dominante, nunca em evento, encosto certo
    guardado = carrega_plano()
    base = base_de(guardado)
    L, W, H, v, escritas, contas = plano_mapa(carimbos, base)
    d = json.load(open(f"{RAIZ}/data/maps/{ALVO}/map.json"))
    ev = E.eventos(d)
    por_id = {c["id"]: c for c in carimbos}

    def solido(x, y):
        return 0 <= x < W and 0 <= y < H and ((v[y * W + x] >> 10) & 3)

    for i, val in escritas.items():
        x, y = i % W, i // W
        if (x, y) in ev:
            mau.append("escreveu no evento (%d,%d)" % (x, y))
        if (v[i] & 0x3FF) != CHAO:
            mau.append("escreveu fora do carimbo dominante em (%d,%d)" % (x, y))
        if (val & 0xFC00) != (v[i] & 0xFC00):
            mau.append("mudou colisao ou elevacao em (%d,%d)" % (x, y))
        car = por_id.get(val & 0x3FF)
        if car is None:
            mau.append("celula (%d,%d) recebeu metatile fora do kit" % (x, y))
            continue
        if car["encosto"] == "-":
            if any(solido(x + dx, y + dy) for dx, dy in N4):
                mau.append("%s: peca solta encostada em (%d,%d)" % (car["nome"], x, y))
        else:
            dx, dy = VIZINHO[car["encosto"]]
            if not solido(x + dx, y + dy):
                mau.append("%s: sem solido a %s em (%d,%d)"
                           % (car["nome"], car["encosto"], x, y))

    # 5. colisao e elevacao byte a byte, e alcance a pe intacto
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    if [c & 0xFC00 for c in saida] != [c & 0xFC00 for c in v]:
        mau.append("os bits 10 a 15 mudaram em alguma celula")
    ini = E.partidas(d, W, H, v)
    if E.alcance(saida, W, H, ini) != E.alcance(v, W, H, ini):
        mau.append("o alcance a pe mudou, e nenhuma peca deste kit tem colisao")

    # 6. idempotente
    base2 = list(saida)
    for i in sorted(escritas):
        if base2[i] == escritas[i]:
            base2[i] = v[i]
    if base2 != list(v):
        mau.append("desfazer nao devolve a base")
    _, _, _, _, escritas2, _ = plano_mapa(carimbos, base2)
    if escritas2 != escritas:
        mau.append("segunda passada deu plano diferente")

    # 7. o trabalho tem que valer a pena: o carimbo dominante precisa cair
    antes = collections.Counter(c & 0x3FF for c in v if not ((c >> 10) & 3))
    n_and = sum(antes.values())
    frac = 100.0 * (antes[CHAO] - len(escritas)) / n_and
    if len(escritas) < 100:
        mau.append("so %d celulas trocadas; o carimbo nao quebrou" % len(escritas))
    if frac > 52.0:
        mau.append("o carimbo dominante ainda tem %.1f%% do chao andavel" % frac)

    # 8. O QUE ESTA NO DISCO e o que o kit manda. Sem este caso o auto-teste so
    #    conferia o que ele mesmo acabou de calcular em memoria: sabotando o
    #    atributo do metatile 682 e um tile da vaga 230 direto no disco, os sete
    #    casos anteriores continuavam VERDES (medido em 06/09/2026). Quem pegou a
    #    sabotagem foi o render, e verificacao que depende de outra ferramenta
    #    nao e verificacao deste script.
    from PIL import Image
    png = Image.open(f"{DESTINO}/tiles.png")
    cols = png.size[0] // 8
    px = png.convert("P").load()
    disco_meta = open(f"{DESTINO}/metatiles.bin", "rb").read()
    disco_attr = open(f"{DESTINO}/metatile_attributes.bin", "rb").read()

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    postas = [l for l in metas if not enchimento(_entradas(disco_meta, l))]
    if not postas:
        print("aviso: o kit ainda nao foi aplicado no tileset; caso 8 nao roda")
    else:
        if len(postas) != len(metas):
            mau.append("o kit esta pela metade no disco: %d de %d metatiles"
                       % (len(postas), len(metas)))
        for local, ent in metas.items():
            if _entradas(disco_meta, local) != ent:
                mau.append("metatile %d no disco nao e o do kit" % (512 + local))
            if struct.unpack_from("<H", disco_attr, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco nao e o do kit"
                           % (512 + local))
        for vaga, tile in tiles_novos.items():
            if (vaga // cols) * 8 + 8 > png.size[1]:
                mau.append("a vaga de tile %d nao cabe no tiles.png" % vaga)
                continue
            x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
            if [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)] != tile:
                mau.append("o tile da vaga %d no disco nao e o do kit" % vaga)

    if mau:
        print("DEMO VERMELHA")
        for x in mau:
            print("  -", x)
        return 1
    print("DEMO VERDE: %d tiles, %d metatiles, %d pecas, %d celulas, carimbo "
          "dominante de %.1f%% para %.1f%%, 8 casos"
          % (len(tiles_novos), len(metas), sum(contas.values()), len(escritas),
             100.0 * antes[CHAO] / n_and, frac))
    return 0


def main():
    if "--extrai" in sys.argv:
        return extrai()
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo()
    if "--desfazer" in sys.argv:
        return desfaz()
    roda("--aplicar" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
