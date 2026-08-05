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
	lock
	faceplayer
@ ponytail: a Battle Zone (Fight Area, Survival, Resort e rotas 225 a 230) existia
@ no repo e era inalcancavel: nenhum warp, nenhuma conexao levava la. No original
@ so se chega de barco em Snowpoint depois da Liga, entao o porto abre com a
@ FLAG_ELITE_SINNOH_VENCIDA, que ja estava reservada.
	goto_if_unset FLAG_ELITE_SINNOH_VENCIDA, SnowpointCity_EventScript_SailorFechado
	msgbox SnowpointCity_Text_SailorOferece, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SnowpointCity_EventScript_SailorRecusa
	msgbox SnowpointCity_Text_SailorZarpa, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_FIGHT_AREA, 35, 17
	waitstate
	release
	end

SnowpointCity_EventScript_SailorFechado::
	msgbox SnowpointCity_Text_Sailor, MSGBOX_DEFAULT
	release
	end

SnowpointCity_EventScript_SailorRecusa::
	msgbox SnowpointCity_Text_SailorRecusa, MSGBOX_DEFAULT
	release
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

SnowpointCity_Text_SailorOferece:
	.string "Meu barco vai para a Battle Zone,\n"
	.string "do outro lado do mar.\p"
	.string "Quer embarcar?$"

SnowpointCity_Text_SailorZarpa:
	.string "Zarpando para a Battle Zone!$"

SnowpointCity_Text_SailorRecusa:
	.string "Quando mudar de ideia, e so chamar.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

SnowpointCity_EventScript_Placa2::
	msgbox SnowpointCity_Text_Placa2, MSGBOX_SIGN
	end

SnowpointCity_Text_Placa2:
	.string "Snowpoint City Pokémon Gym\nLeader: Candice\pThe Diamond Dust Girl!$"
