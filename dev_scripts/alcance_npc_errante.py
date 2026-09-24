#!/usr/bin/env python3
"""Até onde um NPC que anda chega, e se ele alcança warp, chegada, gatilho ou prova.

Nasceu na fila de bugs 2 do cartucho 1, em 24/09/2026, para medir os NPC de
`MOVEMENT_TYPE_WANDER_*` (e parentes) cujo `map.json` diz raio ZERO num eixo. A
0.ak do ESTADO contou 162 deles e afirmou que raio zero, no motor, quer dizer SEM
LIMITE naquele eixo. **Não quer.** A leitura estava pela metade:

* `IsCoordOutsideObjectEventMovementRange` (`src/event_object_movement.c`) pula
  o eixo cujo raio é zero, e foi só isso que a 0.ak leu;
* `InitObjectEventStateFromTemplate`, no mesmo arquivo, é quem copia o raio do
  `map.json` para o objeto vivo, e logo depois SOBE o zero para UM em todo tipo
  da tabela `sMovementTypeHasRange` (os WANDER, os WALK_*_AND_*, as
  WALK_SEQUENCE e os COPY_PLAYER). É o único caminho que escreve `range` a
  partir do template; `src/trainer_see.c` só guarda e devolve o valor.

Então, no jogo, raio zero é raio UM. A regra está em `rota_de_teste.Mapa.
alcance_do_npc`, que esta ferramenta reaproveita (e que foi corrigida junto), e
a prova está na EWRAM: `--emulador` lê o byte `range` e a posição de cada objeto
vivo quadro a quadro.

O que a ferramenta mede, NPC por NPC (todos os tipos de `sMovementTypeHasRange`,
em todos os mapas; `--so-zero` restringe aos que têm raio zero num eixo):

* as células alcançáveis: busca em largura a partir da célula inicial,
  respeitando colisão, elevação, as células de objeto PARADO e sempre presente
  (sem flag), o eixo do tipo (WANDER_UP_AND_DOWN só anda na vertical, etc.) e o
  raio EFETIVO;
* se alguma delas é célula de `warp_event`, célula de CHEGADA de porta (1 tile
  ao sul do warp de porta, pela mesma leitura de comportamento que o
  `audita_rotas_npc.py` usa), `coord_event`, ou célula de PROVA de caso de teste
  (`prova.pos` e `prova.objetos` dos casos em `dev_scripts/testes_criticos/`
  cujo mapa final é este).

`--regra leitura-0ak` refaz a conta com a leitura antiga (raio zero sem limite),
para mostrar de onde vinham os números da 0.ak. O critério de conserto da fila
(alcance acima de 50 células, ou alcançar warp, chegada, gatilho ou prova) é
aplicado sempre com a regra do MOTOR.

LIMITES, ditos e não escondidos: a busca não atravessa conexão de mapa, não lê
`IsMetatileDirectionallyImpassable` nem escada lateral (as duas só TIRAM células,
então a conta é teto e não piso), e trata objeto com flag como ausente (pode
sumir, então também não tira célula).

Uso:
    python3 dev_scripts/alcance_npc_errante.py                 # todos, resumo
    python3 dev_scripts/alcance_npc_errante.py --mapa OreburghCity -v
    python3 dev_scripts/alcance_npc_errante.py --so-zero --json saida.json
    python3 dev_scripts/alcance_npc_errante.py --regra leitura-0ak --so-zero
    python3 dev_scripts/alcance_npc_errante.py --demo           # planta e morde
    python3 dev_scripts/alcance_npc_errante.py --emulador MAP_X --warp-id 0 \\
        --rom pokeemerald.gba --passos 200 --quadros 60
"""
import argparse
import glob
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(AQUI, "qa"))
import rota_de_teste as R          # noqa: E402
import audita_rotas_npc as A       # noqa: E402

RAIZ = R.RAIZ
LIMIAR = 50


