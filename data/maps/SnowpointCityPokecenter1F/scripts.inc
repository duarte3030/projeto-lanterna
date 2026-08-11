SnowpointCityPokecenter1F_MapScripts::
	.byte 0

SnowpointCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SnowpointCityPokecenter1F_EventScript_Npc1::
	msgbox SnowpointCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

SnowpointCityPokecenter1F_Text_Npc1:
	.string "You know how there are many Ice-type\nPokémon around Snowpoint City?\pI wonder if they also live in the temple?$"

SnowpointCityPokecenter1F_EventScript_Npc2::
	msgbox SnowpointCityPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

SnowpointCityPokecenter1F_Text_Npc2:
	.string "Sound gets swallowed up by the snow.\nThat's why it's very quiet here.$"

SnowpointCityPokecenter1F_EventScript_Npc3::
	msgbox SnowpointCityPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

SnowpointCityPokecenter1F_Text_Npc3:
	.string "PSYDUCK: Gaga guwawa!$"
