import json
import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
LAYOUTS_JSON = os.path.join(POKEMERALD_DIR, "data/layouts/layouts.json")

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

def main():
    print("--- Ajustando tilesets dos mapas de Johto em layouts.json ---")
    with open(LAYOUTS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed = 0
    for layout in data.get("layouts", []):
        pri = layout.get("primary_tileset")
        sec = layout.get("secondary_tileset")

        if pri not in VALID_TILESETS:
            layout["primary_tileset"] = "gTileset_GeneralSinnoh"
            fixed += 1

        if sec not in VALID_TILESETS:
            layout_id = layout.get("id", "")
            if "CAVE" in layout_id or "TUNNEL" in layout_id or "PATH" in layout_id:
                layout["secondary_tileset"] = "gTileset_CaveSinnoh"
            elif "POKEMON_CENTER" in layout_id:
                layout["secondary_tileset"] = "gTileset_PokemonCenter"
            elif "MART" in layout_id or "SHOP" in layout_id:
                layout["secondary_tileset"] = "gTileset_ShopSinnoh"
            else:
                layout["secondary_tileset"] = "gTileset_PetalburgSinnoh"
            fixed += 1

    with open(LAYOUTS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Ajustados {fixed} tilesets em layouts.json!")

if __name__ == "__main__":
    main()
