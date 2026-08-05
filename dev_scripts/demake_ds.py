#!/usr/bin/env python3
"""Protótipo: converte a grade 2D por tile dos mapas de DS em map.bin do pokeemerald.

Descoberta que motiva o script: mapa de DS NÃO é só modelo 3D. Tanto a gen 4
(Platinum) quanto a gen 5 (Black 2) guardam, ao lado do modelo, uma grade 2D de
32x32 tiles com colisão e tipo de terreno. Essa grade converte direto para o
formato de bloco do pokeemerald.

Fontes do formato (conferidas byte a byte, não de memória):

  Gen 4, decomp pokeplatinum (fonte primária, é código do próprio jogo):
    include/constants/field/map.h
      TERRAIN_ATTRIBUTES_OFFSET 0x10, TERRAIN_ATTRIBUTES_SIZE 0x800,
      MAP_TILES_COUNT_X/Z 32, colisão = bit 15, comportamento = bits 0..7.
    include/constants/field/map_tile_behaviors.h  (enum TileBehavior nomeado)
    res/field/matrices/map_matrix_000.json        (planta do mundo, com nomes)

  Gen 5, medido na ROM Black 2 (IREO) porque não existe decomp:
    a/0/0/8  1065 arquivos. Cabeçalho u32 magia + 4 u32 de offset.
             Magia 0x00034257 ("WB\\3") = 961 arquivos com grade 2D.
             A seção do meio é: u16 largura=32, u16 altura=32, depois
             32*32 registros de 8 bytes (4 u16).
    a/0/0/9  416 matrizes: u32 tipo, u16 largura, u16 altura, células.
    a/0/1/2  zonedata, 615 registros de 48 bytes (+4 = índice da matriz,
             byte 26 = índice do nome do lugar em a/0/0/2 arquivo 109).

Uso:
    python3 dev_scripts/demake_ds.py            # autoteste + demonstração
    python3 dev_scripts/demake_ds.py gen4 0 saida.bin
    python3 dev_scripts/demake_ds.py gen5 0 saida.bin

O script NÃO registra nada em layouts.json, map_groups.json ou event_scripts.s.
Ele só lê o DS e escreve um map.bin solto. Registrar é passo separado.
"""

import os
import struct
import sys

RAIZ_DS = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/pokeplatinum"
NARC_MAPAS_GEN5 = "/tmp/claude-501/black_fs/data/a/0/0/8"
SAIDA_PADRAO = "/tmp/claude-501"

LADO = 32  # tanto gen 4 quanto gen 5 usam pedaço de 32x32 tiles


# ---------------------------------------------------------------- leitura DS

def narc_arquivos(caminho):
    """Lista os arquivos de dentro de um NARC de DS.

    NARC = cabeçalho de 16 bytes + chunks. BTAF tem a tabela de offsets,
    GMIF tem os dados. BTNF (nomes) é quase sempre vazio nos NARC da Game Freak.
    """
    dados = open(caminho, "rb").read()
    if dados[:4] != b"NARC":
        raise ValueError(f"{caminho} não é NARC (magia {dados[:4]!r})")
    pos, btaf, gmif = 16, None, None
    while pos < len(dados):
        magia = dados[pos:pos + 4]
        tam = struct.unpack_from("<I", dados, pos + 4)[0]
        if tam == 0:
            break
        if magia == b"BTAF":
            btaf = pos
        elif magia == b"GMIF":
            gmif = pos
        pos += tam
    if btaf is None or gmif is None:
        raise ValueError(f"{caminho}: faltou BTAF ou GMIF")
    n = struct.unpack_from("<I", dados, btaf + 8)[0]
    base = gmif + 8
    saida = []
    for i in range(n):
        ini, fim = struct.unpack_from("<II", dados, btaf + 12 + i * 8)
        saida.append(dados[base + ini:base + fim])
    return saida


def grade_gen4(indice, raiz=RAIZ_DS):
    """Grade 32x32 de um mapa de Platinum. Devolve lista de u16 crus.

    Cada u16: bit 15 = colisão, bits 0..7 = comportamento do tile.
    """
    caminho = os.path.join(raiz, f"res/field/maps/data/map_data_{indice:03d}.bin")
    dados = open(caminho, "rb").read()
    if len(dados) < 0x10 + 0x800:
        raise ValueError(f"{caminho}: curto demais para ter grade de permissão")
    return list(struct.unpack_from("<1024H", dados, 0x10))


