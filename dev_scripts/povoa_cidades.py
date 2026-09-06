#!/usr/bin/env python3
"""Povoa as CIDADES EXTERIORES do cartucho 1 ate o piso de 10 NPCs por cidade.

Lei do Gui (07/09/2026, pergunta 53): "cada cidade deve ter pelo menos uns 10
NPCs". Vale para Kanto, Johto, Hoenn e Sinnoh, que sao o cartucho 1. A regua
desta casa conta NPC como OBJETO QUE E GENTE: fora ficam o Pokemon de cenario
(`OBJ_EVENT_GFX_SPECIES(...)` e os graficos que sao nome de especie), a bola de
item, o pe de berry e o mobiliario que anda (caminhao, barco, pedra). NPC que
so aparece depois de evento CONTA, desde que fique visivel na maior parte do
jogo.

O que esta ferramenta faz, e o que ela NAO faz:

  - escreve `object_events` NOVOS no FIM da lista de `data/maps/<Cidade>/map.json`
    (fim da lista e exigencia de save: a save guarda INDICE de objeto);
  - escreve o roteiro e o texto de cada um no FIM de `data/maps/<Cidade>/scripts.inc`;
  - NAO toca `map.bin`, tileset nem `layouts.json` (a frente de ARTE mexe neles);
  - NAO gasta flag, var, item nem batalha: NPC de povoamento so fala.

POSICAO E DADO CONGELADO, e nao calculo de cada rodada. O `--sugere` propoe uma
posicao lendo o `map.bin` de hoje, e o JSON guarda a resposta; o `--confere`
revalida contra o `map.bin` de AMANHA. Isso importa porque a frente de arte
redesenha cidade: posicao recalculada em silencio a cada rodada faria o NPC
andar sozinho pelo mapa entre duas builds, e ninguem veria.

Regras de posicao, todas conferidas em `--confere`:

  1. celula ANDAVEL (colisao 0) com comportamento de CHAO COMUM (lista branca
     em `CHAO`: lista branca e nao lista negra, porque comportamento novo que
     aparecer amanha entra como suspeito, nao como bom);
  2. ALCANCAVEL a pe a partir das entradas do mapa, com a regra de elevacao do
     motor (`IsElevationMismatchAt`);
  3. nao ilha ninguem: o conjunto alcancavel com os NPCs novos como PAREDE tem
     que ser o mesmo de antes, menos as celulas deles;
  4. longe de porta, placa e gatilho: nem em cima nem na vizinhanca-4 de warp,
     `bg_event` ou `coord_event`, e nunca em cima de objeto que ja existe;
  5. espalhados: distancia de Chebyshev minima de `DISTANCIA` entre NPC novo e
     qualquer outro objeto de gente do mapa;
  6. `movement_range` que nao invade porta: a caixa de alcance inteira passa
     pelas regras 1 e 4;
  7. teto de sprite: nenhuma janela de 20x17 do motor fica com mais de 15
     objetos (`OBJECT_EVENTS_COUNT` menos a vaga do jogador).

Uso:
    python3 dev_scripts/povoa_cidades.py --censo      # quantos NPCs cada cidade tem
    python3 dev_scripts/povoa_cidades.py --sugere     # propoe posicao para o deficit
    python3 dev_scripts/povoa_cidades.py --aplica     # escreve map.json e scripts.inc
    python3 dev_scripts/povoa_cidades.py --confere    # revalida o plano contra a arvore
    python3 dev_scripts/povoa_cidades.py --demo       # auto-teste
"""
import collections
import hashlib
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, f"{RAIZ}/dev_scripts")

PLANO = f"{RAIZ}/dev_scripts/povoa_cidades.json"

# A marca que torna a ferramenta idempotente. Ela vai num campo `origem` dentro
# do proprio `object_event`; `tools/mapjson` le o objeto por CHAVE e ignora
# chave que nao conhece, e `distribui_dex.py` ja usa a mesma tecnica desde
# 21/08/2026.
MARCA = "povoa_cidades"

