@ StriatonPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_StriatonPokecenter1F_MapScripts::
	.byte 0

Unova_StriatonPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_StriatonPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_StriatonPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_StriatonPokecenter1F_Loja1:
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

Unova_StriatonPokecenter1F_EventScript_Npc2::
	msgbox Unova_StriatonPokecenter1F_Text_StriatonPokecenterRangerFText, MSGBOX_NPC
	end

Unova_StriatonPokecenter1F_EventScript_Npc3::
	msgbox Unova_StriatonPokecenter1F_Text_StriatonPokecenterGymGuyText, MSGBOX_NPC
	end

Unova_StriatonPokecenter1F_EventScript_Npc4::
	msgbox Unova_StriatonPokecenter1F_Text_StriatonPokecenterBuenaText, MSGBOX_NPC
	end


Unova_StriatonPokecenter1F_Text_StriatonPokecenterRangerFText::
	.string "Are you catching"
	.string "\nlots of POKéMON?"
	.string "\pHaving a lot of"
	.string "\nPOKéMON makes"
	.string "\plooking at the"
	.string "\nPOKéDEX or the PC"
	.string "\lBOX so much fun!$"

Unova_StriatonPokecenter1F_Text_StriatonPokecenterGymGuyText::
	.string "Have you heard?"
	.string "\nThe GYM here in"
	.string "\ptown was re-opened"
	.string "\nrecently!$"

Unova_StriatonPokecenter1F_Text_StriatonPokecenterBuenaText::
	.string "TEAM PLASMA is no"
	.string "\nlonger in UNOVA."
	.string "\pAt least, they're"
	.string "\nsupposed to have"
	.string "\lgone away.$"
