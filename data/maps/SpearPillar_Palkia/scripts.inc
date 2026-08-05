@ Fenda do espaco, do outro lado do Spear Pillar distorcido.
@ Texto de pret/pokeplatinum, res/text/spear_pillar_palkia.json.
@ Layout emprestado de um mapa nao usado do Cave of Origin.
@ Mesmas ressalvas do SpearPillar_Dialga: bg_event em vez de sprite, e encontro
@ repetivel porque nao posso criar flag nesta tarefa.

SpearPillar_Palkia_MapScripts::
	.byte 0

SpearPillar_Palkia_EventScript_Palkia::
	lockall
	msgbox SpearPillar_Palkia_Text_WillYouChallengePalkia, MSGBOX_DEFAULT
	msgbox SpearPillar_Palkia_Text_PalkiaCry, MSGBOX_DEFAULT
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_PALKIA, 47
	dowildbattle
	releaseall
	end

SpearPillar_Palkia_Text_WillYouChallengePalkia:
	.string "On the other side of the rift...\n"
	.string "In a fantastically bizarre place...\p"
	.string "It's PALKIA!\p"
	.string "An overwhelming feeling of space\n"
	.string "powerfully emanates from this\l"
	.string "rift...$"

SpearPillar_Palkia_Text_PalkiaCry:
	.string "PALKIA: Gagyagyaah!$"
