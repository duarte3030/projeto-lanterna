VeilstoneCityPokecenter1F_MapScripts::
	.byte 0

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
