#!/usr/bin/env python3
"""Camada invertida de Sinnoh: objeto na FRENTE do qual o jogador para tampava a cabeça dele.

O DEFEITO (playtest do Gui na ROM bugs2b, 30/09/2026)
-----------------------------------------------------
"Em Sinnoh inteira está invertida a sobreposição de tile: minha cabeça é tampada
pelos objetos." E, antes, em Veilstone: "andei 1 tile a mais pra cima do teto do
Pokémon Center". As duas queixas são a MESMA coisa: parado embaixo da parede do
Centro Pokémon, a parede é desenhada por cima da cabeça do jogador, e o sprite
parece ter entrado um tile no prédio.

O sprite do jogador tem 16x32: os pés ficam na célula P e a cabeça invade a
célula N, logo ao norte. O motor (`DrawMetatile`, src/field_camera.c) manda a
camada de CIMA de um metatile do tipo NORMAL ou SPLIT para o BG1, que fica POR
CIMA dos sprites de prioridade 2 (toda elevação que não é ponte, ver
`sElevationToPriority` em src/event_object_movement.c). Os tilesets que vieram do
Sinnoh-pokeemerald-expansion (LiderMorti00) e algumas peças das cidades do Retro
Platinum desenham o objeto INTEIRO na camada de cima: parede de prédio, copa de
árvore, arbusto, pedra, cerca. Resultado: toda vez que o jogador para na frente
de um deles, o objeto, que está ATRÁS dele na perspectiva, cobre a cabeça.

Medido com a régua desta ferramenta (célula andável de prioridade 2 cujo vizinho
do norte é bloqueado e tem arte na camada de cima): Sinnoh 2,41% das células
andáveis de cidades e rotas, contra 0,37% em Hoenn, 0,34% em Kanto e 0,20% em
Johto. A fonte (`fontes-mapas/sinnoh`) tem os MESMOS bytes: o defeito é de origem,
não da nossa conversão.

O CONSERTO, na origem
---------------------
Para cada metatile assim, num tileset que só Sinnoh usa e cujo arquivo de
atributo não é apelido de outro (ASSET_ALIAS), o tipo de camada vira COVERED: as
duas camadas passam a ser desenhadas ABAIXO do sprite (BG3 e BG2), na mesma ordem
entre si. O desenho parado não muda um pixel (a ferramenta prova isso metatile a
metatile, incluindo o lixo 0x3014 que o tipo NORMAL põe no BG3); só muda quem
fica por cima quando um sprite encosta.

O que DEVE continuar cobrindo o jogador continua: a regra só mexe em metatile que
é bloqueado em TODA célula onde aparece andável-de-prioridade-2 zero vezes. Ponta
de copa por onde o jogador passa atrás da árvore, beiral de telhado que se pisa e
ponte são células ANDÁVEIS, então o metatile delas fica como está. Metatile que é
bloqueado num lugar e andável em outro entra numa lista de decisão (CONFLITOS)
com o motivo escrito.

REGERAR UM TILESET DESFAZ O CONSERTO: o copiador (`copia_cidade_fonte.py` e
afins) devolve os atributos da fonte. Depois de regerar, rode `--aplicar` de
novo e regrave o carimbo (`qa/lente_carimbo.py --carimba`) com o motivo no
commit. Se alguém esquecer, a `qa/lente_camada.py` do `roda_qa` acusa trava Z1.

Uso:
    python3 dev_scripts/camada_sinnoh.py              # mede e lista, não grava
    python3 dev_scripts/camada_sinnoh.py --aplicar    # grava os atributos
    python3 dev_scripts/camada_sinnoh.py --verifica   # exit 1 se sobrar defeito
"""
import collections
import json
import os
import re
import struct
import sys

from PIL import Image

RAIZ = os.environ.get("POKE_RAIZ") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# src/event_object_movement.c, sElevationToPriority. Prioridade 1 desenha o
# sprite acima do BG1 (ponte), e aí camada nenhuma o cobre.
PRIORIDADE = [2, 2, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 0, 0, 2]
NORMAL, COVERED, SPLIT = 0, 1, 2
GRUPOS_SINNOH_EXTRA = ("gMapGroup_IndoorTwinleaf", "gMapGroup_IndoorSandgem",
                       "gMapGroup_IndoorJubilife", "gMapGroup_IndoorOreburgh",
                       "gMapGroup_IndoorFloaroma", "gMapGroup_TeamGalactic")

