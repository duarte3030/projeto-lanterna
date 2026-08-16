@ VirbankComplexB2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@
@ B4 da Obra 2 (changeblock), 15/08/2026. O caso mais pesado da obra. Linhas de
@ metatile geradas por dev_scripts/changeblock_gen2.py; nenhum id de metatile
@ foi digitado à mão.
@
@ MECANISMO DA FONTE: quatro interruptores de chão, (4,11), (4,17), (16,11) e
@ (16,17), cada um com DUAS posições. Cada um move a própria plataforma E as
@ passarelas que ele divide com os vizinhos, então o desenho de cinco tiles
@ depende de DOIS interruptores ao mesmo tempo. Na fonte isso está escrito como
@ produto cartesiano à mão: o `.SetTiles` (MAPCALLBACK_TILES, 129 linhas) mais
@ oito meias-rotinas `SetPosition1`/`SetPosition2`, ~570 linhas de changeblock
@ com muita repetição.
@
@ O QUE FOI FEITO AQUI, E POR QUÊ (desvio consciente da transcrição literal):
@ em vez das nove rotinas da fonte, UM renderizador
@ (`..._EventScript_Desenha`) que escreve o estado COMPLETO a partir das quatro
@ flags, e que serve tanto ao ON_LOAD quanto aos quatro gatilhos. Motivo: o
@ `.SetTiles` da fonte só sabe DESENHAR o que está ligado (ele conta com o mapa
@ recém-carregado do layout para o resto), e por isso a fonte precisa das oito
@ meias-rotinas para DESFAZER quando o jogador aperta um interruptor com o mapa
@ já mexido. Escrevendo os dois lados de cada grupo, o mesmo código serve para
@ os dois usos e some a chance de os dois caminhos divergirem.
@ Isso não é chute: o estado ESTÁTICO do map.bin é exatamente "os quatro
@ desligados", e a prova é que as 44 linhas dos ramos Desligada mais as 5 do
@ caso 00 das passarelas saem TODAS marcadas `igual ao map.bin: os 4` pelo
@ gerador (49 de 49). Se uma só não fechasse, a tabela estaria errada.
@ Custo: 4 flags, as mesmas do PLANO-OBRAS-UNOVA.md. ZERO flag nova, ZERO var.
@
@ Decomposição (medida na fonte, não inventada): 4 grupos que dependem de UM
@ interruptor (a plataforma e as passarelas dele) e 5 tiles compartilhados que
@ dependem de DOIS: (4,14) de 1 e 2, (10,10) de 1 e 3, (10,14) de 2 e 3,
@ (10,16) de 2 e 4, (16,14) de 3 e 4. Cada grupo tem o MESMO conjunto de
@ coordenadas nas duas posições, conferido um a um.
@
@ ponytail: a fonte toca SFX_ENTER_DOOR e faz `reloadmappart` duas vezes por
@ aperto (primeiro somem as passarelas, depois aparecem as outras). Aqui é um
@ som e um `special DrawWholeMapView` só, no fim. O estado final é o mesmo; o
@ que se perde é o meio-quadro da animação.
@
@ Armadilha da elevação (a de VictoryRoadCave1F e dos mapas de água do B3): não
@ existe aqui. O map.bin deste mapa só tem elevação 0 e 3 (medido: 69 e 415
@ células, ZERO de água), e elevação 0 casa com qualquer outra em
@ IsElevationMismatchAt, então `setmetatile` preservando elevação é seguro.
@
@ Nota de tileset: os blocos $41 e $42 da fonte caem nos MESMOS metatiles aqui
@ (584, 586, 588, 590), então os ramos 00 e 10 de (4,14) e de (16,14) saem com
@ linhas idênticas. Os dois ramos ficam escritos assim mesmo, porque a
@ diferença é da arte da fonte e volta sozinha se o tileset melhorar.
@
@ A memória do quebra-cabeça é apagada ao subir: `.CheckDoor` do
@ VirbankComplexB1F (o andar de cima) faz clearflag nos quatro, e isso está
@ portado lá, não aqui.

Unova_VirbankComplexB2F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_VirbankComplexB2F_EventScript_AoCarregar
	.byte 0

@ `.SetTiles` da fonte, linhas 19-147.
Unova_VirbankComplexB2F_EventScript_AoCarregar::
	call Unova_VirbankComplexB2F_EventScript_Desenha
	end

