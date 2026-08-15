EcruteakCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EcruteakCity_OnTransition
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

EcruteakCity_EventScript_BurnedSign::
	lock
	msgbox EcruteakCity_Text_BurnedTowerSign, MSGBOX_SIGN
	closemessage
	release
	end

EcruteakCity_EventScript_CitySign::
	lock
	msgbox EcruteakCity_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

EcruteakCity_EventScript_GymSign::
	lock
	msgbox EcruteakCity_Text_GymSign, MSGBOX_SIGN
	closemessage
	release
	end

EcruteakCity_EventScript_OfficeSign::
	lock
	msgbox EcruteakCity_Text_OfficeSign, MSGBOX_SIGN
	closemessage
	release
	end

EcruteakCity_EventScript_TheaterSign::
	lock
	msgbox EcruteakCity_Text_DanceTheaterSign, MSGBOX_SIGN
	closemessage
	release
	end

EcruteakCity_Text_BurnedTowerSign::
	.string "BURNED TOWER\p"
	.string "It was destroyed by a mysterious\n"
	.string "fire.\p"
	.string "Please stay away, as it is unsafe.$"

EcruteakCity_Text_DanceTheaterSign::
	.string "ECRUTEAK DANCE THEATER$"

EcruteakCity_Text_GymSign::
	.string "ECRUTEAK CITY POKéMON GYM\n"
	.string "LEADER: MORTY\p"
	.string "The Mystic Seer of the Future$"

EcruteakCity_Text_OfficeSign::
	.string "Barrier Station to TIN TOWER\p"
	.string "No Trespassing by the Unworthy.$"

EcruteakCity_Text_Sign::
	.string "ECRUTEAK CITY\n"
	.string "A Historical City\p"
	.string "Where the Past Meets the Present$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

EcruteakCity_EventScript_Lass::
	lock
	faceplayer
	msgbox EcruteakCity_Text_Lass1, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Text_Lass1::
	.string "I'm going to practice at the DANCE\n"
	.string "THEATER. Care to join me?$"

EcruteakCity_EventScript_SageRight::
	lock
	faceplayer
	msgbox EcruteakCity_Text_Gramps2, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Text_Gramps2::
	.string "Ah, child. Have you learned to\n"
	.string "dance like the KIMONO GIRLS?\p"
	.string "If you go to their DANCE THEATER,\n"
	.string "an odd old man will give you\l"
	.string "something nice, I hear.$"

EcruteakCity_EventScript_Gramps::
	lock
	faceplayer
	msgbox EcruteakCity_Text_Gramps1, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Text_Gramps1::
	.string "ECRUTEAK used to have two towers:\n"
	.string "one each in the east and west.$"

EcruteakCity_EventScript_SageTower::
	lock
	faceplayer
	msgbox EcruteakCity_Text_Gramps3, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Text_Gramps3::
	.string "In the distant past…\p"
	.string "This tower burned in a fire. Three\n"
	.string "nameless POKéMON perished in it.\p"
	.string "A rainbow-colored POKéMON descended\n"
	.string "from the sky and resurrected them…\p"
	.string "It's a legend that has been passed\n"
	.string "down by ECRUTEAK GYM LEADERS.\p"
	.string "Me?\p"
	.string "I was a trainer way back when.\n"
	.string "Hohoho!$"

EcruteakCity_EventScript_Youngster::
	lock
	faceplayer
	msgbox EcruteakCity_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Text_Youngster::
	.string "I hear POKéMON are rampaging at the\n"
	.string "LAKE OF RAGE. I'd like to see that.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

EcruteakCity_EventScript_SageGym::
	lock
	faceplayer
	msgbox EcruteakCity_Text_SageGym, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Text_SageGym::
	.string "Gym Leader MORTY is not here right\n"
	.string "now. You may find him at the\l"
	.string "BURNED TOWER.$"

@ >>> B6 Johto: cena portada do hns (porta_cenas_johto.py) >>>
@ o cameo do rival na porta do teatro, que abre o desafio das cinco
.set LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER, 33

EcruteakCity_Trigger_Silver::
	lockall
	opendoor 39, 40
	waitdooranim
	delay 10
	clearflag FLAG_HIDE_ECRUTEAK_SILVER
	addobject LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER
	playbgm MUS_HG_ENCOUNTER_RIVAL, TRUE
	playse SE_BANG
	applymovement LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER, EcruteakCity_Movement_Silver1
	applymovement OBJ_EVENT_ID_PLAYER, EcruteakCity_Movement_Silver1
	message EcruteakCity_Text_Silver1
	
	waitmovement OBJ_EVENT_ID_PLAYER
	waitmovement LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER
	turnobject OBJ_EVENT_ID_PLAYER, DIR_NORTH
	closedoor 39, 40
	waitdooranim
	msgbox EcruteakCity_Text_Silver2, MSGBOX_DEFAULT
	closemessage
	playse SE_PIN
	applymovement LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER, Common_Movement_ExclamationMark
	delay 60
	turnobject LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER, DIR_SOUTH
	msgbox EcruteakCity_Text_Silver3, MSGBOX_DEFAULT
	closemessage

	applymovement LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER, EcruteakCity_Movement_Silver2
	waitmovement LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER


	setflag FLAG_HIDE_ECRUTEAK_SILVER
	removeobject LOCALID_ECRUTEAKCITY_ECRUTEK_SILVER
	fadedefaultbgm

	setvar VAR_ECRUTEAK_CITY_THEATER, 5
	releaseall
	end

EcruteakCity_OnTransition::
	setflag FLAG_HIDE_ECRUTEAK_SILVER
	end

EcruteakCity_Movement_Silver1::
	delay_16
	lock_facing_direction
	walk_down
	unlock_facing_direction
	step_end

EcruteakCity_Movement_Silver2::
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

EcruteakCity_Text_Silver1::
	.string "THUD!!$"

EcruteakCity_Text_Silver2::
	.string "{RIVAL}: How...? How is this\n"
	.string "possible? How can I lose to mere\l"
	.string "KIMONO GIRLS...?$"

EcruteakCity_Text_Silver3::
	.string "{RIVAL}: You were watching me,\n"
	.string "{PLAYER}...\p"
	.string "Yeah, that's right!\p"
	.string "I never thought defeating five\n"
	.string "KIMONO GIRLS would be so hard...\p"
	.string "I got beaten to a pulp...\p"
	.string "...\p"
	.string "You must have come here for the\n"
	.string "same reason, right?\p"
	.string "Don't get cocky just because you\n"
	.string "defeated TEAM ROCKET!\p"
	.string "These KIMONO GIRLS are insanely\n"
	.string "strong.\p"
	.string "See if you can defeat them.\p"
	.string "But I'm not going back, I don't\n"
	.string "want to see you win.$"

@ <<< B6 Johto: cena portada do hns <<<
