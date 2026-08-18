#!/usr/bin/env python3
"""Da ponto de cura as 7 cidades de ginasio de Sinnoh que nao tinham, mais a
Liga sul (Fase C, 18/08/2026, autorizado em PRD-GOAL.md, secao "Portoes Fable
da Fase C RESOLVIDOS", item 3).

Uso:
    python3 dev_scripts/heal_locations_sinnoh_ginasios.py --demo
    python3 dev_scripts/heal_locations_sinnoh_ginasios.py             # mostra o que faria
    python3 dev_scripts/heal_locations_sinnoh_ginasios.py --gravar

O QUE ESTAVA ERRADO

Sinnoh so tinha ponto de cura para Oreburgh (HEAL_LOCATION_OREBURGH_CITY),
Sandgem e Jubilife. Eterna, Veilstone, Pastoria, Hearthome, Canalave,
Snowpoint, Sunyshore e a Liga sul nao tinham: desmaiar nelas respawnava em
outra regiao (src/chapter_jump.c tinha a mesma limitacao, coberta ali por
MAPA()/CENTRO_SINNOH() em vez de HEAL_LOCATION_*).

O QUE ESTE SCRIPT FAZ (mesmo molde de dev_scripts/heal_locations_unova.py)

Para cada um dos 8 Centros:
  1. uma entrada em `src/data/heal_locations.json`, a FONTE de verdade: os
     dois headers (include/constants/heal_locations.h e
     src/data/heal_locations.h) sao AUTO_GEN_TARGETS do json_data_rules.mk e
     nascem dela na build; editar os headers a mao seria escrever num
     arquivo que a build sobrescreve (tem o aviso DO NOT MODIFY no topo);
  2. o campo `local_id` na enfermeira do `map.json` (primeiro object_event),
     que e como o ponto de cura se refere ao NPC de respawn. O
     `LOCALID_*_PC_NURSE` nao e escrito aqui: include/constants/
     map_event_ids.h tambem e AUTO_GEN_TARGET (map_data_rules.mk, gerado por
     `mapjson event_constants`) e esta no .gitignore;
  3. um MAP_SCRIPT_ON_TRANSITION com `setrespawn`, copiado do molde de
     data/maps/VioletCity_PokemonCenter/scripts.inc (Johto).

DE ONDE SAI A COORDENADA (7,4)

Os 8 Centros compartilham LAYOUT_OREBURGH_CITY_POKEMON_CENTER_1F
(data/layouts/OreburghCity_PokemonCenter_1F/map.bin), o MESMO layout do
Centro de Oreburgh, cujo ponto de cura ja registrado em heal_locations.json
fica em (7,4). Conferido no proprio map.bin: (7,4) e chao (colisao 0) e
(7,3), a casa logo abaixo da enfermeira em (7,2), e parede (colisao 1).

SAVE: append puro. Ponto de cura novo entra no FIM do enum
(HEAL_LOCATION_*), e o que a save guarda nao e o indice e sim
`struct WarpData` (grupo, mapa, x, y) em gSaveBlock1Ptr->lastHealLocation,
entao nenhuma save antiga muda de lugar (ver dev_scripts/guarda_save.py).
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON = f"{RAIZ}/src/data/heal_locations.json"
MAPAS = f"{RAIZ}/data/maps"

X, Y = 7, 4                 # ver o cabecalho
ENFERMEIRA = (7, 2)         # posicao da enfermeira nos 8 Centros
LAYOUT_ESPERADO = "LAYOUT_OREBURGH_CITY_POKEMON_CENTER_1F"

# (pasta do map.json, HEAL_LOCATION_*, LOCALID_*)
CENTROS = [
    ("EternaCityPokecenter1F",         "HEAL_LOCATION_ETERNA_CITY",         "LOCALID_ETERNA_PC_NURSE"),
    ("VeilstoneCityPokecenter1F",      "HEAL_LOCATION_VEILSTONE_CITY",      "LOCALID_VEILSTONE_PC_NURSE"),
    ("PastoriaCityPokecenter1F",       "HEAL_LOCATION_PASTORIA_CITY",       "LOCALID_PASTORIA_PC_NURSE"),
    ("HearthomeCityPokecenter1F",      "HEAL_LOCATION_HEARTHOME_CITY",      "LOCALID_HEARTHOME_PC_NURSE"),
    ("CanalaveCityPokecenter1F",       "HEAL_LOCATION_CANALAVE_CITY",       "LOCALID_CANALAVE_PC_NURSE"),
    ("SnowpointCityPokecenter1F",      "HEAL_LOCATION_SNOWPOINT_CITY",      "LOCALID_SNOWPOINT_PC_NURSE"),
    ("SunyshoreCityPokecenter1F",      "HEAL_LOCATION_SUNYSHORE_CITY",      "LOCALID_SUNYSHORE_PC_NURSE"),
    ("PokemonLeagueSouthPokecenter1F", "HEAL_LOCATION_POKEMON_LEAGUE_SOUTH", "LOCALID_POKEMON_LEAGUE_SOUTH_PC_NURSE"),
]


def mapa_id(pasta):
    return json.load(open(f"{MAPAS}/{pasta}/map.json"))["id"]


def confere(pasta):
    """A enfermeira e mesmo o primeiro object_event, no layout certo, onde esperamos."""
    d = json.load(open(f"{MAPAS}/{pasta}/map.json"))
    if d["layout"] != LAYOUT_ESPERADO:
        return f"{pasta}: layout e {d['layout']}, esperava {LAYOUT_ESPERADO}"
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
    problemas = [p for p in (confere(pasta) for pasta, _h, _l in CENTROS) if p]
    if problemas:
        for p in problemas:
            print("  reprovado:", p)
        return 1

    d = json.load(open(JSON))
    ja = {h["id"] for h in d["heal_locations"]}
    novos = []
    for pasta, heal, localid in CENTROS:
        if heal in ja:
            continue
        mapa = mapa_id(pasta)
        novos.append({"id": heal, "map": mapa, "x": X, "y": Y,
                      "respawn_map": mapa, "respawn_npc": localid})
    d["heal_locations"].extend(novos)

    mudou_json, mudou_script = [], []
    for pasta, heal, localid in CENTROS:
        pj = f"{MAPAS}/{pasta}/map.json"
        md = json.load(open(pj))
        if md["object_events"][0].get("local_id") != localid:
            mudou_json.append((pj, md, localid))
        ps = f"{MAPAS}/{pasta}/scripts.inc"
        s = open(ps, encoding="utf-8").read()
        if f"setrespawn {heal}" not in s:
            mudou_script.append((ps, pasta, heal, s))

    print(f"Centros de Sinnoh (ginasios + Liga sul): {len(CENTROS)}")
    print(f"  entradas novas em heal_locations.json: {len(novos)}")
    print(f"  map.json a receber local_id:           {len(mudou_json)}")
    print(f"  scripts.inc a receber setrespawn:      {len(mudou_script)}")
    if not gravar:
        print("\n(nada gravado; use --gravar)")
        return 0

    with open(JSON, "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")

    for pj, md, localid in mudou_json:
        # `local_id` entra como PRIMEIRA chave, como os Centros ja existentes.
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
                f"@ Ponto de cura de Sinnoh (dev_scripts/heal_locations_sinnoh_ginasios.py).\n"
                f"{pasta}_OnTransition:\n"
                f"\tsetrespawn {heal}\n"
                f"\tend\n")
        s = s.replace(f"{rot}\n\t.byte 0\n", novo, 1)
        open(ps, "w", encoding="utf-8").write(s)

    print("\ngravado.")
    return 0


def demo():
    assert len(CENTROS) == 8, CENTROS
    for pasta, heal, localid in CENTROS:
        assert confere(pasta) is None, confere(pasta)
        assert heal.startswith("HEAL_LOCATION_") and localid.endswith("_PC_NURSE")

    # (7,4) e chao de verdade e (7,3) NAO e, no layout compartilhado pelos 8.
    import struct
    lay = {l["id"]: l for l in
           json.load(open(f"{RAIZ}/data/layouts/layouts.json"))["layouts"]}
    l = lay[LAYOUT_ESPERADO]
    b = open(f"{RAIZ}/{l['blockdata_filepath']}", "rb").read()
    def col(x, y):
        return (struct.unpack_from("<H", b, (y * l["width"] + x) * 2)[0] >> 10) & 3
    assert col(X, Y) == 0, f"({X},{Y}) nao e andavel"
    assert col(X, Y - 1) != 0, f"({X},{Y - 1}) e andavel, revise a escolha de ({X},{Y})"

    # MUTACAO: enfermeira fora do lugar tem que reprovar, senao `confere` nao olha nada.
    p = f"{MAPAS}/EternaCityPokecenter1F/map.json"
    guarda = open(p, encoding="utf-8").read()
    try:
        md = json.loads(guarda)
        md["object_events"][0]["x"] = 2
        open(p, "w", encoding="utf-8").write(json.dumps(md, indent=2) + "\n")
        assert confere("EternaCityPokecenter1F") is not None, \
            "a conferencia aceitou enfermeira em (2,2): ela nao serve"
    finally:
        open(p, "w", encoding="utf-8").write(guarda)

    print(f"demo ok: {len(CENTROS)} Centros de Sinnoh (ginasios + Liga sul), todos com a "
          f"enfermeira em {ENFERMEIRA} e chamando Common_EventScript_PkmnCenterNurse; "
          f"({X},{Y}) e andavel e ({X},{Y - 1}) e parede; mutacao pega")
    return 0


if __name__ == "__main__":
    sys.exit(demo() if "--demo" in sys.argv else aplica("--gravar" in sys.argv))
