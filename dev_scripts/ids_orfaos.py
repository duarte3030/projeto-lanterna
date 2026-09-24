#!/usr/bin/env python3
"""Ids de treinador ÓRFÃOS: prova negativa, reserva da frente Hoenn EX e guarda.

POR QUE EXISTE (23/09/2026, frente Hoenn EX, decisão do Fable no checkpoint da
onda 0): a frente precisa de ~145 ids de treinador novos e só existem 89 ids
livres abaixo do teto (2.200), 35 deles reservados a Johto. Subir
MAX_TRAINERS_COUNT quebra save (a flag de "já venci" é TRAINER_FLAGS_START + id),
então a saída aprovada é REUSAR id órfão: id definido que nenhum mapa, script,
tabela ou caso de teste referencia. A flag desse id nunca acende em jogo
nenhum, e por isso dar o número a outro treinador é invisível para qualquer
save.

"Nenhuma referência" tem de ser PROVADO, não presumido. Este script prova por
NÚMERO, não por nome, porque os dois cabeçalhos (`opponents.h` e
`opponents_frlg.h`) são incluídos juntos no build do Emerald e 150 números têm
dois nomes (13 é TRAINER_ED de Hoenn e TRAINER_YOUNGSTER_BEN_2 de Kanto). Um
número só é órfão se TODOS os nomes dele estiverem mudos.

Onde procura (as três fontes cruzadas da decisão, mais os testes):
  1. `data/**` inteiro (mapas: scripts.inc e map.json; scripts; tabelas .inc/.s).
  2. `src/**` e `include/**` (inclusive `src/data/*.party`, rematch, Match Call,
     Trainer Hill, Frontier, `chapter_jump.c`, tabelas geradas que estão no git).
  3. `dev_scripts/**` (Fase F `fase_f_chefes.json`, JSON gerados, geradores .py
     que citam nome, e `dev_scripts/testes_criticos/*.json`), `test/**`,
     `tools/**`, `asm/**`, `constants/**` e os `*.mk` da raiz.
O que NÃO conta como referência (é a própria definição):
  - a linha `#define TRAINER_X N` em `opponents.h`/`opponents_frlg.h`;
  - o cabeçalho `=== TRAINER_X ===` do bloco de time dele em qualquer `.party`.
Referência por número cru, além do nome:
  - flag de vitória crua em hexadecimal (`0x500 + id`, ex. `0xA4C`) em `data/**`
    e nos casos de teste;
  - `FlagSet/FlagGet/FlagClear` com literal em `src/**`;
  - `"oponente": <int>` e flag inteira (`0x500 + id`) nos casos de teste;
  - `trainerbattle*`/`*_defeated`/`*trainerflag` com número cru em `data/**`.
Macro que cola nome (`TRAINER_##x`): o script conta e recusa se existir (hoje: 0).

Uso:
    python3 dev_scripts/ids_orfaos.py                 # censo e resumo
    python3 dev_scripts/ids_orfaos.py --prova         # prova negativa, id a id
    python3 dev_scripts/ids_orfaos.py --gera-reserva  # escreve hoennex_reserva_ids.json
    python3 dev_scripts/ids_orfaos.py --guarda        # portão (antes_de_empurrar.sh)
    python3 dev_scripts/ids_orfaos.py --autoteste

A GUARDA (vermelho = sai 1), para cada id da reserva da frente:
  a) todo nome ANTIGO do órfão continua sem referência nenhuma (definição à parte);
  b) todo nome que hoje tem esse número é um nome antigo do órfão ou um
     `TRAINER_HOENNEX_*` definido DENTRO do bloco da reserva no `opponents.h`;
  c) nenhum número da reserva tem dois `TRAINER_HOENNEX_*` (colisão entre lotes);
  d) o número tem no máximo um bloco `=== ... ===` em `src/data/trainers.party`;
  e) nenhum `TRAINER_HOENNEX_*` usa número FORA da reserva (nem dos livres dela).

COMO REUSAR UM ÓRFÃO (receita para os lotes): escolha o id na sua faixa do JSON;
apague a linha `#define` antiga e o bloco `=== TRAINER_ANTIGO ===` de
`src/data/trainers.party`; escreva `#define TRAINER_HOENNEX_<NOME> <id>` dentro
do bloco da reserva no `opponents.h` e o bloco novo no `.party`. Se o nome antigo
morar no `opponents_frlg.h` (Kanto), apague a linha de lá do mesmo jeito: o
`trainers_frlg.party` é acervo e não compila no Emerald. Rode `--guarda`.
"""
import argparse
import collections
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CABECALHOS = ('include/constants/opponents.h', 'include/constants/opponents_frlg.h')
PARTY_COMPILADO = 'src/data/trainers.party'
RESERVA = 'dev_scripts/hoennex_reserva_ids.json'
TETO = 2200               # MAX_TRAINERS_COUNT_EMERALD
FLAG_BASE = 0x500         # TRAINER_FLAGS_START
PREFIXO_NOVO = 'TRAINER_HOENNEX_'
MARCA_INI = '// >>> RESERVA DE IDS DA FRENTE HOENN EX'
MARCA_FIM = '// <<< RESERVA DE IDS DA FRENTE HOENN EX'
# Faixas que NÃO entram na reserva mesmo órfãs: pertencem a outra frente.
FAIXAS_DE_OUTROS = [(2157, 2199, 'Johto (0.al) e Temple of Rock (frente D)')]
RAIZES = ('data', 'src', 'include', 'dev_scripts', 'test', 'tools', 'asm', 'constants')
EXT_TEXTO = ('.inc', '.s', '.json', '.c', '.h', '.party', '.py', '.sh', '.txt', '.pory',
             '.mk', '.md', '.csv', '.tsv', '.yaml', '.yml', '.cfg')
