CanalaveCityPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CanalaveCityPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Sinnoh (dev_scripts/heal_locations_sinnoh_ginasios.py).
CanalaveCityPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_CANALAVE_CITY
	end

CanalaveCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CanalaveCityPokecenter1F_EventScript_Npc1::
	msgbox CanalaveCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

CanalaveCityPokecenter1F_Text_Npc1:
	.string "I was lucky enough to get a\nStrength HM from Iron Island.\pBut I can't use it for moving boulders\nuntil I beat Byron, the Gym Leader.\pI should make a note of that on the\nPokétch app Memo Pad.$"

CanalaveCityPokecenter1F_EventScript_Npc2::
	msgbox CanalaveCityPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

CanalaveCityPokecenter1F_Text_Npc2:
	.string "It's easy to get to Iron Island.\nIt's one boat trip from here.$"

CanalaveCityPokecenter1F_EventScript_Npc3::
	msgbox CanalaveCityPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

CanalaveCityPokecenter1F_Text_Npc3:
	.string "I heard this cool rumor.\pIf you can get on Nintendo Wi-Fi\nConnection, you can go to the Wi-Fi\pPlaza.\pThe access to the Wi-Fi Plaza is through\nthe basement of any Pokémon Center.$"

CanalaveCityPokecenter1F_EventScript_Npc4::
	msgbox CanalaveCityPokecenter1F_Text_Npc4, MSGBOX_NPC
	end

CanalaveCityPokecenter1F_Text_Npc4:
	.string "It's possible for one kind of Pokémon\nto have different abilities.\pThat's news to me!$"
