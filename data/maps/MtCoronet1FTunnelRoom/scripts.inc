MtCoronet1FTunnelRoom_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtCoronet1FTunnelRoom_OnTransition
	.byte 0

MtCoronet1FTunnelRoom_EventScript_GalacticGrunt::
	msgbox MtCoronet1FTunnelRoom_Text_GalacticGrunt, MSGBOX_NPC
	end

MtCoronet1FTunnelRoom_Text_GalacticGrunt:
	.string "Yeah, right! You're absolutely right!\nI'm hopelessly lost!\pPlease don't pay attention to a lowly\ngrunt like me without any Pokémon!$"

@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos nascem enquanto
@ derrotar o Cyrus no Spear Pillar nao aconteceu, e somem depois; o motor ja grava a flag de
@ derrotado do gatilho, e este ON_TRANSITION so a traduz. Zero var.
MtCoronet1FTunnelRoom_OnTransition:
	call_if_defeated TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, MtCoronet1FTunnelRoom_EventScript_HideGalactica_mt_coronet
	end

MtCoronet1FTunnelRoom_EventScript_HideGalactica_mt_coronet::
	setflag FLAG_GALACTICA_MT_CORONET
	return
