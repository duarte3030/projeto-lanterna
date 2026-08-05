MtCoronet_B1F_MapScripts::
	.byte 0

MtCoronet_B1F_EventScript_Hiker1::
	msgbox MtCoronet_B1F_Text_Hiker1, MSGBOX_NPC
	end

MtCoronet_B1F_EventScript_Hiker2::
	msgbox MtCoronet_B1F_Text_Hiker2, MSGBOX_NPC
	end

MtCoronet_B1F_Text_Hiker1:
	.string "This mountain runs deep.\p"
	.string "I've heard there are passages\n"
	.string "nobody's mapped yet.$"

MtCoronet_B1F_Text_Hiker2:
	.string "The lake down here stays cold\n"
	.string "year-round.\p"
	.string "Wouldn't recommend a swim.$"

@ Historia: mais um posto da Galactica no caminho para o norte.
@ Texto de pret/pokeplatinum, res/text/mt_coronet_1f_tunnel_room.json.

MtCoronet_B1F_EventScript_GalacticGrunt::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_TUNNEL_ROOM_3, MtCoronet_B1F_Text_GruntIntro, MtCoronet_B1F_Text_GruntDefeat
	msgbox MtCoronet_B1F_Text_GruntPostBattle, MSGBOX_AUTOCLOSE
	end

MtCoronet_B1F_Text_GruntIntro:
	.string "Turn back. Team Galactic is using\n"
	.string "this tunnel.$"

MtCoronet_B1F_Text_GruntDefeat:
	.string "Yeah, right!\n"
	.string "You're absolutely right!$"

MtCoronet_B1F_Text_GruntPostBattle:
	.string "The others went on ahead, up to\n"
	.string "the peak.\p"
	.string "I'm just a lowly grunt.\n"
	.string "Nobody tells me anything.$"
