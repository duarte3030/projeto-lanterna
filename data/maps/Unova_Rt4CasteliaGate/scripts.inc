@ Rt4CasteliaGate do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt4CasteliaGate_MapScripts::
	.byte 0

Unova_Rt4CasteliaGate_EventScript_Npc0::
	msgbox Unova_Rt4CasteliaGate_Text_R4CasteliaGateOfficerText, MSGBOX_NPC
	end

Unova_Rt4CasteliaGate_EventScript_Npc1::
	msgbox Unova_Rt4CasteliaGate_Text_R4CasteliaGateGiveItemfinderText, MSGBOX_NPC
	end


Unova_Rt4CasteliaGate_Text_R4CasteliaGateOfficerText::
	.string "Welcome to"
	.string "\nCASTELIA CITY,"
	.string "\pthe largest city"
	.string "\nin the UNOVA"
	.string "\lregion!$"

Unova_Rt4CasteliaGate_Text_R4CasteliaGateGiveItemfinderText::
	.string "Hi, you must be"
	.string "\n{PLAYER}!"
	.string "\pI'm one of PROF."
	.string "\nBEL's aides."
	.string "\pI came to give"
	.string "\nyou this!$"
