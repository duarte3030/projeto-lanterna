Mahoganytown_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

MahoganyTown_EventScript_CandybarSign::
	lock
	msgbox MahoganyTown_Text_RagecandybarSign, MSGBOX_SIGN
	closemessage
	release
	end

MahoganyTown_EventScript_GymSign::
	lock
	msgbox MahoganyTown_Text_GymSign, MSGBOX_SIGN
	closemessage
	release
	end

MahoganyTown_EventScript_Sign::
	lock
	msgbox MahoganyTown_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

MahoganyTown_Text_GymSign::
    .string "MAHOGANY TOWN POKéMON GYM\p"
    .string "LEADER: PRYCE\p"
    .string "The Teacher of Winter's Harshness$"

MahoganyTown_Text_RagecandybarSign::
    .string "While visiting MAHOGANY TOWN, try\n"
    .string "a RAGECANDYBAR!$"

MahoganyTown_Text_Sign::
    .string "MAHOGANY TOWN\p"
    .string "Welcome to the Home of the Ninja$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

MahoganyTown_EventScript_Lass::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyTown_Text_Lass::
    .string "Visit Grandma's shop. She sells\n"
    .string "stuff that nobody else has.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

MahoganyTown_EventScript_Fisher::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyTown_Text_Fisher::
    .string "Since you came this far, take the\n"
    .string "time to do some sightseeing.\p"
    .string "You should head north and check\n"
    .string "out LAKE OF RAGE right now.$"
