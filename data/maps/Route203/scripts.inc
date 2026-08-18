@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route203_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S4: cena da fonte, rotulo Route203_CoordEvent_Rival >>>
@ BARRY (LOCALID_ROUTE203_RIVAL, sprite trocado para OBJ_EVENT_GFX_RICH_BOY
@ pela tabela de dev_scripts/valida_mapas_sinnoh.py) emboscava o jogador aqui
@ no Platinum. FLAG_SINNOH_ESCONDE_ROUTE_203_RIVAL nasce acesa (ver bloco
@ Sinnoh S4 em data/scripts/new_game.inc) e esta cena e quem revela e some com
@ ele, igual ao par Route207_CoordEvent_Counterpart.
@ Simplificacao anotada: a fonte ramifica o passo de aproximacao em 4 (um por
@ tile do gatilho) e a batalha em 3 (um por inicial de Sinnoh). Sem colisao no
@ NPC (so no jogador; ver CianwoodCity_EventScript_SuicuneTrigger) os 4 passos
@ colapsam num so sem risco de travar o waitmovement.
@ CORRIGIDO em 17/08/2026: o comentario anterior dizia que Sinnoh nunca
@ oferece TURTWIG/CHIMCHAR/PIPLUP nesta ROM e que so sobrava um treinador.
@ Isso ficou velho quando data/maps/SandgemTown_RowanLab/scripts.inc virou
@ mapa proprio (05/08/2026) e passou a entregar o inicial de Sinnoh de
@ verdade, escrevendo VAR_STARTER_MON com 0=TURTWIG/1=CHIMCHAR/2=PIPLUP (o
@ mesmo bug ja identificado pelo cabecalho de CanalaveCity_EventScript_Rival
@ para o comentario do rival de Johto). O triangulo de tipos do rival e
@ verdade aqui: os tres TRAINER_SINNOH_RIVAL_ROUTE_203_* e o time literal de
@ cada um ja vinham prontos em src/data/trainers_sinnoh.party (bulk import),
@ so faltava o id em opponents.h e esta cena. Nome da constante e o inicial
@ DO JOGADOR (regra da casa: a fonte as vezes nomeia o do rival, nao foi o
@ caso aqui, conferido contra res/trainers/data/rival_route_203_*.json).
@ Gatilho por VAR_LAST_TALKED manual (precedente CeruleanCity_Frlg
@ EventScript_Rival): esta cena e uma emboscada por coordevent, nao um clique
@ em objeto, entao trainerbattle_no_intro precisa da var setada a mao.
Route203_EventScript_CoordEvent_Rival::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_ROUTE_203_RIVAL
	addobject LOCALID_ROUTE203_RIVAL
	applymovement LOCALID_ROUTE203_RIVAL, Route203_Movement_RivalNoticePlayer
	waitmovement 0
	applymovement LOCALID_ROUTE203_RIVAL, Route203_Movement_RivalWalkToPlayer
	waitmovement 0
	msgbox Route203_Text_RivalIGotTougher, MSGBOX_DEFAULT
	setvar VAR_LAST_TALKED, LOCALID_ROUTE203_RIVAL
	call_if_eq VAR_STARTER_MON, 0, Route203_EventScript_RivalBattleTurtwig
	call_if_eq VAR_STARTER_MON, 1, Route203_EventScript_RivalBattleChimchar
	call_if_eq VAR_STARTER_MON, 2, Route203_EventScript_RivalBattlePiplup
	applymovement LOCALID_ROUTE203_RIVAL, Route203_Movement_RivalLeave
	waitmovement 0
	setflag FLAG_SINNOH_ESCONDE_ROUTE_203_RIVAL
	removeobject LOCALID_ROUTE203_RIVAL
	setvar VAR_SINNOH_R203_RIVAL_ESTADO, 1
	releaseall
	end

Route203_EventScript_RivalBattleTurtwig::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_ROUTE_203_TURTWIG, Route203_Text_RivalWhatDoYouMeanILost
	return

Route203_EventScript_RivalBattleChimchar::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_ROUTE_203_CHIMCHAR, Route203_Text_RivalWhatDoYouMeanILost
	return

Route203_EventScript_RivalBattlePiplup::
	trainerbattle_no_intro TRAINER_SINNOH_RIVAL_ROUTE_203_PIPLUP, Route203_Text_RivalWhatDoYouMeanILost
	return

Route203_Movement_RivalNoticePlayer:
	delay_8
	emote_exclamation_mark
	delay_8
	step_end