# Piso do Gui. `GRANDE` sobe o piso em mapa grande, medido em celulas SECAS
# alcancaveis, para a cidade grande nao ficar com a mesma populacao da vila.
PISO = 10
GRANDE = [(1000, 2), (700, 1)]

# Chebyshev minima entre um NPC novo e qualquer outro objeto de gente.
DISTANCIA = 3

# `OBJECT_EVENTS_COUNT` (16) menos a vaga do jogador, e a janela que o motor
# acorda. Os dois numeros sao conferidos contra o `.h` no `--demo`.
TETO_SPRITE = 15
JANELA_SPRITE = (20, 17)

# Comportamento de metatile em que um NPC pode ficar de pe sem ficar estranho
# nem atrapalhar mecanica. LISTA BRANCA de proposito: o enum tem 250 nomes e
# quase todos sao mobilia, porta, escada, gelo, agua ou piso de puzzle.
CHAO = ["MB_NORMAL", "MB_SAND", "MB_DEEP_SAND", "MB_SHORT_GRASS",
        "MB_FOOTPRINTS", "MB_NO_RUNNING", "MB_MOUNTAIN_TOP", "MB_PUDDLE"]

N4 = ((0, -1), (0, 1), (-1, 0), (1, 0))


# ------------------------------------------------------------------ o que e NPC
def _especies(_c=set()):
    if not _c:
        txt = open(f"{RAIZ}/include/constants/species.h", encoding="utf-8").read()
        _c.update(m.group(1) for m in re.finditer(r"^\s*SPECIES_([A-Z0-9_]+)",
                                                  txt, re.M))
    return _c


# Objeto que existe, e visivel, e NAO e gente. Mobiliario que anda entra aqui.
NAO_E_GENTE = {
    "ITEM_BALL", "ITEM_BALL_FRLG", "BERRY_TREE", "BERRY_TREE_EARLY_STAGES",
    "BERRY_TREE_LATE_STAGES", "APRICORN_TREE", "CUTTABLE_TREE",
    "CUTTABLE_TREE_FRLG", "BREAKABLE_ROCK", "BREAKABLE_ROCK_FRLG",
    "PUSHABLE_BOULDER", "PUSHABLE_BOULDER_FRLG", "TRUCK", "MOVING_BOX",
    "SEAGALLOP", "MR_BRINEYS_BOAT", "SS_TIDAL", "SS_ANNE", "SUBMARINE_SHADOW",
    "CABLE_CAR", "TRAIN_FRONT", "SIGN", "GYM_SIGN", "TOWN_MAP", "TRAINER_TIPS",
    "POKEDEX", "CLIPBOARD", "FOSSIL", "FOSSIL_FRLG", "OLD_AMBER", "METEORITE",
    "BIRCHS_BAG", "TRICK_HOUSE_STATUE", "MON_BASE", "LIGHT_SPRITE",
    "DEOXYS_TRIANGLE", "KECLEON_BRIDGE_SHADOW", "POKE_BALL",
}


def eh_gente(gfx):
    """True se o `graphics_id` e um personagem, e nao cenario.

    Pokemon entra de tres jeitos nesta arvore e os tres tem que sair: a macro
    `OBJ_EVENT_GFX_SPECIES(...)`, o grafico velho com nome de especie
    (`OBJ_EVENT_GFX_MACHOP`, `OBJ_EVENT_GFX_SLOWBRO`) e as formas de lendario
    (`GROUDON_SIDE`). O `_especies()` pega os dois primeiros; a terceira sai
    pelo prefixo, porque `SPECIES_GROUDON` casa com o comeco de `GROUDON_SIDE`.
    """
    if gfx.startswith("OBJ_EVENT_GFX_SPECIES"):
        return False
    nome = gfx.replace("OBJ_EVENT_GFX_", "")
    if nome in NAO_E_GENTE:
        return False
    sp = _especies()
    if nome in sp:
        return False
    # GROUDON_SIDE, KYOGRE_ASLEEP, RAYQUAZA_STILL, DEOXYS_A...
    return not any(nome.startswith(e + "_") for e in sp)