def carrega_provas():
    """{MAP_X: {(x,y): [ids de caso]}} das células que casos usam como prova."""
    provas = {}
    for arq in sorted(glob.glob(os.path.join(RAIZ, "dev_scripts", "testes_criticos", "*.json"))):
        for c in json.load(open(arq, encoding="utf-8")):
            p = c.get("prova") or {}
            mapa = p.get("mapa") or c.get("warp")
            if not mapa:
                continue
            cel = []
            if p.get("pos"):
                cel.append(tuple(p["pos"]))
            for o in p.get("objetos") or []:
                cel.append((o["x"], o["y"]))
            for xy in cel:
                provas.setdefault(mapa, {}).setdefault(xy, []).append(c["id"])
    return provas


def alvos_do_mapa(nome, mp, provas):
    """{(x,y): [rótulos]} das células que um NPC não deveria alcançar."""
    mj = mp.mj
    alvos = {}
    for i, w in enumerate(mj.get("warp_events") or []):
        alvos.setdefault((w["x"], w["y"]), []).append(f"warp{i}")
        p = A.pouso_do_warp(nome, mj, w)
        if p and p[0] != (w["x"], w["y"]):
            alvos.setdefault(p[0], []).append(f"chegada{i}")
    for i, c in enumerate(mj.get("coord_events") or []):
        alvos.setdefault((c["x"], c["y"]), []).append(f"coord{i}")
    for xy, ids in provas.get(mj.get("id"), {}).items():
        alvos.setdefault(xy, []).append("prova " + ",".join(sorted(set(ids))))
    return alvos


def mede_mapa(nome, regra="motor", provas=None, so_zero=False, mj=None):
    """Lista de dicionários, um por NPC de tipo com raio neste mapa."""
    provas = provas if provas is not None else {}
    mp = R.Mapa(nome)
    if mj is not None:              # --demo planta em memória, nunca em disco
        mp.mj = mj
    tipos = R.tipos_com_raio()
    objs = mp.mj.get("object_events") or []
    parados = set()
    for e in objs:
        if e.get("type") == "clone":
            continue
        if e.get("movement_type") not in tipos and str(e.get("flag", "0")) == "0":
            parados.add((e["x"], e["y"]))
    alvos = alvos_do_mapa(nome, mp, provas)
    saida = []
    for i, e in enumerate(objs):
        t = e.get("movement_type")
        if e.get("type") == "clone" or t not in tipos:
            continue
        rx = int(e.get("movement_range_x") or 0)
        ry = int(e.get("movement_range_y") or 0)
        if so_zero and rx and ry:
            continue
        ini = (e["x"], e["y"])
        if regra == "motor":
            cel = mp.alcance_do_npc(ini[0], ini[1], rx, ry, t, bloqueios=parados - {ini})
            efetivo = (rx or 1, ry or 1)
        else:   # a leitura da 0.ak: zero = sem limite
            cel = mp.alcance_do_npc(ini[0], ini[1], rx, ry, t,
                                    bloqueios=parados - {ini}, raio_minimo=False)
            efetivo = (rx or None, ry or None)
        batidas = {f"{x},{y}": alvos[(x, y)] for (x, y) in sorted(cel)
                   if (x, y) in alvos and (x, y) != ini}
        saida.append({
            "mapa": nome, "indice": i, "local_id": e.get("local_id", i + 1),
            "tipo": t.replace("MOVEMENT_TYPE_", ""), "x": ini[0], "y": ini[1],
            "raio_json": [rx, ry], "raio_efetivo": list(efetivo),
            "celulas": len(cel), "alcanca": batidas,
            "conserta": len(cel) > LIMIAR or bool(batidas),
        })
    return saida


def todos_os_mapas():
    return sorted(os.path.basename(os.path.dirname(p))
                  for p in glob.glob(os.path.join(RAIZ, "data", "maps", "*", "map.json")))


def mede_tudo(regra="motor", so_zero=False, mapas=None):
    provas = carrega_provas()
    tudo, erros = [], []
    for nome in mapas or todos_os_mapas():
        try:
            tudo += mede_mapa(nome, regra, provas, so_zero)
        except (StopIteration, FileNotFoundError, KeyError) as ex:
            erros.append((nome, repr(ex)))
    return tudo, erros


