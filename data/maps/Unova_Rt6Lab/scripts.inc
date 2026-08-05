@ Rt6Lab do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt6Lab_MapScripts::
	.byte 0

Unova_Rt6Lab_EventScript_Placa2::
	msgbox Unova_Rt6Lab_Text_R6LabBlackboardText, MSGBOX_SIGN
	end

Unova_Rt6Lab_EventScript_Placa3::
	msgbox Unova_Rt6Lab_Text_R6LabBlackboardText, MSGBOX_SIGN
	end

Unova_Rt6Lab_EventScript_Npc0::
	msgbox Unova_Rt6Lab_Text_R6LabScientistMText, MSGBOX_NPC
	end

Unova_Rt6Lab_EventScript_Npc1::
	msgbox Unova_Rt6Lab_Text_R6LabAskRockText, MSGBOX_NPC
	end


Unova_Rt6Lab_Text_R6LabBlackboardText::
	.string "It's covered in"
	.string "\ncomplex formulas.$"

Unova_Rt6Lab_Text_R6LabScientistMText::
	.string "Here in this lab,"
	.string "\nwe study the"
	.string "\pweather patterns"
	.string "\nacross UNOVA.$"

Unova_Rt6Lab_Text_R6LabAskRockText::
	.string "I'm researching"
	.string "\ncertain rocks that"
	.string "\pcan affect the"
	.string "\nweather."
	.string "\pIf you have one,"
	.string "\nwould you mind"
	.string "\lgiving it to me?"
	.string "\pI can trade you"
	.string "\nsome shards in"
	.string "\lreturn."
	.string "\pWill you give me"
	.string "\na rock?$"
