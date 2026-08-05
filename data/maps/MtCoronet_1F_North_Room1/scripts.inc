MtCoronet_1F_North_Room1_MapScripts::
	.byte 0

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
