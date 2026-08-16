#!/usr/bin/env python3
"""Prova do renderizador de VirbankComplexB2F (Obra 2, bloco B4, 15/08/2026).

Uso:
    python3 dev_scripts/prova_b2f_interruptores.py     # nao grava nada

POR QUE ESTE ARQUIVO EXISTE

O `data/maps/Unova_VirbankComplexB2F/scripts.inc` NAO e transcricao linha a
linha da fonte. A fonte (`fontes-mapas/bw3g/maps/VirbankComplexB2F.asm`) escreve
o produto cartesiano dos 4 interruptores a mao: o `.SetTiles` de 129 linhas, que
so sabe DESENHAR o que esta ligado, mais oito meias-rotinas
`SetPosition1`/`SetPosition2` que sabem DESFAZER, ~570 linhas com muita
repeticao. Aqui virou UM renderizador que escreve o estado completo a partir das
4 flags e serve ao ON_LOAD e aos 4 gatilhos.

Reescrita merece prova, e a prova e esta: para as 16 combinacoes das 4 flags, o
estado que o nosso `.inc` produz sobre o `map.bin` tem que ser IGUAL, celula por
celula do mapa inteiro, ao que o `.SetTiles` da fonte produz sobre o mesmo
`map.bin`. Os dois lados sao interpretados de verdade (checkevent/iffalse/jump
de um lado, goto_if_set/call/return do outro); os metatiles dos dois vem do
mesmo `changeblock_gen2.py`, entao o que esta sendo medido e a LOGICA, nao a
tabela de tileset (essa quem cobra e o `changeblock_gen2.py --demo`).

Se este teste quebrar depois de alguem mexer no `.inc`, o errado e o `.inc`.
"""
import re, struct, sys
sys.path.insert(0, 'dev_scripts')
import changeblock_gen2 as cg

FONTE = '/Users/duarte/Projetos/pokemon-claude/fontes-mapas/bw3g/maps/VirbankComplexB2F.asm'
INC = 'data/maps/Unova_VirbankComplexB2F/scripts.inc'
ctx = cg.contexto('VirbankComplexB2F')
W = ctx['layout']['width']
FLAGS = ('EVENT_VIRBANK_COMPLEX_B2F_SWITCH1', 'EVENT_VIRBANK_COMPLEX_B2F_SWITCH2',
         'EVENT_VIRBANK_COMPLEX_B2F_SWITCH3', 'EVENT_VIRBANK_COMPLEX_B2F_SWITCH4')
NOSSAS = tuple(f'FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_{i}' for i in (1, 2, 3, 4))


def base():
    """estado estatico do map.bin: (metatile, colisao) por celula"""
    d = {}
    for y in range(ctx['layout']['height']):
        for x in range(W):
            v = struct.unpack_from('<H', ctx['mapbin'], (y * W + x) * 2)[0]
            d[(x, y)] = (v & 0x3FF, bool((v >> 10) & 3))
    return d


def quads(x, y, bloco):
    """(x,y,bloco) do gen 2 -> [(cx, cy, metatile, colisao)] pelo mesmo gerador"""
    txt = f"\tchangeblock {x}, {y}, ${bloco:02x}\n"
    (_o, _x, _y, _b, _l, qs), = cg.traduz('VirbankComplexB2F', txt, ctx)
    return [(q['x'], q['y'], q['metatile'], q['colisao']) for q in qs]


def roda_fonte(estado, ini, fim):
    linhas = open(FONTE).read().splitlines()[ini - 1:fim]
    rot = {l.strip().split(';')[0].strip().rstrip(':').lstrip('.'): i
           for i, l in enumerate(linhas) if re.match(r'^\.\w+:?$', l.strip().split(';')[0].strip())}
    mapa, i, cond = base(), 0, None
    while i < len(linhas):
        l = linhas[i].strip()
        i += 1
        l = l.split(';')[0].strip()
        if not l or re.match(r'^\.\w+:?$', l):
            continue
        if l.startswith('checkevent'):
            cond = estado[FLAGS.index(l.split()[1])]
        elif l.startswith('iffalse'):
            if not cond: i = rot[l.split()[1].lstrip('.')]
        elif l.startswith('iftrue'):
            if cond: i = rot[l.split()[1].lstrip('.')]
        elif l.startswith('jump'):
            i = rot[l.split()[1].lstrip('.')]
        elif l.startswith('changeblock'):
            m = re.match(r'changeblock\s+(\d+),\s*(\d+),\s*\$([0-9a-fA-F]+)', l)
            for cx, cy, mt, col in quads(int(m.group(1)), int(m.group(2)), int(m.group(3), 16)):
                mapa[(cx, cy)] = (mt, col)
        elif l.startswith('return'):
            break
        else:
            raise SystemExit(f'fonte: instrucao nao prevista: {l!r}')
    return mapa


def roda_inc(estado):
    txt = open(INC).read()
    corpo = {}
    atual = None
    for l in txt.splitlines():
        m = re.match(r'^(\w+)::', l)
        if m:
            atual = m.group(1); corpo.setdefault(atual, [])
            # rotulo alias: o de cima aponta para o mesmo corpo
            continue
        if atual is not None:
            corpo[atual].append(l.split('@')[0].strip())
    ordem = [m.group(1) for m in re.finditer(r'^(\w+)::', txt, re.M)]
    plano = []            # sequencia linear (rotulo, indice) para permitir fallthrough
    for r in ordem:
        for j, l in enumerate(corpo[r]):
            plano.append((r, j))
    pos = {r: k for k, (r, j) in enumerate(plano) if j == 0}
    mapa, pilha = base(), []
    k = pos['Unova_VirbankComplexB2F_EventScript_AoCarregar']
    passos = 0
    while k < len(plano):
        passos += 1
        assert passos < 20000, 'laco infinito'
        r, j = plano[k]
        l = corpo[r][j]
        k += 1
        if not l:
            continue
        if l.startswith('changeblock_gen2'):
            a = [t.strip() for t in l.split(None, 1)[1].split(',')]
            x, y = int(a[0]), int(a[1])
            mts = [int(v) for v in a[2:6]]
            cols = [v == 'TRUE' for v in a[6:10]]
            for (dx, dy), mt, col in zip(cg.DESLOC, mts, cols):
                mapa[(x + dx, y + dy)] = (mt, col)
        elif l.startswith('call '):
            pilha.append(k); k = pos[l.split()[1]]
        elif l.startswith('return'):
            if not pilha: break
            k = pilha.pop()
        elif l.startswith('end'):
            break
        elif l.startswith('goto_if_set') or l.startswith('goto_if_unset'):
            flag, dest = [t.strip() for t in l.split(None, 1)[1].split(',')]
            v = estado[NOSSAS.index(flag)]
            if (v if l.startswith('goto_if_set') else not v):
                k = pos[dest]
        elif l.startswith('goto '):
            k = pos[l.split()[1]]
        else:
            raise SystemExit(f'inc: instrucao nao prevista: {l!r}')
    return mapa


falhou = 0
for n in range(16):
    est = tuple(bool(n >> i & 1) for i in range(4))
    a, b = roda_fonte(est, 19, 147), roda_inc(est)
    dif = {c: (a[c], b[c]) for c in a if a[c] != b[c]}
    print(f"sw1..4={tuple(int(x) for x in est)}: {'OK' if not dif else 'DIFERE ' + str(dif)}")
    falhou += bool(dif)
print('RESULTADO:', 'as 16 combinacoes batem com a fonte' if not falhou else f'{falhou} combinacoes diferem')
sys.exit(1 if falhou else 0)
