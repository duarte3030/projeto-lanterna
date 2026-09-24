@ DewfordTown_Ex3_7: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 3.7) por dev_scripts/copia_planta_ex.py.

DewfordTown_Ex3_7_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 3.7), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
DewfordTown_Ex3_7_EventScript_ExNpc0::
	msgbox DewfordTown_Ex3_7_Text_ExNpc0, MSGBOX_NPC
	end

DewfordTown_Ex3_7_Text_ExNpc0:
	.string "Making pots from clay is a timeless art.\p"
	.string "It takes patients and practice to get\n"
	.string "good at, very much like training\l"
	.string "POKéMON.$"

@ Lateral do Pokémon Emerald EX (decisão 7 do Fable): o velho dá o Charcoal uma vez.
DewfordTown_Ex3_7_EventScript_CharcoalMan::
	lock
	faceplayer
	goto_if_unset FLAG_HOENNEX_RECEIVED_CHARCOAL_DEWFORD, DewfordTown_Ex3_7_EventScript_CharcoalOffer
	msgbox DewfordTown_Ex3_7_Text_Retire, MSGBOX_DEFAULT
	closemessage
	release
	end

DewfordTown_Ex3_7_EventScript_CharcoalOffer::
	msgbox DewfordTown_Ex3_7_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, DewfordTown_Ex3_7_EventScript_CharcoalGive
	msgbox DewfordTown_Ex3_7_Text_KeepIt, MSGBOX_DEFAULT
	closemessage
	release
	end

DewfordTown_Ex3_7_EventScript_CharcoalGive::
	giveitem ITEM_CHARCOAL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox DewfordTown_Ex3_7_Text_Retire, MSGBOX_DEFAULT
	setflag FLAG_HOENNEX_RECEIVED_CHARCOAL_DEWFORD
	closemessage
	release
	end

DewfordTown_Ex3_7_Text_Offer:
	.string "I once was a POKéMON TRAINER, Hmmm\n"
	.string "but that was a long time ago.\p"
	.string "Would you like something that may help\n"
	.string "you in your journey.$"

DewfordTown_Ex3_7_Text_KeepIt:
	.string "That’s alright,\n"
	.string "I’ll keep it for someone who needs it.$"

DewfordTown_Ex3_7_Text_Retire:
	.string "DEWFORD TOWN is a wonderful place to\n"
	.string "retire.$"

