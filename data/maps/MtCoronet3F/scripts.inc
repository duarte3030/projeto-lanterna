MtCoronet3F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtCoronet3F_OnTransition
	.byte 0

MtCoronet3F_EventScript_GalacticGruntMtCoronet3f2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_3F_2, MtCoronet3F_Text_GalacticGruntMtCoronet3f2Intro, MtCoronet3F_Text_GalacticGruntMtCoronet3f2Defeat
	msgbox MtCoronet3F_Text_GalacticGruntMtCoronet3f2Post, MSGBOX_AUTOCLOSE
	end

MtCoronet3F_Text_GalacticGruntMtCoronet3f2Intro:
	.string "We Grunts have two jobs.\pOne, ensure the success of our\noperation at the summit.\pTwo, utterly destroy any intruders\nto stop their meddling!$"

MtCoronet3F_Text_GalacticGruntMtCoronet3f2Defeat:
	.string "I don't accept this!\nI will not accept this!$"

MtCoronet3F_Text_GalacticGruntMtCoronet3f2Post:
	.string "Join Team Galactic and then abide\nby our rules.\pThat would solve all our problems!$"

MtCoronet3F_EventScript_GalacticGruntMtCoronet3f1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_3F_1, MtCoronet3F_Text_GalacticGruntMtCoronet3f1Intro, MtCoronet3F_Text_GalacticGruntMtCoronet3f1Defeat
	msgbox MtCoronet3F_Text_GalacticGruntMtCoronet3f1Post, MSGBOX_AUTOCLOSE
	end

MtCoronet3F_Text_GalacticGruntMtCoronet3f1Intro:
	.string "Our time has come!\nIt's Team Galactic's time now!$"

MtCoronet3F_Text_GalacticGruntMtCoronet3f1Defeat:
	.string "When's it gonna be my turn...$"

MtCoronet3F_Text_GalacticGruntMtCoronet3f1Post:
	.string "It's too late!\pNo amount of desperation from a kid\nlike you will make a difference!$"

@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos nascem enquanto
@ derrotar o Cyrus no Spear Pillar nao aconteceu, e somem depois; o motor ja grava a flag de
@ derrotado do gatilho, e este ON_TRANSITION so a traduz. Zero var.
MtCoronet3F_OnTransition:
	call_if_defeated TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, MtCoronet3F_EventScript_HideGalactica_mt_coronet
	end

MtCoronet3F_EventScript_HideGalactica_mt_coronet::
	setflag FLAG_GALACTICA_MT_CORONET
	return
