@ Treinadores de rota de NationalPark_Normal, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

NationalPark_Normal_MapScripts::
	.byte 0

NationalPark_Normal_EventScript_Jack::
	trainerbattle_single TRAINER_JOHTO_JACK, NationalPark_Normal_Text_JackSeen, NationalPark_Normal_Text_JackBeaten
	msgbox NationalPark_Normal_Text_JackAfter, MSGBOX_AUTOCLOSE
	end

NationalPark_Normal_EventScript_Beverly::
	trainerbattle_single TRAINER_JOHTO_BEVERLY, NationalPark_Normal_Text_BeverlySeen, NationalPark_Normal_Text_BeverlyBeaten
	msgbox NationalPark_Normal_Text_BeverlyAfter, MSGBOX_AUTOCLOSE
	end

NationalPark_Normal_EventScript_William::
	trainerbattle_single TRAINER_JOHTO_WILLIAM, NationalPark_Normal_Text_WilliamSeen, NationalPark_Normal_Text_WilliamBeaten
	msgbox NationalPark_Normal_Text_WilliamAfter, MSGBOX_AUTOCLOSE
	end

NationalPark_Normal_EventScript_Krise::
	trainerbattle_single TRAINER_JOHTO_KRISE, NationalPark_Normal_Text_KriseSeen, NationalPark_Normal_Text_KriseBeaten
	msgbox NationalPark_Normal_Text_KriseAfter, MSGBOX_AUTOCLOSE
	end

NationalPark_Normal_Text_JackSeen:
	.string "The world of POKéMON is deep.\p"
	.string "There are still lots of things we\n"
	.string "don't know.\p"
	.string "But I know more than you do!$"

NationalPark_Normal_Text_JackBeaten:
	.string "Wha-wha-what?$"

NationalPark_Normal_Text_JackAfter:
	.string "There is a lot to learn.\p"
	.string "For example…\p"
	.string "There are 50 kinds of TMs.\p"
	.string "Traded POKéMON level up faster.$"

NationalPark_Normal_Text_BeverlySeen:
	.string "My POKéMON are simply darling.\p"
	.string "Let me tell you how proud my\n"
	.string "darlings make me.$"

NationalPark_Normal_Text_BeverlyBeaten:
	.string "I can beat you in pride, but…$"

NationalPark_Normal_Text_BeverlyAfter:
	.string "I must say, your POKéMON are quite\n"
	.string "cute, too.$"

NationalPark_Normal_Text_WilliamSeen:
	.string "We adore our POKéMON, even if they\n"
	.string "dislike us.\p"
	.string "That's what being a FAN is about.$"

NationalPark_Normal_Text_WilliamBeaten:
	.string "M-my POKéMON!$"

NationalPark_Normal_Text_WilliamAfter:
	.string "I lost the battle, but my POKéMON win\n"
	.string "the prize for being most lovely.$"

NationalPark_Normal_Text_KriseSeen:
	.string "Hello? Why are you staring at me?\p"
	.string "Oh, a battle?$"

NationalPark_Normal_Text_KriseBeaten:
	.string "…Hmmm…$"

NationalPark_Normal_Text_KriseAfter:
	.string "I thought you were staring at me\n"
	.string "because I'm cute!$"
