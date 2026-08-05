@ Ginasio de ECRUTEAK CITY, portado de fontes-mapas/hns por
@ dev_scripts/porta_ginasios_johto.py. Nao editar a mao: rode o script.
@ ponytail: o enredo de var do hns foi cortado. Aqui o ginasio e fala,
@ batalha, fala e FLAG_INSIGNIA_JOHTO_4. Zero var gasta.

EcruteakCity_Gym_MapScripts::
	.byte 0

EcruteakCity_Gym_EventScript_Jeffrey::
	trainerbattle_single TRAINER_JOHTO_SAGE_JEFFREY, EcruteakCity_Gym_Text_JeffreySeen, EcruteakCity_Gym_Text_JeffreyBeaten
	msgbox EcruteakCity_Gym_Text_JeffreyAfter, MSGBOX_AUTOCLOSE
	end

EcruteakCity_Gym_EventScript_Martha::
	trainerbattle_single TRAINER_JOHTO_MEDIUM_MARTHA, EcruteakCity_Gym_Text_MarthaSeen, EcruteakCity_Gym_Text_MarthaBeaten
	msgbox EcruteakCity_Gym_Text_MarthaAfter, MSGBOX_AUTOCLOSE
	end

EcruteakCity_Gym_EventScript_Ping::
	trainerbattle_single TRAINER_JOHTO_SAGE_PING, EcruteakCity_Gym_Text_PingSeen, EcruteakCity_Gym_Text_PingBeaten
	msgbox EcruteakCity_Gym_Text_PingAfter, MSGBOX_AUTOCLOSE
	end

EcruteakCity_Gym_EventScript_Grace::
	trainerbattle_single TRAINER_JOHTO_MEDIUM_GRACE, EcruteakCity_Gym_Text_GraceSeen, EcruteakCity_Gym_Text_GraceBeaten
	msgbox EcruteakCity_Gym_Text_GraceAfter, MSGBOX_AUTOCLOSE
	end

EcruteakCity_Gym_EventScript_Morty::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_4, EcruteakCity_Gym_EventScript_MortyDerrotado
	msgbox EcruteakCity_Gym_Text_MortyIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_LEADER_MORTY, EcruteakCity_Gym_Text_MortyDefeat
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox EcruteakCity_Gym_Text_MortyBadge, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_JOHTO_4
	closemessage
	release
	end

EcruteakCity_Gym_EventScript_MortyDerrotado::
	msgbox EcruteakCity_Gym_Text_MortyPost, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Gym_EventScript_GymGuy::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_4, EcruteakCity_Gym_EventScript_GuideAfter
	msgbox EcruteakCity_Gym_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

EcruteakCity_Gym_EventScript_GuideAfter::
	msgbox EcruteakCity_Gym_Text_GuideAfter, MSGBOX_DEFAULT
	release
	end

EcruteakCity_Gym_EventScript_Statue::
	goto_if_set FLAG_INSIGNIA_JOHTO_4, EcruteakCity_Gym_EventScript_StatueCertified
	msgbox EcruteakCity_Gym_Text_Statue, MSGBOX_SIGN
	end

EcruteakCity_Gym_EventScript_StatueCertified::
	msgbox EcruteakCity_Gym_Text_StatueCertified, MSGBOX_SIGN
	end

EcruteakCity_Gym_Text_JeffreySeen:
	.string "I spent the spring with my\n"
	.string "POKéMON.\p"
	.string "Then summer, fall, and winter...\p"
	.string "Then spring came again.\n"
	.string "We've been together a long time.$"

EcruteakCity_Gym_Text_JeffreyBeaten:
	.string "Wins and losses--I've known\n"
	.string "them both.$"

EcruteakCity_Gym_Text_JeffreyAfter:
	.string "Where did POKéMON come from?$"

EcruteakCity_Gym_Text_MarthaSeen:
	.string "I shall win!$"

EcruteakCity_Gym_Text_MarthaBeaten:
	.string "I... I... I lost!$"

EcruteakCity_Gym_Text_MarthaAfter:
	.string "The one who wants to win the\n"
	.string "most is the one who will!$"

EcruteakCity_Gym_Text_PingSeen:
	.string "Can you inflict any damage\n"
	.string "on our POKéMON?$"

EcruteakCity_Gym_Text_PingBeaten:
	.string "Ah! Well done!$"

EcruteakCity_Gym_Text_PingAfter:
	.string "We use GHOST-type POKéMON.\p"
	.string "No NORMAL-type attacks can\n"
	.string "harm them!$"

EcruteakCity_Gym_Text_GraceSeen:
	.string "Stumped by our dark corridors?\n"
	.string "Defeat me if you want a hint!$"

EcruteakCity_Gym_Text_GraceBeaten:
	.string "Wha-what?$"

EcruteakCity_Gym_Text_GraceAfter:
	.string "Fine. I'll tell you the secret\n"
	.string "of the shadows.\p"
	.string "The path is right in front of\n"
	.string "your eyes!$"

EcruteakCity_Gym_Text_MortyIntro:
	.string "Good of you to have come.\p"
	.string "Here in ECRUTEAK, POKéMON have\n"
	.string "always been revered.\p"
	.string "It's said that a rainbow-colored\n"
	.string "POKéMON will come down to\l"
	.string "appear before a true Trainer.\p"
	.string "I believed that tale, so I've\n"
	.string "trained here in secret.\p"
	.string "As a result, I can now see what\n"
	.string "others cannot.\p"
	.string "Just a bit more...\p"
	.string "With a little more, I could see\n"
	.string "a future where I meet the\l"
	.string "rainbow-colored POKéMON.\p"
	.string "You're going to help me reach\n"
	.string "that level!$"

EcruteakCity_Gym_Text_MortyDefeat:
	.string "I'm not good enough yet...\p"
	.string "All right. This BADGE is yours.$"

EcruteakCity_Gym_Text_MortyBadge:
	.string "With the FOGBADGE, POKéMON up\n"
	.string "to Level 50 will obey you.\p"
	.string "Also, any POKéMON that knows\n"
	.string "SURF will be able to use it\l"
	.string "anytime.\p"
	.string "I want you to have this too.$"

EcruteakCity_Gym_Text_MortyPost:
	.string "I see...\p"
	.string "Your journey has taken you to\n"
	.string "far-off places.\p"
	.string "You've witnessed more than I\n"
	.string "ever have.\p"
	.string "I envy you for that...$"

EcruteakCity_Gym_Text_GuideBefore:
	.string "Hey CHAMP! You're almost\n"
	.string "halfway there!\p"
	.string "Trainers here use GHOST and\n"
	.string "DARK-type POKéMON.\p"
	.string "While MORTY is a GHOST-type\n"
	.string "expert, be wary of his mystic\l"
	.string "deer.\p"
	.string "It's said to cause strange\n"
	.string "nightmares...$"

EcruteakCity_Gym_Text_GuideAfter:
	.string "Whew, {PLAYER}. You did great!\p"
	.string "I was cowering in the corner\n"
	.string "out of pure terror!$"

EcruteakCity_Gym_Text_Statue:
	.string "ECRUTEAK CITY POKéMON GYM\n"
	.string "Leader: MORTY$"

EcruteakCity_Gym_Text_StatueCertified:
	.string "ECRUTEAK CITY POKéMON GYM\p"
	.string "MORTY'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"
