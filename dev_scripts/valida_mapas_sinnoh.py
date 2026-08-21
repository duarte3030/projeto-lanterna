#!/usr/bin/env python3
"""Confere e conserta os mapas de Sinnoh povoados por agentes.

Uso:
    python3 dev_scripts/valida_mapas_sinnoh.py            # so relata
    python3 dev_scripts/valida_mapas_sinnoh.py --corrigir # relata e conserta
    python3 dev_scripts/valida_mapas_sinnoh.py --demo     # autoteste, nao grava

Checa quatro coisas que já quebraram o build antes:
1. sprite (`graphics_id`) que esta build não consegue desenhar, ou seja, que
   não tem entrada em object_event_graphics_info_pointers.h fora de `#if IS_FRLG`
2. tipo de movimento que não existe em constants/event_object_movement.h
3. script citado no map.json sem rótulo correspondente no scripts.inc
4. NPC em cima de tile com colisão, ou fora do mapa

Com --corrigir, troca sprite e movimento inexistentes por equivalente real e
move NPC bloqueado para o tile livre mais próximo. Script faltando NÃO se
conserta sozinho: vira relatório, porque inventar diálogo é decisão humana.

O QUE MUDOU NA CHECAGEM 4, em 21/08/2026 (onda das pedras dentro de parede)
--------------------------------------------------------------------------
"Objeto em tile bloqueado" era CONTAGEM CRUA, e contagem crua reprova o jogo
original (lição 4.10 do ESTADO). Medido no repo inteiro: **951 objetos estão em
tile bloqueado**, e a esmagadora maioria é DESENHO, não defeito: 212 em parede
de base secreta, 87 em canteiro de berry, 32 em água do mar, 28 em ledge, 23 em
balcão. A pergunta certa não é "a colisão é zero?", é "o COMPORTAMENTO do
metatile é um em que objeto fica de propósito?".

Três famílias saem da acusação, cada uma por um motivo medido:

- **Pokémon de overworld** (`OBJ_EVENT_GFX_SPECIES(...)`, e as formas shiny e
  female): fantasma e voador ficam sobre parede de propósito, e é assim que a
  fonte desenha. Os 4 MISDREAVUS do ginásio de Ecruteak e o SKARMORY do Lake of
  Rage são isso, não defeito.
- **`OBJ_EVENT_GFX_LIGHT_SPRITE`** (efeito de luz): o motor trata antes de
  virar object event, não bloqueia tile e mora no teto/parede por definição.
  `OBJ_EVENT_GFX_VAR_*` entra junto: quem resolve é o jogo em tempo de execução.
- **Comportamento de metatile da lista `POR_DESENHO`**, nomes lidos de
  `include/constants/metatile_behaviors.h` e nunca número cravado. `MB_COUNTER`
  está nela porque é o mecanismo do PRÓPRIO MOTOR para falar através de um tile
  bloqueado: os 20 atendentes de loja de Sinnoh estão nele.

Uma QUARTA família saiu depois, e ela custou uma quebra de suíte para aparecer:
**objeto em tile bloqueado cujo VIZINHO ORTOGONAL é alcançável não é defeito**,
porque é assim que o motor deixa falar com quem está atrás de balcão. A primeira
versão desta leva acusou 3 NPCs, eles foram movidos, e o T100.14 quebrou na
hora: aquele caso anda até (5,4) e vira para o cientista da Route206_North em
(6,4) desde 18/08, e o texto dele já dizia "tile de parede; falar com NPC atrás
de balcão é legal neste motor". Os 3 voltaram para onde estavam. Ver
`da_para_falar`.

O que SOBRA depois de tudo isso, em Sinnoh, são **2 enfermeiras que o jogador
não consegue encarar**: Jubilife (5,2) e Sandgem (6,2). O tile do balcão à
frente delas, (5,3) e (6,3), é `MB_NORMAL` e não `MB_COUNTER`, e o Emerald de
fábrica faz o contrário (Petalburg põe a enfermeira em (7,2) ANDÁVEL e o
`MB_COUNTER` em (7,3)). Consequência medida no desenho, não deduzida: nesses
dois Pokécenters não há de onde falar com a enfermeira. É defeito de arte de
mapa, não de objeto, e está na fila.

ARMADILHA DO PRÓPRIO PARSER, medida aqui e não deduzida: o enum de
`metatile_behaviors.h` tem comentário de fim de linha, e o de
`MB_INTERIOR_DEEP_WATER` CITA `MB_DEEP_WATER`. Quebrar o corpo por vírgula
ANTES de tirar comentário engole o `MB_DEEP_WATER` de verdade e desloca todos
os valores seguintes em 1: `MB_COUNTER` vira 0x7F em vez de 0x80, e a lista de
água deixa de casar com tile nenhum. Tira comentário PRIMEIRO. Foi esse erro
que fez a primeira medição desta onda dizer `MB_UNUSED_81` onde o jogo diz
`MB_COUNTER`.
"""
import json
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "dev_scripts"))
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
    # 05/08/2026: classes que apareceram ao trazer os NPC do pokeplatinum.
    # Todas são gente comum trocada por gente comum de classe parecida. Líder de
    # ginásio, Galáctica nomeada e Pokémon NÃO entram aqui: sem sprite próprio
    # eles ficam de fora (ver NOMES_PROPRIOS em importa_npcs_sinnoh.py), porque
    # Byron com cara de nadador é o mapa mentindo.
    "OBJ_EVENT_GFX_COLLECTOR": "OBJ_EVENT_GFX_MANIAC",
    "OBJ_EVENT_GFX_RUIN_MANIAC": "OBJ_EVENT_GFX_MANIAC",
    "OBJ_EVENT_GFX_CASHIER_M": "OBJ_EVENT_GFX_CLERK",
    "OBJ_EVENT_GFX_CASHIER_F": "OBJ_EVENT_GFX_MART_EMPLOYEE",
    "OBJ_EVENT_GFX_RECEPTIONIST": "OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST",
    "OBJ_EVENT_GFX_WIFI_PLAZA_ATTENDANT_F": "OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST",
    "OBJ_EVENT_GFX_FRONTIER_BOOTH_ATTENDANT": "OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST",
    "OBJ_EVENT_GFX_FRONTIER_SINGLE_ATTENDANT": "OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST",
    "OBJ_EVENT_GFX_FRONTIER_MULTI_ATTENDANT": "OBJ_EVENT_GFX_CABLE_CLUB_RECEPTIONIST",
    "OBJ_EVENT_GFX_PSYCHIC": "OBJ_EVENT_GFX_PSYCHIC_M",
    "OBJ_EVENT_GFX_SCIENTIST_M": "OBJ_EVENT_GFX_SCIENTIST_1",
    "OBJ_EVENT_GFX_SCIENTIST_F": "OBJ_EVENT_GFX_EXPERT_F",
    "OBJ_EVENT_GFX_POKECENTER_NURSE": "OBJ_EVENT_GFX_NURSE",
    "OBJ_EVENT_GFX_GYM_GUIDE": "OBJ_EVENT_GFX_GYM_GUY",
    "OBJ_EVENT_GFX_MAID": "OBJ_EVENT_GFX_WOMAN_1",
    "OBJ_EVENT_GFX_LADY": "OBJ_EVENT_GFX_WOMAN_5",
    "OBJ_EVENT_GFX_SOCIALITE": "OBJ_EVENT_GFX_BEAUTY",
    "OBJ_EVENT_GFX_MIDDLE_AGED_MAN": "OBJ_EVENT_GFX_MAN_2",
    "OBJ_EVENT_GFX_MIDDLE_AGED_WOMAN": "OBJ_EVENT_GFX_WOMAN_4",
    "OBJ_EVENT_GFX_COWGIRL": "OBJ_EVENT_GFX_PICNICKER",
    "OBJ_EVENT_GFX_RANCHER": "OBJ_EVENT_GFX_CAMPER",
    "OBJ_EVENT_GFX_JOGGER": "OBJ_EVENT_GFX_RUNNING_TRIATHLETE_M",
    "OBJ_EVENT_GFX_ROUGHNECK": "OBJ_EVENT_GFX_BIKER",
    "OBJ_EVENT_GFX_PARASOL_LADY": "OBJ_EVENT_GFX_LASS",
    "OBJ_EVENT_GFX_WAITRESS": "OBJ_EVENT_GFX_WOMAN_2",
    "OBJ_EVENT_GFX_WAITER": "OBJ_EVENT_GFX_CHEF",
    "OBJ_EVENT_GFX_ACE_TRAINER_SNOW_F": "OBJ_EVENT_GFX_PICNICKER",
    "OBJ_EVENT_GFX_ACE_TRAINER_SNOW_M": "OBJ_EVENT_GFX_CAMPER",
    "OBJ_EVENT_GFX_SNOWPOINT_NPC_F": "OBJ_EVENT_GFX_WOMAN_3",
    "OBJ_EVENT_GFX_SNOWPOINT_NPC_M": "OBJ_EVENT_GFX_MAN_2",
    "OBJ_EVENT_GFX_BABY_IN_PRAM": "OBJ_EVENT_GFX_LITTLE_BOY",
    "OBJ_EVENT_GFX_MYSTERY_GIFT_DELIVERYMAN": "OBJ_EVENT_GFX_MG_DELIVERYMAN",
}
SPRITE_PADRAO = "OBJ_EVENT_GFX_MAN_1"
MOVIMENTO_PADRAO = "MOVEMENT_TYPE_LOOK_AROUND"

