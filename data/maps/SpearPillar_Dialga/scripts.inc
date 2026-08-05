@ Fenda do tempo, do outro lado do Spear Pillar distorcido.
@ Texto de pret/pokeplatinum, res/text/spear_pillar_dialga.json.
@ Layout emprestado do Cave of Origin B1F.
@
@ ponytail: o Dialga e um bg_event, nao um object_event, porque esta build nao
@ desenha sprite de Dialga (nao ha entrada fora de #if IS_FRLG em
@ src/data/object_events/object_event_graphics_info_pointers.h). Sem sprite, sem
@ crash na tela de titulo.
@
@ O encontro NAO e unico: marcar "ja capturei" pede uma flag, e criar flag esta
@ fora do escopo desta tarefa. A flag necessaria esta em PENDENCIAS-GALACTICA.md.

SpearPillar_Dialga_MapScripts::
	.byte 0

SpearPillar_Dialga_EventScript_Dialga::
	lockall
	msgbox SpearPillar_Dialga_Text_WillYouChallengeDialga, MSGBOX_DEFAULT
	msgbox SpearPillar_Dialga_Text_DialgaCry, MSGBOX_DEFAULT
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_DIALGA, 47
	dowildbattle
	releaseall
	end

SpearPillar_Dialga_Text_WillYouChallengeDialga:
	.string "On the other side of the rift...\n"
	.string "In a fantastically bizarre place...\p"
	.string "It's DIALGA!\p"
	.string "An overwhelming feeling of time\n"
	.string "powerfully emanates from this\l"
	.string "rift...$"

SpearPillar_Dialga_Text_DialgaCry:
	.string "DIALGA: Gugyugubah!$"
