@ Sala de Bertha, Elite dos Quatro de Sinnoh.
@ Layout emprestado da Elite de Hoenn. A mecanica da porta esta em
@ data/scripts/sinnoh_league.inc e data/scripts/elite_four.inc.

SinnohLeague_BerthasRoom_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SinnohLeague_BerthasRoom_OnLoad
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SinnohLeague_BerthasRoom_OnWarp
	.byte 0

@ Porta do fundo continua aberta se Bertha ja foi derrotado.
SinnohLeague_BerthasRoom_OnLoad:
	checktrainerflag TRAINER_SINNOH_ELITE_FOUR_BERTHA
	call_if TRUE, SinnohLeague_EventScript_OpenNextDoorSilent
	end

SinnohLeague_BerthasRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, SinnohLeague_BerthasRoom_EventScript_PlayerTurnNorth
	.2byte 0

SinnohLeague_BerthasRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

SinnohLeague_BerthasRoom_EventScript_Bertha::
	lock
	faceplayer
	checktrainerflag TRAINER_SINNOH_ELITE_FOUR_BERTHA
	goto_if TRUE, SinnohLeague_BerthasRoom_EventScript_PostBattleSpeech
	playbgm MUS_ENCOUNTER_ELITE_FOUR, FALSE
	msgbox SinnohLeague_BerthasRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_ELITE_FOUR_BERTHA, SinnohLeague_BerthasRoom_Text_Defeat
	goto SinnohLeague_BerthasRoom_EventScript_Defeated
	end

SinnohLeague_BerthasRoom_EventScript_Defeated::
	call PokemonLeague_EliteFour_SetAdvanceToNextRoomMetatiles
	msgbox SinnohLeague_BerthasRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_BerthasRoom_EventScript_PostBattleSpeech::
	msgbox SinnohLeague_BerthasRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_BerthasRoom_Text_IntroSpeech:
	.string "Well, well. Aren't you a spry one?\n"
	.string "I'm BERTHA of the ELITE FOUR.\p"
	.string "I have been battling since long before\n"
	.string "you were born, youngster.\p"
	.string "Let me test that spirit of yours.$"

SinnohLeague_BerthasRoom_Text_Defeat:
	.string "My, my. Beaten by a child.\n"
	.string "How very refreshing.$"

SinnohLeague_BerthasRoom_Text_PostBattleSpeech:
	.string "Off you go, dear.\p"
	.string "FLINT waits in the next room, and that\n"
	.string "boy burns hot.$"
