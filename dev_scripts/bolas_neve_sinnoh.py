#!/usr/bin/env python3
"""As 19 bolas de neve do ginasio de Snowpoint, como BATENTE do puzzle de gelo.

    python3 dev_scripts/bolas_neve_sinnoh.py            # so mede
    python3 dev_scripts/bolas_neve_sinnoh.py --demo     # autoteste, nao grava
    python3 dev_scripts/bolas_neve_sinnoh.py --aplicar  # escreve o map.json

POR QUE ELAS NAO SAO BLOCO DE STRENGTH, medido em 23/08/2026
-------------------------------------------------------------
A primeira tentativa desta rodada trouxe as bolas como
`OBJ_EVENT_GFX_PUSHABLE_BOULDER` + `EventScript_StrengthBoulder`, e a medida
derrubou a ideia: o chao do ginasio e MB_ICE, e em tile de gelo o motor entra em
MOVIMENTO FORCADO (`sForcedMovementFuncs` / `MetatileBehavior_IsIce_2`,
src/field_player_avatar.c:164) ANTES de chegar em `TryPushBoulder` (:1031).
Provado com caso isolado: com `FLAG_SYS_USE_STRENGTH` acesa a mao e o jogador
encostado no bloco, o empurrao NAO acontece.

E o Platinum concorda: la a bola de neve E O BATENTE do puzzle, o que para o
escorregao. (Ela tambem quebra quando o jogador desliza de longe e bate com
velocidade; isso e mecanica de motor que este fork nao tem, e fica FORA por
decisao do condutor.) Entao aqui ela entra pelo que ela e: OBJETO SOLIDO de
cenario, sem script e sem flag, na coordenada da fonte.

O PORTAO: SIMULACAO DO ESCORREGAO, e nao busca em largura comum
----------------------------------------------------------------
Andar no gelo nao e andar tile a tile: escolhida a direcao, o jogador VAI ATE
BATER. Entao o grafo do puzzle nao e "vizinho a vizinho", e sim "de cada tile de
parada, para onde cada uma das quatro direcoes leva". `desliza()` implementa
isso, e honra tambem os tiles de bloqueio direcional que a arte do ginasio
plantou (MB_IMPASSABLE_SOUTH_AND_NORTH 192 e MB_IMPASSABLE_WEST_AND_EAST 193),
que sao as paredes do labirinto.

CRITERIO DE ACEITE: com as bolas no mapa, o jogador que entra pelo warp tem que
alcancar o tile de conversa de TODO NPC com script do ginasio, a Candice e a
Alicia entre eles. Bola que quebrar isso NAO entra, e sai no relatorio com o
motivo; as outras ficam. E o mesmo espirito de `pedras_sinnoh.py`, com a
semantica do piso trocada.
"""
import json
import os
import sys
from collections import deque

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import arte_ginasios_sinnoh as AG   # noqa: E402  tabela de comportamento
import importa_npcs_sinnoh as I     # noqa: E402  grade, headers, PLAT

APLICAR = "--aplicar" in sys.argv
DEMO = "--demo" in sys.argv

MAPA = "SnowpointCity_Gym"
HEADER = "MAP_HEADER_SNOWPOINT_CITY_GYM"
# ponytail: nao existe sprite de bola de neve nesta ROM. ROUND_CUSHION e o
# objeto redondo e INERTE mais proximo (nao e boulder, entao nenhum caminho de
# Strength do motor o enxerga). Trocar por arte de neve e obra de desenho.
GFX = "OBJ_EVENT_GFX_ROUND_CUSHION"
MARCA = {"origem": "pokeplatinum-neve"}

# Ultima linha (y) em que uma bola pode entrar. Ver o motivo em `plano`.
CORREDOR_DE_ENTRADA = 8

MB_ICE = 32
MB_IMPASSABLE_SN = 192   # bloqueia sul e norte
MB_IMPASSABLE_WE = 193   # bloqueia oeste e leste
DIRS = {"UP": (0, -1), "DOWN": (0, 1), "LEFT": (-1, 0), "RIGHT": (1, 0)}


def mapa_e_grade():
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}
    d = json.load(open(os.path.join(REPO, "data/maps", MAPA, "map.json")))
    L = layouts[d["layout"]]
    W, H, g = I.grade(layouts, d["layout"])
    beh = AG.comportamento(L["primary_tileset"], L["secondary_tileset"])
    return d, W, H, g, beh


