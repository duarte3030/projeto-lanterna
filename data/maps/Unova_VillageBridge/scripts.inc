@ VillageBridge do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ ----------------------------------------------------------------------------
@ B3 (Obra 2 de Unova, 15/08/2026): TROCA DE NIVEL, portada de
@ fontes-mapas/bw3g/maps/VillageBridge.asm.
@
@ Na fonte sao tres pedacos:
@   - callback MAPCALLBACK_TILES `.SetTiles`, que reaplica o estado ao carregar o mapa;
@   - `VillageBridgeLowerScript`,
@     que desce para debaixo da ponte;
@   - `VillageBridgeUpperScript`,
@     que volta para o tabuado.
@
@ O estado mora em EVENT_VILLAGE_BRIDGE_LOWER
@ da fonte, que aqui e
@ FLAG_UNOVA_VILLAGE_BRIDGE_ANDAR_INFERIOR
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
@ Gatilho: os 16 `coord_event` da fonte, coordenada IDENTIDADE (a geometria de
@ gen 2 entra 1:1 em Unova, cabecalho de dev_scripts/fila_b6.py). Todos caem em
@ tile andavel do map.bin, conferido um a um.
@
@ POR QUE A VOLTA TAMBEM LEVA ELEVACAO EXPLICITA (isto NAO esta na saida crua da
@ ferramenta): 32 quadrantes trocam entre agua (elevacao 1) e chao/parede.
@ `setmetatile` NAO mexe na elevacao (src/fieldmap.c, MapGridSetMetatileIdAt
@ preserva os bits 12-15) e a marca `agua` de dev_scripts/changeblock_gen2.py e
@ relativa ao MAP.BIN, entao ela pega a ida e NAO pega a volta. Sem isto, o
@ caminho de voltar redesenharia o chao por cima da elevacao 1 da agua, e o
@ jogador surfaria em cima dele. Os 32 quadrantes sairam de comparar os DOIS
@ estados quadrante a quadrante, nao de olho.
@
@ Linha marcada `igual ao map.bin` NAO pode ser apagada: e restauracao de estado.
@ Todo numero abaixo saiu de dev_scripts/changeblock_gen2.py; nenhum digitado.
@ ----------------------------------------------------------------------------

Unova_VillageBridge_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_VillageBridge_EventScript_AoCarregar
	.byte 0

Unova_VillageBridge_EventScript_AoCarregar::
	call_if_set FLAG_UNOVA_VILLAGE_BRIDGE_ANDAR_INFERIOR, Unova_VillageBridge_EventScript_Desce
	end

