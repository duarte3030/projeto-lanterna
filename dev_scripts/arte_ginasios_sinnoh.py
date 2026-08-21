#!/usr/bin/env python3
"""Decora os 8 ginásios de Sinnoh escrevendo SÓ o id de metatile do `map.bin`.

O problema: os 8 ginásios vestem o molde de ginásio de Hoenn com a planta certa
do Platinum, mas o desenho é uma máscara de colisão em duas cores (4 a 8
metatiles distintos por mapa, contra mediana 39 em Sinnoh e piso 10 na régua do
`completude.py`). Não existe arte 2D dos ginásios de Sinnoh em fonte nenhuma (o
Platinum os guarda em 3D, premissa derrubada na 0.h do ESTADO), então a arte é
INVENÇÃO DECLARADA. O vocabulário é o do tileset que cada mapa JÁ carrega, e ele
é o tileset do ginásio de Hoenn do mesmo tema:

    Oreburgh (Roark, pedra)   -> RustboroGym    (ginásio de pedra)
    Eterna   (Gardenia, planta)-> RustboroGym
    Canalave (Byron, aço)     -> RustboroGym
    Veilstone(Maylene, luta)  -> DewfordGym     (ginásio de luta)
    Pastoria (Wake, água)     -> SootopolisGym  (ginásio de água/gelo)
    Snowpoint(Candice, gelo)  -> SootopolisGym
    Hearthome(Fantina, fantasma)-> MossdeepGym
    Sunyshore(Volkner, elétrico)-> MauvilleGym  (ginásio elétrico)

Como funciona, e por que não pode quebrar nada:

1. A célula do `map.bin` é um u16: **10 bits de baixo são o METATILE** e os 6 de
   cima são COLISÃO e ELEVAÇÃO. Este script escreve `(antigo & 0xFC00) | novo`,
   ou seja **nunca toca nos 6 bits de cima**. A máscara de colisão e elevação
   sai byte a byte idêntica, e `confere()` prova isso célula a célula.
2. Andabilidade não muda porque colisão e elevação não mudam. O que ainda podia
   mudar comportamento é o ATRIBUTO do metatile (gelo, esteira, porta, tapete),
   então só entram células cujo metatile tem comportamento `MB_NORMAL` (0), e o
   substituto também tem que ser 0. Isso congela sozinho o tapete de entrada do
   Oreburgh (0x30/0x31), as 497 lajes de gelo do Snowpoint (0x20) e as duas
   pontas dela (0xC0/0xC1): o quebra-cabeça de gelo fica intacto.
3. Célula que tem evento em cima (objeto, warp, placa, gatilho) fica congelada.
   Nenhum `map.json` é lido para escrita e nenhum é tocado.

O desenho vem em dois passos, os dois lendo o ginásio de Hoenn correspondente:

  - PASSO ESTRUTURAL: para cada célula, a assinatura de vizinhança de parede
    (8 vizinhos, fora do mapa conta como parede) escolhe o metatile que o
    artista da Nintendo usou na MESMA assinatura no mapa de Hoenn. É autotiling
    aprendido da fonte, e é o que dá canto, quina, topo e frente de parede em
    vez de um bloco chapado.
  - PASSO DE ENFEITE: os grupos de metatile RAROS do mapa de Hoenn (máquina,
    estátua, quadro) são os enfeites que o artista pôs à mão. Cada grupo é
    recortado com sua máscara de colisão e carimbado no ginásio de Sinnoh onde a
    máscara casa exatamente, espaçado, longe de evento.

Três filtros que a medição obrigou a existir (cada um nasceu de um defeito visto
na imagem, não de teoria):

  - ALCANCE: só se aprende de célula do mapa de Hoenn que é andável ou vizinha
    de andável. Sem isso o "lado de fora da sala" do Rustboro virava buraco
    branco no meio do Oreburgh.
  - RARIDADE (`KMIN`): o passo estrutural só usa metatile que aparece 3+ vezes
    na fonte. Sem isso a máquina do Rustboro e a corda dela apareciam sorteadas
    no meio do salão, porque a assinatura tinha uma amostra só.
  - VAZIO: metatile que renderiza mais de 60% na cor de fundo é PROIBIDO no
    passo estrutural. O ginásio de Mauville é um corredor sobre o vazio e usa
    preto de propósito; copiado para os blocos de parede do Sunyshore, o preto
    virava furo no chão.

Uso:
    python3 dev_scripts/arte_ginasios_sinnoh.py            # mede, não escreve
    python3 dev_scripts/arte_ginasios_sinnoh.py --gravar   # escreve os map.bin
    python3 dev_scripts/arte_ginasios_sinnoh.py --demo     # auto-teste

Idempotente: as escolhas dependem só de colisão, evento e comportamento, que o
script nunca muda. Rodar duas vezes dá o mesmo byte (o `--demo` prova).
"""
import collections
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ginásio de Sinnoh -> ginásio de Hoenn que empresta o vocabulário (mesmo tileset)
PARES = {
    "OreburghCity_Gym":  "RustboroCity_Gym",
    "EternaCity_Gym":    "RustboroCity_Gym",
    "CanalaveCity_Gym":  "RustboroCity_Gym",
    "VeilstoneCity_Gym": "DewfordTown_Gym",
    "PastoriaCity_Gym":  "SootopolisCity_Gym_1F",
    "SnowpointCity_Gym": "SootopolisCity_Gym_1F",
    "HearthomeCity_Gym": "MossdeepCity_Gym",
    "SunyshoreCity_Gym": "MauvilleCity_Gym",
}

