@ ShoppingMallNine do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_ShoppingMallNine_MapScripts::
	.byte 0

Unova_ShoppingMallNine_EventScript_Placa0::
	msgbox Unova_ShoppingMallNine_Text_MallVendingText, MSGBOX_SIGN
	end

Unova_ShoppingMallNine_EventScript_Placa1::
	msgbox Unova_ShoppingMallNine_Text_MallVendingText, MSGBOX_SIGN
	end

Unova_ShoppingMallNine_EventScript_Npc5::
	msgbox Unova_ShoppingMallNine_Text_MallReceptionistText, MSGBOX_NPC
	end

Unova_ShoppingMallNine_EventScript_Npc6::
	msgbox Unova_ShoppingMallNine_Text_MallBlockerText, MSGBOX_NPC
	end

Unova_ShoppingMallNine_EventScript_Npc7::
	msgbox Unova_ShoppingMallNine_Text_MallTeacherText, MSGBOX_NPC
	end

Unova_ShoppingMallNine_EventScript_Npc8::
	msgbox Unova_ShoppingMallNine_Text_MallCooltrainerMText, MSGBOX_NPC
	end

Unova_ShoppingMallNine_EventScript_Npc9::
	msgbox Unova_ShoppingMallNine_Text_MallCooltrainerFText, MSGBOX_NPC
	end

Unova_ShoppingMallNine_EventScript_Npc10::
	msgbox Unova_ShoppingMallNine_Text_MallYoungsterText, MSGBOX_NPC
	end

Unova_ShoppingMallNine_EventScript_Npc11::
	msgbox Unova_ShoppingMallNine_Text_MallBugCatcherText, MSGBOX_NPC
	end

Unova_ShoppingMallNine_EventScript_Npc12::
	msgbox Unova_ShoppingMallNine_Text_MallBuenaText, MSGBOX_NPC
	end


Unova_ShoppingMallNine_Text_MallVendingText::
	.string "A vending machine!"
	.string "\nHere's the menu.$"

Unova_ShoppingMallNine_Text_MallReceptionistText::
	.string "Hi, welcome to"
	.string "\nSHOPPING MALL"
	.string "\lNINE!"
	.string "\pGeneral wares are"
	.string "\non the 1st level."
	.string "\pPOKéBALLs and TMs"
	.string "\nare on the 2nd"
	.string "\llevel."
	.string "\pSupplements and"
	.string "\nstones can be"
	.string "\lpurchased on the"
	.string "\l3rd level."
	.string "\pPlease enjoy your"
	.string "\nstay!$"

Unova_ShoppingMallNine_Text_MallBlockerText::
	.string "Beyond this door"
	.string "\nis the exclusive"
	.string "\lMember's Room."
	.string "\pOnly verified"
	.string "\nmembers are"
	.string "\lpermitted to"
	.string "\lenter.$"

Unova_ShoppingMallNine_Text_MallTeacherText::
	.string "My LAMPENT's not"
	.string "\nvery good at POKé-"
	.string "\lMON battles,"
	.string "\pbut it's great at"
	.string "\nmaking toast!$"

Unova_ShoppingMallNine_Text_MallCooltrainerMText::
	.string "The better trainer"
	.string "\nyou are, the more"
	.string "\pyou'll find your-"
	.string "\nself thinking!"
	.string "\pThat's so you can"
	.string "\nhelp your POKéMON"
	.string "\lpartners win!$"

Unova_ShoppingMallNine_Text_MallCooltrainerFText::
	.string "The thing I buy"
	.string "\nmost often is the"
	.string "\pitem that raises a"
	.string "\nPOKéMON's HP, it's"
	.string "\lcalled HP UP."
	.string "\pThere are also a"
	.string "\nlot of other items"
	.string "\lthat catch my eye.$"

Unova_ShoppingMallNine_Text_MallYoungsterText::
	.string "If you want all"
	.string "\nthe TMs, the MALL"
	.string "\lis a must-visit!"
	.string "\pYou should brag"
	.string "\nabout coming here"
	.string "\pto any TM"
	.string "\ncollector!$"

Unova_ShoppingMallNine_Text_MallBugCatcherText::
	.string "If I were to play"
	.string "\nhide and seek with"
	.string "\pmy POKéMON, they'd"
	.string "\nfind me right"
	.string "\paway! But if I"
	.string "\nwere to get lost,"
	.string "\pI'd be glad they"
	.string "\ncould find me"
	.string "\lright away!$"

Unova_ShoppingMallNine_Text_MallBuenaText::
	.string "Shopping is so"
	.string "\nmuch fun! I'm"
	.string "\pthrilled with all"
	.string "\nI've accomplished!$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ MART_MALL_1 do BW3G (data/items/marts.asm)
Unova_ShoppingMallNine_EventScript_Loja0::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_ShoppingMallNine_EventScript_Loja0_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_ShoppingMallNine_EventScript_Loja0_Itens:
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_REVIVE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_FULL_HEAL
	pokemartlistend

@ MART_MALL_2 do BW3G (data/items/marts.asm)
Unova_ShoppingMallNine_EventScript_Loja1::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_ShoppingMallNine_EventScript_Loja1_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_ShoppingMallNine_EventScript_Loja1_Itens:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	pokemartlistend

@ MART_MALL_3 do BW3G (data/items/marts.asm)
Unova_ShoppingMallNine_EventScript_Loja2::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_ShoppingMallNine_EventScript_Loja2_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_ShoppingMallNine_EventScript_Loja2_Itens:
	.2byte ITEM_TM_BLIZZARD
	.2byte ITEM_TM_THUNDER
	.2byte ITEM_TM_FIRE_BLAST
	.2byte ITEM_TM_HYPER_BEAM
	pokemartlistend

@ MART_MALL_4 do BW3G (data/items/marts.asm)
Unova_ShoppingMallNine_EventScript_Loja3::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_ShoppingMallNine_EventScript_Loja3_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_ShoppingMallNine_EventScript_Loja3_Itens:
	.2byte ITEM_PROTEIN
	.2byte ITEM_IRON
	.2byte ITEM_CARBOS
	.2byte ITEM_CALCIUM
	.2byte ITEM_HP_UP
	.2byte ITEM_X_ATTACK
	.2byte ITEM_X_DEFEND
	.2byte ITEM_X_SPECIAL
	.2byte ITEM_X_SP_DEF
	.2byte ITEM_X_SPEED
	.2byte ITEM_X_ACCURACY
	.2byte ITEM_DIRE_HIT
	.2byte ITEM_GUARD_SPEC
	pokemartlistend

@ MART_MALL_5 do BW3G (data/items/marts.asm)
Unova_ShoppingMallNine_EventScript_Loja4::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_ShoppingMallNine_EventScript_Loja4_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_ShoppingMallNine_EventScript_Loja4_Itens:
	.2byte ITEM_LEAF_STONE
	.2byte ITEM_FIRE_STONE
	.2byte ITEM_WATER_STONE
	.2byte ITEM_THUNDERSTONE
	pokemartlistend
