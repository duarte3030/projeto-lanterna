@ Placas de Galar do LOTE C da onda 1 (06/09/2026).
@ Gerado por dev_scripts/placas_galar_c.py; NAO editar a mao.
@
@ Sao as placas cujo bg_event existe na FONTE e cujo ponteiro de
@ script da fonte nao aponta para texto nenhum (enchimento 0xFF ou
@ dado que nao e bytecode). O texto e NOVO, em ingles (decisao 32),
@ curto e tirado do que o mapa mostra. Uma placa diz o que diz:
@ MSGBOX_SIGN e mais nada.
@
@ O bg_event de cada uma esta pedido em
@ dev_scripts/onda1_lote_c_pedidos_mapjson.txt: nesta onda o
@ map.json de Galar tem outro dono.

@ ---- Galar_Postwick11 (g01m120/bg/0), tile 665 MB_NORMAL ----
GalarPlacaC_G01M120_bg0::
	msgbox GalarPlacaC_G01M120_bg0_Text, MSGBOX_SIGN
	end

GalarPlacaC_G01M120_bg0_Text:
	.string "Dots are carved deep into the\nstone. It must be Braille.$"

@ ---- Galar_TrainerTower01 (g02m10/bg/0), tile 752 MB_NORMAL ----
GalarPlacaC_G02M10_bg0::
	msgbox GalarPlacaC_G02M10_bg0_Text, MSGBOX_SIGN
	end

GalarPlacaC_G02M10_bg0_Text:
	.string "Trainer Tower\nCheck in at the counter to begin.$"

@ ---- Galar_Motostoke23 (g03m02/bg/0), tile 2 MB_SIGNPOST ----
GalarPlacaC_G03M02_bg0::
	msgbox GalarPlacaC_G03M02_bg0_Text, MSGBOX_SIGN
	end

GalarPlacaC_G03M02_bg0_Text:
	.string "Motostoke\nSteam and steel, day and night.$"

@ ---- Galar_Wyndon08 (g13m10/bg/0), tile 168 MB_NORMAL ----
GalarPlacaC_G13M10_bg0::
	msgbox GalarPlacaC_G13M10_bg0_Text, MSGBOX_SIGN
	end

GalarPlacaC_G13M10_bg0_Text:
	.string "Building directory\nLifts to the upper floors: rear.$"

