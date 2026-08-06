@ NimbasaTMMart do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaTMMart_MapScripts::
	.byte 0

Unova_NimbasaTMMart_EventScript_Npc1::
	msgbox Unova_NimbasaTMMart_Text_NimbasaTMMartRoughneckText, MSGBOX_NPC
	end

Unova_NimbasaTMMart_EventScript_Npc2::
	msgbox Unova_NimbasaTMMart_Text_NimbasaTMMartSocialiteText, MSGBOX_NPC
	end


Unova_NimbasaTMMart_Text_NimbasaTMMartRoughneckText::
	.string "Hey. I love strong"
	.string "\nPOKéMON."
	.string "\pI want to use TMs"
	.string "\nto make my POKéMON"
	.string "\leven stronger!$"

Unova_NimbasaTMMart_Text_NimbasaTMMartSocialiteText::
	.string "There are sure to"
	.string "\nbe TMs that are"
	.string "\pjust perfect for"
	.string "\nyour POKéMON.$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ MART_NIMBASA_TM do BW3G (data/items/marts.asm)
Unova_NimbasaTMMart_EventScript_Loja0::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_NimbasaTMMart_EventScript_Loja0_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_NimbasaTMMart_EventScript_Loja0_Itens:
	.2byte ITEM_TM_REFLECT
	.2byte ITEM_TM_LIGHT_SCREEN
	.2byte ITEM_TM_PROTECT
	.2byte ITEM_TM_DIG
	.2byte ITEM_TM_SHOCK_WAVE
	pokemartlistend
