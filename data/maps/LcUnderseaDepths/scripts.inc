@ LcUnderseaDepths: mapa copiado de Pokémon Liquid Crystal.gba (g4m48) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui.
@
@ É o maior mapa da área, 49x140, e o motor aguenta por pouco: InitMapLayoutData
@ monta (49+15) por (140+14) = 9.856 entradas de sBackupMapData, contra o teto
@ MAX_MAP_DATA_SIZE de 10.240. Mapa maior que isso carregaria com o fundo todo
@ MAPGRID_UNDEFINED, sem erro nenhum no build.
@
@ A planta não é uma sala só: são dez regiões andáveis separadas por rocha, e as
@ cinco escadas internas (warps 7 a 16) são o que liga uma na outra. Foi assim
@ que o autor desenhou e é assim que fica.

LcUnderseaDepths_MapScripts::
	.byte 0

LcUnderseaDepths_EventScript_Odell::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_ODELL, LcUnderseaDepths_Text_OdellSeen, LcUnderseaDepths_Text_OdellBeaten
	msgbox LcUnderseaDepths_Text_OdellAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaDepths_EventScript_Tobias::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_TOBIAS, LcUnderseaDepths_Text_TobiasSeen, LcUnderseaDepths_Text_TobiasBeaten
	msgbox LcUnderseaDepths_Text_TobiasAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaDepths_EventScript_Ines::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_INES, LcUnderseaDepths_Text_InesSeen, LcUnderseaDepths_Text_InesBeaten
	msgbox LcUnderseaDepths_Text_InesAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaDepths_EventScript_Koa::
	trainerbattle_single TRAINER_JOHTO_LC_UNDERSEA_KOA, LcUnderseaDepths_Text_KoaSeen, LcUnderseaDepths_Text_KoaBeaten
	msgbox LcUnderseaDepths_Text_KoaAfter, MSGBOX_AUTOCLOSE
	end

LcUnderseaDepths_EventScript_DepthsSign::
	msgbox LcUnderseaDepths_Text_DepthsSign, MSGBOX_SIGN
	end

LcUnderseaDepths_EventScript_DeepSign::
	msgbox LcUnderseaDepths_Text_DeepSign, MSGBOX_SIGN
	end

LcUnderseaDepths_Text_OdellSeen:
	.string "Twelve hours on this ledge and one\n"
	.string "bite. Give me something to do!$"

LcUnderseaDepths_Text_OdellBeaten:
	.string "Should have kept fishing.$"

LcUnderseaDepths_Text_OdellAfter:
	.string "Everything I pull out of these pools\n"
	.string "has no colour in it.\p"
	.string "Put it back in the sea and it takes\n"
	.string "a week to look like itself again.$"

LcUnderseaDepths_Text_TobiasSeen:
	.string "Straight down for a hundred and forty\n"
	.string "tiles and every one of them wet.\p"
	.string "You'll need a battle to warm up.$"

LcUnderseaDepths_Text_TobiasBeaten:
	.string "Cold again already.$"

LcUnderseaDepths_Text_TobiasAfter:
	.string "Count the ladders on the way down.\n"
	.string "There are five.\p"
	.string "Miss one and you will be walking this\n"
	.string "gallery twice.$"

LcUnderseaDepths_Text_InesSeen:
	.string "Nobody gets this far by accident.\n"
	.string "So you meant it. Good.$"

LcUnderseaDepths_Text_InesBeaten:
	.string "You meant it more than I did.$"

LcUnderseaDepths_Text_InesAfter:
	.string "There is a chamber at the bottom of\n"
	.string "all this with carved walls.\p"
	.string "Older than JOHTO. Older than anyone\n"
	.string "who could have carved it.$"

LcUnderseaDepths_Text_KoaSeen:
	.string "I train where nothing is easy.\n"
	.string "Nothing here is easy.$"

LcUnderseaDepths_Text_KoaBeaten:
	.string "Then I'll stay longer.$"

LcUnderseaDepths_Text_KoaAfter:
	.string "Carry your own lamp, carry your own\n"
	.string "water, carry your own POKéMON.\p"
	.string "The cave does not lend anything.$"

LcUnderseaDepths_Text_DepthsSign:
	.string "THE LONG GALLERY\p"
	.string "“Five ladders down. Keep the wall\n"
	.string "on your right and you will not circle.”$"

LcUnderseaDepths_Text_DeepSign:
	.string "“Turn back here if your POKéMON are\n"
	.string "tired.\p"
	.string "There is no short way up from below\n"
	.string "this mark.”$"