# ponytail: quem atende balcao FICA em tile bloqueado, de proposito, como no jogo
# original. Enfermeira e vendedor sao avisados, nunca movidos.
#
# RECONHECIDO PELO SPRITE TAMBEM, e nao so pelo local_id: medido em 21/08/2026,
# 14 dos 18 vendedores de loja de Sinnoh entraram SEM local_id nenhum, entao a
# regra antiga (substring no local_id) protegia 4 e `--corrigir` moveria os
# outros 14 para um tile chutado pelo anel de busca de `tile_livre_perto`.
ATRAS_DO_BALCAO = ("NURSE", "CLERK", "MART", "RECEP", "ATENDENTE", "CASHIER", "SHOPKEEPER")

LUZ = "OBJ_EVENT_GFX_LIGHT_SPRITE"
FORMA_VAR = re.compile(r"^OBJ_EVENT_GFX_VAR_[0-9A-F]$")

# Comportamentos de metatile em que objeto fica em tile bloqueado POR DESENHO.
# NOMES, resolvidos contra include/constants/metatile_behaviors.h em tempo de
# execucao: numero cravado envelheceria calado no dia em que o enum mudasse.
POR_DESENHO = {
    # agua: e onde Pokemon de overworld nada. O Gyarados do Lake of Rage e os
    # 32 objetos de MB_OCEAN_WATER de Hoenn de fabrica sao isto.
    "MB_POND_WATER", "MB_INTERIOR_DEEP_WATER", "MB_DEEP_WATER", "MB_WATERFALL",
    "MB_SOOTOPOLIS_DEEP_WATER", "MB_OCEAN_WATER", "MB_SHALLOW_WATER",
    "MB_NO_SURFACING", "MB_SEAWEED", "MB_SEAWEED_NO_SURFACING",
    "MB_FAST_WATER", "MB_CYCLING_ROAD_WATER", "MB_WATER_DOOR",
    "MB_WATER_SOUTH_ARROW_WARP",
    # balcao: o MOTOR tem lookup proprio para falar ATRAVES do tile bloqueado.
    "MB_COUNTER",
    # mobiliario do Emerald de fabrica, que a varredura sem --so-sinnoh cruza.
    "MB_SECRET_BASE_WALL", "MB_SECRET_BASE_NORTH_WALL", "MB_SECRET_BASE_PC",
    "MB_BERRY_TREE_SOIL", "MB_BOOKSHELF", "MB_BLUEPRINT",
}

