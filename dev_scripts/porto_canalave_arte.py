#!/usr/bin/env python3
"""Traz o CAIS do Golden Glazed para Canalave: cabeços de amarração, cabo e boia.

O `porto_canalave.py` (rodada 13) deu a Canalave o primeiro porto, com peças de
HOENN: o bote, o poste e os tambores de Slateport. Ele resolveu a água. Sobrou a
BEIRA: as 71 células sólidas que separam a calçada do canal continuam sendo o
mesmo muro de guarda-corpo branco repetido, e é esse o carimbo dominante da
cidade portuária. Este script quebra esse carimbo com arte de ROM hack.

FONTE ESCOLHIDA, e o número que decidiu. Os três candidatos eram Golden Glazed,
Light Platinum e Scorched Silver (o GS Chronicles saiu porque a arte dele é a
NOSSA arte, zero pixel de diferença). Venceu o **Golden Glazed**, secundário
`0x3DF74C` (par com o primário `0x3DF704`), a cidade portuária dele: **96,6% dos
tiles 8x8 desse tileset não existem em jogo oficial nenhum e 98,0% não existem
em lugar nenhum do nosso repo** (`fontes-mapas/romhacks/ferramentas/
custom_vs_nosso.json`, campos `frac_nova` e `frac_melhor_nosso`). É um cais de
concreto de verdade: deque, cabeços de amarração com cabo vermelho, boia
salva-vidas e escada. A extração foi provada antes de qualquer instalação, no
molde da onda 0: o mapa 0/4 do hack desenhado direto da ROM contra o mesmo mapa
desenhado pelo `dev_scripts/render_maps.py` a partir do tileset extraído deu
**0 pixel diferente de 716.800**.

O ORÇAMENTO QUE MANDA AQUI NÃO É O DE TILE, É O DE PALETA. Medido no HEAD
`5e38ecc96b`, antes de escrever uma linha:

  - TILES: o `gTileset_Canalave` usa 176 das 512 vagas (a compactação devolveu o
    resto), então sobram 336. O kit gasta 9. Não é aqui que aperta.
  - METATILES: 140 dos 512 estão em uso pelo `map.bin`; os locais a partir de
    300 estão todos em branco de enchimento. O kit ocupa a partir do local 300 e
    o script RECUSA gravar em vaga que o mapa use.
  - PALETAS: e aqui aperta. O motor tem `NUM_PALS_TOTAL 13` (0 a 5 do primário,
    6 a 12 do secundário, `include/fieldmap.h`). Canalave usa 6, 7 e 8 na arte
    dela e o porto de Hoenn tomou 9, 10 e 11. **Sobra UMA vaga, a 12.** Portanto
    o kit inteiro tem que caber em UMA paleta, ou seja, em 15 cores mais a
    transparência. O kit escolhido é a paleta 6 do Golden Glazed e gasta 11
    cores: cabe, e as cores são copiadas EXATAS, sem aproximar nenhuma.

POR QUE O KIT NÃO TEM GUINDASTE, CONTAINER NEM BARCO GRANDE. Duas paredes:
  1. a paleta. O veleiro do `0x3DF92C` (o mais bonito da fonte) sozinho gasta as
     15 cores da vaga 12 e não sobra nada para mais nada; o cais de madeira do
     mesmo tileset gasta outras 5, e 11+5 = 16 não cabe em 15. Guindaste e
     container não existem desenhados em nenhum dos três hacks candidatos: foi
     procurado tileset por tileset, na folha de contato de cada paleta.
  2. a colisão. Esta é onda de REFINO, e a regra 4 da seção 4 do PRD-REFINO
     manda os bits 10 a 15 de TODAS as palavras do `map.bin` ficarem idênticos.
     Peça sólida em cima de água mudaria a colisão, então peça grande boiando no
     canal está proibida por regra, não por gosto. O que sobra, e é o que este
     script faz, é: peça sólida só em célula que JÁ é sólida, e objeto rasteiro
     (a boia salva-vidas) em célula que continua do jeito que era.

COMO O METATILE NOVO É MONTADO. A camada de BAIXO é a do CHÃO DE CANALAVE, igual
à célula que estava ali (o muro 525/519, a calçada 521/545/546, a água 368 do
`gTileset_GeneralSinnoh`), e a camada de CIMA é a peça do Golden Glazed, com o
índice de tile apontado para a vaga nova e a paleta apontada para a 12. O
atributo do metatile novo é COPIADO INTEIRO do metatile antigo, então
`behavior` e `layerType` da célula não mudam nem por um bit.

O script só encosta em célula cuja camada de cima é DESCARTÁVEL: ou ela está
vazia (calçada, água), ou ela é byte a byte igual à camada de baixo, que é um
vício do gerador do demake e desenha duas vezes a mesma coisa (o muro 525 e o
519). Assim a peça é sempre ACRÉSCIMO: nenhum pixel do desenho antigo se perde.
Célula cuja camada de cima desenha algo próprio (o muro 526, por exemplo) é
recusada.

ONDE CADA PEÇA ENCOSTA:
  - cabeço de amarração: só em célula SÓLIDA de muro encostada na água. Em muro
    que corre no sentido leste-oeste os cabeços saem em trio, com o cabo
    vermelho amarrando um no outro; em muro que corre norte-sul (o canal) sai o
    cabeço liso, de três em três células, porque o cabo do Golden Glazed é
    horizontal e ficaria torto na vertical.
  - boia salva-vidas: na calçada, a até 4 células da água. Objeto rasteiro:
    passar por cima de uma boia caída no cais não é mentira nenhuma.
  E nunca em cima de evento, nunca na margem do mapa, nunca no corredor de teste
  da suíte.

NADA ENTRA NA ÁGUA, e isso foi medido, não escolhido no gosto. A estaca do
Golden Glazed (metatile 791) tem na camada de cima só a METADE DE CIMA do poste:
a metade de baixo dele mora na camada de baixo, que aqui é substituída pela água
de Sinnoh. Instalada e renderizada, ela vira um coto cinza de meia célula
boiando, que não lê como estaca. Foi tirada do kit depois de olhar o render, e
fica registrado para ninguém tentar de novo sem resolver a metade que falta.

Os DOIS portões de alcance rodam antes e depois (a pé pelos warps respeitando
elevação, e por água pelo canal) e aqui a exigência é a mais dura possível:
`depois == antes`, sem desconto, porque nenhuma peça deste kit muda colisão.

Idempotente: vagas fixas, plano do mapa guardado em
`dev_scripts/porto_canalave_arte.json` com o valor antigo de cada célula. Rodar
duas vezes dá byte idêntico.

ORDEM: `porto_canalave.py`, depois `porto_canalave_arte.py` (este), depois
`enfeita_cidades.py`.

CRÉDITO: Pokémon Golden Glazed, de redriders180 (Glazed) com a revisão de Zel e
Zeturic; a ficha da fonte está em `fontes-mapas/romhacks/golden-glazed/README.md`
e o crédito também está no `CREDITS.md` deste repo. A ROM nunca sai da máquina;
o que entra aqui é asset convertido, como manda a regra 1 da seção 4 do PRD.

Uso:
    python3 dev_scripts/porto_canalave_arte.py               # mede e mostra o plano
    python3 dev_scripts/porto_canalave_arte.py --aplicar     # escreve tileset e mapa
    python3 dev_scripts/porto_canalave_arte.py --desfazer    # devolve o map.bin
    python3 dev_scripts/porto_canalave_arte.py --demo        # auto-teste curto
    python3 dev_scripts/porto_canalave_arte.py --autoteste   # suíte cheia
    python3 dev_scripts/porto_canalave_arte.py --extrair PASTA
        remonta o kit a partir do par de tilesets JÁ EXTRAÍDO do Golden Glazed
        (pasta com gg_pri/ e gg_sec/, saída do fontes-mapas/romhacks/ferramentas/
        extrai_tileset.py). Só quem tem a ROM privada roda isso; o resto do
        mundo usa o kit já convertido que está no JSON.
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
PRIMARIO = f"{RAIZ}/data/tilesets/primary/general_sinnoh"
KIT = f"{RAIZ}/dev_scripts/porto_canalave_arte_kit.json"
PLANO = f"{RAIZ}/dev_scripts/porto_canalave_arte.json"
PLANO_PORTO = f"{RAIZ}/dev_scripts/porto_canalave.json"
PLANO_ENFEITE = f"{RAIZ}/dev_scripts/enfeita_cidades.json"

META_LOCAL_0 = 300      # primeira vaga de metatile do kit (id global 812)
PAL_NOVA = 12           # a ÚNICA vaga de paleta livre no Canalave
TETO_TILES = 512
TETO_META = 512
MARGEM = 3              # células de folga em relação à borda do mapa

# quantidades e espaçamento, medidos no mapa de 38x64 de Canalave
MAX_CABECOS = 24
PASSO_VERTICAL = 3      # um cabeço a cada N células de muro norte-sul
MAX_BOIAS = 5
ESPACO_BOIA = 9
DIST_BOIA_AGUA = 4

# As peças, e o metatile do Golden Glazed de onde a camada de cima veio.
PECAS = collections.OrderedDict([
    ("cabeco liso", dict(origem=820, chao="muro")),
    ("cabeco cabo duplo", dict(origem=814, chao="muro")),
    ("cabeco cabo a direita", dict(origem=811, chao="muro")),
    ("cabeco cabo a esquerda", dict(origem=812, chao="muro")),
    ("boia salva-vidas", dict(origem=807, chao="calcada")),
])

N4 = E.N4


# ------------------------------------------------------------------ utilidades
def _le(caminho):
    with open(caminho, "rb") as f:
        return f.read()


def entradas(bin_meta, local):
    return [struct.unpack_from("<H", bin_meta, local * 16 + i * 2)[0] for i in range(8)]


class Nosso:
    """Os dois tilesets do layout de Canalave, lidos do disco."""

    def __init__(self):
        self.meta_sec = _le(f"{DESTINO}/metatiles.bin")
        self.attr_sec = _le(f"{DESTINO}/metatile_attributes.bin")
        self.meta_pri = _le(f"{PRIMARIO}/metatiles.bin")
        self.attr_pri = _le(f"{PRIMARIO}/metatile_attributes.bin")

    def ent(self, gid):
        if gid >= 512:
            return entradas(self.meta_sec, gid - 512)
        return entradas(self.meta_pri, gid)

    def attr(self, gid):
        if gid >= 512:
            return struct.unpack_from("<H", self.attr_sec, (gid - 512) * 2)[0]
        return struct.unpack_from("<H", self.attr_pri, gid * 2)[0]

    def sobreponivel(self, gid):
        """A camada de cima desta célula pode ser trocada sem perder desenho?

        Vale quando ela está vazia (calçada, água) ou quando ela é igual à
        camada de baixo, que é o vício do gerador do demake: o mesmo tile
        desenhado nas duas camadas, o que dá o mesmo pixel com ou sem a de cima.
        """
        e = self.ent(gid)
        return all(v == 0 for v in e[4:]) or e[:4] == e[4:]


# ----------------------------------------------------------------- kit de arte
def carrega_kit():
    if not os.path.exists(KIT):
        raise SystemExit("falta %s: rode --extrair" % KIT)
    with open(KIT, encoding="utf-8") as f:
        return json.load(f)


def constroi_kit(pasta, saida=KIT):
    """Monta o JSON do kit a partir do par de tilesets extraído do hack.

    Entra a pasta com `gg_pri/` e `gg_sec/` (saída do extrai_tileset.py) e sai o
    kit convertido: a paleta fundida em 16 cores, os tiles 8x8 já reindexados
    para essa paleta, e as quatro entradas da camada de cima de cada peça.
    """
    from PIL import Image
    sec = f"{pasta}/gg_sec"
    pri = f"{pasta}/gg_pri"
    meta = _le(f"{sec}/metatiles.bin")

    def png(caminho):
        img = Image.open(caminho)
        if img.mode != "P":
            raise SystemExit(f"{caminho} nao e PNG indexado")
        W, _H = img.size
        px = img.load()
        cols = W // 8
        return px, cols

    px_sec, cols_sec = png(f"{sec}/tiles.png")
    px_pri, cols_pri = png(f"{pri}/tiles.png")

    def pal_de(pasta_ts, i):
        linhas = open(f"{pasta_ts}/palettes/%02d.pal" % i).read().split("\n")
        k = linhas.index("16") + 1
        return [tuple(int(x) for x in linhas[j].split()) for j in range(k, k + 16)]

    def tile(idx):
        px, cols, base = (px_sec, cols_sec, idx - 512) if idx >= 512 \
            else (px_pri, cols_pri, idx)
        x0, y0 = (base % cols) * 8, (base // cols) * 8
        return [[px[x0 + x, y0 + y] for x in range(8)] for y in range(8)]

    cores, mapa_cor = [], {}
    tiles, mapa_tile = [], {}
    pecas = {}
    for nome, peca in PECAS.items():
        ent = entradas(meta, peca["origem"] - 512)
        cima = []
        for v in ent[4:]:
            idx, pal = v & 0x3FF, (v >> 12) & 0xF
            if idx == 0 and pal == 0:
                # quadrante VAZIO vira `null` no JSON, e nao [0, 0, 0]. O tile
                # 0 do kit e um tile de verdade (o canto do cabeco), entao os
                # dois casos precisam de codigo diferente: com [0, 0, 0] a
                # estaca desenhava metade de um cabeco na parte de baixo dela.
                cima.append(None)
                continue
            paleta = pal_de(sec if pal >= 6 else pri, pal)
            chave = (idx, pal)
            if chave not in mapa_tile:
                bruto = tile(idx)
                novo = []
                for linha in bruto:
                    saida_linha = []
                    for c in linha:
                        if c == 0:
                            saida_linha.append(0)
                            continue
                        cor = paleta[c]
                        if cor not in mapa_cor:
                            if len(cores) >= 15:
                                raise SystemExit(
                                    "o kit passa de 15 cores e so ha a vaga de "
                                    "paleta %d livre" % PAL_NOVA)
                            cores.append(cor)
                            mapa_cor[cor] = len(cores)
                        saida_linha.append(mapa_cor[cor])
                    novo.append(saida_linha)
                mapa_tile[chave] = len(tiles)
                tiles.append(novo)
            cima.append([mapa_tile[chave], 1 if v & 0x400 else 0,
                         1 if v & 0x800 else 0])
        pecas[nome] = dict(origem=peca["origem"], chao=peca["chao"], cima=cima)

    while len(cores) < 15:
        cores.append((0, 0, 0))      # a paleta do GBA tem 16 entradas sempre
    kit = dict(
        fonte=dict(
            hack="golden-glazed",
            rom="Pokemon Golden Glazed (BPEE)",
            primario="0x3DF704", secundario="0x3DF74C", paleta_da_fonte=6,
            autor="redriders180 (Glazed), revisao de Zel e Zeturic",
            prova="mapa 0/4 do hack: 0 pixel diferente de 716.800",
        ),
        paleta=[[0, 0, 0]] + [list(c) for c in cores],
        tiles=["".join("%x" % c for linha in t for c in linha) for t in tiles],
        pecas=pecas,
    )
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(kit, f, indent=1, ensure_ascii=False)
    print("kit gravado em %s: %d tiles, %d cores, %d pecas"
          % (saida, len(tiles), len(cores), len(pecas)))
    return kit


# -------------------------------------------------------------- instalacao
def tiles_em_uso():
    """Quantos tiles o tiles.png do Canalave tem hoje (o png é o teto real)."""
    from PIL import Image
    img = Image.open(f"{DESTINO}/tiles.png")
    W, H = img.size
    return (W // 8) * (H // 8), W // 8


def orcamento(kit, guardado=None):
    """A vaga onde o kit comeca. Ela e ESCOLHIDA uma vez e guardada no plano.

    Sem isso o script nao seria idempotente: depois da primeira gravacao o
    `tiles.png` cresce, e a segunda passada acharia outra vaga livre e
    instalaria o kit de novo, mais adiante. Medido em 06/09/2026, na primeira
    reaplicacao: a base pulou de 176 para 192.
    """
    guardado = guardado if guardado is not None else carrega_plano()
    n_tiles, cols = tiles_em_uso()
    base = guardado.get("kit", {}).get("base_tile", n_tiles)
    if base + len(kit["tiles"]) > TETO_TILES:
        raise SystemExit("o kit estoura o teto de %d tiles" % TETO_TILES)
    return base, cols


def grava_tileset(kit, base_tile):
    from PIL import Image
    antigo = Image.open(f"{DESTINO}/tiles.png")
    cols = antigo.size[0] // 8
    precisa = base_tile + len(kit["tiles"])
    linhas = (precisa + cols - 1) // cols
    novo = Image.new("P", (antigo.size[0], linhas * 8), 0)
    novo.putpalette(antigo.getpalette())
    novo.paste(antigo, (0, 0))
    px = novo.load()
    for i, hexa in enumerate(kit["tiles"]):
        vaga = base_tile + i
        x0, y0 = (vaga % cols) * 8, (vaga // cols) * 8
        for y in range(8):
            for x in range(8):
                px[x0 + x, y0 + y] = int(hexa[y * 8 + x], 16)
    novo.save(f"{DESTINO}/tiles.png")

    with open(f"{DESTINO}/palettes/%02d.pal" % PAL_NOVA, "w") as f:
        f.write("JASC-PAL\r\n0100\r\n16\r\n")
        for cor in kit["paleta"]:
            f.write("%d %d %d\r\n" % tuple(cor))


def grava_metatiles(novos, attrs):
    meta = bytearray(_le(f"{DESTINO}/metatiles.bin"))
    attr = bytearray(_le(f"{DESTINO}/metatile_attributes.bin"))
    for local, ent in novos.items():
        for i, valor in enumerate(ent):
            struct.pack_into("<H", meta, local * 16 + i * 2, valor)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    with open(f"{DESTINO}/metatiles.bin", "wb") as f:
        f.write(bytes(meta))
    with open(f"{DESTINO}/metatile_attributes.bin", "wb") as f:
        f.write(bytes(attr))


# ------------------------------------------------------------- passo do mapa
def agua_alcance(v, W, H, AG, beh):
    """Componente de água ligada às bordas do mapa: quem surfa chega."""
    molhada = {i for i in range(W * H)
               if not ((v[i] >> 10) & 3) and beh(v[i] & 0x3FF) in AG}
    ini = [i for i in molhada
           if i % W in (0, W - 1) or i // W in (0, H - 1)
           or any(0 <= (i % W) + dx < W and 0 <= (i // W) + dy < H
                  and ((i // W + dy) * W + (i % W) + dx) not in molhada
                  for dx, dy in N4)]
    vis, fila = set(ini), collections.deque(ini)
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


def _classifica(v, W, H, nosso, beh, AG, proibidas):
    """Devolve (muros, calcadas): listas de (x, y, direcao_da_agua)."""
    def agua_em(x, y):
        return 0 <= x < W and 0 <= y < H and beh(v[y * W + x] & 0x3FF) in AG

    muros, calcadas = [], []
    molhadas = [(x, y) for y in range(H) for x in range(W) if agua_em(x, y)]
    perto = set()
    for x, y in molhadas:
        for dx in range(-DIST_BOIA_AGUA, DIST_BOIA_AGUA + 1):
            for dy in range(-DIST_BOIA_AGUA, DIST_BOIA_AGUA + 1):
                if abs(dx) + abs(dy) <= DIST_BOIA_AGUA:
                    perto.add((x + dx, y + dy))
    for y in range(MARGEM, H - MARGEM):
        for x in range(MARGEM, W - MARGEM):
            if (x, y) in proibidas:
                continue
            w = v[y * W + x]
            mt, col = w & 0x3FF, (w >> 10) & 3
            b = beh(mt)
            if not nosso.sobreponivel(mt):
                continue
            vizinhas = [(dx, dy) for dx, dy in N4 if agua_em(x + dx, y + dy)]
            if col and b == 0 and vizinhas:
                muros.append((x, y, vizinhas[0]))
            elif not col and b == 0 and (x, y) in perto and not vizinhas:
                calcadas.append((x, y, None))
    return muros, calcadas


def _corridas(muros):
    """Agrupa as células de muro em corridas retas de mesma direção de água."""
    porto = {(x, y): d for x, y, d in muros}
    vistos, corridas = set(), []
    for x, y, d in sorted(muros):
        if (x, y) in vistos:
            continue
        passo = (1, 0) if d[1] else (0, 1)   # água ao norte/sul => muro deitado
        corrida = []
        cx, cy = x, y
        while (cx, cy) in porto and porto[(cx, cy)] == d and (cx, cy) not in vistos:
            corrida.append((cx, cy))
            vistos.add((cx, cy))
            cx, cy = cx + passo[0], cy + passo[1]
        corridas.append((d, passo, corrida))
    return corridas


def plano_mapa(nosso, base=None):
    """Escolhe a célula de cada peça. Não escreve nada."""
    d, L, W, H, v0 = G.grade(ALVO)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    _ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(ALVO, v, W, H, d)
    proibidas = set(gelo) | set(E.eventos(d))

    muros, calcadas = _classifica(v, W, H, nosso, beh, AG, proibidas)
    escolha = {}     # (x, y) -> nome da peca

    # 1. cabeços, por corrida de muro
    n = 0
    for _d, passo, corrida in sorted(_corridas(muros), key=lambda c: (-len(c[2]), c[2])):
        if n >= MAX_CABECOS:
            break
        if passo == (1, 0) and len(corrida) >= 3:
            # muro deitado: trio amarrado pelo cabo, no meio da corrida
            k = (len(corrida) - 3) // 2
            trio = corrida[k:k + 3]
            for cel, nome in zip(trio, ("cabeco cabo a direita", "cabeco cabo duplo",
                                        "cabeco cabo a esquerda")):
                escolha[cel] = nome
            n += 3
        elif passo == (0, 1) and len(corrida) >= PASSO_VERTICAL + 2:
            for k in range(1, len(corrida) - 1, PASSO_VERTICAL):
                if n >= MAX_CABECOS:
                    break
                escolha[corrida[k]] = "cabeco liso"
                n += 1

    # 2. boias na calçada, com espaçamento
    def espalha(lista, quantos, espaco, nome):
        postos = []
        ordem = sorted(lista, key=lambda c: (((c[1] * 2654435761 + c[0] * 40503)
                                              & 0xFFFF), c))
        for x, y, _ in ordem:
            if len(postos) >= quantos:
                break
            if (x, y) in escolha:
                continue
            if any(max(abs(x - px), abs(y - py)) < espaco for px, py in postos):
                continue
            if any(max(abs(x - px), abs(y - py)) < 2 for px, py in escolha):
                continue
            escolha[(x, y)] = nome
            postos.append((x, y))
        return len(postos)

    n_boias = espalha(calcadas, MAX_BOIAS, ESPACO_BOIA, "boia salva-vidas")
    contas = collections.Counter(escolha.values())
    return d, L, W, H, v, escolha, contas, dict(boias=n_boias)


def monta_metatiles(kit, nosso, v, W, escolha, base_tile, guardado=None):
    """(escritas, metatiles novos, atributos, vagas) a partir da escolha."""
    pares = sorted({(v[y * W + x] & 0x3FF, nome) for (x, y), nome in escolha.items()})
    if len(pares) + META_LOCAL_0 > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)
    usados = {c & 0x3FF for c in G.grade(ALVO)[4]}
    meta_can = _le(f"{DESTINO}/metatiles.bin")
    guardado = guardado if guardado is not None else carrega_plano()
    nossas_vagas = {int(k) for k in guardado.get("kit", {}).get("metatiles", {})}

    def enchimento(ent):
        return len(set(ent)) == 1 and ent[0] <= 2

    vaga, novos, attrs = {}, {}, {}
    local = META_LOCAL_0
    for chao, nome in pares:
        ent_chao = nosso.ent(chao)
        cima = []
        for entrada in kit["pecas"][nome]["cima"]:
            if entrada is None:      # quadrante vazio: o chao aparece inteiro
                cima.append(0)
                continue
            tile_local, hf, vf = entrada
            valor = (512 + base_tile + tile_local) | (PAL_NOVA << 12)
            if hf:
                valor |= 0x400
            if vf:
                valor |= 0x800
            cima.append(valor)
        antigo = entradas(meta_can, local)
        # a vaga serve se esta em branco de enchimento, se ja tem exatamente o
        # que este kit escreve, ou se ela e NOSSA (o plano guarda quais sao) e o
        # replanejamento so trocou a peca que mora nela.
        if not enchimento(antigo) and antigo != ent_chao[:4] + cima \
                and local not in nossas_vagas:
            raise SystemExit("vaga de metatile %d ja esta ocupada" % (512 + local))
        if (512 + local) in usados and enchimento(antigo):
            raise SystemExit("o mapa usa o metatile %d" % (512 + local))
        novos[local] = ent_chao[:4] + cima
        attrs[local] = nosso.attr(chao)      # behavior E layerType, inteiros
        vaga[(chao, nome)] = 512 + local
        local += 1

    escritas = {}
    for (x, y), nome in sorted(escolha.items()):
        i = y * W + x
        chao = v[i] & 0x3FF
        escritas[i] = (v[i] & 0xFC00) | vaga[(chao, nome)]
    return escritas, novos, attrs, vaga


# --------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def _outros_planos():
    saida = []
    for cam in (PLANO_PORTO, PLANO_ENFEITE):
        if os.path.exists(cam):
            saida.append(json.load(open(cam)))
    return saida


def base_de(guardado):
    """A grade sem NADA deste script (os outros dois planos ficam de pé).

    O `porto_canalave.py` e o `enfeita_cidades.py` desenham nesta mesma
    Canalave e rodam ANTES; este script planeja em cima do que eles deixaram,
    tirando só o que ele mesmo escreveu.
    """
    v = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(aplicar):
    kit = carrega_kit()
    nosso = Nosso()
    guardado = carrega_plano()
    base_tile, _cols = orcamento(kit, guardado)
    print("kit do cais: %d tiles novos (vagas %d a %d de %d), paleta %d, %d cores"
          % (len(kit["tiles"]), base_tile, base_tile + len(kit["tiles"]) - 1,
             TETO_TILES, PAL_NOVA, len(kit["paleta"]) - 1))
    d, L, W, H, v, escolha, contas, extra = plano_mapa(nosso, base_de(guardado))
    escritas, novos, attrs, vaga = monta_metatiles(kit, nosso, v, W, escolha,
                                                   base_tile, guardado)
    print("no mapa: " + ", ".join("%s x%d" % (k, n) for k, n in sorted(contas.items()))
          + " | %d celulas, %d metatiles novos (locais %d a %d)"
          % (len(escritas), len(novos), min(novos), max(novos)))
    if not aplicar:
        return escritas
    grava_tileset(kit, base_tile)
    grava_metatiles(novos, attrs)
    saida = list(G.grade(ALVO)[4])
    for idx, antigo, novo in guardado.get(ALVO, {}).get("celulas", []):
        if saida[idx] == novo:
            saida[idx] = antigo
    for i, val in escritas.items():
        saida[i] = val
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(saida), *saida))
    guardado[ALVO] = {"celulas": [[i, v[i], escritas[i]] for i in sorted(escritas)]}
    guardado["kit"] = {
        "base_tile": base_tile,
        "metatiles": {str(local): [chao, nome] for (chao, nome), gid in vaga.items()
                      for local in [gid - 512]},
    }
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("aplicado")
    return escritas


def desfaz():
    guardado = carrega_plano()
    if ALVO not in guardado:
        print("nada a desfazer")
        return 0
    _d, L, _W, _H, v = G.grade(ALVO)
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
    print("desfeitas %d celulas do cais" % n)
    return 0


# ------------------------------------------------------------------- conferes
def confere(v, saida, W, H, d, L, nosso, escritas, novos, attrs, kit):
    """A lista de reprovações. Vazia = passou."""
    mau = []
    beh_disco = G.comportamento(L["primary_tileset"], L["secondary_tileset"])

    def beh(mt):
        """Comportamento contando os metatiles novos, que ainda nao estao no disco."""
        if mt - 512 in attrs:
            return attrs[mt - 512] & 0x1FF
        return beh_disco(mt)

    AG = E.agua()

    # 1. bits 10 a 15 idênticos em TODAS as palavras
    difs = [i for i in range(len(v)) if (v[i] >> 10) != (saida[i] >> 10)]
    if difs:
        mau.append("bits 10-15 mudaram em %d celulas" % len(difs))

    # 2. (behavior, layerType) idêntico célula a célula, lido do attributes
    def attr_de(gid, attrs_novos):
        local = gid - 512
        if local in attrs_novos:
            return attrs_novos[local]
        return nosso.attr(gid)

    ruins = 0
    for i in range(len(v)):
        a, b = nosso.attr(v[i] & 0x3FF), attr_de(saida[i] & 0x3FF, attrs)
        if (a & 0x00FF, (a >> 12) & 0xF) != (b & 0x00FF, (b >> 12) & 0xF):
            ruins += 1
    if ruins:
        mau.append("(behavior, layerType) mudou em %d celulas" % ruins)

    # 3. nenhuma peça em cima de evento
    ev = set(E.eventos(d))
    for i in escritas:
        if (i % W, i // W) in ev:
            mau.append("escreveu no evento (%d,%d)" % (i % W, i // W))

    # 4. camada de baixo do metatile novo == camada de baixo do chão trocado
    for i, val in escritas.items():
        antigo, novo = v[i] & 0x3FF, val & 0x3FF
        if nosso.ent(antigo)[:4] != novos[novo - 512][:4]:
            mau.append("a camada de baixo mudou em (%d,%d)" % (i % W, i // W))

    # 5. os dois portões de alcance: aqui a exigência é igualdade pura
    ini = E.partidas(d, W, H, v)
    if E.alcance(v, W, H, ini) != E.alcance(saida, W, H, ini):
        mau.append("o alcance a pe mudou")
    if agua_alcance(v, W, H, AG, beh) != agua_alcance(saida, W, H, AG, beh):
        mau.append("o alcance por agua mudou")

    # 6. orçamento
    base_tile, _ = orcamento(kit)
    if base_tile + len(kit["tiles"]) > TETO_TILES:
        mau.append("estoura o teto de tiles")
    if max(novos) >= TETO_META:
        mau.append("estoura o teto de metatiles")
    if len(kit["paleta"]) != 16:
        mau.append("paleta do kit fora de 16 entradas")

    # 7. a vaga de paleta 12 nao pode ser usada por metatile que nao seja do kit
    meta_can = _le(f"{DESTINO}/metatiles.bin")
    for local in range(len(meta_can) // 16):
        if local in novos:
            continue
        for valor in entradas(meta_can, local):
            if ((valor >> 12) & 0xF) == PAL_NOVA and (512 + local) in {
                    c & 0x3FF for c in saida}:
                mau.append("a paleta %d ja e usada pelo metatile %d"
                           % (PAL_NOVA, 512 + local))
                break
    return mau


def _monta_tudo():
    kit = carrega_kit()
    nosso = Nosso()
    guardado = carrega_plano()
    base_tile, _ = orcamento(kit, guardado)
    base = base_de(guardado)
    d, L, W, H, v, escolha, contas, extra = plano_mapa(nosso, base)
    escritas, novos, attrs, vaga = monta_metatiles(kit, nosso, v, W, escolha,
                                                   base_tile, guardado)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    return dict(kit=kit, nosso=nosso, d=d, L=L, W=W, H=H, v=v, saida=saida,
                escritas=escritas, novos=novos, attrs=attrs, contas=contas,
                escolha=escolha, extra=extra, base_tile=base_tile)


def demo():
    t = _monta_tudo()
    mau = confere(t["v"], t["saida"], t["W"], t["H"], t["d"], t["L"], t["nosso"],
                  t["escritas"], t["novos"], t["attrs"], t["kit"])
    if sum(t["contas"].values()) < 12:
        mau.append("so %d pecas no cais" % sum(t["contas"].values()))
    # idempotencia
    _d, _L, _W, _H, v2, escolha2, _c, _e = plano_mapa(t["nosso"], list(t["v"]))
    if escolha2 != t["escolha"]:
        mau.append("segunda passada deu plano diferente")
    if mau:
        print("DEMO VERMELHA")
        for x in mau:
            print("  -", x)
        return 1
    print("DEMO VERDE: %d tiles, %d metatiles, %d pecas, %d celulas, 7 conferes"
          % (len(t["kit"]["tiles"]), len(t["novos"]), sum(t["contas"].values()),
             len(t["escritas"])))
    return 0


def autoteste():
    """A suíte cheia, com a prova NEGATIVA no fim."""
    falhas = []
    t = _monta_tudo()
    mau = confere(t["v"], t["saida"], t["W"], t["H"], t["d"], t["L"], t["nosso"],
                  t["escritas"], t["novos"], t["attrs"], t["kit"])
    print("1. conferes no plano de verdade: %s"
          % ("VERDE" if not mau else "VERMELHO %s" % mau))
    if mau:
        falhas.append("plano de verdade reprovou")

    # peca em chao errado
    ruim = 0
    beh = G.comportamento(t["L"]["primary_tileset"], t["L"]["secondary_tileset"])
    AG = E.agua()
    for (x, y), nome in t["escolha"].items():
        w = t["v"][y * t["W"] + x]
        chao = t["kit"]["pecas"][nome]["chao"]
        molhado, solido = beh(w & 0x3FF) in AG, bool((w >> 10) & 3)
        if chao == "agua" and not molhado:
            ruim += 1
        if chao == "muro" and not solido:
            ruim += 1
        if chao == "calcada" and (solido or molhado):
            ruim += 1
    print("2. peca no chao certo: %s" % ("VERDE" if not ruim else "VERMELHO %d" % ruim))
    if ruim:
        falhas.append("peca em chao errado")

    # idempotencia e desfazer
    base2 = list(t["saida"])
    for i in t["escritas"]:
        if base2[i] == t["escritas"][i]:
            base2[i] = t["v"][i]
    ok_desfaz = base2 == list(t["v"])
    _d, _L, _W, _H, _v, escolha2, _c, _e = plano_mapa(t["nosso"], base2)
    print("3. desfazer devolve a base: %s | segunda passada igual: %s"
          % ("VERDE" if ok_desfaz else "VERMELHO",
             "VERDE" if escolha2 == t["escolha"] else "VERMELHO"))
    if not ok_desfaz or escolha2 != t["escolha"]:
        falhas.append("nao e idempotente")

    # PROVA NEGATIVA 1: sabotar a colisao de uma celula escrita
    i0 = sorted(t["escritas"])[0]
    sab = list(t["saida"])
    sab[i0] ^= 0x0400
    m = confere(t["v"], sab, t["W"], t["H"], t["d"], t["L"], t["nosso"],
                t["escritas"], t["novos"], t["attrs"], t["kit"])
    print("4. prova negativa (colisao sabotada): %s"
          % ("ACUSOU: %s" % m[0] if m else "NAO ACUSOU"))
    if not m:
        falhas.append("a conferencia nao acusou colisao sabotada")

    # PROVA NEGATIVA 2: sabotar o atributo de um metatile novo
    attrs_sab = dict(t["attrs"])
    alvo = sorted(attrs_sab)[0]
    attrs_sab[alvo] = (attrs_sab[alvo] & 0xFF00) | 0x2A
    m = confere(t["v"], t["saida"], t["W"], t["H"], t["d"], t["L"], t["nosso"],
                t["escritas"], t["novos"], attrs_sab, t["kit"])
    print("5. prova negativa (behavior sabotado): %s"
          % ("ACUSOU: %s" % m[0] if m else "NAO ACUSOU"))
    if not m:
        falhas.append("a conferencia nao acusou behavior sabotado")

    # PROVA NEGATIVA 3: sabotar a camada de baixo de um metatile novo
    novos_sab = {k: list(vv) for k, vv in t["novos"].items()}
    novos_sab[alvo][0] ^= 1
    m = confere(t["v"], t["saida"], t["W"], t["H"], t["d"], t["L"], t["nosso"],
                t["escritas"], novos_sab, t["attrs"], t["kit"])
    print("6. prova negativa (camada de baixo sabotada): %s"
          % ("ACUSOU: %s" % m[0] if m else "NAO ACUSOU"))
    if not m:
        falhas.append("a conferencia nao acusou camada de baixo sabotada")

    if falhas:
        print("AUTOTESTE VERMELHO")
        for f in falhas:
            print("  -", f)
        return 1
    print("AUTOTESTE VERDE: 6 blocos, %d pecas, %d celulas"
          % (sum(t["contas"].values()), len(t["escritas"])))
    return 0


def main():
    if "--extrair" in sys.argv:
        constroi_kit(sys.argv[sys.argv.index("--extrair") + 1])
        return 0
    if "--demo" in sys.argv:
        return demo()
    if "--autoteste" in sys.argv:
        return autoteste()
    if "--desfazer" in sys.argv:
        return desfaz()
    roda("--aplicar" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
