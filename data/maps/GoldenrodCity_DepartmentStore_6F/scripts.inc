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

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodDeptStore6_EventScript_Nerd::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_6FSuperNerd, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_6FSuperNerd::
    .string "If you're tired, try the vending\n"
    .string "machine's drinks.\p"
    .string "Your POKéMON will love them too.$"

GoldenrodDeptStore6_EventScript_Lass::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_6FLass, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_6FLass::
    .string "Do you listen to LUCKY CHANNEL?\p"
    .string "They say if you want to win,\n"
	.string "you should trade POKéMON with as\l"
    .string "many people as possible to get\l"
    .string "different ID numbers.\p"
	.string "However, trading isn't as widely\n"
	.string "available as it once was.$"
