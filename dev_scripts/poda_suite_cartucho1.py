"""Ferramenta de 28/10/2026 (fase 0 do PRD de assets). Tira da suíte do cartucho 2 os casos que citam mapa ou layout que não é de Unova nem de Galar.
uso: poda_suite_cartucho1.py <arvore> <saida.json> [--aplicar]
Critério: token MAP_* ou LAYOUT_* do caso que (a) não existe mais na árvore ou (b) é de mapa
que ficou como túmulo (pasta que não começa com Unova_ ou Galar_). O nome do caso não conta:
só os campos que o motor executa ou confere. Medido na árvore DEPOIS da remoção."""
import json, glob, re, os, sys, collections
R, OUT = sys.argv[1], sys.argv[2]
APLICA = '--aplicar' in sys.argv
os.chdir(R)
g = json.load(open('data/maps/map_groups.json'))
mapa_pasta, lay_pastas = {}, collections.defaultdict(set)
for k in g['group_order']:
    for m in g[k]:
        j = json.load(open(f'data/maps/{m}/map.json'))
        mapa_pasta[j['id']] = m
        lay_pastas[j['layout']].add(m)
lays = {l['id'] for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id')}
fica = lambda m: m.startswith(('Unova_', 'Galar_')) or m.startswith(('Unova', 'Galar'))
CONST_OK = {'MAP_UNDEFINED', 'MAP_DYNAMIC', 'MAP_NONE', 'LAYOUT_NONE'}
def ruins(caso):
    s = json.dumps({k: v for k, v in caso.items() if k != "nome"})
    out = []
    for t in sorted(set(re.findall(r'\b(?:MAP|LAYOUT)_[A-Z0-9_]+', s))):
        if t in CONST_OK: continue
        if t.startswith('MAP_'):
            if t in mapa_pasta:
                if not fica(mapa_pasta[t]): out.append(t + ' (túmulo)')
            elif t.startswith('MAP_GROUP') or t.startswith('MAP_NUM'):
                continue
            else:
                out.append(t + ' (não existe)')
        else:
            if t in lay_pastas:
                if not any(fica(m) for m in lay_pastas[t]): out.append(t + ' (túmulo)')
            elif t in lays:
                out.append(t + ' (sem mapa)')
            else:
                out.append(t + ' (não existe)')
    return out

def tira_casos(raw, ids):
    """Apaga do TEXTO os objetos de caso cujo id está em ids, sem reformatar o resto."""
    dec = json.JSONDecoder()
    if raw.lstrip().startswith('{'):
        i = raw.index('"casos"'); i = raw.index('[', i)
    else:
        i = raw.index('[')
    spans, j = [], i + 1
    while True:
        while raw[j] in ' \t\r\n,': j += 1
        if raw[j] == ']': break
        obj, fim = dec.raw_decode(raw, j)
        spans.append((j, fim, obj.get('id')))
        j = fim
    fecha = j
    manter = [(a, b) for a, b, cid in spans if cid not in ids]
    if not manter:
        return raw[:i + 1] + raw[fecha:]
    # separador original entre o 1o e o 2o objeto (ou ',\n ' por padrão)
    sep = raw[spans[0][1]:spans[1][0]] if len(spans) > 1 else ',\n'
    abre = raw[i + 1:spans[0][0]]
    fim_txt = raw[spans[-1][1]:fecha]
    return raw[:i + 1] + abre + sep.join(raw[a:b] for a, b in manter) + fim_txt + raw[fecha:]
rel = {}
for f in sorted(glob.glob('dev_scripts/testes_criticos/*.json')):
    raw = open(f, encoding='utf-8').read()
    d = json.loads(raw)
    lista = d['casos'] if isinstance(d, dict) else d
    sai = [c for c in lista if ruins(c)]
    for c in sai:
        rel[c['id']] = dict(arq=os.path.basename(f), motivo=ruins(c)[:3])
    if APLICA and sai:
        resto = [c for c in lista if not ruins(c)]
        if not resto:
            os.remove(f); continue
        open(f, 'w', encoding='utf-8').write(tira_casos(raw, {c['id'] for c in sai}))
        d2 = json.loads(open(f, encoding='utf-8').read())
        l2 = d2['casos'] if isinstance(d2, dict) else d2
        assert [c['id'] for c in l2] == [c['id'] for c in resto], f
json.dump(rel, open(OUT, 'w'), indent=1, ensure_ascii=False)
por = collections.Counter(v['arq'] for v in rel.values())
print('saem', len(rel), 'casos de', len(por), 'arquivos')
