#!/usr/bin/env python3
"""Traduz o `behavior` do enum do FireRed para o do Emerald nos tilesets copiados
do subsolo de Goldenrod (GS Chronicles), e SÓ neles.

POR QUE ISTO EXISTE
-------------------
`copia_cidade.py` copia o atributo do metatile do hack byte a byte: ele converte
o formato (4 bytes do FireRed para 2 do Emerald, `extrai_tileset.py:146`) mas
NÃO traduz o VALOR do `behavior`, porque o valor é um índice de enum e os dois
enums não são o mesmo. O de fábrica está em `include/constants/metatile_behaviors.h`
e o do FireRed em `include/constants/metatile_behaviors_frlg.h`, que já estava no
repositório. Nos 0x00 a 0x65 os dois coincidem; a partir daí, não.

Medido nos SETE mapas do subsolo (os sete `map.bin`, metatile a metatile,
`dev_scripts/qa/...` e a varredura de 11/09/2026): dos 15 comportamentos que a
arte usa, SEIS divergem, e cinco deles são porta:

    0x60 MB_FRLG_CAVE_DOOR         -> MB_NON_ANIMATED_DOOR   (mesmo valor 0x60,
         nome diferente, MESMA função: teleporta ao PISAR. Fica como está.)
    0x6C MB_FRLG_UP_RIGHT_STAIR_WARP   -> MB_WATER_DOOR              -> 0xEB
    0x6D MB_FRLG_UP_LEFT_STAIR_WARP    -> MB_WATER_SOUTH_ARROW_WARP  -> 0xEC
    0x6E MB_FRLG_DOWN_RIGHT_STAIR_WARP -> MB_DEEP_SOUTH_WARP         -> 0xED
    0x6F MB_FRLG_DOWN_LEFT_STAIR_WARP  -> MB_UNUSED_6F               -> 0xEE
    0x89 MB_FRLG_CABINET               -> MB_SLOT_MACHINE            -> 0x00

As quatro escadas: o nosso motor TEM as quatro (`MB_UP_RIGHT_STAIR_WARP` e
irmãs, 0xEB a 0xEE, lidas por `IsDirectionalStairWarpMetatileBehavior`,
src/field_screen_effect.c:1743), só que em outro número. Sem esta tradução, as
NOVE escadas do subsolo viram porta de água e warp do sul, e a galeria da entrada
não desce para lugar nenhum.

O 0x89: `MB_SLOT_MACHINE` dispara o roteiro da máquina caça-níqueis do Game
Corner. É UMA célula, em (19,4) do labirinto de canos, e era um armário do
FireRed. Vira `MB_NORMAL`: a colisão da célula vem dos bits 10 e 11 do `map.bin`,
que são do autor e não mudam, então a parede continua parede e nada dispara.

O 0x81 (MB_FRLG_BOOKSHELF -> MB_UNUSED_81) fica como está DE PROPÓSITO: o nosso
0x81 não faz nada, que é exatamente o que queremos de um cano de esgoto. Traduzir
para `MB_BOOKSHELF` faria o esgoto responder "Crammed full of POKéMON books!".

Uso:
    python3 dev_scripts/atributos_frlg_subsolo.py            # aplica e imprime
    python3 dev_scripts/atributos_frlg_subsolo.py --conferir # só confere, exit 1
"""
import os
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TILESETS = []
for _base in ("goldenrod_city_underground_entrance", "goldenrod_city_underground_tunnel",
              "goldenrod_city_underground_switches", "goldenrod_city_underground_storage",
              "goldenrod_city_underground_warehouse", "goldenrod_city_sewers",
              "goldenrod_city_sewers_pipes"):
    TILESETS.append("data/tilesets/primary/%s_copia_pri/metatile_attributes.bin" % _base)
    TILESETS.append("data/tilesets/secondary/%s_copia_sec/metatile_attributes.bin" % _base)

DE_PARA = {
    0x6C: 0xEB,   # MB_FRLG_UP_RIGHT_STAIR_WARP   -> MB_UP_RIGHT_STAIR_WARP
    0x6D: 0xEC,   # MB_FRLG_UP_LEFT_STAIR_WARP    -> MB_UP_LEFT_STAIR_WARP
    0x6E: 0xED,   # MB_FRLG_DOWN_RIGHT_STAIR_WARP -> MB_DOWN_RIGHT_STAIR_WARP
    0x6F: 0xEE,   # MB_FRLG_DOWN_LEFT_STAIR_WARP  -> MB_DOWN_LEFT_STAIR_WARP
    0x89: 0x00,   # MB_FRLG_CABINET               -> MB_NORMAL (neutralizado)
}


def main():
    so_conferir = "--conferir" in sys.argv
    total = 0
    pendentes = 0
    for rel in TILESETS:
        caminho = os.path.join(REPO, rel)
        if not os.path.isfile(caminho):
            print("ERRO: não existe %s" % rel, file=sys.stderr)
            return 1
        dados = bytearray(open(caminho, "rb").read())
        mudou = 0
        for i in range(len(dados) // 2):
            v = struct.unpack_from("<H", dados, i * 2)[0]
            beh = v & 0xFF
            if beh in DE_PARA:
                novo = (v & 0xFF00) | DE_PARA[beh]
                struct.pack_into("<H", dados, i * 2, novo)
                mudou += 1
        if mudou:
            if so_conferir:
                pendentes += mudou
            else:
                with open(caminho, "wb") as f:
                    f.write(dados)
            print("%-72s %3d metatiles" % (rel, mudou))
        total += mudou
    if so_conferir:
        if pendentes:
            print("FALTA TRADUZIR: %d metatiles" % pendentes)
            return 1
        print("todos os atributos já estão no enum do Emerald")
        return 0
    print("total: %d metatiles traduzidos" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())
