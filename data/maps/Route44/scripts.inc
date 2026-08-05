@ Treinadores de rota de Route44, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route44_MapScripts::
	.byte 0

Route44_EventScript_Wilton::
	trainerbattle_single TRAINER_JOHTO_WILTON, Route44_Text_WiltonSeen, Route44_Text_WiltonBeaten
	msgbox Route44_Text_WiltonAfter, MSGBOX_AUTOCLOSE
	end

Route44_EventScript_Edgar::
	trainerbattle_single TRAINER_JOHTO_EDGAR, Route44_Text_EdgarSeen, Route44_Text_EdgarBeaten
	msgbox Route44_Text_EdgarAfter, MSGBOX_AUTOCLOSE
	end

Route44_EventScript_Vance::
	trainerbattle_single TRAINER_JOHTO_VANCE, Route44_Text_VanceSeen, Route44_Text_VanceBeaten
	msgbox Route44_Text_VanceAfter, MSGBOX_AUTOCLOSE
	end

Route44_EventScript_Phil::
	trainerbattle_single TRAINER_JOHTO_PHIL, Route44_Text_PhilSeen, Route44_Text_PhilBeaten
	msgbox Route44_Text_PhilAfter, MSGBOX_AUTOCLOSE
	end

Route44_EventScript_Zach::
	trainerbattle_single TRAINER_JOHTO_ZACH, Route44_Text_ZachSeen, Route44_Text_ZachBeaten
	msgbox Route44_Text_ZachAfter, MSGBOX_AUTOCLOSE
	end

Route44_EventScript_Allen::
	trainerbattle_single TRAINER_JOHTO_ALLEN, Route44_Text_AllenSeen, Route44_Text_AllenBeaten
	msgbox Route44_Text_AllenAfter, MSGBOX_AUTOCLOSE
	end

Route44_EventScript_Cybil::
	trainerbattle_single TRAINER_JOHTO_CYBIL, Route44_Text_CybilSeen, Route44_Text_CybilBeaten
	msgbox Route44_Text_CybilAfter, MSGBOX_AUTOCLOSE
	end

Route44_Text_WiltonSeen:
	.string "Aack!\p"
	.string "You made me lose a POLIWAG!\n"
	.string "What are you going to do about it?$"

Route44_Text_WiltonBeaten:
	.string "Just forget about it.$"

Route44_Text_WiltonAfter:
	.string "That POLIWAG that got away…\n"
	.string "it was huge.\p"
	.string "I swear it must've been\n"
	.string "16 feet long!$"

Route44_Text_EdgarSeen:
	.string "I fish until I can't anymore.\p"
	.string "I also battle until I drop.\p"
	.string "That's my relationship with my\n"
	.string "POKéMON.$"

Route44_Text_EdgarBeaten:
	.string "Hmmmm… This isn't right.$"

Route44_Text_EdgarAfter:
	.string "That's 100 wins to 101 losses.\p"
	.string "I won't battle again for a while.$"

Route44_Text_VanceSeen:
	.string "Do you know about the legendary\n"
	.string "bird POKéMON?$"

Route44_Text_VanceBeaten:
	.string "Whew! You're hot stuff.$"

Route44_Text_VanceAfter:
	.string "ARTICUNO, ZAPDOS and MOLTRES are\n"
	.string "the three legendary bird POKéMON.\p"
	.string "I heard there are other legendary\n"
	.string "birds, though.$"

Route44_Text_PhilSeen:
	.string "I'm gonna win, for sure!$"

Route44_Text_PhilBeaten:
	.string "Arrgh… That's a shocking loss…$"

Route44_Text_PhilAfter:
	.string "It's important to have conviction\n"
	.string "on your side.$"

Route44_Text_ZachSeen:
	.string "I'll do anything to get my hands\n"
	.string "on rare POKéMON!$"

Route44_Text_ZachBeaten:
	.string "Oooh, your POKéMON are so\n"
	.string "appealing.$"

Route44_Text_ZachAfter:
	.string "If a POKéMON has different colors\n"
	.string "from usual, it's more valuable.\p"
	.string "What? You mean that's not true?$"

Route44_Text_AllenSeen:
	.string "I can tell you're a good trainer\n"
	.string "by looking at you.\p"
	.string "I'm good at POKéMON, and I can\n"
	.string "see that you are too.$"

Route44_Text_AllenBeaten:
	.string "Tch! It's a total loss on my part.$"

Route44_Text_AllenAfter:
	.string "Wow. You have a lot of BADGES.\p"
	.string "No wonder you're so tough.\p"
	.string "I wonder if ECRUTEAK GYM's MORTY\n"
	.string "is still in training?\p"
	.string "He really hammered me.$"

Route44_Text_CybilSeen:
	.string "You look strong.\p"
	.string "Good trainers seek tough\n"
	.string "opponents instinctively.$"

Route44_Text_CybilBeaten:
	.string "Nope! This won't do at all.$"

Route44_Text_CybilAfter:
	.string "We all get better by experiencing\n"
	.string "many battles.\p"
	.string "I battled a lot to become what I\n"
	.string "am today--an elite.$"
