#!/usr/bin/env python3
"""Traz de volta do túmulo os mapas de Sinnoh que o Gui reabriu na decisão 48.

    python3 dev_scripts/ressuscita_mapas_sinnoh.py             # tabela, não escreve
    python3 dev_scripts/ressuscita_mapas_sinnoh.py --dry-run   # idem, explícito
    python3 dev_scripts/ressuscita_mapas_sinnoh.py --demo      # autoteste
    python3 dev_scripts/ressuscita_mapas_sinnoh.py --aplicar   # escreve

Este arquivo é o INVERSO exato de `remove_mapas_cortados.py`, e só dele
--------------------------------------------------------------------
Em 22/08/2026 o commit `721c77fb63` transformou 111 mapas em TÚMULO: o cabeçalho
ficou na tabela (para nenhum índice de save andar), e o conteúdo saiu. Em
07/09/2026 o Gui decidiu (decisão 48) que PARTE daquele corte volta para o
cartucho 1. Os 32 mapas de `MAPAS_QUE_VOLTAM` são essa parte.

O conteúdo original está VIVO no git, em `721c77fb63^`, e é de lá que ele volta.
Reimportar da fonte seria mais caro e menos fiel: o que saiu não foi a fonte, foi
a nossa versão dela, já convertida, já traduzida de metatile e já ligada por
warp aos vizinhos. Ressuscitar do git devolve exatamente o que existia; qualquer
melhoria em cima disso é obra separada, feita pelos geradores de Sinnoh.

Os DOIS índices de save, e por que nenhum anda aqui
---------------------------------------------------
1. `SaveBlock1.location.mapGroup`/`mapNum` é a POSIÇÃO do mapa dentro do grupo em
   `data/maps/map_groups.json`. O corte NÃO tirou nenhum mapa da tabela, então
   ressuscitar no lugar não move nada, e este script não escreve uma linha
   sequer em `map_groups.json`. Conferido no passo 6.
2. `SaveBlock1.mapLayoutId` é o ORDINAL do layout dentro de
   `data/layouts/layouts.json`, contando só quem tem `border_filepath`
   (`tools/mapjson/mapjson.cpp:895`). O corte ENCOLHEU os layouts exclusivos
   para 1x1 em vez de apagá-los, justamente para o ordinal não andar. Aqui eles
   voltam ao tamanho de antes NO MESMO LUGAR: `layouts.json` só muda `width` e
   `height`, nunca a ordem nem o número de entradas. Conferido no passo 6.

Layout compartilhado com túmulo que FICA túmulo
-----------------------------------------------
`LAYOUT_ROUTE226_ACCESS` (o molde de portão 13x9) veste quatro mapas que voltam
(AmitySquare, PalPark, GreatMarsh6, SpringPath) e três que continuam cortados
(Route226_Access, StarkMountainOutside, TrophyGarden). Layout é um só: devolver
a geometria devolve para os sete. Os três cortados continuam sem evento nenhum e
com `MAPSEC_NONE`, ou seja continuam túmulo pela régua (`completude.tumulos()`
filtra por `cortado_por`, não por tamanho de layout). O que eles ganham é peso de
ROM, e é o preço, medido, de os quatro que voltam terem chão.

A porta que reabre, e a que continua fechada
--------------------------------------------
O corte trocou o warp que ia para túmulo por LÁPIDE (a entrada fica no mesmo
índice, repetindo as coordenadas do warp doador) ou, quando a porta era de duas
células, por ADOÇÃO da gêmea viva. Os dois casos guardam marca no `map.json`
(`fechado`/`porta_original` e `gemea`), e por isso a reabertura não precisa
adivinhar: o warp volta LITERAL do `721c77fb63^`, no mesmo índice.

A PLACA "Closed for renovations." é uma por MAPA, não uma por porta, e o mapa
pode ter mais de uma porta fechada (a `PokemonLeagueNorthPokecenter1F` tem duas:
o elevador da Liga, que volta, e o 2F de Wi-Fi, que não volta). Por isso a placa
só sai quando NÃO SOBRA nenhuma porta fechada naquele mapa. Conferido no passo 5.

Idempotente: rodar duas vezes não muda nada. Mapa já vivo é pulado, layout já do
tamanho certo é pulado, warp já reaberto não tem marca para casar, placa já
removida não é achada duas vezes.
"""
import json
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = f"{RAIZ}/data/maps"
CORTE = "721c77fb63"          # o commit que virou túmulo
ANTES = f"{CORTE}^"           # a árvore de onde o conteúdo volta
MARCA_PLACA = "@ >>> porta fechada (remove_mapas_cortados.py) >>>"
FIM_PLACA = "@ <<< porta fechada <<<"

