SunyshoreCityPokecenter1F_MapScripts::
	.byte 0

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
