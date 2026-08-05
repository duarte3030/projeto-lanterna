CherrygroveCity_Mart_MapScripts::
	.byte 0

CherrygroveCity_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart CherrygroveCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
CherrygroveCity_Mart_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	pokemartlistend

CherrygroveCity_Mart_EventScript_Youngster::
	lock
	faceplayer
	msgbox CherrygroveCity_Mart_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

CherrygroveCity_Mart_EventScript_BugCatcher::
	lock
	faceplayer
	msgbox CherrygroveCity_Mart_Text_BugCatcher, MSGBOX_DEFAULT
	closemessage
	release
	end

CherrygroveCity_Mart_Text_Youngster:
	.string "When I was walking in the grass, a\n"
	.string "bug POKéMON poisoned my POKéMON!\p"
	.string "I just kept going, but then my\n"
	.string "POKéMON fainted.\p"
	.string "You should keep an ANTIDOTE\n"
	.string "with you.$"

CherrygroveCity_Mart_Text_BugCatcher:
	.string "POKé BALLS are in stock!\n"
	.string "Now I can catch POKéMON!$"
