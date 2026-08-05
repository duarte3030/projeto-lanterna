import json
import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")

def main():
    print("--- Removendo object_events com coordenadas negativas fora do mapa ---")
    fixed_count = 0

    for map_name in os.listdir(MAPS_DIR):
        map_json = os.path.join(MAPS_DIR, map_name, "map.json")
        if os.path.exists(map_json):
            try:
                with open(map_json, "r", encoding="utf-8") as f:
                    data = json.load(f)

                objs = data.get("object_events", [])
                valid_objs = [o for o in objs if o.get("x", 0) >= 0 and o.get("y", 0) >= 0]

                if len(valid_objs) != len(objs):
                    data["object_events"] = valid_objs
                    with open(map_json, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2)
                    fixed_count += 1
            except Exception:
                pass

    print(f"Limpos {fixed_count} arquivos map.json com eventos fora dos limites!")

if __name__ == "__main__":
    main()
