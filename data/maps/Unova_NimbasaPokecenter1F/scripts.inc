@ NimbasaPokecenter1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaPokecenter1F_MapScripts::
	.byte 0

Unova_NimbasaPokecenter1F_EventScript_Npc0::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

Unova_NimbasaPokecenter1F_EventScript_Npc1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_NimbasaPokecenter1F_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_NimbasaPokecenter1F_Loja1:
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

Unova_NimbasaPokecenter1F_EventScript_Npc2::
	msgbox Unova_NimbasaPokecenter1F_Text_NimbasaPokecenterGrampsText, MSGBOX_NPC
	end

Unova_NimbasaPokecenter1F_EventScript_Npc3::
	msgbox Unova_NimbasaPokecenter1F_Text_NimbasaPokecenterLassText, MSGBOX_NPC
	end

Unova_NimbasaPokecenter1F_EventScript_Npc4::
	msgbox Unova_NimbasaPokecenter1F_Text_NimbasaPokecenterTrubbishText, MSGBOX_NPC
	end


Unova_NimbasaPokecenter1F_Text_NimbasaPokecenterGrampsText::
	.string "Have you found"
	.string "\nany colored shards"
	.string "\paround? I hear"
	.string "\nthere's a place in"
	.string "\pDRIFTVEIL CITY"
	.string "\nwhere you can"
	.string "\ptrade them in for"
	.string "\nsomething good.$"

Unova_NimbasaPokecenter1F_Text_NimbasaPokecenterLassText::
	.string "This is my POKé-"
	.string "\nMON, TRUBBISH!"
	.string "\pI caught it in"
	.string "\nROUTE 16."
	.string "\pIt may be trash,"
	.string "\nbut it's my"
	.string "\lspecial trash!$"

Unova_NimbasaPokecenter1F_Text_NimbasaPokecenterTrubbishText::
	.string "Truuub.$"
