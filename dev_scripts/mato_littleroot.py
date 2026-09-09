#!/usr/bin/env python3
"""Refino de `LittlerootTown` (tema VILA DE MATO), e o KIT COMPARTILHADO das três
cidades do `gTileset_Petalburg` (`LittlerootTown`, `PetalburgCity` e
`OldaleTown`).

Este arquivo é o gerador de Littleroot E o módulo que `bosque_petalburg.py` e
`estrada_oldale.py` importam: as três cidades dividem UM secundário, então o kit
de metatiles é escrito UMA vez, aqui, e as outras duas passadas só planejam o
mapa delas.

O QUE ESTA CIDADE TEM DE ERRADO, medido pela `dev_scripts/regua_cidades.py`
nesta árvore em 09/09/2026: `LittlerootTown` gasta 79,5% do chão andável a pé
(213 células de 268) com UM metatile, o 1, a grama lisa do `gTileset_General`.
É o pior carimbo das quatro regiões da onda. A vila do professor Birch é, hoje,
um tapete verde de vinte por vinte com três prédios em cima e uma cerca de
árvores em volta.

O ORÇAMENTO, medido nesta árvore e não herdado de brief:

  tiles      o `tiles.png` do secundário tem 160 vagas (128x80) e o
             `src/data/tilesets/graphics.h` compila 159 delas
             (`-num_tiles 159 -Wnum_tiles`, medido na linha 1 do arquivo). 130
             vagas são referenciadas por metatile vivo. ESTA PASSADA NÃO GASTA
             NENHUMA: o `tiles.png`, os dezesseis `.pal` e o `graphics.h` ficam
             byte a byte iguais.
  metatiles  o `metatiles.bin` tem 2.304 bytes, ou seja 144 metatiles (ids 512 a
             655), e o `metatile_attributes.bin` tem 288, ou seja 2 bytes por
             metatile. Os seis mapas irmãos usam 99 deles. O kit ENTRA DEPOIS do
             144, em locais novos, e por isso os dois arquivos CRESCEM em vez de
             ter vaga sobrescrita: nenhum metatile que já existe é tocado.
             O teto é 512 (`NUM_METATILES_IN_PRIMARY`, `include/fieldmap.h`,
             `layout_version` `emerald`).
  paletas    nenhuma. O kit não escreve cor nenhuma.
  animação   `python3 dev_scripts/pinos_anim.py gTileset_Petalburg` diz
             "vagas de tile pinadas: nenhuma": o `InitTilesetAnim_Petalburg` põe
             `sSecondaryTilesetAnimCallback = NULL`. Não há vaga reservada.

OS SEIS MAPAS IRMÃOS, lidos do `data/layouts/layouts.json` e não supostos:
`PetalburgCity`, `LittlerootTown`, `OldaleTown`, `Route101`, `Route102` e
`Route103`. E um aviso que precisa ficar escrito: existem MAIS QUATRO layouts
apontando para `gTileset_Petalburg` (`SnowbelleCity_Layout`,
`KiloudeCity_Layout`, `VictoryRoad_Kalos_Layout` e `KalosLeague_Layout`), e os
quatro têm `blockdata_filepath` igual a `data/layouts/PetalburgCity/map.bin`.
São esboços de Kalos que ainda emprestam o mapa de Petalburg; eles não têm
`map.bin` próprio, então mudar o de `PetalburgCity` muda os quatro por
construção, e isso é fato, não risco escondido.

A ARTE, e de onde vem cada peça. NADA É IMPORTADO, e a razão é MEDIDA:

  - O `custom_vs_nosso.json` das ferramentas de ROM hack diz que o secundário da
    família Petalburg do `scorched-silver` (0x492424, o hack que o Gui chama de
    "o mais moderno") tem `frac_nova = 0.000` contra o nosso, e o do
    `run-and-bun` (0x4AAB38) também `0.000`: os dois são, tile a tile, o que já
    está no repositório. Não há o que importar de lá.
  - `mega-emerald-x-y` e `x-y-emerald` não têm secundário da família Petalburg
    nenhum (só `petalburg_gym`, e esse com `frac_nova = 0.000`).
  - `golden-glazed` não tem NENHUM tileset que case com `secondary/petalburg`.
  - Sobra o `light-platinum` 0x286D0C, `frac_nova = 0.960`, e ele foi ABERTO e
    OLHADO (prancha em 09/09/2026): é um tileset de CIDADE MODERNA, com torres
    de vidro, chafariz e escultura, não de vila de mato. O chão dele, medido nos
    mapas g00m09 e g00m16 do próprio hack, tem média RGB (80,114,70) e
    (96,132,67), um verde-oliva escuro; a nossa grama é (116,197,165). A
    distância é 131,2 e 119,3, contra o critério de ~50 que Pastoria, Sandgem e
    Hearthome fixaram. Uma mancha dessas no meio da vila não lê como variação,
    lê como buraco. REPROVADO por cor, com o número.

  Por isso o `CREDITS.md` NÃO É TOCADO nesta passada: não há asset importado a
  creditar, e inventar seção seria mentira de arquivo.

  O que entra vem todo do `gTileset_General`, que é NOSSO e já está compilado na
  ROM, e do próprio `gTileset_Petalburg`:

  CHÃO 1, as MANCHAS com borda de verdade. O `gTileset_General` tem TRÊS
  autotiles de remendo de chão completos, de nove peças cada, com canto
  arredondado e franja desenhada, e nenhum deles custa um byte:
    - grama gasta (o verde-menta com pintas amarelas): 464 465 466 / 472 473 474
      / 480 481 482;
    - terra batida: 259 260 261 / 267 268 269 / 275 276 277;
    - areia: 280 281 282 / 288 289 290 / 296 297 298.
  É a resposta direta à lição paga em Pastoria ("textura de chão importada SEM
  borda de transição vira retalho"): estas texturas JÁ VÊM com a borda, porque
  são autotile e não recorte.
  ARMADILHA MEDIDA no meio delas: o MIOLO da terra batida, o metatile 268, tem
  atributo 0x00A0, ou seja comportamento `MB_BERRY_TREE_SOIL`. Pintar ele numa
  célula de grama mudaria o comportamento de célula ANDÁVEL, que é o item 4 do
  portão de planta, e ainda por cima poria solo de amoreira sem amoreira. O
  miolo da terra entra REMONTADO: metatile novo NOSSO, mesma arte, comportamento
  ZERADO. Os outros oito da terra e os nove das outras duas famílias já são
  0x0000 e entram diretos.

  CHÃO 2, o RUÍDO que quebra o repeat de dezesseis pixels. A grama do carimbo é
  o par de tiles 2 e 3 no arranjo [2,3,3,2], e os dois diferem entre si por 15,4
  (distância RGB média por pixel, a mesma conta do `varia_carimbo.py`). Nove
  ARRANJOS do mesmo par (espelho horizontal, vertical, os dois, troca de
  quadrante e quatro misturas) dão nove metatiles cujas distâncias par a par
  ficam todas entre 12,0 e 17,3, acima do piso de 8,0 do `varia_carimbo.py`, e
  custam ZERO tile e ZERO cor. Os mesmos nove arranjos servem às outras três
  famílias, porque as quatro têm a MESMA estrutura [a,b,b,a]: a grama
  (2/3, paleta 2), a grama gasta (266/282, paleta 2), a terra (268/284,
  paleta 3) e a areia (264/280, paleta 5).
  DITO EM VOZ ALTA, porque boa notícia é suspeita: esta camada é SUTIL. Ela não
  é o enfeite, é o fundo; ela existe para a grama parar de repetir o mesmo bloco
  de 16x16 duzentas vezes, que é o que faz um tapete parecer tapete. O enfeite
  de verdade são as manchas, os caminhos e a mobília, e o relatório separa
  quanto da régua caiu por causa de cada um.

  MÓVEL, tudo em célula SOLIDIFICADA, com comportamento ZERADO e layerType
  COVERED. Oito peças entram DIRETAS, sem gastar metatile nenhum, porque já
  existem com a camada de baixo IGUAL à do carimbo (as quatro entradas
  0x2002 0x2003 0x2003 0x2002, conferidas e não supostas) e já são COVERED:
    - 514, a moita redonda do próprio `gTileset_Petalburg`, que NENHUM dos seis
      mapas irmãos usa hoje;
    - 224, o matacão do `gTileset_General`;
    - 110 e 111, a pedra miúda e o espelho dela;
    - 307, o mourão solto;
    - 328, 329 e 330, a cerca de três peças (ponta esquerda, meio e ponta
      direita), que é o que faz uma vila parecer vila.
  E três peças entram REMONTADAS (metatile novo, arte de cima copiada, camada de
  baixo trocada pela do carimbo, atributo trocado para COVERED): o arbusto do
  metatile 14 e a touceira do 30 com o espelho dela do 31. As três estão no
  primário com layerType NORMAL, que desenha a arte ACIMA do jogador; remontar é
  o que as torna móvel de verdade em vez de defeito E3.

O CAMINHÃO DE MUDANÇA, que é a marca de Littleroot na abertura do Emerald, JÁ
ESTÁ NO MAPA e não precisou de nada: ele não é metatile, é o sprite
`gObjectEventPic_Truck` (`src/data/object_events/object_event_graphics.h`, linha
229) e o `data/maps/LittlerootTown/map.json` já traz DOIS object events com
`OBJ_EVENT_GFX_TRUCK`, em (2,10) e em (11,10). O caminhão aparece na foto do
emulador desta passada, no canto noroeste. Esta passada não põe nem tira object
event nenhum: o `map.json` fica INTOCADO. O que ela fez pelo caminhão foi o
chão em volta dele parar de ser tapete.

O QUE FICOU DE FORA, com o motivo:
  - O metatile 4, o canteiro de flores. Ele é COVERED e as três cidades já o
    usam como célula ANDÁVEL (15 vezes só em Littleroot). Plantá-lo como sólido
    faria a mesma flor ser pisável num canto e parede no outro, que lê como bug.
  - Os metatiles 2, 211 e 212, que a régua de cor apontou como os mais parecidos
    com a grama (19,2 / 19,9 / 21,3). Foram ABERTOS e são grama com uma FAIXA DE
    BARRANCO marrom no topo: são peça de beira de penhasco, não variante de
    gramado. Uma delas solta no meio da vila poria um paredão de dez pixels
    flutuando.
  - O metatile 28, o verde escuro chapado (61,5 de distância). Sem pinta e sem
    borda, no meio do gramado ele lê como sombra sem quem a faça.
  - As placas 27 e 305 (a de recado e a do ginásio). Placa sem texto atrás é
    promessa que o jogo não cumpre.

Uso:
    python3 dev_scripts/mato_littleroot.py                 # mede e mostra o plano
    python3 dev_scripts/mato_littleroot.py --aplicar
    python3 dev_scripts/mato_littleroot.py --desfazer
    python3 dev_scripts/mato_littleroot.py --demo          # auto-teste
    python3 dev_scripts/mato_littleroot.py --so-tileset    # só o kit no tileset
"""
import collections
import glob
import heapq
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")
os.environ.setdefault("REPO_MAPAS", RAIZ)
import arte_ginasios_sinnoh as G     # noqa: E402
import enfeita_cidades as E          # noqa: E402

