PokemonLeagueNorthPokecenter1F_MapScripts::
	.byte 0

@ DESBLOQUEADO na leva final (18/08/2026). Ids TRAINER_SINNOH_RIVAL_
@ POKEMON_LEAGUE_TURTWIG/_CHIMCHAR/_PIPLUP (2515-2517) ja existem. Molde
@ igual ao de Route209_Access_EventScript_CoordEvent_Rival: emboscada por
@ coordevent (nao clique em objeto), entao `setvar VAR_LAST_TALKED` manual
@ antes de `trainerbattle_no_intro`; o texto de derrota curto (TRMSG_
@ DEFEAT do json da fonte) vira o lose_text, e a fala longa de despedida
@ (RivalDefeat) so roda depois, na continuacao da vitoria. `setflag` antes
@ do `removeobject` no fecho, e VAR_SINNOH_RIVAL_VENCEU_SUNYSHORE sobe pra
@ 1 pra desarmar os 3 coord_events (var_value == 0, ja plantados pelo S1).
@ Aproximacao colapsada numa so (sem colisao no NPC), mesma tecnica de toda
@ emboscada de rival ja portada aqui; a fonte ramifica por porta de entrada
@ (oeste/norte/leste) so pra escolher o passo de caminhada.
@ Objeto sem local_id (id 7 por posicao no map.json, sem tocar
@ map_event_ids.h). A fonte so faz AddObject dentro desta cena: o objeto
@ nasce escondido pela flag do grupo, que a fonte tambem liga no jogo novo
@ (scripts_init_new_game.s:79) mas data/scripts/new_game.inc esta fora do
@ escopo desta leva; ver nota no map.json.
PokemonLeagueNorthPokecenter1F_EventScript_CoordEvent_Rival::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_POKEMON_LEAGUE_NORTH_POKECENTER_1F_RIVAL
	addobject 7
	applymovement 7, PokemonLeagueNorthPokecenter1F_Movement_RivalNoticePlayer
	waitmovement 0
	applymovement OBJ_EVENT_ID_PLAYER, PokemonLeagueNorthPokecenter1F_Movement_PlayerFaceRival
	waitmovement 0
	msgbox PokemonLeagueNorthPokecenter1F_Text_RivalIntro, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, 7
	call_if_eq VAR_STARTER_MON, 0, PokemonLeagueNorthPokecenter1F_EventScript_RivalBattleTurtwig
	call_if_eq VAR_STARTER_MON, 1, PokemonLeagueNorthPokecenter1F_EventScript_RivalBattleChimchar
	call_if_eq VAR_STARTER_MON, 2, PokemonLeagueNorthPokecenter1F_EventScript_RivalBattlePiplup
	msgbox PokemonLeagueNorthPokecenter1F_Text_RivalDefeat, MSGBOX_DEFAULT
	applymovement 7, PokemonLeagueNorthPokecenter1F_Movement_RivalLeave
	waitmovement 0
	setflag FLAG_SINNOH_ESCONDE_POKEMON_LEAGUE_NORTH_POKECENTER_1F_RIVAL
	removeobject 7
	setvar VAR_SINNOH_RIVAL_VENCEU_SUNYSHORE, 1
	releaseall
	end

PokemonLeagueNorthPokecenter1F_EventScript_RivalBattleTurtwig::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_POKEMON_LEAGUE_TURTWIG, PokemonLeagueNorthPokecenter1F_Text_RivalDefeatQuip
	return

PokemonLeagueNorthPokecenter1F_EventScript_RivalBattleChimchar::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_POKEMON_LEAGUE_CHIMCHAR, PokemonLeagueNorthPokecenter1F_Text_RivalDefeatQuip
	return

PokemonLeagueNorthPokecenter1F_EventScript_RivalBattlePiplup::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_POKEMON_LEAGUE_PIPLUP, PokemonLeagueNorthPokecenter1F_Text_RivalDefeatQuip
	return

PokemonLeagueNorthPokecenter1F_Movement_RivalNoticePlayer:
	delay_8
	emote_exclamation_mark
	delay_8
	step_end

PokemonLeagueNorthPokecenter1F_Movement_PlayerFaceRival:
	face_down
	step_end

PokemonLeagueNorthPokecenter1F_Movement_RivalLeave:
	walk_up
	walk_up
	step_end

