Route210_South_MapScripts::
	.byte 0

Route210_South_EventScript_AceTrainer::
	msgbox Route210_South_Text_AceTrainer, MSGBOX_NPC
	end

Route210_South_EventScript_Breeder::
	msgbox Route210_South_Text_Breeder, MSGBOX_NPC
	end

Route210_South_EventScript_Rancher::
	msgbox Route210_South_Text_Rancher, MSGBOX_NPC
	end

Route210_South_EventScript_Belle::
	msgbox Route210_South_Text_Belle, MSGBOX_NPC
	end

Route210_South_Text_AceTrainer:
	.string "I'm taking a rest. If I were a\n"
	.string "bird Pokémon, it would be a roost.$"

Route210_South_Text_Breeder:
	.string "I'm walking my Pokémon to keep\n"
	.string "them happy and healthy.$"

Route210_South_Text_Rancher:
	.string "The Pokémon Day Care is just\n"
	.string "down the road in Solaceon.$"

Route210_South_Text_Belle:
	.string "Pa and I raise Miltank here.\n"
	.string "Come say hi anytime.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route210_South_EventScript_Placa1::
	msgbox Route210_South_Text_Placa1, MSGBOX_SIGN
	end

Route210_South_Text_Placa1:
	.string "Rt. 210\nSolaceon Town$"

Route210_South_EventScript_Placa2::
	msgbox Route210_South_Text_Placa2, MSGBOX_SIGN
	end

Route210_South_Text_Placa2:
	.string "Café Cabin\nFreshly Squeezed Milk$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route210_South_EventScript_Npc1::
	msgbox Route210_South_Text_Npc1, MSGBOX_NPC
	end

Route210_South_Text_Npc1:
	.string "I'm taking a rest. If I were a bird\nPokémon, it would be a roost. Haha!\pUh... You should rest up, too.$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route210_South_EventScript_NinjaBoyFabian::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_FABIAN, Route210_South_Text_NinjaBoyFabianIntro, Route210_South_Text_NinjaBoyFabianDefeat
	msgbox Route210_South_Text_NinjaBoyFabianPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_NinjaBoyFabianIntro:
	.string "I am one of the Ninja Trio!\nBeing discovered means I must battle!$"

Route210_South_Text_NinjaBoyFabianDefeat:
	.string "I concede defeat...$"

Route210_South_Text_NinjaBoyFabianPost:
	.string "My cover is blown, so what should\nI do?\pMaybe I'll go catch some Contests in\nHearthome City. Maybe I'll do that.$"

Route210_South_EventScript_NinjaBoyBrennan::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_BRENNAN, Route210_South_Text_NinjaBoyBrennanIntro, Route210_South_Text_NinjaBoyBrennanDefeat
	msgbox Route210_South_Text_NinjaBoyBrennanPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_NinjaBoyBrennanIntro:
	.string "I am one of the Ninja Trio!\nBeing discovered means I must battle!$"

Route210_South_Text_NinjaBoyBrennanDefeat:
	.string "I concede defeat...$"

Route210_South_Text_NinjaBoyBrennanPost:
	.string "While I hid in the tall grass, I\nsensed Pokémon all around me!\pFurtive sounds of movement...\nStifled cries... I heard them!$"

Route210_South_EventScript_TwinTia::
	trainerbattle_double TRAINER_SINNOH_TWINS_TERI_AND_TIA, Route210_South_Text_TwinTiaIntro, Route210_South_Text_TwinTiaDefeat, Route210_South_Text_TwinTiaNoPartner
	msgbox Route210_South_Text_TwinTiaPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_TwinTiaIntro:
	.string "Tia: Yay!\nWe're all going to battle!$"

Route210_South_Text_TwinTiaDefeat:
	.string "Tia: We tried really hard together,\nbut we couldn't win anyway.$"

Route210_South_Text_TwinTiaPost:
	.string "Tia: When Mommy and Aunty and me\nand Teri get together, it's really\pconfusing and fun!$"

Route210_South_Text_TwinTiaNoPartner:
	.string "Tia: Um, no.\nWe all want to battle together.$"

Route210_South_EventScript_TwinTeri::
	trainerbattle_double TRAINER_SINNOH_TWINS_TERI_AND_TIA, Route210_South_Text_TwinTeriIntro, Route210_South_Text_TwinTeriDefeat, Route210_South_Text_TwinTeriNoPartner
	msgbox Route210_South_Text_TwinTeriPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_TwinTeriIntro:
	.string "Teri: Yay! We're gonna battle with\nlots of Pokémon!$"

Route210_South_Text_TwinTeriDefeat:
	.string "Teri: We tried really hard together,\nbut we lost anyway.$"

Route210_South_Text_TwinTeriPost:
	.string "Teri: Our mommy is a twin, too.$"

