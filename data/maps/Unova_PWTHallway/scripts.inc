@ PWTHallway do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_PWTHallway_MapScripts::
	.byte 0

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ STUB A2: cena do bloco A4/A5/A6, rotulo PwtEnterFromLeftScript
Unova_PWTHallway_EventScript_PwtEnterFromLeftScript::
	lockall
	setvar VAR_UNOVA_PWT_CORREDOR_CENA, 1
	applymovement OBJ_EVENT_ID_PLAYER, Unova_PWTHallway_Movement_EsquerdaParaDireita
	waitmovement 0
	releaseall
	end

@ STUB A2: cena do bloco A4/A5/A6, rotulo PwtEnterFromRightScript
Unova_PWTHallway_EventScript_PwtEnterFromRightScript::
	lockall
	setvar VAR_UNOVA_PWT_CORREDOR_CENA, 1
	applymovement OBJ_EVENT_ID_PLAYER, Unova_PWTHallway_Movement_SaidaPelaDireita
	waitmovement 0
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

@ Cenas do PWT (dev_scripts/cenas_pwt_unova.py), autorizadas em 22/08/2026

	.align 2
Unova_PWTHallway_Movement_EsquerdaParaDireita:
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_up
	walk_up
	walk_up
	step_end

	.align 2
Unova_PWTHallway_Movement_SaidaPelaDireita:
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_down
	walk_down
	step_end
