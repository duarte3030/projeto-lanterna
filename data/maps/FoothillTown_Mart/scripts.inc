@ FoothillTown_Mart: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 17.0) por dev_scripts/copia_planta_ex.py.

FoothillTown_Mart_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 17.0), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
FoothillTown_Mart_EventScript_ExNpc1::
	msgbox FoothillTown_Mart_Text_ExNpc1, MSGBOX_NPC
	end

FoothillTown_Mart_Text_ExNpc1:
	.string "What type of medicine do you think\n"
	.string "works best on GRASS TYPE POKéMON?$"

FoothillTown_Mart_EventScript_ExNpc2::
	msgbox FoothillTown_Mart_Text_ExNpc2, MSGBOX_NPC
	end

FoothillTown_Mart_Text_ExNpc2:
	.string "I need a good drink after all that\n"
	.string "running.$"


@ Balconista NOSSO. O do EX escolhe a lista pelas insígnias (script comum dele);
@ aqui a lista é a da loja de Verdanturf, a vizinha, sem os dois itens que só ela vende.
FoothillTown_Mart_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart FoothillTown_Mart_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
FoothillTown_Mart_Pokemart:
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_ICE_HEAL
	.2byte ITEM_REPEL
	.2byte ITEM_X_SP_ATK
	pokemartlistend
