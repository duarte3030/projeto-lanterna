@ ChampionsRoom do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 12/08/2026 (B5) e reescrito em 12/08/2026 (B6).
@
@ A SEGUNDA METADE DA CENA FINAL. A fonte e ChampionsRoom.asm, que tem QUATRO
@ `scene_script`. Aqui eles viram os quatro valores de VAR_UNOVA_LIGA_CENA
@ (include/constants/vars.h), lidos por MAP_SCRIPT_ON_FRAME_TABLE, que e o
@ equivalente do `priorityjump` de entrada de mapa do gen 2.
@
@ O QUE ENTROU, e e a cena inteira do estagio 0:
@   batalha contra o GENESIS (o `trainerbattle_single` solto que o B5 tinha posto
@   no objeto sai daqui e vira `trainerbattle_no_intro` DENTRO da cena), a
@   segunda batalha contra o GENESIS_MON SELVAGEM, a chegada da JUNIPER, as tres
@   sombras da Plasma, a troca do GENESIS pelo GENESECT, a cura, e a subida ao
@   Hall da Fama.
@
@ A BATALHA DE CAMPEA CONTRA A JUNIPER entrou junto, com os TRES treinadores que
@ a fonte exige, criados na faixa exclusiva 2520 a 2529 de include/constants/
@ opponents.h e com o time em src/data/trainers.party. Os tres sao identicos nos
@ cinco primeiros Pokemon e mudam so no sexto (SERPERIOR, EMBOAR ou SAMUROTT),
@ exatamente como em data/trainers/parties.asm do BW3G.
@
@ NIVEL DELES, de onde saiu: a fonte da 68, 69, 68, 70, 70 e 73, e a curva de
@ Unova ja aplicada ao GENESIS neste mesmo repo fixa 67 -> 253, 68 -> 253,
@ 69 -> 255 e 70 -> 255 (lido de src/data/trainers.party, nao recalculado, porque
@ rodar dev_scripts/curva_de_nivel.py de novo converteria DUAS VEZES o arquivo
@ inteiro). 73 fica acima de 70, entao bate no teto 255 (MAX_LEVEL).
@
@ NIVEL DA BATALHA SELVAGEM, de onde saiu: a fonte manda `loadwildmon
@ GENESIS_MON, 70`, e o GENESIS_MON da fonte reusa `gfx/pokemon/genesect` em
@ data/pokemon/base_stats/genesis.asm, ou seja E o GENESECT. O time do GENESIS na
@ fonte e 67 a 70 e aqui esta 253 a 255 (curva de Unova, dev_scripts/
@ curva_de_nivel.py), o que da 1 nivel daqui por 1 nivel de la; 70 cai em 256 e
@ o teto e 255. Por isso SPECIES_GENESECT nivel 255.
@
@ DUAS TROCAS DE MECANICA, com motivo:
@ 1. `returnfromcredits` nao existe neste motor. No BW3G o Hall da Fama volta
@    para esta sala depois dos creditos e o pos-creditos roda ali. Aqui
@    `special GameClear` roda os creditos e devolve o jogador ao ultimo ponto de
@    cura, entao o pos-creditos (estagio 3) roda na PROXIMA vez que o jogador
@    entrar nesta sala, que continua acessivel pelo elevador da estatua da
@    PkmnLeagueMain. O efeito e o mesmo: o GENESECT vai embora e a sala esvazia.
@ 2. `moveobject` do gen 2 e temporario; aqui o equivalente e `setobjectxyperm`
@    (grava no template), entao a JUNIPER e devolvida a (7,10) no fim da cena.
@
@ Ids locais (indice no map.json + 1):
@   1 = JUNIPER   2,3,4 = SOMBRAS   5 = GENESECT_2   6 = GENESECT_1   7 = GENESIS

Unova_ChampionsRoom_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_ChampionsRoom_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Unova_ChampionsRoom_OnFrame
	.byte 0

