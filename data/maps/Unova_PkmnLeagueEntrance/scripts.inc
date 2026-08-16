@ PkmnLeagueEntrance do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@
@ Editado a mao em 12/08/2026 (B6): o porteiro da cena do terremoto.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5): a ULTIMA batalha do rival.
@
@ Traducao do `.PrepareEliteFour` de PkmnLeagueEntrance.asm, que e um
@ MAPCALLBACK_NEWMAP e cuja unica parte que importa aqui e
@ `setmapscene PKMN_LEAGUE_MAIN, SCENE_ELITE_FOUR_ROOM_ENTER`: passar por esta
@ sala e o que arma a cena de entrada da Liga. As outras linhas daquele callback
@ (limpar EVENT_BEAT_ELITE_FOUR_*) sao para o BW3G poder REFAZER a Elite dos
@ Quatro; aqui quem lembra que cada membro caiu e a flag de treinador derrotado
@ do proprio motor, e apaga-la seria apagar o progresso do jogador.
@
@ Zero var. Uma flag, FLAG_UNOVA_LIGA_PORTAO, que a PkmnLeagueMain consome e
@ apaga assim que a cena roda.
@
@ ------------------------------------------------------------------ bloco A5
@ FONTE da cena: `PkmnLeagueInferScript1` / `2`, coord_events (13,15) e (14,15),
@ mesmo fecho. E a DESPEDIDA da INFER: ela pede desculpas, faz a ultima
@ batalha e da a TM de EARTHQUAKE.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   VAR_UNOVA_LIGA_ENTRADA_CENA: 0 = SCENE_DEFAULT, 1 = SCENE_FINISHED.
@
@ EVENT_ da fonte -> FLAG_ da tabela:
@   EVENT_PKMN_LEAGUE_ENTRANCE_INFER -> FLAG_UNOVA_LIGA_ENTRADA_INFER
@ Essa mesma flag e o campo `flag` do object_event da INFER no map.json, e o
@ ON_TRANSITION a ACENDE SEMPRE, porque na fonte ela entra com `appear`: nunca
@ nasce junto com o mapa. Mesmo idioma do ChampionsRoom com a JUNIPER, e zero
@ flag nova (a flag ja existe na tabela do PLANO). O `addobject` do roteiro
@ cria o objeto mesmo com a flag acesa, porque `TrySpawnObjectEvent` nao
@ consulta flag (src/event_object_movement.c); quem consulta e so o nascimento
@ em massa da entrada de mapa (linha 2920).
@
@ Ids locais (indice no map.json + 1): 1 = INFER.
@
@ DESCARTADOS: `setlasttalked` e `reloadmapafterbattle` (cobertos pelo
@ `trainerbattle_no_intro`); `setflag ENGINE_FLYPOINT_PKMN_LEAGUE`, porque
@ nenhum mapa de Unova neste repo acende ponto de voo (o `FLAG_VISITED_*` de
@ Unova nao existe), entao acender um bit qualquer aqui seria inventar recurso.
@ `special FadeOutMusic` -> `special Script_FadeOutMapMusic` + `waitstate`;
@ `playmapmusic` -> `fadedefaultbgm`; `teleport_from` -> SE_WARP_OUT +
@ `removeobject`, o idioma que a ChampionsRoomEntrance ja usa.
@ MUSICA: MUSIC_RIVAL_ENCOUNTER -> MUS_ENCOUNTER_MAY.

Unova_PkmnLeagueEntrance_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_PkmnLeagueEntrance_OnTransition
	.byte 0

Unova_PkmnLeagueEntrance_OnTransition:
	setflag FLAG_UNOVA_LIGA_PORTAO
	setflag FLAG_UNOVA_LIGA_ENTRADA_INFER
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
Unova_PkmnLeagueEntrance_EventScript_PkmnLeagueInferScript1::
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	msgbox Unova_PkmnLeagueEntrance_Text_InferHey, MSGBOX_DEFAULT
	closemessage
	playse SE_DOOR
	addobject 1
	waitse
	playbgm MUS_ENCOUNTER_MAY, FALSE
	turnobject LOCALID_PLAYER, DIR_SOUTH
	applymovement 1, Unova_PkmnLeagueEntrance_Movement_InferSeAproximaPelaEsquerda
	waitmovement 0
	goto Unova_PkmnLeagueEntrance_EventScript_PkmnLeagueInferScript

Unova_PkmnLeagueEntrance_EventScript_PkmnLeagueInferScript2::
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	msgbox Unova_PkmnLeagueEntrance_Text_InferHey, MSGBOX_DEFAULT
	closemessage
	playse SE_DOOR
	addobject 1
	waitse
	playbgm MUS_ENCOUNTER_MAY, FALSE
	turnobject LOCALID_PLAYER, DIR_SOUTH
	applymovement 1, Unova_PkmnLeagueEntrance_Movement_InferSeAproximaPelaDireita
	waitmovement 0
	@ cai no proximo, como na fonte

Unova_PkmnLeagueEntrance_EventScript_PkmnLeagueInferScript::
	msgbox Unova_PkmnLeagueEntrance_Text_InferIntro, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_UNOVA_LIGA_ENTRADA_INFER
	goto Unova_PkmnLeagueEntrance_EventScript_BatalhaInfer7

