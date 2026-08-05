@ RelicPassageBack do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_RelicPassageBack_MapScripts::
	.byte 0

Unova_RelicPassageBack_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_WORKER_RELIC_PASSAGE, Unova_RelicPassageBack_Text_WorkerRelicPassageSeenText, Unova_RelicPassageBack_Text_WorkerRelicPassageBeatenText
	end

Unova_RelicPassageBack_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_PSYCHICF_RELIC_PASSAGE, Unova_RelicPassageBack_Text_PsychicFRelicPassageSeenText, Unova_RelicPassageBack_Text_PsychicFRelicPassageBeatenText
	end

Unova_RelicPassageBack_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_RELIC_PASSAGE, Unova_RelicPassageBack_Text_BackpackerMRelicPassageSeenText, Unova_RelicPassageBack_Text_BackpackerMRelicPassageBeatenText
	end

Unova_RelicPassageBack_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_HEX_MANIAC_RELIC_PASSAGE, Unova_RelicPassageBack_Text_HexManiacRelicPassageSeenText, Unova_RelicPassageBack_Text_HexManiacRelicPassageBeatenText
	end


Unova_RelicPassageBack_Text_WorkerRelicPassageSeenText::
	.string "The fact that you"
	.string "\nare here means…"
	.string "\pYou are also part"
	.string "\nof the sewers?!"
	.string "\pThen I will survey"
	.string "\nyou too!$"

Unova_RelicPassageBack_Text_WorkerRelicPassageBeatenText::
	.string "Huh… Where am I?"
	.string "\nWho are you?$"

Unova_RelicPassageBack_Text_PsychicFRelicPassageSeenText::
	.string "The sewer and this"
	.string "\nRELIC PASSAGE…"
	.string "\pIs it really"
	.string "\ncoincidence that"
	.string "\pthey exist so"
	.string "\nclose to each"
	.string "\lother?$"

Unova_RelicPassageBack_Text_PsychicFRelicPassageBeatenText::
	.string "No! There must be"
	.string "\na reason why!$"

Unova_RelicPassageBack_Text_BackpackerMRelicPassageSeenText::
	.string "First, one big"
	.string "\nlast gulp…"
	.string "\pHold your breath!$"

Unova_RelicPassageBack_Text_BackpackerMRelicPassageBeatenText::
	.string "Puuaaah!"
	.string "\nHolding your"
	.string "\pbreath is really"
	.string "\ntough…$"

Unova_RelicPassageBack_Text_HexManiacRelicPassageSeenText::
	.string "Just being here"
	.string "\nfills me with"
	.string "\lmagical power…$"

Unova_RelicPassageBack_Text_HexManiacRelicPassageBeatenText::
	.string "You seem to be"
	.string "\nfull of magical"
	.string "\lpower, too…$"
