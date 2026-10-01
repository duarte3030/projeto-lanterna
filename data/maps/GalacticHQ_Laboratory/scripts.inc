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

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
GalacticHQ_Laboratory_EventScript_DexGenesectChill::
	lockall
	msgbox GalacticHQ_Laboratory_Text_DexGenesectChillIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_GENESECT_CHILL, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_GENESECT_CHILL, 75
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_GENESECT_CHILL
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, GalacticHQ_Laboratory_EventScript_DexGenesectChillSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, GalacticHQ_Laboratory_EventScript_DexGenesectChillSome
	releaseall
	end

GalacticHQ_Laboratory_EventScript_DexGenesectChillSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_GENESECT_CHILL
	setflag FLAG_HIDE_DEX_GENESECT_CHILL
	fadescreenswapbuffers FADE_FROM_BLACK
	return

GalacticHQ_Laboratory_Text_DexGenesectChillIntro:
	.string "GENESECT_CHILL appeared!$"

@ <<< Dex completa <<<
