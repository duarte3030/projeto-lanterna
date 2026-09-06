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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M12_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M12_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M12_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Hop: My Pokémon looks strong!$"
GalarObj_G04M03_o4_Text2:
	.string "Hop: Come on, {PLAYER}!!!\n"
	.string "Pick your Pokémon!!!$"

@ ---- Galar_SlumberingWeald03 (g04m11) ----
GalarObj_G04M11_o6::
	lock
	faceplayer
	msgbox GalarObj_G04M11_o6_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G04M11_o6_Text0:
	.string "Hop: Take a look at this, {PLAYER}! This\n"
	.string "is something you don't see every day ...\p"
	.string "This place definitely looks like it came\n"
	.string "straight out of a legend.$"

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
	.string "Hello, how can I help you?$"
GalarObj_G05M11_o1_Text1:
	.string "Thank you.$"
GalarObj_G05M11_o1_Text2:
	.string "Hello, how can I help you?$"
GalarObj_G05M11_o1_Text3:
	.string "Thank you.$"
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
	.string "Let me take you to the opening\n"
	.string "ceremony!$"

GalarObj_G06M13_o1::
	lock
	faceplayer
	msgbox GalarObj_G06M13_o1_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M13_o1_Text0:
	.string "Hop: Come on, {PLAYER}! The ceremony is\n"
	.string "starting now!$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M07_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M07_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M07_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M08_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M08_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M08_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Nothing but books. $"
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
	.string "A spot where you can dive, but you need\n"
	.string "equipment.$"
GalarObj_G06M10_o15_Text1:
	.string "Dive?$"

@ ---- Galar_Motostoke06 (g06m12) ----
GalarObj_G06M12_o0::
	lock
	faceplayer
	msgbox GalarObj_G06M12_o0_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G06M12_o0_Text0:
	.string "You had better go and register,\n"
	.string " {PLAYER}$"

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
	.string "hello, challenger. In this Gym there are\n"
	.string "several Marowak straight from Alola.\l"
	.string "They\p"
	.string "have a card. Catch one, take its card\n"
	.string "and you'll be able to pass.$"
GalarObj_G06M33_o0_Text1:
	.string "hello, challenger. In this Gym there are\n"
	.string "several Marowak straight from Alola.\l"
	.string "They\p"
	.string "have a card. Catch one, take its card\n"
	.string "and you'll be able to pass.$"
GalarObj_G06M33_o0_Text2:
	.string "congratulations, you got the card. You\n"
	.string "may pass now!$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M02_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M02_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M02_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Are you {PLAYER}, by any chance? I heard\n"
	.string "you were endorsed by the Champion.$"

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
	.string "A spot where you can dive, but you need\n"
	.string "equipment.$"
GalarObj_G06M27_o20_Text1:
	.string "Dive?$"

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
	.string "A spot where you can dive, but you need\n"
	.string "equipment.$"
GalarObj_G08M24_o9_Text1:
	.string "Dive?$"

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
	.string "A spot where you can dive, but you need\n"
	.string "equipment.$"
GalarObj_G42M10_o23_Text1:
	.string "Dive?$"

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
	.string "A spot where you can dive, but you need\n"
	.string "equipment.$"
GalarObj_G42M13_o9_Text1:
	.string "Dive?$"

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
	.string "A spot where you can dive, but you need\n"
	.string "equipment.$"
GalarObj_G08M11_o1_Text1:
	.string "Dive?$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M15_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M15_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M15_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Hi {PLAYER}, you came too?!\p"
	.string "How about we battle after we eat?$"

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
	.string "{COLOR DARK_GRAY}Excuse me, Chairman Rose is in this\n"
	.string "restaurant.\p"
	.string "I'm trying to put together a story\n"
	.string "about it.$"

GalarObj_G08M07_o13::
	lock
	faceplayer
	msgbox GalarObj_G08M07_o13_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o13_Text0:
	.string "{COLOR DARK_GRAY}It's always good to walk around with\n"
	.string "your Pokémon.\p"
	.string "Every {COLOR RED}128 steps{COLOR DARK_GRAY}, they get happier\n"
	.string "and happier.$"

