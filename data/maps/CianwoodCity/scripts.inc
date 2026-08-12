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

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

CianwoodCity_EventScript_PokefanM::
	lock
	faceplayer
	msgbox CianwoodCity_Text_PokefanM, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodCity_Text_PokefanM::
	.string "Boulders to the north of town can\n"
	.string "be crushed.\p"
	.string "They may be hiding something.\p"
	.string "Your POKéMON could use ROCK SMASH\n"
	.string "to break them.$"

CianwoodCity_EventScript_Youngster::
	lock
	faceplayer
	msgbox CianwoodCity_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodCity_Text_Youngster::
	.string "If you use FLY, you can get back\n"
	.string "to OLIVINE instantly.$"

CianwoodCity_EventScript_Lass::
	lock
	faceplayer
	msgbox CianwoodCity_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodCity_Text_Lass::
	.string "CHUCK, the GYM LEADER, spars with\n"
	.string "his fighting POKéMON.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

CianwoodCity_EventScript_Engineer::
	lock
	faceplayer
	msgbox CianwoodCity_Text_Engineer, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodCity_Text_Engineer::
	.string "This path is under construction.\n"
	.string "We're getting the new SAFARI ZONE\l"
	.string "up and running!$"
