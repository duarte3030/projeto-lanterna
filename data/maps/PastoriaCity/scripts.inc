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

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

PastoriaCity_EventScript_Placa2::
	msgbox PastoriaCity_Text_Placa2, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa2:
	.string "Pastoria City Pokémon Gym\nLeader: Crasher Wake\pThe Torrential Masked Master!$"

PastoriaCity_EventScript_Placa3::
	msgbox PastoriaCity_Text_Placa3, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa3:
	.string "Pastoria Great Marsh\nObservatory Gate$"

PastoriaCity_EventScript_Placa4::
	msgbox PastoriaCity_Text_Placa4, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa4:
	.string "Try the Safari Game in\nPastoria's Great Marsh!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCity_EventScript_Npc1::
	msgbox PastoriaCity_Text_Npc1, MSGBOX_NPC
	end

PastoriaCity_Text_Npc1:
	.string "Some Trainers deliberately prevent\ntheir Pokémon from evolving.\pThey wait until the Pokémon levels up\nand learns certain moves.$"

PastoriaCity_EventScript_Npc2::
	msgbox PastoriaCity_Text_Npc2, MSGBOX_NPC
	end

PastoriaCity_Text_Npc2:
	.string "Pastoria's Gym Leader is awesome with\nhis water attacks.\pYou'll know what I mean when you\nchallenge him.$"

PastoriaCity_EventScript_Npc3::
	msgbox PastoriaCity_Text_Npc3, MSGBOX_NPC
	end

PastoriaCity_Text_Npc3:
	.string "CLEFAIRY: Fiiih?!$"

PastoriaCity_EventScript_Npc4::
	msgbox PastoriaCity_Text_Npc4, MSGBOX_NPC
	end

PastoriaCity_Text_Npc4:
	.string "The Great Marsh keeps the weather\ncool in the summertime.\pThis is a good town for Water-type\nPokémon.$"

PastoriaCity_EventScript_Npc5::
	msgbox PastoriaCity_Text_Npc5, MSGBOX_NPC
	end

PastoriaCity_Text_Npc5:
	.string "Here where I am standing, I'm\nsmack-dab in the middle of town.$"

PastoriaCity_EventScript_Npc6::
	msgbox PastoriaCity_Text_Npc6, MSGBOX_NPC
	end

PastoriaCity_Text_Npc6:
	.string "I study rare Pokémon that appear\nonly in the Great Marsh.$"

PastoriaCity_EventScript_Npc7::
	msgbox PastoriaCity_Text_Npc7, MSGBOX_NPC
	end

PastoriaCity_Text_Npc7:
	.string "I'm visiting here to see the Great\nMarsh.\pI'm staying at the lakeside hotel.$"

PastoriaCity_EventScript_Npc8::
	msgbox PastoriaCity_Text_Npc8, MSGBOX_NPC
	end

PastoriaCity_Text_Npc8:
	.string "I can't use the hidden move Surf until\nI beat the local Gym Leader.$"

PastoriaCity_EventScript_Npc9::
	msgbox PastoriaCity_Text_Npc9, MSGBOX_NPC
	end

PastoriaCity_Text_Npc9:
	.string "Have you been to the Pokémon Mansion?\nIt's on Route 212.\pThe owner, Mr. Backlot, likes to brag\nabout his herd of rare Pokémon.$"

PastoriaCity_EventScript_Placa10::
	msgbox PastoriaCity_Text_Placa10, MSGBOX_SIGN
	end

PastoriaCity_Text_Placa10:
	.string "Pastoria City\nThe Marsh City$"
