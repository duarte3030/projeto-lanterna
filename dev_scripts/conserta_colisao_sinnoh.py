#!/usr/bin/env python3
"""Bloqueia a célula de Sinnoh que APAGA o jogador em vez de deixá-lo passar.

    python3 dev_scripts/conserta_colisao_sinnoh.py            # só relata
    python3 dev_scripts/conserta_colisao_sinnoh.py --demo     # autoteste, não grava
    python3 dev_scripts/conserta_colisao_sinnoh.py --aplicar  # escreve os map.bin
    python3 dev_scripts/conserta_colisao_sinnoh.py --contato /tmp/x.png
                                    # folha de contato dos metatiles que ele bloqueia

O defeito, medido no emulador antes de tocar em qualquer byte
-------------------------------------------------------------
06/09/2026, playtest do Gui em `HearthomeCity`: "está zoado o limite dos tiles,
estou entrando debaixo das árvores" e "o sprite aparece cortado pela metade em
frente à casa". Reproduzido com o `gba_runner` (ROM 2026-09-06, md5
99b141df69aaa917bd7611e3c1f69298), warp pelo menu de debug para o grupo 75 mapa
6, warp 5:

- andando até **(17,16)**, o jogador PARA DENTRO de um arbusto redondo e só o
  alto do gorro aparece por cima dele (PNG aberto e olhado);
- andando até **(20,20)**, o jogador fica **100% invisível**: o balcão da banca
  de flores é desenhado inteiro por cima dele.

O mecanismo é o de sempre nesta casa, e é de DUAS camadas, não uma:

1. `DrawMetatile` (src/field_camera.c) manda as entradas 4..7 do metatile para o
   **Bg1**, e o comentário do próprio motor diz "which covers object event
   sprites". Só o layer type `METATILE_LAYER_TYPE_COVERED` desvia essa metade
   para o Bg2; nos outros dois (`NORMAL` e `SPLIT`) ela fica POR CIMA do sprite.
2. A colisão NÃO vem do tileset: ela são os 2 bits do `map.bin`. Um metatile
   que desenha um objeto sólido por cima do sprite e vem com colisão 0 é o pior
   dos dois mundos, e é exatamente o que o Gui viu.

A régua, e por que ela é ESTREITA de propósito
----------------------------------------------
"Desenha alguma coisa por cima" NÃO serve como critério: em Hoenn de fábrica o
beiral do telhado e a copa da árvore desenham por cima e o jogador passa atrás
DE PROPÓSITO, que é o que dá profundidade ao mapa. Medido em `LittlerootTown`,
`PetalburgCity` e `RustboroCity`: dezenas de células andáveis com pixel opaco no
Bg1, todas legítimas. Ferramenta que discorda do vanilla está errada.

Então uma célula só entra quando ela satisfaz TODAS as condições abaixo:

0. **não é célula de EVENTO** (warp, placa, item escondido, gatilho, objeto).
   Warp porque quase todo caminho de warp do motor exige o jogador EM CIMA do
   tile; item escondido porque se acha pisando em cima; placa e gatilho porque
   fechá-los cala o evento;
1. **colisão 0** no `map.bin`;
2. **comportamento `MB_NORMAL`**. Isso congela sozinho grama de encontro, água,
   porta, seta, escada, gelo, ponte e areia: nada que o motor leia por
   comportamento é tocado, então nenhuma mecânica muda;
3. **COBRE**: a metade de cima do metatile (a que vai para o Bg1) tem pelo menos
   `PISO_COBERTURA` de 256 pixels opacos. Ver a nota da constante para o número e
   para a regra que foi medida e descartada;
4. **é PEÇA e não TERRENO**: o mesmo metatile tem no máximo `TETO_ABERTAS`
   células abertas neste layout;
5. **a célula é de chão comum**, elevação 3 (ver `ELEVACAO_CHAO`);
6. **a célula é ALCANÇÁVEL** pelo jogador (alagamento a partir dos warps, dos
   object_events e das bordas de conexão). Célula que ninguém pisa não é defeito,
   e mexer nela só criaria diferença de bytes sem consequência. Foi essa regra
   que jogou fora os falsos positivos de Hoenn: em `LittlerootTown` as células
   com Bg1 cheio ficam ATRÁS da cerca do topo do mapa;
7. **o layout é EXCLUSIVO da região**: layout que também veste mapa de fora fica
   de lado (ver `layouts_exclusivos`);
8. **bloquear não pode desligar nada**: depois da mudança o conjunto alcançável
   tem que perder EXATAMENTE as células corrigidas, nem uma a mais. Se bloquear
   uma célula cortasse um corredor, ela é devolvida. É essa guarda que garante
   que `completude.py` não cai por objeto que ficou inalcançável.

O que ele escreve
-----------------
Só os 2 bits de colisão: `(antigo & ~0x0C00) | 0x0400`. Metatile e elevação saem
byte a byte idênticos, o que o `--demo` confere. Nenhum `map.json`, nenhum
tileset, nenhum script. É idempotente: rodar duas vezes dá 0 células na segunda.
"""
import argparse
import collections
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
os.environ.setdefault("REPO_MAPAS", RAIZ)
import render_maps as R        # noqa: E402
import valida_warp_tile as W   # noqa: E402

