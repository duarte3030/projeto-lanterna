@ CasteliaSewers do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CasteliaSewers_MapScripts::
	.byte 0

Unova_CasteliaSewers_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTM_CASTELIA_SEWERS, Unova_CasteliaSewers_Text_ScientistMCasteliaSewersSeenText, Unova_CasteliaSewers_Text_ScientistMCasteliaSewersBeatenText
	end

Unova_CasteliaSewers_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTF_CASTELIA_SEWERS, Unova_CasteliaSewers_Text_ScientistFCasteliaSewersSeenText, Unova_CasteliaSewers_Text_ScientistFCasteliaSewersBeatenText
	end

Unova_CasteliaSewers_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_WORKER_CASTELIA_SEWERS_1, Unova_CasteliaSewers_Text_Worker1CasteliaSewersSeenText, Unova_CasteliaSewers_Text_Worker1CasteliaSewersBeatenText
	end

Unova_CasteliaSewers_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_WORKER_CASTELIA_SEWERS_2, Unova_CasteliaSewers_Text_Worker2CasteliaSewersSeenText, Unova_CasteliaSewers_Text_Worker2CasteliaSewersBeatenText
	end

Unova_CasteliaSewers_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_JANITOR_CASTELIA_SEWERS_1, Unova_CasteliaSewers_Text_Janitor1CasteliaSewersSeenText, Unova_CasteliaSewers_Text_Janitor1CasteliaSewersBeatenText
	end

Unova_CasteliaSewers_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_JANITOR_CASTELIA_SEWERS_2, Unova_CasteliaSewers_Text_Janitor2CasteliaSewersSeenText, Unova_CasteliaSewers_Text_Janitor2CasteliaSewersBeatenText
	end

Unova_CasteliaSewers_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_JANITOR_CASTELIA_SEWERS_4, Unova_CasteliaSewers_Text_Janitor3CasteliaSewersSeenText, Unova_CasteliaSewers_Text_Janitor3CasteliaSewersBeatenText
	end

Unova_CasteliaSewers_EventScript_Npc14::
	msgbox Unova_CasteliaSewers_Text_CasteliaSewersBlockerText, MSGBOX_NPC
	end


Unova_CasteliaSewers_Text_ScientistMCasteliaSewersSeenText::
	.string "I'm studying the"
	.string "\nenvironment here.$"

Unova_CasteliaSewers_Text_ScientistMCasteliaSewersBeatenText::
	.string "Oh! Too much data!$"

Unova_CasteliaSewers_Text_ScientistFCasteliaSewersSeenText::
	.string "Hi, would you like"
	.string "\nto assist in my"
	.string "\lresearch?$"

Unova_CasteliaSewers_Text_ScientistFCasteliaSewersBeatenText::
	.string "Duly noted!$"

Unova_CasteliaSewers_Text_Worker1CasteliaSewersSeenText::
	.string "We need sewers,"
	.string "\nbut what about"
	.string "\lPOKéMON?$"

Unova_CasteliaSewers_Text_Worker1CasteliaSewersBeatenText::
	.string "There appears to"
	.string "\nno barrier between"
	.string "\pyou and your"
	.string "\nPOKéMON!$"

Unova_CasteliaSewers_Text_Worker2CasteliaSewersSeenText::
	.string "There's a tunnel"
	.string "\nin the back of"
	.string "\lthe sewers."
	.string "\pIf you can beat"
	.string "\nme, I'll tell you"
	.string "\lhow to get there.$"

Unova_CasteliaSewers_Text_Worker2CasteliaSewersBeatenText::
	.string "Okay, I'll tell"
	.string "\nyou!$"

Unova_CasteliaSewers_Text_Janitor1CasteliaSewersSeenText::
	.string "Cleaning actually"
	.string "\ntakes a lot of"
	.string "\lstrength…$"

Unova_CasteliaSewers_Text_Janitor1CasteliaSewersBeatenText::
	.string "Who cares about"
	.string "\nlosing! There's a"
	.string "\lspot over there!$"

Unova_CasteliaSewers_Text_Janitor2CasteliaSewersSeenText::
	.string "I've been training"
	.string "\nreal hard doing"
	.string "\lall this cleaning!$"

Unova_CasteliaSewers_Text_Janitor2CasteliaSewersBeatenText::
	.string "I missed a spot!$"

Unova_CasteliaSewers_Text_Janitor3CasteliaSewersSeenText::
	.string "Uh-oh, busted!$"

Unova_CasteliaSewers_Text_Janitor3CasteliaSewersBeatenText::
	.string "Darn!$"

Unova_CasteliaSewers_Text_CasteliaSewersBlockerText::
	.string "Hey buddy, there's"
	.string "\nimportant stuff"
	.string "\lgoing on in here."
	.string "\pBuzz off!$"
