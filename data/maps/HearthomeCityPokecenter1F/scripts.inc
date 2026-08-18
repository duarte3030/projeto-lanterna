HearthomeCityPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, HearthomeCityPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Sinnoh (dev_scripts/heal_locations_sinnoh_ginasios.py).
HearthomeCityPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_HEARTHOME_CITY
	end

HearthomeCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

HearthomeCityPokecenter1F_EventScript_Npc1::
	msgbox HearthomeCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

HearthomeCityPokecenter1F_Text_Npc1:
	.string "Have you checked out the Global\nTerminal in Jubilife City?\pIt uses Nintendo Wi-Fi Connection!\nI can't explain it, but it's wicked!$"

HearthomeCityPokecenter1F_EventScript_Npc2::
	msgbox HearthomeCityPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

HearthomeCityPokecenter1F_Text_Npc2:
	.string "Hello, do you have a Poffin Case?\pIf you haven't got one, you really\nmust visit the Pokémon Fan Club.$"

HearthomeCityPokecenter1F_EventScript_Npc3::
	msgbox HearthomeCityPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

HearthomeCityPokecenter1F_Text_Npc3:
	.string "Fantina, the Gym Leader, likes\nContests, too.\pThat lady has a huge appetite for\nexperiencing everything in life!$"
