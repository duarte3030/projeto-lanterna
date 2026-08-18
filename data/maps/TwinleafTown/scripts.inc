@ Mapa de referencia de Sinnoh. O padrao usado aqui vale para os outros 132:
@ ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever qualquer script novo.
@ Textos vindos de pret/pokeplatinum, em ingles, como o resto do jogo.

TwinleafTown_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ Fonte: scripts_twinleaf_town.s, TwinleafTown_CoordEvent_RivalThud. O rival
@ (Barry) sai batendo a porta da casa dele e esbarra no jogador, pedindo pressa
@ para ver o ROWAN. ponytail: a fonte tem LoadDoorAnimation com coordenada de
@ tile que nao da para confirmar sem build; troquei a porta fisica por um
@ "bump" no lugar (thud sonoro + exclamacao), mesmo batimento narrativo sem
@ arriscar abrir porta errada. Upgrade: animar a porta de
@ Twinleaf_Town_RivalsHouse_F1 quando a coordenada for confirmada no jogo.
TwinleafTown_EventScript_CoordEvent_RivalThud::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_TWINLEAF_TOWN_RIVAL
	addobject LOCALID_TWINLEAF_RIVAL_DOOR
	applymovement LOCALID_TWINLEAF_RIVAL_DOOR, TwinleafTown_Movement_RivalBump
	applymovement OBJ_EVENT_ID_PLAYER, TwinleafTown_Movement_PlayerGetPushedBack
	waitmovement 0
	playse SE_WALL_HIT
	msgbox TwinleafTown_Text_BigThud, MSGBOX_DEFAULT
	applymovement LOCALID_TWINLEAF_RIVAL_DOOR, TwinleafTown_Movement_RivalNoticePlayer
	waitmovement 0
	msgbox TwinleafTown_Text_GoingToSeeProfRowan, MSGBOX_DEFAULT
	msgbox TwinleafTown_Text_OhJeezForgotSomething, MSGBOX_DEFAULT
	applymovement LOCALID_TWINLEAF_RIVAL_DOOR, TwinleafTown_Movement_RivalForgotSomething
	waitmovement 0
	@ O rival entrou de volta em casa: acende a MESMA flag que o inicio desta
	@ cena apagou (o campo `flag` do object_event no map.json), senao o
	@ `removeobject` so vale ate a proxima entrada no mapa e ele reaparece
	@ parado na porta para sempre. E a flag que a fonte usa neste objeto,
	@ FLAG_HIDE_TWINLEAF_TOWN_RIVAL.
	setflag FLAG_SINNOH_ESCONDE_TWINLEAF_TOWN_RIVAL
	removeobject LOCALID_TWINLEAF_RIVAL_DOOR
	setvar VAR_SINNOH_TWINLEAF_GUITARRISTA, 1
	setvar VAR_SINNOH_TWINLEAF_RIVAL, 1
	releaseall
	end

	.balign 4, 0
TwinleafTown_Movement_RivalBump:
	emote_exclamation_mark
	step_end

	.balign 4, 0
TwinleafTown_Movement_PlayerGetPushedBack:
	face_up
	delay_8
	step_end

	.balign 4, 0
TwinleafTown_Movement_RivalNoticePlayer:
	walk_in_place_fast_down
	step_end

	.balign 4, 0
TwinleafTown_Movement_RivalForgotSomething:
	emote_question_mark
	walk_up
	set_invisible
	step_end

@ Fonte: TwinleafTown_CoordEvent_RivalWasLookingForYou. O guitarrista corta o
@ caminho de quem tenta sair da cidade para o norte antes de falar com o
@ rival. ponytail: a fonte ramifica em 8 colunas (108-115) com movimento
@ exato por coluna; aqui o guitarrista faz uma unica aproximacao generica
@ (sobe ate a faixa do caminho, avisa, volta), mesmo efeito narrativo sem
@ replicar geometria que nao existe no nosso layout. VAR_VISITED_LAKE_VERITY_
@ WITH_RIVAL da fonte (variante de dialogo pos-Lago Verity) fica de fora: e
@ var interna sem endereco aqui (plano, apendice de vars), conteudo de leva
@ futura.
TwinleafTown_EventScript_CoordEvent_RivalWasLookingForYou::
	lockall
	applymovement LOCALID_TWINLEAF_GUITARIST, TwinleafTown_Movement_GuitaristIntercept
	waitmovement 0
	goto_if_set FLAG_SYS_POKEMON_GET, TwinleafTown_EventScript_EveryoneGoesOnAdventures
	goto_if_ge VAR_SINNOH_TWINLEAF_RIVAL, 1, TwinleafTown_EventScript_RivalWentTearingOff
	msgbox TwinleafTown_Text_RivalWasLookingForYou1, MSGBOX_DEFAULT
	applymovement LOCALID_TWINLEAF_GUITARIST, TwinleafTown_Movement_GuitaristWalkBack
	waitmovement 0
	releaseall
	end

TwinleafTown_EventScript_EveryoneGoesOnAdventures::
	msgbox TwinleafTown_Text_EveryoneGoesOnAdventures, MSGBOX_DEFAULT
	applymovement LOCALID_TWINLEAF_GUITARIST, TwinleafTown_Movement_GuitaristWalkBack
	waitmovement 0
	releaseall
	end

