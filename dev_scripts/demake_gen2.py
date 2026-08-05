#!/usr/bin/env python3
"""Converte mapa de Pokémon Crystal (gen 2) para map.bin do pokeemerald (gen 3).

Uso:
    python3 dev_scripts/demake_gen2.py                      # autoteste, desenha lado a lado
    python3 dev_scripts/demake_gen2.py NomeDoMapa saida.bin # converte um mapa

Por que existe: o `hns` não trouxe tudo de Johto. Faltam o esconderijo da Rocket
em Mahogany, e partes de Sprout Tower, Burned Tower e Farol de Olivine. O
disassembly oficial `pret/pokecrystal` tem TODOS eles, e mapa de gen 2 é
tile-based, não modelo 3D: a conversão para gen 3 é exata, não aproximada.

Como funciona, e por que é 1 para 1:
  - `maps/<Nome>.blk` é um byte por BLOCO, sem cabeçalho. As dimensões, em
    blocos, estão em `constants/map_constants.asm` como `map_const NOME, w, h`.
  - Um bloco de gen 2 tem 32x32 pixels; um metatile de gen 3 tem 16x16. Logo
    **um bloco = 2x2 metatiles**, e o mapa dobra de resolução.
  - `data/tilesets/<nome>_collision.asm` dá, para cada bloco, `tilecoll A,B,C,D`:
    a colisão dos quatro quadrantes, na ordem cima-esquerda, cima-direita,
    baixo-esquerda, baixo-direita. Cada quadrante É um metatile de gen 3. Por
    isso a conversão de colisão é exata: não se estima nada.

O que ESTE script NÃO resolve: qual metatile bonito usar. Ele escolhe pela CLASSE
(chão, parede, água, grama, escada, balcão) usando uma tabela do tileset de
destino. O acabamento visual continua sendo trabalho humano; o que se ganha é a
planta e a colisão corretas, que é o que faz o mapa ser jogável.
"""
import os
import re
import struct
import sys

CRYSTAL = "/tmp/claude-501/pcrystal"

# Fonte corrente. O caminho do pokecrystal continua sendo o padrao; quem converte
# outro projeto pokecrystal (o BW3G, em /tmp/bw3g-probe, cujos blocos sao .ablk)
# so troca estas duas variaveis antes de chamar `converte`. Medido em 05/08/2026:
# o .ablk e byte por bloco igual ao .blk, 198 dos 200 mapas com blocos proprios
# batem exato com `map_const NOME, w, h`.
FONTE = CRYSTAL
EXT = ".blk"

# Colisão do gen 2 -> classe. O gen 2 tem dezenas de nomes; o que importa para
# jogabilidade é andável, bloqueado, água, grama, e os especiais que mudam o
# comportamento (escada, balcão, warp).
CLASSE = {
    "FLOOR": "chao", "TALL_GRASS": "grama", "WATER": "agua",
    "LADDER": "escada", "CAVE": "chao", "DOOR": "porta",
    "COUNTER": "balcao", "BOOKSHELF": "parede", "PC": "parede",
    "RADIO": "parede", "TV": "parede", "TOWN_MAP": "parede",
    "WINDOW": "parede", "WALL": "parede",
}
# Tudo que começar com estes prefixos cai na classe indicada
PREFIXO = [("WARP", "porta"), ("HEADBUTT", "chao"), ("PIT", "chao"),
           ("CUT", "chao"), ("WATER", "agua"), ("WHIRLPOOL", "agua"),
           ("CURRENT", "agua"), ("WALL", "parede"), ("LADDER", "escada")]


def classe_de(nome):
    if nome in CLASSE:
        return CLASSE[nome]
    for p, c in PREFIXO:
        if nome.startswith(p):
            return c
    # desconhecido vira parede: prender o jogador é menos grave que deixá-lo
    # atravessar cenário e cair fora do mapa
    return "parede"


def dimensoes(nome_mapa):
    """(largura, altura) em BLOCOS, lidas da constante, não adivinhadas."""
    texto = open(os.path.join(FONTE, "constants/map_constants.asm")).read()
    # NomeDoMapa -> NOME_DO_MAPA. Separar SO minuscula->maiuscula: incluir digito
    # na regra transforma "B1F" em "B1_F" e nada casa. Este erro apareceu tres
    # vezes nesta sessao, em tres scripts diferentes.
    const = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", nome_mapa).upper()
    m = re.search(rf"^\s*map_const\s+{const},\s*(\d+),\s*(\d+)", texto, re.M)
    if not m:
        raise SystemExit(f"nao achei map_const para {nome_mapa} (tentei {const})")
    return int(m.group(1)), int(m.group(2))


def tileset_do_mapa(nome_mapa):
    """Descobre o arquivo de colisao lendo data/maps/maps.asm, nao chutando.

    O terceiro campo de `map_attributes` NAO e o tileset (e o bloco de borda);
    o tileset esta em `data/maps/maps.asm`, no formato
    `map Nome, TILESET_X, ...`. Usar o arquivo errado faz a colisao sair como
    ruido, e o mapa parece convertido mas e lixo.
    """
    texto = open(os.path.join(FONTE, "data/maps/maps.asm")).read()
    m = re.search(rf"^\s*map\s+{nome_mapa},\s*TILESET_(\w+),", texto, re.M)
    if not m:
        raise SystemExit(f"nao achei o tileset de {nome_mapa} em maps.asm")
    return m.group(1).lower() + "_collision.asm"


