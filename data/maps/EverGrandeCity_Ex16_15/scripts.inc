@ EverGrandeCity_Ex16_15: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 16.15) por dev_scripts/copia_planta_ex.py.

EverGrandeCity_Ex16_15_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 16.15), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
EverGrandeCity_Ex16_15_EventScript_ExNpc2::
	msgbox EverGrandeCity_Ex16_15_Text_ExNpc2, MSGBOX_NPC
	end

EverGrandeCity_Ex16_15_Text_ExNpc2:
	.string "I travel around finding evolution items\n"
	.string "to supply the store here.$"


@ Os dois balconistas da loja nova do EX (16.15). O primeiro, no EX, escolhe a lista pelas
@ insígnias; aqui ele vende a lista do Pokémon League 1F (a loja que já existia em Ever Grande,
@ fim de jogo). O segundo é a loja de itens de evolução do EX, com a lista e os textos da ROM.
EverGrandeCity_Ex16_15_EventScript_ExBalconista::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart EverGrandeCity_PokemonLeague_1F_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Ex16_15_EventScript_ExLojaEvolucao::
	lock
	faceplayer
	message EverGrandeCity_Ex16_15_Text_ExLojaEvolucao
	waitmessage
	pokemart EverGrandeCity_Ex16_15_Pokemart_ExEvolucao
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
EverGrandeCity_Ex16_15_Pokemart_ExEvolucao:
	.2byte ITEM_FIRE_STONE
	.2byte ITEM_WATER_STONE
	.2byte ITEM_LEAF_STONE
	.2byte ITEM_THUNDER_STONE
	.2byte ITEM_ICE_STONE
	.2byte ITEM_DAWN_STONE
	.2byte ITEM_DUSK_STONE
	.2byte ITEM_SHINY_STONE
	.2byte ITEM_SUN_STONE
	.2byte ITEM_MOON_STONE
	.2byte ITEM_BLACK_AUGURITE
	.2byte ITEM_PEAT_BLOCK
	.2byte ITEM_KINGS_ROCK
	.2byte ITEM_DEEP_SEA_TOOTH
	.2byte ITEM_DEEP_SEA_SCALE
	.2byte ITEM_DRAGON_SCALE
	.2byte ITEM_RAZOR_CLAW
	.2byte ITEM_RAZOR_FANG
	.2byte ITEM_REAPER_CLOTH
	.2byte ITEM_UPGRADE
	.2byte ITEM_DUBIOUS_DISC
	.2byte ITEM_LINKING_CORD
	.2byte ITEM_MAGMARIZER
	.2byte ITEM_ELECTIRIZER
	.2byte ITEM_METAL_COAT
	pokemartlistend

EverGrandeCity_Ex16_15_Text_ExLojaEvolucao:
	.string "Welcome to the evolution item store.\p"
	.string "How may I help you?$"

