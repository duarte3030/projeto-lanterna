@ Ginasio de OLIVINE CITY, portado de fontes-mapas/hns por
@ dev_scripts/porta_ginasios_johto.py. Nao editar a mao: rode o script.
@ ponytail: o enredo de var do hns foi cortado. Aqui o ginasio e fala,
@ batalha, fala e FLAG_INSIGNIA_JOHTO_5. Zero var gasta.

OlivineCity_Gym_MapScripts::
	.byte 0

OlivineCity_Gym_EventScript_Jasmine::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_5, OlivineCity_Gym_EventScript_JasmineDerrotado
	msgbox OlivineCity_Gym_Text_JasmineIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_LEADER_JASMINE, OlivineCity_Gym_Text_JasmineDefeat
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox OlivineCity_Gym_Text_JasmineBadge, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_JOHTO_5
	closemessage
	release
	end

OlivineCity_Gym_EventScript_JasmineDerrotado::
	msgbox OlivineCity_Gym_Text_JasminePost, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_5, OlivineCity_Gym_EventScript_GuideAfter
	msgbox OlivineCity_Gym_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

OlivineCity_Gym_EventScript_GuideAfter::
	msgbox OlivineCity_Gym_Text_GuideAfter, MSGBOX_DEFAULT
	release
	end

OlivineCity_Gym_EventScript_Lass::
	msgbox OlivineCity_Gym_Text_Lass, MSGBOX_NPC
	end

OlivineCity_Gym_EventScript_Gent::
	msgbox OlivineCity_Gym_Text_Gent, MSGBOX_NPC
	end

OlivineCity_Gym_EventScript_Statue::
	goto_if_set FLAG_INSIGNIA_JOHTO_5, OlivineCity_Gym_EventScript_StatueCertified
	msgbox OlivineCity_Gym_Text_Statue, MSGBOX_SIGN
	end

OlivineCity_Gym_EventScript_StatueCertified::
	msgbox OlivineCity_Gym_Text_StatueCertified, MSGBOX_SIGN
	end

OlivineCity_Gym_Text_JasmineIntro:
	.string "…Thank you for your help at the\n"
	.string "LIGHTHOUSE…\p"
	.string "But this is different.\n"
	.string "Please allow me to introduce myself.\p"
	.string "I am JASMINE, a GYM LEADER.\n"
	.string "I use the STEEL-type.\p"
	.string "…Do you know about the STEEL-type?\p"
	.string "It's a type that was only recently\n"
	.string "discovered.\p"
	.string "…Um… May I begin?$"

OlivineCity_Gym_Text_JasmineDefeat:
	.string "…You are a better trainer than me,\n"
	.string "in both skill and kindness.\p"
	.string "In accordance with LEAGUE rules,\n"
	.string "I confer upon you this BADGE.$"

OlivineCity_Gym_Text_JasmineBadge:
	.string "MINERALBADGE raises POKéMON's \n"
	.string "SPECIAL DEFENSE.\p"
	.string "…Um… Please take this too…$"

OlivineCity_Gym_Text_JasminePost:
	.string "Um… I don't know how to say this,\n"
	.string "but good luck…$"

OlivineCity_Gym_Text_GuideBefore:
	.string "JASMINE uses the newly discovered\n"
	.string "STEEL-type.\p"
	.string "She's known for having not one,\n"
	.string "but two aces.\p"
	.string "The first is a metal bug that can\n"
	.string "use a technique to boost its ATTACK.\p"
	.string "While fire will hurt it, it can\n"
	.string "sometimes endure powerful blows.\p"
	.string "The second is a giant iron snake\n"
	.string "with lots of powerful moves.\p"
	.string "Approach it with caution.\p"
	.string "It may look slow, but I've seen it\n"
	.string "strike first with shocking displays\l"
	.string "of SPEED.$"

OlivineCity_Gym_Text_GuideAfter:
	.string "That was awesome.\p"
	.string "The STEEL-type, huh?\p"
	.string "That was a close encounter of an\n"
	.string "unknown kind!$"

OlivineCity_Gym_Text_Lass:
	.string "Giggle...\n"
	.string "I know how capable you are\l"
	.string "from the LIGHTHOUSE.\p"
	.string "It's time you showed that side of\n"
	.string "yourself to JASMINE! Good luck!$"

OlivineCity_Gym_Text_Gent:
	.string "I knew you'd come here.\p"
	.string "Thank you for helping the GYM LEADER,\n"
	.string "but battle is a separate matter.\p"
	.string "Go for it!$"

OlivineCity_Gym_Text_Statue:
	.string "OLIVINE CITY POKéMON GYM\n"
	.string "Leader: JASMINE$"

OlivineCity_Gym_Text_StatueCertified:
	.string "OLIVINE CITY POKéMON GYM\p"
	.string "JASMINE'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"
