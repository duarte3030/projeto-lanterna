@ VirbankComplexB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@
@ B4 da Obra 2 (changeblock), 15/08/2026. Linhas de metatile geradas por
@ dev_scripts/changeblock_gen2.py (trecho de maps/VirbankComplexB1F.asm);
@ nenhum id de metatile foi digitado à mão.
@
@ Mecanismo da fonte: UM changeblock só, `2, 4, $07` (chão), a porta da parede
@ oeste. Ele aparece em TRÊS lugares da fonte, e os três são o mesmo estado:
@ (1) `.CheckDoor`, o MAPCALLBACK_TILES que reaplica na entrada; (2)
@ `VirbankComplexDoorScript`, os dois bg_event de (2,5) e (3,5) que o jogador
@ examina de baixo; (3) o fim da cena do BRONIUS. Estado em
@ FLAG_UNOVA_VIRBANK_COMPLEX_PORTA. Dos 4 quadrantes do bloco, os dois de cima
@ já são chão no map.bin; quem muda são (2,5) e (3,5), que são exatamente os
@ dois tiles de parede em que os bg_event estão.
@
@ `.CheckDoor` também APAGA os 4 interruptores do B2F em toda carga deste mapa,
@ e isso é regra de jogo, não faxina: descer de novo pelo elevador recomeça o
@ quebra-cabeça do B2F do zero. Copiado igual, é da fonte.
@
@ ON_LOAD e não ON_TRANSITION, decisão 4 da condutora: InitMapLayoutData roda
@ entre os dois e apagaria o setmetatile.
@
@ Leva de treinadores da Fase B (18/08/2026): TRAINER_UNOVA_BRONIUS1 (2169)
@ já existe e a batalha está escrita abaixo (Unova_VirbankComplexB1F_
@ EventScript_CenaBronius). LIGADA pela fiação final (18/08/2026): objeto
@ plantado em (13,10) com "local_id": "LOCALID_VIRBANKCOMPLEXB1F_BRONIUS"
@ (gráfico OBJ_EVENT_GFX_AQUA_MEMBER_M, o mesmo SPRITE_PZMA_SAGE ->
@ equivalente de dev_scripts/tabela_sprites_bw3g.py); dois
@ coord_event em (9,8) e (9,9), mesma coordenada da fonte (mapa sem offset,
@ conferido pelos outros object_events já plantados). Sem objeto de
@ CHEREN/sombra neste mapa: simplificação já decidida aqui (não é
@ pendência, é decisão), a fonte
@ intercala a luta com CHEREN avisando e duas sombras fugindo com o
@ elemento roubado (specialphonecall, setscene SCENE_FINISHED,
@ EVENT_ASPERTIA_CITY_BLOCKER); sem os objetos de CHEREN/sombra plantados
@ em outro mapa/cena, portei só o essencial fiel à fonte: a luta e a
@ recompensa de HM_FLY que ela dá. O fecho reusa a MESMA
@ Unova_VirbankComplexB1F_EventScript_AbrePorta + setflag
@ FLAG_UNOVA_VIRBANK_COMPLEX_PORTA que a porta já usa (zero flag nova,
@ como a nota antiga já previa). Sem flag/var de "já venceu" nova: uso
@ `goto_if_defeated`, que lê o proprio estado de treinador do jogo (custo
@ zero, mesmo idioma de VeilstoneCity_OnTransition).
@
@ COMO O BRONIUS SOME DEPOIS DE DERROTADO, com ZERO flag nova (conserto de
@ 18/08/2026). A nota anterior daqui dizia que "a fonte nunca seta nem limpa
@ EVENT_VIRBANK_COMPLEX_B1F_BRONIUS em lugar nenhum". É FALSO, e o objeto
@ ficava plantado para sempre por causa disso: `maps/VirbankComplexB1F.asm:82`
@ tem `disappear VIRBANKCOMPLEXB1F_BRONIUS` no fecho da cena, e no gen 2
@ `disappear` ACENDE justamente o event flag do object_event (o último campo
@ da linha 354 da fonte é EVENT_VIRBANK_COMPLEX_B1F_BRONIUS). O mesmo vale
@ para a INFER em `maps/PinwheelForest.asm:96`.
@ Aqui isso vira o par que a casa já usa nas cenas da Obra 1
@ (Unova_GiantChasm1F e Unova_DragonspiralTower6F): `removeobject` no fecho
@ some com ele NESTA visita, e o campo `flag` do object_event some com ele nas
@ próximas. A flag é a de treinador derrotado do próprio motor,
@ TRAINER_FLAGS_START + TRAINER_UNOVA_BRONIUS1 (0x500 + 2169 = 3449), a mesma
@ que o `goto_if_defeated` acima lê e a mesma régua de custo zero de
@ Unova_PkmnLeagueMain. Nenhum `setflag` é preciso: quem acende essa flag é o
@ próprio `trainerbattle_no_intro` ao vencer.
@
@ COREOGRAFIA (18/08/2026), da fonte, rotas conferidas tile a tile em
@ data/layouts/Unova_VirbankComplexB1F/map.bin (todas colisão 0, elevação 3,
@ igual à do objeto):
@   `VirbankComplexBroniusScript1` (gatilho (9,8)) e `...Script2` (gatilho
@   (9,9)) diferem SÓ no passo do jogador, e é por isso que a fonte tem dois
@   rótulos: de (9,8) ele desce e anda para a direita, de (9,9) só para a
@   direita. Os dois terminam em (10,9) virados para leste.
@   `VirbankComplexB1FBroniusMovement` (LEFT, LEFT, UP, turn_head LEFT) traz o
@   BRONIUS de (13,10) para (11,9) virado para oeste, de frente para o
@   jogador, ANTES da fala de batalha.
@   SAÍDA: a fonte toca SFX_ESCAPE_ROPE e dá `disappear` sem andar. Vira
@   `playse SE_WARP_OUT` + `removeobject`, o mesmo idioma de sumiço da Plasma
@   já usado em Unova_DragonspiralTowerRoof e Unova_ChampionsRoomEntrance.
Unova_VirbankComplexB1F_EventScript_Bronius1::
	goto_if_defeated TRAINER_UNOVA_BRONIUS1, Unova_VirbankComplexB1F_EventScript_BroniusFim
	lockall
	applymovement LOCALID_PLAYER, Unova_VirbankComplexB1F_Movement_JogadorDesceEEntra
	waitmovement 0
	goto Unova_VirbankComplexB1F_EventScript_CenaBronius

