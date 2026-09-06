@ Portas de SCRIPT dos orfaos de Galar (onda 2 lote F; onda 3 lote M).
@ Gerado por dev_scripts/portas_script_galar.py; NAO editar a mao.
@
@ Cada rotulo aqui e a transcricao do script do demake que contem `warp` e cai
@ num mapa que nenhum caminho alcanca. O tradutor e o mesmo do c3
@ (cenas_galar.py) e do c4a (objetos_galar.py); o que ele recusa nao aparece
@ aqui, aparece no relatorio com motivo.
@
@ TRES COISAS SAEM DO SCRIPT DA FONTE, e as tres aparecem em comentario no
@ bloco em que acontecem, nunca caladas:
@   * FALA CORTADA: fala que este lote nao consegue escrever em ingles. Galar
@     fala ingles (decisao 32 do Gui) e este lote nao traduz texto novo; o
@     portugues esta em dev_scripts/onda3_lote_m_falta_traduzir.json.
@   * GUARDA DE MOTOR DO DEMAKE SOLTA: `checkflag`/`compare` de flag ou var que
@     NENHUM script nosso escreve. Dar nome a ela seria escrever porta que nunca
@     abre; o ramo que leva ao `warp` fica, o outro sai.
@   * trainerbattle SEM treinador nosso: a batalha sai e a porta segue so com o
@     `warp`. Quando ha treinador numerado por treinadores_galar.py, a batalha
@     FICA, pelo molde sem intro (`goto_if_defeated` + `trainerbattle_no_intro`),
@     que e o unico que a C28 deixa passar em entrada sem objeto selecionado.
@
@ PRECEDENCIA: o rotulo daqui comeca com `GalarPorta_`, e ele esta em
@ `objetos_galar.MANDAM_MAIS`, a lista UNICA que objetos_galar.py (linha 129),
@ fala_galar.py (linha 745) e treinadores_galar.py (desde a onda 3) consultam
@ antes de escrever o campo `script` de um map.json de Galar. Por isso a porta
@ PODE tomar objeto que tem `GalarObj_`, `GalarFala_`, `GalarFalaI_` ou
@ `GalarTrn_`: o rotulo antigo continua definido no `.inc` dele e vira ROM
@ parada, e nada se perde, porque a porta transcreve a MESMA cena da fonte mais
@ o `warp` (no caso da fala, com a igualdade de ponteiro provada) ou a MESMA
@ batalha (no caso do treinador, chamando o texto de derrota dele).
@ Quem escrever campo `script` de map.json de Galar depois desta onda precisa
@ chamar `objetos_galar.manda_mais` antes, senao a porta se apaga calada.

@ ---- Galar_Wedgehurst12 (g03m01), 0x891C50A -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M01_o5::
	goto GalarPorta_G03M01_o5_b1

GalarPorta_G03M01_o5_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Motostoke23 (g03m02), 0x882CC28 -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M02_o8::
	goto GalarPorta_G03M02_o8_b1

GalarPorta_G03M02_o8_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Turffield12 (g03m03), 0x891C50A -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M03_o10::
	goto GalarPorta_G03M03_o10_b1

GalarPorta_G03M03_o10_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Hulbury16 (g03m04), 0x891C50A -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M04_o13::
	goto GalarPorta_G03M04_o13_b1

GalarPorta_G03M04_o13_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Hammerlocke01 (g03m05), 0x891C50A -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M05_o24::
	goto GalarPorta_G03M05_o24_b1

GalarPorta_G03M05_o24_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Hammerlocke23 (g03m06), 0x891C50A -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M06_o11::
	goto GalarPorta_G03M06_o11_b1

GalarPorta_G03M06_o11_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Ballonlea10 (g03m07), 0x8A41B41 -> MAP_GALAR_HAMMERLOCKE_06 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x824, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M07_c0::
	lock
	faceplayer
	call GalarPorta_G03M07_c0_b1
	end

GalarPorta_G03M07_c0_b1::
	setvar VAR_GALAR_PORTA_G03M07, 1
	applymovement 2, GalarPorta_G03M07_c0_Mov0
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G03M07_c0_Mov1
	waitmovement 0
	msgbox GalarPorta_G03M07_c0_Text0, MSGBOX_AUTOCLOSE
	removeobject 2
	warp MAP_GALAR_HAMMERLOCKE_06, 54, 28
	waitstate
	release
	end

