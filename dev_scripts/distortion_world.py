#!/usr/bin/env python3
"""O Distortion World em 2D, com gravidade normal, e o Giratina dentro dele.

    python3 dev_scripts/distortion_world.py --medir    # o que a fonte tem
    python3 dev_scripts/distortion_world.py --demo     # autoteste, nao grava
    python3 dev_scripts/distortion_world.py --aplicar  # escreve

A MEDIDA QUE DECIDIU O DESENHO (21/08/2026)
-------------------------------------------
O Platinum tem DEZ headers de Distortion World (o `1F`, sete subsolos, a sala do
Giratina e a da Turnback Cave), cada um com matriz propria. Nove deles apontam
para `events_empty`; so o `1F` tem tabela de eventos, e ela tem UM warp, de
saida para o `MT_CORONET_6F`. Nada na fonte aponta para DENTRO: a entrada e
cena de script no Spear Pillar.

A grade 2D de colisao dos dez foi lida tile a tile (`--medir`). Ela **nao tem
chao**:

    andar        tamanho   colisao   terra andavel   maior ilha de terra
    1F            64x64      97,8%          1                 1
    B1F           64x32      95,0%          6                 2
    B2F           64x64      95,2%          4                 4
    B3F           64x64      22,8%         49                 3   (+2773 de MAR)
    B4F           64x64      88,0%         25                10
    B5F           64x64      90,0%         33                 4   (+119 de mar)
    B6F           64x64      93,9%         22                 4
    B7F           32x64      95,5%         11                 2
    GIRATINA      32x32      98,1%          6                 2
    TURNBACK      64x64      93,4%          2                 1

A maior mancha de chao andavel do Distortion World INTEIRO tem DEZ tiles, num
andar que nem e o do Giratina. O que sobra nao e chao: os comportamentos que
aparecem sao `TILE_BEHAVIOR_JUMP_*_TWICE` (0x5A a 0x5D), ou seja marcador de
pulo, e no B3F um mar de `TILE_BEHAVIOR_WATER_SEA`. A geometria do Distortion
World mora no MODELO 3D com gravidade variavel, e a grade 2D so carrega os
marcadores. Nao ha nove andares para converter: nao ha um.

Na sala do Giratina a grade inteira sao SEIS tiles, tres pares de pulo na
coluna 15 (linhas 15/16, 18/19 e 21/22). E disso, e so disso, que sai o
desenho: **um andar so, na coluna que a fonte marcou**, com o corredor descendo
por ela ate a camara do Giratina. O tamanho (32x32) e o da matriz da fonte.

O QUE E INVENTADO, DITO EM VOZ ALTA
-----------------------------------
O piso. Ele esta em `CARVADO` e nao sai de lugar nenhum da fonte, porque a
fonte nao tem piso 2D aqui. A decisao de ter o mapa e do Gui em 21/08/2026
("daria pra fazer com gravidade normal? queria o mapa"), e o que a medida
manda e nao fingir que os outros nove andares existem em 2D. **Desenhar os
outros nove seria desenhar, nao converter**, e por isso eles nao entram.

A entrada tambem e invencao declarada, pelo mesmo motivo: a fonte abre o portal
por cena e nao por warp. O warp novo do Spear Pillar fica em (14,11), ao lado do
que ja leva ao `SPEAR_PILLAR_DISTORTED`, num tile que a busca em largura mostra
alcancavel a pe a partir da porta de (14,14), e a cena do mapa nao e tocada.

O tile debaixo dos dois warps NAO e enfeite: warp em chao comum nao dispara
neste motor (licao 4.1 do ESTADO, e o defeito que o OreburghGateB1F pagou em
21/08). Aqui os dois lados usam metatile com comportamento que
`IsWarpMetatileBehavior` aceita, e o `--demo` LE isso da tabela de atributos do
tileset em vez de confiar no numero.
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import converte_cavernas_sinnoh as C          # noqa: E402
import converte_moldes_sinnoh as M            # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAPA = "DistortionWorld"
ID = "MAP_DISTORTION_WORLD"
LAYOUT = "LAYOUT_DISTORTION_WORLD"
GRUPO = "gMapGroup_SinnohCavernas"
HEADER = "MAP_HEADER_DISTORTION_WORLD_GIRATINA_ROOM"

# Flag de HIDE do Giratina. Apelido de `FLAG_UNUSED_*`, portanto CUSTO ZERO de
# save: a faixa ja existe no bloco gravado e so ganha nome. 0x1C59 e o primeiro
# livre depois das 56 bolas de Galar (medido por `flags_livres.py`: 5.711 livres
# no total, a maior faixa contigua em 0x20D2).
FLAG_GIRATINA = "FLAG_HIDE_GIRATINA"
FLAG_GIRATINA_BASE = "FLAG_UNUSED_0x1C59"

# Nivel do Giratina: 47, o mesmo que `SpearPillar_Dialga` e `SpearPillar_Palkia`
# ja usam neste repo e o mesmo do Distortion World do Platinum. Nao e escolha
# nova, e o valor que a obra de Sinnoh ja tinha adotado.
NIVEL = 47

# --------------------------------------------------------------- a geometria
# INVENTADO, ver o cabecalho. Retangulos (x0, y0, x1, y1) inclusivos, no
# vocabulario da PROPRIA fonte: o piso e escrito como grade crua de gen 4 e
# depois traduzido por `converte_cavernas_sinnoh.traduz`, que e quem sabe fazer
# rocha de duas faces. Assim o desenho nao inventa metatile nenhum, so o
# recorte do chao.
#
# O corredor cobre a coluna 15, que e onde os SEIS tiles da fonte estao.
CARVADO = ((14, 10, 16, 23),     # corredor, descendo pela coluna da fonte
           (10, 24, 20, 29))     # camara do Giratina, no fundo

WARP = (15, 10)                  # topo do corredor, a boca do portal
GIRATINA = (15, 26)              # dentro da camara

CHAO_FONTE = 0x0008              # TILE_BEHAVIOR_CAVE_FLOOR, sem colisao
VAZIO = 0x8000                   # bit 15 = colisao, comportamento nenhum

# --------------------------------------------------------------- Spear Pillar
SPEAR = "SpearPillar"
SPEAR_ID = "MAP_SPEAR_PILLAR"
SPEAR_WARP = (14, 11)
# Metatile 588 com colisao 0 e elevacao 3. Nao e numero decorado: e a palavra
# EXATA que ja esta debaixo dos warps de (14,14) e (16,14) do proprio
# `LAYOUT_SPEARPILLAR`, lida do `map.bin` em 21/08/2026. O comportamento e
# `MB_NON_ANIMATED_DOOR`, que `IsWarpMetatileBehavior` aceita, ou seja dispara
# ao CHEGAR no tile, venha o jogador de onde vier.
SPEAR_PORTA = 0x324C


def headers_dw():
    return sorted(h for h in C.headers() if "DISTORTION_WORLD" in h)


def _ilha_maior(pal, larg, alt):
    """Maior mancha conexa de chao de ELEVACAO 3, que e onde se anda a pe.

    Elevacao entra porque colisao sozinha mente: o mar do B3F tem colisao zero
    e elevacao 1, e quem so olhou colisao contou 2.822 tiles de "chao" num
    andar que a pe nao tem nenhum. E a mesma licao do lago do OreburghGateB1F.
    """
    terra = {i for i, p in enumerate(pal)
             if (p >> 10) & 3 == 0 and (p >> 12) & 0xF == 3}
    visto, melhor = set(), 0
    for ini in terra:
        if ini in visto:
            continue
        pilha, n = [ini], 0
        visto.add(ini)
        while pilha:
            i = pilha.pop()
            n += 1
            x, y = i % larg, i // larg
            for j, ok in ((i - 1, x > 0), (i + 1, x + 1 < larg),
                          (i - larg, y > 0), (i + larg, y + 1 < alt)):
                if ok and j in terra and j not in visto:
                    visto.add(j)
                    pilha.append(j)
        melhor = max(melhor, n)
    return len(terra), melhor


def medida():
    """[(andar, larg, alt, colisao, terra, maior ilha)] lido da fonte."""
    saida = []
    for h in headers_dw():
        larg, alt, grade, _off = M.grade_do_mapa(h)
        pal = C.traduz(larg, alt, grade)
        terra, ilha = _ilha_maior(pal, larg, alt)
        saida.append((h[len("MAP_HEADER_DISTORTION_WORLD_"):], larg, alt,
                      M.densidade_de_colisao(grade), terra, ilha))
    return saida


def grade_carvada():
    """(larg, alt, grade) da sala do Giratina com o piso inventado por cima.

    A grade da FONTE entra inteira; o que `CARVADO` faz e trocar tile de vazio
    por chao de caverna. Os seis marcadores de pulo da fonte continuam onde
    estao, e por isso o corredor passa exatamente por cima deles.
    """
    larg, alt, grade, _off = M.grade_do_mapa(HEADER)
    grade = list(grade)
    for x0, y0, x1, y1 in CARVADO:
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                grade[y * larg + x] = CHAO_FONTE
    return larg, alt, grade


def palavras():
    larg, alt, grade = grade_carvada()
    pal = C.traduz(larg, alt, grade)
    pal[WARP[1] * larg + WARP[0]] = C.ESCADA
    return larg, alt, pal


def andavel(p):
    return (p >> 10) & 3 == 0


def alcance(pal, larg, alt, inicio):
    """Tiles a pe a partir de `inicio`, por colisao E elevacao."""
    def ok(i):
        return andavel(pal[i]) and (pal[i] >> 12) & 0xF == 3
    ini = inicio[1] * larg + inicio[0]
    if not ok(ini):
        return set()
    visto, pilha = {ini}, [ini]
    while pilha:
        i = pilha.pop()
        x, y = i % larg, i // larg
        for j, c in ((i - 1, x > 0), (i + 1, x + 1 < larg),
                     (i - larg, y > 0), (i + larg, y + 1 < alt)):
            if c and j not in visto and ok(j):
                visto.add(j)
                pilha.append(j)
    return visto


# ------------------------------------------------------------------ escrita
def _grava_json(caminho, dado):
    json.dump(dado, open(caminho, "w"), indent=2, ensure_ascii=False)
    open(caminho, "a").write("\n")


def _map_json(larg, alt):
    return {
        "id": ID, "name": MAPA, "layout": LAYOUT,
        "music": "MUS_ABNORMAL_WEATHER",
        "region_map_section": "MAPSEC_SINNOH_NORTH",
        "requires_flash": False, "weather": "WEATHER_NONE",
        "map_type": "MAP_TYPE_UNDERGROUND",
        "allow_cycling": False, "allow_escaping": False,
        "allow_running": False, "show_map_name": False,
        "battle_scene": "MAP_BATTLE_SCENE_NORMAL", "connections": 0,
        "object_events": [{
            "local_id": "LOCALID_DISTORTION_WORLD_GIRATINA",
            "graphics_id": "OBJ_EVENT_GFX_SPECIES(GIRATINA)",
            "x": GIRATINA[0], "y": GIRATINA[1], "elevation": 0,
            "movement_type": "MOVEMENT_TYPE_WALK_IN_PLACE_DOWN",
            "movement_range_x": 0, "movement_range_y": 0,
            "trainer_type": "TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id": "0",
            "script": "DistortionWorld_EventScript_Giratina",
            "flag": FLAG_GIRATINA}],
        "warp_events": [{
            "x": WARP[0], "y": WARP[1], "elevation": 0,
            "dest_map": SPEAR_ID, "dest_warp_id": "3"}],
        "bg_events": [], "coord_events": [],
        "origem_geometria": (
            "distortion_world.py: a grade 2D do Platinum "
            f"({HEADER}) tem SEIS tiles e nenhum chao, porque o Distortion "
            "World mora no modelo 3D de gravidade variavel. O tamanho 32x32 e "
            "a coluna 15 do corredor sao da fonte; o PISO e invencao "
            "declarada, decisao do Gui em 21/08/2026"),
    }


SCRIPTS = """@ O Distortion World em 2D, com gravidade normal.
@
@ A grade 2D do Platinum para MAP_HEADER_DISTORTION_WORLD_GIRATINA_ROOM tem
@ SEIS tiles ocupados e nenhum chao: a geometria de verdade e o modelo 3D com
@ gravidade variavel, que este motor nao tem. O tamanho e a coluna do corredor
@ vem da fonte; o piso e invencao declarada (dev_scripts/distortion_world.py).
@ Os outros nove andares NAO foram desenhados de proposito: seria desenhar, e
@ nao converter.
@
@ ponytail: o Giratina e object_event e nao bg_event, ao contrario do Dialga e
@ do Palkia do Spear Pillar. A diferenca nao e gosto: graphics/pokemon/giratina
@ TEM overworld.png, entao o sprite existe nesta build, e so objeto SOLIDO
@ prova a trava (o jogador para um tile antes dele). Foi por nao existir sprite
@ que o Dialga virou placa.