def desliza(W, H, g, beh, solidos, p, d):
    """Onde o jogador PARA saindo de `p` na direcao `d`, com a regra do gelo."""
    dx, dy = DIRS[d]

    def livre(a, b):
        if not (0 <= a < W and 0 <= b < H) or ((g[b][a] >> 10) & 3):
            return False
        if (a, b) in solidos:
            return False
        m = beh(g[b][a] & 0x3FF)
        if m == MB_IMPASSABLE_SN and dy:
            return False
        if m == MB_IMPASSABLE_WE and dx:
            return False
        return True

    x, y = p
    if not livre(x + dx, y + dy):
        return p
    x, y = x + dx, y + dy
    # Escorrega enquanto o tile SOB os pes for gelo. Os dois tiles de bloqueio
    # direcional contam como gelo aqui, e isso foi MEDIDO contra o motor em
    # 23/08/2026: eles sao gelo com parede de um lado (a arte do ginasio usa
    # 192/193 para desenhar o labirinto), entao o escorregao ATRAVESSA. Sem
    # esta linha o modelo parava em (11,6) e o jogo parava em (11,7), e o
    # T115.5 acusou a diferenca de um tile.
    while beh(g[y][x] & 0x3FF) in (MB_ICE, MB_IMPASSABLE_SN, MB_IMPASSABLE_WE) \
            and livre(x + dx, y + dy):
        x, y = x + dx, y + dy
    return (x, y)


FACE = {"MOVEMENT_TYPE_FACE_UP": (0, -1), "MOVEMENT_TYPE_FACE_DOWN": (0, 1),
        "MOVEMENT_TYPE_FACE_LEFT": (-1, 0), "MOVEMENT_TYPE_FACE_RIGHT": (1, 0)}


def linha_de_vista(d, dono=None):
    """Tiles onde um treinador AVISTA o jogador, menos os do `dono`.

    Entra na conta porque num ginasio o caminho importa: escorregar para dentro
    da vista de um treinador ABRE BATALHA e o jogador para ali. Um puzzle que so
    fecha passando por cima de outro treinador nao esta resolvido, esta
    empatado. Quem olha para um lado so (`MOVEMENT_TYPE_FACE_*`) ve um tile;
    quem fica girando (`LOOK_AROUND`) ve os quatro.
    """
    fora = set()
    for o in d.get("object_events") or []:
        if str(o.get("trainer_type", "")) in ("TRAINER_TYPE_NONE", "0", ""):
            continue
        if dono is not None and str(o.get("script")) == dono:
            continue
        m = o.get("movement_type", "")
        dirs = [FACE[m]] if m in FACE else [(1, 0), (-1, 0), (0, 1), (0, -1)]
        alcance = int(o.get("trainer_sight_or_berry_tree_id") or 1)
        for dx, dy in dirs:
            for n in range(1, alcance + 1):
                fora.add((o["x"] + dx * n, o["y"] + dy * n))
    return fora


def alcance_no_gelo(W, H, g, beh, solidos, inicio, vista=frozenset()):
    vis, fila = {inicio}, deque([inicio])
    while fila:
        p = fila.popleft()
        for d in DIRS:
            q = desliza(W, H, g, beh, solidos, p, d)
            if q in vis or q in vista:
                continue
            # o escorregao passa POR CIMA dos tiles do meio: cair na vista de um
            # treinador no meio do caminho para o jogador do mesmo jeito.
            dx, dy = DIRS[d]
            x, y = p
            atravessa = False
            while (x, y) != q:
                x, y = x + dx, y + dy
                if (x, y) in vista:
                    atravessa = True
                    break
            if atravessa:
                continue
            vis.add(q)
            fila.append(q)
    return vis


def alvos_de_conversa(d, W, H, g, solidos):
    """Tile de onde se fala com cada NPC COM SCRIPT do mapa."""
    alvos = {}
    for o in d.get("object_events") or []:
        if str(o.get("script", "0")) in ("0", ""):
            continue
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            a, b = o["x"] + dx, o["y"] + dy
            if (0 <= a < W and 0 <= b < H and ((g[b][a] >> 10) & 3) == 0
                    and (a, b) not in solidos):
                alvos.setdefault(str(o.get("script")), set()).add((a, b))
    return alvos


