LakeVerity_MapScripts::
	.byte 0

LakeVerity_EventScript_Fisherman::
	msgbox LakeVerity_Text_Fisherman, MSGBOX_NPC
	end

LakeVerity_EventScript_Hiker::
	msgbox LakeVerity_Text_Hiker, MSGBOX_NPC
	end

@ Grunt mudo de pret/pokeplatinum (LOCALID_GRUNT_M, hidden_flag
@ FLAG_HIDE_LAKE_VERITY_TEAM_GALACTIC); some com os outros quando a Mars cai.
LakeVerity_EventScript_GruntM::
	msgbox LakeVerity_Text_GruntM, MSGBOX_NPC
	end

LakeVerity_Text_GruntM:
	.string "Ow! Ouch!\n"
	.string "What's with this old-timer?$"

LakeVerity_Text_Fisherman:
	.string "This lake is calm today...\n"
	.string "Good a spot as any to cast a line.$"

LakeVerity_Text_Hiker:
	.string "They say Lake Verity never freezes,\n"
	.string "no matter how cold the winter gets.$"

LakeVerity_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VERITY_1, LakeVerity_Text_Trainer1Intro, LakeVerity_Text_Trainer1Defeat
	msgbox LakeVerity_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

LakeVerity_Text_Trainer1Intro:
	.string "It is our mission to stall you.\n"
	.string "Sorry, but we gotta do our job.$"

LakeVerity_Text_Trainer1Defeat:
	.string "Losing was a part of my job, too.\n"
	.string "...I feel better by saying that.$"

LakeVerity_Text_Trainer1Post:
	.string "From three lakes, we must secure three\n"
	.string "Pokémon.\pYou simply mustn't interfere!$"

LakeVerity_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VERITY_3, LakeVerity_Text_Trainer2Intro, LakeVerity_Text_Trainer2Defeat
	msgbox LakeVerity_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

LakeVerity_Text_Trainer2Intro:
	.string "I'll knock your Pokémon into orbit!$"

LakeVerity_Text_Trainer2Defeat:
	.string "My mind is going orbital!$"

LakeVerity_Text_Trainer2Post:
	.string "The Pokémon here has already been\n"
	.string "taken to our HQ in Veilstone.\pSo, you see?\n"
	.string "A child like you can't touch us!$"

LakeVerity_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VERITY_2, LakeVerity_Text_Trainer3Intro, LakeVerity_Text_Trainer3Defeat
	msgbox LakeVerity_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

LakeVerity_Text_Trainer3Intro:
	.string "In order for us to bring peace to\n"
	.string "the world, we must control it!$"

LakeVerity_Text_Trainer3Defeat:
	.string "You're too young to understand.$"

LakeVerity_Text_Trainer3Post:
	.string "Our boss always had plans for\n"
	.string "the three lakes...\pWhile you were blissfully ignorant,\n"
	.string "our work went ahead...$"

LakeVerity_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_LAKE_VERITY_4, LakeVerity_Text_Trainer4Intro, LakeVerity_Text_Trainer4Defeat
	msgbox LakeVerity_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

LakeVerity_Text_Trainer4Intro:
	.string "If this mission is successful, we\n"
	.string "will get a nice bonus.$"

LakeVerity_Text_Trainer4Defeat:
	.string "There goes our bonus...\n"
	.string "This is an epic tragedy...$"

LakeVerity_Text_Trainer4Post:
	.string "I want Team Galactic to become\n"
	.string "powerful. That is all I want.$"

@ ponytail: a derrota da Mars faz o que o Platinum faz na mesma linha
@ (scripts_lake_verity.s:200 em diante): a Galactica INTEIRA sai do lago e a
@ Jupiter aparece no Lago Acuity. Os quatro grunts que ja estavam neste mapa
@ ganharam FLAG_GALACTICA_LAGO_VERITY no campo `flag`, entao somem com ela; o
@ `removeobject` de cada um e para saírem na hora, sem precisar sair e voltar.
LakeVerity_EventScript_Mars::
	lock
	faceplayer
	msgbox LakeVerity_Text_CenaMarsIntro, MSGBOX_DEFAULT
	trainerbattle_single TRAINER_SINNOH_COMMANDER_MARS_LAKE_VERITY, LakeVerity_Text_CenaMarsIntro, LakeVerity_Text_CenaMarsDefeat, LakeVerity_EventScript_MarsBeaten
	end

LakeVerity_EventScript_MarsBeaten::
	msgbox LakeVerity_Text_CenaPullingOut, MSGBOX_DEFAULT
	msgbox LakeVerity_Text_CenaAllLakePokemon, MSGBOX_DEFAULT
	closemessage
	fadescreen FADE_TO_BLACK
	setflag FLAG_GALACTICA_LAGO_VERITY
	removeobject LOCALID_LAKE_VERITY_MARS
	removeobject LOCALID_LAKE_VERITY_TRAINER1
	removeobject LOCALID_LAKE_VERITY_TRAINER2
	removeobject LOCALID_LAKE_VERITY_TRAINER3
	removeobject LOCALID_LAKE_VERITY_TRAINER4
	removeobject LOCALID_LAKE_VERITY_GRUNT_M
	fadescreen FADE_FROM_BLACK
	release
	end

LakeVerity_Text_CenaAllLakePokemon:
	.string "The Pokémon of the three lakes are\nconnected somehow.\pThanks to Saturn's grandstanding at\nLake Valor, a cavern appeared here.\pIt was the cavern where the Pokémon\nMESPRIT slept.\pMESPRIT appeared, too, probably to\ngo help its friends.\pThat worked out well for us.\nIt was super easy to catch.\pSo, now we've got them all:\nMESPRIT, 'The Being of Emotion.'\pAZELF, 'The Being of Willpower.'\pUXIE, 'The Being of Intelligence.'\pNow that we have them all...\pYou can look forward to what plans\nTeam Galactic has for them!$"

LakeVerity_Text_CenaMarsDefeat:
	.string "I lost again...\pSo, first the windworks, and now\nLake Verity that I owe you for!\pThis shouldn't be happening to Team\nGalactic's Commander...\p...Calm down, Mars...\nI've done my part in all of this...\pMy mission was to transport the\nlake's Pokémon to our HQ...\p...That's right! I accomplished my\nmission without a problem!$"

LakeVerity_Text_CenaMarsIntro:
	.string "Mars: That face...!\nIt brings back bad memories!\pI'm talking about the windworks!\pI caught a whole lot of trouble\nfor that little incident.\pWhat's with that look on your face?\nYou do remember me, don't you?\pFine, whatever.\nI'll tell you who I am again!\pI'm Mars, one of Team Galactic's\nCommanders.\pSo, what is it? Are you some\nlovey-dovey couple to the rescue?\pNot a chance! Not even a teeny one!\nYou're all going down!$"

LakeVerity_Text_CenaPullingOut:
	.string "Team! We're pulling out!\nThe boss is waiting at the HQ!$"
