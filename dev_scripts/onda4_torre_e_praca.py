#!/usr/bin/env python3
"""Onda 4 do cartucho 1: a Trainer Tower de Sevii e a praça da Route 40 saem.

    python3 dev_scripts/onda4_torre_e_praca.py            # tabela, não escreve
    python3 dev_scripts/onda4_torre_e_praca.py --demo     # autoteste
    python3 dev_scripts/onda4_torre_e_praca.py --aplicar  # escreve

As duas decisões do Gui que este arquivo executa
------------------------------------------------
DECISÃO 28. A **TORRE** de Sevii sai, e a ILHA em volta fica. São coisas
diferentes e o nome engana: `SevenIsland_TrainerTower_Frlg` é o pedaço de ILHA
ao ar livre (tem conexão com `MAP_SEVEN_ISLAND`, itens escondidos e dois NPCs),
enquanto a torre são os ONZE mapas fechados `TrainerTower_{Lobby,1F..8F,
Elevator,Roof}_Frlg`. Só os onze saem.

DECISÃO 29. Prédio em Johto não leva a facility de Hoenn. A praça de verdade
não é o portãozinho de nome comprido: `Gate_Route40_TrainerHill_Courtyard` é uma
guarita com dois warps, os dois de volta para a Route 40. Quem leva a Hoenn é
`TrainerHill_Courtyard`, que a Route 40 alcança por CONEXÃO DE MAPA (andando
para o norte), e de lá saem cinco portas: Trainer Hill, as três Battle Tents e o
cais para `BattleFrontier_OutsideWest`. As cinco saem, junto com a conexão e com
a guarita. Trainer Hill e as três tendas CONTINUAM vivas, pela porta de Hoenn
(Route 111, Fallarbor, Verdanturf e Slateport), que nenhuma linha daqui toca.

TÚMULO, e não `rm`
------------------
Mesmo molde de `remove_mapas_cortados.py` e da onda 1 (seção 0.w do ESTADO): o
`map.json` fica no lugar com o id intacto e sem evento nenhum, `MAPSEC_NONE` e
um campo `cortado_por`; o `scripts.inc` fica só com o rótulo. A entrada do
layout NÃO sai de `layouts.json`, encolhe para 1x1 apontando para
`data/layouts/TocoVago`, porque `SaveBlock1.mapLayoutId` (0x32) é a POSIÇÃO do
layout na lista e apagar a entrada desloca todos os seguintes: a save do Gui
abriria no mapa certo com o desenho de outro.

A porta que ficava do lado de fora
----------------------------------
A porta da torre, em `SevenIsland_TrainerTower_Frlg` (58,7), é o ÚNICO warp
daquele mapa, então não há doador para lápide e a entrada é apagada de verdade
(mesma exceção que `remove_mapas_cortados.py` abriu para `RockPeakRuins` e
irmãos). O tile fica desenhado, sem warp, e ganha a placa ÚNICA do projeto,
`Common_EventScript_PortaFechada` ("Closed for renovations."), em inglês como
todo texto de dentro do jogo.

O que este arquivo NÃO faz
--------------------------
Não encosta em `DefinirRetornoPredioCompartilhado` (`src/field_specials.c`), o
special que devolve o jogador pela porta por onde entrou. Ele serve SEIS
prédios: Trainer Hill, as três tendas, e a loja e o museu de Lilycove que
Sinnoh reaproveita em Veilstone e em Oreburgh. Tirar a porta de Johto não tira
prédio nenhum dele: os quatro de Hoenn continuam com a porta de Hoenn e a dupla
de Sinnoh não é tocada. A prova está no `--demo`.
"""
import json
import os
import shutil
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPS = f"{RAIZ}/data/maps"

CORTADO_POR = ("decisoes 28 e 29 do Gui, cartucho 1 onda 4 "
               "(torre de Sevii e praca da Route 40)")

TORRE = ["TrainerTower_Lobby_Frlg"] + \
        [f"TrainerTower_{i}F_Frlg" for i in range(1, 9)] + \
        ["TrainerTower_Elevator_Frlg", "TrainerTower_Roof_Frlg"]
PRACA = ["Gate_Route40_TrainerHill_Courtyard", "TrainerHill_Courtyard"]
TUMULOS = TORRE + PRACA

# A ilha que FICA, e a porta que nela se fecha.
ILHA = "SevenIsland_TrainerTower_Frlg"
PORTA_DA_TORRE = (58, 7)
PLACA_FECHADA = "Common_EventScript_PortaFechada"

