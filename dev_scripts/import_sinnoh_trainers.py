#!/usr/bin/env python3
"""Converte os treinadores de pret/pokeplatinum para o formato .party do expansion.

Uso:
    python3 dev_scripts/import_sinnoh_trainers.py ../fontes-mapas/pokeplatinum

Escreve src/data/trainers_sinnoh.party. Times, níveis, golpes e falas saem
iguais aos de Platinum, que é o que foi pedido: primeiro copiar, ajustar depois.

Classe e pic de treinador são resolvidas contra as constantes que existem NESTE
repo, lidas em tempo de execução. Nada de lista chutada de memória: o que não
casar vira PkMn Trainer e sai no relatório, pra ser decidido a olho.
"""
import json
import os
import re
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "src/data/trainers_sinnoh.party")

# Classes de Sinnoh sem equivalente de nome idêntico no expansion.
# As marcadas com PROVISORIA usam o sprite de outra classe só pra rodar: Sinnoh
# tem classe que Hoenn e Kanto não têm, e sprite novo é arte a desenhar depois.
PROVISORIA = "PROVISORIA"
CLASS_ALIASES = {
    "ACE_TRAINER_MALE": "COOLTRAINER",
    "ACE_TRAINER_FEMALE": "COOLTRAINER_2",
    "ACE_TRAINER_SNOW_MALE": "COOLTRAINER",
    "ACE_TRAINER_SNOW_FEMALE": "COOLTRAINER_2",
    "SCHOOL_KID_MALE": "SCHOOL_KID",
    "SCHOOL_KID_FEMALE": "SCHOOL_KID",
    "SWIMMER_MALE": "SWIMMER_M",
    "SWIMMER_FEMALE": "SWIMMER_F",
    "TUBER_MALE": "TUBER_M",
    "TUBER_FEMALE": "TUBER_F",
    "PSYCHIC_MALE": "PSYCHIC",
    "PSYCHIC_FEMALE": "PSYCHIC",
    "RANGER_MALE": "PKMN_RANGER",
    "RANGER_FEMALE": "PKMN_RANGER",
    "POKEMON_RANGER_MALE": "PKMN_RANGER",
    "POKEMON_RANGER_FEMALE": "PKMN_RANGER",
    "BREEDER_MALE": "PKMN_BREEDER",
    "BREEDER_FEMALE": "PKMN_BREEDER",
    "SCIENTIST": "SCIENTIST_FRLG",
    "INTERVIEWERS": "INTERVIEWER",
    "GYM_LEADER": "LEADER",
    "ELITE_FOUR_MALE": "ELITE_FOUR",
    "ELITE_FOUR_FEMALE": "ELITE_FOUR",
    "DP_PLAYER_MALE": "RS_PROTAG",
    "DP_PLAYER_FEMALE": "RS_PROTAG",
    # Sem equivalente nenhum: sprite provisório, arte pendente.
    "GALACTIC_GRUNT_MALE": ("TEAM_MAGMA", PROVISORIA),
    "GALACTIC_GRUNT_FEMALE": ("TEAM_MAGMA", PROVISORIA),
    "GALACTIC_BOSS": ("MAGMA_LEADER", PROVISORIA),
    "COMMANDER_MARS": ("MAGMA_ADMIN", PROVISORIA),
    "COMMANDER_JUPITER": ("MAGMA_ADMIN", PROVISORIA),
    "COMMANDER_SATURN": ("MAGMA_ADMIN", PROVISORIA),
    "WORKER": ("HIKER", PROVISORIA),
    "VETERAN": ("EXPERT", PROVISORIA),
    "CLOWN": ("GUITARIST", PROVISORIA),
    "POKE_KID": ("LASS", PROVISORIA),
    "IDOL": ("BEAUTY", PROVISORIA),
    "CAMERAMAN": ("GENTLEMAN", PROVISORIA),
    "POLICEMAN": ("GENTLEMAN", PROVISORIA),
    "REPORTER": ("LADY", PROVISORIA),
    "SKIER_MALE": ("CAMPER", PROVISORIA),
    "SKIER_FEMALE": ("PICNICKER", PROVISORIA),
    "JOGGER": ("TRIATHLETE", PROVISORIA),
    "CYCLIST_MALE": ("TRIATHLETE", PROVISORIA),
    "CYCLIST_FEMALE": ("TRIATHLETE", PROVISORIA),
    "ARTIST": ("PAINTER_FRLG", PROVISORIA),
    "POKEFAN_MALE": "POKEFAN",
    "POKEFAN_FEMALE": "POKEFAN",
    "TOWER_TYCOON": "ARENA_TYCOON",
    "ARCADE_STAR": "ARENA_TYCOON",
    "CASTLE_VALET": "PALACE_MAVEN",
    "HALL_MATRON": "SALON_MAIDEN",
    "WAITER": ("GENTLEMAN", PROVISORIA),
    "WAITRESS": ("LADY", PROVISORIA),
    "MAID": ("LADY", PROVISORIA),
    "SOCIALITE": ("LADY", PROVISORIA),
    "COWGIRL": ("PICNICKER", PROVISORIA),
    "RANCHER": ("HIKER", PROVISORIA),
    "ROUGHNECK": ("CUE_BALL_FRLG", PROVISORIA),
    "PI": ("GENTLEMAN", PROVISORIA),
    "DOUBLE_TEAM": ("SIS_AND_BRO", PROVISORIA),
    "BELLE_AND_PA": ("OLD_COUPLE", PROVISORIA),
}

