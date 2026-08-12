ReceptionGate_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

ReceptionGate_EventScript_Officer::
    msgbox VictoryRoadGate_Text_EightBadges, MSGBOX_NPC
    end

VictoryRoadGate_Text_EightBadges::
    .string "Oh! The eight BADGES of JOHTO!\p"
    .string "Please, go right on through!$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

ReceptionGate_EventScript_SilverGuard::
    msgbox VictoryRoadGate_Text_LeftBlackBelt, MSGBOX_NPC
    end

VictoryRoadGate_Text_LeftBlackBelt::
    .string "This way leads to MT.SILVER.\p"
    .string "You'll see scary-strong POKéMON out\n"
    .string "there.$"

ReceptionGate_EventScript_KantoGuard::
    msgbox VictoryRoadGate_Text_RightBlackBelt, MSGBOX_NPC
    end

VictoryRoadGate_Text_RightBlackBelt::
    .string "Off to the POKéMON LEAGUE, are you?\p"
    .string "The ELITE FOUR are so strong it's\n"
    .string "scary, and they're ready for you!$"