# Arquivos que falam SOBRE o censo e não SÃO referência (senão a reserva se
# autorreferenciaria).
IGNORA = {'dev_scripts/ids_orfaos.py', RESERVA}

RE_DEF = re.compile(r'^\s*#define\s+(TRAINER_[A-Z0-9_]+)\s+(\d+)\b', re.M)
RE_TOKEN = re.compile(r'\bTRAINER_[A-Z0-9_]+\b')
RE_HEX = re.compile(r'\b0[xX]([0-9A-Fa-f]{3,4})\b')
RE_CAB_PARTY = re.compile(r'^=== (TRAINER_[A-Z0-9_]+) ===\s*$')
RE_CMD_CRU = re.compile(r'\b(trainerbattle\w*|checktrainerflag|settrainerflag|cleartrainerflag|'
                        r'goto_if_(?:not_)?defeated|call_if_(?:not_)?defeated)\s+(\d+)\b')
RE_FLAG_C = re.compile(r'\bFlag(?:Set|Get|Clear)\s*\(\s*(0[xX][0-9A-Fa-f]+|\d+)\s*\)')
RE_COLA = re.compile(r'TRAINER_\s*##|##\s*TRAINER_')


# O 5º tier de revanche que saiu do jogo (commit do lote B, 23/09/2026):
# gRematchTable passou a 4 times, e o #define e o bloco de time destes 72
# nomes foram apagados. Dez números continuam definidos por um nome de Kanto
# do opponents_frlg.h que ninguém cita, e por isso contam como órfão comum.
NOMES_LIBERADOS = {
    43: 'TRAINER_ROSE_5', 50: 'TRAINER_DUSTY_5', 63: 'TRAINER_LOLA_5',
    70: 'TRAINER_RICKY_5', 87: 'TRAINER_WILTON_5', 104: 'TRAINER_BROOKE_5',
    113: 'TRAINER_VALERIE_5', 123: 'TRAINER_CINDY_6', 135: 'TRAINER_JESSICA_5',
    142: 'TRAINER_WINSTON_5', 150: 'TRAINER_STEVE_5', 178: 'TRAINER_TONY_5',
    187: 'TRAINER_NOB_5', 200: 'TRAINER_DALTON_5', 210: 'TRAINER_BERNIE_5',
    222: 'TRAINER_ETHAN_5', 231: 'TRAINER_JEFFREY_5', 242: 'TRAINER_CAMERON_5',
    253: 'TRAINER_JACKI_5', 260: 'TRAINER_WALTER_5', 279: 'TRAINER_JERRY_5',
    285: 'TRAINER_KAREN_5', 291: 'TRAINER_ANNA_AND_MEG_5', 298: 'TRAINER_MIGUEL_5',
    306: 'TRAINER_ISABEL_5', 311: 'TRAINER_TIMOTHY_5', 317: 'TRAINER_SHELBY_5',
    331: 'TRAINER_CALVIN_5', 349: 'TRAINER_ELLIOT_5', 357: 'TRAINER_BENJAMIN_5',
    363: 'TRAINER_ABIGAIL_5', 368: 'TRAINER_DYLAN_5', 373: 'TRAINER_MARIA_5',
    382: 'TRAINER_ISAIAH_5', 391: 'TRAINER_KATELYN_5', 396: 'TRAINER_NICOLAS_5',
    412: 'TRAINER_ROBERT_5', 424: 'TRAINER_LAO_5', 433: 'TRAINER_CYNDY_5',
    440: 'TRAINER_MADELINE_5', 468: 'TRAINER_JENNY_5', 480: 'TRAINER_DIANA_5',
    489: 'TRAINER_AMY_AND_LIV_6', 500: 'TRAINER_ERNEST_5', 518: 'TRAINER_EDWIN_5',
    544: 'TRAINER_ISAAC_5', 551: 'TRAINER_LYDIA_5', 558: 'TRAINER_JACKSON_5',
    565: 'TRAINER_CATHERINE_5', 610: 'TRAINER_HALEY_5', 625: 'TRAINER_JAMES_5',
    639: 'TRAINER_TRENT_5', 646: 'TRAINER_KIRA_AND_DAN_5', 685: 'TRAINER_JOHN_AND_JAY_5',
    691: 'TRAINER_LILA_AND_ROY_5', 773: 'TRAINER_ROXANNE_5', 777: 'TRAINER_BRAWLY_5',
    781: 'TRAINER_WATTSON_5', 785: 'TRAINER_FLANNERY_5', 789: 'TRAINER_NORMAN_5',
    793: 'TRAINER_WINONA_5', 797: 'TRAINER_TATE_AND_LIZA_5', 801: 'TRAINER_JUAN_5',
    815: 'TRAINER_ANDRES_5', 819: 'TRAINER_CORY_5', 823: 'TRAINER_PABLO_5',
    827: 'TRAINER_KOJI_5', 831: 'TRAINER_CRISTIN_5', 835: 'TRAINER_FERNANDO_5',
    839: 'TRAINER_SAWYER_5', 843: 'TRAINER_GABRIELLE_5', 847: 'TRAINER_THALIA_5',
}


