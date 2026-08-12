GoldenrodCity_DepartmentStore_4F_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

GoldenrodDeptStore4_EventScript_Sign::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_4FDirectory, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_4FDirectory::
    .string "Let Us Pump Up Your POKéMON!\p"
    .string "4F MEDICINE BOX$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

GoldenrodDeptStore4_EventScript_BugCatcher::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_4FBugCatcher, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_4FBugCatcher::
    .string "IRON adds to your POKéMON's\n"
    .string "DEFENSE.$"

GoldenrodDeptStore4_EventScript_Cooltrainer::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_4FCooltrainerM, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_4FCooltrainerM::
    .string "Hey. I love strong POKéMON.\p"
    .string "I feed them PROTEIN to crank up\n"
    .string "their ATTACK.$"

GoldenrodDeptStore4_EventScript_GBAKid::
	lock
	faceplayer
	msgbox GoldenrodDeptStore_Text_4FGameboyKid, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodDeptStore_Text_4FGameboyKid::
    .string "There were rumours that some\n"
    .string "POKéMON evolve only by\l"
    .string "being traded via a Game Link\l"
    .string "cable.\p"
    .string "Pfft...\p"
    .string "Such misinformation.\p"
    .string "I know some of the rumoured\n"
    .string "POKéMON:\l"
    .string "MACHOKE, KADABRA, HAUNTER and,\l"
    .string "um, GRAVELER,\l"
    .string "but they all evolve through\l"
    .string "level up.$"
