import json
import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")
MAP_GROUPS_JSON = os.path.join(POKEMERALD_DIR, "data/maps/map_groups.json")

PRESERVE_MAPS = {
    "PalletTown_Frlg", "VermilionCity_Frlg", "SlateportCity_Harbor", "CanalaveCity"
}

def main():
    print("--- Higienização TOTAL de todos os map.json de Johto ---")
    with open(MAP_GROUPS_JSON, "r", encoding="utf-8") as f:
        map_groups = json.load(f)

    johto_map_names = set()
    for grp, maps in map_groups.items():
        if grp.endswith("_Johto"):
            for m in maps:
                johto_map_names.add(m)

    sanitized = 0
    for map_name in johto_map_names:
        if map_name in PRESERVE_MAPS:
            continue
        map_json_path = os.path.join(MAPS_DIR, map_name, "map.json")
        if os.path.exists(map_json_path):
            with open(map_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Ajustar musica se for simbolo nao-Emerald
            music = str(data.get("music", ""))
            if "POKEMON_CENTER" in music:
                data["music"] = "MUS_HG_POKEMON_CENTER"
            elif not music.startswith("MUS_"):
                data["music"] = "MUS_HG_ROUTE26"

            for obj in data.get("object_events", []):
                # Preservar o marinheiro da balsa em OlivineCity_PortInside
                if map_name == "OlivineCity_PortInside" and obj.get("script") == "OlivinePort_EventScript_Sailor":
                    continue
                obj["flag"] = "0"
                obj["script"] = "0"
                obj["movement_type"] = "MOVEMENT_TYPE_LOOK_AROUND"
                obj["trainer_sight_or_berry_tree_id"] = "0"
                obj["graphics_id"] = "OBJ_EVENT_GFX_ITEM_BALL"

            data["coord_events"] = []
            data["bg_events"] = []

            sanitized += 1
            with open(map_json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    print(f"Higienizados {sanitized} arquivos map.json de Johto!")

if __name__ == "__main__":
    main()
