PokemonMansionOffice_MapScripts::
	.byte 0

PokemonMansionOffice_EventScript_Placa1::
	msgbox PokemonMansionOffice_Text_Placa1, MSGBOX_SIGN
	end

PokemonMansionOffice_Text_Placa1:
	.string "It's a very expensive-looking book\non Pokémon.\pWould you like to read it?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PokemonMansionOffice_EventScript_Npc1::
	msgbox PokemonMansionOffice_Text_Npc1, MSGBOX_NPC
	end

PokemonMansionOffice_Text_Npc1:
	.string "Backlot: Hello, hello!\nWelcome to my opulent mansion!\pThere's a lot for me to be proud of\ninside, and outside, of this home...\pBut what makes me the most proud is\nmy trophy garden in the back!\pWhy bother traveling afar when\nPokémon are attracted by my garden?\pThey come to me in hopes of seeing\nthe garden!\pYou're welcome to join them and\nmarvel at my garden!$"

PokemonMansionOffice_EventScript_Placa2::
	msgbox PokemonMansionOffice_Text_Placa2, MSGBOX_SIGN
	end

PokemonMansionOffice_Text_Placa2:
	.string "It's a very expensive-looking Pokémon\nstatue...\p...!\nYou got fingerprints on it...$"
