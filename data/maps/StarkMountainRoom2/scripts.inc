StarkMountainRoom2_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

StarkMountainRoom2_EventScript_AceTrainerKeenan::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_KEENAN, StarkMountainRoom2_Text_AceTrainerKeenanIntro, StarkMountainRoom2_Text_AceTrainerKeenanDefeat
	msgbox StarkMountainRoom2_Text_AceTrainerKeenanPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_AceTrainerKeenanIntro:
	.string "What it means to win battles...\nThat is what I seek.\pTeach me if you will!$"

StarkMountainRoom2_Text_AceTrainerKeenanDefeat:
	.string "I grow less certain still...$"

StarkMountainRoom2_Text_AceTrainerKeenanPost:
	.string "Perhaps there is no meaning to\nvictory, but still I will battle!\pThat is what makes me a Trainer!$"

StarkMountainRoom2_EventScript_AceTrainerKassandra::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_KASSANDRA, StarkMountainRoom2_Text_AceTrainerKassandraIntro, StarkMountainRoom2_Text_AceTrainerKassandraDefeat
	msgbox StarkMountainRoom2_Text_AceTrainerKassandraPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_AceTrainerKassandraIntro:
	.string "You've come all this way for Pokémon?\nYou must be dedicated.$"

StarkMountainRoom2_Text_AceTrainerKassandraDefeat:
	.string "Your dedication won out.$"

StarkMountainRoom2_Text_AceTrainerKassandraPost:
	.string "The Pokémon here must battle each\nother all the time.\pThat must be why they are so strong\nin this area.$"

StarkMountainRoom2_EventScript_AceTrainerSkylar::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_SKYLAR, StarkMountainRoom2_Text_AceTrainerSkylarIntro, StarkMountainRoom2_Text_AceTrainerSkylarDefeat
	msgbox StarkMountainRoom2_Text_AceTrainerSkylarPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_AceTrainerSkylarIntro:
	.string "I was born in Floaroma Town.\nI'm sure thrilled to be here.\pIt took a long time to get here.\nWe're not going to lose again!$"

StarkMountainRoom2_Text_AceTrainerSkylarDefeat:
	.string "We went down...\nWe couldn't stick it out...$"

StarkMountainRoom2_Text_AceTrainerSkylarPost:
	.string "You can level all you want, but that\nwon't guarantee you any wins.\pBut we keep trying to get better.\nThat's what makes us Trainers.$"

StarkMountainRoom2_EventScript_AceTrainerNatasha::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_NATASHA, StarkMountainRoom2_Text_AceTrainerNatashaIntro, StarkMountainRoom2_Text_AceTrainerNatashaDefeat
	msgbox StarkMountainRoom2_Text_AceTrainerNatashaPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_AceTrainerNatashaIntro:
	.string "I came here after winning my way\nthrough the Battle Tower!$"

StarkMountainRoom2_Text_AceTrainerNatashaDefeat:
	.string "But...\nI had a win streak going...$"

StarkMountainRoom2_Text_AceTrainerNatashaPost:
	.string "Train more at the Battle Tower...\nThat's what I'll do.$"

StarkMountainRoom2_EventScript_PsychicChelsey::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_CHELSEY, StarkMountainRoom2_Text_PsychicChelseyIntro, StarkMountainRoom2_Text_PsychicChelseyDefeat
	msgbox StarkMountainRoom2_Text_PsychicChelseyPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_PsychicChelseyIntro:
	.string "I'll use my mystifying psychic power\nto pulverize you!$"

StarkMountainRoom2_Text_PsychicChelseyDefeat:
	.string "That's what I get for making idle\nclaims...$"

StarkMountainRoom2_Text_PsychicChelseyPost:
	.string "Psychic power is a mystery that\ndefies explanation.\pBut if everything could be explained,\nit would be a boring world.$"