_MB = None


def nomes_de_comportamento():
    """{valor: nome} do enum de include/constants/metatile_behaviors.h.

    Tira comentario ANTES de quebrar por virgula: ver a armadilha do cabecalho.
    """
    global _MB
    if _MB is None:
        txt = open(os.path.join(REPO,
                                "include/constants/metatile_behaviors.h")).read()
        corpo = re.search(r"enum\s*\w*\s*\{(.*?)\}", txt, re.S).group(1)
        corpo = re.sub(r"/\*.*?\*/", "", corpo, flags=re.S)
        corpo = "\n".join(l.split("//")[0] for l in corpo.split("\n"))
        _MB, atual = {}, 0
        for item in corpo.split(","):
            item = item.strip()
            if not item:
                continue
            if "=" in item:
                nome, valor = item.split("=")
                atual, nome = int(valor.strip(), 0), nome.strip()
            else:
                nome = item
            _MB[atual] = nome
            atual += 1
    return _MB


def comportamento(layouts, layout_id, x, y):
    """Nome do comportamento do metatile em (x,y), ou None se nao der para ler.

    Reusa `valida_warp_tile.tabela_de_atributos`, que ja sabe deduzir a largura
    do atributo (2 bytes em Emerald, 4 em FRLG) e onde mora cada tileset.
    """
    import valida_warp_tile as W
    L = layouts[layout_id]
    if not (0 <= x < L["width"] and 0 <= y < L["height"]):
        return None
    with open(os.path.join(REPO, L["blockdata_filepath"]), "rb") as f:
        f.seek((y * L["width"] + x) * 2)
        dados = f.read(2)
    if len(dados) < 2:
        return None
    mt = struct.unpack("<H", dados)[0] & 0x3FF
    # O corte primario/secundario e a CONSTANTE do motor (512), nunca o tamanho
    # do arquivo: gTileset_Building tem 8 metatiles e e primario mesmo assim.
    if mt < 512:
        tab = W.tabela_de_atributos(L["primary_tileset"])[0] or []
        idx = mt
    else:
        tab = W.tabela_de_atributos(L["secondary_tileset"])[0] or []
        idx = mt - 512
    if idx >= len(tab):
        return None
    return nomes_de_comportamento().get(tab[idx])


