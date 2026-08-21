#!/usr/bin/env python3
"""Os lendarios de Sinnoh que ainda nao estavam em mapa nenhum.

Uso:
    python3 dev_scripts/lendarios_sinnoh.py            # so relata o plano
    python3 dev_scripts/lendarios_sinnoh.py --aplica   # escreve
    python3 dev_scripts/lendarios_sinnoh.py --demo     # autoteste com mutacao plantada

## O buraco que este arquivo fecha

Medido em 21/08/2026, dos lendarios de Sinnoh SO Dialga e Palkia existiam nesta
ROM (`SpearPillar_Dialga` e `SpearPillar_Palkia`, como bg_event). Os outros dez
nao tinham objeto nem script em mapa nenhum: `grep SPECIES_<X>` em
`data/maps/*/{map.json,scripts.inc}` devolve vazio para HEATRAN, SHAYMIN,
DARKRAI, CRESSELIA, ARCEUS, REGIGIGAS, ROTOM, UXIE, AZELF e MESPRIT.

Decisao do Gui de 21/08/2026: "os Pokemon lendarios eu quero, nem que coloque em
locais de facil acesso". O Battle Zone inteiro, o Turnback Cave, o Sendoff Spring
e os mapas de Mystery Gift sairam do escopo, entao quem morava la precisa de
casa nova; quem tem casa viva vai para casa.

## Onde cada um entra, e por que

| Pokemon | lar na fonte | existe aqui? | destino |
|---|---|---|---|
| UXIE | acuity_cavern | SIM (`AcuityCavern`) | o lar |
| AZELF | valor_cavern | SIM (`ValorCavern`) | o lar |
| MESPRIT | verity_cavern | SIM (`VerityCavern`) | o lar |
| ROTOM | old_chateau_back_middle_west_room | SIM | o lar |
| REGIGIGAS | snowpoint_temple_b5f | SIM | o lar, SEM a trava |
| HEATRAN | stark_mountain_room_3 | mapa existe, ZONA fora de escopo | Mt. Coronet B1F |
| SHAYMIN | flower_paradise | NAO | Floaroma Town |
| DARKRAI | newmoon_island_forest | NAO | Canalave City |
| CRESSELIA | fullmoon_island_forest | NAO | Canalave City |
| ARCEUS | hall_of_origin | NAO | Spear Pillar, depois de Dialga e Palkia |
| MANAPHY | pokemon_mansion_office (Ranger) | nao ha ENCONTRO na fonte | fica de fora |
| PHIONE | so choca do ovo de Manaphy | idem | fica de fora |

Tres medicoes que mudaram o plano, e por isso ficam escritas:

1. **O Fuego Ironworks NAO existe neste repo** (nem `data/maps/`, nem
   `data/layouts/layouts.json`), entao o Heatran vai para o Mt. Coronet, que era
   a segunda opcao ja prevista. O Stark Mountain existe como mapa, mas o
   `StarkMountainOutside` ainda veste o molde de portao 13x9 e so se chega la
   pela Route227, que e Battle Zone: fora de escopo por decisao do Gui.
2. **A Floaroma Meadow tambem nao existe**, entao o Shaymin fica na Floaroma
   Town, que e o mapa vivo mais ligado a ele.
3. **As tres cavernas do lago EXISTEM** (`AcuityCavern`, `ValorCavern`,
   `VerityCavern`, no grupo `gMapGroup_SinnohCavernas`) e estao vazias. Uma
   listagem apressada de `data/maps/` nao acha porque o nome nao tem "Lake".
   O trio do lago vai para casa, e nao para a beira do lago.

## A trava do Snowpoint Temple

Na fonte (`res/field/scripts/scripts_snowpoint_temple_b5f.s`) o Regigigas so
acorda com `CheckHasAllLegendaryTitansInParty`, ou seja Regirock, Regice e
Registeel no time. **A trava cai por decisao do Gui**: o encontro entra direto.
Nao ha trava de andar no caminho: `SnowpointTemple1F` a `B5F` sao mapas de
verdade e o B5F tem 253 tiles alcancaveis a pe a partir do warp.

## O idioma, copiado do que ja existe aqui

`WhirlIslands_LugiaChamber` e `TinTower_RoofDay` (de `porta_cenas_johto.py`) sao
o molde: `object_event` com `OBJ_EVENT_GFX_SPECIES(...)`, `flag` de HIDE propria,
e script que faz `playmoncry`, `seteventmon`, `FLAG_SYS_CTRL_OBJ_DELETE`,
`special BattleSetup_StartLegendaryBattle`, e em VITORIA ou CAPTURA apaga o bicho
com `fadescreenswapbuffers` + `removeobject` + `setflag` da HIDE. Fuga, derrota e
teleporte NAO apagam nada, senao uma Poke Ball errada tira o lendario do save.

Duas diferencas deliberadas em relacao ao Lugia:

- **Um `msgbox` de abertura ANTES do cry.** E o mesmo que `SpearPillar_Dialga`
  faz. Ele existe por dois motivos: da a fala da fonte (o grito de cada bicho
  esta em `res/text/*.json` do pokeplatinum) e, sobretudo, e o que deixa o T123
  PROVAR a trava sem entrar em batalha, porque o harness nao le a tela de
  batalha. Um A abre a caixa, e dai em diante o D-pad nao anda.
- **Sem gimmick, sem Dynamax.** A Fase F esta congelada.

`OBJ_EVENT_GFX_SPECIES` funciona para os dez: conferido em
`src/data/pokemon/species_info/*.h` que todos tem `OVERWORLD(...)` (o Arceus
pelo macro `ARCEUS_SPECIES_INFO`). Custo de ROM proximo de zero, porque o
desenho ja esta compilado em `gSpeciesInfo`. (De passagem: o comentario de
`SpearPillar_Dialga/scripts.inc` que diz que esta build nao desenha Dialga esta
VELHO; o Dialga tem `OVERWORLD`. Nao mexi neles, so anoto.)

## Onde cada objeto cai (medido, nunca escolhido a olho)

`planeja()` faz busca em largura sobre o `map.bin`, com a regra do motor
(colisao E elevacao, a mesma de `conserta_route222.alcance`), e escolhe o tile
por quatro portoes:

1. o tile e alcancavel a pe a partir dos warps do mapa;
2. **por o lendario ali nao ilha ninguem**: a alcancabilidade DEPOIS, tratando o
   bicho como parede, tem que ser a de antes menos o proprio tile;
3. o tile nao encosta em warp (raio 1) nem em NPC que anda (raio 2), que e a
   familia de caso flaky do T121.4 e do T98.9;
4. existe uma ROTA de pernas retas do warp de teste ate ele, com a ULTIMA perna
   saturando CONTRA o bicho, e pelo menos um tile livre atras dele. E dai que
   sai o par negativo: com a flag acesa o tile some e a mesma perna escorrega
   mais longe.

A primeira perna de toda rota e SATURANTE de proposito: assim a direcao para
onde o boneco olha depois do warp nao muda o resultado, e mapa cujo warp cai em
tile bloqueado (porta de cidade, colisao 1) da no mesmo lugar quer o motor pouse
o jogador na porta, quer no tile de baixo. As pernas seguintes sao exatas com
UM aperto a mais, porque a primeira tecla de uma direcao nova so VIRA o boneco
(medido em 21/08/2026, T121.1).

## Flags

Dez flags novas, 0x3220 a 0x3229, apelido de `FLAG_UNUSED` no fim da maior faixa
livre (0x20D2-0x3230, 4447 flags, `dev_scripts/flags_livres.py`). Escolhida a
CAUDA da faixa de proposito: quem pedir reserva pega a cabeca, e nesta rodada ha
outros executores na mesma arvore. Apelidar `FLAG_UNUSED` nao mexe em
`FLAGS_COUNT`: **custo zero de save**.
"""
import argparse
import json
import os
import re
import struct
from collections import deque

