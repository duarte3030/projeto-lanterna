@ Treinadores de rota de Route42, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route42_MapScripts::
	.byte 0

Route42_EventScript_Tully::
	trainerbattle_single TRAINER_JOHTO_TULLY, Route42_Text_TullySeen, Route42_Text_TullyBeaten
	msgbox Route42_Text_TullyAfter, MSGBOX_AUTOCLOSE
	end

Route42_EventScript_Ben::
	trainerbattle_single TRAINER_JOHTO_BENJAMIN, Route42_Text_BenSeen, Route42_Text_BenBeaten
	msgbox Route42_Text_BenAfter, MSGBOX_AUTOCLOSE
	end

Route42_EventScript_Shane::
	trainerbattle_single TRAINER_JOHTO_SHANE, Route42_Text_ShaneSeen, Route42_Text_ShaneBeaten
	msgbox Route42_Text_ShaneAfter, MSGBOX_AUTOCLOSE
	end

Route42_Text_TullySeen:
	.string "Let me demonstrate the power\n"
	.string "of the POKéMON I caught!$"

Route42_Text_TullyBeaten:
	.string "What? That's not right.\n"
	.string "I can't believe this!$"

Route42_Text_TullyAfter:
	.string "I want to become the trainer\n"
	.string "CHAMP using the POKéMON I\l"
	.string "caught myself.\p"
	.string "That's the best part of fishing!$"

Route42_Text_BenSeen:
	.string "Ah, it's good to be outside!\n"
	.string "I feel so free!$"

Route42_Text_BenBeaten:
	.string "Gahahah! That was a good\n"
	.string "battle!$"

Route42_Text_BenAfter:
	.string "Losing feels insignificant\n"
	.string "if you look up at the big sky!$"

Route42_Text_ShaneSeen:
	.string "HEY!\p"
	.string "This is my secret place!\n"
	.string "Get lost, you outsider!$"

Route42_Text_ShaneBeaten:
	.string "I should have used my\n"
	.string "MOON STONE…$"

Route42_Text_ShaneAfter:
	.string "You're working on a POKéDEX?\p"
	.string "Wow, you must know some\n"
	.string "pretty rare POKéMON!\p"
	.string "May I please see it?\n"
	.string "Please?$"