# AS DUAS FAIXAS DO CORTE. Não é número redondo escolhido a dedo, é o que o
# Gui descreveu com a própria boca em 06/09/2026 jogando Snowpoint, "estou
# entrando 50% dentro dos lugares". O Bg1 de um metatile é 16x16 px e o sprite
# do jogador é 16x32 com os pés no tile, então a metade de cima do metatile
# cobre exatamente a metade de baixo do sprite: 128 de 256 px opacos É os 50%
# que ele viu.
#
# Medido nos dois defeitos que ele trouxe:
#   - Snowpoint, base do muro do templo (gTileset_Snowpoint 568/569/573): 132,
#     128 e 128 px. O desenho é neve acumulada embaixo e madeira do muro em
#     cima; parado ali, o jogador fica com as pernas na neve e o tronco dentro
#     da parede. Estava ANDÁVEL, e a fonte do demake também deixa andável.
#   - Hearthome, arbusto 542 (152 px) e balcão da banca 673 (248 px), os dois do
#     playtest anterior.
# E o contra-exemplo que NÃO pode entrar: o alto do muro da banca de Hearthome
# (640), beiral legítimo por onde se passa atrás, cobre 118 px. A folga entre
# 118 e 128 é de 10 px, estreita, e é por isso que existe o VETO DO VANILLA
# logo abaixo: quando há prova externa de que a peça é chão, ela ganha do corte.
#
# Existiu um corte de 140 aqui (06/09/2026, calibrado só em Hearthome) e ele
# deixava Snowpoint inteira de fora, justamente o mapa da reclamação.
#
# Existiu também uma segunda regra, de CONTRADIÇÃO ("o mesmo metatile aparece
# com colisão 1 em outra célula do mesmo mapa"), e ela foi MEDIDA E JOGADA FORA
# em 06/09/2026: ela olha um dado que a própria ferramenta ESCREVE, então
# bloquear uma célula criava contradição onde não havia, e a resposta passava a
# depender de quantas vezes a ferramenta tinha rodado (medido: 744 células na
# árvore já aplicada contra 1.221 numa árvore limpa, e mais 467 numa terceira
# execução). Régua que muda de resposta a cada execução não é régua. A
# cobertura, ao contrário, é função só do tileset: não se mexe nunca.
PISO_COBERTURA = 128
PISO_SOLTO = 140

MB_NORMAL = 0

# CHÃO COMUM. Só célula de elevação 3 (`ELEVATION_DEFAULT`) entra na régua, e
# isso não é cautela solta: elevação 15 (`ELEVATION_MULTI_LEVEL`) é o IDIOMA DE
# PONTE do Emerald, onde a passarela cobre o sprite de propósito e quem anda por
# baixo some mesmo. Está medido no ESTADO 0.u (o conserto das passarelas de
# Sunyshore): a Cycling Road de Hoenn tem 185 células de elevação 15 e as 185
# cobrem, e em Sinnoh a Route 216 tem 24 e a Route 205 South 15, todas legítimas.
# Bloqueá-las mataria a ponte. Elevação 4 e 5 são o piso ALTO de uma passarela, e
# quem cuida dele é `conserta_passarelas_sinnoh.py`, com régua própria. Medido
# em 06/09/2026: sem esta trava a régua queria fechar 228 células de elevação 4 e
# 58 de elevação 15, entre elas as três pontes da Route 216.
ELEVACAO_CHAO = 3

# QUANTAS células abertas do MESMO metatile o mapa pode ter e ele ainda ser um
# OBJETO. Acima disso é TERRENO, e terreno não se conserta com colisão.
# Medido em 06/09/2026 na Route 212 South: o metatile 705, a lama do brejo, tem
# as duas camadas cheias (256 px embaixo e 256 em cima) e aparece em 191 células
# andáveis em fila. Ele cobre o sprite, sim, mas fechá-lo emparedaria o brejo
# inteiro; o conserto certo ali é `METATILE_LAYER_TYPE_COVERED` no tileset, que é
# outra obra e outra decisão. O que o Gui viu é o contrário disso: peça de
# cenário que aparece POUCAS vezes, cada uma dentro de uma fachada (o arbusto
# 542 de Hearthome tem 2 células abertas e 92 fechadas, o balcão 673 tem 3).
TETO_ABERTAS = 12

