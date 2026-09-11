@ LcNewIsland: mapa copiado de Pokémon Liquid Crystal.gba (g3m70) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO e nosso.
@
@ A ilha nao tem conexao de mapa com Kanto (primario proprio, secao 3.1 do
@ METODO-COPIA-CIDADES.md): entra-se pelo cais, de barco, a partir de CINNABAR
@ ISLAND. Dentro da ilha as ligacoes sao warps de EVENTO de verdade, porque a
@ planta do hack tem doze metatiles de MB_NON_ANIMATED_DOOR, cinco de MB_LADDER
@ e cinco de MB_SOUTH_ARROW_WARP: portas desenhadas pelo autor, que o nosso
@ motor dispara.

LcNewIsland_MapScripts::
	.byte 0

LcNewIsland_EventScript_Dock::
	trainerbattle_single TRAINER_KANTO_LC_NEW_ISLAND_DOCK, LcNewIsland_Text_DockSeen, LcNewIsland_Text_DockBeaten
	msgbox LcNewIsland_Text_DockAfter, MSGBOX_AUTOCLOSE
	end

LcNewIsland_EventScript_Terrace::
	trainerbattle_single TRAINER_KANTO_LC_NEW_ISLAND_TERRACE, LcNewIsland_Text_TerraceSeen, LcNewIsland_Text_TerraceBeaten
	msgbox LcNewIsland_Text_TerraceAfter, MSGBOX_AUTOCLOSE
	end

LcNewIsland_EventScript_Researcher::
	msgbox LcNewIsland_Text_Researcher, MSGBOX_NPC
	end

LcNewIsland_EventScript_SignLanding::
	msgbox LcNewIsland_Text_SignLanding, MSGBOX_SIGN
	end

LcNewIsland_EventScript_SignTerrace::
	msgbox LcNewIsland_Text_SignTerrace, MSGBOX_SIGN
	end

LcNewIsland_Text_DockSeen:
	.string "Everyone who steps off that boat\n"
	.string "wants the same thing. Prove it!$"

LcNewIsland_Text_DockBeaten:
	.string "You wanted it more.$"

LcNewIsland_Text_DockAfter:
	.string "The invitations went out to the\n"
	.string "strongest trainers in KANTO.\p"
	.string "Nobody has ever said who sent\n"
	.string "them.$"

LcNewIsland_Text_TerraceSeen:
	.string "Something on this island is\n"
	.string "listening. Can you feel it?$"

LcNewIsland_Text_TerraceBeaten:
	.string "It heard that, too.$"

LcNewIsland_Text_TerraceAfter:
	.string "The lower terrace connects to\n"
	.string "the inner court.\p"
	.string "Whatever waits in that garden\n"
	.string "has been waiting a long time.$"

LcNewIsland_Text_Researcher:
	.string "The whole building is one machine.\n"
	.string "Every hall feeds the next.\p"
	.string "We were told it was a weather\n"
	.string "station. Nobody believes that.$"

LcNewIsland_Text_SignLanding:
	.string "NEW ISLAND\n"
	.string "Landing stage. Guests through the\l"
	.string "hall, please.$"

LcNewIsland_Text_SignTerrace:
	.string "EAST TERRACE\n"
	.string "Laboratory above, inner court\l"
	.string "below. No entry after dark.$"
