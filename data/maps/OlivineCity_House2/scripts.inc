OlivineCity_House2_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

OlivineCity_EventScript_PunisherBoy::
	lock
	faceplayer
	msgbox OlivineCity_Text_PunishmentBoy, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_Text_PunishmentBoy::
	.string "Whenever I get in trouble,\n"
	.string "big bro always scares me.$"

OlivineCity_EventScript_Punisher::
	lock
	faceplayer
	msgbox OlivineCity_Text_PunishmentBro, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_Text_PunishmentBro::
	.string "Along the way to CIANWOOD,\n"
	.string "there are four deserted islands.\p"
	.string "Bad kids are taken to those\n"
	.string "islands as punishment!$"
