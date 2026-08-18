@ AspertiaSubway do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_AspertiaSubway_MapScripts::
	.byte 0

Unova_AspertiaSubway_EventScript_Npc0::
	msgbox Unova_AspertiaSubway_Text_AspertiaSubwayRideText, MSGBOX_NPC
	end

@ B6 Unova, Fase B (18/08/2026): Script_ArriveFromNimbasa@11,6 da fonte,
@ irma de Unova_NimbasaSubway (mesmo padrao). Oficial e id local 1 (Npc0).
@ VAR_TEMP_0/0 de sempre disparar. Zero flag e zero var novas.
Unova_AspertiaSubway_EventScript_Chegada::
	lock
	applymovement 1, Unova_AspertiaSubway_Movement_OficialChega
	applymovement LOCALID_PLAYER, Unova_AspertiaSubway_Movement_JogadorChega
	waitmovement 0
	applymovement 1, Unova_AspertiaSubway_Movement_OficialVolta
	waitmovement 0
	msgbox Unova_AspertiaSubway_Text_AspertiaSubwayArrivedText, MSGBOX_DEFAULT
	closemessage
	release
	end

Unova_AspertiaSubway_Movement_OficialChega::
	walk_up
	walk_up
	walk_right
	face_left
	step_end

Unova_AspertiaSubway_Movement_JogadorChega::
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_down
	face_up
	step_end

Unova_AspertiaSubway_Movement_OficialVolta::
	walk_left
	walk_down
	walk_down
	step_end

Unova_AspertiaSubway_EventScript_Npc1::
	msgbox Unova_AspertiaSubway_Text_AspertiaSubwayGrampsText, MSGBOX_NPC
	end

Unova_AspertiaSubway_EventScript_Npc2::
	msgbox Unova_AspertiaSubway_Text_AspertiaSubwayLassText, MSGBOX_NPC
	end


Unova_AspertiaSubway_Text_AspertiaSubwayRideText::
	.string "We'll soon depart"
	.string "\nfor NIMBASA."
	.string "\pAre you coming on"
	.string "\nboard?$"

Unova_AspertiaSubway_Text_AspertiaSubwayArrivedText::
	.string "We have arrived in"
	.string "\nASPERTIA."
	.string "\pWe hope to see you"
	.string "\nagain.$"

Unova_AspertiaSubway_Text_AspertiaSubwayGrampsText::
	.string "The new subway has"
	.string "\nmade it so much"
	.string "\peasier for me to"
	.string "\nget back and forth"
	.string "\pbetween home and"
	.string "\nthe big city!$"

Unova_AspertiaSubway_Text_AspertiaSubwayLassText::
	.string "Hi. Do you have a"
	.string "\nRAIL PASS? I have"
	.string "\pone. All the peo-"
	.string "\nple in ASPERTIA"
	.string "\pwho ride the sub-"
	.string "\nway have PASSES.$"
