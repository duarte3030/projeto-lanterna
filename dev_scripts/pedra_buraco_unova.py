#!/usr/bin/env python3
"""Faz os 4 buracos de pedra de Unova virarem buraco DE VERDADE, trocando o
comportamento deles de `MB_NON_ANIMATED_DOOR` para `MB_MT_PYRE_HOLE`.

Uso:
    python3 dev_scripts/pedra_buraco_unova.py --demo    # prova, não grava
    python3 dev_scripts/pedra_buraco_unova.py --censo   # o censo das células
    python3 dev_scripts/pedra_buraco_unova.py           # grava (idempotente)

O PROBLEMA (Obra 2 de Unova, bloco B4, 15/08/2026)
--------------------------------------------------
Três mapas do BW3G têm pedra de Strength que o jogador empurra para dentro de um
buraco; a pedra tapa o buraco e abre caminho. Na fonte quem faz isso é o
`stonetable` do gen 2. Aqui o objeto da pedra já existe no idioma do Emerald
(`OBJ_EVENT_GFX_PUSHABLE_BOULDER` + `EventScript_StrengthBoulder`), mas o motor
só reage a pedra parada em DOIS comportamentos (src/field_control_avatar.c):

  - `MB_STRENGTH_BUTTON`  -> `HandleBoulderActivateVictoryRoadSwitch`, roda o
    coord_event daquela casa (idioma do FRLG, ver `VictoryRoad_1F_Frlg`);
  - `MB_MT_PYRE_HOLE`     -> `HandleBoulderFallThroughHole`, sobe SE_FALL e
    tira a pedra do mapa.

Os 4 buracos estavam com `MB_NON_ANIMATED_DOOR`, posto por
`blockdata_unova.forca_warps` só porque há um `warp_event` em cima deles (a
fonte usa o warp como a queda: ele devolve o jogador à boca do mapa). Com porta
o motor nunca sabe que a pedra caiu, e o `changeblock` da fonte não tem gatilho.

POR QUE `MB_MT_PYRE_HOLE` E NÃO `MB_STRENGTH_BUTTON`
----------------------------------------------------
`MB_STRENGTH_BUTTON` deixaria o buraco ANDÁVEL, e aí o jogador atravessa a pé e
a pedra vira enfeite: mataria o quebra-cabeça. Com `MB_MT_PYRE_HOLE` os dois
lados ficam certos de uma vez:

  - jogador pisa: `TryStartWarpEventScript` chama `SetupWarp` com o warp_event
    que JÁ está lá e roda `EventScript_FallDownHoleMtPyre` (fica invisível,
    SE_FALL, `DoFallWarp`). É a queda da fonte, agora com animação;
  - pedra para em cima: `HandleBoulderFallThroughHole` tira a pedra e roda o
    coord_event da casa, que é onde mora o `changeblock` traduzido.

A segunda metade (rodar o coord_event) foi acrescentada ao motor no mesmo
trabalho, espelhando a função irmã: `RunCoordEventScriptAt` em
src/field_control_avatar.c.

POR QUE MEXER NO ATRIBUTO É SEGURO AQUI, E COMO ISSO É COBRADO
---------------------------------------------------------------
Comportamento é atributo do METATILE (`metatile_attributes.bin`), não da célula:
mudar o atributo vaza para toda célula que usar aquele metatile. Por isso o
censo veio ANTES (15/08/2026, `--censo`): cada metatile de porta forçada destes
três tilesets é usado por EXATAMENTE as células de buraco abaixo, e por mais
nada no repo inteiro. `map.bin` não muda nem um byte: a célula continua com o
mesmo metatile.

O que poderia estragar isso é uma regeneração futura do blockdata pondo o mesmo
metatile de porta debaixo de um warp NOVO nesses tilesets, que herdaria buraco.
É isso que o `--demo` cobra: se aparecer célula fora da lista, ele quebra.
"""
import json
import os
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
import valida_warp_tile as W                                        # noqa: E402
from porta_de_saida_unova import le_attr, grava_attr                # noqa: E402

PORTA = W._MB["MB_NON_ANIMATED_DOOR"]
BURACO = W._MB["MB_MT_PYRE_HOLE"]

# (tileset, metatile) -> as células que DEVEM ser as únicas com esse metatile.
# Medido em 15/08/2026 pelo `--censo`; cada linha é um buraco de pedra da fonte.
ALVOS = {
    ("gTileset_UnovaTower", 539): {("Unova_DragonspiralTower2F", 6, 11)},
    ("gTileset_UnovaDreamyard", 559): {("Unova_Dreamyard", 10, 21)},
    ("gTileset_UnovaCaveRuins", 633): {("Unova_VictoryRoadCave1F", 11, 22),
                                       ("Unova_VictoryRoadCave1F", 32, 10)},
}


