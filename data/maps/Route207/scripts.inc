@ Contraparte (o rival de genero oposto ao do jogador) usa
@ OBJ_EVENT_GFX_VAR_0 no map.json, e QUEM USA VAR_0 SETA A VAR NO PROPRIO
@ ON_TRANSITION: assim o sprite nao depende do que outro mapa deixou na var
@ (ela mora no save, e VAR_OBJ_GFX_ID_0 e compartilhada por todo mundo).
@ Mesmo mecanismo de LakeVerity, SandgemTown e Route202, e os mesmos dois
@ sprites: escolher no meio da cena, como estava aqui, so acertava na
@ primeira vez e ainda usava OBJ_EVENT_GFX_PLAYER_M/F, que e o sprite do
@ jogador, nao o do rival.
Route207_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Route207_OnTransition
	.byte 0

Route207_OnTransition::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, Route207_SetCounterpartFemale
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	end

Route207_SetCounterpartFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	end

@ >>> B6 Sinnoh S4: cena da fonte, rotulo Route207_CoordEvent_Counterpart >>>
@ O "counterpart" (DAWN/LUCAS, sexo oposto ao do jogador) surge uma unica vez
@ e da o VS SEEKER. Fonte tambem da o app de Pokétch Dowsing Machine: caindo,
@ decisao 3 do plano (Pokétch nao existe aqui). VS Seeker em si existe
@ (ITEM_VS_SEEKER); a parte "nivel de carga" (FLAG_UNLOCKED_VS_SEEKER_LVL_1)
@ nao existe neste motor (I_VS_SEEKER_CHARGING = 0 em include/config/item.h,
@ mecanica desligada globalmente), entao so o giveitem entra.
@ O sprite da contraparte sai do ON_TRANSITION deste mapa (topo do arquivo),
@ nao daqui.
Route207_EventScript_CoordEvent_Counterpart::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_ROUTE_207_COUNTERPART
	addobject LOCALID_ROUTE207_COUNTERPART
	applymovement LOCALID_ROUTE207_COUNTERPART, Route207_Movement_CounterpartNoticePlayer
	waitmovement 0
	applymovement LOCALID_ROUTE207_COUNTERPART, Route207_Movement_CounterpartWalkToPlayer
	waitmovement 0
	msgbox Route207_Text_CounterpartChooseAHand, MSGBOX_DEFAULT
	msgbox Route207_Text_CounterpartYouWantTheVsSeeker, MSGBOX_DEFAULT
	giveitem ITEM_VS_SEEKER
	msgbox Route207_Text_CounterpartHaveThisTooThen, MSGBOX_DEFAULT
	applymovement LOCALID_ROUTE207_COUNTERPART, Route207_Movement_CounterpartLeave
	waitmovement 0
	setflag FLAG_SINNOH_ESCONDE_ROUTE_207_COUNTERPART
	removeobject LOCALID_ROUTE207_COUNTERPART
	setvar VAR_SINNOH_R207_COMPANHEIRO_ESTADO, 1
	releaseall
	end

Route207_Movement_CounterpartNoticePlayer:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	emote_exclamation_mark
	step_end

Route207_Movement_CounterpartWalkToPlayer:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

Route207_Movement_CounterpartLeave:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	step_end

Route207_Text_CounterpartChooseAHand:
	.string "{PLAYER}! Fancy meeting you here!\p"
	.string "Hey, choose a hand!\n"
	.string "Which one has something in it?$"

Route207_Text_CounterpartYouWantTheVsSeeker:
	.string "Ah, you got it!\p"
	.string "You want the VS SEEKER, right?\n"
	.string "Take it, take it!$"

Route207_Text_CounterpartHaveThisTooThen:
	.string "Here, have this too!\p"
	.string "The VS SEEKER lets you check if\n"
	.string "Trainers you've beaten want a\l"
	.string "rematch. Use it often!$"
@ <<< B6 Sinnoh S4: cena da fonte <<<

Route207_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_CAMPER_ANTHONY, Route207_Text_Trainer1Intro, Route207_Text_Trainer1Defeat
	msgbox Route207_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer1Intro:
	.string "Go for it, my Pokémon!\n"
	.string "I'll do my best, too!$"

