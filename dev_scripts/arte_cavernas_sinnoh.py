#!/usr/bin/env python3
"""Decora as cavernas pobres de Sinnoh escrevendo SÓ o id de metatile do `map.bin`.

    python3 dev_scripts/arte_cavernas_sinnoh.py --lista     # mede e lista os alvos
    python3 dev_scripts/arte_cavernas_sinnoh.py --dry-run   # arte antes/depois, não escreve
    python3 dev_scripts/arte_cavernas_sinnoh.py --aplicar   # escreve os map.bin
    python3 dev_scripts/arte_cavernas_sinnoh.py --demo      # auto-teste

O problema
----------
O `converte_cavernas_sinnoh.py` traduziu a geometria de verdade das cavernas do
Platinum, e traduziu bem: o labirinto está no lugar. Mas o cabeçalho dele diz
por quê o desenho é pobre, e diz com todas as letras: **"a geometria de uma
caverna É a colisão dela"**. A grade do DS só tem cheio e vazio, então o script
podia escolher entre exatamente sete metatiles (chão 513, rocha 753/761 mais as
quatro pontas 752/754/760/762, saída 519 e escada 575) e as 70 cavernas saíram
com 6 a 9 metatiles distintos, contra o piso 10 da régua do `completude.py`.
Isso não é caverna, é máscara de colisão pintada de cinza.

O que este script faz, e por que não pode quebrar nada
------------------------------------------------------
Vale palavra por palavra a mecânica da 0.j (`arte_ginasios_sinnoh.py`), com uma
regra a mais que a caverna obriga:

1. A célula do `map.bin` é um u16: **10 bits de baixo são o METATILE** e os 6 de
   cima são COLISÃO e ELEVAÇÃO. Só se escreve `(antigo & 0xFC00) | novo`, então
   colisão e elevação saem byte a byte idênticas, e `confere()` prova isso
   célula a célula contra o `git show HEAD:`.
2. **O COMPORTAMENTO do metatile novo tem que ser IGUAL ao do velho**, e não
   apenas `MB_NORMAL` como nos ginásios. Aqui isso é obrigatório e não opcional:
   o chão de caverna é `MB_CAVE` (8), e a regra dos ginásios ("só entra célula
   com comportamento 0") congelaria o chão inteiro das 70 cavernas. A tabela de
   aprendizado é INDEXADA pelo comportamento, então a substituição só pode
   trocar chão de caverna por chão de caverna, rocha-8 por rocha-8, rocha-0 por
   rocha-0 e água por água. Encontro selvagem, corrida, pisada e surf continuam
   o que eram porque o comportamento continua o que era.
3. Comportamento fora da lista branca `BEH_DECORAVEL` nem é olhado. Saída de
   caverna (101), escada (97), buraco, esteira e afins ficam congelados mesmo
   que houvesse metatile do mesmo comportamento para trocar: o preço de errar
   uma escada é o jogador não sair do andar.
4. Célula com evento (objeto, warp, placa, gatilho) **e os 4 vizinhos ortogonais
   dela** ficam congelados. Os vizinhos entram porque um NPC anda, e porque
   enfeite colado na boca do warp esconde a saída.
5. Nenhum `map.json`, script, tileset ou `flags.h` é lido para escrita. Só
   `map.bin`.

De onde vem o vocabulário
-------------------------
De mapa de caverna que JÁ EXISTE no repo e que já foi desenhado à mão, nunca de
invenção de id. São duas famílias de fonte, e a diferença entre elas é medida,
não suposta:

- **Sinnoh** (`FONTES_SINNOH`): os mapas ricos que usam EXATAMENTE o mesmo par
  de tilesets do alvo (`gTileset_GeneralSinnoh` + `gTileset_CaveSinnoh`). São
  42, 38, 36, 33, 22 e 18 metatiles distintos, e é deles que sai a rocha de
  Sinnoh com face, quina, veio e cristal (os 26 metatiles 926..951 que o
  `cave_sinnoh` tem a mais que o `cave` de Hoenn). Aqui não há filtro nenhum a
  aplicar: mesmo tileset, mesmo id, mesmo pixel, mesmo atributo.
- **Hoenn** (`FONTES_HOENN`): Granite Cave e Victory Road, que usam
  `gTileset_General` + `gTileset_Cave`. **Medido, e é o que torna isto legal:**
  o `cave_sinnoh` é o `cave` com 26 metatiles no fim e SÓ DOIS mudados no meio
  (índices 407 e 410, ou seja os ids 919 e 922). Os outros 412 são byte a byte
  iguais, atributo incluído. O PRIMÁRIO é que diverge muito
  (`general_sinnoh` bate com `general` em só 242 dos 512).
  Por isso existe `ids_seguros()`, que só aceita da fonte de Hoenn o id cujos
  16 bytes de metatile E os 2 bytes de atributo são IDÊNTICOS nos dois pares de
  tileset. Sem esse filtro, um id de primário aprendido em Granite Cave
  desenharia outra coisa em Sinnoh, calado, e a régua de arte subiria mentindo.

Os dois passos do desenho são os da 0.j, com a chave estendida:

- PASSO ESTRUTURAL: para cada célula, a assinatura de vizinhança de parede (8
  vizinhos, fora do mapa conta como parede) mais a colisão e o COMPORTAMENTO
  escolhem o metatile que o artista usou na mesma situação na fonte. É o que dá
  face de rocha, quina, topo e canto em vez de mancha chapada.
- PASSO DE ENFEITE: os grupos de metatile RAROS da fonte (estalagmite, pedra
  solta, veio de cristal, poça) são recortados com a máscara de colisão E de
  comportamento e carimbados onde a máscara casa exata, espaçados e longe de
  evento.

Herdados da 0.j porque cada um nasceu de um defeito visto na imagem: ALCANCE (só
se aprende de célula alcançável a partir dos warps, mais a orla), RARIDADE
(`KMIN`: estrutural só usa metatile com 3+ ocorrências) e VAZIO (metatile que
renderiza mais de 40% na cor de fundo não entra no passo estrutural, senão o
"lado de fora" da fonte vira buraco no alvo).

Tudo, alvo e fonte, é lido do `git show HEAD:`, e não da árvore de trabalho.
Duas razões: (a) a rodada tem sete executores em paralelo e dois dos mapas-fonte
(`MtCoronet_1F_South`, `RavagedPath`) são a lista de OUTRO executor, então ler a
árvore faria o meu resultado depender da hora em que ele gravou; (b) é o que
torna o script IDEMPOTENTE de graça, porque a segunda passada lê a mesma
entrada da primeira. O `--demo` prova as duas coisas.
"""
import collections
import json
import os
import struct
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import arte_ginasios_sinnoh as G  # noqa: E402

