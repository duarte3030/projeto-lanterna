#!/usr/bin/env python3
"""Mede laço e volume da música nova de Galar e Unova NO mGBA (c2-musica, 28/10/2026).

Uso:
    python3 dev_scripts/qa/mede_musica.py [--quadros 9000] [--so T1,T2] [--saida DIR]

Para cada faixa nova que algum mapa toca (regra de dev_scripts/musica_c2.py), um caso
de warp para um mapa dela; mais as batalhas (líder e treinador de Galar, líder e
selvagem de Unova) e duas faixas de referência que não mudaram (Wild Area de Galar
e Accumula Town de Unova). Cada caso roda pelo testa_critico.py (o caso só vale se
a música TOCANDO for a esperada, prova `musica`) e grava N quadros de áudio do mGBA
(`gba_runner --wav`).

Medidas, por gravação (estéreo, 32768 Hz):
  - volume: RMS em dBFS depois dos 3 primeiros segundos, e pico;
  - buraco: janelas de 0,5 s abaixo de -50 dBFS depois dos 3 s. Música que acaba em
    vez de voltar ao laço, ou laço que emenda em silêncio, aparece aqui;
  - laço dentro da gravação: o fim do laço sai do marcador "]" do .mid e do andamento.
    Se o fim do laço cai dentro da gravação, a volta foi tocada e medida.
Saída: tabela no terminal e DIR/medida.json.
"""
import argparse
import glob
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import wave

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, 'dev_scripts'))
import musica_c2  # noqa: E402


def fim_do_laco(mid):
    """segundos até o marcador ']' (ou o fim) no .mid tipo 1, pelo mapa de andamento."""
    d = open(mid, 'rb').read()
    tpq = struct.unpack('>H', d[12:14])[0]
    p = 14; eventos = []; fim_max = 0
    while p < len(d) and d[p:p + 4] == b'MTrk':
        n = struct.unpack('>I', d[p + 4:p + 8])[0]; q = p + 8; e = q + n; t = 0; run = 0
        while q < e:
            v = 0
            while True:
                b = d[q]; q += 1; v = (v << 7) | (b & 0x7F)
                if not b & 0x80: break
            t += v; st = d[q]
            if st == 0xFF:
                tp = d[q + 1]; q += 2; ln = 0
                while True:
                    b = d[q]; q += 1; ln = (ln << 7) | (b & 0x7F)
                    if not b & 0x80: break
                if tp == 0x51: eventos.append((t, 'tempo', int.from_bytes(d[q:q + 3], 'big')))
                if tp in (0x06, 0x01) and d[q:q + ln] == b']': eventos.append((t, 'fim', 0))
                q += ln
            elif st in (0xF0, 0xF7):
                q += 1; ln = 0
                while True:
                    b = d[q]; q += 1; ln = (ln << 7) | (b & 0x7F)
                    if not b & 0x80: break
                q += ln
            else:
                if st & 0x80: run = st; q += 1
                q += 1 if (run & 0xF0) in (0xC0, 0xD0) else 2
        fim_max = max(fim_max, t)
        p = e
    alvo = next((t for t, k, _ in eventos if k == 'fim'), fim_max)
    seg = 0.0; t0 = 0; us = 500000
    for t, k, v in sorted(x for x in eventos if x[1] == 'tempo'):
        if t >= alvo: break
        seg += (t - t0) / tpq * us / 1e6; t0 = t; us = v
    return seg + (alvo - t0) / tpq * us / 1e6


def mede_wav(arq):
    import array
    w = wave.open(arq)
    taxa = w.getframerate(); a = array.array('h', w.readframes(w.getnframes()))
    if not a: return None
    mono = [(a[i] + a[i + 1]) / 2 for i in range(0, len(a) - 1, 2)]
    ini = 3 * taxa
    corpo = mono[ini:]
    import math
    def db(x): return 20 * math.log10(max(x, 1e-9) / 32768)
    rms = math.sqrt(sum(x * x for x in corpo) / max(1, len(corpo)))
    pico = max(abs(x) for x in corpo) if corpo else 0
    jan = taxa // 2; buracos = []
    for i in range(0, len(corpo) - jan, jan):
        r = math.sqrt(sum(x * x for x in corpo[i:i + jan]) / jan)
        if db(r) < -50: buracos.append(round((ini + i) / taxa, 1))
    return dict(segundos=round(len(mono) / taxa, 1), rms_db=round(db(rms), 1), pico_db=round(db(pico), 1), buracos=buracos)


