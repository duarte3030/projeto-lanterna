@ P2Lab do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5).
@
@ FONTE: fontes-mapas/bw3g/maps/P2Lab.asm. Dois coord_events, (6,2) e (6,3), no
@ mesmo fecho: a batalha contra o SABIO GORM no fundo do laboratorio P2, com a
@ JUNIPER presa do outro lado. No fim a Plasma foge com o prototipo e a cena
@ manda o jogador de volta para a entrada.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   VAR_UNOVA_P2_LAB_CENA: 0 = SCENE_DEFAULT, 1 = SCENE_FINISHED.
@
@ O setmapscene REMOTO do fim da cena:
@   `setmapscene P2_LAB_ENTRANCE, SCENE_P2_LAB_ENTRANCE_AFTER`
@   -> `setvar VAR_UNOVA_P2_LAB_ENTRADA_CENA, 1`
@   (tabela do PLANO: 0 = SCENE_P2_LAB_ENTRANCE_DEFAULT, 1 = ..._AFTER,
@   2 = ..._NOTHING). Tem que ser gravado ANTES do `warp`, que e para onde o
@   jogador cai.
@
@ ELENCO, zero flag nova (janela de save fechada): os OITO da Plasma que o fim
@ da cena apaga (os cinco treinadores de raio de visao, o GORM, a SOMBRA e a
@ JUNIPER) ja estao no mapa desde o comeco e somem juntos. Um gate so,
@ FLAG_TEMP_11, aceso pelo ON_TRANSITION quando a var ja saiu de 0. O motor
@ limpa os FLAG_TEMP_* em `ClearTempFieldEventData()` (src/overworld.c:893)
@ ANTES do `RunOnTransitionMapScript()` (:909), e os objetos so nascem depois,
@ olhando `template->flagId` (src/event_object_movement.c:2920). Na fonte esses
@ oito estao em EVENT_P2_LAB_GRUNTS, EVENT_P2_LAB_GORM, EVENT_P2_LAB_SHADOW e
@ EVENT_P2_LAB_JUNIPER, nenhum dos quatro na tabela de 21 flags do PLANO (a
@ varredura so pegou EVENT_ escrito DENTRO das cenas, e estes quatro sao campo
@ de object_event).
@
@ Ids locais (indice no map.json + 1): 1-7 = bolas de item, 8-12 = os cinco
@ treinadores da Plasma, 13 = GORM, 14 = SOMBRA, 15 = JUNIPER.
@
@ DESCARTADOS: `setlasttalked`, `dontrestartmapmusic`, `reloadmapafterbattle`
@ (cobertos pelo `trainerbattle_no_intro`); `special ReloadSpritesNoPalettes`
@ (sem equivalente, nenhuma palette muda); `playmusic MUSIC_P2_LAB` seguido de
@ `playmapmusic` na propria fonte vira so `fadedefaultbgm`, porque a segunda
@ linha ja sobrescrevia a primeira.
@ FADES: `special FadeOutMusic` -> `special Script_FadeOutMapMusic` +
@ `waitstate`; `FadeBlackQuickly` -> `fadescreenspeed FADE_TO_BLACK, 8`;
@ `FadeInQuickly` -> `fadescreenspeed FADE_FROM_BLACK, 8`; `FadeOutPalettes`
@ (o fade antes do warp) -> `fadescreen FADE_TO_BLACK`.
@ MUSICA: MUSIC_ROCKET_ENCOUNTER -> MUS_ENCOUNTER_AQUA.
@ O callback `MAPCALLBACK_TILES .SetTiles` e o `P2LabDoorToggleScript` sao
@ changeblock, ou seja Obra 2, e este mapa NAO esta nos 12 da fila dela: ficam
@ fora deste bloco de proposito.
@ ROTAS DO JOGADOR conferidas no map.bin de LAYOUT_UNOVA_P2_LAB:
@ (6,2)->(5,2)->(4,2)->(4,3)->(4,4)->(4,5)->(3,5) e (6,3)->(5,3)->(4,3)->
@ (4,4)->(4,5)->(3,5); colisao 0 em todos os quadrantes.

Unova_P2Lab_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_P2Lab_OnTransition
	.byte 0

Unova_P2Lab_OnTransition:
	goto_if_eq VAR_UNOVA_P2_LAB_CENA, 0, Unova_P2Lab_EventScript_TransicaoFim
	setflag FLAG_TEMP_11
Unova_P2Lab_EventScript_TransicaoFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
Unova_P2Lab_EventScript_P2LabGormScript1::
	lockall
	applymovement LOCALID_PLAYER, Unova_P2Lab_Movement_JogadorDeCima
	waitmovement 0
	goto Unova_P2Lab_EventScript_P2LabGormScript

Unova_P2Lab_EventScript_P2LabGormScript2::
	lockall
	applymovement LOCALID_PLAYER, Unova_P2Lab_Movement_JogadorDeBaixo
	waitmovement 0
	@ cai no proximo, como na fonte

