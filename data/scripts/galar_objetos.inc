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
	checkflag FLAG_GALAR_ESCONDE_20B
	msgbox GalarObj_G06M33_o0_Text2, MSGBOX_AUTOCLOSE
	release
	removeobject 2
	fadescreen 0
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


@ ---- Galar_Turffield03 (g07m11) ----
GalarObj_G07M11_o0::
	removeobject VAR_LAST_TALKED
	end


GalarObj_G07M11_o1::
	removeobject VAR_LAST_TALKED
	end


@ ---- Galar_Hulbury03 (g08m02) ----
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


@ ---- Galar_Hammerlocke04 (g09m10) ----
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
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_BA7
	removeobject 4
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_BA8
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

@ ---- Galar_CrownTundra08 (g37m05) ----
GalarObj_G37M05_o2::
	setflag FLAG_GALAR_ESCONDE_1800
	removeobject VAR_LAST_TALKED
	end