def da_para_falar(layouts, layout_id, mapa, x, y):
    """True se o jogador alcanca algum vizinho ORTOGONAL do tile (x,y).

    ESTA E A REGRA DO MOTOR, e ela chegou tarde: `TryStartInteractionScript`
    olha o objeto do tile que o jogador ENCARA, e o tile do objeto pode ser
    bloqueado sem problema nenhum. Ou seja NPC em parede so e defeito quando o
    jogador nunca consegue ficar de frente para ele.

    MEDIDO na marra em 21/08/2026: sem esta regra o validador acusou o
    cientista do portao norte da Route 206 em (6,4), e ele esta ali DE
    PROPOSITO, atras do balcao do portao, com o T100.14 da suite passando por
    aquele tile desde 18/08 ("o cientista, que fica em (6,4), tile de parede;
    falar com NPC atras de balcao e legal neste motor"). Mover os tres NPCs que
    a regra crua acusou quebrou o T100.14 na hora. Regra que reprova o jogo que
    ja passa na suite esta errada (licao 4.10 do ESTADO), e a camada certa aqui
    e a alcancabilidade do vizinho, nao a colisao do proprio tile.
    """
    import importa_npcs_sinnoh as I
    W, H, g = I.grade(layouts, layout_id)
    base = I.alcancaveis(W, H, g, mapa.get("warp_events") or [])
    return any((x + dx, y + dy) in base
               for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)))


def fica_ai_de_proposito(o, layouts, layout_id, mapa=None):
    """(True, motivo) quando o objeto em tile bloqueado NAO e defeito."""
    gfx = o.get("graphics_id", "") or ""
    if FORMA_ESPECIE.match(gfx):
        return True, "Pokemon de overworld"
    if gfx == LUZ:
        return True, "efeito de luz"
    if FORMA_VAR.match(gfx):
        return True, "sprite resolvido em tempo de execucao"
    b = comportamento(layouts, layout_id, o["x"], o["y"])
    if b in POR_DESENHO:
        return True, b
    if mapa is not None and da_para_falar(layouts, layout_id, mapa,
                                          o["x"], o["y"]):
        return True, f"{b}, mas o jogador encara o tile de um vizinho alcancavel"
    return False, b or "comportamento ilegivel"


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


