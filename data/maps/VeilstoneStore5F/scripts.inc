VeilstoneStore5F_MapScripts::
	.byte 0

VeilstoneStore5F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore5F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore5F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore5F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore5F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore5F_EventScript_Npc1::
	msgbox VeilstoneStore5F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore5F_Text_Npc1:
	.string "Ah, young Pokémon Trainer...\pAs your senior in life, let me make\na gift of this Sticky Barb!$"

VeilstoneStore5F_EventScript_Placa1::
	msgbox VeilstoneStore5F_Text_Placa1, MSGBOX_SIGN
	end

VeilstoneStore5F_Text_Placa1:
	.string "It's a Vending Machine.\nWhich drink would you like?$"

VeilstoneStore5F_EventScript_Placa2::
	msgbox VeilstoneStore5F_Text_Placa2, MSGBOX_SIGN
	end

VeilstoneStore5F_Text_Placa2:
	.string "It's a Vending Machine.\nWhich drink would you like?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneStore5F_EventScript_Npc4::
	msgbox VeilstoneStore5F_Text_Npc4, MSGBOX_NPC
	end

VeilstoneStore5F_Text_Npc4:
	.string "I've had enough of shopping for\na while.\pI'll grab a drink and unwind a bit.$"

VeilstoneStore5F_EventScript_Npc2::
	msgbox VeilstoneStore5F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneStore5F_Text_Npc2:
	.string "I've shopped here loyally for years.\nNow they consider me a regular! Ha!$"

VeilstoneStore5F_EventScript_Npc3::
	msgbox VeilstoneStore5F_Text_Npc3, MSGBOX_NPC
	end

VeilstoneStore5F_Text_Npc3:
	.string "Two buff guys standing side by side.\nThat's all. What? What's the problem?$"

VeilstoneStore5F_EventScript_Placa4::
	msgbox VeilstoneStore5F_Text_Placa4, MSGBOX_SIGN
	end

VeilstoneStore5F_Text_Placa4:
	.string "B1F: Food & Produce\p1F: Trainers' Zone\p2F: Battle Collection\p3F: TM Corner\p4F: Poké Dolls & Goods\p5F: Rooftop Plaza$"
