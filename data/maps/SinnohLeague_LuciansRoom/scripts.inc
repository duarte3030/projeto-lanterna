@ Sala de Lucian, Elite dos Quatro de Sinnoh.
@ Layout emprestado da Elite de Hoenn. A mecanica da porta esta em
@ data/scripts/sinnoh_league.inc e data/scripts/elite_four.inc.

SinnohLeague_LuciansRoom_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SinnohLeague_LuciansRoom_OnLoad
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SinnohLeague_LuciansRoom_OnWarp
	.byte 0

@ Porta do fundo continua aberta se Lucian ja foi derrotado.
SinnohLeague_LuciansRoom_OnLoad:
	checktrainerflag TRAINER_SINNOH_ELITE_FOUR_LUCIAN
	call_if TRUE, SinnohLeague_EventScript_OpenNextDoorSilent
	end

SinnohLeague_LuciansRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, SinnohLeague_LuciansRoom_EventScript_PlayerTurnNorth
	.2byte 0

SinnohLeague_LuciansRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

SinnohLeague_LuciansRoom_EventScript_Lucian::
	lock
	faceplayer
	checktrainerflag TRAINER_SINNOH_ELITE_FOUR_LUCIAN
	goto_if TRUE, SinnohLeague_LuciansRoom_EventScript_PostBattleSpeech
	playbgm MUS_ENCOUNTER_ELITE_FOUR, FALSE
	msgbox SinnohLeague_LuciansRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_ELITE_FOUR_LUCIAN, SinnohLeague_LuciansRoom_Text_Defeat
	goto SinnohLeague_LuciansRoom_EventScript_Defeated
	end

SinnohLeague_LuciansRoom_EventScript_Defeated::
	call PokemonLeague_EliteFour_SetAdvanceToNextRoomMetatiles
	msgbox SinnohLeague_LuciansRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_LuciansRoom_EventScript_PostBattleSpeech::
	msgbox SinnohLeague_LuciansRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_LuciansRoom_Text_IntroSpeech:
	.string "One moment. I was finishing a chapter.\n"
	.string "I'm LUCIAN of the ELITE FOUR.\p"
	.string "PSYCHIC POKéMON see further than any\n"
	.string "pair of eyes ever could.\p"
	.string "Let us see how far you can see.$"

SinnohLeague_LuciansRoom_Text_Defeat:
	.string "The final page turns.\n"
	.string "And I did not see it coming.$"

SinnohLeague_LuciansRoom_Text_PostBattleSpeech:
	.string "Beyond this door waits CYNTHIA, the\n"
	.string "CHAMPION of SINNOH.\p"
	.string "No challenger has ever gone further.\n"
	.string "Show me that you can.$"