Unova_P2Lab_EventScript_P2LabGormScript::
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	msgbox Unova_P2Lab_Text_P2LabJuniperIntro, MSGBOX_DEFAULT
	closemessage
	msgbox Unova_P2Lab_Text_P2LabShadowIntro, MSGBOX_DEFAULT
	closemessage
	applymovement 13, Unova_P2Lab_Movement_GormSeAproxima
	waitmovement 0
	msgbox Unova_P2Lab_Text_P2LabGorm, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_UNOVA_GORM1, Unova_P2Lab_Text_P2LabGormBeaten
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	applymovement 14, Unova_P2Lab_Movement_SombraSai
	waitmovement 0
	msgbox Unova_P2Lab_Text_P2LabShadowLeave, MSGBOX_DEFAULT
	closemessage
	applymovement 13, Unova_P2Lab_Movement_GormSai
	waitmovement 0
	special Script_FadeOutMapMusic
	waitstate
	fadescreenspeed FADE_TO_BLACK, 8
	delay 15
	playse SE_WARP_OUT
	waitse
	removeobject 13
	removeobject 14
	removeobject 8
	removeobject 9
	removeobject 10
	removeobject 11
	removeobject 12
	delay 15
	fadescreenspeed FADE_FROM_BLACK, 8
	fadedefaultbgm
	delay 15
	turnobject 15, DIR_SOUTH
	turnobject LOCALID_PLAYER, DIR_NORTH
	msgbox Unova_P2Lab_Text_P2LabJuniperAfter, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_P2_LAB_CENA, 1
	@ setmapscene remoto: arma a cena da entrada do P2
	setvar VAR_UNOVA_P2_LAB_ENTRADA_CENA, 1
	fadescreen FADE_TO_BLACK
	playse SE_DOOR
	waitse
	removeobject 15
	warp MAP_UNOVA_P2_LAB_ENTRANCE, 4, 7
	waitstate
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_P2Lab_Movement_JogadorDeCima:
	walk_left
	walk_left
	walk_down
	walk_down
	walk_down
	walk_left
	step_end

Unova_P2Lab_Movement_JogadorDeBaixo:
	walk_left
	walk_left
	walk_down
	walk_down
	walk_left
	step_end

Unova_P2Lab_Movement_GormSeAproxima:
	walk_down
	walk_down
	walk_down
	walk_right
	step_end

Unova_P2Lab_Movement_GormSai:
	walk_left
	walk_up
	walk_up
	step_end

Unova_P2Lab_Movement_SombraSai:
	walk_fast_left
	walk_fast_up
	walk_fast_up
	step_end

Unova_P2Lab_Text_P2LabJuniperIntro::
	.string "JUNIPER: {PLAYER}!"
	.string "\nIt's just as I"
	.string "\pthought, TEAM"
	.string "\nPLASMA is trying"
	.string "\pto get something"
	.string "\nout of that"
	.string "\lchamber!$"

Unova_P2Lab_Text_P2LabShadowIntro::
	.string "SHADOW: SAGE GORM,"
	.string "\nhas the prototype"
	.string "\pbeen safely"
	.string "\nremoved?"
	.string "\pGORM: … … …"
	.string "\pSHADOW: Then why"
	.string "\ndon't we take care"
	.string "\lof these"
	.string "\lintruders?$"

Unova_P2Lab_Text_P2LabGorm::
	.string "GORM: … … …$"

Unova_P2Lab_Text_P2LabGormBeaten::
	.string "GORM: … … … ?$"

Unova_P2Lab_Text_P2LabShadowLeave::
	.string "SHADOW: Quickly,"
	.string "\nmy SAGE! We must"
	.string "\lgo!$"

Unova_P2Lab_Text_P2LabJuniperAfter::
	.string "JUNIPER: That"
	.string "\nthing they took…"
	.string "\pIt must be some"
	.string "\nkind of experi-"
	.string "\lmental weapon…"
	.string "\pCome on, {PLAYER},"
	.string "\nlet's get out of"
	.string "\lhere.$"

Unova_P2Lab_EventScript_Placa0::
	msgbox Unova_P2Lab_Text_P2LabDoorText, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Placa1::
	msgbox Unova_P2Lab_Text_P2LabDoorText, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Placa2::
	msgbox Unova_P2Lab_Text_P2LabDoorText, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Placa3::
	msgbox Unova_P2Lab_Text_P2LabDoorText, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Placa4::
	msgbox Unova_P2Lab_Text_P2LabDoorText, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Placa5::
	msgbox Unova_P2Lab_Text_P2LabDiaryText1, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Placa6::
	msgbox Unova_P2Lab_Text_P2LabDiaryText2, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Placa7::
	msgbox Unova_P2Lab_Text_P2LabDiaryText3, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Placa8::
	msgbox Unova_P2Lab_Text_P2LabDiaryText4, MSGBOX_SIGN
	end

