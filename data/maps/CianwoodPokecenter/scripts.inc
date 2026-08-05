CianwoodPokecenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CianwoodPokecenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

CianwoodPokecenter_OnTransition:
	setrespawn HEAL_LOCATION_CIANWOOD_CITY
	end

CianwoodPokecenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_CIANWOOD_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

CianwoodPokecenter_EventScript_Nerd::
	lock
	faceplayer
	msgbox CianwoodPokecenter_Text_Nerd, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodPokecenter_EventScript_Guide::
	lock
	faceplayer
	msgbox CianwoodPokecenter_Text_Guide, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodPokecenter_EventScript_Lass::
	lock
	faceplayer
	msgbox CianwoodPokecenter_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodPokecenter_EventScript_Fisher::
	lock
	faceplayer
	msgbox CianwoodPokecenter_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodPokecenter_Text_Nerd:
	.string "I love showing off the POKéMON\n"
	.string "that I've raised.\p"
	.string "Don't you?\p"
	.string "I'm going to get into a bunch of\n"
	.string "battles, and show off my POKéMON!$"

CianwoodPokecenter_Text_Guide:
	.string "The POKéMON GYM trainers here are\n"
	.string "macho bullies.\p"
	.string "Here's some advice: the GYM LEADER\n"
	.string "uses the FIGHTING-type.\p"
	.string "So you should confound him with\n"
	.string "psychic POKéMON.$"

CianwoodPokecenter_Text_Lass:
	.string "Did you meet the POKéMANIAC?\p"
	.string "He's always bragging about his\n"
	.string "rare POKéMON.$"

CianwoodPokecenter_Text_Fisher:
	.string "As far as water POKéMON go,\n"
	.string "TENTACOOL is the best by a\l"
	.string "nautical mile!$"
