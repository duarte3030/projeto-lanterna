Gate_GoldenrodCity_Route35_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Gate_GoldenrodCity_Route35_EventScript_Fisher::
	lock
	faceplayer
	msgbox Route35GoldenrodGate_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

Route35GoldenrodGate_Text_Fisher::
	.string "I wonder how many kinds of POKéMON\n"
	.string "there are in the world.\p"
	.string "Three years ago, PROF.OAK said that\n"
	.string "there were 150 different kinds.\p"
	.string "But recently I heard there's\n"
	.string "over 400!$"
