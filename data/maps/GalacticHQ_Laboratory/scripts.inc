@ QG da Galactica, laboratorio: onde a Corrente Vermelha foi feita.
@ Texto de pret/pokeplatinum, res/text/galactic_hq_laboratory.json.
@ Layout emprestado do Museu Oceanico de Slateport.

GalacticHQ_Laboratory_MapScripts::
	.byte 0

GalacticHQ_Laboratory_EventScript_Scientist1::
	msgbox GalacticHQ_Laboratory_Text_ExperimentWentTooFar, MSGBOX_NPC
	end

GalacticHQ_Laboratory_EventScript_Scientist2::
	msgbox GalacticHQ_Laboratory_Text_IFeelTooSickened, MSGBOX_NPC
	end

GalacticHQ_Laboratory_EventScript_GreenFluid::
	msgbox GalacticHQ_Laboratory_Text_SomethingInGreenFluid, MSGBOX_SIGN
	end

GalacticHQ_Laboratory_Text_ExperimentWentTooFar:
	.string "I feel awful about what we did...\n"
	.string "This experiment went too far...\p"
	.string "I'm not sure if I can stomach what\n"
	.string "Master Cyrus plans...$"

GalacticHQ_Laboratory_Text_IFeelTooSickened:
	.string "Urff...\n"
	.string "I feel too sickened to say\l"
	.string "anything...\p"
	.string "But that thing we made...\n"
	.string "What is it going to be used for?$"

GalacticHQ_Laboratory_Text_SomethingInGreenFluid:
	.string "There is something suspended in\n"
	.string "a green fluid...$"
