@ VirbankCity do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ ----------------------------------------------------------------------------
@ B3 (Obra 2 de Unova, 15/08/2026): TROCA DE NIVEL, portada de
@ fontes-mapas/bw3g/maps/VirbankCity.asm.
@
@ Na fonte sao tres pedacos:
@   - callback MAPCALLBACK_TILES `.SetTiles`, que reaplica o estado ao carregar o mapa;
@   - `VirbankCityLowerFloorScript`,
@     que desce para o nivel de baixo do porto;
@   - `VirbankCityUpperFloorScript`,
@     que volta para o nivel de cima.
@
@ O estado mora em EVENT_VIRBANK_CITY_LOWER_FLOOR
@ da fonte, que aqui e
@ FLAG_UNOVA_VIRBANK_CITY_ANDAR_INFERIOR
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
@ Gatilho: os 11 `coord_event` da fonte, coordenada IDENTIDADE (a geometria de
@ gen 2 entra 1:1 em Unova, cabecalho de dev_scripts/fila_b6.py). Todos caem em
@ tile andavel do map.bin, conferido um a um.
@
@ POR QUE A VOLTA TAMBEM LEVA ELEVACAO EXPLICITA (isto NAO esta na saida crua da
@ ferramenta): 51 quadrantes trocam entre agua (elevacao 1) e chao/parede.
@ `setmetatile` NAO mexe na elevacao (src/fieldmap.c, MapGridSetMetatileIdAt
@ preserva os bits 12-15) e a marca `agua` de dev_scripts/changeblock_gen2.py e
@ relativa ao MAP.BIN, entao ela pega a ida e NAO pega a volta. Sem isto, o
@ caminho de voltar redesenharia o chao por cima da elevacao 1 da agua, e o
@ jogador surfaria em cima dele. Os 51 quadrantes sairam de comparar os DOIS
@ estados quadrante a quadrante, nao de olho.
@
@ Linha marcada `igual ao map.bin` NAO pode ser apagada: e restauracao de estado.
@ Todo numero abaixo saiu de dev_scripts/changeblock_gen2.py; nenhum digitado.
@ ----------------------------------------------------------------------------

Unova_VirbankCity_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_VirbankCity_EventScript_AoCarregar
	.byte 0

Unova_VirbankCity_EventScript_AoCarregar::
	call_if_set FLAG_UNOVA_VIRBANK_CITY_ANDAR_INFERIOR, Unova_VirbankCity_EventScript_Desce
	end

