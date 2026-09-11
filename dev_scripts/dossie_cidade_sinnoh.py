#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Escreve o dossiê do JOGO de uma cidade de Sinnoh copiada do Retro Platinum.

Uso:
    python3 dev_scripts/dossie_cidade_sinnoh.py --cidade TwinleafTown \
        --saida dev_scripts/dossies_sinnoh --imagem /private/tmp/.../dossies
    python3 dev_scripts/dossie_cidade_sinnoh.py --cidade OreburghCity --opcao 2

O QUE ESTE ARQUIVO É
--------------------
O contrato `Pokemon Claude/METODO-COPIA-CIDADES.md`, seção 2, manda que numa
cópia com REMAPEAMENTO cada prédio nosso seja casado com o prédio equivalente
do hack pela FUNÇÃO do script, que o warp nosso vá para a porta dele, que o NPC
nosso vá para o lugar equivalente e que tudo continue alcançável a pé. Este
script é quem escreve esse plano, célula a célula, num JSON que o executor
seguinte aplica sem ter de adivinhar nada.

Ele NÃO edita map.json, nem map.bin, nem tileset. Só mede e planeja.

O QUE FOI MEDIDO ANTES DE ESCREVER ISTO (11/09/2026, não presumir de novo)
-------------------------------------------------------------------------
1. **As portas do hack TÊM comportamento.** O dossiê de Jubilife afirmava que
   "nenhum metatile deles tem comportamento de porta". É falso: as portas do
   Retro Platinum usam `MB_NON_ANIMATED_DOOR` (0x60 = 96), e o censo bate com
   os warps deles em todas as cidades. O que falta é a ANIMAÇÃO: o nosso motor
   quer `MB_ANIMATED_DOOR` para a porta abrir. Ou seja, o trabalho da execução é
   PROMOVER 96 para porta animada nos metatiles certos, não inventar
   comportamento do zero.
2. **O resto do atributo é mesmo quase todo zero.** Fora as portas, só aparecem
   escada lateral (73 a 79), água (16, 21) e seta de warp (98 a 101). Não há
   grama alta, não há placa, não há pulo. O censo por cidade está no dossiê.
3. **A moldura decorativa do hack tem colisão 0** e a busca em largura vaza por
   cima dela. Medido: Floaroma alcança as 1.656 células livres (o mapa inteiro,
   água e floresta) e Oreburgh sul alcança 2.287 de 2.296. Twinleaf e Sandgem
   NÃO vazam: a busca crua para nas saídas de verdade. Por isso a moldura é
   declarada cidade a cidade, e o dossiê traz os dois números.
4. **A água entra na colisão.** Lago e mar têm colisão 0; a prova de alcance a
   pé exclui os comportamentos de água e conta a superfície de Surf à parte.
5. **Offsets de conexão.** A convenção do motor é `x_do_vizinho = x_nosso -
   offset` (e o mesmo em y para leste/oeste). Conferido nos quatro mapas de
   hoje, que batem tile a tile com o corredor das rotas.
