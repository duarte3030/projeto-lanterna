MahoganyTown_House1_MapScripts::
	.byte 0

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

MahoganyRedGyaradosHouse_Text_BlackBelt::
    .string "I heard that a red GYARADOS appeared\n"
    .string "at the LAKE.\p"
    .string "That's odd, since even ordinary\n"
    .string "GYARADOS are rare in that lake…$"

MahoganyTown_House1_EventScript_BlackBelt::
	msgbox MahoganyRedGyaradosHouse_Text_BlackBelt, MSGBOX_NPC
	end
