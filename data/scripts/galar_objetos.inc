@ Cenas de OBJETO de Galar (bloco c4a da fase de conteudo).
@ Gerado por dev_scripts/objetos_galar.py; NAO editar a mao.
@ Rotulo GalarObj_* tem PRECEDENCIA sobre GalarFala_*: onde a cena
@ inteira foi portada, ela ja contem a fala que o balde (a) deu.
@ Ordem: a da rota da historia, de Postwick e Wedgehurst em diante.

@ ---- Galar_Postwick169 (g40m12) ----
GalarObj_G40M12_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M12_o0_b1
	goto GalarObj_G40M12_o0_b2

GalarObj_G40M12_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M12_o0_b3
	msgbox GalarObj_G40M12_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M12_o0_Mart0
	msgbox GalarObj_G40M12_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M12_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M12_o0_b3
	msgbox GalarObj_G40M12_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M12_o0_Mart23
	msgbox GalarObj_G40M12_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M12_o0_b3::
	release
	end

GalarObj_G40M12_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M12_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M12_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M12_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M12_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M12_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Postwick21 (g04m00) ----
GalarObj_G04M00_bg0::
	lockall
	compare VAR_FACING, 2
	goto_if 1, GalarObj_G04M00_bg0_b1
	msgbox GalarObj_G04M00_bg0_Text0, MSGBOX_DEFAULT
	releaseall
	end

GalarObj_G04M00_bg0_b1::
	checkplayergender
	compare VAR_RESULT, 0
	call_if 1, GalarObj_G04M00_bg0_b2
	compare VAR_RESULT, 1
	call_if 1, GalarObj_G04M00_bg0_b3
	releaseall
	end

GalarObj_G04M00_bg0_b2::
	msgbox GalarObj_G04M00_bg0_Text1, MSGBOX_DEFAULT
	return

GalarObj_G04M00_bg0_b3::
	msgbox GalarObj_G04M00_bg0_Text2, MSGBOX_DEFAULT
	return

GalarObj_G04M00_bg0_Text0:
	.string "Oops, wrong side…$"
GalarObj_G04M00_bg0_Text1:
	.string "There’s a movie on TV.\nFour boys are walking on railroad\ltracks.\p…I better go, too.$"
GalarObj_G04M00_bg0_Text2:
	.string "There’s a movie on TV.\nA girl with her hair in pigtails is\lwalking up a brick road.\p…I better go, too.$"

@ ---- Galar_Postwick22 (g04m03) ----
GalarObj_G04M03_o4::
	lock
	faceplayer
	compare VAR_GALAR_G04M03_CENA, 3
	goto_if 1, GalarObj_G04M03_o4_b1
	compare VAR_GALAR_G04M03_CENA, 2
	goto_if 1, GalarObj_G04M03_o4_b2
	msgbox GalarObj_G04M03_o4_Text0, MSGBOX_DEFAULT
	release
	end

GalarObj_G04M03_o4_b1::
	msgbox GalarObj_G04M03_o4_Text1, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G04M03_o4_b2::
	msgbox GalarObj_G04M03_o4_Text2, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G04M03_o4_Text0:
	.string "{RIVAL}: What, it’s only {PLAYER}?\nGramps isn’t around.$"
GalarObj_G04M03_o4_Text1:
	.string "Hop: Meu pokémon parece ser\nforte!$"
GalarObj_G04M03_o4_Text2:
	.string "Hop: Vamos, {PLAYER}!!!\nEscolha seu pokémon!!!$"

@ ---- Galar_SlumberingWeald03 (g04m11) ----
GalarObj_G04M11_o6::
	lock
	faceplayer
	msgbox GalarObj_G04M11_o6_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G04M11_o6_Text0:
	.string "Hop:Dê uma olhada nisso, {PLAYER}!\nIsso é algo que você não vê todos\los dias ...\pEste lugar definitivamente parece\nsair de uma lenda.$"

@ ---- Galar_Wedgehurst02 (g05m02) ----
GalarObj_G05M02_o0::
	lock
	faceplayer
	msgbox GalarObj_G05M02_o0_Text0, MSGBOX_DEFAULT
	closemessage
	applymovement 1, GalarObj_G05M02_o0_Mov0
	waitmovement 0
	release
	end

GalarObj_G05M02_o0_Text0:
	.string "Okay!\pBe sure to read what’s on the\nblackboard carefully!$"
GalarObj_G05M02_o0_Mov0:
	.byte MOVEMENT_ACTION_FACE_ORIGINAL_DIRECTION
	.byte MOVEMENT_ACTION_STEP_END

GalarObj_G05M02_o1::
	lock
	faceplayer
	msgbox GalarObj_G05M02_o1_Text0, MSGBOX_DEFAULT
	closemessage
	applymovement 2, GalarObj_G05M02_o1_Mov0
	waitmovement 0
	release
	end

GalarObj_G05M02_o1_Text0:
	.string "Whew! I’m trying to memorize all my\nnotes.$"
GalarObj_G05M02_o1_Mov0:
	.byte MOVEMENT_ACTION_FACE_UP
	.byte MOVEMENT_ACTION_STEP_END

@ ---- Galar_Wedgehurst03 (g05m04) ----
GalarObj_G05M04_o2::
	lock
	faceplayer
	compare VAR_GALAR_G05M04_OBJ, 1
	goto_if 4, GalarObj_G05M04_o2_b1
	msgbox GalarObj_G05M04_o2_Text0, MSGBOX_DEFAULT
	closemessage
	call GalarObj_G05M04_o2_b2
	msgbox GalarObj_G05M04_o2_Text1, MSGBOX_DEFAULT
	release
	end

GalarObj_G05M04_o2_b1::
	msgbox GalarObj_G05M04_o2_Text2, MSGBOX_DEFAULT
	release
	end

GalarObj_G05M04_o2_b2::
	fadescreen 1
	playfanfare 256
	waitfanfare
	special HealPlayerParty
	fadescreen 0
	return

GalarObj_G05M04_o2_Text0:
	.string "You look tired.\nYou should take a quick nap.$"
GalarObj_G05M04_o2_Text1:
	.string "Don’t give up!$"
GalarObj_G05M04_o2_Text2:
	.string "Thank you so much.$"

@ ---- Galar_Wedgehurst07 (g05m11) ----
GalarObj_G05M11_o1::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G05M11_o1_b1
	goto GalarObj_G05M11_o1_b2

GalarObj_G05M11_o1_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G05M11_o1_b3
	msgbox GalarObj_G05M11_o1_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G05M11_o1_Mart0
	msgbox GalarObj_G05M11_o1_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G05M11_o1_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G05M11_o1_b3
	msgbox GalarObj_G05M11_o1_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G05M11_o1_Mart22
	msgbox GalarObj_G05M11_o1_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G05M11_o1_b3::
	release
	end

GalarObj_G05M11_o1_Text0:
	.string "Olá como posso ajudar você?$"
GalarObj_G05M11_o1_Text1:
	.string "Obrigado.$"
GalarObj_G05M11_o1_Text2:
	.string "Olá como posso ajudar você?$"
GalarObj_G05M11_o1_Text3:
	.string "Obrigado.$"
	.align 2
GalarObj_G05M11_o1_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_NONE
	.align 2
GalarObj_G05M11_o1_Mart22:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_NONE

@ ---- Galar_Wedgehurst09 (g06m13) ----
GalarObj_G06M13_o0::
	lock
	faceplayer
	msgbox GalarObj_G06M13_o0_Text0, MSGBOX_AUTOCLOSE
	warp MAP_GALAR_MOTOSTOKE_07, 7, 4
	waitstate
	release
	end

GalarObj_G06M13_o0_Text0:
	.string "Deixe-me levá-los à\ncerimônia de abertura!$"

GalarObj_G06M13_o1::
	lock
	faceplayer
	msgbox GalarObj_G06M13_o1_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M13_o1_Text0:
	.string "Hop: Vamos, {PLAYER}! A cerimônia é \nagora!$"

