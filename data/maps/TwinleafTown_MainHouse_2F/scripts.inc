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
