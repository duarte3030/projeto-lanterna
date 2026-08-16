@ P2LabEntrance do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Cenas do portao escritas a mao em 15/08/2026 (B6 Unova, Obra 1, bloco A6),
@ no molde de data/maps/Unova_ChampionsRoom/scripts.inc.
@
@ UM GATILHO, TRES ESTADOS. A fonte tem TRES `scene_script` e um `coord_event`
@ so. VAR_UNOVA_P2_LAB_ENTRADA_CENA guarda os tres, com os valores da tabela do
@ PLANO-OBRAS-UNOVA.md:
@   0 = SCENE_P2_LAB_ENTRANCE_DEFAULT, a JUNIPER esperando na porta do laboratorio;
@       e o `coord_event 8,3` da fonte (`P2LabEntranceJuniperScript`).
@   1 = SCENE_P2_LAB_ENTRANCE_AFTER, a despedida depois do GORM; na fonte e o
@       `scene_script .AfterGorm` com `priorityjump`, que aqui e
@       MAP_SCRIPT_ON_FRAME_TABLE, igual a sala do Campeao.
@   2 = SCENE_P2_LAB_ENTRANCE_NOTHING, nada acontece; as duas cenas terminam nele.
@
@ QUEM ESCREVE O ESTADO 1 e o P2Lab (`maps/P2Lab.asm` linha 109: `setmapscene
@ P2_LAB_ENTRANCE, SCENE_P2_LAB_ENTRANCE_AFTER` logo antes de `warp
@ P2_LAB_ENTRANCE, 4, 7`), que e do bloco A4 e nao foi escrito nesta leva.
@ Enquanto ninguem gravar 1 nesta var, o estado 1 simplesmente nunca roda: nada
@ aqui depende disso para o estado 0 funcionar.
@
@ ESCONDER A JUNIPER SEM FLAG NOVA: mesma solucao de
@ data/maps/Unova_NuvemaLab/scripts.inc. `appear`/`disappear` da fonte mexem em
@ EVENT_P2_LAB_ENTRANCE_JUNIPER, que NAO esta na tabela de flags do plano (a
@ varredura le `setevent`/`clearevent`, e `appear` nao escreve o nome do
@ evento), e a janela de save esta fechada. O objeto usa FLAG_UNOVA_CENA_JUNIPER,
@ o mesmo bit da sala do Campeao, e este mapa o REESCREVE no proprio
@ ON_TRANSITION antes de os objetos nascerem, entao o bit nunca carrega estado
@ de um mapa para o outro.
@
@ O QUE FOI DESCARTADO no estado 1, e o motivo:
@   `setevent EVENT_BEAT_P2_LAB`, `setevent EVENT_NUVEMA_LAB_BIANCA` e
@   `setevent EVENT_P2_LAB_GRUNTS`: nenhum dos tres tem FLAG_ na tabela do
@   PLANO-OBRAS-UNOVA.md e a janela de save esta fechada, entao nao ha bit para
@   gravar e inventar um seria escrever fora do plano. O que se perde: a BIANCA
@   do laboratorio de Nuvema nao troca de fala nem some depois do P2, e os
@   grunts do P2 nao ficam marcados.
@   `specialphonecall SPECIALCALL_BIANCA_P2`: este motor nao tem lista
@   telefonica (mesma razao do XTRANSCEIVER em Unova_PlayersHouse1F).
@   `moveobject` do gen 2 e temporario; aqui o equivalente e `setobjectxyperm`
@   (grava no template), e o template e devolvido a (8,2) no fim da cena.
@
@ Ids locais (indice no map.json + 1):  1 = JUNIPER

Unova_P2LabEntrance_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_P2LabEntrance_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Unova_P2LabEntrance_OnFrame
	.byte 0