@ `VirbankComplexB2FSwitch1Script` da fonte: coord_event (4,11).
Unova_VirbankComplexB2F_EventScript_Interruptor1::
	lockall
	playse SE_SWITCH
	msgbox Unova_VirbankComplexB2F_Text_Interruptor, MSGBOX_DEFAULT
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1, Unova_VirbankComplexB2F_EventScript_Interruptor1Desliga
	setflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1
	goto Unova_VirbankComplexB2F_EventScript_Aplica
Unova_VirbankComplexB2F_EventScript_Interruptor1Desliga::
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1
	goto Unova_VirbankComplexB2F_EventScript_Aplica

@ `VirbankComplexB2FSwitch2Script` da fonte: coord_event (4,17).
Unova_VirbankComplexB2F_EventScript_Interruptor2::
	lockall
	playse SE_SWITCH
	msgbox Unova_VirbankComplexB2F_Text_Interruptor, MSGBOX_DEFAULT
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2, Unova_VirbankComplexB2F_EventScript_Interruptor2Desliga
	setflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2
	goto Unova_VirbankComplexB2F_EventScript_Aplica
Unova_VirbankComplexB2F_EventScript_Interruptor2Desliga::
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2
	goto Unova_VirbankComplexB2F_EventScript_Aplica

@ `VirbankComplexB2FSwitch3Script` da fonte: coord_event (16,11).
Unova_VirbankComplexB2F_EventScript_Interruptor3::
	lockall
	playse SE_SWITCH
	msgbox Unova_VirbankComplexB2F_Text_Interruptor, MSGBOX_DEFAULT
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3, Unova_VirbankComplexB2F_EventScript_Interruptor3Desliga
	setflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3
	goto Unova_VirbankComplexB2F_EventScript_Aplica
Unova_VirbankComplexB2F_EventScript_Interruptor3Desliga::
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3
	goto Unova_VirbankComplexB2F_EventScript_Aplica

@ `VirbankComplexB2FSwitch4Script` da fonte: coord_event (16,17).
Unova_VirbankComplexB2F_EventScript_Interruptor4::
	lockall
	playse SE_SWITCH
	msgbox Unova_VirbankComplexB2F_Text_Interruptor, MSGBOX_DEFAULT
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4, Unova_VirbankComplexB2F_EventScript_Interruptor4Desliga
	setflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4
	goto Unova_VirbankComplexB2F_EventScript_Aplica
Unova_VirbankComplexB2F_EventScript_Interruptor4Desliga::
	clearflag FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4
Unova_VirbankComplexB2F_EventScript_Aplica::
	call Unova_VirbankComplexB2F_EventScript_Desenha
	playse SE_DOOR
	special DrawWholeMapView
	waitse
	releaseall
	end

@ O renderizador: estado completo do andar a partir das 4 flags.
Unova_VirbankComplexB2F_EventScript_Desenha::
	call Unova_VirbankComplexB2F_EventScript_Plataforma1
	call Unova_VirbankComplexB2F_EventScript_Plataforma2
	call Unova_VirbankComplexB2F_EventScript_Plataforma3
	call Unova_VirbankComplexB2F_EventScript_Plataforma4
	call Unova_VirbankComplexB2F_EventScript_Passarela0414
	call Unova_VirbankComplexB2F_EventScript_Passarela1010
	call Unova_VirbankComplexB2F_EventScript_Passarela1014
	call Unova_VirbankComplexB2F_EventScript_Passarela1016
	call Unova_VirbankComplexB2F_EventScript_Passarela1614
	return

@ Plataforma 1, os 11 blocos que só dependem do interruptor 1.
@ Ligada: maps/VirbankComplexB2F.asm:22-32. Desligada: :195-205 (o
@ `.SetPosition1` do mesmo interruptor), e é o estado do map.bin.
Unova_VirbankComplexB2F_EventScript_Plataforma1::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1, Unova_VirbankComplexB2F_EventScript_Plataforma1Ligada
	changeblock_gen2 4, 8, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 4, 12, 647, 649, 651, 653, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 8, 10, 600, 602, 604, 606, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 8, 12, 642, 643, 594, 594, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 4, 10, 596, 622, 624, 622, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 0, 10, 564, 638, 618, 622, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 2, 10, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 2, 12, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 10, 8, 636, 636, 594, 594, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 6, 10, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 6, 12, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Plataforma1Ligada::
	changeblock_gen2 4, 8, 636, 636, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 4, 12, 639, 640, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 8, 10, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 8, 12, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 4, 10, 618, 618, 624, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BE
	changeblock_gen2 0, 10, 564, 620, 618, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	changeblock_gen2 2, 10, 600, 602, 604, 606, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 2, 12, 642, 643, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 10, 8, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 6, 10, 608, 610, 612, 614, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 6, 12, 644, 645, 594, 594, TRUE, TRUE, FALSE, FALSE
	return

