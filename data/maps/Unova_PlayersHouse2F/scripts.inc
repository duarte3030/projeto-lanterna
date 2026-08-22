@ PlayersHouse2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_PlayersHouse2F_MapScripts::
	.byte 0

Unova_PlayersHouse2F_EventScript_Placa1::
	msgbox Unova_PlayersHouse2F_Text_PlayersRadioText4, MSGBOX_SIGN
	end


Unova_PlayersHouse2F_Text_PlayersRadioText4::
	.string "There's nothing"
	.string "\ninteresting on"
	.string "\lthe radio…$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Placas fechadas por dev_scripts/completa_placas_unova.py
Unova_PlayersHouse2F_EventScript_Poster::
	msgbox Unova_PlayersHouse2F_Text_Poster, MSGBOX_SIGN
	end

Unova_PlayersHouse2F_Text_Poster::
	.string "A POKéMON poster is stuck to\n"
	.string "the wall.$"