GalarObj_G08M07_o14::
	lock
	faceplayer
	msgbox GalarObj_G08M07_o14_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o14_Text0:
	.string "{COLOR LIGHT_RED}Do you really use your Pokémon in\n"
	.string "battle?\p"
	.string "I'd never do that to my Zigzagoon, he's\n"
	.string "a baby.$"

GalarObj_G08M07_o18::
	lock
	faceplayer
	msgbox GalarObj_G08M07_o18_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o18_Text0:
	.string "{COLOR DARK_GRAY}I swear by the light that guides me\n"
	.string "that I saw an {COLOR BLUE}Eevee{COLOR DARK_GRAY} swimming toward\l"
	.string "the horizon.\p"
	.string "Bolt tried to jump in after it, but I\n"
	.string "held him back.$"

GalarObj_G08M07_o3::
	msgbox GalarObj_G08M07_o3_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G08M07_o3_Text0:
	.string "{COLOR DARK_GRAY}Looks like the sea isn't giving up any\n"
	.string "fish today...$"

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
	.string "{COLOR BLUE}Welcome to my shop, what can I help\n"
	.string "you with?$"
GalarObj_G08M07_o31_Text1:
	.string "{COLOR BLUE}Come again!$"
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
	.string "{COLOR BLUE}Welcome to my shop, what can I help\n"
	.string "you with?$"
GalarObj_G08M07_o32_Text1:
	.string "{COLOR BLUE}Come again!$"
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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M00_o1_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M00_o1_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M00_o1_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M10_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M10_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M10_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Don't interrupt our fight!$"

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
	.string "Don't interrupt our fight!$"

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
	.string "Rose: Hammerlocke Stadium works as a\n"
	.string "power plant.\p"
	.string "Now, take a look at my tablet.$"
GalarObj_G09M11_o1_Text1:
	.string "I have all the information\p"
	.string "you need to see.\p"
	.string "Rose: See? An easy to understand\n"
	.string "description of the power plant! First,\p"
	.string "the energy is absorbed in the tower of\n"
	.string "Hammerlocke Stadium. Next,\p"
	.string "it is turned into electricity in the\n"
	.string "underground Power Plant and delivered\l"
	.string "to\p"
	.string "the people of the whole Galar region!\n"
	.string "Our lives and our society demand\p"
	.string "many kinds of energy sources, such as\n"
	.string "electricity and natural gas. My\p"
	.string "associated groups aim to improve\n"
	.string "everyone's lives by harnessing the$"
GalarObj_G09M11_o1_Mov0:
	.byte MOVEMENT_ACTION_FACE_RIGHT
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarObj_G09M11_o1_Mov1:
	.byte MOVEMENT_ACTION_EMOTE_EXCLAMATION_MARK
	.byte MOVEMENT_ACTION_STEP_END
