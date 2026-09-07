@ Sala da campea Cynthia. Layout emprestado da sala do campeao de Hoenn.
@
@ ponytail: Sinnoh agora tem Hall da Fama proprio
@ (MAP_SINNOH_LEAGUE_HALL_OF_FAME), entao a cena termina la e nao no de Hoenn.
@ A porta do fundo continua NAO sendo warp, de proposito: quem leva o jogador
@ para dentro e o `warp` da derrota da Cynthia. Porta de verdade deixaria entrar
@ antes de bater nela, e um par de warp a mais para quebrar.

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
	closemessage
	warp MAP_SINNOH_LEAGUE_HALL_OF_FAME, 7, 12
	waitstate
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

@ A ÚLTIMA fala do cartucho 1, e por isso ela aponta para o pós-jogo que
@ EXISTE, e não para o que soaria bonito. Cada linha foi conferida no arquivo:
@
@ - DIALGA e PALKIA: `data/maps/SpearPillar_Dialga/scripts.inc` e o irmão
@   `SpearPillar_Palkia`, encontro único fechado por FLAG_CAUGHT_DIALGA e
@   FLAG_CAUGHT_PALKIA. GIRATINA: `data/maps/DistortionWorld/scripts.inc:25`.
@   ARCEUS aparece no Spear Pillar SÓ com os dois primeiros já capturados
@   (`data/maps/SpearPillar/scripts.inc:268`), então ela cita a ordem certa.
@ - BATTLE FRONTIER de Hoenn: quem abre é FLAG_SYS_GAME_CLEAR, acesa pelo
@   `special GameClear` do Hall da Fama (`src/post_battle_event_funcs.c:44`),
@   e a porta é o barco de Lilycove
@   (`data/maps/LilycoveCity_Harbor/scripts.inc:12` pergunta pela flag, a
@   linha 94 é o `warp MAP_BATTLE_FRONTIER_OUTSIDE_WEST`). Este é o único
@   item que a vitória sobre ela DESTRAVA; os outros já estavam lá.
@ - BATTLE TOWER de Olivine: `MAP_ROUTE40_BATTLE_TOWER`, obra da mesma onda.
@   Ela NÃO diz que a torre abriu agora, porque a torre está aberta desde
@   Johto: diz só que a série é de sete e que continua de pé.
@
@ O que ela NÃO promete: nada de Unova, nada de Galar, nada de "uma nova
@ jornada" genérica. As duas regiões saíram do cartucho em 07/09/2026 e o
@ barco perdeu os dois destinos.
SinnohLeague_ChampionsRoom_Text_PostBattleSpeech:
	.string "You are the new CHAMPION of SINNOH.\p"
	.string "Your POKéMON trusted you the whole way\n"
	.string "here, and you never let them down.\p"
	.string "This room is not the end of the road.\p"
	.string "SPEAR PILLAR still keeps DIALGA and\n"
	.string "PALKIA, and the DISTORTION WORLD under\l"
	.string "it still keeps GIRATINA.\p"
	.string "Bring me the first two and I am told\n"
	.string "something older answers.\p"
	.string "In HOENN, the ferry at LILYCOVE will\n"
	.string "sail to the BATTLE FRONTIER now that\l"
	.string "your name is in the HALL OF FAME.\p"
	.string "And the BATTLE TOWER on ROUTE 40, out\n"
	.string "past OLIVINE, still lines up seven\l"
	.string "TRAINERS for anyone who asks.\p"
	.string "Go and see what you are worth.\n"
	.string "I will be watching.$"
