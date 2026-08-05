AzaleaTown_PokemonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, AzaleaTown_PokemonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

AzaleaTown_PokemonCenter_OnTransition:
	setrespawn HEAL_LOCATION_AZALEA_TOWN
	end

AzaleaTown_PokemonCenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_AZALEA_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

AzaleaTown_PokemonCenter_EventScript_PokefanF::
	lock
	faceplayer
	msgbox AzaleaTown_PokemonCenter_Text_PokefanF, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokemonCenter_EventScript_Fisher::
	lock
	faceplayer
	msgbox AzaleaTown_PokemonCenter_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokemonCenter_EventScript_Gentleman::
	lock
	faceplayer
	msgbox AzaleaTown_PokemonCenter_Text_Gentleman, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_PokemonCenter_Text_PokefanF:
	.string "Do you know about BERRIES?\p"
	.string "Crack one open, hollow it out and\n"
	.string "fit it with a special device.\p"
	.string "Then you can catch POKéMON with it.\p"
	.string "Before POKé BALLS were invented,\n"
	.string "everyone used BERRIES.$"

AzaleaTown_PokemonCenter_Text_Fisher:
	.string "BILL's PC can store up to 30\n"
	.string "POKéMON per BOX.$"

AzaleaTown_PokemonCenter_Text_Gentleman:
	.string "Do your POKéMON know HM moves?\p"
	.string "Those moves can be used even if\n"
	.string "your POKéMON has fainted.$"
