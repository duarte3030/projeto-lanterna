Route212_South_MapScripts::
	.byte 0

Route212_South_EventScript_SchoolKid::
	msgbox Route212_South_Text_SchoolKid, MSGBOX_NPC
	end

Route212_South_EventScript_Lady::
	msgbox Route212_South_Text_Lady, MSGBOX_NPC
	end

Route212_South_EventScript_Collector::
	msgbox Route212_South_Text_Collector, MSGBOX_NPC
	end

Route212_South_EventScript_Fisherman::
	msgbox Route212_South_Text_Fisherman, MSGBOX_NPC
	end

Route212_South_EventScript_ShardsSign::
	msgbox Route212_South_Text_ShardsSign, MSGBOX_SIGN
	end

Route212_South_Text_SchoolKid:
	.string "I've been ROCK SMASHing all along this\n"
	.string "route, looking for wild POKéMON hiding\l"
	.string "in the rubble.$"

Route212_South_Text_Lady:
	.string "It rains here so often that I never\n"
	.string "leave home without my umbrella.$"

Route212_South_Text_Collector:
	.string "Shards wash up along this route after\n"
	.string "it rains. I've got quite a collection\l"
	.string "going!$"

Route212_South_Text_Fisherman:
	.string "I come here to fish whenever it rains.\n"
	.string "Something about the sound helps me\l"
	.string "focus on the bite.$"

Route212_South_Text_ShardsSign:
	.string "WANTED: SHARDS!\n"
	.string "Bring your finds to the antique shop\l"
	.string "in PASTORIA for a nice reward.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route212_South_EventScript_Placa1::
	msgbox Route212_South_Text_Placa1, MSGBOX_SIGN
	end

Route212_South_Text_Placa1:
	.string "Rt. 212\nPastoria City$"

Route212_South_EventScript_Placa2::
	msgbox Route212_South_Text_Placa2, MSGBOX_SIGN
	end

Route212_South_Text_Placa2:
	.string "Shards Wanted\nPokémon Moves Taught$"

Route212_South_EventScript_Placa3::
	msgbox Route212_South_Text_Placa3, MSGBOX_SIGN
	end

Route212_South_Text_Placa3:
	.string "Trainer Tips\pIf you get stuck in the bog, you can\ncount on being there a while.\pThere's no need to panic.\nJust struggle and squirm for a bit.\pBicycles cannot be ridden on marshy\nground, incidentally.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route212_South_EventScript_Npc1::
	msgbox Route212_South_Text_Npc1, MSGBOX_NPC
	end

Route212_South_Text_Npc1:
	.string "You can zip across fallen logs like\nbridges on your Bike.$"

Route212_South_EventScript_Npc2::
	msgbox Route212_South_Text_Npc2, MSGBOX_NPC
	end

Route212_South_Text_Npc2:
	.string "...Am I stuck in the bog?\pOf course not. How silly!\nThis is a full-body mud pack.\pIf it weren't, I would be squirming\nand struggling to get out!$"

Route212_South_EventScript_Npc3::
	msgbox Route212_South_Text_Npc3, MSGBOX_NPC
	end

Route212_South_Text_Npc3:
	.string "You've been to the Great Marsh?\nHow about the Pokémon Mansion?\pWherever I go, I get to meet new and\ndifferent Pokémon.\pI feel so privileged and happy about\nthat.$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route212_South_EventScript_FishermanJuan::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_JUAN, Route212_South_Text_FishermanJuanIntro, Route212_South_Text_FishermanJuanDefeat
	msgbox Route212_South_Text_FishermanJuanPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_FishermanJuanIntro:
	.string "Can't you see I'm fishing?\nDon't talk! You'll spook the fish!$"

Route212_South_Text_FishermanJuanDefeat:
	.string "How do you like that?\nBoth my catch and the win got away!$"

Route212_South_Text_FishermanJuanPost:
	.string "Fishing and battling are delicate\nthings--as am I. Is that wrong?$"

Route212_South_EventScript_FishermanJosh::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_JOSH, Route212_South_Text_FishermanJoshIntro, Route212_South_Text_FishermanJoshDefeat
	msgbox Route212_South_Text_FishermanJoshPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_FishermanJoshIntro:
	.string "I wish some fishing-loving lady'd come\nalong. But no, it's all just Trainers.$"

Route212_South_Text_FishermanJoshDefeat:
	.string "Sure, so I lost.\nBut I'll keep on fishing.$"

Route212_South_Text_FishermanJoshPost:
	.string "If you know of any ladies that like\nfishing, help me reel 'em in!$"

Route212_South_EventScript_FishermanTravis::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_TRAVIS, Route212_South_Text_FishermanTravisIntro, Route212_South_Text_FishermanTravisDefeat
	msgbox Route212_South_Text_FishermanTravisPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_FishermanTravisIntro:
	.string "Water Pokémon sure get happy when\nit rains. So do I!$"

Route212_South_Text_FishermanTravisDefeat:
	.string "Oof. Just got trampled right under\nyour feet that time!$"

Route212_South_Text_FishermanTravisPost:
	.string "Yup, a kid like you should be running\naround outside, rain or shine.$"

Route212_South_EventScript_RangerTaylor::
	trainerbattle_single TRAINER_SINNOH_RANGER_TAYLOR, Route212_South_Text_RangerTaylorIntro, Route212_South_Text_RangerTaylorDefeat
	msgbox Route212_South_Text_RangerTaylorPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_RangerTaylorIntro:
	.string "Hi, Trainer!\nCan you keep up with me?$"

