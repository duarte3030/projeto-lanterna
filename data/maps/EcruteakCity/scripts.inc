EcruteakCity_MapScripts::
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
