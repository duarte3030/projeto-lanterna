CherrygroveCity_House2_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

CherrygroveCity_GuideHouse_Text_GuideGent::
	.string "When I was a wee lad, I was a\n"
	.string "hotshot trainer!\p"
	.string "Here's a word of advice:\n"
	.string "Catch lots of POKéMON!\p"
	.string "Treat them all with kindness!$"

CherrygroveCity_House2_EventScript_GuideGent::
	lock
	faceplayer
	msgbox CherrygroveCity_GuideHouse_Text_GuideGent, MSGBOX_DEFAULT
	closemessage
	release
	end
