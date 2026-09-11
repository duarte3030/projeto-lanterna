#!/usr/bin/env python3
"""Troca UM tileset secundário de cidade de Hoenn pelo do Pokémon Blazing Emerald v1.6.

Contexto: decisão do Gui de 11/09/2026 (resposta 71), "copia Blazing Emerald"
inteiro em Hoenn. O primário `general` já foi trocado (commit f9d87a2659). Este
script faz o passo 2, cidade a cidade, e existe porque a operação se repete
treze vezes: treze secundários para as dezesseis cidades (Littleroot, Oldale e
Petalburg dividem `petalburg`; Mauville e Verdanturf dividem `mauville`).

O QUE ELE COPIA, e o que ele recusa a copiar (contrato METODO-COPIA-CIDADES
seções 1 e 3):

  tiles.png            copiado inteiro do hack
  palettes/06..12      copiadas do hack; são as sete que um secundário carrega
                       (NUM_PALS_IN_PRIMARY 6, NUM_PALS_TOTAL 13 em
                       include/fieldmap.h). As 00..05 são do primário e as
                       13..15 são de clima e reflexo: nenhuma das duas famílias
                       vem do tileset, então nenhuma das duas é tocada.
  metatiles.bin        copiado do hack SÓ até a nossa contagem de metatiles (a
                       contagem nossa é size(metatile_attributes.bin)/2). O que
                       passa disso não existe para os nossos mapas.
  metatile_attributes  NÃO É TOCADO. Comportamento e layerType continuam nossos,
                       célula a célula, que é o que a seção 1 do contrato cobra.

A RECUSA QUE JUSTIFICA O SCRIPT EXISTIR, medida em 11/09/2026: três dos treze
tilesets do hack têm metatile que aponta para índice de tile FORA do tileset
deles (petalburg 74 e 75, slateport 253 e 367, mauville 0). No GBA esses índices
caem em vaga de VRAM que o tileset não preenche, ou seja, sobra do tileset
anterior: lixo. Em petalburg os dois aparecem UMA vez cada nos NOSSOS mapas.
Copiar esses metatiles põe lixo no mapa; por isso eles ficam com a definição
NOSSA, e o script imprime quais foram.

O `-num_tiles` de src/data/tilesets/graphics.h é acertado junto, porque o
tileset do hack quase sempre tem mais tile que o nosso (petalburg 159 -> 271) e
um `-num_tiles` velho cortaria a arte nova sem erro de build.

Uso:
    python3 dev_scripts/copia_secundario_blazing.py <pasta>            # só mede
    python3 dev_scripts/copia_secundario_blazing.py <pasta> --aplicar  # escreve

<pasta> é o nome em disco em data/tilesets/secondary/ (ex.: slateport,
ever_grande). A extração do hack é procurada em --fonte (padrão: a pasta
blaz/<pasta> do scratchpad desta frente).
"""
import argparse
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# A extração fica FORA do repositório de propósito: a ROM do hack e o que sai
# dela não entram em repositório com remoto (contrato seção 6). Ela é
# reproduzível com, por exemplo:
#   python3 fontes-mapas/romhacks/ferramentas/extrai_tileset.py \
#       blazing-emerald 0x3DF764 <saida>/slateport --nome slateport --sec
# Offsets dos treze secundários de cidade, medidos em 11/09/2026:
#   petalburg 0x3DF71C   rustboro 0x3DF734   dewford 0x3DF74C
#   slateport 0x3DF764   mauville 0x3DF77C   lavaridge 0x3DF794
#   fallarbor 0x3DF7AC   fortree 0x3DF7C4    lilycove 0x3DF7DC
#   mossdeep 0x3DF7F4    ever_grande 0x3DF80C pacifidlog 0x3DF824
#   sootopolis 0x3DF83C  (e o primário general em 0x3DF704)
FONTE_PADRAO = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/extraidos/blazing-emerald"
GRAPHICS = os.path.join(RAIZ, "src/data/tilesets/graphics.h")
PALETAS_DO_SECUNDARIO = range(6, 13)  # NUM_PALS_IN_PRIMARY .. NUM_PALS_TOTAL-1


def rotulo(pasta):
    """slateport -> Slateport ; ever_grande -> EverGrande"""
    return "".join(p.capitalize() for p in pasta.split("_"))


