Mahoganytown_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

MahoganyTown_EventScript_CandybarSign::
	lock
	msgbox MahoganyTown_Text_RagecandybarSign, MSGBOX_SIGN
	closemessage
	release
	end

MahoganyTown_EventScript_GymSign::
	lock
	msgbox MahoganyTown_Text_GymSign, MSGBOX_SIGN
	closemessage
	release
	end

MahoganyTown_EventScript_Sign::
	lock
	msgbox MahoganyTown_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

MahoganyTown_Text_GymSign::
    .string "MAHOGANY TOWN POKéMON GYM\p"
    .string "LEADER: PRYCE\p"
    .string "The Teacher of Winter's Harshness$"

MahoganyTown_Text_RagecandybarSign::
    .string "While visiting MAHOGANY TOWN, try\n"
    .string "a RAGECANDYBAR!$"

MahoganyTown_Text_Sign::
    .string "MAHOGANY TOWN\p"
    .string "Welcome to the Home of the Ninja$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

MahoganyTown_EventScript_Lass::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyTown_Text_Lass::
    .string "Visit Grandma's shop. She sells\n"
    .string "stuff that nobody else has.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

MahoganyTown_EventScript_Fisher::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Fisher, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyTown_Text_Fisher::
    .string "Since you came this far, take the\n"
    .string "time to do some sightseeing.\p"
    .string "You should head north and check\n"
    .string "out LAKE OF RAGE right now.$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

MahoganyTown_EventScript_Povoa1::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

MahoganyTown_Text_Povoa1:
	.string "The mountain air keeps this town\ncold most of the year.$"

MahoganyTown_EventScript_Povoa2::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

MahoganyTown_Text_Povoa2:
	.string "The shop here sells souvenirs.\nRead the labels twice.$"

MahoganyTown_EventScript_Povoa3::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

MahoganyTown_Text_Povoa3:
	.string "The GYM freezes. Fire and Rock\nwork. So do Steel and Fighting.$"

MahoganyTown_EventScript_Povoa4::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

MahoganyTown_Text_Povoa4:
	.string "ROUTE 43 north leads to the\nLAKE OF RAGE.$"

MahoganyTown_EventScript_Povoa5::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

MahoganyTown_Text_Povoa5:
	.string "Snow makes every fight slower.\nPatience wins here.$"

MahoganyTown_EventScript_Povoa6::
	lock
	faceplayer
	msgbox MahoganyTown_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

MahoganyTown_Text_Povoa6:
	.string "I like the quiet. Most people\nleave for GOLDENROD.$"

@ <<< Povoamento: fim do bloco gerado <<<
