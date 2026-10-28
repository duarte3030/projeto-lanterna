@ VirbankPort do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VirbankPort_MapScripts::
	.byte 0

Unova_VirbankPort_EventScript_Npc0::
	msgbox Unova_VirbankPort_Text_VirbankPortRideText, MSGBOX_NPC
	end

Unova_VirbankPort_EventScript_Marinheiro::
	lock
	faceplayer
	msgbox Unova_VirbankPort_Text_ParaOnde, MSGBOX_DEFAULT
	@ O menu e montado em data/scripts/travessia_regioes.inc e esconde o
	@ destino ainda nao liberado. Os `case` abaixo NAO mudam: o id
	@ empilhado continua sendo o indice antigo da lista.
	call Travessia_EventScript_MenuDeDestinos
	switch VAR_RESULT
	@ Cartucho 2 (28/10/2026): os destinos 0, 1, 2 e 4 (Olivine, Slateport,
	@ Vermilion e Canalave) sairam com as regioes do cartucho 1. Sobra Galar,
	@ destino 6, atras de FLAG_GALAR_QA_ANDAR (data/scripts/travessia_regioes.inc).
	case 6, Travessia_EventScript_ZarparParaGalar
	msgbox Unova_VirbankPort_Text_Volte, MSGBOX_DEFAULT
	release
	end

Unova_VirbankPort_Text_ParaOnde:
	.string "Welcome to VIRBANK CITY, UNOVA!\n"
	.string "Where would you like to sail?$"

Unova_VirbankPort_Text_Volte:
	.string "Come see me whenever you want to\nset sail!$"



Unova_VirbankPort_Text_VirbankPortRideText::
	.string "We'll soon set"
	.string "\nsail for CASTELIA."
	.string "\pAre you coming on"
	.string "\nboard?$"
