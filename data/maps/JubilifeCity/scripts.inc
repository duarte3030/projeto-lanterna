@ Mapa de referencia de Sinnoh. O padrao usado aqui vale para os outros 132:
@ ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever qualquer script novo.
@ Textos vindos de pret/pokeplatinum, em ingles, como o resto do jogo.

@ Contraparte (o rival de genero oposto ao do jogador) usa
@ OBJ_EVENT_GFX_VAR_0 no map.json, e QUEM USA VAR_0 SETA A VAR NO PROPRIO
@ ON_TRANSITION: assim o sprite nao depende do que outro mapa deixou na var
@ (ela mora no save, e VAR_OBJ_GFX_ID_0 e compartilhada por todo mundo).
@ Mesmo mecanismo de LakeVerity, SandgemTown e Route202, e os mesmos dois
@ sprites: escolher no meio da cena, como estava aqui, so acertava na
@ primeira vez e ainda usava OBJ_EVENT_GFX_PLAYER_M/F, que e o sprite do
@ jogador, nao o do rival.
JubilifeCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, JubilifeCity_OnTransition
	.byte 0

JubilifeCity_OnTransition::
	checkplayergender
	goto_if_eq VAR_RESULT, MALE, JubilifeCity_SetCounterpartFemale
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL
	end

JubilifeCity_SetCounterpartFemale::
	setvar VAR_OBJ_GFX_ID_0, OBJ_EVENT_GFX_RIVAL_MAY_NORMAL
	end

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ rotulo da fonte: JubilifeCity_CoordEvent_FirstArrival
@ Simplificacao anotada: a fonte manda o counterpart e o jogador andarem
@ juntos ate avistar o LOOKER (sem sprite aqui, ver comentario acima) e
@ depois ate a escola e de volta, tudo em ApplyMovement do JOGADOR por varios
@ tiles (risco de waitmovement travado sem map.bin conferido, mesma regra de
@ CianwoodCity_EventScript_SuicuneTrigger). Cortado: fica so o encontro com o
@ counterpart (saudacao + comentario do tamanho do time, conteudo real,
@ GetPartySize de verdade) e a mencao ao LOOKER de passagem, sem objeto nem
@ caminhada roteirizada. VS Recorder da fonte nao existe aqui (nenhum
@ ITEM_VS_RECORDER), caiu junto.
@ O sprite da contraparte sai do ON_TRANSITION deste mapa (topo do arquivo),
@ nao daqui.
JubilifeCity_EventScript_CoordEvent_FirstArrival::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_JUBILIFE_CITY_COUNTERPART
	addobject LOCALID_JUBILIFE_COUNTERPART
	applymovement LOCALID_JUBILIFE_COUNTERPART, JubilifeCity_Movement_CounterpartNoticePlayerFirstArrival
	waitmovement 0
	applymovement LOCALID_JUBILIFE_COUNTERPART, JubilifeCity_Movement_CounterpartWalkToPlayerFirstArrival
	waitmovement 0
	msgbox JubilifeCity_Text_CounterpartAreYouCatchingPokemon, MSGBOX_DEFAULT
	getpartysize
	compare VAR_RESULT, 4
	goto_if_ge JubilifeCity_EventScript_CounterpartAtLeastFour
	msgbox JubilifeCity_Text_CounterpartSaferIfYouCatchMore, MSGBOX_DEFAULT
	goto JubilifeCity_EventScript_FirstArrivalLookerMention

JubilifeCity_EventScript_CounterpartAtLeastFour::
	msgbox JubilifeCity_Text_CounterpartWowAlreadyGotXPokemon, MSGBOX_DEFAULT

JubilifeCity_EventScript_FirstArrivalLookerMention::
	msgbox JubilifeCity_Text_CounterpartMentionsLooker, MSGBOX_DEFAULT
	applymovement LOCALID_JUBILIFE_COUNTERPART, JubilifeCity_Movement_CounterpartLeaveFirstArrival
	waitmovement 0
	setflag FLAG_SINNOH_ESCONDE_JUBILIFE_CITY_COUNTERPART
	removeobject LOCALID_JUBILIFE_COUNTERPART
	setvar VAR_SINNOH_JUBILIFE_ESTADO, 1
	releaseall
	end

JubilifeCity_Movement_CounterpartNoticePlayerFirstArrival:
	emote_exclamation_mark
	step_end

JubilifeCity_Movement_CounterpartWalkToPlayerFirstArrival:
	walk_down
	walk_down
	walk_down
	step_end

JubilifeCity_Movement_CounterpartLeaveFirstArrival:
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

JubilifeCity_Text_CounterpartAreYouCatchingPokemon:
	.string "Hi, {PLAYER}! Are you catching\n"
	.string "Pokémon?$"

