@ DesertResort do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_DesertResort_MapScripts::
	.byte 0

Unova_DesertResort_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_ROUGHNECK_DESERT, Unova_DesertResort_Text_RoughneckDesertSeenText, Unova_DesertResort_Text_RoughneckDesertBeatenText
	end

Unova_DesertResort_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_HEX_MANIAC_DESERT, Unova_DesertResort_Text_HexManiacDesertSeenText, Unova_DesertResort_Text_HexManiacDesertBeatenText
	end

Unova_DesertResort_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_DESERT, Unova_DesertResort_Text_YoungsterDesertSeenText, Unova_DesertResort_Text_YoungsterDesertBeatenText
	end

Unova_DesertResort_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_DESERT, Unova_DesertResort_Text_BackpackerMDesertSeenText, Unova_DesertResort_Text_BackpackerMDesertBeatenText
	end

Unova_DesertResort_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_DESERT, Unova_DesertResort_Text_BackpackerFDesertSeenText, Unova_DesertResort_Text_BackpackerFDesertBeatenText
	end

Unova_DesertResort_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_DESERT, Unova_DesertResort_Text_PkmnRangerMDesertSeenText, Unova_DesertResort_Text_PkmnRangerMDesertBeatenText
	end

Unova_DesertResort_EventScript_Lider14::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_DESERT, Unova_DesertResort_Text_PkmnRangerFDesertSeenText, Unova_DesertResort_Text_PkmnRangerFDesertBeatenText
	end

Unova_DesertResort_EventScript_Lider15::
	trainerbattle_single TRAINER_UNOVA_LASS_DESERT, Unova_DesertResort_Text_LassDesertSeenText, Unova_DesertResort_Text_LassDesertBeatenText
	end

Unova_DesertResort_EventScript_Lider16::
	trainerbattle_single TRAINER_UNOVA_NURSE_DESERT, Unova_DesertResort_Text_DesertNurseIntroText, Unova_DesertResort_Text_DesertNurseWinText
	end

Unova_DesertResort_EventScript_Npc17::
	msgbox Unova_DesertResort_Text_DesertSandManGiveText, MSGBOX_NPC
	end


Unova_DesertResort_Text_RoughneckDesertSeenText::
	.string "My shiny head is a"
	.string "\nreflection of my"
	.string "\lfighting spirit!$"

Unova_DesertResort_Text_RoughneckDesertBeatenText::
	.string "My shine is set"
	.string "\nto blind!$"

Unova_DesertResort_Text_HexManiacDesertSeenText::
	.string "Hm… You're strong,"
	.string "\naren't you?"
	.string "\pIt's tough when"
	.string "\nyou know that"
	.string "\pbefore you even"
	.string "\nstart the fight.$"

Unova_DesertResort_Text_HexManiacDesertBeatenText::
	.string "Urk… I can't do"
	.string "\nanything to you…$"

Unova_DesertResort_Text_YoungsterDesertSeenText::
	.string "Starting a day"
	.string "\nago, I decided to"
	.string "\lbecome a bad dude!$"

Unova_DesertResort_Text_YoungsterDesertBeatenText::
	.string "I guess I can't"
	.string "\njust become a bad"
	.string "\pdude. It's tougher"
	.string "\nthan it looks!$"

Unova_DesertResort_Text_BackpackerMDesertSeenText::
	.string "If you want to"
	.string "\nknow what I've got"
	.string "\pin my backpack,"
	.string "\nwhy don't you try"
	.string "\lto beat me!$"

Unova_DesertResort_Text_BackpackerMDesertBeatenText::
	.string "Wooah! I'm going"
	.string "\nto be buried!$"

Unova_DesertResort_Text_BackpackerFDesertSeenText::
	.string "A desert is like"
	.string "\none giant sandbox,"
	.string "\pright? So come on,"
	.string "\nlet's let our"
	.string "\lPOKéMON play!$"

Unova_DesertResort_Text_BackpackerFDesertBeatenText::
	.string "Since this is for"
	.string "\nplay, whoever has"
	.string "\lthe most fun wins!$"

Unova_DesertResort_Text_PkmnRangerMDesertSeenText::
	.string "I will show you"
	.string "\nthe harshness of"
	.string "\pthe desert through"
	.string "\na battle!$"

Unova_DesertResort_Text_PkmnRangerMDesertBeatenText::
	.string "Desert… hot…"
	.string "\nMouth… dry…$"

Unova_DesertResort_Text_PkmnRangerFDesertSeenText::
	.string "A scorching"
	.string "\ndesert! A passion"
	.string "\pfor adventure! And"
	.string "\na heated battle!$"

Unova_DesertResort_Text_PkmnRangerFDesertBeatenText::
	.string "Hot! Hot! Hot!"
	.string "\nHot!!!$"

Unova_DesertResort_Text_LassDesertSeenText::
	.string "No matter how"
	.string "\ndesperately I try"
	.string "\pto scoop up the"
	.string "\nsand, it flows"
	.string "\lthrough my hands."
	.string "\pIt's kind of sad"
	.string "\nsomehow…$"

Unova_DesertResort_Text_LassDesertBeatenText::
	.string "Victory slips"
	.string "\naway… Just like"
	.string "\lthe sand…$"

Unova_DesertResort_Text_DesertNurseIntroText::
	.string "I'm a nurse, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_DesertResort_Text_DesertNurseWinText::
	.string "Ah, I see.$"

Unova_DesertResort_Text_DesertSandManGiveText::
	.string "You're a POKéMON"
	.string "\ntrainer, right?"
	.string "\pHere, this may"
	.string "\nhelp you.$"
