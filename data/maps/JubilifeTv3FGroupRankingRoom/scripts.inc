JubilifeTv3FGroupRankingRoom_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeTv3FGroupRankingRoom_EventScript_Npc1::
	msgbox JubilifeTv3FGroupRankingRoom_Text_Npc1, MSGBOX_NPC
	end

JubilifeTv3FGroupRankingRoom_Text_Npc1:
	.string "You can see the rankings of people\nin your group here.\pIt makes me try even harder 'cause\nI can't stand losing to my friends!$"

JubilifeTv3FGroupRankingRoom_EventScript_Npc2::
	msgbox JubilifeTv3FGroupRankingRoom_Text_Npc2, MSGBOX_NPC
	end

JubilifeTv3FGroupRankingRoom_Text_Npc2:
	.string "These rankings are nifty!\pI'm going to make a group and\ncompete with all my best friends!$"
