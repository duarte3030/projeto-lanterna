EternaCityPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EternaCityPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Sinnoh (dev_scripts/heal_locations_sinnoh_ginasios.py).
EternaCityPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_ETERNA_CITY
	end

EternaCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

EternaCityPokecenter1F_EventScript_Npc1::
	msgbox EternaCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

EternaCityPokecenter1F_Text_Npc1:
	.string "Team Galactic took my Pokémon away.\nThey took other people's, too.\pSomething should be done, but Team\nGalactic creeps everyone out...\pWhat are they doing to my Pokémon?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

EternaCityPokecenter1F_EventScript_Npc2::
	msgbox EternaCityPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

EternaCityPokecenter1F_Text_Npc2:
	.string "When a Pokémon faints, it just means\nit doesn't have the power to battle.\pBut it can still use hidden moves\noutside of battle!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

EternaCityPokecenter1F_EventScript_Npc3::
	bufferleadmonspeciesname STR_VAR_1
	msgbox EternaCityPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

EternaCityPokecenter1F_Text_Npc3:
	.string "Hi, you cute little Trainer!\nWhat kinds of Pokémon are with you?\pOh, your {STR_VAR_1}...$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
EternaCityPokecenter1F_EventScript_PortaFechada::
	msgbox EternaCityPokecenter1F_Text_PortaFechada, MSGBOX_SIGN
	end

EternaCityPokecenter1F_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
