#!/usr/bin/env python3
"""Copia uma cidade de ROM hack INTEIRA para um tileset SECUNDÁRIO novo (regra 3.2).

NOME: a frente da Cianwood escreveu, ao mesmo tempo e sem saber desta, uma
ferramenta com o mesmo propósito e o mesmo nome (`copia_cidade_secundario.py`),
e a dela entrou no master primeiro. Esta é a versão que montou a BLACKTHORN em
24/09/2026 (dois vizinhos dividindo o secundário, Route 45 e Route 44, e o
empacotamento de paleta pelo menor número de cores NOVAS), guardada com o nome
da cidade para a cópia poder ser refeita byte a byte.

CONTRATO: `Pokemon Claude/METODO-COPIA-CIDADES.md`, seções 3.1 e 3.2.

A ordem de tentativa da seção 3.2 manda tentar PRIMEIRO a cidade inteira no
secundário, com o primário da região. É o arranjo do jogo de fábrica: a cidade e
as rotas vizinhas compartilham o primário, e por isso a travessia por conexão
(que recarrega só o secundário, `LoadMapFromCameraTransition`) não leva lixo de
um mapa para o outro. A Azalea foi feita assim em 11/09/2026, mas com um script
que ficou fora do repositório; esta ferramenta é a versão guardada daquilo, e
serve a qualquer cidade que caiba em 384 metatiles, 384 tiles e 6 paletas.

O QUE ELA FAZ
-------------
1. Lê o mapa do hack direto da ROM (mesmos leitores do `copia_cidade.py`).
2. Monta um secundário novo em que:
   - os metatiles que os VIZINHOS de `--vizinho-compartilha` usam do secundário
     deles ficam PINADOS no mesmo índice, com os mesmos pixels e o mesmo
     `(behavior, layerType)`. Assim o vizinho passa a apontar para o secundário
     novo sem mudar um pixel, e a costura dos dois lados da conexão fica certa
     por construção (os dois mapas desenham com o MESMO par);
   - todo o resto é a arte do hack, byte a byte, nas vagas que sobram.
3. Empacota as paletas por TILE (um tile 8x8 indexa uma paleta só), nunca
   fundindo duas cores que não sejam o MESMO RGB, nas 6 vagas do secundário
   (7 a 12, porque o primário de Johto é bigPrimary e fica com 0 a 6).
4. Entrada de metatile pinado que aponta para tile do PRIMÁRIO com paleta do
   PRIMÁRIO fica como está: não copia nada que o primário já desenha.

A PROVA (falha dura, sem "aplica assim mesmo")
----------------------------------------------
- extração fiel: o desenho pelo tileset extraído bate com o render direto da ROM;
- cópia fiel: o desenho da cidade pelo par NOVO (primário nosso + secundário
  novo) bate com o do hack, pixel a pixel;
- vizinhos intactos: cada vizinho desenhado com o par novo bate pixel a pixel
  com ele desenhado com o par de hoje, e cada índice pinado tem o mesmo atributo;
- colisão intacta: os bits 10 a 15 de cada célula são os do autor.

USO
---
    python3 dev_scripts/copia_cidade_secundario_blackthorn.py --hack scorched-silver \\
        --mapa g0m14 --nosso BlackthornCity --simbolo BlackthornCityCopiaSec \\
        --vizinho-compartilha Route45,Route44 --saida /tmp/x          # monta e prova
    ... --aplicar                                             # escreve no repo
"""
import argparse
import json
import os
import shutil
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import copia_cidade as cc  # noqa: E402
import render_maps as rm  # noqa: E402

N_META_PRI = cc.N_META_PRI      # 640, layout "johto"
N_TILES_PRI = cc.N_TILES_PRI    # 640
N_PAL_PRI = cc.N_PAL_PRI        # 7
N_META_SEC = 1024 - N_META_PRI  # 384
N_TILES_SEC = 1024 - N_TILES_PRI
VAGAS_PAL_SEC = 13 - N_PAL_PRI  # 6
MASK = cc.MAPGRID_METATILE_ID_MASK
RESTO = cc.MAPGRID_RESTO_MASK


