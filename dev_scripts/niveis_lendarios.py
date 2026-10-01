#!/usr/bin/env python3
"""Nível de todo lendário, mítico, sublendário e ultra-fera do cartucho 1, por LUGAR.

Regra do Gui de 01/10/2026 (resposta 112, ESTADO 0.ar): "lendário é nível 50 a
100". Vale para todo lendário encontrável ou dado de presente no cartucho 1; os
times de líder da Fase F NÃO entram (são `trainers.party`). O nível sai da
dificuldade de ACESSO do lugar, e não da espécie: lugar alcançável cedo fica
perto de 50, fundo de dungeon pós-Liga, Mt. Silver, Distortion World e o fim
das Sevii ficam perto de 100.

Esta tabela é a ÚNICA fonte do nível. Quem lê:
  - `distribui_dex.py` (`nivel_no_mapa`), para os estáticos da Dex completa e os
    presentes do Birch;
  - `lendarios_sinnoh.py` (a coluna `nivel` da tabela dele precisa bater);
  - `redistribui_lendarios.py`, que reescreve os `setwildbattle`/`seteventmon`
    de cena e os errantes;
  - `inventario_lendarios.py --guarda`, o portão: todo ponto medido tem que
    estar num mapa desta tabela e com o nível dela.

Faixas usadas (a escada, do mais fácil para o mais difícil):
  50  alcançável no começo da região, sem golpe de campo (e os presentes do Birch)
  55  primeira masmorra da região, com Flash ou Cut
  60  meio da região, Surf ou Strength, ou masmorra de enredo
  65  meio para o fim, dois golpes de campo ou masmorra comprida
  70  fim da região, Waterfall/Rock Climb, cena de clímax
  75  masmorra pós-clímax, ilha de evento, braile
  80  fundo de masmorra de fim de região, pós-Liga começando
  85  pós-Liga de verdade, ilhas das Sevii do começo
  90  pós-Liga fundo
  95  Sevii final, Spear Pillar distorcido
  100 Tanoby, Silver Cave, Distortion World, os dois guardiões dos sinos
"""

