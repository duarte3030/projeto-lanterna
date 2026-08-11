VeilstoneStore4F_MapScripts::
	.byte 0

VeilstoneStore4F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore4F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore4F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore4F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore4F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore4F_EventScript_Npc1::
	msgbox VeilstoneStore4F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore4F_Text_Npc1:
	.string "Hello.\nMay I help you with anything?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneStore4F_EventScript_Npc1::
	msgbox VeilstoneStore4F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore4F_Text_Npc1:
	.string "If you encounter a wild Pokémon,\nchuck a Quick Ball right off the bat!\pIf it's taking a long time to catch,\nthe situation calls for a Timer Ball!$"

VeilstoneStore4F_EventScript_Npc2::
	msgbox VeilstoneStore4F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneStore4F_Text_Npc2:
	.string "That boy doesn't have any Pokémon,\nbut he says he's training his image!$"

VeilstoneStore4F_EventScript_Npc3::
	msgbox VeilstoneStore4F_Text_Npc3, MSGBOX_NPC
	end

VeilstoneStore4F_Text_Npc3:
	.string "We need another copy of the game so I\ncan challenge my papa!$"

VeilstoneStore4F_EventScript_Placa4::
	msgbox VeilstoneStore4F_Text_Placa4, MSGBOX_SIGN
	end

VeilstoneStore4F_Text_Placa4:
	.string "B1F: Food & Produce\p1F: Trainers' Zone\p2F: Battle Collection\p3F: TM Corner\p4F: Poké Dolls & Goods\p5F: Rooftop Plaza$"