@ Plataforma 2, os 10 blocos que só dependem do interruptor 2.
@ Ligada: maps/VirbankComplexB2F.asm:79-88. Desligada: :297-317.
Unova_VirbankComplexB2F_EventScript_Plataforma2::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2, Unova_VirbankComplexB2F_EventScript_Plataforma2Ligada
	changeblock_gen2 4, 18, 647, 649, 651, 653, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 8, 16, 600, 602, 604, 606, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 8, 18, 642, 643, 594, 594, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 4, 16, 596, 622, 624, 622, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 4, 20, 517, 517, 517, 517, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 0, 16, 618, 616, 598, 622, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 2, 16, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 2, 18, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 6, 16, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 6, 18, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Plataforma2Ligada::
	changeblock_gen2 4, 18, 639, 640, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 8, 16, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 8, 18, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 4, 16, 618, 618, 624, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BE
	changeblock_gen2 4, 20, 618, 618, 598, 598, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 0, 16, 618, 618, 598, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	changeblock_gen2 2, 16, 600, 602, 604, 606, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 2, 18, 642, 643, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 6, 16, 608, 610, 612, 614, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 6, 18, 644, 645, 594, 594, TRUE, TRUE, FALSE, FALSE
	return

@ Plataforma 3, os 11 blocos que só dependem do interruptor 3.
@ Ligada: maps/VirbankComplexB2F.asm:113-122 mais o (10,12) da linha 137.
@ Desligada: :404-425.
Unova_VirbankComplexB2F_EventScript_Plataforma3::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3, Unova_VirbankComplexB2F_EventScript_Plataforma3Ligada
	changeblock_gen2 16, 8, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 16, 12, 647, 649, 651, 653, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 10, 608, 610, 612, 614, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 12, 644, 645, 594, 594, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 16, 10, 596, 622, 624, 622, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 20, 10, 638, 564, 596, 618, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 18, 10, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 18, 12, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 14, 10, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 14, 12, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 10, 12, 639, 640, 594, 594, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Plataforma3Ligada::
	changeblock_gen2 16, 8, 636, 636, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 16, 12, 639, 640, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 12, 10, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 12, 12, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 16, 10, 618, 618, 624, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BE
	changeblock_gen2 20, 10, 616, 564, 598, 618, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CD, BD
	changeblock_gen2 18, 10, 608, 610, 612, 614, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 18, 12, 644, 645, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 14, 10, 600, 602, 604, 606, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 14, 12, 642, 643, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 10, 12, 647, 649, 651, 653, FALSE, FALSE, FALSE, FALSE
	return

@ Plataforma 4, os 12 blocos que só dependem do interruptor 4.
@ Ligada: maps/VirbankComplexB2F.asm:50-61. Desligada: :513-534.
Unova_VirbankComplexB2F_EventScript_Plataforma4::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4, Unova_VirbankComplexB2F_EventScript_Plataforma4Ligada
	changeblock_gen2 16, 18, 647, 649, 651, 653, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 16, 608, 610, 612, 614, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 18, 644, 645, 594, 594, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 16, 16, 596, 622, 624, 622, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 16, 20, 517, 517, 517, 517, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 10, 20, 618, 618, 598, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 20, 16, 620, 618, 596, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 18, 16, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 18, 18, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 10, 18, 639, 640, 594, 594, TRUE, TRUE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 14, 16, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 14, 18, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Plataforma4Ligada::
	changeblock_gen2 16, 18, 639, 640, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 12, 16, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 12, 18, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 16, 16, 618, 618, 624, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BE
	changeblock_gen2 16, 20, 618, 618, 598, 598, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 10, 20, 517, 517, 517, 517, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 20, 16, 618, 618, 598, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CD, BD
	changeblock_gen2 18, 16, 608, 610, 612, 614, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 18, 18, 644, 645, 594, 594, TRUE, TRUE, FALSE, FALSE
	changeblock_gen2 10, 18, 647, 649, 651, 653, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 14, 16, 600, 602, 604, 606, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 14, 18, 642, 643, 594, 594, TRUE, TRUE, FALSE, FALSE
	return

