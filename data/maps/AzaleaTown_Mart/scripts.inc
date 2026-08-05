AzaleaTown_Mart_MapScripts::
	.byte 0

AzaleaTown_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart AzaleaTown_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
AzaleaTown_Mart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_REPEL
	pokemartlistend

AzaleaTown_Mart_EventScript_BugCatcher::
	lock
	faceplayer
	msgbox AzaleaTown_Mart_Text_BugCatcher, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_Mart_EventScript_Trainer::
	lock
	faceplayer
	msgbox AzaleaTown_Mart_Text_Trainer, MSGBOX_DEFAULT
	closemessage
	release
	end

AzaleaTown_Mart_Text_BugCatcher:
	.string "A GREAT BALL is better for catch-\n"
	.string "ing POKéMON than a POKé BALL.\p"
	.string "But KURT's might be better some-\n"
	.string "times.$"

AzaleaTown_Mart_Text_Trainer:
	.string "Are you able to buy a GREAT BALL?\n"
	.string "All I can buy are POKé BALLS.\p"
	.string "I heard that more items become\n"
	.string "available to buy when you earn\l"
	.string "GYM BADGES!\p"
	.string "I wish KURT would make me some\n"
	.string "of his custom BALLS.$"
