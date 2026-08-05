@ BattleCompany1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_BattleCompany1F_MapScripts::
	.byte 0

Unova_BattleCompany1F_EventScript_Placa0::
	msgbox Unova_BattleCompany1F_Text_BattleCompany1FSignText, MSGBOX_SIGN
	end

Unova_BattleCompany1F_EventScript_Npc0::
	msgbox Unova_BattleCompany1F_Text_BattleCompanyReceptionistText, MSGBOX_NPC
	end

Unova_BattleCompany1F_EventScript_Npc1::
	msgbox Unova_BattleCompany1F_Text_BattleCompanyPresidentIntroText, MSGBOX_NPC
	end


Unova_BattleCompany1F_Text_BattleCompany1FSignText::
	.string "BATTLE COMPANY."
	.string "\pResearch and"
	.string "\ndevelopment"
	.string "\lupstairs.$"

Unova_BattleCompany1F_Text_BattleCompanyReceptionistText::
	.string "Welcome to the"
	.string "\nBATTLE COMPANY."
	.string "\pThe second floor"
	.string "\nis open to"
	.string "\lvisitors.$"

Unova_BattleCompany1F_Text_BattleCompanyPresidentIntroText::
	.string "Oh, you must be a"
	.string "\nPOKéMON trainer."
	.string "\pI'm the PRESIDENT"
	.string "\nof the BATTLE"
	.string "\lCOMPANY."
	.string "\pI'm looking for"
	.string "\nsomeone to test"
	.string "\lour new prototype.$"
