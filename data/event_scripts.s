#include "config/general.h"
#include "config/battle.h"
#include "config/item.h"
#include "constants/global.h"
#include "constants/apprentice.h"
#include "constants/apricorn_tree.h"
#include "constants/battle.h"
#include "constants/battle_arena.h"
#include "constants/battle_dome.h"
#include "constants/battle_factory.h"
#include "constants/battle_frontier.h"
#include "constants/battle_palace.h"
#include "constants/battle_pike.h"
#include "constants/battle_pyramid.h"
#include "constants/battle_setup.h"
#include "constants/battle_special.h"
#include "constants/battle_tent.h"
#include "constants/battle_tower.h"
#include "constants/berry.h"
#include "constants/cable_club.h"
#include "constants/coins.h"
#include "constants/comparison_operators.h"
#include "constants/contest.h"
#include "constants/daycare.h"
#include "constants/decorations.h"
#include "constants/difficulty.h"
#include "constants/easy_chat.h"
#include "constants/event_objects.h"
#include "constants/event_object_movement.h"
#include "constants/fame_checker.h"
#include "constants/field_effects.h"
#include "constants/field_move.h"
#include "constants/field_poison.h"
#include "constants/field_specials.h"
#include "constants/field_tasks.h"
#include "constants/field_weather.h"
#include "constants/flags.h"
#include "constants/follower_npc.h"
#include "constants/frontier_util.h"
#include "constants/game_stat.h"
#include "constants/item.h"
#include "constants/items.h"
#include "constants/heal_locations.h"
#include "constants/layouts.h"
#include "constants/lilycove_lady.h"
#include "constants/map_scripts.h"
#include "constants/maps.h"
#include "constants/mauville_old_man.h"
#include "constants/metatile_labels.h"
#include "constants/move_relearner.h"
#include "constants/moves.h"
#include "constants/mystery_gift.h"
#include "constants/party_menu.h"
#include "constants/pokeball.h"
#include "constants/pokedex.h"
#include "constants/pokemon.h"
#include "constants/pokemon_size_record.h"
#include "constants/random_mon_generation.h"
#include "constants/rtc.h"
#include "constants/roulette.h"
#include "constants/script_menu.h"
#include "constants/seagallop.h"
#include "constants/secret_bases.h"
#include "constants/siirtc.h"
#include "constants/sliding_puzzles.h"
#include "constants/songs.h"
#include "constants/sound.h"
#include "constants/species.h"
#include "constants/trade.h"
#include "constants/trainer_hill.h"
#include "constants/trainer_tower.h"
#include "constants/trainers.h"
#include "constants/trainer_card.h"
#include "constants/tv.h"
#include "constants/union_room.h"
#include "constants/vars.h"
#include "constants/weather.h"
#include "constants/speaker_names.h"
	.include "asm/macros.inc"
	.include "asm/macros/event.inc"
	.include "constants/constants.inc"

	.section script_data, "aw", %progbits

	.set ALLOCATE_SCRIPT_CMD_TABLE, 1
	.include "data/script_cmd_table.inc"

.align 2
gSpecialVars::
	.4byte gSpecialVar_0x8000
	.4byte gSpecialVar_0x8001
	.4byte gSpecialVar_0x8002
	.4byte gSpecialVar_0x8003
	.4byte gSpecialVar_0x8004
	.4byte gSpecialVar_0x8005
	.4byte gSpecialVar_0x8006
	.4byte gSpecialVar_0x8007
	.4byte gSpecialVar_0x8008
	.4byte gSpecialVar_0x8009
	.4byte gSpecialVar_0x800A
	.4byte gSpecialVar_0x800B
	.4byte gSpecialVar_Facing
	.4byte gSpecialVar_Result
	.4byte gSpecialVar_ItemId
	.4byte gSpecialVar_LastTalked
	.4byte gSpecialVar_ContestRank
	.4byte gSpecialVar_ContestCategory
	.4byte gSpecialVar_MonBoxId
	.4byte gSpecialVar_MonBoxPos
	.4byte gSpecialVar_Unused_0x8014
	.4byte gTrainerBattleParameter + 2 // gTrainerBattleParameter.params.opponentA

	.purgem def_special
	.set ALLOCATE_SPECIAL_TABLE, 1
	.include "data/specials.inc"

gStdScripts::
	.4byte Std_ObtainItem              @ STD_OBTAIN_ITEM
	.4byte Std_FindItem                @ STD_FIND_ITEM
	.4byte Std_MsgboxNPC               @ MSGBOX_NPC
	.4byte Std_MsgboxSign              @ MSGBOX_SIGN
	.4byte Std_MsgboxDefault           @ MSGBOX_DEFAULT
	.4byte Std_MsgboxYesNo             @ MSGBOX_YESNO
	.4byte Std_MsgboxAutoclose         @ MSGBOX_AUTOCLOSE
	.4byte Std_ObtainDecoration        @ STD_OBTAIN_DECORATION
	.4byte Std_RegisteredInMatchCall   @ STD_REGISTER_MATCH_CALL
	.4byte Std_MsgboxGetPoints         @ MSGBOX_GETPOINTS
	.4byte Std_MsgboxPokenav           @ MSGBOX_POKENAV
	.4byte Std_PutItemAway             @ STD_PUT_ITEM_AWAY
	.4byte Std_ReceivedItem            @ STD_RECEIVED_ITEM
