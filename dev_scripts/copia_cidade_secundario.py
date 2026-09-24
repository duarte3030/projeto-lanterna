#!/usr/bin/env python3
"""Copia uma cidade de ROM hack INTEIRA para dentro de um tileset SECUNDÁRIO novo.

É a tentativa 1 da seção 3.2 do `Pokemon Claude/METODO-COPIA-CIDADES.md`: a
cidade continua com o NOSSO primário da região e toda a arte do autor vai para
um secundário só dela. As conexões continuam abertas, porque a travessia por
conexão (`LoadMapFromCameraTransition`, src/overworld.c) recarrega só o
secundário e o primário é o mesmo dos dois lados.

POR QUE ESTE ARQUIVO EXISTE, SE JÁ HÁ O `copia_cidade.py`
---------------------------------------------------------
O `copia_cidade.py` monta o arranjo da tentativa 2 (par PRÓPRIO de tilesets,
saídas por warp). A Azalea de 11/09/2026 coube na tentativa 1, mas o secundário
dela foi montado à mão e a receita não ficou no repositório. Esta ferramenta é
essa receita, escrita, com as provas.

O VIZINHO QUE DIVIDE O SECUNDÁRIO
---------------------------------
A conexão desenha a faixa do vizinho com os tilesets do mapa ATUAL. Se o
vizinho usa metatile do secundário antigo, o secundário novo tem de ter aquele
metatile no MESMO índice, com a mesma arte e o mesmo `(behavior, layerType)`.
E o outro sentido também: de dentro do vizinho, a faixa da CIDADE é desenhada
com o secundário DELE. O único arranjo que fecha os dois sentidos por
construção é o do jogo de fábrica: **o vizinho passa a usar o mesmo secundário
novo**. Então `--vizinho` faz isso: cada metatile de secundário que o vizinho
usa é PINADO no mesmo índice local (o `map.bin` dele não muda um byte) e o
layout dele passa a apontar para o secundário novo. A prova é o render do
vizinho inteiro antes e depois, com ZERO pixel de diferença.

AS TRÊS CONTAS QUE DECIDEM SE CABE
----------------------------------
Um secundário de Johto (layout "johto", bigPrimary) tem 384 metatiles, 384
tiles e 6 paletas (7 a 12).

1. Metatile: os do autor mais os pinados do vizinho.
2. Tile: a unidade é o tile 8x8 com as cores RESOLVIDAS em RGB, deduplicado
   pelas quatro orientações. Dois tiles do autor com o mesmo desenho em cores
   diferentes são tiles diferentes; o mesmo desenho indexado em paletas
   diferentes pode virar o MESMO tile depois do empacotamento, e isso só ajuda.
3. Paleta: a unidade é o TILE, e não a paleta de origem (lição da Azalea: um
   tile 8x8 indexa uma paleta só, então basta que as cores de CADA TILE caibam
   juntas num grupo de 15). É um problema de empacotamento com restrição de
   subconjunto, e ele é resolvido EXATO pelo `z3` (brew), sem heurística: ou
   existe arranjo em 6 grupos, ou a ferramenta diz que não existe. Cor nunca é
   aproximada: duas cores só se juntam quando são o MESMO RGB.

AS PROVAS (falha dura, sem "aplica assim mesmo")
------------------------------------------------
A. a extração do hack é fiel: o tileset extraído desenha o mapa igual ao
   `render_hack` lendo direto da ROM;
B. a cópia é fiel: o mapa desenhado a partir dos ARQUIVOS NOVOS, com o nosso
   primário, é idêntico pixel a pixel ao do hack;
C. o vizinho não muda: o render dele com o secundário novo é idêntico ao de
   antes, e cada pinado tem o mesmo `(behavior, layerType)`;
D. a planta do autor (bits 10 a 15 de cada célula) chega intacta.

Uso:
    python3 dev_scripts/copia_cidade_secundario.py --hack scorched-silver --mapa g0m12 \\
        --nosso CianwoodCity --vizinho Route41 --rotulo CianwoodCityCopiaSec \\
        --saida /tmp/x                  # mede, monta e prova em --saida
    ... --aplicar                       # e escreve no repositório
"""
import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image  # noqa: E402

