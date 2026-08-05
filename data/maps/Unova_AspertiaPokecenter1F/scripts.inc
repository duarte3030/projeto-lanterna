@ AspertiaPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_AspertiaPokecenter1F_MapScripts::
	.byte 0

Unova_AspertiaPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_AspertiaPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_AspertiaPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_AspertiaPokecenter1F_Loja1:
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

Unova_AspertiaPokecenter1F_EventScript_Npc2::
	msgbox Unova_AspertiaPokecenter1F_Text_AspertiaPokecenterRangerFText, MSGBOX_NPC
	end

Unova_AspertiaPokecenter1F_EventScript_Npc3::
	msgbox Unova_AspertiaPokecenter1F_Text_AspertiaPokecenterTeacherText, MSGBOX_NPC
	end

Unova_AspertiaPokecenter1F_EventScript_Npc4::
	msgbox Unova_AspertiaPokecenter1F_Text_AspertiaPokecenterCooltrainerFText, MSGBOX_NPC
	end


Unova_AspertiaPokecenter1F_Text_AspertiaPokecenterRangerFText::
	.string "Some POKéMON will"
	.string "\nevolve if you"
	.string "\ltreat them well."
	.string "\pMy YANMA was very"
	.string "\nhappy, and all of"
	.string "\la sudden, it"
	.string "\levolved!$"

Unova_AspertiaPokecenter1F_Text_AspertiaPokecenterTeacherText::
	.string "There's a POKéMON"
	.string "\ncalled EEVEE that"
	.string "\pcan evolve into"
	.string "\nmany different"
	.string "\lPOKéMON!$"

Unova_AspertiaPokecenter1F_Text_AspertiaPokecenterCooltrainerFText::
	.string "Do any of your"
	.string "\nPOKéMON know the"
	.string "\pmove for carrying"
	.string "\npeople on water?"
	.string "\pIt's very useful!$"
