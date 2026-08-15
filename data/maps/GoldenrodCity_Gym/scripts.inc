@ Ginasio de GOLDENROD CITY, portado de fontes-mapas/hns por
@ dev_scripts/porta_ginasios_johto.py. Nao editar a mao: rode o script.
@ ponytail: o enredo de var do hns foi cortado, MENOS a cena do choro da
@ WHITNEY, que e autocontida na fonte e custa UMA var (VAR_JOHTO_GOLDENROD_GYM_STATE).
@ A insignia sai no galho da BRIDGET, nao logo depois da batalha.

GoldenrodCity_Gym_MapScripts::
	.byte 0

GoldenrodCity_Gym_EventScript_Carrie::
	trainerbattle_single TRAINER_JOHTO_LASS_CARRIE, GoldenrodCity_Gym_Text_CarrieSeen, GoldenrodCity_Gym_Text_CarrieBeaten
	msgbox GoldenrodCity_Gym_Text_CarrieAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_Gym_EventScript_Victoria::
	trainerbattle_single TRAINER_JOHTO_BEAUTY_VICTORIA, GoldenrodCity_Gym_Text_VictoriaSeen, GoldenrodCity_Gym_Text_VictoriaBeaten
	msgbox GoldenrodCity_Gym_Text_VictoriaAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_Gym_EventScript_Samantha::
	trainerbattle_single TRAINER_JOHTO_BEAUTY_SAMANTHA, GoldenrodCity_Gym_Text_SamanthaSeen, GoldenrodCity_Gym_Text_SamanthaBeaten
	msgbox GoldenrodCity_Gym_Text_SamanthaAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_Gym_EventScript_Bridget::
	trainerbattle_single TRAINER_JOHTO_LASS_BRIDGET, GoldenrodCity_Gym_Text_BridgetSeen, GoldenrodCity_Gym_Text_BridgetBeaten
	msgbox GoldenrodCity_Gym_Text_BridgetAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_Gym_EventScript_Whitney::
	lock
	faceplayer
	goto_if_eq VAR_JOHTO_GOLDENROD_GYM_STATE, 3, GoldenrodCity_Gym_EventScript_WhitneyChorando
	goto_if_eq VAR_JOHTO_GOLDENROD_GYM_STATE, 4, GoldenrodCity_Gym_EventScript_WhitneyInsignia
	goto_if_set FLAG_INSIGNIA_JOHTO_3, GoldenrodCity_Gym_EventScript_WhitneyDerrotado
	msgbox GoldenrodCity_Gym_Text_WhitneyIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_LEADER_WHITNEY, GoldenrodCity_Gym_Text_WhitneyDefeat
	msgbox GoldenrodCity_Gym_Text_WhitneyYouMeanie, MSGBOX_DEFAULT
	setvar VAR_JOHTO_GOLDENROD_GYM_STATE, 3
	closemessage
	release
	end

GoldenrodCity_Gym_EventScript_WhitneyChorando::
	msgbox GoldenrodCity_Gym_Text_WhitneyYouMeanie, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Gym_EventScript_WhitneyInsignia::
	msgbox GoldenrodCity_Gym_Text_WhitneyWhatDoYouWant, MSGBOX_DEFAULT
	closemessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox GoldenrodCity_Gym_Text_WhitneyBadge, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_JOHTO_3
	setvar VAR_JOHTO_GOLDENROD_GYM_STATE, 5
	closemessage
	release
	end

GoldenrodCity_Gym_EventScript_WhitneyDerrotado::
	msgbox GoldenrodCity_Gym_Text_WhitneyPost, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_Gym_EventScript_ChoroTrigger::
	lock
	turnobject LOCALID_GOLDENROD_CITY_GYM_BRIDGET, DIR_WEST
	msgbox GoldenrodCity_Gym_Text_BridgetWhitneyCries, MSGBOX_DEFAULT
	closemessage
	setvar VAR_JOHTO_GOLDENROD_GYM_STATE, 4
	release
	end

GoldenrodCity_Gym_EventScript_Gym_Guy::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_JOHTO_3, GoldenrodCity_Gym_EventScript_GuideAfter
	msgbox GoldenrodCity_Gym_Text_GuideBefore, MSGBOX_DEFAULT
	release
	end

GoldenrodCity_Gym_EventScript_GuideAfter::
	msgbox GoldenrodCity_Gym_Text_GuideAfter, MSGBOX_DEFAULT
	release
	end

GoldenrodCity_Gym_EventScript_Statue::
	goto_if_set FLAG_INSIGNIA_JOHTO_3, GoldenrodCity_Gym_EventScript_StatueCertified
	msgbox GoldenrodCity_Gym_Text_Statue, MSGBOX_SIGN
	end

