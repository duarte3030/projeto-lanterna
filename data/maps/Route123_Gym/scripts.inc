@ Route123_Gym: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 34.2) por dev_scripts/copia_planta_ex.py.

Route123_Gym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Route123_Gym_OnLoad
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 34.2), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
Route123_Gym_EventScript_ExTrainer2::
	trainerbattle_single TRAINER_HOENNEX_ROUTE123_GYM_LEON, Route123_Gym_Text_ExTrainer2Intro, Route123_Gym_Text_ExTrainer2Defeat
	msgbox Route123_Gym_Text_ExTrainer2PostBattle, MSGBOX_AUTOCLOSE
	end

Route123_Gym_Text_ExTrainer2Intro:
	.string "Welcome to the GYM.\p"
	.string "Are you ready for your first trial?$"

Route123_Gym_Text_ExTrainer2Defeat:
	.string "The mountains must be good for your\n"
	.string "POKéMON!$"

Route123_Gym_Text_ExTrainer2PostBattle:
	.string "I wished to meet strong POKéMON here\n"
	.string "as a kid.\p"
	.string "When I grew up, somehow all the POKéMON\n"
	.string "got stronger!$"

Route123_Gym_EventScript_ExTrainer3::
	trainerbattle_single TRAINER_HOENNEX_ROUTE123_GYM_VIRGINA, Route123_Gym_Text_ExTrainer3Intro, Route123_Gym_Text_ExTrainer3Defeat
	msgbox Route123_Gym_Text_ExTrainer3PostBattle, MSGBOX_AUTOCLOSE
	end

Route123_Gym_Text_ExTrainer3Intro:
	.string "We will crush you under an avalanche!$"

Route123_Gym_Text_ExTrainer3Defeat:
	.string "…Impossible$"

Route123_Gym_Text_ExTrainer3PostBattle:
	.string "How did you defeat me you arrogant\n"
	.string "pup?$"

Route123_Gym_EventScript_ExTrainer4::
	trainerbattle_single TRAINER_HOENNEX_ROUTE123_GYM_ALUCARD, Route123_Gym_Text_ExTrainer4Intro, Route123_Gym_Text_ExTrainer4Defeat
	msgbox Route123_Gym_Text_ExTrainer4PostBattle, MSGBOX_AUTOCLOSE
	end

Route123_Gym_Text_ExTrainer4Intro:
	.string "Your pathetic POKéMON are no match for\n"
	.string "DRAGONS!$"

Route123_Gym_Text_ExTrainer4Defeat:
	.string "How?\n"
	.string "How is this possible?$"

Route123_Gym_Text_ExTrainer4PostBattle:
	.string "Very well, continue brave trainer.$"

@ Lote G3 (onda 2): reescrito no nosso formato a partir do bytecode e do texto do EX.
Route123_Gym_OnLoad:
	goto_if_unset FLAG_HOENNEX_ROUTE123_GYM_SWITCH_1, Route123_Gym_OnLoad_Fim
	goto_if_set FLAG_HOENNEX_ROUTE123_GYM_SWITCH_2, Route123_Gym_OnLoad_Dois
	@ só o interruptor desta sala: abre o portão de baixo (EX 0x834E7F9)
	setmetatile 14, 17, 0x23D, FALSE
	setmetatile 15, 17, 0x201, FALSE
	setmetatile 16, 17, 0x200, FALSE
	setmetatile 17, 17, 0x23A, FALSE
	setmetatile 14, 18, 0x243, FALSE
	setmetatile 15, 18, 0x200, FALSE
	setmetatile 16, 18, 0x200, FALSE
	setmetatile 17, 18, 0x23B, FALSE
	setmetatile 15, 19, 0x200, FALSE
	setmetatile 16, 19, 0x200, FALSE
	setmetatile 17, 19, 0x23C, FALSE
	setmetatile 5, 20, 0x230, FALSE
	special DrawWholeMapView
	end

Route123_Gym_OnLoad_Dois:
	@ os dois interruptores: os dois portões (EX 0x834E718)
	setmetatile 14, 17, 0x23D, TRUE
	setmetatile 15, 17, 0x201, FALSE
	setmetatile 16, 17, 0x200, FALSE
	setmetatile 17, 17, 0x23A, TRUE
	setmetatile 14, 18, 0x243, TRUE
	setmetatile 15, 18, 0x200, FALSE
	setmetatile 16, 18, 0x200, FALSE
	setmetatile 17, 18, 0x23B, TRUE
	setmetatile 15, 19, 0x200, FALSE
	setmetatile 16, 19, 0x200, FALSE
	setmetatile 17, 19, 0x23C, FALSE
	setmetatile 5, 20, 0x230, FALSE
	setmetatile 17, 10, 0x23D, TRUE
	setmetatile 18, 10, 0x201, FALSE
	setmetatile 19, 10, 0x200, FALSE
	setmetatile 20, 10, 0x23A, TRUE
	setmetatile 17, 11, 0x243, TRUE
	setmetatile 18, 11, 0x200, FALSE
	setmetatile 19, 11, 0x200, FALSE
	setmetatile 20, 11, 0x23B, TRUE
	setmetatile 18, 12, 0x200, FALSE
	setmetatile 19, 12, 0x200, FALSE
	setmetatile 20, 12, 0x23C, FALSE
	special DrawWholeMapView
	end

