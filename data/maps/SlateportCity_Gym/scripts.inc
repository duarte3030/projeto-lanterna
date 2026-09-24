@ SlateportCity_Gym: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 9.14) por dev_scripts/copia_planta_ex.py.

SlateportCity_Gym_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 9.14), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
SlateportCity_Gym_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_SLATEPORT_CITY_GYM_GREGORY, SlateportCity_Gym_Text_ExTrainer2Intro, SlateportCity_Gym_Text_ExTrainer2Defeat
	msgbox SlateportCity_Gym_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

SlateportCity_Gym_Text_ExTrainer2Intro:
	.string "You know my father built this place.$"

SlateportCity_Gym_Text_ExTrainer2Defeat:
	.string "Hey you’re strong!$"

SlateportCity_Gym_Text_ExTrainer2PostBattle:
	.string "My father and god-father own a\n"
	.string "construction company and worked\l"
	.string "together to build this GYM for GRETA.$"

SlateportCity_Gym_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_SLATEPORT_CITY_GYM_ACE, SlateportCity_Gym_Text_ExTrainer3Intro, SlateportCity_Gym_Text_ExTrainer3Defeat
	msgbox SlateportCity_Gym_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

SlateportCity_Gym_Text_ExTrainer3Intro:
	.string "Do you like the boat I’m building?.$"

SlateportCity_Gym_Text_ExTrainer3Defeat:
	.string "Maybe I should train my POKéMON as much\n"
	.string "as I work on the boat!$"

SlateportCity_Gym_Text_ExTrainer3PostBattle:
	.string "My dad’s a sailor and I’m building the\n"
	.string "boat as a gift for when he gets back!\p"
	.string "I just don’t know how I’m going to get it\n"
	.string "out the door...$"

SlateportCity_Gym_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_SLATEPORT_CITY_GYM_SKIPPY, SlateportCity_Gym_Text_ExTrainer4Intro, SlateportCity_Gym_Text_ExTrainer4Defeat
	msgbox SlateportCity_Gym_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

SlateportCity_Gym_Text_ExTrainer4Intro:
	.string "Are you going to make something?$"

SlateportCity_Gym_Text_ExTrainer4Defeat:
	.string "Oh, you’re here just to battle.$"

SlateportCity_Gym_Text_ExTrainer4PostBattle:
	.string "I’m trying to think of something to\n"
	.string "make.\p"
	.string "What would be a good starter project?$"

SlateportCity_Gym_EventScript_ExTrainer5::
	trainerbattle_single TRAINER_HOENNEX_SLATEPORT_CITY_GYM_NERDAL, SlateportCity_Gym_Text_ExTrainer5Intro, SlateportCity_Gym_Text_ExTrainer5Defeat
	msgbox SlateportCity_Gym_Text_ExTrainer5PostBattle, MSGBOX_AUTOCLOSE
	end

SlateportCity_Gym_Text_ExTrainer5Intro:
	.string "Stop right there!\p"
	.string "GRETA is way to strong, cool, and\n"
	.string "elegant to battle someone like you.$"

SlateportCity_Gym_Text_ExTrainer5Defeat:
	.string "W-w-w-what!?.$"

SlateportCity_Gym_Text_ExTrainer5PostBattle:
	.string "GRETA is going to crush you.$"

SlateportCity_Gym_EventScript_ExTrainer6::
	trainerbattle_double TRAINER_HOENNEX_SLATEPORT_CITY_GYM_LEAH_LEIA, SlateportCity_Gym_Text_ExTrainer6Intro, SlateportCity_Gym_Text_ExTrainer6Defeat, SlateportCity_Gym_Text_ExTrainer6NotEnough
	msgbox SlateportCity_Gym_Text_ExTrainer6PostBattle, MSGBOX_AUTOCLOSE
	end

SlateportCity_Gym_Text_ExTrainer6NotEnough:
	.string "Come back with another POKéMON, and\n"
	.string "we’ll show you our DARK TYPE POKéMON.$"

