@ Ginasio de Sinnoh com interior reaproveitado de Hoenn: o port nunca construiu
@ este predio. Ver Pokemon Claude/PLANO.md.

CanalaveCity_Gym_MapScripts::
	.byte 0

CanalaveCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_6, CanalaveCity_Gym_EventScript_JaVenceu
	msgbox CanalaveCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_BYRON, CanalaveCity_Gym_Text_Defeat
	msgbox CanalaveCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_6
	release
	end

CanalaveCity_Gym_EventScript_JaVenceu::
	msgbox CanalaveCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

CanalaveCity_Gym_Text_Intro:
	.string "...$"

CanalaveCity_Gym_Text_Defeat:
	.string "Hmm!\nMy sturdy Pokémon, defeated!$"

CanalaveCity_Gym_Text_Post:
	.string "...$"

CanalaveCity_Gym_Text_JaVenceu:
	.string "The MINE BADGE is already yours.$"

@ Treinador do pokeplatinum que os dois scripts irmaos nao alcancam
@ (dev_scripts/treinadores_faltantes_sinnoh.py)

CanalaveCity_Gym_EventScript_WorkerGerardo::
	trainerbattle_single TRAINER_SINNOH_WORKER_GERARDO, CanalaveCity_Gym_Text_WorkerGerardoIntro, CanalaveCity_Gym_Text_WorkerGerardoDefeat
	msgbox CanalaveCity_Gym_Text_WorkerGerardoPost, MSGBOX_AUTOCLOSE
	end

CanalaveCity_Gym_Text_WorkerGerardoIntro:
	.string "Pokémon and people have worked\ntogether for many years.\pLet us show you an example of that\nhistory!$"

CanalaveCity_Gym_Text_WorkerGerardoDefeat:
	.string "A spectacular loss!\nBut it's still a loss!$"

CanalaveCity_Gym_Text_WorkerGerardoPost:
	.string "The way you helped each other...\nThat is what made you prevail!$"

CanalaveCity_Gym_EventScript_WorkerJackson::
	trainerbattle_single TRAINER_SINNOH_WORKER_JACKSON, CanalaveCity_Gym_Text_WorkerJacksonIntro, CanalaveCity_Gym_Text_WorkerJacksonDefeat
	msgbox CanalaveCity_Gym_Text_WorkerJacksonPost, MSGBOX_AUTOCLOSE
	end

CanalaveCity_Gym_Text_WorkerJacksonIntro:
	.string "Up and down you go on the lifts.\nMe? I like to battle!$"

CanalaveCity_Gym_Text_WorkerJacksonDefeat:
	.string "You've got me feeling down!$"

CanalaveCity_Gym_Text_WorkerJacksonPost:
	.string "I can't keep this up!\nI'll go back to working on the lifts.$"

CanalaveCity_Gym_EventScript_BlackBeltDavid::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_DAVID, CanalaveCity_Gym_Text_BlackBeltDavidIntro, CanalaveCity_Gym_Text_BlackBeltDavidDefeat
	msgbox CanalaveCity_Gym_Text_BlackBeltDavidPost, MSGBOX_AUTOCLOSE
	end

CanalaveCity_Gym_Text_BlackBeltDavidIntro:
	.string "Aiyaah! We're coming out swinging\nwith super-heavy judo chops!$"

CanalaveCity_Gym_Text_BlackBeltDavidDefeat:
	.string "That was...\nA complete trashing!$"

CanalaveCity_Gym_Text_BlackBeltDavidPost:
	.string "I must rededicate myself to training.\nThe road extends into infinity...$"

CanalaveCity_Gym_EventScript_BlackBeltRicky::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_RICKY, CanalaveCity_Gym_Text_BlackBeltRickyIntro, CanalaveCity_Gym_Text_BlackBeltRickyDefeat
	msgbox CanalaveCity_Gym_Text_BlackBeltRickyPost, MSGBOX_AUTOCLOSE
	end

CanalaveCity_Gym_Text_BlackBeltRickyIntro:
	.string "Steel represents an unbending spirit!\pIf one refuses to accept defeat,\nthe path to victory reveals itself!$"

CanalaveCity_Gym_Text_BlackBeltRickyDefeat:
	.string "I never gave up, but still I failed to\nwin...$"

CanalaveCity_Gym_Text_BlackBeltRickyPost:
	.string "If you give up, well, that's when\neverything ends for you!$"

CanalaveCity_Gym_EventScript_WorkerGary::
	trainerbattle_single TRAINER_SINNOH_WORKER_GARY, CanalaveCity_Gym_Text_WorkerGaryIntro, CanalaveCity_Gym_Text_WorkerGaryDefeat
	msgbox CanalaveCity_Gym_Text_WorkerGaryPost, MSGBOX_AUTOCLOSE
	end

CanalaveCity_Gym_Text_WorkerGaryIntro:
	.string "A Pokémon Gym isn't only about seeing\nhow tough your Pokémon happen to be.\pIt's so much deeper than just that.\nIt's a test of you as a person.$"

CanalaveCity_Gym_Text_WorkerGaryDefeat:
	.string "That move was devastating!$"

CanalaveCity_Gym_Text_WorkerGaryPost:
	.string "I get to work all day with my\nPokémon, and even battle sometimes.\pI get all the fun I need every day!$"

CanalaveCity_Gym_EventScript_AceTrainerBreanna::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_BREANNA, CanalaveCity_Gym_Text_AceTrainerBreannaIntro, CanalaveCity_Gym_Text_AceTrainerBreannaDefeat
	msgbox CanalaveCity_Gym_Text_AceTrainerBreannaPost, MSGBOX_AUTOCLOSE
	end

CanalaveCity_Gym_Text_AceTrainerBreannaIntro:
	.string "By focusing on only one type, you can\nreally see the strengths and\pweaknesses of that Pokémon.$"

CanalaveCity_Gym_Text_AceTrainerBreannaDefeat:
	.string "My focus was too narrow minded...$"

CanalaveCity_Gym_Text_AceTrainerBreannaPost:
	.string "Start by becoming friendly with your\nPokémon. I mean really friendly.\pIf you do that, you'll learn naturally\nhow you should battle with it.$"

CanalaveCity_Gym_EventScript_AceTrainerCesar::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_CESAR, CanalaveCity_Gym_Text_AceTrainerCesarIntro, CanalaveCity_Gym_Text_AceTrainerCesarDefeat
	msgbox CanalaveCity_Gym_Text_AceTrainerCesarPost, MSGBOX_AUTOCLOSE
	end

CanalaveCity_Gym_Text_AceTrainerCesarIntro:
	.string "An ace has the knowledge and\nexperience of battling at high levels.\pI'll demonstrate what that means to\na noob like you!$"

CanalaveCity_Gym_Text_AceTrainerCesarDefeat:
	.string "Wow...\nI'm in the mood to sing a lullaby...$"

CanalaveCity_Gym_Text_AceTrainerCesarPost:
	.string "Your earnest enthusiasm...\nI guess that kinda makes you an ace.\pMaybe you're a Trainer who has the\npotential to surpass aces!$"