@ `VirbankCityLowerFloorScript` da fonte (a mesma lista do callback de tiles, conferida igual)
Unova_VirbankCity_EventScript_Desce::
	@ maps/VirbankCity.asm:66  changeblock  8,  8, $81
	setmetatile 8, 8, 663, TRUE   @ igual ao map.bin
	setmetatile 9, 8, 660, FALSE   @ igual ao map.bin
	setmetatile 8, 9, 743, TRUE
	setmetatileinrange 9, 9, 9, 9, 744, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:67  changeblock 10,  8, $82
	setmetatile 10, 8, 660, FALSE   @ igual ao map.bin
	setmetatile 11, 8, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 10, 9, 10, 9, 744, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 11, 9, 11, 9, 744, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:68  changeblock  8, 10, $83
	setmetatileinrange 8, 10, 8, 10, 745, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 9, 10, 9, 10, 745, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 8, 11, 8, 11, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 9, 11, 9, 11, 746, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:69  changeblock 10, 10, $83
	setmetatileinrange 10, 10, 10, 10, 745, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 11, 10, 11, 10, 745, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 10, 11, 10, 11, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 11, 11, 11, 11, 746, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:70  changeblock  8, 12, $87
	setmetatileinrange 8, 12, 8, 12, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 9, 12, 9, 12, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 8, 13, 8, 13, 748, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 9, 13, 9, 13, 748, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:71  changeblock 10, 12, $87
	setmetatileinrange 10, 12, 10, 12, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 11, 12, 11, 12, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 10, 13, 10, 13, 748, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 11, 13, 11, 13, 748, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:72  changeblock  8, 14, $8B
	setmetatileinrange 8, 14, 8, 14, 744, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 9, 14, 9, 14, 744, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 8, 15, 8, 15, 749, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 9, 15, 9, 15, 749, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:73  changeblock 10, 14, $8B
	setmetatileinrange 10, 14, 10, 14, 744, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 11, 14, 11, 14, 744, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 10, 15, 10, 15, 749, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 11, 15, 11, 15, 749, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:74  changeblock 12, 16, $8C
	changeblock_gen2 12, 16, 649, 750, 651, 751, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	@ maps/VirbankCity.asm:75  changeblock 14, 16, $8D
	changeblock_gen2 14, 16, 752, 753, 754, 755, TRUE, TRUE, FALSE, FALSE
	@ maps/VirbankCity.asm:76  changeblock 16, 16, $8E
	changeblock_gen2 16, 16, 753, 756, 755, 757, TRUE, TRUE, FALSE, FALSE
	@ maps/VirbankCity.asm:77  changeblock 18, 16, $8F
	changeblock_gen2 18, 16, 758, 650, 759, 651, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: CD, BD
	@ maps/VirbankCity.asm:78  changeblock 12, 18, $90
	setmetatile 12, 18, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 13, 18, 13, 18, 760, FALSE, 1   @ agua: elevacao explicita 1
	setmetatile 12, 19, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 13, 19, 13, 19, 760, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:79  changeblock 14, 18, $91
	setmetatileinrange 14, 18, 14, 18, 761, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 15, 18, 15, 18, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 14, 19, 14, 19, 761, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 15, 19, 15, 19, 746, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:80  changeblock 16, 18, $92
	setmetatileinrange 16, 18, 16, 18, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 17, 18, 17, 18, 762, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 16, 19, 16, 19, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 17, 19, 17, 19, 762, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:81  changeblock 18, 18, $93
	setmetatileinrange 18, 18, 18, 18, 763, FALSE, 1   @ agua: elevacao explicita 1
	setmetatile 19, 18, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 18, 19, 18, 19, 763, FALSE, 1   @ agua: elevacao explicita 1
	setmetatile 19, 19, 660, FALSE   @ igual ao map.bin
	@ maps/VirbankCity.asm:82  changeblock 12, 20, $90
	setmetatile 12, 20, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 13, 20, 13, 20, 760, FALSE, 1   @ agua: elevacao explicita 1
	setmetatile 12, 21, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 13, 21, 13, 21, 760, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:83  changeblock 14, 20, $91
	setmetatileinrange 14, 20, 14, 20, 761, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 15, 20, 15, 20, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 14, 21, 14, 21, 761, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 15, 21, 15, 21, 746, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:84  changeblock 16, 20, $92
	setmetatileinrange 16, 20, 16, 20, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 17, 20, 17, 20, 762, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 16, 21, 16, 21, 746, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 17, 21, 17, 21, 762, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VirbankCity.asm:85  changeblock 18, 20, $93
	setmetatileinrange 18, 20, 18, 20, 763, FALSE, 1   @ agua: elevacao explicita 1
	setmetatile 19, 20, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 18, 21, 18, 21, 763, FALSE, 1   @ agua: elevacao explicita 1
	setmetatile 19, 21, 660, FALSE   @ igual ao map.bin
	@ maps/VirbankCity.asm:86  changeblock  6, 10, $94
	changeblock_gen2 6, 10, 764, 764, 765, 765, TRUE, TRUE, TRUE, TRUE
	@ maps/VirbankCity.asm:87  changeblock 12, 10, $94
	changeblock_gen2 12, 10, 764, 764, 765, 765, TRUE, TRUE, TRUE, TRUE
	@ maps/VirbankCity.asm:88  changeblock  6, 12, $95
	changeblock_gen2 6, 12, 765, 765, 766, 766, TRUE, TRUE, TRUE, TRUE
	@ maps/VirbankCity.asm:89  changeblock 12, 12, $95
	changeblock_gen2 12, 12, 765, 765, 766, 766, TRUE, TRUE, TRUE, TRUE
	@ maps/VirbankCity.asm:90  changeblock 14, 22, $96
	changeblock_gen2 14, 22, 767, 765, 767, 765, TRUE, TRUE, TRUE, TRUE
	@ maps/VirbankCity.asm:91  changeblock 16, 22, $97
	changeblock_gen2 16, 22, 765, 768, 765, 768, TRUE, TRUE, TRUE, TRUE
	return

