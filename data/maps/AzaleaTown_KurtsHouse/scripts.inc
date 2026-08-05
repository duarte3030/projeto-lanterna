AzaleaTown_KurtsHouse_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

AzaleaTown_KurtsHouse_EventScript_CelebiStatue::
	msgbox KurtsHouse_Text_CelebiStatue, MSGBOX_SIGN
	closemessage
	end

AzaleaTown_KurtsHouse_EventScript_OakPhoto::
	msgbox KurtsHouse_Text_OakPhoto, MSGBOX_SIGN
	closemessage
	end

KurtsHouse_Text_CelebiStatue::
	.string "It's a statue of the forest's\n"
	.string "protector.$"

KurtsHouse_Text_OakPhoto::
	.string "…A young PROF. OAK?$"
