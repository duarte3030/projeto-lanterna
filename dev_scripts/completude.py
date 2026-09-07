#!/usr/bin/env python3
"""Quanto de cada regiao ja esta pronto, medido CONTRA A FONTE dela, MAPA A MAPA.

Uso:
    python3 dev_scripts/completude.py
    python3 dev_scripts/completude.py --detalhe Johto

Existe porque numero cru nao significa nada. "82% dos warps disparam" nao diz se
isso e bom: o proprio jogo original nunca chega a 100%, porque muita porta e
trocada por script em tempo de execucao e muito warp so e usado por barco ou
cutscene, sem ninguem pisar nele.

A regua certa e a FONTE. 100% quer dizer "tao completo quanto o jogo de onde a
regiao veio", nao "perfeito".

    Hoenn  -> pret/pokeemerald   (nossa Hoenn e o vanilla; deve dar ~100%)
    Kanto  -> pret/pokefirered
    Johto  -> fontes-mapas/hns
    Sinnoh -> fontes-mapas/sinnoh

PRIMEIRA VERSAO ESTAVA ERRADA e vale registrar: ela casava por NOME DE GRUPO de
mapa. As fontes usam outros nomes de grupo, entao o denominador pegava um punhado
de mapas e Johto saiu com "833% dos mapas" e Hoenn com 270%. Numero acima de 100
era o unico motivo de eu ter olhado de novo; se tivesse dado 91% eu teria
acreditado. **Comparacao so vale se os dois lados falarem do mesmo conjunto**, e
o unico jeito de garantir isso e casar MAPA A MAPA pelo nome.

Regiao sem fonte em disco aparece como "sem fonte", nunca como 100%. Nao saber e
um resultado; fingir que sabe foi o erro que esta sessao cometeu a noite toda.
"""
import collections
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = os.path.dirname(RAIZ) + "/fontes-mapas"

REGIOES = {
    "Kanto":  {"grupo": "Frlg",           "fonte": f"{FONTES}/pokefirered"},
    "Johto":  {"grupo": "Johto",          "fonte": f"{FONTES}/hns"},
    "Hoenn":  {"grupo": "TownsAndRoutes", "fonte": f"{FONTES}/pokeemerald"},
    # Sinnoh saiu de fontes-mapas/sinnoh para o pokeplatinum em 05/08/2026. O
    # motivo esta na ARMADILHA da funcao p(): a fonte antiga tem ZERO NPC nos
    # mapas de Sinnoh, entao ela media "objetos" contra um denominador vazio e
    # imprimia "fonte 0". O pokeplatinum tem os 2278 objetos de verdade, so que
    # em outro formato (events_*.json ligados por MAP_HEADER). Ver le_plat().
    # Sinnoh passa de 100% em placas (105,1% em 05/08/2026) e isso esta CERTO:
    # o denominador e so o Platinum, mas a geometria de Sinnoh veio do
    # fontes-mapas/sinnoh, que ja trazia placa propria. Medido: 31 placas a mais
    # espalhadas por 24 mapas, no maximo 2 por mapa. Nao e conversao gerando
    # placa falsa, e soma de duas fontes.
    # A COLUNA `warps` PASSOU DE 100 EM 21/08/2026 (100,6%), pelo mesmo motivo
    # e vale medir antes de acreditar: os `CORTES_DO_GUI` tiraram do
    # denominador justamente os mapas que carregavam DÉFICIT de warp (o Battle
    # Zone, o Turnback), e nos que ficaram somamos 164 warps a mais que o
    # Platinum contra 157 a menos. O saldo é +7 e vem quase todo de UM mapa, o
    # `GalacticHQ_B1F`, com 25 warps contra 2 da fonte. Ou seja o excedente é
    # anterior ao corte e mora ali; o corte só parou de escondê-lo.
    "Sinnoh": {"grupo": "Sinnoh",         "fonte": f"{FONTES}/pokeplatinum",
               "plat": True},
}

CAMPOS = [("object_events", "objetos (NPC, item)"),
          ("warp_events", "warps"),
          ("bg_events", "placas e sinais")]

# Piso de ARTE: abaixo disto o mapa nao e desenho, e mascara de colisao.
#
# Existe porque a tabela de cima nao enxerga arte, e isso deixou uma regiao
# inteira passar por 94% completa por SEIS DIAS. A licao ficou, mesmo depois de
# a regiao sair do escopo: ela tinha os 1396 NPCs, os 1060 warps e as 497 placas
# nos lugares certos, dentro de caixas com TRES metatiles distintos (chao,
# parede e porta). Presenca de evento nao e desenho.
#
# O piso e 10 e nao 3 porque 3 era o sintoma daquele bug especifico; 10 e o
# ponto onde um mapa deixa de ter mobilia. Mapa minusculo legitimo cai aqui de
# vez em quando (elevador com 4 metatiles distintos na FONTE tambem ja foi
# medido), entao a coluna diz "mediana (quantos abaixo)": o numero entre
# parenteses e para investigar, nao para acusar.
PISO_ARTE = 10


def todos_os_mapas(raiz):
    p = f"{raiz}/data/maps/map_groups.json"
    if not os.path.exists(p):
        return {}
    g = json.load(open(p))
    return {m: grp for grp in g.get("group_order", []) for m in g.get(grp, [])}


def tumulos(_cache=set()):
    """Mapa que SAIU do escopo: o `map.json` continua existindo, com o id
    intacto, sem evento nenhum e com o campo `cortado_por` dizendo qual decisao
    o tirou. E assim que este projeto marca tumulo.

    A regua filtra por ESSE CAMPO, e nao por nome de pasta, porque o mesmo teste
    cobre os dois tipos de tumulo que existem hoje: os 729 de Unova e Galar, que
    sairam no cartucho 1, e os 102 de Sinnoh, que ja existiam desde 22/08/2026.
    Sem o filtro, os tumulos sem prefixo de regiao caem no balde de Hoenn (ele e
    "tudo que nao e das outras tres") e envenenam a coluna de ARTE, que mede
    TODOS os nossos mapas da regiao e nao so os casados com a fonte.
    """
    if not _cache:
        for m in todos_os_mapas(RAIZ):
            p = f"{RAIZ}/data/maps/{m}/map.json"
            if os.path.exists(p) and "cortado_por" in json.load(open(p)):
                _cache.add(m)
    return _cache


def nossos_da_regiao(mapa_grupo, chave):
    if chave == "TownsAndRoutes":
        # Hoenn e "tudo que nao e das outras tres".
        outras = ("frlg", "johto", "sinnoh")
        nossos = [m for m, g in mapa_grupo.items()
                  if not any(o in g.lower() or o in m.lower() for o in outras)]
    else:
        nossos = [m for m, g in mapa_grupo.items()
                  if chave.lower() in g.lower() or chave.lower() in m.lower()]
    return [m for m in nossos if m not in tumulos()]


