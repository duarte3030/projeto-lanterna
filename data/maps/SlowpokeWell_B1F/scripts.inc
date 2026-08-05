@ SLOWPOKE WELL, portado de fontes-mapas/hns/data/maps/SlowpokeWell_B1F.
@ ponytail: no hns esta cena mexe em VAR_AZALEA_TOWN_STATE e em quatro flags de
@ KURT (aparece aqui, some daqui, aparece na casa). Aqui o KURT e um objeto so,
@ sempre presente, e a fala dele muda com goto_if_defeated do PROTON. A unica
@ flag pedida e FLAG_HIDE_AZALEA_TOWN_ROCKETS, que tambem tira os dois grunts de
@ Azalea (o que fecha o ginasio do BUGSY). Zero var.
@ Nao portado: o warp final para a casa do KURT, os quatro item balls (cada um
@ precisaria de uma FLAG_ITEM_) e os SLOWPOKE de decoracao (sem sprite nesta
@ build). Ver PENDENCIAS-JOHTO.md.

SlowpokeWell_B1F_MapScripts::
	.byte 0

SlowpokeWell_B1F_EventScript_Kurt::
	lock
	goto_if_defeated TRAINER_JOHTO_ROCKET_PROTON, SlowpokeWell_B1F_EventScript_KurtDone
	msgbox SlowpokeWell_B1F_Text_KurtIntro, MSGBOX_DEFAULT
	closemessage
	release
	end

SlowpokeWell_B1F_EventScript_KurtDone::
	msgbox SlowpokeWell_B1F_Text_KurtAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

SlowpokeWell_B1F_EventScript_Grunt1::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_WELL_1, SlowpokeWell_B1F_Text_Grunt1Seen, SlowpokeWell_B1F_Text_Grunt1Beaten
	msgbox SlowpokeWell_B1F_Text_Grunt1After, MSGBOX_AUTOCLOSE
	end

SlowpokeWell_B1F_EventScript_Grunt2::
	trainerbattle_single TRAINER_JOHTO_ROCKET_GRUNT_WELL_2, SlowpokeWell_B1F_Text_Grunt2Seen, SlowpokeWell_B1F_Text_Grunt2Beaten
	msgbox SlowpokeWell_B1F_Text_Grunt2After, MSGBOX_AUTOCLOSE
	end

SlowpokeWell_B1F_EventScript_Eto::
	trainerbattle_single TRAINER_JOHTO_ROCKET_ETO, SlowpokeWell_B1F_Text_EtoSeen, SlowpokeWell_B1F_Text_EtoBeaten
	msgbox SlowpokeWell_B1F_Text_EtoAfter, MSGBOX_AUTOCLOSE
	end

SlowpokeWell_B1F_EventScript_Proton::
	lock
	faceplayer
	goto_if_defeated TRAINER_JOHTO_ROCKET_PROTON, SlowpokeWell_B1F_EventScript_ProtonDone
	msgbox SlowpokeWell_B1F_Text_ProtonSeen, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_JOHTO_ROCKET_PROTON, SlowpokeWell_B1F_Text_ProtonBeaten
	msgbox SlowpokeWell_B1F_Text_ProtonAfter, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	setflag FLAG_HIDE_AZALEA_TOWN_ROCKETS
	removeobject LOCALID_SLOWPOKE_WELL_GRUNT_1
	removeobject LOCALID_SLOWPOKE_WELL_GRUNT_2
	removeobject LOCALID_SLOWPOKE_WELL_ETO
	removeobject LOCALID_SLOWPOKE_WELL_PROTON
	delay 60
	fadescreen FADE_FROM_BLACK
	special DrawWholeMapView
	turnobject OBJ_EVENT_ID_PLAYER, DIR_SOUTH
	applymovement LOCALID_SLOWPOKE_WELL_KURT, SlowpokeWell_B1F_Movement_Kurt
	waitmovement 0
	msgbox SlowpokeWell_B1F_Text_KurtAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

SlowpokeWell_B1F_EventScript_ProtonDone::
	msgbox SlowpokeWell_B1F_Text_ProtonAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

SlowpokeWell_B1F_Movement_Kurt:
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	walk_up
	step_end

SlowpokeWell_B1F_Text_KurtIntro:
	.string "KURT: Hey there, {PLAYER}!\p"
	.string "The guard up top took off when\n"
	.string "I shouted at him.\p"
	.string "But then I took a tumble down\n"
	.string "the WELL.\p"
	.string "I slammed down hard on my back,\n"
	.string "so I can't move.\p"
	.string "Rats! If I were fit, my POKéMON\n"
	.string "would've punished them…\p"
	.string "{PLAYER}, show them how gutsy\n"
	.string "you are in my place!$"

SlowpokeWell_B1F_Text_KurtAfter:
	.string "KURT: Way to go, {PLAYER}!\p"
	.string "TEAM ROCKET has taken off.\p"
	.string "My back's better too.\n"
	.string "Let's get out of here.$"

SlowpokeWell_B1F_Text_Grunt1Seen:
	.string "Darn! I was standing guard up\n"
	.string "top when some old coot yelled\l"
	.string "at me.\p"
	.string "He startled me so much that\n"
	.string "I fell down here.\p"
	.string "I think I'll vent my anger by\n"
	.string "taking it out on you!$"

SlowpokeWell_B1F_Text_Grunt1Beaten:
	.string "Arrgh! This is NOT my day!$"

SlowpokeWell_B1F_Text_Grunt1After:
	.string "Sure, we've been hacking the\n"
	.string "tails off SLOWPOKE and selling\l"
	.string "them.\p"
	.string "Everything we do is for profit.\p"
	.string "That's right! We're TEAM ROCKET,\n"
	.string "and we'll do anything for money!$"

SlowpokeWell_B1F_Text_Grunt2Seen:
	.string "Stop taking TAILS?\p"
	.string "Yeah, just try to defeat all\n"
	.string "of us!$"

SlowpokeWell_B1F_Text_Grunt2Beaten:
	.string "You rotten brat!$"

SlowpokeWell_B1F_Text_Grunt2After:
	.string "SLOWPOKETAILS grow back fast!\p"
	.string "What's wrong with selling them?$"

SlowpokeWell_B1F_Text_EtoSeen:
	.string "Hyuck-hyuck-hyuck!\n"
	.string "Quit taking SLOWPOKETAILS?\p"
	.string "You're nuts!\n"
	.string "If we obeyed you, TEAM ROCKET's\l"
	.string "rep would be ruined!$"

SlowpokeWell_B1F_Text_EtoBeaten:
	.string "Hyuck…\n"
	.string "Too strong…$"

SlowpokeWell_B1F_Text_EtoAfter:
	.string "We need the money,\n"
	.string "but selling SLOWPOKETAILS?\p"
	.string "It's tough being a ROCKET GRUNT!$"

SlowpokeWell_B1F_Text_ProtonSeen:
	.string "What do you want?\p"
	.string "If you interrupt our work,\n"
	.string "don't expect any mercy!$"

SlowpokeWell_B1F_Text_ProtonBeaten:
	.string "You did OK today,\n"
	.string "but wait till next time!$"

SlowpokeWell_B1F_Text_ProtonAfter:
	.string "Yeah, TEAM ROCKET was broken up\n"
	.string "three years ago.\p"
	.string "The boss went into hiding.\p"
	.string "But we continued our activities\n"
	.string "underground!\p"
	.string "A small obstacle like you won't be\n"
	.string "much of a problem for our mission.\p"
	.string "I advise you to be very afraid of\n"
	.string "what is to come!$"
