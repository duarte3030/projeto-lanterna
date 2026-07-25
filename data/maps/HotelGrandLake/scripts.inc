HotelGrandLake_MapScripts::
	.byte 0

HotelGrandLake_EventScript_Receptionist::
	lock
	faceplayer
	msgbox HotelGrandLake_Text_Receptionist, MSGBOX_DEFAULT
	release
	end

HotelGrandLake_EventScript_Guest1::
	msgbox HotelGrandLake_Text_Guest1, MSGBOX_NPC
	end

HotelGrandLake_EventScript_Guest2::
	msgbox HotelGrandLake_Text_Guest2, MSGBOX_NPC
	end

HotelGrandLake_EventScript_Guest3::
	msgbox HotelGrandLake_Text_Guest3, MSGBOX_NPC
	end

HotelGrandLake_EventScript_Guest4::
	msgbox HotelGrandLake_Text_Guest4, MSGBOX_NPC
	end

HotelGrandLake_Text_Receptionist:
	.string "Welcome to HOTEL GRAND LAKE!\n"
	.string "Enjoy your stay.$"

HotelGrandLake_Text_Guest1:
	.string "I climbed all the way here from\n"
	.string "ROUTE 214. My legs are killing me.$"

HotelGrandLake_Text_Guest2:
	.string "This hotel has such a lovely view\n"
	.string "of the lake.$"

HotelGrandLake_Text_Guest3:
	.string "The fishing spots nearby are\n"
	.string "some of the best in SINNOH.$"

HotelGrandLake_Text_Guest4:
	.string "Ahh, nothing beats a quiet cup of\n"
	.string "tea after a long trip.$"
