SurvivalArea_MapScripts::
	.byte 0

SurvivalArea_EventScript_RuinManiac::
	msgbox SurvivalArea_Text_RuinManiac, MSGBOX_NPC
	end

SurvivalArea_EventScript_BattleGirl::
	msgbox SurvivalArea_Text_BattleGirl, MSGBOX_NPC
	end

SurvivalArea_EventScript_Youngster::
	msgbox SurvivalArea_Text_Youngster, MSGBOX_NPC
	end

SurvivalArea_EventScript_Cameraman::
	lock
	faceplayer
	msgbox SurvivalArea_Text_Cameraman, MSGBOX_DEFAULT
	release
	end

SurvivalArea_Text_RuinManiac:
	.string "I study the old ruins scattered\n"
	.string "across the SURVIVAL AREA.$"

SurvivalArea_Text_BattleGirl:
	.string "Only the toughest TRAINERS make it\n"
	.string "out this far. Are you one of\l"
	.string "them?$"

SurvivalArea_Text_Youngster:
	.string "It's freezing way out here! But\n"
	.string "the POKéMON are worth it.$"

SurvivalArea_Text_Cameraman:
	.string "I'm a Cameraman, obviously. Have\n"
	.string "you seen that TV program, “Search\l"
	.string "for the Red GYARADOS!”? Yeah,\p"
	.string "that outstanding documentary!\n"
	.string "I filmed that!$"
