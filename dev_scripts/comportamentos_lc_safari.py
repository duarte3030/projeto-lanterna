#!/usr/bin/env python3
"""Traduz os comportamentos de metatile dos dois tilesets do Safari do Liquid
Crystal, do enum do FireRed para o enum deste motor, e planta os tiles de
encontro selvagem das três áreas.

POR QUE ISTO EXISTE
-------------------
O `copia_mapa_rom.py` traz o atributo de metatile do hack BYTE A BYTE, com
`--attr 4` + `layout_version: frlg`, e o cabeçalho dele diz, com razão, que
nesse caminho "não há conversão e não há perda". Só que não perder BITS não é
a mesma coisa que o número QUERER dizer a mesma coisa nos dois jogos: o
FireRed e o Emerald numeram os comportamentos de metatile em enums
DIFERENTES a partir de 0x2A, e o motor deste repositório lê o enum do Emerald
(`include/constants/metatile_behaviors.h`).

Medido em 11/09/2026 nos três mapas do Safari, contando tile a tile:

  FRLG 0x2A MB_FRLG_ROCK_STAIRS   lido como  42 MB_SEAWEED_NO_SURFACING
  FRLG 0x93 MB_FRLG_BLUEPRINTS    lido como 147 MB_SECRET_BASE_SPOT_BROWN_CAVE_OPEN

O primeiro é escada de pedra e aparece 68 vezes na montanha, 44 delas em tile
PISÁVEL. `MB_SEAWEED_NO_SURFACING` está na tabela `sTileBitAttributes` de
src/metatile_behavior.c com `TILE_FLAG_SURFABLE | TILE_FLAG_HAS_ENCOUNTERS`:
o jogador subindo a escada estaria, para o motor, DENTRO D'ÁGUA, sorteando
encontro de `water_mons` no meio da serra. O segundo é a ÁRVORE da floresta
(151 tiles) e `MB_SECRET_BASE_SPOT_*_OPEN` é ponto de base secreta, que o
motor oferece ao jogador que aperta A de frente para ela.

Os 64 tilesets `*_frlg` que este repositório já tem NÃO têm esse defeito
porque a conversão já veio feita do upstream: `LAYOUT_ROUTE1` mede
MB_TALL_GRASS=2 e MB_SIGNPOST=29, e o signpost do FireRed é 0x84, ou seja o
número foi TRADUZIDO antes de entrar aqui. A tabela da tradução é a do
upstream, `migration_scripts/frlg_metatile_behavior_converter.py`, e é dela
que este script importa o de-para, em vez de copiar 200 linhas de tabela que
envelheceriam caladas.

AS DUAS EXCEÇÕES À TABELA DO UPSTREAM, e por quê
------------------------------------------------
1. `MB_FRLG_BLUEPRINTS` -> `MB_NORMAL` (o upstream manda para `MB_BLUEPRINTS`).
   Olhando os oito metatiles que usam 0x93 nestes dois tilesets (5, 517, 518,
   554, 555, 892, 893, 894), TODOS são ÁRVORE de fruto vermelho, e o Liquid
   Crystal usa 0x93 como cenário sólido, não como planta de engenharia.
   `MB_BLUEPRINTS` faz `GetInteractedMetatileScript` (src/field_control_avatar.c)
   devolver `EventScript_Blueprints`, que abre a caixa "Blueprints…" de
   data/scripts/flavor_text.inc. Seriam 151 árvores da floresta falando de
   planta baixa. Árvore sólida e muda é `MB_NORMAL` com colisão 1, que é o que
   ela já é.

2. Os tiles de CHÃO das três áreas ganham comportamento de ENCONTRO. Isto não
   é tradução, é JOGO NOSSO, e está aqui porque é a mesma passada de bytes.
   Medido: as três áreas copiadas do hack não têm UM ÚNICO tile de encontro em
   terra. Não há `MB_FRLG_TALL_GRASS` (0x02) em nenhum dos três `map.bin`,
   embora os tilesets TENHAM a arte de grama alta (metatiles 10 a 13, 508,
   516, 768 a 770) guardada sem uso. Sem tocar nisso, as tabelas de
   `wild_encounters.json` das três áreas nunca sorteariam nada em terra e o
   Safari de Johto seria um labirinto vazio.
   O que NÃO se faz para consertar: plantar grama no `map.bin`. A planta é
   cópia byte a byte do hack, com prova de render de zero pixel de diferença
   (METODO-COPIA-CIDADES.md, seção 1.1), e mexer nela é inventar desenho.
   O que se faz: dar ao chão QUE JÁ EXISTE o comportamento que combina com a
   arte dele, sem mexer em um pixel:
     - floresta, chão de grama  -> MB_TALL_GRASS (encontro + farfalhar verde)
     - montanha, chão de areia  -> MB_DEEP_SAND  (encontro + pegada na areia)
     - água, mar já copiado     -> MB_OCEAN_WATER, que o hack já tinha e que
       já é tile de encontro; nada a fazer.
   O tile da PORTA e os tiles do piso do portão ficam de fora de propósito:
   ninguém quer batalha no primeiro passo dentro da área.

GUARDA CONTRA RODAR DUAS VEZES
------------------------------
A tradução NÃO é idempotente: 0x93 vira 0x00 e 0x2A vira 0x4F, e uma segunda
passada leria esses números como se fossem do FireRed de novo. Por isso o
script confere o sha256 dos dois arquivos ANTES de escrever: só aceita o
estado de ENTRADA (o que saiu da ROM) e reconhece o estado de SAÍDA para
dizer "já foi feito" em vez de estragar.

Uso
---
    python3 dev_scripts/comportamentos_lc_safari.py            # só diz o que faria
    python3 dev_scripts/comportamentos_lc_safari.py --aplicar  # escreve
"""
import hashlib
import importlib.util
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PRIMARIO = "data/tilesets/primary/lc_outdoor/metatile_attributes.bin"
SECUNDARIO = "data/tilesets/secondary/lc_safari/metatile_attributes.bin"