# ---------------------------------------------------------------------------
# --demo: planta um NPC em memória e exige que a lente morda
# ---------------------------------------------------------------------------
def demo():
    """Três plantios em OreburghCity, cidade aberta, todos em memória.

    1. NPC de WANDER_AROUND com raio (8,8) no meio da praça: tem de passar de 50
       células (e com raio (0,0) não pode, porque o motor sobe o zero para 1).
    2. NPC de raio (1,1) colado ao sul da chegada de uma porta: tem de alcançar
       a célula de chegada.
    3. NPC de raio (1,1) em cima de um `coord_event`: tem de alcançar o gatilho
       vizinho quando ele cai no quadrado.
    """
    nome = "OreburghCity"
    base = R.Mapa(nome).mj
    falhas = []

    def planta(e):
        mj = json.loads(json.dumps(base))
        mj["object_events"] = (mj.get("object_events") or []) + [e]
        r = mede_mapa(nome, "motor", {}, False, mj=mj)
        return r[-1]

    npc = {"graphics_id": "OBJ_EVENT_GFX_WOMAN_3", "elevation": 3,
           "movement_type": "MOVEMENT_TYPE_WANDER_AROUND", "trainer_type": "TRAINER_TYPE_NONE",
           "trainer_sight_or_berry_tree_id": "0", "script": "0", "flag": "0"}
    # uma célula andável e aberta: a da própria chegada da primeira porta que tiver
    mp = R.Mapa(nome)
    chegada = None
    for w in base["warp_events"]:
        p = A.pouso_do_warp(nome, base, w)
        if p and p[0] != (w["x"], w["y"]) and mp.col(*p[0]) == 0:
            chegada = p[0]
            break
    grande = planta(dict(npc, x=40, y=30, movement_range_x=8, movement_range_y=8))
    zero = planta(dict(npc, x=40, y=30, movement_range_x=0, movement_range_y=0))
    print(f"  plantio 1: raio (8,8) em (40,30) alcança {grande['celulas']} células; "
          f"com raio (0,0) alcança {zero['celulas']}")
    if not grande["conserta"] or grande["celulas"] <= LIMIAR:
        falhas.append("plantio 1: raio 8 não passou de 50 células")
    if zero["celulas"] > 9:
        falhas.append("plantio 1: raio 0 passou de 9 células (a regra do motor sumiu)")
    if chegada:
        viz = planta(dict(npc, x=chegada[0], y=chegada[1] + 1,
                          movement_range_x=1, movement_range_y=1))
        ok = f"{chegada[0]},{chegada[1]}" in viz["alcanca"]
        print(f"  plantio 2: NPC em {(chegada[0], chegada[1] + 1)} alcança a chegada "
              f"{chegada}: {'SIM' if ok else 'NÃO'}")
        if not ok:
            falhas.append("plantio 2: a chegada de porta não foi acusada")
    else:
        falhas.append("plantio 2: não achei chegada de porta andável em Oreburgh")
    ce = (base.get("coord_events") or [None])[0]
    if ce:
        viz = planta(dict(npc, x=ce["x"] + 1, y=ce["y"], movement_range_x=1, movement_range_y=1))
        ok = any(r.startswith("coord") for v in viz["alcanca"].values() for r in v)
        print(f"  plantio 3: NPC ao lado do coord_event {(ce['x'], ce['y'])}: "
              f"{'acusado' if ok else 'NÃO acusado'}")
        if not ok and mp.col(ce["x"], ce["y"]) == 0:
            falhas.append("plantio 3: o coord_event não foi acusado")
    for f in falhas:
        print("  FALHA", f)
    print("DEMO:", "a lente MORDE" if not falhas else "a lente NÃO morde")
    return 1 if falhas else 0


