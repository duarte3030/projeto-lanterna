#!/usr/bin/env python3
"""Conserta as passarelas elevadas de Sunyshore: o cruzamento deixa de ser um
buraco de sete tiles no corrimão e vira um portão de dois, e nenhuma célula que
o jogador de chão pisa desenha mais no BG1 (a camada que come o sprite).

O DEFEITO, medido antes de tocar em nada (05/09/2026, ROM
`roms/pokemon-claude-2026-09-05.gba`, layout `LAYOUT_SUNYSHORE_CITY`, 70x64):

- `data/layouts/SunyshoreCity/map.bin` tem 68 células com elevação 15
  (`ELEVATION_MULTI_LEVEL`), todas andáveis. Elas são o idioma de PONTE do
  Emerald: `IsElevationMismatchAt` devolve FALSE quando a célula do mapa vale 15,
  então quem anda no chão (elevação 3) e quem anda na passarela (elevação 4)
  passam pelos MESMOS tiles, e `ObjectEventUpdateElevation` sai cedo sem mexer em
  `previousElevation`, ou seja cada um continua com a elevação que trouxe.
- 35 dessas 68 usam metatile de CORRIMÃO (528, 529, 542, 543, 556, 557, 559,
  566, 568), que tem camada de cima cheia e `layer_type` NORMAL. Em
  `DrawMetatile` (src/field_camera.c:287) a camada de cima de um metatile NORMAL
  vai para o BG1, que tem prioridade 1 (`sOverworldBgTemplates`, src/overworld.c:312).
  Quem está com elevação 3 recebe `sElevationToPriority[3] == 2`
  (src/event_object_movement.c:10036), e sprite de prioridade 2 fica ATRÁS do BG1.
  Resultado medido no emulador: em (28,13) e em (25,32) só a ponta do boné do
  jogador aparece; o corpo inteiro some atrás do corrimão.
- As outras 33 usam o metatile 562, o piso liso da passarela, cuja camada de cima
  é o tile 1 (vazio). Ali o jogador de chão aparece INTEIRO, de pé em cima da
  passarela. É a mistura das duas coisas que o Gui viu: ele sobe no piso da
  passarela vindo do chão, some em duas linhas e reaparece em outras duas.
- A passarela de verdade (elevação 4, 455 células) NUNCA foi invadida: uma
  varredura de alcance fiel ao motor (estado = x, y, currentElevation,
  previousElevation) achou ZERO células de elevação 4 pisáveis com elevação
  diferente de 4. As três únicas subidas são as ilhas de elevação 0 em
  (42..45, 20..23), (56..58, 32..35) e (14..17, 38..41), que são as escadas
  desenhadas na arte. Ou seja: o "subir sem escada" que o Gui relatou é subir no
  CRUZAMENTO, não na passarela.

O CONSERTO, uma regra só, aplicada a cada região conexa de elevação 15:

  1. Descobrir o PORTÃO: as colunas (ou linhas) em que chão andável de elevação 3
     encosta na região dos DOIS lados opostos. É por elas que a rua de baixo
     precisa passar. Guardar as 2 do meio (ou todas, se já forem 3 ou
     menos), mais toda coluna que tenha
     object_event dentro da região (o Rival de (26,10) é uma delas, e selar a
     célula dele o deixaria de pé em cima de uma parede).
  2. Fora do portão: célula de piso (metatile que não cobre) vira ELEVAÇÃO 4,
     isto é passa a ser só passarela; célula de corrimão (metatile que cobre)
     vira PAREDE (colisão 1, elevação 0), que é exatamente o que as vizinhas de
     fora da região já são.
  3. Dentro do portão: mantém elevação 15 (é o cruzamento de verdade) e o
     metatile de corrimão é trocado pelo piso liso da própria região, de forma
     que o corrimão ABRE onde a rua cruza e ninguém mais fica encoberto.

Regiões que a regra encontra sozinha em Sunyshore (nada é coordenada cravada):

  | região | células | portão |
  |---|---|---|
  | (25..31, 10..13) | 28 | colunas 26, 27 e 28 (a 26 por causa do Rival) |
  | (21..28, 32..35) | 22 | colunas 27 e 28 |
  | (23..24, 42..45) + (25..34, 45) | 18 | nenhum (não há chão dos dois lados) |

POR QUE NÃO SELAR O CRUZAMENTO INTEIRO: medido. Trocar as 68 células de
elevação 15 por elevação 4 corta a rua de chão em dois e deixa INALCANÇÁVEIS o
Pokécenter (warp 2), a criadora de (26,43) e a Jasmine de (29,4). Os dois
cruzamentos do norte são o único caminho a pé entre a praia, a praça e o
Pokécenter. Por isso o portão fica, com dois tiles em vez de sete.

POR QUE SÓ SUNYSHORE: os outros mapas de Sinnoh com elevação 15 que cobre foram
medidos e são o idioma normal do Emerald, não o defeito. Route 205 South tem 15
células, todas cobrindo, numa ponte de 3 tiles de largura sobre um caminho de
chão; Route 216 tem 24, todas cobrindo, em três pontes de 2 tiles; Route 212
South tem 6, nenhuma encostando em chão de elevação 3; Route 206 tem 271, NENHUMA
cobrindo. O Emerald de fábrica faz igual: Route 110 (a Cycling Road) tem 185
células de elevação 15 e as 185 cobrem. O que faz Sunyshore ser defeito é ser a
única MISTURADA (35 cobrem, 33 não) e larga o bastante (sete tiles) para parecer
que se subiu na passarela.

Uso:
    python3 dev_scripts/conserta_passarelas_sinnoh.py --demo     # mede e prova
    python3 dev_scripts/conserta_passarelas_sinnoh.py --aplica   # grava o map.bin

É idempotente: rodar duas vezes com --aplica muda 0 células na segunda.
"""

