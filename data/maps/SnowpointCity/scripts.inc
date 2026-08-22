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
@ rotulo da fonte: SnowpointCity_CoordEvent_TempleGuard (script 3).
@ LOCALID_SNOWPOINT_CITY_TEMPLE_GUARD sempre visivel (hidden_flag da fonte e
@ "0"). So o ramo de bloqueio e escrito: exige Pokedex Nacional
@ (FLAG_SYS_NATIONAL_DEX) e FLAG_SYS_GAME_CLEAR, e hoje nada nesta obra
@ acende as duas ao mesmo tempo (pos-jogo nao existe ainda). O ramo de
@ liberacao (SnowpointCity_AllowEnterTemple na fonte) fica BLOQUEADO: precisa
@ de LOCALID_CANDICE novo por FLAG_HIDE_SNOWPOINT_CITY_CANDICE, que nao esta
@ no censo do S1 (lider de ginasio, mesma familia de bloqueio do Maylene de
@ Route217). Ver tambem o comentario do topo deste arquivo, ja escrito antes
@ desta leva com a mesma decisao.
SnowpointCity_EventScript_CoordEvent_TempleGuard::
	lockall
	applymovement LOCALID_SNOWPOINT_CITY_TEMPLE_GUARD, SnowpointCity_Movement_TempleGuardWalkOnSpotWest
	waitmovement 0
	msgbox SnowpointCity_Text_OnlyChosenMayEnterTemple, MSGBOX_DEFAULT
	goto_if_unset FLAG_SYS_NATIONAL_DEX, SnowpointCity_EventScript_TempleGuardBlockPlayer
	goto_if_unset FLAG_SYS_GAME_CLEAR, SnowpointCity_EventScript_TempleGuardBlockPlayer
	@ BLOQUEADO: ramo de liberacao precisa da Candice (flag nao autorizada,
	@ ver comentario acima). Volta ao plano antes de escrever.
	releaseall
	end

SnowpointCity_EventScript_TempleGuardBlockPlayer::
	applymovement LOCALID_SNOWPOINT_CITY_TEMPLE_GUARD, SnowpointCity_Movement_TempleGuardWalkOnSpotSouth
	applymovement OBJ_EVENT_ID_PLAYER, SnowpointCity_Movement_PlayerWalkSouth
	waitmovement 0
	releaseall
	end

SnowpointCity_Movement_TempleGuardWalkOnSpotWest:
	walk_in_place_left
	step_end

SnowpointCity_Movement_TempleGuardWalkOnSpotSouth:
	walk_in_place_down
	step_end

SnowpointCity_Movement_PlayerWalkSouth:
	walk_down
	step_end

@ Fala do guarda ao ser abordado (talk, script 1 da fonte): so a recusa
@ geral, igual ao coord_event acima (o ramo que muda de fala depende da
@ Candice, fora do escopo aqui).
SnowpointCity_EventScript_TempleGuard::
	lock
	faceplayer
	msgbox SnowpointCity_Text_OnlyChosenMayEnterTemple, MSGBOX_DEFAULT
	release
	end

@ Texto literal de res/text/snowpoint_city.json (as duas variantes da fonte,
@ OnlyChosenMayEnterTemple/_2, sao o mesmo texto; um so rotulo aqui).
SnowpointCity_Text_OnlyChosenMayEnterTemple:
	.string "Only the chosen may enter\n"
	.string "the Snowpoint Temple.\p"
	.string "I'm sorry, but you will have to\n"
	.string "leave.$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

SnowpointCity_EventScript_Sailor::
	lock
	faceplayer
@ ponytail: a Battle Zone (Fight Area, Survival, Resort e rotas 225 a 230) existia
@ no repo e era inalcancavel: nenhum warp, nenhuma conexao levava la. No original
@ so se chega de barco em Snowpoint depois da Liga, entao o porto abre com a
@ FLAG_ELITE_SINNOH_VENCIDA, que ja estava reservada.
@ A Battle Zone saiu do escopo (PLANO-ESCOPO.md, 21/08/2026): a viagem
@ some e o marinheiro fica no ramo que ja existia.
	goto SnowpointCity_EventScript_SailorFechado

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

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
SnowpointCity_EventScript_DexGlastrier::
	lockall
	msgbox SnowpointCity_Text_DexGlastrierIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GLASTRIER, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GLASTRIER, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GLASTRIER
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, SnowpointCity_EventScript_DexGlastrierSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, SnowpointCity_EventScript_DexGlastrierSome
	releaseall
	end

SnowpointCity_EventScript_DexGlastrierSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GLASTRIER
	setflag FLAG_HIDE_DEX_GLASTRIER
	fadescreenswapbuffers FADE_FROM_BLACK
	return

SnowpointCity_Text_DexGlastrierIntro:
	.string "GLASTRIER appeared!$"

@ <<< Dex completa <<<
