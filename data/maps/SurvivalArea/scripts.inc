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

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SurvivalArea_EventScript_Npc1::
	msgbox SurvivalArea_Text_Npc1, MSGBOX_NPC
	end

SurvivalArea_Text_Npc1:
	.string "I'm taking the Frontier challenges to\nscore some commemorative prints.$"

SurvivalArea_EventScript_Npc2::
	msgbox SurvivalArea_Text_Npc2, MSGBOX_NPC
	end

SurvivalArea_Text_Npc2:
	.string "Trainers who lose at the Battle\nFrontier come here to train.$"

SurvivalArea_EventScript_Npc3::
	msgbox SurvivalArea_Text_Npc3, MSGBOX_NPC
	end

SurvivalArea_Text_Npc3:
	.string "Hey, traveling Trainer.\nIs your big Bag full of items?\pOr is it full of dreams?$"

SurvivalArea_EventScript_Npc4::
	msgbox SurvivalArea_Text_Npc4, MSGBOX_NPC
	end

SurvivalArea_Text_Npc4:
	.string "I'm a Cameraman, obviously.\pHave you seen that TV program,\n'Search for the Red GYARADOS!'?\pYeah, that outstanding documentary!\nI filmed that!$"

SurvivalArea_EventScript_Placa5::
	msgbox SurvivalArea_Text_Placa5, MSGBOX_SIGN
	end

SurvivalArea_Text_Placa5:
	.string "Survival Area\nStaging Point$"

SurvivalArea_EventScript_Placa6::
	msgbox SurvivalArea_Text_Placa6, MSGBOX_SIGN
	end

SurvivalArea_Text_Placa6:
	.string "The door is shut tight.\n'Members Only' is painted on it.$"
