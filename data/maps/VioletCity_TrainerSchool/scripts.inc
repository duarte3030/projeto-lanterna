VioletCity_TrainerSchool_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

VioletCity_TrainerSchool_EventScript_BlackBoard::
	lock
	msgbox VioletCity_TrainerSchool_Text_Blackboard, MSGBOX_DEFAULT
	closemessage
	release
	end

VioletCity_TrainerSchool_Text_Blackboard::
	.string "The blackboard describes\n"
	.string "POKéMON HM moves.\p"
	.string "HMs, once unlocked, don't need to\n"
	.string "be taught to be used.$"
