Route30_MrPokemonsHouse_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

MrPokemonHouse_EventScript_Coins::
	lock
	msgbox MrPokemonHouse_Text_StrangeCoins, MSGBOX_SIGN
	release
	end

MrPokemonHouse_EventScript_Magazine::
	lock
	msgbox MrPokemonHouse_Text_ForeignMagazines, MSGBOX_SIGN
	release
	end

MrPokemonHouse_Text_ForeignMagazines::
	.string "It's packed with foreign\n"
	.string "magazines.\p"
	.string "Can't even read their titles…$"

MrPokemonHouse_Text_StrangeCoins::
	.string "A whole pile of strange coins!\p"
	.string "Maybe they're from another\n"
	.string "country…$"