JubilifeCity_Text_CounterpartWowAlreadyGotXPokemon:
	.string "Wow! You've already got some\n"
	.string "Pokémon with you!\p"
	.string "At that pace, your Pokédex\n"
	.string "should be full in no time!$"

JubilifeCity_Text_CounterpartSaferIfYouCatchMore:
	.string "…Um…\p"
	.string "I think you'd feel a lot safer if\n"
	.string "you were to catch some more.$"

JubilifeCity_Text_CounterpartMentionsLooker:
	.string "By the way, keep an eye out. I saw\n"
	.string "a strange man in a coat asking\l"
	.string "around town about something.\p"
	.string "Anyway, I'll see you around!$"

@ rotulo da fonte: JubilifeCity_CoordEvent_LookerBlockRoute203
@ Na fonte o LOOKER (sem sprite aqui, ver NOMES_PROPRIOS em
@ dev_scripts/importa_npcs_sinnoh.py; nenhuma troca em TROCA_SPRITE) fecha
@ fisicamente a passagem para Route203 ate o jogador visitar a escola E
@ obter Poketch. Poketch nao existe (decisao 3). BLOQUEAR o caminho principal
@ por uma mecanica que nunca destrava travaria o jogo para sempre, entao a
@ trava NAO entra (prioridade de seguranca sobre fidelidade). "a fala fica"
@ (instrucao do plano): a fala sem o corpo do bloqueio, uma vez, sem NPC
@ visivel (sem sprite pra por na cena).
JubilifeCity_EventScript_CoordEvent_LookerBlockRoute203::
	lockall
	msgbox JubilifeCity_Text_HelloHaveYouVisitedTrainersSchool, MSGBOX_DEFAULT
	setvar VAR_SINNOH_JUBILIFE_ESTADO, 3
	releaseall
	end

