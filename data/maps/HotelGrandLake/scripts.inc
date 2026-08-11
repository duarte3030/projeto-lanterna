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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

HotelGrandLake_EventScript_Npc1::
	msgbox HotelGrandLake_Text_Npc1, MSGBOX_NPC
	end

HotelGrandLake_Text_Npc1:
	.string "This hotel is so romantic...\pI hope a knight on a Pokémon will\nsweep me away for a honeymoon here!$"

HotelGrandLake_EventScript_Npc2::
	msgbox HotelGrandLake_Text_Npc2, MSGBOX_NPC
	end

HotelGrandLake_Text_Npc2:
	.string "Ah, hello. You wish to stay a night?\nAh, but you've no reservations.\pI'm afraid we are totally booked.\nYou may rest a while, if you wish.$"