@ Passarela de (4,14): interruptores 1 e 2. Fonte: $41 nos dois desligados,
@ $42 só com o 1, $43 só com o 2, $1B com os dois.
Unova_VirbankComplexB2F_EventScript_Passarela0414::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1, Unova_VirbankComplexB2F_EventScript_Passarela0414Com1
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2, Unova_VirbankComplexB2F_EventScript_Passarela0414So2
	changeblock_gen2 4, 14, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Passarela0414So2::
	changeblock_gen2 4, 14, 591, 592, 594, 594, TRUE, TRUE, FALSE, FALSE
	return
Unova_VirbankComplexB2F_EventScript_Passarela0414Com1::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2, Unova_VirbankComplexB2F_EventScript_Passarela0414Ambos
	changeblock_gen2 4, 14, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Passarela0414Ambos::
	changeblock_gen2 4, 14, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	return

@ Passarela de (10,10): interruptores 1 e 3. Fonte: $50 nos dois desligados,
@ $44 só com o 1, $4A só com o 3, $4B com os dois.
Unova_VirbankComplexB2F_EventScript_Passarela1010::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_1, Unova_VirbankComplexB2F_EventScript_Passarela1010Com1
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3, Unova_VirbankComplexB2F_EventScript_Passarela1010So3
	changeblock_gen2 10, 10, 618, 618, 598, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Passarela1010So3::
	changeblock_gen2 10, 10, 618, 616, 598, 622, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	return
Unova_VirbankComplexB2F_EventScript_Passarela1010Com1::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3, Unova_VirbankComplexB2F_EventScript_Passarela1010Ambos
	changeblock_gen2 10, 10, 596, 598, 596, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BD
	return
Unova_VirbankComplexB2F_EventScript_Passarela1010Ambos::
	changeblock_gen2 10, 10, 596, 622, 596, 622, FALSE, FALSE, FALSE, FALSE
	return

@ Passarela de (10,14): interruptores 2 e 3. Fonte: $1B nos dois desligados,
@ $42 só com o 2, $43 só com o 3, $41 com os dois.
Unova_VirbankComplexB2F_EventScript_Passarela1014::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2, Unova_VirbankComplexB2F_EventScript_Passarela1014Com2
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3, Unova_VirbankComplexB2F_EventScript_Passarela1014So3
	changeblock_gen2 10, 14, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Passarela1014So3::
	changeblock_gen2 10, 14, 591, 592, 594, 594, TRUE, TRUE, FALSE, FALSE
	return
Unova_VirbankComplexB2F_EventScript_Passarela1014Com2::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3, Unova_VirbankComplexB2F_EventScript_Passarela1014Ambos
	changeblock_gen2 10, 14, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE
	return
Unova_VirbankComplexB2F_EventScript_Passarela1014Ambos::
	changeblock_gen2 10, 14, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE
	return

@ Passarela de (10,16): interruptores 2 e 4. Fonte: $50 nos dois desligados,
@ $44 só com o 2, $4A só com o 4, $4B com os dois.
Unova_VirbankComplexB2F_EventScript_Passarela1016::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_2, Unova_VirbankComplexB2F_EventScript_Passarela1016Com2
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4, Unova_VirbankComplexB2F_EventScript_Passarela1016So4
	changeblock_gen2 10, 16, 618, 618, 598, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Passarela1016So4::
	changeblock_gen2 10, 16, 618, 616, 598, 622, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	return
Unova_VirbankComplexB2F_EventScript_Passarela1016Com2::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4, Unova_VirbankComplexB2F_EventScript_Passarela1016Ambos
	changeblock_gen2 10, 16, 596, 598, 596, 598, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: BD
	return
Unova_VirbankComplexB2F_EventScript_Passarela1016Ambos::
	changeblock_gen2 10, 16, 596, 622, 596, 622, FALSE, FALSE, FALSE, FALSE
	return

