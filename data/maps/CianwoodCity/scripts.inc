CianwoodCity_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

CianwoodCity_EventScript_CaveSign::
	lock
	msgbox CianwoodCity_Text_Safari, MSGBOX_SIGN
	closemessage
	release
	end

CianwoodCity_EventScript_CitySign::
	lock
	msgbox CianwoodCity_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

CianwoodCity_EventScript_GymSign::
	lock
	msgbox CianwoodCity_Text_GymSign, MSGBOX_SIGN
	closemessage
	release
	end

CianwoodCity_EventScript_Pharmacy::
	lock
	msgbox CianwoodCity_Text_PharmacySign, MSGBOX_SIGN
	closemessage
	release
	end

CianwoodCity_Text_GymSign::
	.string "CIANWOOD CITY POKéMON GYM\p"
	.string "LEADER: CHUCK\p"
	.string "His Roaring Fists Do the Talking$"

CianwoodCity_Text_PharmacySign::
	.string "500 Years of Tradition\p"
	.string "CIANWOOD CITY PHARMACY\p"
	.string "We Await Your Medicinal Queries$"

CianwoodCity_Text_Safari::
	.string "CLIFF EDGE CAVE\n"
	.string "Road to the SAFARI ZONE.$"

CianwoodCity_Text_Sign::
	.string "CIANWOOD CITY\p"
	.string "A Port Surrounded by Rough Seas$"
