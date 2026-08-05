@ MarlonsHouse do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_MarlonsHouse_MapScripts::
	.byte 0

Unova_MarlonsHouse_EventScript_Placa1::
	msgbox Unova_MarlonsHouse_Text_MarlonsHouseFridgeText, MSGBOX_SIGN
	end

Unova_MarlonsHouse_EventScript_Npc0::
	msgbox Unova_MarlonsHouse_Text_WifeText_GetMon, MSGBOX_NPC
	end

Unova_MarlonsHouse_EventScript_Npc1::
	msgbox Unova_MarlonsHouse_Text_TakeSnivyText, MSGBOX_NPC
	end

Unova_MarlonsHouse_EventScript_Npc2::
	msgbox Unova_MarlonsHouse_Text_TakeTepigText, MSGBOX_NPC
	end

Unova_MarlonsHouse_EventScript_Npc3::
	msgbox Unova_MarlonsHouse_Text_TakeOshawottText, MSGBOX_NPC
	end


Unova_MarlonsHouse_Text_MarlonsHouseFridgeText::
	.string "Better not mess"
	.string "\naround in MARLON's"
	.string "\lfridge!$"

Unova_MarlonsHouse_Text_WifeText_GetMon::
	.string "Go ahead, pick"
	.string "\nyour favorite!$"

Unova_MarlonsHouse_Text_TakeSnivyText::
	.string "You'll take"
	.string "\nSNIVY, the"
	.string "\lgrass POKéMON?$"

Unova_MarlonsHouse_Text_TakeTepigText::
	.string "Do you want"
	.string "\nTEPIG, the"
	.string "\lfire POKéMON?$"

Unova_MarlonsHouse_Text_TakeOshawottText::
	.string "So, you like"
	.string "\nOSHAWOTT, the"
	.string "\lwater POKéMON?$"
