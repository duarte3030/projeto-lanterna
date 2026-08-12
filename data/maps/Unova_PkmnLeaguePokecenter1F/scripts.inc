@ PkmnLeaguePokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_PkmnLeaguePokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_PkmnLeaguePokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Unova (dev_scripts/heal_locations_unova.py).
Unova_PkmnLeaguePokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_UNOVA_PKMN_LEAGUE
	end

Unova_PkmnLeaguePokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_PkmnLeaguePokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_PkmnLeaguePokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_PkmnLeaguePokecenter1F_Loja1:
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

Unova_PkmnLeaguePokecenter1F_EventScript_Npc2::
	msgbox Unova_PkmnLeaguePokecenter1F_Text_PkmnLeaguePokecenterRangerMText, MSGBOX_NPC
	end

Unova_PkmnLeaguePokecenter1F_EventScript_Npc3::
	msgbox Unova_PkmnLeaguePokecenter1F_Text_PkmnLeaguePokecenterCooltrainerFText, MSGBOX_NPC
	end


Unova_PkmnLeaguePokecenter1F_Text_PkmnLeaguePokecenterRangerMText::
	.string "No matter how many"
	.string "\ntimes the ELITE"
	.string "\lFOUR defeat me…"
	.string "\pI'll keep moving"
	.string "\nforward with my"
	.string "\lPOKéMON!$"

Unova_PkmnLeaguePokecenter1F_Text_PkmnLeaguePokecenterCooltrainerFText::
	.string "Understand what"
	.string "\ntype of POKéMON"
	.string "\peach of the ELITE"
	.string "\nFOUR uses. That is"
	.string "\pa shortcut for"
	.string "\nvictory!$"
