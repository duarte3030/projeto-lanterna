@ VictoryRoadOutdoor1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VictoryRoadOutdoor1F_MapScripts::
	.byte 0

Unova_VictoryRoadOutdoor1F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_NURSE_VICTORY_ROAD, Unova_VictoryRoadOutdoor1F_Text_VictoryRoadNurseIntroText, Unova_VictoryRoadOutdoor1F_Text_VictoryRoadNurseWinText
	end

Unova_VictoryRoadOutdoor1F_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_VICTORY_ROAD_EXT, Unova_VictoryRoadOutdoor1F_Text_BackpackerFVictoryRoadOutdoor1FSeenText, Unova_VictoryRoadOutdoor1F_Text_BackpackerFVictoryRoadOutdoor1FBeatenText
	end

Unova_VictoryRoadOutdoor1F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_VETERANF_VICTORY_ROAD_EXT_1, Unova_VictoryRoadOutdoor1F_Text_VeteranFVictoryRoadOutdoor1FSeenText, Unova_VictoryRoadOutdoor1F_Text_VeteranFVictoryRoadOutdoor1FBeatenText
	end

Unova_VictoryRoadOutdoor1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_VETERANM_VICTORY_ROAD_EXT_1, Unova_VictoryRoadOutdoor1F_Text_VeteranMVictoryRoadOutdoor1FSeenText, Unova_VictoryRoadOutdoor1F_Text_VeteranMVictoryRoadOutdoor1FBeatenText
	end


Unova_VictoryRoadOutdoor1F_Text_VictoryRoadNurseIntroText::
	.string "I'm a nurse, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_VictoryRoadOutdoor1F_Text_VictoryRoadNurseWinText::
	.string "Ah, I see.$"

Unova_VictoryRoadOutdoor1F_Text_BackpackerFVictoryRoadOutdoor1FSeenText::
	.string "I am…"
	.string "\pEx-TEAM PLASMA!$"

Unova_VictoryRoadOutdoor1F_Text_BackpackerFVictoryRoadOutdoor1FBeatenText::
	.string "Eek! You're like"
	.string "\nthat trainer from"
	.string "\pall those years"
	.string "\nago!$"

Unova_VictoryRoadOutdoor1F_Text_VeteranFVictoryRoadOutdoor1FSeenText::
	.string "Wait! You, young"
	.string "\ntrainer over"
	.string "\pthere! Look at my"
	.string "\nPOKéMON.$"

Unova_VictoryRoadOutdoor1F_Text_VeteranFVictoryRoadOutdoor1FBeatenText::
	.string "Not bad! I like"
	.string "\nyour strength.$"

Unova_VictoryRoadOutdoor1F_Text_VeteranMVictoryRoadOutdoor1FSeenText::
	.string "Are you sure you"
	.string "\nwant to seriously"
	.string "\ptake on someone"
	.string "\nlike me, who"
	.string "\lbattles seriously?$"

Unova_VictoryRoadOutdoor1F_Text_VeteranMVictoryRoadOutdoor1FBeatenText::
	.string "This is the pain"
	.string "\nthat comes from"
	.string "\pseriously taking"
	.string "\nsomeone head on…$"
