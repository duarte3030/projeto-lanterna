PokemonLeagueSouthPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PokemonLeagueSouthPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Sinnoh (dev_scripts/heal_locations_sinnoh_ginasios.py).
PokemonLeagueSouthPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_POKEMON_LEAGUE_SOUTH
	end

PokemonLeagueSouthPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PokemonLeagueSouthPokecenter1F_EventScript_Npc1::
	msgbox PokemonLeagueSouthPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

PokemonLeagueSouthPokecenter1F_Text_Npc1:
	.string "The objective is to reach the Pokémon\nLeague.\pStay focused and never lose sight of\nthat goal.\pIt will sustain you as you fight through\nthe long and arduous Victory Road.$"

PokemonLeagueSouthPokecenter1F_EventScript_Npc2::
	msgbox PokemonLeagueSouthPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

PokemonLeagueSouthPokecenter1F_Text_Npc2:
	.string "Victory Road confuses me.\nI should draw up a map.$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
PokemonLeagueSouthPokecenter1F_EventScript_PortaFechada::
	msgbox PokemonLeagueSouthPokecenter1F_Text_PortaFechada, MSGBOX_SIGN
	end

PokemonLeagueSouthPokecenter1F_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
