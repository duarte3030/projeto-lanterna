@ VictoryRoadGrove do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VictoryRoadGrove_MapScripts::
	.byte 0

Unova_VictoryRoadGrove_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_VICTORY_ROAD_EXT_2, Unova_VictoryRoadGrove_Text_AceTrainerMVictoryRoadGroveSeenText, Unova_VictoryRoadGrove_Text_AceTrainerMVictoryRoadGroveBeatenText
	end

Unova_VictoryRoadGrove_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_VICTORY_ROAD_EXT_1, Unova_VictoryRoadGrove_Text_AceTrainerFVictoryRoadGroveSeenText, Unova_VictoryRoadGrove_Text_AceTrainerFVictoryRoadGroveBeatenText
	end


Unova_VictoryRoadGrove_Text_AceTrainerMVictoryRoadGroveSeenText::
	.string "One, you are a"
	.string "\nPOKéMON trainer."
	.string "\pTwo, I am an ACE"
	.string "\nTRAINER. Put them"
	.string "\ptogether, and it's"
	.string "\nobvious that we're"
	.string "\lgoing to battle!$"

Unova_VictoryRoadGrove_Text_AceTrainerMVictoryRoadGroveBeatenText::
	.string "One, you won! Two,"
	.string "\nI lost…$"

Unova_VictoryRoadGrove_Text_AceTrainerFVictoryRoadGroveSeenText::
	.string "I want to show how"
	.string "\nmuch I love POKé-"
	.string "\lMON by winning!$"

Unova_VictoryRoadGrove_Text_AceTrainerFVictoryRoadGroveBeatenText::
	.string "I can't show my"
	.string "\nlove for my POKé-"
	.string "\pMON if I go and"
	.string "\nlose…$"