# Decisão 48 do Gui, 07/09/2026: estes voltam para o cartucho 1.
#
# Quem NÃO está aqui continua túmulo, e cada ausência é a mesma decisão: a
# Battle Zone inteira, o Pokétch, o GTS, os 2F de Wi-Fi, a Union Room, o
# Underground, o Mystery Gift, a PokemonMansion e o TrophyGarden.
MAPAS_QUE_VOLTAM = [
    # Great Marsh: só a sexta área, que é a única que chegou a existir aqui.
    "GreatMarsh6",
    # Amity Square e os dois portões de Hearthome que levam a ela.
    "AmitySquare",
    "HearthomeCityWestGateToAmitySquare",
    "HearthomeCityEastGateToAmitySquare",
    # Pal Park e o saguão dele, na Route 221.
    "PalPark", "PalParkLobby",
    # Turnback Cave inteira (o sorteio mora em data/scripts/turnback_cave.inc),
    # mais a Sendoff Spring e o Spring Path, que são o caminho até ela.
    "TurnbackCaveEntrance", "TurnbackCavePillarRoom", "TurnbackCaveGiratinaRoom",
] + [f"TurnbackCavePillar{p}Room{s}" for p in (1, 2, 3) for s in range(1, 7)] + [
    "SendoffSpring", "SpringPath",
    # Game Corner de Veilstone.
    "GameCorner",
    # Palco do Contest sem concurso rolando.
    "ContestHallStageNoContest",
    # O elevador da Liga que sai do Pokécenter norte.
    "PokemonLeagueElevatorToAaronRoom",
]

# Tabelas de mato que saíram com o corte e voltam com o mapa. Só uma: os outros
# 31 mapas nunca tiveram mato (são interior, portão ou caverna de sorteio).
MATO_QUE_VOLTA = ["MAP_SENDOFF_SPRING"]

# O `.include` que `tira_turnback_inc()` apagou, e a linha ANTES da qual ele
# volta (a ordem de include não muda endereço de nada, mas manter o arquivo
# igual ao de antes do corte deixa o diff legível).
INC_TURNBACK = '\t.include "data/scripts/turnback_cave.inc"\n'
INC_DEPOIS_DE = '\t.include "data/maps/TurnbackCaveGiratinaRoom/scripts.inc"\n'

APLICAR = "--aplicar" in sys.argv


