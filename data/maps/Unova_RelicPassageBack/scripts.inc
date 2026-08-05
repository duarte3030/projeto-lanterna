@ RelicPassageBack do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_RelicPassageBack_MapScripts::
	.byte 0

Unova_RelicPassageBack_EventScript_Npc6::
	msgbox Unova_RelicPassageBack_Text_WorkerRelicPassageSeenText, MSGBOX_NPC
	end

Unova_RelicPassageBack_EventScript_Npc7::
	msgbox Unova_RelicPassageBack_Text_PsychicFRelicPassageSeenText, MSGBOX_NPC
	end

Unova_RelicPassageBack_EventScript_Npc8::
	msgbox Unova_RelicPassageBack_Text_BackpackerMRelicPassageSeenText, MSGBOX_NPC
	end

Unova_RelicPassageBack_EventScript_Npc9::
	msgbox Unova_RelicPassageBack_Text_HexManiacRelicPassageSeenText, MSGBOX_NPC
	end


Unova_RelicPassageBack_Text_WorkerRelicPassageSeenText::
	.string "The fact that you"
	.string "\nare here means…"
	.string "\pYou are also part"
	.string "\nof the sewers?!"
	.string "\pThen I will survey"
	.string "\nyou too!$"

Unova_RelicPassageBack_Text_PsychicFRelicPassageSeenText::
	.string "The sewer and this"
	.string "\nRELIC PASSAGE…"
	.string "\pIs it really"
	.string "\ncoincidence that"
	.string "\pthey exist so"
	.string "\nclose to each"
	.string "\lother?$"

Unova_RelicPassageBack_Text_BackpackerMRelicPassageSeenText::
	.string "First, one big"
	.string "\nlast gulp…"
	.string "\pHold your breath!$"

Unova_RelicPassageBack_Text_HexManiacRelicPassageSeenText::
	.string "Just being here"
	.string "\nfills me with"
	.string "\lmagical power…$"
