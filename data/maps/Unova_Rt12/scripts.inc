@ Rt12 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5).
@
@ FONTE: fontes-mapas/bw3g/maps/Rt12.asm. TRES coord_events (9,7), (9,8) e
@ (9,9) caem no mesmo fecho `R12InferScript`: e a PRIMEIRA batalha do rival
@ (INFER), seguida da chegada do MARLON, da entrega da POKéDEX e das 5 POKé
@ BALLs. A ponte esta quebrada, e por isso a INFER esta encurralada aqui.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   VAR_UNOVA_R12_CENA: 0 = SCENE_DEFAULT, 1 = SCENE_FINISHED.
@   `setscene SCENE_FINISHED` -> `setvar VAR_UNOVA_R12_CENA, 1`.
@
@ EVENT_ da fonte -> FLAG_ da tabela:
@   EVENT_PLAYERS_HOUSE_1F_NEIGHBOR        -> FLAG_UNOVA_CASA_JOGADOR_VIZINHO
@   EVENT_PLAYERS_NEIGHBORS_HOUSE_NEIGHBOR -> FLAG_UNOVA_CASA_DO_VIZINHO_NPC
@ (a fonte faz `setevent` no primeiro e `clearevent` no segundo: o vizinho sai
@ da casa do jogador e aparece na casa dele.)
@
@ ELENCO, com zero flag nova (janela de save fechada): duas flags TEMPORARIAS,
@ recalculadas da var pelo ON_TRANSITION a cada entrada de mapa. O motor limpa
@ os FLAG_TEMP_* em `ClearTempFieldEventData()` (src/overworld.c:893) ANTES de
@ `RunOnTransitionMapScript()` (:909), e so depois nascem os objetos, olhando
@ `template->flagId` (src/event_object_movement.c:2920).
@   FLAG_TEMP_11 = a INFER; nasce so enquanto a cena nao rodou.
@   FLAG_TEMP_12 = o MARLON; NUNCA nasce sozinho (na fonte ele entra com
@                  `appear` no meio da cena). O `addobject` do roteiro cria o
@                  objeto mesmo com a flag acesa, porque `TrySpawnObjectEvent`
@                  nao consulta flag nenhuma (src/event_object_movement.c),
@                  quem consulta e so o nascimento em massa da entrada de mapa.
@
@ Ids locais (indice no map.json + 1): 1 = arvore, 2 = bola, 3 = YOUNGSTER,
@ 4 = LASS, 5 = POKEFAN_F, 6 = INFER, 7 = MARLON.
@
@ DESCARTADOS, com motivo:
@ - `writecode VAR_BATTLETYPE, BATTLETYPE_CANLOSE` e o ramo `.AfterYourDefeat`:
@   `trainerbattle_no_intro` nao volta ao roteiro quando o jogador perde (perder
@   e apagar), entao o galho de derrota fica inalcancavel. O texto
@   R12InferText_YouLost nao entrou por isso, e nao por corte de conteudo.
@ - `dontrestartmapmusic`, `reloadmap`, `setlasttalked`: mecanica de gen 2 que o
@   `trainerbattle_no_intro` ja resolve sozinho.
@ - `itemtotext` + `scall MarlonScript_ReceiveTheBalls` (`jumpstd receiveitem`) +
@   `itemnotify`: os quatro viram um `giveitem ITEM_POKE_BALL, 5`, que ja imprime
@   a mensagem e toca a fanfarra.
@ - `special FadeOutMusic` -> `special Script_FadeOutMapMusic` + `waitstate`;
@   `playmapmusic` -> `fadedefaultbgm`.
@ MUSICA: MUSIC_RIVAL_ENCOUNTER -> MUS_ENCOUNTER_MAY (a INFER e a rival);
@ MUSIC_MARLON_THEME -> MUS_ENCOUNTER_MALE. Nenhuma faixa nova foi criada.

Unova_Rt12_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_Rt12_OnTransition
	.byte 0

Unova_Rt12_OnTransition:
	setflag FLAG_TEMP_12
	goto_if_eq VAR_UNOVA_R12_CENA, 0, Unova_Rt12_EventScript_TransicaoFim
	setflag FLAG_TEMP_11