def colisao_do_tileset(arquivo_collision):
    """bloco -> (q_cima_esq, q_cima_dir, q_baixo_esq, q_baixo_dir) em classes."""
    tabela = {}
    caminho = os.path.join(FONTE, "data/tilesets", arquivo_collision)
    for linha in open(caminho):
        m = re.match(r"\s*tilecoll\s+(\w+),\s*(\w+),\s*(\w+),\s*(\w+)\s*;\s*([0-9a-fA-F]+)", linha)
        if m:
            bloco = int(m.group(5), 16)
            tabela[bloco] = tuple(classe_de(m.group(i)) for i in (1, 2, 3, 4))
    return tabela


def metatile_gen3(classe, paleta):
    """Classe -> (metatile, colisao). `paleta` vem do tileset de destino."""
    return paleta.get(classe, paleta["parede"])


def converte_blocos(blocos, lb, hb, tab, paleta):
    """O nucleo: blocos crus + dimensoes + tabela de colisao -> bytes do map.bin.

    Separado de `converte` porque o importador da Unova ja tem os blocos em mao
    (varios mapas do BW3G COMPARTILHAM o mesmo .ablk, entao o nome do mapa nao
    serve para achar o arquivo) e ja sabe as dimensoes.
    """
    lm, hm = lb * 2, hb * 2
    saida = bytearray(lm * hm * 2)
    for by in range(hb):
        for bx in range(lb):
            quad = tab.get(blocos[by * lb + bx], ("parede",) * 4)
            for i, (dx, dy) in enumerate(((0, 0), (1, 0), (0, 1), (1, 1))):
                mt, col = metatile_gen3(quad[i], paleta)
                x, y = bx * 2 + dx, by * 2 + dy
                # formato do pokeemerald: 10 bits de metatile, 2 de colisao, 4 de elevacao
                struct.pack_into("<H", saida, (y * lm + x) * 2, (mt & 0x3FF) | ((col & 3) << 10))
    return lm, hm, bytes(saida)


def converte(nome_mapa, paleta, arquivo_collision=None):
    """Devolve (largura_metatiles, altura_metatiles, bytes do map.bin)."""
    lb, hb = dimensoes(nome_mapa)
    blocos = open(os.path.join(FONTE, "maps", nome_mapa + EXT), "rb").read()
    if len(blocos) != lb * hb:
        raise SystemExit(f"{nome_mapa}: {EXT} tem {len(blocos)} bytes, constante diz {lb}x{hb}={lb*hb}")
    tab = colisao_do_tileset(arquivo_collision or tileset_do_mapa(nome_mapa))
    return converte_blocos(blocos, lb, hb, tab, paleta)


# Paleta provisória: metatiles do tileset que os interiores de Johto já usam.
# Trocar por metatiles bonitos é trabalho de acabamento; a planta e a colisao
# ja saem corretas com esta.
PALETA_INTERIOR = {
    "chao":   (1, 0),
    "parede": (5, 1),
    "agua":   (10, 1),
    "grama":  (3, 0),
    "escada": (7, 0),
    "porta":  (8, 0),
    "balcao": (6, 1),
}

SIMBOLO = {"chao": ".", "parede": "#", "agua": "~", "grama": '"',
           "escada": "^", "porta": "+", "balcao": "="}


def demo():
    if not os.path.isdir(CRYSTAL):
        raise SystemExit(f"clone o pret/pokecrystal em {CRYSTAL} primeiro")
    nome = "TeamRocketBaseB1F"
    lb, hb = dimensoes(nome)
    blocos = open(os.path.join(CRYSTAL, "maps", nome + ".blk"), "rb").read()
    tab = colisao_do_tileset(tileset_do_mapa(nome))
    lm, hm, dados = converte(nome, PALETA_INTERIOR)
    assert len(dados) == lm * hm * 2, "map.bin com tamanho errado"
    assert (lm, hm) == (lb * 2, hb * 2), "escala deveria ser 2x"

    print(f"{nome}: {lb}x{hb} blocos (gen 2)  ->  {lm}x{hm} metatiles (gen 3)")
    print("\nORIGEM: 1 caractere por BLOCO, classe do quadrante de cima-esquerda")
    for by in range(hb):
        print("  " + "".join(
            SIMBOLO[tab.get(blocos[by * lb + bx], ("parede",) * 4)[0]] for bx in range(lb)))
    print("\nGERADO: 1 caractere por METATILE, lido de volta do map.bin")
    inv = {v[0]: k for k, v in PALETA_INTERIOR.items()}
    for y in range(hm):
        linha = ""
        for x in range(lm):
            v = struct.unpack_from("<H", dados, (y * lm + x) * 2)[0]
            linha += SIMBOLO.get(inv.get(v & 0x3FF, "parede"), "?")
        print("  " + linha)
    print("\nautoteste passou: tamanho e escala conferidos")


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        lm, hm, dados = converte(sys.argv[1], PALETA_INTERIOR)
        open(sys.argv[2], "wb").write(dados)
        print(f"{sys.argv[1]}: {lm}x{hm} metatiles gravados em {sys.argv[2]}")
    else:
        demo()
