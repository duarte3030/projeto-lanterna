@ Treinadores de rota de Route33, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route33_MapScripts::
	.byte 0

Route33_EventScript_HikerAnthony::
	trainerbattle_single TRAINER_JOHTO_ANTHONY, Route33_Text_HikerAnthonySeen, Route33_Text_HikerAnthonyBeaten
	msgbox Route33_Text_HikerAnthonyAfter, MSGBOX_AUTOCLOSE
	end

Route33_Text_HikerAnthonySeen:
	.string "I came through the tunnel,\n"
	.string "but I still have plenty\l"
	.string "of energy left.$"

Route33_Text_HikerAnthonyBeaten:
	.string "Whoa! You've got more zip\n"
	.string "than me!$"

Route33_Text_HikerAnthonyAfter:
	.string "We HIKERS are at our best\n"
	.string "in the mountains.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route33_EventScript_Lass::
	lock
	faceplayer
	msgbox Route33_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

Route33_Text_Lass::
	.string "Pant, pant…\p"
	.string "That cave was bigger than\n"
	.string "I'd expected.\p"
	.string "I got too tired exploring\n"
	.string "for MARILL, so I came outside.$"
