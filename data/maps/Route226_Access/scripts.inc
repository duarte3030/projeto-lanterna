Route226_Access_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route226_Access_EventScript_Npc1::
	msgbox Route226_Access_Text_Npc1, MSGBOX_NPC
	end

Route226_Access_Text_Npc1:
	.string "Hey, konnichiwa!\nGlad to meet you, guten tag!\pI'm the Meister.\pIn this language's parlance I would\nbe called a craftsman.\pSomething like that, n'est ce pas?\nComprendo?$"

Route226_Access_EventScript_Placa2::
	msgbox Route226_Access_Text_Placa2, MSGBOX_SIGN
	end

Route226_Access_Text_Placa2:
	.string "There is something scribbled on this\nnotice.\p'The world-traveling Meister has\nvisited over 150 countries!\p'But the world remains as big as ever!'$"
