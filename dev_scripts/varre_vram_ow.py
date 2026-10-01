#!/usr/bin/env python3
"""Varredura estática: em que mapa a VRAM de sprites estoura com os Pokémon de campo.

Uso: python3 dev_scripts/varre_vram_ow.py [raiz do repo]

Por que existe (bugs3-lendario, 30/09/2026): o Pecharunt de Canalave nascia
fatiado porque a folha comprimida dele não cabia na VRAM de sprites junto com
as do Koraidon (64x64, 448 tiles), Poipole, Naganadel, Eternatus e Terapagos.
O motor agora cai num plano B de um quadro só (src/event_object_movement.c,
OwSheetFallback_*), mas o plano B é rede de segurança: Pokémon de campo em
monte continua sendo erro de mapa. Esta conta diz onde há monte.

A conta: para cada posição do jogador, os objetos na janela de nascimento do
motor (TrySpawnObjectEvents: x de -9 a +10, y de -7 a +9 em volta do jogador),
cada espécie com a folha inteira (quadros + 1 de prefixo, em tiles) e cada NPC
com 8 tiles, contra 1024 tiles menos sombra e jogador. Ignora flags (pior caso)
e fragmentação (otimista). Calibrada no emulador: Canalave e Mt. Silver de fora
acusam aqui e acenderam gOwSheetFallbackCount no runner; os outros mapas da
lista só pela conta.
"""
import json, os, re, struct, glob, sys
R = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(R)
# especie -> pasta de gráfico, pelo INCGFX de gObjectEventPic_X e pelo sPicTable do species_info
pic_png = {}
for l in open('src/data/graphics/pokemon.h'):
    m = re.search(r'gObjectEventPic_(\w+)\[\] = INCGFX_COMP\("([^"]+)"', l)
    if m: pic_png[m.group(1)] = m.group(2)
pictab = {}
for l in open('src/data/object_events/object_event_pic_tables_followers.h'):
    m = re.search(r'sPicTable_(\w+)\[\]', l)
    if m: cur = m.group(1)
    m = re.search(r'overworld_ascending_frames\(gObjectEventPic_(\w+), (\d+), (\d+)\)', l)
    if m: pictab[cur] = (m.group(1), int(m.group(2)), int(m.group(3)))
# SPECIES_X -> sPicTable
sp2tab = {}
for f in glob.glob('src/data/pokemon/species_info/*.h'):
    txt = open(f).read()
    for m in re.finditer(r'\[(SPECIES_\w+)\]\s*=\s*\{(.*?)\n    \},', txt, re.S):
        mm = re.search(r'OVERWORLD\(\s*(sPicTable_\w+|\w+)', m.group(2))
        if mm: sp2tab[m.group(1)] = mm.group(1).replace('sPicTable_', '')
def custo(sp):
    tab = sp2tab.get(sp)
    if not tab or tab not in pictab: return None
    pic, w, h = pictab[tab]
    png = pic_png.get(pic)
    if not png or not os.path.exists(png): return None
    d = open(png, 'rb').read(24); W, H = struct.unpack('>II', d[16:24])
    fw, fh = w*8, h*8
    frames = (W//fw) * (H//fh)
    return (frames + 1) * w * h
BUDGET = 1024 - 2 - 16   # sombra(2) + jogador/seta/reflexo (medido em Canalave: ~16)
res = []
for mj in sorted(glob.glob('data/maps/*/map.json')):
    d = json.load(open(mj))
    objs = d.get('object_events', [])
    mons = [o for o in objs if 'GFX_SPECIES' in o.get('graphics_id', '')]
    if not mons: continue
    lay = d['layout']
    xs = [o['x'] for o in objs]; ys = [o['y'] for o in objs]
    pior = (0, None, None)
    for py in range(min(ys)-9, max(ys)+8):
        for px in range(min(xs)-10, max(xs)+10):
            jan = [o for o in objs if px-9 <= o['x'] <= px+10 and py-7 <= o['y'] <= py+9]
            esp = {}
            npc = 0
            for o in jan:
                g = o['graphics_id']
                m = re.match(r'OBJ_EVENT_GFX_SPECIES(?:_SHINY|_FEMALE|_SHINY_FEMALE)?\((\w+)\)', g)
                if m:
                    c = custo('SPECIES_' + m.group(1))
                    esp[m.group(1)] = c if c else 112
                else:
                    npc += 8
            tot = sum(esp.values()) + npc
            if tot > pior[0]: pior = (tot, (px, py), sorted(esp.items(), key=lambda t: -t[1]))
    res.append((pior[0], os.path.basename(os.path.dirname(mj)), pior[1], pior[2]))
res.sort(reverse=True)
for tot, nome, pos, esp in res:
    if tot > BUDGET - 150:
        print(f'{tot:5d} {"ESTOURA" if tot > BUDGET else "perto  "} {nome:32s} jogador~{pos} {[(e, c) for e, c in esp]}')
print('mapas com Pokémon de campo:', len(res), ' estouram:', sum(1 for r in res if r[0] > BUDGET), ' orçamento', BUDGET)
