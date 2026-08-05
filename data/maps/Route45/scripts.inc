@ Treinadores de rota de Route45, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route45_MapScripts::
	.byte 0

Route45_EventScript_Erik::
	trainerbattle_single TRAINER_JOHTO_ERIK, Route45_Text_ErikSeen, Route45_Text_ErikBeaten
	msgbox Route45_Text_ErikAfter, MSGBOX_AUTOCLOSE
	end

Route45_EventScript_Michael::
	trainerbattle_single TRAINER_JOHTO_MICHAEL, Route45_Text_MichaelSeen, Route45_Text_MichaelBeaten
	msgbox Route45_Text_MichaelAfter, MSGBOX_AUTOCLOSE
	end

Route45_EventScript_Parry::
	trainerbattle_single TRAINER_JOHTO_PARRY, Route45_Text_ParrySeen, Route45_Text_ParryBeaten
	msgbox Route45_Text_ParryAfter, MSGBOX_AUTOCLOSE
	end

Route45_EventScript_Timothy::
	trainerbattle_single TRAINER_JOHTO_TIMOTHY, Route45_Text_TimothySeen, Route45_Text_TimothyBeaten
	msgbox Route45_Text_TimothyAfter, MSGBOX_AUTOCLOSE
	end

Route45_EventScript_Kenji::
	trainerbattle_single TRAINER_JOHTO_KENJI, Route45_Text_KenjiSeen, Route45_Text_KenjiBeaten
	msgbox Route45_Text_KenjiAfter, MSGBOX_AUTOCLOSE
	end

Route45_EventScript_Ryan::
	trainerbattle_single TRAINER_JOHTO_RYAN, Route45_Text_RyanSeen, Route45_Text_RyanBeaten
	msgbox Route45_Text_RyanAfter, MSGBOX_AUTOCLOSE
	end

Route45_EventScript_Kelly::
	trainerbattle_single TRAINER_JOHTO_KELLY, Route45_Text_KellySeen, Route45_Text_KellyBeaten
	msgbox Route45_Text_KellyAfter, MSGBOX_AUTOCLOSE
	end

Route45_EventScript_Quentin::
	trainerbattle_single TRAINER_JOHTO_QUENTIN, Route45_Text_QuentinSeen, Route45_Text_QuentinBeaten
	msgbox Route45_Text_QuentinAfter, MSGBOX_AUTOCLOSE
	end

Route45_Text_ErikSeen:
	.string "Be prepared for anything!\p"
	.string "Let me see if your POKéMON have\n"
	.string "been raised properly!$"

Route45_Text_ErikBeaten:
	.string "Oh, I lost that!$"

Route45_Text_ErikAfter:
	.string "I'll head back to BLACKTHORN's\n"
	.string "ICE PATH and train some more.$"

Route45_Text_MichaelSeen:
	.string "Yo! You're spunky! But you know\n"
	.string "what?\p"
	.string "When it comes to sheer\n"
	.string "spunkiness, I'm the man!$"

Route45_Text_MichaelBeaten:
	.string "My POKéMON weren't spunky enough!$"

Route45_Text_MichaelAfter:
	.string "Boy, do I love HP UP! Mmmm, yum!\p"
	.string "I keep drinking my POKéMON's!\p"
	.string "I can't help it!$"

Route45_Text_ParrySeen:
	.string "My POKéMON are power packed!$"

Route45_Text_ParryBeaten:
	.string "Wahahah! I'm the big loser!$"

Route45_Text_ParryAfter:
	.string "I'm not much good at thinking,\n"
	.string "see?\p"
	.string "So, I just plow ahead with power!$"

Route45_Text_TimothySeen:
	.string "Why do I climb mountains?\p"
	.string "Because they're there.\p"
	.string "Why do I train POKéMON?\p"
	.string "Because they're there!$"

Route45_Text_TimothyBeaten:
	.string "Losses… They're there too!$"

Route45_Text_TimothyAfter:
	.string "The best thing to ever happen to\n"
	.string "me was discovering POKéMON.$"

Route45_Text_KenjiSeen:
	.string "I was training here alone.\p"
	.string "Behold the fruits of my labor!$"

Route45_Text_KenjiBeaten:
	.string "Waaaargh!$"

Route45_Text_KenjiAfter:
	.string "This calls for extreme measures.\p"
	.string "I must take to the hills and train\n"
	.string "in solitude.$"

Route45_Text_RyanSeen:
	.string "What are your thoughts on\n"
	.string "raising POKéMON?$"

Route45_Text_RyanBeaten:
	.string "You've won my respect.$"

Route45_Text_RyanAfter:
	.string "I see you're raising your POKéMON\n"
	.string "with care.\p"
	.string "The bond you build will save you\n"
	.string "in tough situations.$"

Route45_Text_KellySeen:
	.string "What is your battle strategy?\p"
	.string "It is foolish to use strong moves\n"
	.string "indiscriminately.$"

Route45_Text_KellyBeaten:
	.string "Fine. I lost.$"

Route45_Text_KellyAfter:
	.string "I'm not in favor of overly\n"
	.string "powerful moves.\p"
	.string "I want to win, but I also don't\n"
	.string "want to harm POKéMON.$"

Route45_Text_QuentinSeen:
	.string "I'm really, really tough!$"

Route45_Text_QuentinBeaten:
	.string "I was tough at the TRAINER HILL…$"

Route45_Text_QuentinAfter:
	.string "Have you been to the TRAINER HILL?\p"
	.string "I never, ever lose there, but…$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route45_EventScript_Sign::
	msgbox Route45_Text_Sign, MSGBOX_SIGN
	end

Route45_Text_Sign::
    .string "ROUTE 45\n"
    .string "MOUNTAIN RD. AHEAD$"
