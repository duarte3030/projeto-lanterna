GoldenrodCity_BillsHouse_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

BillHouse_Text_SisterStorageSystem::
    .string "My big brother BILL made the PC\n"
    .string "POKéMON storage system.$"

GoldenrodCity_BillsHouse_EventScript_Sister::
	lock
	faceplayer
	msgbox BillHouse_Text_SisterStorageSystem, MSGBOX_DEFAULT
	closemessage
	release
	end