# Mapa que a FONTE tem e que JÁ ESTÁ na ROM com outro nome.
#
# Existe porque em 21/08/2026 a régua dizia que faltavam 10 mapas em Johto que
# estão jogáveis desde sempre, só que com sufixo de outra região.
# `cidades_de_outra_fonte()` já desconta 732 mapas assim, mas ela casa pelo
# PREFIXO DE CIDADE (o pedaço antes do primeiro "_"), e o prefixo destes 10 não
# é nome de cidade nenhum: "CeruleanCave1", "SafariZone1", "VictoryRoadKanto_1F".
#
# A tabela é EXPLÍCITA de propósito. Heurística que casasse "OaksLab" com
# "PalletTown_ProfessorOaksLab_Frlg" seria solta o bastante para casar mapa
# diferente, e casamento errado não aparece como erro: aparece como completude
# alta. Cada linha abaixo traz a medida que provou o par.
APELIDOS_FONTE = {
    # --- Johto (fonte `hns`, que é hack de Johto E Kanto). A nossa versão
    # destes veio do pokefirered, com sufixo _Frlg.
    # Topologia: CeruleanCave1 warpa para 2 e para 3 (é o térreo), CeruleanCave3
    # só warpa de volta para o 1 (é o andar sem saída). Igual ao FRLG, onde o 1F
    # liga 2F e B1F. Os três layouts têm 39-40 x 23 nos dois lados.
    "CeruleanCave1": "CeruleanCave_1F_Frlg",
    "CeruleanCave2": "CeruleanCave_2F_Frlg",
    "CeruleanCave3": "CeruleanCave_B1F_Frlg",
    # Safári: casado por DIMENSÃO de layout, que bate exata nos três.
    # LAYOUT_SAFARI_ZONE1 é 51x36 como o nosso SAFARI_ZONE_CENTER; o 2 é 54x35
    # como o EAST; o 3 é 48x36 como o WEST.
    "SafariZone1": "SafariZone_Center_Frlg",
    "SafariZone2": "SafariZone_East_Frlg",
    "SafariZone3": "SafariZone_West_Frlg",
    # O "indoor" é 13x11 e o único warp dele volta para o SafariZone2, ou seja é
    # a casa de descanso da área LESTE.
    "SafariZoneIndoor": "SafariZone_East_RestHouse_Frlg",
    # Estrada da Vitória de Kanto: o hns conta os andares para BAIXO e o FRLG
    # para cima. O 1F dos dois abre na Route 23; o último andar dos dois (B2F lá,
    # 3F aqui) é o que sai no Planalto Índigo.
    "VictoryRoadKanto_1F": "VictoryRoad_1F_Frlg",
    "VictoryRoadKanto_B1F": "VictoryRoad_2F_Frlg",
    "VictoryRoadKanto_B2F": "VictoryRoad_3F_Frlg",
}


TODOS_OS_CAMPOS = tuple(c for c, _ in CAMPOS)