SAIDA_IMG = ("/private/tmp/claude-501/-Users-duarte-Documents-CLAUDE-Claude-"
             "Workspace---Pokemon-Rom-Hacks/f2d3f86f-72f4-40e8-af0e-0982ef81d8ec"
             "/scratchpad/arte/sinnoh-cavernas")

# Mapas de caverna de Sinnoh que são lista de OUTRO executor nesta rodada.
EXCLUIDOS = {
    "RavagedPath", "OreburghGate_1F", "OreburghGateB1F", "MtCoronet_1F_South",
    "MtCoronet_B1F", "MtCoronetOutsideNorth", "MtCoronetOutsideSouth",
    "IronIsland", "Route204North", "DistortionWorld",
}

# Gerado por `--lista` (completude.arte() + tileset lido do map.json + exclusões
# + nenhum layout com mtime de hoje). Fica LITERAL de propósito: depois de
# `--aplicar` estes mapas deixam de ser pobres, e uma lista recalculada na hora
# ficaria vazia na segunda passada, o que faria a idempotência passar por
# acidente em vez de por mérito.
ALVOS = [
    "AcuityCavern", "IcebergRuins", "IronIsland1F", "IronIslandB1FLeftRoom",
    "IronIslandB1FRightRoom", "IronIslandB2FLeftRoom", "IronIslandB2FRightRoom",
    "IronIslandB3F", "IronIslandIronRuins", "IronRuins",
    # OS TRES LAGOS SAIRAM DAQUI EM 22/08/2026, e o motivo e de ORDEM, nao de
    # gosto: `dev_scripts/lagos_sinnoh.py` REFEZ a geometria de
    # LakeVerityLowWater, LakeAcuityLowWater e LakeValorDrained a partir da
    # grade do Platinum, e este gerador le a linha de base do `git show HEAD:`
    # (ver o cabecalho: e o que faz o autoteste dele valer). Enquanto a
    # conversao nao estiver commitada, decorar aqui REESCREVE o map.bin com o
    # mapa velho e desfaz a conversao: medido no dia, 867 tiles voltavam a ter a
    # colisao antiga e o jogador voltava a ficar presente na boca (alcance a pe
    # caiu de 662 para 2 no LakeValorDrained). Os tres voltam para esta lista na
    # rodada seguinte ao commit da geometria nova, e ate la eles contam como
    # mapa pobre na coluna `arte`, o que e verdade e nao maquiagem.
    "ManiacTunnel", "MtCoronet1FTunnelRoom", "MtCoronet2F",
    "MtCoronet3F", "MtCoronet4FRoom3", "MtCoronet5F", "MtCoronet6F",
    "MtCoronetIcebergRuins", "OldChateau", "OldChateauBackEastRoom",
    "OldChateauBackMiddleEastRoom", "OldChateauBackMiddleRoom",
    "OldChateauBackMiddleWestRoom", "OldChateauBackWestRoom",
    "OldChateauCorridor", "OldChateauDiningArea", "OldChateauSideRooms",
    "Route209LostTower1F", "Route209LostTower2F", "Route209LostTower3F",
    "Route209LostTower4F", "Route209LostTower5F", "RuinManiacCaveLong",
    "RuinManiacCaveShort", "SinnohVictoryRoad1F", "SinnohVictoryRoad2F",
    "SinnohVictoryRoadB1F", "SnowpointTemple1F", "SnowpointTempleB1F",
    "SnowpointTempleB2F", "SnowpointTempleB3F", "SnowpointTempleB4F",
    "SnowpointTempleB5F", "SolaceonRuinsManiacTunnelRoom", "SolaceonRuinsRoom1",
    "SolaceonRuinsRoom1NorthwestDeadEnd", "SolaceonRuinsRoom1SoutheastDeadEnd",
    "SolaceonRuinsRoom2", "SolaceonRuinsRoom2NortheastDeadEnd",
    "SolaceonRuinsRoom2SoutheastDeadEnd", "SolaceonRuinsRoom3",
    "SolaceonRuinsRoom3NorthwestDeadEnd", "SolaceonRuinsRoom3SouthwestDeadEnd",
    "SolaceonRuinsRoom4", "SolaceonRuinsRoom4SoutheastDeadEnd",
    "SolaceonRuinsRoom5", "SolaceonRuinsRoom5SoutheastDeadend",
    "SolaceonRuinsRoom5SouthwestDeadEnd", "SolaceonRuinsRoom6",
    "SolaceonRuinsRoom6NorthwestDeadEnd", "SolaceonRuinsRoom6SoutheastDeadEnd",
    "SolaceonRuinsRoom7", "ValorCavern", "VerityCavern", "VictoryRoad1FRoom1",
    "VictoryRoad1FRoom3", "WaywardCave1F", "WaywardCaveB1F",
]

