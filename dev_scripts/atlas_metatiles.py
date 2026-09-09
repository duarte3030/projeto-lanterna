#!/usr/bin/env python3
"""Desenha o ATLAS de metatiles de um layout: cada metatile do par de tilesets,
rotulado com o id, em grade, e opcionalmente só os que o mapa NÃO usa.

Por que existe. A onda 3 do REFINO (Johto) mediu uma coisa que muda a conta da
rodada inteira: o primário de Johto tem 640 metatiles DESENHADOS e cada cidade
usa entre 103 e 162 deles. Ou seja, cada cidade tem cerca de quinhentas peças de
arte já compiladas na ROM que ninguém escreveu no `map.bin`. Pôr uma delas no
mapa custa ZERO byte, ZERO tile e ZERO cor, e foi assim que a rodada de Snowpoint
(`ace0ac7877`) pagou placa, poste, cerca, pedra e arbusto sem gastar orçamento:
os cinco JÁ ESTAVAM no `gTileset_Snowpoint` e nenhum dos cinco mapas os usava.

Só que ninguém consegue garimpar quinhentas peças por número. Tem que OLHAR. Era
esse o passo que faltava ter ferramenta: `neve_snowpoint2.py` fala em "o atlas
dos 512 metatiles daquele secundário foi renderizado nesta frente", mas o código
que fez isso morreu junto com a rodada. Aqui ele fica.

O QUE O ATLAS MOSTRA, e o que ele NÃO mostra:

  - mostra as DUAS camadas do metatile compostas, com a paleta certa de cada
    entrada, que é o que o jogo desenha;
  - mostra o id do metatile e, com `--attr`, o atributo cru em hexa;
  - NÃO mostra comportamento nem colisão em linguagem de gente. Metatile bonito
    com comportamento errado continua sendo defeito, e a lente
    (`dev_scripts/qa/lente_carimbo.py`) é que decide isso, não o olho.
  - o fundo é (20,20,20) de propósito, o mesmo tom dos atlas salvos em
    `amostras-tileset/refino/`, para que dois atlas do mesmo tileset possam ser
    comparados byte a byte. Não troque essa cor sem trocar em todos.

Uso:
    python3 dev_scripts/atlas_metatiles.py GoldenrodCity saida.png
    python3 dev_scripts/atlas_metatiles.py GoldenrodCity saida.png --nao-usados
    python3 dev_scripts/atlas_metatiles.py GoldenrodCity saida.png --lado primario
    python3 dev_scripts/atlas_metatiles.py --demo

`--nao-usados` é o modo que interessa nesta onda: ele tira do atlas tudo que já
está no `map.bin` do mapa e deixa só a pilha para garimpar.
"""
import collections
import json
import os
import struct
import sys

from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))

FUNDO = (20, 20, 20)
CEL = 16          # o metatile tem 16x16
ESCALA = 2        # 32x32 na folha, que é onde o olho ainda lê o desenho
ROT = 9           # altura da faixa de rótulo
COLS = 16

# Tetos por versão de layout, de include/fieldmap.h. A versão "johto" é
# bigPrimary, e foi ela que fez a conta desta onda ser diferente da de Sinnoh.
TETOS = {
    "emerald": (512, 512, 6),
    "johto": (640, 640, 7),
    "frlg": (640, 640, 7),
}


def carrega_layouts():
    with open(os.path.join(RAIZ, "data/layouts/layouts.json"), encoding="utf-8") as f:
        return json.load(f)["layouts"]


def _rm():
    """O render_maps do proprio repo. Reusar os carregadores dele nao e economia
    de linha: e a garantia de que o atlas ve exatamente o que o render ve. Se a
    leitura divergir, o atlas vira uma segunda verdade e passa a mentir calado
    (foi assim que o `12_over.pal` derrubou o render de Goldenrod uma vez)."""
    import render_maps
    return render_maps



