import json
import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
LAYOUTS_JSON = os.path.join(POKEMERALD_DIR, "data/layouts/layouts.json")
HNS_LAYOUTS_JSON = os.path.join(POKEMERALD_DIR, "../fontes-mapas/hns/data/layouts/layouts.json")
SINNOH_LAYOUTS_JSON = os.path.join(POKEMERALD_DIR, "../fontes-mapas/sinnoh/data/layouts/layouts.json")

VALID_TILESETS = {
    "gTileset_General", "gTileset_GeneralSinnoh", "gTileset_Petalburg", "gTileset_PetalburgSinnoh",
    "gTileset_Slateport", "gTileset_Mauville", "gTileset_MauvilleSinnoh", "gTileset_Rustboro",
    "gTileset_RustboroSinnoh", "gTileset_Fortree", "gTileset_Lilycove", "gTileset_LilycoveSinnoh",
    "gTileset_Mossdeep", "gTileset_Sootopolis", "gTileset_EverGrande", "gTileset_EverGrandeSinnoh",
    "gTileset_Building", "gTileset_Shop", "gTileset_ShopSinnoh", "gTileset_PokemonCenter",
    "gTileset_Facility", "gTileset_InsideOfTruck", "gTileset_Cave", "gTileset_CaveSinnoh",
    "gTileset_Underwater", "gTileset_BikeShop", "gTileset_NavelRock", "gTileset_BattleFrontierOutsideWest",
    "gTileset_BattleFrontierOutsideEast", "gTileset_Fallarbor", "gTileset_Lavaridge", "gTileset_LavaridgeSinnoh",
    "gTileset_Pacifidlog", "gTileset_Dewford"
}

def sanitize_tileset(layout):
    pri = layout.get("primary_tileset")
    sec = layout.get("secondary_tileset")
    layout_id = layout.get("id", "")

    if pri not in VALID_TILESETS:
        layout["primary_tileset"] = "gTileset_GeneralSinnoh"

    if sec not in VALID_TILESETS:
        if "CAVE" in layout_id or "TUNNEL" in layout_id or "PATH" in layout_id:
            layout["secondary_tileset"] = "gTileset_CaveSinnoh"
        elif "POKEMON_CENTER" in layout_id:
            layout["secondary_tileset"] = "gTileset_PokemonCenter"
        elif "MART" in layout_id or "SHOP" in layout_id:
            layout["secondary_tileset"] = "gTileset_ShopSinnoh"
        elif "HOUSE" in layout_id or "BUILDING" in layout_id or "TOWER" in layout_id or "GATE" in layout_id:
            layout["secondary_tileset"] = "gTileset_Building"
        else:
            layout["secondary_tileset"] = "gTileset_PetalburgSinnoh"

def main():
    print("--- Restaurando layouts.json limpo e mesclando apenas os novos ---")
    os.system(f"git checkout {LAYOUTS_JSON}")

    with open(LAYOUTS_JSON, "r", encoding="utf-8") as f:
        target = json.load(f)

    existing_ids = {l["id"] for l in target.get("layouts", [])}
    existing_names = {l["name"] for l in target.get("layouts", [])}

    added = 0
    for src_path in [HNS_LAYOUTS_JSON, SINNOH_LAYOUTS_JSON]:
        if os.path.exists(src_path):
            with open(src_path, "r", encoding="utf-8") as f:
                src_data = json.load(f)
            for l in src_data.get("layouts", []):
                lid = l.get("id")
                lname = l.get("name")
                if lid and lid not in existing_ids and lname not in existing_names:
                    sanitize_tileset(l)
                    target["layouts"].append(l)
                    existing_ids.add(lid)
                    existing_names.add(lname)
                    added += 1

    with open(LAYOUTS_JSON, "w", encoding="utf-8") as f:
        json.dump(target, f, indent=2)

    print(f"Adicionados {added} novos layouts de Johto/Sinnoh sem duplicar nomes ou IDs!")

if __name__ == "__main__":
    main()