# Mesmo par de tilesets do alvo: nada a filtrar, o id vale por si.
FONTES_SINNOH = ("MtCoronet_1F_South", "MtCoronet_B1F",
                 "MtCoronet_1F_North_Room1", "RavagedPath",
                 "OreburghMine_B2F", "OreburghGate_1F",
                 "MtCoronet_1F_North_Room2")
# Par de Hoenn: entra filtrado por `ids_seguros`.
FONTES_HOENN = ("GraniteCave_1F", "GraniteCave_B1F", "GraniteCave_B2F",
                "VictoryRoad_1F", "VictoryRoad_B1F", "VictoryRoad_B2F")

N8 = G.N8
N4 = G.N4

KMIN = 3             # ocorrências mínimas na fonte para o metatile ser estrutural
FRACAO_VAZIO = 0.4   # acima disso o metatile é "vazio" e não entra no estrutural
ESPACO = 6           # distância mínima (Chebyshev) entre dois enfeites
PISO_ARTE = 15       # metatiles distintos por mapa (régua do completude.py, dobrada)
# MB_NORMAL, MB_CAVE e as quatro águas. Fora daqui não se toca: escada (97),
# boca de caverna (101), buraco, esteira e tapete ficam como estão.
BEH_DECORAVEL = {0, 8, 16, 21, 22, 23}


