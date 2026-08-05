import os

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")
EVENT_SCRIPTS_S = os.path.join(POKEMERALD_DIR, "data/event_scripts.s")

def main():
    print("--- Garantindo stub e inclusão de TODOS os mapas de Johto ---")
    
    with open(EVENT_SCRIPTS_S, "r", encoding="utf-8") as f:
        text = f.read()

    all_maps = [m for m in os.listdir(MAPS_DIR) if os.path.exists(os.path.join(MAPS_DIR, m, "map.json"))]
    new_includes = []

    for map_name in sorted(all_maps):
        map_dir = os.path.join(MAPS_DIR, map_name)
        scripts_inc = os.path.join(map_dir, "scripts.inc")
        script_symbol = f"{map_name}_MapScripts"
        
        # Garantir que scripts.inc contenha apenas o stub limpo
        stub_content = f"{script_symbol}::\n\t.byte 0\n"
        if not os.path.exists(scripts_inc) or map_name not in ["PalletTown", "VermilionCity_Frlg", "SlateportCity_Harbor", "CanalaveCity"]:
            with open(scripts_inc, "w", encoding="utf-8") as sf:
                sf.write(stub_content)

        inc_line = f'\t.include "data/maps/{map_name}/scripts.inc"'
        if inc_line not in text:
            new_includes.append(inc_line)

    if new_includes:
        text += "\n" + "\n".join(new_includes) + "\n"
        with open(EVENT_SCRIPTS_S, "w", encoding="utf-8") as f:
            f.write(text)

    print(f"Adicionados {len(new_includes)} inclui de mapas em event_scripts.s!")

if __name__ == "__main__":
    main()
