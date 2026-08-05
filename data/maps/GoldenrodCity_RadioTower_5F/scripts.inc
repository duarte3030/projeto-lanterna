@ TORRE RADIO de GOLDENROD, 5F. Portado de
@ fontes-mapas/hns/data/maps/GoldenrodCity_RadioTower_5F/scripts.inc.
@ ponytail: aqui fecha o arco. O hns troca dois objetos para revelar o PETREL
@ disfarcado de DIRETOR e um terceiro para o DIRETOR de verdade aparecer, tudo
@ com flag e VAR_GOLDENROD_CITY_STATE. Aqui e UM objeto so: o falso diretor gira
@ e vira o PETREL sem trocar de sprite, e o DIRETOR de verdade nao aparece
@ (a recompensa dele e a asa do LUGIA/HO-OH, que depende de VAR_LUGIA_OR_HOOH).
@ Derrotar o ARCHER liga FLAG_HIDE_GOLDENROD_ROCKETS e limpa a torre inteira.
@ Quem lembra que PETREL e ARCHER ja cairam e goto_if_defeated, nao var.

GoldenrodCity_RadioTower_5F_MapScripts::
	.byte 0

RadioTower5F_EventScript_Petrel::
	lock
	faceplayer
	goto_if_defeated TRAINER_JOHTO_ROCKET_PETREL, RadioTower5F_EventScript_PetrelDone
	msgbox RadioTower5F_Text_FakeDirector1, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_RADIO_TOWER_5F_PETREL, RadioTower5F_Movement_Spin
	waitmovement 0
	msgbox RadioTower5F_Text_FakeDirector2, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_ROCKET_PETREL, RadioTower5F_Text_FakeDirectorWin
	msgbox RadioTower5F_Text_FakeDirectorAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower5F_EventScript_PetrelDone::
	msgbox RadioTower5F_Text_FakeDirectorAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower5F_EventScript_Ariana::
	trainerbattle_single TRAINER_JOHTO_ROCKET_ARIANA, RadioTower5F_Text_ArianaSeen, RadioTower5F_Text_ArianaBeaten
	msgbox RadioTower5F_Text_ArianaAfter, MSGBOX_AUTOCLOSE
	end

RadioTower5F_EventScript_Archer::
	lock
	faceplayer
	goto_if_defeated TRAINER_JOHTO_ROCKET_ARCHER, RadioTower5F_EventScript_ArcherDone
	msgbox RadioTower5F_Text_RocketBossSeen, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_ROCKET_ARCHER, RadioTower5F_Text_RocketBossBeaten
	msgbox RadioTower5F_Text_RocketBossAfter, MSGBOX_DEFAULT
	delay 55
	closemessage
	fadescreen FADE_TO_BLACK
	setflag FLAG_HIDE_GOLDENROD_ROCKETS
	playse SE_EXIT
	removeobject LOCALID_RADIO_TOWER_5F_ARCHER
	removeobject LOCALID_RADIO_TOWER_5F_ARIANA
	removeobject LOCALID_RADIO_TOWER_5F_PETREL
	delay 120
	fadescreen FADE_FROM_BLACK
	special DrawWholeMapView
	release
	end

RadioTower5F_EventScript_ArcherDone::
	msgbox RadioTower5F_Text_RocketBossAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower5F_EventScript_Ben::
	lock
	faceplayer
	msgbox RadioTower5F_Text_Ben, MSGBOX_DEFAULT
	closemessage
	release
	end

RadioTower5F_Movement_Spin:
	face_right
	delay_8
	face_up
	delay_8
	face_left
	delay_8
	face_down
	delay_8
	face_right
	delay_4
	face_up
	delay_4
	face_left
	delay_4
	face_down
	delay_4
	face_right
	delay_2
	face_up
	delay_2
	face_left
	delay_2
	face_down
	step_end

RadioTower5F_Text_FakeDirector1:
	.string "Y-you! You came to rescue me?$"

RadioTower5F_Text_FakeDirector2:
	.string "Is that what you were expecting?\p"
	.string "Wrong! I'm an imposter!\p"
	.string "I pretended to be the real thing to\n"
	.string "prepare for our takeover.\p"
	.string "Do you want to know where we hid\n"
	.string "the real DIRECTOR?\p"
	.string "Sure, I'll tell you. But only if you\n"
	.string "can beat me!$"

RadioTower5F_Text_FakeDirectorWin:
	.string "OK, OK. I'll tell you where he is.$"

RadioTower5F_Text_FakeDirectorAfter:
	.string "The boss stashed the DIRECTOR in\n"
	.string "the UNDERGROUND WAREHOUSE.\p"
	.string "It's at the far end of the UNDER-\n"
	.string "GROUND.\p"
	.string "But I doubt you'll get that far.$"

RadioTower5F_Text_ArianaSeen:
	.string "Remember me from the HIDEOUT in\n"
	.string "MAHOGANY TOWN?\p"
	.string "My boss scolded me but I'm stronger.\p"
	.string "I lost then, but I won't this time.$"

RadioTower5F_Text_ArianaBeaten:
	.string "This can't be happening!\p"
	.string "I fought hard, but I still lost…\p"
	.string "I'm so sorry GIOVANNI…$"

RadioTower5F_Text_ArianaAfter:
	.string "{PLAYER}, isn't it?\p"
	.string "A brat like you won't appreciate\n"
	.string "the magnificence of TEAM ROCKET.\p"
	.string "That's too bad. I really admire\n"
	.string "your power.$"

RadioTower5F_Text_RocketBossSeen:
	.string "Oh? You managed to get this far?\p"
	.string "You must be quite the trainer.\p"
	.string "We intend to take over this RADIO\n"
	.string "STATION and announce our comeback.\p"
	.string "That should bring our boss GIOVANNI\n"
	.string "back from his solitary training.\p"
	.string "We are going to regain our former\n"
	.string "glory…\p"
	.string "I won't allow you to interfere with\n"
	.string "our meticulous plans!$"

RadioTower5F_Text_RocketBossBeaten:
	.string "No! Forgive me, GIOVANNI!$"

RadioTower5F_Text_RocketBossAfter:
	.string "How could this be?\p"
	.string "Our dreams have come to naught.\p"
	.string "I wasn't up to the task after all.\p"
	.string "Like GIOVANNI did before me, I will\n"
	.string "disband TEAM ROCKET here today.\p"
	.string "Farewell.$"

RadioTower5F_Text_Ben:
	.string "BEN: Do you listen to our music?$"
