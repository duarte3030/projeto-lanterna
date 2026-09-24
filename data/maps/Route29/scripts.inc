Route29_MapScripts::
	.byte 0

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

Route29_EventScript_Sign::
	lock
	msgbox Route29_Text_Sign1, MSGBOX_SIGN
	closemessage
	release
	end

Route29_Text_Sign1::
	.string "ROUTE 29\p"
	.string "CHERRYGROVE CITY - NEW BARK TOWN$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

Route29_EventScript_Youngster::
	lock
	faceplayer
	msgbox Route29_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

Route29_Text_Youngster::
	.string "Yo. How are your POKéMON?\p"
	.string "If they're weak and not ready\n"
	.string "for battle, keep out of the grass.$"

Route29_EventScript_Girl::
	lock
	faceplayer
	msgbox Route29_Text_Girl, MSGBOX_DEFAULT
	closemessage
	release
	end

Route29_Text_Girl::
	.string "I wanted to take a break,\n"
	.string "so I saved to record my progress.$"

Route29_EventScript_Lass::
	lock
	faceplayer
	msgbox Route29_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

Route29_Text_Lass::
	.string "See those ledges?\n"
	.string "It's scary to jump off them.\p"
	.string "But you can go to NEW BARK\n"
	.string "without walking through the grass.$"

@ Volta da Route29 para a CHERRYGROVE CITY (dev_scripts/remapeia_cherrygrove.py).
@ A cidade é cópia do Scorched Silver com secundário próprio, e a Route29 é
@ da New Bark: a conexão saiu e a travessia virou warp. Do lado da cidade é
@ seta; deste lado é gatilho, porque o primário está cheio e o secundário
@ não é desta frente. Um gatilho por célula, cada um para a seta da mesma linha.

Route29_EventScript_VoltaCherrygrove0::
	lockall
	warp MAP_CHERRYGROVE_CITY, 10
	waitstate
	releaseall
	end

Route29_EventScript_VoltaCherrygrove1::
	lockall
	warp MAP_CHERRYGROVE_CITY, 11
	waitstate
	releaseall
	end

Route29_EventScript_VoltaCherrygrove2::
	lockall
	warp MAP_CHERRYGROVE_CITY, 12
	waitstate
	releaseall
	end

Route29_EventScript_VoltaCherrygrove3::
	lockall
	warp MAP_CHERRYGROVE_CITY, 13
	waitstate
	releaseall
	end
