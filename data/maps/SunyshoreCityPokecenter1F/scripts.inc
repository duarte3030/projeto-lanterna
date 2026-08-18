SunyshoreCityPokecenter1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SunyshoreCityPokecenter1F_OnTransition
	.byte 0

@ Ponto de cura de Sinnoh (dev_scripts/heal_locations_sinnoh_ginasios.py).
SunyshoreCityPokecenter1F_OnTransition:
	setrespawn HEAL_LOCATION_SUNYSHORE_CITY
	end

SunyshoreCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

SunyshoreCityPokecenter1F_EventScript_Npc1::
	msgbox SunyshoreCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

SunyshoreCityPokecenter1F_Text_Npc1:
	.string "Wow, you're really cool!\nYou have seven Gym Badges!\pAll you need is one more to challenge\nthe Pokémon League.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SunyshoreCityPokecenter1F_EventScript_Npc3::
	msgbox SunyshoreCityPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

SunyshoreCityPokecenter1F_Text_Npc3:
	.string "I once dreamed of becoming a Gym\nLeader...\pThough that dream never came true,\nI got to live with Pokémon all\pthis time.\pIt's been a blessed life.$"

SunyshoreCityPokecenter1F_EventScript_Npc2::
	msgbox SunyshoreCityPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

SunyshoreCityPokecenter1F_Text_Npc2:
	.string "To make up for the lack of space, the\ncity built roads out of solar panels.\pThose solar panels provide us with\nclean energy, and they're good roads.\pIt's a symbol of Sunyshore's will to\nsurvive, I think.$"