# sha256 do arquivo COMO SAIU DA ROM (entrada válida desta ferramenta).
ENTRADA = {
    PRIMARIO: "31a999ff87f1479eade4dc5f857d68d81b850d3ebeff0218a4e15de865a1e5e0",
    SECUNDARIO: "61558cd9706602df293d8bde84045f0afe1beda1a5be4b8a2d372b54e877ecb8",
}

BEHAVIOR_MASK = 0x000001FF

# O corte primário/secundário da versão de layout "frlg", de include/fieldmap.h.
# É por ele que o id de metatile do map.bin vira índice dentro de um dos dois
# arquivos: id < 640 é primário, id >= 640 é o secundário menos 640.
CORTE_FRLG = 640

# Chão de ENCONTRO, por id de metatile como ele aparece no map.bin (ou seja, já
# com o 640 somado no secundário). Os ids saíram da contagem dos tiles PISÁVEIS
# (colisão 0) dos três map.bin, e cada um foi OLHADO no atlas antes de entrar:
# id 890 é areia, id 898 é grama, e assim por diante.
CHAO_DE_ENCONTRO = {
    # floresta: grama rasteira com tufos e flores
    898: "MB_TALL_GRASS",   # 474 tiles, o chão liso da floresta
    1: "MB_TALL_GRASS",     # 131 tiles, grama com flores (aparece também na água)
    9: "MB_TALL_GRASS",     # 94 tiles
    784: "MB_TALL_GRASS",   # 84 tiles
    786: "MB_TALL_GRASS",   # 70 tiles
    785: "MB_TALL_GRASS",   # 68 tiles
    8: "MB_TALL_GRASS",     # 62 tiles, grama com moita baixa
    17: "MB_TALL_GRASS",    # 1 tile, grama com flor vermelha
    # montanha: chão de areia batida
    890: "MB_DEEP_SAND",    # 660 tiles, o chão de toda a serra
    187: "MB_DEEP_SAND",    # 15 tiles
    113: "MB_DEEP_SAND",    # 12 tiles
    108: "MB_DEEP_SAND",    # 3 tiles
    186: "MB_DEEP_SAND",    # 3 tiles
}

# Fica FORA do encontro de propósito: o piso do portão de cada área (883, 887,
# 889 na montanha; 731, 733 na floresta; 211 a 213 na entrada de areia) e o
# próprio tile da porta. Batalha no tile de chegada tiraria do jogador a chance
# de ler a fala do atendente antes do primeiro passo.


