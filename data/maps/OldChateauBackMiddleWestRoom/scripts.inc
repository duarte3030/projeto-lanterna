OldChateauBackMiddleWestRoom_MapScripts::
	.byte 0

OldChateauBackMiddleWestRoom_EventScript_Placa1::
	msgbox OldChateauBackMiddleWestRoom_Text_Placa1, MSGBOX_SIGN
	end

OldChateauBackMiddleWestRoom_Text_Placa1:
	.string "Inside the TV...\nThere appears to be a Pokémon?...\pThe Pokémon appears as if it will come\nout. Want to thump the TV?$"

OldChateauBackMiddleWestRoom_EventScript_Placa2::
	msgbox OldChateauBackMiddleWestRoom_Text_Placa2, MSGBOX_SIGN
	end

OldChateauBackMiddleWestRoom_Text_Placa2:
	.string "Inside the TV...\nThere appears to be a Pokémon?...\pThe Pokémon appears as if it will come\nout. Want to thump the TV?$"

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
OldChateauBackMiddleWestRoom_EventScript_Rotom::
	lockall
	msgbox OldChateauBackMiddleWestRoom_Text_RotomIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ROTOM, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ROTOM, 20
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_OLD_CHATEAU_BACK_MIDDLE_WEST_ROOM_ROTOM
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, OldChateauBackMiddleWestRoom_EventScript_RotomSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, OldChateauBackMiddleWestRoom_EventScript_RotomPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
OldChateauBackMiddleWestRoom_EventScript_RotomPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_OLD_CHATEAU_BACK_MIDDLE_WEST_ROOM_ROTOM
	setflag FLAG_HIDE_ROTOM_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

OldChateauBackMiddleWestRoom_EventScript_RotomSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_OLD_CHATEAU_BACK_MIDDLE_WEST_ROOM_ROTOM
	setflag FLAG_HIDE_ROTOM_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox OldChateauBackMiddleWestRoom_Text_RotomSome, MSGBOX_DEFAULT
	return

OldChateauBackMiddleWestRoom_Text_RotomIntro:
	.string "Something inside the old room is\nstaring back...$"

OldChateauBackMiddleWestRoom_Text_RotomSome:
	.string "ROTOM disappeared into the TV set...$"

@ <<< Lendarios de Sinnoh <<<