GalarPorta_G03M07_c0_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M07_c0_Mov1:
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M07_c0_Text0:
	.string "Opal: Hold on now. If you're heading to\n"
	.string "the next Gym, you'll need to go to\l"
	.string "Hammerlocke. I also have a few things\l"
	.string "to sort out there. Would you like to join\l"
	.string "me for the walk?\p"
	.string "{PLAYER}: Gladly!\p"
	.string "Opal: So we're a duet, after all.$"

@ ---- Galar_Ballonlea10 (g03m07), 0x8A48779 -> MAP_GALAR_HAMMERLOCKE_06 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x824, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M07_c1::
	lock
	faceplayer
	call GalarPorta_G03M07_c1_b1
	end

GalarPorta_G03M07_c1_b1::
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G03M07_c1_Mov0
	waitmovement 0
	goto GalarPorta_G03M07_c1_b2

GalarPorta_G03M07_c1_b2::
	setvar VAR_GALAR_PORTA_G03M07, 1
	applymovement 2, GalarPorta_G03M07_c1_Mov1
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G03M07_c1_Mov2
	waitmovement 0
	msgbox GalarPorta_G03M07_c1_Text0, MSGBOX_AUTOCLOSE
	removeobject 2
	warp MAP_GALAR_HAMMERLOCKE_06, 54, 28
	waitstate
	release
	end

GalarPorta_G03M07_c1_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_RIGHT
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M07_c1_Mov1:
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M07_c1_Mov2:
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M07_c1_Text0:
	.string "Opal: Hold on now. If you're heading to\n"
	.string "the next Gym, you'll need to go to\l"
	.string "Hammerlocke. I also have a few things\l"
	.string "to sort out there. Would you like to join\l"
	.string "me for the walk?\p"
	.string "{PLAYER}: Gladly!\p"
	.string "Opal: So we're a duet, after all.$"

@ ---- Galar_Ballonlea10 (g03m07), 0x8A4A1C5 -> MAP_GALAR_HAMMERLOCKE_06 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x824, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M07_c2::
	lock
	faceplayer
	call GalarPorta_G03M07_c2_b1
	end

GalarPorta_G03M07_c2_b1::
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G03M07_c2_Mov0
	waitmovement 0
	goto GalarPorta_G03M07_c2_b2

GalarPorta_G03M07_c2_b2::
	setvar VAR_GALAR_PORTA_G03M07, 1
	applymovement 2, GalarPorta_G03M07_c2_Mov1
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G03M07_c2_Mov2
	waitmovement 0
	msgbox GalarPorta_G03M07_c2_Text0, MSGBOX_AUTOCLOSE
	removeobject 2
	warp MAP_GALAR_HAMMERLOCKE_06, 54, 28
	waitstate
	release
	end

GalarPorta_G03M07_c2_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_LEFT
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M07_c2_Mov1:
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M07_c2_Mov2:
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M07_c2_Text0:
	.string "Opal: Hold on now. If you're heading to\n"
	.string "the next Gym, you'll need to go to\l"
	.string "Hammerlocke. I also have a few things\l"
	.string "to sort out there. Would you like to join\l"
	.string "me for the walk?\p"
	.string "{PLAYER}: Gladly!\p"
	.string "Opal: So we're a duet, after all.$"

@ ---- Galar_Ballonlea10 (g03m07), 0x891C50A -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M07_o2::
	goto GalarPorta_G03M07_o2_b1

GalarPorta_G03M07_o2_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Circhester16 (g03m08), 0x8AB913C -> MAP_GALAR_HULBURY_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x825, ramo fecha (nenhum script nosso escreve nela)
GalarPorta_G03M08_c0::
	lock
	faceplayer
	setvar VAR_GALAR_PORTA_G03M08, 1
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G03M08_c0_Mov0
	applymovement 16, GalarPorta_G03M08_c0_Mov1
	waitmovement 0
	goto GalarPorta_G03M08_c0_b1

GalarPorta_G03M08_c0_b1::
	lock
	faceplayer
	msgbox GalarPorta_G03M08_c0_Text0, MSGBOX_AUTOCLOSE
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_5FD
	removeobject 17
	fadescreen 0
	release
	goto GalarPorta_G03M08_c0_b2

GalarPorta_G03M08_c0_b2::
	setvar VAR_GALAR_PORTA_G03M08, 1
	warp MAP_GALAR_HULBURY_01, 12, 27
	waitstate
	end

