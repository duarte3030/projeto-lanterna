@ Treinadores de rota de GoldenrodCity_UndergroundTunnel, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

GoldenrodCity_UndergroundTunnel_MapScripts::
	.byte 0

GoldenrodCity_UndergroundTunnel_EventScript_Eric::
	trainerbattle_single TRAINER_JOHTO_ERIC, GoldenrodCity_UndergroundTunnel_Text_EricSeen, GoldenrodCity_UndergroundTunnel_Text_EricBeaten
	msgbox GoldenrodCity_UndergroundTunnel_Text_EricAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundTunnel_EventScript_Teru::
	trainerbattle_single TRAINER_JOHTO_TERU, GoldenrodCity_UndergroundTunnel_Text_TeruSeen, GoldenrodCity_UndergroundTunnel_Text_TeruBeaten
	msgbox GoldenrodCity_UndergroundTunnel_Text_TeruAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundTunnel_EventScript_Issac::
	trainerbattle_single TRAINER_JOHTO_ISSAC, GoldenrodCity_UndergroundTunnel_Text_IssacSeen, GoldenrodCity_UndergroundTunnel_Text_IssacBeaten
	msgbox GoldenrodCity_UndergroundTunnel_Text_IssacAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundTunnel_EventScript_Donald::
	trainerbattle_single TRAINER_JOHTO_DONALD, GoldenrodCity_UndergroundTunnel_Text_DonaldSeen, GoldenrodCity_UndergroundTunnel_Text_DonaldBeaten
	msgbox GoldenrodCity_UndergroundTunnel_Text_DonaldAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundTunnel_Text_EricSeen:
	.string "I got booted out of the GAME CORNER.\p"
	.string "I was trying to cheat using my\n"
	.string "POKéMON…$"

GoldenrodCity_UndergroundTunnel_Text_EricBeaten:
	.string "…Grumble…$"

GoldenrodCity_UndergroundTunnel_Text_EricAfter:
	.string "I guess I have to do things fair and\n"
	.string "square…$"

GoldenrodCity_UndergroundTunnel_Text_TeruSeen:
	.string "Do you consider type alignments in\n"
	.string "battle?\p"
	.string "If you know your type advantages,\n"
	.string "you'll do better in battle.$"

GoldenrodCity_UndergroundTunnel_Text_TeruBeaten:
	.string "Ow, ow, ow!$"

GoldenrodCity_UndergroundTunnel_Text_TeruAfter:
	.string "I know my POKéMON type alignments.\p"
	.string "But I only use one type of POKéMON.$"

GoldenrodCity_UndergroundTunnel_Text_IssacSeen:
	.string "My POKéMON just got a haircut!\p"
	.string "I'll show you how strong it is!$"

GoldenrodCity_UndergroundTunnel_Text_IssacBeaten:
	.string "Aiyeeee!$"

GoldenrodCity_UndergroundTunnel_Text_IssacAfter:
	.string "Your POKéMON will like you more if\n"
	.string "you give them haircuts.$"

GoldenrodCity_UndergroundTunnel_Text_DonaldSeen:
	.string "I think you have some rare POKéMON\n"
	.string "with you.\p"
	.string "Let me see them!$"

GoldenrodCity_UndergroundTunnel_Text_DonaldBeaten:
	.string "Gaah! I lost! That makes me mad!$"

GoldenrodCity_UndergroundTunnel_Text_DonaldAfter:
	.string "When I was walking near the BIKE\n"
	.string "SHOP last night, I felt like I was\l"
	.string "being watched from the rooftops...$"
