@ Sala de Aaron, Elite dos Quatro de Sinnoh.
@ Layout emprestado da Elite de Hoenn. A mecanica da porta esta em
@ data/scripts/sinnoh_league.inc e data/scripts/elite_four.inc.

SinnohLeague_AaronsRoom_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SinnohLeague_AaronsRoom_OnLoad
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SinnohLeague_AaronsRoom_OnWarp
	.byte 0

@ Porta do fundo continua aberta se Aaron ja foi derrotado.
SinnohLeague_AaronsRoom_OnLoad:
	checktrainerflag TRAINER_SINNOH_ELITE_FOUR_AARON
	call_if TRUE, SinnohLeague_EventScript_OpenNextDoorSilent
	end

SinnohLeague_AaronsRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, SinnohLeague_AaronsRoom_EventScript_PlayerTurnNorth
	.2byte 0

SinnohLeague_AaronsRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

SinnohLeague_AaronsRoom_EventScript_Aaron::
	lock
	faceplayer
	checktrainerflag TRAINER_SINNOH_ELITE_FOUR_AARON
	goto_if TRUE, SinnohLeague_AaronsRoom_EventScript_PostBattleSpeech
	playbgm MUS_ENCOUNTER_ELITE_FOUR, FALSE
	msgbox SinnohLeague_AaronsRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_ELITE_FOUR_AARON, SinnohLeague_AaronsRoom_Text_Defeat
	goto SinnohLeague_AaronsRoom_EventScript_Defeated
	end

SinnohLeague_AaronsRoom_EventScript_Defeated::
	call PokemonLeague_EliteFour_SetAdvanceToNextRoomMetatiles
	msgbox SinnohLeague_AaronsRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_AaronsRoom_EventScript_PostBattleSpeech::
	msgbox SinnohLeague_AaronsRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_AaronsRoom_Text_IntroSpeech:
	.string "Welcome to the SINNOH POKéMON LEAGUE.\n"
	.string "I'm AARON of the ELITE FOUR.\p"
	.string "I love BUG POKéMON. They give a battle\n"
	.string "everything they have, every time.\p"
	.string "Let me show you what that looks like!$"

SinnohLeague_AaronsRoom_Text_Defeat:
	.string "My bugs and I gave it all we had.\n"
	.string "That is the only way we know how.$"

SinnohLeague_AaronsRoom_Text_PostBattleSpeech:
	.string "You are strong. Very strong.\p"
	.string "Go on ahead. The next room is BERTHA's,\n"
	.string "and she will not go easy on you.$"
