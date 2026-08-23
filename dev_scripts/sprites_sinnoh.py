#!/usr/bin/env python3
"""Desenha os 26 sprites de overworld dos nomes próprios de Sinnoh.

Por que este arquivo existe
---------------------------
`fontes-mapas/SPRITES-SINNOH.md` mediu que 104 objetos de Sinnoh apontam para
26 pessoas que NÃO têm sprite neste repo, e que nenhuma fonte da comunidade
serve de recorte direto (as que existem são estilo DS, ou não conferidas, e a
redistribuição é proibida na maior delas). A regra do Gui de 05/08/2026 diz que
boneco genérico NÃO pode fingir ser a pessoa. Logo: sprite próprio, autoral,
desenhado aqui, no traço gen 3.

O método, e por que ele é este
------------------------------
Cada sprite nasce de um NPC que JÁ EXISTE no repo (silhueta mais próxima em
porte e roupa), passa por uma troca de papel de cor (cabelo, roupa de cima,
roupa de baixo) e depois por edições de pixel que marcam o traço distintivo
(cabelo comprido, espetado, boné, capacete, óculos, barra de sobretudo).
A silhueta base é gen 3 de verdade, então o resultado nasce no estilo certo,
e o que diferencia a pessoa é desenhado.

A REGRA DE PALETA, que é o que segura o custo
---------------------------------------------
O motor carrega palete de sprite por TAG (`LoadObjectEventPalette`), e só há 16
paletas de sprite na tela inteira, com metade já reservada. Palette própria por
personagem estouraria: a `Villa` tem DEZ desta lista no mesmo mapa (medido no
censo). Por isso NENHUMA paleta nova é criada: cada personagem é desenhado
DENTRO de uma das oito paletas compartilhadas que o jogo já carrega
(`npc_1..4`, `npc_blue/green/pink/white`). Custo de paleta: zero. Pressão de
slot: a mesma de um NPC comum. Medido: o pior mapa (Villa) usa 5 paletas
distintas, das quais 2 já estão sempre carregadas.

As oito paletas têm a MESMA estrutura, o que é o que torna a troca possível:
    0        cor-chave (transparente)
    1,2,3    pele, claro -> sombra           (idênticas nas oito)
    4        marrom escuro (123,65,65)       (idêntico nas oito)
    5,6,7    rampa A, clara -> escura
    8,9,10   rampa B
    11,12,13 rampa C
    14       branco
    15       preto

Zonas do corpo (medidas nos PNG do repo, não chutadas): com `t` = primeira
linha opaca do quadro, cabeça = t..t+10, tronco = t+11..t+16, pernas = t+17
até o fim. Confere em woman_1, cooltrainer_f e nos quadros de andar (que são
os mesmos deslocados um pixel para baixo).

Uso:
    python3 dev_scripts/sprites_sinnoh.py --aplicar   # escreve os 26 PNG
    python3 dev_scripts/sprites_sinnoh.py --contato   # folha de aprovação
    python3 dev_scripts/sprites_sinnoh.py --demo      # auto-teste
"""

import argparse
import os
import sys

from PIL import Image, ImageDraw

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICS = os.path.join(RAIZ, "graphics/object_events/pics/people")
SAIDA = os.path.join(PICS, "sinnoh")
PALETAS = os.path.join(RAIZ, "graphics/object_events/palettes")

TRANSP = 0
PELE = (1, 2, 3)
BRANCO = 14
PRETO = 15
# Papéis de cor preservados em qualquer zona: pele, branco e preto seguram o
# contorno, o olho e o brilho. Trocá-los apagaria o rosto.
PRESERVA = set(PELE) | {BRANCO, PRETO}

A = (5, 6, 7)
B = (8, 9, 10)
C = (11, 12, 13)
ESCURO = (12, 13, 15)
NEGRO = (13, 15, 15)
CLARO = (14, 11, 12)


def le_pal(nome):
    linhas = open(os.path.join(PALETAS, nome + ".pal")).read().split("\n")
    n = int(linhas[2])
    return [tuple(int(v) for v in linhas[3 + i].split()) for i in range(n)][:16]


def luz(rgb):
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


