@ Rt18 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt18_MapScripts::
	.byte 0

Unova_Rt18_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_HIKER_R18, Unova_Rt18_Text_HikerR18SeenText, Unova_Rt18_Text_HikerR18BeatenText
	end

Unova_Rt18_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_R18, Unova_Rt18_Text_BlackbeltR18SeenText, Unova_Rt18_Text_BlackbeltR18BeatenText
	end

Unova_Rt18_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_R18, Unova_Rt18_Text_BattleGirlR18SeenText, Unova_Rt18_Text_BattleGirlR18BeatenText
	end

Unova_Rt18_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_R18, Unova_Rt18_Text_BackpackerMR18SeenText, Unova_Rt18_Text_BackpackerMR18BeatenText
	end

Unova_Rt18_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_R18, Unova_Rt18_Text_BackpackerFR18SeenText, Unova_Rt18_Text_BackpackerFR18BeatenText
	end


Unova_Rt18_Text_HikerR18SeenText::
	.string "When I look down"
	.string "\nfrom a high place,"
	.string "\lI feel very good!"
	.string "\pPOKéMON battles"
	.string "\nare the same!$"

Unova_Rt18_Text_HikerR18BeatenText::
	.string "You're great! I"
	.string "\ncan't help but look"
	.string "\lup to you!$"

Unova_Rt18_Text_BlackbeltR18SeenText::
	.string "I just won a"
	.string "\nbattle back there,"
	.string "\pso I'm feeling"
	.string "\ngood!$"

Unova_Rt18_Text_BlackbeltR18BeatenText::
	.string "Oh whatever! I'm"
	.string "\nin a terrible mood"
	.string "\lnow!$"

Unova_Rt18_Text_BattleGirlR18SeenText::
	.string "Number! Eight!"
	.string "\nTeen!$"

Unova_Rt18_Text_BattleGirlR18BeatenText::
	.string "OK! Thank you very"
	.string "\nmuch!$"

Unova_Rt18_Text_BackpackerMR18SeenText::
	.string "BACKPACKERs are"
	.string "\nexactly what they"
	.string "\lsound like."
	.string "\pThey set out on"
	.string "\nthe road with only"
	.string "\pthe packs on their"
	.string "\nbacks and the"
	.string "\pPOKéMON in their"
	.string "\nPOKéBALLs!$"

Unova_Rt18_Text_BackpackerMR18BeatenText::
	.string "I wish I could"
	.string "\npack some wins in"
	.string "\lmy backpack too…$"

Unova_Rt18_Text_BackpackerFR18SeenText::
	.string "Your POKéMON and"
	.string "\nyour strategy!"
	.string "\pI'll be taking"
	.string "\nnotes on both!$"

Unova_Rt18_Text_BackpackerFR18BeatenText::
	.string "There's still so"
	.string "\nmuch more to"
	.string "\llearn!$"
