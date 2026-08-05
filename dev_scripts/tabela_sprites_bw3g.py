#!/usr/bin/env python3
"""Tabela de tradução BW3G (pokecrystal) -> pokeemerald-expansion desta build.

Todo valor de destino foi conferido em:
  - include/constants/event_objects.h                        (constante existe)
  - src/data/object_events/object_event_graphics_info_pointers.h
    (o sprite é realmente desenhado FORA do bloco `#if IS_FRLG`)
  - include/constants/event_object_movement.h
  - include/constants/songs.h

Esta build é Emerald (Makefile: GAME_VERSION ?= EMERALD -> IS_FRLG 0), portanto
NENHUM `OBJ_EVENT_GFX_*` de dentro do `#if IS_FRLG` pode ser usado: ele existe no
enum mas não tem entrada na tabela de gráficos e derruba o jogo. Por isso não
aparecem aqui nomes "óbvios" como OBJ_EVENT_GFX_CLERK, OBJ_EVENT_GFX_GYM_GUY,
OBJ_EVENT_GFX_SCIENTIST, OBJ_EVENT_GFX_BIKER, OBJ_EVENT_GFX_ROCKER,
OBJ_EVENT_GFX_LANCE, OBJ_EVENT_GFX_PROF_OAK, OBJ_EVENT_GFX_JIGGLYPUFF,
OBJ_EVENT_GFX_POLICEMAN, OBJ_EVENT_GFX_COOLTRAINER_M/F: todos são FRLG.

Rode `python3 dev_scripts/tabela_sprites_bw3g.py` para revalidar.
"""