# Mapa que a FONTE tem e que NÃO ENTRA NESTE PORTE, por decisão do Gui.
#
# Existe porque escopo é decisão dele, e decisão que não vira RÉGUA MEDIDA
# envelhece: até 21/08/2026 a completude cobrava o Battle Zone inteiro, o
# Underground e os mapas de Mystery Gift, que nunca vão existir aqui, e o
# denominador media o Platinum em vez de medir a obra.
#
# Três modos, os do inventário de cortes que produziu esta tabela mais o de
# OBJETO, aberto em 23/08/2026:
#
#   "mapa_fonte"   -> o `alvo` é REGEX, casada contra os nomes que a fonte tem
#                     e nós não. O registro sai da coluna `mapas`.
#   "deficit"      -> o `alvo` é LISTA DE NOMES DE MAPA NOSSO, e só o BURACO
#                     dos campos citados sai do denominador: o mapa passa a
#                     valer 100% naqueles campos (ver `corta_campo`). É o modo
#                     de mapa que EXISTE na ROM e vai continuar existindo, mas
#                     que ninguém vai terminar de povoar.
#   "objeto_fonte" -> o `alvo` é REGEX casada contra o `graphics_id` de cada
#                     OBJETO da fonte, e o objeto que casa sai do denominador
#                     da coluna `objetos` em TODOS os mapas da região. É o modo
#                     do mobiliário: o mapa fica, a obra dele fica, e só aquele
#                     tipo de registro é que nunca vai virar objeto nosso.
#
#                     A TRAVA que o torna honesto, conferida em
#                     `confere_cortes` e travada no `--demo`: o gráfico cortado
#                     tem que ter ZERO ocorrências nos NOSSOS map.json da
#                     região. Cortar do denominador um gráfico que nós usamos
#                     seria contá-lo só de um lado, e a coluna subiria sem obra
#                     nenhuma, que é o jeito mais caro de errar nesta casa.
#
# O que cada linha tirou sai em `--detalhe <região>`: corte que não é visível
# vira completude alta sem obra, que é a mentira mais cara desta casa.
#
# NÃO ESTÁ AQUI, de propósito, e cada ausência é decisão dele de 21/08/2026: o
# **Distortion World** (fica, com gravidade normal), os 8 ginásios de Sinnoh
# (ficam; a arte é obra de outro executor), o **Bug Contest** de Johto, e os 4
# moldes que sobram (IronIsland, MtCoronetOutsideNorth, MtCoronetOutsideSouth,
# Route204North). Dos 7 `UNUSED_*` da fonte de Sinnoh que têm conteúdo, ficam
# 3: os outros 4 (Battle Park e o mart do Resort) moram DENTRO da Battle Zone e
# saem com ela, por correção do condutor em 21/08/2026.
CORTES_DO_GUI = [
    # ---------------------------------------------------------------- Sinnoh
    dict(regiao="Sinnoh", grupo="Battle Zone: a ilha inteira de pós-Liga",
         modo="deficit", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="ilha que só abre depois da Liga, com o Battle Frontier de gen "
                "4 e suas cinco instalações dentro; a ROM já tem o Battle "
                "Frontier de Hoenn inteiro",
         alvo=["FightArea", "FightAreaMart", "FightAreaMiddleHouse",
               "FightAreaPokecenter1F", "FightAreaPokecenter2F",
               "FightAreaPokecenterB1F", "FightAreaSouthHouse",
               "SurvivalArea", "SurvivalAreaMart", "SurvivalAreaNorthHouse",
               "SurvivalAreaPokecenter1F", "SurvivalAreaPokecenter2F",
               "SurvivalAreaPokecenterB1F", "SurvivalAreaSouthHouse",
               "ResortArea", "ResortAreaHouse", "ResortAreaPokecenter1F",
               "ResortAreaPokecenter2F", "ResortAreaPokecenterB1F",
               "ResortAreaRibbonSyndicate1F", "ResortAreaRibbonSyndicateElevator",
               "Villa",
               "Route225", "Route225House", "Route225_Access",
               "Route226", "Route226_Access", "Route227", "Route227House",
               "Route228", "Route228GateToRoute226", "Route228NorthHouse",
               "Route228RockPeakRuins", "Route228SouthHouse",
               # Acrescentado em 22/08/2026 pelo condutor, depois que a remoção
               # física mediu: o ÚNICO warp da `RockPeakRuins` ia para a
               # `Route228`, e sem ela o mapa fica sem caminho nenhum. Ele é a
               # sala das Ruínas do Pico de Pedra, dentro da Battle Zone, e a
               # ordem do Gui foi a ilha inteira. As irmãs `IronRuins` e
               # `IcebergRuins` NÃO entram, e foi medido: elas saem da
               # `IronIslandB3F` e do `MtCoronet_1F_North_Room2`, dois mapas
               # vivos, e continuam alcançáveis.
               "RockPeakRuins",
               "Route229", "Route230",
               "StarkMountainOutside", "StarkMountainRoom1",
               "StarkMountainRoom2", "StarkMountainRoom3",
               "BattleFrontier", "BattleFrontierGateToFightArea", "BattleTower",
               "BattleHall", "BattleFactory", "BattleCastle", "BattleArcade",
               "Battleground"]),
    dict(regiao="Sinnoh", grupo="Battle Zone: o que só a fonte tem",
         modo="mapa_fonte", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="salas internas da Battle Tower de gen 4, o 2F do Ribbon "
                "Syndicate e os 4 `UNUSED_*` que moram DENTRO da Battle Zone "
                "(Battle Park e o mart do Resort): a ordem foi a ilha inteira, "
                "e mapa não usado que fica dentro dela sai com ela",
         alvo=r"BATTLE_TOWER|RIBBON_SYNDICATE|UNUSED_BATTLE_PARK"
              r"|UNUSED_RESORT_AREA_MART"),
    dict(regiao="Sinnoh", grupo="Pokémon Mansion e Trophy Garden (Route 212)",
         modo="deficit", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="a mansão e o jardim do Sr. Backlot, cujo conteúdo é sorteio "
                "diário de Pokémon e caça a estatueta",
         alvo=["PokemonMansion", "PokemonMansionMaidsRoom",
               "PokemonMansionOffice", "TrophyGarden"]),
    dict(regiao="Sinnoh", grupo="Turnback Cave, Sendoff Spring e Spring Path",
         modo="deficit", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="labirinto de pilares gerado por RNG, pós-jogo; o Giratina "
                "passa a morar no Distortion World, que FICA no escopo",
         alvo=["SendoffSpring", "SpringPath", "TurnbackCaveEntrance",
               "TurnbackCavePillarRoom", "TurnbackCaveGiratinaRoom"]
              + [f"TurnbackCavePillar{p}Room{s}"
                 for p in (1, 2, 3) for s in range(1, 7)]),
    dict(regiao="Sinnoh", grupo="Great Marsh (o Safari de gen 4)",
         modo="deficit", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="Safari com bloco, lama e contador de passos de gen 4; o "
                "Safari de Hoenn é outro jogo e continua na ROM",
         alvo=["GreatMarsh6"]),
    dict(regiao="Sinnoh", grupo="Great Marsh: as 5 áreas que só a fonte tem",
         modo="mapa_fonte", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="mesmo motivo do GreatMarsh6", alvo=r"GREAT_MARSH"),
    dict(regiao="Sinnoh", grupo="Amity Square", modo="deficit",
         campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="passear com o Pokémon seguindo; OW_FOLLOWERS_ENABLED é FALSE "
                "em include/config/overworld.h (decisão 3, 16/08/2026)",
         alvo=["AmitySquare", "HearthomeCityWestGateToAmitySquare",
               "HearthomeCityEastGateToAmitySquare"]),
    dict(regiao="Sinnoh", grupo="Pal Park", modo="deficit",
         campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="migração de GBA para DS; não há de onde migrar",
         alvo=["PalPark", "PalParkLobby"]),
    dict(regiao="Sinnoh", grupo="Underground (mineração e base secreta)",
         modo="mapa_fonte", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="subterrâneo é minigame de tela dupla mais troca local",
         alvo=r"UNDERGROUND"),
    dict(regiao="Sinnoh", grupo="Palco de Contest", modo="deficit",
         campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="concurso de gen 4 (ritmo por toque) não tem motor aqui; o "
                "Contest de Hoenn continua na ROM e o saguão fica de pé",
         alvo=["ContestHallStageNoContest"]),
    dict(regiao="Sinnoh", grupo="Palco de Contest em andamento (só a fonte)",
         modo="mapa_fonte", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="variante do palco com concurso rolando",
         alvo=r"CONTEST_HALL_STAGE"),
    dict(regiao="Sinnoh", grupo="Pokétch Company", modo="deficit",
         campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="o Pokétch é a tela de baixo do DS (decisão 3, 16/08/2026)",
         alvo=["JubilifeCity_PoketchCompany_F1",
               "JubilifeCity_PoketchCompany_F2",
               "JubilifeCity_PoketchCompany_F3"]),
    dict(regiao="Sinnoh", grupo="GTS (Global Terminal)", modo="deficit",
         campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="troca global por Wi-Fi (decisão 3, 16/08/2026)",
         alvo=["GlobalTerminal1F", "GlobalTerminal2F", "GlobalTerminal3F"]),
    dict(regiao="Sinnoh", grupo="2º andar Wi-Fi dos Pokécenters",
         modo="deficit", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="o 2F de gen 4 é só Union Room e Colosseum de Wi-Fi: sem "
                "multiplayer não sobra nada jogável lá em cima",
         alvo=["CanalaveCityPokecenter2F", "CelesticTownPokecenter2F",
               "EternaCityPokecenter2F", "HearthomeCityPokecenter2F",
               "PastoriaCityPokecenter2F", "PokemonLeagueNorthPokecenter2F",
               "PokemonLeagueSouthPokecenter2F", "SnowpointCityPokecenter2F",
               "SolaceonTownPokecenter2F", "SunyshoreCityPokecenter2F",
               "VeilstoneCityPokecenter2F"]),
    dict(regiao="Sinnoh", grupo="Union Room, Wi-Fi e Record Mixing",
         modo="mapa_fonte", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="multiplayer de DS: não existe em GBA de um jogador",
         alvo=r"UNION_ROOM|COMMUNICATION_CLUB|WIFI_PLAZA|GLOBAL_RANKING"
              r"|RECORD_MIXING"),
    dict(regiao="Sinnoh", grupo="Elevadores da Liga e corredor do Hall",
         modo="deficit", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="cena de elevador entre as salas da Elite; a nossa Liga liga "
                "sala a sala por warp",
         alvo=["PokemonLeagueElevatorToAaronRoom"]),
    dict(regiao="Sinnoh", grupo="Elevadores da Liga (só a fonte)",
         modo="mapa_fonte", campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="os outros quatro elevadores e o corredor do Hall of Fame",
         alvo=r"POKEMON_LEAGUE_ELEVATOR|HALLWAY_TO_HALL_OF_FAME"),
    dict(regiao="Sinnoh", grupo="Mapas de Mystery Gift", modo="mapa_fonte",
         campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="só abrem com item de distribuição, e Mystery Gift não existe "
                "aqui (decisão 6 do plano de Sinnoh). Os lendários DELES não "
                "são cortados: outro executor os realoca (ver PLANO-ESCOPO.md)",
         alvo=r"FULLMOON|NEWMOON|FLOWER_PARADISE|HALL_OF_ORIGIN|SEABREAK"),
    dict(regiao="Sinnoh", grupo="Game Corner de Veilstone", modo="deficit",
         campos=TODOS_OS_CAMPOS, data="21/08/2026",
         motivo="caça-níquel de gen 4, minigame sem motor aqui. SÓ ELE: o Bug "
                "Contest de Johto fica, por decisão do Gui no mesmo dia",
         alvo=["GameCorner"]),
    # Os dois cortes de OBJETO de Sinnoh, decisão do Gui em 23/08/2026 ("vamos
    # completar Sinnoh" e "normalizar a porcentagem com base no que realmente
    # vai ficar"). Eles não tiram mapa nenhum do porte: tiram do denominador da
    # coluna `objetos` os REGISTROS que nunca vão virar objeto nosso, e por isso
    # o modo é `objeto_fonte` e não `deficit`.
    #
    # MEDIDO no dia, e é o que autoriza os dois: nenhum dos três gráficos tem
    # UMA ocorrência sequer nos nossos `data/maps/*/map.json`. Eles são
    # denominador puro, então tirá-los não conta nada duas vezes.
    dict(regiao="Sinnoh", grupo="Mobiliário sem mecânica: respiro e balizador",
         modo="objeto_fonte", campos=("object_events",), data="23/08/2026",
         motivo="`VENT` (o respiro de calçada, 55 registros em 14 mapas) e "
                "`BOLLARD` (o balizador de rua, 8 em 3) são DESENHO com "
                "colisão, sem fala, sem item e sem gatilho. Este motor não tem "
                "objeto decorativo sólido: o que existe é NPC, e NPC de pé em "
                "cima de respiro de calçada faz o mapa mentir (decisão 4 do "
                "importador de Sinnoh). Onde eles importam, o desenho já está "
                "no tileset",
         alvo=r"OBJ_EVENT_GFX_(VENT|BOLLARD)$"),
    dict(regiao="Sinnoh", grupo="Canteiros de berry, até a janela de save",
         modo="objeto_fonte", campos=("object_events",), data="23/08/2026",
         motivo="os 90 `BERRY_SOIL` em 23 mapas. O canteiro não é desenho: é "
                "estado, e o id da árvore de berry MORA NA SAVE "
                "(`SaveBlock1.berryTrees`). Plantá-los hoje mexe no leiaute da "
                "save com a janela FECHADA (ver `guarda_save.py` e ESTADO 0.h), "
                "e a ordem é que quem quebra a save sobe "
                "`SAVE_LAYOUT_REVISION` junto. Corte com prazo, não para "
                "sempre: ele cai na primeira janela de save aberta de "
                "propósito",
         alvo=r"OBJ_EVENT_GFX_BERRY_SOIL$"),
]


