EcruteakCity_PokemonCenter_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EcruteakCity_PokemonCenter_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, CableClub_OnResume
	.byte 0

EcruteakCity_PokemonCenter_OnTransition:
	setrespawn HEAL_LOCATION_ECRUTEAK_CITY
	end

EcruteakCity_PokemonCenter_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_ECRUTEAK_PC_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

EcruteakCity_PokemonCenter_EventScript_Nerd::
	lock
	faceplayer
	msgbox EcruteakCity_PokemonCenter_Text_Nerd, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_PokemonCenter_EventScript_Hiker::
	lock
	faceplayer
	msgbox EcruteakCity_PokemonCenter_Text_Hiker, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_PokemonCenter_EventScript_Woman::
	lock
	faceplayer
	msgbox EcruteakCity_PokemonCenter_Text_Woman, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_PokemonCenter_Text_Nerd:
	.string "LAKE OF RAGE…\p"
	.string "The appearance of a GYARADOS\n"
	.string "swarm…\p"
	.string "I smell a conspiracy. I know it!$"

EcruteakCity_PokemonCenter_Text_Hiker:
	.string "The way the KIMONO GIRLS dance is\n"
	.string "marvelous.\p"
	.string "Just like the way they use their\n"
	.string "POKéMON.$"

EcruteakCity_PokemonCenter_Text_Woman:
	.string "MORTY, the GYM LEADER, is soooo\n"
	.string "cool.\p"
	.string "His POKéMON are really tough too.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

EcruteakCity_PokemonCenter1F_Text_Bill1::
	.string "Hi, I'm BILL. And who are you?\p"
	.string "Hmm, {PLAYER}, huh?\n"
	.string "You've come at the right time.$"

EcruteakCity_PokemonCenter_EventScript_BillFala::
	msgbox EcruteakCity_PokemonCenter1F_Text_Bill1, MSGBOX_NPC
	end
