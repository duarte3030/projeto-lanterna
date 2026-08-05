@ RelicPassageFront do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_RelicPassageFront_MapScripts::
	.byte 0

Unova_RelicPassageFront_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_NURSE_RELIC_PASSAGE, Unova_RelicPassageFront_Text_RelicPassageNurseIntroText, Unova_RelicPassageFront_Text_RelicPassageNurseWinText
	end

Unova_RelicPassageFront_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_PSYCHICM_RELIC_PASSAGE, Unova_RelicPassageFront_Text_PsychicMRelicPassageSeenText, Unova_RelicPassageFront_Text_PsychicMRelicPassageBeatenText
	end

Unova_RelicPassageFront_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_HIKER_RELIC_PASSAGE_1, Unova_RelicPassageFront_Text_Hiker1RelicPassageSeenText, Unova_RelicPassageFront_Text_Hiker1RelicPassageBeatenText
	end

Unova_RelicPassageFront_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_HIKER_RELIC_PASSAGE_2, Unova_RelicPassageFront_Text_Hiker2RelicPassageSeenText, Unova_RelicPassageFront_Text_Hiker2RelicPassageBeatenText
	end

Unova_RelicPassageFront_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_RELIC_PASSAGE, Unova_RelicPassageFront_Text_BackpackerFRelicPassageSeenText, Unova_RelicPassageFront_Text_BackpackerFRelicPassageBeatenText
	end


Unova_RelicPassageFront_Text_RelicPassageNurseIntroText::
	.string "I'm a nurse, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_RelicPassageFront_Text_RelicPassageNurseWinText::
	.string "Ah, I see.$"

Unova_RelicPassageFront_Text_PsychicMRelicPassageSeenText::
	.string "It's coming… It's"
	.string "\ncoming! The"
	.string "\pancient spiritual"
	.string "\npower!$"

Unova_RelicPassageFront_Text_PsychicMRelicPassageBeatenText::
	.string "The ancient power!"
	.string "\nThe sacred power!$"

Unova_RelicPassageFront_Text_Hiker1RelicPassageSeenText::
	.string "Hold up! Did you"
	.string "\nknow this path was"
	.string "\psupposedly made"
	.string "\nages and ages ago?$"

Unova_RelicPassageFront_Text_Hiker1RelicPassageBeatenText::
	.string "S-sorry… I just"
	.string "\ngot so excited…$"

Unova_RelicPassageFront_Text_Hiker2RelicPassageSeenText::
	.string "Just because you"
	.string "\nwork hard doesn't"
	.string "\pmean you're gonna"
	.string "\nget what you want!"
	.string "\pBut if you don't"
	.string "\nwork hard, there"
	.string "\pare many things"
	.string "\nyou can't do!$"

Unova_RelicPassageFront_Text_Hiker2RelicPassageBeatenText::
	.string "Everything went"
	.string "\ndark all of a"
	.string "\lsudden!$"

Unova_RelicPassageFront_Text_BackpackerFRelicPassageSeenText::
	.string "My path and yours…"
	.string "\nThey cross here"
	.string "\land now…$"

Unova_RelicPassageFront_Text_BackpackerFRelicPassageBeatenText::
	.string "Now that I think"
	.string "\nabout it, I've"
	.string "\lcome quite far…$"