@ `VillageBridgeLowerScript` da fonte (a mesma lista do callback de tiles, conferida igual)
Unova_VillageBridge_EventScript_Desce::
	@ maps/VillageBridge.asm:49  changeblock 28, 14, $a0
	changeblock_gen2 28, 14, 671, 714, 718, 714, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD
	@ maps/VillageBridge.asm:50  changeblock 30, 14, $a1
	setmetatile 30, 14, 527, FALSE   @ igual ao map.bin
	setmetatile 31, 14, 529, FALSE   @ igual ao map.bin
	setmetatileinrange 30, 15, 30, 15, 719, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 31, 15, 31, 15, 720, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:51  changeblock 32, 14, $9a
	setmetatileinrange 32, 14, 32, 14, 710, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 33, 14, 33, 14, 711, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 32, 15, 32, 15, 712, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 33, 15, 33, 15, 713, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:52  changeblock 34, 14, $a2
	setmetatile 34, 14, 529, FALSE   @ igual ao map.bin
	setmetatile 35, 14, 529, FALSE   @ igual ao map.bin
	setmetatileinrange 34, 15, 34, 15, 719, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 35, 15, 35, 15, 720, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:53  changeblock 36, 14, $a3
	changeblock_gen2 36, 14, 717, 533, 714, 721, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD
	@ maps/VillageBridge.asm:54  changeblock 28, 16, $b3
	changeblock_gen2 28, 16, 731, 724, 731, 725, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CD, BD
	@ maps/VillageBridge.asm:55  changeblock 30, 16, $a4
	setmetatileinrange 30, 16, 30, 16, 722, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 31, 16, 31, 16, 723, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 30, 17, 30, 17, 722, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 31, 17, 31, 17, 723, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:56  changeblock 32, 16, $b1
	setmetatileinrange 32, 16, 32, 16, 740, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 33, 16, 33, 16, 741, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 32, 17, 32, 17, 742, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 33, 17, 33, 17, 743, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:57  changeblock 34, 16, $a4
	setmetatileinrange 34, 16, 34, 16, 722, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 35, 16, 35, 16, 723, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 34, 17, 34, 17, 722, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 35, 17, 35, 17, 723, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:58  changeblock 36, 16, $e3
	changeblock_gen2 36, 16, 724, 735, 725, 735, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	@ maps/VillageBridge.asm:59  changeblock 28, 18, $ac
	changeblock_gen2 28, 18, 731, 727, 718, 732, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CD
	@ maps/VillageBridge.asm:60  changeblock 30, 18, $ad
	setmetatileinrange 30, 18, 30, 18, 722, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 31, 18, 31, 18, 723, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 30, 19, 30, 19, 720, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 31, 19, 31, 19, 720, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:61  changeblock 32, 18, $b5
	setmetatileinrange 32, 18, 32, 18, 752, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 33, 18, 33, 18, 753, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 32, 19, 32, 19, 754, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 33, 19, 33, 19, 755, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:62  changeblock 34, 18, $ad
	setmetatileinrange 34, 18, 34, 18, 722, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 35, 18, 35, 18, 723, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 34, 19, 34, 19, 720, FALSE, 1   @ agua: elevacao explicita 1
	setmetatileinrange 35, 19, 35, 19, 720, FALSE, 1   @ agua: elevacao explicita 1
	@ maps/VillageBridge.asm:63  changeblock 36, 18, $af
	changeblock_gen2 36, 18, 727, 735, 732, 718, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE
	return

