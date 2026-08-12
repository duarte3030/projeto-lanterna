FloaromaTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FloaromaTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

FloaromaTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_FLOAROMA_TOWN
	end

FloaromaTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_FLOAROMA_PC1_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

FloaromaTown_PokemonCenter_1F_Text_Nurse:
	.string "Welcome to the POKéMON CENTER.\n"
	.string "We heal your POKéMON free of charge.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

FloaromaTown_PokemonCenter_1F_EventScript_Npc1::
	msgbox FloaromaTown_PokemonCenter_1F_Text_Npc1, MSGBOX_NPC
	end

FloaromaTown_PokemonCenter_1F_Text_Npc1:
	.string "There've been problems with the\nelectric power lately.\pIs there some trouble at the Valley\nWindworks?$"

FloaromaTown_PokemonCenter_1F_EventScript_Npc2::
	msgbox FloaromaTown_PokemonCenter_1F_Text_Npc2, MSGBOX_NPC
	end

FloaromaTown_PokemonCenter_1F_Text_Npc2:
	.string "I had a battle the other day, and my\nPokémon's HP got low.\pI thought we were done for.\pAnd then, all of a sudden, my Pokémon\nate the Berry it was holding! Whew!$"

FloaromaTown_PokemonCenter_1F_EventScript_Npc3::
	msgbox FloaromaTown_PokemonCenter_1F_Text_Npc3, MSGBOX_NPC
	end

FloaromaTown_PokemonCenter_1F_Text_Npc3:
	.string "If you've got Pokémon with you,\nit's safe for even a kid like you\pto go off traveling alone.$"