_CACHE_NARC = {}


def _narc_cache(caminho):
    if caminho not in _CACHE_NARC:
        _CACHE_NARC[caminho] = narc_arquivos(caminho)
    return _CACHE_NARC[caminho]


def grade_gen5(indice, narc=NARC_MAPAS_GEN5):
    """Grade 32x32 de um pedaço de mapa de Black 2. Devolve (larg, alt, tuplas de 4 u16).

    O cabeçalho é: u32 magia + N u32 de offset, e o primeiro offset é o próprio
    tamanho do cabeçalho, então dá para descobrir N sem tabela fixa. Duas magias
    carregam grade: 0x00034257 ("WB", 961 arquivos, 4 offsets), 0x00044347
    ("GC", 60 arquivos, 5 offsets) e 0x00034452 ("RD", 8). A seção da grade é a
    que começa com u16 32, u16 32; os 0x0002474E ("NG", 36) não têm grade.
    Medido: 1028 dos 1065 arquivos entregam grade.
    """
    dados = _narc_cache(narc)[indice]
    if len(dados) < 8:
        raise ValueError(f"mapa {indice}: arquivo vazio")
    tam_cabecalho = struct.unpack_from("<I", dados, 4)[0]
    if tam_cabecalho % 4 or not 8 <= tam_cabecalho <= 64:
        raise ValueError(f"mapa {indice}: cabeçalho estranho ({tam_cabecalho})")
    offsets = list(struct.unpack_from(f"<{tam_cabecalho // 4 - 1}I", dados, 4))
    for ini, fim in zip(offsets, offsets[1:]):
        corpo = dados[ini:fim]
        if len(corpo) < 4 + LADO * LADO * 8:
            continue
        larg, alt = struct.unpack_from("<HH", corpo, 0)
        if (larg, alt) != (LADO, LADO):
            continue
        return larg, alt, [struct.unpack_from("<4H", corpo, 4 + i * 8) for i in range(larg * alt)]
    magia = struct.unpack_from("<I", dados, 0)[0]
    raise ValueError(f"mapa {indice}: magia {magia:#x} sem seção de grade 32x32")


def matriz_gen5(indice, narc="/tmp/claude-501/black_fs/data/a/0/0/9"):
    """Matriz de gen 5: (largura, altura, células). Célula = índice em a/0/0/8, 0xFFFF = vazio."""
    dados = narc_arquivos(narc)[indice]
    tipo, larg, alt = struct.unpack_from("<IHH", dados, 0)
    celulas = [struct.unpack_from("<H", dados, 8 + i * 4)[0] for i in range(larg * alt)]
    return larg, alt, celulas, tipo


# ------------------------------------------------------- tabela de tradução

# Metatiles do gTileset_GeneralSinnoh que já existem no repo. Os números não são
# chutados: saíram de contar o que os mapas de Sinnoh já feitos à mão usam
# (data/layouts/*/map.bin com primary_tileset gTileset_GeneralSinnoh) e de
# conferir o comportamento em data/tilesets/primary/general_sinnoh/metatile_attributes.bin.
# Formato: (metatile, colisão, elevação).
CHAO = (1, 0, 3)         # grama rasa andável, o bloco mais comum de Sinnoh
AREIA = (289, 0, 3)      # caminho de terra
GRAMA_ALTA = (13, 0, 3)  # comportamento MB_TALL_GRASS (0x02)
AGUA_MAR = (368, 0, 1)   # MB_OCEAN_WATER (0x15), elevação 1 = surfável
AGUA_LAGO = (161, 0, 1)  # MB_POND_WATER (0x10)
ARVORE = (470, 471, 478, 479)  # árvore 2x2 bloqueante, sempre colisão 1 elev 0