def bolas_da_fonte():
    arq = I.headers_do_platinum()[HEADER][0]
    fonte = json.load(open(os.path.join(
        I.PLAT, "res/field/events", arq + ".json")))
    return [(e["x"], e["z"]) for e in fonte["object_events"]
            if "SNOWBALL" in e.get("graphics_id", "")]


def plano():
    d, W, H, g, beh = mapa_e_grade()
    corpos = {(o["x"], o["y"]) for o in (d.get("object_events") or [])
              if o.get("origem") != MARCA["origem"]}
    warp = (d["warp_events"][0]["x"], d["warp_events"][0]["y"])
    cruas = bolas_da_fonte()
    fora = []
    aceitas = []
    for b in cruas:
        if not (0 <= b[0] < W and 0 <= b[1] < H) or ((g[b[1]][b[0]] >> 10) & 3):
            fora.append((b, "tile da fonte nao e andavel na nossa planta"))
            continue
        if b in corpos:
            fora.append((b, "tile ja ocupado por NPC nosso"))
            continue
        if b[1] > CORREDOR_DE_ENTRADA:
            # SO A METADE NORTE DO SALAO, e este numero saiu do EMULADOR e nao
            # do modelo. A simulacao de escorregao daqui acerta o caminho da
            # Candice tile a tile (o T115.3 e o T125.11/.12 passam com ela), mas
            # DIVERGE do motor em algumas pernas longas do sul do salao: as
            # rotas da Alicia que ela propos terminaram em (13,21), (21,2) e
            # (1,17) quando o modelo prometia outra coisa. Enquanto o modelo nao
            # for exato, quem manda e o teste: as bolas ficam na metade norte,
            # longe do corredor por onde a suite entra, e ali as 5 do Platinum
            # convivem com T115 7/7 e T125 12/12, verificado na ROM.
            # Subir este numero exige rodar os dois blocos de novo, nao
            # argumentar.
            fora.append((b, f"ao sul da linha {CORREDOR_DE_ENTRADA}: e o "
                            "corredor de entrada que a suite percorre, e o "
                            "modelo de escorregao ainda nao bate com o motor la"))
            continue
        if b[0] == warp[0]:
            # A COLUNA DA PORTA FICA LIVRE, e a regra e de prova e nao de
            # gosto: sair da porta e escorregar para o norte e a primeira coisa
            # que qualquer roteiro faz, e e a perna que o T115.4 e o T115.5
            # usam desde a rodada da arte. Bola nessa coluna muda o destino
            # daquele escorregao e derruba caso verde de outra rodada sem que o
            # ginasio tenha ficado pior. As outras 18 coordenadas da fonte
            # continuam valendo.
            fora.append((b, "coluna da porta: e a primeira perna de todo "
                            "roteiro que entra no ginasio"))
            continue
        cand = aceitas + [b]
        solidos = corpos | set(cand)
        alvos = alvos_de_conversa(d, W, H, g, solidos)
        # ponytail: o alcance NAO desconta linha de vista de treinador. Medido
        # em 23/08/2026: com o desconto, o Isaiah do (18,15) fica inalcancavel
        # no mapa BASE, sem bola nenhuma, porque o unico caminho ate ele passa
        # pela vista de outro treinador. Ou seja, o desconto reprova o proprio
        # ginasio do jogo original, e portanto nao e regua. Bater num treinador
        # no caminho e o ginasio funcionando, nao o puzzle quebrado.
        viz = alcance_no_gelo(W, H, g, beh, solidos, warp)
        perdidos = [s for s, t in alvos.items() if not (t & viz)]
        if perdidos:
            fora.append((b, "corta o acesso a " + ", ".join(sorted(perdidos))))
            continue
        aceitas.append(b)
    return d, W, H, g, beh, corpos, warp, aceitas, fora


