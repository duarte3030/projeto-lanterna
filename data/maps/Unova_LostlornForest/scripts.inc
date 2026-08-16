@ LostlornForest do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5).
@
@ FONTE: fontes-mapas/bw3g/maps/LostlornForest.asm. DUAS cenas encadeadas na
@ mesma var, cada uma com o seu coord_event:
@   (5,27) valor 0 = a dupla de grunts da Plasma, DUAS batalhas seguidas;
@   (10,36) valor 1 = a SEGUNDA batalha do rival (INFER), que so fica valendo
@   depois que os grunts sairam.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   VAR_UNOVA_LOSTLORN_FOREST_CENA: 0 = SCENE_LOSTLORN_GRUNTS,
@   1 = SCENE_LOSTLORN_INFER, 2 = SCENE_LOSTLORN_NOTHING.
@
@ ELENCO, zero flag nova (janela de save fechada): duas flags TEMPORARIAS
@ recalculadas da var pelo ON_TRANSITION. O motor limpa os FLAG_TEMP_* em
@ `ClearTempFieldEventData()` (src/overworld.c:893) ANTES do
@ `RunOnTransitionMapScript()` (:909), e os objetos so nascem depois, olhando
@ `template->flagId` (src/event_object_movement.c:2920).
@   FLAG_TEMP_11 = os dois grunts; nascem so no estagio 0.
@   FLAG_TEMP_12 = a INFER; nasce nos estagios 0 e 1 (a fonte nunca faz
@                  `appear` nela, ou seja ela ja esta plantada no mapa desde o
@                  comeco) e some no 2.
@
@ Ids locais (indice no map.json + 1): 1-7 = bolas de item, 8-13 = os seis
@ treinadores de raio de visao, 14 = INFER, 15 = GRUNTM, 16 = GRUNTF.
@
@ DESCARTADOS: `setlasttalked`, `dontrestartmapmusic` e `reloadmapafterbattle`
@ (o `trainerbattle_no_intro` ja faz o papel dos tres); `special FadeOutMusic`
@ vira `special Script_FadeOutMapMusic` + `waitstate`; `playmapmusic` vira
@ `fadedefaultbgm`; o `;playmusic MUSIC_FOREST` que ja estava comentado na
@ fonte continua fora.
@ MUSICA: MUSIC_ROCKET_ENCOUNTER -> MUS_ENCOUNTER_AQUA (mesmo apelido que a
@ ChampionsRoomEntrance usa para as sombras da Plasma); MUSIC_RIVAL_ENCOUNTER
@ -> MUS_ENCOUNTER_MAY.
@ `fix_facing`/`remove_fixed_facing` do gen 2 nao existe aqui: vira `slide_*`
@ (que anda sem animacao de passo, mas VIRA o sprite) mais um `turnobject` de
@ volta para a direcao original. Resultado final igual, uma linha a mais.

Unova_LostlornForest_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_LostlornForest_OnTransition
	.byte 0

Unova_LostlornForest_OnTransition:
	goto_if_eq VAR_UNOVA_LOSTLORN_FOREST_CENA, 0, Unova_LostlornForest_EventScript_TransicaoFim
	setflag FLAG_TEMP_11
	goto_if_eq VAR_UNOVA_LOSTLORN_FOREST_CENA, 1, Unova_LostlornForest_EventScript_TransicaoFim
	setflag FLAG_TEMP_12