StarkMountainRoom2_EventScript_PsychicSterling::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_STERLING, StarkMountainRoom2_Text_PsychicSterlingIntro, StarkMountainRoom2_Text_PsychicSterlingDefeat
	msgbox StarkMountainRoom2_Text_PsychicSterlingPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_PsychicSterlingIntro:
	.string "I had a revelation this morning.\pI knew that I would have a wonderful\nencounter here today.$"

StarkMountainRoom2_Text_PsychicSterlingDefeat:
	.string "There's nothing wonderful about this!$"

StarkMountainRoom2_Text_PsychicSterlingPost:
	.string "Is my sense of premonition nothing\nto write home about?$"

StarkMountainRoom2_EventScript_BirdKeeperKrystal::
	trainerbattle_single TRAINER_SINNOH_BIRD_KEEPER_KRYSTAL, StarkMountainRoom2_Text_BirdKeeperKrystalIntro, StarkMountainRoom2_Text_BirdKeeperKrystalDefeat
	msgbox StarkMountainRoom2_Text_BirdKeeperKrystalPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_BirdKeeperKrystalIntro:
	.string "With one mighty flap, my birds blow\naway the embers of aggression!$"

StarkMountainRoom2_Text_BirdKeeperKrystalDefeat:
	.string "We failed to get off the ground...$"

StarkMountainRoom2_Text_BirdKeeperKrystalPost:
	.string "The HM Fly isn't useful inside caves.\nIt's such a shame.$"

StarkMountainRoom2_EventScript_BlackBeltRay::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_RAY, StarkMountainRoom2_Text_BlackBeltRayIntro, StarkMountainRoom2_Text_BlackBeltRayDefeat
	msgbox StarkMountainRoom2_Text_BlackBeltRayPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_BlackBeltRayIntro:
	.string "My Pokémon can destroy anything.\nAnd you think you can win?!$"

StarkMountainRoom2_Text_BlackBeltRayDefeat:
	.string "We weren't up to the task!$"

StarkMountainRoom2_Text_BlackBeltRayPost:
	.string "Even though my team could break\nbricks and shatter boulders, they\pfailed to dent your spirits!$"

StarkMountainRoom2_EventScript_AceTrainerStefan::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_STEFAN, StarkMountainRoom2_Text_AceTrainerStefanIntro, StarkMountainRoom2_Text_AceTrainerStefanDefeat
	msgbox StarkMountainRoom2_Text_AceTrainerStefanPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_AceTrainerStefanIntro:
	.string "Let me ask to see if you know.\nWhat is time?$"

StarkMountainRoom2_Text_AceTrainerStefanDefeat:
	.string "Another memory...\nIn a chain of memories.$"

StarkMountainRoom2_Text_AceTrainerStefanPost:
	.string "For me, time is the fabric woven by\nmemories, one after another...$"

StarkMountainRoom2_EventScript_AceTrainerJasmin::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_JASMIN, StarkMountainRoom2_Text_AceTrainerJasminIntro, StarkMountainRoom2_Text_AceTrainerJasminDefeat
	msgbox StarkMountainRoom2_Text_AceTrainerJasminPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_AceTrainerJasminIntro:
	.string "Can you answer this for me?\nWhat is space?$"

StarkMountainRoom2_Text_AceTrainerJasminDefeat:
	.string "And another...\nA new memory was born.$"

StarkMountainRoom2_Text_AceTrainerJasminPost:
	.string "For me, space is where memories are\nmade...$"

StarkMountainRoom2_EventScript_DragonTamerDrake::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_DRAKE, StarkMountainRoom2_Text_DragonTamerDrakeIntro, StarkMountainRoom2_Text_DragonTamerDrakeDefeat
	msgbox StarkMountainRoom2_Text_DragonTamerDrakePost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_DragonTamerDrakeIntro:
	.string "Dragons and a fiery mountain...\nIt's a totally classic setup!$"

StarkMountainRoom2_Text_DragonTamerDrakeDefeat:
	.string "Losing isn't a happy occasion...$"

