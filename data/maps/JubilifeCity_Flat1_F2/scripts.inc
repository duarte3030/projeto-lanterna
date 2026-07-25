JubilifeCity_Flat1_F2_MapScripts::
	.byte 0

JubilifeCity_Flat1_F2_EventScript_BugCatcher::
	msgbox JubilifeCity_Flat1_F2_Text_BugCatcher, MSGBOX_NPC
	end

JubilifeCity_Flat1_F2_EventScript_BreederM::
	msgbox JubilifeCity_Flat1_F2_Text_BreederM, MSGBOX_NPC
	end

JubilifeCity_Flat1_F2_Text_BugCatcher:
	.string "I caught three KRICKETOT today!\p"
	.string "This building's garden is a\n"
	.string "bug-catching paradise.$"

JubilifeCity_Flat1_F2_Text_BreederM:
	.string "Raising POKéMON in an apartment\n"
	.string "isn't easy, but mine don't seem\l"
	.string "to mind.$"
