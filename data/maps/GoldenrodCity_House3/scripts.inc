GoldenrodCity_House3_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodCity_House3_EventScript_PokefanM::
	lock
	faceplayer
	msgbox GoldenrodHappinessRater_Text_PokefanM, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodHappinessRater_Text_PokefanM::
    .string "I keep losing in battles, and my\n"
    .string "POKéMON end up fainting…\p"
    .string "Maybe that's why my POKéMON don't\n"
    .string "like me much…$"

GoldenrodCity_House3_EventScript_Twin::
	lock
	faceplayer
	msgbox GoldenrodHappinessRater_Text_Twin, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodHappinessRater_Text_Twin::
    .string "When I use an item on my POKéMON,\n"
    .string "it acts really glad!$"
