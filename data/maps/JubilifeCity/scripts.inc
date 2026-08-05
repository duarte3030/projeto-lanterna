@ Mapa de referencia de Sinnoh. O padrao usado aqui vale para os outros 132:
@ ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever qualquer script novo.
@ Textos vindos de pret/pokeplatinum, em ingles, como o resto do jogo.

JubilifeCity_MapScripts::
	.byte 0

JubilifeCity_EventScript_AceTrainerF::
	msgbox JubilifeCity_Text_AceTrainerF, MSGBOX_NPC
	end

JubilifeCity_EventScript_AceTrainerM1::
	msgbox JubilifeCity_Text_AceTrainerM1, MSGBOX_NPC
	end

JubilifeCity_EventScript_SchoolKidM1::
	lock
	faceplayer
	msgbox JubilifeCity_Text_SchoolKidM1, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_Twin::
	msgbox JubilifeCity_Text_Twin, MSGBOX_NPC
	end

JubilifeCity_EventScript_ExpertM1::
	lock
	faceplayer
	msgbox JubilifeCity_Text_ExpertM1, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_SchoolKidM2::
	msgbox JubilifeCity_Text_SchoolKidM2, MSGBOX_NPC
	end

JubilifeCity_EventScript_ExpertM2::
	lock
	faceplayer
	msgbox JubilifeCity_Text_ExpertM2, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_AceTrainerM2::
	msgbox JubilifeCity_Text_AceTrainerM2, MSGBOX_NPC
	end

JubilifeCity_EventScript_AceTrainerM3::
	msgbox JubilifeCity_Text_AceTrainerM3, MSGBOX_NPC
	end

JubilifeCity_EventScript_KidWithNds1::
	msgbox JubilifeCity_Text_KidWithNds1, MSGBOX_NPC
	end

JubilifeCity_EventScript_KidWithNds2::
	msgbox JubilifeCity_Text_KidWithNds2, MSGBOX_NPC
	end

JubilifeCity_EventScript_CitySign::
	msgbox JubilifeCity_Text_CitySign, MSGBOX_SIGN
	end

JubilifeCity_EventScript_MartSign::
	msgbox JubilifeCity_Text_MartSign, MSGBOX_SIGN
	end

JubilifeCity_EventScript_SchoolSign::
	msgbox JubilifeCity_Text_SchoolSign, MSGBOX_SIGN
	end

JubilifeCity_Text_AceTrainerF:
	.string "This city is huge... I could use it\n"
	.string "to train my legs as much as my\l"
	.string "POKéMON!$"

JubilifeCity_Text_AceTrainerM1:
	.string "Jubilife's got Trainers on every\n"
	.string "corner. Keep your guard up if you\l"
	.string "don't want to get challenged!$"

JubilifeCity_Text_SchoolKidM1:
	.string "The way you look... You're obviously\n"
	.string "a Trainer!\p"
	.string "What type of POKéMON do you like\n"
	.string "best? I bet it says a lot about you!$"

JubilifeCity_Text_Twin:
	.string "Me and my sister came all the way\n"
	.string "to JUBILIFE just to see the TV\l"
	.string "station. Isn't that exciting?$"

JubilifeCity_Text_ExpertM1:
	.string "Hello, Trainer! Do you know much\n"
	.string "about POKéMON?\p"
	.string "There's a TRAINERS' SCHOOL here in\n"
	.string "town. Even if you know a lot, you\l"
	.string "may still discover something new!$"

JubilifeCity_Text_SchoolKidM2:
	.string "I'm still practicing, but someday\n"
	.string "I'll be a great POKéMON Trainer!$"

JubilifeCity_Text_ExpertM2:
	.string "JUBILIFE CITY was built on land\n"
	.string "carved out of a mountain. The people\l"
	.string "of OREBURGH CITY helped out.\p"
	.string "Have you visited the TV station yet?\n"
	.string "You could be a star! Or at least\l"
	.string "dream of being one!$"

JubilifeCity_Text_AceTrainerM2:
	.string "I like to walk this whole city end\n"
	.string "to end. Good way to scout for tough\l"
	.string "Trainers to battle.$"

JubilifeCity_Text_AceTrainerM3:
	.string "The POKÉTCH COMPANY has its main\n"
	.string "office right here in JUBILIFE.\l"
	.string "Pretty neat, huh?$"

JubilifeCity_Text_KidWithNds1:
	.string "I'm trying to beat this game before\n"
	.string "dinner! No time to chat!$"

JubilifeCity_Text_KidWithNds2:
	.string "Wanna trade high scores sometime?$"

JubilifeCity_Text_CitySign:
	.string "JUBILIFE CITY\n"
	.string "The City of Vibrant People and\l"
	.string "POKéMON$"

JubilifeCity_Text_MartSign:
	.string "JUBILIFE CITY MART$"

JubilifeCity_Text_SchoolSign:
	.string "TRAINERS' SCHOOL$"

@ ---------------------------------------------------------------------------
@ Historia: primeiro encontro com a Equipe Galactica.
@ Texto de pret/pokeplatinum, res/text/jubilife_city.json. Dois grunts pressionam
@ o Prof. Rowan em frente a Trainers' School. Vencer os DOIS encerra a cena,
@ liga FLAG_GALACTICA_JUBILIFE e some com os tres NPCs. Zero var: quem sabe se a
@ cena acabou e a flag de treinador derrotado, que o jogo ja guarda de graca.

