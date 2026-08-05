#!/usr/bin/env python3
"""Confere e conserta os mapas de Sinnoh povoados por agentes.

Uso:
    python3 dev_scripts/valida_mapas_sinnoh.py            # so relata
    python3 dev_scripts/valida_mapas_sinnoh.py --corrigir # relata e conserta

Checa quatro coisas que já quebraram o build antes:
1. sprite (`graphics_id`) que esta build não consegue desenhar, ou seja, que
   não tem entrada em object_event_graphics_info_pointers.h fora de `#if IS_FRLG`
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
    "SinnohLeague", "GalacticHQ", "TeamGalacticEternaBuilding",
)

# Os 8 ginásios de Johto usam o mesmo padrão e passam pelas mesmas checagens.
GINASIOS_JOHTO = (
    "VioletCity_Gym", "AzaleaTown_Gym", "GoldenrodCity_Gym", "EcruteakCity_Gym",
    "OlivineCity_Gym", "CianwoodGym", "MahoganyTown_Gym", "BlackthornCity_Gym",
)

# Trocas conhecidas: sprite que Sinnoh usa e o GBA não tem.
TROCA_SPRITE = {
    "OBJ_EVENT_GFX_ACE_TRAINER_F": "OBJ_EVENT_GFX_PICNICKER",
    "OBJ_EVENT_GFX_ACE_TRAINER_M": "OBJ_EVENT_GFX_CAMPER",
    "OBJ_EVENT_GFX_POKEMON_BREEDER_F": "OBJ_EVENT_GFX_POKEFAN_F",
    "OBJ_EVENT_GFX_POKEMON_BREEDER_M": "OBJ_EVENT_GFX_POKEFAN_M",
    "OBJ_EVENT_GFX_BATTLE_GIRL": "OBJ_EVENT_GFX_WOMAN_3",
    "OBJ_EVENT_GFX_SCHOOL_KID_F": "OBJ_EVENT_GFX_SCHOOL_KID_M",
    "OBJ_EVENT_GFX_BARRY": "OBJ_EVENT_GFX_RICH_BOY",
    "OBJ_EVENT_GFX_PROF_ROWAN": "OBJ_EVENT_GFX_PROF_BIRCH",
    "OBJ_EVENT_GFX_GRUNT_M": "OBJ_EVENT_GFX_MAGMA_MEMBER_M",
    "OBJ_EVENT_GFX_GRUNT_F": "OBJ_EVENT_GFX_MAGMA_MEMBER_F",
    "OBJ_EVENT_GFX_WORKER": "OBJ_EVENT_GFX_MAN_4",
    "OBJ_EVENT_GFX_GUITARIST": "OBJ_EVENT_GFX_MAN_3",
    "OBJ_EVENT_GFX_KID_WITH_NDS": "OBJ_EVENT_GFX_GAMEBOY_KID",
    "OBJ_EVENT_GFX_VETERAN": "OBJ_EVENT_GFX_EXPERT_M",
    "OBJ_EVENT_GFX_CLOWN": "OBJ_EVENT_GFX_MAN_3",
    "OBJ_EVENT_GFX_IDOL": "OBJ_EVENT_GFX_BEAUTY",
    "OBJ_EVENT_GFX_CAMERAMAN": "OBJ_EVENT_GFX_GENTLEMAN",
    "OBJ_EVENT_GFX_POLICEMAN": "OBJ_EVENT_GFX_GENTLEMAN",
    "OBJ_EVENT_GFX_REPORTER": "OBJ_EVENT_GFX_WOMAN_2",
    "OBJ_EVENT_GFX_SKIER_M": "OBJ_EVENT_GFX_CAMPER",
    "OBJ_EVENT_GFX_SKIER_F": "OBJ_EVENT_GFX_PICNICKER",
    "OBJ_EVENT_GFX_CYCLIST_M": "OBJ_EVENT_GFX_CYCLING_TRIATHLETE_M",
    "OBJ_EVENT_GFX_CYCLIST_F": "OBJ_EVENT_GFX_CYCLING_TRIATHLETE_F",
}
SPRITE_PADRAO = "OBJ_EVENT_GFX_MAN_1"
MOVIMENTO_PADRAO = "MOVEMENT_TYPE_LOOK_AROUND"

# ponytail: quem atende balcao FICA em tile bloqueado, de proposito, como no jogo
# original. Enfermeira e vendedor sao avisados, nunca movidos.
ATRAS_DO_BALCAO = ("NURSE", "CLERK", "MART", "RECEP", "ATENDENTE", "CASHIER", "SHOPKEEPER")


def constantes(caminho, prefixo):
    texto = open(os.path.join(REPO, caminho)).read()
    return set(re.findall(rf"\b{prefixo}[A-Z_0-9]+", texto))


def sprites_utilizaveis():
    """Sprites que esta build realmente consegue desenhar.

    Conferir contra constants/event_objects.h NÃO basta, e essa foi a falha que
    deixou o mesmo crash voltar duas vezes: a constante existe sempre, mas o
    gráfico, o pic table, o GraphicsInfo e a entrada na tabela de ponteiros só
    existem dentro de `#if IS_FRLG`. Numa build Emerald o id aponta para o vazio,
    NPC parado sobrevive e NPC que anda reinicia o jogo na tela de título. O
    validador passava limpo porque olhava o header errado.

    Verdade de verdade: as entradas de object_event_graphics_info_pointers.h que
    ficam FORA de um bloco `#if IS_FRLG`.
    """
    caminho = "src/data/object_events/object_event_graphics_info_pointers.h"
    dentro_frlg, fora_frlg = set(), set()
    profundidade, dentro, nivel = 0, False, 0
    for linha in open(os.path.join(REPO, caminho)):
        s = linha.strip()
        if s.startswith("#if"):
            profundidade += 1
            if "IS_FRLG" in s and not s.startswith("#if !"):
                dentro, nivel = True, profundidade
        elif s.startswith("#endif"):
            if dentro and profundidade == nivel:
                dentro = False
            profundidade -= 1
        achado = re.search(r"\[(OBJ_EVENT_GFX_[A-Z0-9_]+)\]", s)
        if achado:
            (dentro_frlg if dentro else fora_frlg).add(achado.group(1))

    # OBJ_EVENT_GFX_VAR_0 a VAR_F são falso positivo: o jogo os resolve em tempo
    # de execução (src/decoration.c, src/secret_base.c), nunca por esta tabela.
    return fora_frlg | {f"OBJ_EVENT_GFX_VAR_{d}" for d in "0123456789ABCDEF"}


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


_GLOBAIS = None


def rotulos_globais():
    """Rótulos de script que valem em qualquer mapa (empurrar pedra, quebrar rocha).

    Sem isto o validador acusa EventScript_StrengthBoulder como inexistente, que
    é falso: ele mora em data/scripts/field_move_scripts.inc.
    """
    global _GLOBAIS
    if _GLOBAIS is None:
        partes = []
        pasta = os.path.join(REPO, "data/scripts")
        for f in sorted(os.listdir(pasta)):
            if f.endswith(".inc"):
                partes.append(open(os.path.join(pasta, f), errors="replace").read())
        partes.append(open(os.path.join(REPO, "data/event_scripts.s"), errors="replace").read())
        _GLOBAIS = "\n".join(partes)
    return _GLOBAIS


def confere_tabela_de_trocas(sprites):
    """Impede que a própria tabela replante o bug.

    Em 04/08/2026 cinco destinos daqui (COOLTRAINER_F, COOLTRAINER_M, CRUSH_GIRL,
    WORKER_M, GBA_KID) só existiam dentro de `#if IS_FRLG`, então rodar
    --corrigir PLANTAVA o crash em vez de tirar. Foi assim que 82 objetos em 44
    mapas voltaram depois de já terem sido consertados uma vez.
    """
    ruins = sorted(d for d in TROCA_SPRITE.values() if d not in sprites)
    if ruins:
        print("ABORTADO: TROCA_SPRITE aponta para sprite que esta build não desenha:")
        for d in ruins:
            print("  ", d)
        sys.exit(1)


def main():
    sprites = sprites_utilizaveis()
    confere_tabela_de_trocas(sprites)
    movimentos = constantes("include/constants/event_object_movement.h", "MOVEMENT_TYPE_")
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}

    total = {"sprite": 0, "movimento": 0, "bloqueado": 0, "fora": 0, "script": 0}
    mapas_tocados = 0

    base = os.path.join(REPO, "data/maps")
    for nome in sorted(os.listdir(base)):
        # ponytail: "_Frlg" e mapa de Kanto que casa com o prefixo Route2 sem ser de Sinnoh
        # ponytail: ate 05/08/2026 isto so olhava prefixo de Sinnoh (mais os 8
        # ginasios de Johto), entao os 103 mapas de Johto e os 17 da Galactica
        # nunca foram verificados por ninguem. Agora varre TUDO que nao seja de
        # FRLG; --so-sinnoh volta ao comportamento antigo.
        if nome.endswith("_Frlg"):
            continue
        if "--so-sinnoh" in sys.argv and not (
                any(nome.startswith(p) for p in PREFIXOS_SINNOH) or nome in GINASIOS_JOHTO):
            continue
        caminho = os.path.join(base, nome, "map.json")
        if not os.path.exists(caminho):
            continue
        d = json.load(open(caminho))
        objs = d.get("object_events", [])
        if not objs:
            continue
        alterou = False
        caminho_scripts = os.path.join(base, nome, "scripts.inc")
        if not os.path.exists(caminho_scripts):
            print(f"  {nome}: sem scripts.inc, mas o map.json tem objeto")
            total["script"] += len(objs)
            continue
        scripts_txt = open(caminho_scripts).read() + rotulos_globais()

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
