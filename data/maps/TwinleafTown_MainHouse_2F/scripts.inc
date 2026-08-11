TwinleafTown_MainHouse_2F_MapScripts::
	.byte 0

TwinleafTown_MainHouse_2F_EventScript_PC::
	msgbox TwinleafTown_MainHouse_2F_Text_PC, MSGBOX_SIGN
	end

@ E a TV que da o motivo da aventura: e nela que o jogador ouve falar do
@ ROWAN. Fala do Platinum, res/text/twinleaf_town_player_house_2f.json.
TwinleafTown_MainHouse_2F_EventScript_TV::
	msgbox TwinleafTown_MainHouse_2F_Text_TV, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_TV:
	.string "That concludes our special program,\n"
	.string "“Let's Ask PROF. ROWAN!”\p"
	.string "Brought to you by JUBILIFE TV on\n"
	.string "Nationwide Net!\p"
	.string "See you next week, same time,\n"
	.string "same channel!$"

TwinleafTown_MainHouse_2F_Text_PC:
	.string "POKéMON BASICS\p"
	.string "People live alongside POKéMON in\n"
	.string "this world. The people that battle\n"
	.string "POKéMON are called POKéMON Trainers.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TwinleafTown_MainHouse_2F_EventScript_Placa1::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa1, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa1:
	.string "It's a Wii!\nIt's controlled by a Wii Remote!$"

TwinleafTown_MainHouse_2F_EventScript_Placa2::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa2, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa2:
	.string "{PLAYER} checked the PC.\pPokémon Basics...\pPeople live alongside Pokémon in\nthis world.\pThe people that battle Pokémon are\ncalled Pokémon Trainers.$"

TwinleafTown_MainHouse_2F_EventScript_Placa3::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa3, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa3:
	.string "The X Button\nopens the menu!$"

TwinleafTown_MainHouse_2F_EventScript_Placa4::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa4, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa4:
	.string "Mom bought this TV as a gift.$"

TwinleafTown_MainHouse_2F_EventScript_Placa5::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa5, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa5:
	.string "Mom bought this TV as a gift.$"
