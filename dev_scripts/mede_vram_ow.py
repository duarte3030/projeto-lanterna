#!/usr/bin/env python3
"""Mede no emulador QUEM cai no plano B de folha de sprite (T355) num mapa.

Uso:
    python3 dev_scripts/mede_vram_ow.py --mapa MtCoronet_B1F --warp 0 \\
        --alvos 7,9 [--alvos 4,30 ...] [--png-destino PASTA] [--rom ROM]

Por que existe (fila de bugs 3, dívidas, 01/10/2026): `varre_vram_ow.py` faz a
conta ESTÁTICA (pior caso, sem flag e sem fragmentação) e apontou 7 mapas onde a
VRAM de sprites pode estourar. O contador `gOwSheetFallbackCount` do plano B
(src/event_object_movement.c, OwSheetFallback_*) diz QUANTOS objetos caíram no
plano B, mas não QUAIS. Esta ferramenta responde "quais", lendo a memória do
jogo a cada passo de uma caminhada de verdade:

1. entra no mapa pelo menu de debug (warp `--warp`) e anda até cada `--alvos`
   pela rota de `rota_de_teste.py` (busca em largura com a régua do motor);
2. roda DUAS vezes o mesmo roteiro, porque o runner lê no máximo 64 palavras de
   32 bits por passo: a primeira lê os 16 `gObjectEvents` (bits, localId,
   coordenadas e spriteId), a segunda os 64 `gSprites[i].images`. O relógio do
   runner é pregado, então as duas rodadas são o MESMO jogo; o contador do
   plano B é lido nas duas e a ferramenta recusa se divergir;
3. objeto no plano B é o que tem `sprite->images` apontando para a EWRAM
   (`sOwSheetFallbackImages`); com folha normal ele aponta para a ROM.

Imprime, por objeto atingido: localId, espécie (do map.json), célula, e se ele
estava NA TELA no passo em que caiu. Com `--png-destino`, copia o quadro desse
passo para lá (nunca sobrescreve: soma -v2, -v3).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import testa_critico as T          # noqa: E402
import rota_de_teste as R          # noqa: E402

EWRAM = (0x02000000, 0x02040000)
TAM_OBJ = 0x24
TAM_SPRITE = 0x44


def le_estados(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    estados = []
    for linha in p.stdout.splitlines():
        m = T.LINHA_ESTADO.match(linha)
        if m:
            d = {"rotulo": m.group(1)}
            for par in m.group(2).split():
                k, _, v = par.partition("=")
                d[k] = int(v, 0)
            estados.append(d)
    if not estados:
        raise SystemExit("o runner não imprimiu estado nenhum:\n" + p.stderr[-800:])
    return estados


def s16(v):
    return v - 0x10000 if v & 0x8000 else v


def nome_livre(destino):
    if not os.path.exists(destino):
        return destino
    base, ext = os.path.splitext(destino)
    n = 2
    while os.path.exists(f"{base}-v{n}{ext}"):
        n += 1
    return f"{base}-v{n}{ext}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mapa", required=True, help="pasta em data/maps")
    ap.add_argument("--warp", type=int, default=0)
    ap.add_argument("--alvos", action="append", default=[], metavar="X,Y")
    ap.add_argument("--rom", default=os.path.join(T.RAIZ, "pokeemerald.gba"))
    ap.add_argument("--png-destino", help="pasta para o quadro do objeto atingido")
    ap.add_argument("--prefixo-png", default="vram-sprites")
    a = ap.parse_args()

    mapfile = os.path.splitext(a.rom)[0] + ".map"
    simb = T.carrega_simbolos(mapfile)
    # gSprites não está na lista do testa_critico: lido aqui, do mesmo .map.
    for linha in open(mapfile):
        partes = linha.split()
        if len(partes) == 2 and partes[1] == "gSprites" and partes[0].startswith("0x"):
            simb["gSprites"] = partes[0]
            break
    else:
        raise SystemExit("gSprites não está no .map")
    por_nome, _ = T.carrega_mapas()
    tab_flags = T.carrega_flags()
    mj = json.load(open(os.path.join(T.RAIZ, "data", "maps", a.mapa, "map.json")))
    const = mj["id"]
    objs = mj.get("object_events", [])
    por_local = {}
    for i, o in enumerate(objs):
        por_local[int(o.get("local_id", i + 1)) if str(o.get("local_id", "")).isdigit()
                  else i + 1] = o

    # Rodada 0: só entra, para saber onde o jogador chega e para onde olha.
    base_obj = int(simb["gObjectEvents"], 16)
    base_spr = int(simb["gSprites"], 16)
    contador = int(simb["gOwSheetFallbackCount"], 16)
    comum = ["--dump-estado", "--sb1ptr", simb["gSaveBlock1Ptr"],
             "--partycount", simb["gPartiesCount"],
             "--oponente", simb["gTrainerBattleParameter"],
             "--rtc-hora", "12", "--mem16", hex(contador)]
    flags = ["FLAG_SEM_ENCONTRO_SELVAGEM"]

    def roteiro(passos):
        caso = {"warp": const, "warp_id": a.warp, "flags": flags,
                "roteiro": ",".join(["120:NADA"] + passos + ["120:NADA"])}
        return T.monta_roteiro(caso, por_nome, tab_flags)

    def jogador(e):
        for i in range(16):
            b = e.get("mem32_0x%08X" % (base_obj + i * TAM_OBJ))
            if b is not None and b & 1 and b & (1 << 16):
                xy = e["mem32_0x%08X" % (base_obj + i * TAM_OBJ + 0x10)]
                return (s16(xy & 0xFFFF) - 7, s16(xy >> 16) - 7)
        return None

    leituras_obj = []
    for i in range(16):
        for off in (0x00, 0x08, 0x10, 0x20):
            leituras_obj += ["--mem32", hex(base_obj + i * TAM_OBJ + off)]
    leituras_spr = []
    for s in range(64):
        leituras_spr += ["--mem32", hex(base_spr + s * TAM_SPRITE + 0x0C)]

    saida = os.environ.get("SAIDA_TESTES", "/tmp/claude-501/mede_vram_ow")
    os.makedirs(saida, exist_ok=True)
    leituras_r0 = []
    for i in range(16):
        for off in (0x00, 0x10, 0x18):
            leituras_r0 += ["--mem32", hex(base_obj + i * TAM_OBJ + off)]
    e0 = le_estados([T.RUNNER, a.rom, "900", roteiro([]), f"{saida}/r0.png",
                     "--sem-png"] + comum + leituras_r0)
    pos = jogador(e0[-1])
    # Para onde o jogador olha ao chegar: o primeiro aperto numa direção nova só
    # vira, e errar isto desloca a caminhada inteira em uma célula.
    olhando = None
    for i in range(16):
        b = e0[-1].get("mem32_0x%08X" % (base_obj + i * TAM_OBJ))
        if b is not None and b & 1 and b & (1 << 16):
            face = e0[-1]["mem32_0x%08X" % (base_obj + i * TAM_OBJ + 0x18)] & 0xF
            olhando = {1: "DOWN", 2: "UP", 3: "LEFT", 4: "RIGHT"}.get(face)
    if pos is None or (e0[-1].get("grupo"), e0[-1].get("num")) != por_nome[const]:
        raise SystemExit(f"não entrei em {const} pelo warp {a.warp}")

    m = R.Mapa(a.mapa)
    # Linha de visão de treinador também é bloqueio: um passo nela começa uma
    # batalha, e a caminhada inteira sai do plano (medido em Victory Road 2F e
    # na Viridian Forest). Direção pelo tipo de movimento; tipo que gira ou
    # anda conta as quatro.
    vira = {"UP": [(0, -1)], "DOWN": [(0, 1)], "LEFT": [(-1, 0)], "RIGHT": [(1, 0)]}
    for o in objs:
        if o.get("trainer_type") not in ("TRAINER_TYPE_NORMAL", "TRAINER_TYPE_SEE_ALL_DIRECTIONS"):
            continue
        alcance = int(o.get("trainer_sight_or_berry_tree_id") or 0)
        tipo = o.get("movement_type", "")
        dirs = []
        if tipo.startswith("MOVEMENT_TYPE_FACE_") and o.get("trainer_type") == "TRAINER_TYPE_NORMAL":
            for parte in tipo[len("MOVEMENT_TYPE_FACE_"):].split("_AND_"):
                dirs += vira.get(parte, [])
        if not dirs:
            dirs = [v[0] for v in vira.values()]
        for dx, dy in dirs:
            x, y = o["x"], o["y"]
            for _ in range(alcance):
                x, y = x + dx, y + dy
                if not (0 <= x < m.w and 0 <= y < m.h) or m.col(x, y):
                    break
                m.occ.add((x, y))
    passos, onde = [], pos
    for alvo in a.alvos:
        fim = tuple(int(v) for v in alvo.split(","))
        cam = R.busca(m, onde, fim)
        if cam is None:
            # Alvo fora do chão alcançável (a conta estática aponta até
            # coordenada negativa): vai à célula alcançável mais perto dele.
            alcance = R.Mapa.alcance_do_npc(m, onde[0], onde[1], 0, 0, None,
                                            bloqueios=m.occ, raio_minimo=False)
            perto = min(alcance, key=lambda c: (abs(c[0] - fim[0]) + abs(c[1] - fim[1]), c))
            print(f"alvo {fim} sem rota; vou a {perto}, a célula alcançável mais perto")
            fim = perto
            cam = R.busca(m, onde, fim)
        ps = R.pernas(cam, olhando)
        onde, olhando = R.anda(m, onde, olhando, ps)
        # Uma perna por passo do roteiro, no formato de rota_de_teste.py, que
        # é o calibrado (o aperto a mais de cada virada está em `pernas`).
        passos += [f"24:{d}*{n}" for d, n in ps]
    r = roteiro(passos)

    prefixo = f"{saida}/{a.mapa}"
    for f in os.listdir(saida):
        if f.startswith(a.mapa + "-") and f.endswith(".png"):
            os.remove(os.path.join(saida, f))
    eo = le_estados([T.RUNNER, a.rom, "900", r, f"{prefixo}.png"] + comum + leituras_obj)
    es = le_estados([T.RUNNER, a.rom, "900", r, f"{saida}/descarte.png", "--sem-png"]
                    + comum + leituras_spr)
    chave_c = "mem16_0x%08X" % contador
    if len(eo) != len(es) or any(x.get(chave_c) != y.get(chave_c) for x, y in zip(eo, es)):
        raise SystemExit("as duas rodadas divergiram (contador ou número de passos): "
                         "a medição não vale")

    g, n = por_nome[const]
    atingidos = {}
    for k, (x, y) in enumerate(zip(eo, es)):
        if (x.get("grupo"), x.get("num")) != (g, n):
            continue
        pj = jogador(x)
        for i in range(16):
            ler = lambda off: x["mem32_0x%08X" % (base_obj + i * TAM_OBJ + off)]  # noqa: E731
            bits = ler(0x00)
            if not bits & 1 or bits & (1 << 16):
                continue
            local = ler(0x08) & 0xFF
            cel = (s16(ler(0x10) & 0xFFFF) - 7, s16(ler(0x10) >> 16) - 7)
            sid = (ler(0x20) >> 24) & 0xFF
            if sid >= 64:
                continue
            img = y["mem32_0x%08X" % (base_spr + sid * TAM_SPRITE + 0x0C)]
            if not EWRAM[0] <= img < EWRAM[1]:
                continue
            na_tela = (pj is not None and abs(cel[0] - pj[0]) <= 7
                       and -5 <= cel[1] - pj[1] <= 4)
            d = atingidos.setdefault(local, {"cel": cel, "passos": [], "tela": None,
                                             "jogador": pj})
            d["passos"].append(k)
            if na_tela and d["tela"] is None:
                d["tela"] = (x["rotulo"], pj)
    maximo = max(e.get(chave_c, 0) for e in eo)
    final = jogador(eo[-1])
    print(f"{a.mapa}: entrada {pos} pelo warp {a.warp}, caminho até {onde}, "
          f"{len(passos)} pernas; gOwSheetFallbackCount máximo {maximo}")
    if os.environ.get("MEDE_VRAM_TRILHA"):
        trilha = []
        for e in eo:
            pj = jogador(e)
            if pj and (not trilha or trilha[-1] != pj):
                trilha.append(pj)
        print("  trilha:", trilha)
    if final != onde:
        print(f"  AVISO: no emulador o jogador parou em {final}, e não em {onde}: "
              "a caminhada não foi a planejada (NPC, treinador ou regra que a "
              "rota não conhece); só vale o que foi medido até ali")
    if not atingidos:
        print("  nenhum objeto no plano B nesta caminhada")
    for local, d in sorted(atingidos.items()):
        o = por_local.get(local, {})
        gfx = o.get("graphics_id", "?")
        print(f"  localId {local:2d} {gfx:45s} célula {d['cel']} "
              f"(map.json {o.get('x')},{o.get('y')}, flag {o.get('flag')}); "
              + (f"NA TELA no passo {d['tela'][0]} com o jogador em {d['tela'][1]}"
                 if d["tela"] else "fora da tela em todos os passos medidos"))
        if d["tela"] and a.png_destino:
            png = f"{prefixo}-{d['tela'][0][len('passo'):]}.png"
            if os.path.exists(png):
                dest = nome_livre(os.path.join(a.png_destino,
                                               f"{a.prefixo_png}-{a.mapa}.png"))
                shutil.copy(png, dest)
                print(f"    quadro: {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
