@ SandgemTown_House1 = LABORATORIO DE POKEMON DO PROFESSOR ROWAN.
@ Sinnoh nao ganhou mapa proprio de laboratorio: layouts.json e map_groups.json
@ estavam com outro agente. Ver PENDENCIAS-INTRO.md, item 1.
@
@ Falas: pret/pokeplatinum, res/text/route_201.json e
@ res/text/sandgem_town_pokemon_research_lab.json. As UNICAS linhas que nao vem
@ do Platinum sao os dois avisos mecanicos (a pergunta sim/nao de cada Poke Bola
@ e a linha de "recebeu"), porque no Platinum quem escolhe e uma tela de menu
@ que este mapa nao tem.

@ Depois que o jogador ja tem inicial, as tres bolas somem. Quem faz isso e o
@ campo "flag" das tres no map.json, apontado para FLAG_SYS_POKEMON_GET: o
@ objeto nem chega a nascer com a flag ligada. Nao foi preciso criar flag nem
@ var, e nao ha script ON_TRANSITION (removeobject nao persiste sozinho).
SandgemTown_House1_MapScripts::
	.byte 0

SandgemTown_House1_EventScript_Rowan::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEMON_GET, SandgemTown_House1_EventScript_RowanAfter
	msgbox SandgemTown_House1_Text_RowanEntrust, MSGBOX_DEFAULT
	release
	end

SandgemTown_House1_EventScript_RowanAfter::
	msgbox SandgemTown_House1_Text_RowanAdventureAwaits, MSGBOX_DEFAULT
	release
	end

SandgemTown_House1_EventScript_Rival::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEMON_GET, SandgemTown_House1_EventScript_RivalAfter
	msgbox SandgemTown_House1_Text_RivalYouChooseFirst, MSGBOX_DEFAULT
	release
	end

SandgemTown_House1_EventScript_RivalAfter::
	msgbox SandgemTown_House1_Text_RivalOnlyOneThingToDo, MSGBOX_DEFAULT
	release
	end

SandgemTown_House1_EventScript_Assistant::
	msgbox SandgemTown_House1_Text_Assistant, MSGBOX_NPC
	end

SandgemTown_House1_EventScript_Bookshelf::
	msgbox SandgemTown_House1_Text_Bookshelf, MSGBOX_SIGN
	end

SandgemTown_House1_EventScript_BallTurtwig::
	lock
	faceplayer
	showmonpic SPECIES_TURTWIG, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_TURTWIG
	msgbox SandgemTown_House1_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandgemTown_House1_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_TURTWIG, 5
	goto SandgemTown_House1_EventScript_ChoseStarter

SandgemTown_House1_EventScript_BallChimchar::
	lock
	faceplayer
	showmonpic SPECIES_CHIMCHAR, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_CHIMCHAR
	msgbox SandgemTown_House1_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandgemTown_House1_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_CHIMCHAR, 5
	goto SandgemTown_House1_EventScript_ChoseStarter

SandgemTown_House1_EventScript_BallPiplup::
	lock
	faceplayer
	showmonpic SPECIES_PIPLUP, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_PIPLUP
	msgbox SandgemTown_House1_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandgemTown_House1_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_PIPLUP, 5
	goto SandgemTown_House1_EventScript_ChoseStarter

SandgemTown_House1_EventScript_DeclinedStarter::
	hidemonpic
	release
	end

SandgemTown_House1_EventScript_ChoseStarter::
	setflag FLAG_SYS_POKEMON_GET
	message SandgemTown_House1_Text_ReceivedStarter
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandgemTown_House1_EventScript_AfterStarter
	setvar VAR_0x8004, 0
	call Common_EventScript_NameReceivedPartyMon
	goto SandgemTown_House1_EventScript_AfterStarter

SandgemTown_House1_EventScript_AfterStarter::
	removeobject LOCALID_ROWAN_LAB_BALL_TURTWIG
	removeobject LOCALID_ROWAN_LAB_BALL_CHIMCHAR
	removeobject LOCALID_ROWAN_LAB_BALL_PIPLUP
	msgbox SandgemTown_House1_Text_RivalPicksHis, MSGBOX_DEFAULT
	msgbox SandgemTown_House1_Text_RowanHopeYoullDoWell, MSGBOX_DEFAULT
	msgbox SandgemTown_House1_Text_RowanRecordData, MSGBOX_DEFAULT
	setflag FLAG_SYS_POKEDEX_GET
	message SandgemTown_House1_Text_ObtainedPokedex
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox SandgemTown_House1_Text_RowanGrandAdventure, MSGBOX_DEFAULT
	release
	end

