@ PetalburgWoods_River: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 27.119) por dev_scripts/copia_planta_ex.py.

PetalburgWoods_River_MapScripts::
	.byte 0

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
PetalburgWoods_River_EventScript_DexOgerponTealTera::
	lockall
	msgbox PetalburgWoods_River_Text_DexOgerponTealTeraIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_OGERPON_TEAL_TERA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_OGERPON_TEAL_TERA, 55
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_OGERPON_TEAL_TERA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, PetalburgWoods_River_EventScript_DexOgerponTealTeraSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, PetalburgWoods_River_EventScript_DexOgerponTealTeraSome
	releaseall
	end

PetalburgWoods_River_EventScript_DexOgerponTealTeraSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_OGERPON_TEAL_TERA
	setflag FLAG_HIDE_DEX_OGERPON_TEAL_TERA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

PetalburgWoods_River_Text_DexOgerponTealTeraIntro:
	.string "OGERPON_TEAL_TERA appeared!$"

@ <<< Dex completa <<<