@ ---- Galar_Wedgehurst11 (g40m07) ----
GalarObj_G40M07_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M07_o0_b1
	goto GalarObj_G40M07_o0_b2

GalarObj_G40M07_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M07_o0_b3
	msgbox GalarObj_G40M07_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M07_o0_Mart0
	msgbox GalarObj_G40M07_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M07_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M07_o0_b3
	msgbox GalarObj_G40M07_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M07_o0_Mart23
	msgbox GalarObj_G40M07_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M07_o0_b3::
	release
	end

GalarObj_G40M07_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M07_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M07_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M07_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M07_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M07_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Wedgehurst17 (g40m08) ----
GalarObj_G40M08_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M08_o0_b1
	goto GalarObj_G40M08_o0_b2

GalarObj_G40M08_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M08_o0_b3
	msgbox GalarObj_G40M08_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M08_o0_Mart0
	msgbox GalarObj_G40M08_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M08_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M08_o0_b3
	msgbox GalarObj_G40M08_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M08_o0_Mart23
	msgbox GalarObj_G40M08_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M08_o0_b3::
	release
	end

GalarObj_G40M08_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M08_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M08_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M08_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M08_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M08_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Route0203 (g05m13) ----
GalarObj_G05M13_o2::
	msgbox GalarObj_G05M13_o2_Text0, MSGBOX_AUTOCLOSE
	closemessage
	@ clearflag 0x002 da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	@ setflag 0x233 da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	setvar VAR_0x8004, 1
	@ clearflag 0x033 da fonte: flag de motor do demake, sem leitor aqui (cenas_galar.py)
	applymovement 1, GalarObj_G05M13_o2_Mov0
	releaseall
	end

GalarObj_G05M13_o2_Text0:
	.string "Nada nada além de livros. $"
GalarObj_G05M13_o2_Mov0:
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END

@ ---- Galar_Route0301 (g06m17) ----
GalarObj_G06M17_o0::
	removeobject VAR_LAST_TALKED
	end


@ ---- Galar_GalarMine03 (g08m20) ----
GalarObj_G08M20_o0::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G08M20_o1::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G08M20_o5::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G08M20_o6::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G08M20_o7::
	removeobject VAR_LAST_TALKED
	end


@ ---- Galar_Motostoke01 (g00m06) ----
GalarObj_G00M06_o3::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G00M06_o3_b1
	lock
	faceplayer
	message GalarObj_G00M06_o3_Msg0
	waitmessage
	pokemart GalarObj_G00M06_o3_Mart2
	msgbox GalarObj_G00M06_o3_Text0, MSGBOX_DEFAULT
	release
	end

GalarObj_G00M06_o3_b1::
	removeobject 3
	fadescreen 0
	release
	end

GalarObj_G00M06_o3_Text0:
	.string "Please come again!$"
GalarObj_G00M06_o3_Msg0:
	.string "Hi, there!\nMay I help you?$"
	.align 2
GalarObj_G00M06_o3_Mart2:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_NONE

@ ---- Galar_Motostoke05 (g06m10) ----
GalarObj_G06M10_o15::
	checkitem ITEM_GO_GOGGLES, 1
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G06M10_o15_b1
	msgbox GalarObj_G06M10_o15_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M10_o15_b1::
	msgbox GalarObj_G06M10_o15_Text1, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G06M10_o15_b2
	call GalarObj_G06M10_o15_b3
	end

GalarObj_G06M10_o15_b2::
	warp MAP_GALAR_UNDERWATER_01, 14, 41
	waitstate
	end

GalarObj_G06M10_o15_b3::
	releaseall
	end

GalarObj_G06M10_o15_Text0:
	.string "Um local que da pra mergulhar\nmas precisa de equipamento$"
GalarObj_G06M10_o15_Text1:
	.string "Mergulhar?$"

@ ---- Galar_Motostoke06 (g06m12) ----
GalarObj_G06M12_o0::
	lock
	faceplayer
	msgbox GalarObj_G06M12_o0_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M12_o0_Text0:
	.string "Melhor você ir se resgistrar\n {PLAYER}$"

GalarObj_G06M12_o1::
	lock
	faceplayer
	msgbox GalarObj_G06M12_o1_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M12_o1_Text0:
	.string "faCa o nosso chek-in {PLAYER}$"

@ ---- Galar_Motostoke18 (g06m33) ----
GalarObj_G06M33_o0::
	checkitem ITEM_CARD_KEY, 1
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G06M33_o0_b1
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G06M33_o0_b2
	lock
	faceplayer
	msgbox GalarObj_G06M33_o0_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M33_o0_b1::
	lock
	faceplayer
	msgbox GalarObj_G06M33_o0_Text1, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M33_o0_b2::
	lock
	faceplayer
	@ checkflag FLAG_GALAR_ESCONDE_20B sem goto_if/call_if depois: leitura morta, o ramo da fonte nao atravessou o filtro (cenas_galar.py)
	msgbox GalarObj_G06M33_o0_Text2, MSGBOX_AUTOCLOSE
	removeobject 2
	fadescreen 0
	release
	end

GalarObj_G06M33_o0_Text0:
	.string "ola desafiante neste ginasio ha vaios\nmarowack vindos direto de alola,eles\pestao com um cartao capture um e pegue\no cartao dele e voce podera passar$"
GalarObj_G06M33_o0_Text1:
	.string "ola desafiante neste ginasio ha vaios\nmarowack vindos direto de alola,eles\pestao com um cartao capture um e pegue\no cartao dele e voce podera passar$"
GalarObj_G06M33_o0_Text2:
	.string "parabens voce conseguiu o cartao\nvoce ja pode passar!$"

@ ---- Galar_Motostoke20 (g06m35) ----
GalarObj_G06M35_o4::
	removeobject VAR_LAST_TALKED
	end


@ ---- Galar_Motostoke22 (g40m02) ----
GalarObj_G40M02_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M02_o0_b1
	goto GalarObj_G40M02_o0_b2

GalarObj_G40M02_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M02_o0_b3
	msgbox GalarObj_G40M02_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M02_o0_Mart0
	msgbox GalarObj_G40M02_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M02_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M02_o0_b3
	msgbox GalarObj_G40M02_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M02_o0_Mart23
	msgbox GalarObj_G40M02_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M02_o0_b3::
	release
	end

GalarObj_G40M02_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M02_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M02_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M02_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M02_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M02_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_WildArea02 (g03m42) ----
GalarObj_G03M42_o4::
	lock
	faceplayer
	msgbox GalarObj_G03M42_o4_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G03M42_o4_Text0:
	.string "Você por acaso é o {PLAYER}?Ouvir\ndizer que você foi endoçado pelo\lcampeao$"

@ ---- Galar_WildArea03 (g06m27) ----
GalarObj_G06M27_o20::
	checkitem ITEM_GO_GOGGLES, 1
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G06M27_o20_b1
	msgbox GalarObj_G06M27_o20_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M27_o20_b1::
	msgbox GalarObj_G06M27_o20_Text1, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G06M27_o20_b2
	call GalarObj_G06M27_o20_b3
	end

GalarObj_G06M27_o20_b2::
	warp MAP_GALAR_UNDERWATER_01, 33, 64
	waitstate
	end

GalarObj_G06M27_o20_b3::
	releaseall
	end

GalarObj_G06M27_o20_Text0:
	.string "Um local que da pra mergulhar\nmas precisa de equipamento$"
GalarObj_G06M27_o20_Text1:
	.string "Mergulhar?$"

@ ---- Galar_WildArea06 (g06m31) ----
GalarObj_G06M31_o1::
	lock
	faceplayer
	compare VAR_GALAR_G06M31_OBJ, 1
	goto_if 4, GalarObj_G06M31_o1_b1
	msgbox GalarObj_G06M31_o1_Text0, MSGBOX_DEFAULT
	closemessage
	call GalarObj_G06M31_o1_b2
	msgbox GalarObj_G06M31_o1_Text1, MSGBOX_DEFAULT
	release
	end