def carrega_tabela_do_upstream():
    """Importa FRLG_BEHAVIORS / EMERALD_BEHAVIORS / FRLG_TO_EMERALD do conversor
    que veio no upstream. Importar em vez de copiar: se o upstream corrigir o
    de-para, esta ferramenta corrige junto."""
    caminho = os.path.join(RAIZ, "migration_scripts",
                           "frlg_metatile_behavior_converter.py")
    spec = importlib.util.spec_from_file_location("_conv_frlg", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.FRLG_BEHAVIORS, mod.EMERALD_BEHAVIORS, mod.FRLG_TO_EMERALD


def de_para(frlg_behaviors, emerald_behaviors, frlg_to_emerald):
    """número do FireRed -> número deste motor, com a exceção da BLUEPRINTS."""
    tabela = {}
    for numero, nome in frlg_behaviors.items():
        alvo = frlg_to_emerald[nome]
        if nome == "MB_FRLG_BLUEPRINTS":
            alvo = "MB_NORMAL"      # exceção 1, motivo no cabeçalho
        tabela[numero] = emerald_behaviors[alvo]
    return tabela


def sha(caminho):
    return hashlib.sha256(open(caminho, "rb").read()).hexdigest()


def converte(dados, tabela, desconhecidos):
    saida = []
    for valor in dados:
        bruto = valor & BEHAVIOR_MASK
        if bruto in tabela:
            novo = tabela[bruto]
        else:
            desconhecidos.add(bruto)
            novo = bruto
        saida.append(novo | (valor & ~BEHAVIOR_MASK))
    return saida


def main():
    aplicar = "--aplicar" in sys.argv
    frlg, eme, mapa = carrega_tabela_do_upstream()
    tabela = de_para(frlg, eme, mapa)
    nome_de = {v: k for k, v in eme.items()}

    estados = {}
    for rel in (PRIMARIO, SECUNDARIO):
        caminho = os.path.join(RAIZ, rel)
        estados[rel] = sha(caminho)
    if all(estados[r] == ENTRADA[r] for r in ENTRADA):
        pass
    else:
        print("Os atributos NÃO estão no estado de entrada desta ferramenta.")
        for rel in (PRIMARIO, SECUNDARIO):
            print(f"  {rel}\n    agora    {estados[rel]}\n    esperado {ENTRADA[rel]}")
        print("Provavelmente a conversão já foi aplicada e commitada. Nada a fazer:\n"
              "rodar de novo leria os números JÁ convertidos como se fossem do\n"
              "FireRed e estragaria o tileset.")
        return 1

    desconhecidos = set()
    total_mudou = 0
    for rel in (PRIMARIO, SECUNDARIO):
        caminho = os.path.join(RAIZ, rel)
        bruto = open(caminho, "rb").read()
        dados = list(struct.unpack("<%dI" % (len(bruto) // 4), bruto))
        novos = converte(dados, tabela, desconhecidos)

        base = 0 if rel == PRIMARIO else CORTE_FRLG
        plantados = 0
        for mid, nome in CHAO_DE_ENCONTRO.items():
            i = mid - base
            if not (0 <= i < len(novos)):
                continue
            if base == 0 and mid >= CORTE_FRLG:
                continue
            novos[i] = (novos[i] & ~BEHAVIOR_MASK) | eme[nome]
            plantados += 1

        mudou = sum(1 for a, b in zip(dados, novos) if a != b)
        total_mudou += mudou
        print(f"{rel}: {len(dados)} metatiles, {mudou} atributos mudam, "
              f"{plantados} deles são chão de encontro plantado")
        for antes, depois in sorted({(a & BEHAVIOR_MASK, b & BEHAVIOR_MASK)
                                     for a, b in zip(dados, novos)
                                     if (a & BEHAVIOR_MASK) != (b & BEHAVIOR_MASK)}):
            print(f"    0x{antes:02X} {frlg.get(antes, '?')} -> "
                  f"{depois} {nome_de.get(depois, '?')}")
        if aplicar:
            with open(caminho, "wb") as f:
                f.write(struct.pack("<%dI" % len(novos), *novos))

    if desconhecidos:
        print("comportamentos do FireRed que a tabela do upstream não conhece "
              "(ficaram como estavam): " +
              ", ".join("0x%02X" % d for d in sorted(desconhecidos)))
    if aplicar:
        print(f"ESCRITO. {total_mudou} atributos mudaram.")
        for rel in (PRIMARIO, SECUNDARIO):
            print(f"  {rel}  sha256 {sha(os.path.join(RAIZ, rel))}")
    else:
        print("(ensaio: nada foi escrito; passe --aplicar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