PokemonLeagueNorthPokecenter1F_Text_RivalIntro:
	.string "BARRY: Hold it!\n"
	.string "Don't go off without me!\p"
	.string "You're challenging the Pokémon\n"
	.string "League, aren't you?\p"
	.string "Let's see who's more worthy of\n"
	.string "making the challenge with a battle!$"

PokemonLeagueNorthPokecenter1F_Text_RivalDefeatQuip:
	.string "What just went down?!\n"
	.string "My team still needs raising?!$"

PokemonLeagueNorthPokecenter1F_Text_RivalDefeat:
	.string "BARRY: I guess I'm not ready for\n"
	.string "the Pokémon League if I'm losing\lto you! Darn it!\p"
	.string "You watch, though!\n"
	.string "I'll get tougher and win my way\lthrough the Pokémon League!\p"
	.string "{PLAYER}! You'd better not lose to\n"
	.string "anyone before me!$"

PokemonLeagueNorthPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

PokemonLeagueNorthPokecenter1F_EventScript_Npc1::
	msgbox PokemonLeagueNorthPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

PokemonLeagueNorthPokecenter1F_Text_Npc1:
	.string "Let me confirm that you are qualified\nto challenge the Pokémon League.\pSo! Let us examine the Gym Badges\nyou gathered from Sinnoh.\pOreburgh City's Coal Badge!\pEterna City's Forest Badge!\pHearthome City's Relic Badge!\pVeilstone City's Cobble Badge!\pPastoria City's Fen Badge!\pCanalave City's Mine Badge!\pSnowpoint City's Icicle Badge!\pAnd...\nSunyshore City's Beacon Badge!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PokemonLeagueNorthPokecenter1F_EventScript_Npc3::
	msgbox PokemonLeagueNorthPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

PokemonLeagueNorthPokecenter1F_Text_Npc3:
	.string "It doesn't matter if the going is slow.\pNor does it matter how many challenges\nit takes.\pI'm never giving up!\nNot until I beat the Elite Four!$"

PokemonLeagueNorthPokecenter1F_EventScript_Npc2::
	msgbox PokemonLeagueNorthPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

PokemonLeagueNorthPokecenter1F_Text_Npc2:
	.string "What is the Pokémon League?\nDon't take my word for it.\pTake the challenge and experience it\nfor yourself!$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

PokemonLeagueNorthPokecenter1F_Text_LojaSaudacao:
	.string "Welcome! Take a look around, we've\ngot everything a TRAINER needs.$"

@ loja_comum do Platinum (lista comum), tabela de include/data/mart_items.h
PokemonLeagueNorthPokecenter1F_EventScript_Loja1::
	lock
	faceplayer
	msgbox PokemonLeagueNorthPokecenter1F_Text_LojaSaudacao, MSGBOX_DEFAULT
	pokemart PokemonLeagueNorthPokecenter1F_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
PokemonLeagueNorthPokecenter1F_Pokemart_Loja1:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

@ loja_especial do Platinum (MART_SPECIALTIES_ID_POKEMON_LEAGUE), tabela de include/data/mart_items.h
PokemonLeagueNorthPokecenter1F_EventScript_Loja2::
	lock
	faceplayer
	msgbox PokemonLeagueNorthPokecenter1F_Text_LojaSaudacao, MSGBOX_DEFAULT
	pokemart PokemonLeagueNorthPokecenter1F_Pokemart_Loja2
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
PokemonLeagueNorthPokecenter1F_Pokemart_Loja2:
	.2byte ITEM_HEAL_BALL
	.2byte ITEM_NET_BALL
	.2byte ITEM_NEST_BALL
	.2byte ITEM_DUSK_BALL
	.2byte ITEM_QUICK_BALL
	.2byte ITEM_TIMER_BALL
	.2byte ITEM_REPEAT_BALL
	.2byte ITEM_LUXURY_BALL
	pokemartlistend

@ >>> porta fechada (remove_mapas_cortados.py) >>>
PokemonLeagueNorthPokecenter1F_EventScript_PortaFechada::
	msgbox PokemonLeagueNorthPokecenter1F_Text_PortaFechada, MSGBOX_SIGN
	end

PokemonLeagueNorthPokecenter1F_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