gStdScripts_End::


	.include "data/maps/PetalburgCity/scripts.inc"
	.include "data/maps/SlateportCity/scripts.inc"
	.include "data/maps/MauvilleCity/scripts.inc"
	.include "data/maps/RustboroCity/scripts.inc"
	.include "data/maps/FortreeCity/scripts.inc"
	.include "data/maps/LilycoveCity/scripts.inc"
	.include "data/maps/MossdeepCity/scripts.inc"
	.include "data/maps/SootopolisCity/scripts.inc"
	.include "data/maps/EverGrandeCity/scripts.inc"
	.include "data/maps/LittlerootTown/scripts.inc"
	.include "data/maps/DewfordTown/scripts.inc"
	.include "data/maps/LavaridgeTown/scripts.inc"
	.include "data/maps/Route102/scripts.inc"
	.include "data/maps/Route103/scripts.inc"
	.include "data/maps/Route104/scripts.inc"
	.include "data/maps/Route105/scripts.inc"
	.include "data/maps/Route106/scripts.inc"
	.include "data/maps/Route107/scripts.inc"
	.include "data/maps/Route108/scripts.inc"
	.include "data/maps/Route109/scripts.inc"
	.include "data/maps/Route110/scripts.inc"
	.include "data/maps/Route111/scripts.inc"
	.include "data/maps/Route112/scripts.inc"
	.include "data/maps/Route113/scripts.inc"
	.include "data/maps/Route114/scripts.inc"
	.include "data/maps/Route115/scripts.inc"
	.include "data/maps/Route116/scripts.inc"
	.include "data/maps/Route117/scripts.inc"
	.include "data/maps/Route118/scripts.inc"
	.include "data/maps/Route119/scripts.inc"
	.include "data/maps/Route120/scripts.inc"
	.include "data/maps/Route121/scripts.inc"
	.include "data/maps/Route122/scripts.inc"
	.include "data/maps/Route123/scripts.inc"
	.include "data/maps/Route124/scripts.inc"
	.include "data/maps/Route125/scripts.inc"
	.include "data/maps/Route126/scripts.inc"
	.include "data/maps/Route127/scripts.inc"
	.include "data/maps/Route128/scripts.inc"
	.include "data/maps/Route129/scripts.inc"
	.include "data/maps/Route130/scripts.inc"
	.include "data/maps/Route131/scripts.inc"
	.include "data/maps/Route132/scripts.inc"
	.include "data/maps/Route133/scripts.inc"
	.include "data/maps/Route134/scripts.inc"
	.include "data/maps/Underwater_Route127/scripts.inc"
	.include "data/maps/Underwater_Route129/scripts.inc"
	.include "data/maps/Underwater_Route105/scripts.inc"
	.include "data/maps/Underwater_Route125/scripts.inc"
	.include "data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc"
	.include "data/maps/LittlerootTown_BrendansHouse_2F/scripts.inc"
	.include "data/maps/LittlerootTown_MaysHouse_1F/scripts.inc"
	.include "data/maps/LittlerootTown_MaysHouse_2F/scripts.inc"
	.include "data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc"
	.include "data/maps/OldaleTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/OldaleTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/OldaleTown_Mart/scripts.inc"
	.include "data/maps/DewfordTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/DewfordTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/DewfordTown_Gym/scripts.inc"
	.include "data/maps/LavaridgeTown_Gym_1F/scripts.inc"
	.include "data/maps/LavaridgeTown_Gym_B1F/scripts.inc"
	.include "data/maps/LavaridgeTown_Mart/scripts.inc"
	.include "data/maps/LavaridgeTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/LavaridgeTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/FallarborTown_Mart/scripts.inc"
	.include "data/maps/FallarborTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/FallarborTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/VerdanturfTown_Mart/scripts.inc"
	.include "data/maps/VerdanturfTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/VerdanturfTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/PacifidlogTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/PacifidlogTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/PetalburgCity_Gym/scripts.inc"
	.include "data/maps/PetalburgCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/PetalburgCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/PetalburgCity_Mart/scripts.inc"
	.include "data/maps/SlateportCity_SternsShipyard_1F/scripts.inc"
	.include "data/maps/SlateportCity_SternsShipyard_2F/scripts.inc"
	.include "data/maps/SlateportCity_NameRatersHouse/scripts.inc"
	.include "data/maps/SlateportCity_Harbor/scripts.inc"
	.include "data/maps/SlateportCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/SlateportCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/SlateportCity_Mart/scripts.inc"
	.include "data/maps/MauvilleCity_Gym/scripts.inc"
	.include "data/maps/MauvilleCity_BikeShop/scripts.inc"
	.include "data/maps/MauvilleCity_GameCorner/scripts.inc"
	.include "data/maps/MauvilleCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/MauvilleCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/MauvilleCity_Mart/scripts.inc"
	.include "data/maps/RustboroCity_Gym/scripts.inc"
	.include "data/maps/RustboroCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/RustboroCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/RustboroCity_Mart/scripts.inc"
	.include "data/maps/FortreeCity_Gym/scripts.inc"
	.include "data/maps/FortreeCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/FortreeCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/FortreeCity_Mart/scripts.inc"
	.include "data/maps/LilycoveCity_CoveLilyMotel_1F/scripts.inc"
	.include "data/maps/LilycoveCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/LilycoveCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/LilycoveCity_Harbor/scripts.inc"
	.include "data/maps/LilycoveCity_MoveDeletersHouse/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_1F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_2F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_3F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_4F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_5F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStoreRooftop/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStoreElevator/scripts.inc"
	.include "data/maps/MossdeepCity_Gym/scripts.inc"
	.include "data/maps/MossdeepCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/MossdeepCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/MossdeepCity_Mart/scripts.inc"
	.include "data/maps/MossdeepCity_SpaceCenter_1F/scripts.inc"
	.include "data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc"
	.include "data/maps/SootopolisCity_Gym_1F/scripts.inc"
	.include "data/maps/SootopolisCity_Gym_B1F/scripts.inc"
	.include "data/maps/SootopolisCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/SootopolisCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/SootopolisCity_Mart/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonLeague_1F/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonLeague_2F/scripts.inc"
	.include "data/maps/Route112_CableCarStation/scripts.inc"
	.include "data/maps/MtChimney_CableCarStation/scripts.inc"
	.include "data/maps/Route117_PokemonDayCare/scripts.inc"
	.include "data/maps/Route121_SafariZoneEntrance/scripts.inc"
	.include "data/maps/MeteorFalls_1F_1R/scripts.inc"
	.include "data/maps/MeteorFalls_1F_2R/scripts.inc"
	.include "data/maps/RusturfTunnel/scripts.inc"
	.include "data/maps/Underwater_SootopolisCity/scripts.inc"
	.include "data/maps/DesertRuins/scripts.inc"
	.include "data/maps/PetalburgWoods/scripts.inc"
	.include "data/maps/MtChimney/scripts.inc"
	.include "data/maps/JaggedPass/scripts.inc"
	.include "data/maps/MtPyre_3F/scripts.inc"
	.include "data/maps/MtPyre_6F/scripts.inc"
	.include "data/maps/MtPyre_Summit/scripts.inc"
	.include "data/maps/CaveOfOrigin_Entrance/scripts.inc"
	.include "data/maps/VictoryRoad_1F/scripts.inc"
	.include "data/maps/NewMauville_Inside/scripts.inc"
	.include "data/maps/AbandonedShip_Rooms_1F/scripts.inc"
	.include "data/maps/AbandonedShip_Rooms2_1F/scripts.inc"
	.include "data/maps/IslandCave/scripts.inc"
	.include "data/maps/AncientTomb/scripts.inc"
	.include "data/maps/SealedChamber_OuterRoom/scripts.inc"
	.include "data/maps/SkyPillar_Outside/scripts.inc"
	.include "data/maps/ShoalCave_LowTideIceRoom/scripts.inc"
	.include "data/maps/SkyPillar_Top/scripts.inc"
	.include "data/maps/Underwater_MarineCave/scripts.inc"
	.include "data/maps/MarineCave_Entrance/scripts.inc"
	.include "data/maps/MarineCave_End/scripts.inc"
	.include "data/maps/TerraCave_Entrance/scripts.inc"
	.include "data/maps/TerraCave_End/scripts.inc"
	.include "data/maps/AlteringCave/scripts.inc"
	.include "data/scripts/shared_secret_base.inc"
	.include "data/scripts/portas_fechadas.inc"
	.include "data/scripts/travessia_regioes.inc"
	.include "data/maps/BattleColosseum_2P/scripts.inc"
	.include "data/maps/TradeCenter/scripts.inc"
	.include "data/maps/RecordCorner/scripts.inc"
	.include "data/maps/BattleColosseum_4P/scripts.inc"
	.include "data/maps/ContestHall/scripts.inc"
	.include "data/maps/InsideOfTruck/scripts.inc"
	.include "data/maps/SSTidalCorridor/scripts.inc"
	.include "data/maps/SSTidalLowerDeck/scripts.inc"
	.include "data/maps/SSTidalRooms/scripts.inc"
	.include "data/maps/BattlePyramidSquare01/scripts.inc"
	.include "data/maps/UnionRoom/scripts.inc"
	.include "data/maps/SafariZone_Northwest/scripts.inc"
	.include "data/maps/SafariZone_North/scripts.inc"
	.include "data/maps/SafariZone_Southwest/scripts.inc"
	.include "data/maps/SafariZone_South/scripts.inc"
	.include "data/maps/BattleFrontier_OutsideWest/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerElevator/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerBattleRoom/scripts.inc"
	.include "data/maps/SouthernIsland_Exterior/scripts.inc"
	.include "data/maps/SouthernIsland_Interior/scripts.inc"
	.include "data/maps/SafariZone_Northeast/scripts.inc"
	.include "data/maps/SafariZone_Southeast/scripts.inc"
	.include "data/maps/BattleFrontier_OutsideEast/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerMultiPartnerRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerMultiCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerMultiBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleDomeLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattleDomeCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattleDomePreBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleDomeBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePalaceLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePalaceCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePalaceBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePyramidLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePyramidFloor/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePyramidTop/scripts.inc"
	.include "data/maps/BattleFrontier_BattleArenaLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattleArenaCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattleArenaBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleFactoryLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattleFactoryPreBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattleFactoryBattleRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeLobby/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeThreePathRoom/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeRoomNormal/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeRoomFinal/scripts.inc"
	.include "data/maps/BattleFrontier_BattlePikeRoomWildMons/scripts.inc"
	.include "data/maps/BattleFrontier_ExchangeServiceCorner/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge2/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge3/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge5/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge7/scripts.inc"
	.include "data/maps/BattleFrontier_PokemonCenter_1F/scripts.inc"
	.include "data/maps/BattleFrontier_PokemonCenter_2F/scripts.inc"
	.include "data/maps/BattleFrontier_Mart/scripts.inc"
	.include "data/maps/FarawayIsland_Interior/scripts.inc"
	.include "data/maps/BirthIsland_Exterior/scripts.inc"
	.include "data/maps/TrainerHill_Entrance/scripts.inc"
	.include "data/maps/TrainerHill_2F/scripts.inc"
	.include "data/maps/TrainerHill_3F/scripts.inc"
	.include "data/maps/TrainerHill_4F/scripts.inc"
	.include "data/maps/TrainerHill_Roof/scripts.inc"
	.include "data/maps/Route110_TrickHouseEntrance/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle1/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle2/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle3/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle4/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle5/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle6/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle7/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle8/scripts.inc"
	.include "data/maps/Route110_SeasideCyclingRoadNorthEntrance/scripts.inc"
	.include "data/maps/Route119_WeatherInstitute_1F/scripts.inc"
	.include "data/maps/Route119_WeatherInstitute_2F/scripts.inc"


	@ Mapas de Sinnoh
	.include "data/maps/AcuityLakefront/scripts.inc"
	.include "data/maps/CanalaveCity/scripts.inc"
	.include "data/maps/EternaCity/scripts.inc"
	.include "data/maps/EternaForest/scripts.inc"
	.include "data/maps/FloaromaTown_FlowerShop/scripts.inc"
	.include "data/maps/FloaromaTown_House1/scripts.inc"
	.include "data/maps/FloaromaTown_House2/scripts.inc"
	.include "data/maps/FloaromaTown_Mart/scripts.inc"
	.include "data/maps/FloaromaTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/FloaromaTwon_PokemonCenter_2F/scripts.inc"
	.include "data/maps/HearthomeCity/scripts.inc"
	.include "data/maps/HotelGrandLake/scripts.inc"
	.include "data/maps/JubilifeCity_Flat1_F1/scripts.inc"
	.include "data/maps/JubilifeCity_Flat1_F3/scripts.inc"
	.include "data/maps/JubilifeCity_Flat2_F2/scripts.inc"
	.include "data/maps/JubilifeCity_Flat2_F3/scripts.inc"
	.include "data/maps/JubilifeCity_Flat3_F1/scripts.inc"
	.include "data/maps/JubilifeCity_Flat3_F3/scripts.inc"
	.include "data/maps/JubilifeCity_JubilifeTV_F1/scripts.inc"
	.include "data/maps/JubilifeCity_JubilifeTV_F2/scripts.inc"
	.include "data/maps/JubilifeCity_JubilifeTV_F4/scripts.inc"
	.include "data/maps/JubilifeCity_Mart/scripts.inc"
	.include "data/maps/JubilifeCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/JubilifeCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/JubilifeCity_PokemonSchool/scripts.inc"
	.include "data/maps/LakeAcuity/scripts.inc"
	.include "data/maps/LakeValor/scripts.inc"
	.include "data/maps/LakeVerity/scripts.inc"
	.include "data/maps/MtCoronet_1F_North_Room1/scripts.inc"
	.include "data/maps/MtCoronet_1F_South/scripts.inc"
	.include "data/maps/MtCoronet_B1F/scripts.inc"
	.include "data/maps/OreburghCity_Flat1_F1/scripts.inc"
	.include "data/maps/OreburghCity_Flat1_F2/scripts.inc"
	.include "data/maps/OreburghCity_Flat2_F1/scripts.inc"
	.include "data/maps/OreburghCity_Flat2_F2/scripts.inc"
	.include "data/maps/OreburghCity_Flat3_F1/scripts.inc"
	.include "data/maps/OreburghCity_Flat3_F2/scripts.inc"
	.include "data/maps/OreburghCity_House1/scripts.inc"
	.include "data/maps/OreburghCity_House3/scripts.inc"
	.include "data/maps/OreburghCity_Mart/scripts.inc"
	.include "data/maps/OreburghCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/OreburghCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/OreburghGate_1F/scripts.inc"
	.include "data/maps/OreburghMine_B1F/scripts.inc"
	.include "data/maps/OreburghMine_B2F/scripts.inc"
	.include "data/maps/PastoriaCity/scripts.inc"
	.include "data/maps/PokmonLeague/scripts.inc"
	.include "data/maps/RavagedPath/scripts.inc"
	.include "data/maps/Route205_North/scripts.inc"
	.include "data/maps/Route213/scripts.inc"
	.include "data/maps/Route214/scripts.inc"
	.include "data/maps/Route215/scripts.inc"
	.include "data/maps/Route216/scripts.inc"
	.include "data/maps/Route217/scripts.inc"
	.include "data/maps/Route218/scripts.inc"
	.include "data/maps/Route219/scripts.inc"
	.include "data/maps/Route220/scripts.inc"
	.include "data/maps/Route223/scripts.inc"
	.include "data/maps/Route224/scripts.inc"
	.include "data/maps/SandgemTown_House1/scripts.inc"
	.include "data/maps/SandgemTown_RowanLab/scripts.inc"
	.include "data/maps/SandgemTown_Mart/scripts.inc"
	.include "data/maps/SandgemTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/SandgemTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/SandgemTown_RivalHouse_F1/scripts.inc"
	.include "data/maps/SnowpointCity/scripts.inc"
	.include "data/maps/SolaceonTown/scripts.inc"
	.include "data/maps/SunyshoreCity/scripts.inc"
	.include "data/maps/TwinleafTown_Haouse1/scripts.inc"
	.include "data/maps/TwinleafTown_House2/scripts.inc"
	.include "data/maps/TwinleafTown_MainHouse_1F/scripts.inc"
	.include "data/maps/Twinleaf_Town_RivalsHouse_F1/scripts.inc"
	.include "data/maps/Twinleaf_Town_RivalsHouse_F2/scripts.inc"
	.include "data/maps/ValleyWindworks/scripts.inc"
	.include "data/maps/ValorLakefront/scripts.inc"
	.include "data/maps/VeilstoneCity/scripts.inc"
	.include "data/maps/VerityLakefront/scripts.inc"
	.include "data/maps/EternaCity_Gym/scripts.inc"
	.include "data/maps/VeilstoneCity_Gym/scripts.inc"
	.include "data/maps/PastoriaCity_Gym/scripts.inc"
	.include "data/maps/HearthomeCity_Gym/scripts.inc"
	.include "data/maps/CanalaveCity_Gym/scripts.inc"
	.include "data/maps/SnowpointCity_Gym/scripts.inc"
	.include "data/maps/SunyshoreCity_Gym/scripts.inc"
@ Os 418 scripts de Kanto ficavam fechados aqui por .if IS_FRLG. Nesta ROM as
@ cinco regioes convivem, entao Kanto precisa dos scripts dela compilados.

@ FRLG scripts
	.include "data/maps/BattleColosseum_2P_Frlg/scripts.inc"
	.include "data/maps/TradeCenter_Frlg/scripts.inc"
	.include "data/maps/BattleColosseum_4P_Frlg/scripts.inc"
	.include "data/maps/UnionRoom_Frlg/scripts.inc"
	.include "data/maps/ViridianForest_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B1F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B2F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B4F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_1F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_2F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_3F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_4F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_5F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_6F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_7F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_8F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_9F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_10F_Frlg/scripts.inc"
	.include "data/maps/SilphCo_11F_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_ChampionsRoom_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B3F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B4F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_1F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_2F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_3F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_4F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_5F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_6F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_7F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Exterior_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_1F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_2F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_3F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_4F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_5F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_6F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_7F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_8F_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_Roof_Frlg/scripts.inc"
	.include "data/maps/TrainerTower_Lobby_Frlg/scripts.inc"
	.include "data/maps/BirthIsland_Exterior_Frlg/scripts.inc"
	.include "data/maps/BirthIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Harbor_Frlg/scripts.inc"
	.include "data/maps/PalletTown_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_Frlg/scripts.inc"
	.include "data/maps/IndigoPlateau_Exterior_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Frlg/scripts.inc"
	.include "data/maps/Route10_Frlg/scripts.inc"
	.include "data/maps/Route17_Frlg/scripts.inc"
	.include "data/maps/Route21_North_Frlg/scripts.inc"
	.include "data/maps/Route23_Frlg/scripts.inc"
	.include "data/maps/Route25_Frlg/scripts.inc"
	.include "data/maps/SixIsland_RuinValley_Frlg/scripts.inc"
	.include "data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_1F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_2F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_3F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_4F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_5F_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/OneIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/FourIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/SixIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Harbor_Frlg/scripts.inc"

	.include "data/scripts/trainer_tower.inc"
	.include "data/scripts/cable_club_frlg.inc"
	.include "data/text/new_game_intro_frlg.inc"
	.include "data/scripts/flavor_text.inc"
	.include "data/scripts/pkmn_center_nurse_frlg.inc"

