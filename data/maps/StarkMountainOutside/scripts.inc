StarkMountainOutside_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S7: cena da fonte, rotulo StarkMountainOutside_CoordEvent_Grunts >>>
@ Os dois grunts (OBJ_EVENT_GFX_MAGMA_MEMBER_M, mesmo molde ja usado em
@ ValorLakefront/EternaCity) ja nascem visiveis (fonte nao clearflag/
@ addobject aqui); FLAG_HIDE_STARK_MOUNTAIN_OUTSIDE_GRUNTS ja esta no censo
@ do S1, mas como o grupo so tem 2 objetos e os dois somem juntos no fecho
@ desta MESMA cena, a flag entra so no `setflag` final (setflag ANTES de
@ removeobject).
StarkMountainOutside_EventScript_CoordEvent_Grunts::
	lockall
	applymovement LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_1, StarkMountainOutside_Movement_GruntM1Enter
	applymovement LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_2, StarkMountainOutside_Movement_GruntM2Enter
	waitmovement 0
	msgbox StarkMountainOutside_Text_LetsDoThis, MSGBOX_DEFAULT
	applymovement LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_1, StarkMountainOutside_Movement_GruntM1WalkToEntrance
	applymovement LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_2, StarkMountainOutside_Movement_GruntM2WalkToEntrance
	waitmovement 0
	applymovement LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_2, StarkMountainOutside_Movement_GruntM2WalkOnSpotEast
	waitmovement 0
	msgbox StarkMountainOutside_Text_CanHeReplaceCyrus, MSGBOX_DEFAULT
	applymovement LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_1, StarkMountainOutside_Movement_GruntM1WalkOnSpotWestNorth
	waitmovement 0
	msgbox StarkMountainOutside_Text_GoodTimeToBeDone, MSGBOX_DEFAULT
	applymovement LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_1, StarkMountainOutside_Movement_GruntM1EnterStarkMountain
	applymovement LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_2, StarkMountainOutside_Movement_GruntM2EnterStarkMountain
	waitmovement 0
	playse SE_EXIT
	setflag FLAG_SINNOH_ESCONDE_STARK_MOUNTAIN_OUTSIDE_GRUNTS
	removeobject LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_1
	removeobject LOCALID_STARK_MOUNTAIN_OUTSIDE_GRUNT_M_2
	waitse
	setvar VAR_SINNOH_STARK_FORA_ESTADO, 1
	releaseall
	end

StarkMountainOutside_Movement_GruntM1Enter:
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

StarkMountainOutside_Movement_GruntM1WalkToEntrance:
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_right
	walk_up
	step_end

StarkMountainOutside_Movement_GruntM1WalkOnSpotWestNorth:
	walk_in_place_left
	delay_16
	delay_8
	walk_in_place_up
	step_end

StarkMountainOutside_Movement_GruntM1EnterStarkMountain:
	walk_up
	walk_up
	set_invisible
	step_end

StarkMountainOutside_Movement_GruntM2Enter:
	walk_up
	walk_right
	walk_right
	walk_right
	step_end

StarkMountainOutside_Movement_GruntM2WalkToEntrance:
	walk_right
	walk_down
	walk_down
	walk_right
	walk_right
	walk_right
	walk_up
	step_end

StarkMountainOutside_Movement_GruntM2WalkOnSpotEast:
	walk_in_place_right
	step_end

StarkMountainOutside_Movement_GruntM2EnterStarkMountain:
	walk_right
	walk_up
	walk_up
	set_invisible
	step_end

StarkMountainOutside_Text_LetsDoThis:
	.string "Grunt 1: This is it!\n"
	.string "Stark Mountain!\p"
	.string "Now we need to get deep inside.\n"
	.string "Let's do this!$"

StarkMountainOutside_Text_CanHeReplaceCyrus:
	.string "Grunt 2: Yeah, but...\n"
	.string "Can that old guy really take over?\p"
	.string "Can he replace Master Cyrus?$"

StarkMountainOutside_Text_GoodTimeToBeDone:
	.string "Grunt 1: Yeah, I hear you...\p"
	.string "That elder Charon is a Commander,\n"
	.string "but he can't replace Master Cyrus.\p"
	.string "...Maybe this is a good time for me to\n"
	.string "be done with this Team Galactic thing...$"

@ <<< B6 Sinnoh S7: cena da fonte <<<

@ Treinador do pokeplatinum que os dois scripts irmaos nao alcancam
@ (dev_scripts/treinadores_faltantes_sinnoh.py)

StarkMountainOutside_EventScript_DragonTamerDarien::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_DARIEN, StarkMountainOutside_Text_DragonTamerDarienIntro, StarkMountainOutside_Text_DragonTamerDarienDefeat
	msgbox StarkMountainOutside_Text_DragonTamerDarienPost, MSGBOX_AUTOCLOSE
	end

StarkMountainOutside_Text_DragonTamerDarienIntro:
	.string "My Pokémon and I seek only victory!$"

StarkMountainOutside_Text_DragonTamerDarienDefeat:
	.string "Arrrgh! My Pokémon...$"

StarkMountainOutside_Text_DragonTamerDarienPost:
	.string "I failed my Pokémon!\nI wasn't prepared enough to lead it!\pI don't ever want my precious Pokémon\nto be humiliated again!$"