def conta_npcs(d):
    return sum(1 for o in (d.get("object_events") or [])
               if eh_gente(o["graphics_id"]))


def nossos(d):
    return [o for o in (d.get("object_events") or []) if o.get("origem") == MARCA]


# ------------------------------------------------------------------- geometria
def _mb(_c={}):
    if not _c:
        import enfeita_cidades as E
        _c["chao"] = E._valores(CHAO)
        _c["E"] = E
    return _c


def geometria(nome):
    """(d, W, H, v, comportamento) do mapa, lidos do disco de agora."""
    E = _mb()["E"]
    import arte_ginasios_sinnoh as G
    d, L, W, H, v = E.grade(nome)
    beh = G.comportamento(L["primary_tileset"], L["secondary_tileset"])
    return d, W, H, v, beh


def _sementes(d, W, H, v, beh=None):
    """Por onde o jogador entra no mapa, para a busca de alcance comecar.

    Warp, o tile ao sul do warp (a chegada de porta) e a BORDA SECA de cada
    lado que tem conexao. A borda importa: o `IndigoPlateau_Exterior_Frlg` tem
    UM warp, ele mora em cima de metatile de porta (colisao 1), e sem a borda o
    mapa inteiro sai por inalcancavel, com 85 celulas livres.

    OBJETO QUE JA EXISTE NAO E SEMENTE, e isso custou uma medicao. Pokemon de
    cenario mora em praia e em penhasco onde o jogador so chega surfando: em
    CianwoodCity, semear a busca nos 22 objetos abria 868 celulas contra as 404
    que se alcancam a pe pelas portas, e cinco NPCs foram parar na praia oeste.
    A lente C2 do `mapas_qa.py` acusou os cinco, e ela estava certa.
    """
    p = [(w["x"], w["y"]) for w in (d.get("warp_events") or [])]
    p += [(w["x"], w["y"] + 1) for w in (d.get("warp_events") or [])]
    for c in (d.get("connections") or []):
        dirr = c["direction"]
        if dirr == "up":
            p += [(x, 0) for x in range(W)]
        elif dirr == "down":
            p += [(x, H - 1) for x in range(W)]
        elif dirr == "left":
            p += [(0, y) for y in range(H)]
        elif dirr == "right":
            p += [(W - 1, y) for y in range(H)]
    ag = _mb()["E"].agua() if beh else set()
    return [(x, y) for x, y in p
            if 0 <= x < W and 0 <= y < H and not ((v[y * W + x] >> 10) & 3)
            and (beh is None or beh(v[y * W + x] & 0x3FF) not in ag)]


def alcance(v, W, H, ini, parede=(), beh=None):
    """Celulas andaveis A PE alcancaveis, com a regra de elevacao do motor.

    Duas elevacoes diferentes e ambas nao-nulas nao se ligam
    (`IsElevationMismatchAt`), senao a busca atravessaria canal e penhasco.
    `parede` e o conjunto de celulas ocupadas por NPC, que sao solidas.

    AGUA E PAREDE aqui, e isso nao e detalhe. A agua do Emerald tem COLISAO 0
    (quem barra e a elevacao, e quem atravessa e o SURF), entao uma busca que
    so olha colisao atravessa o mar. Medido em 06/09/2026 em CianwoodCity: com
    a agua dentro, a busca dava 1.133 celulas contra 405 a pe, e cinco NPCs
    foram parar na praia oeste, que so se alcanca surfando. A lente C2 do
    `mapas_qa.py` acusou os cinco, e ela estava certa.
    """
    parede = set(parede)
    ag = _mb()["E"].agua() if beh else set()

    def seco(x, y):
        return beh is None or beh(v[y * W + x] & 0x3FF) not in ag

    vis = set(p for p in ini if p not in parede and seco(*p))
    fila = collections.deque(vis)
    while fila:
        x, y = fila.popleft()
        ea = (v[y * W + x] >> 12) & 0xF
        for dx, dy in N4:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H) or (nx, ny) in vis:
                continue
            if (nx, ny) in parede:
                continue
            j = ny * W + nx
            if (v[j] >> 10) & 3:
                continue
            eb = (v[j] >> 12) & 0xF
            if ea and eb and ea != eb:
                continue
            if not seco(nx, ny):
                continue
            vis.add((nx, ny))
            fila.append((nx, ny))
    return vis