# SPRITE_* do BW3G -> OBJ_EVENT_GFX_* seguro nesta build.
SPRITE = {
    # --- protagonistas, rivais e figuras de história -------------------------
    "SPRITE_HILBERT": "OBJ_EVENT_GFX_BRENDAN_NORMAL",
    "SPRITE_HILDA": "OBJ_EVENT_GFX_MAY_NORMAL",
    "SPRITE_NATE": "OBJ_EVENT_GFX_RED",
    "SPRITE_ROSA": "OBJ_EVENT_GFX_LEAF",
    "SPRITE_CHRIS": "OBJ_EVENT_GFX_LINK_RS_BRENDAN",
    "SPRITE_CHEREN": "OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL",
    "SPRITE_BIANCA": "OBJ_EVENT_GFX_RIVAL_MAY_NORMAL",
    "SPRITE_HUGH": "OBJ_EVENT_GFX_WALLY",
    "SPRITE_N": "OBJ_EVENT_GFX_STEVEN",
    "SPRITE_MOM": "OBJ_EVENT_GFX_MOM",
    "SPRITE_REDS_MOM": "OBJ_EVENT_GFX_MOM",
    "SPRITE_OAK": "OBJ_EVENT_GFX_PROF_BIRCH",
    "SPRITE_ELM": "OBJ_EVENT_GFX_SCIENTIST_2",
    "SPRITE_JUNIPER": "OBJ_EVENT_GFX_WOMAN_3",
    "SPRITE_COLRESS": "OBJ_EVENT_GFX_SCIENTIST_2",

    # --- líderes de ginásio de Unova ---------------------------------------
    "SPRITE_CILAN": "OBJ_EVENT_GFX_COOK",
    "SPRITE_LENORA": "OBJ_EVENT_GFX_ROXANNE",
    "SPRITE_BURGH": "OBJ_EVENT_GFX_ARTIST",
    "SPRITE_ELESA": "OBJ_EVENT_GFX_BEAUTY",
    "SPRITE_CLAY": "OBJ_EVENT_GFX_HIKER",
    "SPRITE_SKYLA": "OBJ_EVENT_GFX_WINONA",
    "SPRITE_DRAYDEN": "OBJ_EVENT_GFX_WATTSON",
    "SPRITE_ROXIE": "OBJ_EVENT_GFX_FLANNERY",
    "SPRITE_MARLON": "OBJ_EVENT_GFX_BRAWLY",
    "SPRITE_IRIS": "OBJ_EVENT_GFX_PHOEBE",

    # --- Elite dos Quatro / campeões ---------------------------------------
    "SPRITE_SHAUNTAL": "OBJ_EVENT_GFX_HEX_MANIAC",
    "SPRITE_GRIMSLEY": "OBJ_EVENT_GFX_SIDNEY",
    "SPRITE_MARSHAL": "OBJ_EVENT_GFX_BLACK_BELT",
    "SPRITE_CAITLIN": "OBJ_EVENT_GFX_ANABEL",
    "SPRITE_ALDER": "OBJ_EVENT_GFX_SPENSER",
    "SPRITE_CYNTHIA": "OBJ_EVENT_GFX_GLACIA",
    "SPRITE_LANCE": "OBJ_EVENT_GFX_DRAKE",

    # --- vilões -------------------------------------------------------------
    "SPRITE_INFER": "OBJ_EVENT_GFX_MAXIE",
    "SPRITE_INFER_SAGE": "OBJ_EVENT_GFX_MAGMA_MEMBER_M",
    "SPRITE_PZMA_SAGE": "OBJ_EVENT_GFX_AQUA_MEMBER_M",
    "SPRITE_VIO": "OBJ_EVENT_GFX_AQUA_MEMBER_M",
    "SPRITE_ROOD": "OBJ_EVENT_GFX_OLD_MAN",
    "SPRITE_ROCKET": "OBJ_EVENT_GFX_MAGMA_MEMBER_M",
    "SPRITE_ROCKET_GIRL": "OBJ_EVENT_GFX_MAGMA_MEMBER_F",
    "SPRITE_VIRBANK_GRUNT_1": "OBJ_EVENT_GFX_AQUA_MEMBER_M",
    "SPRITE_VIRBANK_GRUNT_2": "OBJ_EVENT_GFX_AQUA_MEMBER_F",
    "SPRITE_VIRBANK_GRUNT_3": "OBJ_EVENT_GFX_MAGMA_MEMBER_M",

    # --- NPCs genéricos e classes de treinador ------------------------------
    "SPRITE_YOUNGSTER": "OBJ_EVENT_GFX_YOUNGSTER",
    "SPRITE_STANDING_YOUNGSTER": "OBJ_EVENT_GFX_YOUNGSTER",
    "SPRITE_LASS": "OBJ_EVENT_GFX_LASS",
    "SPRITE_TWIN": "OBJ_EVENT_GFX_TWIN",
    "SPRITE_BUG_CATCHER": "OBJ_EVENT_GFX_BUG_CATCHER",
    "SPRITE_BLACK_BELT": "OBJ_EVENT_GFX_BLACK_BELT",
    "SPRITE_LINEBACKER": "OBJ_EVENT_GFX_BLACK_BELT",
    "SPRITE_GENTLEMAN": "OBJ_EVENT_GFX_GENTLEMAN",
    "SPRITE_SOCIALITE": "OBJ_EVENT_GFX_WOMAN_1",
    "SPRITE_TEACHER": "OBJ_EVENT_GFX_WOMAN_5",
    "SPRITE_BUENA": "OBJ_EVENT_GFX_WOMAN_2",
    "SPRITE_GRAMPS": "OBJ_EVENT_GFX_OLD_MAN",
    "SPRITE_GRANNY": "OBJ_EVENT_GFX_OLD_WOMAN",
    "SPRITE_SLEEPING_MAN": "OBJ_EVENT_GFX_MAN_5",
    "SPRITE_ROUGHNECK": "OBJ_EVENT_GFX_MAN_4",
    "SPRITE_ROCKER": "OBJ_EVENT_GFX_MANIAC",
    "SPRITE_HARLEQUIN": "OBJ_EVENT_GFX_MANIAC",
    "SPRITE_MUSICIAN": "OBJ_EVENT_GFX_BARD",
    "SPRITE_SUPER_NERD": "OBJ_EVENT_GFX_SCIENTIST_1",
    "SPRITE_SCIENTIST": "OBJ_EVENT_GFX_SCIENTIST_1",
    "SPRITE_SCIENTIST_F": "OBJ_EVENT_GFX_WOMAN_4",
    "SPRITE_GAMEBOY_KID": "OBJ_EVENT_GFX_GAMEBOY_KID",
    "SPRITE_POKEFAN_M": "OBJ_EVENT_GFX_POKEFAN_M",
    "SPRITE_POKEFAN_F": "OBJ_EVENT_GFX_POKEFAN_F",
    "SPRITE_COOLTRAINER_M": "OBJ_EVENT_GFX_RUNNING_TRIATHLETE_M",
    "SPRITE_COOLTRAINER_F": "OBJ_EVENT_GFX_RUNNING_TRIATHLETE_F",
    "SPRITE_CYCLIST_M": "OBJ_EVENT_GFX_CYCLING_TRIATHLETE_M",
    "SPRITE_CYCLIST_F": "OBJ_EVENT_GFX_CYCLING_TRIATHLETE_F",
    "SPRITE_BIKER": "OBJ_EVENT_GFX_CYCLING_TRIATHLETE_M",
    "SPRITE_RANGER_M": "OBJ_EVENT_GFX_CAMPER",
    "SPRITE_RANGER_F": "OBJ_EVENT_GFX_PICNICKER",
    "SPRITE_SWIMMER_GUY": "OBJ_EVENT_GFX_SWIMMER_M",
    "SPRITE_SWIMMER_GIRL": "OBJ_EVENT_GFX_SWIMMER_F",
    "SPRITE_SAILOR": "OBJ_EVENT_GFX_SAILOR",
    "SPRITE_OFFICER": "OBJ_EVENT_GFX_SAILOR",
    "SPRITE_FISHER": "OBJ_EVENT_GFX_FISHERMAN",
    "SPRITE_FISHING_GURU": "OBJ_EVENT_GFX_FISHERMAN",
    "SPRITE_GYM_GUY": "OBJ_EVENT_GFX_MAN_2",

    # --- balcões e atendimento ---------------------------------------------
    "SPRITE_NURSE": "OBJ_EVENT_GFX_NURSE",
    "SPRITE_CLERK": "OBJ_EVENT_GFX_MART_EMPLOYEE",
    "SPRITE_PHARMACIST": "OBJ_EVENT_GFX_MART_EMPLOYEE",
    "SPRITE_RECEPTIONIST": "OBJ_EVENT_GFX_UNION_ROOM_NURSE",
    "SPRITE_LINK_RECEPTIONIST": "OBJ_EVENT_GFX_LINK_RECEPTIONIST",

    # --- "variablesprite": placeholders trocados em runtime pelo BW3G -------
    # (o valor abaixo é só a aparência de fallback; ver relatório)
    "SPRITE_BATTLE_HOUSE_BLUE": "OBJ_EVENT_GFX_MAN_3",
    "SPRITE_MEMBERS_ROOM_BLUE": "OBJ_EVENT_GFX_MAN_1",
    "SPRITE_MEMBERS_ROOM_BROWN": "OBJ_EVENT_GFX_REPORTER_F",

    # --- Pokémon ------------------------------------------------------------
    "SPRITE_AUDINO": "OBJ_EVENT_GFX_KIRLIA",
    "SPRITE_DUCKLETT": "OBJ_EVENT_GFX_WINGULL",
    "SPRITE_YANMA": "OBJ_EVENT_GFX_WINGULL",
    "SPRITE_FLAAFFY": "OBJ_EVENT_GFX_PIKACHU",
    "SPRITE_GROWLITHE": "OBJ_EVENT_GFX_POOCHYENA",
    "SPRITE_SNEASEL": "OBJ_EVENT_GFX_POOCHYENA",
    "SPRITE_JIGGLYPUFF": "OBJ_EVENT_GFX_SKITTY",
    "SPRITE_KROKOROK": "OBJ_EVENT_GFX_KECLEON",
    "SPRITE_LARVESTA": "OBJ_EVENT_GFX_AZURILL",
    "SPRITE_MUNNA": "OBJ_EVENT_GFX_AZUMARILL",
    "SPRITE_ODDISH": "OBJ_EVENT_GFX_SUDOWOODO",
    "SPRITE_TRUBBISH": "OBJ_EVENT_GFX_SUDOWOODO",
    "SPRITE_PATRAT_SIDE": "OBJ_EVENT_GFX_ZIGZAGOON_1",
    "SPRITE_PURRLOIN_SIDE": "OBJ_EVENT_GFX_ZIGZAGOON_2",
    "SPRITE_METAGROSS": "OBJ_EVENT_GFX_REGISTEEL",
    "SPRITE_GENESECT": "OBJ_EVENT_GFX_DEOXYS",
    "SPRITE_GENESIS": "OBJ_EVENT_GFX_RAYQUAZA",
    "SPRITE_SHADOW": "OBJ_EVENT_GFX_DUSCLOPS",

    # --- objetos ------------------------------------------------------------
    "SPRITE_POKE_BALL": "OBJ_EVENT_GFX_ITEM_BALL",
    "SPRITE_BOULDER": "OBJ_EVENT_GFX_PUSHABLE_BOULDER",
    "SPRITE_FRUIT_TREE": "OBJ_EVENT_GFX_BERRY_TREE",
    "SPRITE_FOSSIL": "OBJ_EVENT_GFX_FOSSIL",
    "SPRITE_FAIRY": "OBJ_EVENT_GFX_CLEFAIRY_DOLL",
    "SPRITE_DOLL_1": "OBJ_EVENT_GFX_PIKACHU_DOLL",
    "SPRITE_DOLL_2": "OBJ_EVENT_GFX_MARILL_DOLL",
    "SPRITE_BIG_DOLL": "OBJ_EVENT_GFX_BIG_SNORLAX_DOLL",
    "SPRITE_CONSOLE": "OBJ_EVENT_GFX_MOVING_BOX",
    "SPRITE_FAN": "OBJ_EVENT_GFX_MOVING_BOX",
    "SPRITE_FOUNTAIN": "OBJ_EVENT_GFX_TRICK_HOUSE_STATUE",
    "SPRITE_CABLE": "OBJ_EVENT_GFX_TRICK_HOUSE_STATUE",

    # Insígnias: objetos pequenos, coloridos e estáticos de decoração.
    "SPRITE_BADGE_1": "OBJ_EVENT_GFX_BALL_CUSHION",
    "SPRITE_BADGE_2": "OBJ_EVENT_GFX_ROUND_CUSHION",
    "SPRITE_BADGE_3": "OBJ_EVENT_GFX_KISS_CUSHION",
    "SPRITE_BADGE_4": "OBJ_EVENT_GFX_ZIGZAG_CUSHION",
    "SPRITE_BADGE_5": "OBJ_EVENT_GFX_SPIN_CUSHION",
    "SPRITE_BADGE_6": "OBJ_EVENT_GFX_DIAMOND_CUSHION",
    "SPRITE_BADGE_7": "OBJ_EVENT_GFX_GRASS_CUSHION",
    "SPRITE_BADGE_8": "OBJ_EVENT_GFX_FIRE_CUSHION",
}

