@ LavaridgeTown_Ex4_9: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 4.9) por dev_scripts/copia_planta_ex.py.

LavaridgeTown_Ex4_9_MapScripts::
	.byte 0

@ Lateral do Pokémon Emerald EX (decisão 7 do Fable): o artista dá uma Black Augurite uma vez.
LavaridgeTown_Ex4_9_EventScript_Artist::
	lock
	faceplayer
	goto_if_unset FLAG_HOENNEX_RECEIVED_BLACK_AUGURITE_LAVARIDGE, LavaridgeTown_Ex4_9_EventScript_ArtistOffer
	msgbox LavaridgeTown_Ex4_9_Text_Clay, MSGBOX_DEFAULT
	closemessage
	release
	end

LavaridgeTown_Ex4_9_EventScript_ArtistOffer::
	msgbox LavaridgeTown_Ex4_9_Text_Offer, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, YES, LavaridgeTown_Ex4_9_EventScript_ArtistGive
	msgbox LavaridgeTown_Ex4_9_Text_Shy, MSGBOX_DEFAULT
	closemessage
	release
	end

LavaridgeTown_Ex4_9_EventScript_ArtistGive::
	giveitem ITEM_BLACK_AUGURITE
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	msgbox LavaridgeTown_Ex4_9_Text_Careful, MSGBOX_DEFAULT
	setflag FLAG_HOENNEX_RECEIVED_BLACK_AUGURITE_LAVARIDGE
	closemessage
	release
	end

LavaridgeTown_Ex4_9_Text_Offer:
	.string "The ash from the volcano makes great\n"
	.string "clay. While gathering it I keep finding\l"
	.string "these odd volcanic rocks.\p"
	.string "Would you like one?$"

LavaridgeTown_Ex4_9_Text_Shy:
	.string "Don’t be shy I’ve got plenty of em.$"

LavaridgeTown_Ex4_9_Text_Careful:
	.string "Be careful with it,\n"
	.string "Broken pieces of that stuff can be\l"
	.string "sharp.$"

LavaridgeTown_Ex4_9_Text_Clay:
	.string "It’s important to get all the rocks and\n"
	.string "plants out of your clay before you use\l"
	.string "it!$"

