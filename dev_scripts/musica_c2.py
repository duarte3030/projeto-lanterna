#!/usr/bin/env python3
"""Liga a música própria de Galar e Unova aos mapas (c2-musica, 28/10/2026).

Uso:
    python3 dev_scripts/musica_c2.py           # aplica nos map.json
    python3 dev_scripts/musica_c2.py --demo    # portão: nada fora da regra, e a regra pega um mapa trocado
    python3 dev_scripts/musica_c2.py --lista   # mostra mapa, música de antes e música da regra

Galar (piloto aprovado, decisão 139). Nomes de mapa do Ultimate Plus: `Galar_<Lugar><NN>`.
  - rota numerada (`Galar_RouteNNNN`, tipo ROUTE): MUS_GALAR_ROTA1.
  - Wedgehurst: os mapas que tocavam a faixa do exterior da vila: MUS_GALAR_WEDGEHURST.
  - cidades (Motostoke, Turffield, Hulbury, Hammerlocke, Ballonlea, Circhester, Wyndon):
    todo EXTERIOR da cidade (tipo CITY, TOWN ou ROUTE) passa a tocar MUS_GALAR_CIDADE, e
    junto vão casa, loja e prédio que dividiam a faixa da rua (menos faixa de função que o
    hack pôs na rua: ginásio, Victory Road, Pokécenter, laboratório). O resto fica.
  - lote 2 (decisão 154, 28/10/2026):
    - as rotas usam os 4 temas de rota que o banco do Shield tem (r01, r03, r06 e r10; a
      busca exaustiva de `bgm_or_fi_r00` a `r99` só acha esses). Cada tema leva o nome da
      primeira rota do trecho dele: Rotas 1 e 2 ROTA1, 3 a 5 ROTA3, 6 a 9 ROTA6, 10 ROTA10.
      O número sai do `region_map_section` (GALAR_ROUTENN). Que o tema cubra as rotas
      seguintes é presumido.
    - rota de tipo NONE com conexão de mapa também é exterior (Galar_Route1001, a Rota 10
      que liga em Wyndon, e Galar_Route0801, que liga na Rota 7), menos a que toca MUS_NONE.
    - Pokécenter: todo mapa de Galar que tocava MUS_RG_POKE_CENTER toca MUS_GALAR_POKECEN.
    - Wild Area (exteriores, tipo ROUTE): a metade sul, que liga na estação de Wedgehurst
      (Postwick35) e em Motostoke, toca wr01; o resto, que liga em Hammerlocke e Wyndon,
      toca wr02. Qual tema é de qual metade é presumido.
  - DLC (Isle of Armor, Crown Tundra), cavernas, Postwick, Spikemuth e Stow-on-Side ficam
    como estavam: a faixa deles não existe na ROM.
Unova (decisão 138). Faixa pelo que o Black 2 toca no lugar, lido da zonedata da ROM
(a/0/1/2, campos +12 a +18; `fontes-mapas/prd-assets/fase4-musica/unova/zonas_bw2.py`).
Lugar cuja faixa não tem porte limpo (Accumula, Icirrus, Mistralton, Rota 1, Rotas 21 e 22,
Liga, Esgoto de Castelia, Marine Tube) fica como estava.
Mapas cuja música de hoje é de função (Game Corner, Poké Mart, avião, esconderijo) ficam.
"""
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GALAR_CIDADES = ('Motostoke', 'Turffield', 'Hulbury', 'Hammerlocke', 'Ballonlea', 'Circhester', 'Wyndon')
EXTERIOR = ('MAP_TYPE_CITY', 'MAP_TYPE_TOWN', 'MAP_TYPE_ROUTE')
# faixa de função que o Ultimate Plus pôs num exterior não puxa os interiores que a dividem
NAO_PUXA = {'MUS_NONE', 'MUS_RG_GYM', 'MUS_RG_VICTORY_ROAD', 'MUS_RG_POKE_CENTER', 'MUS_RG_OAK_LAB'}
# tema de rota por número de rota (lote 2): o tema vale da rota dele até a seguinte da lista
ROTA_TEMA = ((10, 'MUS_GALAR_ROTA10'), (6, 'MUS_GALAR_ROTA6'), (3, 'MUS_GALAR_ROTA3'), (1, 'MUS_GALAR_ROTA1'))
# metade sul da Wild Area (liga em Postwick35, a estação, e em Motostoke); o resto é a metade norte
WILD_AREA_SUL = {3, 4, 5, 6, 7, 8, 9, 15}

