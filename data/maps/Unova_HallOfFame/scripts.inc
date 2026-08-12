@ HallOfFame do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Escrito a mao em 12/08/2026 (B6): a cena de HallOfFame.asm.
@
@ Antes disto o mapa tinha `.byte 0` de MapScripts e um unico objeto mudo: dava
@ para chegar aqui pelo warp da sala do Campeao e nao acontecia nada, com a
@ maquina do Hall da Fama desenhada no chao.
@
@ ponytail: a mecanica NAO e nova, e copiada de data/maps/SinnohLeague_HallOfFame,
@ que por sua vez copiou EverGrandeCity_HallOfFame: ON_FRAME_TABLE com VAR_TEMP_1
@ (var temporaria, nao gasta var de save), o efeito de campo
@ FLDEFF_HALL_OF_FAME_RECORD e o `special GameClear`, que grava o time, mostra a
@ tela do Hall da Fama, salva e roda os creditos.
@
@ O QUE MUDA em relacao ao de Sinnoh, e por que:
@ 1. O "Continue" cai no Centro Pokemon da LIGA, e nao em Littleroot. Ate
@    12/08/2026 Unova nao tinha UM ponto de cura declarado e nenhum Centro dela
@    chamava `setrespawn`, entao quem terminava aqui voltava para a ultima cama
@    de OUTRA regiao, a uma viagem de barco de distancia. Os 18 Centros de Unova
@    ganharam ponto de cura no mesmo dia, por
@    `dev_scripts/heal_locations_unova.py`.
@ 2. `returnfromcredits` da fonte nao existe aqui: o pos-creditos da sala do
@    Campeao roda na proxima visita, por VAR_UNOVA_LIGA_CENA = 3, que e o mesmo
@    `setmapscene CHAMPIONS_ROOM, SCENE_POST_CREDITS` da fonte. Ver o cabecalho
@    de data/maps/Unova_ChampionsRoom/scripts.inc.
@ 3. A JUNIPER (id local 1) anda em paralelo com o jogador em vez de `follow`,
@    que e comando do gen 2 e nao tem equivalente. Como ela ja nasce no tile
@    imediatamente acima do warp de entrada, andar os dois juntos mantem a
@    formacao da fonte.

Unova_HallOfFame_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Unova_HallOfFame_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Unova_HallOfFame_OnWarp
	.byte 0

Unova_HallOfFame_OnWarp:
	map_script_2 VAR_TEMP_1, 0, Unova_HallOfFame_EventScript_ViraJogadorParaNorte
	.2byte 0

Unova_HallOfFame_EventScript_ViraJogadorParaNorte::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

Unova_HallOfFame_OnFrame:
	map_script_2 VAR_TEMP_1, 0, Unova_HallOfFame_EventScript_EntraNoHall
	.2byte 0

Unova_HallOfFame_EventScript_EntraNoHall::
	lockall
	delay 30
	applymovement 1, Unova_HallOfFame_Movement_JuniperSobe
	applymovement LOCALID_PLAYER, Unova_HallOfFame_Movement_JogadorSobe
	waitmovement 0
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterRight
	applymovement 1, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox Unova_HallOfFame_Text_JuniperHallDaFama, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Common_Movement_WalkInPlaceFasterUp
	applymovement LOCALID_PLAYER, Unova_HallOfFame_Movement_JogadorAteAMaquina
	waitmovement 0
	delay 15
	dofieldeffect FLDEFF_HALL_OF_FAME_RECORD
	waitfieldeffect FLDEFF_HALL_OF_FAME_RECORD
	delay 40
	setvar VAR_TEMP_1, 1
	setflag FLAG_UNOVA_LIGA_VENCIDA
	setvar VAR_UNOVA_LIGA_CENA, 3
	setrespawn HEAL_LOCATION_UNOVA_PKMN_LEAGUE
	setvar VAR_0x8004, HEAL_LOCATION_UNOVA_PKMN_LEAGUE
	special SetGameClearHealLocation
	fadescreenspeed FADE_TO_BLACK, 24
	special GameClear
	releaseall
	end

Unova_HallOfFame_Movement_JuniperSobe:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_right
	step_end

Unova_HallOfFame_Movement_JogadorSobe:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

Unova_HallOfFame_Movement_JogadorAteAMaquina:
	walk_slow_up
	step_end

Unova_HallOfFame_Text_JuniperHallDaFama::
	.string "JUNIPER: This room is the HALL\n"
	.string "OF FAME.\p"
	.string "It exists to commemorate the\n"
	.string "Trainers and POKéMON who have\l"
	.string "demonstrated their stellar\l"
	.string "strength and kindness of heart.\p"
	.string "{PLAYER}, with your skill and\n"
	.string "persistence, you have earned\l"
	.string "your place in this HALL OF FAME.\p"
	.string "Your name, the account of your\n"
	.string "journey, and the history of your\l"
	.string "battles will all be recorded\l"
	.string "here.\p"
	.string "Now, {PLAYER}, you and the\n"
	.string "POKéMON who fought by your side\l"
	.string "will be recorded in this\l"
	.string "machine, as CHAMPIONS!$"
