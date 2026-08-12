GoldenrodCity_DepartmentStore_7F_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodDeptStore_Text_RoofSuperNerdOhWow::
    .string "Oh, wow!$"

GoldenrodCity_DepartmentStore_7F_EventScript_NerdFala::
	msgbox GoldenrodDeptStore_Text_RoofSuperNerdOhWow, MSGBOX_NPC
	end

GoldenrodDeptStore7_EventScript_PokefanF::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_RoofPokefanF, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_RoofPokefanF::
    .string "Whew, I'm tired.\p"
    .string "I sometimes come up to the rooftop\n"
    .string "to take a break from shopping.$"

GoldenrodDeptStore7_EventScript_PokefanM::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_RoofPokefanM, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_RoofPokefanM::
    .string "There's something I really want,\n"
    .string "but I don't have the necessary cash…\p"
    .string "Maybe I'll sell off the BERRIES I've\n"
    .string "collected…$"

GoldenrodDeptStore7_EventScript_Bugcatcher::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_RoofBugCatcher, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_RoofBugCatcher::
    .string "My POKéMON always get paralyzed or\n"
    .string "poisoned when the chips are down…\p"
    .string "So I came to buy some FULL HEAL.\p"
    .string "I wonder if there's any left?$"
