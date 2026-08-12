VeilstoneStore2F_MapScripts::
	.byte 0

VeilstoneStore2F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStore2F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore2F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore2F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStore2F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStore2F_EventScript_Npc1::
	msgbox VeilstoneStore2F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStore2F_Text_Npc1:
	.string "We're giving away a Pokétch app for\nfree as a promotion.\pI can give you the Counter app\nover the counter. Would you like it?$"

VeilstoneStore2F_EventScript_Npc2::
	msgbox VeilstoneStore2F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneStore2F_Text_Npc2:
	.string "Hello.\nMay I help you with anything?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneStore2F_EventScript_Npc4::
	msgbox VeilstoneStore2F_Text_Npc4, MSGBOX_NPC
	end

VeilstoneStore2F_Text_Npc4:
	.string "Where can I find matching dresses for\nmyself and my dear Pokémon?$"

VeilstoneStore2F_EventScript_Npc5::
	msgbox VeilstoneStore2F_Text_Npc5, MSGBOX_NPC
	end

VeilstoneStore2F_Text_Npc5:
	.string "I'm going to give an HP Up to\nmy KRICKETOT.\pThis is going to raise its HP, huh?$"

VeilstoneStore2F_EventScript_Npc3::
	msgbox VeilstoneStore2F_Text_Npc3, MSGBOX_NPC
	end

VeilstoneStore2F_Text_Npc3:
	.string "I'm getting the Carbos!\nI should get a Protein instead, maybe.\pBut Iron's not bad, either.$"

VeilstoneStore2F_EventScript_Placa4::
	msgbox VeilstoneStore2F_Text_Placa4, MSGBOX_SIGN
	end

VeilstoneStore2F_Text_Placa4:
	.string "B1F: Food & Produce\p1F: Trainers' Zone\p2F: Battle Collection\p3F: TM Corner\p4F: Poké Dolls & Goods\p5F: Rooftop Plaza$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

@ loja_especial do Platinum (MART_SPECIALTIES_ID_VEILSTONE_2F_UP), tabela de include/data/mart_items.h
VeilstoneStore2F_EventScript_Loja1::
	lock
	faceplayer
	msgbox VeilstoneStore2F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore2F_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore2F_Pokemart_Loja1:
	.2byte ITEM_X_SPEED
	.2byte ITEM_X_ATTACK
	.2byte ITEM_X_DEFENSE
	.2byte ITEM_GUARD_SPEC
	.2byte ITEM_DIRE_HIT
	.2byte ITEM_X_ACCURACY
	.2byte ITEM_X_SPECIAL
	.2byte ITEM_X_SP_DEF
	pokemartlistend

@ loja_especial do Platinum (MART_SPECIALTIES_ID_VEILSTONE_2F_MID), tabela de include/data/mart_items.h
VeilstoneStore2F_EventScript_Loja2::
	lock
	faceplayer
	msgbox VeilstoneStore2F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStore2F_Pokemart_Loja2
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStore2F_Pokemart_Loja2:
	.2byte ITEM_PROTEIN
	.2byte ITEM_IRON
	.2byte ITEM_CALCIUM
	.2byte ITEM_ZINC
	.2byte ITEM_CARBOS
	.2byte ITEM_HP_UP
	pokemartlistend