Unova_VirbankComplexB1F_EventScript_Bronius2::
	goto_if_defeated TRAINER_UNOVA_BRONIUS1, Unova_VirbankComplexB1F_EventScript_BroniusFim
	lockall
	applymovement LOCALID_PLAYER, Unova_VirbankComplexB1F_Movement_JogadorEntra
	waitmovement 0

Unova_VirbankComplexB1F_EventScript_CenaBronius::
	setvar VAR_LAST_TALKED, LOCALID_VIRBANKCOMPLEXB1F_BRONIUS
	msgbox Unova_VirbankComplexB1F_Text_BroniusIntro, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_VIRBANKCOMPLEXB1F_BRONIUS, Unova_VirbankComplexB1F_Movement_BroniusSeAproxima
	waitmovement 0
	trainerbattle_no_intro TRAINER_UNOVA_BRONIUS1, Unova_VirbankComplexB1F_Text_BroniusBeaten
	giveitem ITEM_HM_FLY
	call Unova_VirbankComplexB1F_EventScript_AbrePorta
	setflag FLAG_UNOVA_VIRBANK_COMPLEX_PORTA
	playse SE_WARP_OUT
	waitse
	removeobject LOCALID_VIRBANKCOMPLEXB1F_BRONIUS
Unova_VirbankComplexB1F_EventScript_BroniusFim::
	releaseall
	end