GalarObj_G06M31_o1_b1::
	msgbox GalarObj_G06M31_o1_Text2, MSGBOX_DEFAULT
	release
	end

GalarObj_G06M31_o1_b2::
	fadescreen 1
	playfanfare 256
	waitfanfare
	special HealPlayerParty
	fadescreen 0
	return

GalarObj_G06M31_o1_Text0:
	.string "You look tired.\nYou should take a quick nap.$"
GalarObj_G06M31_o1_Text1:
	.string "Don’t give up!$"
GalarObj_G06M31_o1_Text2:
	.string "Thank you so much.$"

@ ---- Galar_WildArea09 (g08m24) ----
GalarObj_G08M24_o9::
	checkitem ITEM_GO_GOGGLES, 1
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G08M24_o9_b1
	msgbox GalarObj_G08M24_o9_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M24_o9_b1::
	msgbox GalarObj_G08M24_o9_Text1, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G08M24_o9_b2
	call GalarObj_G08M24_o9_b3
	end

GalarObj_G08M24_o9_b2::
	warp MAP_GALAR_UNDERWATER_01, 61, 43
	waitstate
	end

GalarObj_G08M24_o9_b3::
	releaseall
	end

GalarObj_G08M24_o9_Text0:
	.string "Um local que da pra mergulhar\nmas precisa de equipamento$"
GalarObj_G08M24_o9_Text1:
	.string "Mergulhar?$"

@ ---- Galar_WildArea13 (g42m06) ----
GalarObj_G42M06_o8::
	lock
	faceplayer
	compare VAR_GALAR_G42M06_OBJ, 1
	goto_if 4, GalarObj_G42M06_o8_b1
	msgbox GalarObj_G42M06_o8_Text0, MSGBOX_DEFAULT
	closemessage
	call GalarObj_G42M06_o8_b2
	msgbox GalarObj_G42M06_o8_Text1, MSGBOX_DEFAULT
	release
	end

GalarObj_G42M06_o8_b1::
	msgbox GalarObj_G42M06_o8_Text2, MSGBOX_DEFAULT
	release
	end

GalarObj_G42M06_o8_b2::
	fadescreen 1
	playfanfare 256
	waitfanfare
	special HealPlayerParty
	fadescreen 0
	return

GalarObj_G42M06_o8_Text0:
	.string "You look tired.\nYou should take a quick nap.$"
GalarObj_G42M06_o8_Text1:
	.string "Don’t give up!$"
GalarObj_G42M06_o8_Text2:
	.string "Thank you so much.$"

@ ---- Galar_WildArea14 (g42m07) ----
GalarObj_G42M07_o11::
	lock
	faceplayer
	setvar VAR_0x8004, 10
	setvar VAR_0x8005, 5
	special SetFlavorTextFlagFromSpecialVars
	msgbox GalarObj_G42M07_o11_Text0, MSGBOX_DEFAULT
	release
	end

GalarObj_G42M07_o11_Text0:
	.string "Training by oneself is certainly\nnot a bad thing.\pBut it’s also not bad to aim for\nthe top with a partner.\pEven Bruno…\nHe trained with a fellow by the\lname of Brawly before.$"

@ ---- Galar_WildArea17 (g42m10) ----
GalarObj_G42M10_o23::
	checkitem ITEM_GO_GOGGLES, 1
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G42M10_o23_b1
	msgbox GalarObj_G42M10_o23_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G42M10_o23_b1::
	msgbox GalarObj_G42M10_o23_Text1, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G42M10_o23_b2
	call GalarObj_G42M10_o23_b3
	end

GalarObj_G42M10_o23_b2::
	warp MAP_GALAR_UNDERWATER_01, 32, 10
	waitstate
	end

GalarObj_G42M10_o23_b3::
	releaseall
	end

GalarObj_G42M10_o23_Text0:
	.string "Um local que da pra mergulhar\nmas precisa de equipamento$"
GalarObj_G42M10_o23_Text1:
	.string "Mergulhar?$"

@ ---- Galar_WildArea20 (g42m13) ----
GalarObj_G42M13_o9::
	checkitem ITEM_GO_GOGGLES, 1
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G42M13_o9_b1
	msgbox GalarObj_G42M13_o9_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G42M13_o9_b1::
	msgbox GalarObj_G42M13_o9_Text1, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G42M13_o9_b2
	call GalarObj_G42M13_o9_b3
	end

GalarObj_G42M13_o9_b2::
	warp MAP_GALAR_UNDERWATER_01, 67, 8
	waitstate
	end

GalarObj_G42M13_o9_b3::
	releaseall
	end

GalarObj_G42M13_o9_Text0:
	.string "Um local que da pra mergulhar\nmas precisa de equipamento$"
GalarObj_G42M13_o9_Text1:
	.string "Mergulhar?$"

@ ---- Galar_WildArea27 (g08m11) ----
GalarObj_G08M11_o1::
	checkitem ITEM_GO_GOGGLES, 1
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G08M11_o1_b1
	msgbox GalarObj_G08M11_o1_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M11_o1_b1::
	msgbox GalarObj_G08M11_o1_Text1, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G08M11_o1_b2
	call GalarObj_G08M11_o1_b3
	end

GalarObj_G08M11_o1_b2::
	warp MAP_GALAR_UNDERWATER_01, 67, 8
	waitstate
	end

GalarObj_G08M11_o1_b3::
	releaseall
	end

GalarObj_G08M11_o1_Text0:
	.string "Um local que da pra mergulhar\nmas precisa de equipamento$"
GalarObj_G08M11_o1_Text1:
	.string "Mergulhar?$"

@ ---- Galar_Turffield03 (g07m11) ----
GalarObj_G07M11_o0::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G07M11_o1::
	removeobject VAR_LAST_TALKED
	end


@ ---- Galar_Turffield11 (g40m15) ----
GalarObj_G40M15_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M15_o0_b1
	goto GalarObj_G40M15_o0_b2

GalarObj_G40M15_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M15_o0_b3
	msgbox GalarObj_G40M15_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M15_o0_Mart0
	msgbox GalarObj_G40M15_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M15_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M15_o0_b3
	msgbox GalarObj_G40M15_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M15_o0_Mart23
	msgbox GalarObj_G40M15_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M15_o0_b3::
	release
	end

GalarObj_G40M15_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M15_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M15_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M15_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M15_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M15_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Hulbury01 (g00m08) ----
GalarObj_G00M08_o0::
	lock
	faceplayer
	msgbox GalarObj_G00M08_o0_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M08_o0_Text0:
	.string "Oi {PLAYER}, você veio tambem?!\pque tal batalhamos depois de comer$"

@ ---- Galar_Hulbury03 (g08m02) ----
GalarObj_G08M02_bg0::
	lockall
	setvar VAR_0x8004, 14
	setvar VAR_0x8005, 2
	special SetFlavorTextFlagFromSpecialVars
	msgbox GalarObj_G08M02_bg0_Text0, MSGBOX_DEFAULT
	releaseall
	end

GalarObj_G08M02_bg0_Text0:
	.string "Pokémon Fan Magazine\nMonthly Grand Prize Drawing!\pThe application form is…\pGone! It’s been clipped out.\nSomeone must have applied already.$"

GalarObj_G08M02_o4::
	lock
	faceplayer
	checkflag FLAG_GALAR_ESCONDE_23C
	goto_if 1, GalarObj_G08M02_o4_b1
	msgbox GalarObj_G08M02_o4_Text0, MSGBOX_DEFAULT
	release
	end

GalarObj_G08M02_o4_b1::
	msgbox GalarObj_G08M02_o4_Text1, MSGBOX_DEFAULT
	release
	end

GalarObj_G08M02_o4_Text0:
	.string "That’s odd, Mr. Fuji isn’t here.\nWhere’d he go?$"
