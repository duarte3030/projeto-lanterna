SunyshoreCity_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S7: cena da fonte, rotulo SunyshoreCity_CoordEvent_RivalAndJasmine >>>
@ ponytail: a fonte ramifica em 5 variantes (X 853 a 857, GetPlayerMapPos)
@ so pra calibrar de qual lado o Rival entra e quantos tiles ele anda, mesmo
@ dialogo e mesmo desfecho nas 5. O gerador expandiu o gatilho em 5 tiles
@ (decisao 7); aqui os 5 caem no MESMO script e usam UMA rota unica (a
@ variante X855 da fonte, entrada por cima e sem desvio lateral), em vez de
@ portar as 5 ApplyMovement quase identicas. Se algum dos 5 tiles ficar com
@ o Rival atravessando cenario, e ajuste de rota, nao de dialogo.
@ Onda 5 (18/08/2026), as duas pontas que faltavam:
@ - o `clearflag` daqui so tem o que limpar porque data/scripts/new_game.inc
@   agora acende FLAG_SINNOH_ESCONDE_SUNYSHORE_CITY_RIVAL no jogo novo, como
@   a fonte faz em scripts_init_new_game.s:122;
@ - quem grava VAR_SINNOH_SUNYSHORE_ESTADO = 2 (a condicao dos 5 gatilhos) e
@   a vitoria contra o Volkner, em SunyshoreCity_Gym/scripts.inc, igual a
@   fonte (scripts_sunyshore_city_gym_room_3.s:51). Antes disso a cena
@   inteira era inalcancavel.
SunyshoreCity_EventScript_CoordEvent_RivalAndJasmine::
	lockall
	applymovement LOCALID_SUNYSHORE_JASMINE, SunyshoreCity_Movement_JasmineNoticePlayer
	waitmovement 0
	clearflag FLAG_SINNOH_ESCONDE_SUNYSHORE_CITY_RIVAL
	addobject LOCALID_SUNYSHORE_RIVAL
	applymovement LOCALID_SUNYSHORE_RIVAL, SunyshoreCity_Movement_RivalEnter
	applymovement OBJ_EVENT_ID_PLAYER, SunyshoreCity_Movement_PlayerWatchRivalEnter
	waitmovement 0
	msgbox SunyshoreCity_Text_YouGotAllBadges, MSGBOX_DEFAULT
	applymovement LOCALID_SUNYSHORE_RIVAL, SunyshoreCity_Movement_RivalWalkOnSpotSouth
	waitmovement 0
	msgbox SunyshoreCity_Text_YouWatchMe, MSGBOX_DEFAULT
	applymovement LOCALID_SUNYSHORE_RIVAL, SunyshoreCity_Movement_RivalWalkOnSpotNorth
	waitmovement 0
	msgbox SunyshoreCity_Text_HurryToPokemonLeague, MSGBOX_DEFAULT
	applymovement LOCALID_SUNYSHORE_RIVAL, SunyshoreCity_Movement_RivalLeave
	waitmovement 0
	setflag FLAG_SINNOH_ESCONDE_SUNYSHORE_CITY_RIVAL
	removeobject LOCALID_SUNYSHORE_RIVAL
	applymovement LOCALID_SUNYSHORE_JASMINE, SunyshoreCity_Movement_JasmineWalkToPlayer
	applymovement OBJ_EVENT_ID_PLAYER, SunyshoreCity_Movement_PlayerWalkOnSpotNorth
	waitmovement 0
	msgbox SunyshoreCity_Text_HaveThisAsMyThanks, MSGBOX_DEFAULT
	call SunyshoreCity_EventScript_GiveWaterfall
	applymovement LOCALID_SUNYSHORE_JASMINE, SunyshoreCity_Movement_JasmineLeave
	waitmovement 0
	setvar VAR_SINNOH_SUNYSHORE_ESTADO, 3
	releaseall
	end

@ Fonte: SunyshoreCity_GiveWaterfall. O coord_event so dispara uma vez (o
@ var muda de valor e o proprio motor nao repete o mesmo tile), entao nao
@ precisa de FLAG_RECEIVED_* nova pra travar reentrega.
SunyshoreCity_EventScript_GiveWaterfall::
	msgbox SunyshoreCity_Text_ThisIsntMuchBut, MSGBOX_DEFAULT
	giveitem ITEM_HM07
	msgbox SunyshoreCity_Text_ThatHMContainsWaterfall, MSGBOX_DEFAULT
	return

SunyshoreCity_Movement_JasmineNoticePlayer:
	walk_in_place_down
	emote_exclamation_mark
	step_end

SunyshoreCity_Movement_RivalEnter:
	delay_8
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

SunyshoreCity_Movement_PlayerWatchRivalEnter:
	walk_in_place_down
	step_end

SunyshoreCity_Movement_RivalWalkOnSpotSouth:
	walk_in_place_fast_down
	step_end

SunyshoreCity_Movement_RivalWalkOnSpotNorth:
	walk_in_place_fast_up
	step_end

SunyshoreCity_Movement_RivalLeave:
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

SunyshoreCity_Movement_JasmineWalkToPlayer:
	walk_left
	walk_left
	walk_down
	step_end

SunyshoreCity_Movement_JasmineLeave:
	walk_up
	walk_up
	walk_right
	walk_right
	walk_in_place_down
	step_end

SunyshoreCity_Movement_PlayerWalkOnSpotNorth:
	walk_in_place_up
	step_end

SunyshoreCity_Text_YouGotAllBadges:
	.string "BARRY: Hey!\n"
	.string "{PLAYER}!\p"
	.string "What the...\p"
	.string "You went and got all eight Gym\n"
	.string "Badges of Sinnoh!\p"
	.string "Aww, you...\n"
	.string "That's wicked! I envy you!\p"
	.string "But don't think you've won!$"