GalarPorta_G03M08_c0_Mov0:
	.byte MOVEMENT_ACTION_FACE_RIGHT
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M08_c0_Mov1:
	.byte MOVEMENT_ACTION_FACE_LEFT
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G03M08_c0_Text0:
	.string "Sonia: Your battle was brilliant! The\n"
	.string "Gym Leader was really strong, but you\l"
	.string "had no trouble beating him.\p"
	.string "Circhester has great restaurants.\n"
	.string "There are a few things I want to talk\l"
	.string "about, so let's go to a restaurant to\l"
	.string "celebrate your victory! The\l"
	.string "restaurant's name is Bob's Your Uncle!$"

@ ---- Galar_Spikemuth09 (g03m10), 0x891C50A -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G03M10_o11::
	goto GalarPorta_G03M10_o11_b1

GalarPorta_G03M10_o11_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


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
	.string "You're Gym Challengers, right?\p"
	.string "You can rest for today. Tomorrow is the\n"
	.string "opening ceremony.$"
GalarPorta_G06M12_o7_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_UP
	.byte MOVEMENT_ACTION_WALK_NORMAL_UP
	.byte MOVEMENT_ACTION_WALK_NORMAL_UP
	.byte MOVEMENT_ACTION_WALK_NORMAL_LEFT
	.byte MOVEMENT_ACTION_FACE_DOWN
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G06M12_o7_Text1:
	.string "So that's it, {PLAYER}. Let's rest.\p"
	.string "Tomorrow is the big day.$"
GalarPorta_G06M12_o7_Text2:
	.string "This hotel is known all over the world!$"

