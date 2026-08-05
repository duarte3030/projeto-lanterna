@ QG da Galactica, 3F: as portas trancadas e a descida para os subsolos.
@ Texto de pret/pokeplatinum, res/text/galactic_hq_3f.json.
@ Layout emprestado do estaleiro do Stern, em Slateport.
@
@ ponytail: no Platinum a porta do fundo exige a Galactic Key, e agora exige aqui
@ tambem. O KeyGrunt saiu de (4,2), onde so falava, para (3,2), que e o unico
@ tile de acesso a escada de (3,1) para os subsolos. Mostrar ITEM_GALACTIC_KEY
@ faz ele sair da frente; FLAG_GALACTICA_QG_CHAVE (a mesma que a Poke Ball do 2F
@ liga) impede que ele volte. Chave unica para as duas portas, como no original.

GalacticHQ_3F_MapScripts::
	.byte 0

GalacticHQ_3F_EventScript_Grunt1::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_3F_1, GalacticHQ_3F_Text_Grunt1Intro, GalacticHQ_3F_Text_Grunt1Defeat
	msgbox GalacticHQ_3F_Text_TeamGalacticCredo, MSGBOX_AUTOCLOSE
	end

GalacticHQ_3F_EventScript_Grunt2::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_3F_2, GalacticHQ_3F_Text_Grunt2Intro, GalacticHQ_3F_Text_Grunt2Defeat
	msgbox GalacticHQ_3F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

GalacticHQ_3F_EventScript_Grunt3::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_3F_3, GalacticHQ_3F_Text_Grunt3Intro, GalacticHQ_3F_Text_Grunt3Defeat
	msgbox GalacticHQ_3F_Text_Grunt3PostBattle, MSGBOX_AUTOCLOSE
	end

GalacticHQ_3F_EventScript_Grunt4::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_3F_4, GalacticHQ_3F_Text_Grunt4Intro, GalacticHQ_3F_Text_Grunt4Defeat
	msgbox GalacticHQ_3F_Text_TeamGalacticCredo, MSGBOX_AUTOCLOSE
	end

GalacticHQ_3F_EventScript_KeyGrunt::
	lock
	faceplayer
	checkitem ITEM_GALACTIC_KEY
	goto_if_eq VAR_RESULT, FALSE, GalacticHQ_3F_EventScript_KeyGruntNoKey
	msgbox GalacticHQ_3F_Text_SoTheKeyIsGone, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_GALACTIC_HQ_3F_KEY_GRUNT, GalacticHQ_3F_Movement_StepAside
	waitmovement 0
	removeobject LOCALID_GALACTIC_HQ_3F_KEY_GRUNT
	release
	end

GalacticHQ_3F_EventScript_KeyGruntNoKey::
	msgbox GalacticHQ_3F_Text_DoorsOpenWithSpecialKey, MSGBOX_DEFAULT
	release
	end

GalacticHQ_3F_Movement_StepAside:
	walk_right
	walk_right
	step_end

GalacticHQ_3F_EventScript_Credo::
	msgbox GalacticHQ_3F_Text_TeamGalacticCredo, MSGBOX_SIGN
	end

GalacticHQ_3F_Text_Grunt1Intro:
	.string "How did you even get up here?\n"
	.string "This floor is off limits!$"

GalacticHQ_3F_Text_Grunt1Defeat:
	.string "Off limits, I said...$"

GalacticHQ_3F_Text_Grunt2Intro:
	.string "The locked doors are locked for a\n"
	.string "reason. Turn around!$"

GalacticHQ_3F_Text_Grunt2Defeat:
	.string "Fine. Go and look.$"

GalacticHQ_3F_Text_Grunt2PostBattle:
	.string "The door is locked.\n"
	.string "A special key is needed.$"

GalacticHQ_3F_Text_Grunt3Intro:
	.string "Team Galactic will take everything\n"
	.string "that can be taken.\p"
	.string "Starting with your Pokémon!$"

GalacticHQ_3F_Text_Grunt3Defeat:
	.string "I took nothing at all...$"

GalacticHQ_3F_Text_Grunt3PostBattle:
	.string "The door opened.\n"
	.string "Go down if you dare.$"

GalacticHQ_3F_Text_Grunt4Intro:
	.string "You are not going any further.\n"
	.string "Master Cyrus gave the order!$"

GalacticHQ_3F_Text_Grunt4Defeat:
	.string "I could not stop one kid...$"

GalacticHQ_3F_Text_DoorsOpenWithSpecialKey:
	.string "The locked doors only open with\n"
	.string "a special key.\p"
	.string "Now, if I was a comedy relief sort\n"
	.string "of bad guy, I'd tell you...\p"
	.string "But I really don't know!$"

GalacticHQ_3F_Text_SoTheKeyIsGone:
	.string "These doors only open with a\n"
	.string "special key, and...\p"
	.string "...and you are holding it.\p"
	.string "How? Who let a kid get hold of\n"
	.string "the Galactic Key?$"

GalacticHQ_3F_Text_TeamGalacticCredo:
	.string "The Team Galactic credo!\n"
	.string "Everything belongs to Team\l"
	.string "Galactic!\p"
	.string "Look beyond the world, space will\n"
	.string "become Team Galactic's!$"
