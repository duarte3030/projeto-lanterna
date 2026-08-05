EcruteakCity_Theater_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

EcruteakCity_Theater_EventScript_FancyPanel::
	lock
	msgbox EcruteakCity_Theater_Text_FancyPanel, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Theater_Text_FancyPanel::
	.string "It's a fancy panel that's\n"
	.string "decorated with flowers.$"
