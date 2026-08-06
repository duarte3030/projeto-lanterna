@ Rt4NimbasaGate do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt4NimbasaGate_MapScripts::
	.byte 0

Unova_Rt4NimbasaGate_EventScript_Npc0::
	msgbox Unova_Rt4NimbasaGate_Text_R4NimbasaGatePokefanMText, MSGBOX_NPC
	end

Unova_Rt4NimbasaGate_EventScript_Npc1::
	msgbox Unova_Rt4NimbasaGate_Text_R4NimbasaGateYoungsterText, MSGBOX_NPC
	end


Unova_Rt4NimbasaGate_Text_R4NimbasaGatePokefanMText::
	.string "This place used to"
	.string "\nbe a shopping"
	.string "\pcenter called JOIN"
	.string "\nAVENUE."
	.string "\pBut after a few"
	.string "\nyears, vendors"
	.string "\lstarted to leave."
	.string "\pNow the place is"
	.string "\nabandoned.$"

Unova_Rt4NimbasaGate_Text_R4NimbasaGateYoungsterText::
	.string "I'm searching to"
	.string "\nsee if any of the"
	.string "\pvendors left any"
	.string "\nof their stuff"
	.string "\lbehind!$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ MART_R4_NIMBASA_GATE do BW3G (data/items/marts.asm)
Unova_Rt4NimbasaGate_EventScript_Loja0::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart Unova_Rt4NimbasaGate_EventScript_Loja0_Itens
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
Unova_Rt4NimbasaGate_EventScript_Loja0_Itens:
	.2byte ITEM_ENERGYPOWDER
	.2byte ITEM_ENERGY_ROOT
	.2byte ITEM_HEAL_POWDER
	.2byte ITEM_REVIVAL_HERB
	pokemartlistend
