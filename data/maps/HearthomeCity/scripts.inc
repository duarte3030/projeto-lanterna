@ Textos vindos de pret/pokeplatinum (res/text/hearthome_city.json), em ingles.
@ Pokefan_M_2, Hiker_2, Hiker_3, Keira e o Gym_Guide ENTRARAM em 18/08/2026,
@ leva S5: a maquina ja tinha aliasado as flags (0x1B22 a 0x1B27), a cabeca
@ acima so estava desatualizada. Buneary NAO entrou: nao existe sprite OW
@ para ela aqui (nem em include/, nem em TROCA_SPRITE), e ela nunca e
@ interativa sozinha (fonte: script:0, sempre em par com a Keira). A cena
@ de baixo mantem so o grito (playmoncry), sem objeto visual.
@ O reporter da Amity Square (LOCALID nao trazido, FLAG_SINNOH_ESCONDE_
@ HEARTHOME_CITY_GATE_TO_AMITY_SQUARE_REPORTER) e o da Fan Club (FLAG_
@ ..._POKEMON_FAN_CLUB_REPORTER) tambem ficam de fora: a fonte so os mostra
@ via CheckTVInterviewEligible (mecanica de TV Interview/PokeNews, que nao
@ existe aqui), sem SetFlag em new_game.inc. Nao ha estado padrao correto
@ para inventar; ficam pendentes ate essa mecanica ganhar desenho (mesma
@ regua da decisao 3 do plano, mecanica inexistente).

HearthomeCity_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ S5: rotulo da fonte HearthomeCity_CoordEvent_BunearyAndKeira. A fonte
@ reposiciona Keira/Buneary por GetPlayerMapPos + 5 ramos fixos (script:21,
@ decisao 8 do plano); os 5 tiles do gatilho aqui (dev_scripts/maquina_
@ sinnoh.json) preservam a mesma ordem de linha (z725..729 -> y42..46, y42
@ empurrado de x11 para x16 por colisao, ver "tiles_movidos"). Spawn = tile
@ do gatilho +10 no x (fonte: 461->471); Keira anda 8 tiles para oeste e
@ para em gatilho+2 (fonte: 471->463), literal da fonte.
HearthomeCity_EventScript_CoordEvent_BunearyAndKeira::
	lockall
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_eq VAR_0x8005, 42, HearthomeCity_EventScript_BunearyKeiraRow42
	goto_if_eq VAR_0x8005, 43, HearthomeCity_EventScript_BunearyKeiraRow43
	goto_if_eq VAR_0x8005, 44, HearthomeCity_EventScript_BunearyKeiraRow44
	goto_if_eq VAR_0x8005, 45, HearthomeCity_EventScript_BunearyKeiraRow45
	goto_if_eq VAR_0x8005, 46, HearthomeCity_EventScript_BunearyKeiraRow46
	releaseall
	end

HearthomeCity_EventScript_BunearyKeiraRow42::
	setobjectxy LOCALID_HEARTHOME_KEIRA, 26, 42
	goto HearthomeCity_EventScript_BunearyKeiraScene

HearthomeCity_EventScript_BunearyKeiraRow43::
	setobjectxy LOCALID_HEARTHOME_KEIRA, 21, 43
	goto HearthomeCity_EventScript_BunearyKeiraScene

HearthomeCity_EventScript_BunearyKeiraRow44::
	setobjectxy LOCALID_HEARTHOME_KEIRA, 21, 44
	goto HearthomeCity_EventScript_BunearyKeiraScene

HearthomeCity_EventScript_BunearyKeiraRow45::
	setobjectxy LOCALID_HEARTHOME_KEIRA, 21, 45
	goto HearthomeCity_EventScript_BunearyKeiraScene

HearthomeCity_EventScript_BunearyKeiraRow46::
	setobjectxy LOCALID_HEARTHOME_KEIRA, 21, 46
	goto HearthomeCity_EventScript_BunearyKeiraScene

