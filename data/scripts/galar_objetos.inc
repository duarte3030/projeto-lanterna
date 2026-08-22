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

@ ---- Galar_Wedgehurst09 (g06m13) ----
GalarObj_G06M13_o0::
	lock
	faceplayer
	msgbox GalarObj_G06M13_o0_Text0, MSGBOX_AUTOCLOSE
	release
	warp MAP_GALAR_MOTOSTOKE_07, 7, 4
	waitstate
	end

GalarObj_G06M13_o0_Text0:
	.string "Deixe-me levá-los à\ncerimônia de abertura!$"

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

@ ---- Galar_StowOnSide02 (g00m10) ----
GalarObj_G00M10_o3::
	lock
	faceplayer
	msgbox GalarObj_G00M10_o3_Text0, MSGBOX_AUTOCLOSE
	release
	warp MAP_GALAR_ROUTE10_02, 5, 6
	waitstate
	end

GalarObj_G00M10_o3_Text0:
	.string "Hop: Estamos finalmente indo para\nWyndon! Tem muita coisa que eu\lquero conferir lá. Lá está aquela\lgrande torre... e o monotrilho...\lE o Estádio Wyndon, onde todo\lGalar... näo, o mundo inteiro\lestará nos assistindo! Você\lentende, certo? Você e eu vamos\lfazer da nossa batalha a melhor\lque já existiu!$"

@ ---- Galar_StowOnSide03 (g09m00) ----
GalarObj_G09M00_o3::
	lock
	faceplayer
	msgbox GalarObj_G09M00_o3_Text0, MSGBOX_AUTOCLOSE
	release
	warp MAP_GALAR_ROUTE10_02, 5, 6
	waitstate
	end

GalarObj_G09M00_o3_Text0:
	.string "Estamos finalmente indo para\nWyndon!Há muita coisa que eu\lquero verificar lá.\pHá aquela grande torre ... e o\nmonotrilho... E o Estádio Wyndon,\londe Galar inteiro...näo, o mundo\linteiro vai estar Nos assistindo!\pVocê entendeu, certo? Você e eu\nvamos fazer da nossa batalha a\lmelhor que já existiu!$"

@ ---- Galar_Circhester06 (g12m10) ----
GalarObj_G12M10_o18::
	lock
	faceplayer
	msgbox GalarObj_G12M10_o18_Text0, MSGBOX_AUTOCLOSE
	release
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_5FE
	removeobject 17
	fadescreen 0
	releaseall
	goto GalarObj_G12M10_o18_b1

GalarObj_G12M10_o18_b1::
	setvar VAR_GALAR_G12M10_OBJ, 1
	warp MAP_GALAR_HULBURY_01, 12, 27
	waitstate
	end

GalarObj_G12M10_o18_Text0:
	.string "Sonia:Sua batalha foi brilhante!\nO lider do ginásio era realmente\lforte,mas você näo teve problemas\lem derrota-lo.\pCirchester tem otimos restaurantes\nTenho algumas coisas sobre que\lquero falar,entäo vamos a um\lrestaurante para comemorar sua\lvitoria!\lO nome do restaurante é\lBob’s Your Uncle!$"

@ ---- Galar_Circhester16 (g03m08) ----
GalarObj_G03M08_o19::
	lock
	faceplayer
	msgbox GalarObj_G03M08_o19_Text0, MSGBOX_AUTOCLOSE
	release
	@ DECISAO cenas_galar.py: removeobject so vale a sessao de mapa; a flag e a que a FONTE pendurou neste objeto, o que se acrescenta e o momento de acende-la
	setflag FLAG_GALAR_ESCONDE_5FD
	removeobject 17
	fadescreen 0
	releaseall
	goto GalarObj_G03M08_o19_b1

GalarObj_G03M08_o19_b1::
	setvar VAR_GALAR_G03M08_CENA, 1
	warp MAP_GALAR_HULBURY_01, 12, 27
	waitstate
	end

GalarObj_G03M08_o19_Text0:
	.string "Sonia:Sua batalha foi brilhante!\nO lider do ginásio era realmente\lforte,mas você näo teve problemas\lem derrota-lo.\pCirchester tem otimos restaurantes\nTenho algumas coisas sobre que\lquero falar,entäo vamos a um\lrestaurante para comemorar sua\lvitoria!\lO nome do restaurante é\lBob’s Your Uncle!$"

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


@ ---- Galar_CrownTundra08 (g37m05) ----
GalarObj_G37M05_o2::
	setflag FLAG_GALAR_ESCONDE_1800
	removeobject VAR_LAST_TALKED
	end


@ ---- Galar_TrainerTower01 (g02m10) ----
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