@ Mesmo galho por inicial das outras quatro batalhas da INFER: a fonte manda
@ `checkevent EVENT_GOT_OSHAWOTT -> INFER7_SNIVY`,
@ `checkevent EVENT_GOT_SNIVY -> INFER7_TEPIG`, fallthrough (TEPIG) ->
@ INFER7_OSHAWOTT. Aqui o galho e por VAR_STARTER_MON (0 = SNIVY, 1 = TEPIG,
@ 2 = OSHAWOTT, escrito por data/maps/Unova_NuvemaLab/scripts.inc).
Unova_PkmnLeagueEntrance_EventScript_BatalhaInfer7::
	goto_if_eq VAR_STARTER_MON, 0, Unova_PkmnLeagueEntrance_EventScript_InferComTepig
	goto_if_eq VAR_STARTER_MON, 1, Unova_PkmnLeagueEntrance_EventScript_InferComOshawott
	trainerbattle_no_intro TRAINER_UNOVA_INFER7_SNIVY, Unova_PkmnLeagueEntrance_Text_InferWin
	goto Unova_PkmnLeagueEntrance_EventScript_DepoisDaInfer7

Unova_PkmnLeagueEntrance_EventScript_InferComTepig::
	trainerbattle_no_intro TRAINER_UNOVA_INFER7_TEPIG, Unova_PkmnLeagueEntrance_Text_InferWin
	goto Unova_PkmnLeagueEntrance_EventScript_DepoisDaInfer7

Unova_PkmnLeagueEntrance_EventScript_InferComOshawott::
	trainerbattle_no_intro TRAINER_UNOVA_INFER7_OSHAWOTT, Unova_PkmnLeagueEntrance_Text_InferWin
Unova_PkmnLeagueEntrance_EventScript_DepoisDaInfer7::
	fadedefaultbgm
	msgbox Unova_PkmnLeagueEntrance_Text_InferAfter, MSGBOX_DEFAULT
	closemessage
	giveitem ITEM_TM_EARTHQUAKE
	msgbox Unova_PkmnLeagueEntrance_Text_InferLeave, MSGBOX_DEFAULT
	closemessage
	playse SE_WARP_OUT
	removeobject 1
	waitse
	setvar VAR_UNOVA_LIGA_ENTRADA_CENA, 1
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_PkmnLeagueEntrance_Movement_InferSeAproximaPelaEsquerda:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	step_end

Unova_PkmnLeagueEntrance_Movement_InferSeAproximaPelaDireita:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_up
	walk_up
	step_end

Unova_PkmnLeagueEntrance_Text_InferHey::
	.string "Hey!$"

Unova_PkmnLeagueEntrance_Text_InferIntro::
	.string "I figured I'd find"
	.string "\nyou here. I've"
	.string "\pdone a lot of"
	.string "\nthinking since the"
	.string "\llast time we met."
	.string "\pAll that stuff"
	.string "\nthat happened back"
	.string "\lat the tower…"
	.string "\pI'm… I'm sorry"
	.string "\nabout all that."
	.string "\pI just wanted to"
	.string "\nbe a great POKéMON"
	.string "\ltrainer so bad,"
	.string "\pand it made me so"
	.string "\nmad that I just"
	.string "\lcouldn't beat you."
	.string "\pBut it wasn't just"
	.string "\nyou, I was mad at"
	.string "\la lot of things…"
	.string "\pMy grandpa…"
	.string "\nTEAM PLASMA…"
	.string "\pAll that anger"
	.string "\nmade me lose sight"
	.string "\pof why I wanted to"
	.string "\nbe a POKéMON"
	.string "\ltrainer in the"
	.string "\lfirst place…"
	.string "\pBecause I love"
	.string "\nPOKéMON! With all"
	.string "\lmy heart!"
	.string "\pI'm going to be a"
	.string "\nbetter trainer"
	.string "\pfrom here on out,"
	.string "\nfor my POKéMON's"
	.string "\lsake."
	.string "\pSo I'm not mad at"
	.string "\nyou anymore,"
	.string "\l{PLAYER}."
	.string "\pAnd I want to"
	.string "\nchallenge you one"
	.string "\llast time!"
	.string "\pSo come on! Give"
	.string "\nit everything"
	.string "\lyou've got!$"

Unova_PkmnLeagueEntrance_Text_InferWin::
	.string "So that's how it"
	.string "\nends, huh…$"

Unova_PkmnLeagueEntrance_Text_InferAfter::
	.string "I had a feeling it"
	.string "\nwould end this"
	.string "\lway…"
	.string "\pLooks like I've"
	.string "\nstill got a lot to"
	.string "\llearn."
	.string "\pBefore I go, I"
	.string "\nwant you to have"
	.string "\pthis. Think of it"
	.string "\nas an apology for"
	.string "\pall the hassle I"
	.string "\nput you through.$"

Unova_PkmnLeagueEntrance_Text_InferLeave::
	.string "That TM teaches"
	.string "\nEARTHQUAKE. It's"
	.string "\pone of the most"
	.string "\npowerful moves out"
	.string "\pthere. You'll need"
	.string "\nit if you want to"
	.string "\ptake on the ELITE"
	.string "\nFOUR. Good luck in"
	.string "\pthere! And you'd"
	.string "\nbetter not lose!"
	.string "\pIf you can take"
	.string "\nout the POKéMON"
	.string "\pLEAGUE, I won't"
	.string "\nfeel as bad for"
	.string "\llosing to you!"
	.string "\pSee you, {PLAYER}!$"
