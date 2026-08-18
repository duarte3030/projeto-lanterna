@ SandgemTown_RowanLab = LABORATORIO DE POKEMON DO PROFESSOR ROWAN.
@ Mapa proprio desde 05/08/2026; antes dividia SandgemTown_House1 com uma casa, e
@ as duas portas de Sandgem caiam no mesmo interior. Reusa o layout do laboratorio
@ do Birch (LAYOUT_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB), sem arte nova.
@
@ Falas: pret/pokeplatinum, res/text/route_201.json e
@ res/text/sandgem_town_pokemon_research_lab.json. As UNICAS linhas que nao vem
@ do Platinum sao os dois avisos mecanicos (a pergunta sim/nao de cada Poke Bola
@ e a linha de "recebeu"), porque no Platinum quem escolhe e uma tela de menu
@ que este mapa nao tem.

@ Depois que o jogador ja pegou O INICIAL DE SINNOH, as tres bolas somem. Quem
@ faz isso e o campo "flag" das tres no map.json, apontado para
@ FLAG_INICIAL_SINNOH: o objeto nem chega a nascer com a flag ligada.
@
@ A flag era FLAG_SYS_POKEMON_GET ate 05/08/2026. Com a ordem cronologica
@ (decisao 66) quem acende essa flag e o Oak, em Kanto, muito antes de o jogador
@ chegar a Sinnoh: as tres bolas do ROWAN deixavam de nascer e a quarta regiao
@ nao entregava trio nenhum. Cada laboratorio passa a ter a flag da SUA regiao,
@ ver o bloco "Trio de iniciais por regiao" em include/constants/flags.h.
@
@ VAR_STARTER_MON: escrita aqui, 0=TURTWIG, 1=CHIMCHAR, 2=PIPLUP (grama, fogo,
@ agua, a mesma ordem de Hoenn). Sem ela nenhum rival monta time por triangulo
@ de tipos, e foi por causa dessa falta que o time do SILVER, em Johto, teve que
@ ser fixo (ver o cabecalho de data/maps/CherrygroveCity/scripts.inc).
SandgemTown_RowanLab_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SandgemTown_RowanLab_OnTransition
	.byte 0

SandgemTown_RowanLab_OnTransition::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, SandgemTown_RowanLab_SetCounterpartFemale
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	end

SandgemTown_RowanLab_SetCounterpartFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	end

@ >>> ESTRADA SUL DE SUNYSHORE: o escritor que faltava (18/08/2026) >>>
@ O Collector do ValorLakefront tranca a estrada sul da Route 222 e NINGUEM
@ escrevia VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE, entao o bloqueio era eterno
@ (dito em data/maps/ValorLakefront/scripts.inc e no PLANO-OBRAS-SINNOH).
@
@ NA FONTE quem desarma e `SandgemTownLab_ObtainSunyshoresBadge`
@ (res/field/scripts/scripts_sandgem_town_pokemon_research_lab.s:108-118), e o
@ que o CHAMA e `SandgemTownLab_OnFrame_ReturnedFromDistortionWorld`: a volta do
@ Mundo Distorcido, depois do Spear Pillar. As duas linhas que interessam sao
@ `SetFlag FLAG_HIDE_VALOR_LAKEFRONT_COLLECTOR` e
@ `SetVar VAR_VALOR_LAKEFRONT_BLOCK_SUNYSHORE_STATE, 1`, e sao os UNICOS toques
@ nessa flag e nessa var no pokeplatinum inteiro.
@
@ POR QUE O GATILHO AQUI E OUTRO, e por que este e o mais fiel que existe: o
@ Mundo Distorcido e o climax do Spear Pillar NAO estao portados (ESTADO 0.e,
@ "fora desta obra"). O ultimo passo do arco da Galactica que ESTA na ROM e a
@ queda do Saturn, que acende FLAG_GALACTICA_QG_TOMADO
@ (data/maps/GalacticHQ_1F/scripts.inc:203 e _2F:191), e na fonte ela fica
@ exatamente ANTES do Coronet/Spear Pillar/Distorcido. O texto da fonte
@ concorda com esse ponto da historia: "You've got seven already! That only
@ leaves Sunyshore's Gym" e "the three Pokemon of the lakes appear to have
@ returned to their homes" (res/text/sandgem_town_pokemon_research_lab.json,
@ SandgemTownLab_Text_ObtainSunyshoresBadge). Ou seja: um passo antes do da
@ fonte, e nunca antes da hora.
@
@ ponytail: la a cena e um ON_FRAME com o companheiro e duas telas de fala; aqui
@ ela e a CONVERSA com o Rowan, que e o mesmo ator dizendo as mesmas linhas, sem
@ tabela de frame nem var de estado nova (a janela de save esta fechada). Quem
@ marca "ja aconteceu" e a PROPRIA flag que a cena acende,
@ FLAG_SINNOH_ESCONDE_VALOR_LAKEFRONT_COLLECTOR: zero flag nova, zero var nova.
SandgemTown_RowanLab_EventScript_Rowan::
	lock
	faceplayer
	goto_if_set FLAG_SINNOH_ESCONDE_VALOR_LAKEFRONT_COLLECTOR, SandgemTown_RowanLab_EventScript_RowanAfter
	goto_if_set FLAG_GALACTICA_QG_TOMADO, SandgemTown_RowanLab_EventScript_RowanAbreSunyshore
	goto_if_set FLAG_INICIAL_SINNOH, SandgemTown_RowanLab_EventScript_RowanAfter
	msgbox SandgemTown_RowanLab_Text_RowanEntrust, MSGBOX_DEFAULT
	release
	end

