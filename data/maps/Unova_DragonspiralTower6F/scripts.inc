@ DragonspiralTower6F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5).
@
@ FONTE: fontes-mapas/bw3g/maps/DragonspiralTower6F.asm. Dois coord_events,
@ (2,13) e (3,13), no mesmo fecho: a QUARTA batalha do rival, agora disfarcada
@ de SABIO da Plasma (INFER_SAGE). E a cena que explica por que a INFER entrou
@ na Plasma, logo antes do topo da torre.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   VAR_UNOVA_DRAGONSPIRAL_6F_CENA: 0 = SCENE_DEFAULT, 1 = SCENE_FINISHED.
@
@ EVENT_ da fonte -> FLAG_ da tabela:
@   EVENT_DRAGONSPIRAL_TOWER_6F_INFER -> FLAG_UNOVA_DRAGONSPIRAL_6F_INFER
@ Essa mesma flag e o campo `flag` do object_event da INFER no map.json, e o
@ ON_TRANSITION a ACENDE SEMPRE: na fonte ela entra na cena com `appear`, ou
@ seja nunca nasce junto com o mapa. E o mesmo idioma do ChampionsRoom com a
@ JUNIPER. Zero flag nova: a flag ja existe na tabela do PLANO.
@ O `addobject` do roteiro cria o objeto mesmo com a flag acesa, porque
@ `TrySpawnObjectEvent` nao consulta flag (src/event_object_movement.c); quem
@ consulta e so o nascimento em massa da entrada de mapa (linha 2920).
@
@ Ids locais (indice no map.json + 1): 1 = MAX ELIXER (bola), 2 = INFER SAGE.
@
@ DESCARTADO, e por que: o callback `MAPCALLBACK_OBJECTS .AppearRoofObjects`.
@ Ele serve para REARMAR o elenco do TOPO da torre quando o jogador perdeu para
@ o ZINZOLIN e voltou. Aqui isso ja acontece de graca: o ON_TRANSITION do
@ proprio DragonspiralTowerRoof recalcula quem nasce a partir de
@ VAR_UNOVA_DRAGONSPIRAL_TOPO_CENA a cada entrada de mapa, entao nao ha estado
@ velho para consertar de fora.
@ Tambem fora: `setlasttalked`, `dontrestartmapmusic`, `reloadmapafterbattle`
@ (o `trainerbattle_no_intro` cobre os tres).
@ `moveobject` do gen 2 e temporario, mas aqui o alvo AINDA NAO NASCEU (ele so
@ entra com `addobject` mais abaixo), e `setobjectxy` so funciona em objeto
@ vivo. Por isso vira `setobjectxyperm`, que mexe no template e portanto vale
@ para o `addobject` seguinte.
@ `fix_facing` + `slow_step UP` vira `walk_slow_up` mais um `turnobject` de
@ volta para o sul: o motor daqui nao anda sem virar o sprite.
@ MUSICA: MUSIC_RIVAL_ENCOUNTER -> MUS_ENCOUNTER_MAY.

Unova_DragonspiralTower6F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_DragonspiralTower6F_OnTransition
	.byte 0

Unova_DragonspiralTower6F_OnTransition:
	setflag FLAG_UNOVA_DRAGONSPIRAL_6F_INFER
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Gatilho de (2,13): a INFER precisa nascer na coluna do jogador.
Unova_DragonspiralTower6F_EventScript_DragonspiralTowerInferScript1::
	lockall
	setobjectxyperm 2, 2, 8
	goto Unova_DragonspiralTower6F_EventScript_CenaInfer

@ Gatilho de (3,13): a INFER fica onde o template ja a poe.
Unova_DragonspiralTower6F_EventScript_DragonspiralTowerInferScript2::
	lockall
	@ cai no proximo (na fonte o Script1 cai DENTRO do Script2; aqui ele desvia
	@ depois do setobjectxyperm porque o `lockall` nao pode rodar duas vezes)

