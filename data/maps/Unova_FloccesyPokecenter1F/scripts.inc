@ FloccesyPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_FloccesyPokecenter1F_MapScripts::
	.byte 0

Unova_FloccesyPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_FloccesyPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_FloccesyPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_FloccesyPokecenter1F_Loja1:
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

Unova_FloccesyPokecenter1F_EventScript_Npc2::
	msgbox Unova_FloccesyPokecenter1F_Text_FloccesyPokecenterPokefanMText, MSGBOX_NPC
	end

Unova_FloccesyPokecenter1F_EventScript_Npc3::
	msgbox Unova_FloccesyPokecenter1F_Text_FloccesyPokecenterRangerMText, MSGBOX_NPC
	end

Unova_FloccesyPokecenter1F_EventScript_Npc4::
	msgbox Unova_FloccesyPokecenter1F_Text_FloccesyPokecenterRangerFText, MSGBOX_NPC
	end


Unova_FloccesyPokecenter1F_Text_FloccesyPokecenterPokefanMText::
	.string "What's this? TEAM"
	.string "\nPLASMA has come"
	.string "\lback?"
	.string "\pI saw some men in"
	.string "\nblack at VIRBANK"
	.string "\lCITY…$"

Unova_FloccesyPokecenter1F_Text_FloccesyPokecenterRangerMText::
	.string "I stop my POKéMON"
	.string "\nfrom evolving too"
	.string "\learly."
	.string "\pI make them learn"
	.string "\ncertain moves be-"
	.string "\lfore I let them"
	.string "\levolve.$"

Unova_FloccesyPokecenter1F_Text_FloccesyPokecenterRangerFText::
	.string "POKéMON do become"
	.string "\nstronger when they"
	.string "\pevolve, but they"
	.string "\nalso learn moves"
	.string "\lmore slowly.$"