# SPRITEMOVEDATA_* do BW3G -> MOVEMENT_TYPE_* desta build.
MOVIMENTO = {
    "SPRITEMOVEDATA_STILL": "MOVEMENT_TYPE_NONE",
    "SPRITEMOVEDATA_STANDING_UP": "MOVEMENT_TYPE_FACE_UP",
    "SPRITEMOVEDATA_STANDING_DOWN": "MOVEMENT_TYPE_FACE_DOWN",
    "SPRITEMOVEDATA_STANDING_LEFT": "MOVEMENT_TYPE_FACE_LEFT",
    "SPRITEMOVEDATA_STANDING_RIGHT": "MOVEMENT_TYPE_FACE_RIGHT",
    "SPRITEMOVEDATA_WANDER": "MOVEMENT_TYPE_WANDER_AROUND",
    "SPRITEMOVEDATA_WALK_LEFT_RIGHT": "MOVEMENT_TYPE_WALK_LEFT_AND_RIGHT",
    "SPRITEMOVEDATA_WALK_UP_DOWN": "MOVEMENT_TYPE_WALK_UP_AND_DOWN",
    "SPRITEMOVEDATA_SPINCLOCKWISE": "MOVEMENT_TYPE_ROTATE_CLOCKWISE",
    "SPRITEMOVEDATA_SPINRANDOM_FAST": "MOVEMENT_TYPE_ROTATE_CLOCKWISE",
    "SPRITEMOVEDATA_SPINRANDOM_SLOW": "MOVEMENT_TYPE_ROTATE_COUNTERCLOCKWISE",
    "SPRITEMOVEDATA_POKEMON": "MOVEMENT_TYPE_FACE_DOWN",
    # objetos parados: gen 3 não tem equivalente animado, tudo vira NONE
    "SPRITEMOVEDATA_STRENGTH_BOULDER": "MOVEMENT_TYPE_NONE",
    "SPRITEMOVEDATA_BADGE": "MOVEMENT_TYPE_NONE",
    "SPRITEMOVEDATA_BIGDOLL": "MOVEMENT_TYPE_NONE",
    "SPRITEMOVEDATA_FOUNTAIN": "MOVEMENT_TYPE_NONE",
    "SPRITEMOVEDATA_CABLE_LEFT": "MOVEMENT_TYPE_NONE",
    "SPRITEMOVEDATA_CABLE_RIGHT": "MOVEMENT_TYPE_NONE",
    "SPRITEMOVEDATA_BRIDGE_RAIL_LEFT": "MOVEMENT_TYPE_NONE",
    "SPRITEMOVEDATA_BRIDGE_RAIL_RIGHT": "MOVEMENT_TYPE_NONE",
}

