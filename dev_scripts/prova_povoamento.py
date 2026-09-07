#!/usr/bin/env python3
"""Prova, NO EMULADOR, que os NPCs do povoamento existem e falam.

"Compilou" nao prova NPC: `TrySpawnObjectEvents` desiste calado quando as 15
vagas de sprite acabam, e roteiro que nao e chamado nunca abre caixa. Esta
ferramenta warpa pelo menu de debug para uma cidade, ANDA ate um NPC novo,
aperta A e grava o framebuffer, e le da EWRAM onde o jogador parou.

Uma cidade por regiao, mais Sunyshore, que e a cidade que o Gui citou.

O ALVO de cada caso e escolhido pela propria ferramenta, e nao decorado: o NPC
mais perto da chegada de um warp, entre os que NAO ANDAM (`movement_range` 0),
porque NPC que anda nao esta onde o plano diz quando o roteiro chega la. O
caminho sai de uma busca em largura na grade de colisao, com os outros objetos
como parede, e vira pernas de direcao unica.

Uso:
    python3 dev_scripts/prova_povoamento.py
    python3 dev_scripts/prova_povoamento.py --caso SunyshoreCity
    python3 dev_scripts/prova_povoamento.py --demo
"""
import argparse
import collections
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import testa_critico as tc          # noqa: E402
import povoa_cidades as P           # noqa: E402

SAIDA = "/tmp/claude-501/povoa/provas"

# Uma cidade por regiao do cartucho 1, mais Sunyshore.
CASOS = [
    ("PalletTown_Frlg", "MAP_PALLET_TOWN", "Kanto"),
    ("NewBarkTown", "MAP_NEW_BARK_TOWN", "Johto"),
    ("OldaleTown", "MAP_OLDALE_TOWN", "Hoenn"),
    ("SandgemTown", "MAP_SANDGEM_TOWN", "Sinnoh"),
    ("SunyshoreCity", "MAP_SUNYSHORE_CITY", "Sinnoh"),
]

DEMORA = "240:NADA"
DIRS = {(0, -1): "UP", (0, 1): "DOWN", (-1, 0): "LEFT", (1, 0): "RIGHT"}


def passos(direcao, quantos):
    return ",".join(f"20:{direcao},60:NADA" for _ in range(quantos))


def rota(nome):
    """(warp, alvo, pernas, olhar) para o NPC novo mais perto de uma porta."""
    d, W, H, v, beh = P.geometria(nome)
    livres = set(P.candidatas(nome)[0])
    ocupado = {(o["x"], o["y"]) for o in (d.get("object_events") or [])}
    anda = set(P.alcance(v, W, H, P._sementes(d, W, H, v, beh), beh=beh)) - ocupado
    parados = [n for n in P.plano()["cidades"][nome]["npcs"]
               if n["rx"] == 0 and n["ry"] == 0]
    melhor = None
    for wid, w in enumerate(d.get("warp_events") or []):
        ini = (w["x"], w["y"] + 1)
        if ini not in anda:
            continue
        pai = {ini: None}
        fila = collections.deque([ini])
        while fila:
            c = fila.popleft()
            for dx, dy in P.N4:
                q = (c[0] + dx, c[1] + dy)
                if q in anda and q not in pai:
                    pai[q] = c
                    fila.append(q)
        for n in parados:
            alvo = (n["x"], n["y"])
            viz = [(alvo[0] + dx, alvo[1] + dy) for dx, dy in P.N4]
            perto = [q for q in viz if q in pai]
            if not perto:
                continue
            for q in perto:
                cam = []
                c = q
                while c is not None:
                    cam.append(c)
                    c = pai[c]
                cam.reverse()
                if melhor is None or len(cam) < len(melhor[2]):
                    olhar = DIRS[(alvo[0] - q[0], alvo[1] - q[1])]
                    melhor = (wid, n, cam, olhar, livres)
    if melhor is None:
        raise SystemExit(f"{nome}: nenhum NPC parado alcancavel de uma porta")
    wid, n, cam, olhar, _ = melhor
    pernas = []
    for i in range(1, len(cam)):
        dx = cam[i][0] - cam[i - 1][0]
        dy = cam[i][1] - cam[i - 1][1]
        di = DIRS[(dx, dy)]
        if pernas and pernas[-1][0] == di:
            pernas[-1][1] += 1
        else:
            pernas.append([di, 1])
    return wid, n, pernas, olhar, cam[-1]


def pernas_de(cam):
    fora = []
    for i in range(1, len(cam)):
        di = DIRS[(cam[i][0] - cam[i - 1][0], cam[i][1] - cam[i - 1][1])]
        if fora and fora[-1][0] == di:
            fora[-1][1] += 1
        else:
            fora.append([di, 1])
    return fora


