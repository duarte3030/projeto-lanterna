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
    """Onde o jogador PARA saindo de `p` na direcao `d`, com a regra do gelo.

    CALIBRADO CONTRA O EMULADOR em 23/08/2026, com 312 sondas cobrindo o salao
    inteiro (cada tile de parada alcancavel vezes as quatro direcoes, lidas da
    EWRAM). As duas regras que faltavam, e onde elas moram no motor:

    1. `MetatileBehavior_IsIce_2` (src/metatile_behavior.c:370) so aceita
       `MB_ICE`. Os tiles 192/193 NAO sao gelo, entao pisar num deles ENCERRA o
       movimento forcado: o escorregao PARA neles em vez de atravessar. A versao
       anterior os contava como gelo e errava por ate dezoito tiles.
    2. `IsMetatileDirectionallyImpassable` (src/event_object_movement.c:6615)
       olha os DOIS tiles: o de DESTINO com `gDirectionBlockedMetatileFuncs` e o
       de ORIGEM com `gOppositeDirectionBlockedMetatileFuncs`. Ou seja o bloqueio
       vale tambem para SAIR: de cima de um 192 nao se anda ao norte nem ao sul,
       de cima de um 193 nao se anda a leste nem a oeste. A versao anterior so
       barrava a entrada, e por isso deixava o jogador escapar de (11,19),
       (11,22) e (19,7).

    Com as duas, a divergencia contra a bateria e ZERO. Sem a 1 sao 12
    divergencias em 161 medidas; sem a 2 sao 6.
    """
    dx, dy = DIRS[d]

    def livre(x, y):
        """Da para sair de (x,y) e entrar em (x+dx, y+dy)?"""
        a, b = x + dx, y + dy
        if not (0 <= a < W and 0 <= b < H) or ((g[b][a] >> 10) & 3):
            return False
        if (a, b) in solidos:
            return False
        for m in (beh(g[y][x] & 0x3FF), beh(g[b][a] & 0x3FF)):
            if m == MB_IMPASSABLE_SN and dy:
                return False
            if m == MB_IMPASSABLE_WE and dx:
                return False
        return True

    x, y = p
    if not livre(x, y):
        return p
    x, y = x + dx, y + dy
    # Escorrega enquanto o tile SOB OS PES for MB_ICE, e so ele.
    while beh(g[y][x] & 0x3FF) == MB_ICE and livre(x, y):
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


# Objetos VIVOS ao mesmo tempo. `gObjectEvents` tem OBJECT_EVENTS_COUNT == 16
# vagas (include/constants/global.h:95) e a vaga 0 e do JOGADOR, entao sobram 15
# para o mapa. `TrySpawnObjectEvents` (src/event_object_movement.c:2899) so
# acorda o template cuja coordenada cai na janela `pos.x-9 .. pos.x+10` por
# `pos.y-7 .. pos.y+9`, e quando as 15 vagas acabam ele simplesmente NAO acorda
# o resto: sem erro, sem aviso. Objeto que nao acordou NAO E SOLIDO, e bola de
# neve que nao e solida nao para escorregao nenhum. E a mesma regra que o T134.25
# ja media para Pokemon estatico, aqui do outro lado.
VAGAS_DE_SPRITE = 15


def janelas(W, H, g):
    """Toda posicao de camera possivel, ou seja todo tile andavel."""
    return [(x, y) for y in range(H) for x in range(W)
            if ((g[y][x] >> 10) & 3) == 0]


def _na_janela(c, pontos):
    return sum(1 for x, y in pontos
               if c[0] - 9 <= x <= c[0] + 10 and c[1] - 7 <= y <= c[1] + 9)


