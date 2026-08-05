#!/usr/bin/env python3
"""Confere e conserta os mapas de Sinnoh povoados por agentes.

Uso:
    python3 dev_scripts/valida_mapas_sinnoh.py            # so relata
    python3 dev_scripts/valida_mapas_sinnoh.py --corrigir # relata e conserta

Checa quatro coisas que já quebraram o build antes:
1. sprite (`graphics_id`) que não existe em constants/event_objects.h
2. tipo de movimento que não existe em constants/event_object_movement.h
3. script citado no map.json sem rótulo correspondente no scripts.inc
4. NPC em cima de tile com colisão, ou fora do mapa

Com --corrigir, troca sprite e movimento inexistentes por equivalente real e
move NPC bloqueado para o tile livre mais próximo. Script faltando NÃO se
conserta sozinho: vira relatório, porque inventar diálogo é decisão humana.
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORRIGIR = "--corrigir" in sys.argv

PREFIXOS_SINNOH = (
    "Twinleaf", "Sandgem", "Jubilife", "Oreburgh", "Floaroma", "Eterna", "Hearthome",
    "Solaceon", "Veilstone", "Pastoria", "Celestic", "Canalave", "Snowpoint", "Sunyshore",
    "Fight", "Survival", "Resort", "MtCoronet", "Lake", "Spear", "Valley", "GreatMarsh",
    "Ravaged", "Wayward", "Iron", "Acuity", "Verity", "Hotel", "Pokmon", "Route2",
)

# Trocas conhecidas: sprite que Sinnoh usa e o GBA não tem.
TROCA_SPRITE = {
    "OBJ_EVENT_GFX_ACE_TRAINER_F": "OBJ_EVENT_GFX_COOLTRAINER_F",
    "OBJ_EVENT_GFX_ACE_TRAINER_M": "OBJ_EVENT_GFX_COOLTRAINER_M",
    "OBJ_EVENT_GFX_POKEMON_BREEDER_F": "OBJ_EVENT_GFX_POKEFAN_F",
    "OBJ_EVENT_GFX_POKEMON_BREEDER_M": "OBJ_EVENT_GFX_POKEFAN_M",
    "OBJ_EVENT_GFX_BATTLE_GIRL": "OBJ_EVENT_GFX_CRUSH_GIRL",
    "OBJ_EVENT_GFX_SCHOOL_KID_F": "OBJ_EVENT_GFX_SCHOOL_KID_M",
    "OBJ_EVENT_GFX_BARRY": "OBJ_EVENT_GFX_RICH_BOY",
    "OBJ_EVENT_GFX_PROF_ROWAN": "OBJ_EVENT_GFX_PROF_BIRCH",
    "OBJ_EVENT_GFX_GRUNT_M": "OBJ_EVENT_GFX_MAGMA_MEMBER_M",
    "OBJ_EVENT_GFX_GRUNT_F": "OBJ_EVENT_GFX_MAGMA_MEMBER_F",
    "OBJ_EVENT_GFX_WORKER": "OBJ_EVENT_GFX_WORKER_M",
    "OBJ_EVENT_GFX_GUITARIST": "OBJ_EVENT_GFX_MAN_3",
    "OBJ_EVENT_GFX_KID_WITH_NDS": "OBJ_EVENT_GFX_GBA_KID",
    "OBJ_EVENT_GFX_VETERAN": "OBJ_EVENT_GFX_EXPERT_M",
    "OBJ_EVENT_GFX_CLOWN": "OBJ_EVENT_GFX_MAN_3",
    "OBJ_EVENT_GFX_IDOL": "OBJ_EVENT_GFX_BEAUTY",
    "OBJ_EVENT_GFX_CAMERAMAN": "OBJ_EVENT_GFX_GENTLEMAN",
    "OBJ_EVENT_GFX_POLICEMAN": "OBJ_EVENT_GFX_GENTLEMAN",
    "OBJ_EVENT_GFX_REPORTER": "OBJ_EVENT_GFX_WOMAN_2",
    "OBJ_EVENT_GFX_SKIER_M": "OBJ_EVENT_GFX_CAMPER",
    "OBJ_EVENT_GFX_SKIER_F": "OBJ_EVENT_GFX_PICNICKER",
    "OBJ_EVENT_GFX_CYCLIST_M": "OBJ_EVENT_GFX_TRIATHLETE_M",
    "OBJ_EVENT_GFX_CYCLIST_F": "OBJ_EVENT_GFX_TRIATHLETE_F",
}
SPRITE_PADRAO = "OBJ_EVENT_GFX_MAN_1"
MOVIMENTO_PADRAO = "MOVEMENT_TYPE_LOOK_AROUND"

# ponytail: quem atende balcao FICA em tile bloqueado, de proposito, como no jogo
# original. Enfermeira e vendedor sao avisados, nunca movidos.
ATRAS_DO_BALCAO = ("NURSE", "CLERK", "MART", "RECEP", "ATENDENTE", "CASHIER", "SHOPKEEPER")


def constantes(caminho, prefixo):
    texto = open(os.path.join(REPO, caminho)).read()
    return set(re.findall(rf"\b{prefixo}[A-Z_0-9]+", texto))


def colisao(layouts, layout_id, x, y):
    """0 = andável. None = fora do mapa."""
    L = layouts[layout_id]
    largura, altura = L["width"], L["height"]
    if not (0 <= x < largura and 0 <= y < altura):
        return None
    with open(os.path.join(REPO, L["blockdata_filepath"]), "rb") as f:
        f.seek((y * largura + x) * 2)
        dados = f.read(2)
    if len(dados) < 2:
        return None
    return (struct.unpack("<H", dados)[0] >> 10) & 0x3


def tile_livre_perto(layouts, layout_id, x, y, raio=6):
    for r in range(1, raio + 1):
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                if max(abs(dx), abs(dy)) != r:
                    continue
                if colisao(layouts, layout_id, x + dx, y + dy) == 0:
                    return x + dx, y + dy
    return None


def main():
    sprites = constantes("include/constants/event_objects.h", "OBJ_EVENT_GFX_")
    movimentos = constantes("include/constants/event_object_movement.h", "MOVEMENT_TYPE_")
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}

    total = {"sprite": 0, "movimento": 0, "bloqueado": 0, "fora": 0, "script": 0}
    mapas_tocados = 0

    base = os.path.join(REPO, "data/maps")
    for nome in sorted(os.listdir(base)):
        # ponytail: "_Frlg" e mapa de Kanto que casa com o prefixo Route2 sem ser de Sinnoh
        if nome.endswith("_Frlg") or not any(nome.startswith(p) for p in PREFIXOS_SINNOH):
            continue
        caminho = os.path.join(base, nome, "map.json")
        if not os.path.exists(caminho):
            continue
        d = json.load(open(caminho))
        objs = d.get("object_events", [])
        if not objs:
            continue
        alterou = False
        scripts_txt = open(os.path.join(base, nome, "scripts.inc")).read()

        for o in objs:
            if o.get("graphics_id", SPRITE_PADRAO) not in sprites:
                total["sprite"] += 1
                novo = TROCA_SPRITE.get(o.get("graphics_id"), SPRITE_PADRAO)
                print(f"  {nome}: sprite {o.get('graphics_id')} -> {novo}")
                if CORRIGIR:
                    o["graphics_id"] = novo
                    alterou = True
            if o.get("movement_type", MOVIMENTO_PADRAO) not in movimentos:
                total["movimento"] += 1
                print(f"  {nome}: movimento {o.get('movement_type')} -> {MOVIMENTO_PADRAO}")
                if CORRIGIR:
                    o["movement_type"] = MOVIMENTO_PADRAO
                    alterou = True
            if "x" not in o or "y" not in o:
                continue
            c = colisao(layouts, d["layout"], o["x"], o["y"])
            if c is None:
                total["fora"] += 1
                print(f"  {nome}: {o.get('local_id','?')} FORA do mapa em ({o['x']},{o['y']})")
            elif c != 0:
                total["bloqueado"] += 1
                balcao = any(t in o.get("local_id", "") for t in ATRAS_DO_BALCAO)
                novo = None if balcao else tile_livre_perto(layouts, d["layout"], o["x"], o["y"])
                if balcao:
                    print(f"  {nome}: {o.get('local_id','?')} em tile bloqueado, mas atende balcao: mantido")
                else:
                    print(f"  {nome}: {o.get('local_id','?')} bloqueado em ({o['x']},{o['y']}) -> {novo}")
                if CORRIGIR and novo:
                    o["x"], o["y"] = novo
                    alterou = True

        for ev in objs + d.get("bg_events", []):
            if ev.get("script") and ev["script"] not in ("0", "NULL") and ev["script"] + "::" not in scripts_txt:
                total["script"] += 1
                print(f"  {nome}: script {ev['script']} NAO existe no scripts.inc")

        if alterou:
            json.dump(d, open(caminho, "w"), indent=2, ensure_ascii=False)
            mapas_tocados += 1

    print("\nresumo:", total)
    print("mapas corrigidos:" if CORRIGIR else "mapas com problema:", mapas_tocados)
    return 1 if total["script"] or total["fora"] else 0


if __name__ == "__main__":
    sys.exit(main())