@ `VillageBridgeUpperScript` da fonte: o caminho de VOLTA ao estado do map.bin
Unova_VillageBridge_EventScript_Sobe::
	@ maps/VillageBridge.asm:71  changeblock 28, 14, $9c
	changeblock_gen2 28, 14, 671, 714, 600, 715, FALSE, FALSE, TRUE, TRUE   @ igual ao map.bin: os 4
	@ maps/VillageBridge.asm:72  changeblock 30, 14, $9d
	setmetatile 30, 14, 527, FALSE   @ igual ao map.bin
	setmetatile 31, 14, 529, FALSE   @ igual ao map.bin
	setmetatileinrange 30, 15, 30, 15, 716, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 31, 15, 31, 15, 600, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:73  changeblock 32, 14, $99
	setmetatileinrange 32, 14, 32, 14, 706, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 33, 14, 33, 14, 707, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 32, 15, 32, 15, 708, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 33, 15, 33, 15, 709, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:74  changeblock 34, 14, $9e
	setmetatile 34, 14, 529, FALSE   @ igual ao map.bin
	setmetatile 35, 14, 529, FALSE   @ igual ao map.bin
	setmetatileinrange 34, 15, 34, 15, 716, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 35, 15, 35, 15, 600, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:75  changeblock 36, 14, $9f
	changeblock_gen2 36, 14, 717, 533, 715, 716, FALSE, FALSE, TRUE, TRUE   @ igual ao map.bin: os 4
	@ maps/VillageBridge.asm:76  changeblock 28, 16, $a5
	changeblock_gen2 28, 16, 611, 724, 611, 725, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VillageBridge.asm:77  changeblock 30, 16, $56
	setmetatileinrange 30, 16, 30, 16, 611, FALSE, 3   @ elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 31, 16, 31, 16, 611, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 30, 17, 30, 17, 611, FALSE, 3   @ elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 31, 17, 31, 17, 611, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:78  changeblock 32, 16, $b0
	setmetatileinrange 32, 16, 32, 16, 736, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 33, 16, 33, 16, 737, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 32, 17, 32, 17, 738, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 33, 17, 33, 17, 739, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:79  changeblock 34, 16, $56
	setmetatileinrange 34, 16, 34, 16, 611, FALSE, 3   @ elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 35, 16, 35, 16, 611, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 34, 17, 34, 17, 611, FALSE, 3   @ elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 35, 17, 35, 17, 611, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:80  changeblock 36, 16, $a6
	changeblock_gen2 36, 16, 724, 726, 725, 726, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/VillageBridge.asm:81  changeblock 28, 18, $a8
	changeblock_gen2 28, 18, 611, 727, 600, 728, FALSE, FALSE, TRUE, TRUE   @ igual ao map.bin: os 4
	@ maps/VillageBridge.asm:82  changeblock 30, 18, $a9
	setmetatileinrange 30, 18, 30, 18, 726, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 31, 18, 31, 18, 611, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 30, 19, 30, 19, 600, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 31, 19, 31, 19, 600, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:83  changeblock 32, 18, $b4
	setmetatileinrange 32, 18, 32, 18, 748, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 33, 18, 33, 18, 749, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 32, 19, 32, 19, 750, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 33, 19, 33, 19, 751, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:84  changeblock 34, 18, $a9
	setmetatileinrange 34, 18, 34, 18, 726, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 35, 18, 35, 18, 611, FALSE, 3   @ igual ao map.bin, elevacao explicita 3: o OUTRO estado poe agua aqui
	setmetatileinrange 34, 19, 34, 19, 600, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	setmetatileinrange 35, 19, 35, 19, 600, TRUE, 0   @ igual ao map.bin, elevacao explicita 0: o OUTRO estado poe agua aqui
	@ maps/VillageBridge.asm:85  changeblock 36, 18, $ab
	changeblock_gen2 36, 18, 727, 726, 728, 600, FALSE, FALSE, TRUE, TRUE   @ igual ao map.bin: os 4
	return

@ coord_events da fonte: (21,30) (21,31) (43,30) (43,31)
Unova_VillageBridge_EventScript_GatilhoDesce::
	lock
	goto_if_set FLAG_UNOVA_VILLAGE_BRIDGE_ANDAR_INFERIOR, Unova_VillageBridge_EventScript_GatilhoFim
	setflag FLAG_UNOVA_VILLAGE_BRIDGE_ANDAR_INFERIOR
	call Unova_VillageBridge_EventScript_Desce
	special DrawWholeMapView
	release
	end

@ coord_events da fonte: (61,19) (60,20) (60,21) (61,22) (4,19) (5,20)
@   (5,21) (4,22) (20,30) (20,31) (44,30) (44,31)
Unova_VillageBridge_EventScript_GatilhoSobe::
	lock
	goto_if_unset FLAG_UNOVA_VILLAGE_BRIDGE_ANDAR_INFERIOR, Unova_VillageBridge_EventScript_GatilhoFim
	clearflag FLAG_UNOVA_VILLAGE_BRIDGE_ANDAR_INFERIOR
	call Unova_VillageBridge_EventScript_Sobe
	special DrawWholeMapView
	release
	end

Unova_VillageBridge_EventScript_GatilhoFim::
	release
	end

Unova_VillageBridge_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_MUSICIAN_VILLAGE_BRIDGE, Unova_VillageBridge_Text_MusicianVillageBridgeSeenText, Unova_VillageBridge_Text_MusicianVillageBridgeBeatenText
	end

Unova_VillageBridge_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SMASHER_VILLAGE_BRIDGE_1, Unova_VillageBridge_Text_Smasher1VillageBridgeSeenText, Unova_VillageBridge_Text_Smasher1VillageBridgeBeatenText
	end

