Route29_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route29_EventScript_Sign::
	lock
	msgbox Route29_Text_Sign1, MSGBOX_SIGN
	closemessage
	release
	end

Route29_Text_Sign1::
	.string "ROUTE 29\p"
	.string "CHERRYGROVE CITY - NEW BARK TOWN$"