N8 = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
N4 = [N8[0], N8[2], N8[4], N8[6]]

KMIN = 3           # metatile precisa aparecer 3+ vezes na fonte para ser estrutural
FRACAO_VAZIO = 0.4  # acima disso o metatile é "vazio" e não entra no passo estrutural
ENFEITES_MAX = 8    # por ginásio, mais os que a régua de arte ainda pedir
ENFEITES_TETO = 24  # e nunca mais que isso
PISO_ARTE = 15      # metatiles distintos por ginásio (régua do completude.py, dobrada)
ESPACO = 4          # distância mínima (Chebyshev) entre dois enfeites


# --------------------------------------------------------------------- leitura
def _layouts(_c={}):
    if not _c:
        d = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
        _c.update({l["id"]: l for l in d["layouts"] if l.get("id")})
    return _c


def _pastas_tileset(_c={}):
    """{gTileset_X: pasta}. A fonte da verdade é o INCBIN dos fontes do jogo."""
    if _c:
        return _c
    tiles = {}
    pad = re.compile(r'const u32 gTilesetTiles_([A-Za-z0-9_]+)\[\] = '
                     r'INC(?:BIN|GFX)_U32\("(data/tilesets/(?:primary|secondary)'
                     r'/[a-z0-9_/]+?)/tiles')
    for rel in ("src/data/tilesets/graphics.h", "src/graphics.c"):
        p = f"{RAIZ}/{rel}"
        if os.path.exists(p):
            for lb, pasta in pad.findall(open(p).read()):
                tiles[lb] = pasta
    cab = open(f"{RAIZ}/src/data/tilesets/headers.h").read()
    for m in re.finditer(r"const struct Tileset (gTileset_\w+)\s*=\s*\{(.*?)\n\};",
                         cab, re.S):
        mm = re.search(r"gTilesetTiles_(\w+)", m.group(2))
        if mm and mm.group(1) in tiles:
            _c[m.group(1)] = tiles[mm.group(1)]
    return _c


