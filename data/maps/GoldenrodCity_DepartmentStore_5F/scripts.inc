GoldenrodCity_DepartmentStore_5F_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodDeptStore5_EventScript_Sign::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_5FDirectory, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_5FDirectory::
    .string "Customize Your POKéMON\p"
    .string "5F TM CORNER$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodDeptStore_Text_5FReceptionistOhYourMon::
    .string "Hello. Oh, your POKéMON…$"

GoldenrodCity_DepartmentStore_5F_EventScript_ReceptionistFala::
	msgbox GoldenrodDeptStore_Text_5FReceptionistOhYourMon, MSGBOX_NPC
	end

GoldenrodDeptStore5_EventScript_Girl::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_Girl, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_Girl::
	.string "The lady gave me RETURN!\n"
    .string "My POKéMON must really like me!$"

GoldenrodDeptStore5_EventScript_Lass::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_5FLass, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_5FLass::
    .string "During the day, a lady comes to check\n"
    .string "out POKéMON.\p"
    .string "She even gives away TMs!$"

GoldenrodDeptStore5_EventScript_PokefanM::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_5FPokefanM, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_5FPokefanM::
    .string "You can't rename a POKéMON you get\n"
    .string "in a trade.\p"
    .string "The name is a reflection of the\n"
    .string "original trainer's feelings for it.$"
