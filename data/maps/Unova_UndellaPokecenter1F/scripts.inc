@ UndellaPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_UndellaPokecenter1F_MapScripts::
	.byte 0

Unova_UndellaPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_UndellaPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_UndellaPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_UndellaPokecenter1F_Loja1:
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

Unova_UndellaPokecenter1F_EventScript_Npc2::
	msgbox Unova_UndellaPokecenter1F_Text_UndellaPokecenterGentlemanText, MSGBOX_NPC
	end

Unova_UndellaPokecenter1F_EventScript_Npc3::
	msgbox Unova_UndellaPokecenter1F_Text_UndellaPokecenterFishingGuruText, MSGBOX_NPC
	end


Unova_UndellaPokecenter1F_Text_UndellaPokecenterGentlemanText::
	.string "Do you know how"
	.string "\nto fish?"
	.string "\pThere's a master"
	.string "\nwho lives in town."
	.string "\pI'm sure he could"
	.string "\nteach you.$"

Unova_UndellaPokecenter1F_Text_UndellaPokecenterFishingGuruText::
	.string "AMANITA's PC can"
	.string "\nstore up to 20"
	.string "\lPOKéMON per BOX.$"
