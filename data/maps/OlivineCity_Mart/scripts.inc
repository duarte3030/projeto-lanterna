OlivineCity_Mart_MapScripts::
	.byte 0

OlivineCity_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart OlivineCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
OlivineCity_Mart_Pokemart:
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_REPEL
	pokemartlistend

OlivineCity_Mart_EventScript_Trainer::
	lock
	faceplayer
	msgbox OlivineCity_Mart_Text_Trainer, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_Mart_EventScript_Lass::
	lock
	faceplayer
	msgbox OlivineCity_Mart_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

OlivineCity_Mart_Text_Trainer:
	.string "Do your POKéMON already know\n"
	.string "the move for carrying people\l"
	.string "across water?$"

OlivineCity_Mart_Text_Lass:
	.string "My BUTTERFREE came from my\n"
	.string "boyfriend overseas.\p"
	.string "It carried some MAIL from him.\p"
	.string "Want to know what it says?\p"
	.string "Let's see… Nope! It's a\n"
	.string "secret!$"