def casos():
    mapas = musica_c2.le_mapas(); base = musica_c2.base_de(mapas); alvo = musica_c2.regra(mapas, base)
    por_musica = {}
    for n in sorted(alvo):
        m = mapas[n][1]
        ext = m.get('map_type') in ('MAP_TYPE_CITY', 'MAP_TYPE_TOWN', 'MAP_TYPE_ROUTE')
        atual = por_musica.get(alvo[n])
        if atual is None or (ext and not atual[1]):
            por_musica[alvo[n]] = (n, ext)
    out = []
    for i, (mus, (n, _)) in enumerate(sorted(por_musica.items())):
        m = mapas[n][1]
        out.append(dict(id=f'T9001.{i + 1}', nome=f'{mus} em {n}', warp=m['id'], warp_id=0, roteiro='300:NADA',
                        prova=dict(mapa=m['id'], musica=mus.lower())))
    refs = [('MAP_GALAR_WILD_AREA_09', 'mus_rg_sevii_45'), ('MAP_UNOVA_ACCUMULA_TOWN', 'mus_oldale')]
    for j, (mp, lab) in enumerate(refs):
        out.append(dict(id=f'T9002.{j + 1}', nome=f'referência {lab} em {mp}', warp=mp, warp_id=0, roteiro='300:NADA',
                        prova=dict(mapa=mp, musica=lab)))
    exist = {}
    for f in glob.glob(os.path.join(RAIZ, 'dev_scripts/testes_criticos/*.json')):
        for c in json.load(open(f)):
            exist[c['id']] = c
    for k, (cid, lab) in enumerate((('T190.4', 'mus_galar_lider'), ('T190.6', 'mus_galar_treinador'),
                     ('T187.2', 'mus_unova_vs_gymleader'), ('T187.3', 'mus_unova_vs_norapoke'))):
        c = json.loads(json.dumps(exist[cid])); c['id'] = f'T9003.{k + 1}'; c['prova'] = dict(c['prova'], musica=lab)
        c['nome'] = f'batalha {lab} ({cid})'
        out.append(c)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quadros', type=int, default=9000)
    ap.add_argument('--so')
    ap.add_argument('--saida', default=os.path.join(RAIZ, 'build.nosync', 'mede_musica'))
    a = ap.parse_args()
    cs = casos()
    if a.so: cs = [c for c in cs if c['id'] in a.so.split(',')]
    os.makedirs(a.saida, exist_ok=True)
    tmp = tempfile.mkdtemp(dir=a.saida)
    json.dump(cs, open(os.path.join(tmp, 'casos.json'), 'w'), ensure_ascii=False, indent=1)
    env = dict(os.environ, TESTA_CASOS=tmp, TESTA_WAV=str(a.quadros), TESTA_SAIDA=a.saida)
    r = subprocess.run([sys.executable, os.path.join(RAIZ, 'dev_scripts/testa_critico.py')], env=env,
                       capture_output=True, text=True, cwd=RAIZ)
    status = {m.group(2): m.group(1) == 'OK' for m in re.finditer(r'^\[(OK|FALHA)\s*\] (\S+)', r.stdout, re.M)}
    res = []
    for c in cs:
        lab = c['prova']['musica']
        w = os.path.join(a.saida, c['id'].replace('.', '_') + '.wav')
        med = mede_wav(w) if os.path.exists(w) else None
        mid = os.path.join(RAIZ, 'sound/songs/midi', lab + '.mid')
        laco = round(fim_do_laco(mid), 1) if os.path.exists(mid) else None
        res.append(dict(id=c['id'], musica=lab, tocando=status.get(c['id'], False), fim_laco_s=laco, **(med or {})))
    json.dump(res, open(os.path.join(a.saida, 'medida.json'), 'w'), indent=1, ensure_ascii=False)
    print(f'{"caso":10} {"música":28} {"toca":5} {"laço s":>7} {"grav s":>6} {"RMS dB":>7} {"pico":>6}  buracos')
    for x in res:
        print(f'{x["id"]:10} {x["musica"]:28} {"sim" if x["tocando"] else "NÃO":5} {str(x["fim_laco_s"]):>7} '
              f'{str(x.get("segundos")):>6} {str(x.get("rms_db")):>7} {str(x.get("pico_db")):>6}  {x.get("buracos")}')
    return 0 if all(x['tocando'] for x in res) else 1


if __name__ == '__main__':
    sys.exit(main())