Unova_DragonspiralTower6F_EventScript_CenaInfer::
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	msgbox Unova_DragonspiralTower6F_Text_InferIntro, MSGBOX_DEFAULT
	closemessage
	turnobject LOCALID_PLAYER, DIR_NORTH
	addobject 2
	playbgm MUS_ENCOUNTER_MAY, FALSE
	applymovement 2, Unova_DragonspiralTower6F_Movement_InferSeAproxima
	waitmovement 0
	msgbox Unova_DragonspiralTower6F_Text_InferSpeech, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_UNOVA_DRAGONSPIRAL_6F_INFER
	goto Unova_DragonspiralTower6F_EventScript_BatalhaInferSage

@ Mesmo galho por inicial das outras batalhas da INFER: a fonte manda
@ `checkevent EVENT_GOT_OSHAWOTT -> INFER_SAGE_SNIVY`,
@ `checkevent EVENT_GOT_SNIVY -> INFER_SAGE_TEPIG`, fallthrough (TEPIG) ->
@ INFER_SAGE_OSHAWOTT. Aqui o galho e por VAR_STARTER_MON (0 = SNIVY,
@ 1 = TEPIG, 2 = OSHAWOTT, escrito por data/maps/Unova_NuvemaLab/scripts.inc).
Unova_DragonspiralTower6F_EventScript_BatalhaInferSage::
	goto_if_eq VAR_STARTER_MON, 0, Unova_DragonspiralTower6F_EventScript_InferComTepig
	goto_if_eq VAR_STARTER_MON, 1, Unova_DragonspiralTower6F_EventScript_InferComOshawott
	trainerbattle_no_intro TRAINER_UNOVA_INFER_SAGE_SNIVY, Unova_DragonspiralTower6F_Text_InferWin
	goto Unova_DragonspiralTower6F_EventScript_DepoisDaInferSage

Unova_DragonspiralTower6F_EventScript_InferComTepig::
	trainerbattle_no_intro TRAINER_UNOVA_INFER_SAGE_TEPIG, Unova_DragonspiralTower6F_Text_InferWin
	goto Unova_DragonspiralTower6F_EventScript_DepoisDaInferSage

Unova_DragonspiralTower6F_EventScript_InferComOshawott::
	trainerbattle_no_intro TRAINER_UNOVA_INFER_SAGE_OSHAWOTT, Unova_DragonspiralTower6F_Text_InferWin
Unova_DragonspiralTower6F_EventScript_DepoisDaInferSage::
	playbgm MUS_ENCOUNTER_MAY, FALSE
	delay 15
	applymovement 2, Unova_DragonspiralTower6F_Movement_InferRecua
	waitmovement 0
	turnobject 2, DIR_SOUTH
	msgbox Unova_DragonspiralTower6F_Text_InferAfterBattle, MSGBOX_DEFAULT
	closemessage
	applymovement 2, Unova_DragonspiralTower6F_Movement_InferSai
	waitmovement 0
	removeobject 2
	special Script_FadeOutMapMusic
	waitstate
	delay 30
	fadedefaultbgm
	setvar VAR_UNOVA_DRAGONSPIRAL_6F_CENA, 1
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_DragonspiralTower6F_Movement_InferSeAproxima:
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Unova_DragonspiralTower6F_Movement_InferRecua:
	walk_slow_up
	step_end

Unova_DragonspiralTower6F_Movement_InferSai:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

Unova_DragonspiralTower6F_Text_InferIntro::
	.string "Hey!!!"
	.string "\nHold it right"
	.string "\lthere!$"