def celulas_por_metatile():
    """{(tileset, metatile): {(mapa, x, y)}} para os metatiles de ALVOS."""
    layouts = {l["id"]: l for l in
               json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    grupos = json.load(open(f"{RAIZ}/data/maps/map_groups.json"))
    achado = {k: set() for k in ALVOS}
    for mapas in grupos.values():
        if not isinstance(mapas, list):
            continue
        for nome in mapas:
            p = f"{RAIZ}/data/maps/{nome}/map.json"
            if not os.path.exists(p):
                continue
            lay = layouts.get(json.load(open(p))["layout"])
            if not lay:
                continue
            sec = lay.get("secondary_tileset")
            quero = [mt for (ts, mt) in ALVOS if ts == sec]
            if not quero:
                continue
            w, h = lay["width"], lay["height"]
            b = open(f"{RAIZ}/{lay['blockdata_filepath']}", "rb").read()
            for y in range(h):
                for x in range(w):
                    mid = struct.unpack_from("<H", b, (y * w + x) * 2)[0] & 0x3FF
                    if mid in quero:
                        achado[(sec, mid)].add((nome, x, y))
    return achado


def confere():
    """Erros do censo: metatile de buraco usado por célula que não é buraco."""
    achado, erros = celulas_por_metatile(), []
    for chave, esperado in ALVOS.items():
        veio = achado[chave]
        if veio != esperado:
            erros.append(f"{chave[0]} metatile {chave[1]}: células {sorted(veio)}, "
                         f"esperava {sorted(esperado)}. Se apareceu célula nova, "
                         f"alguém pôs porta forçada nova neste tileset e ela viraria "
                         f"buraco; duplique o metatile em vez de mexer no atributo.")
    return erros


def aplica(gravar=True):
    mudou = []
    for (tileset, metatile) in ALVOS:
        antes = le_attr(tileset, metatile)
        if antes & 0xFF == BURACO:
            continue
        if antes & 0xFF != PORTA:
            raise SystemExit(f"{tileset} metatile {metatile} tem comportamento "
                             f"{antes & 0xFF}, e não {PORTA}: a premissa mudou, "
                             "não vou sobrescrever às cegas.")
        if gravar:
            grava_attr(tileset, metatile, (antes & ~0xFF) | BURACO)
        mudou.append(f"{tileset} metatile {metatile}: "
                     f"MB_NON_ANIMATED_DOOR -> MB_MT_PYRE_HOLE")
    return mudou


def censo():
    for chave, celulas in sorted(celulas_por_metatile().items()):
        print(f"{chave[0]} metatile {chave[1]}: {len(celulas)} célula(s) no repo")
        for c in sorted(celulas):
            print(f"    {c[0]} ({c[1]},{c[2]})"
                  + ("" if c in ALVOS[chave] else "   <-- NÃO É BURACO DE PEDRA"))
    return 0


def demo():
    erros = confere()
    assert not erros, "censo reprovado:\n  " + "\n  ".join(erros)

    # o comportamento de destino tem que continuar disparando warp, senão o
    # jogador que pisa no buraco fica parado em cima dele
    assert BURACO in W.COMPORTA_WARP, "MB_MT_PYRE_HOLE saiu de COMPORTA_WARP"

    # e o motor tem que continuar com as duas metades: a que tira a pedra e a
    # que roda o coord_event da casa
    c = open(f"{RAIZ}/src/field_control_avatar.c").read()
    for trecho in ("MB_MT_PYRE_HOLE", "RunCoordEventScriptAt(object->currentCoords.x"):
        assert trecho in c, f"src/field_control_avatar.c sem `{trecho}`"

    faltam = aplica(gravar=False)
    print(f"OK: censo limpo, {sum(len(v) for v in ALVOS.values())} células nos "
          f"{len(ALVOS)} metatiles, nenhuma sobrando.")
    print("OK: MB_MT_PYRE_HOLE dispara warp e o motor roda o coord_event da casa.")
    print("aplicado" if not faltam else "PENDENTE de gravar:\n  " + "\n  ".join(faltam))


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    elif "--censo" in sys.argv:
        sys.exit(censo())
    else:
        feito = aplica()
        print("\n".join(feito) if feito else "nada a fazer (já aplicado)")