# Comportamento da gen 4 (enum TileBehavior do pokeplatinum) -> terreno nosso.
# Só entram os que valem a pena; o resto cai no padrão.
TRADUCAO_GEN4 = {
    0x02: GRAMA_ALTA,   # TILE_BEHAVIOR_TALL_GRASS
    0x03: GRAMA_ALTA,   # TILE_BEHAVIOR_VERY_TALL_GRASS
    0x10: AGUA_LAGO,    # TILE_BEHAVIOR_WATER_RIVER
    0x13: AGUA_LAGO,    # TILE_BEHAVIOR_WATERFALL
    0x15: AGUA_MAR,     # TILE_BEHAVIOR_WATER_SEA
    0x16: AGUA_LAGO,    # TILE_BEHAVIOR_PUDDLE
    0x17: AGUA_LAGO,    # TILE_BEHAVIOR_SHALLOW_WATER
    0x21: AREIA,        # TILE_BEHAVIOR_SAND
    0x08: CHAO,         # TILE_BEHAVIOR_CAVE_FLOOR
    0x0C: CHAO,         # TILE_BEHAVIOR_MOUNTAIN_FLOOR
}


def bloco(metatile, colisao, elevacao):
    """u16 do pokeemerald: 10 bits de metatile, 2 de colisão, 4 de elevação."""
    assert 0 <= metatile < 1024 and 0 <= colisao < 4 and 0 <= elevacao < 16
    return metatile | (colisao << 10) | (elevacao << 12)


def _arvore(x, y):
    return bloco(ARVORE[(y % 2) * 2 + (x % 2)], 1, 0)


def traduz_gen4(grade, larg=LADO):
    """Grade crua de Platinum -> lista de blocos do pokeemerald.

    Ordem das regras: terreno nomeado ganha da colisão, porque na gen 4 a água
    tem bit de colisão zerado (medido: comportamento 0x15 aparece 40261 vezes
    sem colisão contra 124 com) e quem impede de andar é o comportamento.
    """
    saida = []
    for i, bruto in enumerate(grade):
        x, y = i % larg, i // larg
        comportamento = bruto & 0xFF
        alvo = TRADUCAO_GEN4.get(comportamento)
        if alvo is not None:
            saida.append(bloco(*alvo))
        elif bruto & 0x8000:
            saida.append(_arvore(x, y))
        else:
            saida.append(bloco(*CHAO))
    return saida


def traduz_gen5(grade, larg=LADO):
    """Grade crua de Black 2 -> lista de blocos do pokeemerald.

    O que está provado: bit 0 do TERCEIRO u16 = bloqueado. Confirmado
    desenhando interiores (chunks 827, 937, 846), onde sai a planta baixa
    exata do prédio, chão cercado de vazio.

    O que NÃO está provado: a mesma regra aplicada aos pedaços do mapa-múndi
    de Unova deixa só ~20% dos tiles andáveis, baixo demais para rua e rota.
    A leitura provável é que os 8 bytes descrevem altura/rampa por tile e a
    regra "bit 0" só é fiel onde o terreno é plano. Enquanto isso não fechar,
    pedaço de exterior sai bloqueado demais e precisa de conserto à mão.

    O segundo u16 é um id de terreno coerente por região (581 valores no jogo
    inteiro) mas sem tradução conhecida, então NÃO vira grama nem água aqui.
    """
    saida = []
    for i, (_f0, _f1, f2, _f3) in enumerate(grade):
        x, y = i % larg, i // larg
        saida.append(_arvore(x, y) if f2 & 1 else bloco(*CHAO))
    return saida


def escreve_map_bin(caminho, blocos):
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "wb") as f:
        f.write(struct.pack(f"<{len(blocos)}H", *blocos))
    return caminho


# ----------------------------------------------------------------- desenho

def _simbolo_destino(b):
    metatile, colisao = b & 0x3FF, (b >> 10) & 3
    if colisao:
        return "T"
    if metatile == GRAMA_ALTA[0]:
        return '"'
    if metatile in (AGUA_MAR[0], AGUA_LAGO[0]):
        return "~"
    if metatile == AREIA[0]:
        return ","
    return "."


def desenha(origem, destino, larg=LADO, alt=LADO, titulo=""):
    """Imprime origem e gerado lado a lado, em texto."""
    print(titulo)
    print(f"{'ORIGEM (DS)':<{larg}}   GERADO (map.bin do pokeemerald)")
    for y in range(alt):
        a = "".join(origem[y * larg + x] for x in range(larg))
        b = "".join(_simbolo_destino(destino[y * larg + x]) for x in range(larg))
        print(f"{a}   {b}")
    print('legenda gerado: . chão   " grama alta   ~ água   , areia   T árvore (colisão)')
    print()


