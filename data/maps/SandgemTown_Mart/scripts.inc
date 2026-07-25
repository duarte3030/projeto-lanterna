SandgemTown_Mart_MapScripts::
	.byte 0

SandgemTown_Mart_EventScript_Clerk::
	lock
	faceplayer
	msgbox SandgemTown_Mart_Text_Clerk, MSGBOX_DEFAULT
	release
	end

SandgemTown_Mart_EventScript_SchoolKid::
	msgbox SandgemTown_Mart_Text_SchoolKid, MSGBOX_NPC
	end

SandgemTown_Mart_EventScript_Breeder::
	msgbox SandgemTown_Mart_Text_Breeder, MSGBOX_NPC
	end

SandgemTown_Mart_Text_Clerk:
	.string "Welcome to the SANDGEM TOWN MART!\p"
	.string "Take a look at our selection whenever\n"
	.string "you're ready.$"

SandgemTown_Mart_Text_SchoolKid:
	.string "I'm saving up my allowance for a new\n"
	.string "POKé BALL.$"

SandgemTown_Mart_Text_Breeder:
	.string "Stocking up on supplies before I head\n"
	.string "back out to the ROUTES.$"
