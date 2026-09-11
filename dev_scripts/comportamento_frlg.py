#!/usr/bin/env python3
"""Traduz o COMPORTAMENTO de metatile de um tileset vindo de ROM FireRed.

Por que existe, e o que ele descobriu
-------------------------------------
O `copia_mapa_rom.py` copia a planta e a arte com fidelidade de PIXEL: o render
do mapa copiado deu ZERO diferenca contra o render do mapa do hack. Isso prova a
imagem, e nao prova o JOGO. Duas coisas ficam erradas se ninguem olhar:

**1. O numero do comportamento nao quer dizer a mesma coisa nas duas bases.**
O nosso `include/constants/metatile_behaviors.h` e o de FireRed
(`fontes-mapas/pokefirered/include/constants/metatile_behaviors.h`) batem ate
0x10 e divergem depois. Quarenta valores mudam de numero. Exemplos medidos:

    FRLG 0x11 MB_FAST_WATER   -> nosso 44        FRLG 0x2A MB_ROCK_STAIRS -> nosso 79
    FRLG 0x84 MB_SIGNPOST     -> nosso 29        FRLG 0x87 MB_POKEBLOCK_FEEDER -> nosso 30

Sem traduzir, uma escada de pedra vira agua "surfavel" e o jogador nao sobe.

A PROVA de que a traducao certa e por NOME, e nao por tabela escrita a mao:
aplicar este de-para ao `data/tilesets/primary/general/metatile_attributes.bin`
do pokefirered reproduz, **byte a byte**, o
`data/tilesets/primary/general_frlg/metatile_attributes.bin` que este repo ja
tem (0 metatiles diferentes em 640). Ou seja, e exatamente a conversao que os
64 tilesets `*_frlg` do repo ja sofreram quando Kanto entrou. Isso e o
`--autoteste` deste arquivo.

**2. O FireRed decide encontro selvagem pelo ATRIBUTO, e nos decidimos pelo
COMPORTAMENTO.** Medido nas duas fontes:

    pokefirered/src/wild_encounter.c:366
        ExtractMetatileAttribute(attrs, METATILE_ATTRIBUTE_ENCOUNTER_TYPE) == TILE_ENCOUNTER_LAND
    nosso src/metatile_behavior.c:147
        sTileBitAttributes[metatileBehavior] & TILE_FLAG_HAS_ENCOUNTERS

Os tilesets do PROPRIO FireRed marcam as duas coisas (a grama da Route 1 e
comportamento 2 E encounterType 1), e por isso Kanto funciona aqui. Os metatiles
que o autor do hack DESENHOU podem marcar so o atributo. Foi o que o Liquid
Crystal fez nas tres areas do Safari: 660 celulas andaveis na montanha e 474 no
bosque tem `encounterType = 1` e comportamento `MB_NORMAL`. No nosso motor isso
e chao morto: **um Safari sem um Pokemon**, com build verde, suite verde e
render identico ao do hack.

`--encontro` fecha esse buraco. Onde o atributo diz "encontro de terra" e o
comportamento ficou `MB_NORMAL`, ele grava **`MB_UNUSED_05`**, que e o unico
comportamento do nosso motor com `TILE_FLAG_HAS_ENCOUNTERS` e NADA mais: da
encontro, nao desenha efeito de campo, nao muda colisao e nao e surfavel. Medido
antes de escolher: `MB_UNUSED_05` e usado por **zero** metatiles em todos os 221
tilesets do repo, entao ninguem herda comportamento novo. Usar `MB_TALL_GRASS`
no lugar daria encontro TAMBEM, mas desenharia moita de grama alta em cima de
caminho de terra, mudando o desenho que o portao de gosto acabou de aprovar.

Onde o atributo diz "encontro de agua" e o comportamento nao e surfavel no nosso
motor, ele grava `MB_POND_WATER`. (Nas tres areas do Safari isso nao acontece: a
agua do hack ja e `0x15`, que e `MB_OCEAN_WATER` nos dois enums.)

RODAR DUAS VEZES ESTRAGA, e por isso ele recusa
-----------------------------------------------
O de-para nao e idempotente, e isso e uma propriedade do dado, nao um descuido:
cinco valores, depois de traduzidos, continuam sendo CHAVE da tabela, e a
segunda passada os traduz de novo.

    32 MB_ICE <-> 35 MB_STRENGTH_BUTTON      (uma TROCA: a segunda passada desfaz)
    161 -> 202, 162 -> 203, 163 -> 204       (placa do Indigo Plateau vira video game)

O caminho normal e o `copia_mapa_rom.py`, que converte a pasta EXTRAIDA em /tmp
antes de instalar: cada import comeca da ROM, entao roda exatamente uma vez. Este
script solto e ferramenta de conserto, e por isso ele **recusa** mexer numa pasta
que ja esta dentro de `data/tilesets/` sem `--forca`.

O que ele NAO faz
-----------------
Ele nao inventa equivalencia. Valor de comportamento que existe no FireRed com
um nome que o nosso enum nao tem e **relatado, um a um, com a contagem**, e
passa intacto. Quem decide o que fazer com ele e gente, nao este script.

Uso
---
    comportamento_frlg.py --autoteste
    comportamento_frlg.py data/tilesets/primary/lc_outdoor            # so mede
    comportamento_frlg.py data/tilesets/primary/lc_outdoor --aplica --encontro
"""
import argparse
import collections
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POKEFIRERED = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/pokefirered"

