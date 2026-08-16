@ DragonspiralTower2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@
@ B4 da Obra 2 (changeblock), 15/08/2026. Linhas de metatile geradas por
@ dev_scripts/changeblock_gen2.py (trechos de maps/DragonspiralTower2F.asm);
@ nenhum id de metatile foi digitado à mão.
@
@ Mecanismo da fonte: o mapa tem DOIS andares desenhados no mesmo layout. A
@ fileira y=4 é a passarela; os coord_events do topo (6,10 / 5,11 / 15,10)
@ ligam o andar de cima e os de baixo (6,12 / 7,11 / 7,12 / 14,10 / 15,11)
@ devolvem o de baixo. Estado em FLAG_UNOVA_DRAGONSPIRAL_2F_ANDAR_SUPERIOR.
@ O `.SetTiles` da fonte (MAPCALLBACK_TILES) vira MAP_SCRIPT_ON_LOAD, decisão 4
@ da condutora: em ON_TRANSITION o InitMapLayoutData apagaria tudo.
@ Estado estático do map.bin = andar de baixo (as 7 linhas de DesceAndar saem
@ marcadas `igual ao map.bin: os 4`), por isso a volta só é escrita, nunca
@ apagada: sem ela o mapa não volta ao inicial.
@
@ Sobre a armadilha da elevação (a que pegou VictoryRoadCave1F e os mapas de
@ água do B3): aqui ela NÃO existe. 14 quadrantes trocam de elevação entre os
@ dois andares (parede 0 <-> chão 3) e ficam com `setmetatile`, que preserva a
@ elevação, de propósito: o map.bin deste mapa só tem elevação 0 e 3 (medido:
@ 190 e 162 células, ZERO de água), e elevação 0 casa com qualquer outra em
@ IsElevationMismatchAt. Sem um segundo nível para vazar, andar sobre um tile
@ que ficou em 0 é igual a andar sobre um em 3. Não trocar por
@ `setmetatileinrange` sem antes achar água neste mapa.
@
@ PEDRA (aprovado em 15/08/2026, ver dev_scripts/pedra_buraco_unova.py): o
@ buraco de (6,11) deixou de ser `MB_NON_ANIMATED_DOOR` e virou
@ `MB_MT_PYRE_HOLE`, o comportamento que o motor entende dos DOIS lados: o
@ jogador que pisa CAI (usa o mesmo warp_event que já estava lá) e a pedra que
@ para em cima some por `HandleBoulderFallThroughHole`, que agora também roda o
@ coord_event daquela casa (`RunCoordEventScriptAt`, acrescentado espelhando a
@ função irmã do FRLG). O censo provou que o metatile de porta forçada destes
@ tilesets só existe nas casas de buraco, então mudar o atributo não vaza, e
@ `map.bin` não mudou nem um byte. A pedra fica sumida depois pelo campo `flag`
@ do object_event, que é a MESMA flag da persistência: zero flag nova.

Unova_DragonspiralTower2F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_DragonspiralTower2F_EventScript_AoCarregar
	.byte 0

@ `.SetTiles` da fonte, linhas 19-33.
Unova_DragonspiralTower2F_EventScript_AoCarregar::
	goto_if_unset FLAG_UNOVA_DRAGONSPIRAL_2F_ANDAR_SUPERIOR, Unova_DragonspiralTower2F_EventScript_AoCarregarPedra
	call Unova_DragonspiralTower2F_EventScript_SobeAndar
Unova_DragonspiralTower2F_EventScript_AoCarregarPedra::
	goto_if_unset FLAG_UNOVA_DRAGONSPIRAL_2F_PEDRA, Unova_DragonspiralTower2F_EventScript_AoCarregarFim
	call Unova_DragonspiralTower2F_EventScript_PedraNoBuraco
Unova_DragonspiralTower2F_EventScript_AoCarregarFim::
	end

@ `DragonspiralTower2FUpperLevelScript` da fonte: coord_events (6,10), (5,11) e (15,10).
Unova_DragonspiralTower2F_EventScript_GatilhoSobe::
	goto_if_set FLAG_UNOVA_DRAGONSPIRAL_2F_ANDAR_SUPERIOR, Unova_DragonspiralTower2F_EventScript_GatilhoFim
	call Unova_DragonspiralTower2F_EventScript_SobeAndar
	setflag FLAG_UNOVA_DRAGONSPIRAL_2F_ANDAR_SUPERIOR
	special DrawWholeMapView
Unova_DragonspiralTower2F_EventScript_GatilhoFim::
	end

