@ Fenda do tempo, do outro lado do Spear Pillar distorcido.
@ Texto de pret/pokeplatinum, res/text/spear_pillar_dialga.json.
@ Layout emprestado do Cave of Origin B1F.
@
@ ponytail: o Dialga e um bg_event, nao um object_event, porque esta build nao
@ desenha sprite de Dialga (nao ha entrada fora de #if IS_FRLG em
@ src/data/object_events/object_event_graphics_info_pointers.h). Sem sprite, sem
@ crash na tela de titulo.
@
@ O encontro e unico: FLAG_CAUGHT_DIALGA fecha a fenda depois de vitoria ou
@ captura. Fuga e derrota nao contam, para nao apagar o lendario do save.

SpearPillar_Dialga_MapScripts::
	.byte 0

SpearPillar_Dialga_EventScript_Dialga::
	lockall
	goto_if_set FLAG_CAUGHT_DIALGA, SpearPillar_Dialga_EventScript_RiftIsQuiet
	msgbox SpearPillar_Dialga_Text_WillYouChallengeDialga, MSGBOX_DEFAULT
	msgbox SpearPillar_Dialga_Text_DialgaCry, MSGBOX_DEFAULT
	playmoncry SPECIES_DIALGA, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_DIALGA, 47
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, SpearPillar_Dialga_EventScript_RiftCloses
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SpearPillar_Dialga_EventScript_RiftCloses
	releaseall
	end

@ ponytail: so fecha em vitoria ou captura. Fugir, perder ou ser teleportado
@ deixa a fenda aberta, senao um Poke Ball errado apagaria o lendario do save.
SpearPillar_Dialga_EventScript_RiftCloses::
	setflag FLAG_CAUGHT_DIALGA
	releaseall
	end

SpearPillar_Dialga_EventScript_RiftIsQuiet::
	msgbox SpearPillar_Dialga_Text_RiftIsQuiet, MSGBOX_DEFAULT
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

SpearPillar_Dialga_Text_RiftIsQuiet:
	.string "The rift has closed over.\p"
	.string "Not a trace of time stirs here\n"
	.string "any more.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SpearPillar_Dialga_EventScript_Placa1::
	msgbox SpearPillar_Dialga_Text_Placa1, MSGBOX_SIGN
	end

SpearPillar_Dialga_Text_Placa1:
	.string "On the other side of the rift...\nIn a fantastically bizarre place...\pIt's DIALGA!\pWill you challenge DIALGA?$"

SpearPillar_Dialga_EventScript_Placa2::
	msgbox SpearPillar_Dialga_Text_Placa2, MSGBOX_SIGN
	end

SpearPillar_Dialga_Text_Placa2:
	.string "On the other side of the rift...\nIn a fantastically bizarre place...\pIt's DIALGA!\pWill you challenge DIALGA?$"