SandgemTown_RowanLab_EventScript_RowanAbreSunyshore::
	msgbox SandgemTown_RowanLab_Text_RowanObtainSunyshoresBadge, MSGBOX_DEFAULT
	setflag FLAG_SINNOH_ESCONDE_VALOR_LAKEFRONT_COLLECTOR
	setvar VAR_SINNOH_VALOR_BLOQUEIO_SUNYSHORE, 1
	release
	end

@ Fala do pokeplatinum, res/text/sandgem_town_pokemon_research_lab.json,
@ SandgemTownLab_Text_ObtainSunyshoresBadge. Fora as duas contagens que a fonte
@ monta com STRVAR (quantos Pokemon vistos e quantas insignias), que aqui
@ virariam numero inventado.
SandgemTown_RowanLab_Text_RowanObtainSunyshoresBadge:
	.string "ROWAN: Oh, yes, there was something\n"
	.string "I had to tell you.\p"
	.string "The three POKéMON of the lakes appear\n"
	.string "to have returned to their homes.\p"
	.string "And the road along LAKE VALOR is\n"
	.string "open again.\p"
	.string "Hm! You've come this far.\n"
	.string "Why not obtain SUNYSHORE's BADGE?\p"
	.string "And why not challenge the POKéMON\n"
	.string "LEAGUE?$"
@ <<< ESTRADA SUL DE SUNYSHORE <<<

SandgemTown_RowanLab_EventScript_RowanAfter::
	msgbox SandgemTown_RowanLab_Text_RowanAdventureAwaits, MSGBOX_DEFAULT
	release
	end

SandgemTown_RowanLab_EventScript_Rival::
	lock
	faceplayer
	goto_if_set FLAG_INICIAL_SINNOH, SandgemTown_RowanLab_EventScript_RivalAfter
	msgbox SandgemTown_RowanLab_Text_RivalYouChooseFirst, MSGBOX_DEFAULT
	release
	end

SandgemTown_RowanLab_EventScript_RivalAfter::
	msgbox SandgemTown_RowanLab_Text_RivalOnlyOneThingToDo, MSGBOX_DEFAULT
	release
	end

SandgemTown_RowanLab_EventScript_Assistant::
	msgbox SandgemTown_RowanLab_Text_Assistant, MSGBOX_NPC
	end

SandgemTown_RowanLab_EventScript_Bookshelf::
	msgbox SandgemTown_RowanLab_Text_Bookshelf, MSGBOX_SIGN
	end

