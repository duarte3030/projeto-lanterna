PokmonLeague_MapScripts::
	.byte 0

PokmonLeague_EventScript_Youngster::
	msgbox PokmonLeague_Text_Youngster, MSGBOX_NPC
	end

PokmonLeague_EventScript_Staff::
	msgbox PokmonLeague_Text_Staff, MSGBOX_NPC
	end

PokmonLeague_EventScript_Gentleman::
	msgbox PokmonLeague_Text_Gentleman, MSGBOX_NPC
	end

PokmonLeague_Text_Youngster:
	.string "The CHAMPION's up there...\p"
	.string "I don't know if I'm ready.$"

PokmonLeague_Text_Staff:
	.string "Challengers line up over there.\p"
	.string "Good luck on the ELITE FOUR.$"

PokmonLeague_Text_Gentleman:
	.string "Every step past this gate belongs\n"
	.string "to Trainers strong enough to take\n"
	.string "on SINNOH's best.$"