GalarObj_G08M02_o4_Text1:
	.string "Mr. Fuji had been praying alone\nfor Cubone’s mother.$"

GalarObj_G08M02_o5::
	lock
	faceplayer
	setvar VAR_0x8004, 14
	setvar VAR_0x8005, 0
	special SetFlavorTextFlagFromSpecialVars
	msgbox GalarObj_G08M02_o5_Text0, MSGBOX_DEFAULT
	release
	end

GalarObj_G08M02_o5_Text0:
	.string "This is really Mr. Fuji’s house.\pHe’s really kind.\pHe looks after abandoned and\norphaned Pokémon.$"

@ ---- Galar_Hulbury06 (g08m07) ----
GalarObj_G08M07_o11::
	lock
	faceplayer
	msgbox GalarObj_G08M07_o11_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o11_Text0:
	.string " {COLOR DARK_GRAY}Me dê licença, o presidente Rose\nestá neste restaurante\pEu estou tentando fazer uma\nmatéria sobre isso.$"

GalarObj_G08M07_o13::
	lock
	faceplayer
	msgbox GalarObj_G08M07_o13_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o13_Text0:
	.string " {COLOR DARK_GRAY}É sempre bom passear com seus\nPokémons.\pA cada {COLOR RED}128 passos{COLOR DARK_GRAY}, eles\nficam cada vez mais felizes.$"

GalarObj_G08M07_o14::
	lock
	faceplayer
	msgbox GalarObj_G08M07_o14_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o14_Text0:
	.string " {COLOR LIGHT_RED}Sério que você usa seus Pokémon\nem combate?\pEu nunca faria isso com meu\nZigzagoon, ele é um bebê.$"

GalarObj_G08M07_o18::
	lock
	faceplayer
	msgbox GalarObj_G08M07_o18_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o18_Text0:
	.string " {COLOR DARK_GRAY}Juro pela luz que me ilumina que\nvi um {COLOR BLUE}eevee{COLOR DARK_GRAY}, nadando até o\lhorizonte.\po Bolt tentou pular atrás dele mas\neu segurei.$"

GalarObj_G08M07_o3::
	msgbox GalarObj_G08M07_o3_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o3_Text0:
	.string "{COLOR DARK_GRAY}Parece que hoje o mar não está\npara peixe...$"

GalarObj_G08M07_o31::
	faceplayer
	lock
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G08M07_o31_b1
	msgbox GalarObj_G08M07_o31_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G08M07_o31_Mart0
	msgbox GalarObj_G08M07_o31_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G08M07_o31_b1::
	release
	end

GalarObj_G08M07_o31_Text0:
	.string "{COLOR BLUE}Bem vindo a minha venda, com o\nque posso te ajudar?$"
GalarObj_G08M07_o31_Text1:
	.string "{COLOR BLUE}Volte sempre!$"
	.align 2
GalarObj_G08M07_o31_Mart0:
	.2byte ITEM_NET_BALL
	.2byte ITEM_LUCKY_PUNCH
	.2byte ITEM_METAL_POWDER
	.2byte ITEM_THICK_CLUB
	.2byte ITEM_STICK
	.2byte ITEM_UP_GRADE
	.2byte ITEM_FLUFFY_TAIL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_NONE

GalarObj_G08M07_o32::
	faceplayer
	lock
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G08M07_o32_b1
	msgbox GalarObj_G08M07_o32_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G08M07_o32_Mart0
	msgbox GalarObj_G08M07_o32_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G08M07_o32_b1::
	release
	end

GalarObj_G08M07_o32_Text0:
	.string "{COLOR BLUE}Bem vindo a minha venda, com o\nque posso te ajudar?$"
GalarObj_G08M07_o32_Text1:
	.string "{COLOR BLUE}Volte sempre!$"
	.align 2
GalarObj_G08M07_o32_Mart0:
	.2byte ITEM_SAFARI_BALL
	.2byte ITEM_LEMONADE
	.2byte ITEM_HEAL_POWDER
	.2byte ITEM_ENERGY_POWDER
	.2byte ITEM_ENERGY_ROOT
	.2byte ITEM_RED_SCARF
	.2byte ITEM_BLUE_SCARF
	.2byte ITEM_PINK_SCARF
	.2byte ITEM_GREEN_SCARF
	.2byte ITEM_YELLOW_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Hulbury11 (g08m19) ----
GalarObj_G08M19_o0::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G08M19_o1::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G08M19_o2::
	removeobject VAR_LAST_TALKED
	end


@ ---- Galar_Hulbury14 (g40m00) ----
GalarObj_G40M00_o1::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M00_o1_b1
	goto GalarObj_G40M00_o1_b2

GalarObj_G40M00_o1_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M00_o1_b3
	msgbox GalarObj_G40M00_o1_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M00_o1_Mart0
	msgbox GalarObj_G40M00_o1_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M00_o1_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M00_o1_b3
	msgbox GalarObj_G40M00_o1_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M00_o1_Mart23
	msgbox GalarObj_G40M00_o1_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M00_o1_b3::
	release
	end

GalarObj_G40M00_o1_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M00_o1_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M00_o1_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M00_o1_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M00_o1_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M00_o1_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Hulbury15 (g40m10) ----
GalarObj_G40M10_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M10_o0_b1
	goto GalarObj_G40M10_o0_b2

GalarObj_G40M10_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M10_o0_b3
	msgbox GalarObj_G40M10_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M10_o0_Mart0
	msgbox GalarObj_G40M10_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M10_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M10_o0_b3
	msgbox GalarObj_G40M10_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M10_o0_Mart23
	msgbox GalarObj_G40M10_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M10_o0_b3::
	release
	end

GalarObj_G40M10_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M10_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M10_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M10_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M10_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M10_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Hammerlocke04 (g09m10) ----
GalarObj_G09M10_o17::
	lock
	faceplayer
	msgbox GalarObj_G09M10_o17_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G09M10_o17_Text0:
	.string "Ol {PLAYER},Viu a Sonia?$"

GalarObj_G09M10_o18::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G09M10_o19::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G09M10_o20::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G09M10_o21::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G09M10_o3::
	lock
	applymovement 4, GalarObj_G09M10_o3_Mov0
	waitmovement 0
	msgbox GalarObj_G09M10_o3_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G09M10_o3_Mov0:
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarObj_G09M10_o3_Text0:
	.string "Não atrapalhe nossa luta!$"

GalarObj_G09M10_o5::
	lock
	applymovement 5, GalarObj_G09M10_o5_Mov0
	waitmovement 0
	msgbox GalarObj_G09M10_o5_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G09M10_o5_Mov0:
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarObj_G09M10_o5_Text0:
	.string "Não atrapalhe nossa luta!$"

@ ---- Galar_Hammerlocke05 (g09m11) ----
GalarObj_G09M11_o1::
	msgbox GalarObj_G09M11_o1_Text0, MSGBOX_AUTOCLOSE
	msgbox GalarObj_G09M11_o1_Text1, MSGBOX_AUTOCLOSE
	setvar VAR_GALAR_G09M11_CENA, 1
	applymovement 3, GalarObj_G09M11_o1_Mov0
	applymovement 2, GalarObj_G09M11_o1_Mov1
	waitmovement 0
	msgbox GalarObj_G09M11_o1_Text2, MSGBOX_AUTOCLOSE
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_230
	removeobject 3
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_230
	removeobject 2
	fadescreen 0
	end

GalarObj_G09M11_o1_Text0:
	.string "Rose:O estádio de Hammerlocke\nfunciona como uma usina de energia.\pAgora,dê uma olhada no meu tablet.$"
GalarObj_G09M11_o1_Text1:
	.string "Eu tenho todas as informacoes que\pvocê precisa vê.\pRose:Vejo?Uma descricão fácil de\nentender da usina de energia!Primeiro,\pa energia é absorvida na torre do\nestádio de Hammerlocke.Em seguida,\pé transformada em eletricidade na\nusina subterranea e entregue as\ppessoas de toda a região de Galar!\nNossas vidas e a sociedade exigem\pvários tipos de fontes de energia,\ncomo eletricidade,gás natural,Meus\pgrupos associados visam melhorar\na vida de todos, aproveitando o$"