@ (antes: .endif do .if IS_FRLG que fechava os scripts de Kanto)

	.include "data/scripts/std_msgbox.inc"
	.include "data/scripts/trainer_battle.inc"
	.include "data/scripts/new_game.inc"

	.include "data/scripts/config.inc"
	.include "data/scripts/debug.inc"

EventScript_WhiteOut::
	call EverGrandeCity_HallOfFame_EventScript_ResetEliteFour
	goto EventScript_ResetMrBriney
	end

EventScript_AfterWhiteOutHeal::
	lockall
	msgbox gText_FirstShouldRestoreMonsHealth
	call EventScript_PkmnCenterNurse_TakeAndHealPkmn
	call_if_unset FLAG_DEFEATED_RUSTBORO_GYM, EventScript_AfterWhiteOutHealMsgPreFirstBoss
	call_if_set FLAG_DEFEATED_RUSTBORO_GYM, EventScript_AfterWhiteOutHealMsg
	applymovement VAR_LAST_TALKED, Movement_PkmnCenterNurse_Bow
	waitmovement 0
	fadedefaultbgm
	releaseall
	end

EventScript_AfterWhiteOutHealMsgPreFirstBoss::
	msgbox gText_MonsHealedShouldBuyPotions
	return

EventScript_AfterWhiteOutHealMsg::
	msgbox gText_MonsHealed
	return

EventScript_AfterWhiteOutMomHeal::
	lockall
	textcolor NPC_TEXT_COLOR_FEMALE
	applymovement LOCALID_PLAYERS_HOUSE_1F_MOM, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox gText_HadQuiteAnExperienceTakeRest
	call Common_EventScript_OutOfCenterPartyHeal
	msgbox gText_MomExplainHPGetPotions
	fadedefaultbgm
	releaseall
	end

EventScript_ResetMrBriney::
	goto_if_eq VAR_BRINEY_LOCATION, 1, EventScript_MoveMrBrineyToHouse
	goto_if_eq VAR_BRINEY_LOCATION, 2, EventScript_MoveMrBrineyToDewford
	goto_if_eq VAR_BRINEY_LOCATION, 3, EventScript_MoveMrBrineyToRoute109
	end

EventScript_MoveMrBrineyToHouse::
	setflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	clearflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	clearflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	clearflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	end

EventScript_MoveMrBrineyToDewford::
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	clearflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	clearflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	end

EventScript_MoveMrBrineyToRoute109::
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	setflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	clearflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	clearflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	end

EverGrandeCity_HallOfFame_EventScript_ResetEliteFour::
	clearflag FLAG_DEFEATED_ELITE_4_SIDNEY
	clearflag FLAG_DEFEATED_ELITE_4_PHOEBE
	clearflag FLAG_DEFEATED_ELITE_4_GLACIA
	clearflag FLAG_DEFEATED_ELITE_4_DRAKE
	setvar VAR_ELITE_4_STATE, 0
	return

Common_EventScript_UpdateBrineyLocation::
	goto_if_unset FLAG_RECEIVED_POKENAV, Common_EventScript_NopReturn
	goto_if_set FLAG_DEFEATED_PETALBURG_GYM, Common_EventScript_NopReturn
	goto_if_unset FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT, EventScript_SetBrineyLocation_House
	goto_if_unset FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN, EventScript_SetBrineyLocation_Dewford
	goto_if_unset FLAG_HIDE_ROUTE_109_MR_BRINEY, EventScript_SetBrineyLocation_Route109
	return

EventScript_SetBrineyLocation_House::
	setvar VAR_BRINEY_LOCATION, 1
	return

EventScript_SetBrineyLocation_Dewford::
	setvar VAR_BRINEY_LOCATION, 2
	return

EventScript_SetBrineyLocation_Route109::
	setvar VAR_BRINEY_LOCATION, 3
	return

	.include "data/scripts/pkmn_center_nurse.inc"
	.include "data/scripts/obtain_item.inc"
	.include "data/scripts/pc.inc"
	.include "data/scripts/move_relearner.inc"

@ scripts/notices.inc? signs.inc? See comment about text/notices.inc
Common_EventScript_ShowPokemartSign::
	msgbox gText_PokemartSign, MSGBOX_SIGN
	end

Common_EventScript_ShowPokemonCenterSign::
	msgbox gText_PokemonCenterSign, MSGBOX_SIGN
	end

Common_ShowEasyChatScreen::
	fadescreen FADE_TO_BLACK
	special ShowEasyChatScreen
	fadescreen FADE_FROM_BLACK
	return

Common_EventScript_ReadyPetalburgGymForBattle::
	clearflag FLAG_HIDE_PETALBURG_GYM_GREETER
	setflag FLAG_PETALBURG_MART_EXPANDED_ITEMS
	return

Common_EventScript_BufferTrendyPhrase::
	dotimebasedevents
	setvar VAR_0x8004, 0
	special BufferTrendyPhraseString
	return

EventScript_BackupMrBrineyLocation::
	copyvar VAR_0x8008, VAR_BRINEY_LOCATION
	setvar VAR_BRINEY_LOCATION, 0
	return

	.include "data/scripts/surf.inc"
	.include "data/scripts/rival_graphics.inc"
	.include "data/scripts/set_gym_trainers.inc"

EventScript_CancelMessageBox::
	special UseBlankMessageToCancelPokemonPic
	release
	end

Common_EventScript_ShowBagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	release
	end

Common_EventScript_BagIsFull::
	msgbox gText_TooBadBagIsFull, MSGBOX_DEFAULT
	return

EventScript_BagIsFull::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	msgbox gText_TooBadBagIsFull
	release
	end

Common_EventScript_ShowNoRoomForDecor::
	msgbox gText_NoRoomLeftForAnother, MSGBOX_DEFAULT
	release
	end

Common_EventScript_NoRoomForDecor::
	msgbox gText_NoRoomLeftForAnother, MSGBOX_DEFAULT
	return

Common_EventScript_SetAbnormalWeather::
	setweather WEATHER_ABNORMAL
	return

Common_EventScript_PlayGymBadgeFanfare::
	playfanfare MUS_OBTAIN_BADGE
	waitfanfare
	return

Common_EventScript_OutOfCenterPartyHeal::
	fadescreenswapbuffers FADE_TO_BLACK
	playfanfare MUS_HEAL
	waitfanfare
	special HealPlayerParty
	callnative UpdateFollowingPokemon
	fadescreenswapbuffers FADE_FROM_BLACK
	return

EventScript_RegionMap::
	lockall
	msgbox Common_Text_LookCloserAtMap, MSGBOX_DEFAULT
	fadescreen FADE_TO_BLACK
	special FieldShowRegionMap
	releaseall
	end

Common_EventScript_PlayBrineysBoatMusic::
	setflag FLAG_DONT_TRANSITION_MUSIC
	playbgm MUS_SAILING, FALSE
	return

Common_EventScript_StopBrineysBoatMusic::
	clearflag FLAG_DONT_TRANSITION_MUSIC
	fadedefaultbgm
	return

	.include "data/scripts/prof_birch.inc"

@ Below could be split as ferry.inc aside from the Rusturf tunnel script
Common_EventScript_FerryDepart::
	delay 60
	applymovement VAR_0x8004, Movement_FerryDepart
	waitmovement 0
	return

Movement_FerryDepart:
	walk_slow_right
	walk_slow_right
	walk_slow_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

EventScript_HideMrBriney::
	setflag FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN
	setflag FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_109_MR_BRINEY_BOAT
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY
	setflag FLAG_HIDE_ROUTE_104_MR_BRINEY_BOAT
	setflag FLAG_HIDE_BRINEYS_HOUSE_MR_BRINEY
	setflag FLAG_HIDE_BRINEYS_HOUSE_PEEKO
	setvar VAR_BRINEY_LOCATION, 0
	return

RusturfTunnel_EventScript_SetRusturfTunnelOpen::
	removeobject LOCALID_RUSTURF_TUNNEL_WANDAS_BF
	removeobject LOCALID_RUSTURF_TUNNEL_WANDA
	clearflag FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDAS_BOYFRIEND
	clearflag FLAG_HIDE_VERDANTURF_TOWN_WANDAS_HOUSE_WANDA
	setvar VAR_RUSTURF_TUNNEL_STATE, 6
	setflag FLAG_RUSTURF_TUNNEL_OPENED
	return

EventScript_UnusedBoardFerry::
	delay 30
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterUp
	waitmovement 0
	showplayer
	delay 30
	applymovement LOCALID_PLAYER, Movement_UnusedBoardFerry
	waitmovement 0
	delay 30
	return

Movement_UnusedBoardFerry:
	walk_up
	step_end

Common_EventScript_FerryDepartIsland::
	call_if_eq VAR_FACING, DIR_SOUTH, Ferry_EventScript_DepartIslandSouth
	call_if_eq VAR_FACING, DIR_WEST, Ferry_EventScript_DepartIslandWest
	delay 30
	hideplayer
	call Common_EventScript_FerryDepart
	return

	.include "data/scripts/kecleon.inc"

Common_EventScript_NameReceivedPartyMon::
	fadescreen FADE_TO_BLACK
	special ChangePokemonNickname
	return

Common_EventScript_PlayerHandedOverTheItem::
	bufferitemname STR_VAR_1, VAR_0x8004
	playfanfare MUS_OBTAIN_TMHM
	message gText_PlayerHandedOverTheItem
	waitmessage
	waitfanfare
	removeitem VAR_0x8004
	return

	.include "data/scripts/movement.inc"
	.include "data/scripts/check_furniture.inc"
	.include "data/scripts/mart_clerk.inc"
	.include "data/text/pc.inc"
	.include "data/text/pkmn_center_nurse.inc"
	.include "data/text/obtain_item.inc"
	.include "data/text/move_relearner.inc"

@ The below and surf.inc could be split into some text/notices.inc
gText_PokemartSign::
	.string "“Selected items for your convenience!”\n"
	.string "POKéMON MART$"

gText_PokemonCenterSign::
	.string "“Rejuvenate your tired partners!”\n"
	.string "POKéMON CENTER$"

gText_MomOrDadMightLikeThisProgram::
	.string "{STR_VAR_1} might like this program.\n"
	.string "… … … … … … … … … … … … … … … …\p"
	.string "Better get going!$"

gText_WhichFloorWouldYouLike::
	.string "Welcome to LILYCOVE DEPARTMENT STORE.\p"
	.string "Which floor would you like?$"

gText_SandstormIsVicious::
	.string "The sandstorm is vicious.\n"
	.string "It's impossible to keep going.$"

gText_SelectWithoutRegisteredItem::
	.string "An item in the BAG can be\n"
	.string "registered to SELECT for easy use.$"

gText_PokemonTrainerSchoolEmail::
	.string "There's an e-mail from POKéMON TRAINER\n"
	.string "SCHOOL.\p"
	.string "… … … … … …\p"
	.string "A POKéMON may learn up to four moves.\p"
	.string "A TRAINER's expertise is tested on the\n"
	.string "move sets chosen for POKéMON.\p"
	.string "… … … … … …$"

