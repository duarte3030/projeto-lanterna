@ Rt11 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ ----------------------------------------------------------------------------
@ B3 (Obra 2 de Unova, 15/08/2026): TROCA DE NIVEL, portada de
@ fontes-mapas/bw3g/maps/Rt11.asm.
@
@ Na fonte sao tres pedacos:
@   - callback MAPCALLBACK_TILES `.SetTiles`, que reaplica o estado ao carregar o mapa;
@   - `Rt11LowerFloorScript`,
@     que passa por baixo da ponte;
@   - `Rt11UpperFloorScript`,
@     que volta para cima da ponte.
@
@ O estado mora em EVENT_R11_LOWER_FLOOR
@ da fonte, que aqui e
@ FLAG_UNOVA_R11_ANDAR_INFERIOR
@ (tabela da Obra 2 do PLANO-OBRAS-UNOVA.md). ZERO var e ZERO flag nova.
@
@ As listas do callback e do script que ACENDE a flag foram conferidas identicas,
@ tripla a tripla, por isso aqui existe UMA rotina so, chamada pelos dois.
@
@ MAP_SCRIPT_ON_LOAD e nao ON_TRANSITION, decisao 4 do plano: InitMapLayoutData
@ roda DEPOIS do ON_TRANSITION e ANTES do ON_LOAD (src/fieldmap.c, InitMap), entao
@ setmetatile no ON_TRANSITION seria varrido pela releitura do layout antes de o
@ jogador ver a tela. O `special DrawWholeMapView` so aparece nos gatilhos ao
@ vivo; no ON_LOAD o mapa ainda vai ser desenhado.
@
@ Gatilho: os 12 `coord_event` da fonte, coordenada IDENTIDADE (a geometria de
@ gen 2 entra 1:1 em Unova, cabecalho de dev_scripts/fila_b6.py). Todos caem em
@ tile andavel do map.bin, conferido um a um.
@
@ Linha marcada `igual ao map.bin` NAO pode ser apagada: e restauracao de estado.
@ Todo numero abaixo saiu de dev_scripts/changeblock_gen2.py; nenhum digitado.
@
@ Quatro dos 12 gatilhos caem em tile de AGUA (elevacao 1): (31,18) e (31,19) do
@ lado de descer, (27,16) e (27,17) do lado de subir. Nao e defeito, e o desenho
@ da fonte: por baixo da ponte se chega surfando. O `elevation: 0` do coord_event
@ do map.json casa com qualquer elevacao, entao o gatilho pega surfando tambem.
@ ----------------------------------------------------------------------------

Unova_Rt11_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_Rt11_EventScript_AoCarregar
	.byte 0

Unova_Rt11_EventScript_AoCarregar::
	call_if_set FLAG_UNOVA_R11_ANDAR_INFERIOR, Unova_Rt11_EventScript_Desce
	end

@ `Rt11LowerFloorScript` da fonte (a mesma lista do callback de tiles, conferida igual)
Unova_Rt11_EventScript_Desce::
	@ maps/Rt11.asm:40  changeblock 28, 10, $d6
	changeblock_gen2 28, 10, 795, 795, 796, 796, TRUE, TRUE, TRUE, TRUE
	@ maps/Rt11.asm:41  changeblock 28, 12, $d7
	changeblock_gen2 28, 12, 796, 796, 797, 797, TRUE, TRUE, TRUE, TRUE
	@ maps/Rt11.asm:42  changeblock 30, 10, $d5
	changeblock_gen2 30, 10, 793, 793, 794, 794, FALSE, FALSE, FALSE, FALSE
	@ maps/Rt11.asm:43  changeblock 30, 12, $d9
	changeblock_gen2 30, 12, 794, 794, 798, 798, FALSE, FALSE, FALSE, FALSE
	@ maps/Rt11.asm:44  changeblock 32, 10, $d5
	changeblock_gen2 32, 10, 793, 793, 794, 794, FALSE, FALSE, FALSE, FALSE
	@ maps/Rt11.asm:45  changeblock 32, 12, $d9
	changeblock_gen2 32, 12, 794, 794, 798, 798, FALSE, FALSE, FALSE, FALSE
	@ maps/Rt11.asm:46  changeblock 34, 10, $d6
	changeblock_gen2 34, 10, 795, 795, 796, 796, TRUE, TRUE, TRUE, TRUE
	@ maps/Rt11.asm:47  changeblock 34, 12, $d7
	changeblock_gen2 34, 12, 796, 796, 797, 797, TRUE, TRUE, TRUE, TRUE
	return

