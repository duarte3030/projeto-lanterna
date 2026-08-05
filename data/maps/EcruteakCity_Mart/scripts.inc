EcruteakCity_Mart_MapScripts::
	.byte 0

EcruteakCity_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart EcruteakCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
EcruteakCity_Mart_Pokemart:
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_REPEL
	pokemartlistend

EcruteakCity_Mart_EventScript_Granny::
	lock
	faceplayer
	msgbox EcruteakCity_Mart_Text_Granny, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Mart_EventScript_Nerd::
	lock
	faceplayer
	msgbox EcruteakCity_Mart_Text_Nerd, MSGBOX_DEFAULT
	closemessage
	release
	end

EcruteakCity_Mart_Text_Granny:
	.string "If you use REVIVE, a POKéMON that's\n"
	.string "fainted will wake right up.$"

EcruteakCity_Mart_Text_Nerd:
	.string "My EEVEE evolved into an ESPEON.\p"
	.string "But my friend's EEVEE turned into\n"
	.string "an UMBREON.\p"
	.string "I wonder why? We both were raising\n"
	.string "our EEVEE in the same way…$"
