@ Ginasio de BLACKTHORN CITY, portado de fontes-mapas/hns por
@ dev_scripts/porta_ginasios_johto.py. Nao editar a mao: rode o script.
@ ponytail: o enredo de var do hns foi cortado. Aqui o ginasio e fala,
@ batalha, fala e FLAG_INSIGNIA_JOHTO_8. Zero var gasta.

BlackthornCity_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, BlackthornCity_Gym_EventScript_Pontes
	.byte 0

BlackthornCity_Gym_EventScript_Pontes::
	call_if_ge VAR_BLACKTHORN_GYM_STATE, 1, BlackthornCity_Gym_EventScript_Ponte1
	call_if_ge VAR_BLACKTHORN_GYM_STATE, 2, BlackthornCity_Gym_EventScript_Ponte2
	call_if_ge VAR_BLACKTHORN_GYM_STATE, 3, BlackthornCity_Gym_EventScript_Ponte3
	call_if_ge VAR_BLACKTHORN_GYM_STATE, 4, BlackthornCity_Gym_EventScript_Ponte4
	end

BlackthornCity_Gym_EventScript_Ponte1::
	setmetatile 19, 47, 889, FALSE
	setmetatile 19, 48, 889, FALSE
	setmetatile 19, 49, 889, FALSE
	setmetatile 19, 50, 889, FALSE
	setmetatile 19, 51, 889, FALSE
	setmetatile 19, 52, 889, FALSE
	setmetatile 19, 53, 889, FALSE
	setmetatile 19, 54, 889, FALSE
	setmetatile 20, 47, 889, FALSE
	setmetatile 20, 48, 889, FALSE
	setmetatile 20, 49, 889, FALSE
	setmetatile 20, 50, 889, FALSE
	setmetatile 20, 51, 889, FALSE
	setmetatile 20, 52, 889, FALSE
	setmetatile 20, 53, 889, FALSE
	setmetatile 20, 54, 889, FALSE
	setmetatile 21, 47, 889, FALSE
	setmetatile 21, 48, 889, FALSE
	setmetatile 21, 49, 889, FALSE
	setmetatile 21, 50, 889, FALSE
	setmetatile 21, 51, 889, FALSE
	setmetatile 21, 52, 889, FALSE
	setmetatile 21, 53, 889, FALSE
	setmetatile 21, 54, 889, FALSE
	return

BlackthornCity_Gym_EventScript_Ponte2::
	setmetatile 17, 35, 889, FALSE
	setmetatile 17, 36, 889, FALSE
	setmetatile 17, 37, 889, FALSE
	setmetatile 17, 38, 889, FALSE
	setmetatile 17, 39, 889, FALSE
	setmetatile 17, 40, 889, FALSE
	setmetatile 18, 35, 889, FALSE
	setmetatile 18, 36, 889, FALSE
	setmetatile 18, 37, 889, FALSE
	setmetatile 18, 38, 889, FALSE
	setmetatile 18, 39, 889, FALSE
	setmetatile 18, 40, 889, FALSE
	setmetatile 19, 35, 889, FALSE
	setmetatile 19, 36, 889, FALSE
	setmetatile 19, 37, 889, FALSE
	setmetatile 19, 38, 889, FALSE
	setmetatile 19, 39, 889, FALSE
	setmetatile 19, 40, 889, FALSE
	setmetatile 20, 32, 889, FALSE
	setmetatile 21, 32, 889, FALSE
	setmetatile 22, 32, 889, FALSE
	setmetatile 20, 35, 889, TRUE
	setmetatile 21, 35, 889, TRUE
	setmetatile 22, 35, 889, TRUE
	setmetatile 20, 33, 889, FALSE
	setmetatile 20, 34, 889, FALSE
	setmetatile 21, 33, 889, FALSE
	setmetatile 21, 34, 889, FALSE
	setmetatile 22, 33, 889, FALSE
	setmetatile 22, 34, 889, FALSE
	return

BlackthornCity_Gym_EventScript_Ponte3::
	setmetatile 17, 26, 889, FALSE
	setmetatile 18, 26, 889, FALSE
	setmetatile 19, 26, 889, FALSE
	setmetatile 20, 26, 889, FALSE
	setmetatile 21, 26, 889, FALSE
	setmetatile 22, 26, 889, FALSE
	setmetatile 23, 26, 889, FALSE
	return

BlackthornCity_Gym_EventScript_Ponte4::
	setmetatile 19, 11, 889, FALSE
	setmetatile 19, 12, 889, FALSE
	setmetatile 19, 13, 889, FALSE
	setmetatile 19, 14, 889, FALSE
	setmetatile 19, 15, 889, FALSE
	setmetatile 20, 11, 889, FALSE
	setmetatile 20, 12, 889, FALSE
	setmetatile 20, 13, 889, FALSE
	setmetatile 20, 14, 889, FALSE
	setmetatile 20, 15, 889, FALSE
	setmetatile 21, 11, 889, FALSE
	setmetatile 21, 12, 889, FALSE
	setmetatile 21, 13, 889, FALSE
	setmetatile 21, 14, 889, FALSE
	setmetatile 21, 15, 889, FALSE
	return

