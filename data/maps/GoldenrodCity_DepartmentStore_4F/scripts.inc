GoldenrodCity_DepartmentStore_4F_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodDeptStore4_EventScript_Sign::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_4FDirectory, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_4FDirectory::
    .string "Let Us Pump Up Your POKéMON!\p"
    .string "4F MEDICINE BOX$"
