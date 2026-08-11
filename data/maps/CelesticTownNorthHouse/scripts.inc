CelesticTownNorthHouse_MapScripts::
	.byte 0

CelesticTownNorthHouse_EventScript_Npc1::
	msgbox CelesticTownNorthHouse_Text_Npc1, MSGBOX_NPC
	end

CelesticTownNorthHouse_Text_Npc1:
	.string "Where are you from?\p...\pHm, Twinleaf Town, you say.\nIsn't that close to Lake Verity?\pThat lake is said to be home to MESPRIT,\n'The Being of Emotion.'\pThat Pokémon may well be watching\nover you.\pWould you like to know more about\nMESPRIT?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CelesticTownNorthHouse_EventScript_Npc2::
	msgbox CelesticTownNorthHouse_Text_Npc2, MSGBOX_NPC
	end

CelesticTownNorthHouse_Text_Npc2:
	.string "My big sister is studying the myths\nof Sinnoh.\pShe wants to know how people and\nPokémon interacted in the days of\pmyths.\pWere things different back then?\nOr were they the same as now?\pShe says that's the focus of her\nresearch.$"

CelesticTownNorthHouse_EventScript_Placa2::
	msgbox CelesticTownNorthHouse_Text_Placa2, MSGBOX_SIGN
	end

CelesticTownNorthHouse_Text_Placa2:
	.string "It's hard to tell for sure, but it's\nprobably an invaluable scroll.$"
