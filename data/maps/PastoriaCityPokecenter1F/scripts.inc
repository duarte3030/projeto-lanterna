PastoriaCityPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PastoriaCityPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Sinnoh (dev_scripts/heal_locations_sinnoh_ginasios.py).
PastoriaCityPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_PASTORIA_CITY
	end

PastoriaCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCityPokecenter1F_EventScript_Npc1::
	msgbox PastoriaCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

PastoriaCityPokecenter1F_Text_Npc1:
	.string "The Great Marsh is vast!\nHow vast is it, you ask?\pTake a look from the Observatory\nand you can see for yourself!$"

PastoriaCityPokecenter1F_EventScript_Npc2::
	msgbox PastoriaCityPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

PastoriaCityPokecenter1F_Text_Npc2:
	.string "Pastoria's Great Marsh was once\na part of the sea.\pThe seawater drained slowly away over\ntime, leaving the huge marshland.\pThat's why they say there are rare\nPokémon that you can only see here.$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
PastoriaCityPokecenter1F_EventScript_PortaFechada::
	msgbox PastoriaCityPokecenter1F_Text_PortaFechada, MSGBOX_SIGN
	end

PastoriaCityPokecenter1F_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
