#!/usr/bin/env python3
"""De-para dos metatiles que o Pokémon Emerald EX REDEFINIU, para a NOSSA arte do Blazing.

Contexto (frente Hoenn EX, onda 1, PLANO-HOENN-EX.md seção a.3; decisão do Fable
no checkpoint da onda 0, item 4): a planta do EX usa o índice de metatile do
Emerald vanilla, o mesmo que a nossa Hoenn repintada pelo Blazing preservou
(ESTADO 0.af). Então um `map.bin` copiado do EX renderiza com a nossa arte, com
uma exceção: metatiles que o autor do EX REDEFINIU no tileset dele (mesmo índice,
desenho outro). Nessas células o nosso tileset desenha o metatile VANILLA, e o
mapa sai com casa virando lixo (Lavaridge, 76) ou buraco (Fallarbor, 17).

O QUE ESTA FERRAMENTA FAZ, para UM mapa do EX e o NOSSO par de tilesets:

1. Acha os metatiles usados no mapa do EX cuja definição no EX difere da vanilla
   (ou cujo índice nem existe no vanilla, ou que apontam para tile que o EX mudou).
2. Traduz cada definição do EX para o nosso par, entrada a entrada:
   - tile do EX IGUAL a um tile vanilla (mesmo índice, ou outro índice, com ou sem
     espelhamento) = usa o NOSSO tile correspondente, isto é, a arte do Blazing.
     O correspondente é achado por VOTO sobre os metatiles vanilla x nossos no
     mesmo índice (medido em 23/09/2026: o Blazing preserva o índice de tile em
     ~90% das entradas, e não em 100%; o voto pega os 10% que ele moveu);
   - tile do EX TRANSPARENTE = tile 0 (regra do método §3.1: o tile 0 é vazio);
   - tile do EX NOVO = entra numa vaga LIVRE de tile do NOSSO secundário, com os
     índices de cor traduzidos para a paleta vanilla do mesmo slot (a nossa paleta
     daquele slot é a repintura do Blazing da vanilla, então a cor sai no estilo do
     Blazing). Cor sem par exato vira a mais próxima, e a distância é impressa.
3. Instala a definição traduzida numa vaga LIVRE de metatile do NOSSO secundário,
   ACIMA da contagem que usamos (nenhum metatile existente muda), com o ATRIBUTO
   do EX. Redefinição de metatile do PRIMÁRIO também vai para o secundário do mapa:
   o `general` é de 243 mapas e NÃO se mexe. Definição traduzida idêntica a uma
   que já existe no nosso secundário (inclusive a instalada por outro mapa irmão)
   é REUSADA: a ferramenta é idempotente.
4. Reescreve os índices no `map.bin` do layout, SÓ nas células cujo metatile ainda
   é o do EX naquela posição (célula que o executor mexeu depois fica como está).

A RECUSA: se o secundário não tem vaga de metatile ou de tile para o que o mapa
pede, a ferramenta não escreve NADA e diz quantas vagas faltam (exit 2). Não
inventa saída: quem decide é o condutor.

Vagas livres de TILE: índices de `-num_tiles` até 512 primeiro (o `-num_tiles`
de graphics.h é acertado junto), depois tiles dentro do PNG que nenhum metatile
do secundário (nem do primário) referencia e que nenhuma animação do tileset
escreve (`src/tileset_anims.c`).

VAGA REUSADA (`--vagas 510,511,2`, decisão do condutor de 23/09/2026 para o
Mauville, que usa 510 de 512): vaga DENTRO da nossa contagem que nenhum layout
usa. Nunca escolhida sozinha: só a lista dada, e cada uma é conferida (não é a 0,
não está em map.bin nem border.bin de layout do secundário, não é METATILE_*
citado, não é número cru em src/field_door.c); falhou, recusa.

A PROVA (`--prova <pasta>`): renderiza o layout depois do de-para, o mapa do EX
com a arte do EX, e TODOS os layouts irmãos que dividem o secundário antes e
depois (exige 0 pixel de mudança), e conta os buracos: célula que o EX desenha e
a nossa deixa só com o fundo.

Uso:
    python3 dev_scripts/depara_metatiles_ex.py --ex 0.13 --layout LAYOUT_LAVARIDGE_TOWN
    python3 dev_scripts/depara_metatiles_ex.py --ex 0.13 --layout LAYOUT_LAVARIDGE_TOWN --aplicar --prova <pasta>
    python3 dev_scripts/depara_metatiles_ex.py --autoteste

`--repo` troca a árvore alvo (padrão: a deste script). O `map.bin` do layout tem
de estar no TAMANHO do mapa do EX (a planta já copiada, `copia_planta_ex.py`);
senão a ferramenta recusa.

Fonte do EX (PRIVADA, nunca entra no repositório): a ROM e o inventário em
fontes-mapas/romhacks/emerald-ex, lidos pelo `gbamap.py`; o decomp vanilla em
fontes-mapas/pokeemerald.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FM = os.environ.get("FONTES_MAPAS", "/Users/duarte/Projetos/pokemon-claude/fontes-mapas")
EX_DIR = os.path.join(FM, "romhacks/emerald-ex")
EX_ROM = os.path.join(EX_DIR, "pokemon-emerald-ex-1.0.4.gba")
EX_INV = os.path.join(FM, "romhacks/ferramentas/inv/emerald-ex.json")
VAN = os.path.join(FM, "pokeemerald")

N_META_PRI = 512
N_TILES_PRI = 512
N_PAL_PRI = 6
N_PAL_TOTAL = 13


# ---------------------------------------------------------------- utilidades

def u16s(b):
    return list(struct.unpack(f"<{len(b)//2}H", b))


def png_para_4bpp(caminho):
    """Lista de tiles 4bpp (32 B cada), na ordem da tira do PNG."""
    from PIL import Image
    im = Image.open(caminho)
    if im.mode != "P":
        raise ValueError(f"{caminho}: PNG não indexado ({im.mode})")
    w, h = im.size
    px = im.load()
    out = []
    for ty in range(h // 8):
        for tx in range(w // 8):
            b = bytearray()
            for y in range(8):
                for x in range(0, 8, 2):
                    a = px[tx*8 + x, ty*8 + y] & 0xF
                    c = px[tx*8 + x + 1, ty*8 + y] & 0xF
                    b.append(a | (c << 4))
            out.append(bytes(b))
    return out


def tile_pixels(t):
    return [[(t[y*4 + (x >> 1)] >> (4 * (x & 1))) & 0xF for x in range(8)] for y in range(8)]


def pixels_tile(p):
    b = bytearray()
    for y in range(8):
        for x in range(0, 8, 2):
            b.append((p[y][x] & 0xF) | ((p[y][x+1] & 0xF) << 4))
    return bytes(b)


def espelha(t, hf, vf):
    if not hf and not vf:
        return t
    p = tile_pixels(t)
    if hf:
        p = [row[::-1] for row in p]
    if vf:
        p = p[::-1]
    return pixels_tile(p)


def le_pal_jasc(caminho):
    linhas = [l.strip() for l in open(caminho, encoding="utf-8") if l.strip()]
    return [tuple(int(v) for v in l.split()) for l in linhas[3:19]]


def rgb_de_gba(c):
    return ((c & 31) << 3, ((c >> 5) & 31) << 3, ((c >> 10) & 31) << 3)


def quantiza(rgb):
    """Cor de 8 bits do .pal para a grade de 5 bits do GBA (é o que o gbagfx faz)."""
    return tuple((v >> 3) << 3 for v in rgb)


# ---------------------------------------------------------------- nossa árvore

class Arvore:
    def __init__(self, repo):
        self.repo = repo
        self.gh_path = os.path.join(repo, "src/data/tilesets/graphics.h")
        self.layouts_path = os.path.join(repo, "data/layouts/layouts.json")
        self._pastas = None

    def layouts(self):
        return json.load(open(self.layouts_path, encoding="utf-8"))["layouts"]

    def layout(self, lid):
        for l in self.layouts():
            if l and l.get("id") == lid:
                return l
        raise SystemExit(f"layout {lid} não existe em {self.layouts_path}")

    def pastas(self):
        """rótulo gTileset_X -> pasta em disco (mesma regra do render_maps.py)."""
        if self._pastas is None:
            os.environ["REPO_MAPAS"] = self.repo
            sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
            import importlib
            import render_maps
            render_maps = importlib.reload(render_maps)
            self._pastas = {("gTileset_" + k): v for k, v in render_maps.carregar_mapa_de_pastas_tileset().items()}
        return self._pastas

    def pasta(self, rotulo):
        p = self.pastas().get(rotulo)
        if not p:
            raise SystemExit(f"tileset {rotulo} não achado em graphics.h/graphics.c")
        return p

    def num_tiles(self, pasta):
        """-num_tiles declarado em graphics.h para a pasta (ou None)."""
        rel = os.path.relpath(pasta, self.repo)
        for ln in open(self.gh_path, encoding="utf-8"):
            if f'"{rel}/tiles.png"' in ln:
                m = re.search(r"-num_tiles (\d+)", ln)
                return int(m.group(1)) if m else None
        return None

    def acerta_num_tiles(self, pasta, n):
        rel = os.path.relpath(pasta, self.repo)
        txt = open(self.gh_path, encoding="utf-8").read().split("\n")
        feito = False
        for i, ln in enumerate(txt):
            if f'"{rel}/tiles.png"' in ln:
                if "-num_tiles" in ln:
                    txt[i] = re.sub(r"-num_tiles \d+", f"-num_tiles {n}", ln)
                else:
                    txt[i] = ln.replace('".4bpp.fastSmol");', f'".4bpp.fastSmol", "-num_tiles {n} -Wnum_tiles");')
                feito = True
        if not feito:
            raise SystemExit(f"linha de tiles de {rel} não achada em graphics.h")
        open(self.gh_path, "w", encoding="utf-8").write("\n".join(txt))


def destinos_anim(repo, rotulo):
    """Tiles do secundário que alguma animação do tileset escreve (conservador:
    toda animação cujo nome começa pelo nome do tileset)."""
    nome = rotulo.replace("gTileset_", "")
    txt = open(os.path.join(repo, "src/tileset_anims.c"), encoding="utf-8").read()
    out = set()
    for m in re.finditer(r"gTilesetAnims_(\w+?)_\w*\[i\],\s*\(u16 \*\)\(BG_VRAM \+ TILE_OFFSET_4BPP\(NUM_TILES_IN_PRIMARY \+ (\d+)\)\),\s*(\d+) \* TILE_SIZE_4BPP", txt):
        if m.group(1) == nome or m.group(1).startswith(nome + "_") or nome.startswith(m.group(1)):
            base, n = int(m.group(2)), int(m.group(3))
            out |= set(range(base, base + n))
    # tabelas de destino (listas de ponteiros) perto do nome do tileset
    for m in re.finditer(r"(\w+)\[\] = \{([^}]*NUM_TILES_IN_PRIMARY[^}]*)\}", txt):
        if nome.lower() in m.group(1).lower():
            for d in re.findall(r"NUM_TILES_IN_PRIMARY \+ (\d+)", m.group(2)):
                out |= set(range(int(d), int(d) + 4))
    return out


# rótulo nosso -> rótulo do decomp vanilla, quando o nome mudou aqui
APELIDO_VANILLA = {"Building": "InsideBuilding"}


def nosso_rotulo(rot):
    n = rot.replace("gTileset_", "")
    return APELIDO_VANILLA.get(n, n)


# ---------------------------------------------------------------- o EX

class Ex:
    def __init__(self):
        sys.path.insert(0, os.path.join(FM, "romhacks/ferramentas"))
        from gbamap import Rom
        self.r = Rom(EX_ROM)
        self.inv = json.load(open(EX_INV))
        self._ts = {}

    def mapa(self, gm):
        g, m = (int(x) for x in gm.split("."))
        for gr in self.inv["grupos"]:
            if gr["g"] == g:
                if m < len(gr["mapas"]) and gr["mapas"][m]:
                    return gr["mapas"][m]
        raise SystemExit(f"mapa {gm} não existe no inventário do EX")

    def ts(self, off):
        if off not in self._ts:
            self._ts[off] = self.r.parse_tileset(off)
        return self._ts[off]

    def blocos(self, hdr):
        L = hdr["layout"]
        return u16s(self.r.rom[L["blockdata"]:L["blockdata"] + 2*L["w"]*L["h"]])

    def tiles(self, t):
        raw = t["tiles"]
        return [raw[i*32:(i+1)*32] for i in range(len(raw)//32)]

    def pal(self, t, slot):
        return [rgb_de_gba(c) for c in struct.unpack_from("<16H", t["pal"], slot*32)]


class Vanilla:
    def __init__(self):
        gh = open(os.path.join(VAN, "src/data/tilesets/metatiles.h")).read()
        self.meta_path = dict(re.findall(r'gMetatiles_(\w+)\[\] = INCBIN_U16\("(data/tilesets/[^"]+)/metatiles.bin"\)', gh))
        self._c = {}

    def rotulos(self, secundario):
        k = "secondary" if secundario else "primary"
        return [n for n, p in self.meta_path.items() if f"/{k}/" in p]

    def carrega(self, nome):
        if nome not in self._c:
            pasta = os.path.join(VAN, self.meta_path[nome])
            pals = {}
            pp = os.path.join(pasta, "palettes")
            for f in os.listdir(pp):
                m = re.match(r"^(\d\d)\.pal$", f)
                if m:
                    pals[int(m.group(1))] = [quantiza(c) for c in le_pal_jasc(os.path.join(pp, f))]
            self._c[nome] = {
                "nome": nome, "pasta": pasta,
                "meta": open(os.path.join(pasta, "metatiles.bin"), "rb").read(),
                "attr": open(os.path.join(pasta, "metatile_attributes.bin"), "rb").read(),
                "tiles": png_para_4bpp(os.path.join(pasta, "tiles.png")),
                "pals": pals,
            }
        return self._c[nome]

    def melhor(self, ex_meta, secundario, usados=None):
        """Rótulo vanilla cujo metatiles.bin mais bate com o do EX (nos índices usados)."""
        melhor = (-1, None)
        for n in self.rotulos(secundario):
            v = open(os.path.join(VAN, self.meta_path[n], "metatiles.bin"), "rb").read()
            idx = usados if usados is not None else range(len(v)//16)
            s = sum(1 for i in idx if i*16 + 16 <= len(v) and v[i*16:i*16+16] == ex_meta[i*16:i*16+16])
            if s > melhor[0]:
                melhor = (s, n)
        return melhor[1]


# ---------------------------------------------------------------- o de-para

def voto_tiles(v_pri, v_sec, o_pri_meta, o_sec_meta):
    """(tile vanilla, paleta vanilla) -> (tile nosso, xor de espelho, paleta nossa),
    por voto sobre os metatiles vanilla x nossos no MESMO índice."""
    votos = collections.defaultdict(collections.Counter)
    for vm, om in ((v_pri["meta"], o_pri_meta), (v_sec["meta"], o_sec_meta)):
        n = min(len(vm), len(om)) // 16
        for i in range(n):
            a = u16s(vm[i*16:i*16+16])
            b = u16s(om[i*16:i*16+16])
            for va, vb in zip(a, b):
                votos[(va & 0x3FF, va >> 12)][(vb & 0x3FF, ((va ^ vb) >> 10) & 3, vb >> 12)] += 1
    por_tile = collections.defaultdict(collections.Counter)
    for (t, p), c in votos.items():
        for k, n in c.items():
            por_tile[t][k] += n
    return votos, por_tile


def analisa(ex, van, arv, gm, lid, verbose=True, vagas_extra=None):
    hdr = ex.mapa(gm)
    L = hdr["layout"]
    w, h = L["w"], L["h"]
    blocos = ex.blocos(hdr)
    t1, t2 = ex.ts(L["ts1"]), ex.ts(L["ts2"])
    usados = sorted({b & 0x3FF for b in blocos})
    usados_sec = [m - N_META_PRI for m in usados if m >= N_META_PRI]
    lay = arv.layout(lid)
    rot_pri, rot_sec = lay["primary_tileset"], lay["secondary_tileset"]
    vn1 = van.melhor(t1["meta"], False)
    if usados_sec:
        vn2 = van.melhor(t2["meta"], True, [i for i in usados_sec if i < 1024])
    else:
        # o mapa do EX não usa NENHUM metatile do secundário (medido: Route 130):
        # o secundário não entra na conta, e vale o do nosso layout
        vn2 = rot_sec.replace("gTileset_", "")
        if vn2 not in van.meta_path:
            vn2 = van.melhor(t2["meta"], True)
    v1, v2 = van.carrega(vn1), van.carrega(vn2)
    if nosso_rotulo(rot_sec) != vn2 or nosso_rotulo(rot_pri) != vn1:
        raise SystemExit(f"RECUSA: o mapa {gm} do EX usa o par vanilla ({vn1}, {vn2}) e o nosso layout "
                         f"{lid} usa ({rot_pri}, {rot_sec}). O de-para só vale no par equivalente.")
    p_pri, p_sec = arv.pasta(rot_pri), arv.pasta(rot_sec)
    o_pri_meta = open(os.path.join(p_pri, "metatiles.bin"), "rb").read()
    o_sec_meta = open(os.path.join(p_sec, "metatiles.bin"), "rb").read()
    o_sec_attr = open(os.path.join(p_sec, "metatile_attributes.bin"), "rb").read()
    o_sec_tiles = png_para_4bpp(os.path.join(p_sec, "tiles.png"))

    ex_t1, ex_t2 = ex.tiles(t1), ex.tiles(t2)

    def ex_tile(t):
        if t < N_TILES_PRI:
            return ex_t1[t] if t < len(ex_t1) else None
        t -= N_TILES_PRI
        return ex_t2[t] if t < len(ex_t2) else None

    def van_tile(t):
        if t < N_TILES_PRI:
            return v1["tiles"][t] if t < len(v1["tiles"]) else None
        t -= N_TILES_PRI
        return v2["tiles"][t] if t < len(v2["tiles"]) else None

    def ex_def(m):
        if m < N_META_PRI:
            return t1["meta"][m*16:m*16+16], struct.unpack_from("<H", t1["attr"], m*2)[0]
        k = m - N_META_PRI
        return t2["meta"][k*16:k*16+16], struct.unpack_from("<H", t2["attr"], k*2)[0]

    def van_def(m):
        if m < N_META_PRI:
            v, k = v1, m
        else:
            v, k = v2, m - N_META_PRI
        if k*16 + 16 > len(v["meta"]):
            return None, None
        return v["meta"][k*16:k*16+16], struct.unpack_from("<H", v["attr"], k*2)[0]

    # 1. quais metatiles o EX redefiniu (entre os usados no mapa)
    redef = {}
    for m in usados:
        d, a = ex_def(m)
        vd, va = van_def(m)
        motivo = None
        if vd is None:
            motivo = "sem par vanilla"
        elif d != vd:
            motivo = "definição"
        else:
            for e in u16s(d):
                t = e & 0x3FF
                if t and ex_tile(t) is not None and ex_tile(t) != van_tile(t):
                    motivo = "tile mudado"
                    break
        if motivo:
            redef[m] = {"motivo": motivo, "def": d, "attr": a, "attr_vanilla": va}

    # 2. dicionário de tiles vanilla (com espelho) -> índice vanilla
    vt_idx = {}
    for base, lista in ((0, v1["tiles"]), (N_TILES_PRI, v2["tiles"])):
        for i, t in enumerate(lista):
            for hf in (0, 1):
                for vf in (0, 1):
                    vt_idx.setdefault(espelha(t, hf, vf), (base + i, hf | (vf << 1)))
    votos, por_tile = voto_tiles(v1, v2, o_pri_meta, o_sec_meta)

    def nosso_de_vanilla(tv, flip, pal):
        """tile vanilla tv (+espelho, paleta) -> entrada nossa."""
        c = votos.get((tv, pal))
        if c:
            (to, fx, po), _ = c.most_common(1)[0]
        elif por_tile.get(tv):
            (to, fx, _), _ = por_tile[tv].most_common(1)[0]
            po = pal
        else:
            to, fx, po = tv, 0, pal
        return to, flip ^ fx, po

    # 3. vagas
    n_sec = len(o_sec_meta) // 16
    vagas_meta = list(range(n_sec, N_META_PRI))
    if vagas_extra:
        vagas_meta += confere_vagas_reusadas(arv, rot_sec, vagas_extra, n_sec)
    num_tiles = arv.num_tiles(p_sec) or len(o_sec_tiles)
    ref = set()
    for mm in (o_sec_meta, o_pri_meta):
        for e in u16s(mm):
            if (e & 0x3FF) >= N_TILES_PRI:
                ref.add((e & 0x3FF) - N_TILES_PRI)
    anim = destinos_anim(arv.repo, rot_sec)
    vagas_tile = list(range(num_tiles, N_TILES_PRI))
    vagas_tile += [i for i in range(1, min(num_tiles, len(o_sec_tiles))) if i not in ref and i not in anim]

    # 4. tradução
    novos_tiles = {}          # bytes -> índice local no secundário (novo)
    existentes = {}
    for i, t in enumerate(o_sec_tiles[:num_tiles]):
        for hf in (0, 1):
            for vf in (0, 1):
                existentes.setdefault(espelha(t, hf, vf), (i, hf | (vf << 1)))
    dist_cor = []
    traduz = {}
    for m, R in sorted(redef.items()):
        ents = []
        for e in u16s(R["def"]):
            t, flip, pal = e & 0x3FF, (e >> 10) & 3, e >> 12
            tb = ex_tile(t)
            if t == 0 or tb is None or tb == bytes(32):
                ents.append(("zero", 0, flip, pal))
                continue
            if tb in vt_idx:
                tv, fv = vt_idx[tb]
                to, fo, po = nosso_de_vanilla(tv, fv ^ flip, pal)
                ents.append(("nosso", to, fo, po))
                continue
            # tile novo do EX: cor para a paleta vanilla do mesmo slot
            exp = ex.pal(t1 if pal < N_PAL_PRI else t2, pal)
            vp = (v1 if pal < N_PAL_PRI else v2)["pals"].get(pal)
            px = tile_pixels(tb)
            mapa_cor, pior = {}, 0
            for c in {v for row in px for v in row}:
                if c == 0:
                    mapa_cor[0] = 0
                    continue
                alvo = exp[c]
                if vp and vp[c] == alvo:
                    mapa_cor[c] = c
                    continue
                cands = [(sum((a - b) ** 2 for a, b in zip(alvo, vp[j])), j) for j in range(1, 16)] if vp else [(0, c)]
                d, j = min(cands)
                mapa_cor[c] = j
                pior = max(pior, d)
            nb = pixels_tile([[mapa_cor[v] for v in row] for row in px])
            if pior:
                dist_cor.append((m, pal, round(pior ** 0.5, 1)))
            ents.append(("novo", nb, flip, pal))
        traduz[m] = ents

    # tiles novos distintos (considerando espelho e os que já existem)
    precisa_tiles = []
    vistos = {}
    for m, ents in traduz.items():
        for k, e in enumerate(ents):
            if e[0] != "novo":
                continue
            nb = e[1]
            if nb in existentes or nb in vistos:
                continue
            achou = False
            for hf in (0, 1):
                for vf in (0, 1):
                    if espelha(nb, hf, vf) in vistos:
                        achou = True
            if not achou:
                vistos[nb] = len(precisa_tiles)
                precisa_tiles.append(nb)

    rel = {
        "ex": gm, "layout": lid, "tamanho_ex": [w, h],
        "par_vanilla": [vn1, vn2], "par_nosso": [rot_pri, rot_sec],
        "usados": len(usados), "redefinidos": len(redef),
        "celulas_redefinidas": sum(1 for b in blocos if (b & 0x3FF) in redef),
        "por_motivo": dict(collections.Counter(R["motivo"] for R in redef.values())),
        "tiles_novos": len(precisa_tiles),
        "vagas_meta": len(vagas_meta), "vagas_tile": len(vagas_tile),
        "metatiles_nossos": n_sec, "num_tiles": num_tiles,
        "cor_aproximada": dist_cor,
        "attr_ex_diferente_vanilla": sorted(m for m, R in redef.items() if R["attr_vanilla"] is not None and R["attr"] != R["attr_vanilla"]),
    }
    ctx = dict(hdr=hdr, blocos=blocos, redef=redef, traduz=traduz, precisa_tiles=precisa_tiles,
               vagas_meta=vagas_meta, vagas_tile=vagas_tile, existentes=existentes,
               p_sec=p_sec, o_sec_meta=o_sec_meta, o_sec_attr=o_sec_attr, o_sec_tiles=o_sec_tiles,
               num_tiles=num_tiles, lay=lay, rot_sec=rot_sec)
    return rel, ctx


def confere_vagas_reusadas(arv, rot_sec, vagas, n_sec):
    """Vaga DENTRO da nossa contagem, dada à mão pelo condutor (--vagas). Só passa
    se nenhum layout do secundário a usa (map.bin e border.bin), se nenhum
    METATILE_* do secundário a cita, se não é a 0 e se não aparece como número cru
    em src/field_door.c. Qualquer falha é RECUSA (não escolhe outra sozinha)."""
    ruins = []
    usadas = set()
    for l in arv.layouts():
        if not l or l.get("secondary_tileset") != rot_sec:
            continue
        for chave in ("blockdata_filepath", "border_filepath"):
            p = os.path.join(arv.repo, l.get(chave, ""))
            if os.path.isfile(p):
                usadas |= {(v & 0x3FF) - N_META_PRI for v in u16s(open(p, "rb").read()) if (v & 0x3FF) >= N_META_PRI}
    nome = rot_sec.replace("gTileset_", "")
    rotulos = set()
    lab = os.path.join(arv.repo, "include/constants/metatile_labels.h")
    if os.path.exists(lab):
        for m in re.finditer(r"#define METATILE_" + nome + r"_\w+\s+(0x[0-9A-Fa-f]+)", open(lab).read()):
            rotulos.add(int(m.group(1), 16) - N_META_PRI)
    porta = open(os.path.join(arv.repo, "src/field_door.c")).read() if os.path.exists(os.path.join(arv.repo, "src/field_door.c")) else ""
    extra = []
    for v in vagas:
        if n_sec <= v < N_META_PRI:
            continue          # acima da contagem: já é vaga livre, entra pela lista normal
        extra.append(v)
        if v <= 0 or v >= n_sec:
            ruins.append(f"{v} (fora de 1..{n_sec - 1})")
        elif v in usadas:
            ruins.append(f"{v} (usada em map.bin/border.bin)")
        elif v in rotulos:
            ruins.append(f"{v} (citada por METATILE_{nome}_*)")
        elif re.search(r"\b(0x%X|0x%x|%d)\b" % (v + N_META_PRI, v + N_META_PRI, v + N_META_PRI), porta):
            ruins.append(f"{v} (número cru em field_door.c)")
    if ruins:
        raise SystemExit("RECUSA: vaga reusada inválida: " + ", ".join(ruins))
    return extra


def monta(ctx):
    """Aloca tiles e metatiles e devolve o que escrever. Não escreve nada."""
    existentes = dict(ctx["existentes"])
    vagas_tile = list(ctx["vagas_tile"])
    novos_tiles = {}   # índice local -> bytes
    for nb in ctx["precisa_tiles"]:
        i = vagas_tile.pop(0)
        novos_tiles[i] = nb
        for hf in (0, 1):
            for vf in (0, 1):
                existentes.setdefault(espelha(nb, hf, vf), (i, hf | (vf << 1)))
    meta = bytearray(ctx["o_sec_meta"])
    attr = bytearray(ctx["o_sec_attr"])
    vagas = list(ctx["vagas_meta"])
    n_orig = len(meta) // 16
    defs = {}
    for k in range(len(meta) // 16):
        defs.setdefault((bytes(meta[k*16:k*16+16]), struct.unpack_from("<H", attr, k*2)[0]), k)
    remap = {}
    novos_meta = []
    for m, ents in sorted(ctx["traduz"].items()):
        ws = []
        for tipo, v, flip, pal in ents:
            if tipo == "zero":
                ws.append(0 | (flip << 10) | (pal << 12))
            elif tipo == "nosso":
                ws.append((v & 0x3FF) | (flip << 10) | (pal << 12))
            else:
                i, fx = existentes[v]
                ws.append((N_TILES_PRI + i) | ((flip ^ fx) << 10) | (pal << 12))
        d = struct.pack("<8H", *ws)
        a = ctx["redef"][m]["attr"]
        k = defs.get((d, a))
        if k is None:
            if not vagas:
                raise SystemExit("RECUSA: acabou vaga de metatile")
            k = vagas.pop(0)
            if k == len(meta) // 16:
                meta += d
                attr += struct.pack("<H", a)
            elif k < len(meta) // 16:
                meta[k*16:k*16+16] = d
                struct.pack_into("<H", attr, k*2, a)
            else:
                raise SystemExit(f"RECUSA: vaga {k} deixaria buraco na tabela de metatiles")
            defs[(d, a)] = k
            novos_meta.append(k)
        remap[m] = N_META_PRI + k
    return dict(novos_tiles=novos_tiles, meta=bytes(meta), attr=bytes(attr), remap=remap,
                novos_meta=novos_meta, n_orig=n_orig)


def escreve(arv, ctx, plano, mapbin_path):
    from PIL import Image
    p_sec = ctx["p_sec"]
    # tiles
    if plano["novos_tiles"]:
        png = os.path.join(p_sec, "tiles.png")
        im = Image.open(png)
        w, h = im.size
        cols = w // 8
        maior = max(plano["novos_tiles"])
        precisa_h = ((maior // cols) + 1) * 8
        if precisa_h > h:
            novo = Image.new("P", (w, precisa_h), 0)
            novo.putpalette(im.getpalette())
            novo.paste(im, (0, 0))
            if "transparency" in im.info:
                novo.info["transparency"] = im.info["transparency"]
            im = novo
        px = im.load()
        for i, nb in plano["novos_tiles"].items():
            p = tile_pixels(nb)
            x0, y0 = (i % cols) * 8, (i // cols) * 8
            for y in range(8):
                for x in range(8):
                    px[x0 + x, y0 + y] = p[y][x]
        im.save(png, **({"transparency": im.info["transparency"]} if "transparency" in im.info else {}))
        n = max(ctx["num_tiles"], maior + 1)
        if n != ctx["num_tiles"]:
            arv.acerta_num_tiles(p_sec, n)
    open(os.path.join(p_sec, "metatiles.bin"), "wb").write(plano["meta"])
    open(os.path.join(p_sec, "metatile_attributes.bin"), "wb").write(plano["attr"])
    # map.bin
    blocos = ctx["blocos"]
    atual = u16s(open(mapbin_path, "rb").read())
    trocadas = 0
    for i, (b_ex, b_nos) in enumerate(zip(blocos, atual)):
        m = b_ex & 0x3FF
        if m in plano["remap"] and (b_nos & 0x3FF) == m:
            atual[i] = (b_nos & ~0x3FF) | plano["remap"][m]
            trocadas += 1
    open(mapbin_path, "wb").write(struct.pack(f"<{len(atual)}H", *atual))
    return trocadas


# ---------------------------------------------------------------- render e prova

def render_layout(arv, lay, cache):
    os.environ["REPO_MAPAS"] = arv.repo
    import render_maps
    from PIL import Image
    w, h = lay["width"], lay["height"]
    mb = open(os.path.join(arv.repo, lay["blockdata_filepath"]), "rb").read()
    for k in (lay["primary_tileset"], lay["secondary_tileset"]):
        if k not in cache:
            pasta = arv.pasta(k)
            render_maps._MAPA_TILESETS[k.replace("gTileset_", "")] = pasta
            cache[k] = render_maps.carregar_tileset(k)
    pri, sec = cache[lay["primary_tileset"]], cache[lay["secondary_tileset"]]
    fundo = pri["paletas"][0][0]
    img = Image.new("RGB", (w*16, h*16), fundo)
    px = img.load()
    buraco = []
    for i in range(w*h):
        v = struct.unpack_from("<H", mb, i*2)[0] & 0x3FF
        ts, k = (pri, v) if v < N_META_PRI else (sec, v - N_META_PRI)
        if k >= len(ts["metatiles"]) // 16:
            buraco.append(i)
            continue
        ents = render_maps.entradas_metatile(ts["metatiles"], k)
        for cam in (0, 1):
            for q in range(4):
                t, hf, vf, p = ents[cam*4 + q]
                tile = render_maps.resolver_tile(pri, sec, t)
                if tile is None:
                    continue
                cores = (pri if p < N_PAL_PRI else sec)["paletas"].get(p)
                if cores is None:
                    continue
                render_maps.desenhar_tile(px, (i % w)*16 + (q % 2)*8, (i // w)*16 + (q // 2)*8, tile, cores, hf, vf)
    return img, buraco


def celulas_vazias(img, w, h, fundo):
    px = img.load()
    out = set()
    for i in range(w*h):
        x0, y0 = (i % w)*16, (i // w)*16
        if all(px[x0 + x, y0 + y] == fundo for y in range(0, 16, 2) for x in range(0, 16, 2)):
            out.add(i)
    return out


def render_ex(ex, gm):
    sys.path.insert(0, os.path.join(FM, "romhacks/ferramentas"))
    from render_hack import Render
    return Render(ex.r).mapa(ex.mapa(gm))


def md5_img(img):
    return hashlib.md5(img.tobytes()).hexdigest()


def irmas(arv, lay):
    """Layouts que dividem o secundário (os que têm map.bin em disco; o que não
    tem é variante que aponta para arquivo inexistente e não entra no build)."""
    return [l for l in arv.layouts() if l and l.get("secondary_tileset") == lay["secondary_tileset"]
            and l["id"] != lay["id"] and os.path.exists(os.path.join(arv.repo, l["blockdata_filepath"]))]


# ---------------------------------------------------------------- CLI

def roda(gm, lid, repo=RAIZ, aplicar=False, prova=None, mapbin=None, ex=None, van=None, silencio=False, vagas=None):
    ex = ex or Ex()
    van = van or Vanilla()
    arv = Arvore(repo)
    rel, ctx = analisa(ex, van, arv, gm, lid, vagas_extra=vagas)
    lay = ctx["lay"]
    w, h = rel["tamanho_ex"]
    mapbin = mapbin or os.path.join(repo, lay["blockdata_filepath"])
    falta_m = len(set(ctx["redef"])) - len(ctx["vagas_meta"])
    falta_t = len(ctx["precisa_tiles"]) - len(ctx["vagas_tile"])
    try:
        plano = monta(ctx) if falta_t <= 0 else None
    except (IndexError, SystemExit):
        plano = None
    if plano is None or (falta_m > 0 and len(plano["novos_meta"]) > len(ctx["vagas_meta"])):
        rel["recusa"] = (f"faltam {max(falta_m, 0)} vagas de metatile (precisa até {len(ctx['redef'])}, "
                         f"livres {len(ctx['vagas_meta'])}) e {max(falta_t, 0)} de tile "
                         f"(precisa {len(ctx['precisa_tiles'])}, livres {len(ctx['vagas_tile'])})")
        if not silencio:
            print(json.dumps(rel, indent=1, ensure_ascii=False))
            print("RECUSA:", rel["recusa"], file=sys.stderr)
        return rel, 2
    rel["metatiles_instalados"] = len(plano["novos_meta"])
    rel["metatiles_reusados"] = len(plano["remap"]) - len(plano["novos_meta"])
    rel["tiles_instalados"] = len(plano["novos_tiles"])
    rel["remap"] = {str(k): v for k, v in sorted(plano["remap"].items())}
    if not aplicar:
        if not silencio:
            print(json.dumps(rel, indent=1, ensure_ascii=False))
            print("(só mediu; --aplicar escreve)", file=sys.stderr)
        return rel, 0
    tam = os.path.getsize(mapbin)
    if tam != 2*w*h:
        raise SystemExit(f"RECUSA: {mapbin} tem {tam} B e o mapa do EX pede {2*w*h} ({w}x{h}): copie a planta antes")
    antes = {}
    if prova:
        os.makedirs(prova, exist_ok=True)
        cache = {}
        for l in irmas(arv, lay):
            img, _ = render_layout(arv, l, cache)
            antes[l["id"]] = md5_img(img)
    rel["celulas_trocadas"] = escreve(arv, ctx, plano, mapbin)
    if prova:
        cache = {}
        mud = []
        for l in irmas(arv, lay):
            img, _ = render_layout(arv, l, cache)
            if md5_img(img) != antes[l["id"]]:
                mud.append(l["id"])
        rel["irmas"] = len(antes)
        rel["irmas_mudaram"] = mud
        img, fora = render_layout(arv, lay, cache)
        fundo = cache[lay["primary_tileset"]]["paletas"][0][0]
        eximg = render_ex(ex, gm)
        vaz_nos = celulas_vazias(img, w, h, fundo)
        exfundo = eximg.getpixel((0, 0))
        exp = eximg.load()
        vaz_ex = {i for i in range(w*h) if all(exp[(i % w)*16 + x, (i // w)*16 + y] == (0, 0, 0)
                                                 for y in range(0, 16, 2) for x in range(0, 16, 2))}
        rel["buracos"] = sorted(i for i in vaz_nos - vaz_ex)
        rel["metatile_fora"] = fora
        nome = lay["id"].replace("LAYOUT_", "")
        img.save(os.path.join(prova, f"{nome}-depara.png"))
        eximg.save(os.path.join(prova, f"{nome}-ex.png"))
        from PIL import Image
        lado = Image.new("RGB", (eximg.width + img.width + 16, max(eximg.height, img.height)), (255, 255, 255))
        lado.paste(eximg, (0, 0))
        lado.paste(img, (eximg.width + 16, 0))
        lado.save(os.path.join(prova, f"{nome}-ex-x-depara.png"))
    if not silencio:
        print(json.dumps(rel, indent=1, ensure_ascii=False))
    return rel, 0


def autoteste():
    """Espelho, 4bpp e voto: provas pequenas, sem ROM."""
    t = bytes(range(32))
    assert espelha(espelha(t, 1, 0), 1, 0) == t
    assert espelha(espelha(t, 0, 1), 0, 1) == t
    assert espelha(espelha(t, 1, 1), 1, 1) == t
    assert pixels_tile(tile_pixels(t)) == t
    v = {"meta": struct.pack("<8H", 5, 6 | 0x400, 7, 8, 0, 0, 0, 0)}
    o = struct.pack("<8H", 9, 6, 7, 8, 0, 0, 0, 0)
    votos, por = voto_tiles(v, {"meta": b""}, o, b"")
    assert votos[(5, 0)].most_common(1)[0][0] == (9, 0, 0)
    assert votos[(6, 0)].most_common(1)[0][0] == (6, 1, 0)
    print("autoteste OK")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--ex", help="mapa do EX, grupo.índice (ex.: 0.13)")
    ap.add_argument("--layout", help="LAYOUT_* nosso (par de tilesets e map.bin)")
    ap.add_argument("--repo", default=RAIZ)
    ap.add_argument("--mapbin", help="map.bin alternativo (padrão: o do layout)")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--prova", help="pasta para as imagens da prova (com --aplicar)")
    ap.add_argument("--vagas", help="vagas de metatile DENTRO da contagem, dadas pelo condutor, ex.: 510,511,2 (índice local no secundário)")
    ap.add_argument("--autoteste", action="store_true")
    a = ap.parse_args()
    if a.autoteste:
        autoteste()
        return
    if not a.ex or not a.layout:
        ap.error("--ex e --layout são obrigatórios")
    vg = [int(x) for x in a.vagas.split(",")] if a.vagas else None
    _, cod = roda(a.ex, a.layout, os.path.abspath(a.repo), a.aplicar, a.prova, a.mapbin, vagas=vg)
    sys.exit(cod)


if __name__ == "__main__":
    main()
