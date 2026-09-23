@ LcUnderseaCavern: mapa copiado de Pokémon Liquid Crystal.gba (g4m47) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui.

LcUnderseaCavern_MapScripts::
	.byte 0

LcUnderseaCavern_EventScript_Marcus::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_MARCUS, LcUnderseaCavern_Text_MarcusSeen, LcUnderseaCavern_Text_MarcusBeaten
	msgbox LcUnderseaCavern_Text_MarcusAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaCavern_EventScript_Noelle::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_NOELLE, LcUnderseaCavern_Text_NoelleSeen, LcUnderseaCavern_Text_NoelleBeaten
	msgbox LcUnderseaCavern_Text_NoelleAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaCavern_EventScript_EntranceSign::
	msgbox LcUnderseaCavern_Text_EntranceSign, MSGBOX_SIGN
	end

LcUnderseaCavern_Text_MarcusSeen:
	.string "You came down the trench too?\n"
	.string "Then you can hold your breath.\p"
	.string "Let's see if your POKéMON can.$"

LcUnderseaCavern_Text_MarcusBeaten:
	.string "Out of air and out of luck.$"

LcUnderseaCavern_Text_MarcusAfter:
	.string "There is air in here. Nobody can\n"
	.string "tell me where it comes from.\p"
	.string "The deeper you go, the warmer it\n"
	.string "gets. That is the part I don't like.$"

LcUnderseaCavern_Text_NoelleSeen:
	.string "Careful. The floor looks solid and\n"
	.string "then it isn't.$"

LcUnderseaCavern_Text_NoelleBeaten:
	.string "I slipped. That's all.$"

LcUnderseaCavern_Text_NoelleAfter:
	.string "The red rock is coral. Dead coral,\n"
	.string "hundreds of years of it.\p"
	.string "This whole cave was a reef once,\n"
	.string "before the sea closed over it.$"

LcUnderseaCavern_Text_EntranceSign:
	.string "UNDERSEA CAVERN\p"
	.string "“Air pockets ahead. Water below.\n"
	.string "Do not go further alone.”$"