Route207_Text_Trainer1Defeat:
	.string "Oh...\n"
	.string "We lost...$"

Route207_Text_Trainer1Post:
	.string "Dig for Fossils in the Underground.\pThe mining museum might be able to\n"
	.string "bring back the ancient Pokémon!$"

Route207_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_LAUREN, Route207_Text_Trainer2Intro, Route207_Text_Trainer2Defeat
	msgbox Route207_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer2Intro:
	.string "Go do it, my Pokémon!\n"
	.string "I'll work hard, too!$"

Route207_Text_Trainer2Defeat:
	.string "Oh...\n"
	.string "We lost...$"

Route207_Text_Trainer2Post:
	.string "I think we'll visit the TV station in\n"
	.string "Jubilife City next.\pOr maybe we should go to the Global\n"
	.string "Terminal?$"

Route207_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_AUSTIN, Route207_Text_Trainer3Intro, Route207_Text_Trainer3Defeat
	msgbox Route207_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer3Intro:
	.string "I wear shorts the whole year!\n"
	.string "I've got energy to burn!$"

Route207_Text_Trainer3Defeat:
	.string "I couldn't win with just energy...\n"
	.string "Nothing's really that easy!$"

Route207_Text_Trainer3Post:
	.string "Pokémon don't wear clothes.\n"
	.string "I worry about them getting cold.$"

Route207_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_HIKER_JUSTIN, Route207_Text_Trainer4Intro, Route207_Text_Trainer4Defeat
	msgbox Route207_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer4Intro:
	.string "I just got through Mt. Coronet, but\n"
	.string "I've still got energy to burn!$"

Route207_Text_Trainer4Defeat:
	.string "Whoops!\n"
	.string "Taken down easily!$"

Route207_Text_Trainer4Post:
	.string "We need to rest up in Oreburgh City\n"
	.string "before heading to Mt. Coronet again.$"

Route207_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_HIKER_KEVIN, Route207_Text_Trainer5Intro, Route207_Text_Trainer5Defeat
	msgbox Route207_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer5Intro:
	.string "Wahaha!\n"
	.string "Laughter brings good fortune!$"

Route207_Text_Trainer5Defeat:
	.string "Wahahaha! There's nothing that\n"
	.string "I can do but laugh!$"

Route207_Text_Trainer5Post:
	.string "Wahahahaha!\n"
	.string "...Go ahead, laugh at me--the loser!$"

Route207_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_BATTLE_GIRL_HELEN, Route207_Text_Trainer6Intro, Route207_Text_Trainer6Defeat
	msgbox Route207_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer6Intro:
	.string "OK, OK!\n"
	.string "Let's be quick about this!$"

Route207_Text_Trainer6Defeat:
	.string "Oh, yeah? Let's do this again!\n"
	.string "...Oops. I'm out of Pokémon!$"

Route207_Text_Trainer6Post:
	.string "Yup! Good going!\n"
	.string "I like the way you battle!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route207_EventScript_Placa1::
	msgbox Route207_Text_Placa1, MSGBOX_SIGN
	end

Route207_Text_Placa1:
	.string "Rt. 207\nOreburgh City$"

Route207_EventScript_Placa2::
	msgbox Route207_Text_Placa2, MSGBOX_SIGN
	end

Route207_Text_Placa2:
	.string "Rt. 207\nMt. Coronet$"

Route207_EventScript_Placa3::
	msgbox Route207_Text_Placa3, MSGBOX_SIGN
	end

Route207_Text_Placa3:
	.string "Trainer Tips\pPokémon may become immobilized if\nthey are asleep or paralyzed.\pIf it happens to your Pokémon,\nit could be disastrous.\pIf your opponent's Pokémon can't\nmove, it's a big opportunity!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route207_EventScript_Npc1::
	msgbox Route207_Text_Npc1, MSGBOX_NPC
	end

Route207_Text_Npc1:
	.string "That slope's too slippery.\nYou'll need a Bike to get up.\pYou don't have a Bicycle?\nThere's a Cycle Shop in Eterna City.$"