def proibidas(d, W=0, H=0):
    """Celulas em que NPC nenhum pode ficar: porta, placa, gatilho e vizinhanca.

    O ANEL DE BORDA tambem sai. Celula da borda de um mapa com conexao aparece
    dentro do mapa VIZINHO enquanto o jogador anda na rota, e NPC de cidade
    aparecendo no meio da rota le como defeito.
    """
    fora = set()
    for x in range(W):
        fora.add((x, 0))
        fora.add((x, H - 1))
    for y in range(H):
        fora.add((0, y))
        fora.add((W - 1, y))
    for o in (d.get("object_events") or []):
        # O objeto que ESTA ferramenta plantou nao e obstaculo para ela mesma,
        # senao a segunda conferida recusa o proprio trabalho da primeira.
        if o.get("origem") == MARCA:
            continue
        fora.add((o["x"], o["y"]))
    for grupo in ("warp_events", "bg_events", "coord_events"):
        for e in (d.get(grupo) or []):
            fora.add((e["x"], e["y"]))
            for dx, dy in N4:
                fora.add((e["x"] + dx, e["y"] + dy))
    return fora


def candidatas(nome):
    """(livres, d, W, H, v) - as celulas em que um NPC novo poderia ficar."""
    d, W, H, v, beh = geometria(nome)
    chao = _mb()["chao"]
    alc = alcance(v, W, H, _sementes(d, W, H, v, beh), beh=beh)
    proib = proibidas(d, W, H)
    livres = sorted(p for p in alc
                    if p not in proib and beh(v[p[1] * W + p[0]] & 0x3FF) in chao)
    return livres, d, W, H, v


def secas(nome):
    """Quantas celulas SECAS o mapa tem alcancaveis. E a regua de porte."""
    d, W, H, v, beh = geometria(nome)
    alc = alcance(v, W, H, _sementes(d, W, H, v, beh), beh=beh)
    return len(alc)


def piso_de(area):
    for corte, extra in GRANDE:
        if area >= corte:
            return PISO + extra
    return PISO


def lotacao(pontos):
    """Quantos objetos caem, no PIOR caso, dentro de UMA janela de sprite.

    Pessimista de proposito (nao exige que exista tile andavel na ancora):
    errar para o lado de sobrar sprite custa reposicionamento, errar para o
    outro custa NPC invisivel que nenhum teste de compilacao acha.
    """
    if not pontos:
        return 0
    W, H = JANELA_SPRITE
    return max(sum(1 for x, y in pontos if xl <= x < xl + W and yt <= y < yt + H)
               for xl in {p[0] for p in pontos} for yt in {p[1] for p in pontos})


# ------------------------------------------------------------------- o plano
def plano():
    return json.load(open(PLANO, encoding="utf-8"))


def cidades_do_cartucho1():
    """[(regiao, mapa)] de toda cidade e vila exterior de Kanto a Sinnoh."""
    import regua_cidades as R
    dentro, _ = R.cidades()
    return [(r, n) for r, n in dentro if n not in FORA_DA_LEI]


# Cidade que a lei do Gui NAO alcanca, com o motivo medido de cada uma.
FORA_DA_LEI = {
    # Battle Zone: a ilha inteira saiu do porte por decisao do Gui em
    # 21/08/2026 (`completude.CORTES_DO_GUI`). Os tres mapas sao cotocos de
    # 1x1 celula, sem chao para NPC nenhum.
    "FightArea": "cortada pelo Gui: Battle Zone, e o mapa e 1x1",
    "SurvivalArea": "cortada pelo Gui: Battle Zone, e o mapa e 1x1",
    "ResortArea": "cortada pelo Gui: Battle Zone, e o mapa e 1x1",
}