# ---------------------------------------------------------------- o elenco
# base    : PNG de 144x32 (9 quadros) já no repo, escolhido pela silhueta
# pal     : paleta compartilhada de destino
# cabelo / cima / baixo : rampas de destino, clara -> escura
# ops     : edições de pixel que marcam o traço da pessoa
ELENCO = {
    # 12 objetos. Sobretudo bege, o traço que o jogo inteiro usa para ele.
    "looker": dict(base="gentleman", pal="npc_1", objetos=12,
                   cabelo=(4, 4, 15), cima=C, baixo=ESCURO,
                   ops=[("barra", C[1], 3)],
                   nota="sobretudo bege comprido, cabelo escuro"),
    # 11 objetos. Cabelo louro MUITO comprido e casaco preto.
    "cynthia": dict(base="hex_maniac", pal="npc_2", objetos=11, cabelo_preto=True,
                    cabelo=A, cima=NEGRO, baixo=NEGRO,
                    ops=[("cabelo_longo", 6, 9), ("presilha", BRANCO)],
                    nota="cabelo louro longo, casaco preto"),
    # 7 objetos. Cabelo azul espetado, uniforme Galáctico branco e cinza.
    "cyrus": dict(base="scientist_1", pal="npc_4", objetos=7, cabelo_preto=True,
                  cabelo=(5, 5, 6), cima=CLARO, baixo=ESCURO,
                  ops=[("espeta", 5)],
                  nota="cabelo azul espetado, uniforme Galáctico"),
    # 7 objetos. Menino de boné, jaqueta azul.
    "buck": dict(base="youngster", pal="npc_1", objetos=7,
                 cabelo=(4, 4, 15), cima=B, baixo=C,
                 ops=[("bone", 9, 8)],
                 nota="boné azul, jaqueta azul"),
    # 5 objetos. Cabelo rosa curto, gi azul e branco.
    "maylene": dict(base="running_triathlete_f", pal="npc_pink", objetos=5,
                    cabelo=A, cima=(14, 8, 9), baixo=C,
                    ops=[("faixa", 6)],
                    nota="cabelo rosa, gi azul e branco"),
    # 5 objetos. Cabelo vermelho em duas pontas, uniforme Galáctico.
    "mars": dict(base="lass", pal="npc_2", objetos=5,
                 cabelo=B, cima=(14, 13, 15), baixo=NEGRO,
                 ops=[("espeta", 8), ("pontas", 9)],
                 nota="cabelo vermelho espetado, uniforme Galáctico"),
    # 5 objetos. Cabelo roxo em corte tigela, uniforme Galáctico.
    "jupiter": dict(base="reporter_f", pal="npc_4", objetos=5,
                    cabelo=B, cima=CLARO, baixo=NEGRO,
                    ops=[("tigela", 8, 9)],
                    nota="corte tigela roxo, uniforme Galáctico"),
    # 5 objetos. Verde da líder de planta, faixa na cabeça.
    "gardenia": dict(base="picnicker", pal="npc_3", objetos=5,
                     cabelo=(4, 4, 15), cima=B, baixo=C,
                     ops=[("faixa", 8)],
                     nota="roupa verde, faixa verde"),
    # 5 objetos. Homem grande, máscara de luta azul e roupa laranja.
    "crasher_wake": dict(base="black_belt", pal="npc_blue", objetos=5,
                         cabelo=B, cima=C, baixo=ESCURO,
                         ops=[("tigela", 8, 9), ("faixa", 11)],
                         nota="máscara azul de luta, roupa laranja"),
    # 4 objetos. Cabelo louro espetado, jaqueta azul.
    "volkner": dict(base="man_4", pal="npc_blue", objetos=4,
                    cabelo=A, cima=B, baixo=ESCURO,
                    ops=[("espeta", 5)],
                    nota="cabelo louro espetado, jaqueta azul"),
    # 4 objetos. Cabelo vermelho, capacete amarelo de mineiro, óculos.
    "roark": dict(base="school_kid_m", pal="npc_2", objetos=4, cabelo_preto=True,
                  cabelo=B, cima=C, baixo=ESCURO,
                  ops=[("capacete", 5, 6), ("oculos", 15)],
                  nota="capacete amarelo, cabelo vermelho"),
    # 4 objetos. Cabelo vermelho enorme (afro), roupa preta.
    "flint": dict(base="man_3", pal="npc_2", objetos=4,
                  cabelo=B, cima=NEGRO, baixo=NEGRO,
                  ops=[("afro", 8, 9)],
                  nota="afro vermelho, roupa preta"),
    # 4 objetos. Cabelo roxo, vestido roxo e branco.
    "fantina": dict(base="beauty", pal="npc_blue", objetos=4,
                    cabelo=B, cima=(14, 8, 9), baixo=(10, 10, 15),
                    ops=[("cabelo_longo", 5, 7)],
                    nota="cabelo roxo, vestido roxo e branco"),
    # 4 objetos. Velho de cabelo branco e óculos, uniforme Galáctico.
    "charon": dict(base="scientist_2", pal="npc_4", objetos=4, cabelo_preto=True,
                   cabelo=CLARO, cima=C, baixo=ESCURO,
                   ops=[("oculos", 15)],
                   nota="cabelo branco, óculos, uniforme Galáctico"),
    # 3 objetos. Cabelo azul escuro, uniforme Galáctico.
    "saturn": dict(base="man_1", pal="npc_4", objetos=3,
                   cabelo=A, cima=CLARO, baixo=NEGRO,
                   ops=[("tigela", 5, 6)],
                   nota="cabelo azul escuro, uniforme Galáctico"),
    # 3 objetos. Cabelo escuro comprido, cachecol rosa.
    "candice": dict(base="girl_3", pal="npc_pink", objetos=3,
                    cabelo=(10, 10, 15), cima=CLARO, baixo=ESCURO,
                    ops=[("cabelo_longo", 10, 7), ("faixa", 5)],
                    nota="cabelo escuro longo, cachecol rosa"),
    # 3 objetos. Homem grande, cabelo e barba grisalhos, capacete.
    "byron": dict(base="hiker", pal="npc_white", objetos=3,
                  cabelo=C, cima=B, baixo=ESCURO,
                  ops=[("capacete", 11, 12), ("barba", 11)],
                  nota="barba grisalha, capacete, roupa marrom"),
    # 2 objetos. Boné e terno azul, camisa branca.
    "riley": dict(base="man_2", pal="npc_pink", objetos=2,
                  cabelo=(10, 13, 15), cima=(9, 10, 15), baixo=ESCURO,
                  ops=[("bone", 9, 8), ("faixa", 14)],
                  nota="boné azul, terno azul, camisa branca"),
    # 2 objetos. Cabelo prateado comprido, roupa escura.
    "marley": dict(base="girl_2", pal="npc_3", objetos=2,
                   cabelo=A, cima=NEGRO, baixo=NEGRO,
                   ops=[("cabelo_longo", 5, 8)],
                   nota="cabelo prateado longo, roupa escura"),
    # 2 objetos. Cabelo roxo, óculos, roupa azul de gala.
    "lucian": dict(base="psychic_m", pal="npc_4", objetos=2,
                   cabelo=B, cima=A, baixo=ESCURO,
                   ops=[("oculos", 15), ("tigela", 8, 9)],
                   nota="cabelo roxo, óculos, roupa azul"),
    # 2 objetos. Cameo de Johto em Sinnoh: castanha, vestido azul e branco.
    "jasmine": dict(base="woman_2", pal="npc_pink", objetos=2,
                    cabelo=(4, 4, 15), cima=B, baixo=C,
                    ops=[("cabelo_longo", 4, 6)],
                    nota="cabelo castanho longo, vestido azul"),
    # 1 objeto. Sobretudo laranja comprido, cabelo claro espetado.
    "palmer": dict(base="contest_judge", pal="npc_blue", objetos=1,
                   cabelo=(14, 5, 6), cima=C, baixo=ESCURO,
                   ops=[("barra", 11, 3)],
                   nota="sobretudo laranja, cabelo claro"),
    # 1 objeto. Menina de capacete de mineira, cabelo azul.
    "mira": dict(base="twin", pal="npc_2", objetos=1,
                 cabelo=(12, 13, 15), cima=B, baixo=C,
                 ops=[("capacete", 5, 6)],
                 nota="capacete de mineira, cabelo azul"),
    # 1 objeto. Cabelo verde, roupa clara.
    "cheryl": dict(base="woman_5", pal="npc_green", objetos=1,
                   cabelo=B, cima=(14, 5, 6), baixo=(9, 10, 15),
                   ops=[("cabelo_longo", 8, 7)],
                   nota="cabelo verde, roupa clara"),
    # 1 objeto. Velha da Elite, cabelo grisalho, vestido marrom.
    "bertha": dict(base="old_woman", pal="npc_white", objetos=1,
                   cabelo=C, cima=B, baixo=A,
                   ops=[("faixa", 9)],
                   nota="cabelo grisalho, vestido marrom"),
    # 1 objeto. Cabelo verde espetado, roupa clara.
    "aaron": dict(base="boy_1", pal="npc_3", objetos=1,
                  cabelo=B, cima=(14, 5, 6), baixo=(9, 10, 15),
                  ops=[("espeta", 8)],
                  nota="cabelo verde espetado, roupa clara"),
}