def simbolos_gen4(grade):
    saida = []
    for bruto in grade:
        c = bruto & 0xFF
        if c in (0x02, 0x03):
            saida.append('"')
        elif c in (0x10, 0x13, 0x15, 0x16, 0x17):
            saida.append("~")
        elif c == 0x21:
            saida.append(",")
        elif bruto & 0x8000:
            saida.append("#")
        else:
            saida.append(".")
    return saida


def simbolos_gen5(grade):
    return ["#" if t[2] & 1 else "." for t in grade]


# -------------------------------------------------------------------- demo

def demo():
    """Autoteste: falha alto se qualquer regra de conversão quebrar."""
    # 1. codificação do bloco
    assert bloco(13, 0, 3) == 0x300D, hex(bloco(13, 0, 3))
    assert bloco(470, 1, 0) == 0x05D6, hex(bloco(470, 1, 0))

    # 2. gen 4: Twinleaf Town é map_data_000 (map_matrix_000.json, célula x=3 y=27,
    #    header MAP_HEADER_TWINLEAF_TOWN -> MAP_000).
    g4 = grade_gen4(0)
    assert len(g4) == 1024
    b4 = traduz_gen4(g4)
    assert len(b4) == 1024
    # tem que existir chão livre e tem que existir bloqueio, senão a leitura está errada
    assert any((b >> 10) & 3 == 0 for b in b4) and any((b >> 10) & 3 for b in b4)
    escreve_map_bin(os.path.join(SAIDA_PADRAO, "demake_gen4_twinleaf.bin"), b4)
    desenha(simbolos_gen4(g4), b4,
            titulo="GEN 4  Platinum  map_data_000.bin  =  Twinleaf Town")

    # 3. gen 5
    if os.path.exists(NARC_MAPAS_GEN5):
        larg, alt, g5 = grade_gen5(0)
        assert (larg, alt) == (32, 32), (larg, alt)
        b5 = traduz_gen5(g5)
        assert any((b >> 10) & 3 == 0 for b in b5) and any((b >> 10) & 3 for b in b5)
        escreve_map_bin(os.path.join(SAIDA_PADRAO, "demake_gen5_000.bin"), b5)
        onde = ""
        try:
            mw, mh, cel, _t = matriz_gen5(175)
            i = cel.index(0)
            onde = f"  (célula x={i % mw} y={i // mw} da matriz 175, o mapa-múndi de Unova {mw}x{mh})"
        except (OSError, ValueError):
            pass
        desenha(simbolos_gen5(g5), b5,
                titulo=f"GEN 5  Black 2  a/0/0/8 arquivo 0{onde}")

        # interior: é aqui que a regra de colisão da gen 5 se prova sozinha,
        # porque sai a planta baixa do prédio em vez de ruído.
        _, _, g5i = grade_gen5(827)
        b5i = traduz_gen5(g5i)
        assert sum(1 for b in b5i if (b >> 10) & 3) == 826
        desenha(simbolos_gen5(g5i), b5i,
                titulo="GEN 5  Black 2  a/0/0/8 arquivo 827  =  interior da zona 1 (matriz 13, 1x1)")
    else:
        print(f"gen 5 pulada: {NARC_MAPAS_GEN5} não existe (desempacote a ROM antes)")

    print("autoteste OK")


def main():
    if len(sys.argv) == 1:
        demo()
        return
    gen, indice = sys.argv[1], int(sys.argv[2])
    saida = sys.argv[3] if len(sys.argv) > 3 else os.path.join(SAIDA_PADRAO, f"{gen}_{indice}.bin")
    if gen == "gen4":
        blocos = traduz_gen4(grade_gen4(indice))
    elif gen == "gen5":
        blocos = traduz_gen5(grade_gen5(indice)[2])
    else:
        raise SystemExit("uso: demake_ds.py [gen4|gen5] <indice> [saida.bin]")
    print(escreve_map_bin(saida, blocos), len(blocos), "blocos")


if __name__ == "__main__":
    main()
