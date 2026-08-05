@ Treinadores de rota de Route43, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route43_MapScripts::
	.byte 0

Route43_EventScript_Ben::
	trainerbattle_single TRAINER_JOHTO_BEN, Route43_Text_BenSeen, Route43_Text_BenBeaten
	msgbox Route43_Text_BenAfter, MSGBOX_AUTOCLOSE
	end

Route43_EventScript_Brent::
	trainerbattle_single TRAINER_JOHTO_BRENT, Route43_Text_BrentSeen, Route43_Text_BrentBeaten
	msgbox Route43_Text_BrentAfter, MSGBOX_AUTOCLOSE
	end

Route43_EventScript_Ron::
	trainerbattle_single TRAINER_JOHTO_RON, Route43_Text_RonSeen, Route43_Text_RonBeaten
	msgbox Route43_Text_RonAfter, MSGBOX_AUTOCLOSE
	end

Route43_EventScript_Marvin::
	trainerbattle_single TRAINER_JOHTO_MARVIN, Route43_Text_MarvinSeen, Route43_Text_MarvinBeaten
	msgbox Route43_Text_MarvinAfter, MSGBOX_AUTOCLOSE
	end

Route43_EventScript_Spencer::
	trainerbattle_single TRAINER_JOHTO_SPENCER, Route43_Text_SpencerSeen, Route43_Text_SpencerBeaten
	msgbox Route43_Text_SpencerAfter, MSGBOX_AUTOCLOSE
	end

Route43_EventScript_Tiffany::
	trainerbattle_single TRAINER_JOHTO_TIFFANY, Route43_Text_TiffanySeen, Route43_Text_TiffanyBeaten
	msgbox Route43_Text_TiffanyAfter, MSGBOX_AUTOCLOSE
	end

Route43_Text_BenSeen:
	.string "I love POKéMON!\p"
	.string "That's why I started--and why I'll\n"
	.string "keep on collecting POKéMON!$"

Route43_Text_BenBeaten:
	.string "How could you do this to me?$"

Route43_Text_BenAfter:
	.string "What else do I like besides\n"
	.string "POKéMON?\p"
	.string "MARY on the radio. I bet she's\n"
	.string "cute!$"

Route43_Text_BrentSeen:
	.string "Hey! Do you have any rare\n"
	.string "POKéMON?$"

Route43_Text_BrentBeaten:
	.string "Oh, my poor POKéMON! Darlings!$"

Route43_Text_BrentAfter:
	.string "I'd be happy just to own a single\n"
	.string "rare POKéMON.$"

Route43_Text_RonSeen:
	.string "Would you get this?\p"
	.string "Some your rival guy made fun of my\n"
	.string "POKéMON!\p"
	.string "Darn it! My POKéMON's great!$"

Route43_Text_RonBeaten:
	.string "My NIDOKING did pretty right on!$"

Route43_Text_RonAfter:
	.string "It's okay for people to like\n"
	.string "different types of POKéMON.\p"
	.string "POKéMON isn't just about having the\n"
	.string "most powerful one.$"

Route43_Text_MarvinSeen:
	.string "I'm in a slump.\p"
	.string "Maybe it's the gear I'm using.\p"
	.string "Let's battle for a change of pace!$"

Route43_Text_MarvinBeaten:
	.string "I lost, but I feel better anyway.$"

Route43_Text_MarvinAfter:
	.string "KURT's LURE BALL is the best for\n"
	.string "catching hooked POKéMON.\p"
	.string "It's much more effective than a\n"
	.string "ULTRA BALL.$"

Route43_Text_SpencerSeen:
	.string "I can do so much with my\n"
	.string "POKéMON--it's super-fun!$"

Route43_Text_SpencerBeaten:
	.string "Losing isn't fun at all…$"

Route43_Text_SpencerAfter:
	.string "What is going on at LAKE OF RAGE?\p"
	.string "We were planning to camp there.$"

Route43_Text_TiffanySeen:
	.string "Are you going to LAKE OF RAGE too?\p"
	.string "Let's play for a little while!$"

Route43_Text_TiffanyBeaten:
	.string "I played too much!$"

Route43_Text_TiffanyAfter:
	.string "I'm having a picnic with POKéMON.\p"
	.string "Won't you join us?$"
