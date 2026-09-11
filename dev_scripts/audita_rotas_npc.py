#!/usr/bin/env python3
"""Quais casos da suíte encostam em célula que um NPC que anda pode ocupar.

Nasceu na integração da onda 5 da frente C, em 11/09/2026, de um vermelho
INTERMITENTE que não era bug do jogo: o T175.4 descia a coluna 44 de Oreburgh e
o `object_event` 13, uma WOMAN_3 de `MOVEMENT_TYPE_WANDER_AROUND` parada em
(43,21) com raio (0,2), estava às vezes no caminho. O caso passava ou falhava
conforme a mulher tivesse andado, que é o pior tipo de teste.

A REGRA DE MOTOR QUE NINGUÉM TINHA LIDO, e que é a raiz disso:
`IsCoordOutsideObjectEventMovementRange` (`src/event_object_movement.c`) só
compara o eixo quando o raio dele é DIFERENTE DE ZERO. **Raio zero num eixo não
quer dizer "não anda nesse eixo": quer dizer SEM LIMITE nesse eixo**, e o único
freio que sobra é a colisão. Em Oreburgh isso leva a conta de células que um NPC
pode ocupar para 457.

O que este script faz: para cada caso da suíte que começa por um `warp` de uma
das cinco cidades copiadas de Sinnoh, ele simula o ANDAR do roteiro (com a regra
do motor de que o primeiro aperto numa direção nova só VIRA) e pergunta se
alguma célula pisada está no alcance de um NPC que anda. Ele NÃO simula o jogo, e
não substitui o emulador: ele aponta o caso que PODE piscar, mesmo estando verde
hoje.

Ele separa duas coisas, e a separação importa:

  * a célula INICIAL de um NPC está sempre ocupada, e vários casos usam isso de
    propósito como anteparo (o T266.1 diz com todas as letras "o próprio NPC é o
    anteparo"). Isso é estável e não é acusado;
  * a célula que o NPC pode ALCANÇAR e nem sempre ocupa é a que faz o caso
    piscar. É essa que sai na lista.

Uso:
    python3 dev_scripts/audita_rotas_npc.py
"""

import json, sys, glob, os
sys.path.insert(0, 'dev_scripts')
import rota_de_teste as R

MAPA_DE = {'MAP_TWINLEAF_TOWN':'TwinleafTown','MAP_SANDGEM_TOWN':'SandgemTown',
           'MAP_FLOAROMA_TOWN':'FloaromaTown','MAP_OREBURGH_CITY':'OreburghCity',
           'MAP_JUBILIFE_CITY':'JubilifeCity'}
DIR={'DOWN':(0,1),'UP':(0,-1),'LEFT':(-1,0),'RIGHT':(1,0)}
cache={}
def mapa(n):
    if n not in cache: cache[n]=R.Mapa(n)
    return cache[n]

def passos(roteiro):
    for parte in roteiro.split(','):
        parte=parte.strip()
        if ':' not in parte: continue
        _, botao = parte.split(':',1)
        rep=1
        if '*' in botao: botao, r = botao.split('*'); rep=int(r)
        botao=botao.strip().rstrip('!')
        if botao in DIR:
            for _ in range(rep): yield botao

achados=[]
for arq in sorted(glob.glob('dev_scripts/testes_criticos/*.json')):
    for c in json.load(open(arq,encoding='utf-8')):
        m=c.get('warp')
        if m not in MAPA_DE: continue
        nome=MAPA_DE[m]
        try: mp=mapa(nome)
        except Exception as e:
            print('pulei', nome, e); continue
        mj=mp.mj
        wid=c.get('warp_id')
        if wid is None or wid>=len(mj.get('warp_events') or []): continue
        w=mj['warp_events'][wid]
        tocadas=set()
        # as DUAS hipóteses de pouso do warp de depuração
        for ini in ((w['x'],w['y']), (w['x'],w['y']+1)):
            x,y=ini; olhando=None
            if not (0<=x<mp.w and 0<=y<mp.h): continue
            tocadas.add((x,y))
            for b in passos(c.get('roteiro','')):
                dx,dy=DIR[b]
                if olhando!=b:
                    olhando=b; continue        # o primeiro aperto só vira
                nx,ny=x+dx,y+dy
                if not (0<=nx<mp.w and 0<=ny<mp.h): break
                if mp.col(nx,ny)!=0: continue
                e1,e2=mp.ele(x,y),mp.ele(nx,ny)
                if not (e1==e2 or e1==0 or e2==0): continue
                x,y=nx,ny; tocadas.add((x,y))
        # a célula INICIAL de um NPC é estável: ela está sempre ocupada, e vários
        # casos usam isso de propósito como anteparo. O que faz caso piscar é a
        # célula que o NPC pode ALCANÇAR e nem sempre ocupa.
        partidas={(e['x'],e['y']) for e in (mj.get('object_events') or [])}
        moveis=mp.occ - partidas
        risco=sorted(tocadas & moveis)
        ancora=sorted(tocadas & partidas)
        if risco:
            achados.append((c['id'], nome, len(risco), risco[:6], len(ancora)))
for a in achados:
    print(f'  PISCA? {a[0]:9} {a[1]:14} {a[2]} célula(s) que um NPC pode ANDAR até, ex.: {a[3]}')
print(f'{len(achados)} caso(s) que encostam em célula móvel de NPC')
