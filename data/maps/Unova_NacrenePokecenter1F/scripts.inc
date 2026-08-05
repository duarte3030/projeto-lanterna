@ NacrenePokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NacrenePokecenter1F_MapScripts::
	.byte 0

Unova_NacrenePokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_NacrenePokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_NacrenePokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_NacrenePokecenter1F_Loja1:
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

Unova_NacrenePokecenter1F_EventScript_Npc2::
	msgbox Unova_NacrenePokecenter1F_Text_NacrenePokecenterSocialiteText, MSGBOX_NPC
	end

Unova_NacrenePokecenter1F_EventScript_Npc3::
	msgbox Unova_NacrenePokecenter1F_Text_NacreneJigglypuffText, MSGBOX_NPC
	end

Unova_NacrenePokecenter1F_EventScript_Npc4::
	msgbox Unova_NacrenePokecenter1F_Text_NacrenePokecenterBugCatcherText, MSGBOX_NPC
	end


Unova_NacrenePokecenter1F_Text_NacrenePokecenterSocialiteText::
	.string "The POKéMON with"
	.string "\nme right now are"
	.string "\pthe ones that, out"
	.string "\nof all those I've"
	.string "\pmet so far, I've"
	.string "\ntaken a particular"
	.string "\lshine to!$"

Unova_NacrenePokecenter1F_Text_NacreneJigglypuffText::
	.string "JIGGLYPUFF: Puu"
	.string "\npupuu.$"

Unova_NacrenePokecenter1F_Text_NacrenePokecenterBugCatcherText::
	.string "Most POKéMON get"
	.string "\ndrowsy if they"
	.string "\phear a JIGGLYPUFF"
	.string "\nsinging.$"
