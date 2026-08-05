@ NacreneMuseum do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NacreneMuseum_MapScripts::
	.byte 0

Unova_NacreneMuseum_EventScript_Placa0::
	msgbox Unova_NacreneMuseum_Text_NacreneMuseumDisplayText, MSGBOX_SIGN
	end

Unova_NacreneMuseum_EventScript_Placa1::
	msgbox Unova_NacreneMuseum_Text_NacreneMuseumDisplayText, MSGBOX_SIGN
	end

Unova_NacreneMuseum_EventScript_Npc0::
	msgbox Unova_NacreneMuseum_Text_NacreneMuseumNoDiskText, MSGBOX_NPC
	end

Unova_NacreneMuseum_EventScript_Npc1::
	msgbox Unova_NacreneMuseum_Text_NacreneMuseumRangerMText, MSGBOX_NPC
	end

Unova_NacreneMuseum_EventScript_Npc2::
	msgbox Unova_NacreneMuseum_Text_NacreneMuseumTwinText, MSGBOX_NPC
	end


Unova_NacreneMuseum_Text_NacreneMuseumDisplayText::
	.string "Many ancient POKé-"
	.string "\nMON artifacts are"
	.string "\lon display.$"

Unova_NacreneMuseum_Text_NacreneMuseumNoDiskText::
	.string "Welcome to"
	.string "\nNACRENE MUSEUM."
	.string "\pUnfortunately,"
	.string "\nwithout the DATA"
	.string "\lDISK that was"
	.string "\pstolen, we can't"
	.string "\nrevive POKéMON"
	.string "\lfrom fossils.$"

Unova_NacreneMuseum_Text_NacreneMuseumRangerMText::
	.string "Rarities from"
	.string "\naround the world…"
	.string "\pMuseums are packed"
	.string "\nwith adventure!$"

Unova_NacreneMuseum_Text_NacreneMuseumTwinText::
	.string "I heard that the"
	.string "\ndirector, LENORA,"
	.string "\pis too busy with"
	.string "\nher research on"
	.string "\pfossils and POKé-"
	.string "\nMON bones, so she"
	.string "\ptook a break from"
	.string "\nbeing a GYM"
	.string "\lLEADER.$"
