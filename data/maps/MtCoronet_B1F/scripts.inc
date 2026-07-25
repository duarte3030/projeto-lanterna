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