def arquivos(raiz):
    saida = subprocess.run(['git', '-C', raiz, 'ls-files', '-z'], capture_output=True, check=True).stdout
    for rel in saida.decode().split('\0'):
        if not rel or rel in IGNORA:
            continue
        topo = rel.split('/', 1)[0]
        if topo in RAIZES or (topo == rel and rel.endswith('.mk')):
            if rel.endswith(EXT_TEXTO):
                yield rel


def definicoes(raiz):
    """número -> [(nome, arquivo)] lidos dos dois cabeçalhos."""
    nums = collections.defaultdict(list)
    for p in CABECALHOS:
        texto = open(os.path.join(raiz, p), encoding='utf-8', errors='replace').read()
        for m in RE_DEF.finditer(texto):
            nums[int(m.group(2))].append((m.group(1), p))
    return nums


def varre(raiz, faixa_flag):
    """Devolve (refs_nome, refs_num, colas): referência fora da definição."""
    refs_nome = collections.defaultdict(list)
    refs_num = collections.defaultdict(list)
    colas = []
    lo, hi = faixa_flag
    for rel in arquivos(raiz):
        try:
            texto = open(os.path.join(raiz, rel), encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        eh_cab = rel in CABECALHOS
        eh_party = rel.endswith('.party')
        eh_data = rel.startswith('data/')
        eh_teste = rel.startswith('dev_scripts/testes_criticos/')
        eh_src = rel.startswith(('src/', 'include/'))
        if RE_COLA.search(texto):
            colas.append(rel)
        for n, linha in enumerate(texto.split('\n'), 1):
            if eh_cab and RE_DEF.match(linha):
                # a definição não conta; um comentário na MESMA linha também não
                continue
            if eh_party and RE_CAB_PARTY.match(linha):
                continue
            if 'TRAINER_' in linha:
                for tok in RE_TOKEN.findall(linha):
                    lst = refs_nome[tok]
                    if len(lst) < 8:
                        lst.append(f'{rel}:{n}')
            if eh_data or eh_teste:
                for h in RE_HEX.findall(linha):
                    v = int(h, 16)
                    if lo <= v <= hi:
                        refs_num[v - FLAG_BASE].append(f'{rel}:{n} (flag 0x{v:X})')
            if eh_data:
                for cmd, num in RE_CMD_CRU.findall(linha):
                    refs_num[int(num)].append(f'{rel}:{n} ({cmd} cru)')
            if eh_src:
                for lit in RE_FLAG_C.findall(linha):
                    v = int(lit, 0)
                    if lo <= v <= hi:
                        refs_num[v - FLAG_BASE].append(f'{rel}:{n} (Flag* 0x{v:X})')
        if eh_teste:
            try:
                caso = json.loads(texto)
            except ValueError:
                continue
            _anda_teste(caso, None, rel, refs_num, faixa_flag)
    return refs_nome, refs_num, colas


def _anda_teste(o, chave, rel, refs_num, faixa_flag):
    lo, hi = faixa_flag
    if isinstance(o, dict):
        for k, v in o.items():
            _anda_teste(v, k, rel, refs_num, faixa_flag)
    elif isinstance(o, list):
        if chave == 'oponente_faixa':
            return  # faixa de asserção: não cita id nenhum (ver relatório)
        for v in o:
            _anda_teste(v, chave, rel, refs_num, faixa_flag)
    elif isinstance(o, bool):
        return
    elif isinstance(o, int) and chave:
        k = chave.lower()
        if k == 'oponente':
            refs_num[o].append(f'{rel} ("oponente": {o})')
        elif 'flag' in k and lo <= o <= hi:
            refs_num[o - FLAG_BASE].append(f'{rel} ({chave}: {o} = flag 0x{o:X})')


def faixas_teste(raiz):
    """Faixas de "oponente_faixa" dos casos: não são referência, mas o relatório as mostra."""
    fx = []
    pasta = os.path.join(raiz, 'dev_scripts/testes_criticos')
    for f in sorted(os.listdir(pasta)):
        if not f.endswith('.json'):
            continue
        texto = open(os.path.join(pasta, f), encoding='utf-8').read()
        for m in re.finditer(r'"oponente_faixa"\s*:\s*\[\s*(\d+)\s*,\s*(\d+)\s*\]', texto):
            fx.append((int(m.group(1)), int(m.group(2)), f))
    return fx


def censo(raiz=RAIZ):
    nums = definicoes(raiz)
    refs_nome, refs_num, colas = varre(raiz, (FLAG_BASE, FLAG_BASE + TETO - 1))
    orfaos, vivos = {}, {}
    for num in sorted(nums):
        if num == 0 or num >= TETO:
            continue
        nomes = sorted({n for n, _ in nums[num]})
        achados = []
        for nome in nomes:
            achados += refs_nome.get(nome, [])
        achados += refs_num.get(num, [])
        (vivos if achados else orfaos)[num] = {'nomes': nomes, 'refs': achados[:6],
                                                'arquivos': sorted({a for _, a in nums[num]})}
    livres = [i for i in range(1, TETO) if i not in nums and i not in NOMES_LIBERADOS]
    # Número LIBERADO pela frente (o #define saiu): vira órfão se o nome antigo
    # dele também não for citado em lugar nenhum.
    for num in sorted(NOMES_LIBERADOS):
        if num in nums:
            continue
        nomes = [NOMES_LIBERADOS[num]]
        achados = [r for n in nomes for r in refs_nome.get(n, [])] + refs_num.get(num, [])
        if achados:
            vivos[num] = {'nomes': nomes, 'refs': achados[:6], 'arquivos': []}
        else:
            orfaos[num] = {'nomes': nomes, 'refs': [], 'arquivos': ['(liberado)']}
    return {'nums': nums, 'orfaos': orfaos, 'vivos': vivos, 'livres': livres,
            'colas': colas, 'refs_nome': refs_nome}


def de_outro(num):
    for lo, hi, dono in FAIXAS_DE_OUTROS:
        if lo <= num <= hi:
            return dono
    return None


def faixas(lista):
    r = []
    for i in sorted(lista):
        if r and i == r[-1][1] + 1:
            r[-1][1] = i
        else:
            r.append([i, i])
    return r


def fmt_faixas(lista):
    return ', '.join(f'{a}-{b}' if a != b else f'{a}' for a, b in faixas(lista))


# Tabela do briefing da onda 1 (os 54 livres, fora de Johto). Órfãos por lote:
# decisão do condutor de 23/09/2026, A 12, B 6, C 45, e TODO o resto para a
# onda 2 (os 8 que sobram dos 71 e os liberados pelo 5º tier de revanche).
LIVRES_POR_LOTE = {
    'A-oeste': list(range(2060, 2077)) + list(range(2087, 2097)),
    'B-centro': list(range(2117, 2127)) + list(range(2140, 2154)),
    'C-leste': list(range(2154, 2157)),
}
ORFAOS_POR_LOTE = [('A-oeste', 12), ('B-centro', 6), ('C-leste', 45), ('onda-2', None)]


def gera_reserva(c, anterior=None):
    """Fatia os órfãos em ORDEM numérica (cada lote leva um trecho seguido da
    lista, que é o mais contíguo possível: o maior bloco de órfãos tem 4 ids).
    Com `anterior`, quem já tinha id continua com os MESMOS ids (reserva é
    promessa feita a outro executor) e só a onda 2 recebe o que é novo."""
    disp = sorted(n for n in c['orfaos'] if not de_outro(n))
    fixos = sum(q for _, q in ORFAOS_POR_LOTE if q)
    if len(disp) < fixos:
        return None, f'órfãos provados {len(disp)} < {fixos} pedidos'
    res = {}
    if anterior:
        usados = set()
        for lote, q in ORFAOS_POR_LOTE:
            if q:
                res[lote] = list(anterior['lotes'][lote]['orfaos_ids'])
                usados |= set(res[lote])
        falta = [n for n in usados if n not in c['orfaos'] and not any(
            x.startswith(PREFIXO_NOVO) for x, _ in c['nums'].get(n, []))]
        if falta:
            return None, f'ids já prometidos deixaram de ser órfãos: {falta}'
        res['onda-2'] = sorted(set(anterior['lotes']['onda-2']['orfaos_ids']) |
                               {n for n in disp if n not in usados})
    else:
        i = 0
        for lote, q in ORFAOS_POR_LOTE:
            res[lote] = disp[i:i + q] if q else disp[i:]
            i += q or 0
    saida = {
        'o_que_e': 'Reserva de ids de treinador da frente Hoenn EX (cartucho 1). Gerado por '
                   'dev_scripts/ids_orfaos.py --gera-reserva; o portão é --guarda.',
        'teto': TETO,
        'prefixo_dos_nomes_novos': PREFIXO_NOVO,
        'lotes': {},
    }
    for lote, _ in ORFAOS_POR_LOTE:
        orf = res[lote]
        nomes = {}
        for n in orf:
            if n in c['orfaos']:
                nomes[str(n)] = c['orfaos'][n]['nomes']
            else:
                nomes[str(n)] = anterior['lotes'][lote]['nomes_antigos'][str(n)]
        saida['lotes'][lote] = {
            'livres': fmt_faixas(LIVRES_POR_LOTE.get(lote, [])),
            'livres_ids': LIVRES_POR_LOTE.get(lote, []),
            'orfaos': fmt_faixas(orf),
            'orfaos_ids': orf,
            'nomes_antigos': nomes,
        }
    return saida, None


def guarda(raiz=RAIZ):
    caminho = os.path.join(raiz, RESERVA)
    if not os.path.exists(caminho):
        print(f'guarda: {RESERVA} não existe, nada a guardar')
        return 0
    reserva = json.load(open(caminho, encoding='utf-8'))
    nums = definicoes(raiz)
    refs_nome, refs_num, colas = varre(raiz, (FLAG_BASE, FLAG_BASE + TETO - 1))
    cab = open(os.path.join(raiz, CABECALHOS[0]), encoding='utf-8').read()
    i0, i1 = cab.find(MARCA_INI), cab.find(MARCA_FIM)
    bloco = cab[i0:i1] if 0 <= i0 < i1 else ''
    dentro = {m.group(1) for m in RE_DEF.finditer(bloco)}
    blocos_party = collections.Counter()
    nome2num = {n: k for k, v in nums.items() for n, _ in v}
    for m in re.finditer(r'^=== (TRAINER_[A-Z0-9_]+) ===', open(os.path.join(raiz, PARTY_COMPILADO),
                                                              encoding='utf-8').read(), re.M):
        blocos_party[nome2num.get(m.group(1), m.group(1))] += 1
    erros = []
    if colas:
        erros.append(f'macro que cola nome de treinador: {colas}')
    reservados = set()
    antigos = {}
    for lote, d in reserva['lotes'].items():
        for n in d['livres_ids']:
            reservados.add(n)
        for n in d['orfaos_ids']:
            reservados.add(n)
            antigos[n] = d['nomes_antigos'][str(n)]
    for num in sorted(reservados):
        velhos = antigos.get(num, [])
        for nome in velhos:
            achados = refs_nome.get(nome, [])
            if achados:
                erros.append(f'id {num}: nome antigo {nome} voltou a ser referenciado: {achados[:3]}')
        if num in antigos and refs_num.get(num):
            # Id JÁ reusado por um TRAINER_HOENNEX_* (junção da onda 1, 24/09/2026):
            # a flag de vitória crua nos casos de teste é a do treinador NOVO, e é
            # assim que o bloco prova a batalha. Só em teste; em data/ continua
            # vermelho, porque ali a flag crua esconderia o nome.
            reusado = any(n.startswith(PREFIXO_NOVO) for n, _ in nums.get(num, []))
            fora_de_teste = [r for r in refs_num[num] if not r.startswith('dev_scripts/testes_criticos/')]
            if not reusado or fora_de_teste:
                erros.append(f'id {num}: referência crua ao número: {(fora_de_teste or refs_num[num])[:3]}')
        novos = []
        for nome, arq in nums.get(num, []):
            if nome in velhos:
                continue
            if not nome.startswith(PREFIXO_NOVO):
                erros.append(f'id {num}: {nome} ({arq}) usa número da reserva e não é {PREFIXO_NOVO}*')
            elif nome not in dentro:
                erros.append(f'id {num}: {nome} está fora do bloco da reserva no opponents.h')
            else:
                novos.append(nome)
        if len(novos) > 1:
            erros.append(f'id {num}: colisão entre nomes novos {novos}')
        if novos and any(v in {x for x, _ in nums.get(num, [])} for v in velhos):
            erros.append(f'id {num}: {novos[0]} convive com o #define antigo {velhos}: apague o antigo')
        if blocos_party.get(num, 0) > 1:
            erros.append(f'id {num}: {blocos_party[num]} blocos de time em {PARTY_COMPILADO}')
    for num, defs in nums.items():
        for nome, _ in defs:
            if nome.startswith(PREFIXO_NOVO) and num not in reservados:
                erros.append(f'{nome} = {num}, fora da reserva da frente')
    if erros:
        print(f'guarda de ids da frente Hoenn EX: {len(erros)} VERMELHO(S)')
        for e in erros:
            print('  ' + e)
        return 1
    print(f'guarda de ids da frente Hoenn EX: verde ({len(reservados)} ids reservados, '
          f'{sum(1 for n in reservados for x, _ in nums.get(n, []) if x.startswith(PREFIXO_NOVO))} já em uso)')
    return 0


def autoteste():
    """Monta um repositório de brinquedo e prova os quatro caminhos."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix='ids_orfaos_')
    def w(rel, txt):
        p = os.path.join(tmp, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w').write(txt)
    w(CABECALHOS[0], f'#define TRAINER_A 1\n#define TRAINER_B 2\n#define TRAINER_C 3\n'
                     f'#define TRAINER_D 4\n#define TRAINER_E 5\n{MARCA_INI}\n{MARCA_FIM}\n')
    w(CABECALHOS[1], '#define TRAINER_KB 2\n#define TRAINER_KC 3\n')
    w(PARTY_COMPILADO, '=== TRAINER_A ===\n=== TRAINER_B ===\n=== TRAINER_C ===\n'
                       '=== TRAINER_D ===\n=== TRAINER_E ===\n')
    w('data/maps/X/scripts.inc', 'trainerbattle_single TRAINER_A, x\n')
    w('src/data/rematches.h', '{ TRAINER_KB }\n')          # número 2 vivo pelo nome de Kanto
    w('dev_scripts/testes_criticos/1_x.json', '{"flags": ["0x504"]}')  # 4 vivo pela flag crua
    w('data/scripts/y.inc', '@ TRAINER_E citado em comentario conta\n')
    w('data/scripts/z.inc', f'trainerbattle_single {NOMES_LIBERADOS[43]}, x\n')  # liberado que volta
    subprocess.run(['git', 'init', '-q', tmp], check=True)
    subprocess.run(['git', '-C', tmp, 'add', '-A'], check=True)
    c = censo(tmp)
    ok = True
    def confere(cond, msg):
        nonlocal ok
        print(('ok    ' if cond else 'FALHA ') + msg)
        ok &= bool(cond)
    comuns = sorted(n for n in c['orfaos'] if n not in NOMES_LIBERADOS)
    confere(comuns == [3], f'só o 3 é órfão entre os definidos (achou {comuns})')
    confere(43 in c['vivos'] and 50 in c['orfaos'],
            'número liberado: vivo se o nome antigo é citado, órfão se não')
    confere(2 in c['vivos'], 'o 2 vive pelo nome de Kanto que divide o número')
    confere(4 in c['vivos'], 'o 4 vive pela flag crua 0x504 no caso de teste')
    confere(5 in c['vivos'], 'comentário conta como referência (lado conservador)')
    json.dump({'lotes': {'L': {'livres_ids': [], 'orfaos_ids': [3],
                               'nomes_antigos': {'3': ['TRAINER_C', 'TRAINER_KC']}}}},
              open(os.path.join(tmp, RESERVA), 'w'))
    confere(guarda(tmp) == 0, 'guarda verde com a reserva intocada')
    w('data/maps/Z/scripts.inc', 'trainerbattle_single TRAINER_KC, x\n')
    subprocess.run(['git', '-C', tmp, 'add', '-A'], check=True)
    confere(guarda(tmp) == 1, 'guarda VERMELHA quando o nome antigo volta a ser usado')
    os.remove(os.path.join(tmp, 'data/maps/Z/scripts.inc'))
    subprocess.run(['git', '-C', tmp, 'add', '-A'], check=True)
    w(CABECALHOS[0], f'#define TRAINER_A 1\n#define TRAINER_B 2\n#define TRAINER_D 4\n#define TRAINER_E 5\n'
                     f'{MARCA_INI}\n#define TRAINER_HOENNEX_NOVO 3\n{MARCA_FIM}\n#define TRAINER_HOENNEX_FORA 3\n')
    w(CABECALHOS[1], '#define TRAINER_KB 2\n')
    confere(guarda(tmp) == 1, 'guarda VERMELHA com dois nomes novos no mesmo número')
    w(CABECALHOS[0], f'#define TRAINER_A 1\n#define TRAINER_B 2\n#define TRAINER_D 4\n#define TRAINER_E 5\n'
                     f'{MARCA_INI}\n#define TRAINER_HOENNEX_NOVO 3\n{MARCA_FIM}\n')
    confere(guarda(tmp) == 0, 'guarda verde com o reuso feito pela receita')
    print('AUTOTESTE ' + ('VERDE' if ok else 'VERMELHO'))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--prova', action='store_true')
    ap.add_argument('--gera-reserva', action='store_true')
    ap.add_argument('--guarda', action='store_true')
    ap.add_argument('--autoteste', action='store_true')
    ap.add_argument('--json', help='escreve o censo completo neste caminho')
    a = ap.parse_args()
    if a.autoteste:
        return autoteste()
    if a.guarda:
        return guarda()
    c = censo()
    orf = c['orfaos']
    fora = {n: d for n, d in orf.items() if not de_outro(n)}
    print(f'números definidos abaixo de {TETO}: {len(c["nums"]) - (1 if 0 in c["nums"] else 0)}; '
          f'livres: {len(c["livres"])} ({fmt_faixas(c["livres"])})')
    print(f'órfãos provados: {len(orf)}; fora das faixas de outras frentes: {len(fora)}')
    print(f'macro que cola nome de treinador: {c["colas"] or "nenhuma"}')
    por_arq = collections.Counter(tuple(d['arquivos']) for d in fora.values())
    for arqs, q in por_arq.most_common():
        print(f'  {q:4d} definidos em {", ".join(arqs)}')
    fx = faixas_teste(RAIZ)
    dentro_fx = [n for n in fora if any(lo <= n <= hi for lo, hi, _ in fx)]
    print(f'  {len(dentro_fx)} deles caem dentro de alguma "oponente_faixa" de caso de teste '
          f'(faixa de asserção, não é referência)')
    if a.prova:
        print('\nPROVA NEGATIVA (número: nomes -> referências fora da definição)')
        for n in sorted(fora):
            print(f'  {n}: {" / ".join(fora[n]["nomes"])} -> 0 referências')
    if a.json:
        json.dump({'orfaos': {str(k): v for k, v in orf.items()},
                   'livres': c['livres']}, open(a.json, 'w'), indent=1, ensure_ascii=False)
    if a.gera_reserva:
        cam = os.path.join(RAIZ, RESERVA)
        anterior = json.load(open(cam, encoding='utf-8')) if os.path.exists(cam) else None
        res, erro = gera_reserva(c, anterior)
        if erro:
            print(f'\nPARE: {erro}. Nada foi escrito.')
            return 2
        json.dump(res, open(os.path.join(RAIZ, RESERVA), 'w'), indent=1, ensure_ascii=False)
        print(f'\nreserva escrita em {RESERVA}:')
        for lote, d in res['lotes'].items():
            print(f'  {lote:9s} livres [{d["livres"]}]  órfãos [{d["orfaos"]}]')
    return 0


if __name__ == '__main__':
    sys.exit(main())