def corta_campo(a, b, cortado):
    """(nosso, da fonte) depois do corte de DÉFICIT daquele campo.

    `min(a, b)` e não `a = b = 0`: o campo passa a valer 100% naquele mapa, e o
    excedente NOSSO não empurra a coluna acima de 100. Tirar só do denominador
    (o erro óbvio aqui) daria 10 de 5 num mapa em que pusemos mais gente que a
    fonte, e a coluna passaria de 200%. Travado no `--demo`.
    """
    return (min(a, b), min(a, b)) if cortado else (a, b)


def cortes_da_regiao(regiao, tabela=None):
    """(regex dos mapas da fonte cortados, {mapa nosso: campos cortados})."""
    tabela = CORTES_DO_GUI if tabela is None else tabela
    fonte, defi = [], {}
    for x in tabela:
        if x["regiao"] != regiao:
            continue
        if x["modo"] == "mapa_fonte":
            fonte.append(x["alvo"])
        elif x["modo"] == "deficit":
            for m in x["alvo"]:
                defi.setdefault(m, set()).update(x["campos"])
    return (re.compile("|".join(fonte)) if fonte else None), defi


def cortes_de_objeto(regiao, tabela=None):
    """(regex dos gráficos cortados, [grupos]) do modo `objeto_fonte`.

    Separada de `cortes_da_regiao` de propósito: aquela devolve MAPA, esta
    devolve GRÁFICO, e juntar os dois num retorno só já seria a próxima
    armadilha.
    """
    tabela = CORTES_DO_GUI if tabela is None else tabela
    g = [x for x in tabela
         if x["regiao"] == regiao and x["modo"] == "objeto_fonte"]
    rx = re.compile("|".join(x["alvo"] for x in g)) if g else None
    return rx, g


def confere_cortes(tabela=None):
    """Problemas na tabela de cortes. Lista vazia = tabela sã.

    Mesma lógica de `confere_apelidos`: corte errado não aparece como erro,
    aparece como completude ALTA. Um nome de mapa com um dígito trocado corta
    NADA e ninguém percebe, porque o número sobe do mesmo jeito pelos outros.
    """
    tabela = CORTES_DO_GUI if tabela is None else tabela
    ruim, vistos = [], set()
    for x in tabela:
        if x["grupo"] in vistos:
            ruim.append(f"grupo repetido: {x['grupo']}")
        vistos.add(x["grupo"])
        if x["regiao"] not in REGIOES:
            ruim.append(f"{x['grupo']}: região {x['regiao']} não existe")
        for c in x["campos"]:
            if c not in TODOS_OS_CAMPOS:
                ruim.append(f"{x['grupo']}: campo {c} não existe")
        if x["modo"] == "mapa_fonte":
            try:
                re.compile(x["alvo"])
            except re.error as e:
                ruim.append(f"{x['grupo']}: regex inválida ({e})")
        elif x["modo"] == "deficit":
            for m in x["alvo"]:
                if not os.path.exists(f"{RAIZ}/data/maps/{m}/map.json"):
                    ruim.append(f"{x['grupo']}: o mapa {m} não existe em "
                                "data/maps")
        elif x["modo"] == "objeto_fonte":
            try:
                rx = re.compile(x["alvo"])
            except re.error as e:
                ruim.append(f"{x['grupo']}: regex inválida ({e})")
                continue
            if x["campos"] != ("object_events",):
                ruim.append(f"{x['grupo']}: corte de objeto só corta "
                            "object_events")
            usados = graficos_nossos(x["regiao"])
            meus = sorted(g for g in usados if rx.search(g))
            if meus:
                ruim.append(f"{x['grupo']}: corta gráfico que NÓS usamos "
                            f"({', '.join(meus)}); sairia do denominador e "
                            "ficaria no numerador")
        else:
            ruim.append(f"{x['grupo']}: modo {x['modo']} não existe")
    return ruim


def graficos_nossos(regiao, _cache={}):
    """Todo `graphics_id` que aparece nos NOSSOS mapas daquela região.

    É a trava do modo `objeto_fonte`: gráfico que nós usamos não pode sair do
    denominador, senão a mesma coisa é descontada de um lado e contada do
    outro.
    """
    if regiao not in _cache:
        cfg = REGIOES[regiao]
        if cfg.get("plat"):
            sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
            import importa_npcs_sinnoh as I
            nossos = I.nossos_mapas_sinnoh()
        elif cfg.get("censo"):
            nossos = [v["nome"] for v in
                      json.load(open(cfg["censo"]))["de_para"].values()]
        else:
            nossos = nossos_da_regiao(todos_os_mapas(RAIZ), cfg["grupo"])
        g = set()
        for m in nossos:
            p = f"{RAIZ}/data/maps/{m}/map.json"
            if not os.path.exists(p):
                continue
            g |= {o.get("graphics_id", "") for o in
                  (json.load(open(p)).get("object_events") or [])}
        _cache[regiao] = g
    return _cache[regiao]


def normaliza(nome):
    """Nosso 'PalletTown_Frlg' e o 'PalletTown' da fonte sao o mesmo mapa."""
    nome = APELIDOS_FONTE.get(nome, nome)
    n = re.sub(r"_Frlg$", "", nome)
    n = re.sub(r"_johto$", "", n, flags=re.I)
    return n.lower().replace("_", "")


def cidades_de_outra_fonte(fonte_atual=""):
    """Prefixo de nome (a parte antes do primeiro '_') das cidades que vieram
    de OUTRA fonte. `CeladonCity_PokemonCenter` do hns e o
    `CeladonCity_PokemonCenter_1F` do pokefirered sao o mesmo lugar, mas o nome
    difere no sufixo, entao o desconto por nome inteiro nao pega. O que nao
    varia e a cidade. Sem isto, Johto saia com 63,6% dos mapas por causa de 92
    mapas de Kanto que ja estao no jogo, vindos do FireRed com outro nome."""
    cidades = set()
    for f in ("pokefirered", "pokeemerald"):
        # ARMADILHA que eu cai: sem esta linha, medir Kanto contra o
        # pokefirered descontava o pokefirered inteiro e Kanto dava 100,0% com
        # qualquer buraco. A fonte da propria regiao nunca entra no desconto.
        if f in fonte_atual:
            continue
        raiz = f"{FONTES}/{f}/data/maps"
        if os.path.isdir(raiz):
            cidades |= {m.split("_")[0].lower() for m in os.listdir(raiz)
                        if os.path.isdir(f"{raiz}/{m}")}
    return cidades


# Mapa que a fonte tem e que nao e conteudo: rascunho do autor do hack e
# variante de horario, que aqui nao existe como mapa separado.
LIXO = re.compile(r"^(NewMap|Trees|.*_Temp|Gate_)|(Day|Night)$", re.I)


def mapas_so_na_fonte(deles, nosso_mg, fonte=""):
    nossos = {normaliza(x) for x in nosso_mg}
    cidades = cidades_de_outra_fonte(fonte)
    return [m for k, m in deles.items()
            if k not in nossos
            and m.split("_")[0].lower() not in cidades
            and not LIXO.search(m)]


def _cru(n):
    """Chave crua de nome de mapa, para casar as DUAS grafias do mesmo lugar.

    A fonte escreve o destino de um warp como constante (`MAP_VICTORY_ROAD_KANTO_1F`,
    `MAP_HEADER_UNKNOWN_197`) e o mapa em si como diretório ou arquivo
    (`VictoryRoadKanto_1F`). Onde cai cada `_` varia entre os dois, então tirar
    TODOS eles é o único casamento que não depende de adivinhar a convenção.
    """
    return re.sub(r"^MAP(_HEADER)?_", "", n).replace("_", "").lower()


