BlackthornCity_Mart_MapScripts::
	.byte 0

BlackthornCity_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart BlackthornCity_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
BlackthornCity_Mart_Pokemart:
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_REVIVE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_MAX_REPEL
	pokemartlistend

BlackthornCity_Mart_EventScript_BlackBelt::
	msgbox BlackthornCity_Mart_Text_BlackBelt, MSGBOX_NPC
	end

BlackthornCity_Mart_EventScript_Trainer::
	msgbox BlackthornCity_Mart_Text_Trainer, MSGBOX_NPC
	end

BlackthornCity_Mart_Text_BlackBelt:
	.string "MAX REPEL keeps weak POKéMON away\n"
	.string "from you.\p"
	.string "It's the longest lasting of the\n"
	.string "REPEL sprays.$"

BlackthornCity_Mart_Text_Trainer:
	.string "You can't buy MAX REVIVE, but it\n"
	.string "fully restores a fainted POKéMON.\p"
	.string "Beware--it won't restore PP, the\n"
	.string "POWER POINTS needed for moves.$"