GalarObj_G09M11_o1_Mov0:
	.byte MOVEMENT_ACTION_FACE_RIGHT
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarObj_G09M11_o1_Mov1:
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarObj_G09M11_o1_Text2:
	.string "rose:hora de eu comecar a trabalhar.\nEu devo me mexer logo antes que\pOleana decida me dar mais avisos,\n{PLAYER},sugiro que você vá para o\pcofre em seguida.Apenas siga em\ndirecão   Rota 6 do estádio e você\pencontrará o cofre sem problemas!$"

GalarObj_G09M11_o4::
	lock
	faceplayer
	msgbox GalarObj_G09M11_o4_Text0, MSGBOX_AUTOCLOSE
	fadescreen 1
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_BA7
	removeobject 4
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_BA8
	removeobject 5
	fadescreen 0
	release
	end

GalarObj_G09M11_o4_Text0:
	.string "G-Gym Challenger! Você deve me\najudar! E-eu quero dizer,\lpor favor, me ajude!\pMeu Pokémon de repente Dynamaxed\npor algum motivo e começou a\lcorrer enlouquecido no estádio ...\lRaihan ... quero dizer, o Sr.\lRaihan foi capaz de subjugar o\lPokémon Dynamax no estádio,mas...\pSe outro Pokémon também Dynamax e\nentrar em f ria ...\la usina subterr nea entraria em\lcolapso!\pMr. Rose está lá embaixo agora!\pEu sei que isso é egoismo da\nminha parte, mas devo implorar\lsua ajuda!\pQuero que você entre na usina\nsubterr nea e pare o Sr.Rose!\pMr. Rose despertou um Pokémon\nconhecido como Eternatus ...\pAparentemente,a energia emitida\npor seu corpo é o que causa o\lDynamaxing.\pNesse ritmo, todos os Pokémon na\nregião de Galar irão Dynamax e\lenlouquecer!\lSe isso acontecesse...\pPor favor, você deve salvar o\nSr.Rose!\pVocê pode pegar o elevador\naté lá para alcançá-lo.\pEu pedi a ajuda do irmão mais novo\ndo Campeão também, mas quem sabe o\lque está acontecendo ...Oh não\l... Eternatus é- Oh, Sr.Rose ...$"

@ ---- Galar_Hammerlocke08 (g09m15) ----
GalarObj_G09M15_bg0::
	lockall
	compare VAR_FACING, 2
	goto_if 1, GalarObj_G09M15_bg0_b1
	msgbox GalarObj_G09M15_bg0_Text0, MSGBOX_DEFAULT
	releaseall
	end

GalarObj_G09M15_bg0_b1::
	checkplayergender
	compare VAR_RESULT, 0
	call_if 1, GalarObj_G09M15_bg0_b2
	compare VAR_RESULT, 1
	call_if 1, GalarObj_G09M15_bg0_b3
	releaseall
	end

GalarObj_G09M15_bg0_b2::
	msgbox GalarObj_G09M15_bg0_Text1, MSGBOX_DEFAULT
	return

GalarObj_G09M15_bg0_b3::
	msgbox GalarObj_G09M15_bg0_Text2, MSGBOX_DEFAULT
	return

GalarObj_G09M15_bg0_Text0:
	.string "Oops, wrong side…$"
GalarObj_G09M15_bg0_Text1:
	.string "There’s a movie on TV.\nFour boys are walking on railroad\ltracks.\p…I better go, too.$"
GalarObj_G09M15_bg0_Text2:
	.string "There’s a movie on TV.\nA girl with her hair in pigtails is\lwalking up a brick road.\p…I better go, too.$"

@ ---- Galar_Hammerlocke16 (g10m14) ----
GalarObj_G10M14_o1::
	lock
	faceplayer
	msgbox GalarObj_G10M14_o1_Text0, MSGBOX_DEFAULT
	goto GalarObj_G10M14_o1_b1

GalarObj_G10M14_o1_b1::
	closemessage
	applymovement VAR_LAST_TALKED, GalarObj_G10M14_o1_Mov0
	waitmovement 0
	release
	end

GalarObj_G10M14_o1_Text0:
	.string "Keep this quiet.\pIt’s rumored that this place is run\nby Team Rocket.$"
GalarObj_G10M14_o1_Mov0:
	.byte MOVEMENT_ACTION_FACE_ORIGINAL_DIRECTION
	.byte MOVEMENT_ACTION_STEP_END

GalarObj_G10M14_o2::
	lock
	faceplayer
	msgbox GalarObj_G10M14_o2_Text0, MSGBOX_DEFAULT
	goto GalarObj_G10M14_o2_b1

GalarObj_G10M14_o2_b1::
	closemessage
	applymovement VAR_LAST_TALKED, GalarObj_G10M14_o2_Mov0
	waitmovement 0
	release
	end

GalarObj_G10M14_o2_Text0:
	.string "I think these machines have\ndifferent odds.$"
GalarObj_G10M14_o2_Mov0:
	.byte MOVEMENT_ACTION_FACE_ORIGINAL_DIRECTION
	.byte MOVEMENT_ACTION_STEP_END

GalarObj_G10M14_o5::
	lock
	faceplayer
	msgbox GalarObj_G10M14_o5_Text0, MSGBOX_DEFAULT
	goto GalarObj_G10M14_o5_b1

GalarObj_G10M14_o5_b1::
	closemessage
	applymovement VAR_LAST_TALKED, GalarObj_G10M14_o5_Mov0
	waitmovement 0
	release
	end

GalarObj_G10M14_o5_Text0:
	.string "These slot games…\nWin or lose, it’s only by luck.$"
GalarObj_G10M14_o5_Mov0:
	.byte MOVEMENT_ACTION_FACE_ORIGINAL_DIRECTION
	.byte MOVEMENT_ACTION_STEP_END

GalarObj_G10M14_o6::
	lock
	faceplayer
	msgbox GalarObj_G10M14_o6_Text0, MSGBOX_DEFAULT
	goto GalarObj_G10M14_o6_b1

GalarObj_G10M14_o6_b1::
	closemessage
	applymovement VAR_LAST_TALKED, GalarObj_G10M14_o6_Mov0
	waitmovement 0
	release
	end

GalarObj_G10M14_o6_Text0:
	.string "Games are scary!\nIt’s so easy to get hooked!$"
GalarObj_G10M14_o6_Mov0:
	.byte MOVEMENT_ACTION_FACE_ORIGINAL_DIRECTION
	.byte MOVEMENT_ACTION_STEP_END

@ ---- Galar_Hammerlocke22 (g40m03) ----
GalarObj_G40M03_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M03_o0_b1
	goto GalarObj_G40M03_o0_b2

GalarObj_G40M03_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M03_o0_b3
	msgbox GalarObj_G40M03_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M03_o0_Mart0
	msgbox GalarObj_G40M03_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M03_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M03_o0_b3
	msgbox GalarObj_G40M03_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M03_o0_Mart23
	msgbox GalarObj_G40M03_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M03_o0_b3::
	release
	end

GalarObj_G40M03_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M03_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M03_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M03_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M03_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M03_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Route0803 (g20m00) ----
GalarObj_G20M00_bg0::
	lockall
	msgbox GalarObj_G20M00_bg0_Text0, MSGBOX_DEFAULT
	releaseall
	end

GalarObj_G20M00_bg0_Text0:
	.string "{COLOR RED}XX.YY.ZZZZ\n{COLOR GREEN}HH.DD\p{COLOR BLUE}Querido Diário, eu não aguento\nmais...\pNão sei há quanto tempo isso\nacontece, dias? Meses? Anos?\pMinha vida não tem paz há muito\ntempo. Passo dias e dias em claro\ltendo visoes, vivendo com medo...\pNão como há um tempo...\pNão me lembro da última vez que\nbebi água...\pE toda vez que durmo, tenho os\nmesmos pesadelos, e cada vez\lpiores, cada vez mais longos...\pNão sei mais o que fazer...\pNão sei quanto tempo vou aguentar\nou se vou superar isso...\pOh, Arceus, me ajude...$"