# ------------------------------------------------------------------- validacao
def valida(nome, npcs, estrito=True):
    """[] se o plano desta cidade fecha; lista de queixas se nao."""
    livres, d, W, H, v = candidatas(nome)
    livres = set(livres)
    queixas = []
    novos = [(n["x"], n["y"]) for n in npcs]
    if len(set(novos)) != len(novos):
        queixas.append("duas posicoes iguais")
    gente = [(o["x"], o["y"]) for o in (d.get("object_events") or [])
             if eh_gente(o["graphics_id"]) and o.get("origem") != MARCA]
    for n in npcs:
        p = (n["x"], n["y"])
        if p not in livres:
            queixas.append("%s em %s nao e chao livre" % (n["rotulo"], p))
            continue
        for dx in range(-n.get("rx", 0), n.get("rx", 0) + 1):
            for dy in range(-n.get("ry", 0), n.get("ry", 0) + 1):
                q = (p[0] + dx, p[1] + dy)
                if q not in livres and q != p:
                    queixas.append("%s: alcance invade %s" % (n["rotulo"], q))
        if estrito:
            perto = [g for g in gente + [o for o in novos if o != p]
                     if max(abs(g[0] - p[0]), abs(g[1] - p[1])) < 2]
            if perto:
                queixas.append("%s em %s colado em %s" % (n["rotulo"], p, perto[0]))
    # Ilhamento: com os novos como parede, o alcance nao pode encolher.
    beh = geometria(nome)[4]
    sem = _sementes(d, W, H, v, beh)
    antes = alcance(v, W, H, sem, beh=beh)
    depois = alcance(v, W, H, [p for p in sem if p not in set(novos)],
                     parede=novos, beh=beh)
    perdidas = antes - depois - set(novos)
    if perdidas:
        queixas.append("ilha %d celulas, ex.: %s" % (len(perdidas),
                                                     sorted(perdidas)[:3]))
    # Teto de sprite.
    todos = [(o["x"], o["y"]) for o in (d.get("object_events") or [])
             if o.get("origem") != MARCA
             and o["graphics_id"] != "OBJ_EVENT_GFX_LIGHT_SPRITE"] + novos
    lot = lotacao(todos)
    if lot > TETO_SPRITE:
        queixas.append("janela de sprite com %d objetos (teto %d)" % (lot, TETO_SPRITE))
    return queixas


# ------------------------------------------------------------------- sugestao
def abertura(p, livres):
    """Quantas celulas livres cabem na caixa 7x7 em volta. E "praca", nao "beco".

    Existe porque a primeira versao escolhia a celula MAIS LONGE de tudo, e o
    mais longe de tudo e sempre o CANTO do mapa: Vermilion recebia gente em
    (1,1) e (46,38), atras das arvores da borda. Abertura poe o NPC onde ha
    chao em volta, que e onde gente fica.
    """
    return sum(1 for dx in range(-3, 4) for dy in range(-3, 4)
               if (p[0] + dx, p[1] + dy) in livres)


def folga(p, livres):
    """O maior raio r em que a caixa (2r+1) em volta de `p` esta toda livre.

    E o teto de `movement_range`: NPC que anda so anda dentro dela, entao a
    caixa e conferida uma vez aqui e nunca invade porta nem parede.
    """
    for r in (2, 1):
        if all((p[0] + dx, p[1] + dy) in livres
               for dx in range(-r, r + 1) for dy in range(-r, r + 1)):
            return r
    return 0


def _sorteio(nome, p):
    """Desempate estavel e espalhado, para NPC nao sair em fila reta.

    Com desempate por (y, x), Cianwood recebeu os cinco na MESMA coluna x=3 e
    Floaroma os tres na MESMA linha y=5: a abertura e igual em ruas retas, e o
    (y, x) sempre escolhe a ponta de cima. O hash e deterministico (mesma
    entrada, mesma saida, em qualquer maquina), que e o que a idempotencia pede.
    """
    return hashlib.md5(("%s:%d:%d" % (nome, p[0], p[1])).encode()).digest()


