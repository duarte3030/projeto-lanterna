import os
import re

POKEMERALD_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"
MAPS_DIR = os.path.join(POKEMERALD_DIR, "data/maps")
EVENT_SCRIPTS_S = os.path.join(POKEMERALD_DIR, "data/event_scripts.s")

def main():
    print("--- Substituindo applymovement2 por applymovement ---")
    count = 0
    for root, _, files in os.walk(MAPS_DIR):
        for f in files:
            if f.endswith(".inc"):
                fp = os.path.join(root, f)
                with open(fp, "r", encoding="utf-8") as file:
                    content = file.read()
                if "applymovement2" in content:
                    content = content.replace("applymovement2", "applymovement")
                    with open(fp, "w", encoding="utf-8") as file:
                        file.write(content)
                    count += 1

    # Limpar duplicatas de stubs no final de event_scripts.s se houver
    with open(EVENT_SCRIPTS_S, "r", encoding="utf-8") as f:
        es_content = f.read()

    # Se UnusedContestHall1_MapScripts:: .byte 0 foi adicionado no final de event_scripts.s ou scripts.inc
    print(f"Substituído applymovement2 em {count} arquivos .inc!")

if __name__ == "__main__":
    main()