# Metatile que o motor desenha com a metade de cima no Bg2, e não no Bg1.
LAYER_COVERED = 1


# ---------------------------------------------------------------- leitura
def layouts():
    with open(f"{RAIZ}/data/layouts/layouts.json", encoding="utf-8") as f:
        return {l["id"]: l for l in json.load(f)["layouts"]}


def mapas_da_regiao(marca="Sinnoh"):
    """Nomes de pasta de `data/maps` dos grupos cujo nome tem a marca."""
    with open(f"{RAIZ}/data/maps/map_groups.json", encoding="utf-8") as f:
        g = json.load(f)
    fora = []
    for grupo in g["group_order"]:
        if marca.lower() in grupo.lower():
            fora.extend(g[grupo])
    return fora


def n_metatiles_primario(layout):
    """640 em bigPrimary/FRLG, 512 em Emerald. Ver GetNumMetatilesInPrimary."""
    return 640 if layout.get("layout_version") in ("johto", "frlg") else 512


def _atributos(pasta, frlg):
    largura = 4 if frlg else 2
    dados = open(os.path.join(pasta, "metatile_attributes.bin"), "rb").read()
    fora = []
    for i in range(len(dados) // largura):
        v = int.from_bytes(dados[i * largura:(i + 1) * largura], "little")
        if frlg:
            fora.append((v & 0x1FF, (v >> 29) & 3))
        else:
            fora.append((v & 0xFF, (v >> 12) & 0xF))
    return fora


_CACHE_TS = {}


def perfil_do_layout(layout):
    """metatile -> (comportamento, layer type, pixels opacos no Bg1).

    Devolve None quando algum tileset do layout não pode ser lido (sem pasta,
    sem paleta). Mapa assim fica de fora em vez de ser adivinhado.
    """
    chave = (layout["primary_tileset"], layout.get("secondary_tileset"),
             layout.get("layout_version"))
    if chave in _CACHE_TS:
        return _CACHE_TS[chave]
    try:
        pri = R.carregar_tileset(layout["primary_tileset"])
        sec = R.carregar_tileset(layout["secondary_tileset"])
        pasta_pri = W.pasta_do_tileset(layout["primary_tileset"])
        pasta_sec = W.pasta_do_tileset(layout["secondary_tileset"])
        frlg = layout.get("layout_version") == "frlg"
        attr_pri = _atributos(pasta_pri, frlg)
        attr_sec = _atributos(pasta_sec, frlg)
    except Exception:
        _CACHE_TS[chave] = None
        return None

    npri = n_metatiles_primario(layout)
    perfil = {}
    for mt in range(npri + len(attr_sec)):
        if mt < npri:
            if mt >= len(attr_pri):
                continue
            comportamento, camada = attr_pri[mt]
            bruto, local = pri["metatiles"], mt
        else:
            comportamento, camada = attr_sec[mt - npri]
            bruto, local = sec["metatiles"], mt - npri
        if local * 16 + 16 > len(bruto):
            continue
        entradas = R.entradas_metatile(bruto, local)
        opacos = 0
        if camada != LAYER_COVERED:
            for idx, _fh, _fv, _pal in entradas[4:]:
                tile = R.resolver_tile(pri, sec, idx)
                if tile is None:
                    continue
                opacos += sum(1 for linha in tile for c in linha if c != 0)
        perfil[mt] = (comportamento, camada, opacos)
    _CACHE_TS[chave] = perfil
    return perfil


def le_grade(layout):
    w, h = layout["width"], layout["height"]
    dados = open(os.path.join(RAIZ, layout["blockdata_filepath"]), "rb").read()
    if len(dados) < w * h * 2:
        return w, h, None
    return w, h, list(struct.unpack(f"<{w * h}H", dados[:w * h * 2]))


# ------------------------------------------------------------ alcance
def sementes(mapa, w, h):
    """Células por onde o jogador entra: warp, objeto e borda de conexão."""
    fora = set()
    for wp in mapa.get("warp_events", []):
        fora.add((wp["x"], wp["y"]))
    for ob in mapa.get("object_events", []):
        fora.add((ob["x"], ob["y"]))
    for co in mapa.get("coord_events", []):
        fora.add((co["x"], co["y"]))
    for bg in mapa.get("bg_events", []):
        fora.add((bg["x"], bg["y"]))
    for cx in mapa.get("connections") or []:
        d = cx.get("direction")
        if d == "up":
            fora.update((x, 0) for x in range(w))
        elif d == "down":
            fora.update((x, h - 1) for x in range(w))
        elif d == "left":
            fora.update((0, y) for y in range(h))
        elif d == "right":
            fora.update((w - 1, y) for y in range(h))
    return {(x, y) for x, y in fora if 0 <= x < w and 0 <= y < h}


def alcance(grade, w, h, raizes):
    """Alagamento 4-vizinhos sobre célula de colisão 0, a partir das raízes.

    A raiz entra mesmo se ela mesma for sólida (warp de porta animada é sólido
    de propósito), porque é dali que o jogador sai andando.
    """
    visto = set()
    fila = collections.deque()
    for p in raizes:
        if p not in visto:
            visto.add(p)
            fila.append(p)
    while fila:
        x, y = fila.popleft()
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= nx < w and 0 <= ny < h) or (nx, ny) in visto:
                continue
            if (grade[ny * w + nx] >> 10) & 3:
                continue
            visto.add((nx, ny))
            fila.append((nx, ny))
    return visto