SandgemTown_House1_Text_RowanEntrust:
	.string "ROWAN: We exist side by side with\n"
	.string "POKéMON.\p"
	.string "There comes a time when people\n"
	.string "should meet POKéMON.\p"
	.string "There is a world that should be\n"
	.string "explored together.\p"
	.string "For you, today is that time.\n"
	.string "The place, right here.\p"
	.string "Go on! Open the briefcase and\n"
	.string "choose a POKéMON!$"

SandgemTown_House1_Text_RowanAdventureAwaits:
	.string "ROWAN: Go on!\p"
	.string "{PLAYER}, your grand adventure\n"
	.string "awaits you!$"

@ Aviso mecanico, nao e fala do Platinum: no jogo original a escolha e uma tela.
SandgemTown_House1_Text_WillYouTakeThisOne:
	.string "Inside the briefcase is a\n"
	.string "{STR_VAR_1}.\p"
	.string "Will you take this one?$"

@ Aviso mecanico, nao e fala do Platinum.
SandgemTown_House1_Text_ReceivedStarter:
	.string "{PLAYER} received the\n"
	.string "{STR_VAR_1}!$"

SandgemTown_House1_Text_RivalYouChooseFirst:
	.string "Hey, {PLAYER}.\n"
	.string "You can choose first.\p"
	.string "Hey, I'm practically a grown-up.\n"
	.string "I have to show some class here.$"

SandgemTown_House1_Text_RivalPicksHis:
	.string "Then, I choose you!\n"
	.string "I'm picking this one!$"

SandgemTown_House1_Text_RivalOnlyOneThingToDo:
	.string "Heheh, {PLAYER}!\n"
	.string "We've both got POKéMON now.\p"
	.string "There's only one thing to do,\n"
	.string "right?$"

SandgemTown_House1_Text_RowanHopeYoullDoWell:
	.string "ROWAN: Very well! Both of you have\n"
	.string "chosen a good POKéMON, it seems.\p"
	.string "Now, listen well!\p"
	.string "The POKéMON you have been\n"
	.string "entrusted with are unfamiliar with\l"
	.string "the world.\p"
	.string "In that regard, they're much\n"
	.string "like you.\p"
	.string "As fellow newcomers to the world,\n"
	.string "I hope you'll do well together.$"

SandgemTown_House1_Text_RowanRecordData:
	.string "ROWAN: Er-hem!\p"
	.string "Let's move on to the main topic.\p"
	.string "There is something I want you to\n"
	.string "do for me.\p"
	.string "First of all, I want to know\n"
	.string "exactly what kinds of POKéMON\l"
	.string "live in the SINNOH region.\p"
	.string "To do so, it is necessary to\n"
	.string "collect data using the POKéDEX.\p"
	.string "This is what I wish to ask of you.$"

SandgemTown_House1_Text_ObtainedPokedex:
	.string "{PLAYER} obtained\n"
	.string "the POKéDEX!$"

SandgemTown_House1_Text_RowanGrandAdventure:
	.string "ROWAN: That POKéDEX is a very\n"
	.string "high-tech device.\p"
	.string "It will automatically record data\n"
	.string "on every kind of POKéMON you\l"
	.string "encounter.\p"
	.string "I've lived for 60 long years.\n"
	.string "Even now, I get a thrill when\l"
	.string "I'm with a POKéMON.\p"
	.string "Now go!\p"
	.string "{PLAYER}, your grand adventure\n"
	.string "begins right now!$"

SandgemTown_House1_Text_Assistant:
	.string "PROFESSOR ROWAN invented a new\n"
	.string "POKéDEX while working alongside a\l"
	.string "professor from the KANTO region.\p"
	.string "Oh, my name is ROSEANNE.\p"
	.string "It's an honor to be an assistant\n"
	.string "to our professor!$"

SandgemTown_House1_Text_Bookshelf:
	.string "It's crammed full of books with\n"
	.string "all sorts of POKéMON information.$"