import valida_warp_tile as V   # o leitor de comportamento de metatile ja existe

# O motor faz o jogador SAIR de porta andando um tile para o sul: entrar por um
# warp de comportamento de porta pousa em (x, y+1), nao em (x, y). Medido em
# 21/08/2026 com sonda no emulador: `MAP_CANALAVE_CITY` warp 10 esta em (27,13),
# que e MB_NON_ANIMATED_DOOR e tem colisao ZERO, e o jogador acorda em (27,14).
# Os warps de MB_LADDER e MB_SOUTH_ARROW_WARP pousam no proprio tile, e foi por
# isso que a primeira versao desta ferramenta acertou oito mapas e errou um: ela
# olhava COLISAO, que e uma camada mais rasa que a da afirmacao (licao 4.1).
PORTAS = ("MB_ANIMATED_DOOR", "MB_NON_ANIMATED_DOOR", "MB_WATER_DOOR")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FLAGS_H = f"{RAIZ}/include/constants/flags.h"
CASOS = f"{RAIZ}/dev_scripts/testes_criticos/123_lendarios_sinnoh.json"
MARCA = "lendarios_sinnoh"
MARCA_INI = "// >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>"
MARCA_FIM = "// <<< Lendarios de Sinnoh <<<"
INC_INI = "@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>"
INC_FIM = "@ <<< Lendarios de Sinnoh <<<"
FLAG_BASE = 0x3220

DIRS = {"RIGHT": (1, 0), "LEFT": (-1, 0), "DOWN": (0, 1), "UP": (0, -1)}
OPOSTO = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
# Tipos de movimento que TIRAM o NPC do lugar. Caso escrito perto de um deles
# nasce flaky: e a familia do T121.4, do T98.9 e do T108.2.
MOVEIS = ("WANDER", "WALK_UP_AND_DOWN", "WALK_LEFT_AND_RIGHT", "COPY", "FOLLOW")

# id: usado no rotulo do script, no nome da flag e no id do caso.
# nivel: o da fonte. O modo LV.5 de fabrica rebaixa sozinho (commit 0d18b35a80).
LENDARIOS = [
    dict(id="UXIE", especie="SPECIES_UXIE", nivel=50, mapa="AcuityCavern",
         mapa_const="MAP_ACUITY_CAVERN", warp=0,
         lar="acuity_cavern (o lar; existe aqui)",
         intro="Kyouuuun!",
         some="UXIE disappeared deep into its\\ncavern..."),
    dict(id="AZELF", especie="SPECIES_AZELF", nivel=50, mapa="ValorCavern",
         mapa_const="MAP_VALOR_CAVERN", warp=0,
         lar="valor_cavern (o lar; existe aqui)",
         intro="Kyuuun...",
         some="AZELF disappeared deep into\\nthe cavern..."),
    dict(id="MESPRIT", especie="SPECIES_MESPRIT", nivel=50, mapa="VerityCavern",
         mapa_const="MAP_VERITY_CAVERN", warp=0,
         lar="verity_cavern (o lar; existe aqui)",
         intro="Kyauun.",
         some="MESPRIT flew off somewhere..."),
    dict(id="ROTOM", especie="SPECIES_ROTOM", nivel=20,
         mapa="OldChateauBackMiddleWestRoom",
         mapa_const="MAP_OLD_CHATEAU_BACK_MIDDLE_WEST_ROOM", warp=0,
         lar="old_chateau_back_middle_west_room (o lar; existe aqui)",
         intro="Something inside the old room is\\nstaring back...",
         some="ROTOM disappeared into the TV set..."),
    dict(id="REGIGIGAS", especie="SPECIES_REGIGIGAS", nivel=1,
         mapa="SnowpointTempleB5F", mapa_const="MAP_SNOWPOINT_TEMPLE_B5F", warp=0,
         lar="snowpoint_temple_b5f (o lar; a trava dos tres titas caiu)",
         intro="...Zut zutt!",
         some="REGIGIGAS disappeared from view..."),
    dict(id="HEATRAN", especie="SPECIES_HEATRAN", nivel=50, mapa="MtCoronet_B1F",
         mapa_const="MAP_MT_CORONET_B1F", warp=0,
         lar="stark_mountain_room_3 (zona fora de escopo)",
         intro="A furnace heat wells up from the\\nbottom of the mountain...",
         some="HEATRAN sank back into the rock..."),
    dict(id="SHAYMIN", especie="SPECIES_SHAYMIN", nivel=30, mapa="FloaromaTown",
         mapa_const="MAP_FLOAROMA_TOWN", warp=0,
         lar="flower_paradise (nao existe aqui)",
         intro="Kyuu uuhn.",
         some="SHAYMIN disappeared among\\nthe flowers..."),
    dict(id="DARKRAI", especie="SPECIES_DARKRAI", nivel=50, mapa="CanalaveCity",
         mapa_const="MAP_CANALAVE_CITY", warp=10,
         lar="newmoon_island_forest (nao existe aqui)",
         intro="A shadow with no one to cast it\\nstands still by the harbor...",
         some="DARKRAI melted away into the\\ndarkness..."),
    dict(id="CRESSELIA", especie="SPECIES_CRESSELIA", nivel=50, mapa="CanalaveCity",
         mapa_const="MAP_CANALAVE_CITY", warp=10,
         lar="fullmoon_island_forest (nao existe aqui)",
         intro="A crescent glow drifts in from over\\nthe sea...",
         some="The Pokemon flew off somewhere..."),
    dict(id="ARCEUS", especie="SPECIES_ARCEUS", nivel=80, mapa="SpearPillar",
         mapa_const="MAP_SPEAR_PILLAR", warp=0,
         lar="hall_of_origin (nao existe aqui)",
         intro="Dodogyuuun!",
         some="ARCEUS disappeared from sight...",
         # O unico com portao: so aparece depois que Dialga E Palkia cairam.
         portao=("FLAG_CAUGHT_DIALGA", "FLAG_CAUGHT_PALKIA")),
]


