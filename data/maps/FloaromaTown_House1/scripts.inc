FloaromaTown_House1_MapScripts::
	.byte 0

FloaromaTown_House1_EventScript_Twin::
	msgbox FloaromaTown_House1_Text_Twin, MSGBOX_NPC
	end

FloaromaTown_House1_EventScript_Clefairy::
	msgbox FloaromaTown_House1_Text_Clefairy, MSGBOX_NPC
	end

FloaromaTown_House1_Text_Twin:
	.string "Do you think it's cute how POKéMON\n"
	.string "pluck Berries?$"

FloaromaTown_House1_Text_Clefairy:
	.string "CLEFAIRY stares back at you\n"
	.string "curiously.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

FloaromaTown_House1_EventScript_Npc1::
	msgbox FloaromaTown_House1_Text_Npc1, MSGBOX_NPC
	end

FloaromaTown_House1_Text_Npc1:
	.string "Pokémon must have an acute sense\nof smell.\pThey can sense the aroma of Honey\nfrom very far away.$"

FloaromaTown_House1_EventScript_Npc2::
	msgbox FloaromaTown_House1_Text_Npc2, MSGBOX_NPC
	end

FloaromaTown_House1_Text_Npc2:
	.string "Some kinds of Pokémon appear only\nif they're attracted by the sweet\pscent of Honey.$"
