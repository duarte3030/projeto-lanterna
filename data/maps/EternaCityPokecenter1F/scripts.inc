EternaCityPokecenter1F_MapScripts::
	.byte 0

EternaCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

EternaCityPokecenter1F_EventScript_Npc1::
	msgbox EternaCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

EternaCityPokecenter1F_Text_Npc1:
	.string "Team Galactic took my Pokémon away.\nThey took other people's, too.\pSomething should be done, but Team\nGalactic creeps everyone out...\pWhat are they doing to my Pokémon?$"
