@ Quartel-general da Equipe Galactica, em Veilstone. Saguao de entrada.
@ Texto de pret/pokeplatinum, res/text/galactic_hq_1f.json.
@
@ ponytail: layout emprestado do saguao do Concurso de Lilycove. As duas portas
@ do fundo ja existem no map.bin de Hoenn, entao warp nenhum foi inventado:
@ (9,1) leva ao salao (a "porta ao lado do balcao de recepcao" que o grunt do
@ B2F menciona) e (21,1) leva ao 2F. Zero flag e zero var: quem lembra que o
@ grunt caiu e a flag de treinador que o jogo ja grava.

GalacticHQ_1F_MapScripts::
	.byte 0

GalacticHQ_1F_EventScript_Receptionist1::
	lock
	faceplayer
	goto_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, GalacticHQ_1F_EventScript_Receptionist1NoPlans
	msgbox GalacticHQ_1F_Text_CosmicEnergy, MSGBOX_DEFAULT
	release
	end

GalacticHQ_1F_EventScript_Receptionist1NoPlans::
	msgbox GalacticHQ_1F_Text_WeHaveNoPlansNow, MSGBOX_DEFAULT
	release
	end

GalacticHQ_1F_EventScript_Receptionist2::
	msgbox GalacticHQ_1F_Text_GalacticConductsRnD, MSGBOX_NPC
	end

GalacticHQ_1F_EventScript_DoorGrunt::
	msgbox GalacticHQ_1F_Text_ThisIsWhereWeWork, MSGBOX_NPC
	end

GalacticHQ_1F_EventScript_RndGrunt::
	lock
	faceplayer
	goto_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, GalacticHQ_1F_EventScript_NothingLeft
	msgbox GalacticHQ_1F_Text_WeWillTakeEverything, MSGBOX_DEFAULT
	release
	end

GalacticHQ_1F_EventScript_NothingLeft::
	msgbox GalacticHQ_1F_Text_NothingLeftNow, MSGBOX_DEFAULT
	release
	end

GalacticHQ_1F_EventScript_Grunt::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_GALACTIC_HQ_1F, GalacticHQ_1F_Text_GruntIntro, GalacticHQ_1F_Text_GruntDefeat
	msgbox GalacticHQ_1F_Text_YoureTooYoung, MSGBOX_AUTOCLOSE
	end

GalacticHQ_1F_EventScript_Credo::
	msgbox GalacticHQ_1F_Text_TeamGalacticCredo, MSGBOX_SIGN
	end

GalacticHQ_1F_Text_CosmicEnergy:
	.string "Welcome.\n"
	.string "This is Team Galactic Headqu...\p"
	.string "I am sorry, this is the Galactic\n"
	.string "Veilstone Building.\p"
	.string "Cosmic energy for the win!\p"
	.string "Wouldn't it be wonderful if we\n"
	.string "could harness that boundless\l"
	.string "energy?$"

GalacticHQ_1F_Text_WeHaveNoPlansNow:
	.string "Welcome.\n"
	.string "This is Team Galactic Headqu...\p"
	.string "I am sorry, this is the Galactic\n"
	.string "Veilstone Building.\p"
	.string "I'm not certain if it's a good\n"
	.string "thing or not, but we have no\l"
	.string "plans now.$"

GalacticHQ_1F_Text_GalacticConductsRnD:
	.string "Team Galactic conducts R&D around\n"
	.string "the clock here.\p"
	.string "We focus on the development of\n"
	.string "new energy resources.$"

GalacticHQ_1F_Text_ThisIsWhereWeWork:
	.string "This is where we, Team Galactic,\n"
	.string "work. What are we supposed to do?\p"
	.string "I'm not sure how, but we're\n"
	.string "supposed to chase our dream.\p"
	.string "Our dream of making a wonderful\n"
	.string "new world!$"

GalacticHQ_1F_Text_WeWillTakeEverything:
	.string "We, Team Galactic, will take\n"
	.string "everything that can be taken!\p"
	.string "We will eliminate everything that\n"
	.string "is not needed!\p"
	.string "That is Team Galactic's policy!$"

GalacticHQ_1F_Text_NothingLeftNow:
	.string "We, Team Galactic, will take\n"
	.string "everything that can be taken!\p"
	.string "We will eliminate everything that\n"
	.string "is not needed!\p"
	.string "That is Team Galactic's policy!\p"
	.string "At least it used to be.\n"
	.string "There's nothing left now...$"

GalacticHQ_1F_Text_GruntIntro:
	.string "You're too young for us...\n"
	.string "You can join us when you're older.$"

GalacticHQ_1F_Text_GruntDefeat:
	.string "I wonder where our boss went...$"

GalacticHQ_1F_Text_YoureTooYoung:
	.string "I wonder where our boss went...$"

GalacticHQ_1F_Text_TeamGalacticCredo:
	.string "The Team Galactic credo!\n"
	.string "Everything belongs to Team\l"
	.string "Galactic!\p"
	.string "Look beyond the world, space will\n"
	.string "become Team Galactic's!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

GalacticHQ_1F_EventScript_Npc1::
	msgbox GalacticHQ_1F_Text_Npc1, MSGBOX_NPC
	end

GalacticHQ_1F_Text_Npc1:
	.string "Welcome.\nThis is Team Galactic Headqu...\pI'm sorry, this is the Galactic\nVeilstone Building.\pCosmic energy for the win!\pWouldn't it be wonderful if we\ncould harness that boundless energy?$"

GalacticHQ_1F_EventScript_Npc2::
	msgbox GalacticHQ_1F_Text_Npc2, MSGBOX_NPC
	end

GalacticHQ_1F_Text_Npc2:
	.string "Team Galactic conducts R&D around\nthe clock here.\pWe focus on the development of new\nenergy resources.$"

GalacticHQ_1F_EventScript_Npc3::
	msgbox GalacticHQ_1F_Text_Npc3, MSGBOX_NPC
	end

GalacticHQ_1F_Text_Npc3:
	.string "You're too young for us...\nYou can join us when you're older.$"

GalacticHQ_1F_EventScript_Npc4::
	msgbox GalacticHQ_1F_Text_Npc4, MSGBOX_NPC
	end

GalacticHQ_1F_Text_Npc4:
	.string "We, Team Galactic, will take everything\nthat can be taken!\pWe will eliminate everything that is\nnot needed!\pThat is Team Galactic's policy!$"

GalacticHQ_1F_EventScript_Placa5::
	msgbox GalacticHQ_1F_Text_Placa5, MSGBOX_SIGN
	end

GalacticHQ_1F_Text_Placa5:
	.string "The Team Galactic credo!\nEverything belongs to Team Galactic!\pLook beyond the world--space will\nbecome Team Galactic's!$"
