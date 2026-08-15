MtCoronet_1F_North_Room1_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtCoronet_1F_North_Room1_OnTransition
	.byte 0

@ ponytail: a cena e a flag sao a mesma coisa. Estes objetos nascem enquanto
@ derrotar o Cyrus no Spear Pillar nao aconteceu, e somem depois; o motor ja
@ grava a flag de derrotado do gatilho, e este ON_TRANSITION so a traduz. Zero
@ var. Mesma flag que os outros andares do Mt. Coronet ja usam.
MtCoronet_1F_North_Room1_OnTransition:
	call_if_defeated TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_SPEAR_PILLAR, MtCoronet_1F_North_Room1_EventScript_HideGalactica_mt_coronet
	end

MtCoronet_1F_North_Room1_EventScript_HideGalactica_mt_coronet::
	setflag FLAG_GALACTICA_MT_CORONET
	return

MtCoronet_1F_North_Room1_EventScript_Hiker1::
	msgbox MtCoronet_1F_North_Room1_Text_Hiker1, MSGBOX_NPC
	end

MtCoronet_1F_North_Room1_EventScript_Hiker2::
	msgbox MtCoronet_1F_North_Room1_Text_Hiker2, MSGBOX_NPC
	end

MtCoronet_1F_North_Room1_Text_Hiker1:
	.string "Strange, the fog rolls in thick\n"
	.string "around here.\p"
	.string "Never seen anything like it.$"

MtCoronet_1F_North_Room1_Text_Hiker2:
	.string "I got turned around in here\n"
	.string "earlier.\p"
	.string "Glad to see another face.$"

@ Historia: os dois grunts perdidos na neblina.
@ Texto de pret/pokeplatinum, res/text/mt_coronet_1f_north_room_1.json. So
@ conversa, como no original.

MtCoronet_1F_North_Room1_EventScript_GalacticGrunt1::
	msgbox MtCoronet_1F_North_Room1_Text_GalacticGrunt1, MSGBOX_NPC
	end

MtCoronet_1F_North_Room1_EventScript_GalacticGrunt2::
	msgbox MtCoronet_1F_North_Room1_Text_GalacticGrunt2, MSGBOX_NPC
	end

MtCoronet_1F_North_Room1_Text_GalacticGrunt1:
	.string "The fog is so thick ahead I can't\n"
	.string "even see my own hand!\p"
	.string "Can you use Defog so we can see?$"

MtCoronet_1F_North_Room1_Text_GalacticGrunt2:
	.string "Hah? The Pokémon they gave me\n"
	.string "can't use Defog, either.\p"
	.string "I think we're stuck.\n"
	.string "Let's wait till the others get here.$"

@ Grunt mudo de pret/pokeplatinum (LOCALID_GRUNT_F, hidden_flag
@ FLAG_HIDE_MT_CORONET_1F_NORTH_ROOM_1_GRUNT_F).
MtCoronet_1F_North_Room1_EventScript_GalacticGruntF::
	msgbox MtCoronet_1F_North_Room1_Text_GalacticGruntF, MSGBOX_NPC
	end

MtCoronet_1F_North_Room1_Text_GalacticGruntF:
	.string "There's no way of getting to the\n"
	.string "peak of Mt. Coronet from this side!\p"
	.string "Uh-oh... Was I supposed to go up\n"
	.string "from the Oreburgh City side?\p"
	.string "Maybe I wasn't supposed to climb\n"
	.string "from the Eterna City side?\p"
	.string "Oh, didn't I need hidden moves\n"
	.string "like Surf, too?$"