# ------------------------------------------------------------------ geometria

def layouts():
    return {l["id"]: l for l in
            json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}


def grade(lid, tabela=None):
    l = (tabela or layouts())[lid]
    W, H = l["width"], l["height"]
    b = open(f"{RAIZ}/{l['blockdata_filepath']}", "rb").read()
    g = [[struct.unpack("<H", b[(y * W + x) * 2:(y * W + x) * 2 + 2])[0]
          for x in range(W)] for y in range(H)]
    return W, H, g


def anda(v):
    return ((v >> 10) & 3) == 0


def elev(v):
    return (v >> 12) & 0xF


def compat(e, eb):
    """Regra do motor: elevacao 0 e transicao e casa com tudo; 15 mantem a atual."""
    return e == 0 or eb in (0, 15) or e == eb


def passo(W, H, g, x, y, e, bloq):
    if not (0 <= x < W and 0 <= y < H) or (x, y) in bloq:
        return None
    v = g[y][x]
    if not anda(v):
        return None
    eb = elev(v)
    if not compat(e, eb):
        return None
    return e if eb == 15 else eb


def alcance(W, H, g, sementes, bloq=()):
    vistos, fila = set(), deque()
    for x, y in sementes:
        if anda(g[y][x]) and (x, y) not in bloq:
            st = (x, y, elev(g[y][x]))
            vistos.add(st)
            fila.append(st)
    while fila:
        x, y, e = fila.popleft()
        for dx, dy in DIRS.values():
            ne = passo(W, H, g, x + dx, y + dy, e, bloq)
            if ne is None:
                continue
            st = (x + dx, y + dy, ne)
            if st not in vistos:
                vistos.add(st)
                fila.append(st)
    return {(x, y) for x, y, _ in vistos}


def sementes_dos_warps(d, W, H, g):
    """Onde o jogador pousa entrando por cada warp: o tile, ou o vizinho andavel."""
    s = []
    for w in d.get("warp_events", []):
        x, y = w["x"], w["y"]
        if not (0 <= x < W and 0 <= y < H):
            continue
        if anda(g[y][x]):
            s.append((x, y))
            continue
        for dx, dy in DIRS.values():
            if passo(W, H, g, x + dx, y + dy, 0, ()) is not None:
                s.append((x + dx, y + dy))
    return s


def escorrega(W, H, g, bloq, x, y, e, D):
    """Escorrega ate travar. Devolve os tiles pisados, sem o de partida."""
    dx, dy = DIRS[D]
    c = []
    while True:
        ne = passo(W, H, g, x + dx, y + dy, e, bloq)
        if ne is None:
            break
        x, y, e = x + dx, y + dy, ne
        c.append((x, y, e))
    return c


# ------------------------------------------------------------------- escolha

def comportamento(d, x, y):
    """O comportamento do metatile embaixo de (x,y), pelo NOME do MB_."""
    lay = layouts()[d["layout"]]
    W = lay["width"]
    b = open(f"{RAIZ}/{lay['blockdata_filepath']}", "rb").read()
    mt = struct.unpack("<H", b[(y * W + x) * 2:(y * W + x) * 2 + 2])[0] & 0x3FF
    tab = ((V.tabela_de_atributos(lay.get("primary_tileset"))[0] or [])
           + (V.tabela_de_atributos(lay.get("secondary_tileset"))[0] or []))
    if mt >= len(tab):
        return None
    inv = {v: k for k, v in V.valores_dos_comportamentos().items()}
    return inv.get(tab[mt])


def contexto(nome, extra=()):
    d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json", encoding="utf-8"))
    W, H, g = grade(d["layout"])
    objs = {(o["x"], o["y"]) for o in d.get("object_events", [])
            if o.get("origem") != MARCA}
    objs |= set(extra)
    moveis = {(o["x"], o["y"]) for o in d.get("object_events", [])
              if any(k in o.get("movement_type", "") for k in MOVEIS)}
    warps = {(w["x"], w["y"]) for w in d.get("warp_events", [])}
    return d, W, H, g, objs, moveis, warps