QUADROS = 9
LARG = 16
ALT = 32
# Quadros virados para o norte: são as COSTAS, e é onde a massa de cabelo
# aparece inteira. Quadros do sul mostram o rosto; oeste, o perfil.
NORTE = (1, 5, 6)
SUL = (0, 3, 4)
OESTE = (2, 7, 8)


class Quadro:
    """Um quadro 16x32 com as zonas do corpo já medidas."""

    def __init__(self, px, f):
        self.px = px
        self.f = f
        self.x0 = f * LARG
        linhas = [y for y in range(ALT)
                  if any(px[self.x0 + x, y] != TRANSP for x in range(LARG))]
        self.t = linhas[0] if linhas else 0
        self.b = linhas[-1] if linhas else 0
        self.cabeca = (self.t, self.t + 10)
        self.tronco = (self.t + 11, self.t + 16)
        self.pernas = (self.t + 17, self.b)

    def get(self, x, y):
        if 0 <= x < LARG and 0 <= y < ALT:
            return self.px[self.x0 + x, y]
        return TRANSP

    def set(self, x, y, v):
        if 0 <= x < LARG and 0 <= y < ALT:
            self.px[self.x0 + x, y] = v

    def opaco(self, x, y):
        return self.get(x, y) != TRANSP

    def extremos(self, y):
        xs = [x for x in range(LARG) if self.opaco(x, y)]
        return (xs[0], xs[-1]) if xs else None

    def zona(self, y):
        if y <= self.cabeca[1]:
            return "cabeca"
        if y <= self.tronco[1]:
            return "tronco"
        return "pernas"


