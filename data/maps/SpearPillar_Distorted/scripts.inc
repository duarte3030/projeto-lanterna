@ Spear Pillar distorcido: depois que o Cyrus some, a Cynthia explica o Giratina
@ e as duas fendas ficam abertas.
@ Texto de pret/pokeplatinum, res/text/spear_pillar_distorted.json.
@
@ ponytail: layout emprestado do topo limpo do Sky Pillar. Os tres tiles de fenda
@ nao existem no map.bin, entao o ON_LOAD troca o chao por metatile de escada
@ (588, o mesmo que o layout ja usa em 16,14). Enquanto o metatile nao fosse de
@ warp, os warp_def ficariam inertes, entao aqui a troca e incondicional: para
@ chegar neste mapa o jogador ja precisou vencer o Cyrus.

SpearPillar_Distorted_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SpearPillar_Distorted_OnLoad
	.byte 0

SpearPillar_Distorted_OnLoad:
	setmetatile 10, 11, 588, FALSE
	setmetatile 14, 11, 588, FALSE
	setmetatile 18, 11, 588, FALSE
	end

SpearPillar_Distorted_EventScript_Cynthia::
	lock
	faceplayer
	msgbox SpearPillar_Distorted_Text_No, MSGBOX_DEFAULT
	msgbox SpearPillar_Distorted_Text_SorryITookSoLong, MSGBOX_DEFAULT
	msgbox SpearPillar_Distorted_Text_WorldWillBeDestroyed, MSGBOX_DEFAULT
	msgbox SpearPillar_Distorted_Text_AreYouReady, MSGBOX_DEFAULT
	release
	end

SpearPillar_Distorted_EventScript_Mars::
	msgbox SpearPillar_Distorted_Text_WhereDidHeGo, MSGBOX_NPC
	end

SpearPillar_Distorted_EventScript_Jupiter::
	msgbox SpearPillar_Distorted_Text_WhatWasIt, MSGBOX_NPC
	end

SpearPillar_Distorted_EventScript_Grunt::
	msgbox SpearPillar_Distorted_Text_CanOnlyPanicAimlessly, MSGBOX_NPC
	end

SpearPillar_Distorted_Text_No:
	.string "Cynthia: No...!$"

SpearPillar_Distorted_Text_SorryITookSoLong:
	.string "Cynthia: I'm sorry I took so long.\p"
	.string "I think I finally found the answer\n"
	.string "from studying the myths.\p"
	.string "When this world was made, DIALGA\n"
	.string "and PALKIA appeared.\p"
	.string "Apparently, there was one more\n"
	.string "Pokémon that appeared at the same\l"
	.string "time.\p"
	.string "A Pokémon with as much power as\n"
	.string "DIALGA and PALKIA...\p"
	.string "But also one whose name was never\n"
	.string "to be spoken, GIRATINA!\p"
	.string "It's said to lurk in another\n"
	.string "world... A world on the opposite\l"
	.string "side of ours...\p"
	.string "That's what the shadow was.\n"
	.string "It must have been GIRATINA.$"

SpearPillar_Distorted_Text_WorldWillBeDestroyed:
	.string "The pillars are distorting...\p"
	.string "It's because of that portal.\n"
	.string "It's joined us to the other world.\p"
	.string "If it's not closed, the distortion\n"
	.string "will spread to Sinnoh and\l"
	.string "beyond...\p"
	.string "Our world will be destroyed...$"

SpearPillar_Distorted_Text_AreYouReady:
	.string "Cynthia: Are you ready?\n"
	.string "We have to chase Cyrus!$"

SpearPillar_Distorted_Text_WhereDidHeGo:
	.string "Mars: M-Master Cyrus?!\n"
	.string "Where did he go?!$"

SpearPillar_Distorted_Text_WhatWasIt:
	.string "Jupiter: That shadow...\n"
	.string "What was it...?!$"

SpearPillar_Distorted_Text_CanOnlyPanicAimlessly:
	.string "Without anyone to guide us, we can\n"
	.string "only panic aimlessly...$"
