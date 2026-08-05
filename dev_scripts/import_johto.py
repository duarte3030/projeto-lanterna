import json
import os
import shutil

HNS_DIR = "/Users/duarte/Projetos/pokemon-claude/fontes-mapas/hns"
DEST_DIR = "/Users/duarte/Projetos/pokemon-claude/pokeemerald-expansion"

JOHTO_TOWNS_ROUTES = [
    "NewBarkTown", "CherrygroveCity", "VioletCity", "AzaleaTown", "GoldenrodCity",
    "EcruteakCity", "OlivineCity", "CianwoodCity", "Mahoganytown", "BlackthornCity",
    "SafariZoneGate", "LakeOfRage", "LakeOfRageLowTide", "BellchimeTrail",
    "NationalPark_Normal", "NationalPark_BugContest", "RuinsOfAlph_Outside",
    "MtSilver_Outside", "MtSilver_Snow", "MtSilver_SummitDay", "MtSilver_SummitNight",
    "Route26", "Route26North", "Route26_House1", "Route26_House2",
    "Route27", "Route27_House", "Route28", "Route28_House",
    "Route29", "Route30", "Route30_House", "Route30_MrPokemonsHouse",
    "Route31", "Route32", "Route32_PokemonCenter", "Route33", "Route34", "Route34_DayCare",
    "Route35", "Route36", "Route37", "Route38", "Route39", "Route39_Barn", "Route39_FarmHouse",
    "Route40", "Route41", "Route42", "Route43", "Route44", "Route45", "Route46", "Route47", "Route48",
    "ReceptionGate", "WorldHub", "WorldHub2"
]

JOHTO_GROUPS_TO_IMPORT = [
    "gMapGroup_IndoorNewBark", "gMapGroup_IndoorCherrygrove", "gMapGroup_IndoorViolet",
    "gMapGroup_IndoorAzalea", "gMapGroup_IndoorGoldenrod", "gMapGroup_IndoorEcruteak",
    "gMapGroup_IndoorOlivine", "gMapGroup_IndoorCianwood", "gMapGroup_IndoorMahogany",
    "gMapGroup_IndoorBlackthorn", "gMapGroup_IndoorJohtoRoutes"
]

JOHTO_DUNGEONS_PREFIXES = [
    "SproutTower_", "BurnedTower_", "TinTower_", "WhirlIslands_", "MtMortar_",
    "IcePath_", "DarkCave_", "SlowpokeWell_", "IlexForest", "RuinsOfAlph_",
    "TohjoFalls_", "MtSilver_", "DragonsDen_", "SSAqua_", "EmbeddedTower",
    "UnionCave_", "CliffEdgeCave", "CliffEdgeGate", "DiglettsCave_", "SafariZoneGate_"
]