@ Quem nasce em cada estagio. Roda ANTES de InitMap(), que e quem cria os
@ object_events (tecnica 2 do SINNOH-PADRAO.md), entao acender a flag aqui basta
@ para o objeto nao nascer.
@ A JUNIPER fica escondida em TODO estagio: os quatro roteiros a trazem com
@ `clearflag` + `addobject`, que e o idioma vanilla equivalente ao `appear` do
@ gen 2, e a escondem de novo quando ela sai.
@ DEPENDENCIA COMPARTILHADA, anotada em 15/08/2026 (bloco A6), nao mexer aqui
@ sozinho: FLAG_UNOVA_CENA_JUNIPER passou a ser o MESMO bit em Unova_NuvemaLab,
@ Unova_P2LabEntrance, Unova_ChampionsRoom, Unova_UndellaTown (lá esconde o
@ MARLON da cena de chegada), Unova_CasteliaCityStreets (lá esconde o CHEREN
@ da cena da insígnia), Unova_FloccesyTown (JUNIPER), Unova_NacreneCity
@ (LENORA) e Unova_PWTOutside (CHEREN e BIANCA juntos, que sempre escondem
@ sob a mesma condição), porque `disappear`/`appear` desses NPCs de cena
@ nao tem FLAG_ propria na tabela do
@ PLANO-OBRAS-UNOVA.md e a janela de save estava fechada. Os três últimos
@ entraram em 16/08/2026: eles usavam ON_LOAD + `removeobject`, que é no-op
@ (ON_LOAD roda dentro de InitMap(), src/fieldmap.c:135-140, ANTES de
@ InitObjectEventsLocal() criar os objetos), e o NPC renascia a cada
@ reentrada. O contrato que faz
@ isso funcionar e "todo mapa que usa o bit o REESCREVE no seu proprio
@ ON_TRANSITION, antes de os objetos nascerem" (o `setflag` logo abaixo e a
@ ponta deste mapa). Quem tirar ou condicionar essa escrita em UM dos oito
@ quebra os outros sete. Mudou um, confira os oito.
Unova_ChampionsRoom_OnTransition:
	setflag FLAG_UNOVA_CENA_JUNIPER
	setflag FLAG_UNOVA_CENA_SOMBRAS
	setflag FLAG_UNOVA_CENA_GENESECT_1
	setflag FLAG_UNOVA_CENA_GENESECT_2
	clearflag FLAG_UNOVA_CENA_GENESIS
	goto_if_eq VAR_UNOVA_LIGA_CENA, 0, Unova_ChampionsRoom_EventScript_TransicaoFim
	@ dai em diante o GENESIS ja caiu
	setflag FLAG_UNOVA_CENA_GENESIS
	@ na revanche (estagio 2) a sala esta vazia: `.ChampionBattleScript` da fonte
	@ comeca com `disappear` nos dois GENESECT
	goto_if_eq VAR_UNOVA_LIGA_CENA, 2, Unova_ChampionsRoom_EventScript_TransicaoFim
	clearflag FLAG_UNOVA_CENA_GENESECT_1
Unova_ChampionsRoom_EventScript_TransicaoFim::
	end

Unova_ChampionsRoom_OnFrame:
	map_script_2 VAR_UNOVA_LIGA_CENA, 0, Unova_ChampionsRoom_EventScript_CenaGenesis
	map_script_2 VAR_UNOVA_LIGA_CENA, 1, Unova_ChampionsRoom_EventScript_CenaJuniper
	map_script_2 VAR_UNOVA_LIGA_CENA, 2, Unova_ChampionsRoom_EventScript_Revanche
	map_script_2 VAR_UNOVA_LIGA_CENA, 3, Unova_ChampionsRoom_EventScript_PosCreditos
	.2byte 0

