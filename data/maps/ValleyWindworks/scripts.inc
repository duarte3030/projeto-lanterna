ValleyWindworks_MapScripts::
	.byte 0

ValleyWindworks_EventScript_Worker1::
	msgbox ValleyWindworks_Text_Worker1, MSGBOX_NPC
	end

ValleyWindworks_EventScript_Worker2::
	msgbox ValleyWindworks_Text_Worker2, MSGBOX_NPC
	end

ValleyWindworks_EventScript_Sign::
	msgbox ValleyWindworks_Text_Sign, MSGBOX_SIGN
	end

ValleyWindworks_Text_Worker1:
	.string "These turbines keep the lights on\n"
	.string "for half of Sinnoh.$"

ValleyWindworks_Text_Worker2:
	.string "Careful around the blades, trainer.\n"
	.string "The wind out here doesn't quit.$"

ValleyWindworks_Text_Sign:
	.string "VALLEY WINDWORKS\n"
	.string "Sinnoh's Clean Energy Plant$"