def planeja(nome, warp_id, extra=(), longe=(), max_pernas=4):
    """Onde por o lendario, e a rota que o T123 anda ate ele.

    Devolve o melhor candidato como dict, ou None se o mapa nao der nenhum.
    Determinismo: a ordenacao nao empata (desempate por coordenada), entao rodar
    de novo devolve a MESMA escolha, que e o que faz o gerador ser idempotente.
    """
    d, W, H, g, objs, moveis, warps = contexto(nome, extra)
    w = d["warp_events"][warp_id]
    porta = (w["x"], w["y"])
    zerar = None
    if comportamento(d, *porta) in PORTAS:
        # Porta: o jogador acorda UM tile ao sul, ande ou nao o tile da porta.
        pouso = (porta[0], porta[1] + 1)
        if passo(W, H, g, pouso[0], pouso[1], 0, objs) is None:
            return None
    else:
        pouso = porta
    if anda(g[pouso[1]][pouso[0]]):
        inicio = (pouso[0], pouso[1], elev(g[pouso[1]][pouso[0]]))
        saida = None
        # Perna de ZERAR: um aperto contra parede fixa a direcao do boneco sem
        # andar, e a partir dai toda perna exata vale. Existe porque o warp de
        # debug nao promete para onde o jogador fica olhando, e caso que depende
        # disso nasce dependente de um detalhe que ninguem mediu.
        for D, (dx, dy) in DIRS.items():
            viz = (pouso[0] + dx, pouso[1] + dy)
            # NENHUM warp serve de parede, nem o de colisao 1. Medido em
            # 21/08/2026: a porta da Floaroma Town tem colisao 1 e o jogador
            # ENTRA nela mesmo assim (o motor trata comportamento de porta a
            # parte da colisao), entao a perna de zerar virava viagem para
            # dentro do Pokecenter. Onde nao houver parede de verdade, quem
            # fixa a direcao e a primeira perna saturante.
            if viz in warps:
                continue
            if passo(W, H, g, viz[0], viz[1], inicio[2], objs) is None:
                zerar = D
                break
        # Sem parede nenhuma em volta do pouso (o Spear Pillar e assim), a saida
        # e a PRIMEIRA PERNA SATURANTE: quem escorrega ate travar chega no mesmo
        # tile venha o boneco olhando para onde vier.
        saida = None if zerar else "*"
    else:
        return None

    sem = sementes_dos_warps(d, W, H, g)
    base = alcance(W, H, g, sem, objs)
    perto_warp = {(x + dx, y + dy) for x, y in warps
                  for dx in (-1, 0, 1) for dy in (-1, 0, 1)}

    def limpo(caminho):
        """A perna nao pode pisar em warp nem chegar perto de NPC que anda."""
        for x, y, _ in caminho:
            if (x, y) in warps:
                return False
            if any(max(abs(x - m[0]), abs(y - m[1])) <= 2 for m in moveis):
                return False
        return True

    # Nos alcancaveis por pernas retas. A PRIMEIRA perna e sempre saturante.
    raiz = inicio
    rotas = {raiz: []}
    fila = deque([(raiz, 0)])
    while fila:
        st, nivel = fila.popleft()
        if nivel >= max_pernas:
            continue
        for D in ("UP", "DOWN", "LEFT", "RIGHT"):
            if nivel == 0 and saida not in (None, "*") and D != saida:
                continue
            c = escorrega(W, H, g, objs, *st, D)
            if not c or not limpo(c):
                continue
            # Warp de porta (colisao 1): a PRIMEIRA perna tem que saturar, e so
            # assim os dois pousos possiveis (a porta e o tile de baixo) caem no
            # mesmo lugar. Com perna de zerar, perna exata ja vale desde a
            # primeira.
            passos = ([len(c)] if (nivel == 0 and saida is not None)
                      else range(1, len(c) + 1))
            for m in passos:
                fim = c[m - 1]
                if fim in rotas:
                    continue
                rotas[fim] = rotas[st] + [(D, m, m == len(c))]
                fila.append((fim, nivel + 1))

    cands = []
    for Q, rota in rotas.items():
        for D in ("UP", "DOWN", "LEFT", "RIGHT"):
            c = escorrega(W, H, g, objs, *Q, D)
            if len(c) < 3 or not limpo(c):
                continue
            for j in range(2, len(c)):
                T = (c[j - 1][0], c[j - 1][1])
                P = (c[j - 2][0], c[j - 2][1])
                R = (c[-1][0], c[-1][1])
                if T in perto_warp or T in objs or T not in base:
                    continue
                # Dois lendarios no mesmo mapa nao ficam colados: o segundo
                # viraria parede na rota do primeiro e os dois casos passariam
                # a depender um do outro sem dizer.
                if any(max(abs(T[0] - o[0]), abs(T[1] - o[1])) < 5 for o in longe):
                    continue
                cabeca = [(zerar, 0, False)] if zerar else []
                cands.append(dict(
                    T=T, para=P, vazio=R, dir=D, saturante=len(c),
                    rota=cabeca + rota + [(D, len(c), True)],
                    elev_T=c[j - 1][2], porta=porta, pouso=pouso, warp=warp_id,
                    andou=sum(n for _, n, _ in rota) + (j - 1)))
    if not cands:
        return None
    # ROTA CURTA primeiro, fundo depois. A ordem e deliberada: o Gui pediu
    # "nem que coloque em locais de facil acesso", e rota curta e o que mantem o
    # T123 barato e longe da familia de caso flaky. Entre duas rotas do mesmo
    # tamanho vale o tile mais longe do warp; empate se resolve por coordenada,
    # e por isso a escolha e ESTAVEL entre rodadas (o gerador e idempotente).
    cands.sort(key=lambda c: (len(c["rota"]), -c["andou"], c["T"]))
    # O portao caro (por o bicho ali nao pode ilhar ninguem) roda so no melhor
    # candidato, e desce a lista ate um passar. Rodar em todos custa minutos.
    for c in cands:
        if alcance(W, H, g, sem, objs | {c["T"]}) == base - {c["T"]}:
            return c
    return None


_PLANO = []