# --------------------------------------------------------------- tileset seguro
def _bytes_tileset(label, _c={}):
    """(metatiles de 16 bytes, atributos de 2 bytes) do tileset."""
    if label not in _c:
        p = f"{RAIZ}/{G._pastas_tileset()[label]}"
        b = open(f"{p}/metatiles.bin", "rb").read()
        a = open(f"{p}/metatile_attributes.bin", "rb").read()
        _c[label] = ([b[i * 16:i * 16 + 16] for i in range(len(b) // 16)],
                     [a[i * 2:i * 2 + 2] for i in range(len(a) // 2)])
    return _c[label]


def ids_seguros(par_alvo, par_fonte, _c={}):
    """Ids de metatile que desenham e se comportam IGUAL nos dois pares.

    Um id aprendido na fonte só pode ser escrito no alvo se os 16 bytes do
    metatile e os 2 bytes do atributo forem idênticos nos dois tilesets. Se os
    pares forem o mesmo, é tudo. Sem esta função, o id 344 (primário de Hoenn)
    viraria outro desenho em Sinnoh sem ninguém ver.
    """
    if par_alvo == par_fonte:
        return None  # None = tudo liberado, e evita varrer 950 metatiles à toa
    k = (par_alvo, par_fonte)
    if k not in _c:
        ok = set()
        for base, ia, ifo in ((0, par_alvo[0], par_fonte[0]),
                              (512, par_alvo[1], par_fonte[1])):
            (ma, aa), (mf, af) = _bytes_tileset(ia), _bytes_tileset(ifo)
            for i in range(min(len(ma), len(mf), len(aa), len(af))):
                if ma[i] == mf[i] and aa[i] == af[i]:
                    ok.add(base + i)
        _c[k] = ok
    return _c[k]


# ------------------------------------------------------------- leitura do HEAD
def do_head(rel):
    r = subprocess.run(["git", "-C", RAIZ, "show", f"HEAD:{rel}"],
                       capture_output=True)
    if r.returncode != 0:
        return None
    b = r.stdout
    return list(struct.unpack_from("<%dH" % (len(b) // 2), b, 0))


def grade(nome, _c={}):
    """(map.json, layout, W, H, células) com o `map.bin` do HEAD, não da árvore."""
    if nome not in _c:
        d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))
        L = G._layouts()[d["layout"]]
        v = do_head(L["blockdata_filepath"])
        if v is None:
            sys.exit(f"{nome}: `git show HEAD:` falhou, e sem HEAD não há prova")
        _c[nome] = (d, L, L["width"], L["height"], v)
    return _c[nome]


def par(L):
    return (L["primary_tileset"], L["secondary_tileset"])


# ------------------------------------------------------------------ aprendizado
def aprende(fontes, par_alvo):
    """(tabela (parede, comportamento, n, assinatura) -> metatile, enfeites)."""
    tab = collections.defaultdict(collections.Counter)
    enfeites = []
    for nome in fontes:
        d, L, W, H, v = grade(nome)
        pf = par(L)
        beh = G.comportamento(*pf)
        seg = ids_seguros(par_alvo, pf)
        med = G.metricas(*pf)
        mask = G._mascara(v)
        perto = G._perto_do_jogavel(d, W, H, mask)
        freq = collections.Counter(v[y * W + x] & 0x3FF
                                   for y in range(H) for x in range(W)
                                   if (x, y) in perto)

        def util(mt):
            return (seg is None or mt in seg) and beh(mt) in BEH_DECORAVEL

        def estrutural(mt):
            return (freq[mt] >= KMIN and util(mt)
                    and med.get(mt, (1.0, 0.0))[0] <= FRACAO_VAZIO)

        for y in range(H):
            for x in range(W):
                if (x, y) not in perto:
                    continue
                mt = v[y * W + x] & 0x3FF
                if not estrutural(mt):
                    continue
                ch = (mask[y * W + x], beh(mt))
                tab[ch + (8, G._assin(mask, W, H, x, y, N8))][mt] += 1
                tab[ch + (4, G._assin(mask, W, H, x, y, N4))][mt] += 1
                tab[ch][mt] += 1

        # enfeite: grupo 4-conexo de metatile RARO, que é o que o artista pôs à
        # mão (estalagmite, pedra solta, veio de cristal, poça).
        raro = {(x, y) for x in range(W) for y in range(H)
                if (x, y) in perto and util(v[y * W + x] & 0x3FF)
                and freq[v[y * W + x] & 0x3FF] < KMIN}
        visto = set()
        for p0 in sorted(raro):
            if p0 in visto:
                continue
            grupo, fila = {p0}, [p0]
            visto.add(p0)
            while fila:
                x, y = fila.pop()
                for dx, dy in N4:
                    n = (x + dx, y + dy)
                    if n in raro and n not in visto:
                        visto.add(n)
                        grupo.add(n)
                        fila.append(n)
            xs, ys = [p[0] for p in grupo], [p[1] for p in grupo]
            w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
            if w > 3 or h > 3 or w * h != len(grupo):
                continue  # só retângulo cheio: pedaço solto de objeto fica fora
            x0, y0 = min(xs), min(ys)
            enfeites.append({
                "w": w, "h": h,
                "cel": [(x - x0, y - y0, v[y * W + x] & 0x3FF,
                         mask[y * W + x], beh(v[y * W + x] & 0x3FF))
                        for x, y in sorted(grupo)],
            })
    # enfeite de parede primeiro: é o que menos atrapalha a leitura do corredor
    enfeites.sort(key=lambda e: (-min(c[3] for c in e["cel"]), -len(e["cel"]),
                                 [c[2] for c in e["cel"]]))
    # sem repetido: dois mapas-fonte trazem a mesma estalagmite
    unicos, vistos = [], set()
    for e in enfeites:
        k = (e["w"], e["h"], tuple(e["cel"]))
        if k not in vistos:
            vistos.add(k)
            unicos.append(e)
    return tab, unicos


# ---------------------------------------------------------------------- geração
def _congelado(d, W, H):
    """Célula de evento e os 4 vizinhos ortogonais dela."""
    ev = set()
    for k in ("object_events", "warp_events", "bg_events", "coord_events"):
        for o in (d.get(k) or []):
            x, y = o.get("x"), o.get("y")
            if x is None or y is None:
                continue
            ev.add((x, y))
            for dx, dy in N4:
                ev.add((x + dx, y + dy))
    return ev


def _visivel(d, W, H, mask, raio=2):
    """Células alcançáveis a partir dos warps, mais uma orla de `raio` em volta.

    ARMADILHA MEDIDA, e ela custou a primeira imagem do MtCoronet2F: sem esta
    restrição o passo estrutural reescrevia também o MACIÇO de rocha, isto é os
    milhares de tiles de pedra que ficam atrás da parede e que o jogador nunca
    vê. O maciço saía de um cinza chapado (que é o certo para o que não se vê)
    para uma textura de tijolo repetida no mapa inteiro, e os enfeites iam
    parar no meio do nada. A silhueta da caverna tem 2 células de fundura (a
    face que dá para o corredor e o topo logo acima), então é isso que entra.
    """
    ini = [(w["x"], w["y"]) for w in (d.get("warp_events") or [])
           if 0 <= w["x"] < W and 0 <= w["y"] < H and not mask[w["y"] * W + w["x"]]]
    if not ini:
        ini = [(x, y) for y in range(H) for x in range(W) if not mask[y * W + x]]
    vis = set(ini)
    fila = collections.deque(ini)
    while fila:
        x, y = fila.popleft()
        for dx, dy in N4:
            n = (x + dx, y + dy)
            if (0 <= n[0] < W and 0 <= n[1] < H and not mask[n[1] * W + n[0]]
                    and n not in vis):
                vis.add(n)
                fila.append(n)
    orla = set(vis)
    for _ in range(raio):
        nova = set(orla)
        for x, y in orla:
            for dx, dy in N8:
                if 0 <= x + dx < W and 0 <= y + dy < H:
                    nova.add((x + dx, y + dy))
        orla = nova
    return orla


def decora(alvo, tabelas={}):
    """(layout, W, H, antes, depois, enfeites postos)."""
    d, L, W, H, v = grade(alvo)
    pa = par(L)
    if pa not in tabelas:
        tabelas[pa] = aprende(FONTES_SINNOH + FONTES_HOENN, pa)
    tab, enfeites = tabelas[pa]
    beh = G.comportamento(*pa)
    ev = _congelado(d, W, H)
    mask = G._mascara(v)
    vis = _visivel(d, W, H, mask)
    out = list(v)

    def livre(x, y):
        return ((x, y) not in ev and (x, y) in vis
                and beh(v[y * W + x] & 0x3FF) in BEH_DECORAVEL)

    for y in range(H):
        for x in range(W):
            if not livre(x, y):
                continue
            i = y * W + x
            ch = (mask[i], beh(v[i] & 0x3FF))
            novo = G._escolhe(tab, [ch + (8, G._assin(mask, W, H, x, y, N8)),
                                    ch + (4, G._assin(mask, W, H, x, y, N4)),
                                    ch])
            if novo is not None:
                out[i] = (v[i] & 0xFC00) | novo

    # Orçamento por área: uma sala de 32x32 não aguenta o mesmo número de
    # estalagmites que o labirinto 96x64 da Wayward Cave.
    area = W * H
    minimo = max(4, area // 400)
    teto = max(16, area // 110)
    postos, n = [], 0
    espaco = ESPACO

    def basta():
        return (n >= minimo and G.distintos(out) >= PISO_ARTE) or n >= teto

    def cabe(e, x, y):
        if any(max(abs(x - px), abs(y - py)) < espaco for px, py in postos):
            return False
        for dx, dy, mt, m, b in e["cel"]:
            nx, ny = x + dx, y + dy
            j = ny * W + nx
            if (mask[j] != m or beh(v[j] & 0x3FF) != b or not livre(nx, ny)):
                return False
        return True

    # Varredura em passos primos: espalha os enfeites pelo mapa em vez de
    # empilhar todos no canto superior esquerdo, e é determinística.
    # O espaçamento AFROUXA se a régua de arte ainda não fechou. As salinhas
    # sem saída das Solaceon Ruins são quem obriga: 971 células de rocha para 26
    # de chão, e com `ESPACO` fixo em 6 cabia UM enfeite, o que deixava a
    # SolaceonRuinsRoom2NortheastDeadEnd em 12 metatiles, abaixo da meta de 15.
    passos = [(7, 5), (5, 3), (3, 2), (1, 1)]
    for espaco in (ESPACO, 3, 2):
        if basta():
            break
        for sy, sx in passos:
            if basta():
                break
            for k, e in enumerate(enfeites):
                if basta():
                    break
                oy, ox = (k * 3) % max(1, sy), (k * 2) % max(1, sx)
                for y in range(oy, H - e["h"] + 1, sy):
                    if basta():
                        break
                    for x in range(ox, W - e["w"] + 1, sx):
                        if not cabe(e, x, y):
                            continue
                        for dx, dy, mt, _m, _b in e["cel"]:
                            j = (y + dy) * W + x + dx
                            out[j] = (v[j] & 0xFC00) | mt
                        postos.append((x, y))
                        n += 1
                        break
    return L, W, H, v, out, n


def confere_beh(pa, antes, depois):
    """Células em que o COMPORTAMENTO mudou. Tem que sair vazio."""
    beh = G.comportamento(*pa)
    return [i for i, (a, b) in enumerate(zip(antes, depois))
            if beh(a & 0x3FF) != beh(b & 0x3FF)]


# ------------------------------------------------------------------------ imagem
def render(L, W, H, v, caminho, escala=1):
    """PNG do `map.bin` dado (e não do que está em disco). Reusa `render_maps`."""
    import render_maps as RM
    from PIL import Image
    tp, ts = RM.carregar_tileset(L["primary_tileset"]), \
        RM.carregar_tileset(L["secondary_tileset"])
    img = Image.new("RGB", (W * 16, H * 16), tp["paletas"][0][0])
    px = img.load()
    for i, w in enumerate(v):
        mt = w & 0x3FF
        tset, loc = (tp, mt) if mt < 512 else (ts, mt - 512)
        if loc >= len(tset["metatiles"]) // 16:
            continue
        x0, y0 = (i % W) * 16, (i // W) * 16
        for k, (it, fh, fv, ip) in enumerate(RM.entradas_metatile(tset["metatiles"], loc)):
            t = RM.resolver_tile(tp, ts, it)
            cores = (tp if ip < 6 else ts)["paletas"].get(ip)
            if t is None or cores is None:
                continue
            RM.desenhar_tile(px, x0 + (k % 2) * 8, y0 + (k % 4 // 2) * 8,
                             t, cores, fh, fv)
    if escala != 1:
        img = img.resize((max(1, img.width // escala), max(1, img.height // escala)),
                         Image.NEAREST)
    img.save(caminho)
    return img


def par_de_imagens(alvo, L, W, H, antes, depois):
    """Um PNG com antes à esquerda e depois à direita, rotulado."""
    from PIL import Image, ImageDraw
    a = render(L, W, H, antes, os.path.join(SAIDA_IMG, ".tmp_a.png"))
    b = render(L, W, H, depois, os.path.join(SAIDA_IMG, ".tmp_b.png"))
    esc = max(1, (a.width * 2) // 1200 + (1 if a.width * 2 > 1200 else 0))
    if esc > 1:
        a = a.resize((a.width // esc, a.height // esc), Image.NEAREST)
        b = b.resize((b.width // esc, b.height // esc), Image.NEAREST)
    fx = 12
    fora = Image.new("RGB", (a.width + b.width + 12, a.height + fx + 4), (20, 20, 24))
    fora.paste(a, (0, fx))
    fora.paste(b, (a.width + 12, fx))
    dr = ImageDraw.Draw(fora)
    dr.text((2, 1), f"{alvo}  ANTES {G.distintos(antes)}", fill=(200, 200, 200))
    dr.text((a.width + 14, 1), f"DEPOIS {G.distintos(depois)}", fill=(120, 255, 120))
    p = os.path.join(SAIDA_IMG, f"{alvo}.png")
    fora.save(p)
    for t in (".tmp_a.png", ".tmp_b.png"):
        q = os.path.join(SAIDA_IMG, t)
        if os.path.exists(q):
            os.remove(q)
    return p


def folha_de_contato(caminhos):
    from PIL import Image
    cel = 300
    cols = 6
    linhas = (len(caminhos) + cols - 1) // cols
    fora = Image.new("RGB", (cols * cel, linhas * cel), (20, 20, 24))
    for i, p in enumerate(caminhos):
        im = Image.open(p)
        im.thumbnail((cel - 6, cel - 6), Image.NEAREST)
        fora.paste(im, ((i % cols) * cel + 3, (i // cols) * cel + 3))
    p = os.path.join(SAIDA_IMG, "CONTATO.png")
    fora.save(p)
    return p


# ------------------------------------------------------------------------ lista
def lista():
    """Recalcula os alvos do zero, para auditar a constante ALVOS."""
    import datetime
    import completude as C
    import importa_npcs_sinnoh as I
    fora = C._cortados_deficit()
    hoje = datetime.date.today()
    achados = []
    for m in sorted(I.nossos_mapas_sinnoh()):
        p = f"{RAIZ}/data/maps/{m}/map.json"
        if not os.path.exists(p) or m in fora:
            continue
        L = G._layouts().get(json.load(open(p))["layout"])
        if not L or "cave" not in (L.get("secondary_tileset") or "").lower():
            continue
        rel = L["blockdata_filepath"]
        v = do_head(rel)
        if v is None:
            continue
        n = len({c & 0x3FF for c in v})
        if n >= C.PISO_ARTE:
            continue
        mt = datetime.date.fromtimestamp(os.path.getmtime(f"{RAIZ}/{rel}"))
        achados.append((m, n, m in EXCLUIDOS, mt == hoje))
    meus = [m for m, _n, exc, novo in achados if not exc and not novo]
    for m, n, exc, novo in achados:
        marca = "EXCLUIDO(outro executor)" if exc else ("NOVO-HOJE" if novo else "")
        print(f"{m:38} {n:3} metatiles  {marca}")
    print(f"\n{len(achados)} pobres de caverna, {len(meus)} meus.")
    if meus != ALVOS:
        print("ATENÇÃO: a lista recalculada NÃO bate com a constante ALVOS.")
        print("  só na constante:", sorted(set(ALVOS) - set(meus)))
        print("  só recalculado :", sorted(set(meus) - set(ALVOS)))
    else:
        print("A constante ALVOS bate com o recálculo.")
    return meus


# ------------------------------------------------------------------------- demo
def demo():
    """As regras que este script não pode quebrar, medidas e não afirmadas."""
    amostra = ["WaywardCave1F", "SolaceonRuinsRoom1", "OldChateauCorridor",
               "MtCoronet2F", "SnowpointTempleB5F", "IronIslandB3F"]
    for alvo in amostra:
        L, W, H, antes, depois, n = decora(alvo)
        pa = par(L)

        # 1. colisão e elevação byte a byte contra o HEAD
        assert not G.confere(antes, depois), f"{alvo}: colisão/elevação mudou"

        # 2. comportamento de metatile idêntico célula a célula
        maus = confere_beh(pa, antes, depois)
        assert not maus, f"{alvo}: comportamento mudou em {len(maus)} células"

        # 3. evento e os 4 vizinhos ortogonais dele intocados
        d = grade(alvo)[0]
        for x, y in _congelado(d, W, H):
            if 0 <= x < W and 0 <= y < H:
                i = y * W + x
                assert antes[i] == depois[i], f"{alvo}: mexeu em ({x},{y}), perto de evento"

        # 4. a régua de arte sobe e passa do piso
        assert G.distintos(depois) >= PISO_ARTE, \
            f"{alvo}: {G.distintos(depois)} metatiles distintos, piso é {PISO_ARTE}"

        # 5. mutação plantada: se o gerador escrevesse a célula inteira em vez
        #    dos 10 bits de baixo, a colisão viajaria junto e é `confere` quem
        #    tem que gritar. Uma para colisão e uma para comportamento.
        mut = list(depois)
        mut[len(mut) // 2] ^= 0x0400
        assert G.confere(antes, mut), f"{alvo}: mutação de colisão passou batido"
        beh = G.comportamento(*pa)
        alvo_beh = next((i for i, w in enumerate(depois)
                         if beh(w & 0x3FF) == 8), None)
        assert alvo_beh is not None
        mut2 = list(depois)
        mut2[alvo_beh] = (mut2[alvo_beh] & 0xFC00) | 519  # 519 é comportamento 101
        assert confere_beh(pa, antes, mut2), \
            f"{alvo}: mutação de comportamento passou batido"

        print(f"OK  {alvo:24} {G.distintos(antes):3} -> {G.distintos(depois):3} "
              f"metatiles, {n} enfeites")

    # 6. o filtro de id seguro existe e corta de verdade
    seg = ids_seguros(("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh"),
                      ("gTileset_General", "gTileset_Cave"))
    assert seg is not None and 200 < len(seg) < 950, len(seg)
    assert 919 not in seg and 922 not in seg, "os dois metatiles que MUDARAM passaram"
    assert 753 in seg and 513 in seg, "a rocha e o chão de caverna foram cortados à toa"
    assert ids_seguros(("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh"),
                       ("gTileset_GeneralSinnoh", "gTileset_CaveSinnoh")) is None

    # 7. idempotência: ler do HEAD faz a segunda passada ser igual à primeira,
    #    mesmo com o `map.bin` da árvore já gravado.
    origem = {}
    try:
        um = {}
        for alvo in amostra:
            L, W, H, _, depois, _ = decora(alvo)
            rel = L["blockdata_filepath"]
            origem[rel] = open(f"{RAIZ}/{rel}", "rb").read()
            um[alvo] = depois
            grava(L, W, H, depois)
        grade.__defaults__[0].clear()  # esvazia o cache e força reler
        for alvo in amostra:
            L, W, H, _, dois, _ = decora(alvo)
            assert dois == um[alvo], f"{alvo}: não é idempotente"
    finally:
        for rel, b in origem.items():
            open(f"{RAIZ}/{rel}", "wb").write(b)
    print("OK  idempotente, e o repo voltou ao estado de antes do demo")


def grava(L, W, H, v):
    open(f"{RAIZ}/{L['blockdata_filepath']}", "wb").write(
        struct.pack("<%dH" % (W * H), *v))


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--lista" in sys.argv:
        return lista()
    aplicar = "--aplicar" in sys.argv
    imagens = aplicar or "--dry-run" in sys.argv
    if imagens:
        os.makedirs(SAIDA_IMG, exist_ok=True)
    antes_n, depois_n, pngs = [], [], []
    for alvo in ALVOS:
        L, W, H, antes, depois, n = decora(alvo)
        maus = G.confere(antes, depois)
        if maus:
            sys.exit(f"ABORTA {alvo}: colisão/elevação mudaria em {len(maus)} células")
        mb = confere_beh(par(L), antes, depois)
        if mb:
            sys.exit(f"ABORTA {alvo}: comportamento mudaria em {len(mb)} células")
        a, b = G.distintos(antes), G.distintos(depois)
        antes_n.append(a)
        depois_n.append(b)
        print(f"{alvo:38} arte {a:3} -> {b:3}  enfeites={n:3}  "
              f"colisão e comportamento idênticos")
        if imagens:
            pngs.append(par_de_imagens(alvo, L, W, H, antes, depois))
        if aplicar:
            grava(L, W, H, depois)
    if pngs:
        print("folha de contato:", folha_de_contato(pngs))
    antes_n.sort()
    depois_n.sort()
    med = lambda x: x[len(x) // 2] if len(x) % 2 else (x[len(x) // 2 - 1] + x[len(x) // 2]) / 2
    print(f"\n{len(ALVOS)} mapas | antes mediana {med(antes_n):g} mínimo {antes_n[0]} "
          f"| depois mediana {med(depois_n):g} mínimo {depois_n[0]}")
    if not aplicar:
        print("(nada escrito; use --aplicar)")


if __name__ == "__main__":
    main()
