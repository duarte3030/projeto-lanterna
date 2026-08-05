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
