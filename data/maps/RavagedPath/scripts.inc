RavagedPath_MapScripts::
	.byte 0

RavagedPath_EventScript_Ranger::
	msgbox RavagedPath_Text_Ranger, MSGBOX_NPC
	end

RavagedPath_EventScript_Hiker::
	msgbox RavagedPath_Text_Hiker, MSGBOX_NPC
	end

RavagedPath_EventScript_Camper::
	msgbox RavagedPath_Text_Camper, MSGBOX_NPC
	end

RavagedPath_Text_Ranger:
	.string "This path caved in ages ago.\p"
	.string "We're still clearing debris where\n"
	.string "we can.$"

RavagedPath_Text_Hiker:
	.string "The water cutting through here used\n"
	.string "to be a proper trail, or so I'm\n"
	.string "told.$"

RavagedPath_Text_Camper:
	.string "Careful up ahead.\p"
	.string "The ground gets uneven past the\n"
	.string "rubble.$"