Route212_South_Text_RangerTaylorDefeat:
	.string "You've got energy to burn!$"

Route212_South_Text_RangerTaylorPost:
	.string "Even if a battle gets heated, don't\nbreak branches off trees or anything.$"

Route212_South_EventScript_RangerAllison::
	trainerbattle_single TRAINER_SINNOH_RANGER_ALLISON, Route212_South_Text_RangerAllisonIntro, Route212_South_Text_RangerAllisonDefeat
	msgbox Route212_South_Text_RangerAllisonPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_RangerAllisonIntro:
	.string "Protect the natural environment.\nThat's what we Rangers do!$"

Route212_South_Text_RangerAllisonDefeat:
	.string "We've got to get tougher than this...$"

Route212_South_Text_RangerAllisonPost:
	.string "I love how natural it is here.\nI wish I could live out here.$"

Route212_South_EventScript_RangerJeffrey::
	trainerbattle_single TRAINER_SINNOH_RANGER_JEFFREY, Route212_South_Text_RangerJeffreyIntro, Route212_South_Text_RangerJeffreyDefeat
	msgbox Route212_South_Text_RangerJeffreyPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_RangerJeffreyIntro:
	.string "Heya, Trainer!\nAre you being good to Mother Nature?$"

Route212_South_Text_RangerJeffreyDefeat:
	.string "Good. You seem to be a kindhearted\nTrainer.$"

Route212_South_Text_RangerJeffreyPost:
	.string "Listen, people and Pokémon, we're all a\npart of Mother Nature.$"

Route212_South_EventScript_ScientistStefano::
	trainerbattle_single TRAINER_SINNOH_SCIENTIST_STEFANO, Route212_South_Text_ScientistStefanoIntro, Route212_South_Text_ScientistStefanoDefeat
	msgbox Route212_South_Text_ScientistStefanoPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_ScientistStefanoIntro:
	.string "I find it reassuring to be on this\ndamp soil...$"

Route212_South_Text_ScientistStefanoDefeat:
	.string "Ufufufufu...\nYou had to beat me...$"

Route212_South_Text_ScientistStefanoPost:
	.string "It feels good to mope here after a\nloss... Ufufufufu...$"

Route212_South_EventScript_CollectorDean::
	trainerbattle_single TRAINER_SINNOH_COLLECTOR_DEAN, Route212_South_Text_CollectorDeanIntro, Route212_South_Text_CollectorDeanDefeat
	msgbox Route212_South_Text_CollectorDeanPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_CollectorDeanIntro:
	.string "I'm proud of my Pokémon!\nHere, I'll show you why!$"

Route212_South_Text_CollectorDeanDefeat:
	.string "Youch! You sure showed me how tough\nyou were.$"

Route212_South_Text_CollectorDeanPost:
	.string "Oh, what have we here?\nThat's a Pokédex!\pIt records Pokémon data upon\nsight? I've never seen one before!\pI heard you can move the sun or\nmoon icon to check the Pokémon\phabitat map by time of day!$"

Route212_South_EventScript_ScientistShaun::
	trainerbattle_single TRAINER_SINNOH_SCIENTIST_SHAUN, Route212_South_Text_ScientistShaunIntro, Route212_South_Text_ScientistShaunDefeat
	msgbox Route212_South_Text_ScientistShaunPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_ScientistShaunIntro:
	.string "Oh? Here comes a nice-looking\nTrainer. This is worth evaluation.$"

Route212_South_Text_ScientistShaunDefeat:
	.string "Our research has arrived at this one\nconclusion: you're a tough one!$"

Route212_South_Text_ScientistShaunPost:
	.string "A huge variety of Pokémon live in the\nGreat Marsh.\pYou see, countless years ago,\nthis whole area was under the sea.$"

Route212_South_EventScript_ParasolLadyAlexa::
	trainerbattle_single TRAINER_SINNOH_PARASOL_LADY_ALEXA, Route212_South_Text_ParasolLadyAlexaIntro, Route212_South_Text_ParasolLadyAlexaDefeat
	msgbox Route212_South_Text_ParasolLadyAlexaPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_ParasolLadyAlexaIntro:
	.string "There are Pokémon that grow stronger\nwhen it's raining.$"

Route212_South_Text_ParasolLadyAlexaDefeat:
	.string "Like rain, my tears flow from losing...\nThey call me the Rain Woman...$"

Route212_South_Text_ParasolLadyAlexaPost:
	.string "I want to show off my pretty parasol,\nbut it will get dirty in the rain.\pOh, such a big dilemma!$"

Route212_South_EventScript_ParasolLadySabrina::
	trainerbattle_single TRAINER_SINNOH_PARASOL_LADY_SABRINA, Route212_South_Text_ParasolLadySabrinaIntro, Route212_South_Text_ParasolLadySabrinaDefeat
	msgbox Route212_South_Text_ParasolLadySabrinaPost, MSGBOX_AUTOCLOSE
	end

Route212_South_Text_ParasolLadySabrinaIntro:
	.string "When it rains, I get more tense!$"

Route212_South_Text_ParasolLadySabrinaDefeat:
	.string "It's not very easy trying to battle\nwhile holding an umbrella.$"

Route212_South_Text_ParasolLadySabrinaPost:
	.string "If it rained every day, I could have\nmy umbrella open all the time.$"