# MUSIC_* de data/maps/maps.asm -> MUS_* desta build.
#
# ATENÇÃO (verificado em include/constants/songs.h): quase todos os MUS_HG_*
# existem só como apelido de fallback (`#ifndef MUS_HG_X / #define MUS_HG_X
# MUS_PETALBURG_WOODS`); nada no repo os define de verdade. Usá-los em massa
# faria metade dos mapas tocar Petalburg Woods, então as faixas abaixo são as
# reais (Hoenn/RG/GSC) que estão na tabela de músicas.
MUSICA = {
    "MUSIC_NONE": "MUS_NONE",
    # cidades e vilas
    "MUSIC_NUVEMA_TOWN": "MUS_RG_PALLET",
    "MUSIC_ASPERTIA_CITY": "MUS_LITTLEROOT",
    "MUSIC_ACCUMULA_TOWN": "MUS_OLDALE",
    "MUSIC_FLOCCESY_TOWN": "MUS_VERDANTURF",
    "MUSIC_LACUNOSA_TOWN": "MUS_FALLARBOR",
    "MUSIC_LENTIMAS_TOWN": "MUS_GSC_PEWTER",
    "MUSIC_STRIATON_CITY": "MUS_RG_PEWTER",
    "MUSIC_CASTELIA_CITY": "MUS_RG_CELADON",
    "MUSIC_NIMBASA_CITY": "MUS_LILYCOVE",
    "MUSIC_DRIFTVEIL_CITY": "MUS_SLATEPORT",
    "MUSIC_MISTRALTON_CITY": "MUS_RG_VERMILLION",
    "MUSIC_ICIRRUS_CITY": "MUS_FORTREE",
    "MUSIC_OPELUCID_CITY": "MUS_SOOTOPOLIS",
    "MUSIC_HUMILAU_CITY": "MUS_DEWFORD",
    "MUSIC_VIRBANK_CITY": "MUS_RUSTBORO",
    # rotas e exterior
    "MUSIC_R_3": "MUS_ROUTE101",
    "MUSIC_R_4": "MUS_ROUTE113",
    "MUSIC_R_6": "MUS_ROUTE104",
    "MUSIC_R_14": "MUS_ROUTE119",
    "MUSIC_R_17": "MUS_ROUTE122",
    "MUSIC_R_22": "MUS_ROUTE120",
    "MUSIC_SKYARROW": "MUS_ROUTE110",
    "MUSIC_FOREST": "MUS_PETALBURG_WOODS",
    "MUSIC_DESERT_RESORT": "MUS_DESERT",
    # interiores e masmorras
    "MUSIC_POKEMON_CENTER": "MUS_POKE_CENTER",
    "MUSIC_MART": "MUS_POKE_MART",
    "MUSIC_GAME_CORNER": "MUS_GAME_CORNER",
    "MUSIC_MAGNET_TRAIN": "MUS_CABLE_CAR",
    "MUSIC_UNOVA_CAVE": "MUS_RG_MT_MOON",
    "MUSIC_UNOVA_TOWER": "MUS_MT_PYRE",
    "MUSIC_STRANGE_HOUSE": "MUS_RG_POKE_MANSION",
    "MUSIC_SEWERS": "MUS_RG_ROCKET_HIDEOUT",
    "MUSIC_P2_LAB": "MUS_AQUA_MAGMA_HIDEOUT",
    # ginásio e liga
    "MUSIC_GYM": "MUS_GYM",
    "MUSIC_VICTORY_ROAD": "MUS_VICTORY_ROAD",
    "MUSIC_PKMN_LEAGUE": "MUS_EVER_GRANDE",
}


