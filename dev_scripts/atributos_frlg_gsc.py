#!/usr/bin/env python3
"""Traduz o `behavior` do enum do FireRed para o do Emerald nos tilesets copiados
do GS Chronicles pelo pacote da resposta 69 (e na Goldenrod GSC, que ficou com
o mesmo defeito desde 11/09/2026).

É o mesmo problema que `atributos_frlg_subsolo.py` resolveu no subsolo: a
`copia_cidade.py` converte o FORMATO do atributo (4 bytes para 2) mas não o
VALOR, e o valor é índice de enum. Medido metatile a metatile nos mapas do
pacote (`map.bin` de cada um), os valores usados que divergem são dois:

    0x84 MB_FRLG_SIGNPOST            -> nosso 0x84 é MB_CABLE_BOX_RESULTS_1
                                        vira MB_SIGNPOST (0x1D)
    0x87 MB_FRLG_POKEMON_CENTER_SIGN -> nosso 0x87 é MB_POKEBLOCK_FEEDER
                                        vira MB_POKEMON_CENTER_SIGN (0x1E)

O 0x87 importa: MB_POKEBLOCK_FEEDER abre o menu de pôr Pokéblock do Safari de
Hoenn quando o jogador encara a célula. Na Goldenrod GSC ele estava na placa do
Centro Pokémon, em (42,22). O 0x84 deixava placa sem evento respondendo como
caixa de TV a cabo. Os ginásios de Ecruteak e Olivine já tinham sido
traduzidos assim (0x1D e 0x1E) pelos executores deles.

Depois da tradução, uma segunda passada NEUTRALIZA (vira MB_NORMAL, layerType
intacto) porta e seta que o autor desenhou em célula que ninguém alcança, e que
a `lente_portas.py` acusaria como porta ao ar livre sem warp (P1):

    praça da torre, metatile 29   MB_ANIMATED_DOOR no telhado da torre, (11,5),
                                  cercado de mar e sem caminho a pé
    National Park, metatiles 80 e 84   MB_WEST_ARROW_WARP no lado de lá da
                                  guarita leste, (40,17) e (40,18), colisão 1
    National Park, metatiles 53 e 54   MB_NON_ANIMATED_DOOR no pé da guarita
                                  sul, (10,57) e (11,57), colisão 1

É o mesmo conserto da seta num tile de parede da Azalea (ESTADO 0.ah, item 5).

Os destinos não são chave da tabela, então rodar duas vezes não estraga.
Só a camada de comportamento muda: o render fica com ZERO pixel de diferença.

Uso:
    python3 dev_scripts/atributos_frlg_gsc.py            # aplica e imprime
    python3 dev_scripts/atributos_frlg_gsc.py --conferir # só confere, exit 1
"""
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASES = ("goldenrod_city", "violet_city_gym", "violet_city_gym2_f",
         "goldenrod_city_radio_plaza", "route36_clearing", "route42_clearing",
         "national_park_normal")
TILESETS = []
for _b in BASES:
    TILESETS.append("data/tilesets/primary/%s_copia_pri/metatile_attributes.bin" % _b)
    TILESETS.append("data/tilesets/secondary/%s_copia_sec/metatile_attributes.bin" % _b)

DE_PARA = {
    0x84: 0x1D,   # MB_FRLG_SIGNPOST            -> MB_SIGNPOST
    0x87: 0x1E,   # MB_FRLG_POKEMON_CENTER_SIGN -> MB_POKEMON_CENTER_SIGN
}


NEUTRALIZA = {
    "data/tilesets/primary/goldenrod_city_radio_plaza_copia_pri/metatile_attributes.bin": (29,),
    "data/tilesets/primary/national_park_normal_copia_pri/metatile_attributes.bin": (53, 54, 80, 84),
}


def main():
    so_conferir = "--conferir" in sys.argv
    pendentes = 0
    for rel in TILESETS:
        caminho = os.path.join(REPO, rel)
        dados = bytearray(open(caminho, "rb").read())
        mudou = 0
        for i in range(len(dados) // 2):
            v = struct.unpack_from("<H", dados, i * 2)[0]
            if (v & 0xFF) in DE_PARA:
                struct.pack_into("<H", dados, i * 2, (v & 0xFF00) | DE_PARA[v & 0xFF])
                mudou += 1
        for idx in NEUTRALIZA.get(rel, ()):
            v = struct.unpack_from("<H", dados, idx * 2)[0]
            if v & 0xFF:
                struct.pack_into("<H", dados, idx * 2, v & 0xFF00)
                mudou += 1
        if mudou:
            pendentes += mudou
            if not so_conferir:
                open(caminho, "wb").write(dados)
            print("%-72s %3d metatiles" % (rel, mudou))
    if so_conferir:
        print("FALTA TRADUZIR: %d metatiles" % pendentes if pendentes else "todos traduzidos")
        return 1 if pendentes else 0
    print("total: %d metatiles traduzidos" % pendentes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