# Pokémon de overworld NÃO mora na tabela de ponteiros: `OBJ_EVENT_GFX_SPECIES(X)`
# é macro que soma OBJ_EVENT_MON à espécie, e o desenho vem de
# `gSpeciesInfo[X].overworldData` (src/event_object_movement.c,
# SpeciesToGraphicsInfo), ligado porque OW_POKEMON_OBJECT_EVENTS é TRUE.
#
# ACHADO em 19/08/2026, e ele era uma armadilha de verdade: o validador contava
# TODA forma de macro como "sprite que esta build não desenha", e com
# `--corrigir` trocaria cada uma por OBJ_EVENT_GFX_MAN_1. Antes desta leva eram
# 6 objetos (os ARIADOS do ginásio de Azalea e companhia) e ninguém tropeçou;
# depois que `restaura_gfx_johto.py` devolveu 775 Pokémon de overworld a Johto,
# um `--corrigir` distraído viraria 781 Pokémon em homens de camisa vermelha.
FORMA_ESPECIE = re.compile(
    r"^OBJ_EVENT_GFX_SPECIES(?:_SHINY|_FEMALE|_SHINY_FEMALE)?\("
    r"\s*[A-Z0-9_]+\s*\)$")


def desenhavel(gfx, sprites):
    """O gráfico existe nesta build, na tabela de ponteiros OU como espécie."""
    return gfx in sprites or bool(FORMA_ESPECIE.match(gfx or ""))


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


def tile_livre_perto(layouts, layout_id, x, y, raio=6, mapa=None):
    """Para onde mover um objeto enterrado em parede. None quando não há alvo.

    ANDÁVEL NÃO BASTA, TEM QUE SER ALCANÇÁVEL E VAZIO, e isso mudou em
    21/08/2026 porque a versão antiga escolhia mal nos três casos reais que
    existiam. Ela varria o anel em ordem de `dx` e devolvia o PRIMEIRO tile de
    colisão zero, sem perguntar se o jogador chega nele nem se já tem alguém em
    cima: para o BARRY de OreburghCity ela apontava (7,13) em vez de (8,13),
    para o SCIENTIST da Route206_North (5,3) em vez de (5,4), e para o GRUNT_2
    do SpearPillar (12,11), que é WARP. Mover NPC para tile ilhado ou para cima
    de warp troca um defeito por outro mais difícil de ver.

    A régua nova é a mesma do resto da casa: `importa_npcs_sinnoh.alcancaveis`,
    ou seja BFS com regra de elevação semeada pelos warps do mapa. Empate se
    resolve pela distância de Manhattan e, dentro dela, pela ordem estável
    (y, x). Medido: nos três casos reais o candidato de distância 1 é ÚNICO,
    então desempate por direção de olhar seria código sem cliente.
    """
    import importa_npcs_sinnoh as I
    if mapa is None:
        return None
    W, H, g = I.grade(layouts, layout_id)
    base = I.alcancaveis(W, H, g, mapa.get("warp_events") or [])
    ocupados = {(o["x"], o["y"]) for o in (mapa.get("object_events") or [])
                if isinstance(o.get("x"), int) and isinstance(o.get("y"), int)}
    ocupados |= {(w["x"], w["y"]) for w in (mapa.get("warp_events") or [])}
    cands = sorted(
        (abs(cx - x) + abs(cy - y), cy, cx)
        for cx, cy in base if (cx, cy) not in ocupados
        and abs(cx - x) + abs(cy - y) <= raio)
    return (cands[0][2], cands[0][1]) if cands else None


_GLOBAIS = None


