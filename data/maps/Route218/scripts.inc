Route218_MapScripts::
	.byte 0

Route218_EventScript_JubilifeSign::
	msgbox Route218_Text_JubilifeSign, MSGBOX_SIGN
	end

Route218_Text_JubilifeSign:
	.string "JUBILIFE CITY\n"
	.string "This way.$"

Route218_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_SAILOR_SKYLER, Route218_Text_Trainer1Intro, Route218_Text_Trainer1Defeat
	msgbox Route218_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route218_Text_Trainer1Intro:
	.string "A man of the sea is also a man of\nPokémon!\p$"

Route218_Text_Trainer1Defeat:
	.string "Anchors away!\n$"

Route218_Text_Trainer1Post:
	.string "You've got what it takes to be\na Trainer among Trainers!\n$"

Route218_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_MIGUEL, Route218_Text_Trainer2Intro, Route218_Text_Trainer2Defeat
	msgbox Route218_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route218_Text_Trainer2Intro:
	.string "Outdoor fishing for the win!\pShouting doesn't help my fishing any,\nbut shout I must!\p$"

Route218_Text_Trainer2Defeat:
	.string "Gwaaah!\nThis is hurting!\n$"

Route218_Text_Trainer2Post:
	.string "Oh, right... My shouting is scaring\naway the Pokémon.\n$"

Route218_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_LUC, Route218_Text_Trainer3Intro, Route218_Text_Trainer3Defeat
	msgbox Route218_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route218_Text_Trainer3Intro:
	.string "Yeah, yeah...\nNothing's biting!\p$"

Route218_Text_Trainer3Defeat:
	.string "Can't catch a fish!\nCan't catch a break!\n$"

Route218_Text_Trainer3Post:
	.string "I was counting on strength in numbers,\nbut...\pPacking it in and going home sounds good\nat a time like this...\n$"


Route218_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_GUITARIST_TONY, Route218_Text_Trainer4Intro, Route218_Text_Trainer4Defeat
	msgbox Route218_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route218_Text_Trainer4Intro:
	.string "Let it rock!\nIt's the rhythm of battle!\p$"

Route218_Text_Trainer4Defeat:
	.string "Can you hear it?\nThat's my guitar weeping...\n$"

Route218_Text_Trainer4Post:
	.string "I'm too torn up to sing anymore...\nI am so cool that way...\n$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route218_EventScript_Placa1::
	msgbox Route218_Text_Placa1, MSGBOX_SIGN
	end

Route218_Text_Placa1:
	.string "Rt. 218\nJubilife City$"

Route218_EventScript_Placa2::
	msgbox Route218_Text_Placa2, MSGBOX_SIGN
	end

Route218_Text_Placa2:
	.string "Rt. 218\nCanalave City$"

@ ponytail: MEDIDO, e a medida contradiz o Platinum. La estes seis selam uma
@ ponte de um tile e a estrada para Canalave so abre com a Cynthia. Aqui a
@ geometria convertida e mais larga: medido com busca em largura na grade, para
@ selar a estrada seria preciso tapar as colunas 8, 9 E 10 inteiras das linhas 12
@ a 26 (a contraprova do --demo faz exatamente isso e so entao reprova). Seis
@ objetos nao chegam perto disso: eles OCUPAM a estrada sem tranca-la, e ha
@ desvio pelas fileiras 16 a 21. Fechar o vao a mao seria inventar bloqueio, e bloqueio
@ inventado e exatamente o risco que o PRD proibe: some Celestic da rota do
@ jogador e o hack trava. Ficam como cena que se desfaz, e a medida fica escrita.
Route218_EventScript_ShowGuitarist::
	msgbox Route218_Text_CenaCuter, MSGBOX_NPC
	end

Route218_EventScript_ShowFisherman::
	msgbox Route218_Text_CenaDazzle, MSGBOX_NPC
	end

Route218_EventScript_ShowClefairySouth::
	lock
	faceplayer
	playmoncry SPECIES_CLEFAIRY, CRY_MODE_NORMAL
	msgbox Route218_Text_CenaPippiih, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route218_EventScript_ShowClefairyNorth::
	lock
	faceplayer
	playmoncry SPECIES_CLEFAIRY, CRY_MODE_NORMAL
	msgbox Route218_Text_CenaPippippiih, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route218_EventScript_ShowPikachu::
	lock
	faceplayer
	playmoncry SPECIES_PIKACHU, CRY_MODE_NORMAL
	msgbox Route218_Text_CenaPikaCry, MSGBOX_DEFAULT
	waitmoncry
	release
	end

Route218_Text_CenaCuter:
	.string "That's right, CLEFAIRY!\nCuter, now!$"

Route218_Text_CenaDazzle:
	.string "PIKACHU! Try to keep up!\nYou need to dazzle!$"

Route218_Text_CenaPikaCry:
	.string "PIKACHU: Puhppikaah!$"

Route218_Text_CenaPippiih:
	.string "CLEFAIRY: Pippiih!$"

Route218_Text_CenaPippippiih:
	.string "CLEFAIRY: Pippippiih!$"