def mapeia_rampa(origem, destino, cores_origem, cores_destino):
    """Casa índices de origem com a rampa de destino pela ordem de luz.

    O sprite base sombreia com 2 ou 3 tons; a rampa de destino tem 3. Casar por
    POSTO de luminância (do mais claro ao mais escuro) preserva o volume, que é
    o que faz o resultado continuar parecendo gen 3 e não decalque chapado.
    """
    ordem = sorted(origem, key=lambda i: -luz(cores_origem[i]))
    n = len(ordem)
    mapa = {}
    for k, idx in enumerate(ordem):
        pos = 0 if n == 1 else round(k * (len(destino) - 1) / (n - 1))
        mapa[idx] = destino[pos]
    return mapa


# ------------------------------------------------------------------- edições
# Cada edição trabalha sobre a máscara opaca do quadro, então vale para os 9
# quadros sem tabela por quadro, e acompanha o deslocamento de 1 px dos quadros
# de andar automaticamente.

def op_espeta(q, cor):
    """Pontas de cabelo acima da cabeça (Cyrus, Volkner, Mars, Aaron)."""
    y = q.t
    ext = q.extremos(y)
    if not ext:
        return
    a, b = ext
    for x in range(a, b + 1):
        if (x - a) % 2 == 0 and q.opaco(x, y):
            q.set(x, y - 1, cor)
            if (x - a) % 4 == 0:
                q.set(x, y - 2, cor)
    q.t = max(0, q.t - 2)


def op_afro(q, claro, escuro):
    """Massa de cabelo alta e larga (Flint, Charon, Bertha)."""
    for dy in (1, 2):
        y = q.t - dy
        ext = q.extremos(q.t)
        if not ext:
            return
        a, b = ext
        a, b = (a - 1, b + 1) if dy == 1 else (a, b)
        for x in range(a, b + 1):
            q.set(x, y, claro if dy == 2 else escuro)
    ext = q.extremos(q.t + 2)
    if ext:
        a, b = ext
        for y in range(q.t, q.t + 3):
            q.set(a - 1, y, escuro)
            q.set(b + 1, y, escuro)
    q.t = max(0, q.t - 2)


def op_cabelo_longo(q, cor, comprimento):
    """Cabelo que desce pelas laterais e cobre as costas.

    Nos quadros do norte o cabelo preenche o miolo, porque ali se vê a nuca.
    """
    ini = q.cabeca[1] - 2
    for k in range(comprimento):
        y = ini + k
        ext = q.extremos(y)
        if not ext:
            break
        a, b = ext
        q.set(a, y, cor)
        q.set(b, y, cor)
        if q.f in NORTE and k < comprimento - 2:
            for x in range(a, b + 1):
                q.set(x, y, cor)


def op_bone(q, copa, aba):
    """Boné: copa nas duas primeiras linhas da cabeça e aba à frente."""
    for dy in (0, 1):
        y = q.t + dy
        ext = q.extremos(y)
        if not ext:
            continue
        a, b = ext
        for x in range(a, b + 1):
            if q.opaco(x, y):
                q.set(x, y, copa)
    y = q.t + 2
    ext = q.extremos(y)
    if ext:
        a, b = ext
        for x in range(a, b + 1):
            if q.opaco(x, y):
                q.set(x, y, copa)
        if q.f in SUL:
            for x in range(a - 1, b + 2):
                q.set(x, y + 1, aba)
        elif q.f in OESTE:
            for x in range(a - 2, a + 2):
                q.set(x, y + 1, aba)


def op_tigela(q, claro, escuro):
    """Corte tigela / máscara: cabeça inteira coberta até a testa."""
    for dy in range(0, 4):
        y = q.t + dy
        ext = q.extremos(y)
        if not ext:
            continue
        a, b = ext
        for x in range(a, b + 1):
            if q.opaco(x, y):
                q.set(x, y, claro if dy == 0 else escuro)