# ------------------------------------------------------------ o conserto
def bloqueia(palavra):
    """Liga a colisão sem tocar em metatile nem em elevação."""
    return (palavra & ~0x0C00) | (1 << 10)


def candidatos_do_mapa(mapa, layout, grade, w, h, perfil, veto, voltas=8):
    """Células que a régua aceita, até o ponto fixo.

    O laço existe porque a GUARDA muda de resposta entre passadas: uma célula
    que na primeira volta cortaria o caminho para um beco pode ser bloqueada na
    segunda, depois que o beco deixou de ser alcançável por outra célula do
    mesmo prédio. Sem o laço a ferramenta não é idempotente (medido: 6 células
    sobravam para a segunda execução), e ferramenta que muda de resposta a cada
    execução não serve de régua.
    """
    todos, atual = [], list(grade)
    for _ in range(voltas):
        novos, atual = _uma_volta(mapa, layout, atual, w, h, perfil, veto)
        if not novos:
            break
        todos.extend(novos)
    return todos, atual


def _uma_volta(mapa, layout, grade, w, h, perfil, veto):
    """Uma passada da régua: candidatos, alcance e guarda."""

    abertas = collections.Counter(palavra & 0x3FF for palavra in grade
                                  if not ((palavra >> 10) & 3))
    raizes = sementes(mapa, w, h)
    antes = alcance(grade, w, h, raizes)
    # Célula de warp nunca é bloqueada, mesmo que o desenho cubra o sprite.
    # Quase todo caminho de warp do motor exige o jogador EM CIMA do tile
    # (`TryStartWarpEventScript`, `TryArrowWarp`, escada diagonal), então
    # bloquear ali mata a porta. Medido em 06/09/2026: sem esta linha, a passada
    # de colisão fechava o arco do ginásio de Hearthome que a passada de portas
    # tinha acabado de abrir.
    # Célula de EVENTO nunca é bloqueada: warp, placa, item escondido e gatilho.
    # Medido em 06/09/2026: o item escondido de `VeilstoneCity` em (26,24) mora
    # num tile de `MB_NORMAL` cujo desenho cobre o sprite, e a primeira versão
    # fechou o tile DELE e os três vizinhos, deixando o item impossível de pegar
    # (item escondido se acha pisando em cima). Placa é o mesmo problema um passo
    # ao lado: fechar o tile de onde se lê a placa cala a placa.
    de_evento = {(wp["x"], wp["y"]) for wp in mapa.get("warp_events", [])}
    de_evento |= {(bg["x"], bg["y"]) for bg in mapa.get("bg_events", [])}
    de_evento |= {(co["x"], co["y"]) for co in mapa.get("coord_events", [])}
    de_evento |= {(ob["x"], ob["y"]) for ob in mapa.get("object_events", [])}

    brutos = []
    for (x, y) in sorted(antes - de_evento):
        i = y * w + x
        palavra = grade[i]
        if (palavra >> 10) & 3:
            continue
        if (palavra >> 12) & 0xF != ELEVACAO_CHAO:
            continue
        mt = palavra & 0x3FF
        p = perfil.get(mt)
        if p is None:
            continue
        comportamento, _camada, opacos = p
        if comportamento != MB_NORMAL:
            continue
        if opacos < PISO_COBERTURA:
            continue
        # As DUAS FAIXAS. Cobertura sozinha não separa defeito de decoração
        # legítima, e está medido: o vaso de planta dos portões de Sinnoh
        # (`gTileset_Pasos` 520 e 538) cobre 138 px, MAIS que a base do muro do
        # templo de Snowpoint (128) que é defeito de verdade. Um número só
        # nunca vai ordenar os dois. Então:
        #   - de `PISO_SOLTO` para cima, a peça cobre tanto que ela apaga o
        #     jogador esteja onde estiver (arbusto 152, balcão 248, tronco 232);
        #   - entre `PISO_COBERTURA` e `PISO_SOLTO`, ela só é defeito se for
        #     BASE DE PAREDE, isto é, se a célula logo ACIMA já é bloqueada.
        #     É o que separa a neve encostada no muro do templo (acima está o
        #     muro, bloqueado) do vaso de planta do portão da Route 209 (acima
        #     está o chão da sala, e o vaso existe para se passar atrás).
        if opacos < PISO_SOLTO and not (y > 0 and (grade[(y - 1) * w + x] >> 10) & 3):
            continue
        if identidade(layout, mt) in veto:
            continue
        if abertas[mt] > TETO_ABERTAS:
            continue
        brutos.append(((x, y), mt, "cobre", opacos))

    # Guarda: bloquear não pode desligar nada. Uma de cada vez, e devolve a que
    # cortar corredor. A ordem é estável (varredura por linha), então o
    # resultado não depende de sorte.
    aceitos = []
    trabalho = list(grade)
    for (pos, mt, motivo, opacos) in brutos:
        x, y = pos
        antigo = trabalho[y * w + x]
        trabalho[y * w + x] = bloqueia(antigo)
        depois = alcance(trabalho, w, h, raizes)
        perdidos = antes - depois - {p for p, *_ in aceitos} - {pos}
        if perdidos:
            trabalho[y * w + x] = antigo
            continue
        aceitos.append((pos, mt, motivo, opacos))
    return aceitos, trabalho


