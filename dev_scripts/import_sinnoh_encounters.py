#!/usr/bin/env python3
"""Converte as tabelas de encontro selvagem de Sinnoh (pokeplatinum) para o
formato de src/data/wild_encounters.json do pokeemerald-expansion.

Fontes: fontes-mapas/pokeplatinum/res/field/encounters/*.json (188 arquivos)
Mapas de destino: fontes-mapas/sinnoh/data/maps/<NomeDoMapa>/ (nomes de pasta)

O nome do mapa de destino (MAP_*, base_label) é derivado do nome da pasta em
sinnoh/data/maps, não inventado: convertemos CamelCase -> SCREAMING_SNAKE do
jeito que o pokeemerald-expansion já faz (ex.: pasta "AbandonedShip_HiddenFloor"
vira "MAP_ABANDONED_SHIP_HIDDEN_FLOOR", igual aos mapas de Hoenn existentes).

Regras de conversão:
- land_encounters (12 slots) -> land_mons, taxa = land_rate.
- surf_encounters (5 slots)  -> water_mons, taxa = surf_rate.
- old/good/super_rod_encounters (5 slots cada, 15 no total) -> fishing_mons,
  com "groups" próprios (old 0-4, good 5-9, super 10-14) porque o Platinum usa
  5 slots por vara, diferente do fixo 2/3/5 do Emerald. A taxa reportada em
  "encounter_rate" é a do old_rod_rate (ponytail: os três rods do Platinum têm
  taxa própria e o formato do expansion só aceita uma; ajustar depois se for
  preciso taxa por vara).
- Blocos com rate 0 (ou todos os slots SPECIES_NONE) são omitidos.
- Campos sem equivalente no expansion (day/night/radar/swarms/rate_form*/
  unown_table/ruby/sapphire/emerald/firered/leafgreen/map_category) são
  ignorados: são mecânicas do Platinum (Poké Radar, formas de Unown, DPPt
  version exclusives) sem campo correspondente no schema do expansion.
- rock_smash não existe nos dados do Platinum (não há campo de origem), então
  nenhum mapa gera rock_smash_mons.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = Path(
    "/Users/duarte/Documents/CLAUDE/Claude Workspace - Pokemon Rom Hacks/"
    "Pokemon Claude/fontes-mapas/pokeplatinum/res/field/encounters"
)
MAPS_DIR = Path(
    "/Users/duarte/Documents/CLAUDE/Claude Workspace - Pokemon Rom Hacks/"
    "Pokemon Claude/fontes-mapas/sinnoh/data/maps"
)
SPECIES_H = ROOT / "include/constants/species.h"
OUT_PATH = ROOT / "src/data/wild_encounters_sinnoh.json"

LAND_RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
WATER_RATES = [60, 30, 5, 4, 1]
FISHING_RATES = [30, 25, 15, 10, 10, 5, 2, 1, 1, 1, 30, 25, 15, 10, 10]


def normalizar(nome):
    """Remove tudo que não for letra/dígito e poe em minúsculas, pra casar
    nome de arquivo de origem com nome de pasta de mapa de destino."""
    return re.sub(r"[^a-z0-9]", "", nome.lower())


def camel_para_screaming_snake(segmento):
    """'TrickHouseCorridor' -> 'TRICK_HOUSE_CORRIDOR' (mesma regra que o
    expansion já usa nos MAP_* de Hoenn, ex. MAP_ROUTE110_TRICK_HOUSE_CORRIDOR)."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", segmento).upper()


def pasta_para_map_constant(nome_pasta):
    partes = nome_pasta.split("_")
    return "MAP_" + "_".join(camel_para_screaming_snake(p) for p in partes)


def carregar_especies_validas():
    texto = SPECIES_H.read_text(encoding="utf-8")
    return set(re.findall(r"SPECIES_[A-Z0-9_]+", texto))


