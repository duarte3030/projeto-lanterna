GoldenrodCity_DepartmentStore_6F_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodDeptStore6_EventScript_Sign::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_6FDirectory, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_6FDirectory::
    .string "Take a Break from Shopping!\p"
    .string "6F TRANQUIL SQUARE$"