Unova_DragonspiralTower6F_Text_InferSpeech::
	.string "Don't you take"
	.string "\nanother step! You"
	.string "\pmay have beaten"
	.string "\nthe other sages,"
	.string "\pbut I'm not"
	.string "\nletting you past"
	.string "\lhere."
	.string "\pWhat? Are you"
	.string "\nsurprised to see"
	.string "\lme here?"
	.string "\pHuh? My Grandpa?"
	.string "\nHe told you to"
	.string "\psave me from TEAM"
	.string "\nPLASMA? Ha!"
	.string "\pI don't need"
	.string "\nsaving from"
	.string "\lanyone!"
	.string "\pMy Grandpa's an"
	.string "\nidiot. He always"
	.string "\ptreated me like"
	.string "\nsome helpless kid."
	.string "\pHe refused to even"
	.string "\nacknowledge my"
	.string "\pskill. He wouldn't"
	.string "\neven let me try…"
	.string "\pBut TEAM PLASMA"
	.string "\nrecognized my"
	.string "\ppotential. They"
	.string "\nsaid they would"
	.string "\ptrain me to be a"
	.string "\npowerful POKéMON"
	.string "\ptrainer. And now,"
	.string "\nthanks to that"
	.string "\ptraining, I've"
	.string "\nbecome strong"
	.string "\penough to become a"
	.string "\nSAGE of TEAM"
	.string "\lPLASMA!"
	.string "\p…you say he's"
	.string "\nworried that TEAM"
	.string "\pPLASMA's just"
	.string "\nusing me?"
	.string "\p…sorry, but I"
	.string "\ndon't really care"
	.string "\lif they are."
	.string "\pBecause I'm just"
	.string "\nusing them."
	.string "\pI don't care what"
	.string "\nZINZOLIN's big"
	.string "\pscheme is, I only"
	.string "\njoined TEAM PLASMA"
	.string "\lto become strong."
	.string "\pI'm going to"
	.string "\nbecome the most"
	.string "\ppowerful trainer"
	.string "\nin all of UNOVA!"
	.string "\pI'll be the"
	.string "\ngreatest POKéMON"
	.string "\ptrainer in all"
	.string "\nthe world!"
	.string "\pAnd now, there's"
	.string "\njust one obstacle"
	.string "\lleft in my way…"
	.string "\pRight here, right"
	.string "\nnow, I'm finally"
	.string "\lgoing to beat you!"
	.string "\pCome on!!!$"

Unova_DragonspiralTower6F_Text_InferWin::
	.string "N-no! This is"
	.string "\nimpossible!$"

Unova_DragonspiralTower6F_Text_InferAfterBattle::
	.string "H-how…?"
	.string "\nI did everything"
	.string "\pright. I trained"
	.string "\nup a great team…"
	.string "\pI became a SAGE of"
	.string "\nTEAM PLASMA…"
	.string "\pWhy, then…"
	.string "\pWhy can't I beat"
	.string "\nyou?!"
	.string "\pWhat do you have"
	.string "\nthat I don't?!"
	.string "\p…I-"
	.string "\pAaaargh!!!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Unova_DragonspiralTower6F_EventScript_DexReshiram::
	lockall
	msgbox Unova_DragonspiralTower6F_Text_DexReshiramIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_RESHIRAM, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_RESHIRAM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_RESHIRAM
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_DragonspiralTower6F_EventScript_DexReshiramSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_DragonspiralTower6F_EventScript_DexReshiramSome
	releaseall
	end

Unova_DragonspiralTower6F_EventScript_DexReshiramSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_RESHIRAM
	setflag FLAG_HIDE_DEX_RESHIRAM
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_DragonspiralTower6F_Text_DexReshiramIntro:
	.string "RESHIRAM appeared!$"

Unova_DragonspiralTower6F_EventScript_DexZekrom::
	lockall
	msgbox Unova_DragonspiralTower6F_Text_DexZekromIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZEKROM, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZEKROM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ZEKROM
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_DragonspiralTower6F_EventScript_DexZekromSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_DragonspiralTower6F_EventScript_DexZekromSome
	releaseall
	end

Unova_DragonspiralTower6F_EventScript_DexZekromSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ZEKROM
	setflag FLAG_HIDE_DEX_ZEKROM
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_DragonspiralTower6F_Text_DexZekromIntro:
	.string "ZEKROM appeared!$"

@ <<< Dex completa <<<