def identidade(layout, mt):
    """(tileset, índice local). O número solto do metatile não identifica nada.

    O 528 de `gTileset_DewfordGym` e o 528 de qualquer outro secundário são
    desenhos diferentes; contar os dois juntos faz o veto abaixo vetar mapa
    errado.
    """
    npri = n_metatiles_primario(layout)
    if mt < npri:
        return ("pri", layout["primary_tileset"], mt)
    return ("sec", layout.get("secondary_tileset"), mt - npri)


def veto_do_vanilla(marca):
    """Metatiles que algum mapa DE FORA da região pisa: esses nunca se bloqueia.

    O corte de cobertura sozinho não separa "base de muro" de "peça de chão que
    cobre um pouco", e a folga entre os dois é de 10 px. Quando existe prova
    EXTERNA, ela ganha do corte, e a prova externa mais forte que este repo tem
    é o Hoenn de fábrica: mapa que a GameFreak desenhou e que ninguém aqui
    editou.

    Medido em 06/09/2026, foi este veto que impediu o estrago: os ginásios de
    Veilstone e de Sunyshore vestem `gTileset_DewfordGym` e
    `gTileset_MauvilleGym`, e o corte de 128 queria fechar 39 células deles. Os
    mesmos metatiles (530, 531, 533, 534, 536, 546, 547, 528...) aparecem
    ANDÁVEIS no ginásio de Dewford e no de Mauville de fábrica, dezenas de
    vezes. Ferramenta que discorda do vanilla está errada, e aqui ela estava.

    Tileset que só a região usa (Snowpoint, Hearthome, Jubilife, Canalave...)
    não tem prova externa nenhuma, e aí quem decide é a cobertura.
    """
    todos = layouts()
    with open(f"{RAIZ}/data/maps/map_groups.json", encoding="utf-8") as f:
        mg = json.load(f)
    da_regiao = set(mapas_da_regiao(marca))
    fora = set()
    lidos = set()
    for grupo in mg["group_order"]:
        for nome in mg[grupo]:
            if nome in da_regiao:
                continue
            caminho = f"{RAIZ}/data/maps/{nome}/map.json"
            if not os.path.exists(caminho):
                continue
            with open(caminho, encoding="utf-8") as f:
                layout = todos.get(json.load(f)["layout"])
            if layout is None or layout["id"] in lidos:
                continue
            lidos.add(layout["id"])
            w, h, grade = le_grade(layout)
            if grade is None:
                continue
            for palavra in grade:
                if not ((palavra >> 10) & 3):
                    fora.add(identidade(layout, palavra & 0x3FF))
    return fora


