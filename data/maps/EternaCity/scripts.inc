@ Textos vindos de pret/pokeplatinum (res/text/eterna_city.json), em ingles.
@ Grunt_M x3, Cynthia, Cyrus, Gardenia e o Rival ficaram de fora: dependem de
@ flag de historia (FLAG_HIDE_ETERNA_CITY_*), que este agente nao pode inventar.

EternaCity_MapScripts::
	.byte 0

EternaCity_EventScript_BreederM::
	msgbox EternaCity_Text_BreederM, MSGBOX_NPC
	end

EternaCity_EventScript_Expert::
	msgbox EternaCity_Text_Expert, MSGBOX_NPC
	end

EternaCity_EventScript_NinjaBoy::
	msgbox EternaCity_Text_NinjaBoy, MSGBOX_NPC
	end

EternaCity_EventScript_BreederF1::
	msgbox EternaCity_Text_BreederF1, MSGBOX_NPC
	end

EternaCity_EventScript_AceTrainer::
	msgbox EternaCity_Text_AceTrainer, MSGBOX_NPC
	end

EternaCity_EventScript_BreederF2::
	msgbox EternaCity_Text_BreederF2, MSGBOX_NPC
	end

EternaCity_EventScript_BugCatcher1::
	msgbox EternaCity_Text_BugCatcher1, MSGBOX_NPC
	end

EternaCity_EventScript_BugCatcher2::
	msgbox EternaCity_Text_BugCatcher2, MSGBOX_NPC
	end

EternaCity_EventScript_GalacticBuildingSign::
	msgbox EternaCity_Text_GalacticBuildingSign, MSGBOX_SIGN
	end

EternaCity_EventScript_GymSign::
	msgbox EternaCity_Text_GymSign, MSGBOX_SIGN
	end

EternaCity_Text_BreederM:
	.string "I raise POKéMON here in ETERNA\n"
	.string "CITY. Fresh air does them good.$"

EternaCity_Text_Expert:
	.string "ETERNA CITY is one of the oldest\n"
	.string "cities in SINNOH.$"

EternaCity_Text_NinjaBoy:
	.string "I've been training in secret around\n"
	.string "here. Don't tell anyone, okay?$"

EternaCity_Text_BreederF1:
	.string "Since that TEAM GALACTIC building\n"
	.string "went up, the city's atmosphere has\l"
	.string "gotten all creepy and tense.\p"
	.string "I don't know what those people are\n"
	.string "doing up in that place...$"

EternaCity_Text_AceTrainer:
	.string "I train here every day. This city\n"
	.string "has some tough Trainers around.$"

EternaCity_Text_BreederF2:
	.string "The POKéMON here are always so\n"
	.string "well cared for. It's a nice place\l"
	.string "to raise them.$"

EternaCity_Text_BugCatcher1:
	.string "My friend said TEAM GALACTIC took\n"
	.string "his favorite POKéMON away. I don't\l"
	.string "think he's telling the truth.\p"
	.string "TEAM GALACTIC looks so cool. They\n"
	.string "don't look like common thugs.$"

EternaCity_Text_BugCatcher2:
	.string "Oh, wow! You got a Bicycle! You can\n"
	.string "ride down CYCLING ROAD and end up\l"
	.string "in HEARTHOME CITY.\p"
	.string "It's a fast and fun ride. You\n"
	.string "should check it out!$"

EternaCity_Text_GalacticBuildingSign:
	.string "TEAM GALACTIC ETERNA BUILDING$"

EternaCity_Text_GymSign:
	.string "ETERNA CITY POKéMON GYM\n"
	.string "Leader: GARDENIA\p"
	.string "The Grass-Type Endurance Style!$"

@ ---------------------------------------------------------------------------
@ Historia: a Equipe Galactica instalada em Eterna.
@ Texto de pret/pokeplatinum, res/text/eterna_city.json. O predio deles
@ (team_galactic_eterna_building_*) NAO existe neste hack, entao a porta continua
@ fechada e os grunts ficam do lado de fora, que e o que explica a porta fechada.
@ Sem flag e sem var: sao treinadores comuns, o jogo ja lembra quem foi derrotado.

EternaCity_EventScript_GalacticGrunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_1F_1, EternaCity_Text_Grunt1Intro, EternaCity_Text_Grunt1Defeat
	msgbox EternaCity_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

EternaCity_EventScript_GalacticGrunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_TEAM_GALACTIC_ETERNA_BUILDING_1F_2, EternaCity_Text_Grunt2Intro, EternaCity_Text_Grunt2Defeat
	msgbox EternaCity_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

EternaCity_EventScript_GalacticGrunt3::
	msgbox EternaCity_Text_Grunt3, MSGBOX_NPC
	end

EternaCity_Text_Grunt1Intro:
	.string "Hey! You there, kid!\n"
	.string "Stay away from that Pokémon statue!\p"
	.string "Team Galactic is conducting an\n"
	.string "official investigation here!$"

EternaCity_Text_Grunt1Defeat:
	.string "You're no ordinary kid...$"

EternaCity_Text_Grunt1PostBattle:
	.string "Our Commander Jupiter is up in the\n"
	.string "building. You'll never get past\l"
	.string "that door.$"

EternaCity_Text_Grunt2Intro:
	.string "Have you seen our building?\p"
	.string "Team Galactic is so stinking rich\n"
	.string "that we can have one built\l"
	.string "instantly!$"

EternaCity_Text_Grunt2Defeat:
	.string "You're going to regret this!$"

EternaCity_Text_Grunt2PostBattle:
	.string "Team Galactic is going to do\n"
	.string "something huge for everyone's sake.\p"
	.string "That's why you should keep out of\n"
	.string "Team Galactic's way.$"

EternaCity_Text_Grunt3:
	.string "Don't come whining about poor\n"
	.string "Pokémon and other trivial junk\l"
	.string "like that.\p"
	.string "And don't waste your time coming\n"
	.string "to our HQ in Veilstone.$"