@ ---------------------------------------------------------------- estagio 0
@ `.GenesisFightScript` da fonte, inteiro.
Unova_ChampionsRoom_EventScript_CenaGenesis::
	lockall
	delay 15
	applymovement LOCALID_PLAYER, Unova_ChampionsRoom_Movement_JogadorSobe
	waitmovement 0
	delay 60
	playmoncry SPECIES_GENESECT, CRY_MODE_NORMAL
	waitmoncry
	turnobject 7, DIR_SOUTH
	delay 30
	applymovement 7, Unova_ChampionsRoom_Movement_GenesisDesce
	waitmovement 0
	playmoncry SPECIES_GENESECT, CRY_MODE_NORMAL
	waitmoncry
	msgbox Unova_ChampionsRoom_Text_GenesisRuge, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_UNOVA_CHAMPION_GENESIS, Unova_ChampionsRoom_Text_GenesisDerrotado
	@ a segunda batalha: o proprio GENESIS_MON, selvagem
	playmoncry SPECIES_GENESECT, CRY_MODE_NORMAL
	waitmoncry
	msgbox Unova_ChampionsRoom_Text_GenesisRuge, MSGBOX_DEFAULT
	closemessage
	setwildbattle SPECIES_GENESECT, 255
	dowildbattle
	setflag FLAG_UNOVA_GENESIS_VENCIDO
	playmoncry SPECIES_GENESECT, CRY_MODE_NORMAL
	waitmoncry
	msgbox Unova_ChampionsRoom_Text_GenesisRuge, MSGBOX_DEFAULT
	closemessage
	playse SE_PC_OFF
	waitse
	delay 60
	@ a JUNIPER entra pela porta do sul, entao o template dela vai para (7,18)
	setobjectxyperm 1, 7, 18
	clearflag FLAG_UNOVA_CENA_JUNIPER
	playse SE_DOOR
	addobject 1
	waitse
	playbgm MUS_ENCOUNTER_MAY, FALSE
	turnobject LOCALID_PLAYER, DIR_SOUTH
	delay 15
	applymovement 1, Unova_ChampionsRoom_Movement_JuniperSobe
	waitmovement 0
	msgbox Unova_ChampionsRoom_Text_JuniperViuTudo, MSGBOX_DEFAULT
	closemessage
	playse SE_DOOR
	applymovement LOCALID_PLAYER, Unova_ChampionsRoom_Movement_JogadorSaiDoCaminho
	applymovement 1, Unova_ChampionsRoom_Movement_JuniperSaiDoCaminho
	waitmovement 0
	clearflag FLAG_UNOVA_CENA_SOMBRAS
	addobject 2
	applymovement 2, Unova_ChampionsRoom_Movement_SombraEsquerda
	playse SE_DOOR
	addobject 3
	waitse
	applymovement 3, Unova_ChampionsRoom_Movement_SombraDireita
	playse SE_DOOR
	addobject 4
	waitse
	applymovement 4, Unova_ChampionsRoom_Movement_SombraCentro
	waitmovement 0
	msgbox Unova_ChampionsRoom_Text_SombrasDerrotadas, MSGBOX_DEFAULT
	closemessage
	playse SE_PC_LOGIN
	fadescreenspeed FADE_TO_BLACK, 8
	clearflag FLAG_UNOVA_CENA_GENESECT_1
	addobject 6
	setflag FLAG_UNOVA_CENA_GENESIS
	removeobject 7
	turnobject LOCALID_PLAYER, DIR_SOUTH
	fadescreenspeed FADE_FROM_BLACK, 8
	waitse
	msgbox Unova_ChampionsRoom_Text_SombrasVaoEmbora, MSGBOX_DEFAULT
	closemessage
	playse SE_WARP_OUT
	removeobject 2
	waitse
	playse SE_WARP_OUT
	removeobject 3
	waitse
	playse SE_WARP_OUT
	removeobject 4
	waitse
	setflag FLAG_UNOVA_CENA_SOMBRAS
	turnobject LOCALID_PLAYER, DIR_EAST
	turnobject 1, DIR_WEST
	msgbox Unova_ChampionsRoom_Text_JuniperCura, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_ChampionsRoom_Movement_JuniperUmPassoEsquerda
	waitmovement 0
	playse SE_USE_ITEM
	special HealPlayerParty
	waitse
	msgbox Unova_ChampionsRoom_Text_PrimeiroDesafioJuniper, MSGBOX_DEFAULT
	closemessage
	setobjectxyperm 1, 7, 10
	setvar VAR_UNOVA_LIGA_CENA, 1
	goto Unova_ChampionsRoom_EventScript_BatalhaCampea

