@ Treinadores de rota de MtMortar_2F, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

MtMortar_2F_MapScripts::
	.byte 0

MtMortar_2F_EventScript_Nerd::
	trainerbattle_single TRAINER_JOHTO_HUGH, MtMortar_2F_Text_NerdSeen, MtMortar_2F_Text_NerdBeaten
	msgbox MtMortar_2F_Text_NerdAfter, MSGBOX_AUTOCLOSE
	end

MtMortar_2F_Text_NerdSeen:
	.string "Yo! MARKUS!$"

MtMortar_2F_Text_NerdBeaten:
	.string "Sorry, my mistake.\n"
	.string "I misjudged you.$"

MtMortar_2F_Text_NerdAfter:
	.string "I'm investigating MT.MORTAR,\n"
	.string "but my pal's gone AWOL.\p"
	.string "Have you seen a trainer who\n"
	.string "has a SLOWPOKE that can use\l"
	.string "STRENGTH?$"
