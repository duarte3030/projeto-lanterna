@ Treinadores de rota de MtMortar_1F_North, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

MtMortar_1F_North_MapScripts::
	.byte 0

MtMortar_1F_North_EventScript_Miller::
	trainerbattle_single TRAINER_JOHTO_MILLER, MtMortar_1F_North_Text_MillerSeen, MtMortar_1F_North_Text_MillerBeaten
	msgbox MtMortar_1F_North_Text_MillerAfter, MSGBOX_AUTOCLOSE
	end

MtMortar_1F_North_EventScript_Markus::
	trainerbattle_single TRAINER_JOHTO_MARKUS, MtMortar_1F_North_Text_MarkusSeen, MtMortar_1F_North_Text_MarkusBeaten
	msgbox MtMortar_1F_North_Text_MarkusAfter, MSGBOX_AUTOCLOSE
	end

MtMortar_1F_North_Text_MillerSeen:
	.string "I'm not losing this time!$"

MtMortar_1F_North_Text_MillerBeaten:
	.string "I lost to some kid...?$"

MtMortar_1F_North_Text_MillerAfter:
	.string "A while back, this karate dude\n"
	.string "wanted to battle.\p"
	.string "He was ridiculously good.\n"
	.string "He just thrashed us silly.\p"
	.string "He went in deeper saying it\n"
	.string "was for his training.\p"
	.string "I wonder how he is?$"

MtMortar_1F_North_Text_MarkusSeen:
	.string "Hey! HUGH!$"

MtMortar_1F_North_Text_MarkusBeaten:
	.string "I mistook you for someone\n"
	.string "else…$"

MtMortar_1F_North_Text_MarkusAfter:
	.string "I came to explore MT.MORTAR,\n"
	.string "but I got separated from my\l"
	.string "partner…\p"
	.string "Did you run into a trainer\n"
	.string "who uses a SEADRA that knows\l"
	.string "WATERFALL?$"
