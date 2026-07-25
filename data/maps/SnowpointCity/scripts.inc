@ Textos vindos de pret/pokeplatinum (res/text/snowpoint_city.json), em ingles.
@ Candice, o Sailor do SS SPIRAL e Cynthia ficaram de fora: dependem de flag
@ de historia (FLAG_HIDE_SNOWPOINT_CITY_*), que este agente nao pode inventar.
@ O Temple_Guard usa so a fala geral sobre o templo (as falas sobre deixar
@ o jogador entrar dependem da Candice, que esta fora do escopo).
@ OBJ_EVENT_GFX_ACE_TRAINER_SNOW_F e OBJ_EVENT_GFX_SNOWPOINT_NPC_M/F nao
@ existem em event_objects.h: trocados por COOLTRAINER_F, MAN_2 e WOMAN_2.

SnowpointCity_MapScripts::
	.byte 0

SnowpointCity_EventScript_AceTrainer::
	msgbox SnowpointCity_Text_AceTrainer, MSGBOX_NPC
	end

SnowpointCity_EventScript_NpcM::
	msgbox SnowpointCity_Text_NpcM, MSGBOX_NPC
	end

SnowpointCity_EventScript_NpcF1::
	msgbox SnowpointCity_Text_NpcF1, MSGBOX_NPC
	end

SnowpointCity_EventScript_Sailor::
	msgbox SnowpointCity_Text_Sailor, MSGBOX_NPC
	end

SnowpointCity_EventScript_TempleGuard::
	msgbox SnowpointCity_Text_TempleGuard, MSGBOX_NPC
	end

SnowpointCity_EventScript_NpcF2::
	msgbox SnowpointCity_Text_NpcF2, MSGBOX_NPC
	end

SnowpointCity_EventScript_GymSign::
	msgbox SnowpointCity_Text_GymSign, MSGBOX_SIGN
	end

SnowpointCity_EventScript_TempleSign::
	msgbox SnowpointCity_Text_TempleSign, MSGBOX_SIGN
	end

SnowpointCity_Text_AceTrainer:
	.string "SNOWPOINT is the northernmost city\n"
	.string "in SINNOH. It's cold, but I like\l"
	.string "it that way.$"

SnowpointCity_Text_NpcM:
	.string "I want to take a look around in the\n"
	.string "SNOWPOINT TEMPLE. But only really\l"
	.string "tough Trainers are allowed inside.$"

SnowpointCity_Text_NpcF1:
	.string "POKéMON are said to have dragged\n"
	.string "SNOWPOINT CITY here. The SNOWPOINT\l"
	.string "TEMPLE is their resting place,\l"
	.string "they say.$"

SnowpointCity_Text_Sailor:
	.string "The sea gets rough up here, but a\n"
	.string "good sailor doesn't mind the cold.$"

SnowpointCity_Text_TempleGuard:
	.string "The temple is said to have been\n"
	.string "built in ancient times. It pays\l"
	.string "homage to the POKéMON of rock,\l"
	.string "ice, and steel that shape the\l"
	.string "land. So it is told.$"

SnowpointCity_Text_NpcF2:
	.string "Bundle up before you go outside.\n"
	.string "The wind here bites hard.$"

SnowpointCity_Text_GymSign:
	.string "SNOWPOINT CITY POKéMON GYM\p"
	.string "The Ice-Type Diamond Dust Style!$"

SnowpointCity_Text_TempleSign:
	.string "SNOWPOINT TEMPLE$"
