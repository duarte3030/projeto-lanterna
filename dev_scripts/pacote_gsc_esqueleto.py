#!/usr/bin/env python3
"""Cria o ESQUELETO dos mapas NOVOS do pacote GS Chronicles (resposta 69 do Gui).

A arte de cada um vem depois, inteira, da `copia_cidade.py` (que só sabe
substituir um layout que JÁ existe, no lugar). Este arquivo só abre a vaga:
pasta do mapa, `map.json` com cabeçalho, `scripts.inc` vazio, layout novo no FIM
de `layouts.json` (id de layout é índice de save) e mapa novo no FIM do grupo
dele em `map_groups.json` (número de mapa dentro do grupo também é).

    mapa novo                    fonte (GS Chronicles)   grupo
    VioletCity_Gym_2F            g6m2  13x20             IndoorViolet_Johto
    GoldenrodCity_RadioPlaza     g3m66 28x30             TownsAndRoutes_Johto
    Route36_Clearing             g1m36 22x22             TownsAndRoutes_Johto
    Route42_Clearing             g12m1 64x32             TownsAndRoutes_Johto

Idempotente: o que já existe não é tocado. O `map.bin` provisório é todo
metatile 0; a `copia_cidade.py --aplicar` troca pelo do autor.

Uso:
    python3 dev_scripts/pacote_gsc_esqueleto.py
"""
import json
import os
import struct

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NOVOS = [
    dict(nome="VioletCity_Gym_2F", id="MAP_VIOLET_CITY_GYM_2F", w=13, h=20,
         grupo="gMapGroup_IndoorViolet_Johto", musica="MUS_HG_GYM",
         secao="MAPSEC_VIOLET_CITY", popup="VIOLET CITY", tipo="MAP_TYPE_INDOOR",
         fora=False, molde="VioletCity_Gym"),
    dict(nome="GoldenrodCity_RadioPlaza", id="MAP_GOLDENROD_CITY_RADIO_PLAZA", w=28, h=30,
         grupo="gMapGroup_TownsAndRoutes_Johto", musica="MUS_HG_GOLDENROD",
         secao="MAPSEC_GOLDENROD_CITY", popup="GOLDENROD CITY", tipo="MAP_TYPE_CITY",
         fora=True, molde="GoldenrodCity"),
    dict(nome="Route36_Clearing", id="MAP_ROUTE36_CLEARING", w=22, h=22,
         grupo="gMapGroup_TownsAndRoutes_Johto", musica="MUS_HG_ROUTE34",
         secao="MAPSEC_ROUTE_36", popup="ROUTE 36", tipo="MAP_TYPE_ROUTE",
         fora=True, molde="Route36"),
    dict(nome="Route42_Clearing", id="MAP_ROUTE42_CLEARING", w=64, h=32,
         grupo="gMapGroup_TownsAndRoutes_Johto", musica="MUS_HG_ROUTE42",
         secao="MAPSEC_ROUTE_42", popup="ROUTE 42", tipo="MAP_TYPE_ROUTE",
         fora=True, molde="Route42"),
]


def layout_id(nome):
    s = ""
    for i, c in enumerate(nome.replace("_", "")):
        if c.isupper() and i and (s[-1:].islower() or s[-1:].isdigit()):
            s += "_"
        elif c.isdigit() and i and s[-1:].isalpha():
            s += "_"
        s += c.upper()
    return "LAYOUT_" + s


def main():
    caminho_lay = os.path.join(REPO, "data/layouts/layouts.json")
    lay = json.load(open(caminho_lay, encoding="utf-8"))
    caminho_grp = os.path.join(REPO, "data/maps/map_groups.json")
    grp = json.load(open(caminho_grp, encoding="utf-8"))
    ids = {L["id"] for L in lay["layouts"] if "id" in L}
    for m in NOVOS:
        lid = m.get("layout") or ("LAYOUT_" + m["id"][4:])
        pasta_lay = os.path.join(REPO, "data/layouts", m["nome"])
        if lid not in ids:
            os.makedirs(pasta_lay, exist_ok=True)
            with open(os.path.join(pasta_lay, "map.bin"), "wb") as f:
                f.write(struct.pack("<H", 0) * (m["w"] * m["h"]))
            with open(os.path.join(pasta_lay, "border.bin"), "wb") as f:
                f.write(struct.pack("<H", 0) * 4)
            molde = json.load(open(os.path.join(REPO, "data/maps", m["molde"], "map.json")))
            lm = next(L for L in lay["layouts"] if L.get("id") == molde["layout"])
            lay["layouts"].append({
                "id": lid, "name": m["nome"] + "_Layout", "width": m["w"], "height": m["h"],
                "primary_tileset": lm["primary_tileset"], "secondary_tileset": lm["secondary_tileset"],
                "border_filepath": "data/layouts/%s/border.bin" % m["nome"],
                "blockdata_filepath": "data/layouts/%s/map.bin" % m["nome"],
                "layout_version": "johto"})
            print("layout novo:", lid)
        pasta = os.path.join(REPO, "data/maps", m["nome"])
        if not os.path.isfile(os.path.join(pasta, "map.json")):
            os.makedirs(pasta, exist_ok=True)
            mj = {
                "id": m["id"], "name": m["nome"], "layout": lid, "music": m["musica"],
                "region_map_section": m["secao"], "map_name_popup": m["popup"],
                "requires_flash": False, "weather": "WEATHER_NONE", "map_type": m["tipo"],
                "allow_cycling": m["fora"], "allow_escaping": False, "allow_running": m["fora"],
                "show_map_name": m["tipo"] == "MAP_TYPE_ROUTE",
                "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": 0,
                "object_events": [], "warp_events": [], "coord_events": [], "bg_events": [],
            }
            with open(os.path.join(pasta, "map.json"), "w", encoding="utf-8") as f:
                json.dump(mj, f, indent=2, ensure_ascii=False)
                f.write("\n")
            with open(os.path.join(pasta, "scripts.inc"), "w", encoding="utf-8") as f:
                f.write("%s_MapScripts::\n\t.byte 0\n" % m["nome"])
            print("mapa novo:", m["id"])
        if m["nome"] not in grp[m["grupo"]]:
            grp[m["grupo"]].append(m["nome"])
    with open(caminho_lay, "w", encoding="utf-8") as f:
        json.dump(lay, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(caminho_grp, "w", encoding="utf-8") as f:
        json.dump(grp, f, indent=2, ensure_ascii=False)
        f.write("\n")
    # event_scripts.s: um .include por mapa novo, no fim da lista de mapas
    caminho_ev = os.path.join(REPO, "data/event_scripts.s")
    ev = open(caminho_ev, encoding="utf-8").read()
    for m in NOVOS:
        linha = '\t.include "data/maps/%s/scripts.inc"\n' % m["nome"]
        if linha not in ev:
            ancora = '\t.include "data/maps/GoldenrodCity_UndergroundWarehouse/scripts.inc"\n'
            if ancora not in ev:
                raise SystemExit("ERRO: âncora do event_scripts.s sumiu")
            ev = ev.replace(ancora, ancora + linha, 1)
            ancora_nova = linha
    open(caminho_ev, "w", encoding="utf-8").write(ev)


if __name__ == "__main__":
    main()
