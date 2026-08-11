ValleyWindworks_MapScripts::
	.byte 0

ValleyWindworks_EventScript_Worker1::
	lock
	faceplayer
	goto_if_set FLAG_GALACTICA_WINDWORKS, ValleyWindworks_EventScript_Worker1Freed
	msgbox ValleyWindworks_Text_Worker1, MSGBOX_DEFAULT
	release
	end

ValleyWindworks_EventScript_Worker1Freed::
	msgbox ValleyWindworks_Text_Worker1Freed, MSGBOX_DEFAULT
	release
	end

ValleyWindworks_EventScript_Worker2::
	msgbox ValleyWindworks_Text_Worker2, MSGBOX_NPC
	end

ValleyWindworks_EventScript_Sign::
	msgbox ValleyWindworks_Text_Sign, MSGBOX_SIGN
	end

ValleyWindworks_Text_Worker1:
	.string "These turbines keep the lights on\n"
	.string "for half of Sinnoh.$"

ValleyWindworks_Text_Worker2:
	.string "Careful around the blades, trainer.\n"
	.string "The wind out here doesn't quit.$"

ValleyWindworks_Text_Sign:
	.string "VALLEY WINDWORKS\n"
	.string "Sinnoh's Clean Energy Plant$"

@ ---------------------------------------------------------------------------
@ Historia: a usina tomada pela Equipe Galactica, e a Comandante Mars.
@ Texto de pret/pokeplatinum, res/text/valley_windworks_outside.json e
@ valley_windworks_building.json. O interior da usina NAO existe neste hack, entao
@ a cena inteira acontece do lado de fora: Mars fica na porta, no lugar da sala de
@ controle. Vencer Mars liga FLAG_GALACTICA_WINDWORKS e some com os tres.

ValleyWindworks_EventScript_GalacticGrunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_VALLEY_WINDWORKS_2, ValleyWindworks_Text_GruntIntro, ValleyWindworks_Text_GruntDefeat
	msgbox ValleyWindworks_Text_GruntPostBattle, MSGBOX_AUTOCLOSE
	end

ValleyWindworks_EventScript_GalacticGrunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_VALLEY_WINDWORKS_3, ValleyWindworks_Text_Grunt2Intro, ValleyWindworks_Text_Grunt2Defeat
	msgbox ValleyWindworks_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

ValleyWindworks_EventScript_Mars::
	trainerbattle_single TRAINER_SINNOH_COMMANDER_MARS_VALLEY_WINDWORKS, ValleyWindworks_Text_MarsIntro, ValleyWindworks_Text_MarsDefeat, ValleyWindworks_EventScript_MarsDefeated
	msgbox ValleyWindworks_Text_MarsLeaving, MSGBOX_AUTOCLOSE
	end

ValleyWindworks_EventScript_MarsDefeated::
	msgbox ValleyWindworks_Text_MarsLeaving, MSGBOX_DEFAULT
	removeobject LOCALID_VALLEY_WINDWORKS_GALACTIC_GRUNT_1
	removeobject LOCALID_VALLEY_WINDWORKS_GALACTIC_GRUNT_2
	removeobject LOCALID_VALLEY_WINDWORKS_MARS
	setflag FLAG_GALACTICA_WINDWORKS
	release
	end

ValleyWindworks_Text_GruntIntro:
	.string "Don't you dare go into the Valley\n"
	.string "Windworks.\p"
	.string "I got ordered to keep everyone out\n"
	.string "if they're not part of Team\l"
	.string "Galactic.\p"
	.string "You're giving me a look that makes\n"
	.string "me think you're gonna try to get in.\p"
	.string "OK, then.\n"
	.string "You'll have to battle me for it!$"

ValleyWindworks_Text_GruntDefeat:
	.string "Isn't that just great.\n"
	.string "Getting owned by some kid.$"

ValleyWindworks_Text_GruntPostBattle:
	.string "Humph! Just you wait!\n"
	.string "Our Commander will smoosh you!$"

ValleyWindworks_Text_Grunt2Intro:
	.string "The mission is proceeding without\n"
	.string "a hitch. The boss should be pleased.\p"
	.string "Everything is for everyone, and\n"
	.string "for the good of Team Galactic!$"

ValleyWindworks_Text_Grunt2Defeat:
	.string "My Pokémon can't battle anymore.$"

ValleyWindworks_Text_Grunt2PostBattle:
	.string "They're gonna take away my Pokémon\n"
	.string "for messing this one up...$"

ValleyWindworks_Text_MarsIntro:
	.string "I'm one of Team Galactic's three\n"
	.string "Commanders.\p"
	.string "...No, wait.\n"
	.string "That's one of four Commanders.\l"
	.string "My name is Mars!\p"
	.string "We've been trying to create a new\n"
	.string "world that's better than this one...\p"
	.string "But people have shown little\n"
	.string "understanding about what we do.\p"
	.string "You don't understand either, do you?\n"
	.string "It's a little saddening...\p"
	.string "So, let's have a battle to decide\n"
	.string "what we should do next.\p"
	.string "If I win, you leave.\p"
	.string "If you win, we, Team Galactic,\n"
	.string "will leave!$"

ValleyWindworks_Text_MarsDefeat:
	.string "Mars: Oops!\n"
	.string "I messed that one up!\p"
	.string "That's all right, though.\n"
	.string "I quite enjoyed our battle.$"

ValleyWindworks_Text_MarsLeaving:
	.string "Mars: We've collected plenty of\n"
	.string "electricity here.\p"
	.string "With the power we obtained, we can\n"
	.string "do something quite spectacular.\p"
	.string "I guess it's time to say good-bye\n"
	.string "and leave for the time being!$"

ValleyWindworks_Text_Worker1Freed:
	.string "Team Galactic...\p"
	.string "They were saying they had to gather\n"
	.string "Pokémon and energy no matter what.\p"
	.string "It was for creating a new universe,\n"
	.string "or so they claimed.\p"
	.string "Nothing they said made any sort of\n"
	.string "sense to me.\p"
	.string "I can't tell you how grateful I am\n"
	.string "for you saving me.\p"
	.string "I can finally see my little daughter\n"
	.string "again!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

ValleyWindworks_EventScript_Placa1::
	msgbox ValleyWindworks_Text_Placa1, MSGBOX_SIGN
	end

ValleyWindworks_Text_Placa1:
	.string "Valley Windworks\nEcological, Wind-Driven Energy$"

ValleyWindworks_EventScript_Placa2::
	msgbox ValleyWindworks_Text_Placa2, MSGBOX_SIGN
	end

ValleyWindworks_Text_Placa2:
	.string "It's locked from inside!$"
