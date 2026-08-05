SolaceonTownPokecenter1F_MapScripts::
	.byte 0

SolaceonTownPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end