def layouts_exclusivos(marca):
    """Layouts cujos usuários são TODOS da região. Os outros ficam de fora.

    Sem esta trava a ferramenta vaza para fora de Sinnoh, e vaza no pior lugar:
    medido em 06/09/2026, os cinco quartos da Elite dos Quatro de Sinnoh vestem
    os layouts `LAYOUT_EVER_GRANDE_CITY_*_ROOM` DE HOENN, e a primeira execução
    mexeu em 13 células de cada um deles, ou seja no Hoenn de fábrica. O mesmo
    vale para a planta de Pokecenter, usada por dezenas de mapas de outras
    regiões. Layout compartilhado só se conserta com dono declarado.
    """
    with open(f"{RAIZ}/data/maps/map_groups.json", encoding="utf-8") as f:
        mg = json.load(f)
    da_regiao = set(mapas_da_regiao(marca))
    donos = collections.defaultdict(set)
    for grupo in mg["group_order"]:
        for nome in mg[grupo]:
            caminho = f"{RAIZ}/data/maps/{nome}/map.json"
            if os.path.exists(caminho):
                with open(caminho, encoding="utf-8") as f:
                    donos[json.load(f)["layout"]].add(nome)
    return {lid for lid, usuarios in donos.items() if usuarios <= da_regiao}


def varre(marca="Sinnoh", so=None):
    todos = layouts()
    exclusivos = layouts_exclusivos(marca)
    veto = veto_do_vanilla(marca)
    fora = []
    for nome in mapas_da_regiao(marca):
        if so and nome not in so:
            continue
        caminho = f"{RAIZ}/data/maps/{nome}/map.json"
        if not os.path.exists(caminho):
            continue
        with open(caminho, encoding="utf-8") as f:
            mapa = json.load(f)
        layout = todos.get(mapa.get("layout"))
        if layout is None or mapa["layout"] not in exclusivos:
            continue
        perfil = perfil_do_layout(layout)
        if perfil is None:
            continue
        w, h, grade = le_grade(layout)
        if grade is None:
            continue
        aceitos, nova = candidatos_do_mapa(mapa, layout, grade, w, h, perfil, veto)
        if aceitos:
            fora.append((nome, layout, w, h, grade, nova, aceitos))
    return fora


def grava(resultado):
    """Escreve os map.bin. Um layout pode servir vários mapas: grava uma vez."""
    escritos, celulas = {}, 0
    for nome, layout, w, h, grade, nova, aceitos in resultado:
        caminho = os.path.join(RAIZ, layout["blockdata_filepath"])
        if caminho in escritos:
            continue
        with open(caminho, "wb") as f:
            f.write(struct.pack(f"<{w * h}H", *nova))
        escritos[caminho] = nome
        celulas += len(aceitos)
    return len(escritos), celulas