def sugere(nome, quantos, ja=()):
    """`quantos` posicoes deterministicas para NPC novo, da melhor para a pior.

    Guloso por ABERTURA mais ESPALHAMENTO: `abertura` puxa para a praca e
    `2 * min(6, distancia)` empurra para longe de quem ja esta la. Desempate
    por (y, x), para a resposta nao depender da ordem do conjunto.

    A distancia minima cede de 3 para 2 quando a cidade nao tem chao para 3:
    Pacifidlog e uma passarela de troncos e o Indigo Plateau e uma trilha, e
    nas duas o piso de 10 do Gui e mais importante que a folga de conforto.

    Cada candidato passa pela prova de ILHAMENTO antes de ser aceito, e a fila
    fica ORDENADA para o segundo colocado entrar quando o primeiro fecha
    caminho. Sem isso, Pacifidlog perdia 9 celulas atras de um NPC plantado no
    meio de um tronco de uma celula de largura, Fallarbor 4, SixIsland 2 e
    FiveIsland 1: NPC e solido, e beco de largura 1 e comum em vila.
    """
    livres, d, W, H, v = candidatas(nome)
    Lset = set(livres)
    ocupadas = [(o["x"], o["y"]) for o in (d.get("object_events") or [])
                if eh_gente(o["graphics_id"]) and o.get("origem") != MARCA] + list(ja)
    ab = {p: abertura(p, Lset) for p in livres}
    beh = geometria(nome)[4]
    sem = _sementes(d, W, H, v, beh)
    base = alcance(v, W, H, sem, beh=beh)
    for dmin in (DISTANCIA, 2):
        escolhidas = []
        for _ in range(quantos):
            fila = []
            for p in livres:
                dist = min([max(abs(p[0] - q[0]), abs(p[1] - q[1]))
                            for q in ocupadas + escolhidas] or [99])
                if dist < dmin:
                    continue
                fila.append(((-(ab[p] + 2 * min(6, dist)), _sorteio(nome, p),
                              p[1], p[0]), p))
            fila.sort()
            melhor = None
            for _chave, p in fila:
                parede = set(escolhidas + [p])
                depois = alcance(v, W, H, [q for q in sem if q not in parede],
                                 parede=parede, beh=beh)
                if not (base - depois - parede):
                    melhor = p
                    break
            if melhor is None:
                break
            escolhidas.append(melhor)
        if len(escolhidas) == quantos:
            return escolhidas, dmin
    return escolhidas, dmin


# ------------------------------------------------------------------- aplicacao
def objeto(n):
    return {
        "graphics_id": n["gfx"],
        "x": n["x"],
        "y": n["y"],
        "elevation": n.get("elevation", 3),
        "movement_type": "MOVEMENT_TYPE_" + n["mov"],
        "movement_range_x": n.get("rx", 0),
        "movement_range_y": n.get("ry", 0),
        "trainer_type": "TRAINER_TYPE_NONE",
        "trainer_sight_or_berry_tree_id": "0",
        "script": "%s_EventScript_%s" % (n["_prefixo"], n["rotulo"]),
        "flag": "0",
        "origem": MARCA,
    }


CABECALHO = ("\n@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>\n"
             "@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.\n"
             "@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json\n"
             "@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.\n")
FIM = "@ <<< Povoamento: fim do bloco gerado <<<\n"


def texto_asm(prefixo, npcs):
    linhas = [CABECALHO]
    for n in npcs:
        rot = n["rotulo"]
        linhas.append("%s_EventScript_%s::\n\tlock\n\tfaceplayer\n"
                      "\tmsgbox %s_Text_%s, MSGBOX_DEFAULT\n\trelease\n\tend\n"
                      % (prefixo, rot, prefixo, rot))
        corpo = "\\p".join(n["falas"])
        linhas.append('%s_Text_%s:\n\t.string "%s$"\n' % (prefixo, rot, corpo))
    linhas.append(FIM)
    return "\n".join(linhas)


