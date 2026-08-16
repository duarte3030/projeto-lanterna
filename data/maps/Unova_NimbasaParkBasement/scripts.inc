@ NimbasaParkBasement do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5).
@
@ FONTE: fontes-mapas/bw3g/maps/NimbasaParkBasement.asm. QUATRO coord_events em
@ DUAS cenas, cada cena com dois gatilhos lado a lado que caem no mesmo fecho:
@   (6,2) e (6,3), valor 0  -> a TERCEIRA batalha do rival (INFER);
@   (4,16) e (5,16), valor 1 -> a Plasma no fundo do porao: o SABIO GIALLO, uma
@   SOMBRA e o CHEREN. O CHEREN segura a SOMBRA e o jogador enfrenta o SABIO.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   VAR_UNOVA_NIMBASA_PARK_PORAO_CENA: 0 = SCENE_NIMBASA_PARK_BASEMENT_INFER,
@   1 = ..._PLASMA, 2 = ..._NOTHING.
@
@ O setmapscene REMOTO, que e o ponto delicado deste mapa:
@   `setmapscene NIMBASA_PARK_OUTSIDE, SCENE_NIMBASA_PARK_OUTSIDE_AFTER`
@   -> `setvar VAR_UNOVA_NIMBASA_PARK_FORA_CENA, 2`
@   O valor 2 sai da tabela do PLANO (0 = SCENE_DEFAULT, 1 = ..._CHEREN,
@   2 = ..._AFTER, 3 = ..._NOTHING), nao foi inventado aqui. Ele arma a cena do
@   lado de FORA do parque, para onde o `warp` do fim desta cena joga o jogador,
@   e por isso tem que ser gravado ANTES do warp. Os dois gatilhos de (4,16) e
@   (5,16) chegam nesta linha, entao o setvar remoto tem DOIS caminhos ate ele.
@   O outro `setmapscene NIMBASA_PARK_OUTSIDE` da fonte inteira mora em
@   CasteliaCityStreets (valor ..._CHEREN) e e do bloco A4, nao deste.
@
@ EVENT_ da fonte -> FLAG_ da tabela:
@   EVENT_NIMBASA_PARK_GRUNTS       -> FLAG_UNOVA_NIMBASA_PARK_GRUNTS
@   EVENT_NIMBASA_PARK_HIDDEN_GRUNT -> FLAG_UNOVA_NIMBASA_PARK_GRUNT_ESCONDIDO
@
@ ELENCO, zero flag nova (janela de save fechada): duas flags TEMPORARIAS
@ recalculadas da var pelo ON_TRANSITION. O motor limpa os FLAG_TEMP_* em
@ `ClearTempFieldEventData()` (src/overworld.c:893) ANTES do
@ `RunOnTransitionMapScript()` (:909) e os objetos so nascem depois, olhando
@ `template->flagId` (src/event_object_movement.c:2920).
@   FLAG_TEMP_11 = a INFER; nasce so no estagio 0.
@   FLAG_TEMP_12 = GIALLO, CHEREN e a SOMBRA; nascem nos estagios 0 e 1 (a
@                  fonte nunca faz `appear` neles) e somem no 2.
@
@ Ids locais (indice no map.json + 1): 1 = INFER, 2 = GIALLO, 3 = CHEREN,
@ 4 = SOMBRA.
@
@ DESCARTADOS: `setlasttalked`, `dontrestartmapmusic` e `reloadmapafterbattle`
@ (cobertos pelo `trainerbattle_no_intro`); `special ReloadSpritesNoPalettes`
@ (nao existe equivalente e nada aqui troca palette); `playmusic MUSIC_SEWERS`
@ vira `fadedefaultbgm`, porque a faixa do porao ja e a musica deste mapa.
@ FADES: `special FadeOutMusic` -> `special Script_FadeOutMapMusic` +
@ `waitstate`; `FadeBlackQuickly` -> `fadescreenspeed FADE_TO_BLACK, 8`;
@ `FadeInQuickly` -> `fadescreenspeed FADE_FROM_BLACK, 8`; `FadeOutPalettes`
@ (o fade antes do warp) -> `fadescreen FADE_TO_BLACK`.
@ MUSICA: MUSIC_RIVAL_ENCOUNTER -> MUS_ENCOUNTER_MAY; MUSIC_ROCKET_ENCOUNTER ->
@ MUS_ENCOUNTER_AQUA.
@ ROTAS DO JOGADOR conferidas no map.bin de LAYOUT_UNOVA_NIMBASA_PARK_BASEMENT:
@ (4,16)->(4,15)->(4,14)->(5,14)->(5,13)->(5,12) e (5,16)->(4,16)->... , todos
@ com colisao 0; o empurrao da INFER sobe de (6,2) para (6,1), tambem livre.

