GoldenrodCity_DepartmentStore_1F_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodDeptStore1_EventScript_Directory::
	lock
	msgbox GoldenrodDeptStore1_Text_Directory, MSGBOX_SIGN
	closemessage
	release
	end

GoldenrodDeptStore1_Text_Directory::
    .string "1F SERVICE COUNTER\n"
	.string "YOU ARE HERE.\p"
    .string "2F TRAINER'S MARKET\p"
    .string "3F BATTLE COLLECTION\p"
    .string "4F MEDICINE BOX\p"
    .string "5F TM CORNER\p"
    .string "6F TRANQUIL SQUARE\p"
    .string "ROOFTOP LOOKOUT$"