import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAYOUT = "LAYOUT_SUNYSHORE_CITY"

ELEV_TRANSICAO = 0
ELEV_CHAO = 3
ELEV_PASSARELA = 4
ELEV_MULTINIVEL = 15

# Comportamentos de água do pokeemerald: quem anda a pé não pisa neles.
AGUA = set(range(0x10, 0x21))


# ------------------------------------------------------------------ leitura

def carrega_layout(nome=LAYOUT):
    with open(os.path.join(RAIZ, "data/layouts/layouts.json"), encoding="utf-8") as f:
        for l in json.load(f)["layouts"]:
            if l["id"] == nome:
                return l
    raise SystemExit(f"layout {nome} não existe em data/layouts/layouts.json")


def pastas_de_tileset():
    """{rotulo_gTileset: pasta}, lido do INCBIN/INCGFX, nunca deduzido do nome."""
    import re
    texto = ""
    for arq in ("src/data/tilesets/graphics.h", "src/graphics.c"):
        texto += open(os.path.join(RAIZ, arq), encoding="utf-8").read()
    padrao = re.compile(
        r'gTilesetTiles_([A-Za-z0-9]+)\[\] = INC(?:BIN|GFX)_U32\('
        r'"(data/tilesets/(?:primary|secondary)/[a-z0-9_/]+?)/tiles')
    return {"gTileset_" + m.group(1): m.group(2) for m in padrao.finditer(texto)}


class Tilesets:
    """Atributos e metatiles do par primário+secundário de um layout."""

    def __init__(self, layout):
        pastas = pastas_de_tileset()
        self.attr, self.mt = [], []
        for chave in ("primary_tileset", "secondary_tileset"):
            p = os.path.join(RAIZ, pastas[layout[chave]])
            bruto = open(os.path.join(p, "metatile_attributes.bin"), "rb").read()
            self.attr.append(struct.unpack(f"<{len(bruto) // 2}H", bruto))
            self.mt.append(open(os.path.join(p, "metatiles.bin"), "rb").read())

    def atributo(self, m):
        i, tab = (0, m) if m < 512 else (1, m - 512)
        return self.attr[i][tab] if tab < len(self.attr[i]) else 0

    def comportamento(self, m):
        return self.atributo(m) & 0xFF

    def camada(self, m):
        return (self.atributo(m) >> 12) & 0xF

    def tiles(self, m):
        i, tab = (0, m) if m < 512 else (1, m - 512)
        b = self.mt[i][tab * 16:tab * 16 + 16]
        return struct.unpack("<8H", b) if len(b) == 16 else (0,) * 8

    def cobre(self, m):
        """O metatile desenha no BG1 e por isso passa NA FRENTE de sprite de
        prioridade 2. Só METATILE_LAYER_TYPE_NORMAL manda a camada de cima para o
        BG1; COVERED manda para o BG2 (prioridade 2, e sprite ganha empate) e
        SPLIT também usa o BG1, mas nenhum metatile de Sunyshore é SPLIT."""
        if self.camada(m) != 0:
            return False
        return any((t & 0x3FF) > 1 for t in self.tiles(m)[4:])


