GoldenrodCity_DepartmentStore_3F_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodDeptStore3_EventScript_Sign::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_3FDirectory, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_3FDirectory::
    .string "For Victory Seekers\p"
    .string "3F BATTLE COLLECTION$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodDeptStore3_EventScript_Nerd::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_3FSuperNerd, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_3FSuperNerd::
    .string "I, I, I'm really impatient!\p"
    .string "I use X SPEED in battle to speed up\n"
    .string "my POKéMON.$"

GoldenrodDeptStore3_EventScript_Rocker::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_3FRocker, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_3FRocker::
    .string "Hey! When you battle, do you use X\n"
    .string "SPECIAL?\p"
    .string "It's awesome. It really jacks up\n"
    .string "SPECIAL ATTACK!$"