StarkMountainRoom2_Text_DragonTamerDrakePost:
	.string "My Pokémon seem to like it here\na lot.$"

StarkMountainRoom2_EventScript_BlackBeltJarrett::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_JARRETT, StarkMountainRoom2_Text_BlackBeltJarrettIntro, StarkMountainRoom2_Text_BlackBeltJarrettDefeat
	msgbox StarkMountainRoom2_Text_BlackBeltJarrettPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_BlackBeltJarrettIntro:
	.string "Hear the howl of my iron fists!\nHowdy! I'm crazy for karate!$"

StarkMountainRoom2_Text_BlackBeltJarrettDefeat:
	.string "Losing made it clear to me.\nYou're crazy about Pokémon!$"

StarkMountainRoom2_Text_BlackBeltJarrettPost:
	.string "I love seeing people who love Pokémon\nmore than anything!$"

StarkMountainRoom2_EventScript_AceTrainerAbel::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ABEL, StarkMountainRoom2_Text_AceTrainerAbelIntro, StarkMountainRoom2_Text_AceTrainerAbelDefeat
	msgbox StarkMountainRoom2_Text_AceTrainerAbelPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_AceTrainerAbelIntro:
	.string "The Trainers and Pokémon that gather\nhere aren't pushovers.\pThey all have tricks up their sleeves!$"

StarkMountainRoom2_Text_AceTrainerAbelDefeat:
	.string "You're not a Trainer that can be\ntaken lightly!$"

StarkMountainRoom2_Text_AceTrainerAbelPost:
	.string "The Pokémon you'll meet here won't\nmake it easy for you to move onward.$"

StarkMountainRoom2_EventScript_AceTrainerMonique::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_MONIQUE, StarkMountainRoom2_Text_AceTrainerMoniqueIntro, StarkMountainRoom2_Text_AceTrainerMoniqueDefeat
	msgbox StarkMountainRoom2_Text_AceTrainerMoniquePost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_AceTrainerMoniqueIntro:
	.string "We're all good to go!\nWe just have to battle now!$"

StarkMountainRoom2_Text_AceTrainerMoniqueDefeat:
	.string "Aww...\nI'm out of useful items!$"

StarkMountainRoom2_Text_AceTrainerMoniquePost:
	.string "We came completely unprepared for\nthis little adventure...$"

StarkMountainRoom2_EventScript_VeteranHarlan::
	trainerbattle_single TRAINER_SINNOH_VETERAN_HARLAN, StarkMountainRoom2_Text_VeteranHarlanIntro, StarkMountainRoom2_Text_VeteranHarlanDefeat
	msgbox StarkMountainRoom2_Text_VeteranHarlanPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_VeteranHarlanIntro:
	.string "What do you expect to achieve here?\nI'll be the one to make that call!$"

StarkMountainRoom2_Text_VeteranHarlanDefeat:
	.string "You've earned the right to be here.\nBoth you and your Pokémon.$"

StarkMountainRoom2_Text_VeteranHarlanPost:
	.string "You may find it odd, but the stink\nof sulfur from the volcanic gas\pis what draws me here.$"

StarkMountainRoom2_EventScript_DragonTamerKenny::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_KENNY, StarkMountainRoom2_Text_DragonTamerKennyIntro, StarkMountainRoom2_Text_DragonTamerKennyDefeat
	msgbox StarkMountainRoom2_Text_DragonTamerKennyPost, MSGBOX_AUTOCLOSE
	end

StarkMountainRoom2_Text_DragonTamerKennyIntro:
	.string "Are you seeking the mythical\nPokémon, too? Let's battle, then!$"

StarkMountainRoom2_Text_DragonTamerKennyDefeat:
	.string "There's nothing left...$"

StarkMountainRoom2_Text_DragonTamerKennyPost:
	.string "The mythical Pokémon that sleeps\ndeep in a volcano...\pCould it be a dragon Pokémon?$"
