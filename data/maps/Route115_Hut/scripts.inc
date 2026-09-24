@ Route115_Hut: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 22.3) por dev_scripts/copia_planta_ex.py.

Route115_Hut_MapScripts::
	.byte 0

@ Decisão 7: o diário da cabana do EX (0x8352A80) dá o MYSTIC TICKET uma vez e libera o barco da
@ Navel Rock; as duas flags do EX (0x13B e 0x8E0) são as nossas de mesmo nome e mesmo papel.
Route115_Hut_EventScript_Journal::
	lock
	faceplayer
	msgbox Route115_Hut_Text_OldJournal, MSGBOX_SIGN
	msgbox Route115_Hut_Text_JournalPages, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_MYSTIC_TICKET, Route115_Hut_EventScript_JournalFim
	msgbox Route115_Hut_Text_PaperBetween, MSGBOX_SIGN
	giveitem ITEM_MYSTIC_TICKET
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_MYSTIC_TICKET
	setflag FLAG_ENABLE_SHIP_NAVEL_ROCK
Route115_Hut_EventScript_JournalFim::
	msgbox Route115_Hut_Text_TwoBrighter, MSGBOX_SIGN
	release
	end

Route115_Hut_Text_OldJournal:
	.string "An old journal.$"

Route115_Hut_Text_JournalPages:
	.string "...\n"
	.string "...After eight days of sailing, the SS\l"
	.string "NOVA spotted an odd tower on the\l"
	.string "horizon...\p"
	.string "...The tower was tall, emerging from the\n"
	.string "ocean on a small island not much larger\l"
	.string "than the base of the tower...\p"
	.string "...Storms erupted, POKéMON beyond\n"
	.string "powerful...\p"
	.string "...I’ve saved the route, but do not\n"
	.string "return without a POKéMON MASTER...$"

Route115_Hut_Text_PaperBetween:
	.string "There’s a paper in between the pages...$"

Route115_Hut_Text_TwoBrighter:
	.string "...Two,\n"
	.string "brighter than the sun and deeper than\l"
	.string "the sea...$"

