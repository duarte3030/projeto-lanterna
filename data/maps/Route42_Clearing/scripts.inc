@ Campo de flores escondido ao sul da Rota 42, copiado do mapa `g12m1` do
@ Pokémon GS Chronicles. A arte é do autor, byte a byte; o jogo é o nosso, e os
@ 13 itens escondidos ficam nas 13 células onde o autor os escondeu
@ (dev_scripts/pacote_gsc_jogo.py).
Route42_Clearing_MapScripts::
	.byte 0

Route42_Clearing_EventScript_Florist::
	msgbox Route42_Clearing_Text_Florist, MSGBOX_NPC
	end

Route42_Clearing_Text_Florist:
	.string "Hardly anyone finds this field.\p"
	.string "People say things get lost among\n"
	.string "the flowers. Look closely and you\l"
	.string "might find some of them!$"

@ A placa da trilha fica na Route42, em (13,14), ao lado da fresta que leva a
@ este campo; o rótulo mora aqui para o scripts.inc gerado da rota não mudar.
Route42_EventScript_ClearingSign::
	msgbox Route42_Text_ClearingSign, MSGBOX_SIGN
	end

Route42_Text_ClearingSign:
	.string "A quiet clearing lies beyond\n"
	.string "the trees.$"
