NewBarkTown_PlayersHouse_1F_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

NewBarkTown_PlayersHouse_1F_Text_MomsFriend::
	.string "Hi, {PLAYER}!\p"
	.string "I'm visiting!\p"
	.string "Have you heard?\p"
	.string "My daughter is adamant about\n"
	.string "becoming PROF.ELM's assistant.\p"
	.string "She really loves POKéMON!$"

NewBarkTown_PlayersHouse_1F_EventScript_MomsFriendFala::
	msgbox NewBarkTown_PlayersHouse_1F_Text_MomsFriend, MSGBOX_NPC
	end