@ `VirbankCityUpperFloorScript` da fonte: o caminho de VOLTA ao estado do map.bin
Unova_VirbankCity_EventScript_Sobe::
	@ maps/VirbankCity.asm:99  changeblock  8,  8, $3E
	setmetatile 8, 8, 663, TRUE   @ igual ao map.bin
	setmetatile 9, 8, 660, FALSE   @ igual ao map.bin
	setmetatile 8, 9, 664, TRUE   @ igual ao map.bin
	setmetatileinrange 9, 9, 9, 9, 622, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:100  changeblock 10,  8, $31
	setmetatile 10, 8, 660, FALSE   @ igual ao map.bin
	setmetatile 11, 8, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 10, 9, 10, 9, 622, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 11, 9, 11, 9, 622, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:101  changeblock  8, 10, $85
	setmetatileinrange 8, 10, 8, 10, 681, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 9, 10, 9, 10, 681, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 8, 11, 8, 11, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 9, 11, 9, 11, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:102  changeblock 10, 10, $85
	setmetatileinrange 10, 10, 10, 10, 681, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 11, 10, 11, 10, 681, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 10, 11, 10, 11, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 11, 11, 11, 11, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:103  changeblock  8, 12, $89
	setmetatileinrange 8, 12, 8, 12, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 9, 12, 9, 12, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 8, 13, 8, 13, 517, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 9, 13, 9, 13, 517, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:104  changeblock 10, 12, $89
	setmetatileinrange 10, 12, 10, 12, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 11, 12, 11, 12, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 10, 13, 10, 13, 517, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 11, 13, 11, 13, 517, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:105  changeblock  8, 14, $27
	setmetatileinrange 8, 14, 8, 14, 622, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 9, 14, 9, 14, 622, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 8, 15, 8, 15, 642, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 9, 15, 9, 15, 642, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:106  changeblock 10, 14, $27
	setmetatileinrange 10, 14, 10, 14, 622, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 11, 14, 11, 14, 622, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 10, 15, 10, 15, 642, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 11, 15, 11, 15, 642, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:107  changeblock 12, 16, $33
	changeblock_gen2 12, 16, 649, 659, 651, 659, TRUE, TRUE, FALSE, TRUE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:108  changeblock 14, 16, $84
	changeblock_gen2 14, 16, 662, 515, 662, 515, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:109  changeblock 16, 16, $88
	changeblock_gen2 16, 16, 515, 738, 515, 738, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:110  changeblock 18, 16, $32
	changeblock_gen2 18, 16, 657, 650, 657, 651, TRUE, TRUE, TRUE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:111  changeblock 12, 18, $37
	setmetatile 12, 18, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 13, 18, 13, 18, 659, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatile 12, 19, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 13, 19, 13, 19, 659, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:112  changeblock 14, 18, $84
	setmetatileinrange 14, 18, 14, 18, 662, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 15, 18, 15, 18, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 14, 19, 14, 19, 662, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 15, 19, 15, 19, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:113  changeblock 16, 18, $88
	setmetatileinrange 16, 18, 16, 18, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 17, 18, 17, 18, 738, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 16, 19, 16, 19, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 17, 19, 17, 19, 738, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:114  changeblock 18, 18, $36
	setmetatileinrange 18, 18, 18, 18, 657, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatile 19, 18, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 18, 19, 18, 19, 657, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatile 19, 19, 660, FALSE   @ igual ao map.bin
	@ maps/VirbankCity.asm:115  changeblock 12, 20, $37
	setmetatile 12, 20, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 13, 20, 13, 20, 659, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatile 12, 21, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 13, 21, 13, 21, 659, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:116  changeblock 14, 20, $84
	setmetatileinrange 14, 20, 14, 20, 662, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 15, 20, 15, 20, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 14, 21, 14, 21, 662, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 15, 21, 15, 21, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:117  changeblock 16, 20, $88
	setmetatileinrange 16, 20, 16, 20, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 17, 20, 17, 20, 738, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 16, 21, 16, 21, 515, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 17, 21, 17, 21, 738, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VirbankCity.asm:118  changeblock 18, 20, $36
	setmetatileinrange 18, 20, 18, 20, 657, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatile 19, 20, 660, FALSE   @ igual ao map.bin
	setmetatileinrange 18, 21, 18, 21, 657, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatile 19, 21, 660, FALSE   @ igual ao map.bin
	@ maps/VirbankCity.asm:119  changeblock  6, 10, $85
	changeblock_gen2 6, 10, 681, 681, 515, 515, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:120  changeblock 12, 10, $85
	changeblock_gen2 12, 10, 681, 681, 515, 515, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:121  changeblock  6, 12, $89
	changeblock_gen2 6, 12, 515, 515, 517, 517, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:122  changeblock 12, 12, $89
	changeblock_gen2 12, 12, 515, 515, 517, 517, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:123  changeblock 14, 22, $84
	changeblock_gen2 14, 22, 662, 515, 662, 515, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VirbankCity.asm:124  changeblock 16, 22, $88
	changeblock_gen2 16, 22, 515, 738, 515, 738, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return

