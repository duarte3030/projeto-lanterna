VeilstoneCityPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, VeilstoneCityPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Sinnoh (dev_scripts/heal_locations_sinnoh_ginasios.py).
VeilstoneCityPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_VEILSTONE_CITY
	end

VeilstoneCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

VeilstoneCityPokecenter1F_EventScript_Npc1::
	msgbox VeilstoneCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

VeilstoneCityPokecenter1F_Text_Npc1:
	.string "If you use the hidden move Fly,\nyou'll be instantly whisked to any\ptown you've visited before.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

VeilstoneCityPokecenter1F_EventScript_Npc2::
	msgbox VeilstoneCityPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

VeilstoneCityPokecenter1F_Text_Npc2:
	.string "Maylene, the Gym Leader, is a cute\ngirl.\pBut don't let her looks fool you.\nEven grown-ups have trouble with her.$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
VeilstoneCityPokecenter1F_EventScript_PortaFechada::
	msgbox VeilstoneCityPokecenter1F_Text_PortaFechada, MSGBOX_SIGN
	end

VeilstoneCityPokecenter1F_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