Route210_South_Text_TwinTeriNoPartner:
	.string "Teri: We want to battle with lots\nof Pokémon.$"

Route210_South_EventScript_NinjaBoyBruce::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_BRUCE, Route210_South_Text_NinjaBoyBruceIntro, Route210_South_Text_NinjaBoyBruceDefeat
	msgbox Route210_South_Text_NinjaBoyBrucePost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_NinjaBoyBruceIntro:
	.string "I am one of the Ninja Trio!\nBeing discovered means I must battle!\pBut how did you discover me?\nDon't tell me you're a ninja, too!$"

Route210_South_Text_NinjaBoyBruceDefeat:
	.string "I concede defeat...$"

Route210_South_Text_NinjaBoyBrucePost:
	.string "A Pokémon Trainer's good at finding\nstuff, I guess.$"

Route210_South_EventScript_BreederAmber::
	trainerbattle_single TRAINER_SINNOH_BREEDER_AMBER, Route210_South_Text_BreederAmberIntro, Route210_South_Text_BreederAmberDefeat
	msgbox Route210_South_Text_BreederAmberPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_BreederAmberIntro:
	.string "I'm a rookie breeder, but I'll do\nmy very best!$"

Route210_South_Text_BreederAmberDefeat:
	.string "It's all right!\nI'm still a rookie!$"

Route210_South_Text_BreederAmberPost:
	.string "The best way to raise Pokémon?\p...Hmm, when it comes right down to it,\nisn't it all about love?$"

Route210_South_EventScript_BelleAva::
	trainerbattle_double TRAINER_SINNOH_BELLE_AND_PA_AVA_AND_MATT, Route210_South_Text_BelleAvaIntro, Route210_South_Text_BelleAvaDefeat, Route210_South_Text_BelleAvaNoPartner
	msgbox Route210_South_Text_BelleAvaPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_BelleAvaIntro:
	.string "Ava: I can get away with slacking\noff if I have my Pokémon out!$"

Route210_South_Text_BelleAvaDefeat:
	.string "Ava: Oh, sheesh!$"

Route210_South_Text_BelleAvaPost:
	.string "Ava: Papa, I'm so sorry!\nI'll work harder from tomorrow on!\p...Yup, tomorrow's when I'm going to\nstart working.$"

Route210_South_Text_BelleAvaNoPartner:
	.string "Ava: You're battling me and my pa.\nOne Pokémon won't cut it, dear!$"

Route210_South_EventScript_PaMatt::
	trainerbattle_double TRAINER_SINNOH_BELLE_AND_PA_AVA_AND_MATT, Route210_South_Text_PaMattIntro, Route210_South_Text_PaMattDefeat, Route210_South_Text_PaMattNoPartner
	msgbox Route210_South_Text_PaMattPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_PaMattIntro:
	.string "Matt: Uhohoho! I'll show y'all how\ntightly I've bonded with my daughter!$"

Route210_South_Text_PaMattDefeat:
	.string "Matt: Parent-and-child power couldn't\nget the job done.$"

Route210_South_Text_PaMattPost:
	.string "Matt: I reckon the bonds between you\nand your Pokémon are like the bonds\pparents share with their kids.$"

Route210_South_Text_PaMattNoPartner:
	.string "Matt: Oh, there's no way you could\nbeat us both with one Pokémon.$"

Route210_South_EventScript_RancherMarco::
	trainerbattle_single TRAINER_SINNOH_RANCHER_MARCO, Route210_South_Text_RancherMarcoIntro, Route210_South_Text_RancherMarcoDefeat
	msgbox Route210_South_Text_RancherMarcoPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_RancherMarcoIntro:
	.string "My Pokémon toughened up while working\non the ranch.\pI'm right proud of them!$"

Route210_South_Text_RancherMarcoDefeat:
	.string "Hahahah! Your Pokémon sure can be\ncounted on!$"

Route210_South_Text_RancherMarcoPost:
	.string "When I cuddle with my Pokémon, I can\nfeel not just their bodies' warmth, but\ptheir compassion.$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route210_South_EventScript_BreederKahlil::
	trainerbattle_single TRAINER_SINNOH_BREEDER_KAHLIL, Route210_South_Text_BreederKahlilIntro, Route210_South_Text_BreederKahlilDefeat
	msgbox Route210_South_Text_BreederKahlilPost, MSGBOX_AUTOCLOSE
	end

Route210_South_Text_BreederKahlilIntro:
	.string "Hey, check this out! Look at the\nluster of my Pokémon's fur!$"

Route210_South_Text_BreederKahlilDefeat:
	.string "Hey, hey, did you take a good look?$"

Route210_South_Text_BreederKahlilPost:
	.string "The Veilstone Department Store is\npretty impressive!\pDid you know they even sell Poffins?$"