Unova_NimbasaParkBasement_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_NimbasaParkBasement_OnTransition
	.byte 0

Unova_NimbasaParkBasement_OnTransition:
	goto_if_eq VAR_UNOVA_NIMBASA_PARK_PORAO_CENA, 0, Unova_NimbasaParkBasement_EventScript_TransicaoFim
	setflag FLAG_TEMP_11
	goto_if_eq VAR_UNOVA_NIMBASA_PARK_PORAO_CENA, 1, Unova_NimbasaParkBasement_EventScript_TransicaoFim
	setflag FLAG_TEMP_12
Unova_NimbasaParkBasement_EventScript_TransicaoFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Estagio 0, gatilho de (6,2). A fonte vira o jogador para a esquerda aqui e
@ NAO vira no gatilho de baixo; ficou como esta.
Unova_NimbasaParkBasement_EventScript_NimbasaParkInferScript1::
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	playse SE_DOOR
	waitse
	delay 15
	turnobject LOCALID_PLAYER, DIR_WEST
	playbgm MUS_ENCOUNTER_MAY, FALSE
	applymovement 1, Unova_NimbasaParkBasement_Movement_InferChegaDeCima
	waitmovement 0
	goto Unova_NimbasaParkBasement_EventScript_NimbasaParkInferScript

@ Estagio 0, gatilho de (6,3).
Unova_NimbasaParkBasement_EventScript_NimbasaParkInferScript2::
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	playse SE_DOOR
	waitse
	delay 15
	playbgm MUS_ENCOUNTER_MAY, FALSE
	applymovement 1, Unova_NimbasaParkBasement_Movement_InferChegaDeBaixo
	waitmovement 0
	@ cai no proximo, como na fonte

Unova_NimbasaParkBasement_EventScript_NimbasaParkInferScript::
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkInferIntro, MSGBOX_DEFAULT
	closemessage
	goto Unova_NimbasaParkBasement_EventScript_BatalhaInfer3

@ Mesmo galho por inicial das batalhas anteriores (Rt12 e LostlornForest): a
@ fonte manda `checkevent EVENT_GOT_OSHAWOTT -> INFER3_SNIVY`,
@ `checkevent EVENT_GOT_SNIVY -> INFER3_TEPIG`, fallthrough (TEPIG) ->
@ INFER3_OSHAWOTT. Aqui o galho e por VAR_STARTER_MON (0 = SNIVY, 1 = TEPIG,
@ 2 = OSHAWOTT, escrito por data/maps/Unova_NuvemaLab/scripts.inc).
Unova_NimbasaParkBasement_EventScript_BatalhaInfer3::
	goto_if_eq VAR_STARTER_MON, 0, Unova_NimbasaParkBasement_EventScript_InferComTepig
	goto_if_eq VAR_STARTER_MON, 1, Unova_NimbasaParkBasement_EventScript_InferComOshawott
	trainerbattle_no_intro TRAINER_UNOVA_INFER3_SNIVY, Unova_NimbasaParkBasement_Text_NimbasaParkInferWin
	goto Unova_NimbasaParkBasement_EventScript_DepoisDaInfer3

Unova_NimbasaParkBasement_EventScript_InferComTepig::
	trainerbattle_no_intro TRAINER_UNOVA_INFER3_TEPIG, Unova_NimbasaParkBasement_Text_NimbasaParkInferWin
	goto Unova_NimbasaParkBasement_EventScript_DepoisDaInfer3

Unova_NimbasaParkBasement_EventScript_InferComOshawott::
	trainerbattle_no_intro TRAINER_UNOVA_INFER3_OSHAWOTT, Unova_NimbasaParkBasement_Text_NimbasaParkInferWin