# O bloco de teste DESTA rodada é o único que o varredor de corredores pula: os
# casos dele foram escritos DEPOIS do desenho e a partir dele, então tratá-los
# como corredor a preservar seria circular. Os outros blocos valem inteiros.
E.BLOCO_PROPRIO = "210_mato_littleroot.json"

DESTINO = f"{RAIZ}/data/tilesets/secondary/petalburg"
PRIMARIO = "gTileset_General"
SECUNDARIO = "gTileset_Petalburg"
PLANO = f"{RAIZ}/dev_scripts/vila_petalburg.json"   # plano das TRÊS cidades

# Os seis irmãos com `map.bin` próprio, lidos do layouts.json.
IRMAOS = ["PetalburgCity", "LittlerootTown", "OldaleTown",
          "Route101", "Route102", "Route103"]

TETO_TILES = 512            # NUM_TILES_IN_PRIMARY, include/fieldmap.h
TETO_META = 512             # NUM_METATILES_IN_PRIMARY, include/fieldmap.h
META_LOCAL_0 = 144          # o `metatiles.bin` tem 144 hoje: o kit vai DEPOIS
MARGEM = 1
TETO_REGUA = 20.0
MULTI_NIVEL = 15            # ELEVATION_MULTI_LEVEL: casa com QUALQUER elevação
PISO_DISTANCIA = 8.0        # o piso do `varia_carimbo.py` para variante visível

CARIMBO = 1                 # a grama lisa do primário, o carimbo das TRÊS
# O MIOLO do autotile de grama gasta. Ele é o SEGUNDO carimbo de `OldaleTown`
# (69 células, 28,9%), e por isso o kit monta uma segunda cópia de TODA a
# mobília com a camada de baixo dele: móvel com chão de grama pousado numa
# célula de grama gasta deixaria um quadrado verde em volta da peça, que é a
# costura que a frente de Veilstone pagou para aprender. As duas cópias existem
# sempre, para o kit sair igual nas três cidades, e cada cidade usa a que quer.
CARIMBO2 = 473
BASES_MOVEL = [CARIMBO, CARIMBO2]
SUFIXO_BASE = {CARIMBO: "", CARIMBO2: " clara"}

# ------------------------------------------------------------- as FAMÍLIAS
# Cada família é um chão [a,b,b,a] do `gTileset_General`. `fill` é o metatile do
# primário que JÁ desenha o miolo dela (None quando o miolo do primário tem
# comportamento próprio e precisa ser remontado); `auto` são as nove peças do
# autotile na ordem [NO,N,NE, O,C,E, SO,S,SE].
FAMILIAS = {
    "grama": dict(a=2, b=3, pal=2, fill=1, auto=None),
    "gasta": dict(a=266, b=282, pal=2, fill=473,
                  auto=[464, 465, 466, 472, 473, 474, 480, 481, 482]),
    # o miolo da terra (268) é MB_BERRY_TREE_SOIL: entra remontado, ver o
    # cabeçalho. `fill=None` manda o kit criar o miolo NOSSO.
    "terra": dict(a=268, b=284, pal=3, fill=None,
                  auto=[259, 260, 261, 267, None, 269, 275, 276, 277]),
    "areia": dict(a=264, b=280, pal=5, fill=289,
                  auto=[280, 281, 282, 288, 289, 290, 296, 297, 298]),
}

# Os nove arranjos do par [a,b,b,a]. Cada entrada é (tile, espelho), com espelho
# em 0..3: bit 1 = horizontal (0x400), bit 2 = vertical (0x800). O primeiro é o
# ARRANJO DO CARIMBO e não vira metatile novo: ele está aqui para a conferência
# de distância poder comparar contra ele.
ARRANJOS = [
    ("carimbo",   [("a", 0), ("b", 0), ("b", 0), ("a", 0)]),
    ("espelhoH",  [("a", 1), ("b", 1), ("b", 1), ("a", 1)]),
    ("espelhoV",  [("a", 2), ("b", 2), ("b", 2), ("a", 2)]),
    ("espelhoHV", [("a", 3), ("b", 3), ("b", 3), ("a", 3)]),
    ("giro",      [("b", 1), ("a", 1), ("a", 1), ("b", 1)]),
    ("troca",     [("b", 0), ("a", 0), ("a", 0), ("b", 0)]),
    ("misto1",    [("a", 0), ("b", 1), ("b", 2), ("a", 3)]),
    ("misto2",    [("b", 3), ("a", 2), ("a", 1), ("b", 0)]),
    ("misto3",    [("a", 1), ("b", 0), ("b", 3), ("a", 2)]),
    ("misto4",    [("b", 2), ("a", 3), ("a", 0), ("b", 1)]),
]

# ------------------------------------------------------------------ os MÓVEIS
# DIRETO: metatile que JÁ existe, já é COVERED, já tem a camada de baixo igual à
# do carimbo e nenhum dos seis irmãos usa como sólido novo. Custo: ZERO.
MOVEIS_DIRETOS = [
    dict(nome="moita redonda", mt=514),
    dict(nome="matacao",       mt=224),
    dict(nome="pedra",         mt=110),
    dict(nome="pedra virada",  mt=111),
    dict(nome="mourao",        mt=307),
]
# REMONTADO: a arte de cima de um metatile do primário, posta sobre a camada de
# baixo do carimbo, com atributo COVERED e comportamento ZERADO.
MOVEIS_REMONTADOS = [
    dict(nome="arbusto",            de=14),
    dict(nome="touceira",           de=30),
    dict(nome="touceira espelhada", de=31),
]
# CERCA: corrida horizontal de células sólidas, ponta esquerda, meio e ponta
# direita. As três peças já existem no primário e já são COVERED.
CERCA = dict(esq=328, meio=329, dir=330)

ESPACO_ENTRE_MOVEIS = 2     # Chebyshev mínimo entre dois móveis QUAISQUER

N4 = E.N4


def _mistura(*n):
    """Hash determinista de inteiros, 32 bits. Nada de `random`: o plano tem que
    sair idêntico em qualquer máquina e em qualquer versão de Python."""
    h = 0x811C9DC5
    for x in n:
        h = ((h ^ (x & 0xFFFFFFFF)) * 0x01000193) & 0xFFFFFFFF
        h ^= h >> 15
    return h


# ------------------------------------------------------------ leitura do nosso
def _ler(nome):
    return open(f"{DESTINO}/{nome}", "rb").read()


def _tileset(rotulo):
    import render_maps as RM
    return RM.carregar_tileset(rotulo)


def _entradas_pri(mt):
    tp = _tileset(PRIMARIO)
    return list(struct.unpack_from("<8H", tp["metatiles"], mt * 16))


def _entradas_qq(mt):
    """As oito entradas do metatile, venha ele do primário ou do secundário."""
    if mt < 512:
        return _entradas_pri(mt)
    ts = _tileset(SECUNDARIO)
    return list(struct.unpack_from("<8H", ts["metatiles"], (mt - 512) * 16))


def _n_metatiles_sec():
    return len(_ler("metatiles.bin")) // 16


def chao_nosso(mt=CARIMBO):
    """(as quatro entradas da camada de BAIXO do carimbo, o atributo dele)."""
    ents = _entradas_pri(mt)
    if any(v & 0x3FF for v in ents[4:]):
        raise SystemExit("o carimbo %d tem arte na camada de cima" % mt)
    return ents[:4], G._attrs(PRIMARIO)[mt]


# -------------------------------------------------------- a RÉGUA DE COR
def _px_quads(quads, pal):
    """Os 256 pixels RGB de um metatile montado só com a camada de baixo."""
    from PIL import Image
    import render_maps as RM
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    im = Image.new("RGB", (16, 16), (0, 0, 0))
    p = im.load()
    cores = [tuple(c) for c in tp["paletas"][pal]]
    for q, (t, f) in enumerate(quads):
        tile = RM.resolver_tile(tp, ts, t)
        RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile, cores,
                         bool(f & 1), bool(f & 2))
    return list(im.get_flattened_data())


def _dist(a, b):
    """Distância RGB MÉDIA POR PIXEL, a mesma conta do `varia_carimbo.py`."""
    return sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
               for p, q in zip(a, b)) / 256.0


def arranjos_da_familia(fam):
    """(sobreviventes, cortados) dos nove arranjos, pela régua de cor.

    O corte é MEDIDO e não escolhido a dedo, e a razão é uma medida que só
    apareceu depois de rodar o auto-teste: espelhar um par de tiles só produz
    variante VISÍVEL se os tiles tiverem textura. A grama (2/3) e a grama gasta
    (266/282) têm pinta, e os nove arranjos delas ficam entre 12,0 e 17,3 de
    distância. A terra (268/284) e a areia (264/280) são quase chapadas, e os
    mesmos nove arranjos caem para 2,7 a 5,8, abaixo do piso de 8,0: ali o
    espelho não é variação, é enganar a régua, e o gerador CORTA sozinho.
    """
    tiles = {"a": fam["a"], "b": fam["b"]}
    pix = {nome: _px_quads([(tiles[k], f) for (k, f) in quads], fam["pal"])
           for nome, quads in ARRANJOS}
    fica, corta = [ARRANJOS[0][0]], []
    for nome, _quads in ARRANJOS[1:]:
        pior = min(_dist(pix[nome], pix[o]) for o in fica)
        if pior < PISO_DISTANCIA:
            corta.append((nome, pior))
        else:
            fica.append(nome)
    return [n for n in fica[1:]], corta