def _sobra_gen3(fonte):
    dest, ev = set(), {}
    for m in todos_os_mapas(fonte):
        d = json.load(open(f"{fonte}/data/maps/{m}/map.json"))
        ev[m] = sum(len(d.get(c) or []) for c in
                    ("object_events", "warp_events", "bg_events", "coord_events"))
        dest |= {_cru(w["dest_map"]) for w in d.get("warp_events") or []}
        dest |= {_cru(c["map"]) for c in d.get("connections") or []}
    return {m: (n, _cru(m) in dest) for m, n in ev.items()}


def _sobra_plat(fonte, heads):
    dest, ev = set(), {}
    for h, arq in heads.items():
        p = f"{fonte}/res/field/events/{arq[0]}.json"
        if not os.path.exists(p):
            ev[h] = 0
            continue
        d = json.load(open(p))
        ev[h] = sum(len(d.get(c) or []) for c in
                    ("object_events", "warp_events", "bg_events", "coord_events"))
        dest |= {_cru(w["dest_header_id"]) for w in d.get("warp_events") or []}
    return {h: (n, _cru(h) in dest) for h, n in ev.items()}


# Registro que a regra de sobra pegaria, e que é CONTEÚDO. Exceção por NOME, de
# propósito e curta: a regra corta por AUSÊNCIA DE DADO (zero evento e nenhuma
# porta de entrada), e há lugar de verdade cujo dado a fonte simplesmente não
# traz no formato que lemos.
#
#   Distortion World: os 9 andares apontam para `events_empty` no Platinum
#   porque a cena inteira é código, não tabela de evento; e o 1F, que TEM
#   evento, prova que o lugar existe. O Gui decidiu em 21/08/2026 que ele FICA
#   no escopo, com gravidade normal. Se ele ficasse no balde, o mapa sumiria do
#   denominador calado e ninguém veria a dívida.
#   Seabreak Path: idem, zero evento na fonte, e é caminho andável de verdade.
#   Ele SAI do escopo, mas por decisão datada em `CORTES_DO_GUI` (Mystery
#   Gift), que é o lugar onde o Gui enxerga o corte, e não por esta regra.
CONTEUDO_APESAR_DE_VAZIO = re.compile(r"DISTORTION_WORLD|SEABREAK", re.I)


def julga_sobra(medido):
    """As DUAS condições, e só elas. Julgamento separado da leitura de disco
    para poder ser testado com medição plantada em `--demo`."""
    return {m for m, (eventos, tem_entrada) in medido.items()
            if not eventos and not tem_entrada
            and not CONTEUDO_APESAR_DE_VAZIO.search(m)}


def sobra_de_tabela(fonte, cfg, heads=None, _cache={}):
    """Registro da fonte que NÃO É LUGAR: sobra de tabela do motor dela.

    Existe porque a coluna `mapas` estava dividindo por um denominador que tem
    53 headers `UNKNOWN_*` do Platinum, 8 mapas do FireRed que o próprio
    FireRed nunca ligou a lugar nenhum, e as sentinelas `EVERYWHERE` e
    `NOTHING`, que são valor de enum e não mapa.

    A REGRA É MEDIDA, não é lista de nome: sai do denominador o header que tem
    **zero evento na fonte E nenhum warp (ou conexão) de entrada vindo de outro
    mapa da fonte**. As duas condições juntas, sempre: mapa sem warp de entrada
    mas COM conteúdo fica (a fonte pode ter perdido o mapa externo que levava a
    ele, e o lugar continua sendo lugar), e mapa sem conteúdo mas COM porta fica
    também (alguém entra nele).

    ARMADILHA, e por isso `--detalhe` imprime a lista inteira: a regra corta por
    AUSÊNCIA DE DADO, então ela também pega header cujo conteúdo a fonte
    simplesmente não traz. Medido em 21/08/2026: os 9 andares do Distortion
    World do Platinum apontam para `events_empty` e caem aqui, e o Distortion
    World é conteúdo de verdade. Ninguém pode esconder corte de escopo atrás
    desta regra: o corte de escopo é decisão do Gui, e a lista impressa é o
    lugar onde ele o vê.
    """
    if fonte not in _cache:
        _cache[fonte] = julga_sobra(
            _sobra_plat(fonte, heads) if cfg.get("plat") else
            _sobra_gen3(fonte))
    return _cache[fonte]


def le_plat(fonte, header, rx_obj=None):
    """Conta eventos num mapa do pokeplatinum (formato de DS).

    O mapa la nao guarda os eventos: guarda o NOME do arquivo de eventos, em
    include/data/map_headers.h. Placa de rua no Platinum e object_event com
    grafico de SIGNBOARD, nao bg_event, entao ela e contada como placa aqui,
    senao o denominador de "placas" fica quase zero e a coluna mente para cima.

    `rx_obj` e o corte de OBJETO do modo `objeto_fonte` (ver CORTES_DO_GUI): o
    objeto da fonte cujo `graphics_id` casa com ele sai do denominador e vai
    contado em `_cortados`, para `--detalhe` poder imprimir quantos e de que
    tipo. Ele NUNCA pode casar com grafico que nos usamos, e isso e conferido
    em `confere_cortes`.
    """
    import importa_npcs_sinnoh as I
    arq = I.headers_do_platinum().get(header)
    if not arq:
        return None
    p = f"{fonte}/res/field/events/{arq[0]}.json"
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    objs = d.get("object_events") or []
    placas = [o for o in objs
              if any(t in o.get("graphics_id", "") for t in I.GRAFICOS_PLACA)]
    cortados = collections.Counter(
        o.get("graphics_id", "") for o in objs
        if rx_obj and rx_obj.search(o.get("graphics_id", ""))
        and not any(t in o.get("graphics_id", "") for t in I.GRAFICOS_PLACA))
    return {"object_events": len(objs) - len(placas) - sum(cortados.values()),
            "warp_events": len(d.get("warp_events") or []),
            "bg_events": len(d.get("bg_events") or []) + len(placas),
            "_cortados": cortados}


def _distintos(blob):
    """Metatiles distintos num `map.bin`.

    Cada celula do layout e um u16: os 10 bits de baixo sao o METATILE e os 6 de
    cima sao colisao e elevacao. Sem a mascara, dois pedacos do mesmo desenho com
    elevacao diferente contariam como desenho diferente e a coluna mentiria para
    cima. Ver `include/fieldmap.h` (MAPGRID_METATILE_ID_MASK = 0x03FF).
    """
    return {(blob[i] | (blob[i + 1] << 8)) & 0x3FF for i in range(0, len(blob), 2)}


def _layouts(_cache={}):
    if not _cache:
        d = json.load(open(f"{RAIZ}/data/layouts/layouts.json"))
        _cache.update({l["id"]: l["blockdata_filepath"] for l in d["layouts"]
                       if l.get("id")})
    return _cache


def _cortados_deficit():
    """Todo mapa nosso que saiu do escopo (modo `deficit` de CORTES_DO_GUI)."""
    return {m for x in CORTES_DO_GUI if x["modo"] == "deficit" for m in x["alvo"]}