Unova_LostlornForest_EventScript_TransicaoFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ Estagio 0: `LostlornForestGruntsScript` da fonte, inteiro.
Unova_LostlornForest_EventScript_LostlornForestGruntsScript::
	lockall
	msgbox Unova_LostlornForest_Text_LostlornGruntsIntro, MSGBOX_DEFAULT
	closemessage
	applymovement 16, Common_Movement_ExclamationMark
	waitmovement 0
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	msgbox Unova_LostlornForest_Text_LostlornGruntsBehindYou, MSGBOX_DEFAULT
	closemessage
	turnobject 15, DIR_WEST
	msgbox Unova_LostlornForest_Text_LostlornGruntsBattle1, MSGBOX_DEFAULT
	closemessage
	applymovement 15, Unova_LostlornForest_Movement_GruntMSeAproxima
	waitmovement 0
	trainerbattle_no_intro TRAINER_UNOVA_GRUNTM_LOSTLORN, Unova_LostlornForest_Text_LostlornGrunt1Win
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	delay 15
	applymovement 15, Unova_LostlornForest_Movement_GruntMRecua
	waitmovement 0
	turnobject 15, DIR_WEST
	msgbox Unova_LostlornForest_Text_LostlornGruntsBattle2, MSGBOX_DEFAULT
	closemessage
	applymovement 16, Unova_LostlornForest_Movement_GruntFSeAproxima
	waitmovement 0
	trainerbattle_no_intro TRAINER_UNOVA_GRUNTF_LOSTLORN, Unova_LostlornForest_Text_LostlornGrunt2Win
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	delay 15
	applymovement 16, Unova_LostlornForest_Movement_GruntFRecua
	waitmovement 0
	turnobject 16, DIR_WEST
	msgbox Unova_LostlornForest_Text_LostlornGruntsLeave, MSGBOX_DEFAULT
	closemessage
	applymovement 15, Unova_LostlornForest_Movement_GruntsSaem
	applymovement 16, Unova_LostlornForest_Movement_GruntsSaem
	waitmovement 0
	removeobject 15
	removeobject 16
	special Script_FadeOutMapMusic
	waitstate
	delay 30
	fadedefaultbgm
	setvar VAR_UNOVA_LOSTLORN_FOREST_CENA, 1
	releaseall
	end

@ Estagio 1: `LostlornForestInferScript` da fonte.
Unova_LostlornForest_EventScript_LostlornForestInferScript::
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 30
	playbgm MUS_ENCOUNTER_MAY, FALSE
	turnobject LOCALID_PLAYER, DIR_SOUTH
	applymovement 14, Unova_LostlornForest_Movement_InferChega
	waitmovement 0
	msgbox Unova_LostlornForest_Text_LostlornForestInferIntro, MSGBOX_DEFAULT
	closemessage
	goto Unova_LostlornForest_EventScript_BatalhaInfer2

@ Mesmo galho por inicial da primeira batalha (Rt12): a fonte manda
@ `checkevent EVENT_GOT_OSHAWOTT -> INFER2_SNIVY`,
@ `checkevent EVENT_GOT_SNIVY -> INFER2_TEPIG` e o fallthrough (TEPIG) ->
@ INFER2_OSHAWOTT. Aqui o galho e por VAR_STARTER_MON (0 = SNIVY, 1 = TEPIG,
@ 2 = OSHAWOTT, escrito por data/maps/Unova_NuvemaLab/scripts.inc).
Unova_LostlornForest_EventScript_BatalhaInfer2::
	goto_if_eq VAR_STARTER_MON, 0, Unova_LostlornForest_EventScript_InferComTepig
	goto_if_eq VAR_STARTER_MON, 1, Unova_LostlornForest_EventScript_InferComOshawott
	trainerbattle_no_intro TRAINER_UNOVA_INFER2_SNIVY, Unova_LostlornForest_Text_LostlornForestInferWin
	goto Unova_LostlornForest_EventScript_DepoisDaInfer2

Unova_LostlornForest_EventScript_InferComTepig::
	trainerbattle_no_intro TRAINER_UNOVA_INFER2_TEPIG, Unova_LostlornForest_Text_LostlornForestInferWin
	goto Unova_LostlornForest_EventScript_DepoisDaInfer2

Unova_LostlornForest_EventScript_InferComOshawott::
	trainerbattle_no_intro TRAINER_UNOVA_INFER2_OSHAWOTT, Unova_LostlornForest_Text_LostlornForestInferWin
Unova_LostlornForest_EventScript_DepoisDaInfer2::
	playbgm MUS_ENCOUNTER_MAY, FALSE
	msgbox Unova_LostlornForest_Text_LostlornForestInferYouWon, MSGBOX_DEFAULT
	closemessage
	applymovement 14, Unova_LostlornForest_Movement_InferSai
	waitmovement 0
	removeobject 14
	special Script_FadeOutMapMusic
	waitstate
	delay 30
	fadedefaultbgm
	setvar VAR_UNOVA_LOSTLORN_FOREST_CENA, 2
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

