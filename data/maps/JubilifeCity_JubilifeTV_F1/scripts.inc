JubilifeCity_JubilifeTV_F1_MapScripts::
	.byte 0

JubilifeCity_JubilifeTV_F1_EventScript_Beauty::
	msgbox JubilifeCity_JubilifeTV_F1_Text_Beauty, MSGBOX_NPC
	end

JubilifeCity_JubilifeTV_F1_EventScript_GymGuide::
	msgbox JubilifeCity_JubilifeTV_F1_Text_GymGuide, MSGBOX_NPC
	end

JubilifeCity_JubilifeTV_F1_EventScript_President::
	lock
	faceplayer
	msgbox JubilifeCity_JubilifeTV_F1_Text_President, MSGBOX_DEFAULT
	release
	end

JubilifeCity_JubilifeTV_F1_EventScript_Lottery::
	lock
	faceplayer
	msgbox JubilifeCity_JubilifeTV_F1_Text_Lottery, MSGBOX_DEFAULT
	release
	end

JubilifeCity_JubilifeTV_F1_EventScript_AceTrainer::
	msgbox JubilifeCity_JubilifeTV_F1_Text_AceTrainer, MSGBOX_NPC
	end

JubilifeCity_JubilifeTV_F1_Text_Beauty:
	.string "JUBILIFE TV films all sorts of\n"
	.string "programs about TRAINERS.$"

JubilifeCity_JubilifeTV_F1_Text_GymGuide:
	.string "Looking for GYM info? You won't find\n"
	.string "it here, try the GYM itself!$"

JubilifeCity_JubilifeTV_F1_Text_President:
	.string "I run the POKÉTCH COMPANY next door.\n"
	.string "Always good publicity, coming here.$"

JubilifeCity_JubilifeTV_F1_Text_Lottery:
	.string "This is the POKéMON Lottery Corner.\p"
	.string "We're not drawing numbers just yet,\n"
	.string "but come back soon!$"

JubilifeCity_JubilifeTV_F1_Text_AceTrainer:
	.string "I came to watch the taping of a\n"
	.string "battle special!$"