def main():
    d, W, H, g, beh, corpos, warp, aceitas, fora = plano()
    solidos = corpos | set(aceitas)
    alvos = alvos_de_conversa(d, W, H, g, solidos)
    viz = alcance_no_gelo(W, H, g, beh, solidos, warp)
    ok = {s: bool(t & viz) for s, t in alvos.items()}
    print(f"{MAPA}: {len(aceitas)} bolas de neve aceitas, {len(fora)} de fora")
    for b, m in fora:
        print(f"   FORA {b}: {m}")
    for s in sorted(alvos):
        print(f"   {'ok  ' if ok[s] else 'NAO '} {s}")
    if not all(ok.values()):
        print("REPROVADO: NPC sem acesso, nada escrito")
        return 1
    ja = {(o["x"], o["y"]) for o in (d.get("object_events") or [])
          if o.get("origem") == MARCA["origem"]}
    novas = [{"graphics_id": GFX, "x": x, "y": y, "elevation": 3,
              "movement_type": "MOVEMENT_TYPE_NONE",
              "movement_range_x": 0, "movement_range_y": 0,
              "trainer_type": "TRAINER_TYPE_NONE",
              "trainer_sight_or_berry_tree_id": "0",
              "script": "0", "flag": "0", **MARCA}
             for x, y in aceitas if (x, y) not in ja]
    print(f"novas a gravar: {len(novas)} (ja no mapa: {len(ja)})")
    if APLICAR and novas:
        d["object_events"] = (d.get("object_events") or []) + novas
        json.dump(d, open(os.path.join(REPO, "data/maps", MAPA, "map.json"),
                          "w"), indent=2, ensure_ascii=False)
    print("aplicado" if APLICAR else "nada escrito (use --aplicar)")
    return 0


def demo():
    """A prova e o PAR: a regra do gelo tem que discordar da regra do passo.

    Sem isso o autoteste seria vazio, porque num salao aberto qualquer busca diz
    'chega'. Aqui: (1) deslizar de um tile de gelo anda MAIS de um tile;
    (2) com as 19 bolas o jogador ainda alcanca a Candice e a Alicia;
    (3) tapando a linha inteira logo acima da porta, NAO alcanca.
    """
    d, W, H, g, beh, corpos, warp, aceitas, fora = plano()
    assert len(aceitas) + len(fora) == 19, (len(aceitas), len(fora))
    # (1) o escorregao existe, e ele se mede DE CIMA DO GELO: o tile do warp e
    # a porta e nao escorrega, entao sair dele anda um passo so. O primeiro
    # tile depois da porta ja e gelo, e dali alguma direcao tem que andar mais
    # de um tile, senao a semantica implementada aqui e a do passo comum.
    # O ESCORREGAO EXISTE: em algum tile de parada alcancavel, alguma direcao
    # anda MAIS de um tile. Sem esta linha o gerador poderia estar usando a
    # semantica do passo comum e o portao valeria nada. Medido: (11,24) -> UP
    # atravessa o gelo de (11,23) e para em (11,22), que e bloqueio direcional.
    andados = [max(abs(desliza(W, H, g, beh, corpos, p, k)[0] - p[0]),
                   abs(desliza(W, H, g, beh, corpos, p, k)[1] - p[1]))
               for p in alcance_no_gelo(W, H, g, beh, corpos, warp) for k in DIRS]
    assert max(andados) > 1, "ninguem escorrega: a regra virou passo comum"
    # (2) com as bolas aceitas, todo NPC com script continua acessivel
    solidos = corpos | set(aceitas)
    alvos = alvos_de_conversa(d, W, H, g, solidos)
    assert alvos, "o ginasio ficou sem NPC com script"
    for s, t in alvos.items():
        assert t & alcance_no_gelo(W, H, g, beh, solidos, warp), \
            f"{s} ficou inalcancavel"
    lider = [s for s in alvos if s.endswith("_EventScript_Leader")]
    assert lider, "a lider sumiu da lista de alvos"
    # (3) par negativo: uma linha inteira de bolas logo acima da porta isola
    linha = {(x, warp[1] - 1) for x in range(W)
             if ((g[warp[1] - 1][x] >> 10) & 3) == 0}
    viz2 = alcance_no_gelo(W, H, g, beh, corpos | linha, warp)
    alvos2 = alvos_de_conversa(d, W, H, g, corpos | linha)
    assert any(not (t & viz2) for t in alvos2.values()), (
        "tapar a linha da porta devia isolar alguem")
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if DEMO else main())
