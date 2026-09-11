#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Repinta a FAIXA DE BORDA de uma cidade copiada com a arte do vizinho.

Por que isto existe, medido em 11/09/2026 em Ecruteak
------------------------------------------------------
O `copia_cidade.py` resolve METADE da costura. O motor desenha a faixa do mapa
vizinho com os TILESETS DO MAPA ATUAL, e isso vale nos DOIS sentidos:

  1. de dentro da cidade, a faixa da rota é desenhada com o tileset da CIDADE;
  2. de dentro da rota, a faixa da cidade é desenhada com o tileset da ROTA.

O `copia_cidade.py` só cobre o sentido 1, pinando os índices que a rota usa. O
sentido 2 não tem conserto por pino nenhum: teria de mudar `gTileset_JohtoGeneral`,
que é de toda a região. Medido em Ecruteak antes desta ferramenta: as 5 linhas de
baixo da cidade, vistas da Route37, viravam telhado azul, tijolo e água, porque os
índices da arte do hack significam outra coisa no tileset da rota.

O conserto é o único que existe: **as linhas da faixa passam a usar os índices
PINADOS**, que carregam a arte do vizinho e, por isso, desenham igual nos dois
lados. A cidade perde a arte do hack nessas linhas, e só nelas; é a declaração da
seção 3 do contrato ("a mudança declarada"), não um refino escondido.

Regra da repintura, e por que ela é esta
----------------------------------------
- célula ANDÁVEL vira grama do vizinho: é o que a Route37 tem do outro lado da
  borda (índice 188, usado pela própria trilha dela que entra na cidade), então o
  caminho do sul continua sem emenda;
- célula BLOQUEADA vira árvore do vizinho, com a PARIDADE certa: a árvore de
  Johto ocupa 2x1 metatiles (topo 20/21, base 28/29) e repete a cada 2 linhas e 2
  colunas. A linha 45 da cidade é a que encosta na linha 0 da Route37, e a Route37
  começa com o TOPO, então a linha 45 tem de ser a BASE para a árvore fechar em
  cima da emenda. A coluna segue `x % 2`, e como o offset da conexão é 16 (par) a
  paridade da cidade e a da rota são a mesma.
- os bits 10 a 15 (colisão e elevação do autor do hack) NÃO são tocados: só o
  índice de metatile, que são os 10 bits baixos.

A prova é a própria emenda: depois de rodar, a faixa desenhada com o tileset da
cidade e a mesma faixa desenhada com o tileset do vizinho têm de dar 0 pixel de
diferença. `--prova` mede isso e sai 1 se não der zero.

POR QUE ECRUTEAK NÃO USA ISTO NO FIM
------------------------------------
Rodou, deu 0 pixel nos dois sentidos, e MESMO ASSIM a conexão ficou quebrada: o
motor recarrega só o tileset SECUNDÁRIO quando o jogador atravessa uma conexão
(`LoadMapFromCameraTransition`, src/overworld.c:911), e a cidade copiada tem
primário próprio, então a rota inteira passava a ser desenhada com as paletas do
hack depois da travessia. Ecruteak tirou TODAS as conexões e virou travessia por
warp. Esta ferramenta fica de pé para a cidade que, por acaso, mantenha vizinho
de primário igual, e fica sobretudo como a MEDIDA que achou o defeito.

Uso:
    python3 dev_scripts/repinta_faixa_de_costura.py --mapa EcruteakCity \\
        --vizinho Route37 --linhas 41:45 --aplicar
    python3 dev_scripts/repinta_faixa_de_costura.py --mapa EcruteakCity \\
        --vizinho Route37 --linhas 41:45 --prova
"""
import argparse
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import copia_cidade as cc  # noqa: E402
import render_maps as rm  # noqa: E402

REPO = rm.REPO

MASCARA_INDICE = 0x03FF
MASCARA_RESTO = 0xFC00

# Arte de borda de Johto, lida de `gTileset_JohtoGeneral` e conferida no uso real
# da Route37 (linhas 0 a 7): a árvore é o par (20,21) em cima e (28,29) embaixo, e
# 188 é a grama do caminho que entra na cidade.
GRAMA = 188
ARVORE_TOPO = 20
ARVORE_BASE = 28


def carrega_layout(nome_mapa):
    layouts = rm.carregar_layouts()
    with open(os.path.join(REPO, "data/maps", nome_mapa, "map.json"), encoding="utf-8") as f:
        mj = json.load(f)
    return mj, layouts[mj["layout"]]


def palavras(lay):
    dados = open(os.path.join(REPO, lay["blockdata_filepath"]), "rb").read()
    return [struct.unpack_from("<H", dados, i * 2)[0] for i in range(len(dados) // 2)]


def repinta(pal, w, linhas, linha_de_baixo):
    """Devolve a lista de palavras já repintada, sem tocar em colisão/elevação."""
    novo = list(pal)
    for y in linhas:
        for x in range(w):
            v = pal[y * w + x]
            if ((v >> 10) & 3) == 0:
                i = GRAMA
            else:
                base = ((linha_de_baixo - y) % 2 == 0)
                i = (ARVORE_BASE if base else ARVORE_TOPO) + (x % 2)
            novo[y * w + x] = (v & MASCARA_RESTO) | i
    return novo


def desenha(lado, pal, w, xs, ys):
    from PIL import Image
    img = Image.new("RGB", (len(xs) * 16, len(ys) * 16), (0, 0, 0))
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            p = lado.desenha(pal[y * w + x] & MASCARA_INDICE, (0, 0, 0))
            if p is not None:
                img.paste(p, (i * 16, j * 16))
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--mapa", required=True)
    ap.add_argument("--vizinho", required=True)
    ap.add_argument("--linhas", required=True, help="faixa inclusiva, ex.: 41:45")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--prova", action="store_true")
    a = ap.parse_args()

    _mj, lay = carrega_layout(a.mapa)
    _vj, layv = carrega_layout(a.vizinho)
    w, h = lay["width"], lay["height"]
    y0, y1 = (int(t) for t in a.linhas.split(":"))
    linhas = list(range(y0, y1 + 1))

    pal = palavras(lay)
    novo = repinta(pal, w, linhas, h - 1)

    if a.aplicar:
        with open(os.path.join(REPO, lay["blockdata_filepath"]), "wb") as f:
            f.write(b"".join(struct.pack("<H", v) for v in novo))
        print("repintadas as linhas %d a %d de %s (%d células)"
              % (y0, y1, a.mapa, len(linhas) * w))

    if a.prova:
        atual = palavras(lay)
        cidade = cc.Lado(lay["primary_tileset"], lay["secondary_tileset"], 640, 640, 7)
        vizinho = cc.Lado(layv["primary_tileset"], layv["secondary_tileset"], 640, 640, 7)
        xs = list(range(w))
        a_img = desenha(cidade, atual, w, xs, linhas)
        b_img = desenha(vizinho, atual, w, xs, linhas)
        n, onde = cc.difere(a_img, b_img)
        print("prova de costura REVERSA (%s desenhado com o tileset de %s): "
              "%d pixels diferentes%s" % (a.mapa, a.vizinho, n,
                                          "" if n == 0 else " (primeiro em %s)" % (onde,)))
        return 0 if n == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
