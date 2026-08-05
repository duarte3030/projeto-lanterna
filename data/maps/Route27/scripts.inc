@ Treinadores de rota de Route27, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route27_MapScripts::
	.byte 0

Route27_EventScript_Blake::
	trainerbattle_single TRAINER_JOHTO_BLAKE, Route27_Text_BlakeSeen, Route27_Text_BlakeBeaten
	msgbox Route27_Text_BlakeAfter, MSGBOX_AUTOCLOSE
	end

Route27_EventScript_Brian::
	trainerbattle_single TRAINER_JOHTO_BRIAN, Route27_Text_BrianSeen, Route27_Text_BrianBeaten
	msgbox Route27_Text_BrianAfter, MSGBOX_AUTOCLOSE
	end

Route27_EventScript_Reena::
	trainerbattle_single TRAINER_JOHTO_REENA, Route27_Text_ReenaSeen, Route27_Text_ReenaBeaten
	msgbox Route27_Text_ReenaAfter, MSGBOX_AUTOCLOSE
	end

Route27_EventScript_Megan::
	trainerbattle_single TRAINER_JOHTO_MEGAN, Route27_Text_MeganSeen, Route27_Text_MeganBeaten
	msgbox Route27_Text_MeganAfter, MSGBOX_AUTOCLOSE
	end

Route27_EventScript_Gilbert::
	trainerbattle_single TRAINER_JOHTO_GILBERT, Route27_Text_GilbertSeen, Route27_Text_GilbertBeaten
	msgbox Route27_Text_GilbertAfter, MSGBOX_AUTOCLOSE
	end

Route27_EventScript_Jose::
	trainerbattle_single TRAINER_JOHTO_JOSE, Route27_Text_JoseSeen, Route27_Text_JoseBeaten
	msgbox Route27_Text_JoseAfter, MSGBOX_AUTOCLOSE
	end

Route27_EventScript_Scott::
	trainerbattle_single TRAINER_JOHTO_SCOTT, Route27_Text_ScottSeen, Route27_Text_ScottBeaten
	msgbox Route27_Text_ScottAfter, MSGBOX_AUTOCLOSE
	end

Route27_Text_BlakeSeen:
	.string "You look pretty strong.\n"
	.string "Let me battle you!$"

Route27_Text_BlakeBeaten:
	.string "Yow!$"

Route27_Text_BlakeAfter:
	.string "If you prevail on this harsh trek,\n"
	.string "the truth will be revealed!\p"
	.string "Heh, sorry, I just wanted to say\n"
	.string "something cool.$"

Route27_Text_BrianSeen:
	.string "Hm? You're good, aren't you?$"

Route27_Text_BrianBeaten:
	.string "Just as I thought!$"

Route27_Text_BrianAfter:
	.string "A good trainer can recognize other\n"
	.string "good trainers.$"

Route27_Text_ReenaSeen:
	.string "You shouldn't underestimate the\n"
	.string "wild POKéMON in these parts.$"

Route27_Text_ReenaBeaten:
	.string "Oh! You're much too strong!$"

Route27_Text_ReenaAfter:
	.string "You're just a kid, but you're not\n"
	.string "to be underestimated either.$"

Route27_Text_MeganSeen:
	.string "It's rare to see anyone come here.\p"
	.string "Are you training on your own?$"

Route27_Text_MeganBeaten:
	.string "Oh! You're really strong!$"

Route27_Text_MeganAfter:
	.string "I'm checking out pre- and post-\n"
	.string "evolution POKéMON.\p"
	.string "Evolution really does make\n"
	.string "POKéMON stronger.\p"
	.string "But evolved forms also learn\n"
	.string "moves later on.$"

Route27_Text_GilbertSeen:
	.string "Don't say a thing!\p"
	.string "Let me guess what you're thinking.\p"
	.string "Mmmmmmm…\p"
	.string "I got it! You're on the POKéMON\n"
	.string "LEAGUE challenge!$"

Route27_Text_GilbertBeaten:
	.string "You're too much!$"

Route27_Text_GilbertAfter:
	.string "With your skills, you'll do well at\n"
	.string "the LEAGUE.\p"
	.string "That's what my premonition says.$"

Route27_Text_JoseSeen:
	.string "Tweet! Tweet! Tetweet!$"

Route27_Text_JoseBeaten:
	.string "Tweet!$"

Route27_Text_JoseAfter:
	.string "BIRD KEEPERS like me mimic bird\n"
	.string "whistles to command POKéMON.$"

Route27_Text_ScottSeen:
	.string "I'm feeling great today!\p"
	.string "I feel like I could boot even the\n"
	.string "LEAGUE CHAMP!$"

Route27_Text_ScottBeaten:
	.string "No! Not in this battle!$"

Route27_Text_ScottAfter:
	.string "Just like in fishing, it's all over\n"
	.string "in POKéMON if you give up.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route27_EventScript_TohjoFallsSign::
    msgbox TohjoFalls_Text_Sign, MSGBOX_SIGN
    end

TohjoFalls_Text_Sign::
    .string "TOHJO FALLS\p"
    .string "THE LINK BETWEEN KANTO AND JOHTO$"