SunyshoreCity_Text_YouWatchMe:
	.string "Because I'm going to be the toughest\n"
	.string "Trainer ever! You watch me!\p"
	.string "Before I was dreaming.\n"
	.string "I just wanted to be like my dad.\p"
	.string "Now, things are different.\p"
	.string "I thought about what being a\n"
	.string "Trainer involves.\p"
	.string "I thought about what Pokémon are.\p"
	.string "We're going to get tougher one step\n"
	.string "at a time!$"

SunyshoreCity_Text_HurryToPokemonLeague:
	.string "I'm not going to challenge you to a\n"
	.string "battle now.\p"
	.string "I hate to say it, but I know you're\n"
	.string "tougher than me.\p"
	.string "But not a whole lot tougher.\n"
	.string "Just a little.\p"
	.string "Our difference is about a yard?\p"
	.string "Nah, not even an inch.\p"
	.string "...What I'm trying to say is that I\n"
	.string "will catch up to you in no time.\p"
	.string "If you don't hurry to the Pokémon\n"
	.string "League, I'll leave you in my wake!$"

SunyshoreCity_Text_HaveThisAsMyThanks:
	.string "JASMINE: ...Was that your friend?\p"
	.string "Seeing how you two got along made\n"
	.string "me happy somehow.\p"
	.string "It must be wonderful having a\n"
	.string "friend like that.\p"
	.string "A person that you can share\n"
	.string "anything and everything with.\p"
	.string "A person you can compete with\n"
	.string "without fighting.\p"
	.string "...Um, it made me feel sort of warm\n"
	.string "seeing you two.\p"
	.string "It may seem odd, but I'd like you\n"
	.string "to have this as my thanks.$"

SunyshoreCity_Text_ThisIsntMuchBut:
	.string "JASMINE: This isn't much, but...$"

SunyshoreCity_Text_ThatHMContainsWaterfall:
	.string "...That Hidden Machine...\n"
	.string "It contains Waterfall.\p"
	.string "If you use it, you can get to the\n"
	.string "Pokémon League.\p"
	.string "...Um... I... I don't know how I\n"
	.string "should say this, but good luck.$"

@ <<< B6 Sinnoh S7: cena da fonte <<<

SunyshoreCity_EventScript_Jasmine::
	lock
	faceplayer
	msgbox SunyshoreCity_Text_Jasmine, MSGBOX_DEFAULT
	release
	end

SunyshoreCity_EventScript_BreederF::
	msgbox SunyshoreCity_Text_BreederF, MSGBOX_NPC
	end

SunyshoreCity_Text_Jasmine:
	.string "...This city makes me feel at\n"
	.string "home somehow.\p"
	.string "It's next to the sea, and there's\n"
	.string "a lighthouse...$"

SunyshoreCity_Text_BreederF:
	.string "My POKéMON love the salty air\n"
	.string "here. It's good for their coats.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

SunyshoreCity_EventScript_Placa1::
	msgbox SunyshoreCity_Text_Placa1, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa1:
	.string "Sunyshore Market\nA Selection of the World's Seals$"

SunyshoreCity_EventScript_Placa3::
	msgbox SunyshoreCity_Text_Placa3, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa3:
	.string "Sunyshore City Pokémon Gym\nLeader: Volkner\pThe Shining, Shocking Star$"

SunyshoreCity_EventScript_Placa4::
	msgbox SunyshoreCity_Text_Placa4, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa4:
	.string "Vista Lighthouse\nThe Beacon That Lights Sinnoh$"

SunyshoreCity_EventScript_Placa5::
	msgbox SunyshoreCity_Text_Placa5, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa5:
	.string "Julia's House\nDelightful Ribbons for Pokémon$"

SunyshoreCity_EventScript_Placa6::
	msgbox SunyshoreCity_Text_Placa6, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa6:
	.string "Pokémon Rock\nSunyshore's Heritage Site$"

SunyshoreCity_EventScript_Placa7::
	msgbox SunyshoreCity_Text_Placa7, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa7:
	.string "It's a blank sign painted white.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SunyshoreCity_EventScript_Npc1::
	msgbox SunyshoreCity_Text_Npc1, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc1:
	.string "That giant rock...\nIsn't it really a Pokémon?$"

SunyshoreCity_EventScript_Npc2::
	msgbox SunyshoreCity_Text_Npc2, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc2:
	.string "The city uses a lot of electricity,\nespecially the lighthouse and the Gym.\pThey finally decided to turn all the\ncity's roads into giant solar panels.\pSunyshore is the Sunshine City, so\nthe system works perfectly.$"

SunyshoreCity_EventScript_Npc3::
	msgbox SunyshoreCity_Text_Npc3, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc3:
	.string "This is a major port town.\nAnd...\pIt's the gateway to the Pokémon\nLeague.$"

SunyshoreCity_EventScript_Npc4::
	msgbox SunyshoreCity_Text_Npc4, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc4:
	.string "The Gym Leader uses too much\nelectricity!\pHe needs to think about the city's\npower needs, too!$"

SunyshoreCity_EventScript_Npc5::
	msgbox SunyshoreCity_Text_Npc5, MSGBOX_NPC
	end

SunyshoreCity_Text_Npc5:
	.string "Whatever the environment, people\nand Pokémon adapt to live there.\pThat's what we all do to survive.$"

SunyshoreCity_EventScript_Placa2::
	msgbox SunyshoreCity_Text_Placa2, MSGBOX_SIGN
	end

SunyshoreCity_Text_Placa2:
	.string "Sunyshore City\nSolar Powered!$"
