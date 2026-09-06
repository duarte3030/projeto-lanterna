@ Portas de SCRIPT dos orfaos de Galar (onda 2, lote F).
@ Gerado por dev_scripts/portas_script_galar.py; NAO editar a mao.
@
@ Cada rotulo aqui e a transcricao FIEL de um script do demake que contem
@ `warp` e cai num mapa que hoje nenhum caminho alcanca. O tradutor e o mesmo
@ do c3 (cenas_galar.py) e do c4a (objetos_galar.py); o que ele recusa nao
@ aparece aqui, aparece no relatorio com motivo.
@
@ PRECEDENCIA: o rotulo daqui comeca com `GalarPorta_`. Ele so e pendurado em
@ objeto que estava MUDO (`script` valia "0") ou em objeto/gatilho NOVO, e
@ nunca por cima de `GalarObj_`, `GalarFala_`, `GalarTrn_`, `GalarSelvagem_`
@ ou `GalarEstatico_`. Quem escrever campo `script` de map.json de Galar
@ depois desta onda precisa respeitar `GalarPorta_` do mesmo jeito que ja
@ respeita `GalarObj_`, senao a porta se apaga calada.

@ ---- Galar_Motostoke06 (g06m12), 0x88A42E4 -> MAP_GALAR_WEDGEHURST_09 ----
GalarPorta_G06M12_o7::
	checkflag FLAG_GALAR_PORTA_G06M12_72C
	goto_if 1, GalarPorta_G06M12_o7_b1
	setflag FLAG_GALAR_PORTA_G06M12_72C
	msgbox GalarPorta_G06M12_o7_Text0, MSGBOX_AUTOCLOSE
	applymovement 2, GalarPorta_G06M12_o7_Mov0
	msgbox GalarPorta_G06M12_o7_Text1, MSGBOX_AUTOCLOSE
	removeobject 2
	warp MAP_GALAR_WEDGEHURST_09, 7, 4
	waitstate
	release
	end

GalarPorta_G06M12_o7_b1::
	msgbox GalarPorta_G06M12_o7_Text2, MSGBOX_AUTOCLOSE
	release
	end

GalarPorta_G06M12_o7_Text0:
	.string "You're Gym Challengers, right?\pYou can rest for today. Tomorrow is the\nopening ceremony.$"
GalarPorta_G06M12_o7_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_UP
	.byte MOVEMENT_ACTION_WALK_NORMAL_UP
	.byte MOVEMENT_ACTION_WALK_NORMAL_UP
	.byte MOVEMENT_ACTION_WALK_NORMAL_LEFT
	.byte MOVEMENT_ACTION_FACE_DOWN
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G06M12_o7_Text1:
	.string "So that's it, {PLAYER}. Let's rest.\pTomorrow is the big day.$"
GalarPorta_G06M12_o7_Text2:
	.string "This hotel is known all over the world!$"

@ ---- Galar_Hammerlocke04 (g09m10), 0x8877934 -> MAP_GALAR_STOW_ON_SIDE_01 ----
GalarPorta_G09M10_o24::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_IsleOfArmor05 (g38m01), 0x88D1CE4 -> MAP_GALAR_ISLE_OF_ARMOR_01 ----
GalarPorta_G38M01_o4::
	warp MAP_GALAR_ISLE_OF_ARMOR_01, 10, 9
	waitstate
	end


@ ---- Galar_IsleOfArmor08 (g38m04), 0x88D240C -> MAP_GALAR_ISLE_OF_ARMOR_01 ----
GalarPorta_G38M04_o13::
	warp MAP_GALAR_ISLE_OF_ARMOR_01, 10, 9
	waitstate
	end


@ ---- Galar_IsleOfArmor09 (g38m05), 0x88D2740 -> MAP_GALAR_ISLE_OF_ARMOR_01 ----
GalarPorta_G38M05_o4::
	warp MAP_GALAR_ISLE_OF_ARMOR_01, 10, 9
	waitstate
	end


@ ---- Galar_IsleOfArmor12 (g38m08), 0x88D27DC -> MAP_GALAR_ISLE_OF_ARMOR_01 ----
GalarPorta_G38M08_o3::
	warp MAP_GALAR_ISLE_OF_ARMOR_01, 10, 9
	waitstate
	end


@ ---- Galar_WildArea22 (g42m15), 0x88D2148 -> MAP_GALAR_WILD_AREA_17 ----
GalarPorta_G42M15_o16::
	warp MAP_GALAR_WILD_AREA_17, 39, 34
	waitstate
	end