import copia_cidade as cc  # noqa: E402
import render_maps as rm  # noqa: E402

REPO = rm.REPO
N_META_PRI = 640
N_TILES_PRI = 640
N_PAL_PRI = 7
N_META_SEC = 384
N_TILES_SEC = 384
SLOTS_SEC = list(range(7, 13))   # 6 vagas de paleta do secundário
CAP = 15                         # a cor 0 de cada paleta é transparente


def canon(grade):
    """Forma canônica de uma grade 8x8 entre as quatro orientações, e o flip
    que leva da canônica até ela."""
    melhor = None
    for g, fh, fv in cc.orientacoes(grade):
        chave = repr(g)
        if melhor is None or chave < melhor[0]:
            melhor = (chave, g, fh, fv)
    return melhor[1], melhor[2], melhor[3]


def grade_rgb(grade, cores):
    return tuple(tuple(None if c == 0 else tuple(cores[c]) if c < len(cores) else (0, 0, 0)
                       for c in linha) for linha in grade)


def aplica_flip(g, fh, fv):
    if fh:
        g = cc.flip_h(g)
    if fv:
        g = cc.flip_v(g)
    return g


def cores_de(g):
    return frozenset(c for linha in g for c in linha if c is not None)


def empacota_z3(conjuntos, vagas, cap=CAP):
    """Grupos de no máximo `cap` cores em que cada conjunto cabe inteiro em um.

    Só os conjuntos MAXIMAIS entram na conta (um subconjunto cabe onde o maior
    couber). Resolvido pelo z3 como satisfatibilidade exata.
    """
    unicos = sorted(set(conjuntos), key=lambda s: (-len(s), sorted(s)))
    maximais = [s for s in unicos if not any(s < o for o in unicos)]
    cores = sorted(frozenset().union(*maximais)) if maximais else []
    ci = {c: i for i, c in enumerate(cores)}
    L = ["(set-logic QF_LIA)"]
    for s in range(len(maximais)):
        for b in range(vagas):
            L.append("(declare-const a%d_%d Bool)" % (s, b))
        L.append("(assert (or %s))" % " ".join("a%d_%d" % (s, b) for b in range(vagas)))
    for b in range(vagas):
        for c in range(len(cores)):
            L.append("(declare-const c%d_%d Bool)" % (c, b))
        if cores:
            L.append("(assert (<= (+ %s) %d))" % (" ".join("(ite c%d_%d 1 0)" % (c, b)
                                                         for c in range(len(cores))), cap))
    for s, st in enumerate(maximais):
        for b in range(vagas):
            for c in st:
                L.append("(assert (=> a%d_%d c%d_%d))" % (s, b, ci[c], b))
    if maximais:
        L.append("(assert a0_0)")   # quebra de simetria
    L.append("(check-sat)")
    L.append("(get-model)")
    with tempfile.NamedTemporaryFile("w", suffix=".smt2", delete=False) as f:
        f.write("\n".join(L))
        caminho = f.name
    try:
        saida = subprocess.run(["z3", "-T:600", caminho], capture_output=True, text=True).stdout
    finally:
        os.unlink(caminho)
    if not saida.startswith("sat"):
        return None, len(maximais), len(cores)
    verdade = set(re.findall(r"define-fun (a\d+_\d+) \(\) Bool\s+true", saida))
    grupos = [set() for _ in range(vagas)]
    for s, st in enumerate(maximais):
        b = next(b for b in range(vagas) if "a%d_%d" % (s, b) in verdade)
        grupos[b] |= st
    return [sorted(g) for g in grupos], len(maximais), len(cores)


