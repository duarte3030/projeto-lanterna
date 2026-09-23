@ LcCinnabarVolcano: mapa copiado de Pokémon Liquid Crystal.gba (g5m45) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) e nosso e entra aqui.
@
@ A cratera nao tem conexao de mapa com Kanto, de proposito: o primario dela e o
@ gTileset_LcOutdoor e o de Kanto e outro, e travessia por conexao so recarrega
@ o tileset SECUNDARIO (secao 3.1 do METODO-COPIA-CIDADES.md). A ENTRADA e por
@ guia, um warp de script em Cinnabar Island, no molde do marinheiro da Outskirt
@ Island; a SAIDA e warp de evento de verdade, nas duas fendas que o autor
@ desenhou, (7,37) e (40,37), as duas em MB_SOUTH_ARROW_WARP.
@
@ A planta tem DOIS ramos que nao se ligam a pe: o oeste sobe ate a porta de
@ (20,7), que da na camara de cinzas, e o leste sobe ate a galeria e a poca de
@ agua. Por isso ha dois guias e duas fendas, uma por ramo.

LcCinnabarVolcano_MapScripts::
	.byte 0

@ ---------------------------------------------------------------- treinadores

LcCinnabarVolcano_EventScript_HikerWestFlue::
	trainerbattle_single TRAINER_KANTO_LC_VOLCANO_WEST_HIKER, LcCinnabarVolcano_Text_HikerSeen, LcCinnabarVolcano_Text_HikerBeaten
	msgbox LcCinnabarVolcano_Text_HikerAfter, MSGBOX_AUTOCLOSE
	end

LcCinnabarVolcano_EventScript_BlackBeltWestFlue::
	trainerbattle_single TRAINER_KANTO_LC_VOLCANO_WEST_BELT, LcCinnabarVolcano_Text_BeltSeen, LcCinnabarVolcano_Text_BeltBeaten
	msgbox LcCinnabarVolcano_Text_BeltAfter, MSGBOX_AUTOCLOSE
	end

LcCinnabarVolcano_EventScript_BurglarEastFlue::
	trainerbattle_single TRAINER_KANTO_LC_VOLCANO_EAST_BIKER, LcCinnabarVolcano_Text_BikerSeen, LcCinnabarVolcano_Text_BikerBeaten
	msgbox LcCinnabarVolcano_Text_BikerAfter, MSGBOX_AUTOCLOSE
	end

LcCinnabarVolcano_EventScript_CamperGallery::
	trainerbattle_single TRAINER_KANTO_LC_VOLCANO_GALLERY_CAMPER, LcCinnabarVolcano_Text_CamperSeen, LcCinnabarVolcano_Text_CamperBeaten
	msgbox LcCinnabarVolcano_Text_CamperAfter, MSGBOX_AUTOCLOSE
	end

LcCinnabarVolcano_EventScript_BeautyGallery::
	trainerbattle_single TRAINER_KANTO_LC_VOLCANO_GALLERY_BEAUTY, LcCinnabarVolcano_Text_BeautySeen, LcCinnabarVolcano_Text_BeautyBeaten
	msgbox LcCinnabarVolcano_Text_BeautyAfter, MSGBOX_AUTOCLOSE
	end

@ ---------------------------------------------------------------- gente e placas

LcCinnabarVolcano_EventScript_Surveyor::
	msgbox LcCinnabarVolcano_Text_Surveyor, MSGBOX_NPC
	end

LcCinnabarVolcano_EventScript_SignWestFlue::
	msgbox LcCinnabarVolcano_Text_SignWestFlue, MSGBOX_SIGN
	end

LcCinnabarVolcano_EventScript_SignEastFlue::
	msgbox LcCinnabarVolcano_Text_SignEastFlue, MSGBOX_SIGN
	end

LcCinnabarVolcano_EventScript_SignPool::
	msgbox LcCinnabarVolcano_Text_SignPool, MSGBOX_SIGN
	end

@ ---------------------------------------------------------------- textos

LcCinnabarVolcano_Text_HikerSeen:
	.string "This flue is mine until sundown!\n"
	.string "Climb past me and you battle me!$"

LcCinnabarVolcano_Text_HikerBeaten:
	.string "The mountain wins again…$"

LcCinnabarVolcano_Text_HikerAfter:
	.string "The west flue runs all the way to\n"
	.string "the old ash chamber up top.\p"
	.string "The east one doesn't meet it.\n"
	.string "Two chimneys, one mountain.$"

LcCinnabarVolcano_Text_BeltSeen:
	.string "Heat like this tests a trainer.\n"
	.string "Show me what you have!$"

LcCinnabarVolcano_Text_BeltBeaten:
	.string "Your POKéMON never wavered.$"

LcCinnabarVolcano_Text_BeltAfter:
	.string "I train here because the air\n"
	.string "fights back.\p"
	.string "An hour on this slope is worth a\n"
	.string "week on the beach.$"

LcCinnabarVolcano_Text_BikerSeen:
	.string "You came up the east crack?\n"
	.string "Then you're not here for a walk!$"

LcCinnabarVolcano_Text_BikerBeaten:
	.string "Burned out. Literally.$"

LcCinnabarVolcano_Text_BikerAfter:
	.string "Every year the crack opens a\n"
	.string "little wider.\p"
	.string "One day the whole east wall goes,\n"
	.string "and I want to be here to see it.$"

LcCinnabarVolcano_Text_CamperSeen:
	.string "Careful on the gallery!\n"
	.string "One slip and it's a long drop.$"

LcCinnabarVolcano_Text_CamperBeaten:
	.string "I slipped first, then.$"

LcCinnabarVolcano_Text_CamperAfter:
	.string "This ledge is the only level\n"
	.string "ground in the whole crater.\p"
	.string "Everyone who comes up here ends\n"
	.string "up camping on it.$"

LcCinnabarVolcano_Text_BeautySeen:
	.string "The steam here is good for the\n"
	.string "skin. The POKéMON, less so!$"

LcCinnabarVolcano_Text_BeautyBeaten:
	.string "So much for a quiet soak.$"

LcCinnabarVolcano_Text_BeautyAfter:
	.string "Follow the gallery west and it\n"
	.string "drops to a warm pool.\p"
	.string "Nothing walks across that water.\n"
	.string "You swim it or you turn back.$"

LcCinnabarVolcano_Text_Surveyor:
	.string "CINNABAR ISLAND sits on this\n"
	.string "mountain, not beside it.\p"
	.string "I read the flue every week. The\n"
	.string "day the numbers jump, the town\l"
	.string "hears it from me first.$"

LcCinnabarVolcano_Text_SignWestFlue:
	.string "WEST FLUE\n"
	.string "Loose rock above. Keep to the\l"
	.string "wall and keep climbing.$"

LcCinnabarVolcano_Text_SignEastFlue:
	.string "EAST FLUE\n"
	.string "Opened by the last tremor.\l"
	.string "Depth unknown.$"

LcCinnabarVolcano_Text_SignPool:
	.string "The rock ends at the water.\n"
	.string "Steam rises off the far side.$"