def op_capacete(q, claro, escuro):
    """Capacete com aba reta (Roark, Byron, Mira).

    Três linhas de copa e UMA de aba. Mais que isso vira balde: medido na
    primeira folha de contato de 22/08/2026, em que Byron e Mira sumiram
    dentro do capacete.
    """
    for dy in range(0, 3):
        y = q.t + dy
        ext = q.extremos(y)
        if not ext:
            continue
        a, b = ext
        for x in range(a, b + 1):
            if q.opaco(x, y):
                q.set(x, y, claro if dy == 0 else escuro)
    y = q.t + 3
    ext = q.extremos(y)
    if ext:
        a, b = ext
        for x in range(a - 1, b + 2):
            q.set(x, y, escuro)


def op_oculos(q, cor):
    """Óculos: um traço na linha dos olhos, só de frente e de perfil."""
    y = q.t + 6
    ext = q.extremos(y)
    if not ext:
        return
    a, b = ext
    if q.f in SUL:
        for x in (a + 1, a + 2, b - 2, b - 1):
            if q.opaco(x, y):
                q.set(x, y, cor)
    elif q.f in OESTE:
        for x in (a + 1, a + 2):
            if q.opaco(x, y):
                q.set(x, y, cor)


def op_faixa(q, cor):
    """Faixa/cachecol na linha do pescoço."""
    y = q.cabeca[1]
    ext = q.extremos(y)
    if not ext:
        return
    a, b = ext
    for x in range(a, b + 1):
        if q.opaco(x, y):
            q.set(x, y, cor)


def op_barba(q, cor):
    """Barba: base da cabeça, só onde já havia pele."""
    for y in range(q.t + 7, q.cabeca[1] + 1):
        for x in range(LARG):
            if q.get(x, y) in PELE and y >= q.t + 8:
                q.set(x, y, cor)


def op_presilha(q, cor):
    """Presilhas no alto da cabeça (Cynthia)."""
    y = q.t + 1
    ext = q.extremos(y)
    if not ext:
        return
    a, b = ext
    q.set(a, y, cor)
    q.set(b, y, cor)


def op_pontas(q, cor):
    """Duas pontas laterais na altura da orelha (Mars)."""
    y = q.t + 4
    ext = q.extremos(y)
    if not ext:
        return
    a, b = ext
    q.set(a - 1, y, cor)
    q.set(b + 1, y, cor)
    q.set(a - 1, y + 1, cor)
    q.set(b + 1, y + 1, cor)


def op_barra(q, cor, altura):
    """Barra de sobretudo: alonga a roupa por cima das pernas."""
    ini = q.tronco[1] + 1
    for k in range(altura):
        y = ini + k
        ext = q.extremos(y)
        if not ext:
            break
        a, b = ext
        for x in range(a, b + 1):
            if q.opaco(x, y):
                q.set(x, y, cor)


OPS = {
    "espeta": op_espeta,
    "afro": op_afro,
    "cabelo_longo": op_cabelo_longo,
    "bone": op_bone,
    "tigela": op_tigela,
    "capacete": op_capacete,
    "oculos": op_oculos,
    "faixa": op_faixa,
    "barba": op_barba,
    "presilha": op_presilha,
    "pontas": op_pontas,
    "barra": op_barra,
}


def desenha(nome, ficha):
    origem = Image.open(os.path.join(PICS, ficha["base"] + ".png"))
    if origem.mode != "P":
        raise SystemExit("base %s nao e indexada" % ficha["base"])
    if origem.size[1] != ALT or origem.size[0] < QUADROS * LARG:
        raise SystemExit("base %s tem tamanho %s" % (ficha["base"], origem.size))
    origem = origem.crop((0, 0, QUADROS * LARG, ALT))
    pl = origem.getpalette()[:48]
    cores_origem = [tuple(pl[i * 3:i * 3 + 3]) for i in range(16)]
    cores_destino = le_pal(ficha["pal"])

    img = Image.new("P", (QUADROS * LARG, ALT), TRANSP)
    achatado = []
    for rgb in cores_destino:
        achatado += list(rgb)
    img.putpalette(achatado + [0] * (768 - len(achatado)))
    px_dst = img.load()
    px_src = origem.load()

    # 1) troca de papel de cor, zona por zona.
    destinos = {"cabeca": ficha["cabelo"], "tronco": ficha["cima"],
                "pernas": ficha["baixo"]}
    # Bases de cabelo PRETO (scientist_1, hex_maniac, school_kid_m) pintam o
    # cabelo com o índice 15, que normalmente é contorno e fica preservado.
    # Sem esta chave o "cabelo louro da Cynthia" sairia preto: medido.
    preto_e_cabelo = ficha.get("cabelo_preto", False)
    for f in range(QUADROS):
        q = Quadro(px_src, f)
        por_zona = {"cabeca": set(), "tronco": set(), "pernas": set()}
        for y in range(ALT):
            z = q.zona(y)
            guarda = PRESERVA - {PRETO} if (z == "cabeca" and preto_e_cabelo) \
                else PRESERVA
            for x in range(LARG):
                v = q.get(x, y)
                if v != TRANSP and v not in guarda:
                    por_zona[z].add(v)
        mapas = {z: mapeia_rampa(sorted(s), destinos[z], cores_origem,
                                 cores_destino)
                 for z, s in por_zona.items()}
        for y in range(ALT):
            z = q.zona(y)
            for x in range(LARG):
                v = q.get(x, y)
                px_dst[f * LARG + x, y] = mapas[z].get(v, v)

    # 2) edições de pixel sobre o resultado já recolorido.
    for f in range(QUADROS):
        q = Quadro(px_dst, f)
        for op in ficha["ops"]:
            OPS[op[0]](q, *op[1:])
    return img


