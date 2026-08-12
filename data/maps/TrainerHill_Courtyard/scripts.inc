TrainerHill_Courtyard_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

BattleTowerOutsideSignText::
	.string "{UP_ARROW} TRAINER HILL ENTRANCE\p"
	.string "“Scale the heights, you hot-blooded\n"
	.string "TRAINERS!”\p"
	.string "{RIGHT_ARROW} BATTLE TENTS.$"

BattleTower_Battle_Tent_Text_Arena::
	.string "BATTLE TENT: ARENA\n"
	.string "“May the Greatest Teams Gather!”$"

BattleTower_Battle_Tent_Text_Factory::
	.string "BATTLE TENT: FACTORY\n"
	.string "“Find it! The ultimate POKéMON!”$"

BattleTower_Battle_Tent_Text_Palace::
	.string "BATTLE TENT: PALACE\n"
	.string "“Feast Your Eyes on Battles!”$"

TrainerHill_Courtyard_EventScript_BattleTowerSign::
	lock
	msgbox BattleTowerOutsideSignText, MSGBOX_SIGN	
	closemessage	
	release
	end

TrainerHill_Courtyard_EventScript_Tent_Arena::
	lock
	msgbox BattleTower_Battle_Tent_Text_Arena, MSGBOX_SIGN	
	closemessage	
	release
	end

TrainerHill_Courtyard_EventScript_Tent_Factory::
	lock
	msgbox BattleTower_Battle_Tent_Text_Factory, MSGBOX_SIGN	
	closemessage	
	release
	end

TrainerHill_Courtyard_EventScript_Tent_Palace::
	lock
	msgbox BattleTower_Battle_Tent_Text_Palace, MSGBOX_SIGN	
	closemessage	
	release
	end

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

BattleTowerOutsideYoungsterText::
	.string "Wow, the TRAINER HILL is huge!\p"
	.string "There must be many kinds of\n"
	.string "POKéMON in there!$"

TrainerHill_Courtyard_EventScript_Youngster::
	lock
	faceplayer
	msgbox BattleTowerOutsideYoungsterText, MSGBOX_DEFAULT
	closemessage
	release
	end

BattleTowerOutsideBeautyText::
	.string "In the BATTLE TENTS, you can\n"
	.string "use only three POKéMON.\p"
	.string "It's so hard to decide which\n"
	.string "three should go into battle…$"

TrainerHill_Courtyard_EventScript_Beauty::
	lock
	faceplayer
	msgbox BattleTowerOutsideBeautyText, MSGBOX_DEFAULT
	closemessage
	release
	end

BattleTowerOutsideSailorText::
	.string "Hehehe, I snuck out from work.\p"
	.string "I can't bail out until I've won!\p"
	.string "I have to win it all. That I must!$"

TrainerHill_Courtyard_EventScript_Sailor::
	lock
	faceplayer
	msgbox BattleTowerOutsideSailorText, MSGBOX_DEFAULT
	closemessage
	release
	end