MASCARA_COMPORTAMENTO = 0x1FF          # bits 0-8, formato de 4 bytes do FireRed
DESLOCA_ENCONTRO = 24
MASCARA_ENCONTRO = 0x7                 # bits 24-26
TILE_ENCOUNTER_LAND = 1
TILE_ENCOUNTER_WATER = 2


# --------------------------------------------------------------- as tres fontes

def enum_nosso(caminho=None):
    """nome -> valor, lido do nosso enum (que tem entradas com `= valor`)."""
    p = caminho or os.path.join(RAIZ, "include/constants/metatile_behaviors.h")
    s = open(p, encoding="utf-8").read()
    s = re.sub(r"//[^\n]*", "", s)
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    m = re.search(r"enum\s*\w*\s*\{(.*?)\}", s, re.S)
    if not m:
        raise ValueError("nao achei o enum em %s" % p)
    valor, tabela = 0, {}
    for item in [x.strip() for x in m.group(1).split(",") if x.strip()]:
        if "=" in item:
            nome, v = item.split("=")
            nome, valor = nome.strip(), int(v.strip(), 0)
        else:
            nome = item
        tabela[nome] = valor
        valor += 1
    return tabela


def enum_frlg(caminho=None):
    """nome -> valor, lido do pokefirered (que usa #define)."""
    p = caminho or os.path.join(POKEFIRERED, "include/constants/metatile_behaviors.h")
    s = open(p, encoding="utf-8").read()
    return {m.group(1): int(m.group(2), 0)
            for m in re.finditer(r"#define\s+(MB_[A-Z0-9_]+)\s+(0x[0-9A-Fa-f]+|\d+)", s)}


def de_para():
    """valor do FireRed -> valor nosso, casado por NOME.

    Devolve tambem os nomes do FireRed que o nosso enum nao tem: esses valores
    passam intactos e sao relatados.
    """
    N, F = enum_nosso(), enum_frlg()
    tabela = {v: N[nome] for nome, v in F.items() if nome in N}
    sem_par = {v: nome for nome, v in F.items() if nome not in N}
    return tabela, sem_par


def surfavel_no_nosso_motor():
    """Comportamentos com TILE_FLAG_SURFABLE, lidos de src/metatile_behavior.c.

    Lido, e nao lembrado: e essa tabela que decide se a agua copiada vira agua
    ou vira parede.
    """
    s = open(os.path.join(RAIZ, "src/metatile_behavior.c"), encoding="utf-8").read()
    m = re.search(r"sTileBitAttributes\[NUM_METATILE_BEHAVIORS\]\s*=\s*\{(.*?)\n\};", s, re.S)
    if not m:
        raise ValueError("nao achei sTileBitAttributes")
    N = enum_nosso()
    surf, enc = set(), set()
    for nome, flags in re.findall(r"\[(MB_[A-Z0-9_]+)\]\s*=\s*([^,\n]+)", m.group(1)):
        if nome not in N:
            continue
        if "TILE_FLAG_SURFABLE" in flags:
            surf.add(N[nome])
        if "TILE_FLAG_HAS_ENCOUNTERS" in flags:
            enc.add(N[nome])
    return surf, enc


# ------------------------------------------------------------------- a conversao

