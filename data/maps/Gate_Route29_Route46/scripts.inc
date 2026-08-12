Gate_Route29_Route46_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Gate_Route29_Route46_EventScript_Officer::
	lock
	faceplayer
	msgbox Gate_Route29_Route46_Text_Officer, MSGBOX_DEFAULT
	closemessage
	release
	end

Gate_Route29_Route46_Text_Officer::
	.string "You can't climb ledges.\p"
	.string "But you can jump down from\n"
	.string "them to take a shortcut.$"

Gate_Route29_Route46_EventScript_Youngster::
	lock
	faceplayer
	msgbox Gate_Route29_Route46_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

Gate_Route29_Route46_Text_Youngster::
	.string "Different kinds of POKéMON\n"
	.string "appear past here.\p"
	.string "If you want to catch them all,\n"
	.string "you have to look everywhere.$"