@ ---- Galar_StowOnSide02 (g00m10) ----
GalarObj_G00M10_o3::
	lock
	faceplayer
	msgbox GalarObj_G00M10_o3_Text0, MSGBOX_AUTOCLOSE
	warp MAP_GALAR_ROUTE10_02, 5, 6
	waitstate
	release
	end

GalarObj_G00M10_o3_Text0:
	.string "Hop: Estamos finalmente indo para\nWyndon! Tem muita coisa que eu\lquero conferir lá. Lá está aquela\lgrande torre... e o monotrilho...\lE o Estádio Wyndon, onde todo\lGalar... não, o mundo inteiro\lestará nos assistindo! Você\lentende, certo? Você e eu vamos\lfazer da nossa batalha a melhor\lque já existiu!$"

@ ---- Galar_StowOnSide03 (g09m00) ----
GalarObj_G09M00_o3::
	lock
	faceplayer
	msgbox GalarObj_G09M00_o3_Text0, MSGBOX_AUTOCLOSE
	warp MAP_GALAR_ROUTE10_02, 5, 6
	waitstate
	release
	end

GalarObj_G09M00_o3_Text0:
	.string "Estamos finalmente indo para\nWyndon!Há muita coisa que eu\lquero verificar lá.\pHá aquela grande torre ... e o\nmonotrilho... E o Estádio Wyndon,\londe Galar inteiro...não, o mundo\linteiro vai estar Nos assistindo!\pVocê entendeu, certo? Você e eu\nvamos fazer da nossa batalha a\lmelhor que já existiu!$"

@ ---- Galar_StowOnSide12 (g40m01) ----
GalarObj_G40M01_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M01_o0_b1
	goto GalarObj_G40M01_o0_b2

GalarObj_G40M01_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M01_o0_b3
	msgbox GalarObj_G40M01_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M01_o0_Mart0
	msgbox GalarObj_G40M01_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M01_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M01_o0_b3
	msgbox GalarObj_G40M01_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M01_o0_Mart23
	msgbox GalarObj_G40M01_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M01_o0_b3::
	release
	end

GalarObj_G40M01_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M01_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M01_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M01_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M01_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M01_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Ballonlea09 (g40m05) ----
GalarObj_G40M05_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M05_o0_b1
	goto GalarObj_G40M05_o0_b2

GalarObj_G40M05_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M05_o0_b3
	msgbox GalarObj_G40M05_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M05_o0_Mart0
	msgbox GalarObj_G40M05_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M05_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M05_o0_b3
	msgbox GalarObj_G40M05_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M05_o0_Mart23
	msgbox GalarObj_G40M05_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M05_o0_b3::
	release
	end

GalarObj_G40M05_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M05_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M05_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M05_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M05_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M05_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Circhester06 (g12m10) ----
GalarObj_G12M10_o18::
	lock
	faceplayer
	msgbox GalarObj_G12M10_o18_Text0, MSGBOX_AUTOCLOSE
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_5FE
	removeobject 17
	fadescreen 0
	release
	goto GalarObj_G12M10_o18_b1

GalarObj_G12M10_o18_b1::
	setvar VAR_GALAR_G12M10_OBJ, 1
	warp MAP_GALAR_HULBURY_01, 12, 27
	waitstate
	end

GalarObj_G12M10_o18_Text0:
	.string "Sonia:Sua batalha foi brilhante!\nO lider do ginásio era realmente\lforte,mas você não teve problemas\lem derrota-lo.\pCirchester tem otimos restaurantes\nTenho algumas coisas sobre que\lquero falar,então vamos a um\lrestaurante para comemorar sua\lvitoria!\lO nome do restaurante é\lBob’s Your Uncle!$"

GalarObj_G12M10_o20::
	lock
	faceplayer
	msgbox GalarObj_G12M10_o20_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G12M10_o20_Text0:
	.string "Hop: Olha {PLAYER}, esse é o\nbanho dos herois!$"

@ ---- Galar_Circhester15 (g40m06) ----
GalarObj_G40M06_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M06_o0_b1
	goto GalarObj_G40M06_o0_b2

GalarObj_G40M06_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M06_o0_b3
	msgbox GalarObj_G40M06_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M06_o0_Mart0
	msgbox GalarObj_G40M06_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M06_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M06_o0_b3
	msgbox GalarObj_G40M06_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M06_o0_Mart23
	msgbox GalarObj_G40M06_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M06_o0_b3::
	release
	end

GalarObj_G40M06_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M06_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M06_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M06_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M06_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M06_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Circhester16 (g03m08) ----
GalarObj_G03M08_o19::
	lock
	faceplayer
	msgbox GalarObj_G03M08_o19_Text0, MSGBOX_AUTOCLOSE
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_5FD
	removeobject 17
	fadescreen 0
	release
	goto GalarObj_G03M08_o19_b1

GalarObj_G03M08_o19_b1::
	setvar VAR_GALAR_G03M08_CENA, 1
	warp MAP_GALAR_HULBURY_01, 12, 27
	waitstate
	end

GalarObj_G03M08_o19_Text0:
	.string "Sonia:Sua batalha foi brilhante!\nO lider do ginásio era realmente\lforte,mas você não teve problemas\lem derrota-lo.\pCirchester tem otimos restaurantes\nTenho algumas coisas sobre que\lquero falar,então vamos a um\lrestaurante para comemorar sua\lvitoria!\lO nome do restaurante é\lBob’s Your Uncle!$"

@ ---- Galar_Spikemuth08 (g40m09) ----
GalarObj_G40M09_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M09_o0_b1
	goto GalarObj_G40M09_o0_b2

GalarObj_G40M09_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M09_o0_b3
	msgbox GalarObj_G40M09_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M09_o0_Mart0
	msgbox GalarObj_G40M09_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M09_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M09_o0_b3
	msgbox GalarObj_G40M09_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M09_o0_Mart23
	msgbox GalarObj_G40M09_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M09_o0_b3::
	release
	end

GalarObj_G40M09_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M09_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M09_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M09_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M09_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M09_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Wyndon01 (g03m09) ----
GalarObj_G03M09_o10::
	lock
	faceplayer
	msgbox GalarObj_G03M09_o10_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G03M09_o10_Text0:
	.string "Va logo {PLAYER}!!!$"

GalarObj_G03M09_o12::
	lock
	faceplayer
	msgbox GalarObj_G03M09_o12_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G03M09_o12_Text0:
	.string "Va logo {PLAYER}!!!$"

@ ---- Galar_Wyndon02 (g13m00) ----
GalarObj_G13M00_o7::
	lock
	faceplayer
	msgbox GalarObj_G13M00_o7_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G13M00_o7_Text0:
	.string "Hop: olha ,{PLAYER}, quem esta aqui!$"

@ ---- Galar_Wyndon07 (g40m11) ----
GalarObj_G40M11_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M11_o0_b1
	goto GalarObj_G40M11_o0_b2

GalarObj_G40M11_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M11_o0_b3
	msgbox GalarObj_G40M11_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M11_o0_Mart0
	msgbox GalarObj_G40M11_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M11_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M11_o0_b3
	msgbox GalarObj_G40M11_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M11_o0_Mart23
	msgbox GalarObj_G40M11_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M11_o0_b3::
	release
	end

GalarObj_G40M11_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M11_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M11_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M11_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M11_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M11_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_Wyndon08 (g13m10) ----
GalarObj_G13M10_o12::
	lock
	faceplayer
	msgbox GalarObj_G13M10_o12_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G13M10_o12_Text0:
	.string "{COLOR DARK_GRAY}Seja Bem-vindo ao {COLOR RED}Rose of the\n Rondelands.$"