@ `LostlornGruntMovement1` a `5` e os dois roteiros da INFER, da fonte.
Unova_LostlornForest_Movement_GruntMSeAproxima:
	walk_left
	walk_left
	step_end

Unova_LostlornForest_Movement_GruntMRecua:
	slide_right
	slide_right
	step_end

Unova_LostlornForest_Movement_GruntFSeAproxima:
	walk_down
	walk_left
	walk_left
	walk_up
	walk_left
	step_end

Unova_LostlornForest_Movement_GruntFRecua:
	slide_right
	step_end

Unova_LostlornForest_Movement_GruntsSaem:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

Unova_LostlornForest_Movement_InferChega:
	walk_up
	walk_up
	walk_right
	walk_up
	walk_up
	step_end

Unova_LostlornForest_Movement_InferSai:
	walk_fast_down
	walk_fast_down
	walk_fast_left
	walk_fast_down
	walk_fast_down
	step_end

Unova_LostlornForest_Text_LostlornGruntsIntro::
	.string "Are you sure we're"
	.string "\ngoing the right"
	.string "\lway?"
	.string "\pNIMBASA CITY has"
	.string "\ngot to be around"
	.string "\lhere somewhere…$"

Unova_LostlornForest_Text_LostlornGruntsBehindYou::
	.string "Hey! There's"
	.string "\nsomeone behind"
	.string "\lyou!$"

Unova_LostlornForest_Text_LostlornGruntsBattle1::
	.string "Hey, you better"
	.string "\nnot mess with us!"
	.string "\pI'll show you the"
	.string "\npower of TEAM"
	.string "\lPLASMA!$"

Unova_LostlornForest_Text_LostlornGrunt1Win::
	.string "Arrgh, no way!$"

Unova_LostlornForest_Text_LostlornGruntsBattle2::
	.string "Darn it, you were"
	.string "\ntoo soft."
	.string "\pI'll show you how"
	.string "\nit's done!$"

Unova_LostlornForest_Text_LostlornGrunt2Win::
	.string "No, how could I"
	.string "\nlose?!$"

Unova_LostlornForest_Text_LostlornGruntsLeave::
	.string "C'mon, let's get"
	.string "\nout of here!"
	.string "\pYou haven't seen"
	.string "\nthe last of us!$"

Unova_LostlornForest_Text_LostlornForestInferIntro::
	.string "You, what are you"
	.string "\ndoing here?"
	.string "\pWhat? TEAM PLASMA?"
	.string "\nI don't know what"
	.string "\lyou're talking"
	.string "\labout."
	.string "\pI told you not"
	.string "\nto follow me."
	.string "\pGuess I'll have"
	.string "\nto teach you a"
	.string "\llesson!$"

Unova_LostlornForest_Text_LostlornForestInferWin::
	.string "No! How could"
	.string "\nI lose?$"

Unova_LostlornForest_Text_LostlornForestInferYouWon::
	.string "Darn, I'm still"
	.string "\nnot strong enough…"
	.string "\pWhatever, this"
	.string "\nwon't hold me"
	.string "\lback."
	.string "\pI'm telling you,"
	.string "\ndon't get involved"
	.string "\lwith TEAM PLASMA."
	.string "\pNext time we meet,"
	.string "\nyou won't be so"
	.string "\llucky!$"

Unova_LostlornForest_EventScript_Placa0::
	msgbox Unova_LostlornForest_Text_LostlornForestSignText, MSGBOX_SIGN
	end

Unova_LostlornForest_EventScript_Placa1::
	msgbox Unova_LostlornForest_Text_LostlornR16SignText, MSGBOX_SIGN
	end

Unova_LostlornForest_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_LOSTLORN, Unova_LostlornForest_Text_SchoolKidFLostlornSeenText, Unova_LostlornForest_Text_SchoolKidFLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_LOSTLORN, Unova_LostlornForest_Text_SchoolKidMLostlornSeenText, Unova_LostlornForest_Text_SchoolKidMLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERM_LOSTLORN, Unova_LostlornForest_Text_PkmnBreederMLostlornSeenText, Unova_LostlornForest_Text_PkmnBreederMLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_PKMN_BREEDERF_LOSTLORN, Unova_LostlornForest_Text_PkmnBreederFLostlornSeenText, Unova_LostlornForest_Text_PkmnBreederFLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_LOSTLORN, Unova_LostlornForest_Text_YoungsterLostlornSeenText, Unova_LostlornForest_Text_YoungsterLostlornBeatenText
	end