# (regex no nome sem o prefixo `Unova_`, faixa do Black 2 ou None = não mexe). Primeira que casa vale.
UNOVA = [
    (r'^PkmnLeague', None),
    (r'Pokecenter(\d*F)?$', 'POKECEN'),
    (r'Gym(\d*F|B\d*F)?$', 'GYM'),
    (r'Gate$', 'GATE'),
    (r'^Aspertia', 'SW_C_12'),
    (r'^CasteliaSewers', None),
    (r'^Castelia', 'C_03'),
    (r'^CelestialTower', 'D_05'),
    (r'^ChargestoneCave', 'D_02'),
    (r'^DesertResort', 'D_02'),
    (r'^DragonspiralTower', 'D_05'),
    (r'^Dreamyard', 'D_01'),
    (r'^DriftveilDrawbridge', 'H_02'),
    (r'^Driftveil', 'SW_C_5_NEW'),
    (r'^FloccesyRanch', None),
    (r'^Floccesy', 'SW_T_06'),
    (r'^GiantChasm', 'D_05'),
    (r'^Humilau', 'SW_C_14'),
    (r'^Lacunosa', 'T_04'),
    (r'^Lentimas', 'SW_T_07'),
    (r'^LostlornForest', 'D_06'),
    (r'^MistraltonCave', 'D_02'),
    (r'^MoorOfIcirrus', 'D_01'),
    (r'^NacreneOutskirt', None),
    (r'^Nacrene', 'C_02'),
    (r'^NimbasaPark(Basement|CoasterRoom|Runway)', None),
    (r'^Nimbasa', 'C_04'),
    (r'^NsRoom', 'SW_D_N_ROOM'),
    (r'^NuvemaLab', 'LABO'),
    (r'^Nuvema', 'T_01'),
    (r'^Opelucid', 'C_08_W'),
    (r'^P2Lab', 'D_03'),
    (r'^PWTOutside', 'SW_C_5_NEW'),
    (r'^PWT(Inside|Hallway|QualifierRoom|BackRoom)', 'WBT_LOBBY'),
    (r'^PinwheelForest', 'D_01'),
    (r'^RelicCastle', 'D_04'),
    (r'^RelicPassage', 'D_02'),
    (r'^ReversalMountain', 'SW_D_24_B'),
    (r'^SeasideCave', 'D_02'),
    (r'^SkyarrowBridge', 'H_01'),
    (r'^StrangeHouse', 'SW_D_25'),
    (r'^Striaton', 'C_01'),
    (r'^TubelineBridge', 'H_03'),
    (r'^TwistMountain', 'D_03'),
    (r'^Undella', 'T_05_SU'),
    (r'^VictoryRoad', 'D_CHAMPROAD'),
    (r'^VillageBridge', 'H_04'),
    (r'^VirbankComplex', None),
    (r'^Virbank', 'SW_C_13'),
    (r'^WellspringCave', 'D_02'),
    (r'^Rt(2|3)(?!\d)', 'R_B_SP'),
    (r'^Rt(4|5|16)(?!\d)', 'R_C_SU'),
    (r'^Rt(6|7|8|9|17|18)(?!\d)', 'R_D_SP'),
    (r'^Rt(11|12|13|14|15)(?!\d)', 'R_E_SP'),
    (r'^Rt(19|20)(?!\d)', 'SW_R_19_SP'),
    (r'^Rt23', 'SW_R_23'),
]
FUNCAO = {'MUS_GAME_CORNER', 'MUS_POKE_MART', 'MUS_CABLE_CAR', 'MUS_RG_ROCKET_HIDEOUT', 'MUS_RG_GAME_CORNER'}


def le_mapas():
    g = json.load(open(os.path.join(RAIZ, 'data/maps/map_groups.json')))
    out = {}
    for grp in g['group_order']:
        for n in g[grp]:
            if n.startswith(('Galar_', 'Unova_')):
                p = os.path.join(RAIZ, 'data/maps', n, 'map.json')
                out[n] = (p, json.load(open(p)))
    return out