@ `VirbankComplexB1FPlayerMovement1` da fonte: step DOWN, step RIGHT.
Unova_VirbankComplexB1F_Movement_JogadorDesceEEntra:
	walk_down
	walk_right
	step_end

@ `VirbankComplexB1FPlayerMovement2` da fonte: step RIGHT.
Unova_VirbankComplexB1F_Movement_JogadorEntra:
	walk_right
	step_end

@ `VirbankComplexB1FBroniusMovement` da fonte: step LEFT, LEFT, UP, turn_head
@ LEFT. (13,10) -> (12,10) -> (11,10) -> (11,9), virado para oeste.
Unova_VirbankComplexB1F_Movement_BroniusSeAproxima:
	walk_left
	walk_left
	walk_up
	face_left
	step_end

Unova_VirbankComplexB1F_Text_BroniusIntro:
	.string "???: Darn! I'm so close!\n"
	.string "The FIRE ELEMENT is nearly ours!\p"
	.string "BRONIUS: Let's see if you have\n"
	.string "what it takes to stand up to the\lmight of TEAM PLASMA!$"

Unova_VirbankComplexB1F_Text_BroniusBeaten:
	.string "No! This is impossible!$"

Unova_VirbankComplexB1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_VirbankComplexB1F_EventScript_AoCarregar
	.byte 0

@ `.CheckDoor` da fonte, linhas 23-32.
Unova_VirbankComplexB1F_EventScript_AoCarregar::
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4
	goto_if_unset FLAG_UNOVA_VIRBANK_COMPLEX_PORTA, Unova_VirbankComplexB1F_EventScript_AoCarregarFim
	call Unova_VirbankComplexB1F_EventScript_AbrePorta
Unova_VirbankComplexB1F_EventScript_AoCarregarFim::
	end

@ `VirbankComplexDoorScript` da fonte, linhas 128-142: os bg_event de (2,5) e
@ (3,5), os dois com o mesmo script (por isso os dois rótulos aqui).
Unova_VirbankComplexB1F_EventScript_Placa0::
Unova_VirbankComplexB1F_EventScript_Placa1::
	lock
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_PORTA, Unova_VirbankComplexB1F_EventScript_PortaJaAberta
	msgbox Unova_VirbankComplexB1F_Text_VirbankComplexOpenDoorText, MSGBOX_DEFAULT
	call Unova_VirbankComplexB1F_EventScript_AbrePorta
	setflag FLAG_UNOVA_VIRBANK_COMPLEX_PORTA
	playse SE_DOOR
	special DrawWholeMapView
	waitse
Unova_VirbankComplexB1F_EventScript_PortaJaAberta::
	release
	end

@ maps/VirbankComplexB1F.asm:31 (e 103 e 134, as mesmas 3 chamadas iguais)
Unova_VirbankComplexB1F_EventScript_AbrePorta::
	changeblock_gen2 2, 4, 517, 517, 517, 517, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD
	return

Unova_VirbankComplexB1F_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTF_VIRBANK_COMPLEX_1, Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FSeenText, Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FBeatenText
	end


Unova_VirbankComplexB1F_Text_VirbankComplexOpenDoorText::
	.string "The door opened!$"

Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FSeenText::
	.string "TEAM PLASMA is"
	.string "\nstudying things"
	.string "\pyou couldn't"
	.string "\npossibly under-"
	.string "\pstand. For that"
	.string "\npurpose, please"
	.string "\phand over your"
	.string "\nPOKéMON.$"

Unova_VirbankComplexB1F_Text_ScientistFVirbankComplexB1FBeatenText::
	.string "What? You can"
	.string "\nactually draw out"
	.string "\pthe power of your"
	.string "\nPOKéMON?$"
