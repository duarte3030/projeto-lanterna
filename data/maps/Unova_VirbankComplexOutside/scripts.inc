@ VirbankComplexOutside do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ ----------------------------------------------------------------------------
@ B3 (Obra 2 de Unova, 15/08/2026): TROCA DE NIVEL, portada de
@ fontes-mapas/bw3g/maps/VirbankComplexOutside.asm.
@
@ Na fonte sao tres pedacos:
@   - callback MAPCALLBACK_TILES `.SetTiles`, que reaplica o estado ao carregar o mapa;
@   - `VirbankComplexUpperFloorScript`,
@     que sobe para a passarela;
@   - `VirbankComplexLowerFloorScript`,
@     que volta para o chao do complexo.
@
@ O estado mora em EVENT_VIRBANK_COMPLEX_UPPER_FLOOR
@ da fonte, que aqui e
@ FLAG_UNOVA_VIRBANK_COMPLEX_ANDAR_SUPERIOR
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
@ Gatilho: os 9 `coord_event` da fonte, coordenada IDENTIDADE (a geometria de
@ gen 2 entra 1:1 em Unova, cabecalho de dev_scripts/fila_b6.py). Todos caem em
@ tile andavel do map.bin, conferido um a um.
@
@ Linha marcada `igual ao map.bin` NAO pode ser apagada: e restauracao de estado.
@ Todo numero abaixo saiu de dev_scripts/changeblock_gen2.py; nenhum digitado.
@ ----------------------------------------------------------------------------

Unova_VirbankComplexOutside_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_VirbankComplexOutside_EventScript_AoCarregar
	.byte 0

Unova_VirbankComplexOutside_EventScript_AoCarregar::
	call_if_set FLAG_UNOVA_VIRBANK_COMPLEX_ANDAR_SUPERIOR, Unova_VirbankComplexOutside_EventScript_Sobe
	end

@ `VirbankComplexUpperFloorScript` da fonte (a mesma lista do callback de tiles, conferida igual)
Unova_VirbankComplexOutside_EventScript_Sobe::
	@ maps/VirbankComplexOutside.asm:36  changeblock 12, 30, $8C
	changeblock_gen2 12, 30, 621, 601, 622, 613, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD, BE
	@ maps/VirbankComplexOutside.asm:37  changeblock 14, 30, $8D
	changeblock_gen2 14, 30, 602, 621, 613, 624, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD, BD
	@ maps/VirbankComplexOutside.asm:38  changeblock 12, 36, $90
	changeblock_gen2 12, 36, 636, 613, 620, 619, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BE, BD
	@ maps/VirbankComplexOutside.asm:39  changeblock 14, 36, $91
	changeblock_gen2 14, 36, 613, 613, 628, 643, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BE, BD
	@ maps/VirbankComplexOutside.asm:40  changeblock 16, 36, $92
	changeblock_gen2 16, 36, 613, 636, 643, 629, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BE, BD
	return

@ `VirbankComplexLowerFloorScript` da fonte: o caminho de VOLTA ao estado do map.bin
Unova_VirbankComplexOutside_EventScript_Desce::
	@ maps/VirbankComplexOutside.asm:48  changeblock 12, 30, $3C
	changeblock_gen2 12, 30, 621, 601, 622, 623, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankComplexOutside.asm:49  changeblock 14, 30, $3D
	changeblock_gen2 14, 30, 602, 621, 623, 624, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankComplexOutside.asm:50  changeblock 12, 36, $49
	changeblock_gen2 12, 36, 642, 623, 620, 619, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankComplexOutside.asm:51  changeblock 14, 36, $4A
	changeblock_gen2 14, 36, 623, 623, 628, 643, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankComplexOutside.asm:52  changeblock 16, 36, $4B
	changeblock_gen2 16, 36, 623, 642, 643, 629, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return

