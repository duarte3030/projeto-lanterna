MtCoronet5F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtCoronet5F_OnTransition
	.byte 0

MtCoronet5F_EventScript_GalacticGruntMtCoronet5f2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_5F_2, MtCoronet5F_Text_GalacticGruntMtCoronet5f2Intro, MtCoronet5F_Text_GalacticGruntMtCoronet5f2Defeat
	msgbox MtCoronet5F_Text_GalacticGruntMtCoronet5f2Post, MSGBOX_AUTOCLOSE
	end

MtCoronet5F_Text_GalacticGruntMtCoronet5f2Intro:
	.string "...Our boss is going to do something\nhuge at the summit.\pBut here I am dealing with some pesky\nintruder.\pYou're spoiling the atmosphere.\nYou can lose quickly, right?$"

MtCoronet5F_Text_GalacticGruntMtCoronet5f2Defeat:
	.string "You're not supposed to work me\nover like that.$"

MtCoronet5F_Text_GalacticGruntMtCoronet5f2Post:
	.string "All my excitement's gone now...\pThis whole Mt. Coronet trip is too\nrough, long, and draining...$"

MtCoronet5F_EventScript_GalacticGruntMtCoronet5f1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_5F_1, MtCoronet5F_Text_GalacticGruntMtCoronet5f1Intro, MtCoronet5F_Text_GalacticGruntMtCoronet5f1Defeat
	msgbox MtCoronet5F_Text_GalacticGruntMtCoronet5f1Post, MSGBOX_AUTOCLOSE
	end

MtCoronet5F_Text_GalacticGruntMtCoronet5f1Intro:
	.string "Team Galactic will take control of\neverything!\pYou can try all you want, but you\ncan't do anything alone!$"

MtCoronet5F_Text_GalacticGruntMtCoronet5f1Defeat:
	.string "All you gave me was the taste of\ndefeat...$"

MtCoronet5F_Text_GalacticGruntMtCoronet5f1Post:
	.string "...Is our boss about to ditch us\nand claim everything for himself?$"

@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos nascem enquanto
@ derrotar o Cyrus no Spear Pillar nao aconteceu, e somem depois; o motor ja grava a flag de
@ derrotado do gatilho, e este ON_TRANSITION so a traduz. Zero var.
MtCoronet5F_OnTransition:
	call_if_defeated TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, MtCoronet5F_EventScript_HideGalactica_mt_coronet
	end

MtCoronet5F_EventScript_HideGalactica_mt_coronet::
	setflag FLAG_GALACTICA_MT_CORONET
	return