Unova_VillageBridge_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_SMASHER_VILLAGE_BRIDGE_2, Unova_VillageBridge_Text_Smasher2VillageBridgeSeenText, Unova_VillageBridge_Text_Smasher2VillageBridgeBeatenText
	end

Unova_VillageBridge_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_LINEBACKER_VILLAGE_BRIDGE, Unova_VillageBridge_Text_LinebackerVillageBridgeSeenText, Unova_VillageBridge_Text_LinebackerVillageBridgeBeatenText
	end

Unova_VillageBridge_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_HOOPSTER_VILLAGE_BRIDGE_1, Unova_VillageBridge_Text_Hoopster1VillageBridgeSeenText, Unova_VillageBridge_Text_Hoopster1VillageBridgeBeatenText
	end

Unova_VillageBridge_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_HOOPSTER_VILLAGE_BRIDGE_2, Unova_VillageBridge_Text_Hoopster2VillageBridgeSeenText, Unova_VillageBridge_Text_Hoopster2VillageBridgeBeatenText
	end


Unova_VillageBridge_Text_MusicianVillageBridgeSeenText::
	.string "Hum fiercely! My"
	.string "\nbattle song!"
	.string "\pBattle fiercely!"
	.string "\nMy POKéMON!$"

Unova_VillageBridge_Text_MusicianVillageBridgeBeatenText::
	.string "Hm… I guess"
	.string "\nstrumming instead"
	.string "\pof tapping would"
	.string "\nbe best…$"

Unova_VillageBridge_Text_Smasher1VillageBridgeSeenText::
	.string "My serve is 120"
	.string "\nmiles per hour!"
	.string "\pThat's the kind of"
	.string "\nkiller attack I'm"
	.string "\labout to show you!$"

Unova_VillageBridge_Text_Smasher1VillageBridgeBeatenText::
	.string "I wanted to cont-"
	.string "\ninue the rally a"
	.string "\llittle bit longer!$"

Unova_VillageBridge_Text_Smasher2VillageBridgeSeenText::
	.string "Watch my furious"
	.string "\ntennis footwork!"
	.string "\pyou get it now?"
	.string "\nWe're tough!$"

Unova_VillageBridge_Text_Smasher2VillageBridgeBeatenText::
	.string "But… I'm tough"
	.string "\nenough to play all"
	.string "\lday and all night…$"

Unova_VillageBridge_Text_LinebackerVillageBridgeSeenText::
	.string "Shut up and battle"
	.string "\nwith me!$"

Unova_VillageBridge_Text_LinebackerVillageBridgeBeatenText::
	.string "…!$"

Unova_VillageBridge_Text_Hoopster1VillageBridgeSeenText::
	.string "Oh! You look"
	.string "\npretty good! Let's"
	.string "\lplay some pickup!$"

Unova_VillageBridge_Text_Hoopster1VillageBridgeBeatenText::
	.string "That's game! You"
	.string "\ntotally crushed"
	.string "\lme!$"

Unova_VillageBridge_Text_Hoopster2VillageBridgeSeenText::
	.string "Fooling you fair"
	.string "\nand square! That's"
	.string "\pwhat we call a"
	.string "\ntrick play!$"

Unova_VillageBridge_Text_Hoopster2VillageBridgeBeatenText::
	.string "What the hoops? I"
	.string "\nwas the one who"
	.string "\lwas tricked!$"

@ NPCs ligados a partir do BW3G por dev_scripts/importa_npcs_unova.py

@ FRUITTREE_VILLAGE_BRIDGE do BW3G. ponytail: no gen 2 a arvore reenche;
@ aqui a fruta sai uma vez, porque replantio e outra mecanica.
Unova_VillageBridge_EventScript_Arvore::
	lock
	goto_if_set FLAG_UNOVA_ARVORE_VILLAGE_BRIDGE, Unova_EventScript_GrutaVazia
	giveitem ITEM_CHESTO_BERRY
	setflag FLAG_UNOVA_ARVORE_VILLAGE_BRIDGE
	release
	end