"""
import argparse
import json
import os
import re
import struct
import sys
from collections import Counter, deque

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE_PADRAO = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/romhacks/retro-platinum/fonte"

# Comportamentos de água: a prova de alcance a pé não passa por eles.
MB_AGUA = set(range(16, 44))
MB_PORTA_FONTE = 96          # MB_NON_ANIMATED_DOOR
MB_SETA_WARP = {98, 99, 100, 101}


# ------------------------------------------------------------------ leitura --

def le_layouts(raiz):
    with open(os.path.join(raiz, "data/layouts/layouts.json"), encoding="utf-8") as f:
        return json.load(f)["layouts"]


def layout_por(raiz, chave, campo):
    for l in le_layouts(raiz):
        if l.get(campo) == chave:
            return l
    raise KeyError("%s=%s em %s" % (campo, chave, raiz))


def pasta_tileset(raiz, simbolo):
    nome = re.sub(r"^gTileset_", "", simbolo)
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", nome).lower()
    for sub in ("data/tilesets/primary/", "data/tilesets/secondary/"):
        p = os.path.join(raiz, sub + snake)
        if os.path.isdir(p):
            return p
    raise KeyError(simbolo)


def le_u16(caminho):
    with open(caminho, "rb") as f:
        dados = f.read()
    return struct.unpack("<%dH" % (len(dados) // 2), dados)


def atributos(raiz, layout):
    """metatile global -> comportamento (attr & 0xFF). Vale para os dois repos."""
    saida = {}
    for simbolo, base in ((layout["primary_tileset"], 0), (layout["secondary_tileset"], 512)):
        caminho = os.path.join(pasta_tileset(raiz, simbolo), "metatile_attributes.bin")
        for i, a in enumerate(le_u16(caminho)):
            saida[base + i] = a & 0xFF
    return saida


class Mapa(object):
    """Um mapa já montado: pode ser um layout inteiro ou a colagem de vários.

    ATENÇÃO: quando a colagem junta mapas de SECUNDÁRIOS diferentes (é o caso de
    Oreburgh: norte usa gTileset_OreburghNorth e sul gTileset_OreburghSouth), o
    mesmo número de metatile acima de 511 quer dizer coisas diferentes em cada
    metade. Por isso o mapa guarda de qual PARTE cada célula veio, e o
    comportamento é lido na tabela daquela parte. A execução vai ter de
    renumerar o secundário; este dossiê só não pode mentir enquanto mede.
    """

    def __init__(self, largura, altura, blocos, attrs, parte=None):
        self.w, self.h, self.v, self.attrs = largura, altura, blocos, attrs
        self.parte = parte if parte is not None else [0] * (largura * altura)

    def mid(self, x, y):
        return self.v[y * self.w + x] & 0x3FF

    def col(self, x, y):
        return (self.v[y * self.w + x] >> 10) & 3

    def elev(self, x, y):
        return (self.v[y * self.w + x] >> 12) & 0xF

    def beh(self, x, y):
        tab = self.attrs[self.parte[y * self.w + x]]
        return tab.get(self.mid(x, y), 0)

    def dentro(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h


def monta(raiz_fonte, partes, preenchimento):
    """Cola pedaços de mapas da fonte num mapa único.

    `partes`: lista de dicts com mapa, recorte (sx, sy, sw, sh) e destino (dx, dy).
    Devolve (Mapa, largura, altura). O que nenhuma parte cobre recebe
    `preenchimento` (um metatile de moldura DELES, nunca desenho inventado).
    """
    w = max(p["dx"] + p["sw"] for p in partes)
    h = max(p["dy"] + p["sh"] for p in partes)
    v = [preenchimento] * (w * h)
    dono = [0] * (w * h)
    attrs = []
    for k, p in enumerate(partes):
        lay = layout_por(raiz_fonte, p["mapa"] + "_Layout", "name")
        sw, sh = lay["width"], lay["height"]
        src = le_u16(os.path.join(raiz_fonte, lay["blockdata_filepath"]))
        attrs.append(atributos(raiz_fonte, lay))
        for j in range(p["sh"]):
            for i in range(p["sw"]):
                sx, sy = p["sx"] + i, p["sy"] + j
                if not (0 <= sx < sw and 0 <= sy < sh):
                    continue
                v[(p["dy"] + j) * w + (p["dx"] + i)] = src[sy * sw + sx]
                dono[(p["dy"] + j) * w + (p["dx"] + i)] = k
    return Mapa(w, h, v, attrs, dono), w, h


# ------------------------------------------------------------------- alcance --

def busca(mapa, origem, livre):
    vis = {origem}
    fila = deque([origem])
    while fila:
        x, y = fila.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in vis and mapa.dentro(*n) and livre(*n):
                vis.add(n)
                fila.append(n)
    return vis


def corridas(celulas):
    saida = []
    for c in celulas:
        if saida and (c[0] - saida[-1][-1][0]) + (c[1] - saida[-1][-1][1]) == 1:
            saida[-1].append(c)
        else:
            saida.append([c])
    return [[list(r[0]), list(r[-1])] for r in saida]


# ------------------------------------------------------- plano de uma cidade --

class Plano(object):
    def __init__(self, cfg, raiz_fonte, raiz_nosso):
        self.cfg = cfg
        self.fonte = raiz_fonte
        self.raiz = raiz_nosso
        self.mapa, self.W, self.H = monta(raiz_fonte, cfg["partes"], cfg.get("preenchimento", 0))
        self.moldura = set(cfg.get("moldura", ()))
        self.extra_bloqueado = {tuple(c) for c in cfg.get("bloqueia_celulas", ())}
        self.extra_livre = {tuple(c) for c in cfg.get("libera_celulas", ())}
        self.nosso = json.load(open(os.path.join(raiz_nosso, "data/maps/%s/map.json" % cfg["nosso_mapa"]), encoding="utf-8"))
        self.lay_nosso = layout_por(raiz_nosso, cfg["nosso_layout"], "id")

    # -- regras de andar --------------------------------------------------
    def livre_cru(self, x, y):
        return self.mapa.col(x, y) == 0

    def livre(self, x, y):
        if (x, y) in self.extra_livre:
            return True
        if (x, y) in self.extra_bloqueado:
            return False
        if self.mapa.mid(x, y) in self.moldura and self.mapa.mid(x, y) < 512:
            return False
        if self.mapa.beh(x, y) in MB_AGUA:
            return False
        return self.mapa.col(x, y) == 0

    def livre_sem_moldura(self, x, y):
        if (x, y) in self.extra_livre:
            return True
        if (x, y) in self.extra_bloqueado:
            return False
        return self.mapa.col(x, y) == 0 and self.mapa.beh(x, y) not in MB_AGUA

    def agua(self, x, y):
        return self.mapa.col(x, y) == 0 and self.mapa.beh(x, y) in MB_AGUA

    # -- transposição ------------------------------------------------------
    def ancoras(self):
        anc = []
        for w in self.cfg["warps"]:
            if not w.get("novo") or w.get("casa") == "ENCAIXADO":
                continue
            nw = self.nosso["warp_events"][w["id"]]
            # warps empilhados na mesma porta não viram âncora duas vezes
            par = ((nw["x"], nw["y"]), tuple(w["novo"]))
            if par not in anc:
                anc.append(par)
        return anc

    def transpoe(self, p, anc, delta):
        cands = sorted((abs(p[0] - a[0]) + abs(p[1] - a[1]), a, b) for a, b in anc)
        if not cands or cands[0][0] > self.cfg.get("raio_ancora", 12):
            return (p[0] + delta[0], p[1] + delta[1]), "delta global (%+d,%+d)" % delta
        d, a, b = cands[0]
        return (p[0] + b[0] - a[0], p[1] + b[1] - a[1]), \
               "âncora %s->%s (delta %+d,%+d)" % (list(a), list(b), b[0] - a[0], b[1] - a[1])

    def perto(self, alvo, vis, ocupadas=()):
        if alvo in vis and alvo not in ocupadas:
            return alvo, 0
        melhor = None
        for c in vis:
            if c in ocupadas:
                continue
            d = abs(c[0] - alvo[0]) + abs(c[1] - alvo[1])
            if melhor is None or d < melhor[0]:
                melhor = (d, c)
        return (melhor[1], melhor[0]) if melhor else (alvo, -1)

    def encosta(self, p, vis, ocupadas=()):
        """Placa quer tile BLOQUEANTE com chão alcançável do lado, para ser lida de frente."""
        def serve(c):
            return (self.mapa.dentro(*c) and c not in ocupadas and not self.livre(*c)
                    and any((c[0] + a, c[1] + b) in vis for a, b in ((0, 1), (0, -1), (1, 0), (-1, 0))))
        if serve(p):
            return p, ""
        melhor = None
        for r in range(1, 10):
            for dy in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    c = (p[0] + dx, p[1] + dy)
                    if not serve(c):
                        continue
                    d = abs(dx) + abs(dy)
                    if melhor is None or d < melhor[0]:
                        melhor = (d, c)
            if melhor:
                break
        if not melhor:
            return p, "; ATENÇÃO: nenhum tile bloqueante alcançável por perto"
        return melhor[1], "; empurrada %d tile(s) para o tile bloqueante vizinho, para ser lida de frente" % melhor[0]

    # -- censos ------------------------------------------------------------
    def censo_comportamento(self):
        c = Counter()
        for y in range(self.H):
            for x in range(self.W):
                c[self.mapa.beh(x, y)] += 1
        nomes = mb_nomes(os.path.join(self.raiz, "include/constants/metatile_behaviors.h"))
        detalhe = {}
        for b, n in sorted(c.items()):
            if b == 0:
                continue
            detalhe["%d (%s)" % (b, nomes[b] if b < len(nomes) else "?")] = n
        return {
            "celulas": self.W * self.H,
            "MB_NORMAL_zerado": c[0],
            "com_comportamento_de_verdade": self.W * self.H - c[0],
            "por_comportamento": detalhe,
        }

    def portas_da_fonte(self):
        return [(x, y) for y in range(self.H) for x in range(self.W)
                if self.mapa.beh(x, y) == MB_PORTA_FONTE]


def mb_nomes(caminho):
    corpo = open(caminho, encoding="utf-8").read().split("enum {", 1)[1].split("};", 1)[0]
    nomes = []
    for linha in corpo.splitlines():
        linha = linha.split("//")[0].strip().rstrip(",").strip()
        if linha.startswith("MB_"):
            nomes.append(linha)
    return nomes


# ------------------------------------------------------------ configuração --
# Cada cidade traz: como a planta deles é montada, para onde vai cada warp
# nosso, quais prédios são encaixados, o que fazer com porta deles sem dono, as
# conexões com o offset recalculado e os riscos que eu não consegui fechar.

CIDADES = {}

BARREIRA_TWINLEAF = (
    "barreira do rival na entrada norte: o corredor deles tem 4 tiles (x=10..13) contra 8 do nosso, "
    "então os 7 gatilhos cobrem o corredor inteiro em DUAS linhas (y=1 e y=2) em vez de uma, e o "
    "jogador não tem por onde passar sem disparar")

CIDADES["TwinleafTown"] = {
    "nosso_mapa": "TwinleafTown",
    "nosso_layout": "LAYOUT_TWINLEAF_TOWN",
    "partes": [dict(mapa="TwinleafTown", sx=0, sy=0, sw=22, sh=34, dx=0, dy=0)],
    "preenchimento": 0,
    "origem": (16, 24),
    "moldura": [],
    "tamanho_porque": (
        "a planta deles (22x34) entra inteira, sem recorte nem esticamento. A nossa é 24x30: "
        "duas colunas a menos e quatro linhas a mais. As quatro linhas extras são o lago do sul, "
        "que na nossa planta de hoje não existe; as duas colunas que somem são margem de mata sem "
        "nada dentro. O mapLayoutId não muda"),
    "warps": [
        dict(id=0, predio="Casa do jogador (MAIN_HOUSE)", novo=(16, 23),
             casa="[16,23] porta da Players House deles", porque="casa do jogador com casa do jogador"),
        dict(id=1, predio="Casa do rival (RIVALS_HOUSE)", novo=(5, 13),
             casa="[5,13] porta da Rivals House deles", porque="casa do rival com casa do rival"),
        dict(id=2, predio="Casa 1 (HAOUSE1)", novo=(6, 23),
             casa="[6,23] porta da House A deles", porque="casa com casa, mesmo canto sudoeste"),
        dict(id=3, predio="Casa 2 (HOUSE2)", novo=(16, 13),
             casa="[16,13] porta da House B deles", porque="casa com casa, mesmo canto nordeste"),
    ],
    "perto_de": {0: "frente da casa do jogador", 1: "praça central, ao norte",
                 2: "calçada da casa 2 (nordeste)", 3: "caminho do sudoeste",
                 4: "porta da casa do rival (contraparte escondida)", 5: "entrada norte",
                 6: "rua do meio, a oeste", 7: "rua do sul", 8: "rua do norte",
                 9: "caminho a oeste da casa do rival"},
    "coord_fixo": {i: (xy, BARREIRA_TWINLEAF) for i, xy in enumerate(
        [[10, 1], [11, 1], [12, 1], [13, 1], [10, 2], [11, 2], [12, 2]])},
    "bg_fixo": {
        0: ([12, 15], "placa da cidade na placa de cidade DELES, no cruzamento central (12,15)"),
        1: ([14, 23], "a nossa segunda placa do cruzamento vai para o poste que eles desenharam em "
                      "frente à casa do jogador, (14,23): as duas não cabem na mesma célula, e esse é "
                      "o único outro poste de placa da planta deles que ainda não tem dono"),
    },
    "conexoes": [
        dict(direcao="up", mapa="MAP_ROUTE201", existe=True, offset_hoje=-4, offset=-4,
             onde="já existe: x=10..13 na linha 0 (4 tiles); hoje a nossa é x=8..15 (8 tiles)",
             conta=("x_da_rota = x_nosso - offset. Route201 tem o corredor de baixo em x=14..17. "
                    "Com offset -4, o corredor novo x=10..13 cai em 14..17 da rota, tile a tile. "
                    "O offset NÃO muda; o que muda é a largura, de 8 para 4")),
        dict(direcao="down", mapa="MAP_ROUTE220", existe=True, offset_hoje=0, offset=0,
             onde="já existe: x=8..15 na linha 33, mas é ÁGUA (o lago deles encosta na borda de baixo)",
             conta=("Route220 é mar: a borda de cima dela é livre em x=0..3, 6..18 e 21..61. Com offset 0, "
                    "o lago deles (x=8..15) cai em 8..15 da rota, que é água livre. A conexão continua "
                    "no mesmo offset; o que muda é que ela deixa de ser só cosmética (ver riscos)")),
    ],
    "encaixes": [],
    "riscos": [
        ("As quatro portas casam uma a uma, sem encaixe e sem porta órfã: a planta deles é a mesma "
         "ideia da nossa (quatro casas em cruz), só maior. Esta é a cidade mais barata das quatro"),
        ("A nossa Route220 hoje é conexão CÓSMETICA: a borda de baixo do nosso mapa não tem uma só "
         "célula andável nem de água. A planta deles encosta o lago na linha 33, então depois da cópia "
         "o jogador com Surf passa do lago de Twinleaf para o mar da Route220. É passagem NOVA. Se o "
         "condutor não quiser, basta pôr colisão 1 na linha y=33 do lago (8 células) e a conexão volta "
         "a ser só desenho"),
        ("A prova de alcance vale para o desenho DELES como está. Se a execução mexer na colisão para "
         "encaixar prédio ou abrir saída, a prova tem de ser refeita: o script é este mesmo, "
         "dev_scripts/dossie_cidade_sinnoh.py"),
        ("A coluna x=21 da planta deles é grama andável com a mata desenhada só na metade direita do "
         "tile: o jogador encosta na borda leste em y=6..29. Não é vazamento de colisão, é a margem do "
         "mapa deles mesmo, e não há conexão leste para desenhar nada ali. O border.bin deles é que "
         "aparece. Fica como está"),
        ("Os 7 gatilhos do rival na entrada norte foram REDESENHADOS, não transpostos: hoje eles são "
         "uma linha de 7 em y=2 cobrindo um corredor de 8 tiles, e o corredor deles tem 4. Virei duas "
         "linhas, de 4 e de 3, em y=1 e y=2. É decisão minha, não cópia: se o condutor quiser "
         "fidelidade ao nosso arranjo de hoje, os 7 ficam numa linha só e o jogador escapa pelas "
         "laterais do corredor"),
        ("A nossa segunda placa do cruzamento (bg 1) foi para o poste que eles desenharam em frente à "
         "casa do jogador. Se o texto dela falar do cruzamento ou apontar direção, tem de ser revisto"),
        ("O item escondido (bg 2) foi transposto para chão andável, não para tile bloqueante: item "
         "escondido fica SOB o chão, e a regra da placa não vale para ele"),
        ("Este dossiê é o plano do JOGO. A conversão de tileset (metatile de três camadas do hack "
         "achatado para duas, de-para do primário, empacotamento do secundário, escolha de paleta) NÃO "
         "está aqui: é o outro braço da frente, dev_scripts/copia_cidade_fonte.py"),
        ("As portas deles têm MB_NON_ANIMATED_DOOR (96), não comportamento zerado como o dossiê de "
         "Jubilife afirmava. A execução tem de PROMOVER esses metatiles a MB_ANIMATED_DOOR no tileset "
         "novo, senão a porta não anima; e tem de dar comportamento de placa às células de placa, que "
         "no hack são MB_NORMAL"),
    ],
}

CIDADES["SandgemTown"] = {
    "nosso_mapa": "SandgemTown",
    "nosso_layout": "LAYOUT_SANDGEM_TOWN",
    "partes": [dict(mapa="SandgemTown", sx=0, sy=0, sw=34, sh=34, dx=0, dy=0)],
    "preenchimento": 0,
    "origem": (19, 13),
    "moldura": [],
    "tamanho_porque": (
        "a planta deles (34x34) entra inteira. A nossa é 34x32: mesma largura, duas linhas a mais, "
        "que é a faixa de praia do sul. O mapLayoutId não muda"),
    "warps": [
        dict(id=0, predio="Laboratório do Rowan", novo=(10, 12),
             casa="[10,12] porta do Professor Rowan's Lab deles", porque="laboratório com laboratório"),
        dict(id=1, predio="Centro Pokémon", novo=(19, 12),
             casa="[19,12] porta do Centro Pokémon deles", porque="Centro com Centro"),
        dict(id=2, predio="Loja", novo=(29, 12), casa="[29,12] porta da Loja deles",
             porque="Loja com Loja"),
        dict(id=3, predio="Casa 1 (HOUSE1)", novo=(9, 24), casa="[9,24] porta da House A deles",
             porque="casa com casa, mesmo bloco sudoeste"),
        dict(id=4, predio="Casa do rival (RIVAL_HOUSE)", novo=(18, 24),
             casa="[18,24] porta da Helper House deles",
             porque="casa do rival com a casa que o hack usa para o mesmo papel, mesmo bloco sul-centro"),
    ],
    "perto_de": {0: "frente do Centro Pokémon (Professor)", 1: "porta da casa do rival",
                 2: "frente do laboratório (contraparte escondida)", 3: "praia a sudeste",
                 4: "rua a oeste, ao sul do laboratório", 5: "rua do sul, a leste",
                 6: "avenida central, a leste", 7: "praia do sul", 8: "rua a oeste do Centro",
                 9: "avenida central"},
    "bg_fixo": {
        0: ([24, 24], "placa da cidade na placa de cidade DELES, na praça do sul"),
        1: ([7, 13], "a nossa placa do laboratório vai para a placa de laboratório DELES"),
        2: ([16, 24], "a placa importada que hoje fica ao lado da casa do rival vai para a placa da "
                      "casa do rival DELES"),
        4: ([22, 12], "a nossa placa do Centro vai para a placa de Centro Pokémon DELES"),
        5: ([27, 12], "a nossa placa da Loja vai para a placa de Loja DELES"),
    },
    "conexoes": [
        dict(direcao="up", mapa="MAP_ROUTE202", existe=True, offset_hoje=2, offset=4,
             onde="já existe: x=22..31 na linha 0 (10 tiles); hoje a nossa é x=20..29 (10 tiles)",
             conta=("x_da_rota = x_nosso - offset. Hoje 20..29 - 2 = 18..27, e o corredor da Route202 "
                    "é x=22..27, encostado na ponta direita. O corredor deles anda 2 para a direita "
                    "(22..31), então o offset anda 2 também: 2 + 2 = 4, e 22..31 - 4 = 18..27, a mesma "
                    "relação de hoje")),
        dict(direcao="down", mapa="MAP_ROUTE219", existe=True, offset_hoje=-2, offset=2,
             onde="já existe: x=22..31 na linha 33 (10 tiles); hoje a nossa é x=20..25 (6 tiles)",
             conta=("hoje 20..25 - (-2) = 22..27, que é exatamente o corredor da Route219. O corredor "
                    "deles é 10 de largura (22..31); centrando os 6 tiles da rota no meio dele, "
                    "x_da_rota 22..27 tem de cair em x_nosso 24..29, logo offset = 24 - 22 = 2")),
        dict(direcao="left", mapa="MAP_ROUTE201", existe=True, offset_hoje=6, offset=10,
             onde="já existe: y=12..17 na coluna 0 (6 tiles); hoje a nossa é y=9..13 (5 tiles)",
             conta=("y_da_rota = y_nosso - offset. Hoje 9..13 - 6 = 3..7, e o corredor direito da "
                    "Route201 é y=2..7. O corredor deles desce 3 (12..17): 12 - 2 = 10. Confere com o "
                    "que o próprio hack usa na Sandgem dele, que também é 10")),
    ],
    "encaixes": [],
    "riscos": [
        ("As cinco portas casam uma a uma. Sandgem é cópia direta de planta, com remapeamento só de "
         "NPC e placa"),
        ("A saída sul deles é 10 tiles (x=22..31) contra 6 nossos: depois da cópia o jogador pode "
         "descer para a Route219 por 4 tiles a mais. Do lado da rota, 4 desses tiles caem em terreno "
         "bloqueado, então vira beco sem saída visível. Se o condutor quiser a largura de hoje, é pôr "
         "colisão 1 em x=22..25 na linha 33"),
        ("A saída oeste deles é 6 tiles contra 5 nossos, e a leste da Route201 só tem 6 livres "
         "(y=2..7): com offset 10 os 6 casam exato, sem beco"),
        ("CINCO das nossas oito placas foram para os postes de placa DELES, casadas por função (cidade "
         "com cidade, laboratório com laboratório, Centro com Centro, Loja com Loja, casa do rival com "
         "casa do rival). As outras três (bg 3, 6 e 7) foram transpostas e empurradas para o tile "
         "bloqueante mais perto, o que pode deixá-las numa parede lisa, sem poste desenhado. Quem "
         "aplicar tem de olhar o render e, se ficar feio, desenhar o poste ou mover a placa"),
        ("A nossa Sandgem tem uma faixa de praia a mais no sul (duas linhas) e dois NPCs que vivem "
         "nela, o Youngster (índice 3) e o Fisherman (índice 7). A planta deles tem praia no mesmo "
         "canto sudeste, e os dois caíram lá; mas se o texto deles citar o mar, conferir que dá para "
         "ver o mar do lugar novo"),
        ("Os 6 gatilhos da contraparte (CounterpartLeadToLab) formam hoje uma barreira em L a oeste do "
         "laboratório. Transpostos, viram (5,14..16), (6,17) e (8,18..19). A forma do L muda um pouco "
         "porque a rua deles é mais larga; a cena tem applymovement e tem de ser conferida rodando"),
        ("Este dossiê é o plano do JOGO. A conversão de tileset (metatile de três camadas do hack "
         "achatado para duas, de-para do primário, empacotamento do secundário, escolha de paleta) NÃO "
         "está aqui: é o outro braço da frente, dev_scripts/copia_cidade_fonte.py"),
        ("As portas deles têm MB_NON_ANIMATED_DOOR (96), não comportamento zerado como o dossiê de "
         "Jubilife afirmava. A execução tem de PROMOVER esses metatiles a MB_ANIMATED_DOOR no tileset "
         "novo, senão a porta não anima; e tem de dar comportamento de placa às células de placa, que "
         "no hack são MB_NORMAL"),
    ],
}

CIDADES["FloaromaTown"] = {
    "nosso_mapa": "FloaromaTown",
    "nosso_layout": "LAYOUT_FLOAROMA_TOWN",
    "partes": [dict(mapa="FloaromaTown", sx=0, sy=0, sw=34, sh=38, dx=0, dy=0)],
    "preenchimento": 0,
    "origem": (18, 33),
    "moldura": [5, 6, 13, 14, 31, 58],
    "tamanho_porque": (
        "34x38: a planta deles é 42x44 e entra até a borda de saída DELES. As 8 colunas x=34..41 e as "
        "6 linhas y=38..43 ficam de fora porque estão ALÉM das saídas do próprio hack: a Floaroma "
        "deles não usa conexão, usa seta de warp, e as setas estão em x=33 (y=25..28, para a "
        "Route205) e em y=37 (x=10 e 12..14, para a Route204). Cortando ali, a borda do nosso mapa "
        "cai exatamente onde o autor terminou a cidade, e os nossos dois corredores de conexão ficam "
        "tile a tile onde estão hoje, só descidos 4 linhas. O que sobra fora do corte é horta de "
        "berry e mata que, no nosso mundo, é Route 205 e Route 204"),
    "warps": [
        dict(id=0, predio="Centro Pokémon", novo=(18, 32), casa="[18,32] porta do Centro deles",
             porque="Centro com Centro"),
        dict(id=1, predio="Casa 2 (HOUSE2)", novo=(26, 32), casa="[26,32] porta da House B deles",
             porque="casa com casa, mesmo bloco sudeste"),
        dict(id=2, predio="Casa 1 (HOUSE1)", novo=(13, 20), casa="[13,20] porta da House A deles",
             porque="casa com casa, mesmo bloco central-oeste"),
        dict(id=3, predio="Floricultura (FLOWER_SHOP)", novo=(22, 16), casa="ENCAIXADO",
             porque=("a floricultura deles está desenhada em (20..24, 12..16), com o toldo listrado em "
                     "(21..23, 16), mas o hack NÃO pôs warp nela. A porta é aberta no centro do toldo, "
                     "(22,16), que já é célula andável")),
        dict(id=4, predio="Loja", novo=(26, 23), casa="[26,23] porta da Loja deles",
             porque="Loja com Loja"),
        dict(id=5, predio="Prado (MEADOW), porta esquerda", novo=(4, 6),
             casa="[4,6] porta esquerda do portão do Floaroma Meadow deles", porque="prado com prado"),
        dict(id=6, predio="Prado (MEADOW), porta direita", novo=(5, 6),
             casa="[5,6] porta direita do portão do Floaroma Meadow deles", porque="idem"),
    ],
    "perto_de": {0: "campo de flor a leste, onde os Galácticos param", 1: "praça em frente ao Centro",
                 2: "campo de flor a oeste", 3: "rua central, ao norte do Centro",
                 4: "campo de flor a oeste, ao sul", 5: "praça a leste da Loja",
                 6: "campo de flor a oeste, no meio", 7: "ao lado do outro Galáctico",
                 8: "canto sudoeste (Shaymin)", 9: "caminho do norte, perto do prado",
                 10: "campo de flor do norte", 11: "campo de flor do noroeste",
                 12: "praça do sul (Shaymin da Dex)", 13: "canteiro de berry a oeste da praça",
                 14: "canteiro de berry a leste da praça"},
    "bg_fixo": {
        0: ([15, 25], "placa da cidade na placa de cidade DELES, no meio da rua"),
    },
    "conexoes": [
        dict(direcao="down", mapa="MAP_ROUTE204", existe=True, offset_hoje=2, offset=2,
             onde=("já existe: x=10 e x=12..14 na linha 37 (as próprias células de seta de warp deles). "
                   "Hoje a nossa saída é x=10 e x=12..14 na linha 35: MESMAS colunas"),
             conta=("x_da_rota = x_nosso - 2. As colunas não mudam (o delta da transposição é (0,+4), "
                    "só em y), então 10 e 12..14 continuam caindo em 8 e 10..12 da Route204, que são "
                    "os corredores dela. Offset inalterado")),
        dict(direcao="right", mapa="MAP_ROUTE205_SOUTH", existe=True, offset_hoje=-64, offset=-60,
             onde=("já existe: y=25..28 na coluna 33 (as células de seta de warp deles). Hoje a nossa é "
                   "y=21..24 na coluna 33: MESMA coluna, 4 linhas acima"),
             conta=("y_da_rota = y_nosso - offset. Hoje 21..24 + 64 = 85..88, que é exatamente o "
                    "corredor esquerdo da Route205_South. O corredor desce 4 linhas, então o offset "
                    "sobe 4: -64 + 4 = -60, e 25..28 + 60 = 85..88 de novo")),
    ],
    "encaixes": [
        dict(predio="Floricultura (MAP_FLOAROMA_TOWN_FLOWER_SHOP, warp 3)", xy=[22, 16],
             fachada=("a própria floricultura deles, em (20..24, 12..16): o hack desenhou o prédio "
                      "inteiro, com telhado, vitrine e toldo listrado, e só esqueceu o warp"),
             muda=("nada muda na rua: (22,16) já é andável e fica no centro do toldo. O que a execução "
                   "faz é dar a esse metatile comportamento de porta animada e pôr o warp 3 nele. As "
                   "células (21,16) e (23,16), as outras duas do toldo, continuam andáveis")),
    ],
    "riscos": [
        ("O corte em 34x38 é a decisão mais discutível deste dossiê. Tirar as 8 colunas e as 6 linhas "
         "de fora das saídas deles é o que faz os dois corredores de conexão caírem tile a tile onde "
         "estão hoje. A alternativa (42x44 inteiro) obriga a pôr a conexão leste na coluna 41, que na "
         "planta deles é o fim de um canteiro de areia fechado, no meio do rio: a costura com a "
         "Route205 sairia dentro d'água"),
        ("As células de seta de warp deles (comportamento 98 a 101) ficam nas nossas duas bordas de "
         "conexão: x=33 em y=25..28 e y=37 em x=10 e 12..14. Se o comportamento vier copiado, o jogador "
         "é teleportado para o mapa errado ao encostar na borda. A execução TEM de zerar esses "
         "comportamentos (9 células, metatiles 94, 102, 110, 118, 64 e 535)"),
        ("A moldura deles (metatiles 5, 6, 13, 14 do primário e 31 e 58, o vazio) tem colisão 0 e a "
         "busca em largura crua anda por cima dela: sem tapar, alcança o mapa inteiro. Os números "
         "estão na prova de alcance"),
        ("A floricultura sem warp é a leitura mais arriscada: eu li o prédio de (20..24, 12..16) como "
         "a floricultura porque é o único prédio da cidade deles sem porta, fica onde a nossa "
         "floricultura fica e tem toldo de loja. Se o condutor achar que é outra coisa, o warp 3 "
         "precisa de outra fachada"),
        ("Os dois NPCs Galácticos (índices 0 e 7) e o Shaymin (8) e o Shaymin da Dex (12) têm flag de "
         "esconder; a posição nova deles foi transposta pela âncora mais próxima, mas a cena dos "
         "Galácticos tem applymovement, e as distâncias da cena têm de ser conferidas rodando"),
        ("As duas árvores de berry (índices 13 e 14) são object_events com script BerryTreeScript: "
         "elas guardam estado por ID de árvore. Mover a posição não mexe no ID, mas se a célula nova "
         "não for chão de terra o desenho fica estranho"),
        ("A planta deles tem DUAS placas que ficam sem dono, e placa sem dono não é o mesmo problema "
         "que porta sem dono: a placa da loja em (19,17) e a placa do prado em (31,20). Não há regra "
         "de closed para placa; ou a execução apaga o poste do desenho, ou sobra poste mudo. "
         "Recomendo deixar o poste e não pôr script: o jogador não interage com o que não tem "
         "bg_event"),
        ("Este dossiê é o plano do JOGO. A conversão de tileset (metatile de três camadas do hack "
         "achatado para duas, de-para do primário, empacotamento do secundário, escolha de paleta) NÃO "
         "está aqui: é o outro braço da frente, dev_scripts/copia_cidade_fonte.py"),
        ("As portas deles têm MB_NON_ANIMATED_DOOR (96), não comportamento zerado como o dossiê de "
         "Jubilife afirmava. A execução tem de PROMOVER esses metatiles a MB_ANIMATED_DOOR no tileset "
         "novo, senão a porta não anima; e tem de dar comportamento de placa às células de placa, que "
         "no hack são MB_NORMAL"),
    ],
}


# --- Oreburgh: a cidade deles são DOIS mapas e a nossa é UM -------------------
# A costura deles: OreburghCityNorth liga para baixo com offset 14, ou seja o
# mapa sul entra em x = 14 do norte. Como o sul tem 58 de largura e 14+58 = 72 =
# a largura do norte, os dois empilhados dão um retângulo exato de 72 x 76.
# O que decide entre as opções NÃO é a geometria, é o tileset: medido tile a
# tile (imagem 8x8 já com a paleta aplicada, deduplicada por espelho), os dois
# mapas inteiros mais a costura pedem 1.111 tiles para 1.024 vagas.

OREBURGH_PARTES_INTEIRO = [
    dict(mapa="OreburghCityNorth", sx=0, sy=0, sw=72, sh=32, dx=0, dy=0),
    dict(mapa="OreburghCitySouth", sx=0, sy=0, sw=58, sh=44, dx=14, dy=32),
]

OREBURGH_OPCOES = [
    dict(numero=1, nome="Os dois mapas inteiros, empilhados",
         tamanho="72x76", partes=OREBURGH_PARTES_INTEIRO,
         tiles=1111, cabe=False,
         portas_casadas=15, encaixes=1, portas_deles_sem_dono=2,
         perde="nada do desenho deles",
         custo=("NÃO CABE: 1.111 tiles para as 1.024 vagas do par de tilesets (512 do primário novo "
                "mais 512 do secundário novo). Faltam 87 tiles, 8,5%. Só entra se 87 tiles quase "
                "iguais forem fundidos por cor aproximada, com o erro medido e mostrado")),
    dict(numero=2, nome="Os dois inteiros, menos a pilha de carvão gigante do pátio",
         tamanho="72x76", partes=OREBURGH_PARTES_INTEIRO,
         tiles=955, cabe=True,
         portas_casadas=15, encaixes=1, portas_deles_sem_dono=2,
         perde=("a pilha de carvão preta do pátio da mina, em (27..36, 4..11) do mapa sul deles "
                "(=(41..50, 36..43) no mapa fundido). No lugar dela entra a rocha de moldura DELES, "
                "que já está no tileset. Nenhum prédio, nenhuma rua e nenhuma porta se perde"),
         custo=("CABE com folga: 955 de 1.024, sobram 69 vagas. A pilha de carvão sozinha custa 156 "
                "tiles exclusivos, de longe a peça mais cara do sul, porque é desenho orgânico sem "
                "repetição")),
    dict(numero=3, nome="Os dois inteiros, menos a pilha de carvão e menos a fábrica branca",
         tamanho="72x76", partes=OREBURGH_PARTES_INTEIRO,
         tiles=878, cabe=True,
         portas_casadas=15, encaixes=1, portas_deles_sem_dono=2,
         perde=("a pilha de carvão mais a fábrica branca de (44..57, 0..9) do sul (=(58..71, 32..41) "
                "no fundido). A casa C (nosso warp 10) fica na quina da fábrica: tirando a fábrica, a "
                "casa C tem de ser encaixada"),
         custo="CABE com muita folga: 878 de 1.024, sobram 146 vagas"),
    dict(numero=4, nome="Norte inteiro, e do sul só da linha 8 para baixo",
         tamanho="72x68", partes=[OREBURGH_PARTES_INTEIRO[0],
                                  dict(mapa="OreburghCitySouth", sx=0, sy=8, sw=58, sh=36, dx=14, dy=32)],
         tiles=989, cabe=True,
         portas_casadas=15, encaixes=1, portas_deles_sem_dono=2,
         perde=("as 8 primeiras linhas do pátio deles, que é justamente por onde a estrada do norte "
                "DESCE para o pátio (a passagem norte-sul está em x=51..55 do fundido, linhas 32 a 39). "
                "Cortar ali SEVERA a ligação entre as duas metades e obriga a redesenhar a descida"),
         custo="CABE: 989 de 1.024, sobram 35 vagas"),
    dict(numero=5, nome="Só o mapa norte deles; a metade sul continua com a nossa arte de hoje",
         tamanho="72x59", partes=[OREBURGH_PARTES_INTEIRO[0]],
         tiles=865, cabe=True,
         portas_casadas=10, encaixes=6, portas_deles_sem_dono=1,
         perde=("o pátio da mina inteiro deles. A mina (nossos warps 11 a 14) e a casa 3 (warp 10) "
                "voltam a ser a nossa arte, que é exatamente a arte pobre que o refino queria "
                "consertar"),
         custo="CABE: 865 de 1.024, sobram 159 vagas"),
]

CIDADES["OreburghCity"] = {
    "nosso_mapa": "OreburghCity",
    "nosso_layout": "LAYOUT_OREBURGH_CITY",
    "partes": OREBURGH_PARTES_INTEIRO,
    "preenchimento": 14,   # rocha de moldura do gTileset_OutdoorOreburgh deles
    "origem": (54, 24),
    "moldura": [],
    "opcoes": OREBURGH_OPCOES,
    "recomendo": 2,
    "tamanho_porque": (
        "72x76. A conexão do hack diz que o mapa sul entra em x=14 do mapa norte; como o sul tem 58 "
        "de largura e 14 + 58 = 72, que é a largura do norte, os dois empilhados fecham um retângulo "
        "exato, sem sobra nem falta. As 14 colunas x=0..13 das linhas 32 a 75, que nenhum dos dois "
        "mapas cobre, recebem a rocha de moldura DELES (metatile 14 do gTileset_OutdoorOreburgh), o "
        "mesmo desenho que o próprio sul usa no canto sudoeste. O mapLayoutId não muda"),
    "warps": [
        dict(id=0, predio="Portão da Oreburgh Gate", novo=(9, 14),
             casa="[9,14] entrada do Oreburgh Gate deles", porque="portão com portão"),
        dict(id=1, predio="Condomínio 1 (FLAT1)", novo=(22, 13),
             casa="[22,13] porta da Tower A deles", porque="condomínio com condomínio, mesmo bloco norte"),
        dict(id=2, predio="Condomínio 2 (FLAT2)", novo=(29, 13),
             casa="[29,13] porta da Tower B deles", porque="condomínio com condomínio, o do lado"),
        dict(id=3, predio="Loja", novo=(36, 13), casa="[36,13] porta da Loja deles",
             porque="Loja com Loja"),
        dict(id=4, predio="Museu (LILYCOVE_MUSEUM)", novo=(56, 13),
             casa="[56,13] porta da rotativa do Museu de Mineração deles",
             porque=("museu com museu: é a entrada principal, a cúpula giratória, e é a que corresponde "
                     "ao nosso pórtico de colunas em (54,14)")),
        dict(id=5, predio="Casa 2 (HOUSE2)", novo=(24, 23), casa="[24,23] porta da House A deles",
             porque="casa com casa, mesmo bloco central"),
        dict(id=6, predio="Ginásio", novo=(33, 23), casa="[33,23] porta do Ginásio deles",
             porque="ginásio com ginásio"),
        dict(id=7, predio="Casa 1 (HOUSE1)", novo=(44, 19), casa="[44,19] porta da House B deles",
             porque="casa com casa, mesmo bloco leste"),
        dict(id=8, predio="Centro Pokémon", novo=(54, 23), casa="[54,23] porta do Centro deles",
             porque="Centro com Centro"),
        dict(id=9, predio="Condomínio 3 (FLAT3)", novo=(63, 30), casa="[63,30] porta da Tower C deles",
             porque="condomínio com condomínio, mesmo canto sudeste do mapa norte"),
        dict(id=10, predio="Casa 3 (HOUSE3)", novo=(58, 41),
             casa="[58,41] porta da House C deles (mapa sul, (44,9))",
             porque="casa com casa: é a única casa do pátio da mina, dos dois lados"),
        dict(id=11, predio="Mina (MINE_B1F), boca 1", novo=(52, 64),
             casa="[52,64] boca da Oreburgh Mine deles (mapa sul, (38,32))",
             porque="mina com mina"),
        dict(id=12, predio="Mina (MINE_B1F), boca 2", novo=(53, 64),
             casa="[53,64] boca da mina deles (mapa sul, (39,32))", porque="mina com mina"),
        dict(id=13, predio="Mina (MINE_B1F), boca 3", novo=(54, 64),
             casa="[54,64] boca da mina deles (mapa sul, (40,32))", porque="mina com mina"),
        dict(id=14, predio="Mina (MINE_B1F), boca 4", novo=(55, 64),
             casa="[55,64] boca da mina deles (mapa sul, (41,32))", porque="mina com mina"),
        dict(id=15, predio="Museu de Mineração (MINING_MUSEUM)", novo=(59, 13), casa="ENCAIXADO",
             porque=("o museu deles tem UMA porta só e ela já é do warp 4. O nosso segundo museu vira "
                     "uma porta nova na base da ala direita do mesmo prédio, em (62,16), emprestando o "
                     "metatile de porta da própria rotativa")),
    ],
    "perto_de": {0: "praça do ginásio (rival)", 1: "pátio da mina (operário)",
                 2: "rua a leste, ao sul do condomínio 3", 3: "frente do Centro Pokémon",
                 4: "avenida do norte, perto da Loja", 5: "rua a leste, no meio",
                 6: "frente do portão (oeste)", 7: "rua a oeste, ao sul", 8: "pátio da mina, a leste",
                 9: "avenida do norte, a leste da Loja", 10: "descida para o pátio",
                 11: "rua a leste, perto do condomínio 3", 12: "calçada dos condomínios do norte",
                 13: "rua central, ao lado da casa 1", 14: "pátio da mina (Machop)",
                 15: "descida para o pátio (Machop)", 16: "pátio da mina (Machop)",
                 17: "rua do museu", 18: "frente do portão (contraparte escondida)",
                 19: "bola de item, pátio de cima", 20: "bola de item, rua do meio",
                 21: "calçada dos condomínios do norte", 22: "pátio da mina (Machop)"},
    "bg_fixo": {
        0: ([51, 4], "placa da cidade na placa que eles puseram na entrada norte, (51,4)"),
        1: ([29, 23], "placa do ginásio na placa de ginásio DELES: por acaso é a MESMA coordenada que "
                      "a nossa de hoje, (29,23)"),
        2: ([11, 12], "a nossa placa do portão vai para a outra placa de cidade DELES, (11,12), que "
                      "fica em frente à Oreburgh Gate"),
        4: ([52, 15], "a nossa placa do museu vai para a placa de museu DELES, (52,15)"),
        5: ([52, 60], "a nossa placa da mina vai para a placa de mina DELES (mapa sul, (38,28))"),
    },
    "bg_alvo": {
        7: ([50, 62], "esta placa HOJE está morta: no nosso mapa ela fica em (12,58), célula bloqueada "
                      "e sem uma só vizinha alcançável. Em vez de copiar o defeito, vai para a boca da "
                      "mina, onde dá para ler"),
        8: ([57, 62], "mesma coisa da placa 7: hoje em (0,58), morta no campo de rocha. Vai para o "
                      "pátio da mina, do lado leste"),
    },
    "conexoes": [
        dict(direcao="up", mapa="MAP_ROUTE207", existe=True, offset_hoje=35, offset=39,
             onde="já existe: x=48..53 na linha 0 (6 tiles); hoje a nossa é x=44..50 (7 tiles)",
             conta=("x_da_rota = x_nosso - offset. Hoje 44..50 - 35 = 9..15, que é o corredor de baixo "
                    "da Route207 tile a tile. O corredor deles anda 4 para a direita (48..53), então "
                    "48 - 9 = 39. O próprio hack usa 39 na Oreburgh dele, o que confirma a conta")),
    ],
    "encaixes": [
        dict(predio="Museu de Mineração (MAP_MINING_MUSEUM, warp 15)", xy=[59, 13],
             fachada=("a ala DIREITA do próprio museu deles: a parede de frente do museu é a linha 13, "
                      "em x=52..60, e a porta da rotativa do warp 4 fica em (56,13). A ala direita, "
                      "x=58..60, repete tile a tile a ala esquerda (metatiles 685/693/701 nas janelas e "
                      "607 na base), então a porta nova em (59,13) fica no centro dela, simétrica à "
                      "outra. O metatile de porta emprestado é o 722, o da própria rotativa"),
             muda=("nada na rua: a calçada em frente, (58..60, 14), já é andável e alcançável, e é por "
                   "onde o jogador entra nas duas portas. O que muda é uma célula da parede, (59,13), "
                   "que deixa de ser alvenaria cega e vira porta. NÃO usar (62,16), que parece porta no "
                   "render mas é um bolsão fechado dentro do prédio: (62..63, 15..18) tem colisão 0 "
                   "cercado por colisão 1 nos quatro lados, é área que o autor deixou solta e a busca "
                   "em largura não alcança")),
    ],
    "portas_deles_sem_dono_extra": [
        dict(xy=[51, 64], descricao=("a quinta boca da mina deles (mapa sul, (37,32)): o hack pôs CINCO "
                                     "células de warp na boca e nós temos QUATRO warps de mina"),
             tratamento=("duas saídas honestas, e quem escolhe é o Gui: (a) placa closed em (51,64) e a "
                         "célula fica bloqueante, deixando a boca com 4 de largura em vez de 5, ou (b) "
                         "um warp NOVO de id 16, acrescentado no FIM da lista (o que a regra de save "
                         "permite), apontando para o mesmo MAP_OREBURGH_MINE_B1F warp 0 do nosso warp "
                         "11. Recomendo (b): mantém a boca da mina com a largura que o autor desenhou")),
        dict(xy=[8, 14], descricao=("célula de porta órfã do portão deles: (8,14) tem comportamento de "
                                    "porta e colisão 1, do lado de dentro da própria Oreburgh Gate, e o "
                                    "warp deles está em (9,14), que é seta de warp para oeste"),
             tratamento=("nada a fazer: é o batente do portão, não é porta de prédio. O nosso warp 0 vai "
                         "para (9,14), a célula que o hack usa de verdade. (8,14) fica bloqueante e sem "
                         "placa")),
    ],
    "riscos": [
        ("A escolha da fusão é do Gui, não minha: a opção 1 (os dois mapas inteiros) é a única 100% "
         "fiel e é a única que NÃO cabe no tileset. As outras quatro trocam pedaço de desenho deles "
         "por espaço de tileset. Este dossiê está escrito sobre a opção 2, que é a que eu recomendo, "
         "mas o plano de warp, NPC e placa é idêntico nas opções 1, 2 e 3, porque nenhuma delas mexe "
         "em rua nem em porta"),
        ("A medida de tileset que o condutor tinha (1.441 tiles para 944 vagas) estava inflada. "
         "Remedindo por IMAGEM de tile 8x8 já com a paleta aplicada, e deduplicando por espelho, o "
         "norte pede 658, o sul 584 e a união 1.051, porque os dois compartilham o primário "
         "gTileset_OutdoorOreburgh. A costura (faixa de 8 tiles da nossa borda norte, o border.bin e "
         "a faixa de baixo da Route207) pede 60, não 194. Total de 1.111 para 1.024"),
        ("A passagem entre as duas metades é ESTREITA e só existe em x=51..55: a linha 31 do norte é "
         "livre em x=31, 38, 51..55 e 57..65, e a linha 0 do sul (linha 32 do fundido) é livre em "
         "x=14..30, 32..36, 40..49, 51..55 e 67..71. O único trecho em que as duas listas se cruzam é "
         "51..55. Todo o resto da emenda é rocha contra rocha dos dois lados, que é o certo"),
        ("Os nossos DOIS museus (warps 4 e 15) contra UM museu deles é o único lugar da cidade em que "
         "o hack não tem prédio para o que a gente tem. O encaixe usa a ala direita do mesmo prédio; "
         "se o condutor achar que os dois museus deviam ser prédios diferentes, o warp 15 precisa de "
         "outra fachada, e a candidata é o prédio escuro de (61..64, 11..16)"),
        ("As nossas 16 portas viram 15 casadas e 1 encaixe, mas a nossa Oreburgh de hoje JÁ é uma "
         "leitura da planta deles (todas as portas do norte batem com um deslocamento quase constante "
         "de +3 a +5 em x). Isso é boa notícia e por isso mesmo é suspeita: significa que quem montou "
         "a nossa já tinha a planta do Platinum na frente, e que a cópia é um refinamento do desenho, "
         "não uma mudança de cidade"),
        ("A pilha de carvão da opção 2 é a peça que eu escolhi sacrificar porque é a mais cara em "
         "tile por metro quadrado. Ela é, porém, um marco visual do pátio. Se o Gui achar que a pilha "
         "importa mais que 87 tiles, a saída é a opção 1 com fusão de cor aproximada"),
        ("SEIS object_events da nossa Oreburgh estão INALCANÇÁVEIS hoje, medido com busca em largura "
         "a partir do Centro Pokémon: os índices 2, 10, 16, 18, 19 e 22 (a Battle Girl, três Machop, "
         "a contraparte do rival e uma bola de item). No plano novo os 23 ficam alcançáveis. Isso é "
         "melhora, não regressão, mas é mudança de comportamento: a bola de item 19 passa a ser "
         "pegável, e a contraparte 18 passa a ser vista. Vale avisar quem cuida do roteiro"),
        ("As placas 7 e 8 (Placa18 e PlacaImportada) também estão MORTAS hoje, em (12,58) e (0,58): "
         "célula bloqueada, sem uma só vizinha alcançável. Levei as duas para o pátio da mina em vez "
         "de copiar o defeito"),
        ("A moldura de rocha deles tem colisão 0 em quase todo o campo morto do sul: medido no mapa "
         "sul SOZINHO, a busca crua alcança 2.287 das 2.296 células livres. No mapa FUNDIDO isso deixa "
         "de acontecer, porque a entrada do pátio vem de cima, pela estrada, e o campo morto fica do "
         "lado de fora da parede: a busca alcança 1.371 de 4.835. Ou seja, o vazamento era do ponto de "
         "partida, não do mapa"),
        ("As 14 colunas x=0..13 das linhas 32 a 75 não vêm de mapa nenhum deles e recebem o metatile "
         "14 do primário OutdoorOreburgh, a rocha de moldura que o próprio sul usa. São 616 células. "
         "É o único lugar dos quatro dossiês em que se escreve desenho que não está num mapa da fonte, "
         "e mesmo assim é um metatile DELES, repetido, sem composição nova"),
        ("Este dossiê é o plano do JOGO. A conversão de tileset (metatile de três camadas do hack "
         "achatado para duas, de-para do primário, empacotamento do secundário, escolha de paleta) NÃO "
         "está aqui: é o outro braço da frente, dev_scripts/copia_cidade_fonte.py"),
        ("As portas deles têm MB_NON_ANIMATED_DOOR (96), não comportamento zerado como o dossiê de "
         "Jubilife afirmava. A execução tem de PROMOVER esses metatiles a MB_ANIMATED_DOOR no tileset "
         "novo, senão a porta não anima; e tem de dar comportamento de placa às células de placa, que "
         "no hack são MB_NORMAL"),
    ],
}


# ------------------------------------------------------------------ dossiê ---

def constroi(nome, raiz_fonte, raiz_nosso, opcao=None):
    cfg = dict(CIDADES[nome])
    if opcao is not None and "opcoes" in cfg:
        esc = [o for o in cfg["opcoes"] if o["numero"] == opcao][0]
        cfg["partes"] = esc["partes"]
    p = Plano(cfg, raiz_fonte, raiz_nosso)
    W, H, mapa = p.W, p.H, p.mapa

    vis = busca(mapa, cfg["origem"], p.livre)
    vis_cru = busca(mapa, cfg["origem"], p.livre_cru)
    vis_sm = busca(mapa, cfg["origem"], p.livre_sem_moldura)
    livres = sum(1 for y in range(H) for x in range(W) if p.livre(x, y))
    livres_cru = sum(1 for y in range(H) for x in range(W) if p.livre_cru(x, y))

    anc = p.ancoras()
    dxs = [b[0] - a[0] for a, b in anc] or [0]
    dys = [b[1] - a[1] for a, b in anc] or [0]
    delta = (round(sum(dxs) / len(dxs)), round(sum(dys) / len(dys)))

    # ---- warps
    warps = []
    for w in cfg["warps"]:
        nw = p.nosso["warp_events"][w["id"]]
        novo = tuple(w["novo"])
        warps.append({
            "id": w["id"], "destino": nw["dest_map"], "dest_warp_id": nw["dest_warp_id"],
            "nosso_xy": [nw["x"], nw["y"]], "predio_nosso": w["predio"],
            "casa_com": w["casa"], "novo_xy": list(novo),
            "porta_deles_tem_MB_NON_ANIMATED_DOOR": mapa.beh(*novo) == MB_PORTA_FONTE,
            "colisao_no_destino": mapa.col(*novo), "elevacao_no_destino": mapa.elev(*novo),
            "de_frente_alcancavel": (novo in vis) or ((novo[0], novo[1] + 1) in vis),
            "justificativa": w["porque"],
        })

    # ---- objetos
    objetos, ocupadas = [], set()
    for i, o in enumerate(p.nosso["object_events"]):
        alvo, regra = p.transpoe((o["x"], o["y"]), anc, delta)
        novo, d = p.perto(alvo, vis, ocupadas)
        ocupadas.add(novo)
        nota = "%s; chão andável alcançável" % regra
        if d:
            nota += "; alvo %s não servia (ocupado ou bloqueado), deslocado %d tile(s)" % (list(alvo), d)
        objetos.append({"indice": i, "graphics": o["graphics_id"],
                        "script": o.get("script") or None, "flag": o.get("flag") or None,
                        "nosso_xy": [o["x"], o["y"]], "novo_xy": [novo[0], novo[1]],
                        "perto_de": cfg["perto_de"].get(i, "(sem nota)"), "justificativa": nota})

    # ---- bg events (placas e itens escondidos)
    bgs = []
    placas_ocupadas = set()
    for i, b in enumerate(p.nosso["bg_events"]):
        pt = (b["x"], b["y"])
        if i in cfg.get("bg_fixo", {}):
            novo, regra = tuple(cfg["bg_fixo"][i][0]), cfg["bg_fixo"][i][1]
        elif i in cfg.get("bg_alvo", {}):
            alvo = tuple(cfg["bg_alvo"][i][0])
            novo, extra = p.encosta(alvo, vis, placas_ocupadas)
            regra = cfg["bg_alvo"][i][1] + extra
        elif b["type"] != "sign":
            alvo, regra = p.transpoe(pt, anc, delta)
            novo, d = p.perto(alvo, vis)
            regra += "; item escondido: vai para chão andável, não para tile bloqueante"
        else:
            alvo, regra = p.transpoe(pt, anc, delta)
            novo, extra = p.encosta(alvo, vis, placas_ocupadas)
            regra += extra
        placas_ocupadas.add(novo)
        bgs.append({"indice": i, "tipo": b["type"], "script": b.get("script"),
                    "nosso_xy": [pt[0], pt[1]], "novo_xy": [novo[0], novo[1]],
                    "colisao_no_destino": mapa.col(*novo),
                    "lado_alcancavel": bool(any((novo[0] + a, novo[1] + c) in vis
                                                for a, c in ((0, 1), (0, -1), (1, 0), (-1, 0)))),
                    "justificativa": regra})

    # ---- coord events (gatilhos)
    coords = []
    for i, c in enumerate(p.nosso["coord_events"]):
        if i in cfg.get("coord_fixo", {}):
            novo, regra, d = tuple(cfg["coord_fixo"][i][0]), cfg["coord_fixo"][i][1], 0
            coords.append({"indice": i, "script": c.get("script"), "nosso_xy": [c["x"], c["y"]],
                           "novo_xy": [novo[0], novo[1]], "justificativa": regra})
            continue
        alvo, regra = p.transpoe((c["x"], c["y"]), anc, delta)
        novo, d = p.perto(alvo, vis)
        coords.append({"indice": i, "script": c.get("script"), "nosso_xy": [c["x"], c["y"]],
                       "novo_xy": [novo[0], novo[1]],
                       "justificativa": regra + ("" if not d else "; deslocado %d tile(s) para chão andável" % d)})

    # ---- portas deles sem dono
    donas = {tuple(w["novo_xy"]) for w in warps}
    sem_dono = []
    ja = {tuple(e["xy"]) for e in cfg.get("portas_deles_sem_dono_extra", [])}
    for c in p.portas_da_fonte():
        if c in donas or c in ja:
            continue
        sem_dono.append({"xy": list(c), "descricao": "porta com MB_NON_ANIMATED_DOOR sem warp nosso",
                         "tratamento": ("placa closed em inglês (molde das 31 portas de Johto) e a célula "
                                        "fica bloqueante")})
    for extra in cfg.get("portas_deles_sem_dono_extra", []):
        sem_dono.append(dict(extra))

    # ---- bordas
    def borda(lado):
        cel = {"up": [(x, 0) for x in range(W)], "down": [(x, H - 1) for x in range(W)],
               "left": [(0, y) for y in range(H)], "right": [(W - 1, y) for y in range(H)]}[lado]
        alc = [c for c in cel if c in vis]
        return {"alcancaveis": len(alc), "corridas": corridas(alc),
                "agua_na_borda": sum(1 for c in cel if p.agua(*c))}

    conexoes = []
    for c in cfg["conexoes"]:
        conexoes.append({"direcao": c["direcao"], "mapa": c["mapa"],
                         "existe_na_planta_deles": c["existe"], "onde_abrir": c["onde"],
                         "offset_hoje": c["offset_hoje"], "offset_novo": c["offset"],
                         "conta": c["conta"], "borda_medida": borda(c["direcao"])})

    # ---- vazamento de moldura
    vaza = []
    if len(vis_sm) > len(vis):
        conta = Counter(mapa.mid(x, y) for (x, y) in (vis_sm - vis))
        vaza = [{"metatile": m, "celulas": n} for m, n in conta.most_common(16)]

    prova = {
        "origem": list(cfg["origem"]),
        "celulas_do_mapa": W * H,
        "celulas_com_colisao_zero": livres_cru,
        "celulas_andaveis_a_pe": livres,
        "celulas_alcancadas": len(vis),
        "celulas_alcancadas_SEM_tapar_a_moldura": len(vis_sm),
        "celulas_alcancadas_so_com_a_colisao_crua_agua_inclusa": len(vis_cru),
        "agua_de_surf": sum(1 for y in range(H) for x in range(W) if p.agua(x, y)),
        "warps_alcancaveis": "%d de %d" % (sum(1 for w in warps if w["de_frente_alcancavel"]), len(warps)),
        "objetos_alcancaveis": "%d de %d" % (sum(1 for o in objetos if tuple(o["novo_xy"]) in vis), len(objetos)),
        "bg_events_com_lado_alcancavel": "%d de %d" % (sum(1 for b in bgs if b["lado_alcancavel"]), len(bgs)),
        "coord_events_alcancaveis": "%d de %d" % (sum(1 for c in coords if tuple(c["novo_xy"]) in vis), len(coords)),
        "bordas": {l: borda(l) for l in ("up", "down", "left", "right")},
        "moldura_tapada": sorted(p.moldura),
        "metatiles_que_precisam_virar_bloqueantes": vaza,
        "nota": ("a busca em largura anda só onde a colisão é 0, o comportamento não é de água e o "
                 "metatile não é da moldura declarada. O número SEM tapar a moldura está acima para o "
                 "condutor ver o tamanho do vazamento. MEDIDO em 11/09/2026 nas quatro cidades: no "
                 "tamanho proposto, tapar a moldura NÃO muda o alcance (os dois números são iguais). "
                 "A armadilha do bosque que valeu em Jubilife não vale aqui, porque a moldura decorativa "
                 "destas quatro está atrás de uma parede que o próprio autor bloqueou. O que sustenta a "
                 "prova não é a moldura declarada, é o fato de a borda só ser alcançada nos corredores "
                 "de conexão listados abaixo"),
    }

    dossie = {
        "cidade": nome,
        "fonte": {"hack": "Retro Platinum (blloop)", "mapas": [q["mapa"] for q in cfg["partes"]]},
        "nosso": {"largura": p.lay_nosso["width"], "altura": p.lay_nosso["height"]},
        "deles": {"largura": W, "altura": H},
        "tamanho_proposto": {"largura": W, "altura": H, "porque": cfg["tamanho_porque"]},
        "delta_global_da_transposicao": list(delta),
        "warps": warps, "objetos": objetos, "bg_events": bgs, "coord_events": coords,
        "conexoes": conexoes,
        "portas_deles_sem_dono": sem_dono,
        "encaixes": cfg.get("encaixes", []),
        "save_intacta": {
            "object_events": ("%d objetos, ordem e índices preservados de 0 a %d; nenhum acrescentado, "
                              "nenhum removido, nenhum trocado de lugar na lista. Só a coordenada muda"
                              % (len(objetos), len(objetos) - 1)),
            "warps": ("%d warps, ids preservados de 0 a %d; os mapas vizinhos apontam para eles por "
                      "número e continuam apontando. Só a coordenada muda"
                      % (len(warps), len(warps) - 1)),
            "mapLayoutId": ("%s, inalterado: o layout é substituído NO LUGAR, com largura e altura "
                            "novas, e a save guarda o layout por id" % cfg["nosso_layout"]),
            "flags_e_vars": "nenhuma flag nem var nova; nenhuma flag existente muda de significado",
            "bg_events": "%d, ordem e índices preservados" % len(bgs),
            "coord_events": "%d, ordem e índices preservados" % len(coords),
        },
        "censo_de_comportamento_de_metatile": p.censo_comportamento(),
        "prova_de_alcance": prova,
        "riscos": cfg["riscos"],
    }
    if "opcoes" in cfg:
        dossie["opcoes_de_fusao"] = [{k: v for k, v in o.items() if k != "partes"} for o in cfg["opcoes"]]
        dossie["opcao_recomendada"] = cfg["recomendo"]
        dossie["opcao_deste_plano"] = opcao if opcao is not None else cfg["recomendo"]
    return p, dossie, vis


def desenha(p, dossie, caminho_png, raiz_fonte):
    from PIL import Image, ImageDraw
    base = Image.new("RGB", (p.W * 16, p.H * 16), (20, 20, 20))
    coberto = [[False] * p.W for _ in range(p.H)]
    for parte in p.cfg["partes"]:
        im = Image.open(os.path.join(raiz_fonte, "..", "render", parte["mapa"] + ".png")).convert("RGB")
        rec = im.crop((parte["sx"] * 16, parte["sy"] * 16,
                       (parte["sx"] + parte["sw"]) * 16, (parte["sy"] + parte["sh"]) * 16))
        base.paste(rec, (parte["dx"] * 16, parte["dy"] * 16))
        for j in range(parte["sh"]):
            for i in range(parte["sw"]):
                if 0 <= parte["dy"] + j < p.H and 0 <= parte["dx"] + i < p.W:
                    coberto[parte["dy"] + j][parte["dx"] + i] = True
    # o que nenhuma parte cobre leva o metatile de moldura DELES, então a imagem
    # também leva: senão o dossiê mostra um buraco preto que não existe no dado.
    alvo = p.cfg.get("preenchimento", 0)
    amostra = None
    for y in range(p.H):
        for x in range(p.W):
            if coberto[y][x] and p.mapa.mid(x, y) == alvo:
                amostra = base.crop((x * 16, y * 16, x * 16 + 16, y * 16 + 16))
                break
        if amostra:
            break
    if amostra:
        for y in range(p.H):
            for x in range(p.W):
                if not coberto[y][x]:
                    base.paste(amostra, (x * 16, y * 16))
    d = ImageDraw.Draw(base)
    for lado, b in dossie["prova_de_alcance"]["bordas"].items():
        pass
    for c in dossie["conexoes"]:
        for a, b in c["borda_medida"]["corridas"]:
            for x in range(a[0], b[0] + 1):
                for y in range(a[1], b[1] + 1):
                    d.rectangle([x * 16, y * 16, x * 16 + 15, y * 16 + 15], outline=(0, 255, 255), width=2)
    for e in dossie["encaixes"]:
        x, y = e["xy"]
        d.rectangle([x * 16 - 2, y * 16 - 2, x * 16 + 17, y * 16 + 17], outline=(255, 140, 0), width=3)
    for o in dossie["objetos"]:
        x, y = o["novo_xy"]
        d.ellipse([x * 16 + 2, y * 16 + 2, x * 16 + 13, y * 16 + 13], fill=(255, 230, 0), outline=(0, 0, 0))
        d.text((x * 16 + 4, y * 16 + 3), str(o["indice"]), fill=(0, 0, 0))
    for b in dossie["bg_events"]:
        x, y = b["novo_xy"]
        d.rectangle([x * 16 + 2, y * 16 + 2, x * 16 + 13, y * 16 + 13], outline=(0, 220, 0), width=2)
        d.text((x * 16 + 4, y * 16 + 3), str(b["indice"]), fill=(0, 255, 0))
    for c in dossie["coord_events"]:
        x, y = c["novo_xy"]
        d.rectangle([x * 16 + 5, y * 16 + 5, x * 16 + 10, y * 16 + 10], fill=(160, 0, 255))
    junta = {}
    for w in dossie["warps"]:
        junta.setdefault(tuple(w["novo_xy"]), []).append(w["id"])
    for (x, y), ids in junta.items():
        d.rectangle([x * 16 - 1, y * 16 - 1, x * 16 + 16, y * 16 + 16], outline=(255, 0, 0), width=3)
        d.text((x * 16 + 2, y * 16 + 2), "/".join(str(i) for i in ids), fill=(255, 255, 255))
    for s in dossie["portas_deles_sem_dono"]:
        x, y = s["xy"]
        d.rectangle([x * 16 - 1, y * 16 - 1, x * 16 + 16, y * 16 + 16], outline=(255, 0, 255), width=3)
        d.line([x * 16, y * 16, x * 16 + 15, y * 16 + 15], fill=(255, 0, 255), width=2)
        d.line([x * 16 + 15, y * 16, x * 16, y * 16 + 15], fill=(255, 0, 255), width=2)
    base.save(caminho_png)
    return base.size


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cidade", required=True, choices=sorted(CIDADES))
    ap.add_argument("--fonte", default=FONTE_PADRAO)
    ap.add_argument("--saida", default=os.path.join(RAIZ, "dev_scripts/dossies_sinnoh"))
    ap.add_argument("--imagem", help="pasta onde gravar o PNG do plano")
    ap.add_argument("--opcao", type=int, help="Oreburgh: qual opção de fusão desenhar")
    ap.add_argument("--diagnostico", action="store_true", help="só imprime as medidas, não grava nada")
    a = ap.parse_args()

    p, dossie, vis = constroi(a.cidade, a.fonte, RAIZ, a.opcao)
    pr = dossie["prova_de_alcance"]
    print("%s  %dx%d" % (a.cidade, p.W, p.H))
    print("  andáveis a pé %d de %d; alcançadas %d (sem tapar a moldura: %d); água de surf %d"
          % (pr["celulas_andaveis_a_pe"], pr["celulas_do_mapa"], pr["celulas_alcancadas"],
             pr["celulas_alcancadas_SEM_tapar_a_moldura"], pr["agua_de_surf"]))
    print("  warps %s | objetos %s | placas %s | gatilhos %s"
          % (pr["warps_alcancaveis"], pr["objetos_alcancaveis"],
             pr["bg_events_com_lado_alcancavel"], pr["coord_events_alcancaveis"]))
    for lado, b in pr["bordas"].items():
        print("    borda %-5s alcançáveis %-3d %s" % (lado, b["alcancaveis"], b["corridas"][:6]))
    if pr["metatiles_que_precisam_virar_bloqueantes"]:
        print("  vazamento por metatile:", pr["metatiles_que_precisam_virar_bloqueantes"])
    ruins = [w["id"] for w in dossie["warps"] if not w["de_frente_alcancavel"]]
    if ruins:
        print("  WARPS INALCANÇÁVEIS:", ruins)
    fora = [o["indice"] for o in dossie["objetos"] if tuple(o["novo_xy"]) not in vis]
    if fora:
        print("  OBJETOS FORA DO ALCANCE:", fora)
    cens = dossie["censo_de_comportamento_de_metatile"]
    print("  comportamento: %d células zeradas, %d com comportamento; %s"
          % (cens["MB_NORMAL_zerado"], cens["com_comportamento_de_verdade"], cens["por_comportamento"]))
    if a.diagnostico:
        return
    os.makedirs(a.saida, exist_ok=True)
    destino = os.path.join(a.saida, a.cidade + ".json")
    with open(destino, "w", encoding="utf-8") as f:
        json.dump(dossie, f, ensure_ascii=False, indent=1)
    print("  dossiê ->", destino)
    if a.imagem:
        os.makedirs(a.imagem, exist_ok=True)
        png = os.path.join(a.imagem, a.cidade + ".png")
        print("  imagem ->", png, desenha(p, dossie, png, a.fonte))


if __name__ == "__main__":
    main()
