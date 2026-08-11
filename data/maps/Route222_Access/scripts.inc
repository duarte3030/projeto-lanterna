Route222_Access_MapScripts::
	.byte 0

Route222_Access_EventScript_Tuber::
	msgbox Route222_Access_Text_Tuber, MSGBOX_NPC
	end

Route222_Access_EventScript_Pokefan::
	msgbox Route222_Access_Text_Pokefan, MSGBOX_NPC
	end

Route222_Access_Text_Tuber:
	.string "SUNYSHORE CITY's beaches are the\n"
	.string "best place to relax!$"

Route222_Access_Text_Pokefan:
	.string "That city runs entirely on solar\n"
	.string "power. Pretty amazing, huh?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route222_Access_EventScript_Npc1::
	msgbox Route222_Access_Text_Npc1, MSGBOX_NPC
	end

Route222_Access_Text_Npc1:
	.string "If I had to describe Sunyshore Gym\nin a word, it'd be...\pShockingly electric!\pWhoops, that's two words!$"

Route222_Access_EventScript_Npc2::
	msgbox Route222_Access_Text_Npc2, MSGBOX_NPC
	end

Route222_Access_Text_Npc2:
	.string "Sunyshore's Gym Leader Volkner's been\nbored lately, I hear.\pWe need tough challengers to visit so\nhe doesn't get bored.\pPeople get up to no good if they have\ntoo much time on their hands.$"