def carregar_mapas_destino():
    """chave normalizada -> nome real da pasta."""
    mapas = {}
    for p in MAPS_DIR.iterdir():
        if p.is_dir():
            mapas[normalizar(p.name)] = p.name
    return mapas


def slot(min_lvl, max_lvl, especie, especies_validas, faltando):
    if especie not in especies_validas:
        faltando.add(especie)
    return {"min_level": min_lvl, "max_level": max_lvl, "species": especie}


def converter_arquivo(dados, especies_validas, faltando):
    """Devolve dict com land_mons/water_mons/fishing_mons (só os presentes)."""
    campos = {}

    if dados.get("land_rate") and dados.get("land_encounters"):
        mons = [
            slot(e["level"], e["level"], e["species"], especies_validas, faltando)
            for e in dados["land_encounters"]
        ]
        campos["land_mons"] = {"encounter_rate": dados["land_rate"], "mons": mons}

    if dados.get("surf_rate") and dados.get("surf_encounters"):
        surf = dados["surf_encounters"]
        if any(e["species"] != "SPECIES_NONE" for e in surf):
            mons = [
                slot(e["level_min"], e["level_max"], e["species"], especies_validas, faltando)
                for e in surf
            ]
            campos["water_mons"] = {"encounter_rate": dados["surf_rate"], "mons": mons}

    rods = []
    for chave in ("old_rod_encounters", "good_rod_encounters", "super_rod_encounters"):
        rods.extend(dados.get(chave) or [])
    if rods and any(e["species"] != "SPECIES_NONE" for e in rods):
        mons = [
            slot(e["level_min"], e["level_max"], e["species"], especies_validas, faltando)
            for e in rods
        ]
        campos["fishing_mons"] = {
            "encounter_rate": dados.get("old_rod_rate") or 0,
            "mons": mons,
        }

    return campos


def main():
    especies_validas = carregar_especies_validas()
    mapas_destino = carregar_mapas_destino()

    arquivos = sorted(SRC_DIR.glob("encounters_*.json"))
    convertidos = []
    nao_casaram = []
    faltando_especies = set()

    for arq in arquivos:
        stem = arq.stem[len("encounters_"):]
        chave = normalizar(stem)
        pasta = mapas_destino.get(chave)
        if pasta is None:
            nao_casaram.append(arq.name)
            continue

        dados = json.loads(arq.read_text(encoding="utf-8"))
        campos = converter_arquivo(dados, especies_validas, faltando_especies)
        if not campos:
            # mapa existe mas não tem nenhum encontro selvagem (ex.: cidade)
            continue

        entrada = {"map": pasta_para_map_constant(pasta), "base_label": f"g{pasta}"}
        entrada.update(campos)
        convertidos.append(entrada)

    saida = {
        "wild_encounter_groups": [
            {
                "label": "gSinnohWildMonHeaders",
                "for_maps": True,
                "fields": [
                    {"type": "land_mons", "encounter_rates": LAND_RATES},
                    {"type": "water_mons", "encounter_rates": WATER_RATES},
                    {
                        "type": "fishing_mons",
                        "encounter_rates": FISHING_RATES,
                        "groups": {
                            "old_rod": list(range(0, 5)),
                            "good_rod": list(range(5, 10)),
                            "super_rod": list(range(10, 15)),
                        },
                    },
                ],
                "encounters": convertidos,
            }
        ]
    }

    OUT_PATH.write_text(json.dumps(saida, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Arquivos de origem: {len(arquivos)}")
    print(f"Mapas convertidos (com encontros): {len(convertidos)}")
    print(f"Nao casaram com pasta de mapa ({len(nao_casaram)}):")
    for n in nao_casaram:
        print(f"  - {n}")
    print(f"Especies inexistentes em species.h ({len(faltando_especies)}):")
    for e in sorted(faltando_especies):
        print(f"  - {e}")


if __name__ == "__main__":
    main()
