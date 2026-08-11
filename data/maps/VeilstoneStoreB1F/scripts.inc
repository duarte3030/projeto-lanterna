VeilstoneStoreB1F_MapScripts::
	.byte 0

VeilstoneStoreB1F_EventScript_Caixa::
	lock
	faceplayer
	msgbox VeilstoneStoreB1F_Text_Caixa, MSGBOX_DEFAULT
	pokemart VeilstoneStoreB1F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
VeilstoneStoreB1F_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

VeilstoneStoreB1F_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

VeilstoneStoreB1F_EventScript_Npc1::
	msgbox VeilstoneStoreB1F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc1:
	.string "Hello, there.\pWould you like some Lava Cookies?\nThey're $200 each.$"

VeilstoneStoreB1F_EventScript_Npc2::
	msgbox VeilstoneStoreB1F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc2:
	.string "Hello!\nI sell Poffins.\pThe ones I sell go for $6,400 each.\nWould you like one?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneStoreB1F_EventScript_Npc7::
	msgbox VeilstoneStoreB1F_Text_Npc7, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc7:
	.string "Welcome to the basement--the food and\nproduce section.\pWe offer a fine and pleasing selection\nof Pokémon food and treats.$"

VeilstoneStoreB1F_EventScript_Npc8::
	msgbox VeilstoneStoreB1F_Text_Npc8, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc8:
	.string "I'm hopeless at cooking Poffins, so I\nbuy them here.\pI wish I could feed my babies Poffins\nthat I made myself, though.$"

VeilstoneStoreB1F_EventScript_Npc3::
	msgbox VeilstoneStoreB1F_Text_Npc3, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc3:
	.string "Have you ever planted Berries, then\npromptly forgotten about them?\pIf that's you, we have Berries on sale,\ntoo.$"

VeilstoneStoreB1F_EventScript_Npc4::
	msgbox VeilstoneStoreB1F_Text_Npc4, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc4:
	.string "Hello!\nRage Candy Bars...\pI'm all sold out.\nI'm terribly sorry.$"

VeilstoneStoreB1F_EventScript_Npc5::
	msgbox VeilstoneStoreB1F_Text_Npc5, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc5:
	.string "Pay attention, please.\pThe flavors of Poffins affect the\ncondition of Pokémon.\pSpicy Poffins enhance coolness.\pDry Poffins enhance beauty.\pSweet Poffins enhance cuteness.\pBitter Poffins enhance smartness.\pAnd Sour Poffins enhance toughness.\pSigh...\nPoffins are wonderful, aren't they?$"

VeilstoneStoreB1F_EventScript_Npc6::
	msgbox VeilstoneStoreB1F_Text_Npc6, MSGBOX_NPC
	end

VeilstoneStoreB1F_Text_Npc6:
	.string "I didn't expect to find paradise in the\ndepartment store's basement.\pI got carried away and bought up all\nthe Rage Candy Bars!$"

VeilstoneStoreB1F_EventScript_Placa7::
	msgbox VeilstoneStoreB1F_Text_Placa7, MSGBOX_SIGN
	end

VeilstoneStoreB1F_Text_Placa7:
	.string "B1F: Food & Produce\p1F: Trainers' Zone\p2F: Battle Collection\p3F: TM Corner\p4F: Poké Dolls & Goods\p5F: Rooftop Plaza$"