@ ---------------------------------------------------------------- estagio 1
@ `.JuniperFightScript` da fonte: o jogador perdeu para a JUNIPER e voltou. O
@ GENESECT continua no meio da sala, e por isso o roteiro de movimento da fonte
@ CONTORNA ele em vez de subir reto.
Unova_ChampionsRoom_EventScript_CenaJuniper::
	lockall
	clearflag FLAG_UNOVA_CENA_JUNIPER
	addobject 1
	delay 15
	applymovement LOCALID_PLAYER, Unova_ChampionsRoom_Movement_JogadorContornaGenesect
	applymovement 1, Unova_ChampionsRoom_Movement_JuniperDesceUmPasso
	waitmovement 0
	msgbox Unova_ChampionsRoom_Text_DesafioJuniper, MSGBOX_DEFAULT
	closemessage
	goto Unova_ChampionsRoom_EventScript_BatalhaCampea

@ ---------------------------------------------------------------- estagio 2
@ `.ChampionBattleScript` da fonte: a revanche, ja com o Hall da Fama feito. A
@ sala esta vazia (o ON_TRANSITION nao acende nenhum GENESECT neste estagio), e
@ o jogador sobe reto.
Unova_ChampionsRoom_EventScript_Revanche::
	lockall
	clearflag FLAG_UNOVA_CENA_JUNIPER
	addobject 1
	delay 15
	applymovement LOCALID_PLAYER, Unova_ChampionsRoom_Movement_JogadorSobe
	waitmovement 0
	msgbox Unova_ChampionsRoom_Text_DesafioJuniper, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_ChampionsRoom_Movement_JuniperDesceUmPasso
	applymovement LOCALID_PLAYER, Unova_ChampionsRoom_Movement_JogadorSobeUmPasso
	waitmovement 0
	@ cai no proximo

@ ------------------------------------------------- a batalha de campea, comum
@ `StartChampionBattleScript` da fonte. O time da JUNIPER muda com o inicial do
@ jogador, e o rotulo da fonte nomeia O POKEMON DELA: quem pegou SNIVY enfrenta
@ JUNIPER_OSHAWOTT (Samurott), quem pegou TEPIG enfrenta JUNIPER_SNIVY
@ (Serperior) e quem pegou OSHAWOTT enfrenta JUNIPER_TEPIG (Emboar), ou seja ela
@ sempre fica com o inicial que PERDE para o seu. Isto e copia da cadeia
@ `checkevent EVENT_GOT_SNIVY / EVENT_GOT_TEPIG` da fonte, nao escolha minha.
@ DECIDIDO em 12/08/2026, nao relitigar: fica como a fonte, pela politica de
@ "portar, nao escrever enredo novo" (secao 2 do PRD-ROM-COMPLETA.md e decisao 69
@ do ESTADO.md). O espelho (jogador planta -> JUNIPER com SERPERIOR) foi
@ considerado e recusado; quem quiser mesmo assim troca as tres linhas de
@ `goto_if_eq` abaixo, e este paragrafo e a documentacao da alternativa.
@ VAR_STARTER_MON e escrita por data/maps/Unova_NuvemaLab/scripts.inc:
@ 0 = SNIVY, 1 = TEPIG, 2 = OSHAWOTT.
Unova_ChampionsRoom_EventScript_BatalhaCampea::
	goto_if_eq VAR_STARTER_MON, 0, Unova_ChampionsRoom_EventScript_CampeaComSamurott
	goto_if_eq VAR_STARTER_MON, 1, Unova_ChampionsRoom_EventScript_CampeaComSerperior
	trainerbattle_no_intro TRAINER_UNOVA_CHAMPION_JUNIPER_TEPIG, Unova_ChampionsRoom_Text_JuniperDerrotada
	goto Unova_ChampionsRoom_EventScript_DepoisDaCampea