Route203_Movement_RivalWalkToPlayer:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	step_end

Route203_Movement_RivalLeave:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

Route203_Text_RivalIGotTougher:
	.string "BARRY: Hey! {PLAYER}!\p"
	.string "Tell me you got a little tougher!\p"
	.string "Me? Do you even need to ask?\n"
	.string "Of course I got tougher!\p"
	.string "Come on!$"

Route203_Text_RivalWhatDoYouMeanILost:
	.string "BARRY: Waah!\n"
	.string "What do you mean I lost?!\p"
	.string "Well, that's it!$"
@ <<< B6 Sinnoh S4: cena da fonte <<<

Route203_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_SEBASTIAN, Route203_Text_Trainer1Intro, Route203_Text_Trainer1Defeat
	msgbox Route203_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route203_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_MICHAEL, Route203_Text_Trainer2Intro, Route203_Text_Trainer2Defeat
	msgbox Route203_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route203_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_LASS_KAITLIN, Route203_Text_Trainer3Intro, Route203_Text_Trainer3Defeat
	msgbox Route203_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route203_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_DALLAS, Route203_Text_Trainer4Intro, Route203_Text_Trainer4Defeat
	msgbox Route203_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route203_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_LASS_MADELINE, Route203_Text_Trainer5Intro, Route203_Text_Trainer5Defeat
	msgbox Route203_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route203_Text_Trainer1Intro:
	.string "Before I challenge the Pokémon Gym\nLeader, I'll test my strength on you!$"

Route203_Text_Trainer1Defeat:
	.string "I guess it means I'm not ready for\nthe Gym challenge yet...$"

Route203_Text_Trainer1Post:
	.string "I guess if you don't have a single\nGym Badge, you're a total nobody...$"

Route203_Text_Trainer2Intro:
	.string "I get my get-up-and-go from my\nPokémon!Here we go!\nKRICKETOT! ZUBAT!$"

Route203_Text_Trainer2Defeat:
	.string "Ack! My Pokémon...$"

Route203_Text_Trainer2Post:
	.string "Keep out of the grass or dodge the\neyes of Trainers...?I always have a tough time choosing.$"

Route203_Text_Trainer3Intro:
	.string "I found a Trainer while looking for\nsome Pokémon!$"

Route203_Text_Trainer3Defeat:
	.string "Hunh? You're finished so soon?$"

Route203_Text_Trainer3Post:
	.string "I walk through tall grass until I\nfind the Pokémon I want.$"

Route203_Text_Trainer4Intro:
	.string "I'm never apart from my SHINX.\nOur bond is strong!$"

Route203_Text_Trainer4Defeat:
	.string "So sad...\nAnd so crushed...$"

Route203_Text_Trainer4Post:
	.string "I don't bear grudges over losing.\nBut I promise I'll get tougher!$"

Route203_Text_Trainer5Intro:
	.string "I got a nifty-keen Gym Badge from\nthe Gym Leader in Oreburgh City!$"

Route203_Text_Trainer5Defeat:
	.string "Oh, I lost! Lalala!$"

Route203_Text_Trainer5Post:
	.string "I'm collecting lots of Gym Badges.\nThey're so sparkly and pretty!$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route203_EventScript_Placa1::
	msgbox Route203_Text_Placa1, MSGBOX_SIGN
	end

Route203_Text_Placa1:
	.string "Rt. 203\nJubilife City$"

Route203_EventScript_Placa2::
	msgbox Route203_Text_Placa2, MSGBOX_SIGN
	end

Route203_Text_Placa2:
	.string "Rt. 203\nOreburgh City$"

Route203_EventScript_Placa3::
	msgbox Route203_Text_Placa3, MSGBOX_SIGN
	end

Route203_Text_Placa3:
	.string "Trainer Tips!\pIf a Pokémon is about to evolve,\nit can be instantly stopped.\pPress the B Button during evolution\nto startle the Pokémon into stopping.\pThat is how evolution can be\ncanceled.$"

Route203_EventScript_Placa4::
	msgbox Route203_Text_Placa4, MSGBOX_SIGN
	end

Route203_Text_Placa4:
	.string "Trainer Tips!\pPokémon moves use energy called\nPower Points, or PP for short.\pIf the PP of moves runs low, head for\nany Pokémon Center.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route203_EventScript_Npc1::
	msgbox Route203_Text_Npc1, MSGBOX_NPC
	end

Route203_Text_Npc1:
	.string "Your favorite Pokémon should be placed\nat the top left of your party list.\pThat way, it will be the first to go out\nin a battle.$"
