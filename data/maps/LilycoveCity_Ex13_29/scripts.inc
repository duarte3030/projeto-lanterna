@ LilycoveCity_Ex13_29: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 13.29) por dev_scripts/copia_planta_ex.py.

LilycoveCity_Ex13_29_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 13.29), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
LilycoveCity_Ex13_29_EventScript_ExNpc0::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc0, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc0:
	.string "GOLDUCK! GOLDUCK! GOLDUCK!.$"

LilycoveCity_Ex13_29_EventScript_ExNpc1::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc1, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc1:
	.string "Shh.\n"
	.string "I don’t want to be it...$"

LilycoveCity_Ex13_29_EventScript_ExNpc2::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc2, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc2:
	.string "I’m gonna catch em.\n"
	.string "You watch!$"

LilycoveCity_Ex13_29_EventScript_ExNpc3::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc3, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc3:
	.string "When will he say GOLDUCK!$"

LilycoveCity_Ex13_29_EventScript_ExNpc4::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc4, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc4:
	.string "PSYDUCK, PSYDUCK, PSYDUCK...$"

LilycoveCity_Ex13_29_EventScript_ExNpc5::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc5, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc5:
	.string "How can I help you?\n"
	.string "That’s what my momma says at the big\l"
	.string "store!$"

LilycoveCity_Ex13_29_EventScript_ExNpc6::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc6, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc6:
	.string "All this food is fake.$"

LilycoveCity_Ex13_29_EventScript_ExNpc7::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc7, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc7:
	.string "I used BITE on SAM and now I’m in time\n"
	.string "out...\p"
	.string "Grrrr, I’m a MIGHTYENA!$"

LilycoveCity_Ex13_29_EventScript_ExNpc8::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc8, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc8:
	.string "If I can figure out how to open this\n"
	.string "one, I can open the one at the store!.$"

LilycoveCity_Ex13_29_EventScript_ExNpc9::
	msgbox LilycoveCity_Ex13_29_Text_ExNpc9, MSGBOX_NPC
	end

LilycoveCity_Ex13_29_Text_ExNpc9:
	.string "My husband and I opened this daycare a\n"
	.string "few years ago.\p"
	.string "It’s great to be around so many kids!$"


@ Presente do EX (13.29): a Eviolite uma vez só. O EX usa a flag 0x170; aqui
@ FLAG_HOENNEX_LILYCOVE_EVIOLITE (faixa do lote C). Reescrito do bytecode e do texto da ROM.
LilycoveCity_Ex13_29_EventScript_ExPresente::
	lock
	faceplayer
	goto_if_unset FLAG_HOENNEX_LILYCOVE_EVIOLITE, LilycoveCity_Ex13_29_EventScript_ExDaPresente
	msgbox LilycoveCity_Ex13_29_Text_ExPausa, MSGBOX_DEFAULT
	closemessage
	release
	end

LilycoveCity_Ex13_29_EventScript_ExDaPresente::
	msgbox LilycoveCity_Ex13_29_Text_ExEscolhas, MSGBOX_DEFAULT
	giveitem ITEM_EVIOLITE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox LilycoveCity_Ex13_29_Text_ExEvoluir, MSGBOX_DEFAULT
	setflag FLAG_HOENNEX_LILYCOVE_EVIOLITE
	closemessage
	release
	end

LilycoveCity_Ex13_29_Text_ExPausa:
	.string "I’m just taking a little break.$"

LilycoveCity_Ex13_29_Text_ExEscolhas:
	.string "Do you ever wonder if you made the\n"
	.string "right choices in life?\p"
	.string "Perhaps I have, Here take this.$"

LilycoveCity_Ex13_29_Text_ExEvoluir:
	.string "It’s depended on that for too long.\p"
	.string "I need to evolve into my future.$"