class Grade:
    def __init__(self, layout):
        self.w, self.h = layout["width"], layout["height"]
        self.caminho = os.path.join(RAIZ, layout["blockdata_filepath"])
        bruto = open(self.caminho, "rb").read()
        esperado = self.w * self.h * 2
        if len(bruto) != esperado:
            raise SystemExit(f"{self.caminho}: {len(bruto)} bytes, esperava {esperado}")
        self.dados = list(struct.unpack(f"<{self.w * self.h}H", bruto))

    def __getitem__(self, xy):
        x, y = xy
        return self.dados[y * self.w + x]

    def __setitem__(self, xy, v):
        x, y = xy
        self.dados[y * self.w + x] = v

    def dentro(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def grava(self):
        open(self.caminho, "wb").write(struct.pack(f"<{self.w * self.h}H", *self.dados))


def metatile(v):
    return v & 0x03FF


def colisao(v):
    return (v >> 10) & 3


def elevacao(v):
    return (v >> 12) & 0xF


def bloco(m, c, e):
    return (m & 0x3FF) | ((c & 3) << 10) | ((e & 0xF) << 12)


# ------------------------------------------------------------------- regra

def andavel(g, ts, x, y):
    v = g[x, y]
    return colisao(v) == 0 and ts.comportamento(metatile(v)) not in AGUA


def regioes_multinivel(g, ts):
    """Componentes conexos (4 vizinhos) de célula andável com elevação 15."""
    alvo = {(x, y) for y in range(g.h) for x in range(g.w)
            if elevacao(g[x, y]) == ELEV_MULTINIVEL and andavel(g, ts, x, y)}
    saida, vistos = [], set()
    for c in sorted(alvo):
        if c in vistos:
            continue
        fila, comp = [c], []
        vistos.add(c)
        while fila:
            x, y = fila.pop()
            comp.append((x, y))
            for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                n = (x + dx, y + dy)
                if n in alvo and n not in vistos:
                    vistos.add(n)
                    fila.append(n)
        saida.append(sorted(comp))
    return saida


def _chao(g, ts, x, y):
    return (g.dentro(x, y) and elevacao(g[x, y]) == ELEV_CHAO
            and andavel(g, ts, x, y))


def celulas_de_objeto():
    """{(x, y)} de todo object_event de Sunyshore.

    Existe por um caso real: `LOCALID_SUNYSHORE_RIVAL` mora em (26,10), que é
    célula de corrimão DENTRO do cruzamento norte. Selar aquela célula deixaria o
    Rival da cena da oitava insígnia de pé em cima de uma parede, e
    `valida_mapas_sinnoh.py` chama isso de objeto enterrado. Toda coluna com
    objeto entra no portão em vez de virar parede.
    """
    mapa = json.load(open(os.path.join(RAIZ, "data/maps/SunyshoreCity/map.json"),
                          encoding="utf-8"))
    return {(o["x"], o["y"]) for o in mapa["object_events"]}


def portao(g, ts, comp):
    """As linhas por onde a rua de chão atravessa a região, e nada além.

    São as 2 colunas (ou linhas) centrais em que chão andável de elevação 3
    encosta na região dos DOIS lados opostos, mais qualquer coluna que tenha
    object_event dentro da região.

    Devolve ('coluna', {x, ...}) ou ('linha', {y, ...}) ou (None, set()) quando
    não há chão encostando dos dois lados opostos, caso em que a região inteira é
    passarela e nenhum portão precisa existir.
    """
    por_coluna = collections.defaultdict(list)
    por_linha = collections.defaultdict(list)
    for x, y in comp:
        por_coluna[x].append(y)
        por_linha[y].append(x)

    colunas = sorted(x for x, ys in por_coluna.items()
                     if _chao(g, ts, x, min(ys) - 1) and _chao(g, ts, x, max(ys) + 1))
    linhas = sorted(y for y, xs in por_linha.items()
                    if _chao(g, ts, min(xs) - 1, y) and _chao(g, ts, max(xs) + 1, y))

    objetos = celulas_de_objeto()
    # Uma região atravessa em UM sentido só; o que tiver mais candidatos manda.
    if len(colunas) >= len(linhas) and colunas:
        aberto = set(_linhas_do_portao(colunas))
        aberto |= {x for x, y in comp if (x, y) in objetos}
        return "coluna", aberto
    if linhas:
        aberto = set(_linhas_do_portao(linhas))
        aberto |= {y for x, y in comp if (x, y) in objetos}
        return "linha", aberto
    return None, set()


def _linhas_do_portao(valores):
    """As 2 do meio, e a lista inteira quando ela já é estreita.

    O `<= 3` é o que torna a regra um ponto fixo: depois de aplicada, a região
    que sobra É o portão, e uma segunda passada sobre ela tem que devolver ela
    mesma. Sem esse corte, um portão de 3 colunas (o caso do cruzamento norte,
    que carrega a coluna do Rival) perderia uma coluna a cada nova passada.
    """
    if len(valores) <= 3:
        return list(valores)
    meio = len(valores) // 2
    return valores[meio - 1:meio + 1]


def piso_da_regiao(g, ts, comp):
    """O metatile de PISO da região: o mais comum entre os que não cobrem."""
    c = collections.Counter(metatile(g[x, y]) for x, y in comp
                            if not ts.cobre(metatile(g[x, y])))
    if not c:
        return None
    return c.most_common(1)[0][0]


def planeja(g, ts):
    """Lista de (x, y, bloco_novo, motivo). Não escreve nada."""
    mudancas = []
    for comp in regioes_multinivel(g, ts):
        sentido, aberto = portao(g, ts, comp)
        piso = piso_da_regiao(g, ts, comp)
        for x, y in comp:
            v = g[x, y]
            m = metatile(v)
            no_portao = (sentido == "coluna" and x in aberto) or \
                        (sentido == "linha" and y in aberto)
            if no_portao:
                if ts.cobre(m):
                    if piso is None:
                        raise SystemExit(f"({x},{y}): região sem metatile de piso")
                    novo = bloco(piso, 0, ELEV_MULTINIVEL)
                    motivo = f"portão: corrimão {m} vira piso {piso}"
                else:
                    continue
            elif ts.cobre(m):
                novo = bloco(m, 1, ELEV_TRANSICAO)
                motivo = "fora do portão: corrimão vira parede"
            else:
                novo = bloco(m, 0, ELEV_PASSARELA)
                motivo = "fora do portão: piso vira só passarela (elevação 4)"
            if novo != v:
                mudancas.append((x, y, novo, motivo))
    return mudancas


# ------------------------------------------------------------- verificação

def alcance(g, ts, sx, sy):
    """Varredura fiel ao motor. Estado = (x, y, currentElevation, previousElevation).

    Copiada de GetVanillaCollision + IsElevationMismatchAt + ObjectEventUpdateElevation.
    Devolve {(x, y): {previousElevation possíveis}}.
    """
    e0 = elevacao(g[sx, sy])
    if e0 == ELEV_MULTINIVEL:
        e0 = ELEV_CHAO
    inicio = (sx, sy, e0, e0)
    fila, vistos, tiles = collections.deque([inicio]), {inicio}, {}
    while fila:
        x, y, cur, prev = fila.popleft()
        tiles.setdefault((x, y), set()).add(prev)
        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            nx, ny = x + dx, y + dy
            if not g.dentro(nx, ny) or not andavel(g, ts, nx, ny):
                continue
            ce = elevacao(g[nx, ny])
            if cur != ELEV_TRANSICAO and ce not in (ELEV_TRANSICAO, ELEV_MULTINIVEL) \
                    and ce != cur:
                continue  # IsElevationMismatchAt
            if ce == ELEV_MULTINIVEL or elevacao(g[x, y]) == ELEV_MULTINIVEL:
                ncur, nprev = cur, prev
            else:
                ncur = ce
                nprev = ce if ce not in (ELEV_TRANSICAO, ELEV_MULTINIVEL) else prev
            novo = (nx, ny, ncur, nprev)
            if novo not in vistos:
                vistos.add(novo)
                fila.append(novo)
    return tiles


def pousadas(g, ts, x, y):
    r = []
    for dx, dy in ((0, 0), (0, 1), (0, -1), (-1, 0), (1, 0)):
        if g.dentro(x + dx, y + dy) and andavel(g, ts, x + dx, y + dy):
            r.append((x + dx, y + dy))
    return r


def censo_alcance(g, ts, layout_nome=LAYOUT):
    """{nome do warp/objeto: alcançável a pé desde a entrada da Route 222}."""
    mapa = json.load(open(os.path.join(RAIZ, "data/maps/SunyshoreCity/map.json"),
                          encoding="utf-8"))
    entrada = pousadas(g, ts, mapa["warp_events"][0]["x"], mapa["warp_events"][0]["y"])
    t = alcance(g, ts, *entrada[0])
    saida = {}
    for i, w in enumerate(mapa["warp_events"]):
        saida[f"warp {i} -> {w['dest_map']}"] = any(
            p in t for p in pousadas(g, ts, w["x"], w["y"]))
    for i, o in enumerate(mapa["object_events"]):
        nome = o.get("local_id") or o.get("graphics_id")
        saida[f"objeto {i} {nome} ({o['x']},{o['y']})"] = any(
            p in t for p in pousadas(g, ts, o["x"], o["y"]))
    return saida, len(t)


def celulas_que_comem_sprite(g, ts):
    """Célula de elevação 15 andável cujo PRÓPRIO metatile desenha no BG1.

    É o defeito exato e a régua é estreita de propósito. Elevação 15 é a única
    em que o motor deixa DOIS andarilhos de elevações diferentes pisarem no
    mesmo tile: o de elevação 4 recebe `sElevationToPriority[4] == 1` e passa na
    frente do BG1, o de elevação 3 recebe 2 e some atrás dele. Metatile que cobre
    num tile desses come metade dos que passam ali, e é isso que o Gui viu.

    Metatile que cobre em chão de elevação 3 comum NÃO entra: é o idioma normal
    do Emerald (a parte de cima do muro desenhada por cima de quem anda na frente
    dele) e Sunyshore tem 84 células assim que não são defeito nenhum.
    """
    r = []
    for y in range(g.h):
        for x in range(g.w):
            v = g[x, y]
            if elevacao(v) != ELEV_MULTINIVEL or not andavel(g, ts, x, y):
                continue
            if ts.cobre(metatile(v)):
                r.append((x, y, metatile(v)))
    return r


# ------------------------------------------------------------------- main

def relatorio(g, ts, titulo):
    comps = regioes_multinivel(g, ts)
    comem = celulas_que_comem_sprite(g, ts)
    censo, n = censo_alcance(g, ts)
    print(f"--- {titulo}")
    print(f"    regiões de elevação 15: {len(comps)}, "
          f"{sum(len(c) for c in comps)} células")
    for c in comps:
        xs = [p[0] for p in c]
        ys = [p[1] for p in c]
        print(f"      x {min(xs)}..{max(xs)}  y {min(ys)}..{max(ys)}  ({len(c)} células)")
    print(f"    células de elevação 15 que COMEM o sprite: {len(comem)}")
    print(f"    tiles alcançáveis a pé desde a Route 222: {n}")
    return censo, comem


def main():
    args = sys.argv[1:]
    aplica = "--aplica" in args
    demo = "--demo" in args or not aplica
    layout = carrega_layout()
    ts = Tilesets(layout)
    g = Grade(layout)

    censo_antes, comem_antes = relatorio(g, ts, "ANTES")
    mudancas = planeja(g, ts)
    print(f"\n{len(mudancas)} células a mudar:")
    por_motivo = collections.Counter(m[3] for m in mudancas)
    for motivo, n in sorted(por_motivo.items()):
        print(f"    {n:3d}  {motivo}")

    for x, y, novo, _ in mudancas:
        g[x, y] = novo
    censo_depois, comem_depois = relatorio(g, ts, "DEPOIS")

    enterrados = [(x, y) for x, y in sorted(celulas_de_objeto())
                  if colisao(g[x, y])]
    ruim = False
    if enterrados:
        print(f"\nVERMELHO: {len(enterrados)} object_event ficaram em cima de "
              f"tile impassável: {enterrados}")
        ruim = True
    if comem_depois:
        print(f"\nVERMELHO: ainda sobraram {len(comem_depois)} células de "
              f"elevação 15 que comem o sprite: {comem_depois[:10]}")
        ruim = True
    perdidos = [k for k, v in censo_antes.items() if v and not censo_depois.get(k)]
    if perdidos:
        print("\nVERMELHO: ficaram INALCANÇÁVEIS:")
        for k in perdidos:
            print("    " + k)
        ruim = True
    if not planeja(g, ts) == []:
        print("\nVERMELHO: não é idempotente, a segunda passada ainda muda células")
        ruim = True
    if not ruim:
        print("\nVERDE: nenhuma célula come sprite, nenhum objeto ficou enterrado, "
              "nada ficou inalcançável, e a segunda passada muda 0 células.")

    if aplica and not ruim:
        g.grava()
        print(f"gravado: {g.caminho}")
    elif aplica:
        raise SystemExit("não gravei nada, o autoteste está vermelho")
    return 1 if ruim else 0


if __name__ == "__main__":
    sys.exit(main())