SandgemTown_RowanLab_EventScript_BallTurtwig::
	lock
	faceplayer
	showmonpic SPECIES_TURTWIG, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_TURTWIG
	msgbox SandgemTown_RowanLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandgemTown_RowanLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_TURTWIG, 55
	setvar VAR_STARTER_MON, 0
	goto SandgemTown_RowanLab_EventScript_ChoseStarter

SandgemTown_RowanLab_EventScript_BallChimchar::
	lock
	faceplayer
	showmonpic SPECIES_CHIMCHAR, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_CHIMCHAR
	msgbox SandgemTown_RowanLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandgemTown_RowanLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_CHIMCHAR, 55
	setvar VAR_STARTER_MON, 1
	goto SandgemTown_RowanLab_EventScript_ChoseStarter

SandgemTown_RowanLab_EventScript_BallPiplup::
	lock
	faceplayer
	showmonpic SPECIES_PIPLUP, 10, 3
	bufferspeciesname STR_VAR_1, SPECIES_PIPLUP
	msgbox SandgemTown_RowanLab_Text_WillYouTakeThisOne, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandgemTown_RowanLab_EventScript_DeclinedStarter
	hidemonpic
	givemon SPECIES_PIPLUP, 55
	setvar VAR_STARTER_MON, 2
	goto SandgemTown_RowanLab_EventScript_ChoseStarter

SandgemTown_RowanLab_EventScript_DeclinedStarter::
	hidemonpic
	release
	end

SandgemTown_RowanLab_EventScript_ChoseStarter::
	setflag FLAG_INICIAL_SINNOH
	setflag FLAG_SYS_POKEMON_GET
	message SandgemTown_RowanLab_Text_ReceivedStarter
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox gText_NicknameThisPokemon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, SandgemTown_RowanLab_EventScript_AfterStarter
	setvar VAR_0x8004, 0
	call Common_EventScript_NameReceivedPartyMon
	goto SandgemTown_RowanLab_EventScript_AfterStarter

SandgemTown_RowanLab_EventScript_AfterStarter::
	removeobject LOCALID_ROWAN_LAB_BALL_TURTWIG
	removeobject LOCALID_ROWAN_LAB_BALL_CHIMCHAR
	removeobject LOCALID_ROWAN_LAB_BALL_PIPLUP
	msgbox SandgemTown_RowanLab_Text_RivalPicksHis, MSGBOX_DEFAULT
	msgbox SandgemTown_RowanLab_Text_RowanHopeYoullDoWell, MSGBOX_DEFAULT
	msgbox SandgemTown_RowanLab_Text_RowanRecordData, MSGBOX_DEFAULT
	setflag FLAG_SYS_POKEDEX_GET
	message SandgemTown_RowanLab_Text_ObtainedPokedex
	waitmessage
	playfanfare MUS_OBTAIN_ITEM
	waitfanfare
	msgbox SandgemTown_RowanLab_Text_RowanGrandAdventure, MSGBOX_DEFAULT
	clearflag FLAG_SINNOH_ESCONDE_SANDGEM_TOWN_LAB_PROF_OAK
	clearflag FLAG_SINNOH_ESCONDE_SANDGEM_TOWN_LAB_COUNTERPART
	addobject LOCALID_ROWAN_LAB_OAK
	addobject LOCALID_ROWAN_LAB_COUNTERPART
	msgbox SandgemTown_RowanLab_Text_OakCongratulations, MSGBOX_DEFAULT
	release
	end

@ FLAG_HIDE_SANDGEM_TOWN_LAB_PROF_OAK/_COUNTERPART (fonte: dois bystanders
@ perto da saida do laboratorio na fonte, mesma coordenada). ponytail: na
@ fonte OAK aparece por VIDEOFONE ligando para o ROWAN parabenizando pelo
@ quarto Pokedex regional; sem tela de chamada aqui, ele entra como visita
@ fisica de verdade, mesmo gancho de continuidade (Oak ja existe em Kanto
@ neste ROM). Somem revelados junto do Pokedex e ficam visiveis dali para
@ frente, mesmo padrao do ROWAN e do RIVAL desta sala (nao voltam a esconder).
SandgemTown_RowanLab_EventScript_Oak::
	lock
	faceplayer
	msgbox SandgemTown_RowanLab_Text_OakTalk, MSGBOX_DEFAULT
	release
	end