BlackthornCity_Gym_EventScript_AcendePonte1::
	call BlackthornCity_Gym_EventScript_Ponte1
	special DrawWholeMapView
	setvar VAR_BLACKTHORN_GYM_STATE, 1
	end

BlackthornCity_Gym_EventScript_AcendePonte2::
	call BlackthornCity_Gym_EventScript_Ponte2
	special DrawWholeMapView
	setvar VAR_BLACKTHORN_GYM_STATE, 2
	end

BlackthornCity_Gym_EventScript_AcendePonte3::
	call BlackthornCity_Gym_EventScript_Ponte3
	special DrawWholeMapView
	setvar VAR_BLACKTHORN_GYM_STATE, 3
	end

BlackthornCity_Gym_EventScript_AcendePonte4::
	call BlackthornCity_Gym_EventScript_Ponte4
	special DrawWholeMapView
	setvar VAR_BLACKTHORN_GYM_STATE, 4
	end

BlackthornCity_Gym_EventScript_Mike::
	trainerbattle_single TRAINER_JOHTO_COOLTRAINER_MIKE, BlackthornCity_Gym_Text_MikeSeen, BlackthornCity_Gym_Text_MikeBeaten
	msgbox BlackthornCity_Gym_Text_MikeAfter, MSGBOX_AUTOCLOSE
	end

BlackthornCity_Gym_EventScript_Paul::
	trainerbattle_single TRAINER_JOHTO_COOLTRAINER_PAUL, BlackthornCity_Gym_Text_PaulSeen, BlackthornCity_Gym_Text_PaulBeaten
	msgbox BlackthornCity_Gym_Text_PaulAfter, MSGBOX_AUTOCLOSE
	end

BlackthornCity_Gym_EventScript_Lola::
	trainerbattle_single TRAINER_JOHTO_COOLTRAINER_LOLA, BlackthornCity_Gym_Text_LolaSeen, BlackthornCity_Gym_Text_LolaBeaten
	msgbox BlackthornCity_Gym_Text_LolaAfter, MSGBOX_AUTOCLOSE
	end

BlackthornCity_Gym_EventScript_Fran::
	trainerbattle_single TRAINER_JOHTO_COOLTRAINER_FRAN, BlackthornCity_Gym_Text_FranSeen, BlackthornCity_Gym_Text_FranBeaten
	msgbox BlackthornCity_Gym_Text_FranAfter, MSGBOX_AUTOCLOSE
	end

BlackthornCity_Gym_EventScript_Cody::
	trainerbattle_single TRAINER_JOHTO_COOLTRAINER_CODY, BlackthornCity_Gym_Text_CodySeen, BlackthornCity_Gym_Text_CodyBeaten
	msgbox BlackthornCity_Gym_Text_CodyAfter, MSGBOX_AUTOCLOSE
	end

BlackthornCity_Gym_EventScript_Clair::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_8, BlackthornCity_Gym_EventScript_ClairDerrotado
	msgbox BlackthornCity_Gym_Text_ClairIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_LEADER_CLAIR, BlackthornCity_Gym_Text_ClairDefeat
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox BlackthornCity_Gym_Text_ClairBadge, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_JOHTO_8
	@ Travessia entre regioes: abre o porto de Slateport no menu dos cinco
	@ cais. Esta ROM nao tem Elite dos Quatro de Johto (a Liga de gen 2 e o
	@ mesmo Planalto Indigo de Kanto), entao o fim de Johto que existe de
	@ verdade e a oitava insignia. Ver data/scripts/travessia_regioes.inc.
	setflag FLAG_REGIAO_HOENN_LIBERADA
	closemessage
	release
	end

BlackthornCity_Gym_EventScript_ClairDerrotado::
	msgbox BlackthornCity_Gym_Text_ClairPost, MSGBOX_DEFAULT
	closemessage
	release
	end

BlackthornCity_Gym_EventScript_GymGuy::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_8, BlackthornCity_Gym_EventScript_GuideAfter
	msgbox BlackthornCity_Gym_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

BlackthornCity_Gym_EventScript_GuideAfter::
	msgbox BlackthornCity_Gym_Text_GuideAfter, MSGBOX_DEFAULT
	release
	end

BlackthornCity_Gym_EventScript_Statue::
	goto_if_set FLAG_INSIGNIA_JOHTO_8, BlackthornCity_Gym_EventScript_StatueCertified
	msgbox BlackthornCity_Gym_Text_Statue, MSGBOX_SIGN
	end

BlackthornCity_Gym_EventScript_StatueCertified::
	msgbox BlackthornCity_Gym_Text_StatueCertified, MSGBOX_SIGN
	end

BlackthornCity_Gym_Text_MikeSeen:
	.string "My chance of losing? Not even one\n"
	.string "percent!$"

BlackthornCity_Gym_Text_MikeBeaten:
	.string "That's odd.$"

