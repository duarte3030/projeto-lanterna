@ Sala da campea Cynthia. Layout emprestado da sala do campeao de Hoenn.
@
@ ponytail: a porta do fundo NAO abre. Ela leva ao Hall da Fama de Hoenn, que
@ dispara creditos e devolve o jogador para Littleroot. Enquanto Sinnoh nao
@ tiver Hall da Fama proprio, vencer a Cynthia liga FLAG_ELITE_SINNOH_VENCIDA
@ (a unica reservada para isto em SINNOH-PADRAO.md) e o jogador volta andando.

SinnohLeague_ChampionsRoom_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SinnohLeague_ChampionsRoom_OnWarp
	.byte 0

SinnohLeague_ChampionsRoom_OnWarp:
	map_script_2 VAR_TEMP_1, 0, SinnohLeague_ChampionsRoom_EventScript_PlayerTurnNorth
	.2byte 0

SinnohLeague_ChampionsRoom_EventScript_PlayerTurnNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

SinnohLeague_ChampionsRoom_EventScript_Cynthia::
	lock
	faceplayer
	goto_if_set FLAG_ELITE_SINNOH_VENCIDA, SinnohLeague_ChampionsRoom_EventScript_PostBattleSpeech
	playbgm MUS_ENCOUNTER_CHAMPION, FALSE
	msgbox SinnohLeague_ChampionsRoom_Text_IntroSpeech, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_CHAMPION_CYNTHIA, SinnohLeague_ChampionsRoom_Text_Defeat
	goto SinnohLeague_ChampionsRoom_EventScript_Defeated
	end

SinnohLeague_ChampionsRoom_EventScript_Defeated::
	setflag FLAG_ELITE_SINNOH_VENCIDA
	playfanfare MUS_OBTAIN_BADGE
	msgbox SinnohLeague_ChampionsRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	waitfanfare
	release
	end

SinnohLeague_ChampionsRoom_EventScript_PostBattleSpeech::
	msgbox SinnohLeague_ChampionsRoom_Text_PostBattleSpeech, MSGBOX_DEFAULT
	release
	end

SinnohLeague_ChampionsRoom_Text_IntroSpeech:
	.string "I have been waiting for you.\n"
	.string "I'm CYNTHIA, the CHAMPION of SINNOH.\p"
	.string "Every TRAINER who reaches this room\n"
	.string "carries something worth seeing.\p"
	.string "Show me everything you have.\n"
	.string "I will do the same.$"

SinnohLeague_ChampionsRoom_Text_Defeat:
	.string "...Wonderful.\n"
	.string "I have never enjoyed a battle more.$"

SinnohLeague_ChampionsRoom_Text_PostBattleSpeech:
	.string "You are the new CHAMPION of SINNOH.\p"
	.string "Your POKéMON trusted you the whole way\n"
	.string "here, and you never let them down.\p"
	.string "Carry that with you wherever you go\n"
	.string "next. I will be watching.$"