HearthomeCity_EventScript_BunearyKeiraScene::
	clearflag FLAG_SINNOH_ESCONDE_HEARTHOME_CITY_KEIRA
	addobject LOCALID_HEARTHOME_KEIRA
	playmoncry SPECIES_BUNEARY, CRY_MODE_NORMAL
	waitmoncry
	applymovement LOCALID_HEARTHOME_KEIRA, HearthomeCity_Movement_KeiraEnter
	waitmovement 0
	msgbox HearthomeCity_Text_ThankGoodnessYoureHere, MSGBOX_DEFAULT
	msgbox HearthomeCity_Text_BackIntoThePokeBall, MSGBOX_DEFAULT
	playmoncry SPECIES_BUNEARY, CRY_MODE_NORMAL
	waitmoncry
	msgbox HearthomeCity_Text_ImKeira, MSGBOX_DEFAULT
	applymovement LOCALID_HEARTHOME_KEIRA, HearthomeCity_Movement_KeiraLeave
	waitmovement 0
	setflag FLAG_SINNOH_ESCONDE_HEARTHOME_CITY_KEIRA
	removeobject LOCALID_HEARTHOME_KEIRA
	setvar VAR_SINNOH_HEARTHOME_ESTADO, 1
	releaseall
	end

HearthomeCity_Movement_KeiraEnter:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	step_end

HearthomeCity_Movement_KeiraLeave:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

HearthomeCity_Text_ThankGoodnessYoureHere:
	.string "Oh, thank goodness that you happened\nto be there!\pIf it weren't for you, who knows how\nfar away my BUNEARY could have run...$"

HearthomeCity_Text_BackIntoThePokeBall:
	.string "Baby BUNEARY, back into the Poké\nBall you go!$"

HearthomeCity_Text_ImKeira:
	.string "I'm Keira!\nI'm a Pokémon Contest Judge.\pBe sure to drop by the Contest Hall\nso I can thank you properly!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ >>> B6 Sinnoh S5: grupo de hidden_flag (dev_scripts/maquina_sinnoh.json) >>>
@ POKEFAN_M_2 + HIKER_2: bloqueiam a saida para a Route209 ate o ginasio de
@ Hearthome ser vencido. A fonte SO os esconde (SetFlag) dentro do script de
@ vitoria do lider (scripts_hearthome_city_gym_leader_room.s / _dp_..., os
@ dois arquivos), que e batalha de ginasio/lider e fica fora do meu escopo
@ (decisao 2 do Gui). Nao ha SetFlag em new_game.inc, entao ficam visiveis
@ desde o inicio, do jeito que a fonte tambem comeca: certo por enquanto,
@ e o setflag entra quando a polimento do ginasio acontecer.
HearthomeCity_EventScript_PokefanM2::
	msgbox HearthomeCity_Text_FoundAnEggAtDayCare, MSGBOX_NPC
	end

HearthomeCity_Text_FoundAnEggAtDayCare:
	.string "Did you know?\pThey found an Egg at the Day Care in\nSolaceon Town past here.$"

HearthomeCity_EventScript_Hiker2::
	msgbox HearthomeCity_Text_EggsInJohtoToo, MSGBOX_NPC
	end

HearthomeCity_Text_EggsInJohtoToo:
	.string "Did you know?\pThey find Eggs in the far-off Johto\nregion, too.$"

@ HIKER_3: a fonte so o esconde (ClearFlag) dentro de scripts_contests.s
@ (sistema de Contest, fora de escopo aqui). Sem SetFlag em new_game.inc,
@ visivel desde o inicio.
HearthomeCity_EventScript_Hiker3::
	msgbox HearthomeCity_Text_SometimesEggsAtDayCare, MSGBOX_NPC
	end

HearthomeCity_Text_SometimesEggsAtDayCare:
	.string "I have a professor friend, and this is\nwhat he told me.\pIf you leave a pair of Pokémon with the\nDay Care, sometimes Eggs are found.\pOr things that are like Eggs, anyway.\pI wonder how my pal Prof. Elm is doing\nthese days?\pHe was always a quiet sort and didn't\nreally stand out.$"

@ GYM_GUIDE: a fonte so o esconde (SetFlag) dentro de scripts_contest_hall_
@ lobby.s (sistema de Contest, fora de escopo). Sem SetFlag em new_game.inc,
@ visivel desde o inicio.
HearthomeCity_EventScript_GymGuide::
	msgbox HearthomeCity_Text_ComeBackAnotherTime, MSGBOX_NPC
	end

HearthomeCity_Text_ComeBackAnotherTime:
	.string "Hey, there!\nHow's it going, Trainer?\pYou being here tells me you're going\nto challenge the Gym Leader.\pWell... I hate to break it to you, but\nthat's impossible.\pYou're questioning why, and the answer\nis: she's not here.\pNot to worry, though.\nWe know she's at the Contest Hall.\pCome back another time, OK?\nI'll be waiting right here.$"
