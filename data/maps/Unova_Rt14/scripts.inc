@ Rt14 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt14_MapScripts::
	.byte 0

Unova_Rt14_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_PRESCHOOLERM_R14_1, Unova_Rt14_Text_PreschoolerM1R14SeenText, Unova_Rt14_Text_PreschoolerM1R14BeatenText
	end

Unova_Rt14_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_PRESCHOOLERF_R14_1, Unova_Rt14_Text_PreschoolerF1R14SeenText, Unova_Rt14_Text_PreschoolerF1R14BeatenText
	end

Unova_Rt14_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_PRESCHOOLERM_R14_2, Unova_Rt14_Text_PreschoolerM2R14SeenText, Unova_Rt14_Text_PreschoolerM2R14BeatenText
	end

Unova_Rt14_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_PRESCHOOLERF_R14_2, Unova_Rt14_Text_PreschoolerF2R14SeenText, Unova_Rt14_Text_PreschoolerF2R14BeatenText
	end

Unova_Rt14_EventScript_Npc4::
	msgbox Unova_Rt14_Text_R14PrizeGiverSeenText, MSGBOX_NPC
	end


Unova_Rt14_Text_PreschoolerM1R14SeenText::
	.string "We're the five"
	.string "\ntrainers of the"
	.string "\lUNDELLA TOWN"
	.string "\lschool!"
	.string "\pCan you beat all"
	.string "\nof us?$"

Unova_Rt14_Text_PreschoolerM1R14BeatenText::
	.string "Wha? I lost?$"

Unova_Rt14_Text_PreschoolerF1R14SeenText::
	.string "I'm number two!"
	.string "\nI won't go easy!$"

Unova_Rt14_Text_PreschoolerF1R14BeatenText::
	.string "Uh-oh, I lost…$"

Unova_Rt14_Text_PreschoolerM2R14SeenText::
	.string "What comes after"
	.string "\ntwo? It's three!"
	.string "\pEveryone knows"
	.string "\nthat!$"

Unova_Rt14_Text_PreschoolerM2R14BeatenText::
	.string "Ow! I got beat!$"

Unova_Rt14_Text_PreschoolerF2R14SeenText::
	.string "Are you tired yet?"
	.string "\nIf you can beat"
	.string "\pme, you get to"
	.string "\nbattle Teacher!$"

Unova_Rt14_Text_PreschoolerF2R14BeatenText::
	.string "I lost too…$"

Unova_Rt14_Text_R14PrizeGiverSeenText::
	.string "Good job making it"
	.string "\npast our little"
	.string "\ltest, trainer!"
	.string "\pIf you can beat"
	.string "\nme, you'll receive"
	.string "\la fabulous prize!"
	.string "\pGo on, let's get"
	.string "\nstarted!$"