JubilifeCity_EventScript_Rowan::
	lock
	faceplayer
	msgbox JubilifeCity_Text_RowanGiveThemALesson, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_GalacticGrunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_JUBILIFE_CITY_1, JubilifeCity_Text_Grunt1Intro, JubilifeCity_Text_GruntDefeat, JubilifeCity_EventScript_Grunt1Defeated
	msgbox JubilifeCity_Text_RowanGiveThemALesson, MSGBOX_AUTOCLOSE
	end

JubilifeCity_EventScript_Grunt1Defeated::
	goto_if_defeated TRAINER_SINNOH_GALACTIC_GRUNT_JUBILIFE_CITY_2, JubilifeCity_EventScript_GalacticRetreats
	msgbox JubilifeCity_Text_RowanLecture, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_GalacticGrunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_JUBILIFE_CITY_2, JubilifeCity_Text_Grunt2Intro, JubilifeCity_Text_GruntDefeat, JubilifeCity_EventScript_Grunt2Defeated
	msgbox JubilifeCity_Text_RowanGiveThemALesson, MSGBOX_AUTOCLOSE
	end

JubilifeCity_EventScript_Grunt2Defeated::
	goto_if_defeated TRAINER_SINNOH_GALACTIC_GRUNT_JUBILIFE_CITY_1, JubilifeCity_EventScript_GalacticRetreats
	msgbox JubilifeCity_Text_RowanLecture, MSGBOX_DEFAULT
	release
	end

JubilifeCity_EventScript_GalacticRetreats::
	msgbox JubilifeCity_Text_GalacticIsBenevolent, MSGBOX_DEFAULT
	msgbox JubilifeCity_Text_RowanCalledThemselvesGalactic, MSGBOX_DEFAULT
	msgbox JubilifeCity_Text_RowanCollectAllBadges, MSGBOX_DEFAULT
	removeobject LOCALID_JUBILIFE_GALACTIC_GRUNT_1
	removeobject LOCALID_JUBILIFE_GALACTIC_GRUNT_2
	removeobject LOCALID_JUBILIFE_ROWAN
	setflag FLAG_GALACTICA_JUBILIFE
	release
	end

JubilifeCity_Text_Grunt1Intro:
	.string "Now, now, now, now, now!\n"
	.string "Professor Rowan, you must comply.\p"
	.string "Hand over all your research\n"
	.string "findings. For free, naturally.\p"
	.string "Failure to comply will result in a\n"
	.string "painful time for your assistant.$"

JubilifeCity_Text_Grunt2Intro:
	.string "Eeeeeh!\n"
	.string "You had to make this personal!\p"
	.string "You have forced our hand into\n"
	.string "making a show of force!\p"
	.string "We will make you regret insulting\n"
	.string "Team Galactic!$"

JubilifeCity_Text_GruntDefeat:
	.string "You leave us no option.\n"
	.string "We will retreat for now.$"

JubilifeCity_Text_GalacticIsBenevolent:
	.string "We shall do so because Team\n"
	.string "Galactic is benevolent to all.$"

JubilifeCity_Text_RowanGiveThemALesson:
	.string "Rowan: You kids, give these thugs\n"
	.string "a lesson in civility, please.$"

JubilifeCity_Text_RowanLecture:
	.string "Rowan: Quiet, you lot!\n"
	.string "Why must you be such a nuisance?\p"
	.string "Let me list some lessons you still\n"
	.string "need to learn.\p"
	.string "No. 1: Don't loiter about for no\n"
	.string "good reason.\p"
	.string "No. 2: Don't interrupt others while\n"
	.string "they are attempting to converse.\p"
	.string "No. 3: If you don't get your way,\n"
	.string "don't raise your voice to be\l"
	.string "intimidating.\p"
	.string "No. 4: Don't think you've grown\n"
	.string "strong just because you're in a\l"
	.string "group.\p"
	.string "No. 5: What is with those outlandish\n"
	.string "outfits you have on?\p"
	.string "My goodness...\n"
	.string "You call yourselves adults?$"

JubilifeCity_Text_RowanCalledThemselvesGalactic:
	.string "Rowan: That lot...\n"
	.string "They called themselves Team\l"
	.string "Galactic.\p"
	.string "When Pokémon evolve, they seem to\n"
	.string "release some type of energy...\p"
	.string "However, I believe that it's a\n"
	.string "mystic power far beyond our\l"
	.string "control.\p"
	.string "But Team Galactic seems to be\n"
	.string "studying that power's potential.\p"
	.string "They want to know if it can be used\n"
	.string "as energy for something...$"

JubilifeCity_Text_RowanCollectAllBadges:
	.string "Rowan: It's all over, so you can\n"
	.string "relax now.\p"
	.string "Thanks to you, nothing came of\n"
	.string "that situation. I appreciate that.\p"
	.string "Kudos to you for your battling\n"
	.string "skill. It got me thinking.\p"
	.string "Why don't you collect all the Gym\n"
	.string "Badges of Sinnoh?\p"
	.string "Doing so, you will be sure to\n"
	.string "encounter lots of Pokémon.\p"
	.string "Take care now.$"
