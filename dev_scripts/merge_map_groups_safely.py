import json
import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")
MAP_GROUPS_JSON = os.path.join(MAPS_DIR, "map_groups.json")
HNS_MAP_GROUPS_JSON = os.path.join(POKEMERALD_DIR, "../fontes-mapas/hns/data/maps/map_groups.json")

def main():
    print("--- Mesclando grupos de mapas de Johto válidos em map_groups.json ---")
    os.system(f"git checkout {MAP_GROUPS_JSON}")

    with open(MAP_GROUPS_JSON, "r", encoding="utf-8") as f:
        target = json.load(f)

    with open(HNS_MAP_GROUPS_JSON, "r", encoding="utf-8") as f:
        hns = json.load(f)

    existing_groups = set(target.get("group_order", []))
    existing_maps = set()
    for grp, maps in target.items():
        if grp != "group_order":
            for m in maps:
                existing_maps.add(m)

    added_groups = 0
    added_maps = 0

    for grp in hns.get("group_order", []):
        grp_name = grp if grp.endswith("_Johto") else f"{grp}_Johto"

        maps_to_add = []
        for m in hns.get(grp, []):
            # Verificar se a pasta do mapa realmente existe em data/maps
            if os.path.exists(os.path.join(MAPS_DIR, m)) and m not in existing_maps:
                maps_to_add.append(m)
                existing_maps.add(m)
                added_maps += 1

        if maps_to_add:
            if grp_name not in existing_groups:
                target["group_order"].append(grp_name)
                existing_groups.add(grp_name)
                added_groups += 1
            target[grp_name] = maps_to_add

    with open(MAP_GROUPS_JSON, "w", encoding="utf-8") as f:
        json.dump(target, f, indent=2)

    print(f"Adicionados {added_groups} grupos e {added_maps} mapas existentes de Johto em map_groups.json!")

if __name__ == "__main__":
    main()