GalarObj_G09M11_o1_Text2:
	.string "Rose: time for me to get to work.\n"
	.string "I should get moving before\p"
	.string "Oleana decides to give me more\n"
	.string "reminders. {PLAYER}, I suggest you head\l"
	.string "to the\p"
	.string "Vault next. Just go toward Route 6 from\n"
	.string "the stadium and you'll\p"
	.string "find the Vault with no trouble!$"

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
	.string "G-Gym Challenger! You have to help me!\n"
	.string "I-I mean, please, help me!\p"
	.string "My Pokémon suddenly Dynamaxed for\n"
	.string "some reason and started running wild in\l"
	.string "the stadium ... Raihan ... I mean, Mr.\l"
	.string "Raihan was able to subdue the Dynamax\l"
	.string "Pokémon in the stadium, but...\p"
	.string "If another Pokémon Dynamaxes and goes\n"
	.string "on a rampage ... the underground Power\l"
	.string "Plant would collapse!\p"
	.string "Mr. Rose is down there right now!\p"
	.string "I know this is selfish of me, but I must\n"
	.string "beg for your help!\p"
	.string "I want you to go into the underground\n"
	.string "Power Plant and stop Mr. Rose!\p"
	.string "Mr. Rose has awakened a Pokémon known\n"
	.string "as Eternatus ...\p"
	.string "Apparently, the energy given off by its\n"
	.string "body is what causes Dynamaxing.\p"
	.string "At this rate, every Pokémon in the Galar\n"
	.string "region will Dynamax and go wild! If that\l"
	.string "were to happen...\p"
	.string "Please, you have to save Mr. Rose!\p"
	.string "You can take the elevator down there\n"
	.string "to reach him.\p"
	.string "I asked the Champion's little brother\n"
	.string "for help too, but who knows what is\l"
	.string "going on ...Oh no ... Eternatus is- Oh, Mr.\l"
	.string "Rose ...$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M03_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M03_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M03_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "{COLOR RED}XX.YY.ZZZZ\n"
	.string "{COLOR GREEN}HH.DD\p"
	.string "{COLOR BLUE}Dear Diary, I can't take it anymore...\p"
	.string "I don't know how long this has been\n"
	.string "going on, days? Months? Years?\p"
	.string "My life has had no peace for a long time.\n"
	.string "I spend days on end awake, having\l"
	.string "visions, living in fear...\p"
	.string "I haven't eaten in a while...\p"
	.string "I can't remember the last time I drank\n"
	.string "water...\p"
	.string "And every time I sleep, I have the same\n"
	.string "nightmares, worse each time, longer\l"
	.string "each time...\p"
	.string "I don't know what to do anymore...\p"
	.string "I don't know how long I can hold out, or\n"
	.string "whether I'll get through this...\p"
	.string "Oh, Arceus, help me...$"

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
	.string "Hop: We're finally heading to Wyndon!\n"
	.string "There's so much I want to check out\l"
	.string "there. There's that huge tower... and\l"
	.string "the monorail... And Wyndon Stadium,\l"
	.string "where all of Galar... no, the whole world\l"
	.string "will be watching us! You get it, right?\l"
	.string "You and I are going to make our battle\l"
	.string "the best there has ever been!$"

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
	.string "We're finally heading to Wyndon! There's\n"
	.string "so much I want to check out there.\p"
	.string "There's that huge tower... and the\n"
	.string "monorail... And Wyndon Stadium, where all\l"
	.string "of Galar... no, the whole world will be\l"
	.string "watching us!\p"
	.string "You get it, right? You and I are going to\n"
	.string "make our battle the best there has ever\l"
	.string "been!$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M01_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M01_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M01_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M05_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M05_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M05_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Sonia: Your battle was brilliant! The\n"
	.string "Gym Leader was really strong, but you\l"
	.string "had no trouble beating him.\p"
	.string "Circhester has great restaurants.\n"
	.string "There are a few things I want to talk\l"
	.string "about, so let's go to a restaurant to\l"
	.string "celebrate your victory! The restaurant\l"
	.string "is called Bob’s Your Uncle!$"

GalarObj_G12M10_o20::
	lock
	faceplayer
	msgbox GalarObj_G12M10_o20_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G12M10_o20_Text0:
	.string "Hop: Look, {PLAYER}, this is the bath of\n"
	.string "heroes!$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M06_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M06_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M06_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Sonia: Your battle was brilliant! The\n"
	.string "Gym Leader was really strong, but you\l"
	.string "had no trouble beating him.\p"
	.string "Circhester has great restaurants.\n"
	.string "There are a few things I want to talk\l"
	.string "about, so let's go to a restaurant to\l"
	.string "celebrate your victory! The restaurant\l"
	.string "is called Bob’s Your Uncle!$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M09_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M09_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M09_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Get going, {PLAYER}!!!$"

