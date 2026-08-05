import json
import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")
LAYOUTS_JSON = os.path.join(POKEMERALD_DIR, "data/layouts/layouts.json")
MAP_GROUPS_JSON = os.path.join(MAPS_DIR, "map_groups.json")
EVENT_SCRIPTS_S = os.path.join(POKEMERALD_DIR, "data/event_scripts.s")
REGION_MAP_H = os.path.join(POKEMERALD_DIR, "include/constants/region_map_sections.h")

UNOVA_MAP_DEFS = [
    ("NuvemaTown", 25, 25, "MAP_TYPE_TOWN", "MAPSEC_UNOVA_NUVEMA_TOWN", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("AccumulaTown", 30, 30, "MAP_TYPE_TOWN", "MAPSEC_UNOVA_ACCUMULA_TOWN", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("StriatonCity", 35, 35, "MAP_TYPE_CITY", "MAPSEC_UNOVA_STRIATON_CITY", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("NacreneCity", 35, 35, "MAP_TYPE_CITY", "MAPSEC_UNOVA_NACRENE_CITY", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("CasteliaCity", 45, 45, "MAP_TYPE_CITY", "MAPSEC_UNOVA_CASTELIA_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("CasteliaCity_Harbor", 20, 20, "MAP_TYPE_INDOOR", "MAPSEC_UNOVA_CASTELIA_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("NimbasaCity", 45, 45, "MAP_TYPE_CITY", "MAPSEC_UNOVA_NIMBASA_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("DriftveilCity", 40, 40, "MAP_TYPE_CITY", "MAPSEC_UNOVA_DRIFTVEIL_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("MistraltonCity", 35, 35, "MAP_TYPE_CITY", "MAPSEC_UNOVA_MISTRALTON_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("IcirrusCity", 35, 35, "MAP_TYPE_CITY", "MAPSEC_UNOVA_ICIRRUS_CITY", "gTileset_GeneralSinnoh", "gTileset_CaveSinnoh"),
    ("OpelucidCity", 40, 40, "MAP_TYPE_CITY", "MAPSEC_UNOVA_OPELUCID_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("LacunosaTown", 30, 30, "MAP_TYPE_TOWN", "MAPSEC_UNOVA_LACUNOSA_TOWN", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("UndellaTown", 30, 30, "MAP_TYPE_TOWN", "MAPSEC_UNOVA_UNDELLA_TOWN", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("HumilauCity", 35, 35, "MAP_TYPE_CITY", "MAPSEC_UNOVA_HUMILAU_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("UnovaLeague", 40, 40, "MAP_TYPE_CITY", "MAPSEC_UNOVA_LEAGUE", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("Route1_Unova", 30, 40, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_1", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route2_Unova", 30, 40, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_2", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route3_Unova", 40, 30, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_3", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route4_Unova", 40, 40, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_4", "gTileset_GeneralSinnoh", "gTileset_CaveSinnoh"),
    ("Route5_Unova", 40, 30, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_5", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route6_Unova", 40, 30, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_6", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route7_Unova", 40, 30, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_7", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route8_Unova", 30, 40, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_8", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route9_Unova", 40, 30, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_9", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("Route10_Unova", 30, 50, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_10", "gTileset_GeneralSinnoh", "gTileset_CaveSinnoh"),
    ("Route11_Unova", 40, 30, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_11", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route12_Unova", 40, 30, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_12", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route13_Unova", 50, 40, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_13", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route14_Unova", 40, 40, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_14", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route15_Unova", 40, 30, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_15", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("Route16_Unova", 30, 40, "MAP_TYPE_ROUTE", "MAPSEC_UNOVA_ROUTE_16", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
]

def map_name_to_const(name):
    # Route1_Unova -> MAP_ROUTE1_UNOVA
    res = ""
    for i, char in enumerate(name):
        if char.isupper() and i > 0 and not name[i-1].isupper() and name[i-1] != '_':
            res += '_'
        res += char.upper()
    return f"MAP_{res.replace('__', '_')}"

def map_name_to_layout(name):
    return map_name_to_const(name).replace("MAP_", "LAYOUT_")

def main():
    print("--- Integrando a 5ª Região: UNOVA (Gen 5 / Teselia) ---")

    # 1. Carregar Layouts
    with open(LAYOUTS_JSON, "r", encoding="utf-8") as f:
        layouts_data = json.load(f)
    existing_layout_ids = {l["id"] for l in layouts_data.get("layouts", [])}

    # 2. Carregar Map Groups
    with open(MAP_GROUPS_JSON, "r", encoding="utf-8") as f:
        map_groups = json.load(f)

    if "gMapGroup_Unova" not in map_groups.get("group_order", []):
        map_groups["group_order"].append("gMapGroup_Unova")
    if "gMapGroup_Unova" not in map_groups:
        map_groups["gMapGroup_Unova"] = []

    unova_map_names = []

    for name, width, height, map_type, mapsec, pri_tile, sec_tile in UNOVA_MAP_DEFS:
        unova_map_names.append(name)
        map_dir = os.path.join(MAPS_DIR, name)
        os.makedirs(map_dir, exist_ok=True)

        layout_id = map_name_to_layout(name)

        # Criar map.json
        map_json = {
            "id": map_name_to_const(name),
            "name": name,
            "layout": layout_id,
            "music": "MUS_HG_ROUTE26",
            "region_map_section": mapsec,
            "requires_flash": False,
            "weather": "WEATHER_SUNNY" if map_type in ["MAP_TYPE_TOWN", "MAP_TYPE_CITY", "MAP_TYPE_ROUTE"] else "WEATHER_NONE",
            "map_type": map_type,
            "allow_cycling": True,
            "allow_escaping": False,
            "allow_running": True,
            "show_map_name": True,
            "battle_scene": "MAP_BATTLE_SCENE_NORMAL",
            "connections": 0,
            "object_events": [],
            "warp_events": [],
            "coord_events": [],
            "bg_events": []
        }

        # Se for CasteliaCity_Harbor, colocar o marinheiro da balsa
        if name == "CasteliaCity_Harbor":
            map_json["object_events"].append({
                "graphics_id": "OBJ_EVENT_GFX_SAILOR",
                "x": 8,
                "y": 12,
                "elevation": 0,
                "movement_type": "MOVEMENT_TYPE_LOOK_AROUND",
                "movement_range_x": 0,
                "movement_range_y": 0,
                "trainer_type": "TRAINER_TYPE_NONE",
                "trainer_sight_or_berry_tree_id": "0",
                "script": "CasteliaHarbor_EventScript_Sailor",
                "flag": "0"
            })

        with open(os.path.join(map_dir, "map.json"), "w", encoding="utf-8") as f:
            json.dump(map_json, f, indent=2)

        # Criar scripts.inc
        script_path = os.path.join(map_dir, "scripts.inc")
        if name == "CasteliaCity_Harbor":
            script_content = """CasteliaCity_Harbor_MapScripts::
	.byte 0

CasteliaHarbor_EventScript_Sailor::
	lock
	faceplayer
	msgbox CasteliaHarbor_Text_WhereTo, MSGBOX_DEFAULT
	multichoice 0, 0, MULTI_BOAT_DESTINATIONS, FALSE
	switch VAR_RESULT
	case 0, CasteliaHarbor_EventScript_SailToCanalave
	case 1, CasteliaHarbor_EventScript_SailToSlateport
	case 2, CasteliaHarbor_EventScript_SailToOlivine
	msgbox CasteliaHarbor_Text_ComeAgain, MSGBOX_DEFAULT
	release
	end

CasteliaHarbor_EventScript_SailToCanalave::
	msgbox CasteliaHarbor_Text_SettingSailToCanalave, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_CANALAVE_CITY, 10, 10
	release
	end

CasteliaHarbor_EventScript_SailToSlateport::
	msgbox CasteliaHarbor_Text_SettingSailToSlateport, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SLATEPORT_CITY_HARBOR, 8, 14
	release
	end

CasteliaHarbor_EventScript_SailToOlivine::
	msgbox CasteliaHarbor_Text_SettingSailToOlivine, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	release
	end

CasteliaHarbor_Text_WhereTo:
	.string "Bem-vindo ao Porto de Castelia City em Unova!\\nPara onde gostaria de navegar?$"

CasteliaHarbor_Text_SettingSailToCanalave:
	.string "Zarpando para Canalave City em Sinnoh!$"

CasteliaHarbor_Text_SettingSailToSlateport:
	.string "Zarpando para Slateport City em Hoenn!$"

CasteliaHarbor_Text_SettingSailToOlivine:
	.string "Zarpando para Olivine City em Johto!$"

CasteliaHarbor_Text_ComeAgain:
	.string "Volte quando quiser navegar.$"
"""
        else:
            script_content = f"{name}_MapScripts::\n\t.byte 0\n"

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)

        # Adicionar layout se nao existir
        if layout_id not in existing_layout_ids:
            layout_entry = {
                "id": layout_id,
                "name": f"{name}_Layout",
                "width": width,
                "height": height,
                "primary_tileset": pri_tile,
                "secondary_tileset": sec_tile,
                "border_filepath": "data/layouts/PetalburgCity/border.bin",
                "blockdata_filepath": "data/layouts/PetalburgCity/map.bin"
            }
            layouts_data["layouts"].append(layout_entry)
            existing_layout_ids.add(layout_id)

        if name not in map_groups["gMapGroup_Unova"]:
            map_groups["gMapGroup_Unova"].append(name)

    # Salvar Layouts
    with open(LAYOUTS_JSON, "w", encoding="utf-8") as f:
        json.dump(layouts_data, f, indent=2)

    # Salvar Map Groups
    with open(MAP_GROUPS_JSON, "w", encoding="utf-8") as f:
        json.dump(map_groups, f, indent=2)

    # Atualizar event_scripts.s
    with open(EVENT_SCRIPTS_S, "r", encoding="utf-8") as f:
        content = f.read()

    new_includes = ""
    for name in unova_map_names:
        inc_line = f'.include "data/maps/{name}/scripts.inc"\n'
        if inc_line not in content:
            new_includes += inc_line

    if new_includes:
        with open(EVENT_SCRIPTS_S, "a", encoding="utf-8") as f:
            f.write(new_includes)

    print(f"Criados e integrados 31 mapas de Unova em data/maps/, layouts.json e map_groups.json!")

if __name__ == "__main__":
    main()