Unova_LostlornForest_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_LASS_LOSTLORN, Unova_LostlornForest_Text_LassLostlornSeenText, Unova_LostlornForest_Text_LassLostlornBeatenText
	end


Unova_LostlornForest_Text_LostlornForestSignText::
	.string "LOSTLORN FOREST"
	.string "\pTake caution not"
	.string "\nto become lost.$"

Unova_LostlornForest_Text_LostlornR16SignText::
	.string "ROUTE 16 ahead."
	.string "\pPassage to"
	.string "\nNIMBASA CITY.$"

Unova_LostlornForest_Text_SchoolKidFLostlornSeenText::
	.string "I need to research"
	.string "\nthe EXP points of"
	.string "\pPOKéMON for my"
	.string "\nhomework!$"

Unova_LostlornForest_Text_SchoolKidFLostlornBeatenText::
	.string "It's not fair to"
	.string "\nuse moves I wasn't"
	.string "\lexpecting!$"

Unova_LostlornForest_Text_SchoolKidMLostlornSeenText::
	.string "I have a riddle"
	.string "\nfor you! Do you"
	.string "\pknow what is"
	.string "\ndistant but close?$"

Unova_LostlornForest_Text_SchoolKidMLostlornBeatenText::
	.string "The difference"
	.string "\nbetween winning"
	.string "\land losing!$"

Unova_LostlornForest_Text_PkmnBreederMLostlornSeenText::
	.string "Having lots of"
	.string "\nbattles is the"
	.string "\pbest way to raise"
	.string "\nPOKéMON quickly.$"

Unova_LostlornForest_Text_PkmnBreederMLostlornBeatenText::
	.string "Your training"
	.string "\nmethod is great,"
	.string "\pI'm going to copy"
	.string "\nit!$"

Unova_LostlornForest_Text_PkmnBreederFLostlornSeenText::
	.string "I need to practice"
	.string "\nmore as a POKéMON"
	.string "\lbreeder."
	.string "\pPlease, be my"
	.string "\nopponent!$"

Unova_LostlornForest_Text_PkmnBreederFLostlornBeatenText::
	.string "I've still got a"
	.string "\nlong way to go…"
	.string "\pI'll keep raising"
	.string "\nmy POKéMON!$"

Unova_LostlornForest_Text_YoungsterLostlornSeenText::
	.string "I might be lost"
	.string "\nright now, but"
	.string "\pI'll battle you"
	.string "\nanyway!$"

Unova_LostlornForest_Text_YoungsterLostlornBeatenText::
	.string "I don't stand a"
	.string "\nchance if I fight"
	.string "\lwhen I'm lost!$"

Unova_LostlornForest_Text_LassLostlornSeenText::
	.string "Are you ready? I"
	.string "\nam! Let's go!$"

Unova_LostlornForest_Text_LassLostlornBeatenText::
	.string "What? I never even"
	.string "\nconsidered losing"
	.string "\pbefore going into"
	.string "\nbattle!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

Unova_EventScript_GrutaTier1::
	lockall
	msgbox Unova_Text_AchouGruta, MSGBOX_DEFAULT
	randomelement ITEM_RED_SHARD, ITEM_RED_SHARD, ITEM_BLUE_SHARD, ITEM_BLUE_SHARD, ITEM_GREEN_SHARD, ITEM_GREEN_SHARD, ITEM_YELLOW_SHARD, ITEM_YELLOW_SHARD, ITEM_MOOMOO_MILK, ITEM_MOOMOO_MILK, ITEM_PEARL, ITEM_PEARL, ITEM_ETHER, ITEM_ETHER, ITEM_REVIVE, ITEM_REVIVE
	giveitem VAR_RESULT
	releaseall
	end

@ Gruta escondida do BW3G (tier 1). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_LostlornForest_EventScript_Gruta4B5::
	goto_if_set FLAG_UNOVA_GRUTA_LOSTLORN, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_LOSTLORN
	goto Unova_EventScript_GrutaTier1
