VioletCity_House1_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

VioletCity_House1_EventScript_Kyle::
	lock
	faceplayer
	msgbox VioletCity_House1_Text_PokefanM, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_House1_Text_PokefanM::
	.string "A POKéMON you get in a trade\n"
	.string "grows quickly.\p"
	.string "But if you don't have the right\n"
	.string "GYM BADGE, they may disobey you.$"
