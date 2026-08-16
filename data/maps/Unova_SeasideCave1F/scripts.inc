@ SeasideCave1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ ----------------------------------------------------------------------------
@ B3 (Obra 2 de Unova, 15/08/2026): TROCA DE NIVEL, portada de
@ fontes-mapas/bw3g/maps/SeasideCave1F.asm.
@
@ Na fonte sao tres pedacos:
@   - callback MAPCALLBACK_TILES `.SetTiles`, que reaplica o estado ao carregar o mapa;
@   - `SeasideCaveLowerFloorScript`,
@     que passa por baixo da ponte;
@   - `SeasideCaveUpperFloorScript`,
@     que volta para cima da ponte.
@
@ O estado mora em EVENT_SEASIDE_CAVE_LOWER_FLOOR
@ da fonte, que aqui e
@ FLAG_UNOVA_SEASIDE_CAVE_ANDAR_INFERIOR
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
@ Gatilho: os 6 `coord_event` da fonte, coordenada IDENTIDADE (a geometria de
@ gen 2 entra 1:1 em Unova, cabecalho de dev_scripts/fila_b6.py). Todos caem em
@ tile andavel do map.bin, conferido um a um.
@
@ Linha marcada `igual ao map.bin` NAO pode ser apagada: e restauracao de estado.
@ Todo numero abaixo saiu de dev_scripts/changeblock_gen2.py; nenhum digitado.
@
@ Ambiente CAVE: o chao vem de `masmorra2mt`, nao de `quad2mt` (a mesma regra do
@ `converte_arte`), entao os metatiles daqui sorteiam encontro como o resto da
@ caverna.
@ ----------------------------------------------------------------------------

Unova_SeasideCave1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_SeasideCave1F_EventScript_AoCarregar
	.byte 0

Unova_SeasideCave1F_EventScript_AoCarregar::
	call_if_set FLAG_UNOVA_SEASIDE_CAVE_ANDAR_INFERIOR, Unova_SeasideCave1F_EventScript_Desce
	end

@ `SeasideCaveLowerFloorScript` da fonte (a mesma lista do callback de tiles, conferida igual)
Unova_SeasideCave1F_EventScript_Desce::
	@ maps/SeasideCave1F.asm:35  changeblock  8, 24, $5C ; left wall bridge
	changeblock_gen2 8, 24, 572, 573, 574, 575, TRUE, FALSE, TRUE, FALSE
	@ maps/SeasideCave1F.asm:36  changeblock 10, 24, $5E ; under bridge
	changeblock_gen2 10, 24, 573, 573, 575, 575, FALSE, FALSE, FALSE, FALSE
	@ maps/SeasideCave1F.asm:37  changeblock 12, 24, $5D ; right wall bridge
	changeblock_gen2 12, 24, 573, 572, 575, 574, FALSE, TRUE, FALSE, TRUE
	return

@ `SeasideCaveUpperFloorScript` da fonte: o caminho de VOLTA ao estado do map.bin
Unova_SeasideCave1F_EventScript_Sobe::
	@ maps/SeasideCave1F.asm:45  changeblock  8, 24, $5F ; over bridge
	changeblock_gen2 8, 24, 576, 576, 577, 577, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/SeasideCave1F.asm:46  changeblock 10, 24, $5F ; over bridge
	changeblock_gen2 10, 24, 576, 576, 577, 577, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/SeasideCave1F.asm:47  changeblock 12, 24, $5F ; over bridge
	changeblock_gen2 12, 24, 576, 576, 577, 577, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	return

@ coord_events da fonte: (11,3) (8,19)
Unova_SeasideCave1F_EventScript_GatilhoDesce::
	lock
	goto_if_set FLAG_UNOVA_SEASIDE_CAVE_ANDAR_INFERIOR, Unova_SeasideCave1F_EventScript_GatilhoFim
	setflag FLAG_UNOVA_SEASIDE_CAVE_ANDAR_INFERIOR
	call Unova_SeasideCave1F_EventScript_Desce
	special DrawWholeMapView
	release
	end

@ coord_events da fonte: (5,6) (5,33) (8,17) (9,2)
Unova_SeasideCave1F_EventScript_GatilhoSobe::
	lock
	goto_if_unset FLAG_UNOVA_SEASIDE_CAVE_ANDAR_INFERIOR, Unova_SeasideCave1F_EventScript_GatilhoFim
	clearflag FLAG_UNOVA_SEASIDE_CAVE_ANDAR_INFERIOR
	call Unova_SeasideCave1F_EventScript_Sobe
	special DrawWholeMapView
	release
	end

Unova_SeasideCave1F_EventScript_GatilhoFim::
	release
	end

Unova_SeasideCave1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_DOCTOR_SEASIDE_CAVE, Unova_SeasideCave1F_Text_SeasideCaveDoctorIntroText, Unova_SeasideCave1F_Text_SeasideCaveDoctorWinText
	end

Unova_SeasideCave1F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_VETERANF_SEASIDE_CAVE, Unova_SeasideCave1F_Text_VeteranFSeasideCave1FSeenText, Unova_SeasideCave1F_Text_VeteranFSeasideCave1FBeatenText
	end

Unova_SeasideCave1F_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_SEASIDE_CAVE_1, Unova_SeasideCave1F_Text_BlackbeltSeasideCave1FSeenText, Unova_SeasideCave1F_Text_BlackbeltSeasideCave1FBeatenText
	end

Unova_SeasideCave1F_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_SEASIDE_CAVE_1, Unova_SeasideCave1F_Text_BattleGirlSeasideCave1FSeenText, Unova_SeasideCave1F_Text_BattleGirlSeasideCave1FBeatenText
	end


Unova_SeasideCave1F_Text_SeasideCaveDoctorIntroText::
	.string "I'm a doctor, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_SeasideCave1F_Text_SeasideCaveDoctorWinText::
	.string "Ah, I see.$"

Unova_SeasideCave1F_Text_VeteranFSeasideCave1FSeenText::
	.string "Let me show you"
	.string "\nthe POKéMON that I"
	.string "\lmet by fate!$"

Unova_SeasideCave1F_Text_VeteranFSeasideCave1FBeatenText::
	.string "The POKéMON that"
	.string "\nyou've met are"
	.string "\pquite formidable,"
	.string "\naren't they?$"

Unova_SeasideCave1F_Text_BlackbeltSeasideCave1FSeenText::
	.string "The path of karate"
	.string "\nis the path of"
	.string "\phumanity… and the"
	.string "\npath of POKéMON!$"

Unova_SeasideCave1F_Text_BlackbeltSeasideCave1FBeatenText::
	.string "Oof! It is not by"
	.string "\nchance that you"
	.string "\lhave won!$"

Unova_SeasideCave1F_Text_BattleGirlSeasideCave1FSeenText::
	.string "Greetings! So…"
	.string "\nshall we do this?$"

Unova_SeasideCave1F_Text_BattleGirlSeasideCave1FBeatenText::
	.string "What an upset!$"
