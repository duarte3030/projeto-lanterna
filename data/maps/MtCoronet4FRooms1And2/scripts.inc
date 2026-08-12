MtCoronet4FRooms1And2_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtCoronet4FRooms1And2_OnTransition
	.byte 0

MtCoronet4FRooms1And2_EventScript_GalacticGruntMtCoronet4f2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_4F_2, MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f2Intro, MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f2Defeat
	msgbox MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f2Post, MSGBOX_AUTOCLOSE
	end

MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f2Intro:
	.string "Team Galactic is all powerful!\pOnly a fool would show defiance to\nthe mighty might of Team Galactic!$"

MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f2Defeat:
	.string "Not standing up to the mighty is\nfoolish, you say...$"

MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f2Post:
	.string "It doesn't matter if you're an adult\nor a kid if you have Pokémon...\pPokémon are the equalizers.\nI should have realized sooner...$"

MtCoronet4FRooms1And2_EventScript_GalacticGruntMtCoronet4f1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_4F_1, MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f1Intro, MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f1Defeat
	msgbox MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f1Post, MSGBOX_AUTOCLOSE
	end

MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f1Intro:
	.string "Our time is coming!\nA time for us alone!\pWe'll send you back in time.\nA time before you started training!$"

MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f1Defeat:
	.string "Gyah!$"

MtCoronet4FRooms1And2_Text_GalacticGruntMtCoronet4f1Post:
	.string "You can struggle all you want, but\nyou can't stop Team Galactic alone!\pIt doesn't matter how many Pokémon\nyou try to use as your tools!$"

@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos nascem enquanto
@ derrotar o Cyrus no Spear Pillar nao aconteceu, e somem depois; o motor ja grava a flag de
@ derrotado do gatilho, e este ON_TRANSITION so a traduz. Zero var.
MtCoronet4FRooms1And2_OnTransition:
	call_if_defeated TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, MtCoronet4FRooms1And2_EventScript_HideGalactica_mt_coronet
	end

MtCoronet4FRooms1And2_EventScript_HideGalactica_mt_coronet::
	setflag FLAG_GALACTICA_MT_CORONET
	return