# ------------------------------------------------------------------ demo
def demo():
    """Autoteste: prova a régua, a guarda e a escrita, sem gravar nada."""
    # 1. Os dois bits, e só eles.
    assert bloqueia(0x3D2A) == 0x352A, hex(bloqueia(0x3D2A))  # colisão 3 -> 1
    assert bloqueia(0x0000) == 0x0400
    for palavra in (0x0001, 0x3FFF, 0x1234, 0xC1A6):
        novo = bloqueia(palavra)
        assert novo & 0x3FF == palavra & 0x3FF, "mexeu no metatile"
        assert novo >> 12 == palavra >> 12, "mexeu na elevação"
        assert (novo >> 10) & 3 == 1, "não bloqueou"

    # 2. O alagamento respeita colisão e enxerga a raiz sólida.
    g = [0x0000, 0x0400, 0x0000]
    assert alcance(g, 3, 1, {(0, 0)}) == {(0, 0)}
    assert alcance([0, 0, 0], 3, 1, {(0, 0)}) == {(0, 0), (1, 0), (2, 0)}
    assert (1, 0) in alcance(g, 3, 1, {(1, 0)}), "raiz sólida tem que entrar"

    # 3. Os três números que decidem o corte, lidos do tileset e não lembrados.
    todos = layouts()
    lay = todos["LAYOUT_HEARTHOME_CITY"]
    perfil = perfil_do_layout(lay)
    assert perfil[542][0] == MB_NORMAL, perfil[542]
    assert perfil[542][2] >= PISO_COBERTURA, ("o arbusto que o Gui atravessou "
                                              f"tem que entrar: {perfil[542]}")
    assert perfil[673][2] >= PISO_COBERTURA, perfil[673]
    assert perfil[640][2] < PISO_COBERTURA, ("o alto do muro da banca é beiral e "
                                             f"não pode entrar: {perfil[640]}")

    # 4. Hoenn de fábrica não pode ser tocado, nem de raspão: os layouts da
    #    Elite dos Quatro de Hoenn vestem os quartos da Elite de Sinnoh.
    exclusivos = layouts_exclusivos("Sinnoh")
    for compartilhado in ("LAYOUT_EVER_GRANDE_CITY_SIDNEYS_ROOM",
                          "LAYOUT_EVER_GRANDE_CITY_DRAKES_ROOM"):
        assert compartilhado not in exclusivos, compartilhado
    assert "LAYOUT_HEARTHOME_CITY" in exclusivos

    # 4b. O VETO DO VANILLA: o que o Hoenn de fábrica pisa, ninguém fecha.
    veto = veto_do_vanilla("Sinnoh")
    ginasio = todos["LAYOUT_VEILSTONE_CITY_GYM"]
    for mt in (530, 531, 533, 534, 546):
        assert identidade(ginasio, mt) in veto, (
            f"o metatile {mt} é chão no ginásio de Dewford de fábrica e tem "
            "que estar vetado")
    assert identidade(lay, 542) not in veto, ("gTileset_Hearthome só veste "
                                              "Sinnoh: não pode ter veto")

    # 5. O caso do Gui, e a escrita que mexe SÓ na colisão.
    w, h, grade = le_grade(lay)
    with open(f"{RAIZ}/data/maps/HearthomeCity/map.json", encoding="utf-8") as f:
        mapa = json.load(f)
    aceitos, nova = candidatos_do_mapa(mapa, lay, grade, w, h, perfil, veto)
    postos = {p for p, *_ in aceitos}
    ja_feito = ((grade[16 * w + 17] >> 10) & 3) != 0
    if not ja_feito:
        assert (17, 16) in postos, "o arbusto que o Gui atravessou ficou de fora"
        assert (20, 20) in postos, "o balcão que apagou o jogador ficou de fora"
    for i, (a, b) in enumerate(zip(grade, nova)):
        assert a & 0x3FF == b & 0x3FF and a >> 12 == b >> 12, i

    # 5c. SNOWPOINT, a reclamação de 06/09: a base do muro do templo tem que
    #     fechar, e ela cobre exatamente a metade do sprite.
    snow = todos["LAYOUT_SNOWPOINT_CITY"]
    p_snow = perfil_do_layout(snow)
    for mt in (568, 569, 573):
        assert p_snow[mt][2] >= PISO_COBERTURA, (mt, p_snow[mt])
    ws, hs, gs = le_grade(snow)
    with open(f"{RAIZ}/data/maps/SnowpointCity/map.json", encoding="utf-8") as f:
        m_snow = json.load(f)
    ac_snow, _ = candidatos_do_mapa(m_snow, snow, gs, ws, hs, p_snow, veto)
    postos_snow = {p for p, *_ in ac_snow}
    if not ((gs[7 * ws + 13] >> 10) & 3):
        for celula in ((13, 7), (14, 7), (19, 7), (20, 7), (21, 7)):
            assert celula in postos_snow, (
                f"a base do muro do templo em {celula} ficou de fora")
        # (12,7) fica de fora DE PROPÓSITO: tem object_event em cima dela, e
        # célula de evento nunca é bloqueada (regra 0). O NPC de Snowpoint está
        # plantado na neve do muro; tirá-lo dali é decisão de conteúdo, não de
        # colisão.
        assert (12, 7) not in postos_snow
        # e a fachada do ginásio, o outro prédio da reclamação
        for celula in ((15, 33), (19, 33)):
            assert celula in postos_snow, celula

    # 5d. O VASO DE PLANTA do portão da Route 209, que cobre MAIS que o defeito
    #     de Snowpoint (138 contra 128) e mesmo assim é decoração legítima: ele
    #     tem chão andável em cima, então a faixa de baixo o recusa. Sem esta
    #     regra a ferramenta emparedava o portão inteiro (medido em 06/09/2026:
    #     a linha 7 de `Route209_Access` fechava de ponta a ponta).
    portao = todos["LAYOUT_ROUTE209_ACCESS"]
    p_portao = perfil_do_layout(portao)
    wp, hp, gp = le_grade(portao)
    assert p_portao[gp[7 * wp + 1] & 0x3FF][2] > PISO_COBERTURA, "o vaso cobre muito"
    assert p_portao[gp[7 * wp + 1] & 0x3FF][2] < PISO_SOLTO, "e mesmo assim é vaso"
    with open(f"{RAIZ}/data/maps/Route209_Access/map.json", encoding="utf-8") as f:
        m_portao = json.load(f)
    ac_p, _ = candidatos_do_mapa(m_portao, portao, gp, wp, hp, p_portao, veto)
    assert (1, 7) not in {q for q, *_ in ac_p}, "o vaso do portão não pode fechar"

    # 6. Idempotência de verdade: a régua não olha nada que ela mesma escreve.
    aceitos2, _ = candidatos_do_mapa(mapa, lay, nova, w, h, perfil, veto)
    assert not aceitos2, f"não é idempotente: {aceitos2[:5]}"

    print(f"demo OK: {len(aceitos)} células em HearthomeCity; arbusto 542 cobre "
          f"{perfil[542][2]}/256 px, balcão 673 cobre {perfil[673][2]}, beiral "
          f"640 cobre {perfil[640][2]}, corte em {PISO_COBERTURA}")
    return 0


