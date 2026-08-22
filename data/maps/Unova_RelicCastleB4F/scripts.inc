@ RelicCastleB4F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_RelicCastleB4F_MapScripts::
	.byte 0

Unova_RelicCastleB4F_EventScript_Npc2::
	msgbox Unova_RelicCastleB4F_Text_LarvestaText, MSGBOX_NPC
	end


Unova_RelicCastleB4F_Text_LarvestaText::
	.string "Screee!$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ CoverFossilB4FScript do BW3G: o `disappear` de la vira a flag do
@ proprio objeto, que e o que esconde o sprite depois de pegar.
Unova_RelicCastleB4F_EventScript_CoverFossilB4F::
	lock
	giveitem ITEM_COVER_FOSSIL
	setflag FLAG_UNOVA_ITEM_COVERFOSSILB4F
	removeobject VAR_LAST_TALKED
	release
	end

@ PlumeFossilB4FScript do BW3G: o `disappear` de la vira a flag do
@ proprio objeto, que e o que esconde o sprite depois de pegar.
Unova_RelicCastleB4F_EventScript_PlumeFossilB4F::
	lock
	giveitem ITEM_PLUME_FOSSIL
	setflag FLAG_UNOVA_ITEM_PLUMEFOSSILB4F
	removeobject VAR_LAST_TALKED
	release
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Unova_RelicCastleB4F_EventScript_DexTerapagosNormal::
	lockall
	msgbox Unova_RelicCastleB4F_Text_DexTerapagosNormalIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_TERAPAGOS_NORMAL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_TERAPAGOS_NORMAL, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_TERAPAGOS_NORMAL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_RelicCastleB4F_EventScript_DexTerapagosNormalSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_RelicCastleB4F_EventScript_DexTerapagosNormalSome
	releaseall
	end

Unova_RelicCastleB4F_EventScript_DexTerapagosNormalSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_TERAPAGOS_NORMAL
	setflag FLAG_HIDE_DEX_TERAPAGOS_NORMAL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_RelicCastleB4F_Text_DexTerapagosNormalIntro:
	.string "TERAPAGOS_NORMAL appeared!$"

@ <<< Dex completa <<<
