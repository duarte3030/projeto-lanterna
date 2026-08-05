@ Ginasio de MAHOGANY TOWN, portado de fontes-mapas/hns por
@ dev_scripts/porta_ginasios_johto.py. Nao editar a mao: rode o script.
@ ponytail: o enredo de var do hns foi cortado. Aqui o ginasio e fala,
@ batalha, fala e FLAG_INSIGNIA_JOHTO_7. Zero var gasta.

MahoganyTown_Gym_MapScripts::
	.byte 0

MahoganyTown_Gym_EventScript_Clarissa::
	trainerbattle_single TRAINER_JOHTO_SKIER_CLARISSA, MahoganyTown_Gym_Text_ClarissaSeen, MahoganyTown_Gym_Text_ClarissaBeaten
	msgbox MahoganyTown_Gym_Text_ClarissaAfter, MSGBOX_AUTOCLOSE
	end

MahoganyTown_Gym_EventScript_Brad::
	trainerbattle_single TRAINER_JOHTO_SKIER_BRAD, MahoganyTown_Gym_Text_BradSeen, MahoganyTown_Gym_Text_BradBeaten
	msgbox MahoganyTown_Gym_Text_BradAfter, MSGBOX_AUTOCLOSE
	end

MahoganyTown_Gym_EventScript_Ronald::
	trainerbattle_single TRAINER_JOHTO_GENTLEMAN_RONALD, MahoganyTown_Gym_Text_RonaldSeen, MahoganyTown_Gym_Text_RonaldBeaten
	msgbox MahoganyTown_Gym_Text_RonaldAfter, MSGBOX_AUTOCLOSE
	end

MahoganyTown_Gym_EventScript_Douglas::
	trainerbattle_single TRAINER_JOHTO_BOARDER_DOUGLAS, MahoganyTown_Gym_Text_DouglasSeen, MahoganyTown_Gym_Text_DouglasBeaten
	msgbox MahoganyTown_Gym_Text_DouglasAfter, MSGBOX_AUTOCLOSE
	end

MahoganyTown_Gym_EventScript_Roxanne::
	trainerbattle_single TRAINER_JOHTO_SKIER_ROXANNE, MahoganyTown_Gym_Text_RoxanneSeen, MahoganyTown_Gym_Text_RoxanneBeaten
	msgbox MahoganyTown_Gym_Text_RoxanneAfter, MSGBOX_AUTOCLOSE
	end

MahoganyTown_Gym_EventScript_Pryce::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_7, MahoganyTown_Gym_EventScript_PryceDerrotado
	msgbox MahoganyTown_Gym_Text_PryceIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_LEADER_PRYCE, MahoganyTown_Gym_Text_PryceDefeat
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox MahoganyTown_Gym_Text_PryceBadge, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_JOHTO_7
	closemessage
	release
	end

MahoganyTown_Gym_EventScript_PryceDerrotado::
	msgbox MahoganyTown_Gym_Text_PrycePost, MSGBOX_DEFAULT
	closemessage
	release
	end

MahoganyTown_Gym_EventScript_GymGuy::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_7, MahoganyTown_Gym_EventScript_GuideAfter
	msgbox MahoganyTown_Gym_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

MahoganyTown_Gym_EventScript_GuideAfter::
	msgbox MahoganyTown_Gym_Text_GuideAfter, MSGBOX_DEFAULT
	release
	end

MahoganyTown_Gym_EventScript_Statue::
	goto_if_set FLAG_INSIGNIA_JOHTO_7, MahoganyTown_Gym_EventScript_StatueCertified
	msgbox MahoganyTown_Gym_Text_Statue, MSGBOX_SIGN
	end

MahoganyTown_Gym_EventScript_StatueCertified::
	msgbox MahoganyTown_Gym_Text_StatueCertified, MSGBOX_SIGN
	end

MahoganyTown_Gym_Text_ClarissaSeen:
	.string "Check out my parallel turn!$"

MahoganyTown_Gym_Text_ClarissaBeaten:
	.string "No! You made me wipe out!$"

MahoganyTown_Gym_Text_ClarissaAfter:
	.string "I shouldn't have been bragging\n"
	.string "about my skiing…$"