def desenha_metatile(mid, meta, tiles_pri, tiles_sec, pals, n_tiles_pri, n_meta_pri):
    """Compoe as duas camadas de um metatile num RGBA de 16x16."""
    fonte = meta["pri"] if mid < n_meta_pri else meta["sec"]
    base = mid if mid < n_meta_pri else mid - n_meta_pri
    o = base * 16
    if o + 16 > len(fonte):
        return None
    img = Image.new("RGBA", (CEL, CEL), (0, 0, 0, 0))
    px = img.load()
    for camada in (0, 1):
        for q in range(4):
            k = (camada * 4 + q) * 2
            w = struct.unpack("<H", fonte[o + k: o + k + 2])[0]
            t, hf, vf, pal = w & 0x3FF, (w >> 10) & 1, (w >> 11) & 1, (w >> 12) & 0xF
            if t < n_tiles_pri:
                tile = tiles_pri[t] if t < len(tiles_pri) else None
            else:
                i = t - n_tiles_pri
                tile = tiles_sec[i] if i < len(tiles_sec) else None
            cores = pals.get(pal)
            if tile is None or cores is None:
                continue
            ox, oy = (q % 2) * 8, (q // 2) * 8
            for y in range(8):
                fy = 7 - y if vf else y
                for x in range(8):
                    fx = 7 - x if hf else x
                    v = tile[fy][fx]
                    if v == 0:      # 0 e transparencia, nas DUAS camadas
                        continue
                    r, g, b = cores[v % len(cores)]
                    px[ox + x, oy + y] = (r, g, b, 255)
    return img


def dados_do_mapa(nome):
    rm = _rm()
    layouts = carrega_layouts()
    alvo = None
    for l in layouts:
        bd = l.get("blockdata_filepath") or ""
        if bd.endswith(f"/{nome}/map.bin"):
            alvo = l
            break
    if alvo is None:
        for l in layouts:
            if l["name"] in (nome, nome + "_Layout"):
                alvo = l
                break
    if alvo is None:
        raise SystemExit(f"layout de {nome} nao achado em data/layouts/layouts.json")
    versao = alvo.get("layout_version") or "emerald"
    n_meta_pri, n_tiles_pri, n_pal_pri = TETOS.get(versao, TETOS["emerald"])
    ts_pri = rm.carregar_tileset(alvo["primary_tileset"])
    ts_sec = rm.carregar_tileset(alvo["secondary_tileset"])
    # O motor resolve tile pelo TETO da versao de layout, nao pelo tamanho do
    # png. Quando o png do primario tem menos tiles que o teto, `resolver_tile`
    # do render_maps erraria; aqui o teto e explicito e conferido.
    if len(ts_pri["tiles"]) != n_tiles_pri:
        print(f"  aviso: {alvo['primary_tileset']} tem {len(ts_pri['tiles'])} tiles no png "
              f"e o teto da versao {versao} e {n_tiles_pri}; o atlas usa o TETO")
    pals = {}
    for v, c in ts_sec["paletas"].items():
        if v >= n_pal_pri:
            pals[v] = c
    for v, c in ts_pri["paletas"].items():
        if v < n_pal_pri:
            pals[v] = c
    meta = {"pri": ts_pri["metatiles"], "sec": ts_sec["metatiles"]}
    attr = {
        "pri": open(os.path.join(rm.caminho_tileset(alvo["primary_tileset"]),
                                 "metatile_attributes.bin"), "rb").read(),
        "sec": open(os.path.join(rm.caminho_tileset(alvo["secondary_tileset"]),
                                 "metatile_attributes.bin"), "rb").read(),
    }
    bd = open(os.path.join(RAIZ, alvo["blockdata_filepath"]), "rb").read()
    usados = collections.Counter()
    for i in range(0, len(bd), 2):
        usados[struct.unpack("<H", bd[i:i + 2])[0] & 0x3FF] += 1
    return dict(layout=alvo, versao=versao, n_meta_pri=n_meta_pri, n_tiles_pri=n_tiles_pri,
                n_pal_pri=n_pal_pri, tiles_pri=ts_pri["tiles"], tiles_sec=ts_sec["tiles"],
                pals=pals, meta=meta, attr=attr, usados=usados,
                nome_pri=alvo["primary_tileset"], nome_sec=alvo["secondary_tileset"])


def attr_de(d, mid):
    """O atributo cru. A LARGURA da entrada e deduzida do proprio par de
    arquivos, nunca da base do hack de origem: Emerald e Ruby usam 2 bytes e o
    FireRed usa 4, e o PRD (risco 3) registra que adivinhar isso pela base ja
    custou uma rodada. Aqui a conta e
    `len(metatile_attributes.bin) / (len(metatiles.bin) / 16)`, que so pode dar 2
    ou 4; qualquer outro valor e arquivo torto e o atlas diz isso em vez de
    desenhar rotulo errado."""
    lado = "pri" if mid < d["n_meta_pri"] else "sec"
    fonte = d["attr"][lado]
    n_meta = len(d["meta"][lado]) // 16
    if n_meta == 0:
        return None
    largura = len(fonte) // n_meta
    if largura not in (2, 4):
        return None
    base = mid if lado == "pri" else mid - d["n_meta_pri"]
    o = base * largura
    if o + largura > len(fonte):
        return None
    return int.from_bytes(fonte[o:o + largura], "little")


def atlas(nome, saida, so_nao_usados=False, lado="ambos", mostra_attr=False):
    d = dados_do_mapa(nome)
    n_pri_def = len(d["meta"]["pri"]) // 16
    n_sec_def = len(d["meta"]["sec"]) // 16
    ids = []
    if lado in ("ambos", "primario"):
        ids += list(range(min(n_pri_def, d["n_meta_pri"])))
    if lado in ("ambos", "secundario"):
        ids += [d["n_meta_pri"] + i for i in range(n_sec_def)]
    if so_nao_usados:
        ids = [m for m in ids if d["usados"].get(m, 0) == 0]
    if not ids:
        raise SystemExit("nenhum metatile para desenhar com esse filtro")
    lado_px = CEL * ESCALA
    linhas = (len(ids) + COLS - 1) // COLS
    cab = 22
    W = COLS * (lado_px + 2) + 2
    H = cab + linhas * (lado_px + ROT + 2) + 2
    folha = Image.new("RGB", (W, H), FUNDO)
    dr = ImageDraw.Draw(folha)
    titulo = (f"{nome}  {d['nome_pri']} + {d['nome_sec']}  ({d['versao']}, "
              f"primario={d['n_meta_pri']} metatiles / {d['n_pal_pri']} paletas)  "
              f"{'SO NAO USADOS  ' if so_nao_usados else ''}{len(ids)} metatiles")
    dr.text((4, 6), titulo, fill=(230, 230, 120))
    for k, mid in enumerate(ids):
        cx = 2 + (k % COLS) * (lado_px + 2)
        cy = cab + (k // COLS) * (lado_px + ROT + 2)
        img = desenha_metatile(mid, d["meta"], d["tiles_pri"], d["tiles_sec"], d["pals"],
                               d["n_tiles_pri"], d["n_meta_pri"])
        if img is not None:
            folha.paste(img.resize((lado_px, lado_px), Image.NEAREST), (cx, cy), img.resize((lado_px, lado_px), Image.NEAREST))
        rot = str(mid)
        if mostra_attr:
            a = attr_de(d, mid)
            rot += f" {a:04X}" if a is not None else " ????"
        cor = (150, 150, 150) if d["usados"].get(mid, 0) == 0 else (120, 220, 120)
        dr.text((cx, cy + lado_px), rot, fill=cor)
    os.makedirs(os.path.dirname(os.path.abspath(saida)) or ".", exist_ok=True)
    folha.save(saida)
    print(f"{saida}  {W}x{H}  {len(ids)} metatiles  "
          f"(verde = a cidade ja usa, cinza = nao usa)")
    return folha


def demo():
    """Auto-teste. Não checa beleza: checa que o atlas sabe REPROVAR."""
    falhas = []

    def caso(n, cond, msg):
        print(f"  T202.{n} {'ok  ' if cond else 'FALHA'} {msg}")
        if not cond:
            falhas.append(n)

    d = dados_do_mapa("GoldenrodCity")
    caso(1, d["versao"] == "johto" and d["n_meta_pri"] == 640 and d["n_pal_pri"] == 7,
         f"GoldenrodCity le como bigPrimary: versao={d['versao']} pri={d['n_meta_pri']} pals={d['n_pal_pri']}")
    usados_pri = [m for m in d["usados"] if m < d["n_meta_pri"]]
    caso(2, len(usados_pri) == 107,
         f"a cidade usa {len(usados_pri)} metatiles do primario (o condutor mediu 107)")
    img = desenha_metatile(sorted(usados_pri)[len(usados_pri) // 2], d["meta"], d["tiles_pri"],
                           d["tiles_sec"], d["pals"], d["n_tiles_pri"], d["n_meta_pri"])
    opacos = sum(1 for p in list(img.getdata()) if p[3] == 255)
    caso(3, opacos > 0, f"um metatile usado desenha {opacos} pixels opacos de 256")
    # O par negativo: um metatile fora do teto NAO pode desenhar.
    fora = desenha_metatile(d["n_meta_pri"] + len(d["meta"]["sec"]) // 16 + 5, d["meta"],
                            d["tiles_pri"], d["tiles_sec"], d["pals"], d["n_tiles_pri"],
                            d["n_meta_pri"])
    caso(4, fora is None, "metatile alem do fim do secundario devolve None em vez de folha preta")
    # Sabotagem: se o filtro de nao usados deixar passar um usado, o caso 5 acusa.
    ids_nu = [m for m in range(d["n_meta_pri"]) if d["usados"].get(m, 0) == 0]
    caso(5, all(d["usados"].get(m, 0) == 0 for m in ids_nu) and len(ids_nu) == d["n_meta_pri"] - len(usados_pri),
         f"o filtro deixa {len(ids_nu)} metatiles do primario, e nenhum deles esta no map.bin")
    # As paletas do primario mandam nas vagas dele, as do secundario nas outras.
    caso(6, all(v < d["n_pal_pri"] or v >= d["n_pal_pri"] for v in d["pals"]) and len(d["pals"]) >= 12,
         f"o atlas montou {len(d['pals'])} paletas resolvidas")
    largs = set()
    for lado in ("pri", "sec"):
        n = len(d["meta"][lado]) // 16
        largs.add(len(d["attr"][lado]) // n if n else 0)
    caso(7, largs == {2},
         f"a largura de atributo deduzida dos arquivos e {sorted(largs)}, e em Johto tem que ser 2")
    print(("DEMO VERDE" if not falhas else f"DEMO VERMELHA nos casos {falhas}"))
    return 1 if falhas else 0


def main():
    a = sys.argv[1:]
    if not a or a[0] == "--demo":
        return demo()
    if len(a) < 2:
        print(__doc__)
        return 1
    nome, saida = a[0], a[1]
    lado = "ambos"
    if "--lado" in a:
        lado = a[a.index("--lado") + 1]
    atlas(nome, saida, so_nao_usados="--nao-usados" in a, lado=lado, mostra_attr="--attr" in a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