gText_PlayerHouseBootPC::
	.string "{PLAYER} booted up the PC.$"

gText_PokeblockLinkCanceled::
	.string "The link was canceled.$"

gText_UnusedNicknameReceivedPokemon::
	.string "Want to give a nickname to\n"
	.string "the {STR_VAR_2} you received?$"

gText_PlayerWhitedOut::
	.string "{PLAYER} is out of usable\n"
	.string "POKéMON!\p{PLAYER} whited out!$"

gText_FirstShouldRestoreMonsHealth::
	.string "First, you should restore your\n"
	.string "POKéMON to full health.$"

gText_MonsHealedShouldBuyPotions::
	.string "Your POKéMON have been healed\n"
	.string "to perfect health.\p"
	.string "If your POKéMON's energy, HP,\n"
	.string "is down, please come see us.\p"
	.string "If you're planning to go far in the\n"
	.string "field, you should buy some POTIONS\l"
	.string "at the POKéMON MART.\p"
	.string "We hope you excel!$"

gText_MonsHealed::
	.string "Your POKéMON have been healed\n"
	.string "to perfect health.\p"
	.string "We hope you excel!$"

gText_HadQuiteAnExperienceTakeRest::
	.string "MOM: {PLAYER}!\n"
	.string "Welcome home.\p"
	.string "It sounds like you had quite\n"
	.string "an experience.\p"
	.string "Maybe you should take a quick\n"
	.string "rest.$"

gText_MomExplainHPGetPotions::
	.string "MOM: Oh, good! You and your\n"
	.string "POKéMON are looking great.\p"
	.string "I just heard from {STR_VAR_1}.\p"
	.string "He said that POKéMON's energy is\n"
	.string "measured in HP.\p"
	.string "If your POKéMON lose their HP,\n"
	.string "you can restore them at any\l"
	.string "POKéMON CENTER.\p"
	.string "If you're going to travel far away,\n"
	.string "the smart TRAINER stocks up on\l"
	.string "POTIONS at the POKéMON MART.\p"
	.string "Make me proud, honey!\p"
	.string "Take care!$"

gText_RegisteredTrainerinPokeNav::
	.string "Registered {STR_VAR_1} {STR_VAR_2}\n"
	.string "in the POKéNAV.$"

gText_ComeBackWithSecretPower::
	.string "Do you know the TM SECRET POWER?\p"
	.string "Our group, we love the TM SECRET\n"
	.string "POWER.\p"
	.string "One of our members will give it to you.\n"
	.string "Come back and show me if you get it.\p"
	.string "We'll accept you as a member and sell\n"
	.string "you good stuff in secrecy.$"

gText_PokerusExplanation::
	.string "Your POKéMON may be infected with\n"
	.string "POKéRUS.\p"
	.string "Little is known about the POKéRUS\n"
	.string "except that they are microscopic life-\l"
	.string "forms that attach to POKéMON.\p"
	.string "While infected, POKéMON are said to\n"
	.string "grow exceptionally well.$"

	.include "data/text/surf.inc"

gText_DoorOpenedFarAway::
	.string "It sounded as if a door opened\n"
	.string "somewhere far away.$"

gText_BigHoleInTheWall::
	.string "There is a big hole in the wall.$"

gText_SorryWirelessClubAdjustments::
	.string "I'm terribly sorry.\n"
	.string "The POKéMON WIRELESS CLUB is\l"
	.string "undergoing adjustments now.$"

gText_UndergoingAdjustments::
	.string "It appears to be undergoing\n"
	.string "adjustments…$"

@ Unused
gText_SorryTradeCenterInspections::
	.string "I'm terribly sorry. The TRADE CENTER\n"
	.string "is undergoing inspections.$"

@ Unused
gText_SorryRecordCornerPreparation::
	.string "I'm terribly sorry. The RECORD CORNER\n"
	.string "is under preparation.$"

gText_PlayerHandedOverTheItem::
	.string "{PLAYER} handed over the\n"
	.string "{STR_VAR_1}.$"

gText_ThankYouForAccessingMysteryGift::
	.string "Thank you for accessing the\n"
	.string "MYSTERY GIFT System.$"

gText_PlayerFoundOneTMHM::
	.string "{PLAYER} found one {STR_VAR_1}\n"
	.string "{STR_VAR_2}!$"

gText_PlayerFoundTMHMs::
	.string "{PLAYER} found {STR_VAR_3} {STR_VAR_1}\n"
	.string "{STR_VAR_2}!$"

gText_Sudowoodo_Attacked::
	.string "The weird tree doesn't like the\n"
	.string "WAILMER PAIL!\p"
	.string "The weird tree attacked!$"

gText_LegendaryFlewAway::
	.string "The {STR_VAR_1} flew away!$"

gText_WantWhichFloor::
	.string "Which floor do you want?$"

	.include "data/text/pc_transfer.inc"
	.include "data/text/questionnaire.inc"
	.include "data/text/abnormal_weather.inc"

EventScript_GetInGameTradeSpeciesInfo::
	copyvar VAR_0x8005, VAR_0x8008
	specialvar VAR_0x8009, GetInGameTradeSpeciesInfo
	return

EventScript_ChooseMonForInGameTrade::
	special ChoosePartyMon
	lock
	faceplayer
	return

EventScript_GetInGameTradeSpecies::
	specialvar VAR_RESULT, GetTradeSpecies
	return

EventScript_DoInGameTrade::
	special CreateInGameTradePokemon
	special DoInGameTradeScene
	lock
	faceplayer
	return

EventScript_SelectWithoutRegisteredItem::
	msgbox gText_SelectWithoutRegisteredItem, MSGBOX_SIGN
	end

	.include "data/scripts/field_poison.inc"

Common_EventScript_NopReturn::
	return

EventScript_SetResultTrue::
	setvar VAR_RESULT, TRUE
	return

EventScript_SetResultFalse::
	setvar VAR_RESULT, FALSE
	return

EventScript_GetElevatorFloor::
	special GetElevatorFloor
	return

@ Unused
EventScript_CableClub_SetVarResult1::
	setvar VAR_RESULT, 1
	return

EventScript_CableClub_SetVarResult0::
	setvar VAR_RESULT, 0
	return

Common_EventScript_UnionRoomAttendant::
#if IS_FRLG
	call CableClub_EventScript_UnionRoomAttendant_Frlg
#else
	call CableClub_EventScript_UnionRoomAttendant
#endif
	end

Common_EventScript_WirelessClubAttendant::
#if IS_FRLG
	call CableClub_EventScript_WirelessClubAttendant_Frlg
#else
	call CableClub_EventScript_WirelessClubAttendant
#endif
	end

Common_EventScript_DirectCornerAttendant::
#if IS_FRLG
	call CableClub_EventScript_DirectCornerAttendant_Frlg
#else
	call CableClub_EventScript_DirectCornerAttendant
#endif
	end

Common_EventScript_RemoveStaticPokemon::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreenswapbuffers FADE_FROM_BLACK
	release
	end

Common_EventScript_LegendaryFlewAway::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreenswapbuffers FADE_FROM_BLACK
	bufferspeciesname STR_VAR_1, VAR_0x8004
	msgbox gText_LegendaryFlewAway, MSGBOX_DEFAULT
	release
	end

EventScript_VsSeekerChargingDone::
	special VsSeekerFreezeObjectsAfterChargeComplete
	waitstate
	special VsSeekerResetObjectMovementAfterChargeComplete
	releaseall
	end

@ FRLG scripts

EventScript_SetExitingCyclingRoad::
	lockall
	clearflag FLAG_SYS_ON_CYCLING_ROAD
	setvar VAR_MAP_SCENE_ROUTE16, 0
	releaseall
	end

EventScript_SetEnteringCyclingRoad::
	lockall
	setvar VAR_MAP_SCENE_ROUTE16, 1
	releaseall
	end

EventScript_TryDarkenRuins::
	goto_if_set FLAG_SYS_UNLOCKED_TANOBY_RUINS, Common_EventScript_NopReturn
	setweather WEATHER_SHADE
	doweather
	return

Text_MonFlewAway::
	.string "The {STR_VAR_1} flew away!$"

@ Call for legendary bird trio
Text_Gyaoo::
	.string "Gyaoo!$"

EventScript_BrailleCursorWaitButton::
	special BrailleCursorToggle
	waitbuttonpress
	closebraillemessage
	playse SE_SELECT
	setvar VAR_0x8006, 1
	special BrailleCursorToggle
	return

EventScript_PalletTown_PlayersHouse_2F_ShutDownPC::
	setvar VAR_0x8004, PC_LOCATION_PLAYER_HOUSE_FRLG
	playse SE_PC_OFF
	special DoPCTurnOffEffect
	releaseall
	end