def le_bin(caminho):
    dados = open(caminho, "rb").read()
    return list(struct.unpack("<%dH" % (len(dados) // 2), dados))


def empacota(visiveis, vagas, cap=cc.CORES_POR_PALETA, tentativas=4000, semente=7):
    """Empacota unidades (tiles) em grupos de até 15 cores, sem fundir cor diferente.

    Diferença para o `copia_cidade.empacota_paletas`: aqui a unidade é o TILE, e
    o critério de escolha do grupo é o MENOR número de cores NOVAS que o tile
    traz (e não o menor tamanho do grupo resultante). Medido em Blackthorn: o
    critério antigo dá 8 grupos para as 62 cores da cidade, este dá 5. Conjuntos
    repetidos e subconjuntos entram de graça, então a ordem é por tamanho
    decrescente, com recomeços aleatórios se não couber de primeira.
    """
    import random
    rnd = random.Random(semente)
    distintos = {}
    for u, s in visiveis.items():
        distintos.setdefault(frozenset(s), []).append(u)
    conj = list(distintos)
    melhor = None
    for t in range(tentativas):
        if t == 0:
            ordem = sorted(conj, key=lambda s: -len(s))
        else:
            ordem = sorted(conj, key=lambda s: (-len(s) + rnd.random() * 3))
        grupos = []
        for s in ordem:
            escolha = None
            for g in grupos:
                u = len(g["cores"] | s)
                if u <= cap:
                    novo = u - len(g["cores"])
                    if escolha is None or (novo, u) < escolha[0]:
                        escolha = ((novo, u), g)
            if escolha is None:
                grupos.append({"cores": set(s), "origens": list(distintos[s])})
            else:
                escolha[1]["cores"] |= s
                escolha[1]["origens"] += distintos[s]
        if melhor is None or len(grupos) < len(melhor):
            melhor = grupos
        if len(melhor) <= vagas:
            break
    return melhor


def monta(copia, args):
    destino = args.saida
    os.makedirs(destino, exist_ok=True)
    pasta_pri, pasta_sec = copia.extrai_hack(destino)
    _f, nm, nt, npal = copia.split_hack
    hack = cc.Lado(pasta_pri, pasta_sec, nm, nt, npal)
    pri_nosso = copia.lay_nosso["primary_tileset"]

    w, h, palavras, bw, bh, borda = copia.le_mapa_hack()
    usados = sorted({v & MASK for v in palavras + borda})

    # ---------------- pinos: o que cada vizinho usa do secundário dele
    vizinhos = [v for v in (args.vizinho_compartilha or "").split(",") if v]
    dono = {}
    for nome in vizinhos:
        lay = rm.carregar_layouts()[json.load(open(os.path.join(cc.REPO, "data/maps", nome, "map.json")))["layout"]]
        if lay["primary_tileset"] != pri_nosso:
            raise SystemExit("ERRO: %s usa o primário %s, e a cidade usa %s. Vizinho que "
                             "compartilha o secundário tem de compartilhar o primário."
                             % (nome, lay["primary_tileset"], pri_nosso))
        for v in le_bin(os.path.join(cc.REPO, lay["blockdata_filepath"])) + \
                le_bin(os.path.join(cc.REPO, lay["border_filepath"])):
            i = v & MASK
            if i < N_META_PRI:
                continue
            par = (lay["primary_tileset"], lay["secondary_tileset"])
            if i in dono and dono[i] != par:
                a, b = copia.lado_de(*dono[i]), copia.lado_de(*par)
                if a.desenha(i).tobytes() != b.desenha(i).tobytes() or a.atributo(i) != b.atributo(i):
                    raise SystemExit("ERRO: o índice %d é pinado por dois vizinhos com arte diferente" % i)
            dono.setdefault(i, par)
    pin = sorted(dono)

    ent_hack = {i: hack.entradas(i) for i in usados}
    if any(e is None for e in ent_hack.values()):
        raise SystemExit("ERRO: o hack usa metatile que não existe no tileset dele")
    ent_pin = {i: copia.lado_de(*dono[i]).entradas(i) for i in pin}
    if any(e is None for e in ent_pin.values()):
        raise SystemExit("ERRO: pino aponta para metatile que o vizinho não tem")
    # entrada crua do pino, para saber se ela aponta para o PRIMÁRIO
    crua_pin = {}
    for i in pin:
        lado = copia.lado_de(*dono[i])
        ts, loc = lado.local(i)
        crua_pin[i] = rm.entradas_metatile(ts["metatiles"], loc)

    # ---------------- unidades de paleta: por TILE
    visiveis = {}
    originais = {}

    def unidade(grade, cores, chave):
        u = (chave, grade)
        s = set()
        for linha in grade:
            for c in linha:
                if c:
                    s.add(cores[c] if c < len(cores) else (0, 0, 0))
        visiveis[u] = s
        originais[u] = cores
        return u

    def fica_no_primario(i, k):
        idx_tile, _fh, _fv, pal = crua_pin[i][k]
        return idx_tile < N_TILES_PRI and pal < N_PAL_PRI

    for i, ent in ent_hack.items():
        for e in ent:
            if e is not None:
                unidade(e[0], e[3], e[4])
    for i, ent in ent_pin.items():
        for k, e in enumerate(ent):
            if e is None or fica_no_primario(i, k):
                continue
            if crua_pin[i][k][3] < N_PAL_PRI:
                continue  # tile do secundário com paleta do primário: não repinta
            unidade(e[0], e[3], e[4])

    grupos = empacota(visiveis, VAGAS_PAL_SEC)
    medida = {"hack": copia.slug, "mapa_hack": "g%dm%d" % (copia.g, copia.m), "nosso": args.nosso,
              "tamanho_hack": [w, h], "tamanho_nosso": [copia.lay_nosso["width"], copia.lay_nosso["height"]],
              "metatiles_do_hack": len(usados), "pinados": len(pin), "vizinhos": vizinhos,
              "paletas": {"unidades": len(visiveis),
                          "cores": len(set().union(*visiveis.values())) if visiveis else 0,
                          "grupos": len(grupos), "vagas": VAGAS_PAL_SEC}}
    if len(grupos) > VAGAS_PAL_SEC:
        medida["veredito"] = "NAO CABE (paleta)"
        return medida, None
    if len(usados) + len(pin) > N_META_SEC:
        medida["veredito"] = "NAO CABE (metatile)"
        return medida, None

    slot_de = {}
    cores_do_slot = []
    for j, g in enumerate(grupos):
        cores_do_slot.append(sorted(g["cores"]))
        for u in g["origens"]:
            slot_de[u] = N_PAL_PRI + j
    indice_no_slot = {N_PAL_PRI + j: {c: n + 1 for n, c in enumerate(cores_do_slot[j])}
                      for j in range(len(grupos))}

    # ---------------- tiles do secundário novo: o 0 é VAZIO (contrato 3.1)
    vazio = tuple(tuple(0 for _ in range(8)) for _ in range(8))
    tiles = {(vazio, 0): 0}
    ordem = [(vazio, 0)]

    def acha_ou_poe(grade, slot, fh, fv):
        for cand, cfh, cfv in cc.orientacoes(grade):
            achado = tiles.get((cand, slot))
            if achado is not None:
                return achado, fh ^ cfh, fv ^ cfv
        tiles[(grade, slot)] = len(ordem)
        ordem.append((grade, slot))
        return len(ordem) - 1, fh, fv

    def entrada_repintada(e):
        grade, fh, fv, cores, chave = e
        u = (chave, grade)
        slot = slot_de[u]
        mapa = indice_no_slot[slot]
        novo = tuple(tuple(0 if c == 0 else mapa[cores[c] if c < len(cores) else (0, 0, 0)]
                           for c in linha) for linha in grade)
        idx, nfh, nfv = acha_ou_poe(novo, slot, fh, fv)
        return (N_TILES_PRI + idx, nfh, nfv, slot)

    vazios = []

    def metatile_hack(i):
        saida = []
        for k, e in enumerate(ent_hack[i]):
            if e is None:
                vazios.append(("hack", i, k))
                saida.append((N_TILES_PRI, False, False, N_PAL_PRI))
            else:
                saida.append(entrada_repintada(e))
        return saida

    def metatile_pin(i):
        saida = []
        for k, e in enumerate(ent_pin[i]):
            idx_tile, fh, fv, pal = crua_pin[i][k]
            if fica_no_primario(i, k):
                saida.append((idx_tile, fh, fv, pal))
            elif e is None:
                vazios.append(("pin", i, k))
                saida.append((N_TILES_PRI, False, False, N_PAL_PRI))
            elif pal < N_PAL_PRI:
                # tile do secundário do vizinho pintado com paleta do primário:
                # copia os nibbles crus, a paleta continua a do primário.
                idx, nfh, nfv = acha_ou_poe(e[0], pal, fh, fv)
                saida.append((N_TILES_PRI + idx, nfh, nfv, pal))
            else:
                saida.append(entrada_repintada(e))
        return saida

    montado_pin = {i: metatile_pin(i) for i in pin}
    montado_hack = {i: metatile_hack(i) for i in usados}
    medida["tiles"] = {"precisa": len(ordem), "vagas": N_TILES_SEC}
    medida["quadrantes_vazios"] = len(vazios)
    if len(ordem) > N_TILES_SEC:
        medida["veredito"] = "NAO CABE (tile)"
        return medida, None

    livres = [i for i in range(N_META_PRI, 1024) if i not in set(pin)]
    de_para = {idx: livres[j] for j, idx in enumerate(usados)}
    n_meta = max([de_para[i] for i in usados] + pin) - N_META_PRI + 1
    meta = bytearray(16 * n_meta)
    attr = bytearray(2 * n_meta)

    def grava(idx_global, entradas, at):
        loc = idx_global - N_META_PRI
        for k, (t, fh, fv, pal) in enumerate(entradas):
            struct.pack_into("<H", meta, loc * 16 + k * 2,
                             (t & 0x3FF) | (0x400 if fh else 0) | (0x800 if fv else 0) | ((pal & 0xF) << 12))
        comp, camada = at
        struct.pack_into("<H", attr, loc * 2, (comp & 0xFF) | ((camada & 0xF) << 12))

    for i in pin:
        grava(i, montado_pin[i], copia.lado_de(*dono[i]).atributo(i) or (0, 0))
    for i in usados:
        grava(de_para[i], montado_hack[i], hack.atributo(i) or (0, 0))

    # ---------------- escreve o secundário
    pasta = os.path.join(destino, "tileset_secundario")
    grupos_arquivo = []
    for j in range(len(grupos)):
        u0 = grupos[j]["origens"][0]
        grupos_arquivo.append({"slot": N_PAL_PRI + j, "cores": cores_do_slot[j],
                               "zero": list(originais[u0][0]) if originais.get(u0) else [0, 0, 0]})
    cc.escreve_tileset(pasta, ordem, list(range(len(ordem))), grupos_arquivo, bytes(meta), bytes(attr),
                       len(ordem))

    def remapeia(lista):
        return b"".join(struct.pack("<H", (de_para[v & MASK] & MASK) | (v & RESTO)) for v in lista)

    open(os.path.join(destino, "map.bin"), "wb").write(remapeia(palavras))
    open(os.path.join(destino, "border.bin"), "wb").write(remapeia(borda[:4]).ljust(8, b"\0"))

    comportamentos = {}
    for i in usados:
        b = (hack.atributo(i) or (0, 0))[0]
        comportamentos[b] = comportamentos.get(b, 0) + 1
    medida["comportamentos_do_hack"] = {cc.dp.nome_behavior(k): v for k, v in sorted(comportamentos.items())}
    medida["metatiles_no_arquivo"] = n_meta
    medida["veredito"] = "CABE"
    plano = {"de_para": de_para, "pin": pin, "dono": dono, "w": w, "h": h, "palavras": palavras,
             "hack": hack, "pasta": pasta, "vizinhos": vizinhos}
    return medida, plano


def prova(copia, plano, args):
    res = {}
    from render_hack import Render
    r = cc.gbamap.Rom(copia.caminho_rom)
    _f, nm, nt, npal = copia.split_hack
    r.n_meta_pri, r.n_tiles_pri, r.n_pal_pri = nm, nt, npal
    img_rom = Render(r).mapa(copia.hdr)
    img_ext = cc.desenha_mapa(plano["hack"], plano["w"], plano["h"], plano["palavras"])
    res["extracao_fiel"] = cc.difere(img_rom, img_ext)[0]

    novo = cc.Lado(copia.lay_nosso["primary_tileset"], plano["pasta"], N_META_PRI, N_TILES_PRI, N_PAL_PRI)
    palavras_novas = le_bin(os.path.join(args.saida, "map.bin"))
    img_copia = cc.desenha_mapa(novo, plano["w"], plano["h"], palavras_novas)
    res["copia_fiel"] = cc.difere(img_ext, img_copia)[0]
    res["colisao_intacta"] = sum(1 for a, b in zip(plano["palavras"], palavras_novas) if (a & RESTO) != (b & RESTO))

    res["vizinhos"] = {}
    for nome in plano["vizinhos"]:
        lay = rm.carregar_layouts()[json.load(open(os.path.join(cc.REPO, "data/maps", nome, "map.json")))["layout"]]
        pal = le_bin(os.path.join(cc.REPO, lay["blockdata_filepath"]))
        velho = copia.lado_de(lay["primary_tileset"], lay["secondary_tileset"])
        a = cc.desenha_mapa(velho, lay["width"], lay["height"], pal)
        b = cc.desenha_mapa(novo, lay["width"], lay["height"], pal)
        n_px = cc.difere(a, b)[0]
        attr_ruins = [i for i in {v & MASK for v in pal} if velho.atributo(i) != novo.atributo(i)]
        res["vizinhos"][nome] = {"pixels_diferentes": n_px, "atributos_diferentes": len(attr_ruins)}
    res["passou"] = (res["extracao_fiel"] == 0 and res["copia_fiel"] == 0 and res["colisao_intacta"] == 0
                     and all(v["pixels_diferentes"] == 0 and v["atributos_diferentes"] == 0
                             for v in res["vizinhos"].values()))
    img_copia.save(os.path.join(args.saida, "copia.png"))
    img_rom.save(os.path.join(args.saida, "hack.png"))
    return res, img_rom, img_copia


def aplica(copia, plano, args):
    rotulo = args.simbolo
    rel = "data/tilesets/secondary/%s" % cc._snake(rotulo)
    dst = os.path.join(cc.REPO, rel)
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    shutil.copytree(plano["pasta"], dst)
    caminhos = {k: os.path.join(cc.REPO, "src/data/tilesets/%s.h" % k) for k in ("graphics", "metatiles", "headers")}
    textos = {k: open(p, encoding="utf-8").read() for k, p in caminhos.items()}
    if "gTilesetTiles_%s[]" % rotulo not in textos["graphics"]:
        bloco = '\nconst u32 gTilesetTiles_%s[] = INCGFX_U32("%s/tiles.png", ".4bpp.smol");\n' % (rotulo, rel)
        bloco += "\nconst u16 ALIGNED(4) gTilesetPalettes_%s[][16] =\n{\n" % rotulo
        for i in range(16):
            bloco += '    INCGFX_U16("%s/palettes/%02d.pal", ".gbapal"),\n' % (rel, i)
        bloco += "};\n"
        open(caminhos["graphics"], "a", encoding="utf-8").write(bloco)
    if "gMetatiles_%s[]" % rotulo not in textos["metatiles"]:
        open(caminhos["metatiles"], "a", encoding="utf-8").write(
            'const u16 gMetatiles_%s[] = INCBIN_U16("%s/metatiles.bin");\n'
            'const u16 gMetatileAttributes_%s[] = INCBIN_U16("%s/metatile_attributes.bin");\n'
            % (rotulo, rel, rotulo, rel))
    if "gTileset_%s =" % rotulo not in textos["headers"]:
        open(caminhos["headers"], "a", encoding="utf-8").write(
            ("\nconst struct Tileset gTileset_%s =\n{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n"
             "    .tiles = gTilesetTiles_%s,\n    .palettes = gTilesetPalettes_%s,\n"
             "    .metatiles = gMetatiles_%s,\n    .metatileAttributes = gMetatileAttributes_%s,\n"
             "    .callback = NULL,\n};\n") % (rotulo, rotulo, rotulo, rotulo, rotulo))

    caminho_layouts = os.path.join(cc.REPO, "data/layouts/layouts.json")
    doc = json.load(open(caminho_layouts, encoding="utf-8"))
    ids_viz = set()
    for nome in plano["vizinhos"]:
        ids_viz.add(json.load(open(os.path.join(cc.REPO, "data/maps", nome, "map.json")))["layout"])
    for L in doc["layouts"]:
        if L.get("id") == copia.lay_nosso["id"]:
            L["width"], L["height"] = plano["w"], plano["h"]
            L["secondary_tileset"] = "gTileset_" + rotulo
        elif L.get("id") in ids_viz:
            L["secondary_tileset"] = "gTileset_" + rotulo
    with open(caminho_layouts, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")
    shutil.copyfile(os.path.join(args.saida, "map.bin"), os.path.join(cc.REPO, copia.lay_nosso["blockdata_filepath"]))
    shutil.copyfile(os.path.join(args.saida, "border.bin"), os.path.join(cc.REPO, copia.lay_nosso["border_filepath"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hack", required=True)
    ap.add_argument("--mapa", required=True)
    ap.add_argument("--nosso", required=True)
    ap.add_argument("--simbolo", required=True, help="rótulo do secundário novo, sem gTileset_")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--vizinho-compartilha", help="mapas (vírgula) que passam a usar o secundário novo")
    ap.add_argument("--aplicar", action="store_true")
    args = ap.parse_args()
    copia = cc.Copia(args)
    medida, plano = monta(copia, args)
    print(json.dumps(medida, indent=1, ensure_ascii=False))
    if plano is None:
        raise SystemExit(1)
    res, _a, _b = prova(copia, plano, args)
    print("PROVA", json.dumps(res, ensure_ascii=False))
    if not res["passou"]:
        raise SystemExit("PROVA REPROVOU: nada foi aplicado")
    json.dump({str(k): v for k, v in plano["de_para"].items()},
              open(os.path.join(args.saida, "de_para.json"), "w"))
    if args.aplicar:
        aplica(copia, plano, args)
        print("APLICADO: gTileset_%s" % args.simbolo)


if __name__ == "__main__":
    main()