Unova_Rt12_EventScript_TransicaoFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Os tres gatilhos so mudam no caminho que o jogador faz ate a beira da ponte.
@ Rotas conferidas no map.bin de LAYOUT_UNOVA_R_12: os tres terminam em (7,9),
@ colisao 0 em todos os quadrantes do caminho.
Unova_Rt12_EventScript_R12InferTopScript::
	lockall
	applymovement LOCALID_PLAYER, Unova_Rt12_Movement_JogadorDeCima
	waitmovement 0
	goto Unova_Rt12_EventScript_R12InferScript

Unova_Rt12_EventScript_R12InferMidScript::
	lockall
	applymovement LOCALID_PLAYER, Unova_Rt12_Movement_JogadorDoMeio
	waitmovement 0
	goto Unova_Rt12_EventScript_R12InferScript

Unova_Rt12_EventScript_R12InferBotScript::
	lockall
	applymovement LOCALID_PLAYER, Unova_Rt12_Movement_JogadorDeBaixo
	waitmovement 0
	@ cai no proximo, como na fonte

@ `R12InferScript` da fonte, o fecho comum aos tres gatilhos.
Unova_Rt12_EventScript_R12InferScript::
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	msgbox Unova_Rt12_Text_R12InferBridge, MSGBOX_DEFAULT
	closemessage
	applymovement 6, Common_Movement_ExclamationMark
	waitmovement 0
	playbgm MUS_ENCOUNTER_MAY, FALSE
	turnobject 6, DIR_EAST
	msgbox Unova_Rt12_Text_R12InferFight, MSGBOX_DEFAULT
	closemessage
	goto Unova_Rt12_EventScript_BatalhaInfer1

@ O time da INFER muda com o inicial do jogador. A fonte escolhe pela cadeia
@ `checkevent EVENT_GOT_OSHAWOTT / EVENT_GOT_SNIVY`, e o rotulo do time nomeia
@ O POKEMON DELA: quem pegou OSHAWOTT enfrenta INFER1_SNIVY, quem pegou SNIVY
@ enfrenta INFER1_TEPIG e quem pegou TEPIG (o fallthrough da fonte) enfrenta
@ INFER1_OSHAWOTT. Ou seja, ela sempre fica com o inicial que GANHA do seu, ao
@ contrario da JUNIPER campea (ChampionsRoom), que fica com o que perde. Isto e
@ copia da fonte, nao escolha nova.
@ Aqui o galho e por VAR_STARTER_MON, que e quem guarda a escolha neste motor
@ (data/maps/Unova_NuvemaLab/scripts.inc: 0 = SNIVY, 1 = TEPIG, 2 = OSHAWOTT).
Unova_Rt12_EventScript_BatalhaInfer1::
	goto_if_eq VAR_STARTER_MON, 0, Unova_Rt12_EventScript_InferComTepig
	goto_if_eq VAR_STARTER_MON, 1, Unova_Rt12_EventScript_InferComOshawott
	trainerbattle_no_intro TRAINER_UNOVA_INFER1_SNIVY, Unova_Rt12_Text_R12InferWin
	goto Unova_Rt12_EventScript_DepoisDaInfer1

Unova_Rt12_EventScript_InferComTepig::
	trainerbattle_no_intro TRAINER_UNOVA_INFER1_TEPIG, Unova_Rt12_Text_R12InferWin
	goto Unova_Rt12_EventScript_DepoisDaInfer1

Unova_Rt12_EventScript_InferComOshawott::
	trainerbattle_no_intro TRAINER_UNOVA_INFER1_OSHAWOTT, Unova_Rt12_Text_R12InferWin