# O prédio novo da obra 3 nasce no tile da porta sul da guarita.
MAPA_TORRE_NOVA = "MAP_ROUTE40_BATTLE_TOWER"
PORTA_DA_TORRE_NOVA = (11, 13)

TOCO_BORDA = "data/layouts/TocoVago/border.bin"
TOCO_BLOCO = "data/layouts/TocoVago/map.bin"


# --------------------------------------------------------------------- leitura
def le(p):
    return json.load(open(p, encoding="utf-8"))


def grava(p, d):
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
        f.write("\n")


def mapa(m):
    return le(f"{MAPS}/{m}/map.json")


# --------------------------------------------------------------------- escrita
def esvazia(m, aplicar):
    """O cabeçalho fica, o conteúdo sai. Devolve True se mudaria alguma coisa."""
    p = f"{MAPS}/{m}/map.json"
    d = le(p)
    novo = dict(d)
    novo["region_map_section"] = "MAPSEC_NONE"
    novo["connections"] = None
    for k in ("object_events", "warp_events", "coord_events", "bg_events"):
        novo[k] = []
    novo["destinos_dinamicos"] = []
    novo["cortado_por"] = CORTADO_POR
    mudou = novo != d
    if mudou and aplicar:
        grava(p, novo)
    corpo = (f"@ Mapa CORTADO do escopo ({CORTADO_POR}). O rótulo abaixo fica\n"
             f"@ porque header.inc, gerado, aponta para ele.\n\n"
             f"{m}_MapScripts::\n\t.byte 0\n")
    ps = f"{MAPS}/{m}/scripts.inc"
    velho = open(ps, encoding="utf-8", errors="replace").read() \
        if os.path.exists(ps) else None
    if velho != corpo:
        mudou = True
        if aplicar:
            open(ps, "w", encoding="utf-8").write(corpo)
    return mudou


def encolhe_layouts(aplicar):
    """1x1 apontando para o TocoVago. O ORDINAL do layout não muda."""
    L = le(f"{RAIZ}/data/layouts/layouts.json")
    alvos = {mapa(m)["layout"] for m in TUMULOS}
    liberado, mexidos, pastas = 0, 0, []
    for x in L["layouts"]:
        if x["id"] not in alvos:
            continue
        if x["border_filepath"] == TOCO_BORDA and x["width"] == 1:
            continue
        for k in ("border_filepath", "blockdata_filepath"):
            f = f"{RAIZ}/{x[k]}"
            if os.path.exists(f):
                liberado += os.path.getsize(f)
                d = os.path.dirname(x[k])
                if d not in pastas and not d.endswith("TocoVago"):
                    pastas.append(d)
        mexidos += 1
        if aplicar:
            x["width"], x["height"] = 1, 1
            x["border_filepath"] = TOCO_BORDA
            x["blockdata_filepath"] = TOCO_BLOCO
    if aplicar and mexidos:
        grava(f"{RAIZ}/data/layouts/layouts.json", L)
        for d in pastas:
            shutil.rmtree(f"{RAIZ}/{d}", ignore_errors=True)
    return mexidos, liberado, pastas


def fecha_porta_da_torre(aplicar):
    """O único warp da ilha sai e o tile ganha a placa única do projeto."""
    p = f"{MAPS}/{ILHA}/map.json"
    d = le(p)
    novo = dict(d)
    novo["warp_events"] = [w for w in d["warp_events"]
                           if (w["x"], w["y"]) != PORTA_DA_TORRE]
    bgs = list(d.get("bg_events") or [])
    if not any(b.get("script") == PLACA_FECHADA for b in bgs):
        bgs.append({
            "type": "sign", "x": PORTA_DA_TORRE[0], "y": PORTA_DA_TORRE[1],
            "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
            "script": PLACA_FECHADA,
            "origem": "porta fechada (onda4_torre_e_praca.py)",
        })
    novo["bg_events"] = bgs
    mudou = novo != d
    if mudou and aplicar:
        grava(p, novo)
    return mudou