def plano():
    """A escolha de cada lendario, na ordem da tabela. Dois no mesmo mapa nao
    disputam tile: o segundo enxerga o primeiro como parede."""
    if _PLANO:
        return _PLANO
    usados = {}
    out = []
    for L in LENDARIOS:
        vizinhos = usados.get(L["mapa"], set())
        e = planeja(L["mapa"], L["warp"], extra=vizinhos, longe=vizinhos)
        if e is None:
            raise SystemExit(f"{L['id']}: nenhum tile passa nos portoes em "
                             f"{L['mapa']}. Nao invento mapa: pare e meca.")
        usados.setdefault(L["mapa"], set()).add(e["T"])
        out.append((L, e))
    _PLANO.extend(out)
    return out


# -------------------------------------------------------------------- escrita

def flag_de(L):
    return f"FLAG_HIDE_{L['id']}_SINNOH"


def flag_resolvido_de(L):
    """Segunda flag, so para quem tem PORTAO. Sem ela o portao ressuscita.

    Medido em 21/08/2026 pelo caso adversarial T123.25: a cabeca de portao roda
    a CADA transicao do mapa e apaga a HIDE sempre que os dois marcos estao
    feitos. Como capturar o Arceus tambem acende a MESMA HIDE, sair da sala e
    voltar apagava ela de novo e o lendario nascia outra vez, quantas vezes o
    jogador quisesse. Uma flag nao distingue "escondido porque o portao esta
    fechado" de "escondido porque o bicho ja foi", e por isso sao duas.
    """
    return f"FLAG_{L['id']}_SINNOH_RESOLVIDO" if L.get("portao") else None


def endereco_de(i):
    return FLAG_BASE + i


def localid_de(L):
    m = re.sub(r"(?<!^)(?=[A-Z])", "_", L["mapa"]).upper()
    return f"LOCALID_{re.sub('_+', '_', m)}_{L['id']}"


def objeto(L, e):
    return {
        "local_id": localid_de(L),
        "graphics_id": f"OBJ_EVENT_GFX_SPECIES({L['id']})",
        "x": e["T"][0],
        "y": e["T"][1],
        # ponytail: elevacao 0 de proposito, como o LUGIA e o HO-OH deste repo.
        # Objeto em elevacao 0 nunca da mismatch, entao ele SEMPRE barra o
        # jogador, que e do que o par positivo do T123 depende.
        "elevation": 0,
        "movement_type": "MOVEMENT_TYPE_FACE_DOWN",
        "movement_range_x": 0,
        "movement_range_y": 0,
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": f"{L['mapa']}_EventScript_{L['id'].title()}",
        "flag": flag_de(L),
        "origem": MARCA,
    }


def trecho(L):
    """O script do encontro. Sem gimmick: a Fase F esta congelada."""
    m, nome = L["mapa"], L["id"].title()
    lid, flag = localid_de(L), flag_de(L)
    fr = flag_resolvido_de(L)
    resolvido = [f"\tsetflag {fr}"] if fr else []
    p = [f"{m}_EventScript_{nome}::",
         "\tlockall",
         f"\tmsgbox {m}_Text_{nome}Intro, MSGBOX_DEFAULT",
         "\twaitse",
         f"\tplaymoncry {L['especie']}, CRY_MODE_ENCOUNTER",
         "\tdelay 30",
         "\twaitmoncry",
         f"\tseteventmon {L['especie']}, {L['nivel']}",
         "\tsetflag FLAG_SYS_CTRL_OBJ_DELETE",
         # ponytail: sem `waitstate` explicito. O macro `special` ja gera um
         # implicito para este special, e o segundo e IGNORADO pelo montador
         # (asm/macros/event.inc:322 avisa). O Lugia tem o de sobra e enche o
         # log de aviso; nao vale copiar defeito.
         "\tspecial BattleSetup_StartLegendaryBattle",
         "\tclearflag FLAG_SYS_CTRL_OBJ_DELETE",
         f"\tsetvar VAR_LAST_TALKED, {lid}",
         "\tspecialvar VAR_RESULT, GetBattleOutcome",
         f"\tcall_if_eq VAR_RESULT, B_OUTCOME_WON, {m}_EventScript_{nome}Some",
         f"\tcall_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, {m}_EventScript_{nome}Preso",
         "\treleaseall",
         "\tend",
         "",
         "@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou",
         "@ ser teleportado deixa ele no mapa, senao uma bola errada tira o",
         "@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.",
         f"{m}_EventScript_{nome}Preso::",
         "\tfadescreenswapbuffers FADE_TO_BLACK",
         f"\tremoveobject {lid}",
         f"\tsetflag {flag}",
         *resolvido,
         "\tfadescreenswapbuffers FADE_FROM_BLACK",
         "\treturn",
         "",
         f"{m}_EventScript_{nome}Some::",
         "\tfadescreenswapbuffers FADE_TO_BLACK",
         f"\tremoveobject {lid}",
         f"\tsetflag {flag}",
         *resolvido,
         "\tfadescreenswapbuffers FADE_FROM_BLACK",
         f"\tmsgbox {m}_Text_{nome}Some, MSGBOX_DEFAULT",
         "\treturn",
         "",
         f"{m}_Text_{nome}Intro:",
         '\t.string "%s$"' % L["intro"],
         "",
         f"{m}_Text_{nome}Some:",
         '\t.string "%s$"' % L["some"],
         ""]
    return "\n".join(p)


def cabeca_de_portao(m, portao, flag, resolvido):
    """ON_TRANSITION que acende a HIDE e so a apaga com os dois marcos feitos.

    Polaridade deliberada, a mesma de `cena_galactica_sinnoh.py`: ACENDE
    primeiro e apaga so no ramo bom, para que qualquer falha de leitura deixe o
    lendario AUSENTE, nunca plantado no mapa antes da hora.
    """
    a, b = portao
    return "\n".join([
        f"{m}_EventScript_PortaoLendario::",
        # Primeira linha, e nao a ultima: quem ja pegou o bicho sai daqui SEM
        # tocar na HIDE, que a captura deixou acesa e ninguem mais apaga.
        f"\tgoto_if_set {resolvido}, Common_EventScript_NopReturn",
        f"\tsetflag {flag}",
        f"\tgoto_if_unset {a}, Common_EventScript_NopReturn",
        f"\tgoto_if_unset {b}, Common_EventScript_NopReturn",
        f"\tclearflag {flag}",
        "\treturn",
        ""])