SandgemTown_RowanLab_EventScript_Counterpart::
	lock
	faceplayer
	msgbox SandgemTown_RowanLab_Text_CounterpartTalk, MSGBOX_DEFAULT
	release
	end

SandgemTown_RowanLab_Text_OakCongratulations:
	.string "???: Rowan! Is that a new Trainer\n"
	.string "getting their first Pokémon?\p"
	.string "ROWAN: Oak! I didn't expect you all\n"
	.string "the way out here.\p"
	.string "OAK: Congratulations on the region's\n"
	.string "fourth Pokédex partnership!$"

SandgemTown_RowanLab_Text_OakTalk:
	.string "OAK: I study Pokémon back in Kanto.\n"
	.string "Rowan and I go a long way back.$"

SandgemTown_RowanLab_Text_CounterpartTalk:
	.string "So you got your Pokémon too!\n"
	.string "Good luck out there.$"

SandgemTown_RowanLab_Text_RowanEntrust:
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

SandgemTown_RowanLab_Text_RowanAdventureAwaits:
	.string "ROWAN: Go on!\p"
	.string "{PLAYER}, your grand adventure\n"
	.string "awaits you!$"

@ Aviso mecanico, nao e fala do Platinum: no jogo original a escolha e uma tela.
SandgemTown_RowanLab_Text_WillYouTakeThisOne:
	.string "Inside the briefcase is a\n"
	.string "{STR_VAR_1}.\p"
	.string "Will you take this one?$"

@ Aviso mecanico, nao e fala do Platinum.
SandgemTown_RowanLab_Text_ReceivedStarter:
	.string "{PLAYER} received the\n"
	.string "{STR_VAR_1}!$"

SandgemTown_RowanLab_Text_RivalYouChooseFirst:
	.string "Hey, {PLAYER}.\n"
	.string "You can choose first.\p"
	.string "Hey, I'm practically a grown-up.\n"
	.string "I have to show some class here.$"

SandgemTown_RowanLab_Text_RivalPicksHis:
	.string "Then, I choose you!\n"
	.string "I'm picking this one!$"

SandgemTown_RowanLab_Text_RivalOnlyOneThingToDo:
	.string "Heheh, {PLAYER}!\n"
	.string "We've both got POKéMON now.\p"
	.string "There's only one thing to do,\n"
	.string "right?$"

SandgemTown_RowanLab_Text_RowanHopeYoullDoWell:
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

SandgemTown_RowanLab_Text_RowanRecordData:
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

SandgemTown_RowanLab_Text_ObtainedPokedex:
	.string "{PLAYER} obtained\n"
	.string "the POKéDEX!$"

SandgemTown_RowanLab_Text_RowanGrandAdventure:
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

SandgemTown_RowanLab_Text_Assistant:
	.string "PROFESSOR ROWAN invented a new\n"
	.string "POKéDEX while working alongside a\l"
	.string "professor from the KANTO region.\p"
	.string "Oh, my name is ROSEANNE.\p"
	.string "It's an honor to be an assistant\n"
	.string "to our professor!$"

SandgemTown_RowanLab_Text_Bookshelf:
	.string "It's crammed full of books with\n"
	.string "all sorts of POKéMON information.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SandgemTown_RowanLab_EventScript_Npc1::
	msgbox SandgemTown_RowanLab_Text_Npc1, MSGBOX_NPC
	end

SandgemTown_RowanLab_Text_Npc1:
	.string "Professor Rowan invented a new\nPokédex while working alongside a\pprofessor from the Kanto region.\pOh, my name is Roseanne.\pIt's an honor to be an assistant to\nour professor!$"