FEMALE_HINTS = ("FEMALE", "LADY", "GIRL", "BEAUTY", "LASS", "_F")


def read_constants(path, prefix):
    with open(os.path.join(REPO, path)) as f:
        return set(re.findall(rf"\b{prefix}[A-Z_0-9]+", f.read()))


def title(const):
    """TRAINER_CLASS_BUG_CATCHER -> Bug Catcher"""
    return " ".join(w.capitalize() for w in const.split("_"))


def iv_from_scale(scale):
    # Platinum guarda 0..255; o expansion quer 0..31 por stat.
    return min(31, scale * 31 // 255)


def convert(src_repo):
    data_dir = os.path.join(src_repo, "res/trainers/data")
    if not os.path.isdir(data_dir):
        sys.exit(f"não achei {data_dir}")

    classes = read_constants("include/constants/trainers.h", "TRAINER_CLASS_")
    pics = read_constants("include/constants/trainers.h", "TRAINER_PIC_")

    out = ["// Gerado por dev_scripts/import_sinnoh_trainers.py a partir de pret/pokeplatinum.",
           "// Times, níveis, golpes e falas iguais aos de Platinum. Não editar à mão:",
           "// rode o script de novo e as edições se perdem.\n"]
    unmapped = Counter()
    provisorias = Counter()
    count = 0

    for fname in sorted(os.listdir(data_dir)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(data_dir, fname), encoding="utf-8") as f:
            t = json.load(f)
        if not t.get("party"):
            continue

        raw = t.get("class", "").replace("TRAINER_CLASS_", "")
        cls = CLASS_ALIASES.get(raw, raw)
        if isinstance(cls, str) and f"TRAINER_CLASS_{cls}" not in classes:
            # LEADER_VOLKNER, ELITE_FOUR_FLINT, CHAMPION_CYNTHIA e afins: em
            # Platinum cada personagem tem classe própria, aqui usa-se a genérica.
            for base in ("LEADER", "ELITE_FOUR", "CHAMPION", "RIVAL"):
                if raw.startswith(base + "_"):
                    cls = base
                    break
        if isinstance(cls, tuple):
            cls, _ = cls
            provisorias[raw] += 1
        if f"TRAINER_CLASS_{cls}" not in classes:
            unmapped[raw] += 1
            cls = None

        slug = os.path.splitext(fname)[0].upper()
        out.append(f"=== TRAINER_SINNOH_{slug} ===")
        out.append(f"Name: {t.get('name', 'TRAINER')}")
        if cls:
            out.append(f"Class: {title(cls)}")
        pic = cls if cls and f"TRAINER_PIC_{cls}" in pics else "HIKER"
        out.append(f"Pic: {title(pic)}")
        gender = "Female" if any(h in raw for h in FEMALE_HINTS) else "Male"
        out.append(f"Gender: {gender}")
        items = [i.replace("ITEM_", "").replace("_", " ").title() for i in t.get("items") or []]
        if items:
            out.append(f"Items: {' / '.join(items)}")
        out.append(f"Double Battle: {'Yes' if t.get('double_battle') else 'No'}")
        out.append("")

        for mon in t["party"]:
            species = mon["species"].replace("SPECIES_", "").replace("_", " ").title()
            line = species
            if mon.get("item"):
                line += f" @ {mon['item'].replace('ITEM_', '').replace('_', ' ').title()}"
            out.append(line)
            out.append(f"Level: {mon['level']}")
            iv = iv_from_scale(mon.get("iv_scale", 0))
            out.append(f"IVs: {iv} HP / {iv} Atk / {iv} Def / {iv} SpA / {iv} SpD / {iv} Spe")
            for mv in mon.get("moves") or []:
                if mv and mv != "MOVE_NONE":
                    out.append(f"- {mv.replace('MOVE_', '').replace('_', ' ').title()}")
            out.append("")
        count += 1

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    print(f"{count} treinadores escritos em {os.path.relpath(OUT, REPO)}")
    if provisorias:
        print(f"\n{sum(provisorias.values())} treinadores usam sprite PROVISORIO "
              f"({len(provisorias)} classes que Sinnoh tem e o GBA não). Arte pendente:")
        for k, v in provisorias.most_common():
            print(f"  {k:38} {v:>4}")
    if unmapped:
        print(f"\n{sum(unmapped.values())} treinadores caíram em PkMn Trainer por classe sem "
              f"equivalente ({len(unmapped)} classes distintas):")
        for k, v in unmapped.most_common():
            print(f"  {k:38} {v:>4}")
    return count, unmapped


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "../fontes-mapas/pokeplatinum"
    convert(os.path.join(REPO, src) if not os.path.isabs(src) else src)