EventScript_PalletTown_PlayersHouse_2F_TurnOnPC::
	lockall
	setvar VAR_0x8004, PC_LOCATION_PLAYER_HOUSE_FRLG
	special DoPCTurnOnEffect
	playse SE_PC_ON
	msgbox gText_PlayerHouseBootPC
	special BedroomPC
	releaseall
	end


	.include "data/scripts/pc_transfer.inc"
	.include "data/scripts/questionnaire.inc"
	.include "data/scripts/abnormal_weather.inc"
	.include "data/scripts/trainer_script.inc"
	.include "data/scripts/berry_tree.inc"
	.include "data/scripts/secret_base.inc"
	.include "data/scripts/cable_club.inc"
	.include "data/text/cable_club.inc"
	.include "data/scripts/contest_hall.inc"
	.include "data/scripts/tv.inc"
	.include "data/text/tv.inc"
	.include "data/scripts/interview.inc"
	.include "data/scripts/gabby_and_ty.inc"
	.include "data/text/pokemon_news.inc"
	.include "data/scripts/mauville_man.inc"
	.include "data/scripts/field_move_scripts.inc"
	.include "data/scripts/item_ball_scripts.inc"
	.include "data/scripts/day_care.inc"
	.include "data/scripts/flash.inc"
	.include "data/scripts/players_house.inc"
	.include "data/text/mauville_man.inc"
	.include "data/text/trainers.inc"
	.include "data/scripts/repel.inc"
	.include "data/scripts/safari_zone.inc"
	.include "data/text/pokedex_rating.inc"
	.include "data/text/event_ticket_1.inc"
	.include "data/text/braille.inc"
	.include "data/text/berries.inc"
	.include "data/text/check_furniture.inc"
	.include "data/scripts/cave_hole.inc"
	.include "data/text/match_call.inc"
	.include "data/scripts/apprentice.inc"
	.include "data/text/apprentice.inc"
	.include "data/scripts/battle_pike.inc"
	.include "data/text/event_ticket_2.inc"
	.include "data/text/move_tutors.inc"
	.include "data/scripts/move_tutors.inc"
	.include "data/scripts/trainer_hill.inc"
	.include "data/scripts/test_signpost.inc"
	.include "data/scripts/follower.inc"
	.include "data/text/save.inc"
	.include "data/text/birch_speech.inc"
	.include "data/scripts/dexnav.inc"
	.include "data/scripts/battle_frontier.inc"
	.include "data/scripts/wild_encounter.inc"

	.include "data/maps/NewBarkTown/scripts.inc"
	.include "data/maps/WorldHub2/scripts.inc"

	.include "data/maps/AzaleaTown_Mart/scripts.inc"
	.include "data/maps/AzaleaTown_PokemonCenter/scripts.inc"
	.include "data/maps/BlackthornCity_Mart/scripts.inc"
	.include "data/maps/BlackthornCity_PokemonCenter/scripts.inc"
	.include "data/maps/CherrygroveCity_Mart/scripts.inc"
	.include "data/maps/CherrygroveCity_PokemonCenter/scripts.inc"
	.include "data/maps/CianwoodPokecenter/scripts.inc"
	.include "data/maps/CianwoodShop/scripts.inc"
	.include "data/maps/EcruteakCity_Mart/scripts.inc"
	.include "data/maps/EcruteakCity_PokemonCenter/scripts.inc"
	.include "data/maps/GoldenrodCity_PokemonCenter/scripts.inc"
	.include "data/maps/MahoganyTown_PokemonCenter/scripts.inc"
	.include "data/maps/MahoganyTown_Shop/scripts.inc"
	.include "data/maps/OlivineCity_Mart/scripts.inc"
	.include "data/maps/OlivineCity_PokemonCenter/scripts.inc"
	.include "data/maps/SecretBase_BlueCave1/scripts.inc"
	.include "data/maps/SecretBase_BlueCave2/scripts.inc"
	.include "data/maps/SecretBase_BlueCave3/scripts.inc"
	.include "data/maps/SecretBase_BlueCave4/scripts.inc"
	.include "data/maps/SecretBase_BrownCave1/scripts.inc"
	.include "data/maps/SecretBase_BrownCave2/scripts.inc"
	.include "data/maps/SecretBase_BrownCave3/scripts.inc"
	.include "data/maps/SecretBase_BrownCave4/scripts.inc"
	.include "data/maps/SecretBase_RedCave1/scripts.inc"
	.include "data/maps/SecretBase_RedCave2/scripts.inc"
	.include "data/maps/SecretBase_RedCave3/scripts.inc"
	.include "data/maps/SecretBase_RedCave4/scripts.inc"
	.include "data/maps/SecretBase_Shrub1/scripts.inc"
	.include "data/maps/SecretBase_Shrub2/scripts.inc"
	.include "data/maps/SecretBase_Shrub3/scripts.inc"
	.include "data/maps/SecretBase_Shrub4/scripts.inc"
	.include "data/maps/SecretBase_Tree1/scripts.inc"
	.include "data/maps/SecretBase_Tree2/scripts.inc"
	.include "data/maps/SecretBase_Tree3/scripts.inc"
	.include "data/maps/SecretBase_Tree4/scripts.inc"
	.include "data/maps/SecretBase_YellowCave1/scripts.inc"
	.include "data/maps/SecretBase_YellowCave2/scripts.inc"
	.include "data/maps/SecretBase_YellowCave3/scripts.inc"
	.include "data/maps/SecretBase_YellowCave4/scripts.inc"
	.include "data/maps/VioletCity_Mart/scripts.inc"
	.include "data/maps/VioletCity_PokemonCenter/scripts.inc"

	@ Mapas de Unova (BW3G, de Azure_Keys)
	.include "data/maps/Unova_GiantChasm1F/scripts.inc"
	.include "data/maps/Unova_GiantChasmRooms/scripts.inc"
	.include "data/maps/Unova_GiantChasmB1F/scripts.inc"
	.include "data/maps/Unova_ReversalMountain1F/scripts.inc"
	.include "data/maps/Unova_ReversalMountainB1F/scripts.inc"
	.include "data/maps/Unova_StrangeHouse1F/scripts.inc"
	.include "data/maps/Unova_StrangeHouseB1F/scripts.inc"
	.include "data/maps/Unova_StrangeHouseRooms/scripts.inc"
	.include "data/maps/Unova_LostlornForest/scripts.inc"
	.include "data/maps/Unova_RelicCastle1F/scripts.inc"
	.include "data/maps/Unova_RelicCastleB1F/scripts.inc"
	.include "data/maps/Unova_RelicCastleB2F/scripts.inc"
	.include "data/maps/Unova_RelicCastleB3F/scripts.inc"
	.include "data/maps/Unova_RelicCastleB4F/scripts.inc"
	.include "data/maps/Unova_NimbasaParkCoasterRoom/scripts.inc"
	.include "data/maps/Unova_NimbasaParkRunway/scripts.inc"
	.include "data/maps/Unova_NimbasaParkBasement/scripts.inc"
	.include "data/maps/Unova_VirbankComplexElevator/scripts.inc"
	.include "data/maps/Unova_VirbankComplexB1F/scripts.inc"
	.include "data/maps/Unova_VirbankComplexB2F/scripts.inc"
	.include "data/maps/Unova_PinwheelForest/scripts.inc"
	.include "data/maps/Unova_WellspringCave1F/scripts.inc"
	.include "data/maps/Unova_WellspringCaveB1F/scripts.inc"
	.include "data/maps/Unova_P2LabEntrance/scripts.inc"
	.include "data/maps/Unova_P2Lab/scripts.inc"
	.include "data/maps/Unova_SeasideCave1F/scripts.inc"
	.include "data/maps/Unova_SeasideCaveB1F/scripts.inc"
	.include "data/maps/Unova_CasteliaSewers/scripts.inc"
	.include "data/maps/Unova_CasteliaSewersRooms/scripts.inc"
	.include "data/maps/Unova_RelicPassageFront/scripts.inc"
	.include "data/maps/Unova_RelicPassageBack/scripts.inc"
	.include "data/maps/Unova_ChargestoneCave1F/scripts.inc"
	.include "data/maps/Unova_ChargestoneCaveB1F/scripts.inc"
	.include "data/maps/Unova_ChargestoneCaveB2F/scripts.inc"
	.include "data/maps/Unova_CelestialTower1F/scripts.inc"
	.include "data/maps/Unova_CelestialTower/scripts.inc"
	.include "data/maps/Unova_CelestialTowerRoof/scripts.inc"
	.include "data/maps/Unova_SeasideCaveB2F/scripts.inc"
	.include "data/maps/Unova_SeasideCaveChamber/scripts.inc"
	.include "data/maps/Unova_DragonspiralTowerOutside/scripts.inc"
	.include "data/maps/Unova_DragonspiralTower1F/scripts.inc"
	.include "data/maps/Unova_DragonspiralTower2F/scripts.inc"
	.include "data/maps/Unova_DragonspiralTower3F/scripts.inc"
	.include "data/maps/Unova_DragonspiralTower4F/scripts.inc"
	.include "data/maps/Unova_DragonspiralTower5F/scripts.inc"
	.include "data/maps/Unova_DragonspiralTower6F/scripts.inc"
	.include "data/maps/Unova_DragonspiralTowerRoof/scripts.inc"
	.include "data/maps/Unova_MistraltonCave1F/scripts.inc"
	.include "data/maps/Unova_MistraltonCave2F/scripts.inc"
	.include "data/maps/Unova_MistraltonCave3F/scripts.inc"
	.include "data/maps/Unova_TwistMountainEntrance/scripts.inc"
	.include "data/maps/Unova_Dreamyard/scripts.inc"
	.include "data/maps/Unova_DreamyardB1F/scripts.inc"
	.include "data/maps/Unova_VictoryRoadCave1F/scripts.inc"
	.include "data/maps/Unova_VictoryRoadCave2F/scripts.inc"
	.include "data/maps/Unova_VictoryRoadCave3F/scripts.inc"
	.include "data/maps/Unova_VictoryRoadOutdoor1F/scripts.inc"
	.include "data/maps/Unova_VictoryRoadOutdoor2F/scripts.inc"
	.include "data/maps/Unova_VictoryRoadGrove/scripts.inc"
	.include "data/maps/Unova_VictoryRoadCastleOutside/scripts.inc"
	.include "data/maps/Unova_NsRoom/scripts.inc"
	.include "data/maps/Unova_TwistMountain1F/scripts.inc"
	.include "data/maps/Unova_TwistMountain2F/scripts.inc"
	.include "data/maps/Unova_TwistMountain3F/scripts.inc"
	.include "data/maps/Unova_TwistMountainOutside/scripts.inc"
	.include "data/maps/Unova_TwistMountainHouse/scripts.inc"
	.include "data/maps/Unova_TwistMountainB1F/scripts.inc"
	.include "data/maps/Unova_TwistMountainGenesectRoom/scripts.inc"
	.include "data/maps/Unova_Pokecenter2F/scripts.inc"
	.include "data/maps/Unova_TradeCenter/scripts.inc"
	.include "data/maps/Unova_Colosseum/scripts.inc"
	.include "data/maps/Unova_TimeCapsule/scripts.inc"
	.include "data/maps/Unova_MobileTradeRoom/scripts.inc"
	.include "data/maps/Unova_MobileBattleRoom/scripts.inc"
	.include "data/maps/Unova_PlayersHouse1F/scripts.inc"
	.include "data/maps/Unova_PlayersHouse2F/scripts.inc"
	.include "data/maps/Unova_HumilauCity/scripts.inc"
	.include "data/maps/Unova_HumilauPokecenter1F/scripts.inc"
	.include "data/maps/Unova_MarlonsHouse/scripts.inc"
	.include "data/maps/Unova_PlayersNeighborsHouse/scripts.inc"
	.include "data/maps/Unova_HumilauTradeHouse/scripts.inc"
	.include "data/maps/Unova_HumilauGym/scripts.inc"
	.include "data/maps/Unova_R22/scripts.inc"
	.include "data/maps/Unova_Rt21/scripts.inc"
	.include "data/maps/Unova_Rt13/scripts.inc"
	.include "data/maps/Unova_LacunosaTown/scripts.inc"
	.include "data/maps/Unova_LacunosaPokecenter1F/scripts.inc"
	.include "data/maps/Unova_Rt12/scripts.inc"
	.include "data/maps/Unova_LacunosaHouse/scripts.inc"
	.include "data/maps/Unova_LacunosaHouse2/scripts.inc"
	.include "data/maps/Unova_Rt12VillageBridgeGate/scripts.inc"
	.include "data/maps/Unova_Rt13UndellaGate/scripts.inc"
	.include "data/maps/Unova_UndellaTown/scripts.inc"
	.include "data/maps/Unova_UndellaPokecenter1F/scripts.inc"
	.include "data/maps/Unova_UndellaOldRodHouse/scripts.inc"
	.include "data/maps/Unova_MarineTubeEntrance/scripts.inc"
	.include "data/maps/Unova_MarineTube/scripts.inc"
	.include "data/maps/Unova_Rt14/scripts.inc"
	.include "data/maps/Unova_CaitlinsHouse/scripts.inc"
	.include "data/maps/Unova_LentimasOutskirts/scripts.inc"
	.include "data/maps/Unova_LentimasTown/scripts.inc"
	.include "data/maps/Unova_LentimasCoinHouse/scripts.inc"
	.include "data/maps/Unova_LentimasPokecenter1F/scripts.inc"
	.include "data/maps/Unova_LentimasHouse/scripts.inc"
	.include "data/maps/Unova_LentimasGym/scripts.inc"
	.include "data/maps/Unova_LentimasLostlornGate/scripts.inc"
	.include "data/maps/Unova_LentimasAirport/scripts.inc"
	.include "data/maps/Unova_NimbasaCity/scripts.inc"
	.include "data/maps/Unova_NimbasaTMMart/scripts.inc"
	.include "data/maps/Unova_NimbasaVitaminMart/scripts.inc"
	.include "data/maps/Unova_NimbasaBallMart/scripts.inc"
	.include "data/maps/Unova_NimbasaPokecenter1F/scripts.inc"
	.include "data/maps/Unova_NimbasaHouse/scripts.inc"
	.include "data/maps/Unova_NimbasaNameRater/scripts.inc"
	.include "data/maps/Unova_Rt4NimbasaGate/scripts.inc"
	.include "data/maps/Unova_NimbasaSubway/scripts.inc"
	.include "data/maps/Unova_NimbasaParkOutside/scripts.inc"
	.include "data/maps/Unova_Rt16/scripts.inc"
	.include "data/maps/Unova_Rt16LostlornGate/scripts.inc"
	.include "data/maps/Unova_Rt16NimbasaGate/scripts.inc"
	.include "data/maps/Unova_Rt5/scripts.inc"
	.include "data/maps/Unova_Rt5NimbasaGate/scripts.inc"
	.include "data/maps/Unova_Rt5BridgeGate/scripts.inc"
	.include "data/maps/Unova_Rt5Truck/scripts.inc"
	.include "data/maps/Unova_Rt4/scripts.inc"
	.include "data/maps/Unova_Rt4House/scripts.inc"
	.include "data/maps/Unova_Rt4CasteliaGate/scripts.inc"
	.include "data/maps/Unova_DesertResort/scripts.inc"
	.include "data/maps/Unova_Rt4DesertGate/scripts.inc"
	.include "data/maps/Unova_CasteliaCityNorth/scripts.inc"
	.include "data/maps/Unova_CasteliaCityStreets/scripts.inc"
	.include "data/maps/Unova_CasteliaCitySouth/scripts.inc"
	.include "data/maps/Unova_CasteliaPokecenter1F/scripts.inc"
	.include "data/maps/Unova_CasteliaBikeShop/scripts.inc"
	.include "data/maps/Unova_CasteliaMassage/scripts.inc"
	.include "data/maps/Unova_CasteliaGameFreak/scripts.inc"
	.include "data/maps/Unova_CasteliaBridgeGate/scripts.inc"
	.include "data/maps/Unova_BattleCompany1F/scripts.inc"
	.include "data/maps/Unova_BattleCompany2F/scripts.inc"
	.include "data/maps/Unova_CasteliaGym/scripts.inc"
	.include "data/maps/Unova_CasteliaPort/scripts.inc"
	.include "data/maps/Unova_FerryLeft/scripts.inc"
	.include "data/maps/Unova_PinwheelBridgeGate/scripts.inc"
	.include "data/maps/Unova_SkyarrowBridge/scripts.inc"
	.include "data/maps/Unova_CasteliaTradeHouse1/scripts.inc"
	.include "data/maps/Unova_CasteliaTradeHouse2/scripts.inc"
	.include "data/maps/Unova_CasteliaPlazaLobby/scripts.inc"
	.include "data/maps/Unova_CasteliaPlazaGameCorner/scripts.inc"
	.include "data/maps/Unova_CasteliaPlazaPrizeRoom/scripts.inc"
	.include "data/maps/Unova_CasteliaPlazaRestaurant/scripts.inc"
	.include "data/maps/Unova_CasteliaPlazaElevator/scripts.inc"
	.include "data/maps/Unova_AspertiaCity/scripts.inc"
	.include "data/maps/Unova_AspertiaSubway/scripts.inc"
	.include "data/maps/Unova_AspertiaBlackbeltHouse/scripts.inc"
	.include "data/maps/Unova_AspertiaPokecenter1F/scripts.inc"
	.include "data/maps/Unova_AspertiaMomHouse/scripts.inc"
	.include "data/maps/Unova_AspertiaMoveDeleterHouse/scripts.inc"
	.include "data/maps/Unova_AspertiaGym/scripts.inc"
	.include "data/maps/Unova_Rt19AspertiaGate/scripts.inc"
	.include "data/maps/Unova_FloccesyTown/scripts.inc"
	.include "data/maps/Unova_FloccesyPokecenter1F/scripts.inc"
	.include "data/maps/Unova_Rt19/scripts.inc"
	.include "data/maps/Unova_Rt20/scripts.inc"
	.include "data/maps/Unova_FloccesyRanch/scripts.inc"
	.include "data/maps/Unova_FloccesyRanchBarn/scripts.inc"
	.include "data/maps/Unova_FloccesyRanchHouse/scripts.inc"
	.include "data/maps/Unova_FloccesyTownHouse/scripts.inc"
	.include "data/maps/Unova_FloccesyTradeHouse/scripts.inc"
	.include "data/maps/Unova_AldersHouse/scripts.inc"
	.include "data/maps/Unova_VirbankCity/scripts.inc"
	.include "data/maps/Unova_VirbankPokecenter1F/scripts.inc"
	.include "data/maps/Unova_VirbankHouse/scripts.inc"
	.include "data/maps/Unova_GameCorner/scripts.inc"
	.include "data/maps/Unova_Rt20VirbankGate/scripts.inc"
	.include "data/maps/Unova_VirbankStatExpHouse/scripts.inc"
	.include "data/maps/Unova_VirbankGym/scripts.inc"
	.include "data/maps/Unova_VirbankPort/scripts.inc"
	.include "data/maps/Unova_FerryRight/scripts.inc"
	.include "data/maps/Unova_VirbankComplexOutside/scripts.inc"
	.include "data/maps/Unova_NacreneOutskirt/scripts.inc"
	.include "data/maps/Unova_NacreneOutskirtEast/scripts.inc"
	.include "data/maps/Unova_NacreneOutskirtConnectionDummy/scripts.inc"
	.include "data/maps/Unova_NacreneCity/scripts.inc"
	.include "data/maps/Unova_NacrenePokecenter1F/scripts.inc"
	.include "data/maps/Unova_NacreneStatExpHouse/scripts.inc"
	.include "data/maps/Unova_NacreneHouse/scripts.inc"
	.include "data/maps/Unova_NacreneCafe/scripts.inc"
	.include "data/maps/Unova_NacreneMuseum/scripts.inc"
	.include "data/maps/Unova_Rt3NacreneGate/scripts.inc"
	.include "data/maps/Unova_Rt3/scripts.inc"
	.include "data/maps/Unova_Rt3DayCare/scripts.inc"
	.include "data/maps/Unova_StriatonCity/scripts.inc"
	.include "data/maps/Unova_StriatonPokecenter1F/scripts.inc"
	.include "data/maps/Unova_StriatonTradeHouse/scripts.inc"
	.include "data/maps/Unova_StriatonLab/scripts.inc"
	.include "data/maps/Unova_StriatonGym/scripts.inc"
	.include "data/maps/Unova_Rt2/scripts.inc"
	.include "data/maps/Unova_Rt2AccumulaGate/scripts.inc"
	.include "data/maps/Unova_AccumulaTown/scripts.inc"
	.include "data/maps/Unova_AccumulaPokecenter1F/scripts.inc"
	.include "data/maps/Unova_AccumulaBallManiacHouse/scripts.inc"
	.include "data/maps/Unova_AccumulaHouse/scripts.inc"
	.include "data/maps/Unova_AccumulaTradeHouse/scripts.inc"
	.include "data/maps/Unova_Rt1/scripts.inc"
	.include "data/maps/Unova_NuvemaTown/scripts.inc"
	.include "data/maps/Unova_NuvemaMomHouse/scripts.inc"
	.include "data/maps/Unova_NuvemaLab/scripts.inc"
	.include "data/maps/Unova_Rt1Rt17Gate/scripts.inc"
	.include "data/maps/Unova_Rt17/scripts.inc"
	.include "data/maps/Unova_Rt18/scripts.inc"
	.include "data/maps/Unova_Rt18House/scripts.inc"
	.include "data/maps/Unova_PWTOutside/scripts.inc"
	.include "data/maps/Unova_PWTInside/scripts.inc"
	.include "data/maps/Unova_PWTHallway/scripts.inc"
	.include "data/maps/Unova_PWTQualifierRoom/scripts.inc"
	.include "data/maps/Unova_PWTBackRoom/scripts.inc"
	.include "data/maps/Unova_PWTBattleRoom/scripts.inc"
	.include "data/maps/Unova_DriftveilCity/scripts.inc"
	.include "data/maps/Unova_PWTDriftveilGate/scripts.inc"
	.include "data/maps/Unova_DriftveilPokecenter1F/scripts.inc"
	.include "data/maps/Unova_DriftveilFossilHouse/scripts.inc"
	.include "data/maps/Unova_DriftveilBridgeGate/scripts.inc"
	.include "data/maps/Unova_DriftveilShelter/scripts.inc"
	.include "data/maps/Unova_DriftveilDrawbridge/scripts.inc"
	.include "data/maps/Unova_DriftveilStoneEmporium/scripts.inc"
	.include "data/maps/Unova_DriftveilHouse/scripts.inc"
	.include "data/maps/Unova_DriftveilTradeHouse/scripts.inc"
	.include "data/maps/Unova_Rt6/scripts.inc"
	.include "data/maps/Unova_Rt6House/scripts.inc"
	.include "data/maps/Unova_Rt6Lab/scripts.inc"
	.include "data/maps/Unova_MistraltonCity/scripts.inc"
	.include "data/maps/Unova_MistraltonPokecenter1F/scripts.inc"
	.include "data/maps/Unova_MistraltonMoveReminderHouse/scripts.inc"
	.include "data/maps/Unova_MistraltonHouse/scripts.inc"
	.include "data/maps/Unova_MistraltonGym1F/scripts.inc"
	.include "data/maps/Unova_MistraltonGym2F/scripts.inc"
	.include "data/maps/Unova_MistraltonAirport/scripts.inc"
	.include "data/maps/Unova_PlaneLeft/scripts.inc"
	.include "data/maps/Unova_PlaneRight/scripts.inc"
	.include "data/maps/Unova_Rt7/scripts.inc"
	.include "data/maps/Unova_Rt7North/scripts.inc"
	.include "data/maps/Unova_Rt7House/scripts.inc"
	.include "data/maps/Unova_Rt7TradeHouse/scripts.inc"
	.include "data/maps/Unova_Rt11/scripts.inc"
	.include "data/maps/Unova_Rt11Truck/scripts.inc"
	.include "data/maps/Unova_Rt11OpelucidGate/scripts.inc"
	.include "data/maps/Unova_OpelucidCity/scripts.inc"
	.include "data/maps/Unova_Rt9OpelucidGate/scripts.inc"
	.include "data/maps/Unova_OpelucidPokecenter1F/scripts.inc"
	.include "data/maps/Unova_OpelucidBattleHouse/scripts.inc"
	.include "data/maps/Unova_OpelucidSuperRodHouse/scripts.inc"
	.include "data/maps/Unova_OpelucidGym/scripts.inc"
	.include "data/maps/Unova_OpelucidCuriosityShop/scripts.inc"
	.include "data/maps/Unova_OpelucidBlackbeltHouse/scripts.inc"
	.include "data/maps/Unova_DraydensHouse1F/scripts.inc"
	.include "data/maps/Unova_DraydensHouse2F/scripts.inc"
	.include "data/maps/Unova_Rt9/scripts.inc"
	.include "data/maps/Unova_ShoppingMallNine/scripts.inc"
	.include "data/maps/Unova_MembersRoom/scripts.inc"
	.include "data/maps/Unova_VillageBridge/scripts.inc"
	.include "data/maps/Unova_Rt11VillageBridgeGate/scripts.inc"
	.include "data/maps/Unova_TubelineBridge/scripts.inc"
	.include "data/maps/Unova_IcirrusCitySouthConnectionDummy/scripts.inc"
	.include "data/maps/Unova_IcirrusCitySouth/scripts.inc"
	.include "data/maps/Unova_IcirrusCityNorth/scripts.inc"
	.include "data/maps/Unova_Rt8/scripts.inc"
	.include "data/maps/Unova_MoorOfIcirrus/scripts.inc"
	.include "data/maps/Unova_IcirrusPokecenter1F/scripts.inc"
	.include "data/maps/Unova_IcirrusBoutique/scripts.inc"
	.include "data/maps/Unova_IcirrusHouse/scripts.inc"
	.include "data/maps/Unova_IcirrusFanClub/scripts.inc"
	.include "data/maps/Unova_IcirrusCave/scripts.inc"
	.include "data/maps/Unova_Rt23East/scripts.inc"
	.include "data/maps/Unova_Rt23West/scripts.inc"
	.include "data/maps/Unova_Rt23Gate/scripts.inc"
	.include "data/maps/Unova_Rt23House/scripts.inc"
	.include "data/maps/Unova_VictoryRoadEntranceSouthRight/scripts.inc"
	.include "data/maps/Unova_VictoryRoadEntranceSouthLeft/scripts.inc"
	.include "data/maps/Unova_VictoryRoadEntranceNorth/scripts.inc"
	.include "data/maps/Unova_VictoryRoadEntranceNorthConnectionDummy/scripts.inc"
	.include "data/maps/Unova_PkmnLeagueEntrance/scripts.inc"
	.include "data/maps/Unova_VictoryRoadPokecenter1F/scripts.inc"
	.include "data/maps/Unova_PkmnLeaguePokecenter1F/scripts.inc"
	.include "data/maps/Unova_PkmnLeagueMain/scripts.inc"
	.include "data/maps/Unova_GrimsleysRoom/scripts.inc"
	.include "data/maps/Unova_MarshalsRoom/scripts.inc"
	.include "data/maps/Unova_ElesasRoom/scripts.inc"
	.include "data/maps/Unova_ColresssRoom/scripts.inc"
	.include "data/maps/Unova_ChampionsRoomEntrance/scripts.inc"
	.include "data/maps/Unova_ChampionsRoom/scripts.inc"
	.include "data/maps/Unova_HallOfFame/scripts.inc"
	.include "data/scripts/chapter_jump.inc"
	.include "data/maps/Galar_Motostoke01/scripts.inc"
	.include "data/maps/Galar_StowOnSide01/scripts.inc"
	.include "data/maps/Galar_Hulbury01/scripts.inc"
	.include "data/maps/Galar_WildArea23/scripts.inc"
	.include "data/maps/Galar_StowOnSide02/scripts.inc"
	.include "data/maps/Galar_Postwick02/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor01/scripts.inc"
	.include "data/maps/Galar_CrownTundra01/scripts.inc"
	.include "data/maps/Galar_Postwick03/scripts.inc"
	.include "data/maps/Galar_CrownTundra02/scripts.inc"
	.include "data/maps/Galar_CrownTundraIndoor01/scripts.inc"
	.include "data/maps/Galar_DynamaxAdventure02/scripts.inc"
	.include "data/maps/Galar_Postwick06/scripts.inc"
	.include "data/maps/Galar_Postwick07/scripts.inc"
	.include "data/maps/Galar_Route0302/scripts.inc"
	.include "data/maps/Galar_SlumberingWeald01/scripts.inc"
	.include "data/maps/Galar_WarmUpTunnel01/scripts.inc"
	.include "data/maps/Galar_BrawlersCave01/scripts.inc"
	.include "data/maps/Galar_GalarMine01/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor02/scripts.inc"
	.include "data/maps/Galar_CourageousCavern01/scripts.inc"
	.include "data/maps/Galar_Underwater01/scripts.inc"
	.include "data/maps/Galar_Underwater02/scripts.inc"
	.include "data/maps/Galar_RoseTower01/scripts.inc"
	.include "data/maps/Galar_RoseTower02/scripts.inc"
	.include "data/maps/Galar_RoseTower03/scripts.inc"
	.include "data/maps/Galar_RoseTower04/scripts.inc"
	.include "data/maps/Galar_GlimwoodTangle01/scripts.inc"
	.include "data/maps/Galar_Postwick10/scripts.inc"
	.include "data/maps/Galar_CrownTundra03/scripts.inc"
	.include "data/maps/Galar_CrownTundra04/scripts.inc"
	.include "data/maps/Galar_Postwick11/scripts.inc"
	.include "data/maps/Galar_AlteringCave01/scripts.inc"
	.include "data/maps/Galar_TrainerTower01/scripts.inc"
	.include "data/maps/Galar_LostCave01/scripts.inc"
	.include "data/maps/Galar_LostCave02/scripts.inc"
	.include "data/maps/Galar_LostCave03/scripts.inc"
	.include "data/maps/Galar_LostCave04/scripts.inc"
	.include "data/maps/Galar_LostCave05/scripts.inc"
	.include "data/maps/Galar_LostCave06/scripts.inc"
	.include "data/maps/Galar_LostCave07/scripts.inc"
	.include "data/maps/Galar_LostCave08/scripts.inc"
	.include "data/maps/Galar_LostCave09/scripts.inc"
	.include "data/maps/Galar_LostCave10/scripts.inc"
	.include "data/maps/Galar_LostCave11/scripts.inc"
	.include "data/maps/Galar_LostCave12/scripts.inc"
	.include "data/maps/Galar_LostCave13/scripts.inc"
	.include "data/maps/Galar_Postwick12/scripts.inc"
	.include "data/maps/Galar_Wedgehurst12/scripts.inc"
	.include "data/maps/Galar_Motostoke23/scripts.inc"
	.include "data/maps/Galar_Turffield12/scripts.inc"
	.include "data/maps/Galar_Hulbury16/scripts.inc"
	.include "data/maps/Galar_Hammerlocke01/scripts.inc"
	.include "data/maps/Galar_Hammerlocke23/scripts.inc"
	.include "data/maps/Galar_Ballonlea10/scripts.inc"
	.include "data/maps/Galar_Circhester16/scripts.inc"
	.include "data/maps/Galar_Wyndon01/scripts.inc"
	.include "data/maps/Galar_Spikemuth09/scripts.inc"
	.include "data/maps/Galar_Route0101/scripts.inc"
	.include "data/maps/Galar_IceDreamCave01/scripts.inc"
	.include "data/maps/Galar_NewmoonIsland01/scripts.inc"
	.include "data/maps/Galar_Route1001/scripts.inc"
	.include "data/maps/Galar_WildArea01/scripts.inc"
	.include "data/maps/Galar_WildArea02/scripts.inc"
	.include "data/maps/Galar_RixyChamber01/scripts.inc"
	.include "data/maps/Galar_Motostoke02/scripts.inc"
	.include "data/maps/Galar_Postwick21/scripts.inc"
	.include "data/maps/Galar_Postwick22/scripts.inc"
	.include "data/maps/Galar_Postwick23/scripts.inc"
	.include "data/maps/Galar_Postwick24/scripts.inc"
	.include "data/maps/Galar_Route0102/scripts.inc"
	.include "data/maps/Galar_Postwick26/scripts.inc"
	.include "data/maps/Galar_Hammerlocke02/scripts.inc"
	.include "data/maps/Galar_Postwick27/scripts.inc"
	.include "data/maps/Galar_SlumberingWeald02/scripts.inc"
	.include "data/maps/Galar_SlumberingWeald03/scripts.inc"
	.include "data/maps/Galar_SlumberingWeald04/scripts.inc"
	.include "data/maps/Galar_Wedgehurst01/scripts.inc"
	.include "data/maps/Galar_Postwick31/scripts.inc"
	.include "data/maps/Galar_Wedgehurst02/scripts.inc"
	.include "data/maps/Galar_Wedgehurst13/scripts.inc"
	.include "data/maps/Galar_Wedgehurst03/scripts.inc"
	.include "data/maps/Galar_Wedgehurst04/scripts.inc"
	.include "data/maps/Galar_Wedgehurst05/scripts.inc"
	.include "data/maps/Galar_Route0204/scripts.inc"
	.include "data/maps/Galar_Wedgehurst06/scripts.inc"
	.include "data/maps/Galar_Route0201/scripts.inc"
	.include "data/maps/Galar_Postwick34/scripts.inc"
	.include "data/maps/Galar_Wedgehurst07/scripts.inc"
	.include "data/maps/Galar_Route0202/scripts.inc"
	.include "data/maps/Galar_Route0203/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor03/scripts.inc"
	.include "data/maps/Galar_CrownTundra05/scripts.inc"
	.include "data/maps/Galar_Wedgehurst08/scripts.inc"
	.include "data/maps/Galar_Motostoke03/scripts.inc"
	.include "data/maps/Galar_Motostoke04/scripts.inc"
	.include "data/maps/Galar_Postwick35/scripts.inc"
	.include "data/maps/Galar_WildArea24/scripts.inc"
	.include "data/maps/Galar_Motostoke05/scripts.inc"
	.include "data/maps/Galar_Postwick37/scripts.inc"
	.include "data/maps/Galar_Motostoke06/scripts.inc"
	.include "data/maps/Galar_Wedgehurst09/scripts.inc"
	.include "data/maps/Galar_Motostoke07/scripts.inc"
	.include "data/maps/Galar_Postwick38/scripts.inc"
	.include "data/maps/Galar_GalarMine04/scripts.inc"
	.include "data/maps/Galar_Route0301/scripts.inc"
	.include "data/maps/Galar_Motostoke08/scripts.inc"
	.include "data/maps/Galar_Motostoke09/scripts.inc"
	.include "data/maps/Galar_Motostoke10/scripts.inc"
	.include "data/maps/Galar_Motostoke11/scripts.inc"
	.include "data/maps/Galar_Motostoke12/scripts.inc"
	.include "data/maps/Galar_Motostoke13/scripts.inc"
	.include "data/maps/Galar_Motostoke14/scripts.inc"
	.include "data/maps/Galar_Motostoke15/scripts.inc"
	.include "data/maps/Galar_Motostoke16/scripts.inc"
	.include "data/maps/Galar_WildArea03/scripts.inc"
	.include "data/maps/Galar_GalarMine02/scripts.inc"
	.include "data/maps/Galar_WildArea04/scripts.inc"
	.include "data/maps/Galar_WildArea05/scripts.inc"
	.include "data/maps/Galar_WildArea06/scripts.inc"
	.include "data/maps/Galar_Motostoke17/scripts.inc"
	.include "data/maps/Galar_Motostoke18/scripts.inc"
	.include "data/maps/Galar_Motostoke19/scripts.inc"
	.include "data/maps/Galar_Motostoke20/scripts.inc"
	.include "data/maps/Galar_Turffield01/scripts.inc"
	.include "data/maps/Galar_Turffield02/scripts.inc"
	.include "data/maps/Galar_Postwick40/scripts.inc"
	.include "data/maps/Galar_GalarMine05/scripts.inc"
	.include "data/maps/Galar_Turffield03/scripts.inc"
	.include "data/maps/Galar_Turffield04/scripts.inc"
	.include "data/maps/Galar_Turffield05/scripts.inc"
	.include "data/maps/Galar_Turffield06/scripts.inc"
	.include "data/maps/Galar_WildArea25/scripts.inc"
	.include "data/maps/Galar_WildArea26/scripts.inc"
	.include "data/maps/Galar_Route0401/scripts.inc"
	.include "data/maps/Galar_Turffield07/scripts.inc"
	.include "data/maps/Galar_Turffield08/scripts.inc"
	.include "data/maps/Galar_Turffield09/scripts.inc"
	.include "data/maps/Galar_Turffield10/scripts.inc"
	.include "data/maps/Galar_Wedgehurst14/scripts.inc"
	.include "data/maps/Galar_Motostoke21/scripts.inc"
	.include "data/maps/Galar_Hulbury02/scripts.inc"
	.include "data/maps/Galar_Hulbury03/scripts.inc"
	.include "data/maps/Galar_Hulbury04/scripts.inc"
	.include "data/maps/Galar_Hulbury05/scripts.inc"
	.include "data/maps/Galar_Postwick45/scripts.inc"
	.include "data/maps/Galar_Route0501/scripts.inc"
	.include "data/maps/Galar_Hulbury06/scripts.inc"
	.include "data/maps/Galar_Hulbury07/scripts.inc"
	.include "data/maps/Galar_Postwick46/scripts.inc"
	.include "data/maps/Galar_Postwick47/scripts.inc"
	.include "data/maps/Galar_WildArea27/scripts.inc"
	.include "data/maps/Galar_Postwick49/scripts.inc"
	.include "data/maps/Galar_Postwick50/scripts.inc"
	.include "data/maps/Galar_Hulbury08/scripts.inc"
	.include "data/maps/Galar_Hulbury09/scripts.inc"
	.include "data/maps/Galar_Hulbury10/scripts.inc"
	.include "data/maps/Galar_WildArea28/scripts.inc"
	.include "data/maps/Galar_WildArea29/scripts.inc"
	.include "data/maps/Galar_Hulbury11/scripts.inc"
	.include "data/maps/Galar_GalarMine03/scripts.inc"
	.include "data/maps/Galar_Postwick53/scripts.inc"
	.include "data/maps/Galar_WildArea07/scripts.inc"
	.include "data/maps/Galar_WildArea08/scripts.inc"
	.include "data/maps/Galar_WildArea09/scripts.inc"
	.include "data/maps/Galar_Wedgehurst15/scripts.inc"
	.include "data/maps/Galar_Hulbury12/scripts.inc"
	.include "data/maps/Galar_StowOnSide03/scripts.inc"
	.include "data/maps/Galar_StowOnSide04/scripts.inc"
	.include "data/maps/Galar_Circhester01/scripts.inc"
	.include "data/maps/Galar_StowOnSide05/scripts.inc"
	.include "data/maps/Galar_Circhester02/scripts.inc"
	.include "data/maps/Galar_Hammerlocke03/scripts.inc"
	.include "data/maps/Galar_Hammerlocke04/scripts.inc"
	.include "data/maps/Galar_Hammerlocke05/scripts.inc"
	.include "data/maps/Galar_Hammerlocke06/scripts.inc"
	.include "data/maps/Galar_Route0701/scripts.inc"
	.include "data/maps/Galar_Hammerlocke07/scripts.inc"
	.include "data/maps/Galar_Hammerlocke08/scripts.inc"
	.include "data/maps/Galar_Hammerlocke09/scripts.inc"
	.include "data/maps/Galar_Hammerlocke10/scripts.inc"
	.include "data/maps/Galar_StowOnSide06/scripts.inc"
	.include "data/maps/Galar_StowOnSide07/scripts.inc"
	.include "data/maps/Galar_Hammerlocke11/scripts.inc"
	.include "data/maps/Galar_Hammerlocke12/scripts.inc"
	.include "data/maps/Galar_Hammerlocke13/scripts.inc"
	.include "data/maps/Galar_Hammerlocke14/scripts.inc"
	.include "data/maps/Galar_Hammerlocke15/scripts.inc"
	.include "data/maps/Galar_Hammerlocke16/scripts.inc"
	.include "data/maps/Galar_Hammerlocke17/scripts.inc"
	.include "data/maps/Galar_Hammerlocke18/scripts.inc"
	.include "data/maps/Galar_Hammerlocke19/scripts.inc"
	.include "data/maps/Galar_Route0601/scripts.inc"
	.include "data/maps/Galar_StowOnSide08/scripts.inc"
	.include "data/maps/Galar_Hulbury13/scripts.inc"
	.include "data/maps/Galar_Route1601/scripts.inc"
	.include "data/maps/Galar_Route1602/scripts.inc"
	.include "data/maps/Galar_StowOnSide09/scripts.inc"
	.include "data/maps/Galar_Route1603/scripts.inc"
	.include "data/maps/Galar_StowOnSide10/scripts.inc"
	.include "data/maps/Galar_Route1604/scripts.inc"
	.include "data/maps/Galar_SixIsland01/scripts.inc"
	.include "data/maps/Galar_Ballonlea01/scripts.inc"
	.include "data/maps/Galar_Ballonlea02/scripts.inc"
	.include "data/maps/Galar_Ballonlea03/scripts.inc"
	.include "data/maps/Galar_Ballonlea04/scripts.inc"
	.include "data/maps/Galar_Ballonlea05/scripts.inc"
	.include "data/maps/Galar_Ballonlea06/scripts.inc"
	.include "data/maps/Galar_Ballonlea07/scripts.inc"
	.include "data/maps/Galar_Ballonlea08/scripts.inc"
	.include "data/maps/Galar_Circhester03/scripts.inc"
	.include "data/maps/Galar_Circhester04/scripts.inc"
	.include "data/maps/Galar_Circhester05/scripts.inc"
	.include "data/maps/Galar_Route0801/scripts.inc"
	.include "data/maps/Galar_Route0802/scripts.inc"
	.include "data/maps/Galar_Circhester06/scripts.inc"
	.include "data/maps/Galar_Circhester07/scripts.inc"
	.include "data/maps/Galar_Circhester08/scripts.inc"
	.include "data/maps/Galar_Circhester09/scripts.inc"
	.include "data/maps/Galar_Circhester10/scripts.inc"
	.include "data/maps/Galar_Circhester11/scripts.inc"
	.include "data/maps/Galar_Circhester12/scripts.inc"
	.include "data/maps/Galar_Circhester13/scripts.inc"
	.include "data/maps/Galar_Circhester14/scripts.inc"
	.include "data/maps/Galar_Wyndon02/scripts.inc"
	.include "data/maps/Galar_Spikemuth01/scripts.inc"
	.include "data/maps/Galar_Spikemuth02/scripts.inc"
	.include "data/maps/Galar_Spikemuth03/scripts.inc"
	.include "data/maps/Galar_Spikemuth04/scripts.inc"
	.include "data/maps/Galar_Route1002/scripts.inc"
	.include "data/maps/Galar_Wyndon03/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor01/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor02/scripts.inc"
	.include "data/maps/Galar_Wyndon08/scripts.inc"
	.include "data/maps/Galar_Postwick58/scripts.inc"
	.include "data/maps/Galar_Circhester17/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor03/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor04/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor05/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor06/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor07/scripts.inc"
	.include "data/maps/Galar_Hammerlocke20/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor08/scripts.inc"
	.include "data/maps/Galar_Wyndon09/scripts.inc"
	.include "data/maps/Galar_Wyndon04/scripts.inc"
	.include "data/maps/Galar_Wyndon05/scripts.inc"
	.include "data/maps/Galar_Spikemuth05/scripts.inc"
	.include "data/maps/Galar_Spikemuth06/scripts.inc"
	.include "data/maps/Galar_Spikemuth07/scripts.inc"
	.include "data/maps/Galar_Route0901/scripts.inc"
	.include "data/maps/Galar_Circhester18/scripts.inc"
	.include "data/maps/Galar_Route0803/scripts.inc"
	.include "data/maps/Galar_StowOnSide11/scripts.inc"
	.include "data/maps/Galar_Wedgehurst10/scripts.inc"
	.include "data/maps/Galar_NewmoonIsland02/scripts.inc"
	.include "data/maps/Galar_DynamaxAdventure03/scripts.inc"
	.include "data/maps/Galar_Hammerlocke21/scripts.inc"
	.include "data/maps/Galar_DynamaxAdventure04/scripts.inc"
	.include "data/maps/Galar_Wyndon06/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor04/scripts.inc"
	.include "data/maps/Galar_DynamaxAdventure01/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor09/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor10/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor11/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor12/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor13/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor14/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor15/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor16/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor17/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor18/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor19/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor20/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor21/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor22/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor23/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor24/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor25/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor26/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor27/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor28/scripts.inc"
	.include "data/maps/Galar_CrownTundra20/scripts.inc"
	.include "data/maps/Galar_CrownTundra06/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor29/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor30/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor31/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor32/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor33/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor34/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor35/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor36/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor37/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor38/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor39/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor40/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor41/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor42/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor43/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor44/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor45/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor46/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor47/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor48/scripts.inc"
	.include "data/maps/Galar_CrownTundra07/scripts.inc"
	.include "data/maps/Galar_CrownTundra08/scripts.inc"
	.include "data/maps/Galar_CrownTundra09/scripts.inc"
	.include "data/maps/Galar_CrownTundra10/scripts.inc"
	.include "data/maps/Galar_CrownTundra11/scripts.inc"
	.include "data/maps/Galar_CrownTundra12/scripts.inc"
	.include "data/maps/Galar_CrownTundra13/scripts.inc"
	.include "data/maps/Galar_ScufibChamber01/scripts.inc"
	.include "data/maps/Galar_CrownTundra14/scripts.inc"
	.include "data/maps/Galar_CrownTundra15/scripts.inc"
	.include "data/maps/Galar_CrownTundra16/scripts.inc"
	.include "data/maps/Galar_TanobyKey01/scripts.inc"
	.include "data/maps/Galar_LiptooChamber01/scripts.inc"
	.include "data/maps/Galar_Postwick111/scripts.inc"
	.include "data/maps/Galar_Postwick112/scripts.inc"
	.include "data/maps/Galar_Postwick113/scripts.inc"
	.include "data/maps/Galar_CrownTundra17/scripts.inc"
	.include "data/maps/Galar_CrownTundra18/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor05/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor06/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor07/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor08/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor09/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor10/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor11/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor12/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor13/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor14/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor15/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor16/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor17/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor18/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor19/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor20/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor21/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor22/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor23/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor24/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor25/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor26/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor27/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor28/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor29/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor30/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor31/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor32/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor33/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor34/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor38/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor39/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor40/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor41/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor42/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor43/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor44/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor45/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor46/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor47/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor48/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor49/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor35/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor36/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor49/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor50/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor51/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor52/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor53/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor54/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor55/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor56/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor57/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor58/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor59/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor60/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor61/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor62/scripts.inc"
	.include "data/maps/Galar_TurffieldIndoor63/scripts.inc"
	.include "data/maps/Galar_WildAreaIndoor01/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor01/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor02/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor03/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor04/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor05/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor06/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor07/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor08/scripts.inc"
	.include "data/maps/Galar_WildAreaIndoor02/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor09/scripts.inc"
	.include "data/maps/Galar_Wyndon10/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor10/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor11/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor12/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor13/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor14/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor15/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor16/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor17/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor18/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor19/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor20/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor21/scripts.inc"
	.include "data/maps/Galar_WyndonIndoor22/scripts.inc"
	.include "data/maps/Galar_Postwick166/scripts.inc"
	.include "data/maps/Galar_Hulbury14/scripts.inc"
	.include "data/maps/Galar_StowOnSide12/scripts.inc"
	.include "data/maps/Galar_Motostoke22/scripts.inc"
	.include "data/maps/Galar_Hammerlocke22/scripts.inc"
	.include "data/maps/Galar_Wedgehurst16/scripts.inc"
	.include "data/maps/Galar_Ballonlea09/scripts.inc"
	.include "data/maps/Galar_Circhester15/scripts.inc"
	.include "data/maps/Galar_Wedgehurst11/scripts.inc"
	.include "data/maps/Galar_Wedgehurst17/scripts.inc"
	.include "data/maps/Galar_Spikemuth08/scripts.inc"
	.include "data/maps/Galar_Hulbury15/scripts.inc"
	.include "data/maps/Galar_Wyndon07/scripts.inc"
	.include "data/maps/Galar_Postwick169/scripts.inc"
	.include "data/maps/Galar_IsleOfArmor37/scripts.inc"
	.include "data/maps/Galar_CrownTundra19/scripts.inc"
	.include "data/maps/Galar_Turffield11/scripts.inc"
	.include "data/maps/Galar_WildAreaCave01/scripts.inc"
	.include "data/maps/Galar_WildArea10/scripts.inc"
	.include "data/maps/Galar_Hammerlocke24/scripts.inc"
	.include "data/maps/Galar_WildArea11/scripts.inc"
	.include "data/maps/Galar_WildArea12/scripts.inc"
	.include "data/maps/Galar_WildArea13/scripts.inc"
	.include "data/maps/Galar_WildArea14/scripts.inc"
	.include "data/maps/Galar_WildArea15/scripts.inc"
	.include "data/maps/Galar_WildArea16/scripts.inc"
	.include "data/maps/Galar_WildArea17/scripts.inc"
	.include "data/maps/Galar_WildArea18/scripts.inc"
	.include "data/maps/Galar_WildArea19/scripts.inc"
	.include "data/maps/Galar_WildArea20/scripts.inc"
	.include "data/maps/Galar_WildArea21/scripts.inc"
	.include "data/maps/Galar_WildArea22/scripts.inc"
	.include "data/maps/Galar_Postwick172/scripts.inc"
	.include "data/scripts/galar_fala.inc"
	.include "data/scripts/galar_cenas.inc"
	.include "data/scripts/galar_objetos.inc"
	.include "data/scripts/galar_estaticos.inc"
	.include "data/scripts/galar_treinadores.inc"
	.include "data/scripts/galar_placas.inc"
	.include "data/scripts/galar_placas_c.inc"
	.include "data/scripts/galar_portas_fechadas.inc"
	.include "data/scripts/galar_portas_script.inc"
	.include "data/scripts/galar_objetos_i.inc"
