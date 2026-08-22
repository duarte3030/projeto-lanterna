@ GiantChasmB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_GiantChasmB1F_MapScripts::
	.byte 0

Unova_GiantChasmB1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_GIANT_CHASM, Unova_GiantChasmB1F_Text_BackpackerMGiantChasmSeenText, Unova_GiantChasmB1F_Text_BackpackerMGiantChasmBeatenText
	end

Unova_GiantChasmB1F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_GIANT_CHASM, Unova_GiantChasmB1F_Text_BackpackerFGiantChasmSeenText, Unova_GiantChasmB1F_Text_BackpackerFGiantChasmBeatenText
	end

Unova_GiantChasmB1F_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_GIANT_CHASM, Unova_GiantChasmB1F_Text_AceTrainerFGiantChasmSeenText, Unova_GiantChasmB1F_Text_AceTrainerFGiantChasmBeatenText
	end

Unova_GiantChasmB1F_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_GIANT_CHASM, Unova_GiantChasmB1F_Text_AceTrainerMGiantChasmSeenText, Unova_GiantChasmB1F_Text_AceTrainerMGiantChasmBeatenText
	end

Unova_GiantChasmB1F_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_HIKER_GIANT_CHASM, Unova_GiantChasmB1F_Text_HikerGiantChasmSeenText, Unova_GiantChasmB1F_Text_HikerGiantChasmBeatenText
	end


Unova_GiantChasmB1F_Text_BackpackerMGiantChasmSeenText::
	.string "What's this? A"
	.string "\nvisitor? Ooh, I'm"
	.string "\pso happy to meet"
	.string "\nsomeone else here!"
	.string "\pCould I ask you to"
	.string "\nbe my opponent?$"

Unova_GiantChasmB1F_Text_BackpackerMGiantChasmBeatenText::
	.string "There is a certain"
	.string "\nthrill to battling"
	.string "\lanother trainer!$"

Unova_GiantChasmB1F_Text_BackpackerFGiantChasmSeenText::
	.string "I may be a BACK-"
	.string "\nPACKER, but I'm"
	.string "\palso a treasure"
	.string "\nhunter!$"

Unova_GiantChasmB1F_Text_BackpackerFGiantChasmBeatenText::
	.string "I missed that"
	.string "\nelusive treasure"
	.string "\lcalled victory.$"

Unova_GiantChasmB1F_Text_AceTrainerFGiantChasmSeenText::
	.string "Have you ever"
	.string "\nnoticed the stone"
	.string "\lcones in the cave?$"

Unova_GiantChasmB1F_Text_AceTrainerFGiantChasmBeatenText::
	.string "That marvelous"
	.string "\npower of yours! I"
	.string "\lwasn't aware!$"

Unova_GiantChasmB1F_Text_AceTrainerMGiantChasmSeenText::
	.string "Let's train! We'll"
	.string "\nget stronger with"
	.string "\lour POKéMON!$"

Unova_GiantChasmB1F_Text_AceTrainerMGiantChasmBeatenText::
	.string "Not yet! I still"
	.string "\nhaven't shared my"
	.string "\ltrue strength!$"

Unova_GiantChasmB1F_Text_HikerGiantChasmSeenText::
	.string "Hi-ho!$"

Unova_GiantChasmB1F_Text_HikerGiantChasmBeatenText::
	.string "Hi-ho…$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

Unova_EventScript_GrutaTier3::
	lockall
	msgbox Unova_Text_AchouGruta, MSGBOX_DEFAULT
	randomelement ITEM_DAMP_ROCK, ITEM_DAMP_ROCK, ITEM_HEAT_ROCK, ITEM_HEAT_ROCK, ITEM_SMOOTH_ROCK, ITEM_SMOOTH_ROCK, ITEM_ICY_ROCK, ITEM_ICY_ROCK, ITEM_PROTEIN, ITEM_IRON, ITEM_CARBOS, ITEM_CALCIUM, ITEM_PP_UP, ITEM_MAX_ELIXIR, ITEM_MAX_REVIVE, ITEM_RARE_CANDY
	giveitem VAR_RESULT
	releaseall
	end

Unova_EventScript_GrutaVazia::
	msgbox Unova_Text_GrutaVazia, MSGBOX_SIGN
	end

Unova_Text_GrutaVazia::
	.string "There's nothing\n"
	.string "here anymore.$"

Unova_Text_AchouGruta::
	.string "Hey! It's a\n"
	.string "hidden grotto!$"

@ Gruta escondida do BW3G (tier 3). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_GiantChasmB1F_EventScript_Gruta4B4::
	goto_if_set FLAG_UNOVA_GRUTA_GIANTCHASMB1F, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_GIANTCHASMB1F
	goto Unova_EventScript_GrutaTier3

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
Unova_GiantChasmB1F_EventScript_DexLandorusIncarnate::
	lockall
	msgbox Unova_GiantChasmB1F_Text_DexLandorusIncarnateIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_LANDORUS_INCARNATE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_LANDORUS_INCARNATE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_LANDORUS_INCARNATE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_GiantChasmB1F_EventScript_DexLandorusIncarnateSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_GiantChasmB1F_EventScript_DexLandorusIncarnateSome
	releaseall
	end

Unova_GiantChasmB1F_EventScript_DexLandorusIncarnateSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_LANDORUS_INCARNATE
	setflag FLAG_HIDE_DEX_LANDORUS_INCARNATE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_GiantChasmB1F_Text_DexLandorusIncarnateIntro:
	.string "LANDORUS_INCARNATE appeared!$"

Unova_GiantChasmB1F_EventScript_DexKyurem::
	lockall
	msgbox Unova_GiantChasmB1F_Text_DexKyuremIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KYUREM, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KYUREM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_KYUREM
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, Unova_GiantChasmB1F_EventScript_DexKyuremSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, Unova_GiantChasmB1F_EventScript_DexKyuremSome
	releaseall
	end

Unova_GiantChasmB1F_EventScript_DexKyuremSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KYUREM
	setflag FLAG_HIDE_DEX_KYUREM
	fadescreenswapbuffers FADE_FROM_BLACK
	return

Unova_GiantChasmB1F_Text_DexKyuremIntro:
	.string "KYUREM appeared!$"

@ <<< Dex completa <<<