# Metatile bloqueado num lugar e andável em outro: a regra é a MAIORIA. Se ele
# tampa a cabeça em pelo menos tantas células quanto as células andáveis em que
# ele cobre o próprio jogador, vira COVERED; senão fica. Medido em 30/09/2026:
#   - as copas e troncos de árvore do GeneralSinnoh (0x1d7, 0x1de, 0x1df) tampam
#     704 cabeças e são andáveis em 16 células, todas colisão errada de tronco ou
#     copa pisável (CanalaveCity x=3, Route203 linhas 11 e 13);
#   - o piso 0x2e1 do Veilstone (a plataforma da linha 6) é andável em 9 células,
#     e ali a camada de cima cobria o CORPO INTEIRO do jogador: trocar conserta
#     as duas coisas;
#   - os que ficam (0x009 do Jubilife, 0x1b1 da CaveSinnoh e cinco peças do Retro
#     Platinum) são andáveis em mais células do que tampam: ali a cobertura é o
#     desenho de passar por trás, e a perda seria maior que o ganho.



def _le(caminho):
    with open(os.path.join(RAIZ, caminho), encoding="utf-8") as f:
        return f.read()


_ROTULOS = None


def rotulos():
    """gTileset_X -> dict(metatiles=caminho, atributos=caminho ou None se apelido, tiles=caminho)."""
    global _ROTULOS
    if _ROTULOS is not None:
        return _ROTULOS
    hdr = _le("src/data/tilesets/headers.h")
    met = _le("src/data/tilesets/metatiles.h")
    gfx = _le("src/data/tilesets/graphics.h") + _le("src/graphics.c")
    incbin = dict(re.findall(r'const u16 (\w+)\[\] = INCBIN_U16\("([^"]+)"\)', met))
    tiles = dict(re.findall(r'const u32 (\w+)\[\] = INC(?:BIN|GFX)_U32\("([^"]+?)\.(?:4bpp|png)[^"]*"', gfx))
    fora = {}
    for nome, corpo in re.findall(r'const struct Tileset (\w+) =\s*\{(.*?)\};', hdr, re.S):
        m = re.search(r'\.metatiles = (\w+)', corpo)
        a = re.search(r'\.metatileAttributes = (\w+)', corpo)
        t = re.search(r'\.tiles = (\w+)', corpo)
        if not (m and a):
            continue
        tp = tiles.get(t.group(1)) if t else None
        fora[nome] = dict(metatiles=incbin.get(m.group(1)), atributos=incbin.get(a.group(1)),
                          tiles=(tp + ".png") if tp else None,
                          secundario="isSecondary = TRUE" in corpo)
    _ROTULOS = fora
    return fora


_CACHE = {}


