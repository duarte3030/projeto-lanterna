@ Rt18 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ ----------------------------------------------------------------------------
@ B3 (Obra 2 de Unova, 15/08/2026): TROCA DE NIVEL, portada de
@ fontes-mapas/bw3g/maps/Rt18.asm.
@
@ Na fonte sao tres pedacos:
@   - callback MAPCALLBACK_TILES `.Tiles`, que reaplica o estado ao carregar o mapa;
@   - `R18LowerScript`,
@     que passa por baixo da ponte;
@   - `R18UpperScript`,
@     que volta para cima da ponte.
@
@ O estado mora em EVENT_R_18_LOWER
@ da fonte, que aqui e
@ FLAG_UNOVA_R18_ANDAR_INFERIOR
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
@ Gatilho: os 8 `coord_event` da fonte, coordenada IDENTIDADE (a geometria de
@ gen 2 entra 1:1 em Unova, cabecalho de dev_scripts/fila_b6.py). Todos caem em
@ tile andavel do map.bin, conferido um a um.
@
@ Linha marcada `igual ao map.bin` NAO pode ser apagada: e restauracao de estado.
@ Todo numero abaixo saiu de dev_scripts/changeblock_gen2.py; nenhum digitado.
@ ----------------------------------------------------------------------------

Unova_Rt18_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_Rt18_EventScript_AoCarregar
	.byte 0

Unova_Rt18_EventScript_AoCarregar::
	call_if_set FLAG_UNOVA_R18_ANDAR_INFERIOR, Unova_Rt18_EventScript_Desce
	end

@ `R18LowerScript` da fonte (a mesma lista do callback de tiles, conferida igual)
Unova_Rt18_EventScript_Desce::
	@ maps/Rt18.asm:36  changeblock 16, 22, $ce ; bridge top
	changeblock_gen2 16, 22, 515, 515, 744, 745, FALSE, FALSE, TRUE, TRUE   @ igual ao map.bin: CE, CD
	@ maps/Rt18.asm:37  changeblock 16, 24, $cf ; bridge main
	changeblock_gen2 16, 24, 746, 747, 748, 749, FALSE, FALSE, FALSE, FALSE
	@ maps/Rt18.asm:38  changeblock 16, 26, $d0 ; up_wall
	changeblock_gen2 16, 26, 515, 515, 515, 515, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return

@ `R18UpperScript` da fonte: o caminho de VOLTA ao estado do map.bin
Unova_Rt18_EventScript_Sobe::
	@ maps/Rt18.asm:46  changeblock 16, 22, $cc ; bridge top
	changeblock_gen2 16, 22, 515, 515, 655, 659, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt18.asm:47  changeblock 16, 24, $cd ; bridge main
	changeblock_gen2 16, 24, 655, 659, 657, 660, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/Rt18.asm:48  changeblock 16, 26, $02 ; up_wall
	changeblock_gen2 16, 26, 515, 515, 515, 515, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return

@ coord_events da fonte: (6,24) (6,25)
Unova_Rt18_EventScript_GatilhoDesce::
	lock
	goto_if_set FLAG_UNOVA_R18_ANDAR_INFERIOR, Unova_Rt18_EventScript_GatilhoFim
	setflag FLAG_UNOVA_R18_ANDAR_INFERIOR
	call Unova_Rt18_EventScript_Desce
	special DrawWholeMapView
	release
	end

@ coord_events da fonte: (5,24) (5,25) (25,16) (25,17) (4,20) (5,20)
Unova_Rt18_EventScript_GatilhoSobe::
	lock
	goto_if_unset FLAG_UNOVA_R18_ANDAR_INFERIOR, Unova_Rt18_EventScript_GatilhoFim
	clearflag FLAG_UNOVA_R18_ANDAR_INFERIOR
	call Unova_Rt18_EventScript_Sobe
	special DrawWholeMapView
	release
	end

Unova_Rt18_EventScript_GatilhoFim::
	release
	end

Unova_Rt18_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_HIKER_R18, Unova_Rt18_Text_HikerR18SeenText, Unova_Rt18_Text_HikerR18BeatenText
	end

Unova_Rt18_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_R18, Unova_Rt18_Text_BlackbeltR18SeenText, Unova_Rt18_Text_BlackbeltR18BeatenText
	end

Unova_Rt18_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_R18, Unova_Rt18_Text_BattleGirlR18SeenText, Unova_Rt18_Text_BattleGirlR18BeatenText
	end

Unova_Rt18_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_R18, Unova_Rt18_Text_BackpackerMR18SeenText, Unova_Rt18_Text_BackpackerMR18BeatenText
	end

Unova_Rt18_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_R18, Unova_Rt18_Text_BackpackerFR18SeenText, Unova_Rt18_Text_BackpackerFR18BeatenText
	end


Unova_Rt18_Text_HikerR18SeenText::
	.string "When I look down"
	.string "\nfrom a high place,"
	.string "\lI feel very good!"
	.string "\pPOKéMON battles"
	.string "\nare the same!$"

Unova_Rt18_Text_HikerR18BeatenText::
	.string "You're great! I"
	.string "\ncan't help but look"
	.string "\lup to you!$"

Unova_Rt18_Text_BlackbeltR18SeenText::
	.string "I just won a"
	.string "\nbattle back there,"
	.string "\pso I'm feeling"
	.string "\ngood!$"

Unova_Rt18_Text_BlackbeltR18BeatenText::
	.string "Oh whatever! I'm"
	.string "\nin a terrible mood"
	.string "\lnow!$"

Unova_Rt18_Text_BattleGirlR18SeenText::
	.string "Number! Eight!"
	.string "\nTeen!$"

Unova_Rt18_Text_BattleGirlR18BeatenText::
	.string "OK! Thank you very"
	.string "\nmuch!$"

Unova_Rt18_Text_BackpackerMR18SeenText::
	.string "BACKPACKERs are"
	.string "\nexactly what they"
	.string "\lsound like."
	.string "\pThey set out on"
	.string "\nthe road with only"
	.string "\pthe packs on their"
	.string "\nbacks and the"
	.string "\pPOKéMON in their"
	.string "\nPOKéBALLs!$"

Unova_Rt18_Text_BackpackerMR18BeatenText::
	.string "I wish I could"
	.string "\npack some wins in"
	.string "\lmy backpack too…$"

Unova_Rt18_Text_BackpackerFR18SeenText::
	.string "Your POKéMON and"
	.string "\nyour strategy!"
	.string "\pI'll be taking"
	.string "\nnotes on both!$"

Unova_Rt18_Text_BackpackerFR18BeatenText::
	.string "There's still so"
	.string "\nmuch more to"
	.string "\llearn!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 2). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_Rt18_EventScript_Gruta4BE::
	goto_if_set FLAG_UNOVA_GRUTA_R18, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R18
	goto Unova_EventScript_GrutaTier2