@ ---- Galar_RoseTower04 (g01m94) ----
GalarObj_G01M94_o2::
	lock
	faceplayer
	msgbox GalarObj_G01M94_o2_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G01M94_o2_Text0:
	.string "Hop: Ei {PLAYER}, olha quem eu achei\naqui!$"

@ ---- Galar_IsleOfArmor02 (g01m34) ----
GalarObj_G01M34_o5::
	lock
	faceplayer
	compare VAR_GALAR_G01M34_OBJ, 1
	goto_if 4, GalarObj_G01M34_o5_b1
	msgbox GalarObj_G01M34_o5_Text0, MSGBOX_DEFAULT
	closemessage
	call GalarObj_G01M34_o5_b2
	msgbox GalarObj_G01M34_o5_Text1, MSGBOX_DEFAULT
	release
	end

GalarObj_G01M34_o5_b1::
	msgbox GalarObj_G01M34_o5_Text2, MSGBOX_DEFAULT
	release
	end

GalarObj_G01M34_o5_b2::
	fadescreen 1
	playfanfare 256
	waitfanfare
	special HealPlayerParty
	fadescreen 0
	return

GalarObj_G01M34_o5_Text0:
	.string "You look tired.\nYou should take a quick nap.$"
GalarObj_G01M34_o5_Text1:
	.string "Don’t give up!$"
GalarObj_G01M34_o5_Text2:
	.string "Thank you so much.$"

@ ---- Galar_IsleOfArmor03 (g05m14) ----
GalarObj_G05M14_o1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G05M14_o1_b1
	lock
	faceplayer
	message GalarObj_G05M14_o1_Msg0
	waitmessage
	pokemart GalarObj_G05M14_o1_Mart2
	msgbox GalarObj_G05M14_o1_Text0, MSGBOX_DEFAULT
	release
	end

GalarObj_G05M14_o1_b1::
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_AC0
	removeobject 3
	fadescreen 0
	release
	end

GalarObj_G05M14_o1_Text0:
	.string "Please come again!$"
GalarObj_G05M14_o1_Msg0:
	.string "Hi, there!\nMay I help you?$"
	.align 2
GalarObj_G05M14_o1_Mart2:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_IsleOfArmor19 (g38m15) ----
GalarObj_G38M15_bg1::
	lockall
	setvar VAR_0x8004, 2
	call GalarObj_G38M15_bg1_b1
	playse 38
	special DrawWholeMapView
	waitse
	releaseall
	end

GalarObj_G38M15_bg1_b1::
	nop
	fadescreen 0
	release
	end


@ ---- Galar_IsleOfArmor37 (g40m13) ----
GalarObj_G40M13_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M13_o0_b1
	goto GalarObj_G40M13_o0_b2

GalarObj_G40M13_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M13_o0_b3
	msgbox GalarObj_G40M13_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M13_o0_Mart0
	msgbox GalarObj_G40M13_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M13_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M13_o0_b3
	msgbox GalarObj_G40M13_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M13_o0_Mart23
	msgbox GalarObj_G40M13_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M13_o0_b3::
	release
	end

GalarObj_G40M13_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M13_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M13_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M13_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M13_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M13_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_CrownTundra08 (g37m05) ----
GalarObj_G37M05_o2::
	setflag FLAG_GALAR_ESCONDE_1800
	removeobject VAR_LAST_TALKED
	end


GalarObj_G37M05_o24::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G37M05_o24_b1
	goto GalarObj_G37M05_o24_b2

GalarObj_G37M05_o24_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G37M05_o24_b3
	msgbox GalarObj_G37M05_o24_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G37M05_o24_Mart0
	msgbox GalarObj_G37M05_o24_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G37M05_o24_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G37M05_o24_b3
	msgbox GalarObj_G37M05_o24_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G37M05_o24_Mart21
	msgbox GalarObj_G37M05_o24_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G37M05_o24_b3::
	release
	end

GalarObj_G37M05_o24_Text0:
	.string "ola, como posso ajudar voce?$"
GalarObj_G37M05_o24_Text1:
	.string "Volte sempre!$"
GalarObj_G37M05_o24_Text2:
	.string "ola, como posso ajudar voce?$"
GalarObj_G37M05_o24_Text3:
	.string "Volte sempre!$"
	.align 2
GalarObj_G37M05_o24_Mart0:
	.2byte ITEM_TM23
	.2byte ITEM_TM40
	.2byte ITEM_TM39
	.2byte ITEM_TM15
	.2byte ITEM_TM16
	.2byte ITEM_TM01
	.2byte ITEM_TM14
	.2byte ITEM_TM03
	.2byte ITEM_TM37
	.2byte ITEM_TM22
	.2byte ITEM_TM44
	.2byte ITEM_TM24
	.2byte ITEM_TM41
	.2byte ITEM_TM36
	.2byte ITEM_TM02
	.2byte ITEM_TM48
	.2byte ITEM_TM50
	.2byte ITEM_TM46
	.2byte ITEM_NONE
	.align 2
GalarObj_G37M05_o24_Mart21:
	.2byte ITEM_TM23
	.2byte ITEM_TM40
	.2byte ITEM_TM39
	.2byte ITEM_TM15
	.2byte ITEM_TM16
	.2byte ITEM_TM01
	.2byte ITEM_TM14
	.2byte ITEM_TM03
	.2byte ITEM_TM37
	.2byte ITEM_TM22
	.2byte ITEM_TM44
	.2byte ITEM_TM24
	.2byte ITEM_TM41
	.2byte ITEM_TM36
	.2byte ITEM_TM02
	.2byte ITEM_TM48
	.2byte ITEM_TM50
	.2byte ITEM_TM46
	.2byte ITEM_NONE

@ ---- Galar_CrownTundra19 (g40m14) ----
GalarObj_G40M14_o0::
	faceplayer
	lock
	checkplayergender
	compare VAR_RESULT, 0
	goto_if 1, GalarObj_G40M14_o0_b1
	goto GalarObj_G40M14_o0_b2

GalarObj_G40M14_o0_b1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M14_o0_b3
	msgbox GalarObj_G40M14_o0_Text0, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M14_o0_Mart0
	msgbox GalarObj_G40M14_o0_Text1, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M14_o0_b2::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G40M14_o0_b3
	msgbox GalarObj_G40M14_o0_Text2, MSGBOX_AUTOCLOSE
	waitmessage
	pokemart GalarObj_G40M14_o0_Mart23
	msgbox GalarObj_G40M14_o0_Text3, MSGBOX_AUTOCLOSE
	waitmessage
	release
	end

GalarObj_G40M14_o0_b3::
	release
	end

GalarObj_G40M14_o0_Text0:
	.string "{COLOR DARK_GRAY}É um prazer recebe-lo na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M14_o0_Text1:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
GalarObj_G40M14_o0_Text2:
	.string "{COLOR DARK_GRAY}É um prazer recebe-la na minha\nloja.\lGostaria de comprar alguma coisa?$"
GalarObj_G40M14_o0_Text3:
	.string "{COLOR BLUE}Não basta simplesmente satifazer\nclientes é preciso encantá-los.$"
	.align 2
GalarObj_G40M14_o0_Mart0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE
	.align 2
GalarObj_G40M14_o0_Mart23:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_POKE_DOLL
	.2byte ITEM_RED_SCARF
	.2byte ITEM_NONE

@ ---- Galar_CrownTundraIndoor01 (g00m16) ----
GalarObj_G00M16_bg0::
	lock
	faceplayer
	msgbox GalarObj_G00M16_bg0_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M16_bg0_Text0:
	.string "{PLAYER}:Nada de interessante aqui!$"

