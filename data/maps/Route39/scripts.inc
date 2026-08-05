@ Treinadores de rota de Route39, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route39_MapScripts::
	.byte 0

Route39_EventScript_Eugene::
	trainerbattle_single TRAINER_JOHTO_EUGENE, Route39_Text_EugeneSeen, Route39_Text_EugeneBeaten
	msgbox Route39_Text_EugeneAfter, MSGBOX_AUTOCLOSE
	end

Route39_EventScript_Derek::
	trainerbattle_single TRAINER_JOHTO_DEREK, Route39_Text_DerekSeen, Route39_Text_DerekBeaten
	msgbox Route39_Text_DerekAfter, MSGBOX_AUTOCLOSE
	end

Route39_EventScript_Ruth::
	trainerbattle_single TRAINER_JOHTO_RUTH, Route39_Text_RuthSeen, Route39_Text_RuthBeaten
	msgbox Route39_Text_RuthAfter, MSGBOX_AUTOCLOSE
	end

Route39_EventScript_Norman::
	trainerbattle_single TRAINER_JOHTO_NORMAN, Route39_Text_NormanSeen, Route39_Text_NormanBeaten
	msgbox Route39_Text_NormanAfter, MSGBOX_AUTOCLOSE
	end

Route39_EventScript_Jamie::
	trainerbattle_single TRAINER_JOHTO_JAMIE, Route39_Text_JamieSeen, Route39_Text_JamieBeaten
	msgbox Route39_Text_JamieAfter, MSGBOX_AUTOCLOSE
	end

Route39_Text_EugeneSeen:
	.string "I just got back to OLIVINE.\p"
	.string "So how about a POKéMON battle?$"

Route39_Text_EugeneBeaten:
	.string "Awaaargh!$"

Route39_Text_EugeneAfter:
	.string "My POKéMON were caught and\n"
	.string "raised overseas.\p"
	.string "They're my companions on\n"
	.string "those long voyages.$"

Route39_Text_DerekSeen:
	.string "This is a good time to brag\n"
	.string "about my PIKACHU!$"

Route39_Text_DerekBeaten:
	.string "I had no time to show off\n"
	.string "PIKACHU…$"

Route39_Text_DerekAfter:
	.string "I'm not listening to your\n"
	.string "bragging!\p"
	.string "We POKé FANS have a policy\n"
	.string "of not listening to bragging!$"

Route39_Text_RuthSeen:
	.string "Such darling POKéMON.\p"
	.string "Let's show our POKéMON\n"
	.string "together at the same time.$"

Route39_Text_RuthBeaten:
	.string "I don't mind losing.$"

Route39_Text_RuthAfter:
	.string "Do you know about baby\n"
	.string "POKéMON?\p"
	.string "I bet they're just adorable!$"

Route39_Text_NormanSeen:
	.string "Let me see what your\n"
	.string "POKéMON are capable of.$"

Route39_Text_NormanBeaten:
	.string "Ooh, your POKéMON have\n"
	.string "potential.$"

Route39_Text_NormanAfter:
	.string "You know how POKéMON have\n"
	.string "different abilities?\p"
	.string "People are like that too.\n"
	.string "Everyone has different\l"
	.string "potential.$"

Route39_Text_JamieSeen:
	.string "You came at just the right\n"
	.string "time.\p"
	.string "Let's battle.$"

Route39_Text_JamieBeaten:
	.string "Oh, how disappointing…$"

Route39_Text_JamieAfter:
	.string "I met UMBREON at night right\n"
	.string "here on ROUTE 39.\p"
	.string "I'm not sure why, but it\n"
	.string "seems to like it when I\l"
	.string "train here.\p"
	.string "It seems to become friendlier\n"
	.string "by training here than\l"
	.string "anywhere else.$"