def substitui(texto, ini, fim, bloco):
    """Troca o bloco marcado, ou acrescenta no fim. Idempotente por construcao."""
    i = texto.find(ini)
    if i < 0:
        return texto if not bloco else texto.rstrip("\n") + "\n\n" + bloco
    j = texto.find(fim, i)
    j = len(texto) if j < 0 else j + len(fim) + 1
    return texto[:i] + bloco + texto[j:]


def liga_portao(inc, m):
    """Poe um `call` no ON_TRANSITION do mapa, criando a cabeca se faltar."""
    chamada = f"\tcall {m}_EventScript_PortaoLendario\n"
    if chamada in inc:
        return inc
    alvo = f"{m}_OnTransition"
    if re.search(rf"^{alvo}:", inc, re.M):
        return re.sub(rf"(^{alvo}:\n)", r"\1" + chamada, inc, count=1, flags=re.M)
    cab = f"{m}_MapScripts::"
    if f"map_script MAP_SCRIPT_ON_TRANSITION, {alvo}" not in inc:
        inc = inc.replace(
            cab + "\n", cab + f"\n\tmap_script MAP_SCRIPT_ON_TRANSITION, {alvo}\n", 1)
    return inc + f"\n{alvo}:\n{chamada}\tend\n"


def bloco_de_flags():
    out = [MARCA_INI,
           "// Uma flag de HIDE por lendario de Sinnoh, na CAUDA da maior faixa",
           "// livre (0x20D2-0x3230, medida por dev_scripts/flags_livres.py).",
           "// A cauda e de proposito: quem pede reserva pega a cabeca da faixa.",
           "// Apelidar FLAG_UNUSED nao mexe em FLAGS_COUNT: a save nao muda.",
           "// Gerado por dev_scripts/lendarios_sinnoh.py; nao editar a mao."]
    larg = max(len(flag_de(L)) for L in LENDARIOS) + 2
    for i, L in enumerate(LENDARIOS):
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // %s"
                   % (larg, flag_de(L), endereco_de(i), L["mapa"]))
    extra = len(LENDARIOS)
    for L in LENDARIOS:
        fr = flag_resolvido_de(L)
        if not fr:
            continue
        out.append("#define %-*s FLAG_UNUSED_0x%04X  // %s, ja pego: trava o portao"
                   % (larg, fr, endereco_de(extra), L["mapa"]))
        extra += 1
    out.append(MARCA_FIM)
    return "\n".join(out) + "\n"


def roteiro_de(e, com_a):
    """Os apertos do T123. Primeira perna saturante, as outras exatas +1."""
    p = ["60:NADA"]
    for i, (D, n, sat) in enumerate(e["rota"]):
        ult = i == len(e["rota"]) - 1
        toques = 2 if n == 0 else (n + 2 if sat else n + 1)
        p.append(f"16:{D}*{toques}")
        p.append("90:NADA" if ult else "40:NADA")
    if com_a:
        p += ["16:A", "180:NADA",
              f"16:{OPOSTO[e['dir']]}*8", "150:NADA"]
    return ",".join(p)


def casos_de(L, e, i):
    flags_base = ["FLAG_SEM_ENCONTRO_SELVAGEM"]
    portao = list(L.get("portao", ()))
    pos = dict(mapa=L["mapa_const"], pos=list(e["para"]))
    neg = dict(mapa=L["mapa_const"], pos=list(e["vazio"]), andou=True)
    rota = " ".join(f"{D}*{n}" if n else f"{D}(zera)" for D, n, _ in e["rota"])
    a = dict(
        id=f"T123.{2 * i + 1}",
        nome=(
            f"{L['id']} EXISTE EM {L['mapa_const']} E A INTERACAO TRAVA O JOGADOR. "
            f"Ate 21/08/2026 este Pokemon nao tinha objeto nem script em mapa "
            f"nenhum desta ROM (medido por grep de {L['especie']} em "
            f"data/maps/*/map.json e scripts.inc). Lar na fonte: {L['lar']}. "
            f"O tile {tuple(e['T'])} saiu de busca em largura sobre o map.bin, com "
            f"colisao E elevacao, e passou pelo portao de que por o bicho ali nao "
            f"ilha nenhum tile do mapa. ROTA: {rota}, a partir do warp "
            f"{e['warp']} ({e['porta'][0]},{e['porta'][1]}), pousando em "
            f"{tuple(e['pouso'])} (warp de comportamento de porta pousa UM tile ao "
            f"sul; de escada pousa no proprio tile). A perna que ZERA e um aperto "
            f"contra parede: fixa a direcao do boneco sem andar, entao para onde o "
            f"warp deixa ele olhando nao muda o resultado (onde nao ha parede em "
            f"volta do pouso, quem faz esse servico e a primeira perna, saturante); "
            f"as outras levam UM aperto a mais porque a primeira tecla de uma "
            f"direcao nova so VIRA o boneco (T121.1). A ultima perna satura CONTRA "
            f"o lendario e para em {tuple(e['para'])}: essa parada ja e meia prova, "
            f"porque o tile atras dele esta livre e sem o bicho a perna iria mais "
            f"longe (e o que o par negativo mede). O A abre o msgbox de abertura, "
            f"que comeca com lockall, e por isso o "
            f"{OPOSTO[e['dir']]}*8 seguinte NAO move o jogador. O harness nao le a "
            f"tela de batalha: por isso o script tem msgbox ANTES do cry, e a "
            f"prova para na caixa de texto, sem entrar na batalha."),
        flags=flags_base + portao,
        warp=L["mapa_const"], warp_id=e["warp"],
        roteiro=roteiro_de(e, True), prova=pos)
    if L.get("portao"):
        b_flags = flags_base
        b_nome = (
            f"PAR NEGATIVO DO T123.{2 * i + 1}, e o portao do {L['id']}. MESMA rota ate o "
            f"lendario (o positivo so acrescenta o A e a perna de volta), SEM as flags {' e '.join(portao)}: o lendario nao "
            f"nasce, o tile {tuple(e['T'])} fica vazio e a mesma perna final "
            f"escorrega ate {tuple(e['vazio'])}. Sem este caso o positivo passaria "
            f"num jogo em que o {L['id']} esta plantado no mapa desde o primeiro "
            f"minuto, que e exatamente o defeito que o portao existe para evitar. "
            f"O `andou` prova que o jogo continua respondendo.")
    else:
        b_flags = flags_base + [flag_de(L)]
        b_nome = (
            f"PAR NEGATIVO DO T123.{2 * i + 1}: com {flag_de(L)} ACESA o tile "
            f"{tuple(e['T'])} esta VAZIO. MESMA rota ate o lendario (o positivo so "
            f"acrescenta o A e a perna de volta), e a perna final escorrega ate {tuple(e['vazio'])} em vez de parar em "
            f"{tuple(e['para'])}. Sem ele o positivo nao prova nada: parada de "
            f"jogador tem muitas causas (parede, elevacao, mapa que nao carregou), "
            f"e a diferenca entre os dois casos e exatamente UMA flag. E tambem a "
            f"prova de que a flag de HIDE escrita no campo `flag` do object_event e "
            f"a mesma que o script acende ao vencer ou capturar.")
    b = dict(id=f"T123.{2 * i + 2}", nome=b_nome, flags=b_flags,
             warp=L["mapa_const"], warp_id=e["warp"],
             roteiro=roteiro_de(e, False), prova=neg)
    return [a, b]