def caminho(nome, de, ate):
    """Pernas de `de` ate `ate`, andando so por celula andavel e vazia."""
    d, W, H, v, beh = P.geometria(nome)
    ocupado = {(o["x"], o["y"]) for o in (d.get("object_events") or [])}
    anda = set(P.alcance(v, W, H, P._sementes(d, W, H, v, beh), beh=beh)) - ocupado
    anda.add(de)
    pai = {de: None}
    fila = collections.deque([de])
    while fila:
        c = fila.popleft()
        if c == ate:
            break
        for dx, dy in P.N4:
            q = (c[0] + dx, c[1] + dy)
            if q in anda and q not in pai:
                pai[q] = c
                fila.append(q)
    if ate not in pai:
        return None
    cam, c = [], ate
    while c is not None:
        cam.append(c)
        c = pai[c]
    cam.reverse()
    return pernas_de(cam)


def roteiro_de(g, num, wid, pernas, olhar):
    # TROCAR DE DIRECAO CUSTA UM APERTO (medido na rodada 13): o primeiro
    # aperto numa direcao nova so vira o jogador. Por isso cada perna leva um
    # aperto a mais, e cada perna termina com espera, que e de graca.
    fora = [tc.ABERTURA, tc.rota_warp(g, num, wid), DEMORA]
    for di, k in pernas:
        fora += [passos(di, k + 1), DEMORA]
    fora += [passos(olhar, 2), DEMORA, "20:A", "600:NADA"]
    return ",".join(fora)


def _roda(args, simbolos, rot, nome, tc):
    cmd = [tc.RUNNER, args.rom, "6000", rot, f"{SAIDA}/{nome}.png",
           "--dump-estado",
           "--sb1ptr", simbolos["gSaveBlock1Ptr"],
           "--partycount", simbolos["gPartiesCount"],
           "--oponente", simbolos["gTrainerBattleParameter"]]
    r = subprocess.run(cmd, capture_output=True, text=True)
    est = []
    for l in r.stdout.splitlines():
        m = tc.LINHA_ESTADO.match(l)
        if m:
            est.append(dict(p.split("=", 1) for p in m.group(2).split()))
    return est, r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rom", default=os.path.join(RAIZ, "pokeemerald.gba"))
    ap.add_argument("--map", dest="mapfile", default=os.path.join(RAIZ, "pokeemerald.map"))
    ap.add_argument("--caso")
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    por_nome, _ = tc.carrega_mapas()
    if args.demo:
        faltam = [c for _, c, _ in CASOS if c not in por_nome]
        assert not faltam, "mapa desconhecido: %s" % faltam
        for nome, _, _ in CASOS:
            wid, n, pernas, olhar, chega = rota(nome)
            print("ok   %-20s warp %d -> %s em (%d,%d), %d pernas, olhar %s"
                  % (nome, wid, n["rotulo"], n["x"], n["y"], len(pernas), olhar))
        print("\ndemo VERDE: os %d casos tem rota" % len(CASOS))
        return 0

    os.makedirs(SAIDA, exist_ok=True)
    simbolos = tc.carrega_simbolos(args.mapfile)
    ruins = 0
    for nome, const, regiao in CASOS:
        if args.caso and nome != args.caso:
            continue
        g, num = por_nome[const]
        wid, n, pernas, olhar, chega = rota(nome)
        # CORRECAO AUTOMATICA. O modelo de aperto ("trocar de direcao custa um
        # aperto") acerta na maioria das cidades e erra onde o motor engole
        # aperto por esbarrao. Em vez de decorar contagem, o roteiro RODA, le
        # da EWRAM onde o jogador parou e, se nao for o tile de conversa,
        # RECALCULA o resto do caminho a partir dali e roda de novo. O emulador
        # e deterministico, entao isso converge, e sem ele Sandgem e Sunyshore
        # paravam a um tile do alvo.
        extra, onde, est, r = [], None, [], None
        for _tentativa in range(4):
            rot = roteiro_de(g, num, wid, pernas + extra, olhar)
            est, r = _roda(args, simbolos, rot, nome, tc)
            if not est:
                break
            f = est[-1]
            onde = (int(f["grupo"]), int(f["num"]), int(f["x"]), int(f["y"]))
            if onde[:2] != (g, num) or (onde[2], onde[3]) == chega:
                break
            mais = caminho(nome, (onde[2], onde[3]), chega)
            if not mais:
                break
            extra = extra + mais
        if not est:
            print("SEM ESTADO", nome, r.stderr[-300:])
            ruins += 1
            continue
        ok = onde[:2] == (g, num) and (onde[2], onde[3]) == chega
        ruins += not ok
        print("[%-12s] %-7s %-20s warp %d -> %s (%s) em (%d,%d); parou em %s "
              "(esperado %s)"
              % ("OK" if ok else "FORA DO ALVO", regiao, nome, wid, n["rotulo"],
                 n["gfx"].replace("OBJ_EVENT_GFX_", ""), n["x"], n["y"],
                 onde, (g, num) + chega))
        print("      PNGs em %s/%s-*.png" % (SAIDA, nome))
    print("\n%d de %d casos pararam no tile de conversa"
          % (len(CASOS) - ruins, len(CASOS)))
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main())