@ ---- Galar_Hammerlocke04 (g09m10), 0x891C50A -> MAP_GALAR_STOW_ON_SIDE_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo fecha (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: compare_var_to_value 0x5467, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G09M10_o23::
	goto GalarPorta_G09M10_o23_b1

GalarPorta_G09M10_o23_b1::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Hammerlocke04 (g09m10), 0x8877934 -> MAP_GALAR_STOW_ON_SIDE_01 ----
GalarPorta_G09M10_o24::
	warp MAP_GALAR_STOW_ON_SIDE_01, 2, 2
	waitstate
	end


@ ---- Galar_Ballonlea05 (g11m10), 0x89EE1CD -> MAP_GALAR_HAMMERLOCKE_06 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x825, ramo abre (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x824, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G11M10_c0::
	lock
	faceplayer
	call GalarPorta_G11M10_c0_b1
	end

GalarPorta_G11M10_c0_b1::
	lock
	faceplayer
	call GalarPorta_G11M10_c0_b2
	end

GalarPorta_G11M10_c0_b2::
	setvar VAR_GALAR_PORTA_G11M10, 1
	applymovement 2, GalarPorta_G11M10_c0_Mov0
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G11M10_c0_Mov1
	waitmovement 0
	msgbox GalarPorta_G11M10_c0_Text0, MSGBOX_AUTOCLOSE
	removeobject 2
	warp MAP_GALAR_HAMMERLOCKE_06, 54, 28
	waitstate
	release
	end

GalarPorta_G11M10_c0_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G11M10_c0_Mov1:
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G11M10_c0_Text0:
	.string "Opal: Hold on now. If you're heading to\n"
	.string "the next Gym, you'll need to go to\l"
	.string "Hammerlocke. I also have a few things\l"
	.string "to sort out there. Would you like to join\l"
	.string "me for the walk?\p"
	.string "{PLAYER}: Gladly!\p"
	.string "Opal: So we're a duet, after all.$"

@ ---- Galar_Ballonlea05 (g11m10), 0x89EE9BF -> MAP_GALAR_HAMMERLOCKE_06 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x825, ramo abre (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x824, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G11M10_c1::
	lock
	faceplayer
	call GalarPorta_G11M10_c1_b1
	end

GalarPorta_G11M10_c1_b1::
	lock
	faceplayer
	call GalarPorta_G11M10_c1_b2
	end

GalarPorta_G11M10_c1_b2::
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G11M10_c1_Mov0
	waitmovement 0
	goto GalarPorta_G11M10_c1_b3

GalarPorta_G11M10_c1_b3::
	setvar VAR_GALAR_PORTA_G11M10, 1
	applymovement 2, GalarPorta_G11M10_c1_Mov1
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G11M10_c1_Mov2
	waitmovement 0
	msgbox GalarPorta_G11M10_c1_Text0, MSGBOX_AUTOCLOSE
	removeobject 2
	warp MAP_GALAR_HAMMERLOCKE_06, 54, 28
	waitstate
	release
	end

GalarPorta_G11M10_c1_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_RIGHT
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G11M10_c1_Mov1:
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G11M10_c1_Mov2:
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G11M10_c1_Text0:
	.string "Opal: Hold on now. If you're heading to\n"
	.string "the next Gym, you'll need to go to\l"
	.string "Hammerlocke. I also have a few things\l"
	.string "to sort out there. Would you like to join\l"
	.string "me for the walk?\p"
	.string "{PLAYER}: Gladly!\p"
	.string "Opal: So we're a duet, after all.$"

@ ---- Galar_Ballonlea05 (g11m10), 0x89EE9CC -> MAP_GALAR_HAMMERLOCKE_06 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x825, ramo abre (nenhum script nosso escreve nela)
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x824, ramo abre (nenhum script nosso escreve nela)
GalarPorta_G11M10_c2::
	lock
	faceplayer
	call GalarPorta_G11M10_c2_b1
	end

GalarPorta_G11M10_c2_b1::
	lock
	faceplayer
	call GalarPorta_G11M10_c2_b2
	end

GalarPorta_G11M10_c2_b2::
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G11M10_c2_Mov0
	waitmovement 0
	goto GalarPorta_G11M10_c2_b3

GalarPorta_G11M10_c2_b3::
	setvar VAR_GALAR_PORTA_G11M10, 1
	applymovement 2, GalarPorta_G11M10_c2_Mov1
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G11M10_c2_Mov2
	waitmovement 0
	msgbox GalarPorta_G11M10_c2_Text0, MSGBOX_AUTOCLOSE
	removeobject 2
	warp MAP_GALAR_HAMMERLOCKE_06, 54, 28
	waitstate
	release
	end

GalarPorta_G11M10_c2_Mov0:
	.byte MOVEMENT_ACTION_WALK_NORMAL_LEFT
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G11M10_c2_Mov1:
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_WALK_NORMAL_DOWN
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G11M10_c2_Mov2:
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G11M10_c2_Text0:
	.string "Opal: Hold on now. If you're heading to\n"
	.string "the next Gym, you'll need to go to\l"
	.string "Hammerlocke. I also have a few things\l"
	.string "to sort out there. Would you like to join\l"
	.string "me for the walk?\p"
	.string "{PLAYER}: Gladly!\p"
	.string "Opal: So we're a duet, after all.$"

@ ---- Galar_Circhester06 (g12m10), 0x8AB913C -> MAP_GALAR_HULBURY_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x825, ramo fecha (nenhum script nosso escreve nela)
GalarPorta_G12M10_c0::
	lock
	faceplayer
	setvar VAR_GALAR_PORTA_G12M10, 1
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G12M10_c0_Mov0
	applymovement 16, GalarPorta_G12M10_c0_Mov1
	waitmovement 0
	goto GalarPorta_G12M10_c0_b1

GalarPorta_G12M10_c0_b1::
	lock
	faceplayer
	msgbox GalarPorta_G12M10_c0_Text0, MSGBOX_AUTOCLOSE
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_5FE
	removeobject 17
	fadescreen 0
	release
	goto GalarPorta_G12M10_c0_b2

GalarPorta_G12M10_c0_b2::
	setvar VAR_GALAR_PORTA_G12M10, 1
	warp MAP_GALAR_HULBURY_01, 12, 27
	waitstate
	end

GalarPorta_G12M10_c0_Mov0:
	.byte MOVEMENT_ACTION_FACE_RIGHT
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G12M10_c0_Mov1:
	.byte MOVEMENT_ACTION_FACE_LEFT
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G12M10_c0_Text0:
	.string "Sonia: Your battle was brilliant! The\n"
	.string "Gym Leader was really strong, but you\l"
	.string "had no trouble beating him.\p"
	.string "Circhester has great restaurants.\n"
	.string "There are a few things I want to talk\l"
	.string "about, so let's go to a restaurant to\l"
	.string "celebrate your victory! The\l"
	.string "restaurant's name is Bob's Your Uncle!$"

@ ---- Galar_Circhester06 (g12m10), 0x886CF40 -> MAP_GALAR_HULBURY_01 ----
@ GUARDA DE MOTOR DO DEMAKE SOLTA: checkflag 0x825, ramo fecha (nenhum script nosso escreve nela)
GalarPorta_G12M10_c1::
	lock
	faceplayer
	setvar VAR_GALAR_PORTA_G12M10, 1
	applymovement 16, GalarPorta_G12M10_c1_Mov0
	applymovement OBJ_EVENT_ID_PLAYER, GalarPorta_G12M10_c1_Mov1
	waitmovement 0
	goto GalarPorta_G12M10_c1_b1

GalarPorta_G12M10_c1_b1::
	lock
	faceplayer
	msgbox GalarPorta_G12M10_c1_Text0, MSGBOX_AUTOCLOSE
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_5FE
	removeobject 17
	fadescreen 0
	release
	goto GalarPorta_G12M10_c1_b2

GalarPorta_G12M10_c1_b2::
	setvar VAR_GALAR_PORTA_G12M10, 1
	warp MAP_GALAR_HULBURY_01, 12, 27
	waitstate
	end

GalarPorta_G12M10_c1_Mov0:
	.byte MOVEMENT_ACTION_FACE_RIGHT
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G12M10_c1_Mov1:
	.byte MOVEMENT_ACTION_FACE_LEFT
	.byte MOVEMENT_ACTION_STEP_END
GalarPorta_G12M10_c1_Text0:
	.string "Sonia: Your battle was brilliant! The\n"
	.string "Gym Leader was really strong, but you\l"
	.string "had no trouble beating him.\p"
	.string "Circhester has great restaurants.\n"
	.string "There are a few things I want to talk\l"
	.string "about, so let's go to a restaurant to\l"
	.string "celebrate your victory! The\l"
	.string "restaurant's name is Bob's Your Uncle!$"

@ ---- Galar_TurffieldIndoor09 (g35m08), 0x889D154 -> MAP_GALAR_TURFFIELD_INDOOR_10 ----
GalarPorta_G35M08_o12::
	msgbox GalarPorta_G35M08_o12_Text0, MSGBOX_AUTOCLOSE
	@ trainerbattle tipo 3, treinador 402 da fonte: SAIU. Nenhum treinador nosso foi numerado para esta entrada por treinadores_galar.py, e a porta segue so com o warp (decisao da condutora, onda 3 lote M).
	msgbox GalarPorta_G35M08_o12_Text1, MSGBOX_AUTOCLOSE
	special HealPlayerParty
	warp MAP_GALAR_TURFFIELD_INDOOR_10, 7, 5
	waitstate
	release
	end

GalarPorta_G35M08_o12_Text0:
	.string "To become a Pokémon Master, I have to\n"
	.string "accept every challenge that comes my\l"
	.string "way, and this one is no different. Let's\l"
	.string "show them what we're capable of,\l"
	.string "Pikachu!!!$"
GalarPorta_G35M08_o12_Text1:
	.string "The Champion of this stage of the World\n"
	.string "Tournament is, {PLAYER}.$"

@ ---- Galar_TurffieldIndoor13 (g35m12), 0x889D4D4 -> MAP_GALAR_TURFFIELD_INDOOR_14 ----
GalarPorta_G35M12_o12::
	msgbox GalarPorta_G35M12_o12_Text0, MSGBOX_AUTOCLOSE
	@ trainerbattle tipo 3, treinador 406 da fonte: SAIU. Nenhum treinador nosso foi numerado para esta entrada por treinadores_galar.py, e a porta segue so com o warp (decisao da condutora, onda 3 lote M).
	msgbox GalarPorta_G35M12_o12_Text1, MSGBOX_AUTOCLOSE
	special HealPlayerParty
	warp MAP_GALAR_TURFFIELD_INDOOR_14, 7, 5
	waitstate
	release
	end

GalarPorta_G35M12_o12_Text0:
	.string "Get ready to feel the strength of the\n"
	.string "strongest Trainer of Water-type\l"
	.string "Pokémon.$"
GalarPorta_G35M12_o12_Text1:
	.string "The Champion of this stage of the World\n"
	.string "Tournament is, {PLAYER}.$"

@ ---- Galar_TurffieldIndoor17 (g35m16), 0x889DA44 -> MAP_GALAR_TURFFIELD_INDOOR_18 ----
GalarPorta_G35M16_o12::
	msgbox GalarPorta_G35M16_o12_Text0, MSGBOX_AUTOCLOSE
	@ trainerbattle tipo 3, treinador 421 da fonte: SAIU. Nenhum treinador nosso foi numerado para esta entrada por treinadores_galar.py, e a porta segue so com o warp (decisao da condutora, onda 3 lote M).
	msgbox GalarPorta_G35M16_o12_Text1, MSGBOX_AUTOCLOSE
	special HealPlayerParty
	warp MAP_GALAR_TURFFIELD_INDOOR_18, 7, 5
	waitstate
	release
	end

GalarPorta_G35M16_o12_Text0:
	.string "A tournament as incredible as this one,\n"
	.string "I couldn't miss the chance to take part.\l"
	.string "You can expect a great battle!$"
GalarPorta_G35M16_o12_Text1:
	.string "The Champion of this stage of the World\n"
	.string "Tournament is, {PLAYER}.$"

@ ---- Galar_TurffieldIndoor21 (g35m20), 0x889DED0 -> MAP_GALAR_TURFFIELD_INDOOR_22 ----
GalarPorta_G35M20_o12::
	msgbox GalarPorta_G35M20_o12_Text0, MSGBOX_AUTOCLOSE
	@ trainerbattle tipo 3, treinador 425 da fonte: SAIU. Nenhum treinador nosso foi numerado para esta entrada por treinadores_galar.py, e a porta segue so com o warp (decisao da condutora, onda 3 lote M).
	msgbox GalarPorta_G35M20_o12_Text1, MSGBOX_AUTOCLOSE
	special HealPlayerParty
	warp MAP_GALAR_TURFFIELD_INDOOR_22, 7, 5
	waitstate
	release
	end

GalarPorta_G35M20_o12_Text0:
	.string "It's time to show the full power of a\n"
	.string "Trainer, I'm going to show you a\l"
	.string "strength never seen before.$"
GalarPorta_G35M20_o12_Text1:
	.string "The Champion of this stage of the World\n"
	.string "Tournament is, {PLAYER}.$"

@ ---- Galar_TurffieldIndoor25 (g35m24), 0x88A4810 -> MAP_GALAR_TURFFIELD_INDOOR_26 ----
GalarPorta_G35M24_o12::
	msgbox GalarPorta_G35M24_o12_Text0, MSGBOX_AUTOCLOSE
	@ trainerbattle tipo 3, treinador 472 da fonte: SAIU. Nenhum treinador nosso foi numerado para esta entrada por treinadores_galar.py, e a porta segue so com o warp (decisao da condutora, onda 3 lote M).
	msgbox GalarPorta_G35M24_o12_Text1, MSGBOX_AUTOCLOSE
	special HealPlayerParty
	warp MAP_GALAR_TURFFIELD_INDOOR_26, 7, 5
	waitstate
	release
	end

GalarPorta_G35M24_o12_Text0:
	.string "Now it's time, time to show my skill as a\n"
	.string "Trainer to all of Galar, LET'S GO!!$"
GalarPorta_G35M24_o12_Text1:
	.string "The Champion of this stage of the World\n"
	.string "Tournament is, {PLAYER}.$"

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


@ ---- Galar_WildAreaIndoor01 (g39m16), 0x88D10A8 -> MAP_GALAR_WYNDON_INDOOR_01 ----
GalarPorta_G39M16_o0::
	lock
	faceplayer
	@ setflag 0x90E da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	@ setflag 0x918 da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	msgbox GalarPorta_G39M16_o0_Text0, MSGBOX_AUTOCLOSE
	@ trainerbattle tipo 3, treinador 351 da fonte: SAIU. Nenhum treinador nosso foi numerado para esta entrada por treinadores_galar.py, e a porta segue so com o warp (decisao da condutora, onda 3 lote M).
	msgbox GalarPorta_G39M16_o0_Text1, MSGBOX_AUTOCLOSE
	special HealPlayerParty
	@ clearflag 0x90E da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	@ clearflag 0x918 da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	warp MAP_GALAR_WYNDON_INDOOR_01, 6, 11
	waitstate
	end

GalarPorta_G39M16_o0_Text0:
	.string "I'm Marcelo AF. sousa, the first member\n"
	.string "of the pcl.g channel. Show me what\l"
	.string "you've got, let's see if you're able to\l"
	.string "beat me!!!$"
GalarPorta_G39M16_o0_Text1:
	.string "All right, no hard feelings. Now you can\n"
	.string "move on$"

@ ---- Galar_WildArea22 (g42m15), 0x88D2148 -> MAP_GALAR_WILD_AREA_17 ----
GalarPorta_G42M15_o16::
	warp MAP_GALAR_WILD_AREA_17, 39, 34
	waitstate
	end