def regra(mapas, base):
    """{mapa: música da regra}. `base` é a música de ANTES (a regra de Galar lê o exterior)."""
    alvo = {}
    ext = {}
    for n, (_, m) in mapas.items():
        mm = re.match(r'^Galar_([A-Za-z]+?)(\d+)$', n)
        if mm and m.get('map_type') in EXTERIOR and base[n] not in NAO_PUXA:
            ext.setdefault(mm.group(1), set()).add(base[n])
    for n, (_, m) in mapas.items():
        b = base[n]
        if n.startswith('Galar_'):
            mm = re.match(r'^Galar_([A-Za-z]+?)(\d+)$', n)
            if not mm:
                continue
            lugar = mm.group(1)
            if b == 'MUS_RG_POKE_CENTER':
                alvo[n] = 'MUS_GALAR_POKECEN'
            elif lugar == 'Route' and (m.get('map_type') == 'MAP_TYPE_ROUTE' or (m.get('connections') and b != 'MUS_NONE')):
                num = int(re.match(r'MAPSEC_GALAR_ROUTE(\d+)$', m['region_map_section']).group(1))
                alvo[n] = next(t for r, t in ROTA_TEMA if num >= r)
            elif lugar == 'WildArea' and m.get('map_type') == 'MAP_TYPE_ROUTE':
                alvo[n] = 'MUS_GALAR_AREA_SELVAGEM1' if int(mm.group(2)) in WILD_AREA_SUL else 'MUS_GALAR_AREA_SELVAGEM2'
            elif lugar == 'Wedgehurst' and (b in ext.get(lugar, ()) or m.get('map_type') in EXTERIOR):
                alvo[n] = 'MUS_GALAR_WEDGEHURST'
            elif lugar in GALAR_CIDADES and (b in ext.get(lugar, ()) or m.get('map_type') in EXTERIOR):
                alvo[n] = 'MUS_GALAR_CIDADE'
        else:
            if b in FUNCAO:
                continue
            nome = n[len('Unova_'):]
            for rx, seq in UNOVA:
                if re.search(rx, nome):
                    if seq:
                        alvo[n] = 'MUS_UNOVA_' + seq
                    break
    return alvo


ANTES = os.path.join(RAIZ, 'dev_scripts/musica_c2_antes.json')


def base_de(mapas):
    """Música de ANTES desta frente: a gravada em musica_c2_antes.json (mapas que a regra
    já trocou) ou, para os outros, a do map.json."""
    antes = json.load(open(ANTES)) if os.path.exists(ANTES) else {}
    return {n: antes.get(n, m['music']) for n, (_, m) in mapas.items()}


def grava(p, novo):
    txt = open(p).read()
    txt2 = re.sub(r'"music": "[A-Z0-9_]+"', f'"music": "{novo}"', txt, count=1)
    if txt2 != txt:
        open(p, 'w').write(txt2)


def confere(mapas, alvo, base, consts):
    ruins = []
    for n, (_, m) in mapas.items():
        esperado = alvo.get(n, base[n])
        if m['music'] != esperado:
            ruins.append(f'{n}: music={m["music"]}, a regra pede {esperado}')
        if esperado.startswith(('MUS_GALAR_', 'MUS_UNOVA_')) and esperado not in consts:
            ruins.append(f'{n}: {esperado} não existe em include/constants/songs.h')
    return ruins


def main():
    mapas = le_mapas()
    base = base_de(mapas)
    alvo = regra(mapas, base)
    consts = set(re.findall(r'#define (MUS_(?:GALAR|UNOVA)_\w+)', open(os.path.join(RAIZ, 'include/constants/songs.h')).read()))
    if '--lista' in sys.argv:
        for n in sorted(alvo):
            print(f'{n:45} {base[n]:28} -> {alvo[n]}')
        return 0
    if '--demo' in sys.argv:
        ruins = confere(mapas, alvo, base, consts)
        for r in ruins[:20]:
            print('  ', r)
        g = sum(1 for n in alvo if n.startswith('Galar_')); u = len(alvo) - g
        print(f'música de região: {g} mapas de Galar e {u} de Unova pela regra; fora da regra: {len(ruins)}')
        # prova de que o portão morde: um mapa da regra com a música de antes tem que reprovar
        n0 = sorted(alvo)[0]
        p, m = mapas[n0]
        falso = dict(mapas); falso[n0] = (p, dict(m, music=base[n0]))
        if not confere(falso, alvo, base, consts):
            print('o portão NÃO pegou um mapa trocado; ele está cego')
            return 1
        return 1 if ruins or not alvo else 0
    n_mud = 0
    for n, (p, m) in mapas.items():
        novo = alvo.get(n, base[n])
        if m['music'] != novo:
            grava(p, novo); n_mud += 1
    json.dump({n: base[n] for n in sorted(alvo)}, open(ANTES, 'w'), indent=1)
    print(f'{n_mud} mapas mudaram; {len(alvo)} pela regra')
    return 0


if __name__ == '__main__':
    sys.exit(main())
