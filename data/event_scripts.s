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
	.include "data/maps/OldaleTown/scripts.inc"
	.include "data/maps/DewfordTown/scripts.inc"
	.include "data/maps/LavaridgeTown/scripts.inc"
	.include "data/maps/FallarborTown/scripts.inc"
	.include "data/maps/VerdanturfTown/scripts.inc"
	.include "data/maps/PacifidlogTown/scripts.inc"
	.include "data/maps/Route101/scripts.inc"
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
	.include "data/maps/Underwater_Route124/scripts.inc"
	.include "data/maps/Underwater_Route126/scripts.inc"
	.include "data/maps/Underwater_Route127/scripts.inc"
	.include "data/maps/Underwater_Route128/scripts.inc"
	.include "data/maps/Underwater_Route129/scripts.inc"
	.include "data/maps/Underwater_Route105/scripts.inc"
	.include "data/maps/Underwater_Route125/scripts.inc"
	.include "data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc"
	.include "data/maps/LittlerootTown_BrendansHouse_2F/scripts.inc"
	.include "data/maps/LittlerootTown_MaysHouse_1F/scripts.inc"
	.include "data/maps/LittlerootTown_MaysHouse_2F/scripts.inc"
	.include "data/maps/LittlerootTown_ProfessorBirchsLab/scripts.inc"
	.include "data/maps/OldaleTown_House1/scripts.inc"
	.include "data/maps/OldaleTown_House2/scripts.inc"
	.include "data/maps/OldaleTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/OldaleTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/OldaleTown_Mart/scripts.inc"
	.include "data/maps/DewfordTown_House1/scripts.inc"
	.include "data/maps/DewfordTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/DewfordTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/DewfordTown_Gym/scripts.inc"
	.include "data/maps/DewfordTown_Hall/scripts.inc"
	.include "data/maps/DewfordTown_House2/scripts.inc"
	.include "data/maps/LavaridgeTown_HerbShop/scripts.inc"
	.include "data/maps/LavaridgeTown_Gym_1F/scripts.inc"
	.include "data/maps/LavaridgeTown_Gym_B1F/scripts.inc"
	.include "data/maps/LavaridgeTown_House/scripts.inc"
	.include "data/maps/LavaridgeTown_Mart/scripts.inc"
	.include "data/maps/LavaridgeTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/LavaridgeTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/FallarborTown_Mart/scripts.inc"
	.include "data/maps/FallarborTown_BattleTentLobby/scripts.inc"
	.include "data/maps/FallarborTown_BattleTentCorridor/scripts.inc"
	.include "data/maps/FallarborTown_BattleTentBattleRoom/scripts.inc"
	.include "data/maps/FallarborTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/FallarborTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/FallarborTown_CozmosHouse/scripts.inc"
	.include "data/maps/FallarborTown_MoveRelearnersHouse/scripts.inc"
	.include "data/maps/VerdanturfTown_BattleTentLobby/scripts.inc"
	.include "data/maps/VerdanturfTown_BattleTentCorridor/scripts.inc"
	.include "data/maps/VerdanturfTown_BattleTentBattleRoom/scripts.inc"
	.include "data/maps/VerdanturfTown_Mart/scripts.inc"
	.include "data/maps/VerdanturfTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/VerdanturfTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/VerdanturfTown_WandasHouse/scripts.inc"
	.include "data/maps/VerdanturfTown_FriendshipRatersHouse/scripts.inc"
	.include "data/maps/VerdanturfTown_House/scripts.inc"
	.include "data/maps/PacifidlogTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/PacifidlogTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/PacifidlogTown_House1/scripts.inc"
	.include "data/maps/PacifidlogTown_House2/scripts.inc"
	.include "data/maps/PacifidlogTown_House3/scripts.inc"
	.include "data/maps/PacifidlogTown_House4/scripts.inc"
	.include "data/maps/PacifidlogTown_House5/scripts.inc"
	.include "data/maps/PetalburgCity_WallysHouse/scripts.inc"
	.include "data/maps/PetalburgCity_Gym/scripts.inc"
	.include "data/maps/PetalburgCity_House1/scripts.inc"
	.include "data/maps/PetalburgCity_House2/scripts.inc"
	.include "data/maps/PetalburgCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/PetalburgCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/PetalburgCity_Mart/scripts.inc"
	.include "data/maps/SlateportCity_SternsShipyard_1F/scripts.inc"
	.include "data/maps/SlateportCity_SternsShipyard_2F/scripts.inc"
	.include "data/maps/SlateportCity_BattleTentLobby/scripts.inc"
	.include "data/maps/SlateportCity_BattleTentCorridor/scripts.inc"
	.include "data/maps/SlateportCity_BattleTentBattleRoom/scripts.inc"
	.include "data/maps/SlateportCity_NameRatersHouse/scripts.inc"
	.include "data/maps/SlateportCity_PokemonFanClub/scripts.inc"
	.include "data/maps/SlateportCity_OceanicMuseum_1F/scripts.inc"
	.include "data/maps/SlateportCity_OceanicMuseum_2F/scripts.inc"
	.include "data/maps/SlateportCity_Harbor/scripts.inc"
	.include "data/maps/SlateportCity_House/scripts.inc"
	.include "data/maps/SlateportCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/SlateportCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/SlateportCity_Mart/scripts.inc"
	.include "data/maps/MauvilleCity_Gym/scripts.inc"
	.include "data/maps/MauvilleCity_BikeShop/scripts.inc"
	.include "data/maps/MauvilleCity_House1/scripts.inc"
	.include "data/maps/MauvilleCity_GameCorner/scripts.inc"
	.include "data/maps/MauvilleCity_House2/scripts.inc"
	.include "data/maps/MauvilleCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/MauvilleCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/MauvilleCity_Mart/scripts.inc"
	.include "data/maps/RustboroCity_DevonCorp_1F/scripts.inc"
	.include "data/maps/RustboroCity_DevonCorp_2F/scripts.inc"
	.include "data/maps/RustboroCity_DevonCorp_3F/scripts.inc"
	.include "data/maps/RustboroCity_Gym/scripts.inc"
	.include "data/maps/RustboroCity_PokemonSchool/scripts.inc"
	.include "data/maps/RustboroCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/RustboroCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/RustboroCity_Mart/scripts.inc"
	.include "data/maps/RustboroCity_Flat1_1F/scripts.inc"
	.include "data/maps/RustboroCity_Flat1_2F/scripts.inc"
	.include "data/maps/RustboroCity_House1/scripts.inc"
	.include "data/maps/RustboroCity_CuttersHouse/scripts.inc"
	.include "data/maps/RustboroCity_House2/scripts.inc"
	.include "data/maps/RustboroCity_Flat2_1F/scripts.inc"
	.include "data/maps/RustboroCity_Flat2_2F/scripts.inc"
	.include "data/maps/RustboroCity_Flat2_3F/scripts.inc"
	.include "data/maps/RustboroCity_House3/scripts.inc"
	.include "data/maps/FortreeCity_House1/scripts.inc"
	.include "data/maps/FortreeCity_Gym/scripts.inc"
	.include "data/maps/FortreeCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/FortreeCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/FortreeCity_Mart/scripts.inc"
	.include "data/maps/FortreeCity_House2/scripts.inc"
	.include "data/maps/FortreeCity_House3/scripts.inc"
	.include "data/maps/FortreeCity_House4/scripts.inc"
	.include "data/maps/FortreeCity_House5/scripts.inc"
	.include "data/maps/FortreeCity_DecorationShop/scripts.inc"
	.include "data/maps/LilycoveCity_CoveLilyMotel_1F/scripts.inc"
	.include "data/maps/LilycoveCity_CoveLilyMotel_2F/scripts.inc"
	.include "data/maps/LilycoveCity_LilycoveMuseum_1F/scripts.inc"
	.include "data/maps/LilycoveCity_LilycoveMuseum_2F/scripts.inc"
	.include "data/maps/LilycoveCity_ContestLobby/scripts.inc"
	.include "data/maps/LilycoveCity_ContestHall/scripts.inc"
	.include "data/maps/LilycoveCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/LilycoveCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/LilycoveCity_UnusedMart/scripts.inc"
	.include "data/maps/LilycoveCity_PokemonTrainerFanClub/scripts.inc"
	.include "data/maps/LilycoveCity_Harbor/scripts.inc"
	.include "data/maps/LilycoveCity_MoveDeletersHouse/scripts.inc"
	.include "data/maps/LilycoveCity_House1/scripts.inc"
	.include "data/maps/LilycoveCity_House2/scripts.inc"
	.include "data/maps/LilycoveCity_House3/scripts.inc"
	.include "data/maps/LilycoveCity_House4/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_1F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_2F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_3F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_4F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStore_5F/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStoreRooftop/scripts.inc"
	.include "data/maps/LilycoveCity_DepartmentStoreElevator/scripts.inc"
	.include "data/maps/MossdeepCity_Gym/scripts.inc"
	.include "data/maps/MossdeepCity_House1/scripts.inc"
	.include "data/maps/MossdeepCity_House2/scripts.inc"
	.include "data/maps/MossdeepCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/MossdeepCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/MossdeepCity_Mart/scripts.inc"
	.include "data/maps/MossdeepCity_House3/scripts.inc"
	.include "data/maps/MossdeepCity_StevensHouse/scripts.inc"
	.include "data/maps/MossdeepCity_House4/scripts.inc"
	.include "data/maps/MossdeepCity_SpaceCenter_1F/scripts.inc"
	.include "data/maps/MossdeepCity_SpaceCenter_2F/scripts.inc"
	.include "data/maps/MossdeepCity_GameCorner_1F/scripts.inc"
	.include "data/maps/MossdeepCity_GameCorner_B1F/scripts.inc"
	.include "data/maps/SootopolisCity_Gym_1F/scripts.inc"
	.include "data/maps/SootopolisCity_Gym_B1F/scripts.inc"
	.include "data/maps/SootopolisCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/SootopolisCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/SootopolisCity_Mart/scripts.inc"
	.include "data/maps/SootopolisCity_House1/scripts.inc"
	.include "data/maps/SootopolisCity_House2/scripts.inc"
	.include "data/maps/SootopolisCity_House3/scripts.inc"
	.include "data/maps/SootopolisCity_House4/scripts.inc"
	.include "data/maps/SootopolisCity_House5/scripts.inc"
	.include "data/maps/SootopolisCity_House6/scripts.inc"
	.include "data/maps/SootopolisCity_House7/scripts.inc"
	.include "data/maps/SootopolisCity_LotadAndSeedotHouse/scripts.inc"
	.include "data/maps/SootopolisCity_MysteryEventsHouse_1F/scripts.inc"
	.include "data/maps/SootopolisCity_MysteryEventsHouse_B1F/scripts.inc"
	.include "data/maps/EverGrandeCity_SidneysRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_PhoebesRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_GlaciasRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_DrakesRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_ChampionsRoom/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall1/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall2/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall3/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall4/scripts.inc"
	.include "data/maps/EverGrandeCity_Hall5/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonLeague_1F/scripts.inc"
	.include "data/maps/EverGrandeCity_HallOfFame/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/EverGrandeCity_PokemonLeague_2F/scripts.inc"
	.include "data/maps/Route104_MrBrineysHouse/scripts.inc"
	.include "data/maps/Route104_PrettyPetalFlowerShop/scripts.inc"
	.include "data/maps/Route111_WinstrateFamilysHouse/scripts.inc"
	.include "data/maps/Route111_OldLadysRestStop/scripts.inc"
	.include "data/maps/Route112_CableCarStation/scripts.inc"
	.include "data/maps/MtChimney_CableCarStation/scripts.inc"
	.include "data/maps/Route114_FossilManiacsHouse/scripts.inc"
	.include "data/maps/Route114_FossilManiacsTunnel/scripts.inc"
	.include "data/maps/Route114_LanettesHouse/scripts.inc"
	.include "data/maps/Route116_TunnelersRestHouse/scripts.inc"
	.include "data/maps/Route117_PokemonDayCare/scripts.inc"
	.include "data/maps/Route121_SafariZoneEntrance/scripts.inc"
	.include "data/maps/MeteorFalls_1F_1R/scripts.inc"
	.include "data/maps/MeteorFalls_1F_2R/scripts.inc"
	.include "data/maps/MeteorFalls_B1F_1R/scripts.inc"
	.include "data/maps/MeteorFalls_B1F_2R/scripts.inc"
	.include "data/maps/RusturfTunnel/scripts.inc"
	.include "data/maps/Underwater_SootopolisCity/scripts.inc"
	.include "data/maps/DesertRuins/scripts.inc"
	.include "data/maps/GraniteCave_1F/scripts.inc"
	.include "data/maps/GraniteCave_B1F/scripts.inc"
	.include "data/maps/GraniteCave_B2F/scripts.inc"
	.include "data/maps/GraniteCave_StevensRoom/scripts.inc"
	.include "data/maps/PetalburgWoods/scripts.inc"
	.include "data/maps/MtChimney/scripts.inc"
	.include "data/maps/JaggedPass/scripts.inc"
	.include "data/maps/FieryPath/scripts.inc"
	.include "data/maps/MtPyre_1F/scripts.inc"
	.include "data/maps/MtPyre_2F/scripts.inc"
	.include "data/maps/MtPyre_3F/scripts.inc"
	.include "data/maps/MtPyre_4F/scripts.inc"
	.include "data/maps/MtPyre_5F/scripts.inc"
	.include "data/maps/MtPyre_6F/scripts.inc"
	.include "data/maps/MtPyre_Exterior/scripts.inc"
	.include "data/maps/MtPyre_Summit/scripts.inc"
	.include "data/maps/AquaHideout_1F/scripts.inc"
	.include "data/maps/AquaHideout_B1F/scripts.inc"
	.include "data/maps/AquaHideout_B2F/scripts.inc"
	.include "data/maps/Underwater_SeafloorCavern/scripts.inc"
	.include "data/maps/SeafloorCavern_Entrance/scripts.inc"
	.include "data/maps/SeafloorCavern_Room1/scripts.inc"
	.include "data/maps/SeafloorCavern_Room2/scripts.inc"
	.include "data/maps/SeafloorCavern_Room3/scripts.inc"
	.include "data/maps/SeafloorCavern_Room4/scripts.inc"
	.include "data/maps/SeafloorCavern_Room5/scripts.inc"
	.include "data/maps/SeafloorCavern_Room6/scripts.inc"
	.include "data/maps/SeafloorCavern_Room7/scripts.inc"
	.include "data/maps/SeafloorCavern_Room8/scripts.inc"
	.include "data/maps/SeafloorCavern_Room9/scripts.inc"
	.include "data/maps/CaveOfOrigin_Entrance/scripts.inc"
	.include "data/maps/CaveOfOrigin_1F/scripts.inc"
	.include "data/maps/CaveOfOrigin_UnusedRubySapphireMap1/scripts.inc"
	.include "data/maps/CaveOfOrigin_UnusedRubySapphireMap2/scripts.inc"
	.include "data/maps/CaveOfOrigin_UnusedRubySapphireMap3/scripts.inc"
	.include "data/maps/CaveOfOrigin_B1F/scripts.inc"
	.include "data/maps/VictoryRoad_1F/scripts.inc"
	.include "data/maps/VictoryRoad_B1F/scripts.inc"
	.include "data/maps/VictoryRoad_B2F/scripts.inc"
	.include "data/maps/ShoalCave_LowTideEntranceRoom/scripts.inc"
	.include "data/maps/ShoalCave_LowTideInnerRoom/scripts.inc"
	.include "data/maps/ShoalCave_LowTideStairsRoom/scripts.inc"
	.include "data/maps/ShoalCave_LowTideLowerRoom/scripts.inc"
	.include "data/maps/ShoalCave_HighTideEntranceRoom/scripts.inc"
	.include "data/maps/ShoalCave_HighTideInnerRoom/scripts.inc"
	.include "data/maps/NewMauville_Entrance/scripts.inc"
	.include "data/maps/NewMauville_Inside/scripts.inc"
	.include "data/maps/AbandonedShip_Deck/scripts.inc"
	.include "data/maps/AbandonedShip_Corridors_1F/scripts.inc"
	.include "data/maps/AbandonedShip_Rooms_1F/scripts.inc"
	.include "data/maps/AbandonedShip_Corridors_B1F/scripts.inc"
	.include "data/maps/AbandonedShip_Rooms_B1F/scripts.inc"
	.include "data/maps/AbandonedShip_Rooms2_B1F/scripts.inc"
	.include "data/maps/AbandonedShip_Underwater1/scripts.inc"
	.include "data/maps/AbandonedShip_Room_B1F/scripts.inc"
	.include "data/maps/AbandonedShip_Rooms2_1F/scripts.inc"
	.include "data/maps/AbandonedShip_CaptainsOffice/scripts.inc"
	.include "data/maps/AbandonedShip_Underwater2/scripts.inc"
	.include "data/maps/AbandonedShip_HiddenFloorCorridors/scripts.inc"
	.include "data/maps/AbandonedShip_HiddenFloorRooms/scripts.inc"
	.include "data/maps/IslandCave/scripts.inc"
	.include "data/maps/AncientTomb/scripts.inc"
	.include "data/maps/Underwater_Route134/scripts.inc"
	.include "data/maps/Underwater_SealedChamber/scripts.inc"
	.include "data/maps/SealedChamber_OuterRoom/scripts.inc"
	.include "data/maps/SealedChamber_InnerRoom/scripts.inc"
	.include "data/maps/ScorchedSlab/scripts.inc"
	.include "data/maps/AquaHideout_UnusedRubyMap1/scripts.inc"
	.include "data/maps/AquaHideout_UnusedRubyMap2/scripts.inc"
	.include "data/maps/AquaHideout_UnusedRubyMap3/scripts.inc"
	.include "data/maps/SkyPillar_Entrance/scripts.inc"
	.include "data/maps/SkyPillar_Outside/scripts.inc"
	.include "data/maps/SkyPillar_1F/scripts.inc"
	.include "data/maps/SkyPillar_2F/scripts.inc"
	.include "data/maps/SkyPillar_3F/scripts.inc"
	.include "data/maps/SkyPillar_4F/scripts.inc"
	.include "data/maps/ShoalCave_LowTideIceRoom/scripts.inc"
	.include "data/maps/SkyPillar_5F/scripts.inc"
	.include "data/maps/SkyPillar_Top/scripts.inc"
	.include "data/maps/MagmaHideout_1F/scripts.inc"
	.include "data/maps/MagmaHideout_2F_1R/scripts.inc"
	.include "data/maps/MagmaHideout_2F_2R/scripts.inc"
	.include "data/maps/MagmaHideout_3F_1R/scripts.inc"
	.include "data/maps/MagmaHideout_3F_2R/scripts.inc"
	.include "data/maps/MagmaHideout_4F/scripts.inc"
	.include "data/maps/MagmaHideout_3F_3R/scripts.inc"
	.include "data/maps/MagmaHideout_2F_3R/scripts.inc"
	.include "data/maps/MirageTower_1F/scripts.inc"
	.include "data/maps/MirageTower_2F/scripts.inc"
	.include "data/maps/MirageTower_3F/scripts.inc"
	.include "data/maps/MirageTower_4F/scripts.inc"
	.include "data/maps/DesertUnderpass/scripts.inc"
	.include "data/maps/ArtisanCave_B1F/scripts.inc"
	.include "data/maps/ArtisanCave_1F/scripts.inc"
	.include "data/maps/Underwater_MarineCave/scripts.inc"
	.include "data/maps/MarineCave_Entrance/scripts.inc"
	.include "data/maps/MarineCave_End/scripts.inc"
	.include "data/maps/TerraCave_Entrance/scripts.inc"
	.include "data/maps/TerraCave_End/scripts.inc"
	.include "data/maps/AlteringCave/scripts.inc"
	.include "data/maps/MeteorFalls_StevensCave/scripts.inc"
	.include "data/scripts/shared_secret_base.inc"
	.include "data/scripts/sinnoh_placas.inc"
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
	.include "data/maps/BattleFrontier_BattleTowerCorridor/scripts.inc"
	.include "data/maps/BattleFrontier_BattleTowerBattleRoom/scripts.inc"
	.include "data/maps/SouthernIsland_Exterior/scripts.inc"
	.include "data/maps/SouthernIsland_Interior/scripts.inc"
	.include "data/maps/SafariZone_RestHouse/scripts.inc"
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
	.include "data/maps/BattleFrontier_RankingHall/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge1/scripts.inc"
	.include "data/maps/BattleFrontier_ExchangeServiceCorner/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge2/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge3/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge4/scripts.inc"
	.include "data/maps/BattleFrontier_ScottsHouse/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge5/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge6/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge7/scripts.inc"
	.include "data/maps/BattleFrontier_ReceptionGate/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge8/scripts.inc"
	.include "data/maps/BattleFrontier_Lounge9/scripts.inc"
	.include "data/maps/BattleFrontier_PokemonCenter_1F/scripts.inc"
	.include "data/maps/BattleFrontier_PokemonCenter_2F/scripts.inc"
	.include "data/maps/BattleFrontier_Mart/scripts.inc"
	.include "data/maps/FarawayIsland_Entrance/scripts.inc"
	.include "data/maps/FarawayIsland_Interior/scripts.inc"
	.include "data/maps/BirthIsland_Exterior/scripts.inc"
	.include "data/maps/BirthIsland_Harbor/scripts.inc"
	.include "data/maps/TrainerHill_Entrance/scripts.inc"
	.include "data/maps/TrainerHill_1F/scripts.inc"
	.include "data/maps/TrainerHill_2F/scripts.inc"
	.include "data/maps/TrainerHill_3F/scripts.inc"
	.include "data/maps/TrainerHill_4F/scripts.inc"
	.include "data/maps/TrainerHill_Roof/scripts.inc"
	.include "data/maps/NavelRock_Exterior/scripts.inc"
	.include "data/maps/NavelRock_Harbor/scripts.inc"
	.include "data/maps/NavelRock_Entrance/scripts.inc"
	.include "data/maps/NavelRock_B1F/scripts.inc"
	.include "data/maps/NavelRock_Fork/scripts.inc"
	.include "data/maps/NavelRock_Up1/scripts.inc"
	.include "data/maps/NavelRock_Up2/scripts.inc"
	.include "data/maps/NavelRock_Up3/scripts.inc"
	.include "data/maps/NavelRock_Up4/scripts.inc"
	.include "data/maps/NavelRock_Top/scripts.inc"
	.include "data/maps/NavelRock_Down01/scripts.inc"
	.include "data/maps/NavelRock_Down02/scripts.inc"
	.include "data/maps/NavelRock_Down03/scripts.inc"
	.include "data/maps/NavelRock_Down04/scripts.inc"
	.include "data/maps/NavelRock_Down05/scripts.inc"
	.include "data/maps/NavelRock_Down06/scripts.inc"
	.include "data/maps/NavelRock_Down07/scripts.inc"
	.include "data/maps/NavelRock_Down08/scripts.inc"
	.include "data/maps/NavelRock_Down09/scripts.inc"
	.include "data/maps/NavelRock_Down10/scripts.inc"
	.include "data/maps/NavelRock_Down11/scripts.inc"
	.include "data/maps/NavelRock_Bottom/scripts.inc"
	.include "data/maps/TrainerHill_Elevator/scripts.inc"
	.include "data/maps/Route104_Prototype/scripts.inc"
	.include "data/maps/Route104_PrototypePrettyPetalFlowerShop/scripts.inc"
	.include "data/maps/Route109_SeashoreHouse/scripts.inc"
	.include "data/maps/Route110_TrickHouseEntrance/scripts.inc"
	.include "data/maps/Route110_TrickHouseEnd/scripts.inc"
	.include "data/maps/Route110_TrickHouseCorridor/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle1/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle2/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle3/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle4/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle5/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle6/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle7/scripts.inc"
	.include "data/maps/Route110_TrickHousePuzzle8/scripts.inc"
	.include "data/maps/Route110_SeasideCyclingRoadSouthEntrance/scripts.inc"
	.include "data/maps/Route110_SeasideCyclingRoadNorthEntrance/scripts.inc"
	.include "data/maps/Route113_GlassWorkshop/scripts.inc"
	.include "data/maps/Route123_BerryMastersHouse/scripts.inc"
	.include "data/maps/Route119_WeatherInstitute_1F/scripts.inc"
	.include "data/maps/Route119_WeatherInstitute_2F/scripts.inc"
	.include "data/maps/Route119_House/scripts.inc"
	.include "data/maps/Route124_DivingTreasureHuntersHouse/scripts.inc"


	@ Mapas de Sinnoh
	.include "data/maps/AcuityLakefront/scripts.inc"
	.include "data/maps/CanalaveCity/scripts.inc"
	.include "data/maps/CelesticTown/scripts.inc"
	.include "data/maps/EternaCity/scripts.inc"
	.include "data/maps/EternaForest/scripts.inc"
	.include "data/maps/FightArea/scripts.inc"
	.include "data/maps/FloaromaTown/scripts.inc"
	.include "data/maps/FloaromaTown_FlowerShop/scripts.inc"
	.include "data/maps/FloaromaTown_House1/scripts.inc"
	.include "data/maps/FloaromaTown_House2/scripts.inc"
	.include "data/maps/FloaromaTown_Mart/scripts.inc"
	.include "data/maps/FloaromaTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/FloaromaTwon_PokemonCenter_2F/scripts.inc"
	.include "data/maps/HearthomeCity/scripts.inc"
	.include "data/maps/HotelGrandLake/scripts.inc"
	.include "data/maps/JubilifeCity/scripts.inc"
	.include "data/maps/JubilifeCity_Flat1_F1/scripts.inc"
	.include "data/maps/JubilifeCity_Flat1_F2/scripts.inc"
	.include "data/maps/JubilifeCity_Flat1_F3/scripts.inc"
	.include "data/maps/JubilifeCity_Flat2_F1/scripts.inc"
	.include "data/maps/JubilifeCity_Flat2_F2/scripts.inc"
	.include "data/maps/JubilifeCity_Flat2_F3/scripts.inc"
	.include "data/maps/JubilifeCity_Flat3_F1/scripts.inc"
	.include "data/maps/JubilifeCity_Flat3_F2/scripts.inc"
	.include "data/maps/JubilifeCity_Flat3_F3/scripts.inc"
	.include "data/maps/JubilifeCity_JubilifeTV_F1/scripts.inc"
	.include "data/maps/JubilifeCity_JubilifeTV_F2/scripts.inc"
	.include "data/maps/JubilifeCity_JubilifeTV_F3/scripts.inc"
	.include "data/maps/JubilifeCity_JubilifeTV_F4/scripts.inc"
	.include "data/maps/JubilifeCity_Mart/scripts.inc"
	.include "data/maps/JubilifeCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/JubilifeCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/JubilifeCity_PokemonSchool/scripts.inc"
	.include "data/maps/JubilifeCity_PoketchCompany_F1/scripts.inc"
	.include "data/maps/JubilifeCity_PoketchCompany_F2/scripts.inc"
	.include "data/maps/JubilifeCity_PoketchCompany_F3/scripts.inc"
	.include "data/maps/LakeAcuity/scripts.inc"
	.include "data/maps/LakeValor/scripts.inc"
	.include "data/maps/LakeVerity/scripts.inc"
	.include "data/maps/MtCoronet_1F_North_Room1/scripts.inc"
	.include "data/maps/MtCoronet_1F_North_Room2/scripts.inc"
	.include "data/maps/MtCoronet_1F_South/scripts.inc"
	.include "data/maps/MtCoronet_B1F/scripts.inc"
	.include "data/maps/OreburghCity/scripts.inc"
	.include "data/maps/OreburghCity_Flat1_F1/scripts.inc"
	.include "data/maps/OreburghCity_Flat1_F2/scripts.inc"
	.include "data/maps/OreburghCity_Flat2_F1/scripts.inc"
	.include "data/maps/OreburghCity_Flat2_F2/scripts.inc"
	.include "data/maps/OreburghCity_Flat3_F1/scripts.inc"
	.include "data/maps/OreburghCity_Flat3_F2/scripts.inc"
	.include "data/maps/OreburghCity_Gym/scripts.inc"
	.include "data/maps/OreburghCity_House1/scripts.inc"
	.include "data/maps/OreburghCity_House2/scripts.inc"
	.include "data/maps/OreburghCity_House3/scripts.inc"
	.include "data/maps/OreburghCity_Mart/scripts.inc"
	.include "data/maps/OreburghCity_PokemonCenter_1F/scripts.inc"
	.include "data/maps/OreburghCity_PokemonCenter_2F/scripts.inc"
	.include "data/maps/OreburghGate_1F/scripts.inc"
	.include "data/maps/OreburghMine_B1F/scripts.inc"
	.include "data/maps/OreburghMine_B2F/scripts.inc"
	.include "data/maps/PastoriaCity/scripts.inc"
	.include "data/maps/PokmonLeague/scripts.inc"
	.include "data/maps/SinnohLeague_Entrance/scripts.inc"
	.include "data/maps/SinnohLeague_AaronsRoom/scripts.inc"
	.include "data/maps/SinnohLeague_BerthasRoom/scripts.inc"
	.include "data/maps/SinnohLeague_FlintsRoom/scripts.inc"
	.include "data/maps/SinnohLeague_LuciansRoom/scripts.inc"
	.include "data/maps/SinnohLeague_ChampionsRoom/scripts.inc"
	.include "data/maps/SinnohLeague_HallOfFame/scripts.inc"
	.include "data/maps/GalacticHQ_1F/scripts.inc"
	.include "data/maps/GalacticHQ_2F/scripts.inc"
	.include "data/maps/GalacticHQ_3F/scripts.inc"
	.include "data/maps/GalacticHQ_B1F/scripts.inc"
	.include "data/maps/GalacticHQ_B2F/scripts.inc"
	.include "data/maps/GalacticHQ_Hall/scripts.inc"
	.include "data/maps/GalacticHQ_Laboratory/scripts.inc"
	.include "data/maps/GalacticHQ_ControlRoom/scripts.inc"
	.include "data/maps/VeilstoneCity_GalacticWarehouse/scripts.inc"
	.include "data/maps/TeamGalacticEternaBuilding_1F/scripts.inc"
	.include "data/maps/TeamGalacticEternaBuilding_2F/scripts.inc"
	.include "data/maps/TeamGalacticEternaBuilding_3F/scripts.inc"
	.include "data/maps/TeamGalacticEternaBuilding_4F/scripts.inc"
	.include "data/maps/SpearPillar/scripts.inc"
	.include "data/maps/SpearPillar_Distorted/scripts.inc"
	.include "data/maps/SpearPillar_Dialga/scripts.inc"
	.include "data/maps/SpearPillar_Palkia/scripts.inc"
	.include "data/maps/RavagedPath/scripts.inc"
	.include "data/maps/ResortArea/scripts.inc"
	.include "data/maps/Route19_UnusedHouse_Frlg/scripts.inc"
	.include "data/maps/Route201/scripts.inc"
	.include "data/maps/Route202/scripts.inc"
	.include "data/maps/Route203/scripts.inc"
	.include "data/maps/Route204/scripts.inc"
	.include "data/maps/Route205_North/scripts.inc"
	.include "data/maps/Route205_South/scripts.inc"
	.include "data/maps/Route206/scripts.inc"
	.include "data/maps/Route206_North/scripts.inc"
	.include "data/maps/Route206_South/scripts.inc"
	.include "data/maps/Route207/scripts.inc"
	.include "data/maps/Route208/scripts.inc"
	.include "data/maps/Route208_Access/scripts.inc"
	.include "data/maps/Route209/scripts.inc"
	.include "data/maps/Route209_Access/scripts.inc"
	.include "data/maps/Route210_North/scripts.inc"
	.include "data/maps/Route210_South/scripts.inc"
	.include "data/maps/Route211_East/scripts.inc"
	.include "data/maps/Route211_West/scripts.inc"
	.include "data/maps/Route212_Access/scripts.inc"
	.include "data/maps/Route212_North/scripts.inc"
	.include "data/maps/Route212_South/scripts.inc"
	.include "data/maps/Route213/scripts.inc"
	.include "data/maps/Route213_Access/scripts.inc"
	.include "data/maps/Route214/scripts.inc"
	.include "data/maps/Route214_Access/scripts.inc"
	.include "data/maps/Route215/scripts.inc"
	.include "data/maps/Route215_Access/scripts.inc"
	.include "data/maps/Route216/scripts.inc"
	.include "data/maps/Route217/scripts.inc"
	.include "data/maps/Route218/scripts.inc"
	.include "data/maps/Route218_East/scripts.inc"
	.include "data/maps/Route218_West/scripts.inc"
	.include "data/maps/Route219/scripts.inc"
	.include "data/maps/Route220/scripts.inc"
	.include "data/maps/Route221/scripts.inc"
	.include "data/maps/Route222/scripts.inc"
	.include "data/maps/Route222_Access/scripts.inc"
	.include "data/maps/Route223/scripts.inc"
	.include "data/maps/Route224/scripts.inc"
	.include "data/maps/Route225/scripts.inc"
	.include "data/maps/Route225_Access/scripts.inc"
	.include "data/maps/Route226/scripts.inc"
	.include "data/maps/Route226_Access/scripts.inc"
	.include "data/maps/Route227/scripts.inc"
	.include "data/maps/Route228/scripts.inc"
	.include "data/maps/Route229/scripts.inc"
	.include "data/maps/Route230/scripts.inc"
	.include "data/maps/SandgemTown/scripts.inc"
	.include "data/maps/SandgemTown_House1/scripts.inc"
	.include "data/maps/SandgemTown_RowanLab/scripts.inc"
	.include "data/maps/SandgemTown_Mart/scripts.inc"
	.include "data/maps/SandgemTown_PokemonCenter_1F/scripts.inc"
	.include "data/maps/SandgemTown_PokemonCenter_2F/scripts.inc"
	.include "data/maps/SandgemTown_RivalHouse_F1/scripts.inc"
	.include "data/maps/SandgemTown_RivalHouse_F2/scripts.inc"
	.include "data/maps/SnowpointCity/scripts.inc"
	.include "data/maps/SolaceonTown/scripts.inc"
	.include "data/maps/SunyshoreCity/scripts.inc"
	.include "data/maps/SurvivalArea/scripts.inc"
	.include "data/maps/TwinleafTown/scripts.inc"
	.include "data/maps/TwinleafTown_Haouse1/scripts.inc"
	.include "data/maps/TwinleafTown_House2/scripts.inc"
	.include "data/maps/TwinleafTown_MainHouse_1F/scripts.inc"
	.include "data/maps/TwinleafTown_MainHouse_2F/scripts.inc"
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
	.include "data/maps/RecordCorner_Frlg/scripts.inc"
	.include "data/maps/BattleColosseum_4P_Frlg/scripts.inc"
	.include "data/maps/UnionRoom_Frlg/scripts.inc"
	.include "data/maps/ViridianForest_Frlg/scripts.inc"
	.include "data/maps/MtMoon_1F_Frlg/scripts.inc"
	.include "data/maps/MtMoon_B1F_Frlg/scripts.inc"
	.include "data/maps/MtMoon_B2F_Frlg/scripts.inc"
	.include "data/maps/SSAnne_Exterior_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Corridor_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Corridor_Frlg/scripts.inc"
	.include "data/maps/SSAnne_3F_Corridor_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Corridor_Frlg/scripts.inc"
	.include "data/maps/SSAnne_Deck_Frlg/scripts.inc"
	.include "data/maps/SSAnne_Kitchen_Frlg/scripts.inc"
	.include "data/maps/SSAnne_CaptainsOffice_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room1_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room2_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room3_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room4_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room5_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room7_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room1_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room2_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room3_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room4_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room5_Frlg/scripts.inc"
	.include "data/maps/SSAnne_2F_Room6_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room1_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room2_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room3_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room4_Frlg/scripts.inc"
	.include "data/maps/SSAnne_B1F_Room5_Frlg/scripts.inc"
	.include "data/maps/SSAnne_1F_Room6_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_NorthSouthTunnel_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_SouthEntrance_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_WestEntrance_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_EastWestTunnel_Frlg/scripts.inc"
	.include "data/maps/UndergroundPath_EastEntrance_Frlg/scripts.inc"
	.include "data/maps/DiglettsCave_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/DiglettsCave_B1F_Frlg/scripts.inc"
	.include "data/maps/DiglettsCave_SouthEntrance_Frlg/scripts.inc"
	.include "data/maps/VictoryRoad_1F_Frlg/scripts.inc"
	.include "data/maps/VictoryRoad_2F_Frlg/scripts.inc"
	.include "data/maps/VictoryRoad_3F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B1F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B2F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B3F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_B4F_Frlg/scripts.inc"
	.include "data/maps/RocketHideout_Elevator_Frlg/scripts.inc"
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
	.include "data/maps/SilphCo_Elevator_Frlg/scripts.inc"
	.include "data/maps/PokemonMansion_1F_Frlg/scripts.inc"
	.include "data/maps/PokemonMansion_2F_Frlg/scripts.inc"
	.include "data/maps/PokemonMansion_3F_Frlg/scripts.inc"
	.include "data/maps/PokemonMansion_B1F_Frlg/scripts.inc"
	.include "data/maps/SafariZone_Center_Frlg/scripts.inc"
	.include "data/maps/SafariZone_East_Frlg/scripts.inc"
	.include "data/maps/SafariZone_North_Frlg/scripts.inc"
	.include "data/maps/SafariZone_West_Frlg/scripts.inc"
	.include "data/maps/SafariZone_Center_RestHouse_Frlg/scripts.inc"
	.include "data/maps/SafariZone_East_RestHouse_Frlg/scripts.inc"
	.include "data/maps/SafariZone_North_RestHouse_Frlg/scripts.inc"
	.include "data/maps/SafariZone_West_RestHouse_Frlg/scripts.inc"
	.include "data/maps/SafariZone_SecretHouse_Frlg/scripts.inc"
	.include "data/maps/CeruleanCave_1F_Frlg/scripts.inc"
	.include "data/maps/CeruleanCave_2F_Frlg/scripts.inc"
	.include "data/maps/CeruleanCave_B1F_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_LoreleisRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_BrunosRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_AgathasRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_LancesRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_ChampionsRoom_Frlg/scripts.inc"
	.include "data/maps/PokemonLeague_HallOfFame_Frlg/scripts.inc"
	.include "data/maps/RockTunnel_1F_Frlg/scripts.inc"
	.include "data/maps/RockTunnel_B1F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_1F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B1F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B2F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B3F_Frlg/scripts.inc"
	.include "data/maps/SeafoamIslands_B4F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_1F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_2F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_3F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_4F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_5F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_6F_Frlg/scripts.inc"
	.include "data/maps/PokemonTower_7F_Frlg/scripts.inc"
	.include "data/maps/PowerPlant_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B4F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_Exterior_Frlg/scripts.inc"
	.include "data/maps/MtEmber_SummitPath_1F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_SummitPath_2F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_SummitPath_3F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_Summit_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B5F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_1F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B1F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B2F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B3F_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B1F_Stairs_Frlg/scripts.inc"
	.include "data/maps/MtEmber_RubyPath_B2F_Stairs_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_BerryForest_Frlg/scripts.inc"
	.include "data/maps/FourIsland_IcefallCave_Entrance_Frlg/scripts.inc"
	.include "data/maps/FourIsland_IcefallCave_1F_Frlg/scripts.inc"
	.include "data/maps/FourIsland_IcefallCave_B1F_Frlg/scripts.inc"
	.include "data/maps/FourIsland_IcefallCave_Back_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_RocketWarehouse_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_1F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_B1F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_B2F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_B3F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_B4F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_DottedHole_SapphireRoom_Frlg/scripts.inc"
	.include "data/maps/SixIsland_PatternBush_Frlg/scripts.inc"
	.include "data/maps/SixIsland_AlteringCave_Frlg/scripts.inc"
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
	.include "data/maps/TrainerTower_Elevator_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Entrance_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room1_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room2_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room3_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room4_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room5_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room6_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room7_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room8_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room9_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room10_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room11_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room12_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room13_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_LostCave_Room14_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_MoneanChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_LiptooChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_WeepthChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_DilfordChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_ScufibChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_RixyChamber_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_ViapoisChamber_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_DunsparceTunnel_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_SevaultCanyon_TanobyKey_Frlg/scripts.inc"
	.include "data/maps/NavelRock_1F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Summit_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Base_Frlg/scripts.inc"
	.include "data/maps/NavelRock_SummitPath_2F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_SummitPath_3F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_SummitPath_4F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_SummitPath_5F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B1F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B2F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B3F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B4F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B5F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B6F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B7F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B8F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B9F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B10F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_BasePath_B11F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_B1F_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Fork_Frlg/scripts.inc"
	.include "data/maps/BirthIsland_Exterior_Frlg/scripts.inc"
	.include "data/maps/OneIsland_KindleRoad_EmberSpa_Frlg/scripts.inc"
	.include "data/maps/BirthIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/NavelRock_Harbor_Frlg/scripts.inc"
	.include "data/maps/PalletTown_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_Frlg/scripts.inc"
	.include "data/maps/IndigoPlateau_Exterior_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Connection_Frlg/scripts.inc"
	.include "data/maps/OneIsland_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Frlg/scripts.inc"
	.include "data/maps/FourIsland_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_Frlg/scripts.inc"
	.include "data/maps/SixIsland_Frlg/scripts.inc"
	.include "data/maps/Route1_Frlg/scripts.inc"
	.include "data/maps/Route2_Frlg/scripts.inc"
	.include "data/maps/Route3_Frlg/scripts.inc"
	.include "data/maps/Route4_Frlg/scripts.inc"
	.include "data/maps/Route5_Frlg/scripts.inc"
	.include "data/maps/Route6_Frlg/scripts.inc"
	.include "data/maps/Route7_Frlg/scripts.inc"
	.include "data/maps/Route8_Frlg/scripts.inc"
	.include "data/maps/Route9_Frlg/scripts.inc"
	.include "data/maps/Route10_Frlg/scripts.inc"
	.include "data/maps/Route11_Frlg/scripts.inc"
	.include "data/maps/Route12_Frlg/scripts.inc"
	.include "data/maps/Route13_Frlg/scripts.inc"
	.include "data/maps/Route14_Frlg/scripts.inc"
	.include "data/maps/Route15_Frlg/scripts.inc"
	.include "data/maps/Route16_Frlg/scripts.inc"
	.include "data/maps/Route17_Frlg/scripts.inc"
	.include "data/maps/Route18_Frlg/scripts.inc"
	.include "data/maps/Route19_Frlg/scripts.inc"
	.include "data/maps/Route20_Frlg/scripts.inc"
	.include "data/maps/Route21_North_Frlg/scripts.inc"
	.include "data/maps/Route21_South_Frlg/scripts.inc"
	.include "data/maps/Route22_Frlg/scripts.inc"
	.include "data/maps/Route23_Frlg/scripts.inc"
	.include "data/maps/Route24_Frlg/scripts.inc"
	.include "data/maps/Route25_Frlg/scripts.inc"
	.include "data/maps/OneIsland_KindleRoad_Frlg/scripts.inc"
	.include "data/maps/OneIsland_TreasureBeach_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_CapeBrink_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_BondBridge_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Port_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_ResortGorgeous_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_WaterLabyrinth_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_Meadow_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_MemorialPillar_Frlg/scripts.inc"
	.include "data/maps/SixIsland_OutcastIsland_Frlg/scripts.inc"
	.include "data/maps/SixIsland_GreenPath_Frlg/scripts.inc"
	.include "data/maps/SixIsland_WaterPath_Frlg/scripts.inc"
	.include "data/maps/SixIsland_RuinValley_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TrainerTower_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_SevaultCanyon_Entrance_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_SevaultCanyon_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_TanobyRuins_Frlg/scripts.inc"
	.include "data/maps/PalletTown_PlayersHouse_1F_Frlg/scripts.inc"
	.include "data/maps/PalletTown_PlayersHouse_2F_Frlg/scripts.inc"
	.include "data/maps/PalletTown_RivalsHouse_Frlg/scripts.inc"
	.include "data/maps/PalletTown_ProfessorOaksLab_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_House_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_Gym_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_School_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_Mart_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/ViridianCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Museum_1F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Museum_2F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Gym_Frlg/scripts.inc"
	.include "data/maps/PewterCity_Mart_Frlg/scripts.inc"
	.include "data/maps/PewterCity_House1_Frlg/scripts.inc"
	.include "data/maps/PewterCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/PewterCity_House2_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House1_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House2_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House3_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_Gym_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_BikeShop_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_Mart_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House4_Frlg/scripts.inc"
	.include "data/maps/CeruleanCity_House5_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_VolunteerPokemonHouse_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_House1_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_House2_Frlg/scripts.inc"
	.include "data/maps/LavenderTown_Mart_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_House1_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_PokemonFanClub_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_House2_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_Mart_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_Gym_Frlg/scripts.inc"
	.include "data/maps/VermilionCity_House3_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_1F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_2F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_3F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_4F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_5F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_Roof_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_DepartmentStore_Elevator_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_1F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_2F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_3F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_Roof_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Condominiums_RoofRoom_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_GameCorner_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_GameCorner_PrizeRoom_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Gym_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Restaurant_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_House1_Frlg/scripts.inc"
	.include "data/maps/CeladonCity_Hotel_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_SafariZone_Entrance_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_Mart_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_SafariZone_Office_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_Gym_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_House1_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_WardensHouse_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_House2_Frlg/scripts.inc"
	.include "data/maps/FuchsiaCity_House3_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_Gym_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonLab_Entrance_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonLab_Lounge_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonLab_ResearchRoom_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonLab_ExperimentRoom_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/CinnabarIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/IndigoPlateau_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/IndigoPlateau_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_CopycatsHouse_1F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_CopycatsHouse_2F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Dojo_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Gym_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_House_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_Mart_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_MrPsychicsHouse_Frlg/scripts.inc"
	.include "data/maps/SaffronCity_PokemonTrainerFanClub_Frlg/scripts.inc"
	.include "data/maps/Route2_ViridianForest_SouthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route2_House_Frlg/scripts.inc"
	.include "data/maps/Route2_EastBuilding_Frlg/scripts.inc"
	.include "data/maps/Route2_ViridianForest_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route4_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/Route4_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/Route5_PokemonDayCare_Frlg/scripts.inc"
	.include "data/maps/Route5_SouthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route6_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route6_UnusedHouse_Frlg/scripts.inc"
	.include "data/maps/Route7_EastEntrance_Frlg/scripts.inc"
	.include "data/maps/Route8_WestEntrance_Frlg/scripts.inc"
	.include "data/maps/Route10_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/Route10_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/Route11_EastEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route11_EastEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route12_NorthEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route12_NorthEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route12_FishingHouse_Frlg/scripts.inc"
	.include "data/maps/Route15_WestEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route15_WestEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route16_House_Frlg/scripts.inc"
	.include "data/maps/Route16_NorthEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route16_NorthEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route18_EastEntrance_1F_Frlg/scripts.inc"
	.include "data/maps/Route18_EastEntrance_2F_Frlg/scripts.inc"
	.include "data/maps/Route22_NorthEntrance_Frlg/scripts.inc"
	.include "data/maps/Route25_SeaCottage_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_House_Room1_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_House_Room2_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/OneIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/OneIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/OneIsland_House1_Frlg/scripts.inc"
	.include "data/maps/OneIsland_House2_Frlg/scripts.inc"
	.include "data/maps/OneIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_JoyfulGameCorner_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_House_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House1_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House2_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House3_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House4_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_House5_Frlg/scripts.inc"
	.include "data/maps/FourIsland_PokemonDayCare_Frlg/scripts.inc"
	.include "data/maps/FourIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/FourIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/FourIsland_House1_Frlg/scripts.inc"
	.include "data/maps/FourIsland_LoreleisHouse_Frlg/scripts.inc"
	.include "data/maps/FourIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/FourIsland_House2_Frlg/scripts.inc"
	.include "data/maps/FourIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_House1_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_House2_Frlg/scripts.inc"
	.include "data/maps/SixIsland_PokemonCenter_1F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_PokemonCenter_2F_Frlg/scripts.inc"
	.include "data/maps/SixIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/SixIsland_House_Frlg/scripts.inc"
	.include "data/maps/SixIsland_Mart_Frlg/scripts.inc"
	.include "data/maps/ThreeIsland_Harbor_Frlg/scripts.inc"
	.include "data/maps/FiveIsland_ResortGorgeous_House_Frlg/scripts.inc"
	.include "data/maps/TwoIsland_CapeBrink_House_Frlg/scripts.inc"
	.include "data/maps/SixIsland_WaterPath_House1_Frlg/scripts.inc"
	.include "data/maps/SixIsland_WaterPath_House2_Frlg/scripts.inc"
	.include "data/maps/SevenIsland_SevaultCanyon_House_Frlg/scripts.inc"

	.include "data/scripts/trainer_tower.inc"
	.include "data/scripts/fame_checker_frlg.inc"
	.include "data/text/fame_checker_frlg.inc"
	.include "data/scripts/item_ball_scripts_frlg.inc"
	.include "data/scripts/silphco_doors.inc"
	.include "data/scripts/move_tutors_frlg.inc"
	.include "data/scripts/cable_club_frlg.inc"
	.include "data/scripts/trainer_card_frlg.inc"
	.include "data/text/trainer_card_frlg.inc"
	.include "data/scripts/mystery_event_club.inc"
	.include "data/scripts/day_care_frlg.inc"
	.include "data/text/day_care_frlg.inc"
	.include "data/scripts/seagallop.inc"
	.include "data/scripts/static_pokemon.inc"
	.include "data/scripts/aide.inc"
	.include "data/scripts/pokemon_mansion.inc"
	.include "data/scripts/pokemon_league.inc"
	.include "data/scripts/route23.inc"
	.include "data/text/new_game_intro_frlg.inc"
	.include "data/scripts/trainers_frlg.inc"
	.include "data/text/trainers_frlg.inc"
	.include "data/text/ingame_trade_frlg.inc"
	.include "data/scripts/flavor_text.inc"
	.include "data/scripts/pkmn_center_nurse_frlg.inc"