def _sem_bloco(txt):
    i = txt.find(CABECALHO.lstrip("\n"))
    if i < 0:
        return txt
    j = txt.find(FIM, i)
    assert j > 0, "bloco de povoamento aberto e sem fim"
    return txt[:i].rstrip("\n") + "\n" + txt[j + len(FIM):]


def aplica(so=None, escreve=True):
    p = plano()
    mudados, total = [], 0
    for nome, c in sorted(p["cidades"].items()):
        if so and nome != so:
            continue
        npcs = c["npcs"]
        for n in npcs:
            n["_prefixo"] = c.get("prefixo", nome)
        total += len(npcs)
        # ---- map.json
        pj = f"{RAIZ}/data/maps/{nome}/map.json"
        d = json.load(open(pj, encoding="utf-8"))
        base = [o for o in (d.get("object_events") or []) if o.get("origem") != MARCA]
        d["object_events"] = base + [objeto(n) for n in npcs]
        novo = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
        velho = open(pj, encoding="utf-8").read()
        if novo != velho:
            mudados.append(pj)
            if escreve:
                _grava(pj, novo)
        # ---- scripts.inc
        pi = f"{RAIZ}/data/maps/{nome}/scripts.inc"
        atual = open(pi, encoding="utf-8").read()
        limpo = _sem_bloco(atual)
        alvo = limpo.rstrip("\n") + "\n" + texto_asm(c.get("prefixo", nome), npcs)
        if alvo != atual:
            mudados.append(pi)
            if escreve:
                _grava(pi, alvo)
    return mudados, total


def _grava(caminho, texto):
    """Temporario e rename. `open(w)` antes de validar ja truncou o ESTADO uma vez."""
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(texto)
    os.replace(tmp, caminho)


# ------------------------------------------------------------------- relatorio
def censo():
    fora = []
    for regiao, nome in cidades_do_cartucho1():
        d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json", encoding="utf-8"))
        n = conta_npcs(d)
        meus = len(nossos(d))
        fora.append((regiao, nome, n, meus))
    return sorted(fora, key=lambda t: (t[2], t[0], t[1]))


def main(argv):
    if "--demo" in argv:
        return demo()
    if "--censo" in argv:
        print("%-7s %-30s %5s %5s %6s %5s" % ("regiao", "cidade", "npcs", "meus",
                                              "secas", "piso"))
        falta = 0
        for regiao, nome, n, meus in censo():
            a = secas(nome)
            piso = piso_de(a)
            marca = "" if n >= piso else "  <- falta %d" % (piso - n)
            falta += max(0, piso - n)
            print("%-7s %-30s %5d %5d %6d %5d%s" % (regiao, nome, n, meus, a, piso, marca))
        print("faltam %d NPCs no total" % falta)
        return 0
    if "--sugere" in argv:
        return _sugere_cli(argv)
    if "--confere" in argv:
        ruim = 0
        for nome, c in sorted(plano()["cidades"].items()):
            q = valida(nome, c["npcs"])
            d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json", encoding="utf-8"))
            n = conta_npcs(d)
            piso = piso_de(secas(nome))
            if n < piso:
                q.append("so %d NPCs, piso %d" % (n, piso))
            if q:
                ruim += 1
                print("%-28s %s" % (nome, "; ".join(q)))
        print("cidades com queixa: %d de %d" % (ruim, len(plano()["cidades"])))
        return 1 if ruim else 0
    mudados, total = aplica(escreve="--aplica" in argv)
    print("%d arquivos %s, %d NPCs no plano"
          % (len(mudados), "escritos" if "--aplica" in argv else "mudariam", total))
    for m in mudados:
        print("  ", m.replace(RAIZ + "/", ""))
    return 0