def rotulos_da_unidade():
    """Todo rótulo definido na UNIDADE DE MONTAGEM, como um conjunto.

    Quem reprova um script inexistente é o assembler, e a pergunta dele não é
    "o rótulo está no scripts.inc DESTE mapa": `data/event_scripts.s` inclui os
    dois mil `scripts.inc` num arquivo só, e um mapa pode apontar para rótulo de
    outro. A versão anterior lia só o arquivo do próprio mapa mais
    `data/scripts/*.inc`, e por isso acusava `Route26North` de citar
    `Route26_EventScript_Jake` "inexistente", quando ele está em
    `data/maps/Route26/scripts.inc` desde sempre, incluído e montado. Dois
    falsos positivos que já mandaram um agente procurar bug que não existia.

    Conjunto, e não texto concatenado: a busca por substring casava
    `Foo_EventScript_Npc1` dentro de `Foo_EventScript_Npc10` (lição 4.9).
    """
    global _GLOBAIS
    if _GLOBAIS is None:
        raiz = os.path.join(REPO, "data/event_scripts.s")
        txt = open(raiz, errors="replace").read()
        arquivos = [raiz] + [os.path.join(REPO, i)
                             for i in re.findall(r'\.include\s+"([^"]+)"', txt)]
        _GLOBAIS = set()
        for p in arquivos:
            if not os.path.exists(p):
                continue
            _GLOBAIS |= set(re.findall(r"^(\w+):{1,2}\s*$",
                                       open(p, errors="replace").read(), re.M))
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

    total = {"sprite": 0, "movimento": 0, "bloqueado": 0, "por_desenho": 0,
             "fora": 0, "script": 0}
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
        rotulos = rotulos_da_unidade()

        for o in objs:
            if not desenhavel(o.get("graphics_id", SPRITE_PADRAO), sprites):
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
                proposital, porque = fica_ai_de_proposito(o, layouts, d["layout"], d)
                if proposital:
                    total["por_desenho"] += 1
                    continue
                total["bloqueado"] += 1
                balcao = any(t in o.get("local_id", "") or t in o.get("graphics_id", "")
                             for t in ATRAS_DO_BALCAO)
                novo = None if balcao else tile_livre_perto(
                    layouts, d["layout"], o["x"], o["y"], mapa=d)
                if balcao:
                    print(f"  {nome}: {o.get('local_id','?')} em tile bloqueado ({porque}), mas atende balcao: mantido")
                else:
                    print(f"  {nome}: {o.get('local_id','?')} ({o.get('graphics_id')}) enterrado em ({o['x']},{o['y']}), {porque} -> {novo}")
                if CORRIGIR and novo:
                    o["x"], o["y"] = novo
                    alterou = True

        for ev in objs + d.get("bg_events", []):
            # ponytail: "0", "0x0" e "NULL" querem dizer "objeto sem script", que e
            # normal. Contar isso como rotulo faltando gerou 765 falsos positivos
            # na primeira varredura do jogo inteiro, e chegou a assustar um agente.
            SEM_SCRIPT = ("0", "0x0", "0X0", "NULL", "null")
            if ev.get("script") and str(ev["script"]) not in SEM_SCRIPT \
                    and ev["script"] not in rotulos:
                total["script"] += 1
                print(f"  {nome}: script {ev['script']} NAO existe no scripts.inc")

        if alterou:
            json.dump(d, open(caminho, "w"), indent=2, ensure_ascii=False)
            mapas_tocados += 1

    print("\nresumo:", total)
    print("mapas corrigidos:" if CORRIGIR else "mapas com problema:", mapas_tocados)
    return 1 if total["script"] or total["fora"] else 0


