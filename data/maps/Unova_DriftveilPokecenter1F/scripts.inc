@ DriftveilPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_DriftveilPokecenter1F_MapScripts::
	.byte 0

Unova_DriftveilPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_DriftveilPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_DriftveilPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_DriftveilPokecenter1F_Loja1:
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

Unova_DriftveilPokecenter1F_EventScript_Npc2::
	msgbox Unova_DriftveilPokecenter1F_Text_DriftveilPokecenterFisherText, MSGBOX_NPC
	end

Unova_DriftveilPokecenter1F_EventScript_Npc3::
	msgbox Unova_DriftveilPokecenter1F_Text_DriftveilPokecenterYoungsterText, MSGBOX_NPC
	end

Unova_DriftveilPokecenter1F_EventScript_Npc4::
	msgbox Unova_DriftveilPokecenter1F_Text_DriftveilPokecenterCooltrainerFText, MSGBOX_NPC
	end


Unova_DriftveilPokecenter1F_Text_DriftveilPokecenterFisherText::
	.string "I just happened to"
	.string "\ncome through RELIC"
	.string "\lPASSAGE. Seems"
	.string "\pthere's some kind"
	.string "\nof commotion with"
	.string "\lthe police here.$"

Unova_DriftveilPokecenter1F_Text_DriftveilPokecenterYoungsterText::
	.string "The marketplace,"
	.string "\nthe POKéMON WORLD"
	.string "\pTOURNAMENT, the"
	.string "\nSTONE EMPOREUM,"
	.string "\pthey're the places"
	.string "\nto see in"
	.string "\lDRIFTVEIL CITY.$"

Unova_DriftveilPokecenter1F_Text_DriftveilPokecenterCooltrainerFText::
	.string "There's a shelter"
	.string "\nfor POKéMON here"
	.string "\pin town, run by"
	.string "\nformer members of"
	.string "\lTEAM PLASMA.$"
