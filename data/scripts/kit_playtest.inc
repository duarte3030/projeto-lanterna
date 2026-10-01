@ Aviso do kit de playtest da mochila, para a save que já existia (o jogo novo
@ recebe o kit calado). Quem entrega os itens e escolhe qual dos dois abre é
@ KitPlaytest_TentaEntregarNaSaveAntiga, em src/kit_playtest.c.

KitPlaytest_EventScript_Entregue::
	lockall
	playfanfare MUS_OBTAIN_ITEM
	message KitPlaytest_Text_Entregue
	waitfanfare
	waitmessage
	waitbuttonpress
	releaseall
	end

KitPlaytest_EventScript_EntregueSemEspaco::
	lockall
	playfanfare MUS_OBTAIN_ITEM
	message KitPlaytest_Text_EntregueSemEspaco
	waitfanfare
	waitmessage
	waitbuttonpress
	releaseall
	end

KitPlaytest_Text_Entregue:
	.string "Playtest kit stored in the BAG.$"

KitPlaytest_Text_EntregueSemEspaco:
	.string "Playtest kit stored in the BAG.\n"
	.string "Some items didn't fit.$"
