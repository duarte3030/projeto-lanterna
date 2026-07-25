Route205_South_MapScripts::
	.byte 0

Route205_South_EventScript_BugCatcher::
	msgbox Route205_South_Text_BugCatcher, MSGBOX_NPC
	end

Route205_South_EventScript_Daniel::
	lock
	faceplayer
	msgbox Route205_South_Text_Daniel, MSGBOX_DEFAULT
	release
	end

Route205_South_EventScript_Jacob::
	lock
	faceplayer
	msgbox Route205_South_Text_Jacob, MSGBOX_DEFAULT
	release
	end

Route205_South_EventScript_Siena::
	lock
	faceplayer
	msgbox Route205_South_Text_Siena, MSGBOX_DEFAULT
	release
	end

Route205_South_EventScript_Nicholas::
	lock
	faceplayer
	msgbox Route205_South_Text_Nicholas, MSGBOX_DEFAULT
	release
	end

Route205_South_Text_BugCatcher:
	.string "This is a great place to catch\n"
	.string "Bug POKéMON. So many of them!$"

Route205_South_Text_Daniel:
	.string "I'm hiking all the way from\n"
	.string "OREBURGH CITY. My legs are tired!$"

Route205_South_Text_Jacob:
	.string "I set up camp right here. The\n"
	.string "view of the valley is amazing.$"

Route205_South_Text_Siena:
	.string "FLOAROMA TOWN smells wonderful\n"
	.string "this time of year, doesn't it?$"

Route205_South_Text_Nicholas:
	.string "The VALLEY WINDWORKS is just\n"
	.string "past here. It generates power.$"
