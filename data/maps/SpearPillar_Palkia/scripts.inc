@ Fenda do espaco, do outro lado do Spear Pillar distorcido.
@ Texto de pret/pokeplatinum, res/text/spear_pillar_palkia.json.
@ Layout emprestado de um mapa nao usado do Cave of Origin.
@ Mesma ressalva do SpearPillar_Dialga: bg_event em vez de sprite. O encontro e
@ unico, fechado por FLAG_CAUGHT_PALKIA em vitoria ou captura.

SpearPillar_Palkia_MapScripts::
	.byte 0

SpearPillar_Palkia_EventScript_Palkia::
	lockall
	goto_if_set FLAG_CAUGHT_PALKIA, SpearPillar_Palkia_EventScript_RiftIsQuiet
	msgbox SpearPillar_Palkia_Text_WillYouChallengePalkia, MSGBOX_DEFAULT
	msgbox SpearPillar_Palkia_Text_PalkiaCry, MSGBOX_DEFAULT
	playmoncry SPECIES_PALKIA, CRY_MODE_ENCOUNTER
	waitmoncry
	setwildbattle SPECIES_PALKIA, 47
	dowildbattle
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, SpearPillar_Palkia_EventScript_RiftCloses
	goto_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SpearPillar_Palkia_EventScript_RiftCloses
	releaseall
	end

@ ponytail: so fecha em vitoria ou captura. Fugir, perder ou ser teleportado
@ deixa a fenda aberta, senao um Poke Ball errado apagaria o lendario do save.
SpearPillar_Palkia_EventScript_RiftCloses::
	setflag FLAG_CAUGHT_PALKIA
	releaseall
	end

SpearPillar_Palkia_EventScript_RiftIsQuiet::
	msgbox SpearPillar_Palkia_Text_RiftIsQuiet, MSGBOX_DEFAULT
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

SpearPillar_Palkia_Text_RiftIsQuiet:
	.string "The rift has closed over.\p"
	.string "Not a trace of space stirs here\n"
	.string "any more.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SpearPillar_Palkia_EventScript_Placa1::
	msgbox SpearPillar_Palkia_Text_Placa1, MSGBOX_SIGN
	end

SpearPillar_Palkia_Text_Placa1:
	.string "On the other side of the rift...\nIn a fantastically bizarre place...\pIt's PALKIA!\pWill you challenge PALKIA?$"

SpearPillar_Palkia_EventScript_Placa2::
	msgbox SpearPillar_Palkia_Text_Placa2, MSGBOX_SIGN
	end

SpearPillar_Palkia_Text_Placa2:
	.string "On the other side of the rift...\nIn a fantastically bizarre place...\pIt's PALKIA!\pWill you challenge PALKIA?$"
