@ Textos vindos de pret/pokeplatinum (res/text/pastoria_city.json), em ingles.
@ Grunt_M, Rival, Crasher Wake, Croagunk e o Collector/Arrow_Signpost de
@ Route 212 South ficaram de fora: dependem de flag ou de MAP_HEADER
@ condicional, que este agente nao pode inventar.
@ OBJ_EVENT_GFX_PARASOL_LADY e OBJ_EVENT_GFX_BEAUTY nao existem em
@ event_objects.h: trocados por WOMAN_4 e WOMAN_5.

PastoriaCity_MapScripts::
	.byte 0

PastoriaCity_EventScript_BlackBelt::
	msgbox PastoriaCity_Text_BlackBelt, MSGBOX_NPC
	end

PastoriaCity_EventScript_ParasolLady::
	msgbox PastoriaCity_Text_ParasolLady, MSGBOX_NPC
	end

PastoriaCity_EventScript_Picnicker::
	msgbox PastoriaCity_Text_Picnicker, MSGBOX_NPC
	end

PastoriaCity_EventScript_AceTrainer1::
	msgbox PastoriaCity_Text_AceTrainer1, MSGBOX_NPC
	end

PastoriaCity_EventScript_Collector1::
	msgbox PastoriaCity_Text_Collector1, MSGBOX_NPC
	end

PastoriaCity_EventScript_Scientist::
	msgbox PastoriaCity_Text_Scientist, MSGBOX_NPC
	end

PastoriaCity_EventScript_Beauty::
	msgbox PastoriaCity_Text_Beauty, MSGBOX_NPC
	end

PastoriaCity_EventScript_Collector2::
	msgbox PastoriaCity_Text_Collector2, MSGBOX_NPC
	end

PastoriaCity_EventScript_AceTrainer2::
	msgbox PastoriaCity_Text_AceTrainer2, MSGBOX_NPC
	end

PastoriaCity_EventScript_GreatMarshSign::
	msgbox PastoriaCity_Text_GreatMarshSign, MSGBOX_SIGN
	end

PastoriaCity_EventScript_GymSign::
	msgbox PastoriaCity_Text_GymSign, MSGBOX_SIGN
	end

PastoriaCity_Text_BlackBelt:
	.string "PASTORIA's GYM LEADER is awesome\n"
	.string "with his water attacks. You'll\l"
	.string "know what I mean when you\l"
	.string "challenge him.$"

PastoriaCity_Text_ParasolLady:
	.string "Someone gave me a Berry, so I\n"
	.string "planted it and grew some more.\p"
	.string "Then I took the Berries and cooked\n"
	.string "them into Poffins. All the work\l"
	.string "is worth it when I see how happy\l"
	.string "they make my POKéMON!$"

PastoriaCity_Text_Picnicker:
	.string "The GREAT MARSH is just up ahead.\n"
	.string "Have you tried the Safari Game?$"

PastoriaCity_Text_AceTrainer1:
	.string "PASTORIA POKéMON are tough. The\n"
	.string "marsh air toughens them right up.$"

PastoriaCity_Text_Collector1:
	.string "I come here often looking for rare\n"
	.string "items washed up near the marsh.$"

PastoriaCity_Text_Scientist:
	.string "The GREAT MARSH has some of the\n"
	.string "rarest POKéMON in all of SINNOH.$"

PastoriaCity_Text_Beauty:
	.string "This city smells a bit like the\n"
	.string "marsh, but I've grown to like it.$"

PastoriaCity_Text_Collector2:
	.string "Keep an eye out near the water.\n"
	.string "You never know what you'll find.$"

PastoriaCity_Text_AceTrainer2:
	.string "I've battled all over PASTORIA.\n"
	.string "Care to test your skills with me?$"

PastoriaCity_Text_GreatMarshSign:
	.string "GREAT MARSH$"

PastoriaCity_Text_GymSign:
	.string "PASTORIA CITY POKéMON GYM\p"
	.string "The Water-Type Technique Style!$"