@ Roda ANTES de InitMap() criar os object_events (tecnica 2 do SINNOH-PADRAO.md):
@ a JUNIPER so nasce sozinha no estado 0; nos outros dois quem a traz e a cena.
@ DEPENDENCIA COMPARTILHADA, nao mexer aqui sozinho: FLAG_UNOVA_CENA_JUNIPER e o
@ MESMO bit em Unova_NuvemaLab, Unova_P2LabEntrance, Unova_ChampionsRoom e
@ Unova_UndellaTown (MARLON da cena de chegada). O
@ contrato que faz isso funcionar e "todo mapa que usa o bit o REESCREVE no seu
@ proprio ON_TRANSITION, antes de os objetos nascerem". Quem tirar ou condicionar
@ esta escrita em UM dos quatro quebra os outros tres (o NPC de cena nasce ou
@ some no mapa errado). Mudou um, confira os quatro.
Unova_P2LabEntrance_OnTransition:
	goto_if_eq VAR_UNOVA_P2_LAB_ENTRADA_CENA, 0, Unova_P2LabEntrance_EventScript_TransicaoEstado0
	setflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_P2LabEntrance_EventScript_TransicaoEstado0::
	clearflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_P2LabEntrance_OnFrame:
	map_script_2 VAR_UNOVA_P2_LAB_ENTRADA_CENA, 1, Unova_P2LabEntrance_EventScript_DespedidaJuniper
	.2byte 0

@ `P2LabEntranceJuniperScript` da fonte, o `coord_event 8,3` (estado 0).
Unova_P2LabEntrance_EventScript_P2LabEntranceJuniperScript::
	lockall
	turnobject LOCALID_PLAYER, DIR_NORTH
	turnobject 1, DIR_SOUTH
	msgbox Unova_P2LabEntrance_Text_JuniperIntro, MSGBOX_DEFAULT
	closemessage
	@ (8,2) -> (9,2), que e o warp para o P2_LAB
	applymovement 1, Unova_P2LabEntrance_Movement_JuniperEntraNoLab
	waitmovement 0
	playse SE_DOOR
	setflag FLAG_UNOVA_CENA_JUNIPER
	removeobject 1
	waitse
	@ `setscene SCENE_P2_LAB_ENTRANCE_NOTHING` da fonte
	setvar VAR_UNOVA_P2_LAB_ENTRADA_CENA, 2
	releaseall
	end

@ `.BeatenP2LabScene` da fonte, o alvo do `priorityjump` do estado 1. O jogador
@ chega aqui pelo `warp P2_LAB_ENTRANCE, 4, 7` do P2Lab, e a JUNIPER nasce ao
@ lado dele, em (5,7).
Unova_P2LabEntrance_EventScript_DespedidaJuniper::
	lockall
	turnobject LOCALID_PLAYER, DIR_EAST
	setobjectxyperm 1, 5, 7
	clearflag FLAG_UNOVA_CENA_JUNIPER
	addobject 1
	turnobject 1, DIR_WEST
	msgbox Unova_P2LabEntrance_Text_JuniperAfter, MSGBOX_DEFAULT
	closemessage
	playse SE_DOOR
	@ (5,7) -> (5,9), que e o warp para a R_17
	applymovement 1, Unova_P2LabEntrance_Movement_JuniperVaiEmbora
	waitmovement 0
	setflag FLAG_UNOVA_CENA_JUNIPER
	removeobject 1
	waitse
	@ template devolvido ao lugar da fonte, para o estado 0 nao herdar (5,7)
	setobjectxyperm 1, 8, 2
	@ `setscene SCENE_P2_LAB_ENTRANCE_NOTHING` da fonte
	setvar VAR_UNOVA_P2_LAB_ENTRADA_CENA, 2
	releaseall
	end

@ `P2LabEntranceJuniperMovement1` da fonte.
Unova_P2LabEntrance_Movement_JuniperEntraNoLab:
	walk_right
	step_end

@ `P2LabEntranceJuniperMovement2` da fonte.
Unova_P2LabEntrance_Movement_JuniperVaiEmbora:
	walk_down
	walk_down
	step_end

@ `P2LabEntranceJuniperIntroText` da fonte, palavra a palavra.
Unova_P2LabEntrance_Text_JuniperIntro::
	.string "JUNIPER: {PLAYER}! It's just as\n"
	.string "I suspected, there's a secret\l"
	.string "entrance.\p"
	.string "After TEAM PLASMA was shut down,\n"
	.string "their labs and hideouts were\l"
	.string "raided.\p"
	.string "They found some pretty dangerous\n"
	.string "technology…\p"
	.string "I wonder what TEAM PLASMA could\n"
	.string "be after here…\p"
	.string "Come on, {PLAYER}, let's go.$"

@ `P2LabEntranceJuniperAfterText` da fonte, palavra a palavra.
Unova_P2LabEntrance_Text_JuniperAfter::
	.string "JUNIPER: Thanks for your help,\n"
	.string "{PLAYER}.\p"
	.string "I hope to meet you again on your\n"
	.string "travels.$"