def cores_usadas(img):
    return {v for v in img.getdata()}


def aplicar(verbose=True):
    os.makedirs(SAIDA, exist_ok=True)
    feitos = []
    for nome, ficha in ELENCO.items():
        img = desenha(nome, ficha)
        alvo = os.path.join(SAIDA, nome + ".png")
        img.save(alvo)
        feitos.append((nome, ficha, alvo))
        if verbose:
            print("%-14s base=%-22s pal=%-10s cores=%2d %s"
                  % (nome, ficha["base"], ficha["pal"], len(cores_usadas(img)),
                     ficha["nota"]))
    return feitos


def contato(destino):
    """Folha de aprovação: quadro de frente de cada um, 4x, com o nome."""
    cols, escala = 6, 4
    cel_w, cel_h = LARG * escala + 12, ALT * escala + 22
    linhas = (len(ELENCO) + cols - 1) // cols
    folha = Image.new("RGB", (cols * cel_w, linhas * cel_h + 26), (26, 26, 26))
    d = ImageDraw.Draw(folha)
    d.text((8, 8), "Pokemon Claude - 26 sprites de Sinnoh (quadro de frente, 4x)",
           fill=(255, 255, 255))
    ordem = sorted(ELENCO.items(), key=lambda kv: -kv[1]["objetos"])
    for i, (nome, ficha) in enumerate(ordem):
        img = Image.open(os.path.join(SAIDA, nome + ".png")).convert("RGB")
        quadro = img.crop((0, 0, LARG, ALT)).resize(
            (LARG * escala, ALT * escala), Image.NEAREST)
        cx = (i % cols) * cel_w + 6
        cy = (i // cols) * cel_h + 26
        folha.paste(quadro, (cx, cy))
        rotulo = "%s %d" % (nome.upper().replace("CRASHER_", "")[:10],
                            ficha["objetos"])
        d.text((cx, cy + ALT * escala + 2), rotulo, fill=(255, 255, 255))
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    folha.save(destino)
    return destino


def demo():
    """Auto-teste: o que tem que ser verdade para a build não quebrar."""
    falhas = []
    feitos = aplicar(verbose=False)
    assert len(feitos) == 26, "elenco tem %d, esperado 26" % len(feitos)
    total = sum(f["objetos"] for _, f, _ in feitos)
    if total != 104:
        falhas.append("soma de objetos = %d, o censo diz 104" % total)
    for nome, ficha, caminho in feitos:
        img = Image.open(caminho)
        if img.mode != "P":
            falhas.append("%s nao e indexado" % nome)
        if img.size != (QUADROS * LARG, ALT):
            falhas.append("%s tem %s, esperado (144, 32)" % (nome, img.size))
        usadas = cores_usadas(img)
        if max(usadas) > 15:
            falhas.append("%s usa indice %d, acima de 15" % (nome, max(usadas)))
        pl = img.getpalette()[:48]
        esperada = le_pal(ficha["pal"])
        achada = [tuple(pl[i * 3:i * 3 + 3]) for i in range(16)]
        if achada != esperada:
            falhas.append("%s nao carrega a paleta %s" % (nome, ficha["pal"]))
        # Cada quadro precisa ter desenho: quadro vazio vira NPC invisível.
        px = img.load()
        for f in range(QUADROS):
            if not any(px[f * LARG + x, y] != TRANSP
                       for x in range(LARG) for y in range(ALT)):
                falhas.append("%s tem o quadro %d vazio" % (nome, f))
        # O sprite tem que caber: nada pode encostar na borda de cima do
        # quadro seguinte (as edições sobem pixels e podiam vazar).
        for f in range(QUADROS):
            if px[f * LARG, 0] != TRANSP:
                falhas.append("%s vaza na coluna 0 do quadro %d" % (nome, f))
        # Idempotência: redesenhar dá byte igual.
        de_novo = desenha(nome, ficha)
        if list(de_novo.getdata()) != list(img.getdata()):
            falhas.append("%s nao e idempotente" % nome)
    # A troca de papel tem que MUDAR alguma coisa: se o mapa saísse identidade
    # o "sprite novo" seria o boneco genérico, que é exatamente o proibido.
    for nome, ficha, caminho in feitos:
        base = Image.open(os.path.join(PICS, ficha["base"] + ".png")).crop(
            (0, 0, QUADROS * LARG, ALT))
        novo = Image.open(caminho)
        iguais = sum(1 for a, b in zip(base.getdata(), novo.getdata()) if a == b)
        if iguais == QUADROS * LARG * ALT:
            falhas.append("%s saiu identico ao base %s" % (nome, ficha["base"]))
    # Paletas distintas por mapa: o pior caso medido é a Villa, com 10 nomes.
    villa = ["byron", "candice", "crasher_wake", "cynthia", "fantina", "flint",
             "gardenia", "maylene", "roark", "volkner"]
    pals = {ELENCO[n]["pal"] for n in villa}
    if len(pals) > 6:
        falhas.append("Villa pediria %d paletas de sprite" % len(pals))
    if falhas:
        for f in falhas:
            print("FALHOU:", f)
        return 1
    print("demo OK: 26 sprites, 144x32, 9 quadros, <=16 cores, paleta "
          "compartilhada declarada, idempotente; Villa em %d paletas" % len(pals))
    return 0



# ---------------------------------------------------------------- registro
# O registro é feito por BLOCO MARCADO em cada arquivo, e não por append solto:
# rodar de novo substitui o bloco no lugar, então o script é idempotente e não
# duplica símbolo se alguém rodar duas vezes.
ABRE = "// >>> sprites de Sinnoh, gerados por dev_scripts/sprites_sinnoh.py"
FECHA = "// <<< fim dos sprites de Sinnoh"

# npc_1..4 têm slot próprio sempre carregado; os quatro de FRLG entram pelo
# slot 1, que é o que o Policeman (OBJ_EVENT_PAL_TAG_NPC_BLUE) já faz aqui.
SLOT = {"npc_1": "PALSLOT_NPC_1", "npc_2": "PALSLOT_NPC_2",
        "npc_3": "PALSLOT_NPC_3", "npc_4": "PALSLOT_NPC_4"}

ARQS = {
    "const": "include/constants/event_objects.h",
    "gfx": "src/data/object_events/object_event_graphics.h",
    "pic": "src/data/object_events/object_event_pic_tables.h",
    "info": "src/data/object_events/object_event_graphics_info.h",
    "ptr": "src/data/object_events/object_event_graphics_info_pointers.h",
}


def simbolo(nome):
    return "Sinnoh" + "".join(p.capitalize() for p in nome.split("_"))


def constante(nome):
    return "OBJ_EVENT_GFX_SINNOH_" + nome.upper()


def tag(pal):
    return "OBJ_EVENT_PAL_TAG_" + pal.upper()


def troca_bloco(caminho, corpo, antes=None, fim_de_arquivo=False):
    """Põe (ou substitui) o bloco marcado em `caminho`."""
    texto = open(caminho).read()
    novo = ABRE + "\n" + corpo.rstrip("\n") + "\n" + FECHA + "\n"
    if ABRE in texto:
        i = texto.index(ABRE)
        j = texto.index(FECHA, i) + len(FECHA) + 1
        texto = texto[:i] + novo + texto[j:]
    elif fim_de_arquivo:
        texto = texto.rstrip("\n") + "\n\n" + novo
    else:
        i = texto.index(antes)
        texto = texto[:i] + novo + texto[i:]
    open(caminho, "w").write(texto)


def registrar():
    ordem = sorted(ELENCO.items(), key=lambda kv: -kv[1]["objetos"])

    # 1) constantes: APPEND no fim do enum. Id de gráfico vive no map.json e
    # nunca na save, então acrescentar no fim não mexe no id de ninguém (é o
    # mesmo argumento escrito para OBJ_EVENT_GFX_RED_2 em 15/08/2026).
    corpo = ("// Os 26 nomes próprios de Sinnoh que o censo achou sem sprite\n"
             "// (fontes-mapas/SPRITES-SINNOH.md, 104 objetos). Entram no FIM\n"
             "// do enum: id de gráfico só vive no map.json, nunca na save.\n")
    corpo += "".join("    %s,\n" % constante(n) for n, _ in ordem)
    troca_bloco(os.path.join(RAIZ, ARQS["const"]), corpo,
                antes="    NUM_OBJ_EVENT_GFX,")

    # 2) os PNG. CRU e não INCGFX_COMP de propósito: folha comprimida ocupa a
    # folha INTEIRA na VRAM de OBJ (80 tiles por NPC de 9 quadros em vez de 8),
    # e a Villa põe DEZ destes na mesma tela. O aviso está no cabeçalho de
    # dev_scripts/comprime_overworld.py, com o borrão medido em 15/08/2026.
    corpo = "".join(
        'const u32 gObjectEventPic_%s[] = INCGFX_U32('
        '"graphics/object_events/pics/people/sinnoh/%s.png", ".4bpp", '
        '"-mwidth 2 -mheight 4");\n' % (simbolo(n), n) for n, _ in ordem)
    troca_bloco(os.path.join(RAIZ, ARQS["gfx"]), corpo, fim_de_arquivo=True)

    # 3) tabelas de quadro: identidade (0..8), que é o que sAnimTable_Standard
    # espera de uma folha de 9 quadros.
    corpo = "".join(
        "static const struct SpriteFrameImage sPicTable_%s[] = {\n"
        "    overworld_ascending_frames(gObjectEventPic_%s, 2, 4),\n};\n\n"
        % (simbolo(n), simbolo(n)) for n, _ in ordem)
    troca_bloco(os.path.join(RAIZ, ARQS["pic"]), corpo, fim_de_arquivo=True)

    # 4) graphics info.
    corpo = ""
    for n, f in ordem:
        corpo += (
            "// %s: %s. Base de silhueta: %s.\n"
            "const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_%s = {\n"
            "    .tileTag = TAG_NONE,\n"
            "    .paletteTag = %s,\n"
            "    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,\n"
            "    .size = 256,\n"
            "    .width = 16,\n"
            "    .height = 32,\n"
            "    .paletteSlot = %s,\n"
            "    .shadowSize = SHADOW_SIZE_M,\n"
            "    .inanimate = FALSE,\n"
            "    .compressed = FALSE,\n"
            "    .tracks = TRACKS_FOOT,\n"
            "    .oam = &gObjectEventBaseOam_16x32,\n"
            "    .subspriteTables = sOamTables_16x32,\n"
            "    .anims = sAnimTable_Standard,\n"
            "    .images = sPicTable_%s,\n"
            "};\n\n" % (n.upper(), f["nota"], f["base"], simbolo(n),
                         tag(f["pal"]), SLOT.get(f["pal"], "PALSLOT_NPC_1"),
                         simbolo(n)))
    troca_bloco(os.path.join(RAIZ, ARQS["info"]), corpo, fim_de_arquivo=True)

    # 5) ponteiros: extern no topo e entrada na tabela.
    caminho = os.path.join(RAIZ, ARQS["ptr"])
    corpo = "".join(
        "extern const struct ObjectEventGraphicsInfo "
        "gObjectEventGraphicsInfo_%s;\n" % simbolo(n) for n, _ in ordem)
    troca_bloco(caminho, corpo,
                antes="const struct ObjectEventGraphicsInfo *const "
                      "gObjectEventGraphicsInfoPointers")
    texto = open(caminho).read()
    ABRE2, FECHA2 = ABRE + " (tabela)", FECHA + " (tabela)"
    linhas = "".join("    [%s] = &gObjectEventGraphicsInfo_%s,\n"
                     % (constante(n), simbolo(n)) for n, _ in ordem)
    novo = ABRE2 + "\n" + linhas + FECHA2 + "\n"
    if ABRE2 in texto:
        i = texto.index(ABRE2)
        j = texto.index(FECHA2, i) + len(FECHA2) + 1
        texto = texto[:i] + novo + texto[j:]
    else:
        marca = "    [MAUVILLE_MAN_UNUSED2]"
        i = texto.index("};", texto.index(
            "gObjectEventGraphicsInfoPointers"))
        texto = texto[:i] + novo + texto[i:]
    open(caminho, "w").write(texto)

    bytes_rom = len(ordem) * QUADROS * 256
    print("registrados %d graficos; %d B crus de arte (%.1f KB)"
          % (len(ordem), bytes_rom, bytes_rom / 1024.0))
    return 0



def de_para():
    """Nome que a fonte usa -> gráfico que este script desenhou.

    `importa_npcs_sinnoh.py` consulta esta tabela ANTES do filtro
    `NOMES_PROPRIOS`: os 26 deixaram de ser "nome próprio sem sprite aqui" e
    passaram a ter sprite. Mora aqui, e não lá, porque quem desenha é quem sabe
    o que existe; e assim acrescentar personagem novo é uma linha só, no
    ELENCO, sem tocar no importador.
    """
    return {"OBJ_EVENT_GFX_" + n.upper(): constante(n) for n in ELENCO}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--aplicar", action="store_true")
    p.add_argument("--contato", metavar="CAMINHO", nargs="?", const="auto")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--registrar", action="store_true")
    a = p.parse_args()
    if a.demo:
        return demo()
    if a.registrar:
        aplicar(verbose=False)
        return registrar()
    if a.aplicar or a.contato:
        aplicar()
    if a.contato:
        destino = a.contato
        if destino == "auto":
            destino = os.path.join(RAIZ, "..", "CONTATO.png")
        print("contato:", contato(destino))
    if not (a.aplicar or a.contato or a.registrar):
        p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