GalarObj_G00M16_bg1::
	lock
	faceplayer
	msgbox GalarObj_G00M16_bg1_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M16_bg1_Text0:
	.string "{PLAYER}: O que é isso? A HONRA\nMONTANHA DO REI: o pokémon cavalo\lque se uniu ao rei como um só e\lem uma única noite eles criaram\luma floresta, esse pokémon já foi\lselvagem, roubava as colheitas\ldas pessoas, mas o rei domou,\lsobre sua aparência alguns dizem\lque ele era branco como a neve, e\loutros dizem que ele era escuro\lcomo a noite, ninguém sabe ao\lcerto quem está certo.$"

GalarObj_G00M16_bg2::
	lock
	faceplayer
	msgbox GalarObj_G00M16_bg2_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M16_bg2_Text0:
	.string "{PLAYER}: O que é isso? GUIA DE\nSEMENTES: tem algumas sementes\lbem curiosas na coroa tundra, se\las cenouras crescerem debaixo da\lneve elas viram Cenouras da Neve\le se crescerem perto dos\lcemitérios Viram Cenouras\lNegras,pokemon Tipo gelo adoram\lCenouras da Neve e os tipo\lfantasmas adoram as Cenouras\lNegras , de acordo com as lendas\lantigas a montaria do rei adora\las duas cenouras ou uma delas ou\la outra, as historias se\lcontradizem muitos relatos de uma\lmontaria branca que gostava de\lCenouras da Neve e outras\lhistorias de uma montaria preta\lque gostava de Cenouras Negras.$"

GalarObj_G00M16_bg3::
	lock
	faceplayer
	msgbox GalarObj_G00M16_bg3_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M16_bg3_Text0:
	.string "{PLAYER}:Nada de interessante aqui!$"

@ ---- Galar_DynamaxAdventure02 (g00m17) ----
GalarObj_G00M17_o3::
	lock
	faceplayer
	compare VAR_GALAR_G00M17_OBJ, 3
	goto_if 1, GalarObj_G00M17_o3_b1
	compare VAR_GALAR_G00M17_OBJ, 2
	goto_if 1, GalarObj_G00M17_o3_b2
	msgbox GalarObj_G00M17_o3_Text0, MSGBOX_DEFAULT
	release
	end

GalarObj_G00M17_o3_b1::
	msgbox GalarObj_G00M17_o3_Text1, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M17_o3_b2::
	msgbox GalarObj_G00M17_o3_Text2, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M17_o3_Text0:
	.string "{RIVAL}: What, it’s only {PLAYER}?\nGramps isn’t around.$"
GalarObj_G00M17_o3_Text1:
	.string "Hop: Meu pokémon parece ser\nforte!$"
GalarObj_G00M17_o3_Text2:
	.string "Hop: Vamos, {PLAYER}!!!\nEscolha seu pokémon!!!$"

GalarObj_G00M17_o6::
	lock
	faceplayer
	msgbox GalarObj_G00M17_o6_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M17_o6_Text0:
	.string "Hop: {PLAYER}, aquela Wooloo sumiu.\nAcho que ela quebrou a cerca!!\pAcho…\nque devemos ir atrás dela …$"

@ ---- Galar_TrainerTower01 (g02m10) ----
GalarObj_G02M10_o1::
	special GetQuestLogState
	compare VAR_RESULT, 2
	goto_if 1, GalarObj_G02M10_o1_b1
	lock
	faceplayer
	message GalarObj_G02M10_o1_Msg0
	waitmessage
	pokemart GalarObj_G02M10_o1_Mart2
	msgbox GalarObj_G02M10_o1_Text0, MSGBOX_DEFAULT
	release
	end

GalarObj_G02M10_o1_b1::
	removeobject 4
	fadescreen 0
	release
	end

GalarObj_G02M10_o1_Text0:
	.string "Please come again!$"
GalarObj_G02M10_o1_Msg0:
	.string "Hi, there!\nMay I help you?$"
	.align 2
GalarObj_G02M10_o1_Mart2:
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_MAX_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_REVIVE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_MAX_REPEL
	.2byte ITEM_NONE

GalarObj_G02M10_o2::
	lock
	faceplayer
	setvar VAR_0x8004, 20
	special CallTrainerTowerFunc
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G02M10_o2_b1
	msgbox GalarObj_G02M10_o2_Text0, MSGBOX_DEFAULT
	goto GalarObj_G02M10_o2_b2

GalarObj_G02M10_o2_b1::
	msgbox GalarObj_G02M10_o2_Text1, MSGBOX_DEFAULT
	release
	end

GalarObj_G02M10_o2_b2::
	release
	end

GalarObj_G02M10_o2_Text0:
	.string "I hope you give it your best.$"
GalarObj_G02M10_o2_Text1:
	.string "Thank you for competing!$"

@ ---- Galar_Underwater01 (g01m63) ----
GalarObj_G01M63_o0::
	msgbox GalarObj_G01M63_o0_Text0, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G01M63_o0_b1
	call GalarObj_G01M63_o0_b2
	end

GalarObj_G01M63_o0_b1::
	warp MAP_GALAR_WILD_AREA_17, 19, 50
	waitstate
	end

GalarObj_G01M63_o0_b2::
	releaseall
	end

GalarObj_G01M63_o0_Text0:
	.string "Emergir?$"

GalarObj_G01M63_o1::
	msgbox GalarObj_G01M63_o1_Text0, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G01M63_o1_b1
	call GalarObj_G01M63_o1_b2
	end

GalarObj_G01M63_o1_b1::
	warp MAP_GALAR_WILD_AREA_20, 33, 28
	waitstate
	end

GalarObj_G01M63_o1_b2::
	releaseall
	end

GalarObj_G01M63_o1_Text0:
	.string "Emergir?$"

GalarObj_G01M63_o2::
	msgbox GalarObj_G01M63_o2_Text0, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G01M63_o2_b1
	call GalarObj_G01M63_o2_b2
	end

GalarObj_G01M63_o2_b1::
	warp MAP_GALAR_WILD_AREA_09, 37, 28
	waitstate
	end

GalarObj_G01M63_o2_b2::
	releaseall
	end

GalarObj_G01M63_o2_Text0:
	.string "Emergir?$"

GalarObj_G01M63_o3::
	msgbox GalarObj_G01M63_o3_Text0, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G01M63_o3_b1
	call GalarObj_G01M63_o3_b2
	end

GalarObj_G01M63_o3_b1::
	warp MAP_GALAR_MOTOSTOKE_05, 28, 23
	waitstate
	end

GalarObj_G01M63_o3_b2::
	releaseall
	end

GalarObj_G01M63_o3_Text0:
	.string "Emergir?$"

GalarObj_G01M63_o4::
	msgbox GalarObj_G01M63_o4_Text0, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G01M63_o4_b1
	call GalarObj_G01M63_o4_b2
	end

GalarObj_G01M63_o4_b1::
	warp MAP_GALAR_WILD_AREA_03, 21, 38
	waitstate
	end

GalarObj_G01M63_o4_b2::
	releaseall
	end

GalarObj_G01M63_o4_Text0:
	.string "Emergir?$"

GalarObj_G01M63_o5::
	msgbox GalarObj_G01M63_o5_Text0, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G01M63_o5_b1
	call GalarObj_G01M63_o5_b2
	end

GalarObj_G01M63_o5_b1::
	warp MAP_GALAR_ROUTE02_02, 29, 26
	waitstate
	end

GalarObj_G01M63_o5_b2::
	releaseall
	end

GalarObj_G01M63_o5_Text0:
	.string "Emergir?$"

GalarObj_G01M63_o6::
	msgbox GalarObj_G01M63_o6_Text0, MSGBOX_YESNO
	compare VAR_RESULT, 1
	goto_if 1, GalarObj_G01M63_o6_b1
	call GalarObj_G01M63_o6_b2
	end

GalarObj_G01M63_o6_b1::
	warp MAP_GALAR_ROUTE09_01, 38, 54
	waitstate
	end

GalarObj_G01M63_o6_b2::
	releaseall
	end

GalarObj_G01M63_o6_Text0:
	.string "Emergir?$"