BlackthornCity_Gym_Text_MikeAfter:
	.string "I know my short-comings now.\p"
	.string "Thanks for showing me!$"

BlackthornCity_Gym_Text_PaulSeen:
	.string "Your first battle against dragons?\p"
	.string "I'll show you how tough they are!$"

BlackthornCity_Gym_Text_PaulBeaten:
	.string "My dragon POKéMON lost?$"

BlackthornCity_Gym_Text_PaulAfter:
	.string "LANCE told you that he'd like to\n"
	.string "see you again?\p"
	.string "Not a chance!$"

BlackthornCity_Gym_Text_LolaSeen:
	.string "Dragons are sacred POKéMON.\p"
	.string "They are full of life energy.\p"
	.string "If you're not serious, you won't\n"
	.string "be able to beat them.$"

BlackthornCity_Gym_Text_LolaBeaten:
	.string "Way to go!$"

BlackthornCity_Gym_Text_LolaAfter:
	.string "Dragons are weak against DRAGON-\n"
	.string "type moves.$"

BlackthornCity_Gym_Text_FranSeen:
	.string "I can't allow a nameless trainer\n"
	.string "past me!\p"
	.string "CLAIR would be livid if I did!$"

BlackthornCity_Gym_Text_FranBeaten:
	.string "Awww… I lost…$"

BlackthornCity_Gym_Text_FranAfter:
	.string "Uh-oh… CLAIR is going to be mad…$"

BlackthornCity_Gym_Text_CodySeen:
	.string "I just got access to use DRAGON-\n"
	.string "type POKéMON!$"

BlackthornCity_Gym_Text_CodyBeaten:
	.string "Rats! If only I had a DRAGONITE!$"

BlackthornCity_Gym_Text_CodyAfter:
	.string "Members of our dragon-user clan\n"
	.string "can use dragon POKéMON only after\l"
	.string "our MASTER allows it.$"

BlackthornCity_Gym_Text_ClairIntro:
	.string "I am CLAIR.\p"
	.string "The world's best dragon master.\p"
	.string "I can hold my own against even the\n"
	.string "POKéMON LEAGUE's ELITE FOUR.\p"
	.string "Do you still want to take me on?\p"
	.string "…Fine. Let's do it!\p"
	.string "As a GYM LEADER, I will use my full\n"
	.string "power against any opponent!$"

BlackthornCity_Gym_Text_ClairDefeat:
	.string "I lost?\p"
	.string "I don't believe it. There must be\n"
	.string "some mistake…$"

BlackthornCity_Gym_Text_ClairBadge:
	.string "I won't admit this.\p"
	.string "I may have lost, but you're still\n"
	.string "not ready for the POKéMON LEAGUE.\p"
	.string "I know. You should take the dragon-\n"
	.string "user challenge.\p"
	.string "Behind this GYM is a place called\n"
	.string "DRAGON'S DEN.\p"
	.string "There is a small shrine at its\n"
	.string "center. Go there.\p"
	.string "If you can prove that you've lost\n"
	.string "your lazy ideals, I will recognize\l"
	.string "you as a trainer worthy of a GYM\l"
	.string "BADGE!$"

BlackthornCity_Gym_Text_ClairPost:
	.string "What's the matter?\p"
	.string "Aren't you headed to the POKéMON\n"
	.string "LEAGUE?\p"
	.string "Don't you know where it is?\p"
	.string "From here, go to NEW BARK TOWN.\p"
	.string "Then SURF east. The route there is\n"
	.string "very tough.\p"
	.string "Don't you dare lose at the POKéMON\n"
	.string "LEAGUE!\p"
	.string "If you do, I'll feel even worse\n"
	.string "about having lost to you!\p"
	.string "Give it everything you've got.$"

BlackthornCity_Gym_Text_GuideBefore:
	.string "Yo! CHAMP in making!\p"
	.string "It's been a long journey, but we\n"
	.string "are almost done! Count on me!\p"
	.string "While CLAIR looks up to the Dragon\n"
	.string "Master, LANCE, she's managed to\l"
	.string "create her own identity with a\l"
	.string "team consisting of dragons from\l"
	.string "the sea.\p"
	.string "Dragons are supposed to be\n"
	.string "weak against ICE-type moves,\l"
	.string "but you'll need some DRAGON-type\l"
	.string "or FAIRY-type moves of your own if\l"
	.string "you want to win.$"
	.string "You got this!$"

BlackthornCity_Gym_Text_GuideAfter:
	.string "You were great to beat CLAIR!\p"
	.string "All that's left is the POKéMON\n"
	.string "LEAGUE challenge.\p"
	.string "You're on the way to becoming the\n"
	.string "POKéMON CHAMPION!$"

BlackthornCity_Gym_Text_Statue:
	.string "BLACKTHORN CITY POKéMON GYM\n"
	.string "Leader: CLAIR$"

BlackthornCity_Gym_Text_StatueCertified:
	.string "BLACKTHORN CITY POKéMON GYM\p"
	.string "CLAIR'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"
