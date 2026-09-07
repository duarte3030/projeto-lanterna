MtCoronet_B1F_MapScripts::
	.byte 0

MtCoronet_B1F_EventScript_Hiker1::
	msgbox MtCoronet_B1F_Text_Hiker1, MSGBOX_NPC
	end

MtCoronet_B1F_EventScript_Hiker2::
	msgbox MtCoronet_B1F_Text_Hiker2, MSGBOX_NPC
	end

MtCoronet_B1F_Text_Hiker1:
	.string "This mountain runs deep.\p"
	.string "I've heard there are passages\n"
	.string "nobody's mapped yet.$"

MtCoronet_B1F_Text_Hiker2:
	.string "The lake down here stays cold\n"
	.string "year-round.\p"
	.string "Wouldn't recommend a swim.$"

@ Historia: mais um posto da Galactica no caminho para o norte.
@ Texto de pret/pokeplatinum, res/text/mt_coronet_1f_tunnel_room.json.

MtCoronet_B1F_EventScript_GalacticGrunt::
	trainerbattle_single TRAINER_SINNOH_GALACTIC_GRUNT_MT_CORONET_TUNNEL_ROOM_3, MtCoronet_B1F_Text_GruntIntro, MtCoronet_B1F_Text_GruntDefeat
	msgbox MtCoronet_B1F_Text_GruntPostBattle, MSGBOX_AUTOCLOSE
	end

MtCoronet_B1F_Text_GruntIntro:
	.string "Turn back. Team Galactic is using\n"
	.string "this tunnel.$"

MtCoronet_B1F_Text_GruntDefeat:
	.string "Yeah, right!\n"
	.string "You're absolutely right!$"

MtCoronet_B1F_Text_GruntPostBattle:
	.string "The others went on ahead, up to\n"
	.string "the peak.\p"
	.string "I'm just a lowly grunt.\n"
	.string "Nobody tells me anything.$"

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
MtCoronet_B1F_EventScript_Heatran::
	lockall
	msgbox MtCoronet_B1F_Text_HeatranIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_HEATRAN, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_HEATRAN, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_MT_CORONET_B1_F_HEATRAN
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_HeatranSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_HeatranPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
MtCoronet_B1F_EventScript_HeatranPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_MT_CORONET_B1_F_HEATRAN
	setflag FLAG_HIDE_HEATRAN_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_EventScript_HeatranSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_MT_CORONET_B1_F_HEATRAN
	setflag FLAG_HIDE_HEATRAN_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox MtCoronet_B1F_Text_HeatranSome, MSGBOX_DEFAULT
	return

MtCoronet_B1F_Text_HeatranIntro:
	.string "A furnace heat wells up from the\nbottom of the mountain...$"

MtCoronet_B1F_Text_HeatranSome:
	.string "HEATRAN sank back into the rock...$"

@ <<< Lendarios de Sinnoh <<<

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
MtCoronet_B1F_EventScript_DexReshiram::
	lockall
	msgbox MtCoronet_B1F_Text_DexReshiramIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_RESHIRAM, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_RESHIRAM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_RESHIRAM
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexReshiramSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexReshiramSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexReshiramSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_RESHIRAM
	setflag FLAG_HIDE_DEX_RESHIRAM
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexReshiramIntro:
	.string "RESHIRAM appeared!$"

MtCoronet_B1F_EventScript_DexZekrom::
	lockall
	msgbox MtCoronet_B1F_Text_DexZekromIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZEKROM, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZEKROM, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ZEKROM
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexZekromSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexZekromSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexZekromSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ZEKROM
	setflag FLAG_HIDE_DEX_ZEKROM
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexZekromIntro:
	.string "ZEKROM appeared!$"

MtCoronet_B1F_EventScript_DexLandorusIncarnate::
	lockall
	msgbox MtCoronet_B1F_Text_DexLandorusIncarnateIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexLandorusIncarnateSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexLandorusIncarnateSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexLandorusIncarnateSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_LANDORUS_INCARNATE
	setflag FLAG_HIDE_DEX_LANDORUS_INCARNATE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexLandorusIncarnateIntro:
	.string "LANDORUS_INCARNATE appeared!$"