# ---------------------------------------------------------------------- o KIT
def desenha_kit():
    """(metas, attrs, kit) sem escrever em disco.

    `metas` é {local: [8 entradas]} e `attrs` {local: atributo}, os dois só com
    locais NOVOS (>= META_LOCAL_0). `kit` descreve as peças por nome.
    """
    base, attr_chao = chao_nosso()
    metas, attrs = {}, {}
    proximo = [META_LOCAL_0]
    kit = dict(familias={}, moveis=[], cerca=None)

    def poe(ents, attr):
        local = proximo[0]
        metas[local] = list(ents)
        attrs[local] = attr
        proximo[0] += 1
        return 512 + local

    # -------------------------------------------------- 1. CHÃO: os arranjos
    for nome_fam, fam in FAMILIAS.items():
        tiles = {"a": fam["a"], "b": fam["b"]}
        vivos, cortados = arranjos_da_familia(fam)
        por_nome = dict(ARRANJOS)
        variantes = []
        for nome_arr in vivos:
            quads = por_nome[nome_arr]
            ents = [(fam["pal"] << 12) | (f << 10) | tiles[k] for (k, f) in quads]
            variantes.append(dict(nome="%s %s" % (nome_fam, nome_arr),
                                  mt=poe(ents + [0, 0, 0, 0], attr_chao)))
        fill = fam["fill"]
        auto = list(fam["auto"]) if fam["auto"] else None
        if fill is None:
            # o miolo do primário tem comportamento próprio: remonta o NOSSO
            ents = [(fam["pal"] << 12) | tiles[k] for (k, _f) in ARRANJOS[0][1]]
            fill = poe(ents + [0, 0, 0, 0], attr_chao)
            if auto:
                auto[4] = fill
        kit["familias"][nome_fam] = dict(fill=fill, auto=auto,
                                         variantes=variantes,
                                         cortados=cortados,
                                         pal=fam["pal"], a=fam["a"], b=fam["b"])

    # ------------------------------------------------------------ 2. MÓVEIS
    # Uma cópia por BASE. Na base do carimbo, as peças diretas não custam nada
    # (o metatile já existe com a camada de baixo certa); nas outras bases toda
    # peça vira metatile novo, com a MESMA arte de cima e a camada de baixo do
    # carimbo daquela base.
    kit["cercas"] = []
    for base_mt in BASES_MOVEL:
        b_ent, _b_attr = chao_nosso(base_mt)
        suf = SUFIXO_BASE[base_mt]
        for m in MOVEIS_DIRETOS:
            if base_mt == CARIMBO:
                kit["moveis"].append(dict(nome=m["nome"], mt=m["mt"],
                                          remontado=False, base=base_mt))
                continue
            cima = _entradas_qq(m["mt"])[4:]
            kit["moveis"].append(dict(nome=m["nome"] + suf, remontado=True,
                                      de=m["mt"], base=base_mt,
                                      mt=poe(list(b_ent) + list(cima), 0x1000)))
        for m in MOVEIS_REMONTADOS:
            cima = _entradas_pri(m["de"])[4:]
            if not any(v & 0x3FF for v in cima):
                raise SystemExit("o metatile %d não tem arte na camada de cima"
                                 % m["de"])
            # comportamento ZERADO e layerType COVERED (0x1000): as duas camadas
            # ficam ABAIXO do sprite do jogador.
            kit["moveis"].append(dict(nome=m["nome"] + suf, remontado=True,
                                      de=m["de"], base=base_mt,
                                      mt=poe(list(b_ent) + list(cima), 0x1000)))
        if base_mt == CARIMBO:
            kit["cercas"].append(dict(CERCA, sobre=base_mt))
        else:
            nova = {}
            for papel, mt_id in CERCA.items():
                nova[papel] = poe(list(b_ent) + list(_entradas_qq(mt_id)[4:]),
                                  0x1000)
            kit["cercas"].append(dict(nova, sobre=base_mt))
    kit["cerca"] = kit["cercas"][0]

    if proximo[0] > TETO_META:
        raise SystemExit("o kit estoura o teto de %d metatiles" % TETO_META)

    # A vaga de metatile só serve se ainda NÃO EXISTIR no arquivo (o kit cresce
    # o `metatiles.bin`) ou se já tiver exatamente o que este kit escreve.
    disco = _ler("metatiles.bin")
    usados = set()
    for nome in IRMAOS:
        usados |= {c & 0x3FF for c in G.grade(nome)[4]}
    for local, ents in metas.items():
        gid = 512 + local
        if gid in usados and local >= len(disco) // 16:
            raise SystemExit("o mapa usa o metatile %d e ele nem existe" % gid)
        if local < len(disco) // 16:
            antigo = list(struct.unpack_from("<8H", disco, local * 16))
            if antigo != ents and not (len(set(antigo)) == 1 and antigo[0] <= 2):
                raise SystemExit("a vaga de metatile %d já está ocupada" % gid)
    return metas, attrs, kit


def grava_tileset(metas, attrs):
    """CRESCE `metatiles.bin` e `metatile_attributes.bin` do secundário.

    Idempotente: os locais são FIXOS e nenhum metatile de 0 a 143 é tocado. O
    `tiles.png` e os `.pal` não são abertos sequer para leitura.
    """
    alvo = max(metas) + 1
    meta = bytearray(_ler("metatiles.bin"))
    attr = bytearray(_ler("metatile_attributes.bin"))
    meta += bytes(max(0, alvo * 16 - len(meta)))
    attr += bytes(max(0, alvo * 2 - len(attr)))
    for local, ents in metas.items():
        for i, v in enumerate(ents):
            struct.pack_into("<H", meta, local * 16 + i * 2, v)
        struct.pack_into("<H", attr, local * 2, attrs[local])
    open(f"{DESTINO}/metatiles.bin", "wb").write(bytes(meta))
    open(f"{DESTINO}/metatile_attributes.bin", "wb").write(bytes(attr))


# ------------------------------------------------------ os CORREDORES da suite
def corredores_multinivel(alvo, v, W, H, d):
    """Os corredores da suite, refeitos com a regra da ELEVAÇÃO 15.

    O `enfeita_cidades.corredores_de_teste` simula a caminhada da suite com a
    regra "elevação 0 é curinga e o resto exige igualdade". Essa regra é uma
    APROXIMAÇÃO do `MapGridGetElevationAt`: a elevação 15
    (`ELEVATION_MULTI_LEVEL`) também casa com qualquer vizinho, e foi a
    diferença entre verde e vermelho na frente da orla de Sunyshore. Em
    `LittlerootTown` a elevação 15 EXISTE (medido: duas células andáveis), então
    aqui as duas simulações NÃO coincidem e usar a errada esconderia corredor.
    """
    pasta = f"{RAIZ}/dev_scripts/testes_criticos"
    nome_mapa = "MAP_" + re.sub(r"(?<!^)(?=[A-Z])", "_",
                                d.get("name", alvo)).upper().replace("__", "_")
    obj = {(o["x"], o["y"]) for o in (d.get("object_events") or [])}
    warps = d.get("warp_events") or []
    pisadas = set()
    passo = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}

    def compativel(ea, eb):
        return ea in (0, MULTI_NIVEL) or eb in (0, MULTI_NIVEL) or ea == eb

    def caminha(x, y, pernas, olhando):
        pisadas.add((x, y))
        for direcao, n in pernas:
            dx, dy = direcao
            passos = n - 1 if olhando != direcao else n
            olhando = direcao
            for _ in range(max(0, passos)):
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H):
                    break
                j = ny * W + nx
                if (v[j] >> 10) & 3 or (nx, ny) in obj:
                    break
                if not compativel((v[y * W + x] >> 12) & 0xF, (v[j] >> 12) & 0xF):
                    break
                x, y = nx, ny
                pisadas.add((x, y))

    for arq in sorted(glob.glob(f"{pasta}/*.json")):
        if os.path.basename(arq) == E.BLOCO_PROPRIO:
            continue
        for caso in json.load(open(arq)):
            if caso.get("warp") != nome_mapa:
                continue
            wid = int(caso.get("warp_id", 0) or 0)
            if wid >= len(warps):
                continue
            pernas = []
            for tok in (caso.get("roteiro") or "").split(","):
                m = E._LEG.match(tok.strip())
                if m:
                    pernas.append((passo[m.group(1)], int(m.group(2) or 1)))
            for x0, y0 in ((warps[wid]["x"], warps[wid]["y"]),
                           (warps[wid]["x"], warps[wid]["y"] + 1)):
                if not (0 <= x0 < W and 0 <= y0 < H):
                    continue
                for olhando in ((0, -1), (0, 1), (-1, 0), (1, 0)):
                    caminha(x0, y0, pernas, olhando)
    return pisadas


# ------------------------------------------------------------- o AUTOTILE
def abre(regiao):
    """ABERTURA morfológica 3x3: só fica a célula que cabe dentro de um quadrado
    3x3 inteiramente na região.

    É ela que garante que o autotile de NOVE peças dá conta: toda célula que
    sobra tem vizinho ao norte OU ao sul e vizinho a leste OU a oeste, então
    nunca cai o caso "sem norte e sem sul", que precisaria de uma décima peça
    que o `gTileset_General` não desenhou. Sem esta poda, uma trilha de uma
    célula de largura sairia com franja dos dois lados e miolo nenhum.
    """
    quadrados = [(x, y) for (x, y) in regiao
                 if all((x + dx, y + dy) in regiao
                        for dx in (-1, 0, 1) for dy in (-1, 0, 1))]
    fora = set()
    for x, y in quadrados:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                fora.add((x + dx, y + dy))
    return fora & set(regiao)


def peca_autotile(auto, regiao, x, y):
    """A peça do autotile para (x,y), pela vizinhança DENTRO da região.

    Canto reentrante (as quatro ortogonais na região e uma diagonal fora) cai no
    MIOLO, e isso é escolha consciente: o autotile do `gTileset_General` tem
    nove peças e não tem canto interno, exatamente como o Emerald original, que
    resolve o mesmo caso do mesmo jeito nas rotas.
    """
    n = (x, y - 1) in regiao
    s = (x, y + 1) in regiao
    o = (x - 1, y) in regiao
    l = (x + 1, y) in regiao
    if not n and not s:
        raise SystemExit("célula (%d,%d) sem norte e sem sul: a abertura falhou"
                         % (x, y))
    if not o and not l:
        raise SystemExit("célula (%d,%d) sem leste e sem oeste: a abertura falhou"
                         % (x, y))
    lin = 0 if not n else (2 if not s else 1)
    col = 0 if not o else (2 if not l else 1)
    return auto[lin * 3 + col], (lin, col)


