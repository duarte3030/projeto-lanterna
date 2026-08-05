@ VictoryRoadPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VictoryRoadPokecenter1F_MapScripts::
	.byte 0

Unova_VictoryRoadPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_VictoryRoadPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_VictoryRoadPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_VictoryRoadPokecenter1F_Loja1:
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

Unova_VictoryRoadPokecenter1F_EventScript_Npc2::
	msgbox Unova_VictoryRoadPokecenter1F_Text_VictoryRoadPokecenterCooltrainerMText, MSGBOX_NPC
	end

Unova_VictoryRoadPokecenter1F_EventScript_Npc3::
	msgbox Unova_VictoryRoadPokecenter1F_Text_VictoryRoadPokecenterRangerFText, MSGBOX_NPC
	end


Unova_VictoryRoadPokecenter1F_Text_VictoryRoadPokecenterCooltrainerMText::
	.string "Thanks to my POKé-"
	.string "\nMON, I've collect-"
	.string "\led 8 GYM BADGEs!"
	.string "\pBut I'm too afraid"
	.string "\nto go further. I'm"
	.string "\pstuck at VICTORY"
	.string "\nROAD.$"

Unova_VictoryRoadPokecenter1F_Text_VictoryRoadPokecenterRangerFText::
	.string "First of all, go"
	.string "\nthrough this long"
	.string "\pand difficult"
	.string "\nVICTORY ROAD."
	.string "\pThen, defeat even"
	.string "\none of the ELITE"
	.string "\pFOUR. Increase"
	.string "\nwhat you can do"
	.string "\plittle by little,"
	.string "\nand get close to"
	.string "\lthe Champion!$"
