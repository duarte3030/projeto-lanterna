@ Ginasio de Sinnoh com interior reaproveitado de Hoenn: o port nunca construiu
@ este predio. Ver Pokemon Claude/PLANO.md.

SnowpointCity_Gym_MapScripts::
	.byte 0

SnowpointCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_7, SnowpointCity_Gym_EventScript_JaVenceu
	msgbox SnowpointCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_CANDICE, SnowpointCity_Gym_Text_Defeat
	msgbox SnowpointCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_7
	release
	end

SnowpointCity_Gym_EventScript_JaVenceu::
	msgbox SnowpointCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

SnowpointCity_Gym_Text_Intro:
	.string "...$"

SnowpointCity_Gym_Text_Defeat:
	.string "I must say, I've warmed up to you!\nI might even admire you a little.$"

SnowpointCity_Gym_Text_Post:
	.string "...$"

SnowpointCity_Gym_Text_JaVenceu:
	.string "The ICICLE BADGE is already yours.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SnowpointCity_Gym_EventScript_Npc1::
	msgbox SnowpointCity_Gym_Text_Npc1, MSGBOX_NPC
	end

SnowpointCity_Gym_Text_Npc1:
	.string "Hey, there!\nHow's it going, Champ-to-be?\pDo you see the big snowballs placed\nhere and there?\pYou need to slide on the ice with\nenough momentum to crush them.\pThe Gym Leader is a user of\nIce-type Pokémon.\pMelt her defenses with scorching-\nhot Fire-type moves!\pIt's all about focus with this Gym.\nBear down and focus!$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

SnowpointCity_Gym_EventScript_AceTrainerAnton::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ANTON, SnowpointCity_Gym_Text_AceTrainerAntonIntro, SnowpointCity_Gym_Text_AceTrainerAntonDefeat
	msgbox SnowpointCity_Gym_Text_AceTrainerAntonPost, MSGBOX_AUTOCLOSE
	end

SnowpointCity_Gym_Text_AceTrainerAntonIntro:
	.string "We spend all our time battling in the\nblizzards of Snowpoint City.\pWe'll show you how it's toughened\nus up!$"

SnowpointCity_Gym_Text_AceTrainerAntonDefeat:
	.string "What's with your toughness?!$"

SnowpointCity_Gym_Text_AceTrainerAntonPost:
	.string "You've battled all over, you say?\nThat makes you tough, perhaps.$"

SnowpointCity_Gym_EventScript_AceTrainerSavannah::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_SAVANNAH, SnowpointCity_Gym_Text_AceTrainerSavannahIntro, SnowpointCity_Gym_Text_AceTrainerSavannahDefeat
	msgbox SnowpointCity_Gym_Text_AceTrainerSavannahPost, MSGBOX_AUTOCLOSE
	end

SnowpointCity_Gym_Text_AceTrainerSavannahIntro:
	.string "Is the Gym's trick floor making you\na little hot under the collar?\pIf you can't maintain your cool in\nbattle, you'll freeze up.$"

SnowpointCity_Gym_Text_AceTrainerSavannahDefeat:
	.string "You were surprisingly cool...\nAt least I have my warm boots.$"

SnowpointCity_Gym_Text_AceTrainerSavannahPost:
	.string "Your Pokémon look so hot in battle.\nSo hot, they're cool! Hahah!$"

SnowpointCity_Gym_EventScript_AceTrainerAlicia::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ALICIA, SnowpointCity_Gym_Text_AceTrainerAliciaIntro, SnowpointCity_Gym_Text_AceTrainerAliciaDefeat
	msgbox SnowpointCity_Gym_Text_AceTrainerAliciaPost, MSGBOX_AUTOCLOSE
	end

SnowpointCity_Gym_Text_AceTrainerAliciaIntro:
	.string "Are you feeling all run-down?\pBut a good Trainer is one who wins no\nmatter the situation!$"

SnowpointCity_Gym_Text_AceTrainerAliciaDefeat:
	.string "That's right. A good Trainer will win,\nno matter what the situation may be.$"

SnowpointCity_Gym_Text_AceTrainerAliciaPost:
	.string "The Trainer's feelings...\nThe Pokémon's feelings...\pIf they are one and the same, you\nwill never lose.$"

SnowpointCity_Gym_EventScript_AceTrainerIsaiah::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_ISAIAH, SnowpointCity_Gym_Text_AceTrainerIsaiahIntro, SnowpointCity_Gym_Text_AceTrainerIsaiahDefeat
	msgbox SnowpointCity_Gym_Text_AceTrainerIsaiahPost, MSGBOX_AUTOCLOSE
	end

SnowpointCity_Gym_Text_AceTrainerIsaiahIntro:
	.string "My willpower was shaped and tempered\nby howling blizzards.\pI'll bring it to bear on you!$"

SnowpointCity_Gym_Text_AceTrainerIsaiahDefeat:
	.string "You weren't even fazed...$"

SnowpointCity_Gym_Text_AceTrainerIsaiahPost:
	.string "I've battled countless Trainers\nand many more Pokémon still.\pMy spirit has been hardened from all\nthe battles I have fought.$"

SnowpointCity_Gym_EventScript_AceTrainerBrenna::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_BRENNA, SnowpointCity_Gym_Text_AceTrainerBrennaIntro, SnowpointCity_Gym_Text_AceTrainerBrennaDefeat
	msgbox SnowpointCity_Gym_Text_AceTrainerBrennaPost, MSGBOX_AUTOCLOSE
	end

SnowpointCity_Gym_Text_AceTrainerBrennaIntro:
	.string "I've only been involved with Pokémon\nfor a short time.\pI managed to get this far because\nskilled friends toughened me up!$"

SnowpointCity_Gym_Text_AceTrainerBrennaDefeat:
	.string "I can't believe how tough you are!$"

SnowpointCity_Gym_Text_AceTrainerBrennaPost:
	.string "If you have wonderful friends, there\nis no limit to how far you can go.$"

SnowpointCity_Gym_EventScript_AceTrainerSergio::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_SERGIO, SnowpointCity_Gym_Text_AceTrainerSergioIntro, SnowpointCity_Gym_Text_AceTrainerSergioDefeat
	msgbox SnowpointCity_Gym_Text_AceTrainerSergioPost, MSGBOX_AUTOCLOSE
	end

SnowpointCity_Gym_Text_AceTrainerSergioIntro:
	.string "...It's t-too cold.\nI can't even feel my t-tongue.$"

SnowpointCity_Gym_Text_AceTrainerSergioDefeat:
	.string "This result...\n...It's cold. Bitter cold.$"

SnowpointCity_Gym_Text_AceTrainerSergioPost:
	.string "The higher up you slide from, the\nmore speed you'll have to smash\pthose big snowballs.$"
