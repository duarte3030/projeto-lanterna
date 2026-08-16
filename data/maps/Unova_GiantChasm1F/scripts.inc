@ GiantChasm1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5).
@
@ FONTE: fontes-mapas/bw3g/maps/GiantChasm1F.asm, `GiantChasm_MeetInferScene`,
@ disparado por `coord_event 13, 17, SCENE_DEFAULT`. Unica cena do arco da
@ Plasma/INFER que NAO tem batalha: a INFER e flagrada no telefone e foge.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   SCENE_DEFAULT = 0, SCENE_FINISHED = 1, na VAR_UNOVA_GIANT_CHASM_CENA.
@   `setscene SCENE_FINISHED` -> `setvar VAR_UNOVA_GIANT_CHASM_CENA, 1`.
@ O coord_event do map.json ja nasce com var/valor certos; aqui so mora o fecho.
@
@ COMO A INFER SOME PARA SEMPRE, com zero flag nova (a janela de save esta
@ fechada): o campo `flag` do object_event dela e FLAG_TEMP_11, e o
@ ON_TRANSITION deste mapa ACENDE essa flag temporaria quando a var ja saiu de
@ 0. Funciona porque `ClearTempFieldEventData()` roda ANTES de
@ `RunOnTransitionMapScript()` (src/overworld.c:893 e :909) e o nascimento dos
@ objetos so acontece depois, conferindo `template->flagId`
@ (src/event_object_movement.c:2920). Ou seja: a flag temporaria e recalculada
@ da var a cada entrada de mapa e nao gasta um bit da save.
@
@ Ids locais (indice no map.json + 1): 1 = PARLYZ HEAL (bola), 2 = INFER.
@
@ DESCARTADOS: `special RestartMapMusic` vira `fadedefaultbgm` (mesmo efeito de
@ voltar a musica do mapa); o parametro de duracao do `showemote` some porque
@ Common_Movement_ExclamationMark ja tem duracao propria.

Unova_GiantChasm1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_GiantChasm1F_OnTransition
	.byte 0

Unova_GiantChasm1F_OnTransition:
	goto_if_eq VAR_UNOVA_GIANT_CHASM_CENA, 0, Unova_GiantChasm1F_EventScript_TransicaoFim
	setflag FLAG_TEMP_11
Unova_GiantChasm1F_EventScript_TransicaoFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
Unova_GiantChasm1F_EventScript_GiantChasm_MeetInferScene::
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	msgbox Unova_GiantChasm1F_Text_GiantChasmInferPhone, MSGBOX_DEFAULT
	closemessage
	applymovement 2, Common_Movement_ExclamationMark
	waitmovement 0
	turnobject 2, DIR_EAST
	msgbox Unova_GiantChasm1F_Text_GiantChasmInferLeave, MSGBOX_DEFAULT
	closemessage
	playse SE_FLEE
	applymovement 2, Unova_GiantChasm1F_Movement_InferFoge
	waitmovement 0
	delay 15
	playse SE_DOOR
	waitse
	delay 15
	setvar VAR_UNOVA_GIANT_CHASM_CENA, 1
	removeobject 2
	fadedefaultbgm
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

@ `GiantChasmInferMovement` da fonte: big_step LEFT duas vezes.
Unova_GiantChasm1F_Movement_InferFoge:
	walk_fast_left
	walk_fast_left
	step_end

Unova_GiantChasm1F_Text_GiantChasmInferPhone::
	.string "Yes, I have the"
	.string "\npackage. I"
	.string "\pmanaged to snag"
	.string "\nit from the GYM"
	.string "\pwhile the LEADER"
	.string "\nwas away. I don't"
	.string "\pthink the GYM"
	.string "\nLEADER followed"
	.string "\lme.$"

Unova_GiantChasm1F_Text_GiantChasmInferLeave::
	.string "Hey, you!"
	.string "\pGet out of here!"
	.string "\nForget what you"
	.string "\lsaw here!$"
