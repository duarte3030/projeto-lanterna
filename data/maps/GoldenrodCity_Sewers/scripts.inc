@ Boca do esgoto de Goldenrod, copiada do mapa `g10m1` do Pokémon GS Chronicles.
@ A arte é do autor, byte a byte; o jogo é nosso, e o enredo da Equipe Rocket
@ dele NÃO entra (contrato, seção 1.2).
GoldenrodCity_Sewers_MapScripts::
	.byte 0

GoldenrodCity_Sewers_EventScript_Janitor::
	lock
	faceplayer
	msgbox GoldenrodCity_Sewers_Text_Janitor, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Sewers_EventScript_Gordon::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_1, GoldenrodCity_Sewers_Text_GordonSeen, GoldenrodCity_Sewers_Text_GordonBeaten
	msgbox GoldenrodCity_Sewers_Text_GordonAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_Sewers_EventScript_Brent::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_2, GoldenrodCity_Sewers_Text_BrentSeen, GoldenrodCity_Sewers_Text_BrentBeaten
	msgbox GoldenrodCity_Sewers_Text_BrentAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_Sewers_Text_Janitor:
	.string "Everything this city drops ends up\n"
	.string "down here sooner or later.\p"
	.string "Coins, keys, umbrellas…\n"
	.string "and the POKéMON that eat them.$"

GoldenrodCity_Sewers_Text_GordonSeen:
	.string "You can fish anywhere. The trick is\n"
	.string "fishing where nobody else will.$"

GoldenrodCity_Sewers_Text_GordonBeaten:
	.string "Should've stayed on the pier…$"

GoldenrodCity_Sewers_Text_GordonAfter:
	.string "The water down here never freezes\n"
	.string "and never runs out.\p"
	.string "Best spot in GOLDENROD, and it's\n"
	.string "all mine.$"

GoldenrodCity_Sewers_Text_BrentSeen:
	.string "Maintenance crew. Nobody comes down\n"
	.string "this walkway without clearance.\p"
	.string "You don't look like clearance.$"

GoldenrodCity_Sewers_Text_BrentBeaten:
	.string "Off the clock. Off the clock!$"

GoldenrodCity_Sewers_Text_BrentAfter:
	.string "Ladder at the end of the walkway\n"
	.string "drops into the pipe works.\p"
	.string "Mind the manholes down there.\n"
	.string "They don't all go where you think.$"
