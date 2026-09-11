@ Labirinto de canos do esgoto de Goldenrod, copiado do mapa `g10m2` do Pokémon
@ GS Chronicles. A arte é do autor, byte a byte, inclusive os oito bueiros que
@ voltam para o próprio mapa; o jogo é nosso.
GoldenrodCity_SewersPipes_MapScripts::
	.byte 0

GoldenrodCity_SewersPipes_EventScript_Klaus::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_3, GoldenrodCity_SewersPipes_Text_KlausSeen, GoldenrodCity_SewersPipes_Text_KlausBeaten
	msgbox GoldenrodCity_SewersPipes_Text_KlausAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_SewersPipes_EventScript_Marnie::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_4, GoldenrodCity_SewersPipes_Text_MarnieSeen, GoldenrodCity_SewersPipes_Text_MarnieBeaten
	msgbox GoldenrodCity_SewersPipes_Text_MarnieAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_SewersPipes_EventScript_Hugh::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_5, GoldenrodCity_SewersPipes_Text_HughSeen, GoldenrodCity_SewersPipes_Text_HughBeaten
	msgbox GoldenrodCity_SewersPipes_Text_HughAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_SewersPipes_EventScript_Dagmar::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_6, GoldenrodCity_SewersPipes_Text_DagmarSeen, GoldenrodCity_SewersPipes_Text_DagmarBeaten
	msgbox GoldenrodCity_SewersPipes_Text_DagmarAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_SewersPipes_EventScript_Rufus::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_7, GoldenrodCity_SewersPipes_Text_RufusSeen, GoldenrodCity_SewersPipes_Text_RufusBeaten
	msgbox GoldenrodCity_SewersPipes_Text_RufusAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_SewersPipes_EventScript_Thomas::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_8, GoldenrodCity_SewersPipes_Text_ThomasSeen, GoldenrodCity_SewersPipes_Text_ThomasBeaten
	msgbox GoldenrodCity_SewersPipes_Text_ThomasAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_SewersPipes_EventScript_Yuki::
	trainerbattle_single TRAINER_JOHTO_ESGOTO_GOLDENROD_9, GoldenrodCity_SewersPipes_Text_YukiSeen, GoldenrodCity_SewersPipes_Text_YukiBeaten
	msgbox GoldenrodCity_SewersPipes_Text_YukiAfter, MSGBOX_AUTOCLOSE
	end

GoldenrodCity_SewersPipes_EventScript_LostMan::
	lock
	faceplayer
	msgbox GoldenrodCity_SewersPipes_Text_LostMan, MSGBOX_DEFAULT
	closemessage
	release
	end

GoldenrodCity_SewersPipes_Text_KlausSeen:
	.string "Eight manholes, five islands.\p"
	.string "I mapped it in one afternoon.\n"
	.string "Beat me and I'll tell you nothing.$"

GoldenrodCity_SewersPipes_Text_KlausBeaten:
	.string "My map was right! I was wrong!$"

GoldenrodCity_SewersPipes_Text_KlausAfter:
	.string "Every manhole has exactly one twin.\p"
	.string "Take the wrong one and you go back\n"
	.string "where you came from.$"

GoldenrodCity_SewersPipes_Text_MarnieSeen:
	.string "I come down here so nobody watches\n"
	.string "me train. Well. Nobody did.$"

GoldenrodCity_SewersPipes_Text_MarnieBeaten:
	.string "Now I have an audience AND a loss.$"

GoldenrodCity_SewersPipes_Text_MarnieAfter:
	.string "The pipes carry sound strangely.\p"
	.string "Sometimes I hear the department\n"
	.string "store music down here.$"

GoldenrodCity_SewersPipes_Text_HughSeen:
	.string "You want the rare stuff, you dig\n"
	.string "where nobody digs.$"

GoldenrodCity_SewersPipes_Text_HughBeaten:
	.string "Dug too deep this time.$"

GoldenrodCity_SewersPipes_Text_HughAfter:
	.string "There is something buried on the\n"
	.string "last island. I never got that far.$"

GoldenrodCity_SewersPipes_Text_DagmarSeen:
	.string "Don't look at me like that.\p"
	.string "The air down here is wonderful for\n"
	.string "GRASS POKéMON.$"

GoldenrodCity_SewersPipes_Text_DagmarBeaten:
	.string "It's the humidity. It has to be.$"

GoldenrodCity_SewersPipes_Text_DagmarAfter:
	.string "Warm, wet and nobody trampling the\n"
	.string "beds. I'd move in if I could.$"

GoldenrodCity_SewersPipes_Text_RufusSeen:
	.string "I've climbed mountains taller than\n"
	.string "this city.\p"
	.string "Turns out going down is harder.$"

GoldenrodCity_SewersPipes_Text_RufusBeaten:
	.string "Rock beats water. Usually.$"

GoldenrodCity_SewersPipes_Text_RufusAfter:
	.string "These walkways sit on pillars sunk\n"
	.string "into bedrock.\p"
	.string "Whoever built GOLDENROD built it\n"
	.string "twice: once up, once down.$"

GoldenrodCity_SewersPipes_Text_ThomasSeen:
	.string "Spent twenty years at sea and ended\n"
	.string "up guarding a drain.$"

GoldenrodCity_SewersPipes_Text_ThomasBeaten:
	.string "Even the drain beats me today.$"

GoldenrodCity_SewersPipes_Text_ThomasAfter:
	.string "Water always finds the way out.\n"
	.string "Follow it and so will you.$"

GoldenrodCity_SewersPipes_Text_YukiSeen:
	.string "I hear thoughts down here that\n"
	.string "nobody up there is thinking.$"

GoldenrodCity_SewersPipes_Text_YukiBeaten:
	.string "I did not foresee that.$"

GoldenrodCity_SewersPipes_Text_YukiAfter:
	.string "Two more manholes and you reach the\n"
	.string "last island.\p"
	.string "Somebody is waiting there, and he\n"
	.string "has been waiting a long time.$"

GoldenrodCity_SewersPipes_Text_LostMan:
	.string "I took the wrong manhole four days\n"
	.string "ago and I've been going in circles.\p"
	.string "Wait. You came in from the east?\n"
	.string "Then east is the way out!\p"
	.string "…I am not going east.\n"
	.string "I like it here now.$"