@ `Rt11UpperFloorScript` da fonte: o caminho de VOLTA ao estado do map.bin
Unova_Rt11_EventScript_Sobe::
	@ maps/Rt11.asm:56  changeblock 28, 10, $a0
	changeblock_gen2 28, 10, 735, 735, 730, 730, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt11.asm:57  changeblock 28, 12, $a4
	changeblock_gen2 28, 12, 730, 730, 732, 732, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt11.asm:58  changeblock 30, 10, $d4
	changeblock_gen2 30, 10, 781, 781, 782, 782, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt11.asm:59  changeblock 30, 12, $d8
	changeblock_gen2 30, 12, 782, 782, 783, 783, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt11.asm:60  changeblock 32, 10, $d4
	changeblock_gen2 32, 10, 781, 781, 782, 782, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt11.asm:61  changeblock 32, 12, $d8
	changeblock_gen2 32, 12, 782, 782, 783, 783, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt11.asm:62  changeblock 34, 10, $a0
	changeblock_gen2 34, 10, 735, 735, 730, 730, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt11.asm:63  changeblock 34, 12, $a4
	changeblock_gen2 34, 12, 730, 730, 732, 732, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return

@ coord_events da fonte: (30,17) (31,18) (31,19)
Unova_Rt11_EventScript_GatilhoDesce::
	lock
	goto_if_set FLAG_UNOVA_R11_ANDAR_INFERIOR, Unova_Rt11_EventScript_GatilhoFim
	setflag FLAG_UNOVA_R11_ANDAR_INFERIOR
	call Unova_Rt11_EventScript_Desce
	special DrawWholeMapView
	release
	end

@ coord_events da fonte: (28,15) (27,16) (27,17) (37,11) (36,12) (36,13)
@   (4,11) (5,12) (5,13)
Unova_Rt11_EventScript_GatilhoSobe::
	lock
	goto_if_unset FLAG_UNOVA_R11_ANDAR_INFERIOR, Unova_Rt11_EventScript_GatilhoFim
	clearflag FLAG_UNOVA_R11_ANDAR_INFERIOR
	call Unova_Rt11_EventScript_Sobe
	special DrawWholeMapView
	release
	end

Unova_Rt11_EventScript_GatilhoFim::
	release
	end

Unova_Rt11_EventScript_Npc4::
	msgbox Unova_Rt11_Text_R11AmoongussText, MSGBOX_NPC
	end

Unova_Rt11_EventScript_Npc5::
	msgbox Unova_Rt11_Text_R11AmoongussText, MSGBOX_NPC
	end

Unova_Rt11_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_BACKERSM_R11, Unova_Rt11_Text_BackersMR11SeenText, Unova_Rt11_Text_BackersMR11BeatenText
	end

Unova_Rt11_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BACKERSM_R11, Unova_Rt11_Text_BackersMR11SeenText, Unova_Rt11_Text_BackersMR11BeatenText
	end

Unova_Rt11_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BACKERSF_R11, Unova_Rt11_Text_BackersFR11SeenText, Unova_Rt11_Text_BackersFR11BeatenText
	end

Unova_Rt11_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_BACKERSF_R11, Unova_Rt11_Text_BackersFR11SeenText, Unova_Rt11_Text_BackersFR11BeatenText
	end


Unova_Rt11_Text_R11AmoongussText::
	.string "Ooong!$"

Unova_Rt11_Text_BackersMR11SeenText::
	.string "Sports and POKé-"
	.string "\nMON battles are"
	.string "\pdramas that don't"
	.string "\nneed scripts!$"

Unova_Rt11_Text_BackersMR11BeatenText::
	.string "We were the"
	.string "\nunderdogs…$"

Unova_Rt11_Text_BackersFR11SeenText::
	.string "Knowing what a"
	.string "\ntruly heated"
	.string "\pbattle is all"
	.string "\nabout is the key"
	.string "\pto truly passion-"
	.string "\nate cheering!$"

Unova_Rt11_Text_BackersFR11BeatenText::
	.string "I cheered as best"
	.string "\nas I could…$"
