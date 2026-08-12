VeilstoneStore1F_MapScripts::
	.byte 0

VeilstoneStore1F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore1F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore1F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore1F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore1F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore1F_EventScript_Npc1::
	msgbox VeilstoneStore1F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore1F_Text_Npc1:
	.string "I made an Accessory modeled after\nthe Pokémon of a Trainer I met.\pWould you like one?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneStore1F_EventScript_Npc4::
	msgbox VeilstoneStore1F_Text_Npc4, MSGBOX_NPC
	end

VeilstoneStore1F_Text_Npc4:
	.string "Welcome to the fabulous Veilstone\nDepartment Store.$"

VeilstoneStore1F_EventScript_Npc2::
	msgbox VeilstoneStore1F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneStore1F_Text_Npc2:
	.string "This department store knows how to\nensure customer satisfaction.\pThey really look after you once you\nbecome a regular customer.$"

VeilstoneStore1F_EventScript_Npc3::
	msgbox VeilstoneStore1F_Text_Npc3, MSGBOX_NPC
	end

VeilstoneStore1F_Text_Npc3:
	.string "I like the formal air of a luxury\ndepartment store.$"

VeilstoneStore1F_EventScript_Placa4::
	msgbox VeilstoneStore1F_Text_Placa4, MSGBOX_SIGN
	end

VeilstoneStore1F_Text_Placa4:
	.string "Discover a new you!\nVeilstone Department Store$"

VeilstoneStore1F_EventScript_Placa5::
	msgbox VeilstoneStore1F_Text_Placa5, MSGBOX_SIGN
	end

VeilstoneStore1F_Text_Placa5:
	.string "B1F: Food & Produce\p1F: Trainers' Zone\p2F: Battle Collection\p3F: TM Corner\p4F: Poké Dolls & Goods\p5F: Rooftop Plaza$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_VEILSTONE_1F_RIGHT), tabela de include/data/mart_items.h
VeilstoneStore1F_EventScript_Loja1::
	lock
	faceplayer
	msgbox VeilstoneStore1F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore1F_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore1F_Pokemart_Loja1:
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_REVIVE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARLYZ_HEAL
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_FULL_HEAL
	pokemartlistend

@ loja_especial do Platinum (MART_SPECIALTIES_ID_VEILSTONE_1F_LEFT), tabela de include/data/mart_items.h
VeilstoneStore1F_EventScript_Loja2::
	lock
	faceplayer
	msgbox VeilstoneStore1F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore1F_Pokemart_Loja2
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore1F_Pokemart_Loja2:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	pokemartlistend
