@ LcHollowCaveChamber: mapa copiado de Pokémon Liquid Crystal.gba (g2m104) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.
@
@ E a sala do fundo, com o piso de areia clara no meio. O unico tile de warp
@ dela, (7,14), volta para o degrau de onde se veio: uma porta, uma volta, que e
@ a regra 0 do valida_conectividade.py.

LcHollowCaveChamber_MapScripts::
	.byte 0

LcHollowCaveChamber_EventScript_SignFloor::
	msgbox LcHollowCaveChamber_Text_SignFloor, MSGBOX_SIGN
	end

LcHollowCaveChamber_Text_SignFloor:
	.string "The pale square in the middle is\n"
	.string "packed sand, not stone.\p"
	.string "Someone swept this room, and it\n"
	.string "was a long time ago.$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
LcHollowCaveChamber_EventScript_DexLunala::
	lockall
	msgbox LcHollowCaveChamber_Text_DexLunalaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_LUNALA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_LUNALA, 85
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_LUNALA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, LcHollowCaveChamber_EventScript_DexLunalaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, LcHollowCaveChamber_EventScript_DexLunalaSome
	releaseall
	end

LcHollowCaveChamber_EventScript_DexLunalaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_LUNALA
	setflag FLAG_HIDE_DEX_LUNALA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

LcHollowCaveChamber_Text_DexLunalaIntro:
	.string "LUNALA appeared!$"

@ <<< Dex completa <<<
