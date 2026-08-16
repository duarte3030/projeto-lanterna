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
@ PENDENTE: a cena do BRONIUS (coord_events (9,8) e (9,9) da fonte, com
@ batalha, HM_FLY, specialphonecall e setscene) NÃO foi portada, é escopo de
@ outra frente. Quando for, o fim dela deve `call
@ Unova_VirbankComplexB1F_EventScript_AbrePorta` + `setflag
@ FLAG_UNOVA_VIRBANK_COMPLEX_PORTA` em vez de repetir a linha de metatile,
@ igual à fonte faz. Custo em flag: ZERO nova.

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