GoldenrodCity_Gym_EventScript_StatueCertified::
	msgbox GoldenrodCity_Gym_Text_StatueCertified, MSGBOX_SIGN
	end

GoldenrodCity_Gym_Text_CarrieSeen:
	.string "Don't let my POKéMON's cute looks\n"
	.string "fool you.\p"
	.string "They can whip you!$"

GoldenrodCity_Gym_Text_CarrieBeaten:
	.string "Darn… I thought you were weak…$"

GoldenrodCity_Gym_Text_CarrieAfter:
	.string "Do my POKéMON think I'm cute?$"

GoldenrodCity_Gym_Text_VictoriaSeen:
	.string "Oh, you are a cute little trainer!\p"
	.string "I like you, but I won't hold back!$"

GoldenrodCity_Gym_Text_VictoriaBeaten:
	.string "Let's see… Oops, it's over?$"

GoldenrodCity_Gym_Text_VictoriaAfter:
	.string "Wow, you must be good to beat me!\n"
	.string "Keep it up!$"

GoldenrodCity_Gym_Text_SamanthaSeen:
	.string "Give it your best shot, or I'll take\n"
	.string "you down!$"

GoldenrodCity_Gym_Text_SamanthaBeaten:
	.string "No! Oh, MEOWTH, I'm so sorry!$"

GoldenrodCity_Gym_Text_SamanthaAfter:
	.string "I taught MEOWTH moves for taking on\n"
	.string "any type…$"

GoldenrodCity_Gym_Text_BridgetSeen:
	.string "I like cute POKéMON better than\n"
	.string "strong POKéMON.\p"
	.string "But I have strong and cute POKéMON!$"

GoldenrodCity_Gym_Text_BridgetBeaten:
	.string "Oh, no, no, no!$"

GoldenrodCity_Gym_Text_BridgetAfter:
	.string "I'm trying to beat WHITNEY, but…\n"
	.string "It's depressing.\p"
	.string "I'm okay! If I lose, I'll just try\n"
	.string "harder next time!$"

GoldenrodCity_Gym_Text_WhitneyIntro:
	.string "Hi! I'm WHITNEY!\p"
	.string "Everyone was into POKéMON, so I got\n"
	.string "into it too!\p"
	.string "POKéMON are super-cute!\p"
	.string "You want to battle? I'm warning\n"
	.string "you- I'm good!$"

GoldenrodCity_Gym_Text_WhitneyDefeat:
	.string "Sob…\p"
	.string "…Waaaaaaah! You're mean!\p"
	.string "You shouldn't be so serious! You…\n"
	.string "you child, you!$"

GoldenrodCity_Gym_Text_WhitneyBadge:
	.string "PLAINBADGE lets your POKéMON use\n"
	.string "STRENGTH outside of battle.\p"
	.string "It also boosts your POKéMON's\n"
	.string "DEFENSE.\p"
	.string "Oh, you can have this too!$"

GoldenrodCity_Gym_Text_WhitneyPost:
	.string "Ah, that was a good cry!$"

GoldenrodCity_Gym_Text_WhitneyYouMeanie:
	.string "Waaaaah!\p"
	.string "Waaaaah!\p"
	.string "…Snivel, hic… …You meanie!$"

GoldenrodCity_Gym_Text_WhitneyWhatDoYouWant:
	.string "…Sniff…\p"
	.string "What? What do you want? A BADGE?\p"
	.string "Oh, right. I forgot. Here's\n"
	.string "PLAINBADGE.$"

GoldenrodCity_Gym_Text_BridgetWhitneyCries:
	.string "Oh, no. You made WHITNEY cry.\p"
	.string "It's OK. She'll stop soon. She\n"
	.string "always cries when she loses.$"

GoldenrodCity_Gym_Text_GuideBefore:
	.string "Yo! CHAMP in making!\p"
	.string "This GYM is home to WHITNEY, the\n"
	.string "master of NORMAL-type POKéMON.\p"
	.string "Be cautious of her cute team.\p"
	.string "Some of the POKéMON in this gym\n"
	.string "have the newly discovered FAIRY\l"
	.string "type as well.\p"
	.string "Check ROUTE 34 if you need a\n"
	.string "FIGHTING-type or POISON-type.$"

GoldenrodCity_Gym_Text_GuideAfter:
	.string "You won? Great! I was busy admiring\n"
	.string "the ladies here.$"

GoldenrodCity_Gym_Text_Statue:
	.string "GOLDENROD CITY POKéMON GYM\n"
	.string "Leader: WHITNEY$"

GoldenrodCity_Gym_Text_StatueCertified:
	.string "GOLDENROD CITY POKéMON GYM\p"
	.string "WHITNEY'S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"