Unova_NimbasaParkBasement_EventScript_DepoisDaInfer3::
	playbgm MUS_ENCOUNTER_MAY, FALSE
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkInferAfter, MSGBOX_DEFAULT
	closemessage
	playse SE_M_TAKE_DOWN
	applymovement LOCALID_PLAYER, Unova_NimbasaParkBasement_Movement_JogadorEmpurrado
	waitmovement 0
	turnobject LOCALID_PLAYER, DIR_EAST
	applymovement 1, Unova_NimbasaParkBasement_Movement_InferSai
	waitmovement 0
	removeobject 1
	playse SE_DOOR
	waitse
	special Script_FadeOutMapMusic
	waitstate
	delay 30
	fadedefaultbgm
	setvar VAR_UNOVA_NIMBASA_PARK_PORAO_CENA, 1
	releaseall
	end

@ Estagio 1, gatilho de (4,16).
Unova_NimbasaParkBasement_EventScript_NimbasaParkPlasmaScript1::
	lockall
	applymovement LOCALID_PLAYER, Unova_NimbasaParkBasement_Movement_JogadorSobeUmPasso
	waitmovement 0
	goto Unova_NimbasaParkBasement_EventScript_NimbasaParkPlasmaScript

@ Estagio 1, gatilho de (5,16).
Unova_NimbasaParkBasement_EventScript_NimbasaParkPlasmaScript2::
	lockall
	applymovement LOCALID_PLAYER, Unova_NimbasaParkBasement_Movement_JogadorEntraNoPorao
	waitmovement 0
	@ cai no proximo, como na fonte

Unova_NimbasaParkBasement_EventScript_NimbasaParkPlasmaScript::
	turnobject 2, DIR_SOUTH
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkGialloIntro, MSGBOX_DEFAULT
	closemessage
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkCherenBasementIntro, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Unova_NimbasaParkBasement_Movement_JogadorSobeUmPasso
	applymovement 4, Unova_NimbasaParkBasement_Movement_SombraInterrompe
	waitmovement 0
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkShadowProtect, MSGBOX_DEFAULT
	closemessage
	applymovement 3, Unova_NimbasaParkBasement_Movement_CherenEntra
	waitmovement 0
	turnobject 3, DIR_EAST
	turnobject 4, DIR_WEST
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkCherenFightShadow, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_PLAYER, Unova_NimbasaParkBasement_Movement_JogadorEncaraGiallo
	waitmovement 0
	turnobject 2, DIR_EAST
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkGialloStartFight, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_UNOVA_GIALLO1, Unova_NimbasaParkBasement_Text_NimbasaParkGialloBeaten
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkGialloAfter, MSGBOX_DEFAULT
	closemessage
	turnobject 4, DIR_NORTH
	turnobject 2, DIR_SOUTH
	special Script_FadeOutMapMusic
	waitstate
	fadescreenspeed FADE_TO_BLACK, 8
	delay 15
	playse SE_WARP_OUT
	waitse
	removeobject 4
	removeobject 2
	delay 15
	fadescreenspeed FADE_FROM_BLACK, 8
	fadedefaultbgm
	delay 15
	applymovement 3, Unova_NimbasaParkBasement_Movement_CherenSeAproxima
	waitmovement 0
	msgbox Unova_NimbasaParkBasement_Text_NimbasaParkCherenAfter, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_NIMBASA_PARK_PORAO_CENA, 2
	setflag FLAG_UNOVA_NIMBASA_PARK_GRUNTS
	setflag FLAG_UNOVA_NIMBASA_PARK_GRUNT_ESCONDIDO
	@ setmapscene remoto: arma a cena do lado de fora do parque
	setvar VAR_UNOVA_NIMBASA_PARK_FORA_CENA, 2
	fadescreen FADE_TO_BLACK
	playse SE_DOOR
	waitse
	removeobject 3
	warp MAP_UNOVA_NIMBASA_PARK_OUTSIDE, 41, 8
	waitstate
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_NimbasaParkBasement_Movement_InferChegaDeCima:
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

Unova_NimbasaParkBasement_Movement_InferChegaDeBaixo:
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

@ `NimbasaParkPushedMovement`: a INFER empurra o jogador ao sair.
Unova_NimbasaParkBasement_Movement_JogadorEmpurrado:
	walk_fast_up
	face_down
	step_end