@ Passarela de (16,14): interruptores 3 e 4. Fonte: $41 nos dois desligados,
@ $42 só com o 3, $43 só com o 4, $1B com os dois.
Unova_VirbankComplexB2F_EventScript_Passarela1614::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_3, Unova_VirbankComplexB2F_EventScript_Passarela1614Com3
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4, Unova_VirbankComplexB2F_EventScript_Passarela1614So4
	changeblock_gen2 16, 14, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Passarela1614So4::
	changeblock_gen2 16, 14, 591, 592, 594, 594, TRUE, TRUE, FALSE, FALSE
	return
Unova_VirbankComplexB2F_EventScript_Passarela1614Com3::
	goto_if_set FLAG_UNOVA_VIRBANK_COMPLEX_B2F_INTERRUPTOR_4, Unova_VirbankComplexB2F_EventScript_Passarela1614Ambos
	changeblock_gen2 16, 14, 584, 586, 588, 590, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return
Unova_VirbankComplexB2F_EventScript_Passarela1614Ambos::
	changeblock_gen2 16, 14, 564, 564, 564, 564, FALSE, FALSE, FALSE, FALSE
	return

Unova_VirbankComplexB2F_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_VIRBANK_COMPLEX_3, Unova_VirbankComplexB2F_Text_GruntMVirbankComplexB2FSeenText, Unova_VirbankComplexB2F_Text_GruntMVirbankComplexB2FBeatenText
	end

Unova_VirbankComplexB2F_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_GRUNTF_VIRBANK_COMPLEX_2, Unova_VirbankComplexB2F_Text_GruntFVirbankComplexB2FSeenText, Unova_VirbankComplexB2F_Text_GruntFVirbankComplexB2FBeatenText
	end

Unova_VirbankComplexB2F_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTM_VIRBANK_COMPLEX, Unova_VirbankComplexB2F_Text_ScientistMVirbankComplexB2FSeenText, Unova_VirbankComplexB2F_Text_ScientistMVirbankComplexB2FBeatenText
	end

Unova_VirbankComplexB2F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTF_VIRBANK_COMPLEX_2, Unova_VirbankComplexB2F_Text_ScientistFVirbankComplexB2FSeenText, Unova_VirbankComplexB2F_Text_ScientistFVirbankComplexB2FBeatenText
	end


@ `VirbankComplexSwitchText` da fonte (maps/VirbankComplexB2F.asm:601).
Unova_VirbankComplexB2F_Text_Interruptor::
	.string "Click!$"

Unova_VirbankComplexB2F_Text_GruntMVirbankComplexB2FSeenText::
	.string "POKéMON are pawns!"
	.string "\nThey're a means to"
	.string "\lan end."
	.string "\pThat's what I was"
	.string "\ntaught! Don't think"
	.string "\labout it too much.$"

Unova_VirbankComplexB2F_Text_GruntMVirbankComplexB2FBeatenText::
	.string "You little… You"
	.string "\nknocked out my"
	.string "\lstupid pawns!$"

Unova_VirbankComplexB2F_Text_GruntFVirbankComplexB2FSeenText::
	.string "Don't get in our"
	.string "\nway! You bother!"
	.string "\pBother, bother,"
	.string "\nbother!$"

Unova_VirbankComplexB2F_Text_GruntFVirbankComplexB2FBeatenText::
	.string "Arrgh! Lame!"
	.string "\nStupid! Fool!"
	.string "\lPlasmaaa!$"

Unova_VirbankComplexB2F_Text_ScientistMVirbankComplexB2FSeenText::
	.string "I used to work in"
	.string "\nthe COMPLEX, but"
	.string "\pnow I run research"
	.string "\nfor TEAM PLASMA!$"

Unova_VirbankComplexB2F_Text_ScientistMVirbankComplexB2FBeatenText::
	.string "Battling isn't"
	.string "\nexactly my strong"
	.string "\lsuit…$"

Unova_VirbankComplexB2F_Text_ScientistFVirbankComplexB2FSeenText::
	.string "Even if you win a"
	.string "\nbattle, you won't"
	.string "\pnecessarily get"
	.string "\nthe answer you're"
	.string "\llooking for."
	.string "\pYou might get"
	.string "\nsomething else,"
	.string "\lthough!$"

Unova_VirbankComplexB2F_Text_ScientistFVirbankComplexB2FBeatenText::
	.string "Grr… What even is"
	.string "\nthe point of a"
	.string "\lPOKéMON battle?$"