if __name__ == "__main__":
    import os
    import re
    import sys

    REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def texto(rel):
        with open(os.path.join(REPO, rel), encoding="utf-8") as fp:
            return fp.read()

    # 1. OBJ_EVENT_GFX_* declarados no enum.
    declarados = set(re.findall(r"\bOBJ_EVENT_GFX_[A-Z0-9_]+",
                                texto("include/constants/event_objects.h")))

    # 2. OBJ_EVENT_GFX_* com gráfico apontado FORA de qualquer #if.
    desenhados, profundidade = set(), 0
    for linha in texto("src/data/object_events/"
                       "object_event_graphics_info_pointers.h").splitlines():
        nu = linha.strip()
        if nu.startswith("#if"):
            profundidade += 1
        elif nu.startswith("#endif"):
            profundidade = max(0, profundidade - 1)
        elif profundidade == 0:
            achado = re.match(r"\[(OBJ_EVENT_GFX_[A-Z0-9_]+)\]", nu)
            if achado:
                desenhados.add(achado.group(1))

    movimentos = set(re.findall(r"#define\s+(MOVEMENT_TYPE_[A-Z0-9_]+)",
                                texto("include/constants/event_object_movement.h")))
    musicas = set(re.findall(r"#define\s+(MUS_[A-Z0-9_]+)",
                             texto("include/constants/songs.h")))

    erros = []
    for chave, valor in sorted(SPRITE.items()):
        if valor not in declarados:
            erros.append(f"{chave}: {valor} não existe em event_objects.h")
        elif valor not in desenhados:
            erros.append(f"{chave}: {valor} só é desenhado dentro de #if "
                         "(FRLG) -- derruba o jogo nesta build")
    for chave, valor in sorted(MOVIMENTO.items()):
        if valor not in movimentos:
            erros.append(f"{chave}: {valor} não existe em "
                         "event_object_movement.h")
    for chave, valor in sorted(MUSICA.items()):
        if valor not in musicas:
            erros.append(f"{chave}: {valor} não existe em songs.h")

    # 3. Cobertura: nenhuma constante usada pelo BW3G pode ficar de fora.
    #    (só roda se o clone de origem ainda estiver por perto)
    BW3G = "/tmp/bw3g-probe"
    if os.path.isdir(os.path.join(BW3G, "maps")):
        import glob
        usados_sprite, usados_mov = set(), set()
        for caminho in glob.glob(os.path.join(BW3G, "maps", "**", "*.asm"),
                                 recursive=True):
            with open(caminho, encoding="utf-8", errors="replace") as fp:
                for linha in fp:
                    if "object_event" not in linha:
                        continue
                    campos = [c.strip() for c in linha.split(",")]
                    if len(campos) > 3:
                        usados_sprite.add(campos[2])
                        usados_mov.add(campos[3])
        for nome in sorted(usados_sprite - set(SPRITE)):
            if nome.startswith("SPRITE_"):
                erros.append(f"{nome}: usado no BW3G e ausente do dict SPRITE")
        for nome in sorted(usados_mov - set(MOVIMENTO)):
            if nome.startswith("SPRITEMOVEDATA_"):
                erros.append(f"{nome}: usado no BW3G e ausente do dict MOVIMENTO")
        maps_asm = os.path.join(BW3G, "data", "maps", "maps.asm")
        if os.path.isfile(maps_asm):
            with open(maps_asm, encoding="utf-8", errors="replace") as fp:
                usados_mus = set(re.findall(r"\bMUSIC_[A-Z0-9_]+", fp.read()))
            for nome in sorted(usados_mus - set(MUSICA)):
                erros.append(f"{nome}: usado no BW3G e ausente do dict MUSICA")

    if erros:
        print("FALHOU:")
        for erro in erros:
            print("  -", erro)
        sys.exit(1)

    print(f"OK: {len(SPRITE)} sprites, {len(MOVIMENTO)} movimentos, "
          f"{len(MUSICA)} musicas")