Unova_ChampionsRoom_EventScript_CampeaComSamurott::
	trainerbattle_no_intro TRAINER_UNOVA_CHAMPION_JUNIPER_OSHAWOTT, Unova_ChampionsRoom_Text_JuniperDerrotada
	goto Unova_ChampionsRoom_EventScript_DepoisDaCampea

Unova_ChampionsRoom_EventScript_CampeaComSerperior::
	trainerbattle_no_intro TRAINER_UNOVA_CHAMPION_JUNIPER_SNIVY, Unova_ChampionsRoom_Text_JuniperDerrotada
Unova_ChampionsRoom_EventScript_DepoisDaCampea::
	setvar VAR_UNOVA_LIGA_CENA, 2
	msgbox Unova_ChampionsRoom_Text_VenhaComigo, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_ChampionsRoom_Movement_JuniperSaiPeloNorte
	waitmovement 0
	playse SE_WARP_OUT
	setflag FLAG_UNOVA_CENA_JUNIPER
	removeobject 1
	waitse
	fadedefaultbgm
	warp MAP_UNOVA_HALL_OF_FAME, 4, 13
	waitstate
	releaseall
	end

@ ---------------------------------------------------------------- estagio 3
@ `.PostCreditsSceneScript` da fonte. O `disappear PLAYER` do gen 2 fica de fora
@ de proposito: la o jogador chega teleportado pelos creditos e nao esta na sala;
@ aqui ele entra andando, e esconder o proprio jogador so o deixaria invisivel
@ sobre um mapa em que ele ainda anda.
Unova_ChampionsRoom_EventScript_PosCreditos::
	lockall
	delay 60
	playse SE_PC_LOGIN
	clearflag FLAG_UNOVA_CENA_GENESECT_2
	addobject 5
	turnobject 5, DIR_SOUTH
	delay 5
	setflag FLAG_UNOVA_CENA_GENESECT_1
	removeobject 6
	waitse
	delay 60
	playmoncry SPECIES_GENESECT, CRY_MODE_NORMAL
	waitmoncry
	delay 60
	playse SE_WARP_IN
	applymovement 5, Unova_ChampionsRoom_Movement_GenesectVaiEmbora
	waitmovement 0
	setflag FLAG_UNOVA_CENA_GENESECT_2
	removeobject 5
	waitse
	delay 60
	setvar VAR_UNOVA_LIGA_CENA, 2
	releaseall
	end

Unova_ChampionsRoom_Movement_JogadorSobe:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

Unova_ChampionsRoom_Movement_GenesisDesce:
	walk_slow_down
	walk_slow_down
	step_end

Unova_ChampionsRoom_Movement_JuniperSobe:
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

Unova_ChampionsRoom_Movement_JogadorSaiDoCaminho:
	walk_left
	walk_up
	walk_up
	face_down
	step_end

Unova_ChampionsRoom_Movement_JuniperSaiDoCaminho:
	walk_right
	walk_up
	walk_up
	walk_up
	face_down
	step_end

Unova_ChampionsRoom_Movement_SombraEsquerda:
	walk_up
	walk_up
	walk_up
	walk_left
	face_up
	step_end

Unova_ChampionsRoom_Movement_SombraDireita:
	walk_up
	walk_up
	walk_up
	walk_right
	face_up
	step_end

Unova_ChampionsRoom_Movement_SombraCentro:
	walk_up
	walk_up
	walk_up
	step_end

Unova_ChampionsRoom_Movement_JuniperUmPassoEsquerda:
	walk_left
	step_end

Unova_ChampionsRoom_Movement_JogadorContornaGenesect:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_left
	walk_up
	walk_up
	face_right
	step_end

Unova_ChampionsRoom_Movement_JuniperDesceUmPasso:
	walk_down
	face_left
	step_end

Unova_ChampionsRoom_Movement_JogadorSobeUmPasso:
	walk_up
	step_end

