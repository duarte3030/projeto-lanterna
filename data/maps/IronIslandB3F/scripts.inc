IronIslandB3F_MapScripts::
	.byte 0

@ BLOQUEADO (S7, 18/08/2026). A fonte (scripts_iron_island_b*.s) resolve a
@ plataforma inteira com dois specials, InitPersistedMapFeaturesForPlatform
@ Lift (OnTransition) e TriggerPlatformLift (o coord_event), nenhum dos dois
@ existe neste motor (`grep` em include/ e src/ confirma zero ocorrencias).
@ Nao e so o texto/movimento que falta: e a mecanica de plataforma
@ deslizante inteira (estado persistido entre visitas ao andar). "Specials
@ inexistentes descartados com comentario", sem substituto aqui. Volta ao
@ plano.
IronIslandB3F_EventScript_CoordEvent_PlatformLift::
	end

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
IronIslandB3F_EventScript_DexArceusSteel::
	lockall
	msgbox IronIslandB3F_Text_DexArceusSteelIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_STEEL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_STEEL, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_STEEL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IronIslandB3F_EventScript_DexArceusSteelSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IronIslandB3F_EventScript_DexArceusSteelSome
	releaseall
	end

IronIslandB3F_EventScript_DexArceusSteelSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_STEEL
	setflag FLAG_HIDE_DEX_ARCEUS_STEEL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IronIslandB3F_Text_DexArceusSteelIntro:
	.string "ARCEUS_STEEL appeared!$"

@ <<< Dex completa <<<