def converte(blob, com_encontro):
    """Devolve (novo_blob, relatorio). `blob` e o metatile_attributes.bin de 4 bytes."""
    if len(blob) % 4:
        raise ValueError("metatile_attributes.bin com %d bytes: nao e multiplo de 4, "
                         "entao nao e o formato de 4 bytes do FireRed" % len(blob))
    tabela, sem_par = de_para()
    surf, tem_encontro = surfavel_no_nosso_motor()
    N = enum_nosso()
    mb_normal = N["MB_NORMAL"]
    mb_sem_efeito = N["MB_UNUSED_05"]
    mb_agua = N["MB_POND_WATER"]

    saida = bytearray(blob)
    rel = {"traduzidos": collections.Counter(), "sem_par": collections.Counter(),
           "encontro_terra": 0, "encontro_agua": 0, "n": len(blob) // 4}
    for i in range(len(blob) // 4):
        v = struct.unpack_from("<I", blob, i * 4)[0]
        beh = v & MASCARA_COMPORTAMENTO
        novo = tabela.get(beh, beh)
        if beh in sem_par:
            rel["sem_par"][(beh, sem_par[beh])] += 1
        elif novo != beh:
            rel["traduzidos"][(beh, novo)] += 1
        if com_encontro:
            enc = (v >> DESLOCA_ENCONTRO) & MASCARA_ENCONTRO
            if enc == TILE_ENCOUNTER_LAND and novo == mb_normal:
                novo = mb_sem_efeito
                rel["encontro_terra"] += 1
            elif enc == TILE_ENCOUNTER_WATER and novo not in surf:
                novo = mb_agua
                rel["encontro_agua"] += 1
        struct.pack_into("<I", saida, i * 4, (v & ~MASCARA_COMPORTAMENTO) | novo)
    return bytes(saida), rel


def relata(rel, nomes_nossos):
    inv = {v: k for k, v in nomes_nossos.items()}
    print("  %d metatiles" % rel["n"])
    if rel["traduzidos"]:
        print("  comportamentos TRADUZIDOS por nome:")
        for (a, b), n in sorted(rel["traduzidos"].items()):
            print("     %3d -> %3d  %-34s  %d metatiles" % (a, b, inv.get(b, "?"), n))
    else:
        print("  nenhum comportamento mudou de numero")
    if rel["sem_par"]:
        print("  comportamentos do FireRed SEM equivalente no nosso enum (passaram intactos):")
        for (v, nome), n in sorted(rel["sem_par"].items()):
            print("     %3d  %-34s  %d metatiles   << decida o que fazer" % (v, nome, n))
    if rel["encontro_terra"] or rel["encontro_agua"]:
        print("  encontro que so existia no atributo e agora existe no comportamento:")
        print("     terra: %d metatiles viraram MB_UNUSED_05" % rel["encontro_terra"])
        print("     agua:  %d metatiles viraram MB_POND_WATER" % rel["encontro_agua"])


# -------------------------------------------------------------------- autoteste

def autoteste():
    falhas = []

    tabela, sem_par = de_para()
    ok = len(tabela) > 90 and tabela.get(0x11) == 44 and tabela.get(0x2A) == 79 and tabela.get(0) == 0
    if not ok:
        falhas.append("de_para")
    print("1. de-para por nome montado dos dois cabecalhos (%d nomes casados, %d sem par): %s"
          % (len(tabela), len(sem_par), "OK" if ok else "FALHOU"))

    # A prova forte: o de-para reproduz o que o repo ja fez com o FRLG.
    a = os.path.join(POKEFIRERED, "data/tilesets/primary/general/metatile_attributes.bin")
    b = os.path.join(RAIZ, "data/tilesets/primary/general_frlg/metatile_attributes.bin")
    if os.path.exists(a) and os.path.exists(b):
        origem, alvo = open(a, "rb").read(), open(b, "rb").read()
        convertido, _ = converte(origem, com_encontro=False)
        dif = sum(1 for i in range(len(alvo) // 4)
                  if struct.unpack_from("<I", convertido, i * 4)[0]
                  != struct.unpack_from("<I", alvo, i * 4)[0])
        ok2 = (len(origem) == len(alvo) and dif == 0)
        detalhe = "%d de %d metatiles diferentes" % (dif, len(alvo) // 4)
    else:
        ok2, detalhe = True, "pokefirered ausente, pulado"
    if not ok2:
        falhas.append("nao reproduz general_frlg")
    print("2. o de-para reproduz o general_frlg do repo a partir do general do "
          "pokefirered (%s): %s" % (detalhe, "OK" if ok2 else "FALHOU"))

    surf, enc = surfavel_no_nosso_motor()
    N = enum_nosso()
    ok3 = (N["MB_OCEAN_WATER"] in surf and N["MB_POND_WATER"] in surf
           and N["MB_PUDDLE"] not in surf and N["MB_UNUSED_05"] in enc
           and N["MB_UNUSED_05"] not in surf and N["MB_NORMAL"] not in enc)
    if not ok3:
        falhas.append("sTileBitAttributes")
    print("3. sTileBitAttributes lido do motor (MB_UNUSED_05 tem encontro e nao e "
          "surfavel, MB_PUDDLE nao tem): %s" % ("OK" if ok3 else "FALHOU"))

    # 4. o modo --encontro so mexe em quem estava em MB_NORMAL
    v_terra = (1 << DESLOCA_ENCONTRO) | N["MB_NORMAL"]
    v_grama = (1 << DESLOCA_ENCONTRO) | N["MB_TALL_GRASS"]
    v_agua = (2 << DESLOCA_ENCONTRO) | 0x15          # 0x15 = MB_OCEAN_WATER nos dois enums
    saida, rel = converte(struct.pack("<3I", v_terra, v_grama, v_agua), com_encontro=True)
    s0, s1, s2 = struct.unpack("<3I", saida)
    ok4 = ((s0 & MASCARA_COMPORTAMENTO) == N["MB_UNUSED_05"]
           and (s1 & MASCARA_COMPORTAMENTO) == N["MB_TALL_GRASS"]
           and (s2 & MASCARA_COMPORTAMENTO) == N["MB_OCEAN_WATER"]
           and rel["encontro_terra"] == 1 and rel["encontro_agua"] == 0
           and (s0 >> DESLOCA_ENCONTRO) & MASCARA_ENCONTRO == 1)
    if not ok4:
        falhas.append("--encontro")
    print("4. --encontro so promove quem ficou em MB_NORMAL, e nao toca no resto "
          "nem nos outros campos: %s" % ("OK" if ok4 else "FALHOU"))

    # 4b. a prova de que rodar duas vezes ESTRAGA, para ninguem tirar a trava
    tabela2, _ = de_para()
    encadeiam = {v: tabela2[v] for v in set(tabela2.values()) if v in tabela2 and tabela2[v] != v}
    ok4b = len(encadeiam) == 5 and encadeiam.get(32) == 35 and encadeiam.get(35) == 32
    if not ok4b:
        falhas.append("chaining")
    print("4b. a traducao NAO e idempotente, e sao estes %d valores que encadeiam "
          "(%s): %s" % (len(encadeiam), sorted(encadeiam), "OK" if ok4b else "FALHOU"))

    erro = None
    try:
        converte(b"\x00\x00\x00", com_encontro=False)
    except ValueError as e:
        erro = str(e)
    ok5 = erro is not None
    if not ok5:
        falhas.append("aceita arquivo de 2 bytes")
    print("5. arquivo que nao e de 4 bytes por metatile e FALHA DURA: %s"
          % ("OK" if ok5 else "FALHOU"))

    print("\n%s" % ("autoteste PASSOU" if not falhas else "autoteste REPROVOU: " + ", ".join(falhas)))
    return 0 if not falhas else 1


def main():
    if "--autoteste" in sys.argv:
        sys.exit(autoteste())
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("pasta", help="pasta do tileset (com metatile_attributes.bin de 4 bytes)")
    ap.add_argument("--aplica", action="store_true", help="grava; sem isso so mede")
    ap.add_argument("--encontro", action="store_true",
                    help="promove encontro que so existia no atributo do FireRed")
    ap.add_argument("--forca", action="store_true",
                    help="grava mesmo numa pasta ja instalada em data/tilesets/")
    a = ap.parse_args()
    p = os.path.join(a.pasta, "metatile_attributes.bin")
    if not os.path.exists(p):
        p2 = os.path.join(RAIZ, a.pasta, "metatile_attributes.bin")
        if not os.path.exists(p2):
            print("ERRO: nao achei %s" % p, file=sys.stderr)
            sys.exit(1)
        p = p2
    blob = open(p, "rb").read()
    novo, rel = converte(blob, a.encontro)
    print(p)
    relata(rel, enum_nosso())
    mudou = sum(1 for i in range(len(blob) // 4)
                if blob[i * 4:i * 4 + 4] != novo[i * 4:i * 4 + 4])
    print("  %d metatiles mudariam" % mudou)
    if a.aplica:
        if "data/tilesets/" in os.path.abspath(p) and not a.forca:
            print("  RECUSADO: esta pasta ja esta instalada no repo, e a traducao NAO e\n"
                  "  idempotente (32 e 35 trocam de lugar, 161-163 viram 202-204). Se este\n"
                  "  tileset ja passou pela conversao, rodar de novo o CORROMPE. O caminho\n"
                  "  normal e reimportar pelo copia_mapa_rom.py, que converte antes de\n"
                  "  instalar. Use --forca so se tiver certeza de que ele ainda esta cru.",
                  file=sys.stderr)
            sys.exit(1)
        open(p, "wb").write(novo)
        print("  GRAVADO")
    else:
        print("  (medicao apenas; use --aplica para gravar)")


if __name__ == "__main__":
    main()
