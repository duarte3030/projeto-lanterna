Route201_MapScripts::
	.byte 0

Route201_EventScript_Cashier::
	msgbox Route201_Text_Cashier, MSGBOX_NPC
	end

Route201_EventScript_SchoolKid::
	msgbox Route201_Text_SchoolKid, MSGBOX_NPC
	end

Route201_EventScript_Lass::
	msgbox Route201_Text_Lass, MSGBOX_NPC
	end

Route201_Text_Cashier:
	.string "Hi! I work at a POKéMON Mart.\n"
	.string "Did you know a POKéMON's health\l"
	.string "is measured by Hit Points (HP)?\p"
	.string "If a POKéMON runs out of HP, it\n"
	.string "faints and can't battle anymore.$"

Route201_Text_SchoolKid:
	.string "I'm studying all about POKéMON\n"
	.string "before I start my own journey.$"

Route201_Text_Lass:
	.string "If your POKéMON's HP is getting\n"
	.string "low, you should go to a POKéMON\l"
	.string "CENTER!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route201_EventScript_Placa1::
	msgbox Route201_Text_Placa1, MSGBOX_SIGN
	end

Route201_Text_Placa1:
	.string "Rt. 201\nTwinleaf Town$"

Route201_EventScript_Placa2::
	msgbox Route201_Text_Placa2, MSGBOX_SIGN
	end

Route201_Text_Placa2:
	.string "Rt. 201\nSandgem Town$"

Route201_EventScript_Placa3::
	msgbox Route201_Text_Placa3, MSGBOX_SIGN
	end

Route201_Text_Placa3:
	.string "Trainer Tips!\pDon't be shy! Talk to anyone and\neveryone you happen to see.\pBy talking to people, you will get\ninvaluable information and advice.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route201_EventScript_Npc1::
	msgbox Route201_Text_Npc1, MSGBOX_NPC
	end

Route201_Text_Npc1:
	.string "Wild Pokémon lurk in tall grass. They\ncan come bursting out at any time.\pSo, if you're wanting to battle wild\nPokémon, just walk in tall grass.\pIf you want to avoid wild Pokémon,\nthen stay out of the tall grass.$"

Route201_EventScript_Npc2::
	msgbox Route201_Text_Npc2, MSGBOX_NPC
	end

Route201_Text_Npc2:
	.string "Hi!\nI work at a Pokémon Mart.\pDid you know that a Pokémon's health\nis measured by Hit Points (HP)?\pIf a Pokémon runs out of HP, it\nfaints and can't battle anymore.\pIf a Pokémon's HP gets low, you\nshould heal it with a Potion.\pHere, let me give you a Potion as\na free sample. First one's free!\pIt will automatically go in the\nMedicine Pocket of your Bag.$"

Route201_EventScript_Npc3::
	msgbox Route201_Text_Npc3, MSGBOX_NPC
	end

Route201_Text_Npc3:
	.string "That ledge is one way. Jump down\nfor a shortcut to Twinleaf Town!$"

Route201_EventScript_Npc4::
	msgbox Route201_Text_Npc4, MSGBOX_NPC
	end

Route201_Text_Npc4:
	.string "If your Pokémon's health--that's its\nHP--is getting low, you should go\phome and get some rest.$"