# ------------------------------------------------------------ o ESPALHAMENTO
def esqueleto(v, W, H, d, elegivel):
    """Caminho de custo mínimo ligando as portas do mapa, em ordem de leitura.

    O custo não é só distância. Andar colado num sólido custa mais, para a
    trilha sair pelo MEIO do vão e não raspando o prédio; virar custa mais, para
    ela sair reta como caminho batido de verdade; e célula que não pode receber
    mancha custa muito mais, mas não é proibida, senão o caminho não atravessa a
    soleira das portas.
    """
    def andavel(i):
        return not ((v[i] >> 10) & 3)

    def perto_de_solido(x, y):
        return sum(1 for dx, dy in N4
                   if not (0 <= x + dx < W and 0 <= y + dy < H)
                   or ((v[(y + dy) * W + x + dx] >> 10) & 3))

    def custo(x, y):
        c = 1.0 + 2.0 * perto_de_solido(x, y)
        if (x, y) not in elegivel:
            c += 12.0
        return c

    def caminho(ini, fim):
        alvo = set(fim)
        dist, pai = {}, {}
        fila = [(0.0, ini[0], ini[1], 0, 0)]
        while fila:
            g, x, y, dx0, dy0 = heapq.heappop(fila)
            if (x, y, dx0, dy0) in dist:
                continue
            dist[(x, y, dx0, dy0)] = g
            if (x, y) in alvo and (dx0, dy0) != (0, 0):
                saida, no = [], (x, y, dx0, dy0)
                while no in pai:
                    saida.append((no[0], no[1]))
                    no = pai[no]
                saida.append((no[0], no[1]))
                return saida
            for dx, dy in N4:
                nx, ny = x + dx, y + dy
                if not (0 <= nx < W and 0 <= ny < H) or not andavel(ny * W + nx):
                    continue
                curva = 9.0 if (dx0, dy0) != (0, 0) and (dx, dy) != (dx0, dy0) else 0.0
                no = (nx, ny, dx, dy)
                if no in dist:
                    continue
                pai[no] = (x, y, dx0, dy0)
                heapq.heappush(fila, (g + custo(nx, ny) + curva, nx, ny, dx, dy))
        return []

    portas = []
    for w in (d.get("warp_events") or []):
        x, y = w["x"], w["y"]
        for dx, dy in ((0, 1), (0, 0), (0, -1), (1, 0), (-1, 0)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < W and 0 <= ny < H and andavel(ny * W + nx):
                portas.append((nx, ny))
                break
    chao = sorted(elegivel)
    if chao:
        ymin, ymax = min(y for _, y in chao), max(y for _, y in chao)
        for alvo_y in (ymin, ymax):
            faixa = [p for p in chao if abs(p[1] - alvo_y) <= 1]
            if faixa:
                xs = sorted({p[0] for p in faixa})
                xe = min(xs, key=lambda x: abs(x - W // 2))
                portas.append(min((p for p in faixa if p[0] == xe),
                                  key=lambda p: abs(p[1] - alvo_y)))
    if not portas:
        return set(), []
    # LIGAÇÃO EM ÁRVORE, não em fila: cada porta nova se liga ao ponto já ligado
    # mais perto, o que dá uma rede com cruzamento em vez de zigue-zague.
    ossos = {portas[0]}
    for p in portas[1:]:
        trecho = caminho(p, ossos)
        if trecho:
            ossos |= set(trecho)
    return ossos, portas


def area_trilha(v, W, H, d, elegivel, largura=1):
    """As células de TRILHA: o esqueleto engordado e depois ABERTO em 3x3."""
    ossos, portas = esqueleto(v, W, H, d, elegivel)
    pav = set()
    for x, y in ossos:
        for dx in range(-largura, largura + 1):
            for dy in range(-largura, largura + 1):
                p = (x + dx, y + dy)
                if p in elegivel:
                    pav.add(p)
    while True:
        entra = {p for p in elegivel if p not in pav
                 and sum(1 for dx, dy in N4 if (p[0] + dx, p[1] + dy) in pav) >= 3}
        if not entra:
            break
        pav |= entra
    return abre(pav), portas


def retangulos(livres, spec, perto=None):
    """[(x0,y0,w,h)] de retângulos disjuntos e afastados dentro de `livres`.

    Retângulo, e não bolha, e a razão é a arte: pintado com o autotile de nove
    peças, um retângulo sai na tela com CANTO ARREDONDADO e franja de grama em
    volta, que é como o Emerald desenha remendo de chão. Bolha de contorno livre
    produz canto reentrante, e canto reentrante não tem peça: sairia costura.
    A ordem de varredura é por hash da posição, não por linha, senão todos os
    remendos encostam no canto superior esquerdo do mapa.
    """
    ordem = sorted(livres, key=lambda p: _mistura(p[0], p[1], spec.get("semente", 0)))
    postos, saida = [], []
    lw, hw = spec["larg"]
    lh, hh = spec["alt"]
    for x0, y0 in ordem:
        if len(saida) >= spec["quantos"]:
            break
        w = lw + _mistura(x0, y0, 0xB10B) % (hw - lw + 1)
        h = lh + _mistura(x0, y0, 0xC0DE) % (hh - lh + 1)
        cels = [(x0 + i, y0 + j) for i in range(w) for j in range(h)]
        if any(c not in livres for c in cels):
            continue
        if any(max(abs(cx - px), abs(cy - py)) < spec["espaco"]
               for cx, cy in cels for px, py in postos):
            continue
        # `perto` é o que faz a praia ser praia: o remendo de areia só vale se
        # ENCOSTAR na água (Chebyshev 2 de alguma célula do conjunto). Sem isso
        # o gerador espalha areia pelo meio do bosque, que lê como buraco.
        if perto is not None and not any(
                max(abs(cx - px), abs(cy - py)) <= spec.get("raio", 2)
                for cx, cy in cels for px, py in perto):
            continue
        postos += cels
        saida.append((x0, y0, w, h))
    return saida


# ----------------------------------------------------------- ligação a pé
def componentes(v, W, H):
    """{célula: rótulo} dos pedaços de chão andável ligados a pé.

    POR QUE NÃO BASTA O `enfeita_cidades.alcance`: aquele mede "quem ainda é
    alcançável a partir de algum ponto de partida", e ponto de partida ali é
    warp OU objeto. Fechar um corredor com warp dos dois lados não tira NENHUMA
    célula do alcance e mesmo assim parte a cidade em duas, que foi como
    `SnowpointCity` passou verde numa sabotagem.
    """
    rot, prox = {}, 0
    for y in range(H):
        for x in range(W):
            if (v[y * W + x] >> 10) & 3 or (x, y) in rot:
                continue
            fila, prox = [(x, y)], prox + 1
            rot[(x, y)] = prox
            while fila:
                cx, cy = fila.pop()
                ea = (v[cy * W + cx] >> 12) & 0xF
                for dx, dy in N4:
                    nx, ny = cx + dx, cy + dy
                    if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in rot:
                        continue
                    j = ny * W + nx
                    if (v[j] >> 10) & 3:
                        continue
                    eb = (v[j] >> 12) & 0xF
                    if ea and eb and ea != eb:
                        continue
                    rot[(nx, ny)] = prox
                    fila.append((nx, ny))
    return rot


def ligacao_intacta(antes, depois, solidificadas):
    """Nenhum pedaço de chão se PARTIU, e nenhum se juntou a outro."""
    mau = []
    por_rotulo = collections.defaultdict(set)
    for p, rr in antes.items():
        if p not in solidificadas:
            por_rotulo[rr].add(p)
    for rr, cels in por_rotulo.items():
        if len({depois.get(p) for p in cels}) > 1:
            mau.append("o pedaço %d de chão se partiu em %d"
                       % (rr, len({depois.get(p) for p in cels})))
    juntou = collections.defaultdict(set)
    for p, rr in depois.items():
        if p in antes:
            juntou[rr].add(antes[p])
    for rr, origens in juntou.items():
        if len(origens) > 1:
            mau.append("dois pedaços de chão que eram separados se juntaram")
    return mau


# ---------------------------------------------------------------- o PLANO
def plano_mapa(alvo, cid, kit, base=None):
    """(L, W, H, v, escritas, contas, regioes) para a cidade `alvo`."""
    d, L, W, H, v0 = G.grade(alvo)
    v = list(base) if base is not None else list(v0)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    base_ent, attr_chao = chao_nosso()
    ap = G._attrs(PRIMARIO)

    def andavel(i):
        return not ((v[i] >> 10) & 3)

    # ELEGÍVEL = célula andável cujo metatile é o CARIMBO. Ela não filtra
    # elevação: quem protege o corredor não é a elevação da mancha (a mancha não
    # muda colisão nem elevação), e sim os portões de alcance e de componentes,
    # que rodam com a regra de elevação dos dois lados.
    # BASES: os carimbos que esta cidade deixa receber MÓVEL. Littleroot e
    # Petalburg têm um só (a grama); Oldale tem dois, porque o miolo do recorte
    # de grama gasta é o segundo carimbo dela e é lá que fica a praça.
    bases = cid.get("bases", [CARIMBO])
    elegivel = {(i % W, i // W) for i in range(W * H)
                if andavel(i) and (v[i] & 0x3FF) in bases
                and beh(v[i] & 0x3FF) not in AG}

    escritas = {}
    aplicado = list(v)
    # DOIS congelamentos, e a diferença entre eles é medida, não estética.
    # `gelo` (evento com folga de uma célula, corredor da suíte com as duas
    # regras de elevação) proíbe SOLIDIFICAR: enfeite sólido no meio de uma perna
    # saturante de teste encurta a perna e derruba caso que nada tem a ver.
    # `gelo_chao` é bem menor de propósito: trocar o DESENHO do chão não muda
    # colisão, elevação nem comportamento, então não encurta perna de teste nem
    # tapa evento, e proibir mancha em volta de cada placa deixaria a vila
    # remendada de buracos. Só as células que o `enfeita_cidades.py` já escreveu
    # entram aqui, porque aquele desenho tem plano próprio e reescrevê-lo por
    # cima quebraria o `--desfazer` dele.
    ev, gelo = E.congelado(d)
    gelo |= E.corredores_de_teste(alvo, v, W, H, d)
    gelo |= corredores_multinivel(alvo, v, W, H, d)
    gelo_chao = set()
    for idx, _a, _n in E.carrega_plano().get(alvo, {}).get("celulas", []):
        gelo_chao.add((idx % W, idx // W))
    gelo |= gelo_chao

    ini = E.partidas(d, W, H, v)
    antes_alc = E.alcance(v, W, H, ini)
    novos_solidos, postos = [], []
    conta_mov = collections.Counter()
    por_movel = collections.defaultdict(list)

    agua = {(i % W, i // W) for i in range(W * H) if beh(v[i] & 0x3FF) in AG}
    if cid.get("trilha"):
        trilha, portas = area_trilha(v, W, H, d, elegivel,
                                     cid.get("largura_trilha", 1))
    else:
        # Cidade que JÁ tem rua desenhada (Petalburg tem a rede de areia do
        # Emerald original ligando as portas) não ganha uma segunda rede de
        # caminho por cima: seria duas ruas paralelas dizendo a mesma coisa.
        trilha, portas = set(), []

    def nao_liga(grade, x, y):
        """Os vizinhos andáveis de (x,y) ainda se falam sem passar por (x,y)?"""
        viz = [(x + dx, y + dy) for dx, dy in N4
               if 0 <= x + dx < W and 0 <= y + dy < H
               and not ((grade[(y + dy) * W + x + dx] >> 10) & 3)]
        if len(viz) < 2:
            return False
        vistos, fila, falta = {viz[0]}, [viz[0]], set(viz[1:])
        while fila and falta:
            cx, cy = fila.pop()
            ea = (grade[cy * W + cx] >> 12) & 0xF
            for dx, dy in N4:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in vistos:
                    continue
                j = ny * W + nx
                if (grade[j] >> 10) & 3:
                    continue
                eb = (grade[j] >> 12) & 0xF
                if ea and eb and ea != eb:
                    continue
                vistos.add((nx, ny))
                falta.discard((nx, ny))
                fila.append((nx, ny))
        return bool(falta)

    def livre(x, y, base_mt=CARIMBO):
        """A célula pode receber a peça de base `base_mt`? E nunca a trilha.

        A célula tem que ser EXATAMENTE do carimbo que é a camada de baixo da
        peça: pousar um móvel de chão de grama numa célula de grama gasta
        deixaria um quadrado verde em volta da peça.
        """
        i = y * W + x
        if x < MARGEM or y < MARGEM or x >= W - MARGEM or y >= H - MARGEM:
            return False
        if (x, y) in gelo or i in escritas or (x, y) not in elegivel:
            return False
        if (x, y) in trilha:
            return False
        return (aplicado[i] & 0x3FF) == base_mt

    def tenta_solidificar(x, y, mt_id):
        """Solidifica (x,y) e devolve True se os DOIS portões deixarem."""
        i = y * W + x
        antigo = aplicado[i]
        aplicado[i] = (antigo & 0xF000) | (1 << 10) | mt_id   # elevação INTACTA
        perdidas = (antes_alc - E.alcance(aplicado, W, H, ini)) \
            - set(novos_solidos) - {(x, y)}
        if perdidas or nao_liga(aplicado, x, y):
            aplicado[i] = antigo
            return False
        escritas[i] = aplicado[i]
        novos_solidos.append((x, y))
        postos.append((x, y))
        return True

    ordem_cel = sorted(((x, y) for y in range(H) for x in range(W)),
                       key=lambda p: ((p[0] * 2654435761 + p[1] * 40503) & 0xFFFF, p))

    # A ORDEM entre mobília e região é OPÇÃO DA CIDADE, e a razão é de espaço
    # medido. Em Littleroot o gramado é largo e a mobília vem primeiro, que é o
    # que Snowpoint mediu: móvel posto no carimbo tira uma célula do numerador E
    # do denominador da régua, e móvel posto em cima de mancha tira só do
    # denominador, o que PIORA a conta. Em Petalburg e em Oldale o chão de
    # carimbo é fita estreita entre rua, prédio e lago: contados nesta árvore em
    # 09/09/2026, Petalburg tem SETE cantos possíveis de retângulo 3x3 nas 140
    # células de grama, e a mobília posta antes come quase todos. Ali a região
    # vem primeiro, e a mobília se acomoda no que sobrar.
    conta_cerca = 0
    por_cerca = []
    regioes = []
    conta_chao = collections.Counter()

    def faz_moveis():
        # -------------------------------------------------------- 1a. as CERCAS
        # Vêm primeiro porque precisam de uma corrida inteira de células e a mobília
        # solta não pode ter comido o meio dela.
        nonlocal conta_cerca, por_cerca
        cercas = [c for c in kit["cercas"] if c["sobre"] in bases]
        for x, y in ordem_cel:
            if conta_cerca >= cid.get("cercas", 0):
                break
            i0 = y * W + x
            cerca = None
            for c in cercas:
                if (aplicado[i0] & 0x3FF) == c["sobre"]:
                    cerca = c
                    break
            if cerca is None:
                continue
            comp = cid["cerca_comp"][0] + _mistura(x, y, 0xFEE1) % (
                cid["cerca_comp"][1] - cid["cerca_comp"][0] + 1)
            cels = [(x + k, y) for k in range(comp)]
            if any(not livre(cx, cy, cerca["sobre"]) for cx, cy in cels):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < cid.get("cerca_espaco", 6)
                   for cx, cy in cels for px, py in por_cerca):
                continue
            if any(max(abs(cx - px), abs(cy - py)) < ESPACO_ENTRE_MOVEIS
                   for cx, cy in cels for px, py in postos):
                continue
            # cerca é de BEIRA: uma das pontas encosta num sólido ou na trilha
            if not _encosta(cels, aplicado, W, H, trilha):
                continue
            ok = True
            for k, (cx, cy) in enumerate(cels):
                mt = cerca["esq"] if k == 0 else (cerca["dir"] if k == comp - 1
                                                  else cerca["meio"])
                if not tenta_solidificar(cx, cy, mt):
                    ok = False
                    break
            if not ok:
                for cx, cy in cels:
                    if (cx, cy) in novos_solidos:
                        novos_solidos.remove((cx, cy))
                        postos.remove((cx, cy))
                        del escritas[cy * W + cx]
                        aplicado[cy * W + cx] = v[cy * W + cx]
                continue
            por_cerca += cels
            conta_cerca += 1

        # ---------------------------------------------------- 1b. a MOBÍLIA solta
        lista = [m for m in kit["moveis"] if m["nome"] in cid["moveis"]]
        quantos = cid["moveis"]
        for x, y in ordem_cel:
            giro = ((x * 73856093) ^ (y * 19349663)) % max(1, len(lista))
            for k in range(len(lista)):
                m = lista[(giro + k) % len(lista)]
                q, espaco = quantos[m["nome"]]
                if conta_mov[m["nome"]] >= q:
                    continue
                if not livre(x, y, m.get("base", CARIMBO)):
                    continue
                if any(max(abs(x - px), abs(y - py)) < ESPACO_ENTRE_MOVEIS
                       for px, py in postos):
                    continue
                if any(max(abs(x - px), abs(y - py)) < espaco
                       for px, py in por_movel[m["nome"]]):
                    continue
                # Móvel de vila encosta em alguma coisa: num sólido ou na
                # trilha. Peça solta no meio do vazio lê como erro de mapa.
                # A BORDA DO RECORTE conta como "alguma coisa" para as peças de
                # base que NÃO é o carimbo, e a exceção é medida: a praça de
                # `OldaleTown` é um tapete de 69 células de miolo de grama gasta
                # sem UM sólido dentro, e pela regra do sólido cabia exatamente
                # UMA peça lá. A borda do próprio recorte é fronteira de verdade
                # (é onde a arte de transição está desenhada), e mobília na
                # beirada de praça é o que qualquer vilarejo tem. A opção é por
                # cidade e vale só para base diferente do carimbo, senão ela
                # afrouxaria a regra em Littleroot e em Petalburg, onde quase
                # toda célula de grama faz fronteira com alguma coisa.
                base_m = m.get("base", CARIMBO)
                if not _encosta([(x, y)], aplicado, W, H, trilha):
                    if not (base_m != CARIMBO and cid.get("beira_da_mancha")
                            and any(0 <= x + dx < W and 0 <= y + dy < H
                                    and (aplicado[(y + dy) * W + x + dx] & 0x3FF)
                                    != base_m for dx, dy in N4)):
                        continue
                if not tenta_solidificar(x, y, m["mt"]):
                    continue
                por_movel[m["nome"]].append((x, y))
                conta_mov[m["nome"]] += 1
                break

    def faz_regioes():
        # ------------------------------------------------------- 2. as REGIÕES
        # Uma REGIÃO é um pedaço de chão pintado com o autotile de uma família. A
        # trilha é a primeira; os remendos vêm depois, nas sobras.
        def pintavel(p):
            i = p[1] * W + p[0]
            return (p in elegivel and i not in escritas
                    and (aplicado[i] & 0x3FF) == CARIMBO)

        def pinta_regiao(nome_fam, celulas):
            fam = kit["familias"][nome_fam]
            celulas = abre({p for p in celulas if pintavel(p)})
            if not celulas:
                return None
            var = [c["mt"] for c in fam["variantes"]]
            for p in sorted(celulas):
                mt_id, (lin, col) = peca_autotile(fam["auto"], celulas, p[0], p[1])
                if (lin, col) == (1, 1):
                    # o MIOLO recebe os arranjos da família, e não o fill puro: sem
                    # isso o miolo vira o carimbo novo e a régua não anda.
                    escolha = [fam["fill"]] + var
                    mt_id = escolha[_mistura(p[0], p[1], 0xA5A5 + len(escolha))
                                    % len(escolha)]
                i = p[1] * W + p[0]
                escritas[i] = (aplicado[i] & 0xFC00) | mt_id
                aplicado[i] = escritas[i]
                conta_chao[nome_fam] += 1
            return dict(familia=nome_fam, celulas=sorted(celulas))

        if cid.get("trilha"):
            r = pinta_regiao(cid["trilha"], trilha)
            if r:
                r["papel"] = "trilha"
                regioes.append(r)

        for spec in cid["remendos"]:
            livres = {p for p in elegivel if pintavel(p) and p not in gelo_chao}
            perto = agua if spec.get("perto") == "agua" else None
            for (x0, y0, w, h) in retangulos(livres, spec, perto):
                r = pinta_regiao(spec["familia"],
                                 {(x0 + i, y0 + j) for i in range(w) for j in range(h)})
                if r:
                    r["papel"] = "remendo"
                    regioes.append(r)

    if cid.get("regioes_antes"):
        faz_regioes()
        faz_moveis()
    else:
        faz_moveis()
        faz_regioes()

    # ------------------------------------------------ 3. o RUÍDO de arranjo
    # O que sobrou do carimbo (e, nas cidades que têm, do segundo carimbo) troca
    # de arranjo por hash da posição. É a camada SUTIL: ela quebra o repeat de
    # dezesseis pixels e não muda o desenho da cidade.
    conta_ruido = collections.Counter()
    for mt_origem, nome_fam in cid["ruido"]:
        fam = kit["familias"][nome_fam]
        escolha = [mt_origem] + [c["mt"] for c in fam["variantes"]]
        for i in range(W * H):
            if not andavel(i) or i in escritas:
                continue
            if (aplicado[i] & 0x3FF) != mt_origem:
                continue
            x, y = i % W, i // W
            mt_id = escolha[_mistura(x, y, 0x5EED + mt_origem) % len(escolha)]
            if mt_id == mt_origem:
                continue
            escritas[i] = (aplicado[i] & 0xFC00) | mt_id
            aplicado[i] = escritas[i]
            conta_ruido[nome_fam] += 1

    # -------------------------------------------------------------- PORTÕES
    depois = E.alcance(aplicado, W, H, ini)
    perdidas = antes_alc - depois - set(novos_solidos)
    if perdidas:
        raise SystemExit("%s: %d células ficariam inalcançáveis, ex.: %s"
                         % (alvo, len(perdidas), sorted(perdidas)[:6]))
    for x, y in E.eventos(d):
        if (x, y) in antes_alc and (x, y) not in depois:
            raise SystemExit("%s: evento em (%d,%d) ficaria inalcançável"
                             % (alvo, x, y))
    queixas = ligacao_intacta(componentes(v, W, H), componentes(aplicado, W, H),
                              set(novos_solidos))
    if queixas:
        raise SystemExit("%s: %s" % (alvo, "; ".join(queixas)))

    contas = dict(trilha=len(trilha), moveis=dict(conta_mov), cercas=conta_cerca,
                  chao=dict(conta_chao), ruido=dict(conta_ruido),
                  solidos=len(novos_solidos), portas=len(portas),
                  elegiveis=len(elegivel), regioes=len(regioes))
    return L, W, H, v, escritas, contas, regioes


def _encosta(cels, grade, W, H, trilha):
    for x, y in cels:
        for dx, dy in N4:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                return True
            if ((grade[ny * W + nx] >> 10) & 3) or (nx, ny) in trilha:
                return True
    return False


def regua(v, W, H, L, escritas=None):
    """(carimbo dominante em %, células andáveis a pé, id do carimbo), como a
    `regua_cidades.py` conta."""
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    AG = E.agua()
    cel = list(v)
    for i, val in (escritas or {}).items():
        cel[i] = val
    and_ = [c & 0x3FF for c in cel
            if not ((c >> 10) & 3) and beh(c & 0x3FF) not in AG]
    top = collections.Counter(and_).most_common(1)[0]
    return 100.0 * top[1] / len(and_), len(and_), top[0]


# --------------------------------------------------------------------- rodagem
def carrega_plano():
    return json.load(open(PLANO)) if os.path.exists(PLANO) else {}


def base_de(alvo, guardado):
    """A grade como está no disco, só tirando o que ESTA passada escreveu."""
    v = list(G.grade(alvo)[4])
    for idx, antigo, novo in guardado.get(alvo, {}).get("celulas", []):
        if v[idx] == novo:
            v[idx] = antigo
    return v


def roda(alvo, cid, aplicar):
    metas, attrs, kit = desenha_kit()
    print("kit: %d metatiles novos (locais %d a %d, ids %d a %d de %d); "
          "0 tile e 0 cor"
          % (len(metas), min(metas), max(metas), 512 + min(metas),
             512 + max(metas), TETO_META))
    for nome_fam, fam in kit["familias"].items():
        print("  %-6s %d arranjos vivos, %d cortados pela régua de cor%s"
              % (nome_fam, len(fam["variantes"]), len(fam["cortados"]),
                 (" (pior " + ", ".join("%s %.1f" % c for c in fam["cortados"][:3])
                  + ")") if fam["cortados"] else ""))
    if aplicar:
        grava_tileset(metas, attrs)
    guardado = carrega_plano()
    L, W, H, v, escritas, contas, _reg = plano_mapa(alvo, cid, kit,
                                                    base_de(alvo, guardado))
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("%s: %d elegíveis, trilha %d, %d regiões, %d solidificadas, "
          "%d células mudadas" % (alvo, contas["elegiveis"], contas["trilha"],
                                  contas["regioes"], contas["solidos"],
                                  len(escritas)))
    print("  chão:  " + ", ".join("%s x%d" % kv for kv in sorted(contas["chao"].items())))
    print("  ruído: " + ", ".join("%s x%d" % kv for kv in sorted(contas["ruido"].items())))
    print("  móvel: " + ", ".join("%s x%d" % kv for kv in sorted(contas["moveis"].items()))
          + ", cerca x%d" % contas["cercas"])
    print("  régua: carimbo %d com %.1f%% de %d células ANTES; carimbo %d com "
          "%.1f%% de %d DEPOIS" % (ida, a, na, idb, b, nb))
    if aplicar:
        saida = list(v)
        for i, val in escritas.items():
            saida[i] = val
        with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
            f.write(struct.pack("<%dH" % len(saida), *saida))
        guardado[alvo] = {"celulas": [[i, v[i], escritas[i]]
                                      for i in sorted(escritas)]}
        with open(PLANO, "w") as f:
            json.dump(guardado, f, indent=1)
        print("aplicado")
    return 0


def desfaz(alvo):
    guardado = carrega_plano()
    if alvo not in guardado:
        print("%s: nada a desfazer" % alvo)
        return 0
    d, L, W, H, v = G.grade(alvo)
    v, n = list(v), 0
    for idx, antigo, novo in guardado[alvo]["celulas"]:
        if v[idx] == novo:
            v[idx] = antigo
            n += 1
    with open(f"{RAIZ}/{L['blockdata_filepath']}", "wb") as f:
        f.write(struct.pack("<%dH" % len(v), *v))
    guardado.pop(alvo)
    with open(PLANO, "w") as f:
        json.dump(guardado, f, indent=1)
    print("%s: desfeitas %d células" % (alvo, n))
    return 0


# ------------------------------------------------------------------ conferência
def confere(alvo, cid, metas, attrs, kit, plano):
    """Todas as regras desta onda, medidas sobre os dados que vierem.

    Ela é chamada uma vez com o plano de verdade, que tem que sair sem queixa, e
    uma vez por sabotagem, que tem que sair com a queixa certa. Regra conferida
    só no caminho feliz não é regra.
    """
    import render_maps as RM
    mau = []
    ap = G._attrs(PRIMARIO)
    asec = G._attrs(SECUNDARIO)
    tp, ts = _tileset(PRIMARIO), _tileset(SECUNDARIO)
    base_ent, attr_chao = chao_nosso()

    def atributo(mt_id):
        if mt_id >= 512:
            local = mt_id - 512
            if local in attrs:
                return attrs[local]
            return asec[local] if local < len(asec) else 0
        return ap[mt_id] if mt_id < len(ap) else 0

    def entradas(mt_id):
        if mt_id >= 512 and (mt_id - 512) in metas:
            return list(metas[mt_id - 512])
        tset, loc = (tp, mt_id) if mt_id < 512 else (ts, mt_id - 512)
        if (loc + 1) * 16 > len(tset["metatiles"]):
            return [0] * 8
        return list(struct.unpack_from("<8H", tset["metatiles"], loc * 16))

    def px_de(mt_id):
        from PIL import Image
        im = Image.new("RGB", (16, 16), (0, 0, 0))
        p = im.load()
        ent = entradas(mt_id)
        for cam in (0, 1):
            for q in range(4):
                val = ent[cam * 4 + q]
                idx, ip = val & 0x3FF, (val >> 12) & 0xF
                if not idx:
                    continue
                tile = RM.resolver_tile(tp, ts, idx)
                if tile is None:
                    continue
                cores = (tp if ip < 6 else ts)["paletas"].get(ip)
                if cores is None:
                    continue
                RM.desenhar_tile(p, (q % 2) * 8, (q // 2) * 8, tile,
                                 [tuple(c) for c in cores],
                                 bool(val & 0x400), bool(val & 0x800))
        return list(im.get_flattened_data())

    # ------------------------------------------------------------ 1. orçamento
    if metas and (min(metas) < META_LOCAL_0 or max(metas) >= TETO_META):
        mau.append("o kit escreve fora da faixa livre de metatile")
    for local in metas:
        if 512 + local < 512:
            mau.append("metatile fora do secundário")

    ids_chao, ids_var = {}, {}
    for nome_fam, fam in kit["familias"].items():
        for c in fam["variantes"]:
            ids_chao[c["mt"]] = nome_fam
            ids_var[c["mt"]] = nome_fam
        if fam["auto"]:
            for mt_id in fam["auto"]:
                ids_chao[mt_id] = nome_fam
        ids_chao[fam["fill"]] = nome_fam
    ids_movel = {m["mt"] for m in kit["moveis"]}
    ids_cerca = {c[papel] for c in kit["cercas"]
                 for papel in ("esq", "meio", "dir")}
    base_do_movel = {m["mt"]: m.get("base", CARIMBO) for m in kit["moveis"]}
    for c in kit["cercas"]:
        for papel in ("esq", "meio", "dir"):
            base_do_movel[c[papel]] = c["sobre"]

    # ---- 2. CHÃO novo: atributo idêntico ao do carimbo e camada de cima VAZIA
    for mt_id in sorted(ids_chao):
        if atributo(mt_id) != attr_chao:
            mau.append("o chão %d tem atributo 0x%04X e o carimbo tem 0x%04X"
                       % (mt_id, atributo(mt_id), attr_chao))
        if any(e & 0x3FF for e in entradas(mt_id)[4:]):
            mau.append("o chão %d usa a camada de cima" % mt_id)

    # ---- 3. MÓVEL: COVERED, comportamento zerado, e o NOSSO chão embaixo
    for mt_id in sorted(ids_movel | ids_cerca):
        a = atributo(mt_id)
        if (a >> 12) & 0xF != 1:
            mau.append("o móvel %d não está em COVERED" % mt_id)
        if a & 0xFF:
            mau.append("o móvel %d tem comportamento 0x%02X" % (mt_id, a & 0xFF))
        if entradas(mt_id)[:4] != chao_nosso(base_do_movel[mt_id])[0]:
            mau.append("o móvel %d não tem o nosso chão na camada de baixo" % mt_id)
        if not any(e & 0x3FF for e in entradas(mt_id)[4:]):
            mau.append("o móvel %d não tem arte na camada de cima" % mt_id)

    # ---- 4. nenhuma variante de chão é cópia de outra nem do carimbo da família
    for nome_fam, fam in kit["familias"].items():
        lista = [fam["fill"]] + [c["mt"] for c in fam["variantes"]]
        pix = {mt: px_de(mt) for mt in lista}
        for i, a in enumerate(lista):
            for b in lista[i + 1:]:
                dd = sum(sum((x - y) ** 2 for x, y in zip(p, q)) ** 0.5
                         for p, q in zip(pix[a], pix[b])) / 256.0
                if dd < PISO_DISTANCIA:
                    mau.append("as variantes de chão %d e %d têm distância %.1f, "
                               "abaixo do piso de %.1f do varia_carimbo.py: isso "
                               "é enganar a régua" % (a, b, dd, PISO_DISTANCIA))

    # ------------------------------------------- 5 a 12. o plano, no mapa
    L, W, H, v, escritas, contas, regioes = plano
    d = json.load(open(f"{RAIZ}/data/maps/{alvo}/map.json"))
    ev = E.eventos(d)
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    origens = {mt for mt, _f in cid["ruido"]} | {CARIMBO}

    for i, val in escritas.items():
        x, y = i % W, i // W
        novo, velho = val & 0x3FF, v[i] & 0x3FF
        cn, cv = (val >> 10) & 3, (v[i] >> 10) & 3
        if (val >> 12) & 0xF != (v[i] >> 12) & 0xF:
            mau.append("%s: mudou ELEVAÇÃO em (%d,%d)" % (alvo, x, y))
        if cv and not cn:
            mau.append("%s: colisão 1 -> 0 em (%d,%d), que segue proibida"
                       % (alvo, x, y))
        if novo in ids_movel or novo in ids_cerca:
            if cv or not cn:
                mau.append("%s: móvel em (%d,%d) não é solidificação 0 -> 1"
                           % (alvo, x, y))
            if velho != base_do_movel[novo]:
                mau.append("%s: o móvel %d, cuja camada de baixo é a do carimbo "
                           "%d, foi posto em cima do carimbo %d em (%d,%d): "
                           "isso deixa costura em volta da peça"
                           % (alvo, novo, base_do_movel[novo], velho, x, y))
            if (x, y) in ev:
                mau.append("%s: móvel em cima do evento (%d,%d)" % (alvo, x, y))
        elif novo in ids_chao:
            if cn != cv:
                mau.append("%s: o chão em (%d,%d) mudou colisão" % (alvo, x, y))
            if velho not in origens:
                mau.append("%s: chão em célula errada em (%d,%d), o velho era %d"
                           % (alvo, x, y, velho))
        else:
            mau.append("%s: metatile %d escrito em (%d,%d) é de fora do kit"
                       % (alvo, novo, x, y))

    # 6. (comportamento, layerType) de toda célula ANDÁVEL fica igual
    for i in range(W * H):
        if (saida[i] >> 10) & 3:
            continue
        a, b = atributo(v[i] & 0x3FF), atributo(saida[i] & 0x3FF)
        if (a & 0xFF, a & 0xF000) != (b & 0xFF, b & 0xF000):
            mau.append("%s: célula andável (%d,%d) mudou (comportamento, "
                       "layerType)" % (alvo, i % W, i // W))
            break

    # 7 e 8. alcance a pé e LIGAÇÃO a pé
    ini = E.partidas(d, W, H, v)
    antes, depois = E.alcance(v, W, H, ini), E.alcance(saida, W, H, ini)
    solid = {(i % W, i // W) for i in escritas
             if not ((v[i] >> 10) & 3) and ((escritas[i] >> 10) & 3)}
    if (antes - depois) - solid:
        mau.append("%s: o alcance a pé perdeu %d células além das solidificadas: "
                   "%s" % (alvo, len((antes - depois) - solid),
                           sorted((antes - depois) - solid)[:6]))
    if depois - antes:
        mau.append("%s: o alcance a pé GANHOU célula" % alvo)
    mau += ["%s: %s" % (alvo, q) for q in
            ligacao_intacta(componentes(v, W, H), componentes(saida, W, H), solid)]

    # 9. O AUTOTILE tem que ser COERENTE: cada célula de região recebeu a peça
    #    que a vizinhança dela manda, e não uma peça qualquer.
    for r in regioes:
        fam = kit["familias"][r["familia"]]
        celulas = {tuple(p) for p in r["celulas"]}
        for p in celulas:
            i = p[1] * W + p[0]
            if i not in escritas:
                mau.append("%s: a célula (%d,%d) da região não foi escrita"
                           % (alvo, p[0], p[1]))
                break
            esperado, (lin, col) = peca_autotile(fam["auto"], celulas, p[0], p[1])
            got = escritas[i] & 0x3FF
            if (lin, col) == (1, 1):
                if got != fam["fill"] and ids_var.get(got) != r["familia"]:
                    mau.append("%s: o miolo (%d,%d) recebeu %d, que não é da "
                               "família %s" % (alvo, p[0], p[1], got, r["familia"]))
                    break
            elif got != esperado:
                mau.append("%s: a borda (%d,%d) recebeu %d e o autotile manda %d"
                           % (alvo, p[0], p[1], got, esperado))
                break

    # 10. A MANCHA VISÍVEL (as regiões) é BOLHA, não sal e pimenta, e a peça
    #     não pode ser adivinhável por projeção simples da posição. O RUÍDO de
    #     arranjo fica FORA desta conta de propósito: ele é, por desenho, uma
    #     textura por célula, e cobrá-lo de bolha seria cobrar dele o contrário
    #     do que ele é. O que o protege de virar padrão é o teste de projeção,
    #     que roda nele também, logo abaixo.
    reg_cels = {tuple(p) for r in regioes for p in r["celulas"]}
    if len(reg_cels) < cid["min_regiao"]:
        mau.append("%s: só %d células de região visível (mínimo %d)"
                   % (alvo, len(reg_cels), cid["min_regiao"]))
    if reg_cels:
        vistos, pedacos = set(), 0
        for p in sorted(reg_cels):
            if p in vistos:
                continue
            pedacos += 1
            pilha = [p]
            vistos.add(p)
            while pilha:
                q = pilha.pop()
                for dx, dy in N4:
                    rr = (q[0] + dx, q[1] + dy)
                    if rr in reg_cels and rr not in vistos:
                        vistos.add(rr)
                        pilha.append(rr)
        if len(reg_cels) / pedacos < 9.0:
            mau.append("%s: a região média tem só %.1f células (%d em %d "
                       "pedaços): virou sal e pimenta, não mancha"
                       % (alvo, len(reg_cels) / pedacos, len(reg_cels), pedacos))

    # O teste é de PERMUTAÇÃO, e não contra o "chute cego", e a razão é uma
    # medida: com cem células e dez peças, oito baldes de mod 8 têm doze células
    # cada, e ATÉ UM SORTEIO PERFEITO acerta 27% delas olhando só o balde. Comparar
    # com o chute cego (13%) reprovaria qualquer ruído honesto. O nulo certo é
    # embaralhar as MESMAS peças pelas MESMAS posições: se o desenho de verdade
    # não é mais adivinhável do que o pior de vinte e quatro embaralhamentos, ele
    # não tem período. Um ruído por (x+y) fica em ~100% e é acusado na hora.
    ruido = {(i % W, i // W): (val & 0x3FF) for i, val in escritas.items()
             if (val & 0x3FF) in ids_var and (i % W, i // W) not in reg_cels}
    if len(ruido) >= 20:
        tot = len(ruido)
        pos = sorted(ruido)
        pecas = [ruido[p] for p in pos]

        def acerto(mapa):
            pior = 0.0
            for _rot, eixo in (("x", lambda p: p[0]), ("y", lambda p: p[1]),
                               ("x+y", lambda p: p[0] + p[1]),
                               ("x-y", lambda p: p[0] - p[1])):
                for mod in range(2, 9):
                    tab = collections.defaultdict(collections.Counter)
                    for p, mt_id in mapa.items():
                        tab[eixo(p) % mod][mt_id] += 1
                    ac = sum(c.most_common(1)[0][1] for c in tab.values()) / tot
                    pior = max(pior, ac)
            return pior

        teto = 0.0
        for k in range(24):
            ordem = sorted(range(tot), key=lambda j: _mistura(j, k, 0x9E37))
            teto = max(teto, acerto({pos[j]: pecas[i]
                                     for i, j in enumerate(ordem)}))
        real = acerto(ruido)
        if real > teto + 1e-9:
            mau.append("%s: a peça do ruído é adivinhável em %.0f%% das células "
                       "por projeção da posição, contra o teto de %.0f%% de 24 "
                       "embaralhamentos das mesmas peças: virou padrão"
                       % (alvo, 100 * real, 100 * teto))

    # 11. a régua tem que fechar no teto
    b, nb, idb = regua(v, W, H, L, escritas)
    if b > cid.get("teto_regua", TETO_REGUA):
        mau.append("%s: a régua ainda marca %.1f%% de carimbo dominante"
                   % (alvo, b))

    # 12. NENHUM irmão AINDA NÃO REFINADO usa um id que este kit criou. É a prova
    #     de "zero pixel no irmão" que dá para dar aqui: o kit não reescreve tile,
    #     cor nem metatile que já existia, então mapa que não escreve id novo não
    #     muda um pixel por construção, e isto mede que nenhum escreve.
    #     As três cidades DESTA frente dividem o tileset e por isso saem da conta
    #     assim que entram no plano: exigir que `LittlerootTown` não use o kit
    #     depois de `mato_littleroot.py` tê-lo aplicado seria exigir que a passada
    #     anterior não tivesse acontecido. Sobram Route101, Route102 e Route103,
    #     que nunca serão refinadas por esta frente, e a conta continua valendo
    #     para elas.
    novos = {512 + local for local in metas}
    refinados = set(carrega_plano())
    for nome in IRMAOS:
        if nome == alvo or nome in refinados:
            continue
        usados = {c & 0x3FF for c in G.grade(nome)[4]}
        if usados & novos:
            mau.append("o irmão %s usa metatile novo: %s"
                       % (nome, sorted(usados & novos)[:4]))
    return mau


# ------------------------------------------------------------------ auto-teste
def demo(alvo, cid):
    """Prova positiva e NOVE provas negativas, cada sabotagem revertida em
    seguida. "Zero diferença" só vale depois que a comparação mostra que sabe
    reprovar."""
    metas, attrs, kit = desenha_kit()
    guardado = carrega_plano()
    plano = plano_mapa(alvo, cid, kit, base_de(alvo, guardado))
    mau = confere(alvo, cid, metas, attrs, kit, plano)
    negativas = []

    def copia():
        return (dict(metas), dict(attrs), json.loads(json.dumps(kit)),
                (plano[0], plano[1], plano[2], list(plano[3]), dict(plano[4]),
                 plano[5], json.loads(json.dumps(plano[6]))))

    def sabota(nome, funcao, espera):
        args = funcao()
        queixas = confere(alvo, cid, *args)
        pega = [q for q in queixas if espera in q]
        if not pega:
            mau.append("SABOTAGEM NÃO ACUSADA (%s): %s" % (nome, queixas[:2]))
        else:
            negativas.append((nome, pega[0]))

    # N1. colisão 1 -> 0 numa célula de chão
    def n1():
        a = copia()
        L, W, H, v, esc, ct, rg = a[3]
        i = sorted(esc)[0]
        v[i] = v[i] | (1 << 10)          # a célula ERA sólida
        return a
    sabota("colisão 1 -> 0", n1, "colisão 1 -> 0")

    # N2. elevação alterada
    def n2():
        a = copia()
        L, W, H, v, esc, ct, rg = a[3]
        i = sorted(esc)[0]
        esc[i] = (esc[i] & 0x0FFF) | (((v[i] >> 12) + 1) & 0xF) << 12
        return a
    sabota("elevação alterada", n2, "mudou ELEVAÇÃO")

    # N3. comportamento de um metatile de CHÃO sabotado
    def n3():
        a = copia()
        mt_id = kit["familias"]["grama"]["variantes"][0]["mt"]
        a[1][mt_id - 512] = (a[1][mt_id - 512] & 0xFF00) | 0x02   # MB_TALL_GRASS
        return a
    sabota("behavior de chão sabotado", n3, "tem atributo")

    # N4. layerType NORMAL onde devia ser COVERED
    def n4():
        a = copia()
        alvo_mt = [m["mt"] for m in kit["moveis"] if m["remontado"]][0]
        a[1][alvo_mt - 512] = a[1][alvo_mt - 512] & 0x0FFF
        return a
    sabota("layerType NORMAL no móvel", n4, "não está em COVERED")

    # N5. camada de BAIXO de um móvel sabotada (arte no lugar do nosso chão)
    def n5():
        a = copia()
        alvo_mt = [m["mt"] for m in kit["moveis"] if m["remontado"]][0]
        ent = list(a[0][alvo_mt - 512])
        ent[0] = ent[4]
        a[0][alvo_mt - 512] = ent
        return a
    sabota("camada de baixo sabotada", n5, "não tem o nosso chão na camada de baixo")

    # N6. BORDA de autotile trocada pelo miolo: é a costura que nenhum outro
    #     portão pega (colisão, elevação, atributo e alcance ficam certos).
    def n6():
        a = copia()
        L, W, H, v, esc, ct, rg = a[3]
        for r in rg:
            fam = kit["familias"][r["familia"]]
            cels = {tuple(p) for p in r["celulas"]}
            for p in sorted(cels):
                _mt, lc = peca_autotile(fam["auto"], cels, p[0], p[1])
                if lc != (1, 1):
                    esc[p[1] * W + p[0]] = (esc[p[1] * W + p[0]] & 0xFC00) | fam["fill"]
                    return a
        raise SystemExit("não achei borda de autotile para a sabotagem N6")
    sabota("borda de autotile virou miolo", n6, "o autotile manda")

    # N7. ruído escolhido por (x + y) % n, que é xadrez com período
    def n7():
        original = globals()["_mistura"]
        globals()["_mistura"] = lambda *n: (n[0] + n[1]) if len(n) > 1 else n[0]
        try:
            p2 = plano_mapa(alvo, cid, kit, base_de(alvo, guardado))
        finally:
            globals()["_mistura"] = original
        return (dict(metas), dict(attrs), json.loads(json.dumps(kit)), p2)
    sabota("ruído por (x+y)", n7, "virou padrão")

    # N8. corredor fechado que PARTE um pedaço de chão. O portão de alcance
    #     sozinho não pega isso quando há warp dos dois lados, e foi assim que
    #     Snowpoint passou verde com a cidade cortada.
    def n8():
        a = copia()
        L, W, H, v, esc, ct, rg = a[3]
        final = list(v)
        for j, val in esc.items():
            final[j] = val
        antes = componentes(final, W, H)
        for y in range(H):
            for x in range(W):
                i = y * W + x
                if (final[i] >> 10) & 3:
                    continue
                teste = list(final)
                teste[i] = (final[i] & 0xF000) | (1 << 10) | (final[i] & 0x3FF)
                if ligacao_intacta(antes, componentes(teste, W, H), {(x, y)}):
                    esc[i] = teste[i]
                    return a
        raise SystemExit("não achei ponto de articulação para a sabotagem N8")
    sabota("corredor fechado", n8, "se partiu")

    # N9. duas variantes de chão IGUAIS pixel a pixel: é enganar a régua
    def n9():
        a = copia()
        lst = kit["familias"]["grama"]["variantes"]
        a[0][lst[1]["mt"] - 512] = list(a[0][lst[0]["mt"] - 512])
        return a
    sabota("variante de chão duplicada", n9, "abaixo do piso de")

    # ------------------------------------------------ o que está NO DISCO
    # Sem este caso o auto-teste só confere o que ele mesmo acabou de calcular.
    meta_disco = _ler("metatiles.bin")
    attr_disco = _ler("metatile_attributes.bin")
    if len(meta_disco) // 16 <= META_LOCAL_0:
        print("aviso: o kit ainda não foi aplicado no tileset; o caso de DISCO "
              "não roda")
    else:
        for local, ents in metas.items():
            if (local + 1) * 16 > len(meta_disco):
                mau.append("o metatile %d não cabe no metatiles.bin" % (512 + local))
                continue
            if list(struct.unpack_from("<8H", meta_disco, local * 16)) != ents:
                mau.append("metatile %d no disco não é o do kit" % (512 + local))
            if struct.unpack_from("<H", attr_disco, local * 2)[0] != attrs[local]:
                mau.append("atributo do metatile %d no disco não é o do kit"
                           % (512 + local))

    # ------------------------------------------------------- idempotência
    L, W, H, v, escritas, contas, _rg = plano
    saida = list(v)
    for i, val in escritas.items():
        saida[i] = val
    volta = list(saida)
    for i in sorted(escritas):
        if volta[i] == escritas[i]:
            volta[i] = v[i]
    if volta != list(v):
        mau.append("%s: desfazer não devolve a base" % alvo)
    esc2 = plano_mapa(alvo, cid, kit, volta)[4]
    if esc2 != escritas:
        mau.append("%s: segunda passada deu plano diferente" % alvo)

    if mau:
        print("DEMO VERMELHA")
        for x in dict.fromkeys(mau):
            print("  -", x)
        return 1
    print("DEMO VERDE")
    a, na, ida = regua(v, W, H, L)
    b, nb, idb = regua(v, W, H, L, escritas)
    print("  %s: %d células mudadas, %d solidificadas, régua %.1f%% (mt %d) -> "
          "%.1f%% (mt %d)" % (alvo, len(escritas), contas["solidos"], a, ida,
                              b, idb))
    print("  %d metatiles, 0 tiles, 0 cores, %d provas negativas:"
          % (len(metas), len(negativas)))
    for nome, queixa in negativas:
        print("    %-32s -> %s" % (nome, queixa[:100]))
    return 0


# ------------------------------------------------------------------- LITTLEROOT
ALVO = "LittlerootTown"
CIDADE = dict(
    trilha="gasta",
    largura_trilha=1,
    # os remendos: retângulos pintados com o autotile da família
    remendos=[
        dict(familia="gasta", quantos=4, larg=(3, 5), alt=(3, 4), espaco=2,
             semente=0x202),
        dict(familia="terra", quantos=3, larg=(3, 4), alt=(3, 3), espaco=2,
             semente=0x101),
        dict(familia="gasta", quantos=4, larg=(3, 3), alt=(3, 3), espaco=2,
             semente=0x303),
    ],
    ruido=[(CARIMBO, "grama")],
    moveis={"moita redonda": (5, 4), "matacao": (3, 5), "pedra": (3, 5),
            "pedra virada": (3, 5), "arbusto": (5, 4), "touceira": (4, 5),
            "touceira espelhada": (4, 5)},
    cercas=2, cerca_comp=(3, 4), cerca_espaco=7,
    min_regiao=40,
)


def main():
    if "--desfazer" in sys.argv:
        return desfaz(ALVO)
    if "--demo" in sys.argv or "--autoteste" in sys.argv:
        return demo(ALVO, CIDADE)
    if "--so-tileset" in sys.argv:
        metas, attrs, _kit = desenha_kit()
        grava_tileset(metas, attrs)
        print("tileset escrito: %d metatiles novos, 0 tiles" % len(metas))
        return 0
    return roda(ALVO, CIDADE, "--aplicar" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
