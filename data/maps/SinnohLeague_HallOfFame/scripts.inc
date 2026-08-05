@ Hall da Fama de Sinnoh. Layout emprestado do Hall da Fama de Hoenn
@ (LAYOUT_EVER_GRANDE_CITY_HALL_OF_FAME), sem map.bin novo.
@
@ ponytail: a mecanica e a mesma do EverGrandeCity_HallOfFame, copiada do repo:
@ ON_FRAME com VAR_TEMP_1 (var temporaria, nao gasta var de save), o efeito de
@ campo FLDEFF_HALL_OF_FAME_RECORD e o special GameClear, que grava o time,
@ mostra a tela do Hall da Fama, salva e roda os creditos.
@
@ O QUE MUDA em relacao ao de Hoenn, e por que:
@ 1. GameClear cravava a volta em Littleroot. Agora o mapa avisa antes, por
@    VAR_0x8004 + special SetGameClearHealLocation, para onde o "Continue" deve
@    cair. Aqui: Sandgem Town, que e o Centro Pokemon do inicio de Sinnoh.
@ 2. NAO chama EverGrandeCity_HallOfFame_EventScript_SetGameClearFlags. Aquele
@    bloco e historia de Hoenn inteira (Sr. Briney, casa do Steven, Safari,
@    rival de Lilycove) e ligar tudo aquilo por ganhar a liga de Sinnoh
@    estragaria o save de Hoenn. Quem marca Sinnoh e FLAG_ELITE_SINNOH_VENCIDA,
@    ligada na sala da Cynthia.
@ 3. Zero warp e zero objeto: entra-se so pelo `warp` que a derrota da Cynthia
@    dispara, e sai-se pelos creditos. Sem porta, ninguem entra antes da hora, e
@    nao existe par de warp para quebrar.

SinnohLeague_HallOfFame_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SinnohLeague_HallOfFame_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SinnohLeague_HallOfFame_OnWarp
	.byte 0

SinnohLeague_HallOfFame_OnWarp:
	map_script_2 VAR_TEMP_1, 0, SinnohLeague_HallOfFame_EventScript_TurnPlayerNorth
	.2byte 0

SinnohLeague_HallOfFame_EventScript_TurnPlayerNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

SinnohLeague_HallOfFame_OnFrame:
	map_script_2 VAR_TEMP_1, 0, SinnohLeague_HallOfFame_EventScript_EnterHallOfFame
	.2byte 0

SinnohLeague_HallOfFame_EventScript_EnterHallOfFame::
	lockall
	applymovement LOCALID_PLAYER, SinnohLeague_HallOfFame_Movement_WalkIn
	waitmovement 0
	msgbox SinnohLeague_HallOfFame_Text_HereWeHonorChampions, MSGBOX_DEFAULT
	closemessage
	delay 20
	msgbox SinnohLeague_HallOfFame_Text_LetsRecordYourNames, MSGBOX_DEFAULT
	closemessage
	delay 20
	dofieldeffect FLDEFF_HALL_OF_FAME_RECORD
	waitfieldeffect FLDEFF_HALL_OF_FAME_RECORD
	delay 40
	setvar VAR_TEMP_1, 1
	setrespawn HEAL_LOCATION_SANDGEM_TOWN
	setvar VAR_0x8004, HEAL_LOCATION_SANDGEM_TOWN
	special SetGameClearHealLocation
	fadescreenspeed FADE_TO_BLACK, 24
	special GameClear
	releaseall
	end

SinnohLeague_HallOfFame_Movement_WalkIn:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SinnohLeague_HallOfFame_Text_HereWeHonorChampions:
	.string "This room keeps the records of\n"
	.string "Pokémon that came through the\l"
	.string "hardest battles in Sinnoh.\p"
	.string "It is here that the Champions of\n"
	.string "the Sinnoh League are honored.$"

SinnohLeague_HallOfFame_Text_LetsRecordYourNames:
	.string "Your name, as the Trainer who\n"
	.string "triumphed over the Sinnoh League,\l"
	.string "and the names of the partners who\l"
	.string "battled at your side.\p"
	.string "Let them be recorded here.$"
