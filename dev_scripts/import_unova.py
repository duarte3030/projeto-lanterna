import json
import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")
LAYOUTS_JSON = os.path.join(POKEMERALD_DIR, "data/layouts/layouts.json")
MAP_GROUPS_JSON = os.path.join(POKEMERALD_DIR, "data/maps/map_groups.json")

UNOVA_MAPS = [
    ("NuvemaTown", 20, 20, "MAP_TYPE_TOWN", "MAPSEC_UNOVA_NUVEMA_TOWN", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("AccumulaTown", 30, 30, "MAP_TYPE_TOWN", "MAPSEC_UNOVA_ACCUMULA_TOWN", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("StriatonCity", 30, 30, "MAP_TYPE_CITY", "MAPSEC_UNOVA_STRIATON_CITY", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("NacreneCity", 35, 35, "MAP_TYPE_CITY", "MAPSEC_UNOVA_NACRENE_CITY", "gTileset_GeneralSinnoh", "gTileset_PetalburgSinnoh"),
    ("CasteliaCity", 40, 40, "MAP_TYPE_CITY", "MAPSEC_UNOVA_CASTELIA_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("CasteliaCity_Harbor", 20, 20, "MAP_TYPE_INDOOR", "MAPSEC_UNOVA_CASTELIA_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
    ("NimbasaCity", 40, 40, "MAP_TYPE_CITY", "MAPSEC_UNOVA_NIMBASA_CITY", "gTileset_GeneralSinnoh", "gTileset_Building"),
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

def main():
    print("--- Atualizando map.json de Unova para usar MAPSEC_UNOVA_* ---")
    for name, width, height, map_type, mapsec, pri_tile, sec_tile in UNOVA_MAPS:
        map_json_path = os.path.join(MAPS_DIR, name, "map.json")
        if os.path.exists(map_json_path):
            with open(map_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data["region_map_section"] = mapsec
            with open(map_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    print("Atualizados identificadores de seção de Unova!")

if __name__ == "__main__":
    main()