def tiles_do_png(caminho):
    from PIL import Image
    im = Image.open(caminho).convert("P")
    w, h = im.size
    px = im.load()
    return [bytes(px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8))
            for ty in range(h // 8) for tx in range(w // 8)]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pasta")
    ap.add_argument("--fonte", default=None)
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()

    nosso = os.path.join(RAIZ, "data/tilesets/secondary", a.pasta)
    fonte = a.fonte or os.path.join(FONTE_PADRAO, a.pasta)
    for p in (nosso, fonte):
        if not os.path.isdir(p):
            sys.exit(f"pasta não encontrada: {p}")

    attr = os.path.join(nosso, "metatile_attributes.bin")
    n_meta = os.path.getsize(attr) // 2
    with open(os.path.join(fonte, "info.json"), encoding="utf-8") as f:
        n_tiles_hack = json.load(f)["tiles_na_rom"]

    mb = open(os.path.join(fonte, "metatiles.bin"), "rb").read()
    ma = open(os.path.join(nosso, "metatiles.bin"), "rb").read()
    if len(mb) < n_meta * 16:
        sys.exit(f"o hack só tem {len(mb)//16} metatiles e nós temos {n_meta}: não dá para copiar")

    # metatile do hack que aponta para tile inexistente no tileset dele
    teto = 512 + n_tiles_hack
    recusados = []
    saida = bytearray()
    for i in range(n_meta):
        bloco = mb[i * 16:(i + 1) * 16]
        ruim = any((struct.unpack_from("<H", bloco, j * 2)[0] & 0x3FF) >= teto for j in range(8))
        if ruim:
            recusados.append(i)
            saida += ma[i * 16:(i + 1) * 16]
        else:
            saida += bloco
    mudados = sum(1 for i in range(n_meta) if saida[i*16:(i+1)*16] != ma[i*16:(i+1)*16])

    ta = tiles_do_png(os.path.join(nosso, "tiles.png"))
    tb = tiles_do_png(os.path.join(fonte, "tiles.png"))
    k = min(len(ta), len(tb))
    tdif = sum(1 for i in range(k) if ta[i] != tb[i]) + abs(len(ta) - len(tb))

    pals = []
    for p in PALETAS_DO_SECUNDARIO:
        fa = os.path.join(nosso, "palettes", f"{p:02d}.pal")
        fb = os.path.join(fonte, "palettes", f"{p:02d}.pal")
        if os.path.exists(fb):
            iguais = (os.path.exists(fa)
                      and open(fa, "rb").read().replace(b"\r\n", b"\n")
                      == open(fb, "rb").read().replace(b"\r\n", b"\n"))
            pals.append((p, iguais))

    print(f"tileset          : {a.pasta}  (gTileset_{rotulo(a.pasta)})")
    print(f"tiles            : nossos {len(ta)} -> deles {len(tb)}; {tdif} tiles mudam")
    print(f"metatiles        : {n_meta} nossos; {mudados} mudam; {len(recusados)} recusados {recusados}")
    print(f"paletas 06 a 12  : {sum(1 for _, ig in pals if not ig)} mudam de {len(pals)}")
    print("atributos        : NÃO tocados (comportamento e layerType continuam nossos)")

    if not a.aplicar:
        print("\n(só medição; rode com --aplicar para escrever)")
        return 0

    import shutil
    shutil.copyfile(os.path.join(fonte, "tiles.png"), os.path.join(nosso, "tiles.png"))
    for p, _ in pals:
        shutil.copyfile(os.path.join(fonte, "palettes", f"{p:02d}.pal"),
                        os.path.join(nosso, "palettes", f"{p:02d}.pal"))
    with open(os.path.join(nosso, "metatiles.bin"), "wb") as f:
        f.write(saida)

    texto = open(GRAPHICS, encoding="utf-8").read()
    alvo = f'const u32 gTilesetTiles_{rotulo(a.pasta)}[] = INCGFX_U32("data/tilesets/secondary/{a.pasta}/tiles.png"'
    linhas = texto.split("\n")
    achou = False
    for i, linha in enumerate(linhas):
        if linha.startswith(alvo):
            achou = True
            nova = re.sub(r'-num_tiles \d+', f'-num_tiles {n_tiles_hack}', linha)
            if nova == linha and "-num_tiles" not in linha:
                nova = linha.replace('".4bpp.fastSmol");',
                                     f'".4bpp.fastSmol", "-num_tiles {n_tiles_hack} -Wnum_tiles");')
            linhas[i] = nova
            print(f"graphics.h       : {nova.strip()}")
            break
    if not achou:
        sys.exit(f"não achei a linha de gTilesetTiles_{rotulo(a.pasta)} em graphics.h")
    open(GRAPHICS, "w", encoding="utf-8").write("\n".join(linhas))
    print("\nescrito.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
