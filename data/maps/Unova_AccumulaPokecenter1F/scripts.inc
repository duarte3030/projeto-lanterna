@ AccumulaPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_AccumulaPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_AccumulaPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Unova (dev_scripts/heal_locations_unova.py).
Unova_AccumulaPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_UNOVA_ACCUMULA
	end

Unova_AccumulaPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_AccumulaPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_AccumulaPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_AccumulaPokecenter1F_Loja1:
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

Unova_AccumulaPokecenter1F_EventScript_Npc2::
	msgbox Unova_AccumulaPokecenter1F_Text_AccumulaPokecenterPharmacistText, MSGBOX_NPC
	end

Unova_AccumulaPokecenter1F_EventScript_Npc3::
	msgbox Unova_AccumulaPokecenter1F_Text_AccumulaPokecenterCooltrainerFText, MSGBOX_NPC
	end


Unova_AccumulaPokecenter1F_Text_AccumulaPokecenterPharmacistText::
	.string "TEAM PLASMA came"
	.string "\nto town years ago."
	.string "\pThey tried to"
	.string "\nconvince the"
	.string "\ltownspeople to"
	.string "\pgive up their"
	.string "\nPOKéMON!$"

Unova_AccumulaPokecenter1F_Text_AccumulaPokecenterCooltrainerFText::
	.string "The GYM over in"
	.string "\nSTRIATON CITY"
	.string "\preopened just"
	.string "\nrecently."
	.string "\pCILAN is a master"
	.string "\nof grass POKéMON."
	.string "\pHe'll make you"
	.string "\npay if you don't"
	.string "\lwatch yourself.$"