Unova_Rt12_EventScript_DepoisDaInfer1::
	playbgm MUS_ENCOUNTER_MAY, FALSE
	msgbox Unova_Rt12_Text_R12InferYouWon, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TAKE_DOWN
	applymovement LOCALID_PLAYER, Unova_Rt12_Movement_JogadorEmpurrado
	waitmovement 0
	turnobject LOCALID_PLAYER, DIR_EAST
	applymovement 6, Unova_Rt12_Movement_InferFoge
	waitmovement 0
	removeobject 6
	special Script_FadeOutMapMusic
	waitstate
	delay 30
	msgbox Unova_Rt12_Text_R12MarlonHey, MSGBOX_DEFAULT
	closemessage
	playbgm MUS_ENCOUNTER_MALE, FALSE
	addobject 7
	applymovement 7, Unova_Rt12_Movement_MarlonChega
	waitmovement 0
	msgbox Unova_Rt12_Text_R12MarlonGreeting, MSGBOX_DEFAULT
	closemessage
	applymovement 7, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox Unova_Rt12_Text_R12MarlonPackage, MSGBOX_DEFAULT
	closemessage
	msgbox Unova_Rt12_Text_R12GetDex, MSGBOX_DEFAULT
	closemessage
	playse SE_USE_ITEM
	waitse
	setflag FLAG_SYS_POKEDEX_GET
	msgbox Unova_Rt12_Text_R12MarlonPokedex, MSGBOX_DEFAULT
	closemessage
	giveitem ITEM_POKE_BALL, 5
	msgbox Unova_Rt12_Text_R12MarlonPokeballs, MSGBOX_DEFAULT
	closemessage
	applymovement 7, Unova_Rt12_Movement_MarlonSai
	waitmovement 0
	removeobject 7
	special HealPlayerParty
	setvar VAR_UNOVA_R12_CENA, 1
	setflag FLAG_UNOVA_CASA_JOGADOR_VIZINHO
	clearflag FLAG_UNOVA_CASA_DO_VIZINHO_NPC
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	fadedefaultbgm
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

@ `R12Infer_TopMovement`, `_MidMovement` e `_BotMovement` da fonte.
Unova_Rt12_Movement_JogadorDeCima:
	walk_down
	walk_down
	walk_left
	walk_left
	step_end

Unova_Rt12_Movement_JogadorDoMeio:
	walk_down
	walk_left
	walk_left
	step_end

Unova_Rt12_Movement_JogadorDeBaixo:
	walk_left
	walk_left
	step_end

@ `R12Infer_PushesYouMovement`: a INFER empurra o jogador para sair do caminho.
Unova_Rt12_Movement_JogadorEmpurrado:
	walk_fast_up
	face_down
	step_end

Unova_Rt12_Movement_InferFoge:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

Unova_Rt12_Movement_MarlonChega:
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Unova_Rt12_Movement_MarlonSai:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

Unova_Rt12_Text_R12InferBridge::
	.string "Darn! What a"
	.string "\nlousy time for"
	.string "\pthe bridge to"
	.string "\nbe out…$"

Unova_Rt12_Text_R12InferFight::
	.string "What? You again?"
	.string "\pI told you not"
	.string "\nto follow me!"
	.string "\pI guess I'll have"
	.string "\nto teach you a"
	.string "\llesson!$"

Unova_Rt12_Text_R12InferWin::
	.string "Darn… I wasn't"
	.string "\ngood enough.$"

Unova_Rt12_Text_R12InferYouWon::
	.string "Okay fine, you"
	.string "\ncan have the"
	.string "\ppackage I stole"
	.string "\nback."
	.string "\pIt wasn't even"
	.string "\nwhat I was"
	.string "\plooking for"
	.string "\nanyway!"
	.string "\pMy name is INFER."
	.string "\pRemember my name,"
	.string "\nI'm going to be"
	.string "\pthe strongest"
	.string "\nPOKéMON trainer"
	.string "\lin the world!"
	.string "\pDon't follow me!$"

Unova_Rt12_Text_R12MarlonHey::
	.string "{PLAYER}!$"

Unova_Rt12_Text_R12MarlonGreeting::
	.string "MARLON: Hey, that"
	.string "\nwas some battle!"
	.string "\pSorry I didn't"
	.string "\nstep in earlier,"
	.string "\pI saw ya battling"
	.string "\nand wanted to see"
	.string "\phow you'd hang in"
	.string "\nthere!"
	.string "\pI'm impressed!"
	.string "\nYou're a natural"
	.string "\lwith POKéMON!"
	.string "\pOh! That reminds"
	.string "\nme, I'd asked ya"
	.string "\pto swing by my"
	.string "\nplace today."
	.string "\pSee, ever since"
	.string "\nyou and your mom"
	.string "\pmoved out this"
	.string "\nway, I've had this"
	.string "\pfeelin' that you'd"
	.string "\nmake a pretty fine"
	.string "\lPOKéMON trainer,"
	.string "\pso I asked the"
	.string "\nPROF. to send over"
	.string "\psome POKéMON for"
	.string "\nyou to pick from."
	.string "\pLooks like my"
	.string "\nhunch was right!$"