def limpa_route40(aplicar):
    """Some a conexão para a praça e as três portas do norte da guarita.

    A porta do SUL (índice 9) não some: ela é o tile de porta já provado e
    passa a ser a entrada da Battle Tower de Olivine (obra 3). As três do norte
    (índices 10, 11 e 12) são as ÚLTIMAS da lista, então apagá-las não desloca
    índice de ninguém.
    """
    p = f"{MAPS}/Route40/map.json"
    d = le(p)
    novo = dict(d)
    novo["connections"] = [c for c in d["connections"]
                           if c["map"] != "MAP_TRAINER_HILL_COURTYARD"]
    ws = []
    for w in d["warp_events"]:
        if (w["x"], w["y"]) == PORTA_DA_TORRE_NOVA:
            w = dict(w, dest_map=MAPA_TORRE_NOVA, dest_warp_id="0")
        elif w["dest_map"] == "MAP_GATE_ROUTE40_TRAINER_HILL_COURTYARD":
            continue
        ws.append(w)
    novo["warp_events"] = ws
    mudou = novo != d
    if mudou and aplicar:
        grava(p, novo)
    return mudou


def tira_o_cais(aplicar):
    """O cais do Battle Frontier para a praça, do lado de Hoenn.

    É o warp de índice 11, o ÚLTIMO de `BattleFrontier_OutsideWest`, então
    apagá-lo não desloca `dest_warp_id` de ninguém.
    """
    p = f"{MAPS}/BattleFrontier_OutsideWest/map.json"
    d = le(p)
    novo = dict(d)
    novo["warp_events"] = [w for w in d["warp_events"]
                           if w["dest_map"] != "MAP_TRAINER_HILL_COURTYARD"]
    mudou = novo != d
    if mudou and aplicar:
        grava(p, novo)
    return mudou


def limpa_destinos_dinamicos(aplicar):
    """A praça sai da lista de origens dos quatro prédios compartilhados."""
    mexidos = []
    for m in ("TrainerHill_Entrance", "FallarborTown_BattleTentLobby",
              "SlateportCity_BattleTentLobby", "VerdanturfTown_BattleTentLobby"):
        p = f"{MAPS}/{m}/map.json"
        d = le(p)
        dd = d.get("destinos_dinamicos")
        if not dd or "MAP_TRAINER_HILL_COURTYARD" not in dd:
            continue
        novo = dict(d)
        novo["destinos_dinamicos"] = [x for x in dd
                                      if x != "MAP_TRAINER_HILL_COURTYARD"]
        mexidos.append(m)
        if aplicar:
            grava(p, novo)
    return mexidos


# ---------------------------------------------------------------------- provas
def prova_hoenn_intacta():
    """As quatro portas de HOENN dos prédios compartilhados continuam de pé."""
    esperado = {
        "TrainerHill_Entrance": "Route111",
        "FallarborTown_BattleTentLobby": "FallarborTown",
        "SlateportCity_BattleTentLobby": "SlateportCity",
        "VerdanturfTown_BattleTentLobby": "VerdanturfTown",
    }
    faltando = []
    for lobby, rua in esperado.items():
        alvo = mapa(lobby)["id"]
        if not any(w["dest_map"] == alvo for w in mapa(rua)["warp_events"]):
            faltando.append(f"{rua} nao leva mais a {alvo}")
    return faltando


def prova_special_intacto():
    """O special de retorno continua servindo a loja e o museu de Lilycove."""
    fonte = open(f"{RAIZ}/src/field_specials.c", encoding="utf-8").read()
    if "DefinirRetornoPredioCompartilhado" not in fonte:
        return ["o special de retorno sumiu de src/field_specials.c"]
    ruim = []
    for m, quantos in (("LilycoveCity_DepartmentStore_1F", 2),
                       ("LilycoveCity_LilycoveMuseum_1F", 2)):
        d = mapa(m)
        n = sum(1 for w in d["warp_events"] if w["dest_map"] == "MAP_DYNAMIC")
        if n < quantos:
            ruim.append(f"{m} tem {n} porta(s) MAP_DYNAMIC, esperado {quantos}")
        inc = open(f"{MAPS}/{m}/scripts.inc", encoding="utf-8").read()
        if "DefinirRetornoPredioCompartilhado" not in inc:
            ruim.append(f"{m} deixou de chamar o special")
    return ruim


