@ Route102_FishingHut: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 18.0) por dev_scripts/copia_planta_ex.py.

Route102_FishingHut_MapScripts::
	.byte 0

@ Decisão 7: o pescador da cabana (EX 0x834F467). Pede a insígnia da Roxanne; dá a OLD ROD
@ (mesma flag nossa, FLAG_RECEIVED_OLD_ROD, dividida com Dewford e RustboroPart2) e a LURE BALL.
Route102_FishingHut_EventScript_Fisherman::
	lock
	faceplayer
	msgbox Route102_FishingHut_Text_MyHut, MSGBOX_DEFAULT
	goto_if_unset FLAG_DEFEATED_RUSTBORO_GYM, Route102_FishingHut_EventScript_SemInsignia
	goto_if_set FLAG_RECEIVED_HOENNEX_ROUTE102_LURE_BALL, Route102_FishingHut_EventScript_Fim
	goto_if_set FLAG_RECEIVED_OLD_ROD, Route102_FishingHut_EventScript_SoLure
	msgbox Route102_FishingHut_Text_TakeOldRod, MSGBOX_DEFAULT
	giveitem ITEM_OLD_ROD
	setflag FLAG_RECEIVED_OLD_ROD
	msgbox Route102_FishingHut_Text_LureBallHelp, MSGBOX_DEFAULT
	giveitem ITEM_LURE_BALL
	setflag FLAG_RECEIVED_HOENNEX_ROUTE102_LURE_BALL
Route102_FishingHut_EventScript_Fim::
	msgbox Route102_FishingHut_Text_WayOfLife, MSGBOX_DEFAULT
	release
	end

Route102_FishingHut_EventScript_SemInsignia::
	msgbox Route102_FishingHut_Text_ComeBackBadge, MSGBOX_DEFAULT
	release
	end

Route102_FishingHut_EventScript_SoLure::
	msgbox Route102_FishingHut_Text_YouHaveRod, MSGBOX_DEFAULT
	giveitem ITEM_LURE_BALL
	setflag FLAG_RECEIVED_HOENNEX_ROUTE102_LURE_BALL
	msgbox Route102_FishingHut_Text_WorksBetter, MSGBOX_DEFAULT
	release
	end

Route102_FishingHut_Text_MyHut:
	.string "This is my fishing hut.$"

Route102_FishingHut_Text_WayOfLife:
	.string "Fishing is a way of life.$"

Route102_FishingHut_Text_ComeBackBadge:
	.string "Come back with a GYM BADGE and I’ll\n"
	.string "teach you how to fish!$"

Route102_FishingHut_Text_TakeOldRod:
	.string "Oh you have a GYM BADGE! Take this OLD\n"
	.string "ROD.$"

Route102_FishingHut_Text_LureBallHelp:
	.string "This LURE BALL will help you catch\n"
	.string "POKEMON that you fished up.$"

Route102_FishingHut_Text_YouHaveRod:
	.string "Oh you have a fishing rod! Take this LURE\n"
	.string "BALL.$"

Route102_FishingHut_Text_WorksBetter:
	.string "It works better on POKéMON caught on a\n"
	.string "fishing line.$"

