@ Terceiro salão do depósito subterrâneo de Goldenrod, copiado do mapa `g1m54`
@ do Pokémon GS Chronicles. A arte é do autor, byte a byte; o jogo é nosso.
GoldenrodCity_UndergroundWarehouse_MapScripts::
	.byte 0

GoldenrodCity_UndergroundWarehouse_EventScript_Grunt29::
	trainerbattle_single TRAINER_JOHTO_DEPOSITO_GOLDENROD_2, GoldenrodCity_UndergroundWarehouse_Text_Grunt29Seen, GoldenrodCity_UndergroundWarehouse_Text_Grunt29Beaten
	msgbox GoldenrodCity_UndergroundWarehouse_Text_Grunt29After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundWarehouse_EventScript_Grunt30::
	trainerbattle_single TRAINER_JOHTO_DEPOSITO_GOLDENROD_3, GoldenrodCity_UndergroundWarehouse_Text_Grunt30Seen, GoldenrodCity_UndergroundWarehouse_Text_Grunt30Beaten
	msgbox GoldenrodCity_UndergroundWarehouse_Text_Grunt30After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundWarehouse_Text_Grunt29Seen:
	.string "Shutter's supposed to stay down.\p"
	.string "If you got through it, you can get\n"
	.string "through me. Try.$"

GoldenrodCity_UndergroundWarehouse_Text_Grunt29Beaten:
	.string "The shutter was the easy part…$"

GoldenrodCity_UndergroundWarehouse_Text_Grunt29After:
	.string "Half this room is walled off.\p"
	.string "Nobody remembers what's behind it,\n"
	.string "and nobody wants to find out.$"

GoldenrodCity_UndergroundWarehouse_Text_Grunt30Seen:
	.string "Deliveries only. And you are not\n"
	.string "a delivery.$"

GoldenrodCity_UndergroundWarehouse_Text_Grunt30Beaten:
	.string "Take it up with the manager!$"

GoldenrodCity_UndergroundWarehouse_Text_Grunt30After:
	.string "There is no manager.\n"
	.string "There never was.$"
