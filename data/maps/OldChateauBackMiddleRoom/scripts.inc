OldChateauBackMiddleRoom_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
OldChateauBackMiddleRoom_EventScript_DexArceusGhost::
	lockall
	msgbox OldChateauBackMiddleRoom_Text_DexArceusGhostIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_GHOST, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_GHOST, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_GHOST
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, OldChateauBackMiddleRoom_EventScript_DexArceusGhostSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, OldChateauBackMiddleRoom_EventScript_DexArceusGhostSome
	releaseall
	end

OldChateauBackMiddleRoom_EventScript_DexArceusGhostSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_GHOST
	setflag FLAG_HIDE_DEX_ARCEUS_GHOST
	fadescreenswapbuffers FADE_FROM_BLACK
	return

OldChateauBackMiddleRoom_Text_DexArceusGhostIntro:
	.string "ARCEUS_GHOST appeared!$"

@ <<< Dex completa <<<