@ coord_events da fonte: (24,16) (29,16)
Unova_VirbankCity_EventScript_GatilhoDesce::
	lock
	goto_if_set FLAG_UNOVA_VIRBANK_CITY_ANDAR_INFERIOR, Unova_VirbankCity_EventScript_GatilhoFim
	setflag FLAG_UNOVA_VIRBANK_CITY_ANDAR_INFERIOR
	call Unova_VirbankCity_EventScript_Desce
	special DrawWholeMapView
	release
	end

@ coord_events da fonte: (23,16) (30,16) (14,10) (15,11) (16,10) (4,11)
@   (5,12) (5,13) (38,26)
Unova_VirbankCity_EventScript_GatilhoSobe::
	lock
	goto_if_unset FLAG_UNOVA_VIRBANK_CITY_ANDAR_INFERIOR, Unova_VirbankCity_EventScript_GatilhoFim
	clearflag FLAG_UNOVA_VIRBANK_CITY_ANDAR_INFERIOR
	call Unova_VirbankCity_EventScript_Sobe
	special DrawWholeMapView
	release
	end

Unova_VirbankCity_EventScript_GatilhoFim::
	release
	end

Unova_VirbankCity_EventScript_Placa0::
	msgbox Unova_VirbankCity_Text_VirbankCitySignText, MSGBOX_SIGN
	end

Unova_VirbankCity_EventScript_Placa1::
	msgbox Unova_VirbankCity_Text_VirbankGameCornerSignText, MSGBOX_SIGN
	end

Unova_VirbankCity_EventScript_Placa2::
	msgbox Unova_VirbankCity_Text_VirbankComplexSignText, MSGBOX_SIGN
	end

Unova_VirbankCity_EventScript_Placa3::
	msgbox Unova_VirbankCity_Text_VirbankFerrySignText, MSGBOX_SIGN
	end

Unova_VirbankCity_EventScript_Npc4::
	msgbox Unova_VirbankCity_Text_VirbankCityBlockerText, MSGBOX_NPC
	end

Unova_VirbankCity_EventScript_Npc5::
	msgbox Unova_VirbankCity_Text_VirbankFerryManText, MSGBOX_NPC
	end

Unova_VirbankCity_EventScript_Npc6::
	msgbox Unova_VirbankCity_Text_VirbankCityGoodRodText, MSGBOX_NPC
	end

Unova_VirbankCity_EventScript_Npc7::
	msgbox Unova_VirbankCity_Text_VirbankCityTeacher1Text, MSGBOX_NPC
	end