MtCoronet_B1F_EventScript_DexKyurem::
	lockall
	msgbox MtCoronet_B1F_Text_DexKyuremIntro, MSGBOX_DEFAULT
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
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexKyuremSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexKyuremSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexKyuremSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KYUREM
	setflag FLAG_HIDE_DEX_KYUREM
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexKyuremIntro:
	.string "KYUREM appeared!$"

MtCoronet_B1F_EventScript_DexKyuremBlack::
	lockall
	msgbox MtCoronet_B1F_Text_DexKyuremBlackIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KYUREM_BLACK, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KYUREM_BLACK, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_KYUREM_BLACK
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexKyuremBlackSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexKyuremBlackSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexKyuremBlackSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KYUREM_BLACK
	setflag FLAG_HIDE_DEX_KYUREM_BLACK
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexKyuremBlackIntro:
	.string "KYUREM_BLACK appeared!$"

MtCoronet_B1F_EventScript_DexKyuremWhite::
	lockall
	msgbox MtCoronet_B1F_Text_DexKyuremWhiteIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_KYUREM_WHITE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_KYUREM_WHITE, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_KYUREM_WHITE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexKyuremWhiteSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexKyuremWhiteSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexKyuremWhiteSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_KYUREM_WHITE
	setflag FLAG_HIDE_DEX_KYUREM_WHITE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexKyuremWhiteIntro:
	.string "KYUREM_WHITE appeared!$"

MtCoronet_B1F_EventScript_DexZygarde50::
	lockall
	msgbox MtCoronet_B1F_Text_DexZygarde50Intro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ZYGARDE_50, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ZYGARDE_50, 70
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ZYGARDE_50
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexZygarde50Some
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexZygarde50Some
	releaseall
	end

MtCoronet_B1F_EventScript_DexZygarde50Some::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ZYGARDE_50
	setflag FLAG_HIDE_DEX_ZYGARDE_50
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexZygarde50Intro:
	.string "ZYGARDE_50 appeared!$"

MtCoronet_B1F_EventScript_DexVolcanion::
	lockall
	msgbox MtCoronet_B1F_Text_DexVolcanionIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_VOLCANION, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_VOLCANION, 30
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_VOLCANION
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexVolcanionSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexVolcanionSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexVolcanionSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_VOLCANION
	setflag FLAG_HIDE_DEX_VOLCANION
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexVolcanionIntro:
	.string "VOLCANION appeared!$"

MtCoronet_B1F_EventScript_DexNihilego::
	lockall
	msgbox MtCoronet_B1F_Text_DexNihilegoIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_NIHILEGO, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_NIHILEGO, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_NIHILEGO
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexNihilegoSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexNihilegoSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexNihilegoSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_NIHILEGO
	setflag FLAG_HIDE_DEX_NIHILEGO
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexNihilegoIntro:
	.string "NIHILEGO appeared!$"

MtCoronet_B1F_EventScript_DexBuzzwole::
	lockall
	msgbox MtCoronet_B1F_Text_DexBuzzwoleIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_BUZZWOLE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_BUZZWOLE, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_BUZZWOLE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexBuzzwoleSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexBuzzwoleSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexBuzzwoleSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_BUZZWOLE
	setflag FLAG_HIDE_DEX_BUZZWOLE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexBuzzwoleIntro:
	.string "BUZZWOLE appeared!$"

MtCoronet_B1F_EventScript_DexPheromosa::
	lockall
	msgbox MtCoronet_B1F_Text_DexPheromosaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_PHEROMOSA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_PHEROMOSA, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_PHEROMOSA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexPheromosaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexPheromosaSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexPheromosaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_PHEROMOSA
	setflag FLAG_HIDE_DEX_PHEROMOSA
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexPheromosaIntro:
	.string "PHEROMOSA appeared!$"

MtCoronet_B1F_EventScript_DexXurkitree::
	lockall
	msgbox MtCoronet_B1F_Text_DexXurkitreeIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_XURKITREE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_XURKITREE, 60
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_XURKITREE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, MtCoronet_B1F_EventScript_DexXurkitreeSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, MtCoronet_B1F_EventScript_DexXurkitreeSome
	releaseall
	end

MtCoronet_B1F_EventScript_DexXurkitreeSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_XURKITREE
	setflag FLAG_HIDE_DEX_XURKITREE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

MtCoronet_B1F_Text_DexXurkitreeIntro:
	.string "XURKITREE appeared!$"

@ <<< Dex completa <<<
