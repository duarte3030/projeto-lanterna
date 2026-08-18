@ Casa do jogador em Twinleaf, terreo. Falas do Platinum,
@ res/text/twinleaf_town_player_house_1f.json.

TwinleafTown_MainHouse_1F_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, TwinleafTown_MainHouse_1F_OnFrame
	.byte 0

@ O DEGRAU QUE FALTAVA da maquina de VAR_SINNOH_CASA_JOGADOR_ESTADO. O
@ coord_event da porta pede o valor 1, e ate 18/08/2026 ninguem escrevia 1
@ nesta var em lugar nenhum da arvore (o unico setvar era o 2 da propria
@ cena), entao o lembrete da mae era inalcancavel. Na fonte quem grava o 1 e
@ TwinleafTownPlayerHouse1F_OnFrame_RivalAlreadyLeft
@ (res/field/scripts/scripts_twinleaf_town_player_house_1f.s:47), disparado
@ pelo InitScript do mapa quando VAR_PLAYER_HOUSE_STATE vale 0
@ (scripts_init_twinleaf_town_player_house_1f.s:9, "estado 0 -> script 2").
@ Progressao literal da fonte, decisao 2 do plano: 0 (jogo novo) -> 1 (a mae
@ avisa que o rival ja saiu) -> 2 (lembrete na porta).
@
@ ponytail: na fonte a mae LEVANTA do sofa e anda ate o jogador (WalkNormal
@ North, East 3, North 3) e volta. Aqui ela so se vira e chama, sem rota: o
@ jogador entra por tres warps diferentes ((2,8), (1,8) e a escada em (8,2)),
@ e uma rota fixa contra o map.bin de 11x9 so seria fiel para uma das tres
@ entradas. Mesmo batimento narrativo, sem waitmovement travado por colisao.
TwinleafTown_MainHouse_1F_OnFrame:
	map_script_2 VAR_SINNOH_CASA_JOGADOR_ESTADO, 0, TwinleafTown_MainHouse_1F_EventScript_OnFrame_RivalAlreadyLeft
	.2byte 0

TwinleafTown_MainHouse_1F_EventScript_OnFrame_RivalAlreadyLeft::
	lockall
	applymovement LOCALID_TWINLEAF_MAIN_HOUSE_1F_MOM, TwinleafTown_MainHouse_1F_Movement_MomCallsPlayer
	waitmovement 0
	msgbox TwinleafTown_MainHouse_1F_Text_RivalAlreadyLeft, MSGBOX_DEFAULT
	setvar VAR_SINNOH_CASA_JOGADOR_ESTADO, 1
	releaseall
	end

	.balign 4, 0
TwinleafTown_MainHouse_1F_Movement_MomCallsPlayer:
	emote_exclamation_mark
	walk_in_place_down
	step_end

TwinleafTown_MainHouse_1F_Text_RivalAlreadyLeft:
	.string "MOM: {PLAYER}!\p"
	.string "{RIVAL} already left.\p"
	.string "I don't know what it was about, but\n"
	.string "he sure was in a hurry!$"

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ Fonte: TwinleafTownPlayerHouse1F_CoordEvent_DontGoIntoTallGrass. Lembrete da
@ mae na porta, depois que ela ja deu o tenis (o mesmo aviso resumido).
@ BLOQUEADO (nao escrito): o grupo hidden_flag FLAG_HIDE_TWINLEAF_TOWN_PLAYER_
@ HOUSE_1F_RIVAL_MOM (mae do rival visitando) so aparece na fonte depois de
@ VAR_PLAYER_HOUSE_STATE chegar a 3, setado em
@ Route201_EndChooseStarterSequenceAndWarpHome; toda a cadeia de Route201 que
@ levaria a esse estado usa VAR_FOLLOWER_RIVAL_STATE, descartada pela decisao
@ 3 do plano (mecanismo de seguidor nao existe aqui). Sem um novo caminho ate
@ esse estado, plantar o objeto deixaria a flag ligada para sempre sem cena
@ que a limpe. Reportado no plano, nao inventado aqui.
TwinleafTown_MainHouse_1F_EventScript_CoordEvent_DontGoIntoTallGrass::
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, TwinleafTown_MainHouse_1F_Movement_PlayerFaceMom
	applymovement LOCALID_TWINLEAF_MAIN_HOUSE_1F_MOM, TwinleafTown_MainHouse_1F_Movement_MomFacePlayer
	waitmovement 0
	setvar VAR_SINNOH_CASA_JOGADOR_ESTADO, 2
	msgbox TwinleafTown_MainHouse_1F_Text_DontGoIntoTallGrassReminder, MSGBOX_DEFAULT
	releaseall
	end

	.balign 4, 0