MahoganyTown_Gym_Text_BradSeen:
	.string "This GYM has a slippery floor.\p"
	.string "It's fun, isn't it?\p"
	.string "But hey--we're not playing\n"
	.string "games here!$"

MahoganyTown_Gym_Text_BradBeaten:
	.string "Do you see how serious we are?$"

MahoganyTown_Gym_Text_BradAfter:
	.string "This GYM is great.\n"
	.string "I love boarding with my\l"
	.string "POKéMON!$"

MahoganyTown_Gym_Text_RonaldSeen:
	.string "I'll freeze your POKéMON,\n"
	.string "so you can't do a thing!$"

MahoganyTown_Gym_Text_RonaldBeaten:
	.string "Darn. I couldn't do a thing.$"

MahoganyTown_Gym_Text_RonaldAfter:
	.string "I think there's a move a\n"
	.string "POKéMON can use while it's\l"
	.string "frozen.$"

MahoganyTown_Gym_Text_DouglasSeen:
	.string "I know PRYCE's secret.$"

MahoganyTown_Gym_Text_DouglasBeaten:
	.string "OK. I'll tell you PRYCE's secret.$"

MahoganyTown_Gym_Text_DouglasAfter:
	.string "The secret behind PRYCE's power…\p"
	.string "He meditates under a waterfall\n"
	.string "daily to strengthen his mind\l"
	.string "and body.$"

MahoganyTown_Gym_Text_RoxanneSeen:
	.string "To get to PRYCE, our GYM LEADER,\n"
	.string "you need to think before you skate.$"

MahoganyTown_Gym_Text_RoxanneBeaten:
	.string "I wouldn't lose to you in skiing!$"

MahoganyTown_Gym_Text_RoxanneAfter:
	.string "If you don't skate with precision,\n"
	.string "you won't get far in this GYM.$"

MahoganyTown_Gym_Text_PryceIntro:
	.string "POKéMON have many experiences\n"
	.string "in their lives, just like we do.\p"
	.string "I, too, have seen and suffered\n"
	.string "much in my life.\p"
	.string "Since I am your elder, let me\n"
	.string "show you what I mean.\p"
	.string "I have been with POKéMON since\n"
	.string "before you were born.\p"
	.string "I do not lose easily.\p"
	.string "I, PRYCE--the winter trainer--\n"
	.string "shall demonstrate my power!$"

MahoganyTown_Gym_Text_PryceDefeat:
	.string "Ah, I am impressed by your\n"
	.string "prowess.\p"
	.string "With your strong will, I know you\n"
	.string "will overcome all life's obstacles.\p"
	.string "You are worthy of this BADGE!$"

MahoganyTown_Gym_Text_PryceBadge:
	.string "That BADGE will raise the SPECIAL\n"
	.string "ATTACK of POKéMON.\p"
	.string "It also lets your POKéMON use\n"
	.string "WHIRLPOOL to get across\l"
	.string "real whirlpools.\p"
	.string "And this… This is a gift from me!$"

MahoganyTown_Gym_Text_PrycePost:
	.string "When the ice and snow melt,\n"
	.string "spring arrives.\p"
	.string "You and your POKéMON will be\n"
	.string "together for many years to come.\p"
	.string "Cherish your time together!$"

MahoganyTown_Gym_Text_GuideBefore:
	.string "PRYCE is a veteran who has\n"
	.string "trained POKéMON for some 50 years.\p"
	.string "He's got a solid lineup of\n"
	.string "POKéMON to cover whatever\l"
	.string "you bring his way.\p"
	.string "Fire is a good place to start,\n"
	.string "but watch out for the rain!$"

MahoganyTown_Gym_Text_GuideAfter:
	.string "PRYCE is something, but you're\n"
	.string "something else!\p"
	.string "That was a hot battle that\n"
	.string "bridged the generation gap!$"

MahoganyTown_Gym_Text_Statue:
	.string "MAHOGANY TOWN POKéMON GYM\n"
	.string "Leader: PRYCE$"

MahoganyTown_Gym_Text_StatueCertified:
	.string "MAHOGANY TOWN POKéMON GYM\p"
	.string "PRYCE'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"