@ `DragonspiralTower2FLowerLevelScript` da fonte: coord_events (6,12), (7,11), (7,12), (14,10) e (15,11).
Unova_DragonspiralTower2F_EventScript_GatilhoDesce::
	goto_if_unset FLAG_UNOVA_DRAGONSPIRAL_2F_ANDAR_SUPERIOR, Unova_DragonspiralTower2F_EventScript_GatilhoFim
	call Unova_DragonspiralTower2F_EventScript_DesceAndar
	clearflag FLAG_UNOVA_DRAGONSPIRAL_2F_ANDAR_SUPERIOR
	special DrawWholeMapView
	end

@ maps/DragonspiralTower2F.asm:21-27 (e 63-69, as mesmas 7 chamadas)
Unova_DragonspiralTower2F_EventScript_SobeAndar::
	changeblock_gen2 2, 4, 515, 682, 517, 684, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	changeblock_gen2 4, 4, 686, 686, 688, 688, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 6, 4, 690, 682, 692, 684, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 8, 4, 686, 686, 688, 688, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 10, 4, 690, 682, 692, 684, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 12, 4, 686, 686, 688, 688, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 14, 4, 690, 694, 692, 696, FALSE, FALSE, FALSE, FALSE
	return

@ maps/DragonspiralTower2F.asm:77-83. As 7 linhas são a restauração do estado
@ inicial: todas `igual ao map.bin`, e por isso mesmo NENHUMA pode ser apagada.
Unova_DragonspiralTower2F_EventScript_DesceAndar::
	changeblock_gen2 2, 4, 515, 666, 517, 668, FALSE, TRUE, FALSE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 4, 4, 670, 670, 672, 672, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 6, 4, 665, 666, 667, 668, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 8, 4, 670, 670, 672, 672, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 10, 4, 665, 666, 667, 668, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 4, 670, 670, 672, 672, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 14, 4, 665, 544, 667, 546, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	return

@ maps/DragonspiralTower2F.asm:31 (e 50, dentro do `.Boulder` do stonetable)
@ ATENCAO: muda warp em (6,11): MB_NON_ANIMATED_DOOR -> MB_CAVE, conferir warp_events
@ Conferido: o warp_event 4 do map.json é (6,11) -> MAP_UNOVA_DRAGONSPIRAL_TOWER_2F
@ warp 0, ou seja o próprio buraco que devolve o jogador à escada de (8,21). É
@ ele mesmo que a pedra tapa; matar o warp é o efeito querido, não acidente.
Unova_DragonspiralTower2F_EventScript_PedraNoBuraco::
	changeblock_gen2 6, 10, 515, 533, 541, 515, FALSE, TRUE, FALSE, FALSE   @ igual ao map.bin: CE, CD, BD
	return

@ `.Boulder` do stonetable da fonte (maps/DragonspiralTower2F.asm:44-53).
@ Gatilho: coord_event de (6,11), a casa do buraco, com var_value que NUNCA casa
@ (VAR_TEMP_0 nasce 0 a cada mapa), pelo idioma do VictoryRoad_1F_Frlg: assim o
@ jogador que pisa no buraco NÃO roda isto (ele cai, MB_MT_PYRE_HOLE), e quem
@ roda é só a pedra que parou ali, via HandleBoulderFallThroughHole. O motor já
@ tocou SE_FALL e tirou a pedra do mapa antes desta linha; o `flag` do
@ object_event é que a mantém sumida depois.
Unova_DragonspiralTower2F_EventScript_PedraCai::
	lockall
	msgbox Unova_DragonspiralTower2F_Text_PedraCaiu, MSGBOX_DEFAULT
	setflag FLAG_UNOVA_DRAGONSPIRAL_2F_PEDRA
	call Unova_DragonspiralTower2F_EventScript_PedraNoBuraco
	special DrawWholeMapView
	releaseall
	end

Unova_DragonspiralTower2F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_GIALLO2, Unova_DragonspiralTower2F_Text_DragonspiralTowerGialloSeenText, Unova_DragonspiralTower2F_Text_DragonspiralTowerGialloBeatenText
	end


@ `DragonspiralBoulderFellText` da fonte.
Unova_DragonspiralTower2F_Text_PedraCaiu::
	.string "The boulder fell\n"
	.string "through!$"

Unova_DragonspiralTower2F_Text_DragonspiralTowerGialloSeenText::
	.string "So, you've come."
	.string "\nWe, the SAGEs of"
	.string "\pTEAM PLASMA shall"
	.string "\ndefeat you here!$"

Unova_DragonspiralTower2F_Text_DragonspiralTowerGialloBeatenText::
	.string "Y-you!$"