TwinleafTown_MainHouse_1F_Movement_PlayerFaceMom:
	delay_8
	walk_in_place_up
	step_end

	.balign 4, 0
TwinleafTown_MainHouse_1F_Movement_MomFacePlayer:
	walk_in_place_down
	step_end

TwinleafTown_MainHouse_1F_Text_DontGoIntoTallGrassReminder:
	.string "MOM: Oh, yes!\n"
	.string "{PLAYER}!\p"
	.string "Don't go into the tall grass.\n"
	.string "Wild POKéMON might attack you.\p"
	.string "It would be OK if you had your own\n"
	.string "POKéMON, but you don't, so...\p"
	.string "Well, take care, sweetie!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

TwinleafTown_MainHouse_1F_EventScript_Mom::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEMON_GET, TwinleafTown_MainHouse_1F_EventScript_MomAfter
	goto_if_set FLAG_SYS_B_DASH, TwinleafTown_MainHouse_1F_EventScript_MomReminder
	msgbox TwinleafTown_MainHouse_1F_Text_MomPutTheseOn, MSGBOX_DEFAULT
	setflag FLAG_SYS_B_DASH
	message TwinleafTown_MainHouse_1F_Text_ReceivedRunningShoes
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox TwinleafTown_MainHouse_1F_Text_MomDontGoIntoTallGrass, MSGBOX_DEFAULT
	release
	end

TwinleafTown_MainHouse_1F_EventScript_MomReminder::
	msgbox TwinleafTown_MainHouse_1F_Text_MomIsntRivalWaiting, MSGBOX_DEFAULT
	release
	end

TwinleafTown_MainHouse_1F_EventScript_MomAfter::
	msgbox TwinleafTown_MainHouse_1F_Text_MomTakeAQuickRest, MSGBOX_DEFAULT
	release
	end

TwinleafTown_MainHouse_1F_Text_MomPutTheseOn:
	.string "MOM: Oh, I know!\n"
	.string "{PLAYER}, put these on.$"

TwinleafTown_MainHouse_1F_Text_ReceivedRunningShoes:
	.string "{PLAYER} received a pair of\n"
	.string "RUNNING SHOES!$"

TwinleafTown_MainHouse_1F_Text_MomDontGoIntoTallGrass:
	.string "MOM: Going to SANDGEM TOWN is like\n"
	.string "an adventure in itself, right?\p"
	.string "With those RUNNING SHOES, you can\n"
	.string "get to faraway places much faster.\p"
	.string "“Press the B Button and dash about\n"
	.string "faster than ever before!”\p"
	.string "Oh, yes! {PLAYER}!\p"
	.string "Don't go into the tall grass.\n"
	.string "Wild POKéMON might attack you.\p"
	.string "It would be OK if you had your own\n"
	.string "POKéMON, but you don't, so...\p"
	.string "Well, take care, sweetie!$"

TwinleafTown_MainHouse_1F_Text_MomIsntRivalWaiting:
	.string "MOM: What is it, dear?\n"
	.string "Isn't your friend waiting for you?$"

TwinleafTown_MainHouse_1F_Text_MomTakeAQuickRest:
	.string "MOM: Welcome home, {PLAYER}.\n"
	.string "Are you and your POKéMON healthy?\p"
	.string "Take a quick rest, dear.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TwinleafTown_MainHouse_1F_EventScript_Placa1::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa1, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa1:
	.string "Mom's favorite dessert is in\nthe refrigerator.$"

TwinleafTown_MainHouse_1F_EventScript_Placa2::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa2, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa2:
	.string "Mom's kitchen is spotless!\nYou can see your face on the floor!$"

TwinleafTown_MainHouse_1F_EventScript_Placa3::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa3, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa3:
	.string "Mom's kitchen is spotless!\nYou can see your face on the floor!$"

TwinleafTown_MainHouse_1F_EventScript_Placa4::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa4, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa4:
	.string "This is where Mom does all her\ndelicious cooking.$"

TwinleafTown_MainHouse_1F_EventScript_Placa5::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa5, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa5:
	.string "This is where Mom does all her\ndelicious cooking.$"

TwinleafTown_MainHouse_1F_EventScript_Placa6::
	msgbox TwinleafTown_MainHouse_1F_Text_Placa6, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_1F_Text_Placa6:
	.string "This is where Mom does all her\ndelicious cooking.$"
