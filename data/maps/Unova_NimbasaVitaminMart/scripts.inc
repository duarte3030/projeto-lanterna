@ NimbasaVitaminMart do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaVitaminMart_MapScripts::
	.byte 0

Unova_NimbasaVitaminMart_EventScript_Npc1::
	msgbox Unova_NimbasaVitaminMart_Text_NimbasaVitaminMartGrannyText, MSGBOX_NPC
	end


Unova_NimbasaVitaminMart_Text_NimbasaVitaminMartGrannyText::
	.string "Vitamins will make"
	.string "\nyour POKéMON"
	.string "\lstronger."
	.string "\pPROTEIN increases"
	.string "\nATTACK, IRON makes"
	.string "\lDEFENSE increase."
	.string "\pCARBOS boosts"
	.string "\nSPEED, and CALCIUM"
	.string "\lworks on both"
	.string "\lSPECIAL stats.$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ MART_NIMBASA_VITAMIN do BW3G (data/items/marts.asm)
Unova_NimbasaVitaminMart_EventScript_Loja0::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_NimbasaVitaminMart_EventScript_Loja0_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_NimbasaVitaminMart_EventScript_Loja0_Itens:
	.2byte ITEM_PROTEIN
	.2byte ITEM_IRON
	.2byte ITEM_CARBOS
	.2byte ITEM_CALCIUM
	.2byte ITEM_HP_UP
	pokemartlistend