@ coord_events da fonte: (6,38) (4,28)
Unova_VirbankComplexOutside_EventScript_GatilhoSobe::
	lock
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_ANDAR_SUPERIOR, Unova_VirbankComplexOutside_EventScript_GatilhoFim
	setflag FLAG_UNOVA_VIRBANK_COMPLEX_ANDAR_SUPERIOR
	call Unova_VirbankComplexOutside_EventScript_Sobe
	special DrawWholeMapView
	release
	end

@ coord_events da fonte: (6,40) (4,30) (13,4) (14,5) (15,5) (16,5) (17,5)
Unova_VirbankComplexOutside_EventScript_GatilhoDesce::
	lock
	goto_if_unset FLAG_UNOVA_VIRBANK_COMPLEX_ANDAR_SUPERIOR, Unova_VirbankComplexOutside_EventScript_GatilhoFim
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_ANDAR_SUPERIOR
	call Unova_VirbankComplexOutside_EventScript_Desce
	special DrawWholeMapView
	release
	end

Unova_VirbankComplexOutside_EventScript_GatilhoFim::
	release
	end

Unova_VirbankComplexOutside_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_VIRBANK_COMPLEX_1, Unova_VirbankComplexOutside_Text_GruntM1VirbankComplexOutsideSeenText, Unova_VirbankComplexOutside_Text_GruntM1VirbankComplexOutsideBeatenText
	end

Unova_VirbankComplexOutside_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_VIRBANK_COMPLEX_2, Unova_VirbankComplexOutside_Text_GruntM2VirbankComplexOutsideSeenText, Unova_VirbankComplexOutside_Text_GruntM2VirbankComplexOutsideBeatenText
	end

Unova_VirbankComplexOutside_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_GRUNTF_VIRBANK_COMPLEX_1, Unova_VirbankComplexOutside_Text_GruntFVirbankComplexOutsideSeenText, Unova_VirbankComplexOutside_Text_GruntFVirbankComplexOutsideBeatenText
	end

Unova_VirbankComplexOutside_EventScript_Npc8::
	msgbox Unova_VirbankComplexOutside_Text_VirbankComplexOutsideCherenIntroText, MSGBOX_NPC
	end


Unova_VirbankComplexOutside_Text_GruntM1VirbankComplexOutsideSeenText::
	.string "Ha! I bet you"
	.string "\nthought I was a"
	.string "\lworker here!$"

Unova_VirbankComplexOutside_Text_GruntM1VirbankComplexOutsideBeatenText::
	.string "Grrrr…$"

Unova_VirbankComplexOutside_Text_GruntM2VirbankComplexOutsideSeenText::
	.string "I trained myself"
	.string "\nendlessly to get"
	.string "\pjustice for TEAM"
	.string "\nPLASMA! I won't"
	.string "\plose to anyone"
	.string "\nanymore!$"

Unova_VirbankComplexOutside_Text_GruntM2VirbankComplexOutsideBeatenText::
	.string "…But if I lose, I"
	.string "\nwon't be able to"
	.string "\pcarry out my"
	.string "\njustice!$"

Unova_VirbankComplexOutside_Text_GruntFVirbankComplexOutsideSeenText::
	.string "What do you want,"
	.string "\nintruder?!$"

Unova_VirbankComplexOutside_Text_GruntFVirbankComplexOutsideBeatenText::
	.string "Hmph! I missed my"
	.string "\nchance to grab"
	.string "\lyour POKéMON!$"

Unova_VirbankComplexOutside_Text_VirbankComplexOutsideCherenIntroText::
	.string "CHEREN: {PLAYER},"
	.string "\ngood timing."
	.string "\pI've been invest-"
	.string "\nigating this"
	.string "\lCOMPLEX."
	.string "\pIt's as I thought,"
	.string "\nTEAM PLASMA has"
	.string "\pinfiltrated the"
	.string "\nCOMPLEX. They"
	.string "\pmust be after"
	.string "\nsomething…"
	.string "\pI managed to snag"
	.string "\na key to the lift"
	.string "\pthat leads into"
	.string "\nthe facility."
	.string "\pHere, you should"
	.string "\ntake it.$"
