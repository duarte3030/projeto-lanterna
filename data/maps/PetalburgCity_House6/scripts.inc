@ PetalburgCity_House6: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 8.10) por dev_scripts/copia_planta_ex.py.

PetalburgCity_House6_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 8.10), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
PetalburgCity_House6_EventScript_ExNpc0::
	msgbox PetalburgCity_House6_Text_ExNpc0, MSGBOX_NPC
	end

PetalburgCity_House6_Text_ExNpc0:
	.string "What should I make for dinner?$"

PetalburgCity_House6_EventScript_ExNpc2::
	msgbox PetalburgCity_House6_Text_ExNpc2, MSGBOX_NPC
	end

PetalburgCity_House6_Text_ExNpc2:
	.string "My husbands food is amazing, but\n"
	.string "sometimes I wish he would cook\l"
	.string "something new.$"


@ Presente do EX (0x834F80E), reescrito: a HEAL BALL, uma vez.
PetalburgCity_House6_EventScript_Twin::
	lock
	faceplayer
	msgbox PetalburgCity_House6_Text_DaddyLovesMart, MSGBOX_DEFAULT
	goto_if_set FLAG_RECEIVED_HOENNEX_PETALBURG_HEAL_BALL, PetalburgCity_House6_EventScript_TwinEnd
	msgbox PetalburgCity_House6_Text_HeBoughtThis, MSGBOX_DEFAULT
	giveitem ITEM_HEAL_BALL
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_RECEIVED_HOENNEX_PETALBURG_HEAL_BALL
PetalburgCity_House6_EventScript_TwinEnd::
	release
	end

PetalburgCity_House6_Text_DaddyLovesMart:
	.string "Daddy loves buying things from the\n"
	.string "POKéMART!$"

PetalburgCity_House6_Text_HeBoughtThis:
	.string "Here he bought this yesterday.$"
