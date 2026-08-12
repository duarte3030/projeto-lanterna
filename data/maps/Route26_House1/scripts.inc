Route26_House1_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route26_Text_HealHouseRest::
    .string "Your POKéMON look a little tired.\p"
    .string "You should rest them a while.$"

Route26_House1_EventScript_HealWomanFala::
	msgbox Route26_Text_HealHouseRest, MSGBOX_NPC
	end