class CopiaSec:
    def __init__(self, args):
        self.args = args
        ns = argparse.Namespace(hack=args.hack, mapa=args.mapa, nosso=args.nosso, costura=None)
        self.copia = cc.Copia(ns)
        self.layouts = rm.carregar_layouts()
        self.lay_nosso = self.copia.lay_nosso
        self.pri = self.lay_nosso["primary_tileset"]
        self.vizinhos = []
        for nome in (args.vizinho or []):
            with open(os.path.join(REPO, "data/maps", nome, "map.json"), encoding="utf-8") as f:
                mj = json.load(f)
            lv = self.layouts[mj["layout"]]
            if lv["primary_tileset"] != self.pri:
                raise SystemExit("ERRO: %s usa o primário %s e a cidade usa %s; dividir o "
                                 "secundário não fecha a costura." % (nome, lv["primary_tileset"], self.pri))
            self.vizinhos.append((nome, lv))

    def monta(self, destino):
        c = self.copia
        os.makedirs(destino, exist_ok=True)
        pasta_pri, pasta_sec = c.extrai_hack(os.path.join(destino, "hack"))
        _f, nm, nt, npal = c.split_hack
        hack = cc.Lado(pasta_pri, pasta_sec, nm, nt, npal)
        w, h, palavras, bw, bh, borda = c.le_mapa_hack()
        usados = sorted({v & 0x3FF for v in palavras + borda[:bw * bh]})
        medida = {"hack": c.slug, "mapa_hack": self.args.mapa, "nosso": self.args.nosso,
                  "tamanho_hack": [w, h], "borda": [bw, bh], "metatiles_do_hack": len(usados)}

        # ---------------- pinados dos vizinhos (mesmo índice local)
        pinados = {}   # índice global -> (Lado antigo do vizinho, nome)
        for nome, lv in self.vizinhos:
            dados = open(os.path.join(REPO, lv["blockdata_filepath"]), "rb").read()
            lado = cc.Lado(lv["primary_tileset"], lv["secondary_tileset"], N_META_PRI, N_TILES_PRI, N_PAL_PRI)
            for i in range(len(dados) // 2):
                v = struct.unpack_from("<H", dados, i * 2)[0] & 0x3FF
                if v >= N_META_PRI:
                    if v in pinados and pinados[v][0].sec is not lado.sec:
                        a, b = pinados[v][0].desenha(v), lado.desenha(v)
                        if a.tobytes() != b.tobytes() or pinados[v][0].atributo(v) != lado.atributo(v):
                            raise SystemExit("ERRO: %s e %s pedem arte diferente no índice %d"
                                             % (pinados[v][1], nome, v))
                    pinados.setdefault(v, (lado, nome))
        medida["pinados"] = len(pinados)
        nosso_pri = cc.Lado(self.pri, self.lay_nosso["secondary_tileset"], N_META_PRI, N_TILES_PRI, N_PAL_PRI)
        if any(any(x for x in linha) for linha in nosso_pri.pri["tiles"][0]):
            raise SystemExit("ERRO: o tile 0 do primário não é vazio; o quadrante transparente "
                             "usa ele.")

        # ---------------- unidades: cada entrada vira tile RGB, ou fica crua no primário
        # entrada crua = (tile, fh, fv, pal) que NÃO muda; entrada unidade = grade RGB orientada
        def entradas_de(lado, idx, cru_permitido):
            ts, loc = lado.local(idx)
            brutas = rm.entradas_metatile(ts["metatiles"], loc)
            resolvidas = lado.entradas(idx)
            saida = []
            for (it, fh, fv, ip), e in zip(brutas, resolvidas):
                if cru_permitido and it < N_TILES_PRI and ip < N_PAL_PRI:
                    saida.append(("cru", (it, fh, fv, ip)))
                elif e is None:
                    saida.append(("vazio", None))
                else:
                    g = aplica_flip(grade_rgb(e[0], e[3]), e[1], e[2])
                    if not cores_de(g):
                        saida.append(("vazio", None))
                    else:
                        saida.append(("rgb", g))
            return saida

        ent = {}
        for i in usados:
            ent[("hack", i)] = entradas_de(hack, i, False)
        for i, (lado, _n) in pinados.items():
            ent[("pin", i)] = entradas_de(lado, i, True)

        conjuntos = [cores_de(g) for lst in ent.values() for k, g in lst if k == "rgb"]
        grupos, n_max, n_cores = empacota_z3(conjuntos, len(SLOTS_SEC))
        medida["paletas"] = {"conjuntos_maximais": n_max, "cores_distintas": n_cores,
                             "vagas": len(SLOTS_SEC), "cabe": grupos is not None}
        if grupos is None:
            medida["veredito"] = "NAO CABE (paleta)"
            return medida, None
        idx_cor = [{cor: j + 1 for j, cor in enumerate(g)} for g in grupos]

        # ---------------- tiles
        tiles = {}       # grade de índices canônica -> índice local no secundário
        ordem = []
        vistos_rgb = set()

        def resolve(g):
            s = cores_de(g)
            b = next(b for b in range(len(grupos)) if s <= set(grupos[b]))
            vistos_rgb.add(canon(g)[0])
            ind = tuple(tuple(0 if c is None else idx_cor[b][c] for c in linha) for linha in g)
            cg, cfh, cfv = canon(ind)
            if cg not in tiles:
                tiles[cg] = len(ordem)
                ordem.append(cg)
            # cg desenhado com (cfh, cfv) dá `ind`; flip é involução
            return (N_TILES_PRI + tiles[cg], cfh, cfv, SLOTS_SEC[b])

        montado = {}
        for chave, lst in ent.items():
            m = []
            for k, x in lst:
                if k == "cru":
                    m.append(x)
                elif k == "vazio":
                    m.append((0, False, False, 0))
                else:
                    m.append(resolve(x))
            montado[chave] = m
        medida["tiles"] = {"precisa": len(ordem), "rgb_distintos": len(vistos_rgb),
                           "vagas": N_TILES_SEC, "cabe": len(ordem) <= N_TILES_SEC}
        # ---------------- metatiles
        livres = [i for i in range(N_META_PRI, N_META_PRI + N_META_SEC) if i not in pinados]
        precisa_meta = len(usados) + len(pinados)
        medida["metatiles"] = {"precisa": precisa_meta, "vagas": N_META_SEC,
                               "cabe": len(usados) <= len(livres)}
        if not (medida["tiles"]["cabe"] and medida["metatiles"]["cabe"]):
            medida["veredito"] = "NAO CABE"
            return medida, None
        de_para = {i: livres[j] for j, i in enumerate(usados)}

        meta = bytearray(16 * N_META_SEC)
        attr = bytearray(2 * N_META_SEC)

        def grava(idx_global, entradas, at):
            loc = idx_global - N_META_PRI
            for k, (it, fh, fv, ip) in enumerate(entradas):
                struct.pack_into("<H", meta, loc * 16 + k * 2,
                                 (it & 0x3FF) | (0x400 if fh else 0) | (0x800 if fv else 0) | ((ip & 0xF) << 12))
            comp, camada = at
            struct.pack_into("<H", attr, loc * 2, (comp & 0xFF) | ((camada & 0xF) << 12))

        for i, (lado, _n) in pinados.items():
            grava(i, montado[("pin", i)], lado.atributo(i) or (0, 0))
        for i in usados:
            grava(de_para[i], montado[("hack", i)], hack.atributo(i) or (0, 0))

        # ---------------- escreve o tileset em destino/tileset
        pasta = os.path.join(destino, "tileset")
        os.makedirs(os.path.join(pasta, "palettes"), exist_ok=True)
        n_lin = (max(1, len(ordem)) + 15) // 16
        img = Image.new("P", (128, n_lin * 8), 0)
        px = img.load()
        for t, g in enumerate(ordem):
            ox, oy = (t % 16) * 8, (t // 16) * 8
            for y in range(8):
                for x in range(8):
                    px[ox + x, oy + y] = g[y][x]
        plana = []
        for cor in [(0, 0, 0)] + list(grupos[0]):
            plana += list(cor)
        plana += [0] * (768 - len(plana))
        img.putpalette(plana)
        img.save(os.path.join(pasta, "tiles.png"))
        for slot in range(16):
            cores = [(0, 0, 0)] * 16
            if slot in SLOTS_SEC:
                g = grupos[SLOTS_SEC.index(slot)]
                for j, cor in enumerate(g):
                    cores[j + 1] = tuple(cor)
            cc.ext.escreve_pal(os.path.join(pasta, "palettes", "%02d.pal" % slot), cores)
        with open(os.path.join(pasta, "metatiles.bin"), "wb") as f:
            f.write(meta)
        with open(os.path.join(pasta, "metatile_attributes.bin"), "wb") as f:
            f.write(attr)

        novo = bytearray()
        for v in palavras:
            novo += struct.pack("<H", (de_para[v & 0x3FF] & 0x3FF) | (v & 0xFC00))
        with open(os.path.join(destino, "map.bin"), "wb") as f:
            f.write(novo)
        nb = bytearray()
        for v in (borda[:bw * bh] + [borda[0]] * 4)[:4]:
            nb += struct.pack("<H", (de_para[v & 0x3FF] & 0x3FF) | (v & 0xFC00))
        with open(os.path.join(destino, "border.bin"), "wb") as f:
            f.write(nb)
        medida["veredito"] = "CABE"
        plano = {"hack": hack, "w": w, "h": h, "palavras": palavras, "de_para": de_para,
                 "pinados": pinados, "pasta": pasta, "destino": destino}
        return medida, plano

    def prova(self, plano):
        c = self.copia
        res = {}
        from render_hack import Render
        r = cc.gbamap.Rom(c.caminho_rom)
        _f, nm, nt, npal = c.split_hack
        r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = nm, nt, npal
        img_rom = Render(r).mapa(c.hdr).convert("RGB")
        w, h = plano["w"], plano["h"]
        img_ext = cc.desenha_mapa(plano["hack"], w, h, plano["palavras"])
        res["A_extracao_fiel"] = cc.difere(img_rom, img_ext)[0]
        novo = cc.Lado(self.pri, plano["pasta"], N_META_PRI, N_TILES_PRI, N_PAL_PRI)
        dados = open(os.path.join(plano["destino"], "map.bin"), "rb").read()
        pal_novas = [struct.unpack_from("<H", dados, i * 2)[0] for i in range(len(dados) // 2)]
        img_copia = cc.desenha_mapa(novo, w, h, pal_novas)
        res["B_copia_fiel"] = cc.difere(img_ext, img_copia)[0]
        viz = {}
        for nome, lv in self.vizinhos:
            d = open(os.path.join(REPO, lv["blockdata_filepath"]), "rb").read()
            pw = [struct.unpack_from("<H", d, i * 2)[0] for i in range(len(d) // 2)]
            antes = cc.Lado(lv["primary_tileset"], lv["secondary_tileset"], N_META_PRI, N_TILES_PRI, N_PAL_PRI)
            a = cc.desenha_mapa(antes, lv["width"], lv["height"], pw)
            b = cc.desenha_mapa(novo, lv["width"], lv["height"], pw)
            atr = sum(1 for i in plano["pinados"] if antes.atributo(i) != novo.atributo(i))
            viz[nome] = {"pixels": cc.difere(a, b)[0], "atributos_diferentes": atr}
        res["C_vizinhos"] = viz
        res["D_colisao_diferente"] = sum(1 for a, b in zip(plano["palavras"], pal_novas)
                                         if (a & 0xFC00) != (b & 0xFC00))
        # camada de baixo com pixel transparente mostra a cor de fundo do NOSSO
        # primário, e não a do hack: conta, para ninguém ser pego de surpresa.
        fundo = 0
        for v in set(pal_novas):
            ent = novo.entradas(v & 0x3FF)
            for q in range(4):
                e = ent[q]
                if e is None:
                    fundo += 64
                else:
                    fundo += sum(1 for linha in e[0] for x in linha if x == 0)
        res["pixels_de_fundo_por_metatile_distinto"] = fundo
        ok = (res["A_extracao_fiel"] == 0 and res["B_copia_fiel"] == 0 and res["D_colisao_diferente"] == 0
              and all(v["pixels"] == 0 and v["atributos_diferentes"] == 0 for v in viz.values()))
        res["passou"] = ok
        img_copia.save(os.path.join(plano["destino"], "copia.png"))
        img_rom.save(os.path.join(plano["destino"], "hack.png"))
        return res

    def aplica(self, plano):
        rot = self.args.rotulo
        rel = "data/tilesets/secondary/%s" % cc._snake(rot)
        dst = os.path.join(REPO, rel)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(plano["pasta"], dst)
        caminhos = {k: os.path.join(REPO, "src/data/tilesets/%s.h" % k)
                    for k in ("graphics", "metatiles", "headers")}
        textos = {k: open(p, encoding="utf-8").read() for k, p in caminhos.items()}
        add = {k: "" for k in caminhos}
        cab = "\n// ---- %s copiada (METODO-COPIA-CIDADES, secundário só dela) ----\n" % self.args.nosso
        if "gTilesetTiles_%s[]" % rot not in textos["graphics"]:
            add["graphics"] += cab
            add["graphics"] += '\nconst u32 gTilesetTiles_%s[] = INCGFX_U32("%s/tiles.png", ".4bpp.smol");\n' % (rot, rel)
            add["graphics"] += "\nconst u16 ALIGNED(4) gTilesetPalettes_%s[][16] =\n{\n" % rot
            for i in range(16):
                add["graphics"] += '    INCGFX_U16("%s/palettes/%02d.pal", ".gbapal"),\n' % (rel, i)
            add["graphics"] += "};\n"
        if "gMetatiles_%s[]" % rot not in textos["metatiles"]:
            add["metatiles"] += 'const u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin");\n' % (rot, rel)
            add["metatiles"] += 'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n' % (rot, rel)
        if "gTileset_%s =" % rot not in textos["headers"]:
            add["headers"] += cab
            add["headers"] += ("\nconst struct Tileset gTileset_%s =\n{\n"
                               "    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
                               "    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n"
                               "    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n"
                               "    .callback = NULL,\n};\n") % (rot, rot, rot, rot, rot)
        for k, bloco in add.items():
            if bloco:
                with open(caminhos[k], "a", encoding="utf-8") as f:
                    f.write(bloco)
        caminho_layouts = os.path.join(REPO, "data/layouts/layouts.json")
        with open(caminho_layouts, encoding="utf-8") as f:
            doc = json.load(f)
        alvo = {self.lay_nosso["id"]} | {lv["id"] for _n, lv in self.vizinhos}
        for L in doc["layouts"]:
            if L.get("id") in alvo:
                L["secondary_tileset"] = "gTileset_" + rot
            if L.get("id") == self.lay_nosso["id"]:
                L["width"], L["height"] = plano["w"], plano["h"]
        with open(caminho_layouts, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)
            f.write("\n")
        for nome, chave in (("map.bin", "blockdata_filepath"), ("border.bin", "border_filepath")):
            shutil.copyfile(os.path.join(plano["destino"], nome), os.path.join(REPO, self.lay_nosso[chave]))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--hack", required=True)
    ap.add_argument("--mapa", required=True)
    ap.add_argument("--nosso", required=True)
    ap.add_argument("--vizinho", action="append", help="mapa que passa a dividir o secundário novo")
    ap.add_argument("--rotulo", required=True, help="nome do tileset novo, sem gTileset_")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    cs = CopiaSec(args)
    medida, plano = cs.monta(args.saida)
    print(json.dumps(medida, indent=1, ensure_ascii=False))
    if plano is None:
        raise SystemExit(1)
    res = cs.prova(plano)
    print(json.dumps(res, indent=1, ensure_ascii=False))
    with open(os.path.join(args.saida, "medida.json"), "w", encoding="utf-8") as f:
        json.dump({"medida": medida, "prova": res, "de_para": plano["de_para"]}, f, indent=1)
    if not res["passou"]:
        raise SystemExit("PROVA REPROVADA: nada foi escrito no repositório.")
    if args.aplicar:
        cs.aplica(plano)
        print("aplicado em", REPO)


if __name__ == "__main__":
    main()
