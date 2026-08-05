MtCoronet_1F_South_MapScripts::
	.byte 0

MtCoronet_1F_South_EventScript_Hiker1::
	msgbox MtCoronet_1F_South_Text_Hiker1, MSGBOX_NPC
	end

MtCoronet_1F_South_EventScript_BlackBelt::
	msgbox MtCoronet_1F_South_Text_BlackBelt, MSGBOX_NPC
	end

MtCoronet_1F_South_EventScript_Hiker2::
	msgbox MtCoronet_1F_South_Text_Hiker2, MSGBOX_NPC
	end

MtCoronet_1F_South_Text_Hiker1:
	.string "MOUNT CORONET splits SINNOH right\n"
	.string "down the middle.\p"
	.string "Quite a climb, isn't it?$"

MtCoronet_1F_South_Text_BlackBelt:
	.string "Training on a mountain like this\n"
	.string "toughens you up fast.$"

MtCoronet_1F_South_Text_Hiker2:
	.string "Watch for loose rocks.\p"
	.string "This place doesn't forgive a\n"
	.string "careless step.$"

@ Historia: a Galactica dentro do Mt. Coronet, e o monologo de Cyrus.
@ Texto de pret/pokeplatinum, res/text/mt_coronet_1f_south.json e
@ mt_coronet_1f_tunnel_room.json. Cyrus so fala: a batalha dele fica em
@ galactic_hq/spear_pillar, mapas que este hack ainda nao tem.

MtCoronet_1F_South_EventScript_GalacticGrunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_TUNNEL_ROOM_1, MtCoronet_1F_South_Text_Grunt1Intro, MtCoronet_1F_South_Text_Grunt1Defeat
	msgbox MtCoronet_1F_South_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

MtCoronet_1F_South_EventScript_GalacticGrunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_TUNNEL_ROOM_2, MtCoronet_1F_South_Text_Grunt2Intro, MtCoronet_1F_South_Text_Grunt2Defeat
	msgbox MtCoronet_1F_South_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

MtCoronet_1F_South_EventScript_Cyrus::
	lock
	faceplayer
	msgbox MtCoronet_1F_South_Text_Cyrus, MSGBOX_DEFAULT
	release
	end

MtCoronet_1F_South_Text_Grunt1Intro:
	.string "Mt. Coronet is off limits to\n"
	.string "anyone but Team Galactic!$"

MtCoronet_1F_South_Text_Grunt1Defeat:
	.string "You're absolutely right!\n"
	.string "I'm hopelessly lost!$"

MtCoronet_1F_South_Text_Grunt1PostBattle:
	.string "Please don't pay attention to a\n"
	.string "lowly grunt like me...$"

MtCoronet_1F_South_Text_Grunt2Intro:
	.string "According to one theory, Mt.\n"
	.string "Coronet is where the Sinnoh region\l"
	.string "began.\p"
	.string "That is why we are here.\n"
	.string "And why you must leave!$"

MtCoronet_1F_South_Text_Grunt2Defeat:
	.string "Everything is for everyone, and\n"
	.string "for the good of Team Galactic...$"

MtCoronet_1F_South_Text_Grunt2PostBattle:
	.string "Our boss climbs this mountain\n"
	.string "again and again.\p"
	.string "I have no idea what he sees here.$"

MtCoronet_1F_South_Text_Cyrus:
	.string "...In a newly created world...\p"
	.string "A world where only time flowed and\n"
	.string "space expanded...\l"
	.string "There should have been no strife.\p"
	.string "But what became of that world?\p"
	.string "Because the human spirit is weak\n"
	.string "and incomplete, strife has\l"
	.string "spread...\p"
	.string "This world is being ruined by it...\p"
	.string "I find this state of affairs to be\n"
	.string "deplorable...$"
