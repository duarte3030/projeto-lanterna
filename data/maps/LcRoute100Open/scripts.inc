@ LcRoute100Open: mapa copiado de Pokémon Liquid Crystal.gba (g3m40) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO é NOSSO.
@ Os três warps do hack, (64,31), (64,37) e (64,48), eram a UNDERSEA EXPRESS,
@ a empresa de trem submarino que leva às Ilhas Laranja. As Ilhas Laranja NÃO
@ vêm para este cartucho (PRD-CARTUCHO-1), então nenhum dos três entrou e cada
@ um ganhou placa em inglês dizendo que a linha está fechada, no molde das
@ portas fechadas de Johto (data/scripts/portas_fechadas.inc). Nenhum prédio
@ novo foi desenhado e nenhum trem existe.

LcRoute100Open_MapScripts::
	.byte 0

LcRoute100Open_EventScript_Torin::
	trainerbattle_single TRAINER_JOHTO_LC_ROUTE100_TORIN, LcRoute100Open_Text_TorinSeen, LcRoute100Open_Text_TorinBeaten
	msgbox LcRoute100Open_Text_TorinAfter, MSGBOX_AUTOCLOSE
	end

LcRoute100Open_EventScript_Marna::
	trainerbattle_single TRAINER_JOHTO_LC_ROUTE100_MARNA, LcRoute100Open_Text_MarnaSeen, LcRoute100Open_Text_MarnaBeaten
	msgbox LcRoute100Open_Text_MarnaAfter, MSGBOX_AUTOCLOSE
	end

LcRoute100Open_EventScript_Haldan::
	trainerbattle_single TRAINER_JOHTO_LC_ROUTE100_HALDAN, LcRoute100Open_Text_HaldanSeen, LcRoute100Open_Text_HaldanBeaten
	msgbox LcRoute100Open_Text_HaldanAfter, MSGBOX_AUTOCLOSE
	end

LcRoute100Open_EventScript_Berrik::
	trainerbattle_single TRAINER_JOHTO_LC_ROUTE100_BERRIK, LcRoute100Open_Text_BerrikSeen, LcRoute100Open_Text_BerrikBeaten
	msgbox LcRoute100Open_Text_BerrikAfter, MSGBOX_AUTOCLOSE
	end

LcRoute100Open_EventScript_SignStationNorth::
	msgbox LcRoute100Open_Text_SignStationNorth, MSGBOX_SIGN
	end

LcRoute100Open_EventScript_SignStationFront::
	msgbox LcRoute100Open_Text_SignStationFront, MSGBOX_SIGN
	end

LcRoute100Open_EventScript_SignDock::
	msgbox LcRoute100Open_Text_SignDock, MSGBOX_SIGN
	end

LcRoute100Open_Text_TorinSeen:
	.string "Swam all the way out to the reef,\n"
	.string "did you?$"

LcRoute100Open_Text_TorinBeaten:
	.string "Worth the swim, then.$"

LcRoute100Open_Text_TorinAfter:
	.string "This island is a station and\n"
	.string "nothing else. No shop, no beds.\p"
	.string "We sleep on the sand and we like\n"
	.string "it.$"

LcRoute100Open_Text_MarnaSeen:
	.string "Trainers who come here are either\n"
	.string "lost or very good.$"

LcRoute100Open_Text_MarnaBeaten:
	.string "Not lost, then.$"

LcRoute100Open_Text_MarnaAfter:
	.string "The rocks out here are the tips of\n"
	.string "one reef, not a hundred stones.\p"
	.string "It runs east until the charts stop.$"

LcRoute100Open_Text_HaldanSeen:
	.string "I crewed that line for nine years.\n"
	.string "Now I crew nothing. Battle me.$"

LcRoute100Open_Text_HaldanBeaten:
	.string "Nine years and still not enough.$"

LcRoute100Open_Text_HaldanAfter:
	.string "The tunnel ran under the sea floor,\n"
	.string "east, for days.\p"
	.string "They shut the whole line and never\n"
	.string "said what for.$"

LcRoute100Open_Text_BerrikSeen:
	.string "Careful on the dock. The boards are\n"
	.string "older than me.$"

LcRoute100Open_Text_BerrikBeaten:
	.string "Older and sturdier, apparently.$"

LcRoute100Open_Text_BerrikAfter:
	.string "Best fishing in JOHTO, right here,\n"
	.string "because nobody else bothers.\p"
	.string "Keep it to yourself.$"

LcRoute100Open_Text_SignStationNorth:
	.string "UNDERSEA EXPRESS, NORTH ENTRANCE\n"
	.string "Closed until further notice.$"

LcRoute100Open_Text_SignStationFront:
	.string "UNDERSEA EXPRESS\n"
	.string "This station is closed.\l"
	.string "No service beyond ROUTE 100.$"

LcRoute100Open_Text_SignDock:
	.string "PLATFORM\n"
	.string "The line east is out of service.\l"
	.string "There is no train and no crew.$"
