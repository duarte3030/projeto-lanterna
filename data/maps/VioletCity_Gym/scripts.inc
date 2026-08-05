@ Ginasio de VIOLET CITY, portado de fontes-mapas/hns por
@ dev_scripts/porta_ginasios_johto.py. Nao editar a mao: rode o script.
@ ponytail: o enredo de var do hns foi cortado. Aqui o ginasio e fala,
@ batalha, fala e FLAG_INSIGNIA_JOHTO_1. Zero var gasta.

VioletCity_Gym_MapScripts::
	.byte 0

VioletCity_Gym_EventScript_Abe::
	trainerbattle_single TRAINER_JOHTO_BIRD_KEEPER_ABE, VioletCity_Gym_Text_AbeSeen, VioletCity_Gym_Text_AbeBeaten
	msgbox VioletCity_Gym_Text_AbeAfter, MSGBOX_AUTOCLOSE
	end

VioletCity_Gym_EventScript_Rod::
	trainerbattle_single TRAINER_JOHTO_BIRD_KEEPER_ROD, VioletCity_Gym_Text_RodSeen, VioletCity_Gym_Text_RodBeaten
	msgbox VioletCity_Gym_Text_RodAfter, MSGBOX_AUTOCLOSE
	end

VioletCity_Gym_EventScript_Falkner::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_1, VioletCity_Gym_EventScript_FalknerDerrotado
	msgbox VioletCity_Gym_Text_FalknerIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_LEADER_FALKNER, VioletCity_Gym_Text_FalknerDefeat
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox VioletCity_Gym_Text_FalknerBadge, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_JOHTO_1
	closemessage
	release
	end

VioletCity_Gym_EventScript_FalknerDerrotado::
	msgbox VioletCity_Gym_Text_FalknerPost, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_Gym_EventScript_GymGuy::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_1, VioletCity_Gym_EventScript_GuideAfter
	msgbox VioletCity_Gym_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

VioletCity_Gym_EventScript_GuideAfter::
	msgbox VioletCity_Gym_Text_GuideAfter, MSGBOX_DEFAULT
	release
	end

VioletCity_Gym_EventScript_Statue::
	goto_if_set FLAG_INSIGNIA_JOHTO_1, VioletCity_Gym_EventScript_StatueCertified
	msgbox VioletCity_Gym_Text_Statue, MSGBOX_SIGN
	end

VioletCity_Gym_EventScript_StatueCertified::
	msgbox VioletCity_Gym_Text_StatueCertified, MSGBOX_SIGN
	end

VioletCity_Gym_Text_AbeSeen:
	.string "Let me see if you are good\n"
	.string "enough to face FALKNER!$"

VioletCity_Gym_Text_AbeBeaten:
	.string "This can't be true!$"

VioletCity_Gym_Text_AbeAfter:
	.string "This is pathetic, losing to some\n"
	.string "rookie trainer…$"

VioletCity_Gym_Text_RodSeen:
	.string "The keyword is guts!\p"
	.string "Those here are training night and\n"
	.string "day to become bird POKéMON masters.\p"
	.string "Come on!$"

VioletCity_Gym_Text_RodBeaten:
	.string "Gaaah!$"

VioletCity_Gym_Text_RodAfter:
	.string "FALKNER's skills are for real!\p"
	.string "Don't get cocky just because\n"
	.string "you beat me!$"

VioletCity_Gym_Text_FalknerIntro:
	.string "I'm FALKNER, the VIOLET POKéMON\n"
	.string "GYM leader!\p"
	.string "People say you can clip\n"
	.string "FLYING-type POKéMON's wings\p"
	.string "with a jolt of electricity…\n"
	.string "I won't allow such insults to bird\l"
	.string "POKéMON!\p"
	.string "I'll show you the real power\n"
	.string "of the magnificent bird POKéMON!$"

VioletCity_Gym_Text_FalknerDefeat:
	.string "…Darn! My dad's cherished bird\n"
	.string "POKéMON…\p"
	.string "All right. Take this.\p"
	.string "It's the official POKéMON LEAGUE\n"
	.string "ZEPHYRBADGE.$"

VioletCity_Gym_Text_FalknerBadge:
	.string "ZEPHYRBADGE raises the ATTACK\n"
	.string "power of POKéMON.\p"
	.string "It also enables POKéMON to use\n"
	.string "FLASH, if they can learn it,\l"
	.string "anytime.\p"
	.string "Here--take this too.$"

VioletCity_Gym_Text_FalknerPost:
	.string "There are POKéMON GYMS in cities\n"
	.string "and towns ahead.\p"
	.string "You should test your skills at\n"
	.string "these GYMS.\p"
	.string "I'm going to train harder to\n"
	.string "become the greatest bird master!$"

VioletCity_Gym_Text_GuideBefore:
	.string "Hey! What's up? I'm no trainer,\n"
	.string "but I can give some advice!\p"
	.string "Believe me! If you believe, a\n"
	.string "championship dream can come true.\p"
	.string "You believe? Then listen.\p"
	.string "FALKNER's ace is a bulky owl\n"
	.string "that loves to eat BERRIES.\p"
	.string "While it's not the strongest,\n"
	.string "it can take a lot of hits.\p"
	.string "You can hurt it with ELECTRIC \n"
	.string "and ROCK-type moves, but watch out\l"
	.string "for MUD-SLAP!\p"
	.string "If you want more help, go visit the\n"
	.string "POKéMON ACADEMY.\p"
	.string "The students there really know\n"
	.string "their stuff!$"

VioletCity_Gym_Text_GuideAfter:
	.string "Nice battle! Keep it up,\n"
	.string "and you'll be the CHAMP in no\l"
	.string "time at all!$"

VioletCity_Gym_Text_Statue:
	.string "VIOLET CITY POKéMON GYM\n"
	.string "Leader: FALKNER$"

VioletCity_Gym_Text_StatueCertified:
	.string "VIOLET CITY POKéMON GYM\p"
	.string "FALKNER'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"