def main():
    print("--- Reconstruindo Registro de Johto em map_groups.json ---")
    
    with open(os.path.join(HNS_DIR, "data/maps/map_groups.json"), "r", encoding="utf-8") as f:
        hns_groups = json.load(f)
        
    with open(os.path.join(HNS_DIR, "data/layouts/layouts.json"), "r", encoding="utf-8") as f:
        hns_layouts = json.load(f)
        
    with open(os.path.join(DEST_DIR, "data/maps/map_groups.json"), "r", encoding="utf-8") as f:
        dest_groups = json.load(f)

    with open(os.path.join(DEST_DIR, "data/layouts/layouts.json"), "r", encoding="utf-8") as f:
        dest_layouts = json.load(f)

    dest_layout_ids = {l["id"]: l for l in dest_layouts["layouts"]}
    
    maps_to_copy = set(JOHTO_TOWNS_ROUTES)
    for group_name in JOHTO_GROUPS_TO_IMPORT:
        if group_name in hns_groups:
            maps_to_copy.update(hns_groups[group_name])

    for m in hns_groups.get("gMapGroup_Dungeons", []):
        if any(m.startswith(p) for p in JOHTO_DUNGEONS_PREFIXES):
            maps_to_copy.add(m)

    for map_name in maps_to_copy:
        src_map_dir = os.path.join(HNS_DIR, f"data/maps/{map_name}")
        dst_map_dir = os.path.join(DEST_DIR, f"data/maps/{map_name}")
        if os.path.exists(src_map_dir):
            if os.path.exists(dst_map_dir):
                shutil.rmtree(dst_map_dir)
            shutil.copytree(src_map_dir, dst_map_dir)
            
            map_json_path = os.path.join(dst_map_dir, "map.json")
            if os.path.exists(map_json_path):
                with open(map_json_path, "r", encoding="utf-8") as mj:
                    map_data = json.load(mj)
                layout_id = map_data.get("layout")
                if layout_id:
                    for l in hns_layouts["layouts"]:
                        if l["id"] == layout_id:
                            if l["id"] not in dest_layout_ids:
                                dest_layouts["layouts"].append(l)
                                dest_layout_ids[l["id"]] = l
                            border_fp = l.get("border_filepath")
                            if border_fp:
                                src_border = os.path.join(HNS_DIR, border_fp)
                                dst_border = os.path.join(DEST_DIR, border_fp)
                                os.makedirs(os.path.dirname(dst_border), exist_ok=True)
                                if os.path.exists(src_border):
                                    shutil.copy2(src_border, dst_border)
                            block_fp = l.get("blockdata_filepath")
                            if block_fp:
                                src_block = os.path.join(HNS_DIR, block_fp)
                                dst_block = os.path.join(DEST_DIR, block_fp)
                                os.makedirs(os.path.dirname(dst_block), exist_ok=True)
                                if os.path.exists(src_block):
                                    shutil.copy2(src_block, dst_block)

    with open(os.path.join(DEST_DIR, "data/layouts/layouts.json"), "w", encoding="utf-8") as f:
        json.dump(dest_layouts, f, indent=2)

    johto_group_names = ["gMapGroup_TownsAndRoutes_Johto", "gMapGroup_Dungeons_Johto"] + [f"{g}_Johto" for g in JOHTO_GROUPS_TO_IMPORT]
    
    dest_groups["group_order"] = [g for g in dest_groups["group_order"] if g not in johto_group_names]
    for jg in johto_group_names:
        if jg in dest_groups:
            del dest_groups[jg]

    existing_maps_set = set()
    for g in dest_groups["group_order"]:
        if g in dest_groups:
            existing_maps_set.update(dest_groups[g])

    dest_groups["group_order"].append("gMapGroup_TownsAndRoutes_Johto")
    dest_groups["gMapGroup_TownsAndRoutes_Johto"] = []
    for m in JOHTO_TOWNS_ROUTES:
        if m not in existing_maps_set and os.path.exists(os.path.join(DEST_DIR, f"data/maps/{m}")):
            dest_groups["gMapGroup_TownsAndRoutes_Johto"].append(m)
            existing_maps_set.add(m)

    for g_name in JOHTO_GROUPS_TO_IMPORT:
        new_g_name = f"{g_name}_Johto"
        dest_groups["group_order"].append(new_g_name)
        dest_groups[new_g_name] = []
        if g_name in hns_groups:
            for m in hns_groups[g_name]:
                if m not in existing_maps_set and os.path.exists(os.path.join(DEST_DIR, f"data/maps/{m}")):
                    dest_groups[new_g_name].append(m)
                    existing_maps_set.add(m)

    dest_groups["group_order"].append("gMapGroup_Dungeons_Johto")
    dest_groups["gMapGroup_Dungeons_Johto"] = []
    for m in hns_groups.get("gMapGroup_Dungeons", []):
        if any(m.startswith(p) for p in JOHTO_DUNGEONS_PREFIXES):
            if m not in existing_maps_set and os.path.exists(os.path.join(DEST_DIR, f"data/maps/{m}")):
                dest_groups["gMapGroup_Dungeons_Johto"].append(m)
                existing_maps_set.add(m)

    with open(os.path.join(DEST_DIR, "data/maps/map_groups.json"), "w", encoding="utf-8") as f:
        json.dump(dest_groups, f, indent=2)

    print("Importação e atualização de Johto concluídas com sucesso!")

if __name__ == "__main__":
    main()
