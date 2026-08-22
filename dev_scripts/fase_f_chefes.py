#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fase F: escreve os times de chefe em src/data/trainers.party a partir de
dev_scripts/fase_f_chefes.json, que e a FONTE DA VERDADE.

Escopo: lider de ginasio, rival, Elite Four, campeao e CHEFE DE EQUIPE VILA
(papel "vilao": Rocket, Magma, Aqua, Galactica, Plasma) das cinco regioes
(Kanto, Johto, Hoenn, Sinnoh, Unova). Treinador comum NAO entra; Galar nao tem
treinador.

Ao contrario de dev_scripts/gens69_treinadores.py, este script E IDEMPOTENTE:
ele SUBSTITUI o time inteiro da batalha pelo que a tabela diz, entao rodar duas
vezes seguidas da diferenca zero. Nada aqui olha "tem vaga".

Uso:
    python3 dev_scripts/fase_f_chefes.py --dry-run   # tabela por regiao, sem tocar em nada
    python3 dev_scripts/fase_f_chefes.py --demo      # planta mutacoes e prova que o guarda reprova
    python3 dev_scripts/fase_f_chefes.py --aplicar   # escreve src/data/trainers.party

O guarda (valida) reprova, entre outras coisas: time com mais de 6 Pokemon,
pedra de Mega no Pokemon que nao tem Mega, lendario repetido dentro da regiao,
batalha com ace acima do nivel 40 sem lendario, mais de 5 chefes com Dynamax
ou mais de 6 com Terastal no jogo inteiro, e chefe de equipe vila sem TEMA
declarado ou com time fora do tema que ele mesmo declarou.
"""
import argparse
import collections
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = os.path.join(RAIZ, 'dev_scripts', 'fase_f_chefes.json')
PARTY = os.path.join(RAIZ, 'src', 'data', 'trainers.party')

MAX_DYNAMAX = 5
MAX_TERA = 6
NIVEL_LENDARIO = 40

CHAVES_CABECALHO = ('Name', 'Class', 'Pic', 'Back Pic', 'Gender', 'Music', 'Items',
                    'Battle Type', 'Double Battle', 'AI', 'Mugshot', 'Starting Status',
                    'Difficulty', 'Party Size', 'Multi Party', 'Pool Rules',
                    'Pool Pick Functions', 'Pool Prune')


# ---------------------------------------------------------------- leitura do motor
def megas_do_motor():
    """{SPECIES_BASE: {ITEM_PEDRA, ...}} lido de form_change_tables.h, nao de memoria."""
    caminho = os.path.join(RAIZ, 'src', 'data', 'pokemon', 'form_change_tables.h')
    texto = open(caminho, encoding='utf-8', errors='replace').read()
    mapa = collections.defaultdict(set)
    padrao = r'FORM_CHANGE_BATTLE_MEGA_EVOLUTION_ITEM,\s*(SPECIES_[A-Z0-9_]+),\s*(ITEM_[A-Z0-9_]+)'
    for forma, item in re.findall(padrao, texto):
        base = re.sub(r'_MEGA(_[XYZ])?$', '', forma)
        mapa[base].add(item)
    return mapa


def cristais_z():
    texto = open(os.path.join(RAIZ, 'include', 'constants', 'items.h'), encoding='utf-8').read()
    return set(re.findall(r'\b(ITEM_[A-Z]+IUM_Z[A-Z_]*)\b', texto))


def orbes_do_motor():
    """{SPECIES_BASE: {ITEM_ORBE, ...}} lido de form_change_tables.h.

    A Primal Reversion NAO e gimmick para o motor, e isso foi MEDIDO em
    22/08/2026, nao lembrado:

    - ela nao esta no `enum Gimmick` (include/battle_gimmick.h:4, que so tem
      MEGA, ULTRA_BURST, Z_MOVE, DYNAMAX e TERA);
    - ela roda sozinha ao entrar em campo (src/battle_switch_in.c:276 chama
      TryPrimalReversion no bloco FIRST_EVENT_BLOCK_GENERAL_ABILITIES), sem
      botao e sem escolha do treinador;
    - ela nunca chama SetActiveGimmick nem SetGimmickAsActivated (a varredura
      dos dois so acha battle_z_move.c, battle_dynamax.c, battle_terastal.c,
      battle_ai_util.c e as duas de Mega/Ultra Burst em battle_util.c:8496 e
      :8514).

    Consequencia: `CanMegaEvolve` (src/battle_util.c:8418) segue devolvendo
    TRUE para o ace com pedra depois do Groudon reverter, porque nem
    HasTrainerUsedGimmick(GIMMICK_MEGA) nem GetActiveGimmick veem a Primal.
    Mega e Primal CONVIVEM na mesma batalha, e por isso o orbe nao gasta o
    "um gimmick por chefe": o guarda o conhece para exigir que ele esteja na
    especie certa, e nada alem disso.
    """
    caminho = os.path.join(RAIZ, 'src', 'data', 'pokemon', 'form_change_tables.h')
    texto = open(caminho, encoding='utf-8', errors='replace').read()
    mapa = collections.defaultdict(set)
    padrao = r'FORM_CHANGE_BATTLE_PRIMAL_REVERSION,\s*(SPECIES_[A-Z0-9_]+),\s*(ITEM_[A-Z0-9_]+)'
    for forma, item in re.findall(padrao, texto):
        mapa[re.sub(r'_PRIMAL$', '', forma)].add(item)
    return mapa


def primal_ligada():
    """A tabela de formas fica atras de `#if P_PRIMAL_REVERSIONS`; se alguem
    desligar o config, o orbe vira item morto e o time perde um Pokemon de fato
    sem erro de compilacao nenhum."""
    caminho = os.path.join(RAIZ, 'include', 'config', 'species_enabled.h')
    texto = open(caminho, encoding='utf-8').read()
    m = re.search(r'#define\s+P_PRIMAL_REVERSIONS\s+(TRUE|FALSE)', texto)
    return bool(m) and m.group(1) == 'TRUE'


def tipos_do_motor():
    """{SPECIES_X: ('TYPE_A', 'TYPE_B')} lido do species_info pelo catalogo_especies.

    Especie escrita por MACRO nao aparece la (medido em 22/08/2026: Genesect,
    Darmanitan e Sawsbuck estao fora; o Gengar TEM tipos e so a habilidade dele e
    que nao da para ler). Quem some conta como FORA do tema, que e o lado seguro:
    erra para o lado de reprovar, nunca para o de aprovar em silencio.
    """
    sys.path.insert(0, os.path.join(RAIZ, 'dev_scripts'))
    import catalogo_especies
    return {n: e.tipos for n, e in catalogo_especies.carrega().items()}


# ---------------------------------------------------------------- guarda
def valida(doc):
    """Devolve a lista de reprovacoes. Lista vazia = tabela sadia."""
    erros = []
    mega = megas_do_motor()
    zs = cristais_z()
    tipos = tipos_do_motor()
    orbes = orbes_do_motor()
    itens_mega = {i for v in mega.values() for i in v}
    itens_orbe = {i for v in orbes.values() for i in v}
    if itens_orbe and not primal_ligada():
        erros.append('P_PRIMAL_REVERSIONS esta FALSE: nenhum orbe reverte nada')
    por_regiao = collections.defaultdict(lambda: collections.defaultdict(set))
    conta = collections.Counter()

    for c in doc['chefes']:
        tid = c['id']
        time = c['time']
        if not 1 <= len(time) <= 6:
            erros.append('%s: time com %d Pokemon (o motor so carrega 6)' % (tid, len(time)))
        gs = c['gimmick_slot']
        if not 0 <= gs < len(time):
            erros.append('%s: gimmick_slot %d fora do time' % (tid, gs))
            continue
        gim = c['gimmick']
        conta[gim] += 1
        item_gim = time[gs]['item']
        esp_gim = time[gs]['especie']

        if gim == 'mega' and item_gim not in mega.get(esp_gim, set()):
            erros.append('%s: pedra de Mega %s em %s, que nao tem essa Mega'
                         % (tid, item_gim, esp_gim))
        if gim == 'z' and item_gim not in zs:
            erros.append('%s: gimmick Z mas o item e %s' % (tid, item_gim))
        if gim == 'dynamax' and time[gs].get('dynamax') is None:
            erros.append('%s: gimmick Dynamax sem "Dynamax Level" no slot' % tid)
        if gim == 'tera' and not time[gs].get('tera'):
            erros.append('%s: gimmick Terastal sem "Tera Type" no slot' % tid)

        for i, m in enumerate(time):
            gimm_aqui = (i == gs and gim in ('mega', 'z', 'dynamax', 'tera'))
            if not gimm_aqui and (m['item'] in itens_mega or m['item'] in zs):
                erros.append('%s: %s carrega gimmick %s fora do slot do gimmick'
                             % (tid, m['especie'], m['item']))
            # O orbe de Primal e a UNICA excecao a linha de cima, e de proposito:
            # ele nao entra em itens_mega nem em zs, entao nunca cai naquele erro.
            # Ele pode viver em qualquer slot, inclusive ao lado do slot do
            # gimmick, porque o motor deixa (ver orbes_do_motor). O que o guarda
            # cobra e so que ele esteja na especie que tem Primal.
            if m['item'] in itens_orbe and m['item'] not in orbes.get(m['especie'], set()):
                erros.append('%s: orbe %s em %s, que nao tem Primal Reversion'
                             % (tid, m['item'], m['especie']))
            if not gimm_aqui and (m.get('dynamax') or m.get('tera')):
                erros.append('%s: %s tem Dynamax/Tera fora do slot do gimmick'
                             % (tid, m['especie']))
            if len(m['golpes']) != 4:
                erros.append('%s: %s com %d golpes' % (tid, m['especie'], len(m['golpes'])))

        if c['papel'] == 'vilao':
            tema = c.get('tema')
            if not tema:
                erros.append('%s: chefe de equipe vila sem tema declarado' % tid)
            else:
                dentro = sum(1 for m in time
                             if set(tipos.get(m['especie'], ())) & set(tema))
                if dentro * 2 < len(time):
                    erros.append('%s: so %d de %d no tema %s da equipe %s'
                                 % (tid, dentro, len(time),
                                    '/'.join(t.replace('TYPE_', '') for t in tema),
                                    c.get('equipe', '?')))

        lend = c['lendario']
        if c['ace'] > NIVEL_LENDARIO and lend is None:
            erros.append('%s: ace no nivel %d (acima de %d) e sem lendario'
                         % (tid, c['ace'], NIVEL_LENDARIO))
        if c['ace'] <= NIVEL_LENDARIO and lend is not None:
            erros.append('%s: ace no nivel %d e ganhou lendario %s' % (tid, c['ace'], lend))
        if lend is not None:
            if lend not in [m['especie'] for m in time]:
                erros.append('%s: lendario %s declarado e ausente do time' % (tid, lend))
            por_regiao[c['regiao']][lend].add(c['identidade'])

    for regiao, mapa in sorted(por_regiao.items()):
        for lend, quem in sorted(mapa.items()):
            if len(quem) > 1:
                erros.append('%s: lendario %s repetido entre %s'
                             % (regiao, lend, ', '.join(sorted(quem))))

    if conta['dynamax'] > MAX_DYNAMAX:
        erros.append('Dynamax em %d chefes; o teto e %d' % (conta['dynamax'], MAX_DYNAMAX))
    if conta['tera'] > MAX_TERA:
        erros.append('Terastal em %d chefes; o teto e %d' % (conta['tera'], MAX_TERA))
    return erros


# ---------------------------------------------------------------- escrita
def bloco_do_mon(m):
    linhas = ['%s @ %s' % (m['especie'], m['item'])]
    linhas.append('Level: %d' % m['nivel'])
    if m.get('habilidade'):
        linhas.append('Ability: %s' % m['habilidade'])
    linhas.append('Nature: %s' % m['natureza'])
    linhas.append('IVs: %s' % m['ivs'])
    linhas.append('EVs: %s' % m['evs'])
    if m.get('dynamax') is not None:
        linhas.append('Dynamax Level: %d' % m['dynamax'])
    if m.get('tera'):
        linhas.append('Tera Type: %s' % m['tera'])
    linhas += ['- %s' % g for g in m['golpes']]
    return linhas


def fatia_bloco(corpo):
    """(cabecalho, rabeira) do corpo de um bloco === TRAINER_X ===.

    A rabeira sao os comentarios e linhas em branco que vivem no FIM do bloco;
    eles marcam o comeco do proximo lote gerado por outro script e nao podem
    sumir. O CPP os apaga antes do trainerproc, mas o arquivo e lido por gente.
    """
    linhas = corpo.split('\n')
    cabecalho = []
    for ln in linhas:
        s = ln.strip()
        if not s:
            break
        m = re.match(r'^([A-Z][A-Za-z. ]*?):\s*(.*)$', s)
        if m and m.group(1) in CHAVES_CABECALHO:
            cabecalho.append((m.group(1), m.group(2)))
        else:
            break
    # rabeira: do fim para tras, linhas em branco e blocos de comentario
    fim = len(linhas)
    dentro = False
    ultimo_util = -1
    for i, ln in enumerate(linhas):
        s = ln.strip()
        if dentro:
            if '*/' in s:
                dentro = False
            continue
        if s.startswith('/*'):
            if '*/' not in s:
                dentro = True
            continue
        if s.startswith('//') or not s:
            continue
        ultimo_util = i
    for i in range(ultimo_util + 1, len(linhas)):
        if linhas[i].strip():
            fim = i
            break
    rabeira = linhas[fim:] if fim < len(linhas) else []
    while rabeira and not rabeira[-1].strip():
        rabeira.pop()
    return cabecalho, rabeira


def escreve(doc, texto):
    porid = {c['id']: c for c in doc['chefes']}
    inicios = [(m.start(), m.group(1), m.end())
               for m in re.finditer(r'(?m)^=== (\S+) ===[ \t]*$', texto)]
    pedacos = []
    fim_anterior = 0
    tocados = 0
    for i, (pos, tid, fim_cab) in enumerate(inicios):
        if tid not in porid:
            continue
        fim_bloco = inicios[i + 1][0] if i + 1 < len(inicios) else len(texto)
        corpo = texto[fim_cab + 1:fim_bloco]
        cabecalho, rabeira = fatia_bloco(corpo)
        c = porid[tid]
        novo = []
        viu_ai = False
        for chave, valor in cabecalho:
            if chave == 'AI':
                novo.append('AI: %s' % ' / '.join(c['ai']))
                viu_ai = True
            else:
                novo.append('%s: %s' % (chave, valor))
        if not viu_ai:
            novo.append('AI: %s' % ' / '.join(c['ai']))
        for m in c['time']:
            novo.append('')
            novo += bloco_do_mon(m)
        novo.append('')
        if rabeira:
            novo += rabeira
            novo.append('')
        pedacos.append(texto[fim_anterior:fim_cab + 1])
        pedacos.append('\n'.join(novo) + '\n')
        fim_anterior = fim_bloco
        tocados += 1
    pedacos.append(texto[fim_anterior:])
    return ''.join(pedacos), tocados


# ---------------------------------------------------------------- relatorio
def dry_run(doc):
    porregiao = collections.OrderedDict()
    for c in doc['chefes']:
        porregiao.setdefault(c['regiao'], []).append(c)
    print('%-8s %6s %5s %5s %5s %5s %5s %6s %5s %5s %5s  %s'
          % ('regiao', 'chefes', 'lider', 'rival', 'e4', 'camp', 'vilao', 'lendas',
             'mega', 'z', 'dmax/tera', 'ace min-max'))
    for regiao, lista in porregiao.items():
        papel = collections.Counter(c['papel'] for c in lista)
        gim = collections.Counter(c['gimmick'] for c in lista)
        aces = [c['ace'] for c in lista]
        lendas = len({c['lendario'] for c in lista if c['lendario']})
        print('%-8s %6d %5d %5d %5d %5d %5d %6d %5d %5d %4d/%-4d  %d-%d'
              % (regiao, len(lista), papel['lider'], papel['rival'], papel['e4'],
                 papel['campeao'] + papel['superchefe'], papel['vilao'], lendas,
                 gim['mega'], gim['z'], gim['dynamax'], gim['tera'], min(aces), max(aces)))
    tot = collections.Counter(c['gimmick'] for c in doc['chefes'])
    print('\ntotal: %d batalhas, %d Pokemon, Dynamax em %d (teto %d), Terastal em %d (teto %d)'
          % (len(doc['chefes']), sum(len(c['time']) for c in doc['chefes']),
             tot['dynamax'], MAX_DYNAMAX, tot['tera'], MAX_TERA))
    print('acima do nivel %d e portanto com lendario: %d batalhas; abaixo, sem lendario: %d'
          % (NIVEL_LENDARIO,
             sum(1 for c in doc['chefes'] if c['ace'] > NIVEL_LENDARIO),
             sum(1 for c in doc['chefes'] if c['ace'] <= NIVEL_LENDARIO)))
    print('\nlendario por chefe:')
    for regiao, lista in porregiao.items():
        vistos = collections.OrderedDict()
        for c in lista:
            if c['lendario']:
                vistos.setdefault(c['identidade'], c['lendario'])
        if vistos:
            print('  %-7s %s' % (regiao, ', '.join('%s=%s' % (k, v.replace('SPECIES_', ''))
                                                   for k, v in vistos.items())))


def demo(doc):
    """Cinco mutacoes plantadas. Cada uma TEM de reprovar, senao o guarda e enfeite."""
    base = valida(doc)
    if base:
        print('DEMO ABORTADA: a tabela de verdade ja esta reprovando:')
        for e in base:
            print('  ' + e)
        return 1

    def copia():
        return json.loads(json.dumps(doc))

    casos = []

    d = copia()
    alvo = d['chefes'][0]
    alvo['time'].append(json.loads(json.dumps(alvo['time'][0])))
    alvo['time'].append(json.loads(json.dumps(alvo['time'][0])))
    casos.append(('time com 7 Pokemon', d))

    d = copia()
    for c in d['chefes']:
        if c['gimmick'] == 'mega':
            c['time'][c['gimmick_slot']]['item'] = 'ITEM_SABLENITE'
            break
    casos.append(('pedra de Mega no Pokemon errado', d))

    d = copia()
    reg = {}
    for c in d['chefes']:
        if c['lendario']:
            k = c['regiao']
            if k in reg and reg[k][1] != c['identidade']:
                c['lendario'] = reg[k][0]
                c['time'][-1]['especie'] = reg[k][0]
                break
            reg.setdefault(k, (c['lendario'], c['identidade']))
    casos.append(('lendario repetido na regiao', d))

    d = copia()
    for c in d['chefes']:
        if c['ace'] > NIVEL_LENDARIO:
            c['lendario'] = None
            break
    casos.append(('ace acima de %d sem lendario' % NIVEL_LENDARIO, d))

    d = copia()
    dados = 0
    for c in d['chefes']:
        if c['gimmick'] == 'mega' and dados < MAX_DYNAMAX + 1:
            c['gimmick'] = 'dynamax'
            c['time'][c['gimmick_slot']]['item'] = 'ITEM_LEFTOVERS'
            c['time'][c['gimmick_slot']]['dynamax'] = 10
            dados += 1
    casos.append(('Dynamax acima do teto de %d' % MAX_DYNAMAX, d))

    d = copia()
    dados = 0
    for c in d['chefes']:
        if c['gimmick'] == 'mega' and dados < MAX_TERA + 1:
            c['gimmick'] = 'tera'
            c['time'][c['gimmick_slot']]['item'] = 'ITEM_LEFTOVERS'
            c['time'][c['gimmick_slot']]['tera'] = 'TYPE_STEEL'
            dados += 1
    casos.append(('Terastal acima do teto de %d' % MAX_TERA, d))

    # Os tres de baixo sao os que a rodada dos vilaes trouxe. Sem eles o papel
    # "vilao" entraria sem tema nenhum e ninguem reclamaria.
    d = copia()
    for c in d['chefes']:
        if c['papel'] == 'vilao':
            c.pop('tema', None)
            break
    casos.append(('vilao sem tema declarado', d))

    d = copia()
    for c in d['chefes']:
        if c['papel'] == 'vilao':
            # Magikarp em tudo MENOS no slot do gimmick: trocar o ace tambem faria
            # a pedra de Mega reprovar primeiro e o caso passaria pelo motivo
            # errado, que e como um guarda de enfeite se disfarca de guarda.
            for i, m in enumerate(c['time']):
                if i != c['gimmick_slot']:
                    m['especie'] = 'SPECIES_MAGIKARP'
            c['lendario'] = None
            c['ace'] = NIVEL_LENDARIO
            break
    casos.append(('vilao com o time fora do tema que ele declarou', d))

    d = copia()
    donos = {}
    for c in d['chefes']:
        if c['papel'] != 'vilao' and c['lendario']:
            donos.setdefault((c['regiao'], c['identidade']), c['lendario'])
    for c in d['chefes']:
        if c['papel'] == 'vilao' and c['lendario']:
            roubo = next((v for (r, _), v in donos.items() if r == c['regiao']), None)
            if roubo:
                i = [m['especie'] for m in c['time']].index(c['lendario'])
                c['lendario'] = roubo
                c['time'][i]['especie'] = roubo
                break
    casos.append(('vilao com o lendario de um lider da mesma regiao', d))

    # O de baixo nasceu com a Primal do Maxie e do Archie (22/08/2026). Sem ele o
    # orbe passaria calado em qualquer bicho, porque orbe nao e pedra de Mega nem
    # cristal Z e nenhuma das duas varreduras de antes o enxergava.
    d = copia()
    orbes = orbes_do_motor()
    algum_orbe = sorted(i for v in orbes.values() for i in v)
    for c in d['chefes']:
        # fora do slot do gimmick, senao a pedra de Mega reprovaria primeiro e o
        # caso passaria pelo motivo errado
        errado = next((m for i, m in enumerate(c['time'])
                       if i != c['gimmick_slot'] and m['especie'] not in orbes), None)
        if algum_orbe and errado:
            errado['item'] = algum_orbe[0]
            break
    casos.append(('orbe de Primal na especie que nao tem Primal', d))

    ruim = 0
    for nome, mutante in casos:
        erros = valida(mutante)
        if erros:
            print('OK   %-42s reprovado: %s' % (nome, erros[0]))
        else:
            print('FALHA %-42s PASSOU e nao devia' % nome)
            ruim += 1
    print('\ndemo: %d/%d mutacoes reprovadas' % (len(casos) - ruim, len(casos)))
    return 1 if ruim else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--demo', action='store_true')
    ap.add_argument('--aplicar', action='store_true')
    args = ap.parse_args()
    doc = json.load(open(JSON, encoding='utf-8'))

    if args.demo:
        return demo(doc)

    erros = valida(doc)
    if erros:
        print('TABELA REPROVADA (%d):' % len(erros))
        for e in erros:
            print('  ' + e)
        return 1

    if args.dry_run or not args.aplicar:
        dry_run(doc)
        return 0

    texto = open(PARTY, encoding='utf-8').read()
    novo, tocados = escreve(doc, texto)
    if tocados != len(doc['chefes']):
        print('ERRO: a tabela tem %d chefes e o arquivo so casou %d'
              % (len(doc['chefes']), tocados))
        return 1
    if novo == texto:
        print('nada a fazer: %d chefes ja estao como a tabela manda' % tocados)
        return 0
    open(PARTY, 'w', encoding='utf-8').write(novo)
    print('escrevi %d chefes em %s' % (tocados, os.path.relpath(PARTY, RAIZ)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