def _sugere_cli(argv):
    alvo = [a for a in argv if not a.startswith("--")]
    p = plano() if os.path.exists(PLANO) else {"cidades": {}}
    fora = {}
    for regiao, nome in cidades_do_cartucho1():
        if alvo and nome not in alvo:
            continue
        d = json.load(open(f"{RAIZ}/data/maps/{nome}/map.json", encoding="utf-8"))
        base = conta_npcs(d) - len(nossos(d))
        piso = piso_de(secas(nome))
        falta = piso - base
        if falta <= 0:
            continue
        pos, dmin = sugere(nome, falta)
        livres = set(candidatas(nome)[0])
        fora[nome] = {"regiao": regiao, "antes": base, "alvo": piso, "dmin": dmin,
                      "posicoes": [[p[0], p[1], folga(p, livres)] for p in pos]}
        print("%-28s antes=%d alvo=%d achou=%d dmin=%d %s"
              % (nome, base, piso, len(pos), dmin,
                 [(p[0], p[1], folga(p, livres)) for p in pos]))
    print(json.dumps(fora, indent=2))
    return 0


# ---------------------------------------------------------------------- demo
def demo():
    ok = 0

    def checa(cond, msg):
        nonlocal ok
        assert cond, msg
        ok += 1
        print("ok  ", msg)

    g = open(f"{RAIZ}/include/constants/global.h", encoding="utf-8").read()
    n = int(re.search(r"#define OBJECT_EVENTS_COUNT\s+(\d+)", g).group(1))
    checa(TETO_SPRITE == n - 1,
          "TETO_SPRITE %d = OBJECT_EVENTS_COUNT %d menos o jogador" % (TETO_SPRITE, n))
    checa(not eh_gente("OBJ_EVENT_GFX_SPECIES(PINECO)"), "Pokemon de cenario nao e NPC")
    checa(not eh_gente("OBJ_EVENT_GFX_MACHOP"), "grafico com nome de especie nao e NPC")
    checa(not eh_gente("OBJ_EVENT_GFX_GROUDON_SIDE"), "forma de lendario nao e NPC")
    checa(not eh_gente("OBJ_EVENT_GFX_ITEM_BALL"), "bola de item nao e NPC")
    checa(not eh_gente("OBJ_EVENT_GFX_BERRY_TREE"), "pe de berry nao e NPC")
    checa(not eh_gente("OBJ_EVENT_GFX_TRUCK"), "caminhao nao e NPC")
    checa(eh_gente("OBJ_EVENT_GFX_FISHERMAN"), "pescador e NPC")
    checa(eh_gente("OBJ_EVENT_GFX_SINNOH_JASMINE"), "chefe e NPC")
    checa(lotacao([(0, 0), (19, 16), (20, 16)]) == 2, "janela de sprite e 20x17")
    checa(piso_de(50) == 10 and piso_de(800) == 11 and piso_de(1200) == 12,
          "o piso sobe com a area seca")
    # Idempotencia: aplicar duas vezes nao muda nada na segunda.
    if os.path.exists(PLANO):
        a1, tot = aplica(escreve=True)
        a2, _ = aplica(escreve=True)
        checa(not a2, "2a passada muda 0 arquivos (1a mudou %d, %d NPCs)" % (len(a1), tot))
        ruim = [n for n, c in plano()["cidades"].items() if valida(n, c["npcs"])]
        checa(not ruim, "todo NPC do plano passa nas 7 regras de posicao")
        p = plano()
        rot = [(n, x["rotulo"]) for n, c in p["cidades"].items() for x in c["npcs"]]
        checa(len(rot) == len(set(rot)), "rotulo unico por cidade")
        falas = [f for c in p["cidades"].values() for x in c["npcs"] for f in x["falas"]]
        checa(all(len(l) <= 34 for f in falas for l in f.split("\\n")),
              "nenhuma linha de fala passa de 34 caracteres")
        letras = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
                     "0123456789 .,!?':;-()é")
        estranhas = {c for f in falas for c in f.replace("\\n", "")} - letras
        checa(not estranhas,
              "fala so usa caractere que o charmap tem (%d falas)" % len(falas))
    print("\n%d provas, todas verdes" % ok)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
