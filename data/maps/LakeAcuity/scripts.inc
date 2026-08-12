LakeAcuity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, LakeAcuity_OnTransition
	.byte 0

LakeAcuity_EventScript_Hiker::
	msgbox LakeAcuity_Text_Hiker, MSGBOX_NPC
	end

LakeAcuity_EventScript_SwimmerF::
	msgbox LakeAcuity_Text_SwimmerF, MSGBOX_NPC
	end

LakeAcuity_Text_Hiker:
	.string "This snow never seems to melt,\n"
	.string "even when spring comes to Sinnoh.$"

LakeAcuity_Text_SwimmerF:
	.string "Brrr! Too cold to swim here,\n"
	.string "but the view is worth the walk.$"

@ ponytail: gatilho DUPLO de proposito, e nao por indecisao. O coord_event de
@ (23,31) da o disparo automatico do original (VAR_TEMP_0 com valor 0: o motor
@ zera os VAR_TEMP_* a cada entrada de mapa, entao ele esta sempre valendo e
@ quem lembra que a cena ja rodou e a FLAG la dentro, tecnica 1 do
@ SINNOH-PADRAO.md). Falar com qualquer um dos dois roda a MESMA cena, e e essa
@ segunda porta que garante que ninguem fica preso: a Jupiter esta em cima do
@ unico tile de acesso a caverna, e jogador que chegue por um caminho que nao
@ pise em (23,31) ainda assim consegue destravar conversando.
@
@ Cortado do original: a camera livre (AddFreeCamera) e os dois ramos de x=14 e
@ x=15, que existem so porque la o coord_event cobre dois tiles. O que a cena
@ diz e faz e o mesmo.
LakeAcuity_EventScript_Jupiter::
	lockall
	goto_if_set FLAG_GALACTICA_ACUITY_VISTO, LakeAcuity_EventScript_CenaAcabou
	@ PORTAO DO MARCO, 12/08/2026. Sem ele a cena rodava NO VAZIO: o ON_TRANSITION
	@ so faz a Jupiter e o rival nascerem com a Mars do Lago Verity derrotada, mas
	@ este script nao olhava o marco, so a flag de "ja vi". Quem chegasse na boca da
	@ caverna antes da hora via as seis caixas de texto com ninguem na tela, e ainda
	@ QUEIMAVA FLAG_GALACTICA_ACUITY_VISTO, o que trancava a cena de verdade para
	@ sempre. Nao aparecia porque o warp 0 largava o jogador dentro do lago e ele
	@ nunca chegava aqui; e o que o T94.6 foi escrito para provar.
	goto_if_not_defeated TRAINER_SINNOH_COMMANDER_MARS_LAKE_VERITY, LakeAcuity_EventScript_CenaAcabou
	applymovement LOCALID_LAKE_ACUITY_RIVAL, LakeAcuity_Movement_RivalOlhaJupiter
	waitmovement 0
	msgbox LakeAcuity_Text_CenaNotGettingAway, MSGBOX_DEFAULT
	msgbox LakeAcuity_Text_CenaBackToVeilstone, MSGBOX_DEFAULT
	msgbox LakeAcuity_Text_CenaDontWaste, MSGBOX_DEFAULT
	closemessage
	removeobject LOCALID_LAKE_ACUITY_JUPITER
	applymovement LOCALID_LAKE_ACUITY_RIVAL, LakeAcuity_Movement_RivalOlhaJogador
	waitmovement 0
	msgbox LakeAcuity_Text_CenaCouldntDo, MSGBOX_DEFAULT
	msgbox LakeAcuity_Text_CenaUxieSuffering, MSGBOX_DEFAULT
	msgbox LakeAcuity_Text_CenaBeStronger, MSGBOX_DEFAULT
	closemessage
	removeobject LOCALID_LAKE_ACUITY_RIVAL
	setflag FLAG_GALACTICA_ACUITY_VISTO
	setflag FLAG_ESCONDE_LAGO_ACUITY
	releaseall
	end

LakeAcuity_EventScript_CenaAcabou::
	releaseall
	end

LakeAcuity_Movement_RivalOlhaJupiter:
	face_left
	step_end

LakeAcuity_Movement_RivalOlhaJogador:
	face_down
	step_end

LakeAcuity_Text_CenaBackToVeilstone:
	.string "Jupiter: Oh?\nAre you finished already?\pYour Pokémon aren't bad, but you're\nlaughably weak.\pYou honestly thought you could save\nthe Pokémon of the lake?\pAnd become the Pokémon Champion?\nDream on, little kid.\pBut, eww, it's so cold here.\nLet's go back to the Veilstone HQ.$"

LakeAcuity_Text_CenaBeStronger:
	.string "I'm going to get tougher...\pIt's not about winning or losing...\nThat's not good enough...\pI have to be stronger...\pIt's not enough to just want to be the\nmost powerful Trainer ever...\pIt takes honest effort...\nAnd a determined heart.$"

LakeAcuity_Text_CenaCouldntDo:
	.string "CEDRIC: ...\n...\pYeah, that's right!\pI couldn't do anything against Team\nGalactic!$"

LakeAcuity_Text_CenaDontWaste:
	.string "Oh? Don't I know you?\nWe met in Eterna City.\pListen. Team Galactic is going to do\nsomething huge for everyone's sake.\pThat's why you should keep out of\nTeam Galactic's way.\pDon't come whining about poor Pokémon\nand other trivial junk like that.\pDon't waste your time coming to our\nHQ in Veilstone.\pNow, if you'll excuse me.$"

LakeAcuity_Text_CenaNotGettingAway:
	.string "CEDRIC: !\pYou're not getting away with this,\nTeam Galactic!$"

LakeAcuity_Text_CenaUxieSuffering:
	.string "That Pokémon called UXIE...\nIt was suffering...$"

@ ponytail: as duas pontas da janela desta cena, num ON_TRANSITION so, que roda
@ ANTES de InitMap() e por isso ja vale para este carregamento. A ordem importa:
@ acende PRIMEIRO (par nao existe), e so o ramo bom apaga. Enquanto a Mars nao
@ cai, e depois que a cena roda, os dois nao nascem; a janela em que eles existem
@ e exatamente a da cena, e a propria cena a fecha.
LakeAcuity_OnTransition:
	setflag FLAG_ESCONDE_LAGO_ACUITY
	goto_if_set FLAG_GALACTICA_ACUITY_VISTO, LakeAcuity_EventScript_CenaJaRodou
	call_if_defeated TRAINER_SINNOH_COMMANDER_MARS_LAKE_VERITY, LakeAcuity_EventScript_MostraJupiter
	end

LakeAcuity_EventScript_MostraJupiter::
	clearflag FLAG_ESCONDE_LAGO_ACUITY
	return

LakeAcuity_EventScript_CenaJaRodou::
	end
