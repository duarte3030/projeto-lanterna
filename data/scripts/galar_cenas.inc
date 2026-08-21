@ Cenas de map script de Galar (bloco c3 da fase de conteudo).
@ Gerado por dev_scripts/cenas_galar.py; NAO editar a mao.
@ A cena vem do demake (fontes-mapas/galar-swsh), desmontada do
@ bytecode do FireRed. O que nao coube saiu com motivo contado.

@ ---- Galar_Hammerlocke01 (g03m05) ----
GalarCena_G03M05_t2_v2::
	lockall
	applymovement OBJ_EVENT_ID_PLAYER, GalarCena_G03M05_t2_v2_Mov0
	waitmovement 0
	setvar VAR_GALAR_G03M05_CENA, 3
	releaseall
	end

GalarCena_G03M05_t2_v2_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_UP
	.byte MOVEMENT_ACTION_WALK_NORMAL_UP
	.byte MOVEMENT_ACTION_STEP_END

@ ---- Galar_Circhester16 (g03m08) ----
GalarCena_G03M08_t2_v3::
	lockall
	textcolor 0
	msgbox GalarCena_G03M08_t2_v3_Text0, MSGBOX_DEFAULT
	closemessage
	applymovement 1, GalarCena_G03M08_t2_v3_Mov0
	waitmovement 0
	removeobject 1
	setvar VAR_GALAR_G03M08_CENA, 4
	@ setflag 0x075 da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	@ clearflag 0x076 da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	releaseall
	end

GalarCena_G03M08_t2_v3_Text0:
	.string "Hey, wasn’t that a long cruise?\pMy buddy Celio seemed to enjoy\nyour company.\pI’m sure he’d welcome you if you\nwere to visit him again.\pIf you have a Tri-Pass, you can\nalways take a ferry there from\lVermilion Port.\pAll right, thanks for your company!$"
GalarCena_G03M08_t2_v3_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_STEP_END

@ ---- Galar_Postwick22 (g04m03) ----
GalarCena_G04M03_t4_v1::
	turnobject OBJ_EVENT_ID_PLAYER, DIR_NORTH
	end


@ ---- Galar_WildArea03 (g06m27) ----
GalarCena_G06M27_t3_x::
	@ setflag 0x91A da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	@ setflag 0x90D da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	random 9
	compare VAR_RESULT, 0
	goto_if 1, GalarCena_G06M27_t3_x_b1
	compare VAR_RESULT, 1
	goto_if 1, GalarCena_G06M27_t3_x_b2
	compare VAR_RESULT, 2
	goto_if 1, GalarCena_G06M27_t3_x_b2
	compare VAR_RESULT, 3
	goto_if 1, GalarCena_G06M27_t3_x_b2
	compare VAR_RESULT, 4
	goto_if 1, GalarCena_G06M27_t3_x_b1
	compare VAR_RESULT, 5
	goto_if 1, GalarCena_G06M27_t3_x_b3
	compare VAR_RESULT, 6
	goto_if 1, GalarCena_G06M27_t3_x_b2
	compare VAR_RESULT, 7
	goto_if 1, GalarCena_G06M27_t3_x_b1
	compare VAR_RESULT, 8
	goto_if 1, GalarCena_G06M27_t3_x_b2
	compare VAR_RESULT, 9
	goto_if 1, GalarCena_G06M27_t3_x_b3
	end

GalarCena_G06M27_t3_x_b1::
	setweather WEATHER_RAIN
	doweather
	release
	end

GalarCena_G06M27_t3_x_b2::
	setweather WEATHER_SUNNY
	doweather
	release
	end

GalarCena_G06M27_t3_x_b3::
	setweather WEATHER_SUNNY
	doweather
	release
	end


@ ---- Galar_WildArea04 (g06m29) ----

@ ---- Galar_WildArea05 (g06m30) ----

@ ---- Galar_WildArea06 (g06m31) ----

@ ---- Galar_WildArea07 (g08m22) ----

@ ---- Galar_WildArea08 (g08m23) ----

@ ---- Galar_WildArea09 (g08m24) ----

@ ---- Galar_WildArea10 (g42m02) ----

@ ---- Galar_WildArea12 (g42m05) ----

@ ---- Galar_WildArea13 (g42m06) ----

@ ---- Galar_WildArea14 (g42m07) ----

@ ---- Galar_WildArea18 (g42m11) ----

@ ---- Galar_WildArea19 (g42m12) ----

