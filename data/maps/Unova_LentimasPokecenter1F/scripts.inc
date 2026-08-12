@ LentimasPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_LentimasPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_LentimasPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Unova (dev_scripts/heal_locations_unova.py).
Unova_LentimasPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_UNOVA_LENTIMAS
	end

Unova_LentimasPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_LentimasPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_LentimasPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_LentimasPokecenter1F_Loja1:
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

Unova_LentimasPokecenter1F_EventScript_Npc2::
	msgbox Unova_LentimasPokecenter1F_Text_LentimasPokecenterGentlemanText, MSGBOX_NPC
	end

Unova_LentimasPokecenter1F_EventScript_Npc3::
	msgbox Unova_LentimasPokecenter1F_Text_LentimasPokecenterGrannyText, MSGBOX_NPC
	end

Unova_LentimasPokecenter1F_EventScript_Npc4::
	msgbox Unova_LentimasPokecenter1F_Text_LentimasPokecenterCooltrainerMText, MSGBOX_NPC
	end


Unova_LentimasPokecenter1F_Text_LentimasPokecenterGentlemanText::
	.string "Do your POKéMON"
	.string "\nknow HM moves?"
	.string "\pThose moves can"
	.string "\nbe used even if"
	.string "\pyour POKéMON has"
	.string "\nfainted.$"

Unova_LentimasPokecenter1F_Text_LentimasPokecenterGrannyText::
	.string "Strange things"
	.string "\nhappen outside"
	.string "\lof town."
	.string "\pBe careful.$"

Unova_LentimasPokecenter1F_Text_LentimasPokecenterCooltrainerMText::
	.string "I'm on a journey."
	.string "\nWhy?"
	.string "\pWell, do you rem-"
	.string "\nember exactly why"
	.string "\lyou're traveling?$"