def aplica(gravar):
    mudou = []
    por_mapa = {}
    for L, e in plano():
        por_mapa.setdefault(L["mapa"], []).append((L, e))
    for mapa, itens in por_mapa.items():
        cam = f"{RAIZ}/data/maps/{mapa}/map.json"
        d = json.load(open(cam, encoding="utf-8"))
        # Tira TUDO que e deste gerador antes de repor. Filtrar por `local_id`
        # deixava orfao quando o nome do local_id mudava, e em 21/08/2026 isso
        # plantou DOIS Heatran no mesmo tile do Mt. Coronet B1F sem nenhum teste
        # ficar vermelho, porque o de cima ja barrava o jogador. `origem` e a
        # unica chave que nao envelhece.
        antes = d.get("object_events", [])
        novos = [o for o in antes if o.get("origem") != MARCA]
        novos += [objeto(L, e) for L, e in itens]
        if novos == antes:
            continue
        d["object_events"] = novos
        if gravar:
            open(cam, "w", encoding="utf-8").write(
                json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        for L, e in itens:
            mudou.append(f"{mapa}: {L['id']} em {e['T']} (flag {flag_de(L)})")

    for L, _e in plano():
        cam = f"{RAIZ}/data/maps/{L['mapa']}/scripts.inc"
        inc = open(cam, encoding="utf-8").read()
        meus = [x for x in LENDARIOS if x["mapa"] == L["mapa"]]
        corpo = [INC_INI]
        for x in meus:
            if x.get("portao"):
                corpo.append(cabeca_de_portao(x["mapa"], x["portao"], flag_de(x),
                                          flag_resolvido_de(x)))
            corpo.append(trecho(x))
        corpo.append(INC_FIM)
        novo = substitui(inc, INC_INI, INC_FIM, "\n".join(corpo) + "\n")
        for x in meus:
            if x.get("portao"):
                novo = liga_portao(novo, x["mapa"])
        if novo != inc:
            if gravar:
                open(cam, "w", encoding="utf-8").write(novo)
            mudou.append(f"{L['mapa']}/scripts.inc: encontro escrito")

    fl = open(FLAGS_H, encoding="utf-8").read()
    novo = substitui(fl, MARCA_INI, MARCA_FIM, bloco_de_flags())
    if novo != fl:
        if gravar:
            open(FLAGS_H, "w", encoding="utf-8").write(novo)
        mudou.append(f"flags.h: {len(LENDARIOS)} apelidos de HIDE")

    casos = [c for i, (L, e) in enumerate(plano()) for c in casos_de(L, e, i)]
    antigo = json.load(open(CASOS, encoding="utf-8")) if os.path.exists(CASOS) else None
    if antigo != casos:
        if gravar:
            open(CASOS, "w", encoding="utf-8").write(
                json.dumps(casos, indent=2, ensure_ascii=False) + "\n")
        mudou.append(f"testes_criticos/123_lendarios_sinnoh.json: {len(casos)} casos")
    return mudou


# ------------------------------------------------------------------ autoteste

def demo():
    """Cada assert abaixo morre se uma REGRA sumir, nunca por numero decorado."""
    falhas = []
    p = plano()

    # 1. Nenhum lendario repetido, e nenhum ja vivo em outro mapa da ROM.
    ids = [L["id"] for L, _ in p]
    assert len(ids) == len(set(ids)), ids
    for L, _ in p:
        achou = []
        for raiz, _dirs, arqs in os.walk(f"{RAIZ}/data/maps"):
            for a in arqs:
                if a not in ("map.json", "scripts.inc"):
                    continue
                t = open(os.path.join(raiz, a), encoding="utf-8", errors="replace").read()
                if re.search(rf"{L['especie']}\b", t) and MARCA not in t \
                        and f"_EventScript_{L['id'].title()}" not in t:
                    achou.append(os.path.join(raiz, a))
        assert not achou, f"{L['id']} ja existe fora deste gerador: {achou}"

    # 2. Uma flag por lendario, todas distintas, todas FLAG_UNUSED sem apelido
    #    de outro dono. Flag dobrada e cena que apaga a cena do vizinho.
    fl = open(FLAGS_H, encoding="utf-8").read()
    ends = [endereco_de(i) for i in range(len(LENDARIOS))]
    assert len(set(ends)) == len(ends)
    for i, L in enumerate(LENDARIOS):
        nome = f"FLAG_UNUSED_0x{endereco_de(i):04X}"
        assert f"#define {nome} " in fl, f"{nome} nao existe no pool"
        donos = re.findall(rf"^#define (FLAG_\w+)\s+{nome}\s*(?://.*)?$", fl, re.M)
        assert donos in ([], [flag_de(L)]), f"{nome} ja tem dono: {donos}"

    # 3. Todo lendario nasce COM flag no campo `flag`. Objeto de cena sem flag e
    #    parede permanente, que e a regra do PRD.
    for L, e in p:
        o = objeto(L, e)
        assert o["flag"] not in ("0", "0x0", ""), L["id"]
        assert o["script"].startswith(L["mapa"]), L["id"]

    # 4. O tile escolhido NAO pode ilhar ninguem. Este e o portao caro, e ele
    #    fica no demo porque a alternativa e descobrir isso no emulador.
    for L, e in p:
        d, W, H, g, objs, _m, _w = contexto(L["mapa"])
        sem = sementes_dos_warps(d, W, H, g)
        base = alcance(W, H, g, sem, objs)
        assert e["T"] in base, f"{L['id']}: tile nao e alcancavel"
        assert alcance(W, H, g, sem, objs | {e['T']}) == base - {e["T"]}, \
            f"{L['id']}: por o bicho em {e['T']} ilha tile"

    # 5. O par negativo tem que PARAR EM OUTRO LUGAR. Se `para` e `vazio` forem
    #    iguais, os dois casos passam com a flag fazendo nada, que e falso
    #    positivo, e falso positivo e pior que validador nenhum (licao 4.3).
    for L, e in p:
        assert e["para"] != e["vazio"], L["id"]
        assert e["T"] not in (e["para"], e["vazio"]), L["id"]

    # 6. Idempotencia de TEXTO: rodar os substituidores em cima da propria saida
    #    tem que devolver o mesmo texto, e a cabeca de portao nao pode duplicar.
    falso = "Foo_MapScripts::\n\t.byte 0\n"
    uma = liga_portao(falso, "Foo")
    assert liga_portao(uma, "Foo") == uma, "liga_portao nao e idempotente"
    assert uma.count("map_script MAP_SCRIPT_ON_TRANSITION") == 1, uma
    um = substitui("abc\n", INC_INI, INC_FIM, INC_INI + "\nX\n" + INC_FIM + "\n")
    assert substitui(um, INC_INI, INC_FIM, INC_INI + "\nX\n" + INC_FIM + "\n") == um

    # 7. MUTACAO PLANTADA: empurrar o lendario para cima de uma parede tem que
    #    ser PEGO. Sem isto o demo so mede o que o gerador ja acertou.
    L, e = p[0]
    d, W, H, g, objs, _m, _w = contexto(L["mapa"])
    parede = next(((x, y) for y in range(H) for x in range(W) if not anda(g[y][x])), None)
    assert parede is not None
    sem = sementes_dos_warps(d, W, H, g)
    assert parede not in alcance(W, H, g, sem, objs), \
        "mutacao plantada nao mutou nada: a parede escolhida e andavel"

    # 8. MUTACAO PLANTADA numero 2: se a rota perder a perna saturante inicial,
    #    o roteiro tem que mudar. E ela que absorve a direcao do boneco depois
    #    do warp, e caso escrito sem ela nasce dependente de um detalhe que
    #    ninguem mediu.
    e2 = dict(e, rota=[(D, n, False) for D, n, _ in e["rota"]])
    assert roteiro_de(e2, True) != roteiro_de(e, True), \
        "roteiro_de nao distingue perna saturante de perna exata"
    # E a perna de zerar tem que valer 2 apertos e nenhum passo.
    assert roteiro_de(dict(e, rota=[("UP", 0, False)]), False).count("UP*2") == 1

    # 8b. NENHUM mapa pode terminar com dois objetos deste gerador no MESMO
    #     tile, nem com objeto orfao de rodada antiga. Este assert nasceu de um
    #     defeito de verdade: em 21/08/2026 o Mt. Coronet B1F ficou com DOIS
    #     Heatran em (5,60), e a suite inteira continuou verde, porque o de
    #     cima ja barrava o jogador. Prova de posicao nao enxerga objeto dobrado.
    for mapa in {L["mapa"] for L, _ in p}:
        d = json.load(open(f"{RAIZ}/data/maps/{mapa}/map.json", encoding="utf-8"))
        meus = [o for o in d.get("object_events", []) if o.get("origem") == MARCA]
        esperado = [L["id"] for L, _ in p if L["mapa"] == mapa]
        assert len(meus) <= len(esperado), \
            f"{mapa}: {len(meus)} objetos do gerador para {len(esperado)} lendarios"
        tiles = [(o["x"], o["y"]) for o in meus]
        assert len(tiles) == len(set(tiles)), f"{mapa}: dois objetos no mesmo tile"

    # 9. Todo caso tem prova, e prova nao vazia; e o par negativo nunca repete a
    #    prova do positivo.
    casos = [c for i, (L, e) in enumerate(p) for c in casos_de(L, e, i)]
    ids_c = [c["id"] for c in casos]
    assert len(ids_c) == len(set(ids_c)), ids_c
    for c in casos:
        assert c.get("prova"), c["id"]
    for a, b in zip(casos[::2], casos[1::2]):
        assert a["prova"] != b["prova"], (a["id"], b["id"])

    print("plano:")
    for L, e in p:
        print(f"  {L['id']:10} {L['mapa']:30} T={e['T']} para={e['para']} "
              f"vazio={e['vazio']} dir={e['dir']} pernas={len(e['rota'])}")
    print("demo: %s" % ("OK" if not falhas else "REPROVADO"))
    return 1 if falhas else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--aplica", action="store_true")
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    if a.demo:
        raise SystemExit(demo())
    for linha in aplica(a.aplica):
        print(("grava " if a.aplica else "faria ") + linha)


if __name__ == "__main__":
    main()