TwinleafTown_EventScript_RivalWentTearingOff::
	msgbox TwinleafTown_Text_RivalWentTearingOff, MSGBOX_DEFAULT
	applymovement LOCALID_TWINLEAF_GUITARIST, TwinleafTown_Movement_GuitaristWalkBack
	waitmovement 0
	releaseall
	end

	@ ROTA CONFERIDA CONTRA data/layouts/TwinleafTown/map.bin. O guitarrista
	@ mora em (9,10) e o `walk_up` direto batia em (9,9), que e o canto
	@ sudeste do bloco macico de (4..9, 6..9): ele nao saia do lugar e o
	@ `waitmovement` segurava a cena. Contornando pela coluna 10, que e livre
	@ de y=10 ate y=4: (9,10) -> (10,10) -> (10,9) -> (10,8), tres casas com
	@ colisao 0, sem objeto nem warp em cima. A volta desfaz o mesmo caminho.
	.balign 4, 0
TwinleafTown_Movement_GuitaristIntercept:
	walk_right
	walk_up
	walk_up
	emote_exclamation_mark
	step_end

	.balign 4, 0
TwinleafTown_Movement_GuitaristWalkBack:
	walk_down
	walk_down
	walk_left
	step_end

TwinleafTown_Text_BigThud:
	.string "Thud!!$"

TwinleafTown_Text_GoingToSeeProfRowan:
	.string "{RIVAL}: What was that about?!\p"
	.string "Oh, hey, {PLAYER}!\p"
	.string "Hey! I'm going to see Prof. Rowan!\n"
	.string "You should come, too! And quickly!$"

TwinleafTown_Text_OhJeezForgotSomething:
	.string "{RIVAL}: Oh, jeez!\n"
	.string "Forgot something!$"

TwinleafTown_Text_RivalWasLookingForYou1:
	.string "Hiya, {PLAYER}.\n"
	.string "{RIVAL} was looking for you.\p"
	.string "I think he's home now.\n"
	.string "Why don't you go check it out?$"

TwinleafTown_Text_RivalWentTearingOff:
	.string "Hiya, {PLAYER}.\n"
	.string "You're looking for {RIVAL}?\p"
	.string "He just went tearing off a little\n"
	.string "while ago.\p"
	.string "He's probably not gone too far.\n"
	.string "Why not go chase after him?$"

TwinleafTown_Text_EveryoneGoesOnAdventures:
	.string "Everyone goes off on adventures,\n"
	.string "and then they gradually grow up...$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

TwinleafTown_EventScript_Guitarist::
	lock
	faceplayer
	msgbox TwinleafTown_Text_Guitarist, MSGBOX_DEFAULT
	release
	end

@ Barry. Antes do inicial ele e quem manda o jogador para SANDGEM; depois,
@ ele ja foi embora e so provoca. Falas do Platinum, twinleaf_town.json e
@ twinleaf_town_player_house_2f.json.
TwinleafTown_EventScript_Rival::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEMON_GET, TwinleafTown_EventScript_RivalAfter
	msgbox TwinleafTown_Text_Rival, MSGBOX_DEFAULT
	release
	end

TwinleafTown_EventScript_RivalAfter::
	msgbox TwinleafTown_Text_RivalAfter, MSGBOX_DEFAULT
	release
	end

TwinleafTown_EventScript_TownSign::
	msgbox TwinleafTown_Text_TownSign, MSGBOX_SIGN
	end

TwinleafTown_Text_Guitarist:
	.string "Everyone goes off on adventures,\n"
	.string "and then they gradually grow up...$"

TwinleafTown_Text_Rival:
	.string "Hey, {PLAYER}!\p"
	.string "Did you just see the TV?\n"
	.string "Sure you did!\p"
	.string "PROF. ROWAN's that really important\n"
	.string "guy who studies POKéMON, right?\p"
	.string "That means he must have lots and\n"
	.string "lots of POKéMON.\p"
	.string "So, if we ask him, I bet he'd give\n"
	.string "us some POKéMON!\p"
	.string "We're going to go see PROF. ROWAN\n"
	.string "in SANDGEM TOWN, north of here.\p"
	.string "OK, {PLAYER}? If you're late, I'm\n"
	.string "fining you ¥10 million!$"

TwinleafTown_Text_RivalAfter:
	.string "How do you like that?\n"
	.string "PROF. ROWAN's really nice.\p"
	.string "On TV, he seems so stern and\n"
	.string "scary.$"

TwinleafTown_Text_TownSign:
	.string "TWINLEAF TOWN\n"
	.string "A Town Whose Leaves Are Always Fresh$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TwinleafTown_EventScript_Npc1::
	msgbox TwinleafTown_Text_Npc1, MSGBOX_NPC
	end

TwinleafTown_Text_Npc1:
	.string "It's true that wild Pokémon do attack\npeople sometimes...\pBut, Pokémon also open their hearts\nto you, so you can become friends.$"

TwinleafTown_EventScript_Npc2::
	msgbox TwinleafTown_Text_Npc2, MSGBOX_NPC
	end

TwinleafTown_Text_Npc2:
	.string "Technology just blows me away!\pI mean, now you can play with people\naround the world...wirelessly!$"

TwinleafTown_EventScript_Placa3::
	msgbox TwinleafTown_Text_Placa3, MSGBOX_SIGN
	end

TwinleafTown_Text_Placa3:
	.string "Twinleaf Town\nFresh and Free!$"
