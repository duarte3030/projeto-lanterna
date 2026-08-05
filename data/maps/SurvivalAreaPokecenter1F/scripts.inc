SurvivalAreaPokecenter1F_MapScripts::
	.byte 0

SurvivalAreaPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

SurvivalAreaPokecenter1F_EventScript_Npc1::
	msgbox SurvivalAreaPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

SurvivalAreaPokecenter1F_Text_Npc1:
	.string "The building next door?\pI see Gym Leaders go in and out every\nso often.$"