@ <<< B6 Sinnoh S5: grupo de hidden_flag <<<

HearthomeCity_EventScript_PokefanM::
	msgbox HearthomeCity_Text_PokefanM, MSGBOX_NPC
	end

HearthomeCity_EventScript_BreederF::
	msgbox HearthomeCity_Text_BreederF, MSGBOX_NPC
	end

HearthomeCity_EventScript_BlackBelt::
	msgbox HearthomeCity_Text_BlackBelt, MSGBOX_NPC
	end

HearthomeCity_EventScript_ContestHallSign::
	msgbox HearthomeCity_Text_ContestHallSign, MSGBOX_SIGN
	end

HearthomeCity_EventScript_GymSign::
	msgbox HearthomeCity_Text_GymSign, MSGBOX_SIGN
	end

HearthomeCity_Text_PokefanM:
	.string "HEARTHOME CITY is famous for its\n"
	.string "POKéMON Contests. Have you seen\l"
	.string "the CONTEST HALL yet?$"

HearthomeCity_Text_BreederF:
	.string "I raise my POKéMON right here in\n"
	.string "the city square. They love all\l"
	.string "the attention.$"

HearthomeCity_Text_BlackBelt:
	.string "Strength of body, strength of\n"
	.string "spirit. That's the way here in\l"
	.string "HEARTHOME.$"

HearthomeCity_Text_ContestHallSign:
	.string "POKéMON CONTEST HALL$"

HearthomeCity_Text_GymSign:
	.string "HEARTHOME CITY POKéMON GYM\p"
	.string "The Normal-Type Beauty Style!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

HearthomeCity_EventScript_Placa1::
	msgbox HearthomeCity_Text_Placa1, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa1:
	.string "Rt. 208\nRt. 212$"

HearthomeCity_EventScript_Placa2::
	msgbox HearthomeCity_Text_Placa2, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa2:
	.string "Rt. 209\nSolaceon Town$"

HearthomeCity_EventScript_Placa3::
	msgbox HearthomeCity_Text_Placa3, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa3:
	.string "Amity Square West Gate\nStroll with Your Pokémon!$"

HearthomeCity_EventScript_Placa4::
	msgbox HearthomeCity_Text_Placa4, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa4:
	.string "Pokémon Contest Hall\nCalling All Enthusiasts!$"

HearthomeCity_EventScript_Placa5::
	msgbox HearthomeCity_Text_Placa5, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa5:
	.string "Amity Square East Gate\nStroll with Your Pokémon!$"

HearthomeCity_EventScript_Placa6::
	msgbox HearthomeCity_Text_Placa6, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa6:
	.string "Pokémon Fan Club\nAll Trainers Welcome$"

HearthomeCity_EventScript_Placa7::
	msgbox HearthomeCity_Text_Placa7, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa7:
	.string "Hearthome City Pokémon Gym\nLeader: Fantina\pThe Alluring, Soulful Dancer!$"

HearthomeCity_EventScript_Placa9::
	msgbox HearthomeCity_Text_Placa9, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa9:
	.string "The Poffin House\nDelicious Poffins--Smiles for All$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

HearthomeCity_EventScript_Npc1::
	msgbox HearthomeCity_Text_Npc1, MSGBOX_NPC
	end

HearthomeCity_Text_Npc1:
	.string "I'm visiting here all the way from\nthe Hoenn region.\pI had been hoping to find the Contest\nHall, but being new, I lost my way.\pFortunately, the local people very\nkindly led me to my destination.\pI was impressed by their kindness and\ngenerosity to a complete stranger.\pNow, may I offer you the courtesy\nof showing you to the Contest Hall?$"

HearthomeCity_EventScript_Npc2::
	msgbox HearthomeCity_Text_Npc2, MSGBOX_NPC
	end

HearthomeCity_Text_Npc2:
	.string "You're a Trainer, are you?\pYou've got two choices of challenges,\neither the Gym or a Contest, right?$"

HearthomeCity_EventScript_Npc3::
	msgbox HearthomeCity_Text_Npc3, MSGBOX_NPC
	end