GalarObj_G03M09_o12::
	lock
	faceplayer
	msgbox GalarObj_G03M09_o12_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G03M09_o12_Text0:
	.string "Get going, {PLAYER}!!!$"

@ ---- Galar_Wyndon02 (g13m00) ----
GalarObj_G13M00_o7::
	lock
	faceplayer
	msgbox GalarObj_G13M00_o7_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G13M00_o7_Text0:
	.string "Hop: Look, {PLAYER}, who's here!$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M11_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M11_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M11_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "Hop: Hey {PLAYER}, look who I found here!$"

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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M13_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M13_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M13_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "hello, how can I help you?$"
GalarObj_G37M05_o24_Text1:
	.string "Come again!$"
GalarObj_G37M05_o24_Text2:
	.string "hello, how can I help you?$"
GalarObj_G37M05_o24_Text3:
	.string "Come again!$"
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
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M14_o0_Text1:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
GalarObj_G40M14_o0_Text2:
	.string "{COLOR DARK_GRAY}It's a pleasure to have you in my shop.\n"
	.string "Would you like to buy something?$"
GalarObj_G40M14_o0_Text3:
	.string "{COLOR BLUE}It isn't enough to simply satisfy\n"
	.string "customers, you have to delight them.$"
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
	.string "{PLAYER}: Nothing interesting here!$"

GalarObj_G00M16_bg1::
	lock
	faceplayer
	msgbox GalarObj_G00M16_bg1_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M16_bg1_Text0:
	.string "{PLAYER}: What is this? THE HONOR, THE\n"
	.string "KING'S STEED: the horse Pokémon that\l"
	.string "became one with the king, and in a\l"
	.string "single night they created a forest.\l"
	.string "This Pokémon was once wild and stole\l"
	.string "people's harvests, but the king tamed\l"
	.string "it. As for its appearance, some say it\l"
	.string "was white as snow, and others say it was\l"
	.string "dark as night; nobody knows for sure\l"
	.string "who is right.$"

GalarObj_G00M16_bg2::
	lock
	faceplayer
	msgbox GalarObj_G00M16_bg2_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M16_bg2_Text0:
	.string "{PLAYER}: What is this? SEED GUIDE:\n"
	.string "there are some very curious seeds in\l"
	.string "the Crown Tundra. If the carrots grow\l"
	.string "under the snow they become Iceroot\l"
	.string "Carrots, and if they grow near the\l"
	.string "cemeteries they become Shaderoot\l"
	.string "Carrots. Ice-type Pokémon love Iceroot\l"
	.string "Carrots and Ghost-types love\l"
	.string "Shaderoot Carrots. According to the old\l"
	.string "legends the king's steed loves both\l"
	.string "carrots, or one of them, or the other;\l"
	.string "the stories contradict each other.\l"
	.string "There are many accounts of a white\l"
	.string "steed that liked Iceroot Carrots and\l"
	.string "other stories of a black steed that\l"
	.string "liked Shaderoot Carrots.$"

GalarObj_G00M16_bg3::
	lock
	faceplayer
	msgbox GalarObj_G00M16_bg3_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M16_bg3_Text0:
	.string "{PLAYER}: Nothing interesting here!$"

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
	.string "Hop: My Pokémon looks strong!$"
GalarObj_G00M17_o3_Text2:
	.string "Hop: Come on, {PLAYER}!!!\n"
	.string "Pick your Pokémon!!!$"

GalarObj_G00M17_o6::
	lock
	faceplayer
	msgbox GalarObj_G00M17_o6_Text0, MSGBOX_AUTOCLOSE
	release
	end

GalarObj_G00M17_o6_Text0:
	.string "Hop: {PLAYER}, that Wooloo is gone. I\n"
	.string "think it broke through the fence!!\p"
	.string "I think…\n"
	.string "we should go after it …$"

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
	.string "Surface?$"

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
	.string "Surface?$"

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
	.string "Surface?$"

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
	.string "Surface?$"

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
	.string "Surface?$"

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
	.string "Surface?$"

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
	.string "Surface?$"