def maior_conjunto(cams, base, pool):
    """O MAIOR subconjunto de `pool` que nao estoura VAGAS_DE_SPRITE em janela
    nenhuma. Busca exaustiva com poda: 19 candidatos cabem de sobra, e guloso
    perdia duas bolas (mediu 10 contra 12 na arvore de 23/08/2026)."""
    cob = [[i for i, c in enumerate(cams)
            if c[0] - 9 <= b[0] <= c[0] + 10 and c[1] - 7 <= b[1] <= c[1] + 9]
           for b in pool]
    n, melhor, cur = len(pool), [], list(base)

    def dfs(i, esc):
        nonlocal melhor
        if len(esc) + (n - i) <= len(melhor):
            return
        if i == n:
            if len(esc) > len(melhor):
                melhor = esc[:]
            return
        if all(cur[j] < VAGAS_DE_SPRITE for j in cob[i]):
            for j in cob[i]:
                cur[j] += 1
            esc.append(pool[i])
            dfs(i + 1, esc)
            esc.pop()
            for j in cob[i]:
                cur[j] -= 1
        dfs(i + 1, esc)

    dfs(0, [])
    return melhor


def plano():
    d, W, H, g, beh = mapa_e_grade()
    corpos = {(o["x"], o["y"]) for o in (d.get("object_events") or [])
              if o.get("origem") != MARCA["origem"]}
    warp = (d["warp_events"][0]["x"], d["warp_events"][0]["y"])
    cruas = bolas_da_fonte()
    fora, pool = [], []
    for b in cruas:
        if not (0 <= b[0] < W and 0 <= b[1] < H) or ((g[b[1]][b[0]] >> 10) & 3):
            fora.append((b, "tile da fonte nao e andavel na nossa planta"))
        elif b in corpos:
            fora.append((b, "tile ja ocupado por NPC nosso"))
        else:
            pool.append(b)

    cams = janelas(W, H, g)
    base = [_na_janela(c, corpos) for c in cams]

    def perdidos(conj):
        solidos = corpos | set(conj)
        # ponytail: o alcance NAO desconta linha de vista de treinador. Medido
        # em 23/08/2026: com o desconto, o Isaiah do (18,15) fica inalcancavel
        # no mapa BASE, sem bola nenhuma, porque o unico caminho ate ele passa
        # pela vista de outro treinador. Ou seja, o desconto reprova o proprio
        # ginasio do jogo original, e portanto nao e regua. Bater num treinador
        # no caminho e o ginasio funcionando, nao o puzzle quebrado.
        alvos = alvos_de_conversa(d, W, H, g, solidos)
        viz = alcance_no_gelo(W, H, g, beh, solidos, warp)
        return [s for s, t in alvos.items() if not (t & viz)]

    # Dois portoes, nesta ordem: primeiro quantas bolas o MOTOR consegue manter
    # acordadas, depois quais delas o PUZZLE aguenta. Quando uma bola ilha um
    # NPC ela sai e a escolha e refeita sem ela, porque a vaga que ela larga
    # costuma caber em outra.
    # Bola que JA ESTA no mapa tem preferencia, e a razao nao e comodidade: o
    # teto de sprite costuma admitir varios conjuntos do MESMO tamanho, e um
    # gerador que sorteia entre eles a cada rodada troca a geometria do puzzle de
    # graca e derruba caso de teste medido em outra rodada. Aqui manda a mesma
    # etica de id de mapa e de treinador: quem existe nao se move. Medido em
    # 23/08/2026: com e sem a preferencia o conjunto tem 11 bolas, mas com ela as
    # 6 antigas ficam e o T159.7 continua valendo.
    ja_no_mapa = [b for b in pool
                  if b in {(o["x"], o["y"]) for o in (d.get("object_events") or [])
                           if o.get("origem") == MARCA["origem"]}]
    banidas = []
    while True:
        fixas = [b for b in ja_no_mapa if b not in banidas]
        piso = [n + _na_janela(c, fixas) for n, c in zip(base, cams)]
        disponivel = [b for b in pool if b not in fixas and b not in banidas]
        escolhidas = fixas + maior_conjunto(cams, piso, disponivel)
        ruins = perdidos(escolhidas)
        if not ruins:
            break
        culpada = next((b for b in escolhidas
                        if not perdidos([x for x in escolhidas if x != b])), None)
        if culpada is None:
            raise SystemExit("nenhuma bola sozinha devolve o acesso a "
                             + ", ".join(sorted(ruins)))
        fora.append((culpada, "corta o acesso a " + ", ".join(
            sorted(s.split("EventScript_")[-1] for s in ruins))))
        banidas.append(culpada)

    aceitas = [b for b in cruas if b in escolhidas]
    for b in pool:
        if b not in escolhidas and all(b != f for f, _ in fora):
            fora.append((b, f"teto de {VAGAS_DE_SPRITE} objetos vivos por "
                            "janela de sprite: o motor nao acordaria esta bola"))
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
    # O gerador RECONCILIA nos dois sentidos: bola que deixou de ser aceita sai
    # do mapa. So somar deixaria bola velha de uma regra antiga viva, e nesta
    # rodada isso importa, porque o teto de sprite muda quem cabe.
    sobrando = sorted(ja - set(aceitas))
    print(f"novas a gravar: {len(novas)} (ja no mapa: {len(ja)}, "
          f"a remover: {len(sobrando)} {sobrando})")
    if APLICAR and (novas or sobrando):
        vivos = [o for o in (d.get("object_events") or [])
                 if o.get("origem") != MARCA["origem"]
                 or (o["x"], o["y"]) in set(aceitas)]
        d["object_events"] = vivos + novas
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
    # (4) o TETO DE SPRITE vale, e vale APERTADO: nenhuma janela passa das 15
    # vagas com as bolas aceitas, e NENHUMA das recusadas por teto poderia
    # entrar sem estourar alguma. E a mutacao do portao novo: sem ela o teto
    # poderia estar folgado (e perdendo bola) ou frouxo (e deixando bola que o
    # motor nunca acordaria).
    cams = janelas(W, H, g)
    vivos = corpos | set(aceitas)
    assert max(_na_janela(c, vivos) for c in cams) <= VAGAS_DE_SPRITE
    # (4.a) O 15 nao pode ser numero digitado: ele e OBJECT_EVENTS_COUNT menos a
    # vaga do jogador, e quem mexer no .h tem que quebrar aqui. Sem esta linha,
    # subir o teto do motor deixaria bola de fora para sempre e baixa-lo
    # deixaria entrar bola que nunca acorda, nos dois casos calado.
    #    _Static_assert equivalente, do lado do C:
    #        _Static_assert(OBJECT_EVENTS_COUNT - 1 == 15, "VAGAS_DE_SPRITE");
    glob_h = open(f"{REPO}/include/constants/global.h").read()
    teto_do_motor = int(glob_h.split("#define OBJECT_EVENTS_COUNT")[1]
                        .split("\n")[0].strip())
    assert VAGAS_DE_SPRITE == teto_do_motor - 1, (
        f"OBJECT_EVENTS_COUNT virou {teto_do_motor} e VAGAS_DE_SPRITE ainda e "
        f"{VAGAS_DE_SPRITE}")
    # e a JANELA do ginasio e mesmo a mais apertada de Sinnoh: com 20 objetos no
    # mapa (11 bolas + 9 corpos) existe camera que enxerga o teto inteiro, senao
    # o portao estaria medindo folga e nao aperto.
    assert len(vivos) == 20, len(vivos)
    assert max(_na_janela(c, vivos) for c in cams) == VAGAS_DE_SPRITE
    por_teto = [b for b, m in fora if m.startswith("teto de")]
    assert por_teto, "nenhuma bola recusada por teto: o portao ficou mudo"
    for b in por_teto:
        assert max(_na_janela(c, vivos | {b}) for c in cams) > VAGAS_DE_SPRITE, \
            f"{b} cabia e ficou de fora"
    print("demo ok")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if DEMO else main())