Unova_VirbankCity_EventScript_Npc8::
	msgbox Unova_VirbankCity_Text_VirbankCityTeacher2Text, MSGBOX_NPC
	end

Unova_VirbankCity_EventScript_Npc9::
	msgbox Unova_VirbankCity_Text_VirbankCitySailorText, MSGBOX_NPC
	end

Unova_VirbankCity_EventScript_Npc10::
	msgbox Unova_VirbankCity_Text_VirbankCityRoughneckText, MSGBOX_NPC
	end

Unova_VirbankCity_EventScript_Npc11::
	msgbox Unova_VirbankCity_Text_VirbankCityYoungsterText, MSGBOX_NPC
	end

Unova_VirbankCity_EventScript_Npc12::
	msgbox Unova_VirbankCity_Text_VirbankCityPokefanMText, MSGBOX_NPC
	end


Unova_VirbankCity_Text_VirbankCitySignText::
	.string "VIRBANK CITY"
	.string "\pCity of falling"
	.string "\nfog and rising"
	.string "\lstars!$"

Unova_VirbankCity_Text_VirbankGameCornerSignText::
	.string "VIRBANK CITY"
	.string "\nGAME CORNER!"
	.string "\pCome win fabulous"
	.string "\nprizes!$"

Unova_VirbankCity_Text_VirbankComplexSignText::
	.string "VIRBANK COMPLEX"
	.string "\nahead.$"

Unova_VirbankCity_Text_VirbankFerrySignText::
	.string "FERRY service to"
	.string "\nCASTELIA CITY."
	.string "\pInquire within.$"

Unova_VirbankCity_Text_VirbankCityBlockerText::
	.string "Sorry kid, POKé-"
	.string "\nSTAR STUDIOS is"
	.string "\pclosed to the"
	.string "\npublic."
	.string "\pYou should go"
	.string "\ncheck out the new"
	.string "\lGAME CORNER.$"

Unova_VirbankCity_Text_VirbankFerryManText::
	.string "Ahoy! This be the"
	.string "\nFERRY to CASTELIA"
	.string "\lCITY."
	.string "\pIf ye've got a"
	.string "\nticket, go show it"
	.string "\lto the fellow"
	.string "\linside!$"

Unova_VirbankCity_Text_VirbankCityGoodRodText::
	.string "Hi there! Do you"
	.string "\nlike to fish?$"

Unova_VirbankCity_Text_VirbankCityTeacher1Text::
	.string "I lost at the slot"
	.string "\nmachines again…"
	.string "\pThe new GAME"
	.string "\nCORNER is a branch"
	.string "\pof the one in"
	.string "\nCASTELIA CITY."
	.string "\pI think they have"
	.string "\ndifferent prizes.$"

Unova_VirbankCity_Text_VirbankCityTeacher2Text::
	.string "ROXIE's poison is"
	.string "\nintense! It"
	.string "\lreally stings!"
	.string "\pBut you know what?"
	.string "\nCatch a MAGNEMITE"
	.string "\pin the COMPLEX and"
	.string "\nyou'll be just"
	.string "\lfine!$"

Unova_VirbankCity_Text_VirbankCitySailorText::
	.string "Aww man, I lost my"
	.string "\nFERRY TICKET at"
	.string "\lthe COMPLEX again…"
	.string "\pBoss is gonna be"
	.string "\nso mad!$"

Unova_VirbankCity_Text_VirbankCityRoughneckText::
	.string "I tried to get"
	.string "\ninto the GYM, but"
	.string "\pI couldn't figure"
	.string "\nout their puzzle!$"

Unova_VirbankCity_Text_VirbankCityYoungsterText::
	.string "CASTELIA CITY is"
	.string "\nacross the sea."
	.string "\pI want to ride"
	.string "\nthe ferry!$"

Unova_VirbankCity_Text_VirbankCityPokefanMText::
	.string "VIRBANK CITY is"
	.string "\nthe city of"
	.string "\lindustry!"
	.string "\pWe're proud of our"
	.string "\nbustling burg!$"
