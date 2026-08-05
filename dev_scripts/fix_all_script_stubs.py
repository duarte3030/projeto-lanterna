import json
import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")
MAP_GROUPS_JSON = os.path.join(POKEMERALD_DIR, "data/maps/map_groups.json")

EXCLUDE_PRESERVE = {
    "PalletTown", "VermilionCity_Frlg", "SlateportCity_Harbor", "CanalaveCity", "OlivineCity_PortInside"
}

JOHTO_GROUPS = [
    "gMapGroup_TownsAndRoutes_Johto", "gMapGroup_IndoorNewBark_Johto", "gMapGroup_IndoorCherrygrove_Johto",
    "gMapGroup_IndoorViolet_Johto", "gMapGroup_IndoorAzalea_Johto", "gMapGroup_IndoorGoldenrod_Johto",
    "gMapGroup_IndoorEcruteak_Johto", "gMapGroup_IndoorOlivine_Johto", "gMapGroup_IndoorCianwood_Johto",
    "gMapGroup_IndoorMahogany_Johto", "gMapGroup_IndoorBlackthorn_Johto", "gMapGroup_IndoorJohtoRoutes_Johto",
    "gMapGroup_Dungeons_Johto"
]

def main():
    print("--- Zerando scripts.inc de TODOS os mapas pertencentes aos grupos de Johto ---")
    with open(MAP_GROUPS_JSON, "r", encoding="utf-8") as f:
        map_groups = json.load(f)

    johto_map_names = set()
    for grp in JOHTO_GROUPS:
        for m in map_groups.get(grp, []):
            johto_map_names.add(m)

    count = 0
    for map_name in sorted(johto_map_names):
        if map_name in EXCLUDE_PRESERVE:
            continue
        map_path = os.path.join(MAPS_DIR, map_name)
        if os.path.isdir(map_path):
            scripts_inc = os.path.join(map_path, "scripts.inc")
            stub = f"{map_name}_MapScripts::\n\t.byte 0\n"
            with open(scripts_inc, "w", encoding="utf-8") as f:
                f.write(stub)
            count += 1

    print(f"Limpos e stubados {count} scripts.inc de Johto!")

if __name__ == "__main__":
    main()
