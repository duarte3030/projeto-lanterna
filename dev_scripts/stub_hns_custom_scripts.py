import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")

EXCLUDE_MAPS = {
    "PalletTown", "VermilionCity_Frlg", "SlateportCity_Harbor", "CanalaveCity", "OlivineCity_PortInside"
}

def main():
    print("--- Verificação universal de scripts.inc de Johto e Sinnoh ---")
    count = 0

    for map_name in os.listdir(MAPS_DIR):
        if map_name in EXCLUDE_MAPS:
            continue
        scripts_inc = os.path.join(MAPS_DIR, map_name, "scripts.inc")
        if os.path.exists(scripts_inc):
            with open(scripts_inc, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Se contiver macros HnS ou flags de tempo/customizadas nao-Emerald
            if any(k in content for k in [
                "applymovement2", "baobacheckmon", "checkrandomizer", "giveoddegg",
                "givebp", "removenamedmon", "setwildbattleshiny", "FLAG_DAY_POKEMON",
                "FLAG_NIGHT_POKEMON", "VAR_TEMP_0", "LOCALID_ILEX_FOREST"
            ]):
                stub_content = f"{map_name}_MapScripts::\n\t.byte 0\n"
                with open(scripts_inc, "w", encoding="utf-8") as f:
                    f.write(stub_content)
                count += 1

    print(f"Limpos {count} scripts.inc com macros/flags incompatíveis!")

if __name__ == "__main__":
    main()
