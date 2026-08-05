@ HumilauPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_HumilauPokecenter1F_MapScripts::
	.byte 0

Unova_HumilauPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_HumilauPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_HumilauPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_HumilauPokecenter1F_Loja1:
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

Unova_HumilauPokecenter1F_EventScript_Npc2::
	msgbox Unova_HumilauPokecenter1F_Text_HumilauPokecenterFisherText, MSGBOX_NPC
	end

Unova_HumilauPokecenter1F_EventScript_Npc3::
	msgbox Unova_HumilauPokecenter1F_Text_HumilauPokecenterGentlemanText, MSGBOX_NPC
	end

Unova_HumilauPokecenter1F_EventScript_Npc4::
	msgbox Unova_HumilauPokecenter1F_Text_HumilauPokecenterTeacherText, MSGBOX_NPC
	end


Unova_HumilauPokecenter1F_Text_HumilauPokecenterFisherText::
	.string "Alright! Here's"
	.string "\nsome advice from a"
	.string "\pguy who spends all"
	.string "\nof his time in"
	.string "\lPOKéMON CENTERs!"
	.string "\pWhen your POKéMON"
	.string "\nhave low HP, make"
	.string "\lsure to heal them!$"

Unova_HumilauPokecenter1F_Text_HumilauPokecenterGentlemanText::
	.string "That PC is free"
	.string "\nfor any trainer"
	.string "\lto use.$"

Unova_HumilauPokecenter1F_Text_HumilauPokecenterTeacherText::
	.string "It's so convenient"
	.string "\nhaving the MART"
	.string "\pbuilt into the"
	.string "\nPOKéMON CENTER."
	.string "\pIt's your one-stop"
	.string "\nshop for all"
	.string "\lthings POKéMON!$"
