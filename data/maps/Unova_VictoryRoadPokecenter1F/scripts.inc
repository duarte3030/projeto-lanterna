@ VictoryRoadPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VictoryRoadPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_VictoryRoadPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Unova (dev_scripts/heal_locations_unova.py).
Unova_VictoryRoadPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_UNOVA_VICTORY_ROAD
	end

Unova_VictoryRoadPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_VictoryRoadPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_VictoryRoadPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_VictoryRoadPokecenter1F_Loja1:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_REPEL
	.2byte ITEM_ESCAPE_ROPE
	pokemartlistend

Unova_VictoryRoadPokecenter1F_EventScript_Npc2::
	msgbox Unova_VictoryRoadPokecenter1F_Text_VictoryRoadPokecenterCooltrainerMText, MSGBOX_NPC
	end

Unova_VictoryRoadPokecenter1F_EventScript_Npc3::
	msgbox Unova_VictoryRoadPokecenter1F_Text_VictoryRoadPokecenterRangerFText, MSGBOX_NPC
	end


Unova_VictoryRoadPokecenter1F_Text_VictoryRoadPokecenterCooltrainerMText::
	.string "Thanks to my POKé-"
	.string "\nMON, I've collect-"
	.string "\led 8 GYM BADGEs!"
	.string "\pBut I'm too afraid"
	.string "\nto go further. I'm"
	.string "\pstuck at VICTORY"
	.string "\nROAD.$"

Unova_VictoryRoadPokecenter1F_Text_VictoryRoadPokecenterRangerFText::
	.string "First of all, go"
	.string "\nthrough this long"
	.string "\pand difficult"
	.string "\nVICTORY ROAD."
	.string "\pThen, defeat even"
	.string "\none of the ELITE"
	.string "\pFOUR. Increase"
	.string "\nwhat you can do"
	.string "\plittle by little,"
	.string "\nand get close to"
	.string "\lthe Champion!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Unova_VictoryRoadPokecenter1F_EventScript_DexVictini::
	lockall
	msgbox Unova_VictoryRoadPokecenter1F_Text_DexVictiniIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_VICTINI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_VICTINI, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_VICTINI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_VictoryRoadPokecenter1F_EventScript_DexVictiniSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_VictoryRoadPokecenter1F_EventScript_DexVictiniSome
	releaseall
	end

Unova_VictoryRoadPokecenter1F_EventScript_DexVictiniSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_VICTINI
	setflag FLAG_HIDE_DEX_VICTINI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_VictoryRoadPokecenter1F_Text_DexVictiniIntro:
	.string "VICTINI appeared!$"

@ <<< Dex completa <<<