SlateportCity_Gym_Text_ExTrainer6Intro:
	.string "LEAH: What’s your favorite TYPE of\n"
	.string "POKéMON?\p"
	.string "LEIA: Our’s is the DARK TYPE!$"

SlateportCity_Gym_Text_ExTrainer6Defeat:
	.string "LEAH: DARK TYPES rule!\p"
	.string "LEIA: LEAH we lost...$"

SlateportCity_Gym_Text_ExTrainer6PostBattle:
	.string "LEAH: DARK TYPE POKéMON are easily the\n"
	.string "best. They’re cool, edgy, sweet,\l"
	.string "awesome, mysterious, fast, wonderful,\l"
	.string "dangerous, powerful, sharp, adaptable,\l"
	.string "affectionate, fearless...\p"
	.string "LEIA: She’ll be going on for a while, it’s\n"
	.string "best if you just walk away.$"


@ Líder, guia e estátuas do ginásio do EX (mapa 9.14), reescritos no nosso formato a partir do
@ texto da ROM (lote G1 da onda 2). A vitória é goto_if_defeated no líder; a insígnia é FLAG_INSIGNIA_HOENN_10.

SlateportCity_Gym_EventScript_Greta::
	trainerbattle_single TRAINER_HOENNEX_GRETA, SlateportCity_Gym_Text_GretaIntro, SlateportCity_Gym_Text_GretaDefeat, SlateportCity_Gym_EventScript_GretaDefeated, NO_MUSIC
	goto_if_unset FLAG_HOENNEX_RECEIVED_TM_TORMENT, SlateportCity_Gym_EventScript_GiveGretaItem
	msgbox SlateportCity_Gym_Text_GretaPostBattle, MSGBOX_DEFAULT
	release
	end

SlateportCity_Gym_EventScript_GretaDefeated::
	message SlateportCity_Gym_Text_ReceivedGretaBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox SlateportCity_Gym_Text_GretaBadgeInfo, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_HOENN_10
	settrainerflag TRAINER_HOENNEX_SLATEPORT_CITY_GYM_GREGORY
	settrainerflag TRAINER_HOENNEX_SLATEPORT_CITY_GYM_ACE
	settrainerflag TRAINER_HOENNEX_SLATEPORT_CITY_GYM_SKIPPY
	settrainerflag TRAINER_HOENNEX_SLATEPORT_CITY_GYM_NERDAL
	settrainerflag TRAINER_HOENNEX_SLATEPORT_CITY_GYM_LEAH_LEIA
	call_if_eq VAR_PETALBURG_GYM_STATE, 6, Common_EventScript_ReadyPetalburgGymForBattle
	goto SlateportCity_Gym_EventScript_GiveGretaItem
	end

SlateportCity_Gym_EventScript_GiveGretaItem::
	giveitem ITEM_TM_TORMENT
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_HOENNEX_RECEIVED_TM_TORMENT
	msgbox SlateportCity_Gym_Text_ExplainGretaItem, MSGBOX_DEFAULT
	release
	end

SlateportCity_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_defeated TRAINER_HOENNEX_GRETA, SlateportCity_Gym_EventScript_GymGuidePostVictory
	msgbox SlateportCity_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

SlateportCity_Gym_EventScript_GymGuidePostVictory::
	msgbox SlateportCity_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	release
	end

SlateportCity_Gym_EventScript_LeftGymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_10, SlateportCity_Gym_EventScript_GymStatueCertified
	goto SlateportCity_Gym_EventScript_GymStatue
	end

SlateportCity_Gym_EventScript_RightGymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_10, SlateportCity_Gym_EventScript_GymStatueCertified
	goto SlateportCity_Gym_EventScript_GymStatue
	end