# mapa -> (nível, acesso, região). A região é a do JOGO (onde o lugar fica),
# e não a do grupo de mapa: o vulcão de Cinnabar do Liquid Crystal mora no
# grupo de masmorras e o QG da Galáctica num grupo próprio.
NIVEL = {
    # ---------------------------------------------------------------- Kanto
    "MtMoon_B1F_Frlg": (50, "Mt. Moon, andar de baixo; começo de Kanto", "Kanto"),
    "MtMoon_B2F_Frlg": (50, "Mt. Moon, fundo; começo de Kanto", "Kanto"),
    "RockTunnel_1F_Frlg": (55, "Rock Tunnel (Flash)", "Kanto"),
    "RockTunnel_B1F_Frlg": (55, "Rock Tunnel, subsolo (Flash)", "Kanto"),
    "RocketHideout_B4F_Frlg": (60, "Esconderijo Rocket de Celadon, último andar", "Kanto"),
    "SafariZone_Center_Frlg": (60, "Safari Zone de Fuchsia", "Kanto"),
    "PowerPlant_Frlg": (60, "Power Plant (Surf)", "Kanto"),
    "PokemonMansion_1F_Frlg": (65, "Mansão de Cinnabar (Surf)", "Kanto"),
    "PokemonMansion_B1F_Frlg": (65, "Mansão de Cinnabar, subsolo (Surf, chave secreta)", "Kanto"),
    "SeafoamIslands_B4F_Frlg": (65, "Seafoam Islands, fundo (Surf, Strength)", "Kanto"),
    "LcCinnabarVolcano": (70, "Vulcão de Cinnabar do Liquid Crystal", "Kanto"),
    "MtEmber_Summit_Frlg": (80, "Mt. Ember, cume (One Island, pós-Liga de Kanto)", "Kanto"),
    "ThreeIsland_BerryForest_Frlg": (80, "Berry Forest (Three Island, pós-Liga de Kanto)", "Kanto"),
    "MtEmber_RubyPath_B5F_Frlg": (85, "Ruby Path, fundo do Mt. Ember (Strength)", "Kanto"),
    "CeruleanCave_1F_Frlg": (85, "Cerulean Cave (pós-Liga de Kanto)", "Kanto"),
    "CeruleanCave_2F_Frlg": (85, "Cerulean Cave, segundo andar (pós-Liga de Kanto)", "Kanto"),
    "CeruleanCave_B1F_Frlg": (90, "Cerulean Cave, fundo (pós-Liga de Kanto)", "Kanto"),
    "BirthIsland_Exterior_Frlg": (80, "Birth Island das Sevii (ilha de evento)", "Kanto"),
    "NavelRock_Base_Frlg": (90, "Navel Rock das Sevii (ilha de evento)", "Kanto"),
    "NavelRock_Summit_Frlg": (90, "Navel Rock das Sevii, cume (ilha de evento)", "Kanto"),
    "LcNewIslandCourtyard": (90, "New Island do Liquid Crystal", "Kanto"),
    "FiveIsland_LostCave_Room10_Frlg": (90, "Lost Cave, sala 10 (Five Island)", "Kanto"),
    "SixIsland_PatternBush_Frlg": (90, "Pattern Bush (Six Island)", "Kanto"),
    "FiveIsland_LostCave_Room14_Frlg": (95, "Lost Cave, última sala (Five Island)", "Kanto"),
    "SixIsland_DottedHole_SapphireRoom_Frlg": (95, "Dotted Hole, sala da safira (Six Island, Braille)", "Kanto"),
    "SevenIsland_SevaultCanyon_Frlg": (95, "Sevault Canyon (Seven Island)", "Kanto"),
    "SevenIsland_TanobyRuins_DilfordChamber_Frlg": (100, "Tanoby Ruins, câmara Dilford (Seven Island, Surf)", "Kanto"),
    "SevenIsland_TanobyRuins_LiptooChamber_Frlg": (100, "Tanoby Ruins, câmara Liptoo (Seven Island, Surf)", "Kanto"),
    "SevenIsland_TanobyRuins_MoneanChamber_Frlg": (100, "Tanoby Ruins, câmara Monean (Seven Island, Surf)", "Kanto"),
    "SevenIsland_TanobyRuins_RixyChamber_Frlg": (100, "Tanoby Ruins, câmara Rixy (Seven Island, Surf)", "Kanto"),
    "SevenIsland_TanobyRuins_ScufibChamber_Frlg": (100, "Tanoby Ruins, câmara Scufib (Seven Island, Surf)", "Kanto"),
    "SevenIsland_TanobyRuins_ViapoisChamber_Frlg": (100, "Tanoby Ruins, câmara Viapois (Seven Island, Surf)", "Kanto"),
    "SevenIsland_TanobyRuins_WeepthChamber_Frlg": (100, "Tanoby Ruins, câmara Weepth (Seven Island, Surf)", "Kanto"),
    # ---------------------------------------------------------------- Johto
    "IlexForest": (55, "Ilex Forest (Cut)", "Johto"),
    "BurnedTower_1F": (60, "Burned Tower, térreo (Ecruteak)", "Johto"),
    "BurnedTower_B1F": (60, "Burned Tower, subsolo (Ecruteak)", "Johto"),
    "RuinsOfAlph_WordsRoom1": (60, "Ruínas de Alph, sala escondida 1 (quebra-cabeça)", "Johto"),
    "RuinsOfAlph_WordsRoom2": (60, "Ruínas de Alph, sala escondida 2 (quebra-cabeça)", "Johto"),
    "RuinsOfAlph_WordsRoom3": (60, "Ruínas de Alph, sala escondida 3 (quebra-cabeça)", "Johto"),
    "MtMortar_B1F": (65, "Mt. Mortar, subsolo (Surf, Strength)", "Johto"),
    "MahoganyHideout_B3F": (65, "Esconderijo Rocket de Mahogany, sala dos geradores", "Johto"),
    "IcePath_1F": (70, "Ice Path (Strength)", "Johto"),
    "TinTower_1F": (70, "Tin Tower, térreo (Ecruteak, depois do sino)", "Johto"),
    "LcUnderseaSprings": (70, "Fontes submarinas do Liquid Crystal (Surf, Dive)", "Johto"),
    "TinTower_9F": (75, "Tin Tower, nono andar", "Johto"),
    "LcSafariForest": (75, "Safari do Liquid Crystal, floresta", "Johto"),
    "LcSafariMountain": (75, "Safari do Liquid Crystal, montanha", "Johto"),
    "LcSafariWater": (75, "Safari do Liquid Crystal, água", "Johto"),
    "LcHollowCaveChamber": (85, "Hollow Cave, câmara do fundo", "Johto"),
    "TinTower_RoofDay": (100, "Tin Tower, telhado (Ho-Oh)", "Johto"),
    "WhirlIslands_LugiaChamber": (100, "Whirl Islands, câmara do Lugia", "Johto"),
    "LcSilverCaveDepths": (100, "Silver Cave, fundo (Mt. Silver)", "Johto"),
    # ---------------------------------------------------------------- Hoenn
    "LittlerootTown_ProfessorBirchsLab": (50, "presente do laboratório do Birch (o mais cedo do jogo)", "Hoenn"),
    "PetalburgWoods": (50, "Petalburg Woods; começo de Hoenn", "Hoenn"),
    "PetalburgWoods_River": (55, "Petalburg Woods, o rio escondido", "Hoenn"),
    "errante (src/roamer.c)": (60, "errante pelas rotas de Hoenn", "Hoenn"),
    "FieryPath": (60, "Fiery Path (Mt. Chimney)", "Hoenn"),
    "NewMauville_Inside": (65, "New Mauville (Surf, chave de New Mauville)", "Hoenn"),
    "AbandonedShip_CaptainsOffice": (65, "Navio abandonado, cabine do capitão (Surf)", "Hoenn"),
    "MuscleIsland": (65, "Muscle Island (Surf)", "Hoenn"),
    "DontoIsland": (65, "Donto Island (Surf)", "Hoenn"),
    "HauntedWoods_Inner": (65, "Haunted Woods, miolo", "Hoenn"),
    "MtPyre_Summit": (70, "Mt. Pyre, cume", "Hoenn"),
    "ShoalCave_LowTideIceRoom": (70, "Shoal Cave, sala de gelo da maré baixa (Surf, Strength)", "Hoenn"),
    "AncientTomb": (75, "Ancient Tomb (Braille, Flash)", "Hoenn"),
    "DesertRuins": (75, "Desert Ruins (Braille, Rock Smash)", "Hoenn"),
    "IslandCave": (75, "Island Cave (Braille)", "Hoenn"),
    "SealedChamber_InnerRoom": (75, "Sealed Chamber, sala de dentro (Dive, Braille)", "Hoenn"),
    "CaveOfOrigin_B1F": (75, "Cave of Origin, fundo (Sootopolis)", "Hoenn"),
    "MeteorFalls_StevensCave": (75, "Meteor Falls, caverna do Steven (Waterfall)", "Hoenn"),
    "FrozenHeights": (75, "Frozen Heights", "Hoenn"),
    "SouthernIsland_Interior": (75, "Southern Island (ilha de evento)", "Hoenn"),
    "SkyPillar_4F": (80, "Sky Pillar, quarto andar (Mach Bike)", "Hoenn"),
    "SkyPillar_Top": (80, "Sky Pillar, topo", "Hoenn"),
    "MarineCave_End": (80, "Marine Cave, fundo (Dive)", "Hoenn"),
    "TerraCave_End": (80, "Terra Cave, fundo", "Hoenn"),
    "FarawayIsland_Interior": (80, "Faraway Island (ilha de evento)", "Hoenn"),
    "BirthIsland_Exterior": (80, "Birth Island (ilha de evento)", "Hoenn"),
    "NavelRock_Top": (85, "Navel Rock, cume (ilha de evento)", "Hoenn"),
    "NavelRock_Bottom": (85, "Navel Rock, fundo (ilha de evento)", "Hoenn"),
    # ---------------------------------------------------------------- Sinnoh
    "EternaForest": (60, "Eterna Forest (Cut, canto fechado)", "Sinnoh"),
    "FloaromaMeadow": (60, "Floaroma Meadow, atrás da cidade", "Sinnoh"),
    "OreburghMine_B2F": (60, "Oreburgh Mine, fundo", "Sinnoh"),
    "Route209LostTower5F": (65, "Lost Tower, topo (Route 209)", "Sinnoh"),
    "WaywardCaveB1F": (65, "Wayward Cave, subsolo (Strength, Flash)", "Sinnoh"),
    "OldChateauBackMiddleRoom": (65, "Old Chateau, sala dos fundos (Cut)", "Sinnoh"),
    "GreatMarsh6": (65, "Great Marsh (Pastoria)", "Sinnoh"),
    "IronIslandB3F": (70, "Iron Island, fundo (balsa de Canalave)", "Sinnoh"),
    "AcuityCavern": (70, "caverna do Lake Acuity", "Sinnoh"),
    "ValorCavern": (70, "caverna do Lake Valor", "Sinnoh"),
    "VerityCavern": (70, "caverna do Lake Verity", "Sinnoh"),
    "IronIslandIronRuins": (75, "Iron Island, ruínas (balsa de Canalave)", "Sinnoh"),
    "GalacticHQ_Laboratory": (75, "QG da Galáctica, laboratório (Veilstone)", "Sinnoh"),
    "MtCoronet_B1F": (75, "Mt. Coronet, subsolo (Surf, Strength)", "Sinnoh"),
    "MtCoronet6F": (80, "Mt. Coronet, sexto andar (Rock Climb)", "Sinnoh"),
    "SinnohVictoryRoad1F": (80, "Victory Road de Sinnoh (Waterfall, Rock Climb)", "Sinnoh"),
    "SpearPillar_Dialga": (80, "Spear Pillar, depois da cena da Galáctica", "Sinnoh"),
    "SpearPillar_Palkia": (80, "Spear Pillar, depois da cena da Galáctica", "Sinnoh"),
    "SpringPath": (80, "Spring Path (Route 214, pós-Liga de Sinnoh)", "Sinnoh"),
    "SendoffSpring": (85, "Sendoff Spring (Route 214 e Spring Path, pós-Liga de Sinnoh)", "Sinnoh"),
    "SnowpointTempleB5F": (85, "Snowpoint Temple, fundo", "Sinnoh"),
    "SpearPillar": (90, "Spear Pillar, depois de pegar Dialga e Palkia", "Sinnoh"),
    "Route224": (90, "Route 224, ponta norte (pós-Liga de Sinnoh, Surf)", "Sinnoh"),
    "SpearPillar_Distorted": (95, "Spear Pillar distorcido", "Sinnoh"),
    "DistortionWorld": (100, "Distortion World", "Sinnoh"),
    "DistortionWorldTurnbackCaveRoom": (100, "Turnback Cave inteira, sala de passagem do Distortion World", "Sinnoh"),
}

# Mapas com `map_type` de cidade que NÃO são cidade: a conversão de Sinnoh
# marcou floresta, lago e rota como MAP_TYPE_TOWN. Lendário pode morar neles.
NAO_E_CIDADE = {"EternaForest", "LakeAcuity", "LakeValor", "Route219", "Route220",
                "ValleyWindworks"}


def nivel_no_mapa(mapa):
    """O nível de qualquer lendário que mora em `mapa`. Mapa fora da tabela é erro."""
    if mapa not in NIVEL:
        raise KeyError(f"{mapa}: mapa com lendário sem nível em dev_scripts/niveis_lendarios.py")
    return NIVEL[mapa][0]


def acesso(mapa):
    return NIVEL[mapa][1]


def regiao(mapa):
    return NIVEL[mapa][2]