def prova_indices():
    """Nenhum warp vivo aponta para índice que se moveu."""
    g = le(f"{MAPS}/map_groups.json")
    todos = [m for grp in g["group_order"] for m in g[grp]]
    porid = {}
    for m in todos:
        p = f"{MAPS}/{m}/map.json"
        if os.path.exists(p):
            porid[le(p)["id"]] = m
    ruim = []
    for m in todos:
        p = f"{MAPS}/{m}/map.json"
        if not os.path.exists(p):
            continue
        d = le(p)
        for i, w in enumerate(d.get("warp_events") or []):
            alvo = w["dest_map"]
            if alvo in ("MAP_DYNAMIC", "MAP_UNDEFINED"):
                continue
            if alvo not in porid:
                ruim.append(f"{m} warp {i} aponta para {alvo}, que nao existe")
                continue
            dd = mapa(porid[alvo])
            n = len(dd.get("warp_events") or [])
            wid = w["dest_warp_id"]
            if str(wid).lstrip("-").isdigit() and int(wid) >= n:
                ruim.append(f"{m} warp {i} -> {alvo} indice {wid}, "
                            f"que so tem {n}")
    return ruim


# ------------------------------------------------------------------------ main
def tabela():
    print("TÚMULO (13 mapas: 11 da torre de Sevii, 2 da praça)")
    for m in TUMULOS:
        d = mapa(m)
        ev = sum(len(d.get(k) or []) for k in
                 ("object_events", "warp_events", "coord_events", "bg_events"))
        print(f"  {m:42s} {d['id']:44s} {ev:3d} eventos"
              f"{'  JÁ É TÚMULO' if d.get('cortado_por') else ''}")
    print()
    print(f"FICA de pé: {ILHA} (ilha, não torre), "
          "TrainerHill_*, as três Battle Tents")
    print()
    n, b, pastas = encolhe_layouts(False)
    print(f"layouts a encolher para 1x1: {n}, "
          f"geometria a liberar: {b} B ({b/1024:.1f} KB), "
          f"{len(pastas)} pastas")


def demo():
    """Autoteste: só lê, e mede o que a onda promete."""
    erros = []

    # 1. A ilha é ilha, e a torre é torre.
    ilha = mapa(ILHA)
    if not any(c["map"] == "MAP_SEVEN_ISLAND"
               for c in (ilha.get("connections") or [])):
        erros.append(f"{ILHA} devia ter conexao com MAP_SEVEN_ISLAND: e ilha")
    if ILHA in TUMULOS:
        erros.append(f"{ILHA} nao pode virar tumulo: e a ilha, nao a torre")
    if len(TORRE) != 11:
        erros.append(f"a torre tem 11 mapas, a lista tem {len(TORRE)}")

    # 2. Hoenn continua entrando nos quatro prédios compartilhados.
    erros += prova_hoenn_intacta()

    # 3. O special de retorno continua inteiro e a dupla de Sinnoh também.
    erros += prova_special_intacto()

    # 4. Nenhum índice de warp se moveu.
    erros += prova_indices()

    # 5. Trainer Hill e as tendas não estão na lista de corte.
    for m in ("TrainerHill_Entrance", "TrainerHill_1F",
              "FallarborTown_BattleTentLobby", "SlateportCity_BattleTentLobby",
              "VerdanturfTown_BattleTentLobby"):
        if m in TUMULOS:
            erros.append(f"{m} NAO pode ser cortado")

    # 6. A placa da porta fechada é a única do projeto, e fala inglês.
    inc = open(f"{RAIZ}/data/scripts/portas_fechadas.inc", encoding="utf-8").read()
    if PLACA_FECHADA not in inc:
        erros.append(f"{PLACA_FECHADA} nao existe em portas_fechadas.inc")

    for e in erros:
        print("VERMELHO:", e)
    print("DEMO VERDE" if not erros else f"DEMO VERMELHO ({len(erros)})")
    return 0 if not erros else 1


def aplica():
    n = 0
    for m in TUMULOS:
        if esvazia(m, True):
            n += 1
    print(f"tumulos escritos: {n} de {len(TUMULOS)}")
    q, b, pastas = encolhe_layouts(True)
    print(f"layouts encolhidos: {q}, geometria apagada: {b} B, "
          f"pastas: {len(pastas)}")
    print("porta da torre fechada:", fecha_porta_da_torre(True))
    print("Route40 limpa:", limpa_route40(True))
    print("cais do Frontier tirado:", tira_o_cais(True))
    print("destinos_dinamicos limpos:", limpa_destinos_dinamicos(True))
    return 0


if __name__ == "__main__":
    if "--demo" in sys.argv:
        sys.exit(demo())
    if "--aplicar" in sys.argv:
        sys.exit(aplica())
    tabela()
