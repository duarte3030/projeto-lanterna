NationalPark_BugContest_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

NationalParkBugContest_Text_Sign_BattleNotice::
	.string "What is this notice?\p"
	.string "Please battle only in the grass.\p"
	.string "NATIONAL PARK WARDEN'S OFFICE$"

NationalParkBugContest_Text_Sign_RelaxationSquare::
	.string "RELAXATION SQUARE\n"
	.string "NATIONAL PARK$"

NationalParkBugContest_Text_TrainerTips::
	.string "The NATIONAL PARK has different\n"
	.string "POKéMON during the BUG-CATCHING\l"
	.string "CONTEST.$"

NationalPark_BugContest_EventScript_BattleSign::
	lock
	msgbox NationalParkBugContest_Text_Sign_BattleNotice, MSGBOX_SIGN
	closemessage
	release
	end

NationalPark_BugContest_EventScript_RelaxationSquare::
	lock
	msgbox NationalParkBugContest_Text_Sign_RelaxationSquare, MSGBOX_SIGN
	closemessage
	release
	end

NationalPark_BugContest_EventScript_TrainerTips::
	lock
	msgbox NationalParkBugContest_Text_TrainerTips, MSGBOX_SIGN
	closemessage
	release
	end

NationalPark_BugContest_EventScript_Trash::
	lock
	msgbox NationalPark_BugContest_Text_Trash, MSGBOX_SIGN
	closemessage
	release
	end

NationalPark_BugContest_Text_Trash::
	.string "Nothing here.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

NationalParkBugContest_Text_Contestant2A::
	.string "ED: My PARASECT puts POKéMON to\n"
	.string "sleep with SPORE.$"

NationalPark_BugContest_EventScript_BC2::
	lock
	faceplayer
	msgbox NationalParkBugContest_Text_Contestant2A, MSGBOX_DEFAULT
	closemessage
	release
	end

NationalParkBugContest_Text_ContestantShaun::
	.string "SHAUN: I'm not concerned about\n"
	.string "winning.\p"
	.string "I'm just looking for rare POKéMON.$"

NationalPark_BugContest_EventScript_BC1::
	lock
	faceplayer
	msgbox NationalParkBugContest_Text_ContestantShaun, MSGBOX_DEFAULT
	closemessage
	release
	end

NationalParkBugContest_Text_Contestant6A::
	.string "BARRY: You should weaken bug\n"
	.string "POKéMON first,\p"
	.string "then throw a BALL.$"

NationalPark_BugContest_EventScript_Boy::
	lock
	faceplayer
	msgbox NationalParkBugContest_Text_Contestant6A, MSGBOX_DEFAULT
	closemessage
	release
	end

NationalParkBugContest_Text_ContestantBelinda::
	.string "BELINDA: I'm going to win!\n"
	.string "Don't bother me.$"

NationalPark_BugContest_EventScript_Belinda::
	lock
	faceplayer
	msgbox NationalParkBugContest_Text_ContestantBelinda, MSGBOX_DEFAULT
	closemessage
	release
	end
