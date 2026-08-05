@ CasteliaPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CasteliaPokecenter1F_MapScripts::
	.byte 0

Unova_CasteliaPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_CasteliaPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_CasteliaPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_CasteliaPokecenter1F_Loja1:
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

Unova_CasteliaPokecenter1F_EventScript_Npc2::
	msgbox Unova_CasteliaPokecenter1F_Text_CasteliaPokecenterRangerMText, MSGBOX_NPC
	end

Unova_CasteliaPokecenter1F_EventScript_Npc3::
	msgbox Unova_CasteliaPokecenter1F_Text_CasteliaPokecenterCooltrainerFText, MSGBOX_NPC
	end

Unova_CasteliaPokecenter1F_EventScript_Npc4::
	msgbox Unova_CasteliaPokecenter1F_Text_CasteliaPokecenterAudinoText, MSGBOX_NPC
	end

Unova_CasteliaPokecenter1F_EventScript_Npc5::
	msgbox Unova_CasteliaPokecenter1F_Text_CasteliaPokecenterPokefanMText, MSGBOX_NPC
	end


Unova_CasteliaPokecenter1F_Text_CasteliaPokecenterRangerMText::
	.string "The BATTLE COMPANY"
	.string "\nmakes all kinds of"
	.string "\pproducts for POKé-"
	.string "\nMON battling.$"

Unova_CasteliaPokecenter1F_Text_CasteliaPokecenterCooltrainerFText::
	.string "BURGH, the GYM"
	.string "\nLEADER, is soooo"
	.string "\lcool."
	.string "\pHis POKéMON are"
	.string "\nreally tough too.$"

Unova_CasteliaPokecenter1F_Text_CasteliaPokecenterAudinoText::
	.string "Audii!$"

Unova_CasteliaPokecenter1F_Text_CasteliaPokecenterPokefanMText::
	.string "NIMBASA CITY…"
	.string "\pStrange people in"
	.string "\nthe abandoned"
	.string "\lpark…"
	.string "\pSomething is going"
	.string "\non, I know it!$"
