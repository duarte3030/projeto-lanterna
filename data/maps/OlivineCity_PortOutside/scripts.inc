OlivineCity_PortOutside_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

OlivineCity_PortOutside_EventScript_Fisherman1::
	lock
	faceplayer
	msgbox OlivineCity_PortOutside_Text_PortFisherman1, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_PortOutside_Text_PortFisherman1::
	.string "FAST SHIP S.S.AQUA used to sail to\n"
	.string "KANTO on Mondays and Fridays. But\l"
	.string "now, it sails almost constantly!$"

OlivineCity_PortOutside_EventScript_Fisherman2::
	lock
	faceplayer
	msgbox OlivineCity_PortOutside_Text_Fisherman2, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_PortOutside_Text_Fisherman2::
	.string "Aw yeah, I'm fishin'.$"