def folha_de_contato(resultado, saida):
    """Desenha cada metatile distinto que a régua bloqueou. Evidência, não fé."""
    from PIL import Image, ImageDraw
    vistos = {}
    for nome, layout, w, h, grade, nova, aceitos in resultado:
        for pos, mt, motivo, opacos in aceitos:
            chave = (layout["primary_tileset"], layout["secondary_tileset"], mt)
            vistos.setdefault(chave, [motivo, opacos, 0, nome, layout])
            vistos[chave][2] += 1
    colunas = min(20, max(1, len(vistos)))
    linhas = (len(vistos) + colunas - 1) // colunas
    folha = Image.new("RGB", (colunas * 78, linhas * 110), (24, 24, 24))
    d = ImageDraw.Draw(folha)
    for i, (chave, (motivo, opacos, n, nome, layout)) in enumerate(sorted(
            vistos.items(), key=lambda kv: -kv[1][2])):
        pri_nome, sec_nome, mt = chave
        pri = R.carregar_tileset(pri_nome)
        sec = R.carregar_tileset(sec_nome)
        npri = n_metatiles_primario(layout)
        local = mt if mt < npri else mt - npri
        bruto = pri["metatiles"] if mt < npri else sec["metatiles"]
        im = Image.new("RGB", (16, 16), (255, 0, 255))
        px = im.load()
        if local * 16 + 16 <= len(bruto):
            for j, (idx, fh, fv, pal) in enumerate(R.entradas_metatile(bruto, local)):
                tile = R.resolver_tile(pri, sec, idx)
                if tile is None:
                    continue
                cores = (pri["paletas"] if pal < 6 else sec["paletas"]).get(pal)
                if not cores:
                    continue
                R.desenhar_tile(px, ((j % 4) % 2) * 8, ((j % 4) // 2) * 8,
                                tile, cores, fh, fv)
        cx, cy = (i % colunas) * 78, (i // colunas) * 110
        folha.paste(im.resize((64, 64), Image.NEAREST), (cx + 6, cy + 6))
        d.text((cx + 6, cy + 72), f"{mt} x{n}", fill=(255, 255, 0))
        d.text((cx + 6, cy + 84), f"{motivo} {opacos}", fill=(0, 255, 160))
        d.text((cx + 6, cy + 96), nome[:12], fill=(160, 160, 160))
    folha.save(saida)
    return len(vistos)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--regiao", default="Sinnoh")
    ap.add_argument("--mapa", action="append")
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--contato")
    args = ap.parse_args()
    if args.demo:
        return demo()

    resultado = varre(args.regiao, set(args.mapa) if args.mapa else None)
    total = sum(len(r[6]) for r in resultado)
    print(f"{len(resultado)} mapas de {args.regiao} com célula que apaga o "
          f"jogador, {total} células no total\n")
    for nome, layout, w, h, grade, nova, aceitos in sorted(
            resultado, key=lambda r: -len(r[6])):
        motivos = collections.Counter(m for _, _, m, _ in aceitos)
        amostra = ", ".join(f"({x},{y})" for (x, y), *_ in aceitos[:6])
        print(f"  {len(aceitos):4d}  {nome:42s} {dict(motivos)}  {amostra}")
    if args.contato:
        n = folha_de_contato(resultado, args.contato)
        print(f"\nfolha de contato: {n} metatiles distintos em {args.contato}")
    if args.aplicar:
        arquivos, celulas = grava(resultado)
        print(f"\ngravados {arquivos} map.bin, {celulas} células bloqueadas")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