SlateportCity_Gym_EventScript_GymStatueCertified::
	msgbox SlateportCity_Gym_Text_GymStatueCertified, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_Gym_EventScript_GymStatue::
	msgbox SlateportCity_Gym_Text_GymStatue, MSGBOX_DEFAULT
	releaseall
	end

SlateportCity_Gym_Text_GretaIntro:
	.string "Hey-ya!\p"
	.string "Welcome to the SLATEPORT CITY GYM!\n"
	.string "I’m GRETA it’s so nice to meet you.\p"
	.string "I hope you don’t mind the mess, when\n"
	.string "your busy making stuff you kinda\l"
	.string "forget to clean up...\p"
	.string "Growing up I always loved making things\n"
	.string "but didn’t have anywhere to work at.\p"
	.string "I ended up finding a cave that I stayed\n"
	.string "in full of DARK TYPE POKéMON.\p"
	.string "Turns out, they are great helpers!\n"
	.string "When I moved here I thought kids would\l"
	.string "want a place to create like I did.\p"
	.string "Sooo, I made this place!\p"
	.string "OK, thats enough chit-chat. Lets build\n"
	.string "a powerful POKéMON battle!$"

SlateportCity_Gym_Text_GretaDefeat:
	.string "Oh My Gosh!\p"
	.string "You are soooo strong.\n"
	.string "You’ve still need a lot of training\l"
	.string "before you could beat me at full\l"
	.string "strength, so don’t get too excited.\p"
	.string "But, of course, you deserve POKéMON\n"
	.string "LEAGUE BUILDER BADGE!$"

SlateportCity_Gym_Text_GretaPostBattle:
	.string "Make sure to keep beating GYMs.\p"
	.string "It would be a bit embarrassing if I was\n"
	.string "the last LEADER to lose to you...$"

SlateportCity_Gym_Text_ReceivedGretaBadge:
	.string "{PLAYER} received the BUILDER BADGE\n"
	.string "from GRETA.$"

SlateportCity_Gym_Text_GretaBadgeInfo:
	.string "With the BUILDER BADGE POKéMON up to\n"
	.string "level 35 listen to ya!$"

SlateportCity_Gym_Text_ExplainGretaItem:
	.string "TM41, contains TORMENT.\p"
	.string "POKéMON hit by it will want to show off,\n"
	.string "and won’t use the same move twice.\p"
	.string "The moves great. Wait till you see the\n"
	.string "faces people make when their POKéMON\l"
	.string "quit listening to them.\p"
	.string "Priceless.$"

SlateportCity_Gym_Text_GymGuideAdvice:
	.string "Hey, hey, hey there’s my favorite\n"
	.string "CHAMP-IN-THE-MAKING!\p"
	.string "Welcome to the SLATEPORT CITY POKéMON\n"
	.string "GYM, specializing in DARK TYPE POKéMON.\l"
	.string "The LEADER here is GRETA.\p"
	.string "She’s a spunky gal but don’t let her\n"
	.string "small stature fool ya, she’s a\l"
	.string "power-house of a GYM LEADER.\p"
	.string "I wouldn’t use PSYCHIC or GHOST TYPE\n"
	.string "POKéMON if I were you. Instead go for\l"
	.string "FIGHTING or BUG TYPEs to break through\l"
	.string "her defences.\p"
	.string "Pst-pst... Hey just between you and me\n"
	.string "maybe bring a ICE TYPE too...\p"
	.string "Good luck {PLAYER}!$"

SlateportCity_Gym_Text_GymGuidePostVictory:
	.string "{PLAYER}!\n"
	.string "That was Out-A-This-World!\p"
	.string "I’m sure my hollering helped you battle\n"
	.string "like no one has before!$"

SlateportCity_Gym_Text_GymStatue:
	.string "SLATEPORT CITY POKéMON GYM$"

SlateportCity_Gym_Text_GymStatueCertified:
	.string "SLATEPORT CITY POKéMON GYM\p"
	.string "GRETA’S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

