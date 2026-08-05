@ OpelucidPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_OpelucidPokecenter1F_MapScripts::
	.byte 0

Unova_OpelucidPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_OpelucidPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_OpelucidPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_OpelucidPokecenter1F_Loja1:
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

Unova_OpelucidPokecenter1F_EventScript_Npc2::
	msgbox Unova_OpelucidPokecenter1F_Text_OpelucidPokecenterMusicianText, MSGBOX_NPC
	end

Unova_OpelucidPokecenter1F_EventScript_Npc3::
	msgbox Unova_OpelucidPokecenter1F_Text_OpelucidPokecenterCooltrainerFText, MSGBOX_NPC
	end

Unova_OpelucidPokecenter1F_EventScript_Npc4::
	msgbox Unova_OpelucidPokecenter1F_Text_OpelucidPokecenterFisherText, MSGBOX_NPC
	end


Unova_OpelucidPokecenter1F_Text_OpelucidPokecenterMusicianText::
	.string "TEAM PLASMA once"
	.string "\ntried to take over"
	.string "\lour city."
	.string "\pThey were beaten"
	.string "\nby our GYM LEADER,"
	.string "\lDRAYDEN!$"

Unova_OpelucidPokecenter1F_Text_OpelucidPokecenterCooltrainerFText::
	.string "DRAYDEN is strong,"
	.string "\nbut his grand-"
	.string "\ldaughter, IRIS,"
	.string "\pwas the POKéMON"
	.string "\nLEAGUE champion!$"

Unova_OpelucidPokecenter1F_Text_OpelucidPokecenterFisherText::
	.string "I was hoping to"
	.string "\nbuy some supplies"
	.string "\pto climb ROUTE 10,"
	.string "\nbut it's closed…$"