# ---------------------------------------------------------------------------
# --emulador: a posição e o raio de verdade, lidos da EWRAM
# ---------------------------------------------------------------------------
def emulador(rom, mapa_const, warp_id, passos, quadros, verboso=False):
    """Roda a ROM, entra no mapa pelo menu de debug e lê gObjectEvents.

    Por objeto vivo (16 slots de 0x24 bytes, `include/global.fieldmap.h`):
    0x0C initialCoords, 0x10 currentCoords e o byte 0x19, que é
    `range` (rangeX nos 4 bits baixos, rangeY nos altos). As coordenadas têm
    MAP_OFFSET (7) somado. Devolve {célula inicial: dados} e imprime a comparação com a
    lente: célula VISITADA fora do alcance calculado é defeito da lente.
    """
    import testa_critico as T
    simb = T.carrega_simbolos(os.path.splitext(rom)[0] + ".map")
    por_nome, _por_id = T.carrega_mapas()
    tab_flags = T.carrega_flags()
    caso = {"warp": mapa_const, "warp_id": warp_id,
            "roteiro": ",".join([f"{quadros}:NADA"] * passos)}
    roteiro = T.monta_roteiro(caso, por_nome, tab_flags)
    base = int(simb["gObjectEvents"], 16)
    cmd = [T.RUNNER, rom, "900", roteiro, "/dev/null", "--dump-estado", "--sem-png",
           "--sb1ptr", simb["gSaveBlock1Ptr"], "--partycount", simb["gPartiesCount"],
           "--oponente", simb["gTrainerBattleParameter"]]
    for i in range(16):
        for off in (0x00, 0x0C, 0x10, 0x18):   # 64 leituras, o teto do runner
            cmd += ["--mem32", hex(base + i * 0x24 + off)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    estados = []
    for linha in p.stdout.splitlines():
        m = T.LINHA_ESTADO.match(linha)
        if m:
            estados.append(dict((k, int(v, 0)) for k, _, v in
                                (par.partition("=") for par in m.group(2).split())))
    if not estados:
        raise SystemExit("o runner não imprimiu estado nenhum:\n" + p.stderr[-800:])
    g, n = por_nome[mapa_const]

    def s16(v):
        return v - 0x10000 if v & 0x8000 else v

    vistos = {}
    for k, e in enumerate(estados):
        if (e.get("grupo"), e.get("num")) != (g, n):
            continue
        for i in range(16):
            ler = lambda off: e["mem32_0x%08X" % (base + i * 0x24 + off)]  # noqa: E731
            bits = ler(0x00)
            if not bits & 1 or bits & (1 << 16):
                continue
            ini = (s16(ler(0x0C) & 0xFFFF) - 7, s16(ler(0x0C) >> 16) - 7)
            cur = (s16(ler(0x10) & 0xFFFF) - 7, s16(ler(0x10) >> 16) - 7)
            rng = (ler(0x18) >> 8) & 0xFF
            d = vistos.setdefault(ini, {"inicial": ini, "range_x": rng & 0xF,
                                               "range_y": rng >> 4, "celulas": set(),
                                               "linha": []})
            d["celulas"].add(cur)
            d["linha"].append((k, cur))
    return vistos, len(estados)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mapa", action="append", help="só este mapa (repetível)")
    ap.add_argument("--regra", choices=("motor", "leitura-0ak"), default="motor")
    ap.add_argument("--so-zero", action="store_true",
                    help="só NPC com raio zero num eixo no map.json")
    ap.add_argument("--json", help="grava a medição inteira neste arquivo")
    ap.add_argument("-v", action="store_true", help="imprime todo NPC, não só os de conserto")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--emulador", metavar="MAP_X")
    ap.add_argument("--warp-id", type=int, default=0)
    ap.add_argument("--rom", default=os.path.join(RAIZ, "pokeemerald.gba"))
    ap.add_argument("--passos", type=int, default=200)
    ap.add_argument("--quadros", type=int, default=60)
    ap.add_argument("--linha", metavar="X,Y",
                    help="com --emulador: imprime a posição, estado a estado, do "
                         "objeto que NASCEU em X,Y (é assim que se escolhe o "
                         "quadro de um caso de teste)")
    a = ap.parse_args()

    if a.demo:
        return demo()
    if a.emulador:
        vistos, n = emulador(a.rom, a.emulador, a.warp_id, a.passos, a.quadros)
        nome = next(os.path.basename(os.path.dirname(p)) for p in
                    glob.glob(os.path.join(RAIZ, "data", "maps", "*", "map.json"))
                    if json.load(open(p, encoding="utf-8")).get("id") == a.emulador)
        lente = {(r["x"], r["y"]): r for r in mede_mapa(nome, "motor", {})}
        velha = {(r["x"], r["y"]): r for r in mede_mapa(nome, "leitura-0ak", {})}
        mp = R.Mapa(nome)
        ruim = 0
        print(f"{n} estados lidos em {a.emulador}")
        for _ini, d in sorted(vistos.items()):
            ini = d["inicial"]
            r = lente.get(ini)
            if r is None:
                continue
            cel = mp.alcance_do_npc(ini[0], ini[1], r["raio_json"][0], r["raio_json"][1],
                                    "MOVEMENT_TYPE_" + r["tipo"])
            fora = sorted(c for c in d["celulas"] if c not in cel)
            dx = max(abs(c[0] - ini[0]) for c in d["celulas"])
            dy = max(abs(c[1] - ini[1]) for c in d["celulas"])
            ruim += bool(fora)
            print(f"  #{r['indice']:<3} {r['tipo']:22} em {ini} raio json {tuple(r['raio_json'])} "
                  f"EWRAM range=({d['range_x']},{d['range_y']}) visitou {len(d['celulas'])} "
                  f"células, desvio máx ({dx},{dy}); lente motor {r['celulas']}, "
                  f"leitura 0.ak {velha[ini]['celulas']}"
                  + (f"  FORA DA LENTE: {fora[:6]}" if fora else ""))
        if a.linha:
            alvo = tuple(int(v) for v in a.linha.split(","))
            for k, cur in vistos.get(alvo, {}).get("linha", []):
                print(f"    estado {k:5} {cur}")
        print("EMULADOR:", "a lente cobre tudo que o jogo fez" if not ruim
              else f"{ruim} objeto(s) andaram FORA do alcance calculado")
        return 1 if ruim else 0

    tudo, erros = mede_tudo(a.regra, a.so_zero, a.mapa)
    zero = [r for r in tudo if 0 in r["raio_json"]]
    cons = [r for r in tudo if r["conserta"]]
    for r in (tudo if a.v else cons):
        print(f"  {'CONSERTA' if r['conserta'] else 'herdado '} {r['mapa']:34} #{r['indice']:<3} "
              f"{r['tipo']:24} ({r['x']},{r['y']}) raio {tuple(r['raio_json'])} "
              f"-> {r['celulas']} células" + (f"  alcança {r['alcanca']}" if r["alcanca"] else ""))
    for nome, ex in erros:
        print(f"  pulei {nome}: {ex}")
    mapas_zero = {r["mapa"] for r in zero}
    print(f"regra {a.regra}: {len(tudo)} NPC de tipo com raio; {len(zero)} com raio zero "
          f"num eixo em {len(mapas_zero)} mapas; maior alcance "
          f"{max((r['celulas'] for r in tudo), default=0)}; {len(cons)} no critério de conserto")
    if a.json:
        # a leitura antiga vai ao lado, NPC por NPC, para que o número da 0.ak
        # (e o de qualquer lente que repita o erro) seja comparável
        outra = "leitura-0ak" if a.regra == "motor" else "motor"
        par = {(r["mapa"], r["indice"]): r["celulas"]
               for r in mede_tudo(outra, a.so_zero, a.mapa)[0]}
        linhas = []
        for r in tudo:
            r = dict(r, **{"celulas_" + outra.replace("-", "_"): par.get((r["mapa"], r["indice"]))})
            r["situacao"] = "CONSERTAR" if r["conserta"] else "herdado"
            linhas.append(r)
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"gerado_por": "dev_scripts/alcance_npc_errante.py",
                       "regra": a.regra, "limiar_celulas": LIMIAR,
                       "so_raio_zero": a.so_zero, "npc": linhas}, f,
                      ensure_ascii=False, indent=1)
            f.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