Unova_NimbasaParkBasement_Movement_InferSai:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

@ `NimbasaParkApproachGialloMovement`: usado DUAS vezes na fonte, uma no gatilho
@ de (4,16) e outra dentro do fecho comum.
Unova_NimbasaParkBasement_Movement_JogadorSobeUmPasso:
	walk_up
	step_end

Unova_NimbasaParkBasement_Movement_JogadorEntraNoPorao:
	walk_left
	walk_up
	step_end

Unova_NimbasaParkBasement_Movement_JogadorEncaraGiallo:
	walk_right
	walk_up
	walk_up
	face_left
	step_end

Unova_NimbasaParkBasement_Movement_SombraInterrompe:
	walk_fast_right
	face_down
	step_end

Unova_NimbasaParkBasement_Movement_CherenEntra:
	walk_up
	walk_up
	step_end

Unova_NimbasaParkBasement_Movement_CherenSeAproxima:
	walk_up
	walk_right
	step_end

Unova_NimbasaParkBasement_Text_NimbasaParkInferIntro::
	.string "INFER: You! What"
	.string "\nare you doing"
	.string "\lhere?"
	.string "\pTEAM PLASMA? I"
	.string "\nthought I told you"
	.string "\pnot to mess around"
	.string "\nwith TEAM PLASMA."
	.string "\pWhat am I doing"
	.string "\nhere? Tch… You've"
	.string "\pgot some nerve"
	.string "\nasking me that."
	.string "\pI'll beat you to"
	.string "\ntest how I've"
	.string "\limproved."
	.string "\pCome on!$"

Unova_NimbasaParkBasement_Text_NimbasaParkInferWin::
	.string "Darn… still not"
	.string "\ngood enough.$"

Unova_NimbasaParkBasement_Text_NimbasaParkInferAfter::
	.string "No… Even after my"
	.string "\ntraining, I still"
	.string "\lcan't beat you!"
	.string "\pWhatever! You'd"
	.string "\nbetter keep your"
	.string "\pnose out of TEAM"
	.string "\nPLASMA's business!$"

Unova_NimbasaParkBasement_Text_NimbasaParkGialloIntro::
	.string "You fools, you've"
	.string "\nbeen interfering"
	.string "\pwith TEAM PLASMA's"
	.string "\nplans, but you're"
	.string "\ltoo late."
	.string "\pThe THUNDER ELE-"
	.string "\nMENT has already"
	.string "\pbeen extracted"
	.string "\nfrom the"
	.string "\lgenerator.$"

Unova_NimbasaParkBasement_Text_NimbasaParkCherenBasementIntro::
	.string "CHEREN: Whatever"
	.string "\nyou're planning,"
	.string "\pyou won't succeed."
	.string "\nWe'll stop you!$"

Unova_NimbasaParkBasement_Text_NimbasaParkShadowProtect::
	.string "I will protect"
	.string "\nyou, SAGE GIALLO…$"

Unova_NimbasaParkBasement_Text_NimbasaParkCherenFightShadow::
	.string "CHEREN: {PLAYER},"
	.string "\nI'll handle him,"
	.string "\lyou take the SAGE.$"

Unova_NimbasaParkBasement_Text_NimbasaParkGialloStartFight::
	.string "GIALLO: Foolish"
	.string "\nchild! You think"
	.string "\pyou are a match"
	.string "\nfor a SAGE of TEAM"
	.string "\lPLASMA?"
	.string "\pAllow me to show"
	.string "\nhow outclassed"
	.string "\lyou truly are!$"

Unova_NimbasaParkBasement_Text_NimbasaParkGialloBeaten::
	.string "No! This cannot"
	.string "\nbe!$"

Unova_NimbasaParkBasement_Text_NimbasaParkGialloAfter::
	.string "GIALLO: It matters"
	.string "\nnot, we have what"
	.string "\lwe came for."
	.string "\pCome, SHADOW, take"
	.string "\nus out of here!$"

Unova_NimbasaParkBasement_Text_NimbasaParkCherenAfter::
	.string "CHEREN: Darn, they"
	.string "\ngot away…"
	.string "\pC'mon, let's go."
	.string "\nI'll take us"
	.string "\lback outside.$"
