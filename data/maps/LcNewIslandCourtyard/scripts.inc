@ LcNewIslandCourtyard: mapa copiado de Pokémon Liquid Crystal.gba (g4m34) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO e nosso.
@
@ Aqui fica o MEW estatico da New Island (resposta 74a do Gui). O molde e o do
@ MEWTWO da CeruleanCave_B1F_Frlg, nao um mecanismo novo: ON_TRANSITION mostra o
@ objeto enquanto a flag de ja enfrentado estiver apagada, ON_RESUME apaga o
@ objeto quando a batalha terminou em CAPTURADO, e o fim do script acende a flag
@ de ja enfrentado. Derrotado ou capturado, o MEW nao volta; se o jogador FUGIR,
@ ele foge tambem e pode ser reencontrado, que e o comportamento do jogo de
@ fabrica para lendario.

LcNewIslandCourtyard_MapScripts::
	map_script MAP_SCRIPT_ON_RESUME, LcNewIslandCourtyard_OnResume
	map_script MAP_SCRIPT_ON_TRANSITION, LcNewIslandCourtyard_OnTransition
	.byte 0

LcNewIslandCourtyard_OnResume::
	call_if_set FLAG_SYS_CTRL_OBJ_DELETE, LcNewIslandCourtyard_EventScript_TryRemoveMew
	end

LcNewIslandCourtyard_EventScript_TryRemoveMew::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, Common_EventScript_NopReturn
	removeobject VAR_LAST_TALKED
	return

LcNewIslandCourtyard_OnTransition::
	call_if_unset FLAG_FOUGHT_KANTO_LC_NEW_ISLAND_MEW, LcNewIslandCourtyard_EventScript_ShowMew
	end

LcNewIslandCourtyard_EventScript_ShowMew::
	clearflag FLAG_HIDE_KANTO_LC_NEW_ISLAND_MEW
	return

LcNewIslandCourtyard_EventScript_Mew::
	lock
	faceplayer
	waitse
	playmoncry SPECIES_MEW, CRY_MODE_ENCOUNTER
	message LcNewIslandCourtyard_Text_Mew
	waitmessage
	waitmoncry
	delay 20
	playbgm MUS_RG_ENCOUNTER_DEOXYS, 0
	waitbuttonpress
	setwildbattle SPECIES_MEW, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, LcNewIslandCourtyard_EventScript_DefeatedMew
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, LcNewIslandCourtyard_EventScript_RanFromMew
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, LcNewIslandCourtyard_EventScript_RanFromMew
	setflag FLAG_FOUGHT_KANTO_LC_NEW_ISLAND_MEW
	release
	end

LcNewIslandCourtyard_EventScript_DefeatedMew::
	setflag FLAG_FOUGHT_KANTO_LC_NEW_ISLAND_MEW
	goto EventScript_RemoveStaticMon
	end

LcNewIslandCourtyard_EventScript_RanFromMew::
	setvar VAR_0x8004, SPECIES_MEW
	goto EventScript_MonFlewAway
	end

LcNewIslandCourtyard_EventScript_SignCourtyard::
	msgbox LcNewIslandCourtyard_Text_SignCourtyard, MSGBOX_SIGN
	end

LcNewIslandCourtyard_Text_Mew:
	.string "Mew!$"

LcNewIslandCourtyard_Text_SignCourtyard:
	.string "INNER COURT\n"
	.string "The garden was here before the\l"
	.string "walls were. Walk softly.$"