Route123_Gym_OnLoad_Fim:
	end

Route123_Gym_EventScript_Switch::
	goto_if_set FLAG_HOENNEX_ROUTE123_GYM_SWITCH_1, Route123_Gym_EventScript_SwitchFim
	lockall
	setmetatile 5, 20, 0x230, FALSE
	special DrawWholeMapView
	playse SE_SWITCH
	waitse
	setflag FLAG_HOENNEX_ROUTE123_GYM_SWITCH_1
	releaseall
	end

Route123_Gym_EventScript_SwitchFim::
	releaseall
	end

Route123_Gym_EventScript_Clair::
	trainerbattle_single TRAINER_HOENNEX_CLAIR, Route123_Gym_Text_ClairIntro, Route123_Gym_Text_ClairDefeat, Route123_Gym_EventScript_ClairDefeated, NO_MUSIC
	goto_if_unset FLAG_HOENNEX_RECEIVED_TM_DRAGON_CLAW, Route123_Gym_EventScript_GiveDragonClaw
	msgbox Route123_Gym_Text_ClairPostBattle, MSGBOX_NPC
	end

Route123_Gym_EventScript_ClairDefeated::
	message Route123_Gym_Text_ReceivedDracoBadge
	waitmessage
	call Common_EventScript_PlayGymBadgeFanfare
	msgbox Route123_Gym_Text_ClairTakeThis, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_HOENN_15
	goto Route123_Gym_EventScript_GiveDragonClaw

Route123_Gym_EventScript_GiveDragonClaw::
	giveitem ITEM_TM02
	goto_if_eq VAR_RESULT, FALSE, Common_EventScript_ShowBagIsFull
	setflag FLAG_HOENNEX_RECEIVED_TM_DRAGON_CLAW
	msgbox Route123_Gym_Text_ExplainDragonClaw, MSGBOX_NPC
	release
	end

Route123_Gym_EventScript_GymGuide::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_HOENN_15, Route123_Gym_EventScript_GymGuidePostVictory
	msgbox Route123_Gym_Text_GymGuideAdvice, MSGBOX_DEFAULT
	release
	end

Route123_Gym_EventScript_GymGuidePostVictory::
	msgbox Route123_Gym_Text_GymGuidePostVictory, MSGBOX_DEFAULT
	releaseall
	end

Route123_Gym_EventScript_GymStatue::
	lockall
	goto_if_set FLAG_INSIGNIA_HOENN_15, Route123_Gym_EventScript_GymStatueCertified
	msgbox Route123_Gym_Text_GymStatue, MSGBOX_SIGN
	releaseall
	end

Route123_Gym_EventScript_GymStatueCertified::
	msgbox Route123_Gym_Text_GymStatueCertified, MSGBOX_SIGN
	releaseall
	end

Route123_Gym_Text_ClairIntro:
	.string "I was warned of a child prodigy\n"
	.string "collecting all the Hoenn Badges.\p"
	.string "My name is Clair.\n"
	.string "I hail from JOHTO where I was raised by\l"
	.string "the elders in the DRAGONS DEN.\p"
	.string "They banished me here for my...\n"
	.string "Poor sportsmanship\p"
	.string "They said I must prove myself in a\n"
	.string "crucible of fire to return.\p"
	.string "You will join me in that fire now.$"

Route123_Gym_Text_ClairDefeat:
	.string "Hrnn...\n"
	.string "Sigh...\p"
	.string "A breathtaking performance.\n"
	.string "I still have so much left to learn.\p"
	.string "Here’s the DRACO BADGE.$"

Route123_Gym_Text_ReceivedDracoBadge:
	.string "{PLAYER} received the DRACO BADGE\n"
	.string "from CLAIR.$"

Route123_Gym_Text_ClairTakeThis:
	.string "Don’t get too confident now.\p"
	.string "I was a child prodigy too you know.\p"
	.string "...\n"
	.string "...\p"
	.string "Here...$"

Route123_Gym_Text_ExplainDragonClaw:
	.string "TM02 contains DRAGON CLAW.\p"
	.string "It’s a powerful attack that few things\n"
	.string "can resist..$"

Route123_Gym_Text_ClairPostBattle:
	.string "Don’t get too confident now.\p"
	.string "I was a child prodigy too you know...$"

Route123_Gym_Text_GymGuideAdvice:
	.string "Welcome to one of the secret GYMS!\p"
	.string "Sorry I never mentioned it, I’d lose my\n"
	.string "job if I did.\p"
	.string "Anyways this is the lair of the DRAGON\n"
	.string "master CLAIR!\p"
	.string "Beware her raw power, but with the help\n"
	.string "of some ICE and DRAGON attacks you are\l"
	.string "sure to succeed!$"

Route123_Gym_Text_GymGuidePostVictory:
	.string "{PLAYER}, you just can’t be beat can\n"
	.string "you!$"

Route123_Gym_Text_GymStatue:
	.string "ROUTE 123 POKéMON GYM$"

Route123_Gym_Text_GymStatueCertified:
	.string "ROUTE 123 POKéMON GYM\p"
	.string "CLAIR’S CERTIFIED TRAINERS:\n"
	.string "{PLAYER}$"

