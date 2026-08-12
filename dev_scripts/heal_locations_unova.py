#!/usr/bin/env python3
"""Da a Unova os pontos de cura que a regiao nunca teve (bloco B6, 12/08/2026).

Uso:
    python3 dev_scripts/heal_locations_unova.py --demo      # autoteste, nao grava
    python3 dev_scripts/heal_locations_unova.py             # mostra o que faria
    python3 dev_scripts/heal_locations_unova.py --gravar

O QUE ESTAVA ERRADO, medido antes de escrever

`grep -n UNOVA include/constants/heal_locations.h` voltava VAZIO e
`grep -rn setrespawn data/maps/Unova_*` tambem. Consequencia: quem desmaiava em
Unova voltava para o ultimo Centro Pokemon de OUTRA regiao, e quem terminava o
Hall da Fama de Unova caia no mesmo lugar, porque `special GameClear` usa o
`lastHealLocation`. Unova e a ultima regiao do jogo, entao isso e uma viagem de
barco a cada desmaio.

O QUE ESTE SCRIPT FAZ, e por que e um script e nao 18 edicoes a mao

Os 18 Centros Pokemon de Unova sao IGUAIS: mesmo layout de 10x10, enfermeira em
(4,2) como PRIMEIRO object_event, e `Common_EventScript_PkmnCenterNurse` no
script dela. Trabalho que repete 18 vezes vira script (regra de trabalho do
projeto), e assim ele pode rodar de novo quando entrar Centro novo.

Para cada Centro:
  1. uma entrada em `src/data/heal_locations.json`, que e a FONTE: os dois
     headers (`include/constants/heal_locations.h` e `src/data/heal_locations.h`)
     sao AUTO_GEN_TARGETS do `json_data_rules.mk` e nascem dela na build. Editar
     header a mao seria escrever num arquivo que a build sobrescreve;
  2. o campo `local_id` na enfermeira do `map.json`, que e como os 40 pontos de
     cura que ja existem se referem ao NPC de respawn. O
     `LOCALID_UNOVA_*_PC_NURSE` NAO e escrito aqui: `include/constants/
     map_event_ids.h` tambem e AUTO_GEN_TARGET (`map_data_rules.mk:41`, gerado
     por `mapjson event_constants` a partir dos proprios `map.json`) e esta no
     `.gitignore`. Escrever nele a mao daria #define REPETIDO na primeira build;
  3. um `MAP_SCRIPT_ON_TRANSITION` com `setrespawn`, copiado de
     `data/maps/MahoganyTown_PokemonCenter/scripts.inc`.

DE ONDE SAI A COORDENADA (4,4), e nao foi chute: no `map.bin` do Centro de Unova
a linha 3 e parede de (3,3) a (6,3), entao (4,3) NAO existe como chao; (4,4) e a
casa andavel em frente ao balcao da enfermeira, alinhada com ela na coluna 4. O
vanilla usa (7,4) com a enfermeira em (7,1), ou seja o mesmo "a coluna dela, na
primeira linha livre do salao".

SAVE: append puro. Ponto de cura novo entra no FIM do enum, e o que a save guarda
nao e o indice e sim `struct WarpData` (grupo, mapa, x, y) em
`gSaveBlock1Ptr->lastHealLocation`, entao nenhuma partida antiga muda de lugar.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = f"{RAIZ}/src/data/heal_locations.json"
IDS = f"{RAIZ}/include/constants/map_event_ids.h"
MAPAS = f"{RAIZ}/data/maps"

X, Y = 4, 4                 # ver o cabecalho
ENFERMEIRA = (4, 2)         # posicao da enfermeira nos 18 Centros


def centros():
    """[(pasta, MAP_*, HEAL_LOCATION_*, LOCALID_*)] dos Centros 1F de Unova."""
    saida = []
    for pasta in sorted(os.listdir(MAPAS)):
        if not (pasta.startswith("Unova_") and pasta.endswith("Pokecenter1F")):
            continue
        d = json.load(open(f"{MAPAS}/{pasta}/map.json"))
        cidade = pasta[len("Unova_"):-len("Pokecenter1F")]
        seco = re.sub(r"(?<!^)(?=[A-Z])", "_", cidade).upper()
        saida.append((pasta, d["id"], f"HEAL_LOCATION_UNOVA_{seco}",
                      f"LOCALID_UNOVA_{seco}_PC_NURSE"))
    return saida


def confere(pasta):
    """A enfermeira e mesmo o primeiro object_event, e esta onde esperamos."""
    d = json.load(open(f"{MAPAS}/{pasta}/map.json"))
    o = (d.get("object_events") or [None])[0]
    if not o:
        return f"{pasta}: sem object_event"
    if (o["x"], o["y"]) != ENFERMEIRA or o["graphics_id"] != "OBJ_EVENT_GFX_NURSE":
        return (f"{pasta}: primeiro objeto e {o['graphics_id']} em "
                f"({o['x']},{o['y']}), esperava OBJ_EVENT_GFX_NURSE em {ENFERMEIRA}")
    s = open(f"{MAPAS}/{pasta}/scripts.inc", encoding="utf-8").read()
    if "Common_EventScript_PkmnCenterNurse" not in s:
        return f"{pasta}: o script nao chama Common_EventScript_PkmnCenterNurse"
    return None


def aplica(gravar):
    itens = centros()
    problemas = [p for p in (confere(c[0]) for c in itens) if p]
    if problemas:
        for p in problemas:
            print("  reprovado:", p)
        return 1

    d = json.load(open(JSON))
    ja = {h["id"] for h in d["heal_locations"]}
    novos = []
    for pasta, mapa, heal, localid in itens:
        if heal in ja:
            continue
        novos.append({"id": heal, "map": mapa, "x": X, "y": Y,
                      "respawn_map": mapa, "respawn_npc": localid})
    d["heal_locations"].extend(novos)

    ids = open(IDS, encoding="utf-8").read()
    faltam_id = [l for _, _, _h, l in itens
                 if not re.search(r"#define " + l + r"\b", ids)]

    mudou_json, mudou_script = [], []
    for pasta, mapa, heal, localid in itens:
        pj = f"{MAPAS}/{pasta}/map.json"
        md = json.load(open(pj))
        if md["object_events"][0].get("local_id") != localid:
            mudou_json.append((pj, pasta, localid, md))
        ps = f"{MAPAS}/{pasta}/scripts.inc"
        s = open(ps, encoding="utf-8").read()
        if f"setrespawn {heal}" not in s:
            mudou_script.append((ps, pasta, heal, s))

    print(f"Centros Pokemon de Unova: {len(itens)}")
    print(f"  entradas novas em heal_locations.json: {len(novos)}")
    print(f"  LOCALID que a build ainda vai gerar:    {len(faltam_id)}")
    print(f"  map.json a receber local_id:           {len(mudou_json)}")
    print(f"  scripts.inc a receber setrespawn:      {len(mudou_script)}")
    if not gravar:
        print("\n(nada gravado; use --gravar)")
        return 0

    with open(JSON, "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")

    for pj, _pasta, localid, md in mudou_json:
        # `local_id` entra como PRIMEIRA chave, que e como os 40 ja existentes
        # estao escritos; a ordem do resto nao muda.
        o = md["object_events"][0]
        md["object_events"][0] = {"local_id": localid,
                                  **{k: v for k, v in o.items() if k != "local_id"}}
        with open(pj, "w") as f:
            json.dump(md, f, indent=2)
            f.write("\n")

    for ps, pasta, heal, s in mudou_script:
        rot = pasta + "_MapScripts::"
        assert rot in s, ps
        novo = (f"{rot}\n"
                f"\tmap_script MAP_SCRIPT_ON_TRANSITION, {pasta}_OnTransition\n"
                f"\t.byte 0\n\n"
                f"@ Ponto de cura de Unova (dev_scripts/heal_locations_unova.py).\n"
                f"{pasta}_OnTransition:\n"
                f"\tsetrespawn {heal}\n"
                f"\tend\n")
        s = s.replace(f"{rot}\n\t.byte 0\n", novo, 1)
        open(ps, "w", encoding="utf-8").write(s)

    print("\ngravado.")
    return 0


def demo():
    itens = centros()
    assert len(itens) >= 18, f"achei so {len(itens)} Centros de Unova"
    for pasta, mapa, heal, localid in itens:
        assert confere(pasta) is None, confere(pasta)
        assert heal.startswith("HEAL_LOCATION_UNOVA_") and localid.endswith("_PC_NURSE")
    # nome derivado do CamelCase, e nao inventado
    por_pasta = {c[0]: c for c in itens}
    assert por_pasta["Unova_AspertiaPokecenter1F"][2] == "HEAL_LOCATION_UNOVA_ASPERTIA"
    assert por_pasta["Unova_PkmnLeaguePokecenter1F"][2] == "HEAL_LOCATION_UNOVA_PKMN_LEAGUE"
    assert por_pasta["Unova_VictoryRoadPokecenter1F"][3] == \
        "LOCALID_UNOVA_VICTORY_ROAD_PC_NURSE"

    # (4,4) e chao de verdade e (4,3) NAO e: e a razao de a coordenada nao ser
    # "logo abaixo da enfermeira". Sem esta conferencia o numero seria chute.
    import struct
    lay = {l["id"]: l for l in
           json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    for pasta, mapa, _h, _l in itens:
        md = json.load(open(f"{MAPAS}/{pasta}/map.json"))
        l = lay[md["layout"]]
        b = open(f"{RAIZ}/{l['blockdata_filepath']}", "rb").read()
        def col(x, y):
            return (struct.unpack_from("<H", b, (y * l["width"] + x) * 2)[0] >> 10) & 3
        assert col(X, Y) == 0, f"{pasta}: ({X},{Y}) nao e andavel"
        assert col(4, 3) != 0, f"{pasta}: (4,3) e andavel, revise a escolha de (4,4)"

    # MUTACAO: uma enfermeira fora do lugar TEM que reprovar a conferencia, senao
    # `confere` nao esta olhando nada.
    p = f"{MAPAS}/Unova_AspertiaPokecenter1F/map.json"
    guarda = open(p, encoding="utf-8").read()
    try:
        md = json.loads(guarda)
        md["object_events"][0]["x"] = 9
        open(p, "w", encoding="utf-8").write(json.dumps(md, indent=2) + "\n")
        assert confere("Unova_AspertiaPokecenter1F") is not None, \
            "a conferencia aceitou enfermeira em (9,2): ela nao serve"
    finally:
        open(p, "w", encoding="utf-8").write(guarda)

    print(f"demo ok: {len(itens)} Centros Pokemon de Unova, todos com a enfermeira em "
          f"{ENFERMEIRA} e chamando Common_EventScript_PkmnCenterNurse; ({X},{Y}) e "
          f"andavel e (4,3) e parede nos {len(itens)}; mutacao pega")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else aplica("--gravar" in sys.argv))
