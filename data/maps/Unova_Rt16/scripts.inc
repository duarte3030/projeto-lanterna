@ Rt16 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt16_MapScripts::
	.byte 0

Unova_Rt16_EventScript_Placa0::
	msgbox Unova_Rt16_Text_R16SignText, MSGBOX_SIGN
	end

Unova_Rt16_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_R16, Unova_Rt16_Text_BackpackerMR16SeenText, Unova_Rt16_Text_BackpackerMR16BeatenText
	end

Unova_Rt16_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_R16, Unova_Rt16_Text_BackpackerFR16SeenText, Unova_Rt16_Text_BackpackerFR16BeatenText
	end

Unova_Rt16_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_BACKERSM_R16, Unova_Rt16_Text_BackersMR16SeenText, Unova_Rt16_Text_BackersMR16BeatenText
	end

Unova_Rt16_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BACKERSM_R16, Unova_Rt16_Text_BackersMR16SeenText, Unova_Rt16_Text_BackersMR16BeatenText
	end

Unova_Rt16_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_CYCLISTM_R16, Unova_Rt16_Text_CyclistMR16SeenText, Unova_Rt16_Text_CyclistMR16BeatenText
	end

Unova_Rt16_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_CYCLISTF_R16, Unova_Rt16_Text_CyclistFR16SeenText, Unova_Rt16_Text_CyclistFR16BeatenText
	end


Unova_Rt16_Text_R16SignText::
	.string "NIMBASA CITY"
	.string "\nahead.$"

Unova_Rt16_Text_BackpackerMR16SeenText::
	.string "A spot of greenery"
	.string "\ngrowing right next"
	.string "\lto a big city!"
	.string "\pTruly an oasis! I"
	.string "\nfeel so refreshed…"
	.string "\pAnd now I'd like"
	.string "\nto battle!$"

Unova_Rt16_Text_BackpackerMR16BeatenText::
	.string "Oh… It no longer"
	.string "\nfeels like an"
	.string "\loasis if I lose.$"

Unova_Rt16_Text_BackpackerFR16SeenText::
	.string "City POKéMON or"
	.string "\nPOKéMON that live"
	.string "\lin the forest…"
	.string "\pWhich do you"
	.string "\nprefer?$"

Unova_Rt16_Text_BackpackerFR16BeatenText::
	.string "I love both kinds"
	.string "\nof POKéMON, but I"
	.string "\ldon't like losing…$"

Unova_Rt16_Text_BackersMR16SeenText::
	.string "Tomorrow will be a"
	.string "\nhome run!$"

Unova_Rt16_Text_BackersMR16BeatenText::
	.string "Farewell, you won!$"

Unova_Rt16_Text_CyclistMR16SeenText::
	.string "When I'm riding my"
	.string "\nbicycle, don't you"
	.string "\pthink I look"
	.string "\nstronger?$"

Unova_Rt16_Text_CyclistMR16BeatenText::
	.string "The cool breeze in"
	.string "\nmy face stopped!$"

Unova_Rt16_Text_CyclistFR16SeenText::
	.string "Ting-a-ling-ling!"
	.string "\nFull speed attack,"
	.string "\lcoming your way!$"

Unova_Rt16_Text_CyclistFR16BeatenText::
	.string "Ting-a-ling-ling!"
	.string "\nTing-a-ling-ling!$"
