GoldenrodCity_PokemonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GoldenrodCity_PokemonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

GoldenrodCity_PokemonCenter_OnTransition:
	setrespawn HEAL_LOCATION_GOLDENROD_CITY
	end

GoldenrodCity_PokemonCenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_GOLDENROD_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

GoldenrodCity_PokemonCenter_EventScript_Lass::
	lock
	faceplayer
	msgbox GoldenrodCity_PokemonCenter_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_PokemonCenter_EventScript_GbaKid1::
	lock
	faceplayer
	msgbox GoldenrodCity_PokemonCenter_Text_GbaKid1, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_PokemonCenter_EventScript_Granny::
	lock
	faceplayer
	msgbox GoldenrodCity_PokemonCenter_Text_Granny, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_PokemonCenter_EventScript_GbaKid2::
	lock
	faceplayer
	msgbox GoldenrodCity_PokemonCenter_Text_GbaKid2, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_PokemonCenter_Text_Lass:
	.string "A higher level POKéMON doesn't\n"
	.string "always win.\p"
	.string "After all, it may have a type\n"
	.string "disadvantage.\p"
	.string "I don't think there is a single\n"
	.string "POKéMON that is the toughest.$"

GoldenrodCity_PokemonCenter_Text_GbaKid1:
	.string "This is a special POKéMON CENTER.\n"
	.string "The roof is made of gold!$"

GoldenrodCity_PokemonCenter_Text_Granny:
	.string "I just love living in the big city!\n"
	.string "I moved here when I was a young\l"
	.string "trainer, like you!$"

GoldenrodCity_PokemonCenter_Text_GbaKid2:
	.string "I told my brother that the roof is\n"
	.string "made of real gold. He'll believe\l"
	.string "anything!$"