Unova_ChampionsRoom_Movement_JuniperSaiPeloNorte:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

Unova_ChampionsRoom_Movement_GenesectVaiEmbora:
	slide_up
	slide_up
	slide_up
	slide_up
	step_end

Unova_ChampionsRoom_Text_GenesisRuge::
	.string "Graaahhh!$"

Unova_ChampionsRoom_Text_GenesisDerrotado::
	.string "…$"

Unova_ChampionsRoom_Text_JuniperViuTudo::
	.string "JUNIPER: {PLAYER}, you've done\n"
	.string "it!$"

Unova_ChampionsRoom_Text_SombrasDerrotadas::
	.string "SHADOW: N-no! This can't be!\p"
	.string "SHADOW: Our king has been…\p"
	.string "JUNIPER: Your monster has been\n"
	.string "stopped, thanks to {PLAYER}.\p"
	.string "SHADOW: …\p"
	.string "It wasn't supposed to be this\n"
	.string "way…\p"
	.string "Lord GHETSIS was supposed to\n"
	.string "lead us… Be our king again…\p"
	.string "He was supposed to claim his\n"
	.string "rightful throne and usher in a\l"
	.string "new era for TEAM PLASMA…\p"
	.string "So why…?\p"
	.string "Why did it turn out this way?!\p"
	.string "JUNIPER: That thing is not your\n"
	.string "king. It's a POKéMON that you've\l"
	.string "turned into a mindless tool of\l"
	.string "destruction.\p"
	.string "SHADOW: …\p"
	.string "Perhaps…\p"
	.string "Perhaps you are right…\p"
	.string "Perhaps it is the case that we\n"
	.string "cannot…\p"
	.string "Bring him back…\p"
	.string "… … … …\p"
	.string "Come, brothers. Let us…\n"
	.string "take him back…$"

Unova_ChampionsRoom_Text_SombrasVaoEmbora::
	.string "SHADOW: We will leave the MIND\n"
	.string "LINK here with you. We…\p"
	.string "We have no need for it anymore…\p"
	.string "He…\p"
	.string "He really isn't coming back…\p"
	.string "TEAM PLASMA truly is finished\n"
	.string "now.\p"
	.string "Without our king by our side,\n"
	.string "there is no point in going on…\p"
	.string "Let us make our final departure\n"
	.string "now, brothers.$"

Unova_ChampionsRoom_Text_JuniperCura::
	.string "JUNIPER: Wow, {PLAYER}! You were\n"
	.string "excellent!\p"
	.string "You've not only defeated the\n"
	.string "ELITE FOUR, you've also stopped\l"
	.string "that thing from wreaking havoc\l"
	.string "across UNOVA!\p"
	.string "I knew from the look in your\n"
	.string "eyes when we first met in\l"
	.string "FLOCCESY TOWN that you were\l"
	.string "going to be a great trainer.\p"
	.string "But first, allow me to heal your\n"
	.string "POKéMON.$"

Unova_ChampionsRoom_Text_VenhaComigo::
	.string "Well done, {PLAYER}!\p"
	.string "You certainly are an unmatched\n"
	.string "talent!\p"
	.string "Please, come with me.$"

Unova_ChampionsRoom_Text_PrimeiroDesafioJuniper::
	.string "Now then, {PLAYER}.\p"
	.string "As CHAMPION of the UNOVA region,\n"
	.string "I, AUREA JUNIPER, accept your\l"
	.string "challenge!$"

Unova_ChampionsRoom_Text_DesafioJuniper::
	.string "You've done well to make it back\n"
	.string "here, {PLAYER}.\p"
	.string "Now as CHAMPION of the UNOVA\n"
	.string "region, I, AUREA JUNIPER, accept\l"
	.string "your challenge!$"

Unova_ChampionsRoom_Text_JuniperDerrotada::
	.string "After this battle, a fresh wind\n"
	.string "has blown through my heart…\p"
	.string "Today, you and your partners are\n"
	.string "CHAMPIONS!$"
