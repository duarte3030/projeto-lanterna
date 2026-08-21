#!/usr/bin/env python3
"""Liga a Battle Frontier de Hoenn a Johto, sem copiar mapa nenhum.

Uso:
    python3 dev_scripts/frontier_johto.py --demo      # só mostra o que faria
    python3 dev_scripts/frontier_johto.py --aplicar   # grava

Decisão do Gui (21/08/2026): a ROM inteira tem UMA battle facility, a de Hoenn,
e ela passa a ser alcançável de Johto, perto de Olivine. Nenhum mapa do Frontier
é copiado: os 40 e tantos mapas ficam onde estão, com os mesmos layouts, e o que
muda é só por onde se entra.

## O que a fonte de Johto tinha (medido, não lembrado)

O demake de HGSS (`fontes-mapas/hns`) NÃO tem `FrontierAccess` nem
`FrontierFront`. No ponto em que HGSS põe a Battle Frontier (norte da Route 40, a
oeste de Olivine) o demake já põe a SUA praça de instalações:
`Gate_Route40_TrainerHill_Courtyard` (portão de passagem no meio da Route 40) e,
pela conexão `up` da Route 40, o `TrainerHill_Courtyard`, com a entrada do
Trainer Hill e as três Battle Tents. Isso já foi importado, já é mapa de Johto
neste repo (`gMapGroup_IndoorJohtoRoutes_Johto`) e é andável desde a Route 40:
medido, de (13,45) da praça, `UP*15` mais `RIGHT*11` chega a (24,30).

Ou seja: a praça de facilities de Johto já existe e está no lugar certo. Só
faltava a Frontier estar nela. Por isso a porta nova entra AQUI, e não num mapa
de acesso inventado.

## Por que a chegada é no CAIS e não na praça do Frontier

Medido: a cena do Scott, o `setflag FLAG_SYS_FRONTIER_PASS` e o
`VAR_HAS_ENTERED_BATTLE_FRONTIER` moram em `BattleFrontier_ReceptionGate`
(`ON_FRAME_TABLE`), não no `OutsideWest`. Quem chega de balsa desembarca em
`OutsideWest` (19,67), ao SUL do portão de recepção, e só entra na praça
passando pela recepção, que é onde a cena dispara.

Se a porta de Johto largasse o jogador NA PRAÇA, ele pularia a recepção e ficaria
sem o Frontier Pass para sempre. Por isso a chegada de Johto é no mesmo cais da
balsa, um tile ao lado de onde a balsa de Lilycove larga o jogador
(`data/maps/LilycoveCity_Harbor/scripts.inc`: `warp
MAP_BATTLE_FRONTIER_OUTSIDE_WEST, 19, 67`). Daí em diante a cena do Scott roda
igual, venha o jogador de Hoenn ou de Johto.

## Os dois metatiles, e por que eles são inevitáveis

ARMADILHA MEDIDA, e é a razão de este script existir em vez de dois `map.json`
editados na mão: **não há um único tile de warp livre em toda a Battle
Frontier.** Varridos os 40 e tantos mapas `BattleFrontier_*` procurando metatile
com comportamento que o motor aceita como warp (`IsWarpMetatileBehavior` mais as
setas e as escadas diagonais, a mesma lista de `dev_scripts/valida_warp_tile.py`),
ANDÁVEL e sem warp declarado: o resultado é ZERO. O único candidato, (26,64) do
`OutsideWest`, é parede (colisão 1), então o jogador nunca pisa nele.

Warp em cima de tile comum é decoração: o jogador pisa e nada acontece. Foi assim
que Johto nasceu com 12 warps vivos de 771 (ver o cabeçalho de
`valida_warp_tile.py`). Então cada ponta precisa de UM metatile com comportamento
de warp:

  Johto  `TrainerHill_Courtyard` (24,29): metatile 35 -> 98.
         98 é `MB_ANIMATED_DOOR` e é o MESMO metatile das três Battle Tents
         deste mapa, em (20,28), (34,28) e (27,19), então a animação de porta já
         está resolvida para este par de tilesets. Colisão 1 e elevação 0 ficam
         como estão, que é exatamente o que aquelas três portas usam: porta
         animada é PAREDE, e entra-se ANDANDO CONTRA ela de baixo para cima
         (`TryDoorWarp`, que só aceita `DIR_NORTH`), não pisando em cima.

  Hoenn  `BattleFrontier_OutsideWest` (20,68): metatile 207 -> 857.
         857 é `MB_SOUTH_ARROW_WARP` do `gTileset_BattleFrontierOutsideWest`,
         o próprio tileset do mapa, e é o metatile que já está em (26,61), sob o
         arco: desenho de piso liso da praça, sem seta pintada. Escolhido por
         causa disso: o 36 do `gTileset_General`, que é o outro
         `MB_SOUTH_ARROW_WARP` à mão, desenha GRAMA, e grama no meio do cais de
         tijolo aparece de longe. (20,68) é a prancha de embarque, um beco sem
         saída (ao sul é o paredão 548): o jogador pisa nela e segura BAIXO para
         embarcar. Colisão 0 e elevação 0 não mudam.
         NÃO é (19,68), que é a outra metade da prancha: lá fica parada a
         atendente da balsa (`OBJ_EVENT_GFX_BEAUTY`, objeto 2, script
         `BattleFrontier_OutsideWest_EventScript_FerryAttendant`). Warp embaixo
         de NPC parado é warp morto, porque o jogador não pisa no tile.

Esse tile e UM warp acrescentado no fim da lista são a ÚNICA coisa que este
script muda fora de Johto. Nenhum warp existente é tocado, e em especial os da
balsa (que nem são warp de mapa: são `warp` por coordenada, feitos por script no
porto de Lilycove).

Idempotente: rodar de novo não duplica warp, placa nem tile.
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JOHTO = "TrainerHill_Courtyard"
HOENN = "BattleFrontier_OutsideWest"

# (mapa, x, y, metatile_novo, metatile_esperado_antes)
TILES = [
    (JOHTO, 24, 29, 98, 35),
    (HOENN, 20, 68, 857, 207),
]

WARP_JOHTO = {"x": 24, "y": 29, "elevation": 0,
              "dest_map": "MAP_BATTLE_FRONTIER_OUTSIDE_WEST", "dest_warp_id": None}
WARP_HOENN = {"x": 20, "y": 68, "elevation": 0,
              "dest_map": "MAP_TRAINER_HILL_COURTYARD", "dest_warp_id": None}

# Placa ao lado da porta, no mesmo lugar em que as três Battle Tents já têm a
# delas (linha 29 do mapa). Sem placa a porta nova é a quinta porta idêntica da
# praça e ninguém acha a Frontier.
PLACA = {"type": "sign", "x": 25, "y": 29, "elevation": 0,
         "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
         "script": "TrainerHill_Courtyard_EventScript_FrontierSign"}


def caminho_blockdata(layout_id):
    dados = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
    for l in dados["layouts"]:
        if l["id"] == layout_id:
            return f"{RAIZ}/{l['blockdata_filepath']}", l["width"], l["height"]
    raise SystemExit(f"layout {layout_id} não existe")


def le_mapa(nome):
    return json.load(open(f"{RAIZ}/data/maps/{nome}/map.json"))


def grava_mapa(nome, mapa):
    with open(f"{RAIZ}/data/maps/{nome}/map.json", "w") as f:
        json.dump(mapa, f, indent=2)
        f.write("\n")


def acha_warp(mapa, modelo):
    for i, w in enumerate(mapa["warp_events"]):
        if (int(w["x"]), int(w["y"]), w["dest_map"]) == (
                modelo["x"], modelo["y"], modelo["dest_map"]):
            return i
    return None


def main():
    aplicar = "--aplicar" in sys.argv
    if not aplicar and "--demo" not in sys.argv:
        raise SystemExit("use --demo ou --aplicar")

    johto, hoenn = le_mapa(JOHTO), le_mapa(HOENN)
    i_johto, i_hoenn = acha_warp(johto, WARP_JOHTO), acha_warp(hoenn, WARP_HOENN)
    idx_johto = len(johto["warp_events"]) if i_johto is None else i_johto
    idx_hoenn = len(hoenn["warp_events"]) if i_hoenn is None else i_hoenn

    mudou = False

    # 1. os dois metatiles
    for nome, x, y, novo, antes in TILES:
        mapa = johto if nome == JOHTO else hoenn
        caminho, w, _ = caminho_blockdata(mapa["layout"])
        blk = bytearray(open(caminho, "rb").read())
        off = 2 * (y * w + x)
        v = struct.unpack_from("<H", blk, off)[0]
        mt = v & 0x3FF
        if mt == novo:
            print(f"já feito  {nome} ({x},{y}) metatile {novo}")
            continue
        if mt != antes:
            raise SystemExit(
                f"PARE: {nome} ({x},{y}) tem metatile {mt}, esperava {antes} ou {novo}. "
                "O mapa mudou embaixo do script; conferir antes de gravar.")
        struct.pack_into("<H", blk, off, (v & ~0x3FF) | novo)
        print(f"tile      {nome} ({x},{y}) metatile {antes} -> {novo} "
              f"(colisão {(v >> 10) & 3} e elevação {v >> 12} inalteradas)")
        mudou = True
        if aplicar:
            open(caminho, "wb").write(bytes(blk))

    # 2. os dois warps, um apontando para o outro
    for mapa, nome, i, modelo, destino in (
            (johto, JOHTO, i_johto, WARP_JOHTO, idx_hoenn),
            (hoenn, HOENN, i_hoenn, WARP_HOENN, idx_johto)):
        warp = dict(modelo, dest_warp_id=str(destino))
        if i is None:
            print(f"warp      {nome}[{len(mapa['warp_events'])}] "
                  f"({warp['x']},{warp['y']}) -> {warp['dest_map']} #{destino}")
            mapa["warp_events"].append(warp)
            mudou = True
        elif mapa["warp_events"][i] != warp:
            print(f"warp      {nome}[{i}] corrigido -> {warp['dest_map']} #{destino}")
            mapa["warp_events"][i] = warp
            mudou = True
        else:
            print(f"já feito  {nome}[{i}] -> {warp['dest_map']} #{destino}")

    # 3. a placa
    if PLACA in johto["bg_events"]:
        print(f"já feito  placa em ({PLACA['x']},{PLACA['y']})")
    else:
        print(f"placa     {JOHTO} ({PLACA['x']},{PLACA['y']}) -> {PLACA['script']}")
        johto["bg_events"].append(PLACA)
        mudou = True

    if aplicar:
        grava_mapa(JOHTO, johto)
        grava_mapa(HOENN, hoenn)

    print("APLICADO" if (aplicar and mudou) else
          ("SEM MUDANÇA" if not mudou else "DEMO, nada gravado"))


if __name__ == "__main__":
    main()
