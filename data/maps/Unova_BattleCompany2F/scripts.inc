@ BattleCompany2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_BattleCompany2F_MapScripts::
	.byte 0

Unova_BattleCompany2F_EventScript_Npc0::
	msgbox Unova_BattleCompany2F_Text_BattleCompanyScientistText, MSGBOX_NPC
	end

Unova_BattleCompany2F_EventScript_Npc1::
	msgbox Unova_BattleCompany2F_Text_BattleCompanyScientistText, MSGBOX_NPC
	end

Unova_BattleCompany2F_EventScript_Npc2::
	msgbox Unova_BattleCompany2F_Text_BattleCompanyBlockerText, MSGBOX_NPC
	end


Unova_BattleCompany2F_Text_BattleCompanyScientistText::
	.string "I'm busy working"
	.string "\non products for"
	.string "\lPOKéMON trainers.$"

Unova_BattleCompany2F_Text_BattleCompanyBlockerText::
	.string "Sorry, we don't"
	.string "\nallow visitors"
	.string "\lpast this floor.$"
