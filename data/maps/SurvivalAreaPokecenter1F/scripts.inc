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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SurvivalAreaPokecenter1F_EventScript_Npc3::
	msgbox SurvivalAreaPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

SurvivalAreaPokecenter1F_Text_Npc3:
	.string "In a Multi Battle, coordination with\nyour partner is vital.\pBy working together, one plus one\ncould become not just two, but even\pthree or four.\pBut one times one is always one.\nDo you understand that?$"

SurvivalAreaPokecenter1F_EventScript_Npc2::
	msgbox SurvivalAreaPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

SurvivalAreaPokecenter1F_Text_Npc2:
	.string "Some say the universe was shaped by\nsomething born from an Egg...\pA man I met long ago told me that.$"
