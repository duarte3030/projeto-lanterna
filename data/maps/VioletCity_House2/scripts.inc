VioletCity_House2_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

VioletCity_House2_EventScript_Teacher::
	lock
	faceplayer
	msgbox VioletCity_NicknameHouse_Text_Teacher, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_NicknameHouse_Text_Teacher::
	.string "She uses the names of her\n"
	.string "favorite things to eat.\p"
	.string "For the nicknames she gives to\n"
	.string "her POKéMON, I mean.$"

VioletCity_House2_EventScript_Lass::
	lock
	faceplayer
	msgbox VioletCity_NicknameHouse_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_NicknameHouse_Text_Lass::
	.string "I call my PIDGEY STRAWBERRY!$"
