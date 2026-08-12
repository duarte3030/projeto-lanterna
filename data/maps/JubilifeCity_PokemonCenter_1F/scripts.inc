JubilifeCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, JubilifeCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

JubilifeCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_JUBILIFE_CITY
	end

JubilifeCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_JUBILIFE_PC1F_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

JubilifeCity_PokemonCenter_1F_Text_Nurse:
	.string "Welcome to the Pokémon Center!\p"
	.string "I'm sorry, I can't heal your POKéMON\n"
	.string "just yet. Please come back later.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_PokemonCenter_1F_EventScript_Npc1::
	msgbox JubilifeCity_PokemonCenter_1F_Text_Npc1, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_1F_Text_Npc1:
	.string "You can still catch a Pokémon if you\nalready have six traveling with you.\pIt automatically gets sent to the PC\nnetwork in Pokémon Centers.\pKnowing that, I can keep on catching\nmore and more Pokémon!\pIt'll make it more fun to check\nthe PC in any Pokémon Center!$"

JubilifeCity_PokemonCenter_1F_EventScript_Npc2::
	msgbox JubilifeCity_PokemonCenter_1F_Text_Npc2, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_1F_Text_Npc2:
	.string "In the Union Room upstairs, you can\nchat and trade with other people.\pAnd that's not all you can do.\nCheck it out!$"

JubilifeCity_PokemonCenter_1F_EventScript_Npc3::
	msgbox JubilifeCity_PokemonCenter_1F_Text_Npc3, MSGBOX_NPC
	end

JubilifeCity_PokemonCenter_1F_Text_Npc3:
	.string "You know how Pokémon have types like\nWater, Fire, and Grass?\pWell, all types have strengths and\nweaknesses against other types.$"
