SolaceonRuinsRoom3_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

SolaceonRuinsRoom3_EventScript_RuinManiacKarl::
	trainerbattle_single TRAINER_SINNOH_RUIN_MANIAC_KARL, SolaceonRuinsRoom3_Text_RuinManiacKarlIntro, SolaceonRuinsRoom3_Text_RuinManiacKarlDefeat
	msgbox SolaceonRuinsRoom3_Text_RuinManiacKarlPost, MSGBOX_AUTOCLOSE
	end

SolaceonRuinsRoom3_Text_RuinManiacKarlIntro:
	.string "Ancient ruins rife with the UNOWN...\nThere has to be a meaning!\pBut its significance eludes me, and\nthat's gotten me cranky!$"

SolaceonRuinsRoom3_Text_RuinManiacKarlDefeat:
	.string "The search must continue!$"

SolaceonRuinsRoom3_Text_RuinManiacKarlPost:
	.string "The significance of the ancient ruins...\pOnly Pokémon that look like the letters\nof some strange language...\pCan they be trying to convey a message\nto us?$"
