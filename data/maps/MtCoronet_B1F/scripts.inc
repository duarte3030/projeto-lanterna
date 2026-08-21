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
