CelesticTownPokecenter1F_MapScripts::
	.byte 0

CelesticTownPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

CelesticTownPokecenter1F_EventScript_Npc1::
	msgbox CelesticTownPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

CelesticTownPokecenter1F_Text_Npc1:
	.string "Oh? Hm, hm...\nYour Pokémon is quite interesting!$"
