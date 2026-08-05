@ Treinadores de rota de GoldenrodCity_UndergroundSwitches, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

GoldenrodCity_UndergroundSwitches_MapScripts::
	.byte 0

GoldenrodCity_UndergroundSwitches_EventScript_Grunt10::
	trainerbattle_single TRAINER_JOHTO_GRUNT_10, GoldenrodCity_UndergroundSwitches_Text_Grunt10Seen, GoldenrodCity_UndergroundSwitches_Text_Grunt10Beaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_Grunt10After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Grunt20::
	trainerbattle_single TRAINER_JOHTO_GRUNT_20, GoldenrodCity_UndergroundSwitches_Text_Grunt20Seen, GoldenrodCity_UndergroundSwitches_Text_Grunt20Beaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_Grunt20After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Duncan::
	trainerbattle_single TRAINER_JOHTO_DUNCAN, GoldenrodCity_UndergroundSwitches_Text_DuncanSeen, GoldenrodCity_UndergroundSwitches_Text_DuncanBeaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_DuncanAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Eddie::
	trainerbattle_single TRAINER_JOHTO_EDDIE, GoldenrodCity_UndergroundSwitches_Text_EddieSeen, GoldenrodCity_UndergroundSwitches_Text_EddieBeaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_EddieAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Grunt11::
	trainerbattle_single TRAINER_JOHTO_GRUNT_11, GoldenrodCity_UndergroundSwitches_Text_Grunt11Seen, GoldenrodCity_UndergroundSwitches_Text_Grunt11Beaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_Grunt11After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_EventScript_Grunt27::
	trainerbattle_single TRAINER_JOHTO_GRUNT_27, GoldenrodCity_UndergroundSwitches_Text_Grunt27Seen, GoldenrodCity_UndergroundSwitches_Text_Grunt27Beaten
	msgbox GoldenrodCity_UndergroundSwitches_Text_Grunt27After, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_UndergroundSwitches_Text_Grunt10Seen:
	.string "Open one shutter, another closes.\p"
	.string "Bet you can't get where you want!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt10Beaten:
	.string "Drat! I was sunk by indecision!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt10After:
	.string "I'm confused too… The switch on the\n"
	.string "end is the one to press first, but…$"

GoldenrodCity_UndergroundSwitches_Text_Grunt20Seen:
	.string "Kwahaha!\p"
	.string "Confounded by the shutters, are we?\p"
	.string "I'll let you in on a secret if you\n"
	.string "can beat me!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt20Beaten:
	.string "Uwww… I blew it.$"

GoldenrodCity_UndergroundSwitches_Text_Grunt20After:
	.string "All right. A hint!\p"
	.string "Change the order of switching.\p"
	.string "That'll change the ways the shutters\n"
	.string "open and close.$"

GoldenrodCity_UndergroundSwitches_Text_DuncanSeen:
	.string "Fork over your goodies!$"

GoldenrodCity_UndergroundSwitches_Text_DuncanBeaten:
	.string "Mercy!$"

GoldenrodCity_UndergroundSwitches_Text_DuncanAfter:
	.string "Steal and sell! That's basic in\n"
	.string "crime, kid!$"

GoldenrodCity_UndergroundSwitches_Text_EddieSeen:
	.string "They ditched this project before they\n"
	.string "finished.\p"
	.string "I'm searching for leftover loot.$"

GoldenrodCity_UndergroundSwitches_Text_EddieBeaten:
	.string "Over the top!$"

GoldenrodCity_UndergroundSwitches_Text_EddieAfter:
	.string "UNDERGROUND WAREHOUSE?\p"
	.string "What do you want to go there for?\p"
	.string "There's nothing down there.$"

GoldenrodCity_UndergroundSwitches_Text_Grunt11Seen:
	.string "I don't care if you're lost.\p"
	.string "You show up here, you're nothing but\n"
	.string "a victim!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt11Beaten:
	.string "Urk! Yeah, think you're cool, huh?$"

GoldenrodCity_UndergroundSwitches_Text_Grunt11After:
	.string "You must have ice in your veins to\n"
	.string "dis TEAM ROCKET.$"

GoldenrodCity_UndergroundSwitches_Text_Grunt27Seen:
	.string "Are you lost? No, you can't be.\p"
	.string "You don't have that scared look.\p"
	.string "I'll give you something to be\n"
	.string "scared about!$"

GoldenrodCity_UndergroundSwitches_Text_Grunt27Beaten:
	.string "How could you?$"

GoldenrodCity_UndergroundSwitches_Text_Grunt27After:
	.string "Go wherever you'd like! Get lost!\n"
	.string "See if I care!$"
