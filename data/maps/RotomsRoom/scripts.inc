RotomsRoom_MapScripts::
	.byte 0

RotomsRoom_EventScript_Placa1::
	msgbox RotomsRoom_Text_Placa1, MSGBOX_SIGN
	end

RotomsRoom_Text_Placa1:
	.string "Oh? ROTOM appears as if it wants to\nrevert to its original form.\pWould you like to recall it from\nthe motor?$"

RotomsRoom_EventScript_Placa2::
	msgbox RotomsRoom_Text_Placa2, MSGBOX_SIGN
	end

RotomsRoom_Text_Placa2:
	.string "Oh? ROTOM appears as if it wants to\nrevert to its original form.\pWould you like to recall it from\nthe motor?$"

RotomsRoom_EventScript_Placa3::
	msgbox RotomsRoom_Text_Placa3, MSGBOX_SIGN
	end

RotomsRoom_Text_Placa3:
	.string "Oh? ROTOM appears as if it wants to\nrevert to its original form.\pWould you like to recall it from\nthe motor?$"

RotomsRoom_EventScript_Placa4::
	msgbox RotomsRoom_Text_Placa4, MSGBOX_SIGN
	end

RotomsRoom_Text_Placa4:
	.string "Oh? ROTOM appears as if it wants to\nrevert to its original form.\pWould you like to recall it from\nthe motor?$"

RotomsRoom_EventScript_Placa5::
	msgbox RotomsRoom_Text_Placa5, MSGBOX_SIGN
	end

RotomsRoom_Text_Placa5:
	.string "Oh? ROTOM appears as if it wants to\nrevert to its original form.\pWould you like to recall it from\nthe motor?$"

@ >>> Sinnoh, 23/08/2026: os cinco eletrodomesticos e os dois livros do quarto
@ do Rotom entram como CENARIO com texto, decisao do condutor.
@ Na fonte eles sao objeto com `hidden_flag` viva (FLAG_HIDE_ROTOMS_ROOM_FAN e
@ irmas) e cada um abre o menu de troca de forma do Rotom, que e mecanica de
@ gen 4 que este motor nao tem no mapa. O que ele TEM e o item:
@ `ITEM_ROTOM_CATALOG` (include/constants/items.h:847) com
@ `ItemUseOutOfBattle_RotomCatalog` (src/data/items.h:13629), entregue pela Dex
@ no laboratorio. Entao o movel fica de pe e o texto manda usar o catalogo, que
@ e verdade nesta ROM e nao promessa.
@ Coordenada: a da fonte cai fora (os eletrodomesticos moram em x=4..12 e o
@ nosso quarto e o molde de 10x9 da casa de Oreburgh), entao eles entram
@ enfileirados na linha 5 como na fonte, e os livros na parte de cima.
RotomsRoom_EventScript_Eletrodomestico::
	msgbox RotomsRoom_Text_Eletrodomestico, MSGBOX_SIGN
	end

RotomsRoom_Text_Eletrodomestico:
	.string "An old household appliance sits here,\nhumming faintly.\pROTOM could slip inside it, but only\nthe ROTOM CATALOG can call it back.$"

RotomsRoom_EventScript_Livro::
	msgbox RotomsRoom_Text_Livro, MSGBOX_SIGN
	end

RotomsRoom_Text_Livro:
	.string "A notebook left open on the shelf.\p“The ROTOM CATALOG lists every\nappliance ROTOM can possess.”$"

RotomsRoom_EventScript_Microwave::
	msgbox RotomsRoom_Text_Microwave, MSGBOX_NPC
	end

RotomsRoom_Text_Microwave:
	.string "Which ROTOM are you choosing?$"
