VeilstoneStore3F_MapScripts::
	.byte 0

VeilstoneStore3F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore3F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore3F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore3F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore3F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore3F_EventScript_Npc1::
	msgbox VeilstoneStore3F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore3F_Text_Npc1:
	.string "Hello.\nMay I help you with anything?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneStore3F_EventScript_Npc4::
	msgbox VeilstoneStore3F_Text_Npc4, MSGBOX_NPC
	end

VeilstoneStore3F_Text_Npc4:
	.string "A friend traded me a MACHOKE using\nDS Wireless Communications.\pBut instead of a MACHOKE, I got\na different Pokémon!$"

VeilstoneStore3F_EventScript_Npc2::
	msgbox VeilstoneStore3F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneStore3F_Text_Npc2:
	.string "I wrote some secrets in my Mail\nas a reminder...\pIf someone reads it...\nI'm in deep trouble.$"

VeilstoneStore3F_EventScript_Npc3::
	msgbox VeilstoneStore3F_Text_Npc3, MSGBOX_NPC
	end

VeilstoneStore3F_Text_Npc3:
	.string "I would love to buy up all the\nmerchandise here.\pEven once would do!$"

VeilstoneStore3F_EventScript_Placa4::
	msgbox VeilstoneStore3F_Text_Placa4, MSGBOX_SIGN
	end

VeilstoneStore3F_Text_Placa4:
	.string "B1F: Food & Produce\p1F: Trainers' Zone\p2F: Battle Collection\p3F: TM Corner\p4F: Poké Dolls & Goods\p5F: Rooftop Plaza$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_VEILSTONE_3F_UP), tabela de include/data/mart_items.h
VeilstoneStore3F_EventScript_Loja1::
	lock
	faceplayer
	msgbox VeilstoneStore3F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore3F_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore3F_Pokemart_Loja1:
	.2byte ITEM_TM_PROTECT
	.2byte ITEM_TM_SAFEGUARD
	.2byte ITEM_TM_REFLECT
	.2byte ITEM_TM_LIGHT_SCREEN
	pokemartlistend

@ loja_especial do Platinum (MART_SPECIALTIES_ID_VEILSTONE_3F_DOWN), tabela de include/data/mart_items.h
VeilstoneStore3F_EventScript_Loja2::
	lock
	faceplayer
	msgbox VeilstoneStore3F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore3F_Pokemart_Loja2
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore3F_Pokemart_Loja2:
	.2byte ITEM_TM_FIRE_BLAST
	.2byte ITEM_TM_THUNDER
	.2byte ITEM_TM_BLIZZARD
	.2byte ITEM_TM_SOLAR_BEAM
	.2byte ITEM_TM_HYPER_BEAM
	pokemartlistend