def arte(nossos):
    """(mediana de metatiles distintos por mapa, quantos abaixo do piso, n).

    Mapa CORTADO nao entra. Desde 22/08/2026 ele e um tumulo de 1x1
    (`dev_scripts/remove_mapas_cortados.py`): contar o metatile unico dele
    afundaria a mediana de arte de Sinnoh sem nada ter piorado no desenho.
    """
    fora = _cortados_deficit()
    n = []
    for m in nossos:
        p = f"{RAIZ}/data/maps/{m}/map.json"
        if not os.path.exists(p) or m in fora:
            continue
        arq = _layouts().get(json.load(open(p)).get("layout"))
        if arq and os.path.exists(f"{RAIZ}/{arq}"):
            n.append(len(_distintos(open(f"{RAIZ}/{arq}", "rb").read())))
    if not n:
        return None
    n.sort()
    meio = n[len(n) // 2] if len(n) % 2 else (n[len(n) // 2 - 1] + n[len(n) // 2]) / 2
    return meio, sum(1 for x in n if x < PISO_ARTE), len(n)


def fmt_arte(a):
    if not a:
        return "  --  "
    meio, abaixo, _ = a
    return f"{meio:g} ({abaixo})"


def confere_apelidos(tabela=None):
    """Problemas na tabela de apelidos. Lista vazia = tabela sã.

    Apelido errado não aparece como erro em lugar nenhum: aparece como
    completude ALTA, que é o jeito mais caro de errar nesta casa. Então a
    tabela é conferida, e não apenas escrita:
      1. o destino tem que EXISTIR em `data/maps` (senão o mapa não está na ROM
         e o "já está na ROM com outro nome" é mentira);
      2. dois mapas da fonte não podem apontar para o MESMO mapa nosso (sinal de
         chute: 1F, 2F e B1F todos casados com o mesmo andar);
      3. a chave não pode ser nome de um mapa NOSSO, senão `normaliza` passaria
         a reescrever o nosso próprio mapa e o casamento inverteria.
    """
    tabela = APELIDOS_FONTE if tabela is None else tabela
    nossos = set(todos_os_mapas(RAIZ))
    ruim = []
    vistos = {}
    for fonte, meu in tabela.items():
        if not os.path.exists(f"{RAIZ}/data/maps/{meu}/map.json"):
            ruim.append(f"{fonte}: o alvo {meu} não existe em data/maps")
        if meu in vistos:
            ruim.append(f"{fonte} e {vistos[meu]} apontam para o mesmo {meu}")
        vistos[meu] = fonte
        if fonte in nossos:
            ruim.append(f"{fonte} também é nome de mapa NOSSO")
    return ruim


def eventos(raiz, mapa):
    p = f"{raiz}/data/maps/{mapa}/map.json"
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return {c: len(d.get(c) or []) for c, _ in CAMPOS}


def linha_da_dex():
    """Dex obtenível: quantos de quantos, por região e no total, lido do censo
    e não decorado.

    A régua do resto deste arquivo mede MAPA. Esta linha mede POKÉMON, e sai do
    mesmo `dev_scripts/censo_dex.py` que a obra da dex usa como fonte da
    verdade: se a régua e o censo discordarem, quem manda é o censo. "Obtenível"
    aqui é o que o censo NÃO chama de `inobtenivel`; a coluna por região conta
    entradas distintas com fonte selvagem, estática ou de presente naquela
    região, e por isso a soma das regiões é MAIOR que o total (o mesmo Pokémon
    aparece em várias regiões) e menor que ele ao mesmo tempo (evolução e forma
    não têm região).
    """
    import censo_dex
    linhas = censo_dex.censo()
    total = len(linhas)
    obt = sum(1 for l in linhas if l.categoria != "inobtenivel")
    por_regiao = {r: len({l.nome for l in linhas if r in l.regioes.split(",")})
                  for r in censo_dex.CINCO}
    print(f"\nDex obtenível: {obt}/{total} ({100 * obt / total:.1f}%) — "
          + ", ".join(f"{r} {n}" for r, n in por_regiao.items()))
    print("   por região = entradas com encontro selvagem, estático ou presente "
          "NAQUELA região;\n   o total inclui também evolução e troca de forma, "
          "que não têm região.")


def main():
    alvo = None
    if "--detalhe" in sys.argv:
        alvo = sys.argv[sys.argv.index("--detalhe") + 1]

    nosso_mg = todos_os_mapas(RAIZ)
    print("Completude por região, normalizada pela FONTE, mapa a mapa.")
    print("100% = tão completo quanto o jogo de onde a região veio.\n")
    print("A coluna ARTE não é completude contra a fonte: é a variedade do "
          "desenho, mediana de\nmetatiles distintos por mapa, com quantos mapas "
          f"abaixo de {PISO_ARTE} entre parênteses.\n")
    print(f"{'região':8} {'mapas':>11} {'objetos':>11} {'warps':>11} "
          f"{'placas':>11} {'arte':>11}")

    faltando_total = {}
    sobras = {}
    cortes = {}
    cortes_obj = {}
    for nome, cfg in REGIOES.items():
        if alvo and alvo.lower() != nome.lower():
            continue
        fonte = cfg["fonte"]
        if not (fonte and os.path.isdir(fonte)):
            nossos = nossos_da_regiao(nosso_mg, cfg["grupo"])
            print(f"{nome:8} {len(nossos):>8} sem fonte" + " " * 30)
            continue

        plat = cfg.get("plat")
        if plat:
            sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
            import importa_npcs_sinnoh as I
            heads = I.headers_do_platinum()
            deles = {}
            for h in heads:
                deles.setdefault(I.chave(h), h)
            nossos = I.nossos_mapas_sinnoh()
            casados = [(m, I.APELIDOS.get(m) or deles.get(I.chave(m)))
                       for m in nossos]
            casados = [(m, h) for m, h in casados if h in heads]
            casadas_norm = {I.chave(h) for _, h in casados}
            so_na_fonte = [h for k, h in deles.items() if k not in casadas_norm]
            sobra = sobra_de_tabela(fonte, cfg, heads)
        else:
            deles = {normaliza(m): m for m in todos_os_mapas(fonte)}
            nossos = nossos_da_regiao(nosso_mg, cfg["grupo"])
            casados = [(m, deles[normaliza(m)]) for m in nossos if normaliza(m) in deles]
            so_na_fonte = mapas_so_na_fonte(deles, nosso_mg, fonte)
            sobra = sobra_de_tabela(fonte, cfg)
        # A sobra de tabela da fonte sai do DENOMINADOR (ver `sobra_de_tabela`),
        # e o que saiu vai impresso em `--detalhe`.
        sobras[nome] = sorted(m for m in so_na_fonte if m in sobra)
        so_na_fonte = [m for m in so_na_fonte if m not in sobra]
        # Os CORTES DO GUI, que são escopo e não régua: o que sai daqui está
        # nomeado, datado e impresso em `--detalhe`.
        rx_corte, defi = cortes_da_regiao(nome)
        rx_obj, grupos_obj = cortes_de_objeto(nome)
        fora = {m for m in so_na_fonte if rx_corte and rx_corte.search(m)}
        so_na_fonte = [m for m in so_na_fonte if m not in fora]
        cortes[nome] = (sorted(fora), {m for m, _ in casados if m in defi})
        # Mapas que a FONTE tem e nos nao.
        #
        # ARMADILHA: o denominador tem que descontar o que ja veio por OUTRA
        # fonte. O hns e um hack de Johto E Kanto, entao ele tem PalletTown,
        # ViridianCity e mais 730. Comparando so contra os nossos mapas de
        # Johto, esses 732 apareciam como "faltando" e Johto saia com 23,3% dos
        # mapas, quando o que falta de verdade e outra coisa. Nos importamos
        # Kanto do pokefirered, entao eles JA ESTAO no jogo.
        # Por isso o desconto e contra TODOS os nossos mapas, nao so os da regiao.

        soma_n = {c: 0 for c, _ in CAMPOS}
        soma_f = {c: 0 for c, _ in CAMPOS}
        piores = []
        obj_cortados = collections.Counter()
        vazios = []
        for meu, seu in casados:
            a = eventos(RAIZ, meu)
            b = le_plat(fonte, seu, rx_obj) if plat else eventos(fonte, seu)
            if not a or not b:
                continue
            if "object_events" not in defi.get(meu, ()):
                obj_cortados.update(b.get("_cortados") or {})
                if b["object_events"] > a["object_events"]:
                    vazios.append((b["object_events"] - a["object_events"], meu,
                                   a["object_events"], b["object_events"]))
            for c, _ in CAMPOS:
                x, y = corta_campo(a[c], b[c], c in defi.get(meu, ()))
                soma_n[c] += x
                soma_f[c] += y
            if b["object_events"] >= 5 and "object_events" not in defi.get(meu, ()):
                r = a["object_events"] / b["object_events"]
                if r < 0.75:
                    piores.append((r, meu, a["object_events"], b["object_events"]))

        def p(c):
            # ARMADILHA: denominador zero nao e "nao da para medir", e um FATO
            # sobre a fonte. A fonte de Sinnoh tem 2778 objetos no total e ZERO
            # nos 69 mapas de cidade de Sinnoh: os objetos dela sao todos de
            # Hoenn. Ou seja, nao ha NPC de Sinnoh para importar dali, e quem
            # quiser fechar essa lacuna tem que ir no pokeplatinum.
            # Imprimir "n/a" escondia isso; agora diz que a fonte esta vazia.
            if not soma_f[c]:
                return "fonte 0" if soma_n[c] else "  --  "
            return f"{100*soma_n[c]/soma_f[c]:5.1f}%"
        # mapas: o denominador e o que a fonte tem daquela regiao, e para as
        # fontes que sao o jogo inteiro isso e o total delas
        pm = 100.0 * len(casados) / max(1, len(casados) + len(so_na_fonte))
        print(f"{nome:8} {pm:10.1f}% {p('object_events'):>11} "
              f"{p('warp_events'):>11} {p('bg_events'):>11} "
              f"  {fmt_arte(arte(nossos)):>11}")
        faltando_total[nome] = (so_na_fonte, sorted(piores)[:6])
        if grupos_obj:
            cortes_obj[nome] = (obj_cortados, grupos_obj, sorted(vazios,
                                                                reverse=True))

    if not alvo:
        linha_da_dex()

    if alvo:
        for nome, (falta, piores) in faltando_total.items():
            print(f"\n=== {nome}: {len(falta)} mapas que a fonte tem e nós não ===")
            for m in falta[:15]:
                print(f"   {m}")
            if piores:
                print(f"\n=== {nome}: mapas mais vazios que o original ===")
                for r, m, a, b in piores:
                    print(f"   {100*r:5.1f}%  {m:42} {a} de {b} objetos")
        for nome, (fonte_fora, nossos_fora) in cortes.items():
            grupos = [x for x in CORTES_DO_GUI if x["regiao"] == nome]
            if not grupos:
                continue
            print(f"\n=== {nome}: o que os CORTES DO GUI tiraram do "
                  f"denominador ===")
            print(f"   {len(fonte_fora)} registros da fonte e "
                  f"{len(nossos_fora)} mapas nossos, em {len(grupos)} grupos.")
            print("   isto É corte de escopo, com data e motivo, ao contrário "
                  "do balde de sobra abaixo.")
            rest = set(fonte_fora)
            for x in grupos:
                if x["modo"] == "mapa_fonte":
                    rx = re.compile(x["alvo"])
                    saiu = sorted(m for m in rest if rx.search(m))
                    rest -= set(saiu)
                else:
                    saiu = sorted(m for m in x["alvo"] if m in nossos_fora)
                print(f"   [{x['data']}] {x['grupo']} ({x['modo']}, "
                      f"{len(saiu)}): {x['motivo']}")
                for m in saiu:
                    print(f"      {m}")
                if not saiu:
                    print("      (nada: este grupo não casou com mapa nenhum "
                          "hoje)")
        for nome, (contagem, grupos, vazios) in cortes_obj.items():
            print(f"\n=== {nome}: o que os CORTES DE OBJETO tiraram do "
                  "denominador ===")
            print(f"   {sum(contagem.values())} objetos da fonte, em "
                  f"{len(grupos)} grupos. O mapa FICA; só este tipo de "
                  "registro é que sai.")
            print("   a trava: nenhum destes gráficos aparece nos NOSSOS "
                  "map.json (conferida em --demo).")
            for x in grupos:
                rx = re.compile(x["alvo"])
                saiu = {g: n for g, n in contagem.items() if rx.search(g)}
                print(f"   [{x['data']}] {x['grupo']} (objeto_fonte, "
                      f"{sum(saiu.values())}): {x['motivo']}")
                for g, n in sorted(saiu.items(), key=lambda kv: -kv[1]):
                    print(f"      {n:4}  {g}")
                if not saiu:
                    print("      (nada: este grupo não casou com objeto "
                          "nenhum hoje)")
            print(f"\n   DEPOIS do corte, {len(vazios)} mapas ainda têm menos "
                  f"objeto que a fonte ({sum(v[0] for v in vazios)} no total).")
            print("   isto é o que AINDA falta, e não é corte de ninguém:")
            for d, m, a, b in vazios:
                print(f"      -{d:<3} {m:44} {a} de {b}")
        for nome, fora in sobras.items():
            if not fora:
                continue
            print(f"\n=== {nome}: {len(fora)} registros da fonte FORA do "
                  f"denominador ===")
            print("   critério MEDIDO: zero evento na fonte E nenhum warp ou "
                  "conexão de entrada.")
            print("   não é corte de escopo; se algo aqui for lugar de "
                  "verdade, a fonte é que não trouxe o dado.")
            for m in fora:
                print(f"   {m}")
    else:
        print("\nuse --detalhe <região> para ver o que falta em cada uma")
    return 0


def demo():
    """Duas regras que a primeira versao quebrou, mais a coluna de arte."""
    # 1. mapa da fonte com sufixo nosso e o MESMO mapa
    assert normaliza("PalletTown_Frlg") == normaliza("PalletTown")
    assert normaliza("Route3_Frlg") == normaliza("Route3")
    # 2. nomes diferentes continuam diferentes
    assert normaliza("Route3_Frlg") != normaliza("Route4")
    # 3. arte conta METATILE, e metatile e so os 10 bits de baixo. A celula
    #    0xF001 e o mesmo desenho da 0x0001 com outra colisao e elevacao.
    assert _distintos(b"\x00\x00\x01\x04") == {0, 1}
    assert _distintos(b"\x01\x00\x01\xF0") == {1}
    assert _distintos(b"\xFF\xFF") == {0x3FF}
    # 4. a mutacao tem que ser pega: trocar um metatile muda a conta
    assert _distintos(b"\x01\x00\x01\x00") != _distintos(b"\x01\x00\x02\x00")
    # 5. TÚMULO não é mapa nosso. Mapa que saiu do escopo continua em
    #    `map_groups.json` com o id intacto e sem evento nenhum, marcado pelo
    #    campo `cortado_por`. Sem o filtro por esse campo os túmulos sem prefixo
    #    de região caem no balde de Hoenn, que é "tudo que não é das outras
    #    três", e afundam a mediana de ARTE sem nada ter piorado no desenho.
    assert tumulos(), "nenhum túmulo achado: o filtro estaria medindo nada"
    mg = todos_os_mapas(RAIZ)
    hoenn = nossos_da_regiao(mg, "TownsAndRoutes")
    assert not (set(hoenn) & tumulos()), sorted(set(hoenn) & tumulos())[:5]
    # ...e o filtro não pode comer mapa vivo
    assert "LittlerootTown" in hoenn
    # mutação plantada: um túmulo posto num grupo alheio, que é exatamente como
    # os mapas cortados moram hoje, tem que sair do balde de Hoenn
    assert "Galar_Ballonlea01" in tumulos()
    plantado_mg = {"Galar_Ballonlea01": "gMapGroup_IndoorRoute117",
                   "LittlerootTown": "gMapGroup_TownsAndRoutes"}
    assert nossos_da_regiao(plantado_mg, "TownsAndRoutes") == ["LittlerootTown"]

    # 6. a tabela de apelidos tem que estar sã, e apelido errado tem que REPROVAR
    assert confere_apelidos() == [], confere_apelidos()
    assert normaliza("SafariZoneIndoor") == normaliza("SafariZone_East_RestHouse_Frlg")
    assert normaliza("CeruleanCave3") == normaliza("CeruleanCave_B1F_Frlg")
    # ...e continuar separando o que é separado: o 1F não pode virar o B1F
    assert normaliza("CeruleanCave1") != normaliza("CeruleanCave_B1F_Frlg")
    # mutação plantada 1: alvo que não existe na ROM
    assert confere_apelidos({"Xyz": "MapaQueNaoExiste"})
    # mutação plantada 2: dois andares da fonte casados com o mesmo mapa nosso
    assert confere_apelidos({"CeruleanCave1": "CeruleanCave_1F_Frlg",
                             "CeruleanCave2": "CeruleanCave_1F_Frlg"})

    # 7. a sobra de tabela sai por MEDIDA, e as duas condições valem juntas.
    #    mutação plantada 3: um mapa COM evento na fonte, e com cara de sobra no
    #    nome, jogado no balde. Quem trocar a regra medida por lista de nome
    #    reprova aqui.
    plantado = {"MAP_HEADER_UNKNOWN_999": (7, False),   # tem evento: FICA
                "MAP_HEADER_UNUSED_CASA": (0, True),    # tem porta: FICA
                "MAP_HEADER_SOBRA_DE_VERDADE": (0, False)}
    assert julga_sobra(plantado) == {"MAP_HEADER_SOBRA_DE_VERDADE"}, julga_sobra(plantado)
    # e na fonte de verdade: os 8 do FireRed são sobra, e nenhum deles tem evento
    med = _sobra_gen3(REGIOES["Kanto"]["fonte"])
    assert all(med[m] == (0, False) for m in julga_sobra(med))
    assert med["Prototype_SeviiIsle_6"] == (0, False)
    # e mapa COM conteúdo não é sobra nem quando ninguém aponta para ele: as
    # duas condições valem juntas, sempre. Quem trocar o `and` por `or` reprova
    # aqui, porque estes existem de verdade na fonte de Kanto.
    sem_porta_com_evento = [m for m, (ev, ent) in med.items() if ev and not ent]
    assert sem_porta_com_evento
    assert not (set(sem_porta_com_evento) & julga_sobra(med))
    # 7.1 O Distortion World é CONTEÚDO e não pode cair no balde de sobra, nem
    #     quando a fonte não traz evento nenhum dele (é o caso real: 9 dos 10
    #     andares apontam para `events_empty`). Se ele sumir do denominador
    #     calado, o corte de escopo deixa de ser decisão do Gui e vira efeito
    #     colateral de uma régua.
    assert julga_sobra({"MAP_HEADER_DISTORTION_WORLD_B3F": (0, False)}) == set()
    assert julga_sobra({"MAP_HEADER_SEABREAK_PATH": (0, False)}) == set()
    sys.path.insert(0, os.path.join(RAIZ, "dev_scripts"))
    import importa_npcs_sinnoh as I
    assert not any("DISTORTION" in m for m in
                   julga_sobra(_sobra_plat(REGIOES["Sinnoh"]["fonte"],
                                           I.headers_do_platinum())))

    # 8. os CORTES DO GUI. Corte errado não aparece como erro: aparece como
    #    completude alta sem obra nenhuma.
    assert confere_cortes() == [], confere_cortes()
    # mutação plantada 4: corte de déficit apontando para mapa que não existe
    assert confere_cortes([dict(regiao="Sinnoh", grupo="x", modo="deficit",
                                alvo=["MapaQueNaoExiste"], data="",
                                campos=TODOS_OS_CAMPOS, motivo="")])
    # mutação plantada 5: modo que não existe, e campo que não existe
    assert confere_cortes([dict(regiao="Sinnoh", grupo="x", modo="apagar",
                                alvo=[], campos=(), motivo="", data="")])
    assert confere_cortes([dict(regiao="Sinnoh", grupo="x", modo="deficit",
                                alvo=[], campos=("cor_dos_olhos",), motivo="",
                                data="")])
    # 8.1 corte de DÉFICIT nunca põe coluna acima de 100 por si só. O mapa A
    #     tem MAIS gente que a fonte e o B tem menos; cortar os dois tem de dar
    #     exatamente 100%, nunca 200%, que é o que sairia se o corte tirasse só
    #     o denominador.
    plantado = [("A", 10, 5), ("B", 0, 5)]
    n = f = 0
    for _, a, b in plantado:
        x, y = corta_campo(a, b, True)
        n += x
        f += y
    assert (n, f) == (5, 5), (n, f)
    # ...e cortar nada não muda nada
    assert [corta_campo(a, b, False) for _, a, b in plantado] == [(10, 5), (0, 5)]
    # 8.2 o corte é POR MAPA NOMEADO: o grupo do Game Corner de Veilstone não
    #     pode mexer em mapa de fora dele (a Ilha de Ferro FICA no escopo, por
    #     decisão do Gui em 21/08/2026), e a régua de Kanto não tem corte nenhum.
    _, defi = cortes_da_regiao("Sinnoh")
    assert "GameCorner" in defi and "IronIsland" not in defi
    assert cortes_da_regiao("Kanto") == (None, {})

    # 9. O corte de OBJETO (modo `objeto_fonte`, 23/08/2026). Ele é o mais
    #    perigoso dos três, porque não tira mapa nenhum da vista: some com
    #    REGISTRO dentro de mapa que fica. Três travas.
    # 9.1 o regex do corte não pode pegar mapa nenhum, só gráfico
    rx_obj, grupos_obj = cortes_de_objeto("Sinnoh")
    assert len(grupos_obj) == 2, grupos_obj
    assert rx_obj.search("OBJ_EVENT_GFX_VENT")
    assert rx_obj.search("OBJ_EVENT_GFX_BOLLARD")
    assert rx_obj.search("OBJ_EVENT_GFX_BERRY_SOIL")
    # ...e não pode pegar quem só PARECE: `SOLAR_VENT` não existe, mas
    # `PREVENT`, `ADVENTURER` e o `BERRY_TREE` de verdade, sim.
    assert not rx_obj.search("OBJ_EVENT_GFX_BERRY_TREE")
    assert not rx_obj.search("OBJ_EVENT_GFX_ADVENTURER")
    assert not rx_obj.search("OBJ_EVENT_GFX_VENTRILOQUIST")
    assert cortes_de_objeto("Kanto") == (None, [])
    # 9.2 nenhuma outra região tem corte de objeto hoje, e o de Sinnoh corta só
    #     `object_events`
    assert all(x["campos"] == ("object_events",) for x in grupos_obj)
    # 9.3 A TRAVA: gráfico cortado não pode aparecer nos NOSSOS mapas. Mutação
    #     plantada: cortar o `ITEM_BALL`, que nós usamos 167 vezes em Sinnoh, e
    #     que sairia do denominador continuando no numerador.
    nossos_gfx = graficos_nossos("Sinnoh")
    assert "OBJ_EVENT_GFX_ITEM_BALL" in nossos_gfx
    assert not any(rx_obj.search(g) for g in nossos_gfx), \
        [g for g in nossos_gfx if rx_obj.search(g)]
    assert confere_cortes([dict(regiao="Sinnoh", grupo="x", modo="objeto_fonte",
                                alvo=r"OBJ_EVENT_GFX_ITEM_BALL$", data="",
                                campos=("object_events",), motivo="")])
    # mutação plantada: corte de objeto que também mexeria em warp
    assert confere_cortes([dict(regiao="Sinnoh", grupo="x", modo="objeto_fonte",
                                alvo=r"OBJ_EVENT_GFX_VENT$", data="",
                                campos=TODOS_OS_CAMPOS, motivo="")])
    # 9.4 e o corte tem que CONTAR: `le_plat` devolve o que tirou, senão
    #     `--detalhe` imprimiria zero e o corte ficaria invisível.
    f = REGIOES["Sinnoh"]["fonte"]
    if os.path.isdir(f):
        antes = le_plat(f, "MAP_HEADER_ROUTE_209")
        depois = le_plat(f, "MAP_HEADER_ROUTE_209", rx_obj)
        tirou = sum(depois["_cortados"].values())
        assert tirou > 0
        assert antes["object_events"] - tirou == depois["object_events"]
        assert antes["bg_events"] == depois["bg_events"]
        assert antes["warp_events"] == depois["warp_events"]

    print("demo ok")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo()
    else:
        sys.exit(main())