def tileset(rotulo):
    """(atributos u16 mutáveis, metatiles bytes, tiles como listas 8x8 de índice)."""
    if rotulo in _CACHE:
        return _CACHE[rotulo]
    r = rotulos().get(rotulo)
    if not r or not r["metatiles"]:
        _CACHE[rotulo] = None
        return None
    mt = open(os.path.join(RAIZ, r["metatiles"]), "rb").read()
    attr_path = r["atributos"]
    if attr_path is None:
        # Apelido: o atributo é o de outro rótulo. Lê pelo nome do arquivo do
        # metatile, que fica na mesma pasta.
        attr_path = os.path.join(os.path.dirname(r["metatiles"]), "metatile_attributes.bin")
    ab = open(os.path.join(RAIZ, attr_path), "rb").read()
    n = len(mt) // 16
    largura = len(ab) // n if n else 2
    if largura == 4:
        attrs = [(v >> 29) & 3 for v in struct.unpack("<%dI" % (len(ab) // 4), ab)]
    else:
        attrs = [(v >> 12) & 0xF for v in struct.unpack("<%dH" % (len(ab) // 2), ab)]
    lista = []
    if r["tiles"] and os.path.exists(os.path.join(RAIZ, r["tiles"])):
        im = Image.open(os.path.join(RAIZ, r["tiles"])).convert("P")
        w, h = im.size
        px = im.load()
        for i in range((w // 8) * (h // 8)):
            cx, cy = (i % (w // 8)) * 8, (i // (w // 8)) * 8
            lista.append([[px[cx + x, cy + y] % 16 for x in range(8)] for y in range(8)])
    _CACHE[rotulo] = (attrs, mt, lista, largura)
    return _CACHE[rotulo]


def _layouts():
    return {l["id"]: l for l in json.load(open(os.path.join(RAIZ, "data/layouts/layouts.json")))["layouts"]
            if "id" in l}


def _grupos():
    return json.load(open(os.path.join(RAIZ, "data/maps/map_groups.json")))


def grupos_sinnoh(mg=None):
    mg = mg or _grupos()
    return [g for g in mg["group_order"] if "Sinnoh" in g or g in GRUPOS_SINNOH_EXTRA]


def tilesets_exclusivos():
    """Rótulos que só mapas de Sinnoh usam E cujo arquivo de atributo é próprio."""
    mg = _grupos()
    L = _layouts()
    sin = set(grupos_sinnoh(mg))
    uso = collections.defaultdict(set)
    for g in mg["group_order"]:
        for m in mg[g]:
            l = L[json.load(open(os.path.join(RAIZ, "data/maps", m, "map.json")))["layout"]]
            for t in (l["primary_tileset"], l["secondary_tileset"]):
                uso[t].add(g in sin)
    # Um arquivo de atributo pode ser lido por dois rótulos (mesma pasta): os
    # dois têm de ser exclusivos.
    por_arquivo = collections.defaultdict(set)
    for rot, r in rotulos().items():
        if r["atributos"]:
            por_arquivo[r["atributos"]].add(rot)
    fora = set()
    for t, s in uso.items():
        r = rotulos().get(t)
        if s != {True} or not r or not r["atributos"]:
            continue
        if all(uso.get(o, {True}) == {True} for o in por_arquivo[r["atributos"]]):
            fora.add(t)
    return fora


def _quadrantes(pri, sec, mid, npri, ntiles_pri):
    """Os 8 quadrantes (4 baixo, 4 cima) do metatile, como pixels 8x8 ou None se vazio."""
    tp, ts = tileset(pri), tileset(sec)
    if mid < npri:
        dono, loc = tp, mid
    else:
        dono, loc = ts, mid - npri
    if dono is None or loc * 16 + 16 > len(dono[1]):
        return None
    out = []
    for q in range(8):
        e = struct.unpack_from("<H", dono[1], loc * 16 + q * 2)[0]
        out.append((e, _tile(tp, ts, e & 0x3FF, ntiles_pri)))
    return out


def _tile(tp, ts, idx, ntiles_pri):
    if idx < ntiles_pri:
        return tp[2][idx] if tp and idx < len(tp[2]) else None
    k = idx - ntiles_pri
    return ts[2][k] if ts and k < len(ts[2]) else None


def _tem_arte(quads, camada):
    for e, t in quads[camada * 4:camada * 4 + 4]:
        if t and any(c for linha in t for c in linha):
            return True
    return False


def camada_de(pri, sec, mid, npri):
    tp, ts = tileset(pri), tileset(sec)
    dono, loc = (tp, mid) if mid < npri else (ts, mid - npri)
    if dono is None or loc >= len(dono[0]):
        return None
    return dono[0][loc]


def _pixel(quads, camada, px, py):
    """Índice de cor (0 = transparente) da camada no pixel (px, py) do metatile 16x16."""
    e, t = quads[camada * 4 + (py // 8) * 2 + (px // 8)]
    if t is None:
        return 0
    x, y = px % 8, py % 8
    if e & 0x400:
        x = 7 - x
    if e & 0x800:
        y = 7 - y
    return t[y][x]


def desenho_igual_como_covered(pri, sec, mid, npri, ntiles_pri):
    """O desenho parado de NORMAL e de COVERED é o mesmo pixel a pixel?

    NORMAL: BG3 = tile 0x14 paleta 3 (o "lixo" de DrawMetatile), BG2 = baixo, BG1 = cima.
    COVERED: BG3 = baixo, BG2 = cima, BG1 = vazio. Só diverge onde baixo e cima
    são transparentes no mesmo pixel e o tile 0x14 não é.
    """
    if camada_de(pri, sec, mid, npri) != NORMAL:
        # SPLIT já desenha o de baixo no BG3 e nada no BG2: virar COVERED só
        # desce a camada de cima de BG1 para BG2, sem lixo nenhum no meio.
        return True
    quads = _quadrantes(pri, sec, mid, npri, ntiles_pri)
    lixo = _tile(tileset(pri), tileset(sec), 0x14, ntiles_pri)
    for py in range(16):
        for px in range(16):
            if _pixel(quads, 0, px, py) or _pixel(quads, 1, px, py):
                continue
            if lixo and lixo[py % 8][px % 8]:
                return False
    return True


def varre(exclusivos=None):
    """Mede o defeito. Devolve (celulas, por_metatile, uso_andavel, objetos, total_andavel).

    celulas: lista de (mapa, x, y, rotulo, metatile_local) com a cabeça tampada.
    """
    exclusivos = tilesets_exclusivos() if exclusivos is None else exclusivos
    mg = _grupos()
    L = _layouts()
    sin = grupos_sinnoh(mg)
    celulas = []
    por = collections.Counter()
    uso_andavel = collections.Counter()
    objetos = collections.Counter()
    total = 0
    vistos = set()
    for g in sin:
        for m in mg[g]:
            j = json.load(open(os.path.join(RAIZ, "data/maps", m, "map.json")))
            l = L[j["layout"]]
            pri, sec = l["primary_tileset"], l["secondary_tileset"]
            npri = 640 if l.get("layout_version") in ("johto", "frlg") else 512
            W, H = l["width"], l["height"]
            try:
                grade = struct.unpack("<%dH" % (W * H), open(os.path.join(RAIZ, l["blockdata_filepath"]), "rb").read())
            except (OSError, struct.error):
                continue

            def chave(mid):
                return (pri, mid) if mid < npri else (sec, mid - npri)

            for o in j.get("object_events", []):
                x, y = o.get("x"), o.get("y")
                if isinstance(x, int) and isinstance(y, int) and 0 <= x < W and 0 <= y < H:
                    k = chave(grade[y * W + x] & 0x3FF)
                    if k[0] in exclusivos:
                        objetos[k] += 1
            if l["id"] in vistos:
                continue
            vistos.add(l["id"])
            for y in range(H):
                for x in range(W):
                    v = grade[y * W + x]
                    if (v >> 10) & 3 or PRIORIDADE[v >> 12] != 2:
                        continue
                    total += 1
                    kp = chave(v & 0x3FF)
                    if kp[0] in exclusivos and camada_de(pri, sec, v & 0x3FF, npri) in (NORMAL, SPLIT):
                        uso_andavel[kp] += 1
                    if y == 0:
                        continue
                    n = grade[(y - 1) * W + x]
                    if not (n >> 10) & 3:
                        continue
                    mid = n & 0x3FF
                    k = chave(mid)
                    if k[0] not in exclusivos:
                        continue
                    if camada_de(pri, sec, mid, npri) not in (NORMAL, SPLIT):
                        continue
                    quads = _quadrantes(pri, sec, mid, npri, npri)
                    if quads and _tem_arte(quads, 1):
                        celulas.append((m, x, y - 1, k[0], k[1]))
                        por[k] += 1
    return celulas, por, uso_andavel, objetos, total


def plano():
    exclusivos = tilesets_exclusivos()
    celulas, por, uso, objs, total = varre(exclusivos)
    troca, conflito = [], []
    for k in sorted(por):
        motivo = []
        if uso[k]:
            motivo.append("andável em %d célula(s)" % uso[k])
        if objs[k]:
            motivo.append("objeto em %d célula(s)" % objs[k])
        if motivo and por[k] < uso[k]:
            conflito.append((k, por[k], ", ".join(motivo)))
        else:
            troca.append(k)
    return exclusivos, celulas, por, troca, conflito, total


def _bottom_vazio(quads, q):
    e, t = quads[q]
    return t is None or not any(c for linha in t for c in linha)


def prepara(troca):
    """Decide, sem gravar, o que cada metatile precisa para virar COVERED.

    Devolve (ok, emendas, recusados). `emendas` são quadrantes de BAIXO
    totalmente transparentes que passam a apontar para 0x3014, o MESMO lixo que o
    tipo NORMAL desenha no BG3: assim o pixel que antes mostrava o lixo continua
    mostrando o lixo. Metatile cujo quadrante de baixo é só PARCIALMENTE
    transparente sobre lixo visível não tem conserto exato e é recusado.
    """
    ok, emendas, recusados = [], [], []
    for rot, loc in troca:
        r = rotulos()[rot]
        mid = loc + 512 if r["secundario"] else loc
        par = _par_de_exemplo(rot)
        if desenho_igual_como_covered(par[0], par[1], mid, 512, 512):
            ok.append((rot, loc))
            continue
        quads = _quadrantes(par[0], par[1], mid, 512, 512)
        lixo = _tile(tileset(par[0]), tileset(par[1]), 0x14, 512)
        precisa, possivel = [], True
        for q in range(4):
            qx, qy = (q % 2) * 8, (q // 2) * 8
            diverge = any(not _pixel(quads, 0, qx + x, qy + y) and not _pixel(quads, 1, qx + x, qy + y)
                          and lixo and lixo[y][x] for x in range(8) for y in range(8))
            if not diverge:
                continue
            if _bottom_vazio(quads, q):
                precisa.append(q)
            else:
                possivel = False
        if possivel:
            ok.append((rot, loc))
            emendas.extend((rot, loc, q) for q in precisa)
        else:
            recusados.append((rot, loc))
    return ok, emendas, recusados


def aplica(troca):
    """Grava COVERED (e as emendas de lixo) só depois de decidir tudo."""
    ok, emendas, recusados = prepara(troca)
    for rot, loc in recusados:
        print("   recusado (desenho parado mudaria): %s 0x%03x" % (rot, loc))
    por_rotulo = collections.defaultdict(list)
    for rot, loc in ok:
        por_rotulo[rot].append(loc)
    mudou = 0
    for rot, locs in sorted(por_rotulo.items()):
        caminho = os.path.join(RAIZ, rotulos()[rot]["atributos"])
        b = bytearray(open(caminho, "rb").read())
        for loc in locs:
            v = struct.unpack_from("<H", b, loc * 2)[0]
            novo = (v & 0x0FFF) | (COVERED << 12)
            if novo != v:
                struct.pack_into("<H", b, loc * 2, novo)
                mudou += 1
        open(caminho, "wb").write(bytes(b))
    por_mt = collections.defaultdict(list)
    for rot, loc, q in emendas:
        por_mt[rot].append((loc, q))
    for rot, lista in sorted(por_mt.items()):
        caminho = os.path.join(RAIZ, rotulos()[rot]["metatiles"])
        b = bytearray(open(caminho, "rb").read())
        for loc, q in lista:
            struct.pack_into("<H", b, loc * 16 + q * 2, 0x3014)
        open(caminho, "wb").write(bytes(b))
    _CACHE.clear()
    print("emendas de lixo 0x3014: %d quadrante(s)" % len(emendas))
    return mudou


_PARES = None


def _par_de_exemplo(rot):
    """Um (primário, secundário) real em que o rótulo aparece, para resolver tile."""
    global _PARES
    if _PARES is None:
        _PARES = {}
        for l in _layouts().values():
            for t in (l["primary_tileset"], l["secondary_tileset"]):
                _PARES.setdefault(t, (l["primary_tileset"], l["secondary_tileset"]))
    return _PARES[rot]


def main():
    exclusivos, celulas, por, troca, conflito, total = plano()
    print("tilesets exclusivos de Sinnoh com atributo próprio: %d" % len(exclusivos))
    print("células andáveis (prioridade 2) em Sinnoh: %d" % total)
    print("cabeça tampada: %d células, %d metatiles" % (len(celulas), len(por)))
    print("metatiles a trocar para COVERED: %d (%d células)" % (len(troca), sum(por[k] for k in troca)))
    print("conflitos que ficam (andáveis em mais células do que tampam): %d (%d células)" % (len(conflito), sum(c for _, c, _ in conflito)))
    for (rot, loc), c, motivo in sorted(conflito, key=lambda z: -z[1]):
        ex = next(e for e in celulas if (e[3], e[4]) == (rot, loc))
        print("   %-26s 0x%03x  %4d célula(s)  %s  ex. %s (%d,%d)" % (rot, loc, c, motivo, ex[0], ex[1], ex[2]))
    if "--aplicar" in sys.argv:
        print("atributos gravados: %d" % aplica(troca))
        return 0
    if "--verifica" in sys.argv:
        return 1 if troca else 0
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
