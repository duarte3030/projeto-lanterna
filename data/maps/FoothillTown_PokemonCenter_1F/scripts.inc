@ FoothillTown_PokemonCenter_1F: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 17.1) por dev_scripts/copia_planta_ex.py.

FoothillTown_PokemonCenter_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, FoothillTown_PokemonCenter_1F_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

FoothillTown_PokemonCenter_1F_OnTransition:
	setrespawn HEAL_LOCATION_FOOTHILL_TOWN
	end

@ Enfermeira NOSSA (PLANO f), na célula da do EX.
FoothillTown_PokemonCenter_1F_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_FOOTHILL_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Eventos novos do Pokémon Emerald EX (mapa 17.1), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
FoothillTown_PokemonCenter_1F_EventScript_ExNpc1::
	msgbox FoothillTown_PokemonCenter_1F_Text_ExNpc1, MSGBOX_NPC
	end

FoothillTown_PokemonCenter_1F_Text_ExNpc1:
	.string "I’ve heard catching the GYARADOS in the\n"
	.string "lake is almost impossible.$"

FoothillTown_PokemonCenter_1F_EventScript_ExNpc2::
	msgbox FoothillTown_PokemonCenter_1F_Text_ExNpc2, MSGBOX_NPC
	end

FoothillTown_PokemonCenter_1F_Text_ExNpc2:
	.string "FOOTHILL TOWN is so quiet and peaceful.\p"
	.string "Maybe I should stop traveling and stay\n"
	.string "here for a while.$"

