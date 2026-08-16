#!/usr/bin/env python3
"""B6 Unova, Obra 1, bloco A2: gatilhos (`coord_event`) da máquina de `setscene`.

Uso:
    python3 dev_scripts/gatilhos_setscene_unova.py            # só relata, nao grava
    python3 dev_scripts/gatilhos_setscene_unova.py --aplicar  # escreve map.json e scripts.inc
    python3 dev_scripts/gatilhos_setscene_unova.py --demo     # autoteste, nao grava

O QUE ESTE SCRIPT FAZ

Varre o `.asm` de cada um dos 24 mapas LOCAIS da tabela "Obra 1" de
`PLANO-OBRAS-UNOVA.md` (mapa cujo próprio `coord_event` grava a var de cena;
os 3 mapas REMOTOS da mesma tabela não têm `coord_event` próprio e ficam de
fora) e, para cada `coord_event` de `setscene` que a fonte tem e o nosso
`data/maps/Unova_<Mapa>/map.json` AINDA NÃO tem naquela coordenada, escreve:

1. um gatilho novo em `coord_events`, apontando para um script que ainda não
   existe;
2. um STUB desse script em `scripts.inc` (só `end`, comentado como stub), para
   a build ficar verde e a suíte provar que o gatilho ARMA antes das cenas de
   verdade chegarem (blocos A4-A6 do plano).

Regra central, e por que ela é rígida: **a tabela `TABELA` abaixo é uma
TRANSCRIÇÃO LITERAL da seção "Tabela mapa → var → valores" de
`PLANO-OBRAS-UNOVA.md`, e não pode divergir dela.** Se um `SCENE_X` da fonte
não estiver na lista de valores do mapa, o gatilho NÃO tem para onde ir: o
script para (`SystemExit`) e reporta, em vez de inventar um índice novo. Quem
resolve a divergência é quem edita o PLANO, nunca este script.

Coordenada é identidade (decisão do plano): o importador de Unova copia x,y
1:1 da fonte, então "já tem `coord_event` naquele x,y" e "cena já portada" são
a mesma pergunta, sem raio para calibrar (a mesma régua que
`dev_scripts/fila_b6.py:coords_do_hack` usa). É por isso que
`CHAMPIONS_ROOM_ENTRANCE` sai com ZERO gatilhos novos: a fonte só tem um
`coord_event` nela, (7,6), e o mapa já tem um gatilho ali (a emboscada
`Unova_ChampionsRoomEntrance_EventScript_Emboscada`, de outra leva) — script e
var são outros, mas a COORDENADA já está ocupada, e reescrever por cima seria
inventar duas verdades para o mesmo tile. Por isso são 23 mapas que RECEBEM
gatilho, dos 24 locais da tabela.

`scene id -1` (achado em `Rt23East`/`Rt23West`) não é um `SCENE_X` de verdade:
é o idioma da casa para "gatilho sem máquina de estado", e a casa já resolve
isso com `VAR_TEMP_0`/`var_value 0` (ver `Unova_LentimasGym`,
`Unova_AspertiaGym`, `Unova_CasteliaGym`, todos escritos por levas
anteriores). Aqui o mesmo idioma é reaplicado, não reinventado.

`ShoppingMallNine` (decisão 5 do plano: zero `scene_script` na fonte) e
`IcirrusCitySouth` (as 16 cenas de lá são `callasm` de OUTRO bloco, a Obra 2)
não entram em `TABELA` de propósito: nenhum dos dois é mapa local da Obra 1.

STUB, elevação e colisão:

- O rótulo do stub é `Unova_<Mapa>_EventScript_<RótuloDaFonte>` (o rótulo QUE
  A CENA VAI TER nos blocos A4-A6, não um nome novo): `Unova_CasteliaCity
  Streets_EventScript_CherenAppears`, por exemplo. Corpo mínimo, só `end`,
  comentado `@ STUB A2: cena do bloco A4/A5/A6, rotulo <fonte>` — é o pedido
  explícito da missão, não o padrão livre de outra leva.
- `elevation` é sempre `0` no JSON, mesmo quando o tile é água (regra do
  plano); a MEDIÇÃO de colisão contra `data/layouts/<Layout>/map.bin` usa a
  elevação de verdade do tile, não a do JSON, porque o disparo em pokeemerald
  não depende de elevação bater, só de colisão ser 0
  (`src/event_object_movement.c`/`src/scrcmd.c`, e ver `PLANO-OBRAS-UNOVA.md`
  decisão 1 sobre a armadilha do `elevation` "não mexe").
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
import importa_unova as U               # noqa: E402  BW3G, PREFIXO, indice_asm

APLICAR = "--aplicar" in sys.argv

# --------------------------------------------------------------------------
# TABELA: transcrição literal da seção "Obra 1 - Tabela mapa -> var -> valores"
# de PLANO-OBRAS-UNOVA.md. Só os 24 mapas LOCAIS (os 3 remotos da mesma tabela
# não têm coord_event próprio, então não entram aqui). Chave é o CamelCase do
# BW3G (o que `dev_scripts/importa_unova.le_grupos` devolve para o MAP_CONST,
# e o que nomeia a pasta `data/maps/Unova_<camel>`).
TABELA = {
    "CasteliaCityStreets": dict(
        const="CASTELIA_CITY_STREETS", var="VAR_UNOVA_CASTELIA_RUAS_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_CASTELIA_CHEREN": "1",
                 "SCENE_CASTELIA_NOTHING": "2"}),
    "ChampionsRoomEntrance": dict(
        const="CHAMPIONS_ROOM_ENTRANCE", var="VAR_UNOVA_SALA_CAMPEAO_ENTRADA_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "DragonspiralTower6F": dict(
        const="DRAGONSPIRAL_TOWER_6F", var="VAR_UNOVA_DRAGONSPIRAL_6F_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "DragonspiralTowerRoof": dict(
        const="DRAGONSPIRAL_TOWER_ROOF", var="VAR_UNOVA_DRAGONSPIRAL_TOPO_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "DriftveilBridgeGate": dict(
        const="DRIFTVEIL_BRIDGE_GATE", var="VAR_UNOVA_DRIFTVEIL_PORTAO_PONTE_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "FloccesyTown": dict(
        const="FLOCCESY_TOWN", var="VAR_UNOVA_FLOCCESY_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "GiantChasm1F": dict(
        const="GIANT_CHASM_1F", var="VAR_UNOVA_GIANT_CHASM_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "LostlornForest": dict(
        const="LOSTLORN_FOREST", var="VAR_UNOVA_LOSTLORN_FOREST_CENA",
        valores={"SCENE_LOSTLORN_GRUNTS": "0", "SCENE_LOSTLORN_INFER": "1",
                 "SCENE_LOSTLORN_NOTHING": "2"}),
    "NacreneCity": dict(
        const="NACRENE_CITY", var="VAR_UNOVA_NACRENE_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "NimbasaParkBasement": dict(
        const="NIMBASA_PARK_BASEMENT", var="VAR_UNOVA_NIMBASA_PARK_PORAO_CENA",
        valores={"SCENE_NIMBASA_PARK_BASEMENT_INFER": "0",
                 "SCENE_NIMBASA_PARK_BASEMENT_PLASMA": "1",
                 "SCENE_NIMBASA_PARK_BASEMENT_NOTHING": "2"}),
    "NuvemaLab": dict(
        const="NUVEMA_LAB", var="VAR_UNOVA_NUVEMA_LAB_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "OpelucidCity": dict(
        const="OPELUCID_CITY", var="VAR_UNOVA_OPELUCID_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "P2Lab": dict(
        const="P2_LAB", var="VAR_UNOVA_P2_LAB_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "P2LabEntrance": dict(
        const="P2_LAB_ENTRANCE", var="VAR_UNOVA_P2_LAB_ENTRADA_CENA",
        valores={"SCENE_P2_LAB_ENTRANCE_DEFAULT": "0",
                 "SCENE_P2_LAB_ENTRANCE_AFTER": "1",
                 "SCENE_P2_LAB_ENTRANCE_NOTHING": "2"}),
    "PWTOutside": dict(
        const="PWT_OUTSIDE", var="VAR_UNOVA_PWT_FORA_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "PkmnLeagueEntrance": dict(
        const="PKMN_LEAGUE_ENTRANCE", var="VAR_UNOVA_LIGA_ENTRADA_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "PlayersHouse1F": dict(
        const="PLAYERS_HOUSE_1F", var="VAR_UNOVA_CASA_JOGADOR_1F_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "Rt12": dict(
        const="R_12", var="VAR_UNOVA_R12_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "Rt23East": dict(
        const="R_23_EAST", var="VAR_UNOVA_R23_LESTE_CENA",
        valores={"SCENE_R23_SHOWED_NONE": "0", "SCENE_R23_SHOWED_SPOOKY": "1",
                 "SCENE_R23_SHOWED_INSECT": "2", "SCENE_R23_SHOWED_TOXIC": "3",
                 "SCENE_R23_SHOWED_BASIC": "4", "SCENE_R23_SHOWED_GARNISH": "5",
                 "SCENE_R23_SHOWED_JET": "6"}),
    "Rt23Gate": dict(
        const="R_23_GATE", var="VAR_UNOVA_R23_PORTAO_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "Rt23West": dict(
        const="R_23_WEST", var="VAR_UNOVA_R23_OESTE_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "Rt5BridgeGate": dict(
        const="R_5_BRIDGE_GATE", var="VAR_UNOVA_R5_PORTAO_PONTE_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "SeasideCaveChamber": dict(
        const="SEASIDE_CAVE_CHAMBER", var="VAR_UNOVA_SEASIDE_CAVE_CAMARA_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_FINISHED": "1"}),
    "UndellaTown": dict(
        const="UNDELLA_TOWN", var="VAR_UNOVA_UNDELLA_CENA",
        valores={"SCENE_DEFAULT": "0", "SCENE_UNDELLA_TOWN_CANT_LEAVE": "1",
                 "SCENE_UNDELLA_TOWN_NOTHING": "2"}),
}

# `-1` na fonte não é SCENE_X: é o idioma da casa para "gatilho sem máquina de
# estado" (ver cabeçalho). Sempre a mesma var, sempre valor 0.
VAR_SEM_CENA = "VAR_TEMP_0"

RE_COORD = re.compile(r"^\s*coord_event\s+(-?\d+),\s*(-?\d+),\s*(-1|\w+),\s*(\w+)", re.M)

ABRE = "@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>"
FECHA = "@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<"


# --------------------------------------------------------------------- leitura

def coord_events_da_fonte(camel, idx):
    """[(x, y, scene, rotulo)] do bloco `<camel>_MapEvents` da fonte."""
    p = idx.get(camel) or f"{U.BW3G}/maps/{camel}.asm"
    if not os.path.exists(p):
        raise SystemExit(f"{camel}: arquivo da fonte não encontrado ({p})")
    asm = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(rf"^{camel}_MapEvents:", asm, re.M)
    if not m:
        raise SystemExit(f"{camel}: sem `{camel}_MapEvents` em {p}")
    return [mm.groups() for mm in RE_COORD.finditer(asm[m.end():])], p


def coords_do_hack(mapa):
    """Os pares (x, y) que `data/maps/<mapa>/map.json` já tem em coord_events."""
    d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                       encoding="utf-8"))
    return {(int(c.get("x", 0)), int(c.get("y", 0)))
            for c in (d.get("coord_events") or [])}


_LAYOUTS = None


def layouts():
    global _LAYOUTS
    if _LAYOUTS is None:
        d = json.load(open(os.path.join(REPO, "data/layouts/layouts.json")))
        _LAYOUTS = {l["id"]: l for l in d["layouts"]}
    return _LAYOUTS


def colisao(mapa, x, y):
    """Bits de colisão (0-3) do `map.bin` do layout de `mapa` em (x, y).

    Mesma leitura de `dev_scripts/changeblock_gen2.py` (`v & 0x3FF` o
    metatile, `(v >> 10) & 3` a colisão, `(v >> 12) & 0xF` a elevação):
    `MAPGRID_COLLISION_MASK` é bits 10-11 (`include/global.fieldmap.h`).
    """
    d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                       encoding="utf-8"))
    l = layouts()[d["layout"]]
    w, h = l["width"], l["height"]
    if not (0 <= x < w and 0 <= y < h):
        raise SystemExit(f"{mapa}: gatilho em ({x},{y}) cai fora do layout "
                         f"{w}x{h}")
    mapbin = open(os.path.join(REPO, l["blockdata_filepath"]), "rb").read()
    v = struct.unpack_from("<H", mapbin, (y * w + x) * 2)[0]
    return (v >> 10) & 3


# ------------------------------------------------------------- montagem

def pendencias():
    """[dict] com um item por gatilho a CRIAR (coordenada ainda não portada).

    Cada item já traz var/var_value resolvidos contra `TABELA` e o rótulo do
    stub. `SystemExit` na hora, não devolve lista parcial, se a fonte citar um
    `SCENE_X` que `TABELA` não conhece: é exatamente a régua "se divergir do
    PLANO, pare e reporte" da missão.
    """
    idx = U.indice_asm()
    saida = []
    for camel, info in TABELA.items():
        mapa = U.PREFIXO + camel
        eventos, caminho_fonte = coord_events_da_fonte(camel, idx)
        ja = coords_do_hack(mapa)
        for x, y, scene, rot in eventos:
            x, y = int(x), int(y)
            if (x, y) in ja:
                continue    # coordenada é identidade: já portado, preserva
            if scene == "-1":
                var, valor = VAR_SEM_CENA, "0"
            else:
                valor = info["valores"].get(scene)
                if valor is None:
                    raise SystemExit(
                        f"DIVERGÊNCIA: {camel} ({x},{y}) usa {scene} na fonte, "
                        f"que não está na tabela de {info['var']} do PLANO. "
                        f"Corrija PLANO-OBRAS-UNOVA.md antes; não estou "
                        f"inventando índice.")
                var = info["var"]
            script = f"{mapa}_EventScript_{rot}"
            col = colisao(mapa, x, y)
            if col != 0:
                raise SystemExit(
                    f"DIVERGÊNCIA: {camel} ({x},{y}) tem colisão {col} no "
                    f"map.bin (esperado 0); gatilho nunca dispararia ali.")
            saida.append(dict(camel=camel, mapa=mapa, const=info["const"],
                              x=x, y=y, var=var, var_value=valor,
                              script=script, rotulo_fonte=rot,
                              caminho_fonte=caminho_fonte))
    return saida


# ------------------------------------------------------------------- escrita

def grava_coord_events(itens_do_mapa, mapa):
    p = os.path.join(REPO, "data/maps", mapa, "map.json")
    d = json.load(open(p, encoding="utf-8"))
    existentes = {(int(c.get("x", 0)), int(c.get("y", 0)))
                  for c in (d.get("coord_events") or [])}
    novos = [i for i in itens_do_mapa if (i["x"], i["y"]) not in existentes]
    if not novos:
        return 0
    d.setdefault("coord_events", [])
    for i in novos:
        d["coord_events"].append({
            "type": "trigger", "x": i["x"], "y": i["y"], "elevation": 0,
            "var": i["var"], "var_value": i["var_value"], "script": i["script"],
        })
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    return len(novos)


def grava_stubs(itens_do_mapa, mapa):
    """Um STUB por RÓTULO único (mais de um gatilho pode citar o mesmo
    script, ex.: uma porta de dois tiles), dentro do bloco marcado
    ABRE/FECHA. Idempotente: relê o disco, só acrescenta rótulo que falta."""
    rotulos = {}
    for i in itens_do_mapa:
        rotulos.setdefault(i["script"], i["rotulo_fonte"])
    if not rotulos:
        return 0
    p = os.path.join(REPO, "data/maps", mapa, "scripts.inc")
    texto = open(p, encoding="utf-8").read()
    ja = set(re.findall(r"^(\w+)::", texto, re.M))
    faltam = {s: r for s, r in rotulos.items() if s not in ja}
    if not faltam:
        return 0
    blocos = "".join(
        f"@ STUB A2: cena do bloco A4/A5/A6, rotulo {r}\n{s}::\n\tend\n\n"
        for s, r in sorted(faltam.items()))
    if ABRE in texto:
        texto = texto.replace(FECHA, blocos + FECHA, 1)
    else:
        marca = f"\n{ABRE}\n{blocos}{FECHA}\n"
        # O bloco `_MapScripts::` pode ter linhas `map_script ...` no meio
        # (ex.: Unova_PkmnLeagueEntrance, editado a mao em 12/08/2026) antes
        # do terminador `.byte 0`; o gancho e o TERMINADOR, nao a primeira
        # linha depois do rotulo.
        gancho = re.search(rf"^{re.escape(mapa)}_MapScripts::\n(?:.*\n)*?\t\.byte 0\n",
                           texto, re.M)
        if not gancho:
            raise SystemExit(f"{mapa}: não achei `{mapa}_MapScripts::` em {p}")
        i = gancho.end()
        texto = texto[:i] + marca + texto[i:]
    with open(p, "w", encoding="utf-8") as f:
        f.write(texto)
    return len(faltam)


def aplica(itens):
    por_mapa = {}
    for i in itens:
        por_mapa.setdefault(i["mapa"], []).append(i)
    resumo = []
    for mapa, seus in sorted(por_mapa.items()):
        nc = grava_coord_events(seus, mapa)
        ns = grava_stubs(seus, mapa)
        resumo.append((mapa, nc, ns))
    return resumo


# --------------------------------------------------------------------- saida

def relatorio(itens):
    por_mapa = {}
    for i in itens:
        por_mapa.setdefault(i["mapa"], []).append(i)
    print(f"{'mapa':32} {'gatilhos novos':>14}")
    for mapa in sorted(TABELA):
        alvo = U.PREFIXO + mapa
        n = len(por_mapa.get(alvo, []))
        print(f"{alvo:32} {n:>14}")
    print(f"\ntotal de gatilhos novos: {len(itens)}   "
          f"mapas com pelo menos um: "
          f"{sum(1 for m in por_mapa if por_mapa[m])}")


def demo():
    """Autoteste. Vale tanto ANTES quanto DEPOIS de `--aplicar` já ter
    rodado: a contagem de PENDÊNCIA muda com o estado do repo (71 antes, 0
    depois de aplicado), mas a contagem da FONTE não muda nunca, e é ela que
    trava os números, junto com a cobertura fonte-contra-hack e as regras de
    processo (colisão, preservação, stub existente, idempotência)."""
    assert len(TABELA) == 24, f"mapas locais na TABELA: {len(TABELA)} (esperado 24)"

    idx = U.indice_asm()
    fonte_total = 0
    for camel in TABELA:
        eventos, _ = coord_events_da_fonte(camel, idx)
        fonte_total += len(eventos)
        mapa = U.PREFIXO + camel
        ja = coords_do_hack(mapa)
        # cobertura: toda coordenada que a fonte tem para este mapa PRECISA
        # estar no hack (aplicado agora, ou preservada de leva anterior,
        # como ChampionsRoomEntrance). Sem isso um gatilho ficaria mudo.
        faltando = [(x, y) for x, y, _, _ in eventos if (int(x), int(y)) not in ja]
        assert not faltando, f"{mapa}: coordenadas da fonte sem gatilho no hack: {faltando}"
        # colisão 0 em TODA coordenada da fonte, não só nas que este script
        # escreveu: se uma leva futura reescrever o hack por fora, a trava
        # ainda vale.
        for x, y, _, _ in eventos:
            c = colisao(mapa, int(x), int(y))
            assert c == 0, f"{mapa} ({x},{y}): colisão {c} (esperado 0)"
    # 71 pendentes + 1 já preservado (ChampionsRoomEntrance) na varredura de
    # 15/08/2026; é a fonte que trava este número, e ela não muda de estado.
    assert fonte_total == 72, f"coord_events de setscene na fonte: {fonte_total} (esperado 72)"

    # CHAMPIONS_ROOM_ENTRANCE: a fonte só tem UM coord_event, (7,6), e o mapa
    # já tinha um gatilho ali (a emboscada de outra leva) -- coordenada é
    # identidade, então este mapa nunca recebe gatilho NOVO deste script.
    ch_fonte, _ = coord_events_da_fonte("ChampionsRoomEntrance", idx)
    assert len(ch_fonte) == 1 and (7, 6) in coords_do_hack("Unova_ChampionsRoomEntrance")

    # todo `script` citado num coord_event de var da máquina de setscene (a
    # var do mapa, ou VAR_TEMP_0 para scene -1) tem rótulo de verdade em
    # scripts.inc -- gatilho que aponta para rótulo inexistente é erro de
    # linker, não bug silencioso.
    stubs_conferidos = 0
    for camel, info in TABELA.items():
        mapa = U.PREFIXO + camel
        d = json.load(open(os.path.join(REPO, "data/maps", mapa, "map.json"),
                           encoding="utf-8"))
        inc = open(os.path.join(REPO, "data/maps", mapa, "scripts.inc"),
                   encoding="utf-8").read()
        rotulos = set(re.findall(r"^(\w+)::", inc, re.M))
        for c in d.get("coord_events") or []:
            if c.get("var") not in (info["var"], VAR_SEM_CENA):
                continue    # gatilho de outra leva (ex.: emboscada), não é nosso
            assert c["script"] in rotulos, \
                f"{mapa}: {c['script']} citado em coord_event mas sem rótulo em scripts.inc"
            stubs_conferidos += 1
    assert stubs_conferidos >= 71, f"gatilhos da máquina de setscene conferidos: {stubs_conferidos}"

    # idempotência: rodar de novo NUNCA pode reabrir pendência (a régua de
    # coordenada-é-identidade garante isso sozinha, mas travar aqui pega
    # regressão se alguém trocar a régua sem querer).
    itens = pendencias()
    segunda = pendencias()
    assert len(itens) == len(segunda), "duas rodadas seguidas divergiram sem escrever nada"
    if itens:
        print(f"ainda NÃO aplicado nesta árvore: {len(itens)} gatilhos pendentes")
    else:
        print("já aplicado nesta árvore: 0 gatilhos pendentes (idempotente)")

    print(f"demo ok: {fonte_total} coord_events de setscene na fonte, "
          f"{stubs_conferidos} com rótulo conferido, ChampionsRoomEntrance preservado")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        itens = pendencias()
        relatorio(itens)
        if APLICAR:
            resumo = aplica(itens)
            print("\naplicado:")
            for mapa, nc, ns in resumo:
                print(f"  {mapa:32} +{nc} coord_events   +{ns} stubs")
        else:
            print("\n(nada gravado; use --aplicar)")
