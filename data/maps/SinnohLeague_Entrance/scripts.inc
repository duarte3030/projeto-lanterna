@ Saguao da Liga Pokemon de Sinnoh. Os dois guardas FICAM em pe na porta do
@ fundo (9,2) e (10,2), que sao os unicos tiles que dao acesso a (9,1) e (10,1).
@ ponytail: falar com o guarda e o que leva o jogador para dentro. Nao existe
@ porta que abre e fica aberta porque isso pediria uma flag nova, e flag nova
@ so o Gui reserva. Ver Pokemon Claude/SINNOH-PADRAO.md.

SinnohLeague_Entrance_MapScripts::
	.byte 0

SinnohLeague_Entrance_EventScript_Nurse::
	setvar VAR_0x800B, LOCALID_SINNOH_LEAGUE_NURSE
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

SinnohLeague_Entrance_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart SinnohLeague_Entrance_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
SinnohLeague_Entrance_Pokemart:
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_MAX_REPEL
	pokemartlistend

SinnohLeague_Entrance_EventScript_DoorGuard::
	lockall
	applymovement VAR_LAST_TALKED, Common_Movement_FacePlayer
	waitmovement 0
	message SinnohLeague_Entrance_Text_MustHaveAllGymBadges
	waitmessage
	delay 60
	goto_if_unset FLAG_INSIGNIA_SINNOH_1, SinnohLeague_Entrance_EventScript_NotAllBadges
	goto_if_unset FLAG_INSIGNIA_SINNOH_2, SinnohLeague_Entrance_EventScript_NotAllBadges
	goto_if_unset FLAG_INSIGNIA_SINNOH_3, SinnohLeague_Entrance_EventScript_NotAllBadges
	goto_if_unset FLAG_INSIGNIA_SINNOH_4, SinnohLeague_Entrance_EventScript_NotAllBadges
	goto_if_unset FLAG_INSIGNIA_SINNOH_5, SinnohLeague_Entrance_EventScript_NotAllBadges
	goto_if_unset FLAG_INSIGNIA_SINNOH_6, SinnohLeague_Entrance_EventScript_NotAllBadges
	goto_if_unset FLAG_INSIGNIA_SINNOH_7, SinnohLeague_Entrance_EventScript_NotAllBadges
	goto_if_unset FLAG_INSIGNIA_SINNOH_8, SinnohLeague_Entrance_EventScript_NotAllBadges
	closemessage
	playfanfare MUS_OBTAIN_BADGE
	message SinnohLeague_Entrance_Text_GoForth
	waitmessage
	waitfanfare
	closemessage
	delay 20
	warp MAP_SINNOH_LEAGUE_AARONS_ROOM, 0
	waitstate
	releaseall
	end

SinnohLeague_Entrance_EventScript_NotAllBadges::
	playse SE_FAILURE
	msgbox SinnohLeague_Entrance_Text_HaventObtainedAllBadges, MSGBOX_DEFAULT
	releaseall
	end

SinnohLeague_Entrance_Text_MustHaveAllGymBadges:
	.string "Beyond this point, only TRAINERS who\n"
	.string "have collected all eight SINNOH GYM\l"
	.string "BADGES are permitted to enter.\p"
	.string "TRAINER, let us confirm your BADGES.$"

SinnohLeague_Entrance_Text_HaventObtainedAllBadges:
	.string "You haven't obtained all the BADGES.\p"
	.string "If you're bound for the SINNOH\n"
	.string "POKéMON LEAGUE, come back with them.$"

SinnohLeague_Entrance_Text_GoForth:
	.string "All eight, confirmed!\p"
	.string "The ELITE FOUR are waiting above.\n"
	.string "TRAINER, go forth!$"
