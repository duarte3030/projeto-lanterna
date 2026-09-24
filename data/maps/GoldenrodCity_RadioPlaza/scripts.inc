@ Praça oeste de Goldenrod, com a Torre do Rádio, copiada do mapa `g3m66` do
@ Pokémon GS Chronicles. A arte é do autor, byte a byte; o jogo é o nosso, e o
@ enredo da Equipe Rocket dele (o guarda na porta e os quatro gatilhos da
@ entrada) NÃO entra (contrato, seção 1.2). Ver dev_scripts/pacote_gsc_jogo.py.
GoldenrodCity_RadioPlaza_MapScripts::
	.byte 0

GoldenrodCity_RadioPlaza_EventScript_OldMan::
	msgbox GoldenrodCity_RadioPlaza_Text_OldMan, MSGBOX_NPC
	end

GoldenrodCity_RadioPlaza_EventScript_Lass::
	msgbox GoldenrodCity_RadioPlaza_Text_Lass, MSGBOX_NPC
	end

GoldenrodCity_RadioPlaza_Text_OldMan:
	.string "I come out here every morning.\p"
	.string "The sea breeze, the gulls, and the\n"
	.string "RADIO TOWER playing my old songs…\p"
	.string "What more could an old man want?$"

GoldenrodCity_RadioPlaza_Text_Lass:
	.string "The RADIO TOWER is right on the\n"
	.string "water. On a clear day you can hear\l"
	.string "the broadcast all the way to the pier!$"
