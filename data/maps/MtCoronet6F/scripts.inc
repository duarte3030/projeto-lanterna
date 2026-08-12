MtCoronet6F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtCoronet6F_OnTransition
	.byte 0

MtCoronet6F_EventScript_GalacticGruntMtCoronet6f::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_6F, MtCoronet6F_Text_GalacticGruntMtCoronet6fIntro, MtCoronet6F_Text_GalacticGruntMtCoronet6fDefeat
	msgbox MtCoronet6F_Text_GalacticGruntMtCoronet6fPost, MSGBOX_AUTOCLOSE
	end

MtCoronet6F_Text_GalacticGruntMtCoronet6fIntro:
	.string "You've worked so hard to get here.\nYou should be proud of yourself!\pAnd now, I'll send you packing home\nwith only that happy thought!$"

MtCoronet6F_Text_GalacticGruntMtCoronet6fDefeat:
	.string "Wh-- How dare you! That's how you\nrespond to my generosity?$"

MtCoronet6F_Text_GalacticGruntMtCoronet6fPost:
	.string "We couldn't stop you...\nWe'll be discarded as useless...\pOur boss is ruthless that way...$"

@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos nascem enquanto
@ derrotar o Cyrus no Spear Pillar nao aconteceu, e somem depois; o motor ja grava a flag de
@ derrotado do gatilho, e este ON_TRANSITION so a traduz. Zero var.
MtCoronet6F_OnTransition:
	call_if_defeated TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, MtCoronet6F_EventScript_HideGalactica_mt_coronet
	end

MtCoronet6F_EventScript_HideGalactica_mt_coronet::
	setflag FLAG_GALACTICA_MT_CORONET
	return