@ rotulo da fonte: JubilifeCity_CoordEvent_LookerPalPad
@ O resto desta cena e Pal Pad/GTS puro (decisao 3, plano explicito: "o que
@ for de Pal Pad/GTS dentro dela e descartado com comentario, a fala fica").
@ Sem sprite do Looker (mesma nota acima) so a fala de despedida do
@ investigador entra, sem objeto.
JubilifeCity_EventScript_CoordEvent_LookerPalPad::
	lockall
	msgbox JubilifeCity_Text_TakeInvestigationElsewhere, MSGBOX_DEFAULT
	setvar VAR_SINNOH_JUBILIFE_LOOKER_ESTADO, 2
	releaseall
	end

@ rotulo da fonte: JubilifeCity_CoordEvent_TeamGalactic
@ CONFERIDO ANTES DE ESCREVER (regra da fila): esta cena, na fonte, e o
@ confronto dos 2 grunts com o Prof. Rowan na porta da escola, RESOLVIDO EM
@ TAG BATTLE com o counterpart. Ja existe versao completa e funcionando mais
@ abaixo neste arquivo (JubilifeCity_EventScript_Rowan/GalacticGrunt1/
@ GalacticGrunt2/GalacticRetreats, leva anterior S2): fala por fala,
@ TRAINER_SINNOH_GALACTIC_GRUNT_JUBILIFE_CITY_1/2, LOCALID_JUBILIFE_ROWAN ja
@ plantado, FLAG_GALACTICA_JUBILIFE ja reservada para exatamente este momento
@ (flags.h: "Rowan e os dois grunts em Jubilife"). So que la e por TALK
@ (o jogador anda ate os grunts), aqui seria por COORD_EVENT (emboscada
@ forcada em tag battle com o counterpart). Escrever os dois duplicaria a
@ mesma dupla de treinadores em dois mecanismos (contra a regra de id de
@ treinador nao repetir em cena). Nao escrevi a emboscada de novo: so
@ avanco a var pra quem depender dela nao travar, a cena de verdade e a do
@ S2.
JubilifeCity_EventScript_CoordEvent_TeamGalactic::
	lockall
	setvar VAR_SINNOH_JUBILIFE_ESTADO, 3
	releaseall
	end

JubilifeCity_Text_HelloHaveYouVisitedTrainersSchool:
	.string "Hello, my friend. Have you visited\n"
	.string "the Trainers' School?\p"
	.string "Did your friend not guide you\n"
	.string "there earlier?$"

JubilifeCity_Text_TakeInvestigationElsewhere:
	.string "Anyway, there appears to be no one\n"
	.string "shady in this Jubilife City.\p"
	.string "I shall therefore take my\n"
	.string "investigation elsewhere.\p"
	.string "But, my friend, I suggest you\n"
	.string "remain vigilant for shady\l"
	.string "grown-ups!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

JubilifeCity_EventScript_AceTrainerM2::
	msgbox JubilifeCity_Text_AceTrainerM2, MSGBOX_NPC
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

JubilifeCity_Text_AceTrainerM2:
	.string "I like to walk this whole city end\n"
	.string "to end. Good way to scout for tough\l"
	.string "Trainers to battle.$"

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

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

JubilifeCity_EventScript_Placa5::
	msgbox JubilifeCity_Text_Placa5, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa5:
	.string "Jubilife Condominiums\nTenants Wanted!$"

JubilifeCity_EventScript_Placa6::
	msgbox JubilifeCity_Text_Placa6, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa6:
	.string "The Pokétch Company\nPokémon Watches for the World!$"

JubilifeCity_EventScript_Placa7::
	msgbox JubilifeCity_Text_Placa7, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa7:
	.string "Jubilife TV\nThe Fun-and-Games TV Station!$"

JubilifeCity_EventScript_Placa8::
	msgbox JubilifeCity_Text_Placa8, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa8:
	.string "Trainers' School\nThe First Step for Trainers!$"

JubilifeCity_EventScript_Placa9::
	msgbox JubilifeCity_Text_Placa9, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa9:
	.string "The Global Terminal\nYour Gateway to the Whole World!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

JubilifeCity_EventScript_Npc1::
	msgbox JubilifeCity_Text_Npc1, MSGBOX_NPC
	end

JubilifeCity_Text_Npc1:
	.string "When you walk with your Pokémon,\nthey gradually grow friendlier.$"

JubilifeCity_EventScript_Npc2::
	msgbox JubilifeCity_Text_Npc2, MSGBOX_NPC
	end

JubilifeCity_Text_Npc2:
	.string "Hiya, where'd you come from?\p...\pTwinleaf Town, huh...\nIt's a nice place. Quiet and all.\pJubilife City is a big place, so it\nmight be a bit of a shock to you.$"

JubilifeCity_EventScript_Npc3::
	msgbox JubilifeCity_Text_Npc3, MSGBOX_NPC
	end

JubilifeCity_Text_Npc3:
	.string "The way you look...\nYou're obviously a Trainer!\pCan you tell me what type of Pokémon\nyou like?$"

JubilifeCity_EventScript_Npc4::
	msgbox JubilifeCity_Text_Npc4, MSGBOX_NPC
	end

JubilifeCity_Text_Npc4:
	.string "Did you see me on TV?\nI was in an interview!$"

JubilifeCity_EventScript_Npc5::
	msgbox JubilifeCity_Text_Npc5, MSGBOX_NPC
	end

JubilifeCity_Text_Npc5:
	.string "Hello, Trainer!\nDo you know much about Pokémon?$"

JubilifeCity_EventScript_Npc6::
	msgbox JubilifeCity_Text_Npc6, MSGBOX_NPC
	end

JubilifeCity_Text_Npc6:
	.string "OK, set six Poké Balls in my\nbelt...\pYeah, that'll do it. At most, you\ncan have six Pokémon with you.$"

JubilifeCity_EventScript_Npc7::
	msgbox JubilifeCity_Text_Npc7, MSGBOX_NPC
	end

JubilifeCity_Text_Npc7:
	.string "Jubilife City's built on land they\ncarved out of a mountain.\pThe people and Pokémon of Oreburgh\nCity helped out with that undertaking.$"

JubilifeCity_EventScript_Npc8::
	msgbox JubilifeCity_Text_Npc8, MSGBOX_NPC
	end

JubilifeCity_Text_Npc8:
	.string "Past here is the Global Terminal.\nIt lets you trade with the whole world!\pTrading Pokémon means connecting\nwith friends, both old and new.\pThat's awesome!$"

JubilifeCity_EventScript_Npc9::
	msgbox JubilifeCity_Text_Npc9, MSGBOX_NPC
	end

JubilifeCity_Text_Npc9:
	.string "I'm trading Pokémon with my buddy!$"

JubilifeCity_EventScript_Npc10::
	msgbox JubilifeCity_Text_Npc10, MSGBOX_NPC
	end

JubilifeCity_Text_Npc10:
	.string "I made my Pokémon hold an item before\ntrading it.\pThat will make the other Trainer\ndouble happy!$"

JubilifeCity_EventScript_Placa11::
	msgbox JubilifeCity_Text_Placa11, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa11:
	.string "Jubilife City\nCity of Joy$"

JubilifeCity_EventScript_Placa12::
	msgbox JubilifeCity_Text_Placa12, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa12:
	.string "Jubilife City\nCity of Joy$"

JubilifeCity_EventScript_Placa13::
	msgbox JubilifeCity_Text_Placa13, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa13:
	.string "Jubilife City\nCity of Joy$"

JubilifeCity_EventScript_Placa14::
	msgbox JubilifeCity_Text_Placa14, MSGBOX_SIGN
	end

JubilifeCity_Text_Placa14:
	.string "Jubilife City\nCity of Joy$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
JubilifeCity_EventScript_PortaFechada::
	msgbox JubilifeCity_Text_PortaFechada, MSGBOX_SIGN
	end

JubilifeCity_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
