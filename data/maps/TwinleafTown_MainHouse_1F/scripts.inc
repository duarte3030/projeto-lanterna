TwinleafTown_MainHouse_1F_MapScripts::
	.byte 0

TwinleafTown_MainHouse_1F_EventScript_Mom::
	lock
	faceplayer
	msgbox TwinleafTown_MainHouse_1F_Text_Mom, MSGBOX_DEFAULT
	release
	end

TwinleafTown_MainHouse_1F_Text_Mom:
	.string "Take care of yourself out there,\n"
	.string "dear, and don't forget to visit\n"
	.string "sometimes!$"
