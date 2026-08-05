@ Sala de Flint, Elite dos Quatro de Sinnoh.
@ Layout emprestado da Elite de Hoenn. A mecanica da porta esta em
@ data/scripts/sinnoh_league.inc e data/scripts/elite_four.inc.

SinnohLeague_FlintsRoom_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SinnohLeague_FlintsRoom_OnLoad
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SinnohLeague_FlintsRoom_OnWarp
	.byte 0

@ Porta do fundo continua aberta se Flint ja foi derrotado.
SinnohLeague_FlintsRoom_OnLoad:
	checktrainerflag TRAINER_SINNOH_ELITE_FOUR_FLINT
	call_if TRUE, SinnohLeague_EventScript_OpenNextDoorSilent
	end

SinnohLeague_FlintsRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, SinnohLeague_FlintsRoom_EventScript_PlayerTurnNorth
	.2byte 0

SinnohLeague_FlintsRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

SinnohLeague_FlintsRoom_EventScript_Flint::
	lock
	faceplayer
	checktrainerflag TRAINER_SINNOH_ELITE_FOUR_FLINT
	goto_if TRUE, SinnohLeague_FlintsRoom_EventScript_PostBattleSpeech
	playbgm MUS_ENCOUNTER_ELITE_FOUR, FALSE
	msgbox SinnohLeague_FlintsRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_ELITE_FOUR_FLINT, SinnohLeague_FlintsRoom_Text_Defeat
	goto SinnohLeague_FlintsRoom_EventScript_Defeated
	end

SinnohLeague_FlintsRoom_EventScript_Defeated::
	call PokemonLeague_EliteFour_SetAdvanceToNextRoomMetatiles
	msgbox SinnohLeague_FlintsRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_FlintsRoom_EventScript_PostBattleSpeech::
	msgbox SinnohLeague_FlintsRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_FlintsRoom_Text_IntroSpeech:
	.string "Hey! Good to meet you.\n"
	.string "I'm FLINT of the ELITE FOUR.\p"
	.string "My FIRE POKéMON burn hotter than\n"
	.string "anything you have faced so far.\p"
	.string "Come on and feel the heat!$"

SinnohLeague_FlintsRoom_Text_Defeat:
	.string "Whew! You put my fire right out.\n"
	.string "What a blast that was.$"

SinnohLeague_FlintsRoom_Text_PostBattleSpeech:
	.string "LUCIAN is up next.\p"
	.string "That guy reads a TRAINER like a book.\n"
	.string "Watch yourself in there.$"