HearthomeCity_Text_Npc3:
	.string "When I take my baby out in his stroller,\nI see the town in a different way.\pI notice things like stairs and bumps\nin the sidewalk.$"

HearthomeCity_EventScript_Npc4::
	msgbox HearthomeCity_Text_Npc4, MSGBOX_NPC
	end

HearthomeCity_Text_Npc4:
	.string "Apapapu!$"

HearthomeCity_EventScript_Npc5::
	msgbox HearthomeCity_Text_Npc5, MSGBOX_NPC
	end

HearthomeCity_Text_Npc5:
	.string "At the Lost Tower, people unburden\nthemselves of unbearable sorrow...\pYou'll understand what I mean if you\nvisit the Lost Tower on Route 209.$"

HearthomeCity_EventScript_Npc6::
	msgbox HearthomeCity_Text_Npc6, MSGBOX_NPC
	end

HearthomeCity_Text_Npc6:
	.string "I get to see Pokémon all day long,\nbut there sure are many kinds.\pHow many are there now?$"

HearthomeCity_EventScript_Npc7::
	msgbox HearthomeCity_Text_Npc7, MSGBOX_NPC
	end

HearthomeCity_Text_Npc7:
	.string "They call me Mr. Goods.\pNo one knows my real name.\nNo, not even I do...\pI dedicate myself to seeking rarities.\nIt's what I live for.$"

HearthomeCity_EventScript_Npc8::
	msgbox HearthomeCity_Text_Npc8, MSGBOX_NPC
	end

HearthomeCity_Text_Npc8:
	.string "I can't decide what Accessories I\nshould dress up Pokémon with.\pThere are just so many kinds.$"

HearthomeCity_EventScript_Npc9::
	msgbox HearthomeCity_Text_Npc9, MSGBOX_NPC
	end

HearthomeCity_Text_Npc9:
	.string "I used a Fire Stone on my Pokémon,\nand it evolved!$"

HearthomeCity_EventScript_Npc10::
	msgbox HearthomeCity_Text_Npc10, MSGBOX_NPC
	end

HearthomeCity_Text_Npc10:
	.string "I went for a stroll in Amity Square\nwith my PACHIRISU today.\pWe came across a Pokémon feather\nwhile we walked.\pDo you think it'd make my PACHIRISU\nlook any cuter?$"

HearthomeCity_EventScript_Npc11::
	msgbox HearthomeCity_Text_Npc11, MSGBOX_NPC
	end

HearthomeCity_Text_Npc11:
	.string "I'd like to live in Hearthome when\nI get married.\pBut my boyfriend wants to live in\nVeilstone 'cause of its Game Corner...$"

HearthomeCity_EventScript_Npc12::
	msgbox HearthomeCity_Text_Npc12, MSGBOX_NPC
	end

HearthomeCity_Text_Npc12:
	.string "I lived in total seclusion up in\nthe mountains for thirty years!\pI'm going to clean up some Contests\nwith a dance move I came up with!$"

HearthomeCity_EventScript_Npc13::
	msgbox HearthomeCity_Text_Npc13, MSGBOX_NPC
	end

HearthomeCity_Text_Npc13:
	.string "Papa! Mama!$"

HearthomeCity_EventScript_Npc14::
	msgbox HearthomeCity_Text_Npc14, MSGBOX_NPC
	end

HearthomeCity_Text_Npc14:
	.string "I can feel the baby stroller getting\nheavier each and every day.\pI wonder what kind of Pokémon my\nchild will become friends with first?$"

HearthomeCity_EventScript_Npc15::
	msgbox HearthomeCity_Text_Npc15, MSGBOX_NPC
	end

HearthomeCity_Text_Npc15:
	.string "This place is beautiful.\nPerhaps even too much so.\pPokémon, people, and nature are in\nperfect harmony here.$"

HearthomeCity_EventScript_Npc16::
	msgbox HearthomeCity_Text_Npc16, MSGBOX_NPC
	end

HearthomeCity_Text_Npc16:
	.string "I put my Vs. Seeker through its paces\na lot.\pI battled this one intriguing Trainer\nover and over using it.\pShe asked me, 'Do you like me?'\nLike, oops! Hahahahah!$"

HearthomeCity_EventScript_Placa17::
	msgbox HearthomeCity_Text_Placa17, MSGBOX_SIGN
	end

HearthomeCity_Text_Placa17:
	.string "Hearthome City\nWarm & Kind$"