# --------------------------------------------------------------------- leitura
def git_texto(caminho, rev=ANTES):
    r = subprocess.run(["git", "-C", RAIZ, "show", f"{rev}:{caminho}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def git_bytes(caminho, rev=ANTES):
    r = subprocess.run(["git", "-C", RAIZ, "show", f"{rev}:{caminho}"],
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None


def le_json(p):
    return json.load(open(p, encoding="utf-8"))


def grava_json(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def grupos():
    return le_json(f"{MAPS}/map_groups.json")


def todos_os_mapas(g=None):
    g = g or grupos()
    return [m for grp in g["group_order"] for m in g[grp]]


def constantes():
    """nome de pasta -> MAP_*, pelo par (grupo, índice), nunca por regex."""
    g = grupos()
    pos = {(gi, i): m for gi, grp in enumerate(g["group_order"])
           for i, m in enumerate(g[grp])}
    h = open(f"{RAIZ}/include/constants/map_groups.h", encoding="utf-8").read()
    saida = {}
    for const, num, gi in re.findall(
            r"(MAP_[A-Z0-9_]+)\s*=\s*\((\d+) \| \((\d+) << 8\)\)", h):
        k = (int(gi), int(num))
        if k in pos:
            saida[pos[k]] = const
    return saida


# ------------------------------------------------------- 1. o mapa em si volta
def revive_mapa(m, aplicar=False):
    """map.json e scripts.inc voltam LITERAIS de `721c77fb63^`. True se mudou."""
    mudou = []
    velho = git_texto(f"data/maps/{m}/map.json")
    if velho is None:
        raise SystemExit(f"{m}: {ANTES} não tem data/maps/{m}/map.json")
    d = json.loads(velho)
    if "cortado_por" in d:
        raise SystemExit(f"{m}: a versão de {ANTES} JÁ é túmulo; nada a reviver")
    p = f"{MAPS}/{m}/map.json"
    atual = le_json(p)
    if atual != d:
        mudou.append("map.json")
        if aplicar:
            grava_json(p, d)
    vs = git_texto(f"data/maps/{m}/scripts.inc")
    ps = f"{MAPS}/{m}/scripts.inc"
    if vs is not None:
        agora = open(ps, encoding="utf-8", errors="replace").read() \
            if os.path.exists(ps) else ""
        if agora != vs:
            mudou.append("scripts.inc")
            if aplicar:
                open(ps, "w", encoding="utf-8").write(vs)
    return mudou


# ---------------------------------------------------- 2. o layout volta a medir
def layouts_a_desencolher():
    """[(id, w, h)] dos layouts que os mapas que voltam vestem e que estão 1x1.

    O critério não é nome: é `width`/`height` de 1x1 AGORA contra o tamanho em
    `721c77fb63^`. Layout que o corte não tocou (porque era compartilhado com
    mapa vivo) não aparece aqui, e é o caso do molde de Oreburgh e do
    `LAYOUT_ROUTE208_ACCESS`.
    """
    quero = set()
    for m in MAPAS_QUE_VOLTAM:
        v = git_texto(f"data/maps/{m}/map.json")
        quero.add(json.loads(v)["layout"])
    L = le_json(f"{RAIZ}/data/layouts/layouts.json")
    O = json.loads(git_texto("data/layouts/layouts.json"))
    velho = {x["id"]: x for x in O["layouts"]}
    saida = []
    for x in L["layouts"]:
        if x["id"] not in quero or x["id"] not in velho:
            continue
        o = velho[x["id"]]
        if (x["width"], x["height"]) != (o["width"], o["height"]):
            saida.append((x["id"], o["width"], o["height"]))
    return saida


def desencolhe_layouts(lista, aplicar=False):
    """Devolve tamanho e blockdata NO LUGAR: a ordem de layouts.json não muda."""
    L = le_json(f"{RAIZ}/data/layouts/layouts.json")
    ordem_antes = [x["id"] for x in L["layouts"]]
    quero = {i: (w, h) for i, w, h in lista}
    bytes_de_volta = 0
    for x in L["layouts"]:
        if x["id"] not in quero:
            continue
        x["width"], x["height"] = quero[x["id"]]
        for campo in ("blockdata_filepath", "border_filepath"):
            rel = x[campo]
            dados = git_bytes(rel)
            if dados is None:
                raise SystemExit(f"{x['id']}: {ANTES} não tem {rel}")
            alvo = f"{RAIZ}/{rel}"
            atual = open(alvo, "rb").read() if os.path.exists(alvo) else b""
            bytes_de_volta += len(dados) - len(atual)
            if aplicar:
                os.makedirs(os.path.dirname(alvo), exist_ok=True)
                open(alvo, "wb").write(dados)
    if aplicar and lista:
        assert [x["id"] for x in L["layouts"]] == ordem_antes, \
            "a ordem de layouts.json andou: o mapLayoutId da save quebraria"
        grava_json(f"{RAIZ}/data/layouts/layouts.json", L)
    return bytes_de_volta


# ------------------------------------------------- 3. o sorteio da Turnback volta
def volta_turnback_inc(aplicar=False):
    inc = f"{RAIZ}/data/scripts/turnback_cave.inc"
    ev = f"{RAIZ}/data/event_scripts.s"
    feito = []
    corpo = git_texto("data/scripts/turnback_cave.inc")
    if corpo is None:
        raise SystemExit(f"{ANTES} não tem data/scripts/turnback_cave.inc")
    agora = open(inc, encoding="utf-8").read() if os.path.exists(inc) else None
    if agora != corpo:
        feito.append("data/scripts/turnback_cave.inc")
        if aplicar:
            open(inc, "w", encoding="utf-8").write(corpo)
    t = open(ev, encoding="utf-8").read()
    if INC_TURNBACK not in t:
        feito.append("include em data/event_scripts.s")
        if aplicar:
            if INC_DEPOIS_DE not in t:
                raise SystemExit("não achei onde reinserir o include da Turnback")
            open(ev, "w", encoding="utf-8").write(
                t.replace(INC_DEPOIS_DE, INC_DEPOIS_DE + INC_TURNBACK, 1))
    return feito


# ------------------------------------------------------- 4. a tabela de mato volta
def volta_mato(aplicar=False):
    """Reinsere POR CHAVE, na posição de antes, sem reescrever o resto."""
    p = f"{RAIZ}/src/data/wild_encounters.json"
    W = le_json(p)
    O = json.loads(git_texto("src/data/wild_encounters.json"))
    tenho = {e.get("map") for g in W["wild_encounter_groups"]
             for e in (g.get("encounters") or [])}
    posto = []
    for gi, grupo in enumerate(O["wild_encounter_groups"]):
        for i, e in enumerate(grupo.get("encounters") or []):
            if e.get("map") not in MATO_QUE_VOLTA or e["map"] in tenho:
                continue
            # A posição de antes é achada pelo VIZINHO ANTERIOR que ainda
            # existe, e não pelo índice cru: 98 entradas saíram do arquivo
            # entre 22/08 e hoje, e o índice cru cairia em outro lugar.
            alvo = W["wild_encounter_groups"][gi].setdefault("encounters", [])
            antes = [x["map"] for x in (grupo["encounters"] or [])[:i]]
            onde = len(alvo)
            for nome in reversed(antes):
                pos = [j for j, y in enumerate(alvo) if y.get("map") == nome]
                if pos:
                    onde = pos[0] + 1
                    break
            posto.append((e["map"], gi, onde))
            if aplicar:
                alvo.insert(onde, e)
    if posto and aplicar:
        grava_json(p, W)
    return posto


# ------------------------------------------------------------ 5. a porta reabre
MARCAS_DE_FECHADO = ("fechado", "porta_original", "gemea")


def porta_fechada(w):
    return any(k in w for k in MARCAS_DE_FECHADO)


def portas_a_reabrir(const=None):
    """[(mapa vivo, [(índice, warp de antes)])] das portas que voltam a abrir."""
    const = const or constantes()
    volta = {const[m] for m in MAPAS_QUE_VOLTAM if m in const}
    saida = []
    for m in todos_os_mapas():
        p = f"{MAPS}/{m}/map.json"
        if not os.path.exists(p):
            continue
        d = le_json(p)
        if "cortado_por" in d:
            continue
        ws = d.get("warp_events") or []
        if not any(porta_fechada(w) for w in ws):
            continue
        velho = git_texto(f"data/maps/{m}/map.json")
        if velho is None:
            continue
        wo = json.loads(velho).get("warp_events") or []
        abre = [(i, wo[i]) for i, w in enumerate(ws)
                if porta_fechada(w) and i < len(wo)
                and wo[i].get("dest_map") in volta]
        if abre:
            saida.append((m, abre))
    return saida


def reabre(aplicar=False):
    """Devolve [(mapa, [índices], placa saiu?)]."""
    feito = []
    for m, abre in portas_a_reabrir():
        p = f"{MAPS}/{m}/map.json"
        d = le_json(p)
        for i, w in abre:
            d["warp_events"][i] = w
        # A PLACA É UMA POR MAPA: ela só sai se não sobrou porta fechada.
        sobrou = [i for i, w in enumerate(d["warp_events"]) if porta_fechada(w)]
        tirou = False
        if not sobrou:
            script = f"{m}_EventScript_PortaFechada"
            antes = d.get("bg_events") or []
            depois = [b for b in antes if b.get("script") != script]
            if len(depois) != len(antes):
                d["bg_events"] = depois
                tirou = True
        if aplicar:
            grava_json(p, d)
            if tirou:
                tira_bloco_da_placa(m)
        feito.append((m, [i for i, _ in abre], tirou, sobrou))
    return feito


def tira_bloco_da_placa(m):
    """Some com o bloco delimitado que `_append_script_placa` escreveu."""
    ps = f"{MAPS}/{m}/scripts.inc"
    if not os.path.exists(ps):
        return
    t = open(ps, encoding="utf-8", errors="replace").read()
    a = t.find(MARCA_PLACA)
    b = t.find(FIM_PLACA, a)
    if a < 0 or b < 0:
        return
    open(ps, "w", encoding="utf-8").write(
        (t[:a].rstrip("\n") + "\n" + t[b + len(FIM_PLACA):].lstrip("\n")))


# ------------------------------------------------ 6. nenhum índice de save andou
def confere_indices():
    """Erros. Lista vazia = nem mapNum nem mapLayoutId se moveram."""
    ruim = []
    g_agora = grupos()
    g_head = json.loads(git_texto("data/maps/map_groups.json", "HEAD"))
    if g_agora != g_head:
        ruim.append("map_groups.json mudou: o mapNum da save anda")
    L = [x["id"] for x in le_json(f"{RAIZ}/data/layouts/layouts.json")["layouts"]]
    H = [x["id"] for x in json.loads(
        git_texto("data/layouts/layouts.json", "HEAD"))["layouts"]]
    if L != H:
        ruim.append("a ORDEM de layouts.json mudou: o mapLayoutId da save anda")
    return ruim


# --------------------------------------------------------------------- relatório
def relatorio(aplicar=False):
    const = constantes()
    faltam = [m for m in MAPAS_QUE_VOLTAM if m not in const]
    if faltam:
        raise SystemExit(f"mapas sem constante em map_groups.h: {faltam}")
    vivos = [m for m in MAPAS_QUE_VOLTAM
             if "cortado_por" not in le_json(f"{MAPS}/{m}/map.json")]
    print(f"mapas que voltam: {len(MAPAS_QUE_VOLTAM)} "
          f"({len(vivos)} já estão vivos)")
    lays = layouts_a_desencolher()
    print(f"\nlayouts que voltam ao tamanho de antes ({len(lays)}), NO MESMO ordinal:")
    for i, w, h in lays:
        print(f"  {i:46s} 1x1 -> {w}x{h}")
    print(f"\ntabelas de mato que voltam: {volta_mato(aplicar=False)}")
    print(f"sorteio da Turnback a devolver: {volta_turnback_inc(aplicar=False)}")
    print("\nportas que reabrem:")
    for m, idx, tirou, sobrou in reabre(aplicar=False):
        print(f"  {m:34s} warps {idx}  placa sai: {tirou}"
              f"{'' if not sobrou else f'  (ainda fechados: {sobrou})'}")
    if not aplicar:
        print("\n(--dry-run: nada foi escrito)")
        return 0

    mudou = []
    for m in MAPAS_QUE_VOLTAM:
        q = revive_mapa(m, aplicar=True)
        if q:
            mudou.append((m, q))
    ganho = desencolhe_layouts(lays, aplicar=True)
    volta_turnback_inc(aplicar=True)
    posto = volta_mato(aplicar=True)
    portas = reabre(aplicar=True)
    ruim = confere_indices()
    if ruim:
        raise SystemExit("ÍNDICE DE SAVE ANDOU: " + "; ".join(ruim))
    print(f"\nAPLICADO: {len(mudou)} mapas de volta, {len(lays)} layouts "
          f"desencolhidos ({ganho/1024:.1f} KB de blockdata e borda), "
          f"{len(posto)} tabelas de mato, "
          f"{sum(len(i) for _m, i, _t, _s in portas)} portas reabertas.")
    print("índices de save: map_groups.json e a ordem de layouts.json intactos.")
    return 0


# ------------------------------------------------------------------------ demo
def demo():
    """Autoteste. Cada passo trava a armadilha que ele poderia cair."""
    ok = True

    def teste(nome, cond):
        nonlocal ok
        print(f"  [{'ok ' if cond else 'RUIM'}] {nome}")
        ok = ok and bool(cond)

    print("1. a lista não pisa em quem continua cortado")
    sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    import completude as C
    ainda = set()
    for x in C.CORTES_DO_GUI:
        if x["modo"] == "deficit":
            ainda |= set(x["alvo"])
    teste("nenhum mapa que volta continua em CORTES_DO_GUI",
          not (set(MAPAS_QUE_VOLTAM) & ainda))
    teste("a Battle Zone continua cortada", "Route225" in ainda)
    teste("o Pokétch continua cortado", "JubilifeCity_PoketchCompany_F1" in ainda)
    teste("o TrophyGarden continua cortado", "TrophyGarden" in ainda)

    print("2. o conteúdo de antes existe no git e não é túmulo")
    for m in MAPAS_QUE_VOLTAM[:3] + MAPAS_QUE_VOLTAM[-3:]:
        v = git_texto(f"data/maps/{m}/map.json")
        teste(f"{m} tem map.json em {ANTES} sem `cortado_por`",
              v is not None and "cortado_por" not in json.loads(v))

    # O QUE A SAVE INDEXA NÃO É A LISTA CRUA, e este teste já mediu a lista crua
    # uma vez, em 07/09/2026, e reprovou sozinho. `mapLayoutId` conta SÓ os
    # layouts cujo `border_filepath` existe no disco (mapjson.cpp:895), e o
    # arquivo carrega mais de cem FANTASMAS declarados sem `.bin`, restos da
    # importação de Johto, que não gastam número. Tirar um fantasma do meio (foi
    # o que a estação de Saffron exigiu, para a entrada de verdade poder entrar
    # no fim) muda a lista crua e não move ordinal nenhum. Medir a lista crua
    # aqui acusaria uma quebra que não existe, que é o jeito mais caro de errar.
    print("3. o ordinal do layout não anda")
    def numerados(js, existe):
        return [x["id"] for x in json.loads(js)["layouts"]
                if existe(x["border_filepath"])]
    L = numerados(open(f"{RAIZ}/data/layouts/layouts.json", encoding="utf-8").read(),
                  lambda p: os.path.exists(f"{RAIZ}/{p}"))
    tinha = set(subprocess.run(
        ["git", "-C", RAIZ, "ls-tree", "-r", "--name-only", ANTES, "data/layouts/"],
        capture_output=True, text=True).stdout.split())
    O = numerados(git_texto("data/layouts/layouts.json"), lambda p: p in tinha)
    teste("os ordinais de antes do corte continuam os mesmos, um a um",
          L[:len(O)] == O)
    teste("nenhum layout a desencolher ficou fora de layouts.json",
          all(i in L for i, _w, _h in layouts_a_desencolher()))

    # `tirou` FALSO com `sobrou` vazio é legítimo e acontece: a HearthomeCity
    # fechou as duas portas de Amity por ADOÇÃO da gêmea, e adoção não põe
    # placa nenhuma. O que a régua proíbe é o contrário, tirar a placa de um
    # mapa que ainda tem porta fechada.
    print("4. a placa nunca sai de mapa que ainda tem porta fechada")
    for m, _idx, tirou, sobrou in reabre(aplicar=False):
        teste(f"{m}: placa sai={tirou} com {len(sobrou)} porta(s) ainda fechada(s)",
              not (tirou and sobrou))

    print("5. idempotência: rodar de novo não acha nada para fazer")
    if all("cortado_por" not in le_json(f"{MAPS}/{m}/map.json")
           for m in MAPAS_QUE_VOLTAM):
        teste("nenhum layout a desencolher", not layouts_a_desencolher())
        teste("nenhuma porta a reabrir", not portas_a_reabrir())
        teste("nenhum mato a devolver", not volta_mato(aplicar=False))
        teste("nenhum índice andou", not confere_indices())
    else:
        print("  (ainda não aplicado; a metade de idempotência roda depois)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else relatorio(APLICAR))