Unova_Rt12_Text_R12MarlonPackage::
	.string "Oh! My package!"
	.string "\pThat's right! That"
	.string "\ngirl ran off with"
	.string "\pa package from my"
	.string "\nGYM, so I took off"
	.string "\pand tailed her"
	.string "\nhere."
	.string "\pLooks like you"
	.string "\nmanaged to get"
	.string "\lit back."
	.string "\pGo ahead, open"
	.string "\nit up!$"

Unova_Rt12_Text_R12GetDex::
	.string "{PLAYER} received"
	.string "\nPOKéDEX!$"

Unova_Rt12_Text_R12MarlonPokedex::
	.string "That's a POKéDEX!"
	.string "\pIt'll keep track"
	.string "\nof any POKéMON"
	.string "\lya come across!"
	.string "\pThe PROF. sent it"
	.string "\nfor ya along with"
	.string "\lthe POKéMON."
	.string "\pWonder what that"
	.string "\ngirl wanted with"
	.string "\lit…"
	.string "\pOh! And now that"
	.string "\nya have a POKé-"
	.string "\lDEX, you should"
	.string "\phave some of"
	.string "\nthese!$"

Unova_Rt12_Text_R12MarlonPokeballs::
	.string "You can use those"
	.string "\nto catch POKé-"
	.string "\lMON!"
	.string "\pWell, I think I'm"
	.string "\ngonna head on down"
	.string "\lto UNDELLA TOWN."
	.string "\pYou can get there"
	.string "\nby passin' through"
	.string "\pLACUNOSA TOWN, and"
	.string "\nthen just head"
	.string "\pSouth along the"
	.string "\nbeach on ROUTE 13."
	.string "\pI'll meet ya"
	.string "\nthere!$"

Unova_Rt12_EventScript_Placa0::
	msgbox Unova_Rt12_Text_R12SignText, MSGBOX_SIGN
	end

Unova_Rt12_EventScript_Placa1::
	msgbox Unova_Rt12_Text_R12BridgeSignText, MSGBOX_SIGN
	end

Unova_Rt12_EventScript_Npc2::
	msgbox Unova_Rt12_Text_R12YoungsterText, MSGBOX_NPC
	end

Unova_Rt12_EventScript_Npc3::
	msgbox Unova_Rt12_Text_R12LassText, MSGBOX_NPC
	end

Unova_Rt12_EventScript_Npc4::
	msgbox Unova_Rt12_Text_R12PokefanFText, MSGBOX_NPC
	end


Unova_Rt12_Text_R12SignText::
	.string "ROUTE 12"
	.string "\pWest to VILLAGE"
	.string "\nBRIDGE.$"

Unova_Rt12_Text_R12BridgeSignText::
	.string "VILLAGE BRIDGE"
	.string "\pPassage to"
	.string "\nOPELUCID CITY.$"

Unova_Rt12_Text_R12YoungsterText::
	.string "POKéMON battles"
	.string "\nbegin when eyes"
	.string "\lmeet!"
	.string "\pIf I were a POKé-"
	.string "\nMON trainer, you"
	.string "\pand I would be"
	.string "\nbattling now!"
	.string "\p…But I don't have"
	.string "\nany POKéMON yet…$"

Unova_Rt12_Text_R12LassText::
	.string "ROUTE 12 is a good"
	.string "\nplace to find"
	.string "\lwild POKéMON!"
	.string "\pI'm looking for"
	.string "\na SHROOMISH, or"
	.string "\lmaybe a RALTS!$"

Unova_Rt12_Text_R12PokefanFText::
	.string "This ROUTE is so"
	.string "\nnice! It's close"
	.string "\pto town, so I"
	.string "\ndon't have to"
	.string "\pworry about my"
	.string "\nPOKéMON fainting.$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ FRUITTREE_R_12 do BW3G. ponytail: no gen 2 a arvore reenche;
@ aqui a fruta sai uma vez, porque replantio e outra mecanica.
Unova_Rt12_EventScript_Arvore::
	lock
	goto_if_set FLAG_UNOVA_ARVORE_R_12, Unova_EventScript_GrutaVazia
	giveitem ITEM_ORAN_BERRY
	setflag FLAG_UNOVA_ARVORE_R_12
	release
	end