Unova_P2Lab_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_P2_1, Unova_P2Lab_Text_GruntM1P2LabSeenText, Unova_P2Lab_Text_GruntM1P2LabBeatenText
	end

Unova_P2Lab_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_P2_2, Unova_P2Lab_Text_GruntM2P2LabSeenText, Unova_P2Lab_Text_GruntM2P2LabBeatenText
	end

Unova_P2Lab_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_GRUNTF_P2_1, Unova_P2Lab_Text_GruntF1P2LabSeenText, Unova_P2Lab_Text_GruntF1P2LabBeatenText
	end

Unova_P2Lab_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_GRUNTF_P2_2, Unova_P2Lab_Text_GruntF2P2LabSeenText, Unova_P2Lab_Text_GruntF2P2LabBeatenText
	end

Unova_P2Lab_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTM_P2, Unova_P2Lab_Text_ScientistP2LabSeenText, Unova_P2Lab_Text_ScientistP2LabBeatenText
	end


Unova_P2Lab_Text_P2LabDoorText::
	.string "There's a switch."
	.string "\nPress it?$"

Unova_P2Lab_Text_P2LabDiaryText1::
	.string "There's a document"
	.string "\non the PC…"
	.string "\pGENESIS PROJECT-"
	.string "\pToday, …e"
	.string "\nspec…en arr…ed."
	.string "\p… …st be"
	.string "\n…ions of years"
	.string "\lol… …"
	.string "\p… …n't wait …"
	.string "\n…n the proj… …$"

Unova_P2Lab_Text_P2LabDiaryText2::
	.string "There's a document"
	.string "\non the PC…"
	.string "\pGENESIS PROJECT-"
	.string "\pThe …ect …"
	.string "\n…ov… …lower tha…"
	.string "\l…pected…"
	.string "\p… …have had"
	.string "\n…ficulty … …ith"
	.string "\l…tegrati… the…"
	.string "\p…bernetic parts"
	.string "\n… …hout serio…"
	.string "\l…gradation."
	.string "\pSt… …e must"
	.string "\npr… on.$"

Unova_P2Lab_Text_P2LabDiaryText3::
	.string "There's a document"
	.string "\non the PC…"
	.string "\pGENESIS PROJECT-"
	.string "\p… …reakthrough!"
	.string "\n… project was"
	.string "\p… …ught fully"
	.string "\nonl… …oday."
	.string "\pDespi… …oss of"
	.string "\ncontr… …he proof"
	.string "\lof conc… …as"
	.string "\l…idated!"
	.string "\p…will not be"
	.string "\n…ng now…$"

Unova_P2Lab_Text_P2LabDiaryText4::
	.string "There's a document"
	.string "\non the PC…"
	.string "\pGENESIS PROJECT-"
	.string "\p…rd fro… …pper"
	.string "\nmanag… …ject has"
	.string "\l…n cancel… …"
	.string "\p…se fools do… …"
	.string "\n… …will no… …"
	.string "\pI wi… …rry out"
	.string "\n… …NESIS P… …T to"
	.string "\l… …letion. I m… …"
	.string "\p… … … …$"

Unova_P2Lab_Text_GruntM1P2LabSeenText::
	.string "This time, we'll"
	.string "\ntake over the"
	.string "\lUNOVA region!$"

Unova_P2Lab_Text_GruntM1P2LabBeatenText::
	.string "Even if I lose, I"
	.string "\nwill not give up"
	.string "\pon justice for"
	.string "\nTEAM PLASMA!$"

Unova_P2Lab_Text_GruntM2P2LabSeenText::
	.string "I'm the fighting"
	.string "\nsweeper! I'll"
	.string "\pclean up garbage"
	.string "\nlike you!$"

Unova_P2Lab_Text_GruntM2P2LabBeatenText::
	.string "Oops…$"

Unova_P2Lab_Text_GruntF1P2LabSeenText::
	.string "I'm going to go"
	.string "\nahead and say it:"
	.string "\pPlasmaaaa!!$"

Unova_P2Lab_Text_GruntF1P2LabBeatenText::
	.string "Do-over! C'mon,"
	.string "\nlet me have a"
	.string "\ldo-over!$"

Unova_P2Lab_Text_GruntF2P2LabSeenText::
	.string "Our king is gone…"
	.string "\nBut we are still"
	.string "\lhere!$"

Unova_P2Lab_Text_GruntF2P2LabBeatenText::
	.string "Ugh… Losing is"
	.string "\nthe worst…$"

Unova_P2Lab_Text_ScientistP2LabSeenText::
	.string "You! You've come"
	.string "\nto steal my work!"
	.string "\pI'll never let my"
	.string "\nproject be taken!$"

Unova_P2Lab_Text_ScientistP2LabBeatenText::
	.string "No! It's not"
	.string "\npossible!$"