def _attrs(label, _c={}):
    if label not in _c:
        b = open(f"{RAIZ}/{_pastas_tileset()[label]}/metatile_attributes.bin", "rb").read()
        _c[label] = [struct.unpack_from("<H", b, i * 2)[0] for i in range(len(b) // 2)]
    return _c[label]


def comportamento(pri, sec):
    ap, asec = _attrs(pri), _attrs(sec)

    def f(mt):
        t, i = (ap, mt) if mt < 512 else (asec, mt - 512)
        return (t[i] & 0x1FF) if 0 <= i < len(t) else 0
    return f


def grade(nome):
    d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))
    L = _layouts()[d["layout"]]
    W, H = L["width"], L["height"]
    b = open(f"{RAIZ}/{L['blockdata_filepath']}", "rb").read()
    return d, L, W, H, list(struct.unpack_from("<%dH" % (W * H), b, 0))


# ----------------------------------------------------------- filtro de "vazio"
def fracao_vazio(pri, sec, _c={}):
    """{metatile: fração de pixels na cor de fundo}, renderizando o metatile.

    Reusa `render_maps.py` em vez de reimplementar 4bpp e paleta JASC.
    """
    if (pri, sec) in _c:
        return _c[(pri, sec)]
    sys.path.insert(0, f"{RAIZ}/dev_scripts")
    import render_maps as RM
    from PIL import Image
    tp, ts = RM.carregar_tileset(pri), RM.carregar_tileset(sec)
    fundo = tp["paletas"][0][0]
    out = {}
    for base, tset in ((0, tp), (512, ts)):
        for i in range(len(tset["metatiles"]) // 16):
            img = Image.new("RGB", (16, 16), fundo)
            px = img.load()
            for k, (it, fh, fv, ip) in enumerate(RM.entradas_metatile(tset["metatiles"], i)):
                t = RM.resolver_tile(tp, ts, it)
                if t is None:
                    continue
                cores = (tp if ip < 6 else ts)["paletas"].get(ip)
                if cores is None:
                    continue
                RM.desenhar_tile(px, (k % 4 % 2) * 8, (k % 4 // 2) * 8, t, cores, fh, fv)
            n = sum(1 for y in range(16) for x in range(16) if px[x, y] == fundo)
            out[base + i] = n / 256.0
    _c[(pri, sec)] = out
    return out


# ------------------------------------------------------------------ aprendizado
def _mascara(v):
    return [1 if ((c >> 10) & 3) else 0 for c in v]


def _assin(mask, W, H, x, y, viz):
    s = 0
    for i, (dx, dy) in enumerate(viz):
        nx, ny = x + dx, y + dy
        s |= (1 if not (0 <= nx < W and 0 <= ny < H) else mask[ny * W + nx]) << i
    return s


def _perto_do_jogavel(d, W, H, mask):
    """Células andáveis a partir dos warps, mais a orla de 1 célula em volta."""
    ini = [(w["x"], w["y"]) for w in (d.get("warp_events") or [])
           if 0 <= w["x"] < W and 0 <= w["y"] < H and not mask[w["y"] * W + w["x"]]]
    if not ini:
        ini = [(x, y) for y in range(H) for x in range(W) if not mask[y * W + x]][:1]
    vis, fila = set(ini), collections.deque(ini)
    while fila:
        x, y = fila.popleft()
        for dx, dy in N4:
            n = (x + dx, y + dy)
            if (0 <= n[0] < W and 0 <= n[1] < H and not mask[n[1] * W + n[0]]
                    and n not in vis):
                vis.add(n)
                fila.append(n)
    perto = set(vis)
    for x, y in vis:
        for dx, dy in N8:
            perto.add((x + dx, y + dy))
    return perto


def aprende(ref):
    """(tabela de assinatura -> metatile, lista de enfeites) do ginásio de Hoenn."""
    d, L, W, H, v = grade(ref)
    beh = comportamento(L["primary_tileset"], L["secondary_tileset"])
    vazio = fracao_vazio(L["primary_tileset"], L["secondary_tileset"])
    mask = _mascara(v)
    perto = _perto_do_jogavel(d, W, H, mask)

    freq = collections.Counter(v[y * W + x] & 0x3FF
                               for y in range(H) for x in range(W) if (x, y) in perto)

    def estrutural(mt):
        return (freq[mt] >= KMIN and beh(mt) == 0
                and vazio.get(mt, 1.0) <= FRACAO_VAZIO)

    tab = collections.defaultdict(collections.Counter)
    for y in range(H):
        for x in range(W):
            if (x, y) not in perto:
                continue
            mt = v[y * W + x] & 0x3FF
            if not estrutural(mt):
                continue
            m = mask[y * W + x]
            tab[(m, 8, _assin(mask, W, H, x, y, N8))][mt] += 1
            tab[(m, 4, _assin(mask, W, H, x, y, N4))][mt] += 1
            tab[(m,)][mt] += 1

    # enfeites: grupos 4-conexos de metatile RARO, que é o que o artista pôs à
    # mão. Guarda a máscara de colisão de cada célula: enfeite de parede só
    # cabe em parede e enfeite de chão só cabe em chão.
    raro = {(x, y) for x in range(W) for y in range(H)
            if (x, y) in perto
            and beh(v[y * W + x] & 0x3FF) == 0
            and freq[v[y * W + x] & 0x3FF] < KMIN}
    enfeites, visto = [], set()
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
        xs = [p[0] for p in grupo]
        ys = [p[1] for p in grupo]
        w, h = max(xs) - min(xs) + 1, max(ys) - min(ys) + 1
        if w > 3 or h > 3 or w * h != len(grupo):
            continue  # só retângulo cheio: pedaço solto de objeto fica de fora
        x0, y0 = min(xs), min(ys)
        enfeites.append({
            "w": w, "h": h,
            "cel": [(x - x0, y - y0, v[y * W + x] & 0x3FF, mask[y * W + x])
                    for x, y in sorted(grupo)],
        })
    # enfeite de parede primeiro: é o que menos atrapalha a leitura do salão
    enfeites.sort(key=lambda e: (-min(c[3] for c in e["cel"]), -len(e["cel"])))
    return tab, enfeites


def _escolhe(tab, chaves):
    for k in chaves:
        c = tab.get(k)
        if c:
            return c.most_common(1)[0][0]
    return None


# ---------------------------------------------------------------------- geração
def decora(alvo):
    """Devolve (layout, W, H, antes, depois, quantos enfeites)."""
    tab, enfeites = aprende(PARES[alvo])
    d, L, W, H, v = grade(alvo)
    beh = comportamento(L["primary_tileset"], L["secondary_tileset"])
    ev = {(o["x"], o["y"])
          for k in ("object_events", "warp_events", "bg_events", "coord_events")
          for o in (d.get(k) or [])}
    mask = _mascara(v)
    out = list(v)

    livre = lambda x, y: (x, y) not in ev and beh(v[y * W + x] & 0x3FF) == 0

    for y in range(H):
        for x in range(W):
            if not livre(x, y):
                continue
            i, m = y * W + x, mask[y * W + x]
            novo = _escolhe(tab, [(m, 8, _assin(mask, W, H, x, y, N8)),
                                  (m, 4, _assin(mask, W, H, x, y, N4)),
                                  (m,)])
            if novo is not None:
                out[i] = (v[i] & 0xFC00) | novo

    # Para enquanto já houver enfeite suficiente E a régua de arte já tiver
    # fechado. O Sunyshore é quem obriga: o vocabulário de parede do ginásio de
    # Mauville é magro (corredor sobre o vazio), e só o passo estrutural deixa
    # ele em 13 metatiles distintos, abaixo do piso.
    postos, n = [], 0
    basta = lambda: (n >= ENFEITES_MAX and distintos(out) >= PISO_ARTE) or n >= ENFEITES_TETO

    def cabe(e, x, y):
        if any(max(abs(x - px), abs(y - py)) < ESPACO for px, py in postos):
            return False
        return all(mask[(y + dy) * W + x + dx] == m and livre(x + dx, y + dy)
                   and beh(mt) == 0 for dx, dy, mt, m in e["cel"])

    # Uma cópia de cada enfeite por volta, e não 24 cópias do primeiro: a
    # primeira versão esgotava o teto carimbando sempre o mesmo objeto, e a
    # régua de arte do Sunyshore CAIA em vez de subir.
    for _ in range(3):
        if basta():
            break
        for e in enfeites:
            if basta():
                break
            for y in range(H - e["h"] + 1):
                posto = False
                for x in range(W - e["w"] + 1):
                    if not cabe(e, x, y):
                        continue
                    for dx, dy, mt, _m in e["cel"]:
                        j = (y + dy) * W + x + dx
                        out[j] = (v[j] & 0xFC00) | mt
                    postos.append((x, y))
                    n += 1
                    posto = True
                    break
                if posto:
                    break
    return L, W, H, v, out, n


def confere(antes, depois):
    """Colisão e elevação idênticas célula a célula. Devolve lista de defeitos."""
    return [i for i, (a, b) in enumerate(zip(antes, depois))
            if (a & 0xFC00) != (b & 0xFC00)]


def distintos(v):
    return len({c & 0x3FF for c in v})


def grava(L, W, H, v):
    open(f"{RAIZ}/{L['blockdata_filepath']}", "wb").write(struct.pack("<%dH" % (W * H), *v))


# ------------------------------------------------------------------------ demo
def demo():
    """As regras que este script não pode quebrar, medidas e não afirmadas."""
    for alvo in PARES:
        L, W, H, antes, depois, n = decora(alvo)
        beh = comportamento(L["primary_tileset"], L["secondary_tileset"])

        # 1. colisão e elevação byte a byte
        assert not confere(antes, depois), f"{alvo}: colisão/elevação mudou"

        # 2. comportamento de metatile idêntico célula a célula (andabilidade,
        #    gelo, tapete e porta continuam o que eram)
        maus = [i for i, (a, b) in enumerate(zip(antes, depois))
                if beh(a & 0x3FF) != beh(b & 0x3FF)]
        assert not maus, f"{alvo}: comportamento mudou em {len(maus)} células"

        # 3. a régua de arte sobe e passa de 15
        assert distintos(depois) >= 15, \
            f"{alvo}: {distintos(depois)} metatiles distintos, piso é 15"

        # 4. a mutação plantada TEM que ser pega: se o gerador escrevesse a
        #    célula inteira em vez dos 10 bits de baixo, a colisão viajaria
        #    junto e `confere` é quem tem que gritar.
        mutante = list(depois)
        mutante[len(mutante) // 2] ^= 0x0400
        assert confere(antes, mutante), f"{alvo}: mutação de colisão passou batido"

        print(f"OK  {alvo:22} {distintos(antes):3} -> {distintos(depois):3} metatiles, "
              f"{n} enfeites")

    # 5. idempotência: o segundo passe não pode mexer em nada. Só dá para medir
    #    escrevendo, então grava, roda de novo e volta ao estado original.
    origem = {a: grade(a)[4] for a in PARES}
    try:
        um = {}
        for alvo in PARES:
            L, W, H, _, depois, _ = decora(alvo)
            um[alvo] = depois
            grava(L, W, H, depois)
        for alvo in PARES:
            L, W, H, _, dois, _ = decora(alvo)
            assert dois == um[alvo], f"{alvo}: não é idempotente"
    finally:
        for alvo, v in origem.items():
            L = _layouts()[json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))["layout"]]
            grava(L, L["width"], L["height"], v)
    print("OK  idempotente, e o repo voltou ao estado de antes do demo")


def main():
    if "--demo" in sys.argv:
        return demo()
    gravar = "--gravar" in sys.argv
    for alvo in PARES:
        L, W, H, antes, depois, n = decora(alvo)
        maus = confere(antes, depois)
        if maus:
            sys.exit(f"ABORTA {alvo}: colisão/elevação mudaria em {len(maus)} células")
        print(f"{alvo:22} arte {distintos(antes):3} -> {distintos(depois):3}  "
              f"enfeites={n}  colisão idêntica")
        if gravar:
            grava(L, W, H, depois)
    if not gravar:
        print("\n(nada escrito; use --gravar)")


if __name__ == "__main__":
    main()
