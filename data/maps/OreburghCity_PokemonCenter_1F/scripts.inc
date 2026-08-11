OreburghCity_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OreburghCity_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

OreburghCity_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_OREBURGH_CITY
	end

OreburghCity_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_OREBURGH_PC1_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

OreburghCity_PokemonCenter_1F_EventScript_AceTrainer::
	msgbox OreburghCity_PokemonCenter_1F_Text_AceTrainer, MSGBOX_NPC
	end

OreburghCity_PokemonCenter_1F_EventScript_Gentleman::
	lock
	faceplayer
	msgbox OreburghCity_PokemonCenter_1F_Text_Gentleman, MSGBOX_DEFAULT
	release
	end

OreburghCity_PokemonCenter_1F_Text_Nurse:
	.string "Welcome to the POKéMON CENTER.\n"
	.string "We heal your POKéMON free of charge.$"

OreburghCity_PokemonCenter_1F_Text_AceTrainer:
	.string "There's a long way from here to\n"
	.string "ETERNA CITY. You should be prepared\l"
	.string "for a long journey.$"

OreburghCity_PokemonCenter_1F_Text_Gentleman:
	.string "Hmmm! What, or who, is this TEAM\n"
	.string "GALACTIC?! They make wonderful claims\l"
	.string "of a dream energy source on one hand...\p"
	.string "But rumor has it they steal POKéMON\n"
	.string "from others by force. It's a mystery!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_PokemonCenter_1F_EventScript_Npc1::
	msgbox OreburghCity_PokemonCenter_1F_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_PokemonCenter_1F_Text_Npc1:
	.string "Hmmm...!\pWhat is your favorite kind of Trainer?\nCan you tell me?$"

OreburghCity_PokemonCenter_1F_EventScript_Npc2::
	msgbox OreburghCity_PokemonCenter_1F_Text_Npc2, MSGBOX_NPC
	end

OreburghCity_PokemonCenter_1F_Text_Npc2:
	.string "Switch on the PC at any Pokémon\nCenter.\pConnect to 'Someone's PC' and access\nthe Pokémon Storage System.\pThat's all you need to do to store\nor bring out your Pokémon.$"

OreburghCity_PokemonCenter_1F_EventScript_Npc3::
	msgbox OreburghCity_PokemonCenter_1F_Text_Npc3, MSGBOX_NPC
	end

OreburghCity_PokemonCenter_1F_Text_Npc3:
	.string "Yay! I got a Pal Pad at the\nPokémon Wi-Fi Club downstairs!$"

OreburghCity_PokemonCenter_1F_EventScript_Npc4::
	msgbox OreburghCity_PokemonCenter_1F_Text_Npc4, MSGBOX_NPC
	end

OreburghCity_PokemonCenter_1F_Text_Npc4:
	.string "Hmmm!\nWhat, or who, is this Team Galactic?!\pThey make wonderful claims of a dream\nenergy source on one hand...\pBut rumor has it, they steal Pokémon\nfrom others by force.\pIt's a mystery! They're mysterious!\nIsn't anyone investigating them?$"

OreburghCity_PokemonCenter_1F_EventScript_Npc5::
	msgbox OreburghCity_PokemonCenter_1F_Text_Npc5, MSGBOX_NPC
	end

OreburghCity_PokemonCenter_1F_Text_Npc5:
	.string "You know how you can battle a friend\nusing wireless communications?\pWell now, you can capture it as a Battle\nVideo using a Vs. Recorder!$"

OreburghCity_PokemonCenter_1F_EventScript_Npc6::
	msgbox OreburghCity_PokemonCenter_1F_Text_Npc6, MSGBOX_NPC
	end

OreburghCity_PokemonCenter_1F_Text_Npc6:
	.string "Cool!\nYou have a Vs. Recorder!\pSo, did you go to the Global Terminal in\nJubilife City? Did ya? Did ya?$"
