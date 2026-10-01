@ Treinadores de rota de IlexForest, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

IlexForest_MapScripts::
	.byte 0

IlexForest_EventScript_BugcatcherWayne::
	trainerbattle_single TRAINER_JOHTO_WAYNE, IlexForest_Text_BugcatcherWayneSeen, IlexForest_Text_BugcatcherWayneBeaten
	msgbox IlexForest_Text_BugcatcherWayneAfter, MSGBOX_AUTOCLOSE
	end

IlexForest_Text_BugcatcherWayneSeen:
	.string "Don't sneak up on me like that!\p"
	.string "You frightened a POKéMON away!$"

IlexForest_Text_BugcatcherWayneBeaten:
	.string "I hadn't seen that POKéMON before…$"

IlexForest_Text_BugcatcherWayneAfter:
	.string "A POKéMON I've never seen before\n"
	.string "fell out of the tree when I used\l"
	.string "HEADBUTT.\p"
	.string "I ought to use HEADBUTT in other\n"
	.string "places too.$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

IlexForest_EventScript_Sign::
	lock
	msgbox IlexForest_Text_Signpost MSGBOX_SIGN
	closemessage
	release
	end

IlexForest_Text_Signpost::
	.string "ILEX FOREST is so overgrown with\n"
	.string "trees that you can't see the sky.\p"
	.string "Please watch out for items that may\n"
	.string "have been dropped.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

IlexForest_EventScript_Picnicker::
	lock
	faceplayer
	msgbox IlexForest_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

IlexForest_Text_Lass::
	.string "Did something happen to the\n"
	.string "forest's guardian?$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

IlexForest_EventScript_Boss::
	lock
	faceplayer
	msgbox IlexForest_Text_CharcoalMasterTalkAfter, MSGBOX_DEFAULT
	closemessage
	release
	end

IlexForest_Text_CharcoalMasterTalkAfter::
	.string "Do you want to apprentice as a\n"
	.string "charcoal maker with me?\p"
	.string "You'll be first-rate in ten years!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
IlexForest_EventScript_DexCelebi::
	lockall
	msgbox IlexForest_Text_DexCelebiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CELEBI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CELEBI, 55
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_CELEBI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_DexCelebiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_DexCelebiSome
	releaseall
	end

IlexForest_EventScript_DexCelebiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_CELEBI
	setflag FLAG_HIDE_DEX_CELEBI
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IlexForest_Text_DexCelebiIntro:
	.string "CELEBI appeared!$"

IlexForest_EventScript_DexArceusGrass::
	lockall
	msgbox IlexForest_Text_DexArceusGrassIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_ARCEUS_GRASS, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_ARCEUS_GRASS, 55
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_ARCEUS_GRASS
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, IlexForest_EventScript_DexArceusGrassSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, IlexForest_EventScript_DexArceusGrassSome
	releaseall
	end

IlexForest_EventScript_DexArceusGrassSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_ARCEUS_GRASS
	setflag FLAG_HIDE_DEX_ARCEUS_GRASS
	fadescreenswapbuffers FADE_FROM_BLACK
	return

IlexForest_Text_DexArceusGrassIntro:
	.string "ARCEUS_GRASS appeared!$"

@ <<< Dex completa <<<

@ Placas e mecanica portadas do hns por completa_placas_johto.py
IlexForest_Text_Shrine:
	.string "ILEX FOREST SHRINE…\p"
	.string "It's in honor of the forest's\n"
	.string "protector…$"
IlexForest_EventScript_Santuario::
	lock
	msgbox IlexForest_Text_Shrine, MSGBOX_DEFAULT
	closemessage
	release
	end