@ (antes: .endif do .if IS_FRLG que fechava os scripts de Kanto)

	.include "data/scripts/std_msgbox.inc"
	.include "data/scripts/trainer_battle.inc"
	.include "data/scripts/new_game.inc"
	.include "data/scripts/hall_of_fame.inc"
	.include "data/scripts/hall_of_fame_frlg.inc"

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
	.include "data/scripts/record_mix.inc"
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

	.include "data/scripts/cave_of_origin.inc"
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

	.include "data/scripts/elite_four.inc"
	.include "data/scripts/sinnoh_league.inc"
	.include "data/scripts/movement.inc"
	.include "data/scripts/check_furniture.inc"
	.include "data/scripts/mart_clerk.inc"
	.include "data/text/record_mix.inc"
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
	.include "data/scripts/profile_man.inc"
	.include "data/scripts/day_care.inc"
	.include "data/scripts/flash.inc"
	.include "data/scripts/players_house.inc"
	.include "data/scripts/berry_blender.inc"
	.include "data/text/mauville_man.inc"
	.include "data/text/trainers.inc"
	.include "data/scripts/repel.inc"
	.include "data/scripts/safari_zone.inc"
	.include "data/scripts/roulette.inc"
	.include "data/scripts/pokedex_rating.inc"
	.include "data/text/pokedex_rating.inc"
	.include "data/text/lottery_corner.inc"
	.include "data/text/event_ticket_1.inc"
	.include "data/text/braille.inc"
	.include "data/text/berries.inc"
	.include "data/text/shoal_cave.inc"
	.include "data/text/check_furniture.inc"
	.include "data/scripts/cave_hole.inc"
	.include "data/scripts/lilycove_lady.inc"
	.include "data/text/match_call.inc"
	.include "data/scripts/apprentice.inc"
	.include "data/text/apprentice.inc"
	.include "data/scripts/battle_pike.inc"
	.include "data/text/blend_master.inc"
	.include "data/text/battle_tent.inc"
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
	.include "data/scripts/apricorn_tree.inc"
	.include "data/scripts/wild_encounter.inc"

	.include "data/maps/AzaleaTown/scripts.inc"
	.include "data/maps/BellchimeTrail/scripts.inc"
	.include "data/maps/BlackthornCity/scripts.inc"
	.include "data/maps/CherrygroveCity/scripts.inc"
	.include "data/maps/CianwoodCity/scripts.inc"
	.include "data/maps/CliffEdgeCave/scripts.inc"
	.include "data/maps/CliffEdgeGate/scripts.inc"
	.include "data/maps/EcruteakCity/scripts.inc"
	.include "data/maps/EmbeddedTower/scripts.inc"
	.include "data/maps/GoldenrodCity/scripts.inc"
	.include "data/maps/IlexForest/scripts.inc"
	.include "data/maps/LakeOfRage/scripts.inc"
	.include "data/maps/LakeOfRageLowTide/scripts.inc"
	.include "data/maps/Mahoganytown/scripts.inc"
	.include "data/maps/MtSilver_Outside/scripts.inc"
	.include "data/maps/MtSilver_Snow/scripts.inc"
	.include "data/maps/MtSilver_SummitDay/scripts.inc"
	.include "data/maps/NationalPark_BugContest/scripts.inc"
	.include "data/maps/NationalPark_Normal/scripts.inc"
	.include "data/maps/NewBarkTown/scripts.inc"
	.include "data/maps/OlivineCity/scripts.inc"
	.include "data/maps/ReceptionGate/scripts.inc"
	.include "data/maps/Route26/scripts.inc"
	.include "data/maps/Route26North/scripts.inc"
	.include "data/maps/Route26_House1/scripts.inc"
	.include "data/maps/Route26_House2/scripts.inc"
	.include "data/maps/Route27/scripts.inc"
	.include "data/maps/Route27_House/scripts.inc"
	.include "data/maps/Route28/scripts.inc"
	.include "data/maps/Route28_House/scripts.inc"
	.include "data/maps/Route29/scripts.inc"
	.include "data/maps/Route30/scripts.inc"
	.include "data/maps/Route30_House/scripts.inc"
	.include "data/maps/Route30_MrPokemonsHouse/scripts.inc"
	.include "data/maps/Route31/scripts.inc"
	.include "data/maps/Route32/scripts.inc"
	.include "data/maps/Route32_PokemonCenter/scripts.inc"
	.include "data/maps/Route33/scripts.inc"
	.include "data/maps/Route34/scripts.inc"
	.include "data/maps/Route34_DayCare/scripts.inc"
	.include "data/maps/Route35/scripts.inc"
	.include "data/maps/Route36/scripts.inc"
	.include "data/maps/Route37/scripts.inc"
	.include "data/maps/Route38/scripts.inc"
	.include "data/maps/Route39/scripts.inc"
	.include "data/maps/Route39_Barn/scripts.inc"
	.include "data/maps/Route39_FarmHouse/scripts.inc"
	.include "data/maps/Route40/scripts.inc"
	.include "data/maps/Route41/scripts.inc"
	.include "data/maps/Route42/scripts.inc"
	.include "data/maps/Route43/scripts.inc"
	.include "data/maps/Route44/scripts.inc"
	.include "data/maps/Route45/scripts.inc"
	.include "data/maps/Route46/scripts.inc"
	.include "data/maps/Route47/scripts.inc"
	.include "data/maps/Route48/scripts.inc"
	.include "data/maps/RuinsOfAlph_Outside/scripts.inc"
	.include "data/maps/SafariZoneGate/scripts.inc"
	.include "data/maps/VioletCity/scripts.inc"
	.include "data/maps/WorldHub/scripts.inc"
	.include "data/maps/WorldHub2/scripts.inc"

	.include "data/maps/AzaleaTown_Gym/scripts.inc"
	.include "data/maps/AzaleaTown_House1/scripts.inc"
	.include "data/maps/AzaleaTown_KurtsHouse/scripts.inc"
	.include "data/maps/AzaleaTown_Mart/scripts.inc"
	.include "data/maps/AzaleaTown_PokemonCenter/scripts.inc"
	.include "data/maps/BattlePyramidSquare02/scripts.inc"
	.include "data/maps/BattlePyramidSquare03/scripts.inc"
	.include "data/maps/BattlePyramidSquare04/scripts.inc"
	.include "data/maps/BattlePyramidSquare05/scripts.inc"
	.include "data/maps/BattlePyramidSquare06/scripts.inc"
	.include "data/maps/BattlePyramidSquare07/scripts.inc"
	.include "data/maps/BattlePyramidSquare08/scripts.inc"
	.include "data/maps/BattlePyramidSquare09/scripts.inc"
	.include "data/maps/BattlePyramidSquare10/scripts.inc"
	.include "data/maps/BattlePyramidSquare11/scripts.inc"
	.include "data/maps/BattlePyramidSquare12/scripts.inc"
	.include "data/maps/BattlePyramidSquare13/scripts.inc"
	.include "data/maps/BattlePyramidSquare14/scripts.inc"
	.include "data/maps/BattlePyramidSquare15/scripts.inc"
	.include "data/maps/BattlePyramidSquare16/scripts.inc"
	.include "data/maps/BlackthornCity_Gym/scripts.inc"
	.include "data/maps/BlackthornCity_House1/scripts.inc"
	.include "data/maps/BlackthornCity_House2/scripts.inc"
	.include "data/maps/BlackthornCity_House3/scripts.inc"
	.include "data/maps/BlackthornCity_Mart/scripts.inc"
	.include "data/maps/BlackthornCity_PokemonCenter/scripts.inc"
	.include "data/maps/BurnedTower_1F/scripts.inc"
	.include "data/maps/BurnedTower_B1F/scripts.inc"
	.include "data/maps/CherrygroveCity_House1/scripts.inc"
	.include "data/maps/CherrygroveCity_House2/scripts.inc"
	.include "data/maps/CherrygroveCity_House3/scripts.inc"
	.include "data/maps/CherrygroveCity_Mart/scripts.inc"
	.include "data/maps/CherrygroveCity_PokemonCenter/scripts.inc"
	.include "data/maps/CianwoodGym/scripts.inc"
	.include "data/maps/CianwoodHouse1/scripts.inc"
	.include "data/maps/CianwoodHouse2/scripts.inc"
	.include "data/maps/CianwoodHouse3/scripts.inc"
	.include "data/maps/CianwoodPokecenter/scripts.inc"
	.include "data/maps/CianwoodShop/scripts.inc"
	.include "data/maps/ContestHallBeauty/scripts.inc"
	.include "data/maps/ContestHallCool/scripts.inc"
	.include "data/maps/ContestHallCute/scripts.inc"
	.include "data/maps/ContestHallSmart/scripts.inc"
	.include "data/maps/ContestHallTough/scripts.inc"
	.include "data/maps/DarkCave_NorthSide/scripts.inc"
	.include "data/maps/DarkCave_SouthSide/scripts.inc"
	.include "data/maps/DiglettsCave_EntranceNorth/scripts.inc"
	.include "data/maps/DiglettsCave_EntranceSouth/scripts.inc"
	.include "data/maps/DiglettsCave_Tunnel/scripts.inc"
	.include "data/maps/DragonsDen_Cavern/scripts.inc"
	.include "data/maps/DragonsDen_Entrance/scripts.inc"
	.include "data/maps/DragonsDen_Shrine/scripts.inc"
	.include "data/maps/EcruteakCity_Gym/scripts.inc"
	.include "data/maps/EcruteakCity_House1/scripts.inc"
	.include "data/maps/EcruteakCity_House2/scripts.inc"
	.include "data/maps/EcruteakCity_Mart/scripts.inc"
	.include "data/maps/EcruteakCity_PokemonCenter/scripts.inc"
	.include "data/maps/EcruteakCity_SageOffice1/scripts.inc"
	.include "data/maps/EcruteakCity_SageOffice2/scripts.inc"
	.include "data/maps/EcruteakCity_Theater/scripts.inc"
	.include "data/maps/Gate_AzaleaTown_IlexForest/scripts.inc"
	.include "data/maps/Gate_EcruteakCity_Route38/scripts.inc"
	.include "data/maps/Gate_EcruteakCity_Route42/scripts.inc"
	.include "data/maps/Gate_GoldenrodCity_Route35/scripts.inc"
	.include "data/maps/Gate_IlexForest_Route34/scripts.inc"
	.include "data/maps/Gate_MahoganyTown_Route43/scripts.inc"
	.include "data/maps/Gate_NationalPark/scripts.inc"
	.include "data/maps/Gate_Route29_Route46/scripts.inc"
	.include "data/maps/Gate_Route31_VioletCity/scripts.inc"
	.include "data/maps/Gate_Route40_TrainerHill_Courtyard/scripts.inc"
	.include "data/maps/Gate_Route43/scripts.inc"
	.include "data/maps/Gate_RuinsOfAlph_Route32/scripts.inc"
	.include "data/maps/Gate_RuinsOfAlph_Route36/scripts.inc"
	.include "data/maps/GoldenrodCity_BikeShop/scripts.inc"
	.include "data/maps/GoldenrodCity_BillsHouse/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStoreBasement/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStoreElevator/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStore_1F/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStore_2F/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStore_3F/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStore_4F/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStore_5F/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStore_6F/scripts.inc"
	.include "data/maps/GoldenrodCity_DepartmentStore_7F/scripts.inc"
	.include "data/maps/GoldenrodCity_FlowerShop/scripts.inc"
	.include "data/maps/GoldenrodCity_GameCorner/scripts.inc"
	.include "data/maps/GoldenrodCity_Gym/scripts.inc"
	.include "data/maps/GoldenrodCity_House1/scripts.inc"
	.include "data/maps/GoldenrodCity_House2/scripts.inc"
	.include "data/maps/GoldenrodCity_House3/scripts.inc"
	.include "data/maps/GoldenrodCity_PokemonCenter/scripts.inc"
	.include "data/maps/GoldenrodCity_RadioTower_1F/scripts.inc"
	.include "data/maps/GoldenrodCity_RadioTower_2F/scripts.inc"
	.include "data/maps/GoldenrodCity_RadioTower_3F/scripts.inc"
	.include "data/maps/GoldenrodCity_RadioTower_4F/scripts.inc"
	.include "data/maps/GoldenrodCity_RadioTower_5F/scripts.inc"
	.include "data/maps/GoldenrodCity_TrainStation/scripts.inc"
	.include "data/maps/GoldenrodCity_UndergroundEntrance/scripts.inc"
	.include "data/maps/GoldenrodCity_UndergroundStorage/scripts.inc"
	.include "data/maps/GoldenrodCity_UndergroundSwitches/scripts.inc"
	.include "data/maps/GoldenrodCity_UndergroundTunnel/scripts.inc"
	.include "data/maps/IcePath_1F/scripts.inc"
	.include "data/maps/IcePath_B1F/scripts.inc"
	.include "data/maps/IcePath_B2F/scripts.inc"
	.include "data/maps/IcePath_B3F/scripts.inc"
	.include "data/maps/IcePath_B4F/scripts.inc"
	.include "data/maps/LakeOfRage_House1/scripts.inc"
	.include "data/maps/LakeOfRage_House2/scripts.inc"
	.include "data/maps/MahoganyTown_Gym/scripts.inc"
	.include "data/maps/MahoganyTown_House1/scripts.inc"
	.include "data/maps/MahoganyTown_PokemonCenter/scripts.inc"
	.include "data/maps/MahoganyTown_Shop/scripts.inc"
	.include "data/maps/MahoganyHideout_B1F/scripts.inc"
	.include "data/maps/MahoganyHideout_B2F/scripts.inc"
	.include "data/maps/MahoganyHideout_B3F/scripts.inc"
	.include "data/maps/MtMortar_1F_North/scripts.inc"
	.include "data/maps/MtMortar_1F_South/scripts.inc"
	.include "data/maps/MtMortar_2F/scripts.inc"
	.include "data/maps/MtMortar_B1F/scripts.inc"
	.include "data/maps/MtSilver_1F_ItemRoom/scripts.inc"
	.include "data/maps/MtSilver_1F_MoltresRoom/scripts.inc"
	.include "data/maps/MtSilver_1F_WaterfallRoom/scripts.inc"
	.include "data/maps/MtSilver_2F/scripts.inc"
	.include "data/maps/MtSilver_3F/scripts.inc"
	.include "data/maps/MtSilver_MountainSide/scripts.inc"
	.include "data/maps/MtSilver_PokemonCenter/scripts.inc"
	.include "data/maps/NewBarkTown_House1/scripts.inc"
	.include "data/maps/NewBarkTown_House2/scripts.inc"
	.include "data/maps/NewBarkTown_Lab/scripts.inc"
	.include "data/maps/NewBarkTown_PlayersHouse_1F/scripts.inc"
	.include "data/maps/NewBarkTown_PlayersHouse_2F/scripts.inc"
	.include "data/maps/OlivineCity_Cafe/scripts.inc"
	.include "data/maps/OlivineCity_Gym/scripts.inc"
	.include "data/maps/OlivineCity_House1/scripts.inc"
	.include "data/maps/OlivineCity_House2/scripts.inc"
	.include "data/maps/OlivineCity_House3/scripts.inc"
	.include "data/maps/OlivineCity_Lighthouse/scripts.inc"
	.include "data/maps/OlivineCity_Mart/scripts.inc"
	.include "data/maps/OlivineCity_PokemonCenter/scripts.inc"
	.include "data/maps/OlivineCity_PortInside/scripts.inc"
	.include "data/maps/OlivineCity_PortOutside/scripts.inc"
	.include "data/maps/Route23_UnusedHouse/scripts.inc"
	.include "data/maps/RuinsOfAlph_B1F/scripts.inc"
	.include "data/maps/RuinsOfAlph_Lab/scripts.inc"
	.include "data/maps/RuinsOfAlph_PuzzleAndRewardChambers/scripts.inc"
	.include "data/maps/RuinsOfAlph_WordsRoom1/scripts.inc"
	.include "data/maps/RuinsOfAlph_WordsRoom2/scripts.inc"
	.include "data/maps/RuinsOfAlph_WordsRoom3/scripts.inc"
	.include "data/maps/RuinsOfAlph_WordsRoom4/scripts.inc"
	.include "data/maps/SafariZoneGate_PokemonCenter/scripts.inc"
	.include "data/maps/SafariZoneGate_SafariZoneEntrance/scripts.inc"
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
	.include "data/maps/SevenIsland_UnusedHouse/scripts.inc"
	.include "data/maps/SlowpokeWell_B1F/scripts.inc"
	.include "data/maps/SlowpokeWell_B2F/scripts.inc"
	.include "data/maps/SproutTower_1F/scripts.inc"
	.include "data/maps/SproutTower_2F/scripts.inc"
	.include "data/maps/SproutTower_3F/scripts.inc"
	.include "data/maps/TinTower_1F/scripts.inc"
	.include "data/maps/TinTower_2F/scripts.inc"
	.include "data/maps/TinTower_3F/scripts.inc"
	.include "data/maps/TinTower_4F/scripts.inc"
	.include "data/maps/TinTower_5F/scripts.inc"
	.include "data/maps/TinTower_6F/scripts.inc"
	.include "data/maps/TinTower_7F/scripts.inc"
	.include "data/maps/TinTower_8F/scripts.inc"
	.include "data/maps/TinTower_9F/scripts.inc"
	.include "data/maps/TinTower_RoofDay/scripts.inc"
	.include "data/maps/TohjoFalls_Cavern/scripts.inc"
	.include "data/maps/TohjoFalls_GiovanniRoom/scripts.inc"
	.include "data/maps/TrainerHill_Courtyard/scripts.inc"
	.include "data/maps/UnionCave_1F/scripts.inc"
	.include "data/maps/UnionCave_B1F/scripts.inc"
	.include "data/maps/UnionCave_B2F/scripts.inc"
	.include "data/maps/UnusedContestHall1/scripts.inc"
	.include "data/maps/UnusedContestHall2/scripts.inc"
	.include "data/maps/UnusedContestHall3/scripts.inc"
	.include "data/maps/UnusedContestHall4/scripts.inc"
	.include "data/maps/UnusedContestHall5/scripts.inc"
	.include "data/maps/UnusedContestHall6/scripts.inc"
	.include "data/maps/VioletCity_Gym/scripts.inc"
	.include "data/maps/VioletCity_House1/scripts.inc"
	.include "data/maps/VioletCity_House2/scripts.inc"
	.include "data/maps/VioletCity_Mart/scripts.inc"
	.include "data/maps/VioletCity_PokemonCenter/scripts.inc"
	.include "data/maps/VioletCity_TrainerSchool/scripts.inc"
	.include "data/maps/WhirlIslands_1F/scripts.inc"
	.include "data/maps/WhirlIslands_B1F/scripts.inc"
	.include "data/maps/WhirlIslands_B1F_Inner/scripts.inc"
	.include "data/maps/WhirlIslands_B2F/scripts.inc"
	.include "data/maps/WhirlIslands_B3F/scripts.inc"
	.include "data/maps/WhirlIslands_Descent/scripts.inc"
	.include "data/maps/WhirlIslands_LugiaChamber/scripts.inc"

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
	.include "data/maps/CanalaveCityPokecenter1F/scripts.inc"
	.include "data/maps/CanalaveCityPokecenter2F/scripts.inc"
	.include "data/maps/CanalaveCityMart/scripts.inc"
	.include "data/maps/CanalaveLibrary1F/scripts.inc"
	.include "data/maps/CanalaveCitySoutheastHouse/scripts.inc"
	.include "data/maps/CelesticTownPokecenter1F/scripts.inc"
	.include "data/maps/CelesticTownPokecenter2F/scripts.inc"
	.include "data/maps/CelesticTownNorthHouse/scripts.inc"
	.include "data/maps/EternaCityPokecenter1F/scripts.inc"
	.include "data/maps/EternaCityPokecenter2F/scripts.inc"
	.include "data/maps/EternaCityMart/scripts.inc"
	.include "data/maps/CycleShop/scripts.inc"
	.include "data/maps/EternaCityHerbShop/scripts.inc"
	.include "data/maps/EternaCityCondominiums1F/scripts.inc"
	.include "data/maps/EternaCitySouthHouse/scripts.inc"
	.include "data/maps/EternaCityEastHouse/scripts.inc"
	.include "data/maps/FightAreaPokecenter1F/scripts.inc"
	.include "data/maps/FightAreaPokecenter2F/scripts.inc"
	.include "data/maps/FightAreaMart/scripts.inc"
	.include "data/maps/BattleFrontierGateToFightArea/scripts.inc"
	.include "data/maps/FightAreaMiddleHouse/scripts.inc"
	.include "data/maps/FightAreaSouthHouse/scripts.inc"
	.include "data/maps/HearthomeCityPokecenter1F/scripts.inc"
	.include "data/maps/HearthomeCityPokecenter2F/scripts.inc"
	.include "data/maps/HearthomeCityMart/scripts.inc"
	.include "data/maps/HearthomeCityWestGateToAmitySquare/scripts.inc"
	.include "data/maps/HearthomeCityEastGateToAmitySquare/scripts.inc"
	.include "data/maps/ContestHallLobby/scripts.inc"
	.include "data/maps/HearthomeCityNorthwestHouse/scripts.inc"
	.include "data/maps/HearthomeCitySoutheastHouse1F/scripts.inc"
	.include "data/maps/ForeignBuilding/scripts.inc"
	.include "data/maps/PoffinHouse/scripts.inc"
	.include "data/maps/HearthomeCityPokemonFanClub/scripts.inc"
	.include "data/maps/HearthomeCityNortheastHouse1F/scripts.inc"
	.include "data/maps/MiningMuseum/scripts.inc"
	.include "data/maps/UnusedOreburghCityEastHouse3F/scripts.inc"
	.include "data/maps/OreburghGateB1F/scripts.inc"
	.include "data/maps/PastoriaCityPokecenter1F/scripts.inc"
	.include "data/maps/PastoriaCityPokecenter2F/scripts.inc"
	.include "data/maps/PastoriaCityMart/scripts.inc"
	.include "data/maps/PastoriaCityObservatoryGate1F/scripts.inc"
	.include "data/maps/PastoriaCityMiddleHouse/scripts.inc"
	.include "data/maps/PastoriaCityNorthHouse/scripts.inc"
	.include "data/maps/PastoriaCityEastHouse/scripts.inc"
	.include "data/maps/PastoriaCityNortheastHouse/scripts.inc"
	.include "data/maps/PastoriaCitySouthwestHouse/scripts.inc"
	.include "data/maps/ResortAreaPokecenter1F/scripts.inc"
	.include "data/maps/ResortAreaPokecenter2F/scripts.inc"
	.include "data/maps/Villa/scripts.inc"
	.include "data/maps/ResortAreaHouse/scripts.inc"
	.include "data/maps/Route205House/scripts.inc"
	.include "data/maps/Route208House/scripts.inc"
	.include "data/maps/Route210GrandmaWilmaHouse/scripts.inc"
	.include "data/maps/Cafe/scripts.inc"
	.include "data/maps/Route212House/scripts.inc"
	.include "data/maps/FootstepHouse/scripts.inc"
	.include "data/maps/GrandLakeRoute213EastHouse/scripts.inc"
	.include "data/maps/GrandLakeRoute213NorthwestHouse/scripts.inc"
	.include "data/maps/GrandLakeRoute213NortheastHouse/scripts.inc"
	.include "data/maps/Route216House/scripts.inc"
	.include "data/maps/Route217WestHouse/scripts.inc"
	.include "data/maps/Route217NortheastHouse/scripts.inc"
	.include "data/maps/Route221House/scripts.inc"
	.include "data/maps/PalParkLobby/scripts.inc"
	.include "data/maps/Route222EastHouse/scripts.inc"
	.include "data/maps/Route222WestHouse/scripts.inc"
	.include "data/maps/Route225House/scripts.inc"
	.include "data/maps/Route228GateToRoute226/scripts.inc"
	.include "data/maps/Route227House/scripts.inc"
	.include "data/maps/Route228NorthHouse/scripts.inc"
	.include "data/maps/Route228SouthHouse/scripts.inc"
	.include "data/maps/PokemonLeagueSouthPokecenter1F/scripts.inc"
	.include "data/maps/PokemonLeagueSouthPokecenter2F/scripts.inc"
	.include "data/maps/PokemonLeagueNorthPokecenter1F/scripts.inc"
	.include "data/maps/PokemonLeagueNorthPokecenter2F/scripts.inc"
	.include "data/maps/SnowpointCityPokecenter1F/scripts.inc"
	.include "data/maps/SnowpointCityPokecenter2F/scripts.inc"
	.include "data/maps/SnowpointCityMart/scripts.inc"
	.include "data/maps/SnowpointCityWestHouse/scripts.inc"
	.include "data/maps/SnowpointCityEastHouse/scripts.inc"
	.include "data/maps/SolaceonTownPokecenter1F/scripts.inc"
	.include "data/maps/SolaceonTownPokecenter2F/scripts.inc"
	.include "data/maps/SolaceonTownMart/scripts.inc"
	.include "data/maps/PokemonDayCare/scripts.inc"
	.include "data/maps/SolaceonTownNortheastHouse/scripts.inc"
	.include "data/maps/SunyshoreCityPokecenter1F/scripts.inc"
	.include "data/maps/SunyshoreCityPokecenter2F/scripts.inc"
	.include "data/maps/SunyshoreMarket/scripts.inc"
	.include "data/maps/SunyshoreCityMart/scripts.inc"
	.include "data/maps/SunyshoreCityNortheastHouse/scripts.inc"
	.include "data/maps/SunyshoreCityWestHouse/scripts.inc"
	.include "data/maps/SunyshoreCityNorthwestHouse/scripts.inc"
	.include "data/maps/UnusedSunyshoreCityHouse1/scripts.inc"
	.include "data/maps/UnusedSunyshoreCityHouse2/scripts.inc"
	.include "data/maps/SurvivalAreaPokecenter1F/scripts.inc"
	.include "data/maps/SurvivalAreaPokecenter2F/scripts.inc"
	.include "data/maps/SurvivalAreaMart/scripts.inc"
	.include "data/maps/Battleground/scripts.inc"
	.include "data/maps/SurvivalAreaSouthHouse/scripts.inc"
	.include "data/maps/SurvivalAreaNorthHouse/scripts.inc"
	.include "data/maps/ValleyWindworksBuilding/scripts.inc"
	.include "data/maps/GrandLakeValorLakefrontEastHouse/scripts.inc"
	.include "data/maps/GrandLakeValorLakefrontWestHouse/scripts.inc"
	.include "data/maps/VeilstoneCityPokecenter1F/scripts.inc"
	.include "data/maps/VeilstoneCityPokecenter2F/scripts.inc"
	.include "data/maps/VeilstoneStore1F/scripts.inc"
	.include "data/maps/VeilstoneCityPrizeExchange/scripts.inc"
	.include "data/maps/GameCorner/scripts.inc"
	.include "data/maps/VeilstoneCitySouthwestHouse/scripts.inc"
	.include "data/maps/VeilstoneCitySoutheastHouse/scripts.inc"
	.include "data/maps/VeilstoneCityNorthwestHouse/scripts.inc"
	.include "data/maps/VeilstoneCityNortheastHouse/scripts.inc"
	.include "data/maps/SSAqua_1F/scripts.inc"
	.include "data/maps/SSAqua_B1F/scripts.inc"
	.include "data/maps/SSAqua_CaptainsRoom/scripts.inc"
	.include "data/maps/SSAqua_PlayersRoom/scripts.inc"
	.include "data/maps/SSAqua_RoomNW/scripts.inc"
	.include "data/maps/SSAqua_RoomNE/scripts.inc"
	.include "data/maps/SSAqua_RoomNNE/scripts.inc"
	.include "data/maps/SSAqua_RoomSSW/scripts.inc"
	.include "data/maps/SSAqua_RoomSSE/scripts.inc"
	.include "data/maps/SSAqua_RoomSE/scripts.inc"
	.include "data/maps/SSAqua_RoomSW/scripts.inc"
	.include "data/maps/CanalaveCityHarborInn/scripts.inc"
	.include "data/maps/CanalaveCitySailorEldritchHouse/scripts.inc"
	.include "data/maps/CanalaveCityEastHouse/scripts.inc"
	.include "data/maps/CanalaveCityWestHouse/scripts.inc"
	.include "data/maps/CanalaveCityPokecenterB1F/scripts.inc"
	.include "data/maps/CelesticTownPokecenterB1F/scripts.inc"
	.include "data/maps/EternaCityUndergroundManHouse/scripts.inc"
	.include "data/maps/EternaCityPokecenterB1F/scripts.inc"
	.include "data/maps/FightAreaPokecenterB1F/scripts.inc"
	.include "data/maps/FloaromaTownPokecenterB1F/scripts.inc"
	.include "data/maps/HearthomeCityPokecenterB1F/scripts.inc"
	.include "data/maps/GlobalTerminal1F/scripts.inc"
	.include "data/maps/UnusedJubilifeCityHouse3/scripts.inc"
	.include "data/maps/UnusedJubilifeCityHouse4/scripts.inc"
	.include "data/maps/JubilifeCityPokecenterB1F/scripts.inc"
	.include "data/maps/OreburghCityPokecenterB1F/scripts.inc"
	.include "data/maps/PastoriaCityPokecenterB1F/scripts.inc"
	.include "data/maps/PokemonLeagueNorthPokecenterB1F/scripts.inc"
	.include "data/maps/PokemonLeagueSouthPokecenterB1F/scripts.inc"
	.include "data/maps/ResortAreaPokecenterB1F/scripts.inc"
	.include "data/maps/PokemonMansion/scripts.inc"
	.include "data/maps/SandgemTownPokecenterB1F/scripts.inc"
	.include "data/maps/SnowpointCityPokecenterB1F/scripts.inc"
	.include "data/maps/SolaceonTownPokemonNewsPress/scripts.inc"
	.include "data/maps/SolaceonTownPokecenterB1F/scripts.inc"
	.include "data/maps/SunyshoreCityPokecenterB1F/scripts.inc"
	.include "data/maps/SurvivalAreaPokecenterB1F/scripts.inc"
	.include "data/maps/VeilstoneCityPokecenterB1F/scripts.inc"
	.include "data/maps/AcuityCavern/scripts.inc"
	.include "data/maps/ValorCavern/scripts.inc"
	.include "data/maps/VerityCavern/scripts.inc"
	.include "data/maps/MtCoronet1FTunnelRoom/scripts.inc"
	.include "data/maps/MtCoronet2F/scripts.inc"
	.include "data/maps/WaywardCave1F/scripts.inc"
	.include "data/maps/RuinManiacCaveShort/scripts.inc"
	.include "data/maps/VictoryRoad1FRoom3/scripts.inc"
	.include "data/maps/SnowpointTemple1F/scripts.inc"
	.include "data/maps/LakeValorDrained/scripts.inc"
	.include "data/maps/LakeAcuityLowWater/scripts.inc"
	.include "data/maps/OldChateau/scripts.inc"
	.include "data/maps/MtCoronet3F/scripts.inc"
	.include "data/maps/MtCoronetIcebergRuins/scripts.inc"
	.include "data/maps/IcebergRuins/scripts.inc"
	.include "data/maps/RuinManiacCaveLong/scripts.inc"
	.include "data/maps/ManiacTunnel/scripts.inc"
	.include "data/maps/Route228RockPeakRuins/scripts.inc"
	.include "data/maps/RockPeakRuins/scripts.inc"
	.include "data/maps/SnowpointTempleB1F/scripts.inc"
	.include "data/maps/SolaceonRuinsManiacTunnelRoom/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom1/scripts.inc"
	.include "data/maps/MtCoronet6F/scripts.inc"
	.include "data/maps/LakeVerityLowWater/scripts.inc"
	.include "data/maps/VictoryRoad1FRoom2/scripts.inc"
	.include "data/maps/WaywardCaveB1F/scripts.inc"
	.include "data/maps/MtCoronet5F/scripts.inc"
	.include "data/maps/OldChateauSideRooms/scripts.inc"
	.include "data/maps/OldChateauDiningArea/scripts.inc"
	.include "data/maps/OldChateauCorridor/scripts.inc"
	.include "data/maps/SnowpointTempleB2F/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom2/scripts.inc"
	.include "data/maps/VictoryRoad1FRoom1/scripts.inc"
	.include "data/maps/MtCoronet4FRoom3/scripts.inc"
	.include "data/maps/OldChateauBackWestRoom/scripts.inc"
	.include "data/maps/OldChateauBackMiddleWestRoom/scripts.inc"
	.include "data/maps/OldChateauBackMiddleRoom/scripts.inc"
	.include "data/maps/OldChateauBackEastRoom/scripts.inc"
	.include "data/maps/SnowpointTempleB3F/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom3/scripts.inc"
	.include "data/maps/SnowpointTempleB4F/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom4/scripts.inc"
	.include "data/maps/SnowpointTempleB5F/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom5/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom6/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom7/scripts.inc"
	.include "data/maps/EternaCityCondominiums3F/scripts.inc"
	.include "data/maps/UnusedOreburghCityNorthwestHouse3F/scripts.inc"
	.include "data/maps/UnusedOreburghCityNorthHouse3F/scripts.inc"
	.include "data/maps/ResortAreaRibbonSyndicate1F/scripts.inc"
	.include "data/maps/SolaceonTownNorthHouse/scripts.inc"
	.include "data/maps/SolaceonTownEastHouse/scripts.inc"
	.include "data/maps/SunyshoreCityEastHouse/scripts.inc"
	.include "data/maps/RotomsRoom/scripts.inc"
	.include "data/maps/UnusedEternaCityCondominiums4F/scripts.inc"
	.include "data/maps/CelesticTownNorthwestHouse/scripts.inc"
	.include "data/maps/CelesticTownNortheastHouse/scripts.inc"
	.include "data/maps/CelesticTownSouthwestHouse/scripts.inc"
	.include "data/maps/EternaCityCondominiums2F/scripts.inc"
	.include "data/maps/GalacticHq4F/scripts.inc"
	.include "data/maps/HearthomeCityGymTrainerRoom2/scripts.inc"
	.include "data/maps/JubilifeTvElevator/scripts.inc"
	.include "data/maps/JubilifeTv2FGallery/scripts.inc"
	.include "data/maps/JubilifeTv3FGroupRankingRoom/scripts.inc"
	.include "data/maps/PastoriaCityObservatoryGate2F/scripts.inc"
	.include "data/maps/SunyshoreCityGymRoom2/scripts.inc"
	.include "data/maps/UnusedOreburghCityNorthHouse4F/scripts.inc"
	.include "data/maps/UnusedOreburghCityNorthwestHouse4F/scripts.inc"
	.include "data/maps/CanalaveLibrary2F/scripts.inc"
	.include "data/maps/ContestHallStageNoContest/scripts.inc"
	.include "data/maps/GlobalTerminal2F/scripts.inc"
	.include "data/maps/GlobalTerminal3F/scripts.inc"
	.include "data/maps/HearthomeCityGymLeaderRoom/scripts.inc"
	.include "data/maps/HearthomeCityNortheastHouseElevator/scripts.inc"
	.include "data/maps/HearthomeCitySoutheastHouseElevator/scripts.inc"
	.include "data/maps/PokemonLeagueElevatorToAaronRoom/scripts.inc"
	.include "data/maps/PokemonMansionMaidsRoom/scripts.inc"
	.include "data/maps/PokemonMansionOffice/scripts.inc"
	.include "data/maps/ResortAreaRibbonSyndicateElevator/scripts.inc"
	.include "data/maps/VistaLighthouseElevator/scripts.inc"
	.include "data/maps/SunyshoreCityGymRoom3/scripts.inc"
	.include "data/maps/Restaurant/scripts.inc"
	.include "data/maps/VeilstoneStore2F/scripts.inc"
	.include "data/maps/VeilstoneStoreElevator/scripts.inc"
	.include "data/maps/VeilstoneStoreB1F/scripts.inc"
	.include "data/maps/CanalaveLibrary3F/scripts.inc"
	.include "data/maps/VeilstoneStore3F/scripts.inc"
	.include "data/maps/VeilstoneStore4F/scripts.inc"
	.include "data/maps/VeilstoneStore5F/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom1SoutheastDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom1NorthwestDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom2NortheastDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom2SoutheastDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom3NorthwestDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom3SouthwestDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom4SoutheastDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom5SouthwestDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom5SoutheastDeadend/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom6NorthwestDeadEnd/scripts.inc"
	.include "data/maps/SolaceonRuinsRoom6SoutheastDeadEnd/scripts.inc"
	.include "data/maps/SinnohVictoryRoad1F/scripts.inc"
	.include "data/maps/SinnohVictoryRoad2F/scripts.inc"
	.include "data/maps/SinnohVictoryRoadB1F/scripts.inc"
	.include "data/maps/OldChateauBackMiddleEastRoom/scripts.inc"
	.include "data/maps/Route209LostTower1F/scripts.inc"
	.include "data/maps/UnusedJubilifeCityCondominiums4F/scripts.inc"
	.include "data/maps/UnusedJubilifeCitySouthHouse4F/scripts.inc"
	.include "data/maps/Route209LostTower2F/scripts.inc"
	.include "data/maps/Route209LostTower3F/scripts.inc"
	.include "data/maps/Route209LostTower4F/scripts.inc"
	.include "data/maps/Route209LostTower5F/scripts.inc"
	.include "data/maps/SendoffSpring/scripts.inc"
	.include "data/maps/IronIsland/scripts.inc"
	.include "data/maps/StarkMountainOutside/scripts.inc"
	.include "data/maps/IronIsland1F/scripts.inc"
	.include "data/maps/TurnbackCaveEntrance/scripts.inc"
	.include "data/maps/StarkMountainRoom1/scripts.inc"
	.include "data/maps/IronIslandB3F/scripts.inc"
	.include "data/maps/IronIslandB1FLeftRoom/scripts.inc"
	.include "data/maps/IronIslandB1FRightRoom/scripts.inc"
	.include "data/maps/StarkMountainRoom2/scripts.inc"
	.include "data/maps/IronIslandB2FLeftRoom/scripts.inc"
	.include "data/maps/IronIslandB2FRightRoom/scripts.inc"
	.include "data/maps/IronIslandIronRuins/scripts.inc"
	.include "data/maps/IronRuins/scripts.inc"
	.include "data/maps/StarkMountainRoom3/scripts.inc"
