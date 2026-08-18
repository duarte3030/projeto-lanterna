@ Textos vindos de pret/pokeplatinum (res/text/snowpoint_city.json), em ingles.
@ Candice, o Sailor do SS SPIRAL e Cynthia ficaram de fora: dependem de flag
@ de historia (FLAG_HIDE_SNOWPOINT_CITY_*), que este agente nao pode inventar.
@ O Temple_Guard usa so a fala geral sobre o templo (as falas sobre deixar
@ o jogador entrar dependem da Candice, que esta fora do escopo).
@ OBJ_EVENT_GFX_ACE_TRAINER_SNOW_F e OBJ_EVENT_GFX_SNOWPOINT_NPC_M/F nao
@ existem em event_objects.h: trocados por COOLTRAINER_F, MAN_2 e WOMAN_2.

SnowpointCity_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
SnowpointCity_EventScript_CoordEvent_TempleGuard::
	@ TODO S6: cena da fonte, rotulo SnowpointCity_CoordEvent_TempleGuard
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

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

SnowpointCity_EventScript_GymSign::
	msgbox SnowpointCity_Text_GymSign, MSGBOX_SIGN
	end

SnowpointCity_EventScript_TempleSign::
	msgbox SnowpointCity_Text_TempleSign, MSGBOX_SIGN
	end

SnowpointCity_Text_Sailor:
	.string "The sea gets rough up here, but a\n"
	.string "good sailor doesn't mind the cold.$"

SnowpointCity_Text_GymSign:
	.string "SNOWPOINT CITY POKéMON GYM\p"
	.string "The Ice-Type Diamond Dust Style!$"

SnowpointCity_Text_TempleSign:
	.string "SNOWPOINT TEMPLE$"

SnowpointCity_Text_SailorOferece:
	.string "My boat sails to the BATTLE ZONE,\n"
	.string "across the sea.\p"
	.string "Care to come aboard?$"

SnowpointCity_Text_SailorZarpa:
	.string "Setting sail for the BATTLE ZONE!$"

SnowpointCity_Text_SailorRecusa:
	.string "Just call me when you change\nyour mind.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

SnowpointCity_EventScript_Placa2::
	msgbox SnowpointCity_Text_Placa2, MSGBOX_SIGN
	end

SnowpointCity_Text_Placa2:
	.string "Snowpoint City Pokémon Gym\nLeader: Candice\pThe Diamond Dust Girl!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SnowpointCity_EventScript_Npc1::
	msgbox SnowpointCity_Text_Npc1, MSGBOX_NPC
	end

SnowpointCity_Text_Npc1:
	.string "Brrr... This snowbound town is always\nfreezing cold.\pBut the spirits of the Trainers and\ntheir Pokémon burn hot and bright.\pEspecially the Gym Leader.$"

SnowpointCity_EventScript_Npc2::
	msgbox SnowpointCity_Text_Npc2, MSGBOX_NPC
	end

SnowpointCity_Text_Npc2:
	.string "I want to take a look around in the\nSnowpoint Temple.\pBut only really tough Trainers are\nallowed inside.$"

SnowpointCity_EventScript_Npc3::
	msgbox SnowpointCity_Text_Npc3, MSGBOX_NPC
	end

SnowpointCity_Text_Npc3:
	.string "Your scarf looks nice and warm.\nI wish I had one like it.$"

SnowpointCity_EventScript_Npc4::
	msgbox SnowpointCity_Text_Npc4, MSGBOX_NPC
	end

SnowpointCity_Text_Npc4:
	.string "There is nothing exceptional here.\nThat makes Snowpoint unique.\pThere's nothing exceptional about me.\nThat's what makes me stand out!$"

SnowpointCity_EventScript_Npc5::
	msgbox SnowpointCity_Text_Npc5, MSGBOX_NPC
	end

SnowpointCity_Text_Npc5:
	.string "Only the chosen may enter\nthe Snowpoint Temple.\pI'm sorry, but you will have to\nleave.$"

SnowpointCity_EventScript_Npc6::
	msgbox SnowpointCity_Text_Npc6, MSGBOX_NPC
	end

SnowpointCity_Text_Npc6:
	.string "Candice is teaching me about Pokémon.\pShe says I have to start by making\nfriends with Pokémon.$"

SnowpointCity_EventScript_Placa7::
	msgbox SnowpointCity_Text_Placa7, MSGBOX_SIGN
	end

SnowpointCity_Text_Placa7:
	.string "Snowpoint City\nCity of Snow$"