DistortionWorld_MapScripts::
\t.byte 0

@ LOCALID_DISTORTION_WORLD_GIRATINA nao e declarado aqui de proposito: quem o
@ declara e o mapjson, a partir do campo `local_id` do map.json. Um `.set` ao
@ lado disso vira `.set 1, 1` depois do pre-processador e o `as` responde
@ "expected symbol name" (medido em 21/08/2026). O WhirlIslands_LugiaChamber
@ declara porque os objetos DELE nao tem `local_id` no map.json.

DistortionWorld_EventScript_Giratina::
\tlockall
\tplaymoncry SPECIES_GIRATINA, CRY_MODE_ENCOUNTER
\tdelay 30
\twaitmoncry
\tsetwildbattle SPECIES_GIRATINA, %d
\tdowildbattle
\tspecialvar VAR_RESULT, GetBattleOutcome
\tgoto_if_eq VAR_RESULT, B_OUTCOME_WON, DistortionWorld_EventScript_GiratinaSumiu
\tgoto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, DistortionWorld_EventScript_GiratinaSumiu
\treleaseall
\tend

@ ponytail: so some em vitoria ou captura, a mesma regra que o
@ SpearPillar_Dialga ja escreveu. Fugir, perder ou ser teleportado deixa o
@ Giratina onde esta, senao uma Poke Ball errada apagaria o lendario do save.
DistortionWorld_EventScript_GiratinaSumiu::
\tfadescreenswapbuffers FADE_TO_BLACK
\tremoveobject LOCALID_DISTORTION_WORLD_GIRATINA
\tsetflag %s
\tfadescreenswapbuffers FADE_FROM_BLACK
\treleaseall
\tend
""" % (NIVEL, FLAG_GIRATINA)


def _anexa_linha(caminho, linha):
    """Escreve `linha` no fim do arquivo se ela ainda nao estiver la."""
    texto = open(caminho).read()
    if linha in texto:
        return False
    if not texto.endswith("\n"):
        texto += "\n"
    open(caminho, "w").write(texto + linha + "\n")
    return True


def aplica():
    """Escreve o mapa, o layout, a flag e o warp do Spear Pillar. Idempotente."""
    feito = []
    larg, alt, pal = palavras()

    # 1. layout proprio
    dst = f"{REPO}/data/layouts/{MAPA}"
    os.makedirs(dst, exist_ok=True)
    open(f"{dst}/map.bin", "wb").write(struct.pack(f"<{len(pal)}H", *pal))
    open(f"{dst}/border.bin", "wb").write(struct.pack("<4H", *([C.ROCHA_TOPO] * 4)))
    lay = json.load(open(f"{REPO}/data/layouts/layouts.json"))
    if not any(l.get("id") == LAYOUT for l in lay["layouts"]):
        # FIM da lista, sempre: indice de layout que anda quebra ROM ja gravada.
        lay["layouts"].append({
            "id": LAYOUT, "name": f"{MAPA}_Layout",
            "width": larg, "height": alt,
            "primary_tileset": "gTileset_GeneralSinnoh",
            "secondary_tileset": "gTileset_CaveSinnoh",
            "border_filepath": f"data/layouts/{MAPA}/border.bin",
            "blockdata_filepath": f"data/layouts/{MAPA}/map.bin",
            "layout_version": "emerald"})
        _grava_json(f"{REPO}/data/layouts/layouts.json", lay)
        feito.append("layout")

    # 2. mapa
    os.makedirs(f"{REPO}/data/maps/{MAPA}", exist_ok=True)
    _grava_json(f"{REPO}/data/maps/{MAPA}/map.json", _map_json(larg, alt))
    open(f"{REPO}/data/maps/{MAPA}/scripts.inc", "w").write(SCRIPTS)

    # 3. grupo de mapa, no FIM do grupo: id de mapa e (grupo << 8 | indice), e
    #    entrar no meio andaria com o id de todo mapa depois dele, o que quebra
    #    save gravada. No fim, ninguem se mexe.
    g = json.load(open(f"{REPO}/data/maps/map_groups.json"))
    if MAPA not in g[GRUPO]:
        g[GRUPO].append(MAPA)
        _grava_json(f"{REPO}/data/maps/map_groups.json", g)
        feito.append("grupo")

    # 4. os scripts entram na montagem
    if _anexa_linha(f"{REPO}/data/event_scripts.s",
                    f'\t.include "data/maps/{MAPA}/scripts.inc"'):
        feito.append("include")

    # 5. a flag, apelido de FLAG_UNUSED e portanto de custo zero de save
    if _anexa_linha(f"{REPO}/include/constants/flags.h",
                    f"#define {FLAG_GIRATINA:<28s}{FLAG_GIRATINA_BASE}"
                    "  // Distortion World, 21/08/2026"):
        feito.append("flag")

    # 6. o warp do Spear Pillar, em APPEND, e o tile debaixo dele
    d = json.load(open(f"{REPO}/data/maps/{SPEAR}/map.json"))
    if not any(w["dest_map"] == ID for w in d["warp_events"]):
        d["warp_events"].append({
            "x": SPEAR_WARP[0], "y": SPEAR_WARP[1], "elevation": 0,
            "dest_map": ID, "dest_warp_id": "0",
            "origem": (
                "portal INVENTADO: no Platinum a entrada do Distortion World e "
                "cena de script, nao warp de tabela. Decisao do Gui em "
                "21/08/2026. Fica em append, no fim da lista, para nao andar "
                "com o indice dos tres warps que ja existiam")})
        _grava_json(f"{REPO}/data/maps/{SPEAR}/map.json", d)
        feito.append("warp do Spear Pillar")
    caminho = f"{REPO}/data/layouts/{SPEAR}/map.bin"
    b = bytearray(open(caminho, "rb").read())
    L = M._layouts()["LAYOUT_SPEARPILLAR"]
    i = (SPEAR_WARP[1] * L["width"] + SPEAR_WARP[0]) * 2
    if (b[i] | (b[i + 1] << 8)) != SPEAR_PORTA:
        b[i], b[i + 1] = SPEAR_PORTA & 0xFF, SPEAR_PORTA >> 8
        open(caminho, "wb").write(bytes(b))
        feito.append("tile do portal")

    kb = len(pal) * 2 / 1024
    return (f"{MAPA}: {larg}x{alt}, {kb:.1f} KB, "
            f"{len(alcance(pal, larg, alt, WARP))} tiles a pe, "
            f"arte {M.arte(pal)}. "
            + (", ".join(feito) if feito else "nada novo a escrever"))


# ------------------------------------------------------------------- saidas
def imprime_medida():
    print(f"{'andar':22s} {'planta':9s} {'colisao':>8s} {'terra':>6s} "
          f"{'maior ilha':>11s}")
    for nome, larg, alt, dens, terra, ilha in medida():
        print(f"{nome:22s} {larg}x{alt:<6d} {dens*100:7.1f}% {terra:6d} "
              f"{ilha:11d}")
    print("\nNENHUM andar tem chao 2D: a maior ilha andavel do Distortion World "
          "inteiro\ncabe em dez tiles. A geometria mora no modelo 3D com "
          "gravidade variavel.")
    return 0


def demo():
    """Autoteste com mutacao plantada: o que quebra tem que ser PEGO."""
    # 1. A MEDIDA que justifica a invencao. Se um dia alguem achar o chao de
    #    verdade da fonte, esta afirmacao cai e a pessoa fica sabendo que o
    #    desenho inventado perdeu a razao de existir. E o contrario do de
    #    sempre: aqui o autoteste guarda a AUSENCIA de dado.
    m = medida()
    assert len(m) == 10, [x[0] for x in m]
    assert max(x[5] for x in m) <= 10, m
    assert dict((x[0], x[5]) for x in m)["GIRATINA_ROOM"] == 2

    # 2. Os seis tiles da fonte na sala do Giratina, e a coluna deles, que e de
    #    onde o corredor sai. Mutacao plantada: corredor fora da coluna 15 nao
    #    passaria por marcador nenhum e o desenho perderia a ancora.
    larg, alt, crua, _off = M.grade_do_mapa(HEADER)
    marcados = [(i % larg, i // larg) for i, v in enumerate(crua) if v & 0xFF]
    assert (larg, alt) == (32, 32), (larg, alt)
    assert marcados == [(15, 15), (15, 16), (15, 18), (15, 19),
                        (15, 21), (15, 22)], marcados
    x0, _y0, x1, _y1 = CARVADO[0]
    assert x0 <= 15 <= x1, CARVADO[0]

    # 3. O mapa e ANDAVEL de ponta a ponta: da boca do portal se chega ao tile
    #    de onde se fala com o Giratina. Mutacao plantada: cortar o corredor
    #    parte a mancha em duas e o jogador entra e nao chega a lugar nenhum.
    larg, alt, pal = palavras()
    andaveis = alcance(pal, larg, alt, WARP)
    assert len(andaveis) > 100, len(andaveis)
    de_frente = (GIRATINA[0], GIRATINA[1] - 1)
    assert de_frente[1] * larg + de_frente[0] in andaveis, de_frente
    # ... e o proprio tile do Giratina e chao, senao o objeto nasce na pedra.
    assert andavel(pal[GIRATINA[1] * larg + GIRATINA[0]])
    # ... e o caminho e RETO pela coluna do warp, que e o que a rota do T124
    #     anda. Um so DOWN saturante tem que ir do portal ate encostar nele.
    for y in range(WARP[1], GIRATINA[1]):
        assert andavel(pal[y * larg + WARP[0]]), y

    # 4. O TILE DEBAIXO DE CADA WARP, lido da tabela de atributos do tileset e
    #    nunca decorado. Warp em chao comum nao dispara neste motor e o mapa
    #    nasce de mao unica calado: e a licao 4.1 e o defeito que o
    #    OreburghGateB1F pagou em 21/08/2026. Mutacao plantada: trocar o
    #    carimbo por chao de caverna tem que ser pego aqui.
    assert M.comportamento(C.ESCADA & 0x3FF) == "MB_LADDER"
    assert M.comportamento(C.CHAO & 0x3FF) == "MB_CAVE"
    assert pal[WARP[1] * larg + WARP[0]] == C.ESCADA
    assert M.comportamento(SPEAR_PORTA & 0x3FF, "gTileset_General",
                           "gTileset_Pacifidlog") == "MB_NON_ANIMATED_DOOR"

    # 5. Nada de mao unica: os dois lados existem e apontam um para o outro.
    #    So vale depois de aplicado; antes disso o assert seria mentira.
    arq = f"{REPO}/data/maps/{MAPA}/map.json"
    if os.path.exists(arq):
        meu = json.load(open(arq))
        spear = json.load(open(f"{REPO}/data/maps/{SPEAR}/map.json"))
        volta = [w for w in spear["warp_events"] if w["dest_map"] == ID]
        assert len(volta) == 1, volta
        assert (volta[0]["x"], volta[0]["y"]) == SPEAR_WARP
        i = int(volta[0]["dest_warp_id"])
        assert meu["warp_events"][i]["dest_map"] == SPEAR_ID
        j = int(meu["warp_events"][0]["dest_warp_id"])
        assert spear["warp_events"][j]["dest_map"] == ID, j
        # o tile do lado do Spear Pillar tambem tem que ter ficado carimbado
        L = M._layouts()["LAYOUT_SPEARPILLAR"]
        b = open(f"{REPO}/{L['blockdata_filepath']}", "rb").read()
        k = (SPEAR_WARP[1] * L["width"] + SPEAR_WARP[0]) * 2
        assert (b[k] | (b[k + 1] << 8)) == SPEAR_PORTA
        # ... e o warp novo tem que ser ALCANCAVEL a pe a partir da porta que
        #     ja existia, senao o portal fica atras de parede.
        pals = [b[n] | (b[n + 1] << 8) for n in range(0, len(b), 2)]
        assert (SPEAR_WARP[1] * L["width"] + SPEAR_WARP[0]
                in alcance(pals, L["width"], L["height"], (14, 14)))
        # ... e a CENA nao foi tocada: os tres warps velhos continuam nos
        #     mesmos indices, senao script que cita warp_id muda de destino.
        assert [w["dest_map"] for w in spear["warp_events"][:3]] == [
            "MAP_MT_CORONET_1F_NORTH_ROOM2", "MAP_SPEAR_PILLAR_DISTORTED",
            "MAP_MT_CORONET_6F"], spear["warp_events"][:3]
        # A cena do Spear Pillar continua inteira. Nao se conta objeto: outra
        # frente pos o Arceus la em 21/08/2026 e contagem fixa quebraria por
        # motivo errado. O que este warp nao pode fazer e SUMIR com alguem.
        scripts = {o.get("script") for o in spear["object_events"]}
        for quem in ("Cyrus", "Mars", "Jupiter", "Grunt"):
            assert f"SpearPillar_EventScript_{quem}" in scripts, quem
        # ... nem nascer em cima de gente: dois objetos no mesmo tile e um
        # invisivel, e o portal ficaria intransponivel se fosse o de baixo.
        assert SPEAR_WARP not in {(o["x"], o["y"])
                                  for o in spear["object_events"]}

    print("demo ok")
    return 0


def main():
    if "--demo" in sys.argv:
        return demo()
    if "--aplicar" in sys.argv:
        print(aplica())
        return 0
    return imprime_medida()


if __name__ == "__main__":
    sys.exit(main())