def demo():
    """MUTACAO PLANTADA: o validador TEM que acusar objeto enterrado em parede.

    Sem esta prova a checagem 4 seria enfeite, e enfeite deixa passar NPC que o
    jogador nunca alcanca. Roda contra mapa de verdade, nunca contra grade
    inventada, e nao grava nada.
    """
    layouts = {l["id"]: l for l in json.load(
        open(os.path.join(REPO, "data/layouts/layouts.json")))["layouts"]}

    # 1. o parser de comportamento nao pode estar deslocado. `MB_DEEP_WATER`
    #    existir e a prova de que o comentario saiu antes da virgula, e
    #    `MB_COUNTER` em 0x80 e a prova do valor certo do outro lado do enum.
    nomes = nomes_de_comportamento()
    assert nomes[0x00] == "MB_NORMAL", nomes[0x00]
    assert nomes[0x12] == "MB_DEEP_WATER", nomes[0x12]
    assert nomes[0x80] == "MB_COUNTER", nomes[0x80]
    assert POR_DESENHO <= set(nomes.values()), POR_DESENHO - set(nomes.values())

    # 2. MUTACAO PLANTADA em RavagedPath, que e mapa de verdade: (12,12) e
    #    parede macica (a pedra da fonte que este porte nao consegue por), e
    #    (11,12) e o corredor ao lado, onde uma pedra JA esta gravada.
    d = json.load(open(os.path.join(REPO, "data/maps/RavagedPath/map.json")))
    lay = d["layout"]
    assert colisao(layouts, lay, 12, 12) != 0, "a parede plantada sumiu"
    assert colisao(layouts, lay, 11, 12) == 0, "o corredor plantado sumiu"
    homem = {"graphics_id": "OBJ_EVENT_GFX_MAN_1", "x": 12, "y": 12}
    assert fica_ai_de_proposito(homem, layouts, lay)[0] is False
    # e com o mapa na mao a resposta continua False, porque (12,12) esta
    # cercado de tile ILHADO: nao ha de onde encarar o coitado
    assert fica_ai_de_proposito(homem, layouts, lay, d)[0] is False
    # e o MESMO sprite no corredor nem chega a esta pergunta: a colisao e zero
    assert colisao(layouts, lay, 11, 12) == 0

    # 3. os tres perdoes, um a um, e cada um no tile em que ele importa
    mon = {"graphics_id": "OBJ_EVENT_GFX_SPECIES(MISDREAVUS)", "x": 12, "y": 12}
    assert fica_ai_de_proposito(mon, layouts, lay)[0] is True
    luz = {"graphics_id": LUZ, "x": 12, "y": 12}
    assert fica_ai_de_proposito(luz, layouts, lay)[0] is True
    var = {"graphics_id": "OBJ_EVENT_GFX_VAR_0", "x": 12, "y": 12}
    assert fica_ai_de_proposito(var, layouts, lay)[0] is True

    # 4. o balcao de loja de Sinnoh e MB_COUNTER de verdade, lido do disco, e e
    #    por isso que os 20 atendentes saem da acusacao. Se um dia o tileset
    #    mudar, este assert cai antes de a contagem mentir.
    dm = json.load(open(os.path.join(REPO, "data/maps/CanalaveCityMart/map.json")))
    assert colisao(layouts, dm["layout"], 2, 3) != 0
    assert comportamento(layouts, dm["layout"], 2, 3) == "MB_COUNTER"
    vendedor = {"graphics_id": "OBJ_EVENT_GFX_MART_EMPLOYEE", "x": 2, "y": 3}
    assert fica_ai_de_proposito(vendedor, layouts, dm["layout"])[0] is True
    # e o mesmo vendedor numa parede de caverna volta a ser acusado
    assert fica_ai_de_proposito(
        {"graphics_id": "OBJ_EVENT_GFX_MART_EMPLOYEE", "x": 12, "y": 12},
        layouts, lay)[0] is False

    # 5. O ALVO DE `--corrigir` tem que ser ALCANÇÁVEL e VAZIO. Prova plantada
    #    em RavagedPath, o mapa com 257 tiles andáveis e ilhados: (12,12) é
    #    parede, o vizinho (11,12) é andável mas ILHADO, e a versão antiga de
    #    `tile_livre_perto` mandaria o NPC justamente para lá. Esta é a
    #    mutação: o alvo devolvido nunca pode ser um tile fora do alcance.
    Wr, Hr, gr = __import__("importa_npcs_sinnoh").grade(layouts, lay)
    alcance = __import__("importa_npcs_sinnoh").alcancaveis(
        Wr, Hr, gr, d.get("warp_events") or [])
    assert colisao(layouts, lay, 11, 12) == 0 and (11, 12) not in alcance
    alvo = tile_livre_perto(layouts, lay, 12, 12, mapa=d)
    assert alvo is None or alvo in alcance, alvo
    # sem `mapa` a função se recusa a chutar, em vez de devolver tile qualquer
    assert tile_livre_perto(layouts, lay, 12, 12) is None

    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
