@ Cenas de OBJETO de Galar (bloco c4a da fase de conteudo).
@ Gerado por dev_scripts/objetos_galar.py; NAO editar a mao.
@ Rotulo GalarObj_* tem PRECEDENCIA sobre GalarFala_*: onde a cena
@ inteira foi portada, ela ja contem a fala que o balde (a) deu.
@ Ordem: a da rota da historia, de Postwick e Wedgehurst em diante.

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

@ ---- Galar_Hammerlocke04 (g09m10) ----
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
	.string "Näo atrapalhe nossa luta!$"

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
	.string "Näo atrapalhe nossa luta!$"

@ ---- Galar_Hammerlocke05 (g09m11) ----
GalarObj_G09M11_o4::
	lock
	faceplayer
	msgbox GalarObj_G09M11_o4_Text0, MSGBOX_AUTOCLOSE
	release
	fadescreen 1
	removeobject 4
	removeobject 5
	fadescreen 0
	end

GalarObj_G09M11_o4_Text0:
	.string "G-Gym Challenger! Você deve me\najudar! E-eu quero dizer,\lpor favor, me ajude!\pMeu Pokémon de repente Dynamaxed\npor algum motivo e começou a\lcorrer enlouquecido no estádio ...\lRaihan ... quero dizer, o Sr.\lRaihan foi capaz de subjugar o\lPokémon Dynamax no estádio,mas...\pSe outro Pokémon também Dynamax e\nentrar em f ria ...\la usina subterr nea entraria em\lcolapso!\pMr. Rose está lá embaixo agora!\pEu sei que isso é egoismo da\nminha parte, mas devo implorar\lsua ajuda!\pQuero que você entre na usina\nsubterr nea e pare o Sr.Rose!\pMr. Rose despertou um Pokémon\nconhecido como Eternatus ...\pAparentemente,a energia emitida\npor seu corpo é o que causa o\lDynamaxing.\pNesse ritmo, todos os Pokémon na\nregiäo de Galar iräo Dynamax e\lenlouquecer!\lSe isso acontecesse...\pPor favor, você deve salvar o\nSr.Rose!\pVocê pode pegar o elevador\naté lá para alcançá-lo.\pEu pedi a ajuda do irmäo mais novo\ndo Campeäo também, mas quem sabe o\lque está acontecendo ...Oh näo\l... Eternatus é- Oh, Sr.Rose ...$"

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

