Cafe_MapScripts::
	.byte 0

Cafe_EventScript_Npc1::
	msgbox Cafe_Text_Npc1, MSGBOX_NPC
	end

Cafe_Text_Npc1:
	.string "How are ya doing?\nWhatcha having?\pCourse, all we ever have is\nMoomoo Milk.\pMoomoo Milk, $500 a bottle.\pWould you like to add some to your\ntraveling supplies?$"

Cafe_EventScript_Npc2::
	msgbox Cafe_Text_Npc2, MSGBOX_NPC
	end

Cafe_Text_Npc2:
	.string "Youngster, you've seen the\nPSYDUCK huddled outside?\pPSYDUCK are Pokémon that suffer from\nchronic headaches...\pI'm afraid we'll have to wait for them\nto get better.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Cafe_EventScript_Npc3::
	msgbox Cafe_Text_Npc3, MSGBOX_NPC
	end

Cafe_Text_Npc3:
	.string "Howdy, traveler!\pSome of our customers are rowdy\ntypes that want to battle.\pDo what you will with them.\nI don't mind.$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

Cafe_EventScript_CollectorFernando::
	trainerbattle_single TRAINER_SINNOH_COLLECTOR_FERNANDO, Cafe_Text_CollectorFernandoIntro, Cafe_Text_CollectorFernandoDefeat
	msgbox Cafe_Text_CollectorFernandoPost, MSGBOX_AUTOCLOSE
	end

Cafe_Text_CollectorFernandoIntro:
	.string "We were having a heated discussion\nover Pokémon the way Collectors do.$"

Cafe_Text_CollectorFernandoDefeat:
	.string "Knowledge alone isn't everything,\nyou know...$"

Cafe_Text_CollectorFernandoPost:
	.string "I'm more knowledgeable than anyone\nelse!\pI have a rare Pokémon!\pBut, I'm weak at battling...\nThat's a Pokémon Collector for you...$"

Cafe_EventScript_CollectorEdwin::
	trainerbattle_single TRAINER_SINNOH_COLLECTOR_EDWIN, Cafe_Text_CollectorEdwinIntro, Cafe_Text_CollectorEdwinDefeat
	msgbox Cafe_Text_CollectorEdwinPost, MSGBOX_AUTOCLOSE
	end

Cafe_Text_CollectorEdwinIntro:
	.string "I'm a Collector, and I love Honey!$"

Cafe_Text_CollectorEdwinDefeat:
	.string "What've you done to my Pokémon?!\pIt took me forever to catch it using\nHoney!$"

Cafe_Text_CollectorEdwinPost:
	.string "I went through a lot of bother to catch\nmy Pokémon.\pBut since I've not raised it, it's\nas weak as when I caught it.$"

Cafe_EventScript_WaitressKati::
	trainerbattle_single TRAINER_SINNOH_WAITRESS_KATI, Cafe_Text_WaitressKatiIntro, Cafe_Text_WaitressKatiDefeat
	msgbox Cafe_Text_WaitressKatiPost, MSGBOX_AUTOCLOSE
	end

Cafe_Text_WaitressKatiIntro:
	.string "Welcome!\nThis place is my pride and joy!$"

Cafe_Text_WaitressKatiDefeat:
	.string "I take losses with an unusually big\nsmile! Do you find that odd at all?$"

Cafe_Text_WaitressKatiPost:
	.string "After a match, you should have some\nMoomoo Milk to quench your thirst!\pJust chug it right down! Glug glug!$"
