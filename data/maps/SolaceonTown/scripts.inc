@ Textos vindos de pret/pokeplatinum (res/text/solaceon_town.json), em ingles.
@ Ver Pokemon Claude/SINNOH-PADRAO.md antes de mexer.

SolaceonTown_MapScripts::
	.byte 0

SolaceonTown_EventScript_Cowgirl1::
	msgbox SolaceonTown_Text_Cowgirl1, MSGBOX_NPC
	end

SolaceonTown_EventScript_DayCareMan::
	msgbox SolaceonTown_Text_DayCareMan, MSGBOX_NPC
	end

SolaceonTown_EventScript_RuinManiac::
	msgbox SolaceonTown_Text_RuinManiac, MSGBOX_NPC
	end

SolaceonTown_EventScript_Rancher1::
	msgbox SolaceonTown_Text_Rancher1, MSGBOX_NPC
	end

SolaceonTown_EventScript_Rancher2::
	msgbox SolaceonTown_Text_Rancher2, MSGBOX_NPC
	end

SolaceonTown_EventScript_Cowgirl2::
	msgbox SolaceonTown_Text_Cowgirl2, MSGBOX_NPC
	end

SolaceonTown_EventScript_DayCareSign::
	msgbox SolaceonTown_Text_DayCareSign, MSGBOX_SIGN
	end

SolaceonTown_EventScript_NewsPressSign::
	msgbox SolaceonTown_Text_NewsPressSign, MSGBOX_SIGN
	end

SolaceonTown_Text_Cowgirl1:
	.string "Howdy, traveling Trainer. Take it\n"
	.string "easy, slow, and casual.\p"
	.string "There's nothing here but plenty of\n"
	.string "time to think. Oh, right, we have\l"
	.string "the ruins. Why not tour through?$"

SolaceonTown_Text_DayCareMan:
	.string "My wife and I look after POKéMON\n"
	.string "here at the DAY-CARE.\p"
	.string "Leave a POKéMON with us, and we'll\n"
	.string "raise it while you're off training.$"

SolaceonTown_Text_RuinManiac:
	.string "A traveling Trainer, huh? Tell me,\n"
	.string "how many kinds of POKéMON have you\l"
	.string "met so far?\p"
	.string "If you're a competent Trainer, I'd\n"
	.string "think you'd've met at least fifty.$"

SolaceonTown_Text_Rancher1:
	.string "The MILTANK around here give the\n"
	.string "richest milk in all of SINNOH.$"

SolaceonTown_Text_Rancher2:
	.string "Nothing beats a quiet morning out\n"
	.string "in the pasture with the herd.$"

SolaceonTown_Text_Cowgirl2:
	.string "This town is small, but the air\n"
	.string "here is the freshest in all of\l"
	.string "SINNOH.$"

SolaceonTown_Text_DayCareSign:
	.string "POKéMON DAY CARE\p"
	.string "Leave your POKéMON here and we'll\n"
	.string "raise it for you.$"

SolaceonTown_Text_NewsPressSign:
	.string "SOLACEON TOWN POKéMON NEWS PRESS$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

SolaceonTown_EventScript_Placa2::
	msgbox SolaceonTown_Text_Placa2, MSGBOX_SIGN
	end

SolaceonTown_Text_Placa2:
	.string "Pokémon Day Care\nLet Us Raise Your Pokémon$"

SolaceonTown_EventScript_Placa3::
	msgbox SolaceonTown_Text_Placa3, MSGBOX_SIGN
	end

SolaceonTown_Text_Placa3:
	.string "Pokémon News Press\nWanted: Pro Pokémon Catcher!$"
