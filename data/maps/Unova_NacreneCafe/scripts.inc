@ NacreneCafe do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NacreneCafe_MapScripts::
	.byte 0

Unova_NacreneCafe_EventScript_Npc0::
	msgbox Unova_NacreneCafe_Text_NacreneCafeAskDrinkText, MSGBOX_NPC
	end

Unova_NacreneCafe_EventScript_Npc1::
	msgbox Unova_NacreneCafe_Text_NacreneCafePokefanFText, MSGBOX_NPC
	end

Unova_NacreneCafe_EventScript_Npc2::
	msgbox Unova_NacreneCafe_Text_NacreneCafeMusicianText, MSGBOX_NPC
	end


Unova_NacreneCafe_Text_NacreneCafeAskDrinkText::
	.string "Hi, welcome to"
	.string "\nNACRENE CAFE!"
	.string "\pWould you like to"
	.string "\nbuy a drink?$"

Unova_NacreneCafe_Text_NacreneCafePokefanFText::
	.string "The CAFE offers"
	.string "\ndifferent kinds"
	.string "\lof drinks."
	.string "\pEven POKéMON love"
	.string "\nthem!$"

Unova_NacreneCafe_Text_NacreneCafeMusicianText::
	.string "NACRENE CITY may"
	.string "\nnot be as big as"
	.string "\psome of the other"
	.string "\ncities in UNOVA,"
	.string "\pbut we more than"
	.string "\nmake up for it in"
	.string "\latmosphere!$"
