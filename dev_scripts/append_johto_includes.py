import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")
EVENT_SCRIPTS_S = os.path.join(POKEMERALD_DIR, "data/event_scripts.s")

EXCLUDE_OVERWRITE = {
    "PalletTown", "VermilionCity_Frlg", "SlateportCity_Harbor", "CanalaveCity", "OlivineCity_PortInside"
}

def main():
    print("--- Garantindo inclui para TODOS os mapas em event_scripts.s ---")
    with open(EVENT_SCRIPTS_S, "r", encoding="utf-8") as f:
        text = f.read()

    new_includes = []
    all_maps = sorted([m for m in os.listdir(MAPS_DIR) if os.path.isdir(os.path.join(MAPS_DIR, m))])

    for map_name in all_maps:
        scripts_inc = os.path.join(MAPS_DIR, map_name, "scripts.inc")
        if not os.path.exists(scripts_inc):
            continue

        if map_name not in EXCLUDE_OVERWRITE:
            # Se scripts.inc estiver vazio ou sem o rótulo do mapa, criar stub limpo
            with open(scripts_inc, "r", encoding="utf-8") as sf:
                s_content = sf.read().strip()
            if not s_content or f"{map_name}_MapScripts::" not in s_content:
                with open(scripts_inc, "w", encoding="utf-8") as sf:
                    sf.write(f"{map_name}_MapScripts::\n\t.byte 0\n")

        inc_line = f'\t.include "data/maps/{map_name}/scripts.inc"'
        if inc_line not in text:
            new_includes.append(inc_line)

    if new_includes:
        text += "\n" + "\n".join(new_includes) + "\n"
        with open(EVENT_SCRIPTS_S, "w", encoding="utf-8") as f:
            f.write(text)

    print(f"Anexados {len(new_includes)} novos inclui em event_scripts.s!")

if __name__ == "__main__":
    main()
