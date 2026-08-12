AzaleaTown_KurtsHouse_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

AzaleaTown_KurtsHouse_EventScript_CelebiStatue::
	msgbox KurtsHouse_Text_CelebiStatue, MSGBOX_SIGN
	closemessage
	end

AzaleaTown_KurtsHouse_EventScript_OakPhoto::
	msgbox KurtsHouse_Text_OakPhoto, MSGBOX_SIGN
	closemessage
	end

KurtsHouse_Text_CelebiStatue::
	.string "It's a statue of the forest's\n"
	.string "protector.$"

KurtsHouse_Text_OakPhoto::
	.string "…A young PROF. OAK?$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

KurtsHouse_Text_KurtMakingBallsMustWait::
	.string "Hm? Who are you?\p"
	.string "{PLAYER}, eh? You want me to make\n"
	.string "some BALLS?\p"
	.string "Sorry, but that'll have to wait.\p"
	.string "Do you know TEAM ROCKET?\n"
	.string "Ah, don't worry.\p"
	.string "I'll tell you anyhow.\p"
	.string "TEAM ROCKET's an evil gang that\n"
	.string "uses POKéMON for their dirty work.\p"
	.string "They're supposed to have disbanded\n"
	.string "three years ago.\p"
	.string "Anyway, they're at the WELL,\n"
	.string "cutting off SLOWPOKETAILS to sell!\p"
	.string "So I'm going to go give them a\n"
	.string "lesson in pain!\p"
	.string "Hang on, SLOWPOKE! Old KURT\n"
	.string "is on his way!$"

AzaleaTown_KurtsHouse_EventScript_KurtBeforeFala::
	msgbox KurtsHouse_Text_KurtMakingBallsMustWait, MSGBOX_NPC
	end
