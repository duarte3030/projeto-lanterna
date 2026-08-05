@ Rt16 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt16_MapScripts::
	.byte 0

Unova_Rt16_EventScript_Placa0::
	msgbox Unova_Rt16_Text_R16SignText, MSGBOX_SIGN
	end

Unova_Rt16_EventScript_Npc4::
	msgbox Unova_Rt16_Text_BackpackerMR16SeenText, MSGBOX_NPC
	end

Unova_Rt16_EventScript_Npc5::
	msgbox Unova_Rt16_Text_BackpackerFR16SeenText, MSGBOX_NPC
	end

Unova_Rt16_EventScript_Npc6::
	msgbox Unova_Rt16_Text_BackersMR16SeenText, MSGBOX_NPC
	end

Unova_Rt16_EventScript_Npc7::
	msgbox Unova_Rt16_Text_BackersMR16SeenText, MSGBOX_NPC
	end

Unova_Rt16_EventScript_Npc8::
	msgbox Unova_Rt16_Text_CyclistMR16SeenText, MSGBOX_NPC
	end

Unova_Rt16_EventScript_Npc9::
	msgbox Unova_Rt16_Text_CyclistFR16SeenText, MSGBOX_NPC
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

Unova_Rt16_Text_BackpackerFR16SeenText::
	.string "City POKéMON or"
	.string "\nPOKéMON that live"
	.string "\lin the forest…"
	.string "\pWhich do you"
	.string "\nprefer?$"

Unova_Rt16_Text_BackersMR16SeenText::
	.string "Tomorrow will be a"
	.string "\nhome run!$"

Unova_Rt16_Text_CyclistMR16SeenText::
	.string "When I'm riding my"
	.string "\nbicycle, don't you"
	.string "\pthink I look"
	.string "\nstronger?$"

Unova_Rt16_Text_CyclistFR16SeenText::
	.string "Ting-a-ling-ling!"
	.string "\nFull speed attack,"
	.string "\lcoming your way!$"
