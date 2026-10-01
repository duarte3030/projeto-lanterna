@ HauntedWoods_Inner: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 27.115) por dev_scripts/copia_planta_ex.py.

HauntedWoods_Inner_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 27.115), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
HauntedWoods_Inner_EventScript_ExNpc1::
	msgbox HauntedWoods_Inner_Text_ExNpc1, MSGBOX_NPC
	end

HauntedWoods_Inner_Text_ExNpc1:
	.string "GHOST POKéMON gather here due to the\n"
	.string "strong emotions that fill this place.\p"
	.string "GHOSTs thrive on strong emotions.$"

HauntedWoods_Inner_EventScript_ExNpc2::
	msgbox HauntedWoods_Inner_Text_ExNpc2, MSGBOX_NPC
	end

HauntedWoods_Inner_Text_ExNpc2:
	.string "I come out here to clean the graves.\p"
	.string "Many of them are older than I am and\n"
	.string "have no one to care for them.\p"
	.string "I hope they will be cared for when I’m\n"
	.string "gone.$"

HauntedWoods_Inner_EventScript_ExNpc3::
	msgbox HauntedWoods_Inner_Text_ExNpc3, MSGBOX_NPC
	end

HauntedWoods_Inner_Text_ExNpc3:
	.string "SNIFF...\n"
	.string "I guess some things can’t last\l"
	.string "forever...$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
HauntedWoods_Inner_EventScript_DexMoltresGalar::
	lockall
	msgbox HauntedWoods_Inner_Text_DexMoltresGalarIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_MOLTRES_GALAR, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_MOLTRES_GALAR, 65
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_MOLTRES_GALAR
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, HauntedWoods_Inner_EventScript_DexMoltresGalarSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, HauntedWoods_Inner_EventScript_DexMoltresGalarSome
	releaseall
	end

HauntedWoods_Inner_EventScript_DexMoltresGalarSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_MOLTRES_GALAR
	setflag FLAG_HIDE_DEX_MOLTRES_GALAR
	fadescreenswapbuffers FADE_FROM_BLACK
	return

HauntedWoods_Inner_Text_DexMoltresGalarIntro:
	.string "MOLTRES_GALAR appeared!$"

@ <<< Dex completa <<<
