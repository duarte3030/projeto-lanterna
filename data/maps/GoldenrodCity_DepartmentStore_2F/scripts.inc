GoldenrodCity_DepartmentStore_2F_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodDeptStore2_EventScript_Sign::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_2FDirectory, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_2FDirectory::
    .string "Your Travel Companion\p"
    .string "2F TRAINER'S MARKET$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodDeptStore2_EventScript_Gent::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_2FGentleman, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_2FGentleman::
    .string "This DEPT.STORE makes me realize\n"
    .string "that GOLDENROD is a big city.\p"
    .string "The selection here is unmatched\n"
    .string "anywhere else.$"

GoldenrodDeptStore2_EventScript_Youngster::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_2FYoungster, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_2FYoungster::
    .string "POKéGEAR can store up to 25 phone\n"
    .string "numbers.\p"
    .string "It's hard to decide which numbers\n"
    .string "to keep.$"

GoldenrodDeptStore2_EventScript_CooltrainerF::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_2FCooltrainerF, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_2FCooltrainerF::
    .string "I got my ABRA at the GAME CORNER.\p"
    .string "Now it's my best partner.$"
