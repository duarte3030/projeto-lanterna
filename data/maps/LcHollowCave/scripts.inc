@ LcHollowCave: mapa copiado de Pokémon Liquid Crystal.gba (g2m102) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.
@
@ A caverna nao tem conexao de mapa com Johto, de proposito: o primario dela e o
@ gTileset_LcOutdoor e o de Johto e o gTileset_JohtoGeneral, e travessia por
@ conexao so recarrega o tileset SECUNDARIO (secao 3.1 do METODO-COPIA-CIDADES.md).
@ As duas entradas sao warp de EVENTO nas duas bocas que
@ dev_scripts/abre_bocas_hollow_cave.py abriu na encosta da Route 45.
@
@ Este andar tem DOIS bolsoes que nao se ligam a pe: o do norte, de 428 celulas,
@ que a boca de (30,30) da rota alcanca, e o do sul, de 71, que a boca de (5,84)
@ alcanca. Os dois se ligam pelo andar de baixo.

LcHollowCave_MapScripts::
	.byte 0

@ ---------------------------------------------------------------- treinadores

LcHollowCave_EventScript_HikerNorthHall::
	trainerbattle_single TRAINER_JOHTO_LC_HOLLOW_NORTH, LcHollowCave_Text_HikerSeen, LcHollowCave_Text_HikerBeaten
	msgbox LcHollowCave_Text_HikerAfter, MSGBOX_AUTOCLOSE
	end

LcHollowCave_EventScript_BeltMidHall::
	trainerbattle_single TRAINER_JOHTO_LC_HOLLOW_MIDDLE, LcHollowCave_Text_BeltSeen, LcHollowCave_Text_BeltBeaten
	msgbox LcHollowCave_Text_BeltAfter, MSGBOX_AUTOCLOSE
	end

LcHollowCave_EventScript_CamperLowHall::
	trainerbattle_single TRAINER_JOHTO_LC_HOLLOW_DEEP, LcHollowCave_Text_CamperSeen, LcHollowCave_Text_CamperBeaten
	msgbox LcHollowCave_Text_CamperAfter, MSGBOX_AUTOCLOSE
	end

LcHollowCave_EventScript_PicnickerSouthHall::
	trainerbattle_single TRAINER_JOHTO_LC_HOLLOW_SOUTH, LcHollowCave_Text_PicnickerSeen, LcHollowCave_Text_PicnickerBeaten
	msgbox LcHollowCave_Text_PicnickerAfter, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- gente e placas

@ O escavador fica EM CIMA do degrau de (11,22). A planta do hack tem treze
@ tiles de escada e de seta nos tres mapas, numero impar, entao um deles fica
@ sem par; em vez de inventar um destino para ele, o degrau ficou soterrado e a
@ fala do escavador diz isso.
LcHollowCave_EventScript_Digger::
	msgbox LcHollowCave_Text_Digger, MSGBOX_NPC
	end

LcHollowCave_EventScript_SignNorthMouth::
	msgbox LcHollowCave_Text_SignNorthMouth, MSGBOX_SIGN
	end

LcHollowCave_EventScript_SignSouthMouth::
	msgbox LcHollowCave_Text_SignSouthMouth, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- textos

LcHollowCave_Text_HikerSeen:
	.string "You came in by the upper mouth?\n"
	.string "Then you can handle a battle!$"

LcHollowCave_Text_HikerBeaten:
	.string "Strong. Stronger than the rock.$"

LcHollowCave_Text_HikerAfter:
	.string "Two mouths, one hill. The lower\n"
	.string "one comes out near ROUTE 46.\p"
	.string "You can't walk between them up\n"
	.string "here. You go down first.$"

LcHollowCave_Text_BeltSeen:
	.string "No lantern, no map, no fear.\n"
	.string "Show me the same!$"

LcHollowCave_Text_BeltBeaten:
	.string "The dark took my nerve, not you.$"

LcHollowCave_Text_BeltAfter:
	.string "I count the turns instead of\n"
	.string "marking the walls.\p"
	.string "Fourteen to the lower stair,\n"
	.string "if you start from the mouth.$"

LcHollowCave_Text_CamperSeen:
	.string "Hey! You're the first face I've\n"
	.string "seen down here all week!$"

LcHollowCave_Text_CamperBeaten:
	.string "And the last one I beat, clearly.$"

LcHollowCave_Text_CamperAfter:
	.string "The floor is sand, all the way\n"
	.string "through.\p"
	.string "Water carried it in here long\n"
	.string "before the hill was a hill.$"

LcHollowCave_Text_PicnickerSeen:
	.string "You came UP from the lower\n"
	.string "stair? Then battle me!$"

LcHollowCave_Text_PicnickerBeaten:
	.string "I should have gone back outside.$"

LcHollowCave_Text_PicnickerAfter:
	.string "This end of the cave only joins\n"
	.string "the rest one floor down.\p"
	.string "Whoever dug it gave up halfway,\n"
	.string "I think.$"

LcHollowCave_Text_Digger:
	.string "This step used to go somewhere.\p"
	.string "The roof came down on it two\n"
	.string "winters ago and I've been moving\l"
	.string "the sand ever since.\p"
	.string "Ask me again in ten years.$"

LcHollowCave_Text_SignNorthMouth:
	.string "HOLLOW CAVE, UPPER MOUTH\n"
	.string "Sand floor. Sound carries.\l"
	.string "Mind the drops.$"

LcHollowCave_Text_SignSouthMouth:
	.string "HOLLOW CAVE, LOWER MOUTH\n"
	.string "This end joins the rest of the\l"
	.string "cave one floor down.$"
