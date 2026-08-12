@ Textos vindos de pret/pokeplatinum (res/text/eterna_city.json), em ingles.
@ Grunt_M x3, Cynthia, Cyrus, Gardenia e o Rival ficaram de fora: dependem de
@ flag de historia (FLAG_HIDE_ETERNA_CITY_*), que este agente nao pode inventar.

EternaCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EternaCity_OnTransition
	.byte 0

@ ponytail: os tres grunts da rua somem depois da Jupiter, igual Jubilife faz com
@ FLAG_GALACTICA_JUBILIFE. A cena da Jupiter mora em outro mapa (o 4F do predio),
@ que nao e desta tarefa, entao quem liga a flag e este ON_TRANSITION: ele le a
@ flag de derrota que o jogo ja grava e traduz para FLAG_GALACTICA_ETERNA, que e
@ o campo "flag" dos tres objetos. Zero var.
EternaCity_OnTransition:
	call_if_defeated TRAINER_SINNOH_COMMANDER_JUPITER_ETERNA_BUILDING, EternaCity_EventScript_HideGalacticGrunts
	end

EternaCity_EventScript_HideGalacticGrunts::
	setflag FLAG_GALACTICA_ETERNA
	return

EternaCity_EventScript_BreederF1::
	msgbox EternaCity_Text_BreederF1, MSGBOX_NPC
	end

EternaCity_EventScript_BreederF2::
	msgbox EternaCity_Text_BreederF2, MSGBOX_NPC
	end

EternaCity_EventScript_GalacticBuildingSign::
	msgbox EternaCity_Text_GalacticBuildingSign, MSGBOX_SIGN
	end

EternaCity_EventScript_GymSign::
	msgbox EternaCity_Text_GymSign, MSGBOX_SIGN
	end

EternaCity_Text_BreederF1:
	.string "Since that TEAM GALACTIC building\n"
	.string "went up, the city's atmosphere has\l"
	.string "gotten all creepy and tense.\p"
	.string "I don't know what those people are\n"
	.string "doing up in that place...$"

EternaCity_Text_BreederF2:
	.string "The POKéMON here are always so\n"
	.string "well cared for. It's a nice place\l"
	.string "to raise them.$"

EternaCity_Text_GalacticBuildingSign:
	.string "TEAM GALACTIC ETERNA BUILDING$"

EternaCity_Text_GymSign:
	.string "ETERNA CITY POKéMON GYM\n"
	.string "Leader: GARDENIA\p"
	.string "The Grass-Type Endurance Style!$"

@ ---------------------------------------------------------------------------
@ Historia: a Equipe Galactica instalada em Eterna.
@ Texto de pret/pokeplatinum, res/text/eterna_city.json. O predio deles agora
@ EXISTE: a porta (27,8) leva a MAP_TEAM_GALACTIC_ETERNA_BUILDING_1F, e os quatro
@ andares terminam na Comandante Jupiter. Estes tres grunts continuam na rua e
@ foram remanejados para perto da porta.
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

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

EternaCity_EventScript_Placa1::
	msgbox EternaCity_Text_Placa1, MSGBOX_SIGN
	end

EternaCity_Text_Placa1:
	.string "Eterna City Pokémon Gym\nLeader: Gardenia\pMaster of Vivid Plant Pokémon!$"

EternaCity_EventScript_Placa2::
	msgbox EternaCity_Text_Placa2, MSGBOX_SIGN
	end

EternaCity_Text_Placa2:
	.string "Rad Rickshaw's Cycle Shop\nGet On and Ride!$"

EternaCity_EventScript_Placa4::
	msgbox EternaCity_Text_Placa4, MSGBOX_SIGN
	end

EternaCity_Text_Placa4:
	.string "Team Galactic Eterna Building\nWe Want Your Pokémon!$"

EternaCity_EventScript_Placa6::
	msgbox EternaCity_Text_Placa6, MSGBOX_SIGN
	end

EternaCity_Text_Placa6:
	.string "Underground Man's House\nGoin' Down for Adventure!$"

EternaCity_EventScript_Placa7::
	msgbox EternaCity_Text_Placa7, MSGBOX_SIGN
	end

EternaCity_Text_Placa7:
	.string "Eterna Condominiums\nName-Rating Services Available$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

EternaCity_EventScript_Npc1::
	msgbox EternaCity_Text_Npc1, MSGBOX_NPC
	end

EternaCity_Text_Npc1:
	.string "If you're visiting Eterna, you need to\nget yourself a Bicycle and take a\pride down the Cycling Road.$"

EternaCity_EventScript_Npc2::
	msgbox EternaCity_Text_Npc2, MSGBOX_NPC
	end

EternaCity_Text_Npc2:
	.string "Eterna City's not anything like it\nwas before, way back in the day.$"

EternaCity_EventScript_Npc3::
	msgbox EternaCity_Text_Npc3, MSGBOX_NPC
	end

EternaCity_Text_Npc3:
	.string "They say this is an awesome Pokémon\nthat people saw long ago.$"

EternaCity_EventScript_Npc4::
	msgbox EternaCity_Text_Npc4, MSGBOX_NPC
	end

EternaCity_Text_Npc4:
	.string "Since that Team Galactic building went\nup, the city's atmosphere has gotten\pall creepy and tense.\pI don't know what those people are\ndoing up in that place...$"

EternaCity_EventScript_Npc5::
	msgbox EternaCity_Text_Npc5, MSGBOX_NPC
	end

EternaCity_Text_Npc5:
	.string "They say this is an old city.\pIt doesn't look it, though.\nNot with all these tall buildings.$"

EternaCity_EventScript_Npc6::
	msgbox EternaCity_Text_Npc6, MSGBOX_NPC
	end

EternaCity_Text_Npc6:
	.string "My friend said Team Galactic took his\nfavorite Pokémon away.\pI don't think he's telling the truth.\nTeam Galactic looks so cool.\pThey don't look like common thugs.$"

EternaCity_EventScript_Npc7::
	msgbox EternaCity_Text_Npc7, MSGBOX_NPC
	end

EternaCity_Text_Npc7:
	.string "Oh, don't tell me you don't have\nan Explorer Kit?\pYou should have a word with the man\nnext door to the Pokémon Center.$"

EternaCity_EventScript_Npc8::
	msgbox EternaCity_Text_Npc8, MSGBOX_NPC
	end

EternaCity_Text_Npc8:
	.string "Oh, wow!\nYou got a Bicycle!\pYou can ride down Cycling Road\nand end up in Hearthome City.\pIt's a fast and fun ride.\nYou should check it out!$"

EternaCity_EventScript_Placa9::
	msgbox EternaCity_Text_Placa9, MSGBOX_SIGN
	end

EternaCity_Text_Placa9:
	.string "Eterna City\nHistory Living$"

EternaCity_EventScript_Placa10::
	msgbox EternaCity_Text_Placa10, MSGBOX_SIGN
	end

EternaCity_Text_Placa10:
	.string "Eterna City\nHistory Living$"

EternaCity_EventScript_Placa11::
	msgbox EternaCity_Text_Placa11, MSGBOX_SIGN
	end

EternaCity_Text_Placa11:
	.string "It's Eterna City's Pokémon statue.\pThere seems to have been a descriptive\nplate, but it appears it was torn off.$"
