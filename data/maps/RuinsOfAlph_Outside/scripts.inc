@ Treinadores de rota de RuinsOfAlph_Outside, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

RuinsOfAlph_Outside_MapScripts::
	.byte 0

RuinsOfAlph_Outside_EventScript_Stan::
	trainerbattle_single TRAINER_JOHTO_STAN, RuinsOfAlph_Outside_Text_StanSeen, RuinsOfAlph_Outside_Text_StanBeaten
	msgbox RuinsOfAlph_Outside_Text_StanAfter, MSGBOX_AUTOCLOSE
	end

RuinsOfAlph_Outside_EventScript_Nathan::
	trainerbattle_single TRAINER_JOHTO_NATHAN, RuinsOfAlph_Outside_Text_NathanSeen, RuinsOfAlph_Outside_Text_NathanBeaten
	msgbox RuinsOfAlph_Outside_Text_NathanAfter, MSGBOX_AUTOCLOSE
	end

RuinsOfAlph_Outside_Text_StanSeen:
	.string "What do you want? I'm studying--\n"
	.string "don't disturb me!$"

RuinsOfAlph_Outside_Text_StanBeaten:
	.string "Sorry…\n"
	.string "I'm frustrated by our lack of\p"
	.string "real understanding…$"

RuinsOfAlph_Outside_Text_StanAfter:
	.string "The RUINS are from about 1500\n"
	.string "years ago.\p"
	.string "Nobody knows who built them.\p"
	.string "It's also not known if the POKéMON\n"
	.string "statues have any meaning.\p"
	.string "It's all one big mystery…$"

RuinsOfAlph_Outside_Text_NathanSeen:
	.string "Hmmm… This is a strange place.$"

RuinsOfAlph_Outside_Text_NathanBeaten:
	.string "…$"

RuinsOfAlph_Outside_Text_NathanAfter:
	.string "I like thinking here.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

RuinsOfAlph_Outside_EventScript_Sign1::
	lock
	msgbox RuinsOfAlph_Outside_Text_MainSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Sign2::
	lock
	msgbox RuinsOfAlph_Outside_Text_ResearchSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_EventScript_Sign3::
	lock
	msgbox RuinsOfAlph_Outside_Text_MysteryChamberSign, MSGBOX_SIGN
	closemessage
	release
	end

RuinsOfAlph_Outside_Text_MainSign::
	.string "RUINS OF ALPH\n"
	.string "VISITORS WELCOME$"

RuinsOfAlph_Outside_Text_MysteryChamberSign::
	.string "MYSTERY STONE PANEL CHAMBER$"

RuinsOfAlph_Outside_Text_ResearchSign::
	.string "RUINS OF ALPH RESEARCH CENTER\p"
	.string "THE AUTHORITY ON THE\n"
	.string "RUINS OF ALPH$"
