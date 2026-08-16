@ IcirrusCitySouth do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ ----------------------------------------------------------------------------
@ B3 (Obra 2 de Unova, 15/08/2026): TROCA DE NIVEL, portada de
@ fontes-mapas/bw3g/maps/IcirrusCitySouth.asm.
@
@ Na fonte sao tres pedacos:
@   - callback MAPCALLBACK_TILES `.SetTiles`, que reaplica o estado ao carregar o mapa;
@   - `IcirrusCityUpperFloorScript`,
@     que sobe para a passarela;
@   - `IcirrusCityLowerFloorScript`,
@     que volta para o chao da cidade.
@
@ O estado mora em EVENT_ICIRRUS_CITY_UPPER_FLOOR
@ da fonte, que aqui e
@ FLAG_UNOVA_ICIRRUS_ANDAR_SUPERIOR
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
@ Linha marcada `igual ao map.bin` NAO pode ser apagada: e restauracao de estado.
@ Todo numero abaixo saiu de dev_scripts/changeblock_gen2.py; nenhum digitado.
@
@ DUAS flags neste mapa, e o `.SetTiles` da fonte confere as duas em ordem: antes
@ do andar ele testa EVENT_OPENED_TWIST_MOUNTAIN (aqui
@ FLAG_UNOVA_TWIST_MOUNTAIN_ABERTO) e abre a boca da caverna em (4,12). Quem
@ ACENDE essa flag e outra cena, fora deste mapa e fora deste bloco; aqui ela so
@ e LIDA.
@
@ MEDIDO, e diverge da fonte: o `warp_event` de (4,13) para
@ MAP_UNOVA_TWIST_MOUNTAIN_1F JA ESTA ABERTO no nosso map.bin (metatile 723,
@ colisao 0, comportamento MB_NON_ANIMATED_DOOR), efeito de
@ `blockdata_unova.forca_warps`, que poe porta embaixo dos 170 warps. Na fonte,
@ antes do evento, ali e desmoronamento. O `changeblock 4, 12, $1d` troca o
@ metatile de (4,13) de 723 para 555, e os dois SAO MB_NON_ANIMATED_DOOR: o warp
@ sobrevive a troca (por isso a ferramenta nao marca `muda warp` aqui), mas a
@ flag hoje muda so o DESENHO, nao o acesso. Fechar a boca antes do evento e
@ mexer no map.bin, nao neste script, e nao esta no escopo do B3.
@
@ O item ball de (22,2) fica DENTRO da area trocada, igual a fonte; nos dois
@ estados o quadrante dele sai andavel (metatile 515, MB_NORMAL), entao a bola
@ nao fica presa em nenhum dos dois.
@ ----------------------------------------------------------------------------

Unova_IcirrusCitySouth_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_IcirrusCitySouth_EventScript_AoCarregar
	.byte 0

Unova_IcirrusCitySouth_EventScript_AoCarregar::
	@ `.SetTiles` da fonte confere DUAS flags, em ordem: primeiro a boca
	@ de Twist Mountain, depois o andar.
	call_if_set FLAG_UNOVA_TWIST_MOUNTAIN_ABERTO, Unova_IcirrusCitySouth_EventScript_AbreTwistMountain
	call_if_set FLAG_UNOVA_ICIRRUS_ANDAR_SUPERIOR, Unova_IcirrusCitySouth_EventScript_Sobe
	end

@ `changeblock 4, 12, $1d` de `.SetTiles`: a boca de TWIST MOUNTAIN.
@ Quem ACENDE FLAG_UNOVA_TWIST_MOUNTAIN_ABERTO e outra cena (fora deste
@ mapa e fora deste bloco); aqui so se reaplica o desenho.
Unova_IcirrusCitySouth_EventScript_AbreTwistMountain::
	@ maps/IcirrusCitySouth.asm:27  changeblock  4, 12, $1d
	changeblock_gen2 4, 12, 552, 552, 555, 556, FALSE, FALSE, FALSE, TRUE   @ igual ao map.bin: CE, CD, BD
	return

@ `IcirrusCityUpperFloorScript` da fonte (a mesma lista do callback de tiles, conferida igual)
Unova_IcirrusCitySouth_EventScript_Sobe::
	@ maps/IcirrusCitySouth.asm:51  changeblock 16,  4, $4c
	changeblock_gen2 16, 4, 515, 611, 515, 612, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	@ maps/IcirrusCitySouth.asm:52  changeblock 18,  4, $4d
	changeblock_gen2 18, 4, 611, 611, 612, 612, FALSE, FALSE, FALSE, FALSE
	@ maps/IcirrusCitySouth.asm:53  changeblock 20,  4, $4d
	changeblock_gen2 20, 4, 611, 611, 612, 612, FALSE, FALSE, FALSE, FALSE
	@ maps/IcirrusCitySouth.asm:54  changeblock 22,  4, $4d
	changeblock_gen2 22, 4, 611, 611, 612, 612, FALSE, FALSE, FALSE, FALSE
	@ maps/IcirrusCitySouth.asm:55  changeblock 24,  4, $4d
	changeblock_gen2 24, 4, 611, 611, 612, 612, FALSE, FALSE, FALSE, FALSE
	@ maps/IcirrusCitySouth.asm:56  changeblock 26,  4, $4e
	changeblock_gen2 26, 4, 611, 515, 612, 515, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CD, BD
	@ maps/IcirrusCitySouth.asm:57  changeblock 18,  2, $a2
	changeblock_gen2 18, 2, 515, 515, 613, 613, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD
	@ maps/IcirrusCitySouth.asm:58  changeblock 20,  2, $a2
	changeblock_gen2 20, 2, 515, 515, 613, 613, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD
	@ maps/IcirrusCitySouth.asm:59  changeblock 22,  2, $a2
	changeblock_gen2 22, 2, 515, 515, 613, 613, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD
	@ maps/IcirrusCitySouth.asm:60  changeblock 24,  2, $a2
	changeblock_gen2 24, 2, 515, 515, 613, 613, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, CD
	@ maps/IcirrusCitySouth.asm:61  changeblock 30,  2, $5c
	changeblock_gen2 30, 2, 515, 624, 515, 625, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CE, BE
	@ maps/IcirrusCitySouth.asm:62  changeblock 32,  2, $5d
	changeblock_gen2 32, 2, 624, 624, 625, 625, FALSE, FALSE, FALSE, FALSE
	@ maps/IcirrusCitySouth.asm:63  changeblock 34,  2, $5d
	changeblock_gen2 34, 2, 624, 624, 625, 625, FALSE, FALSE, FALSE, FALSE
	@ maps/IcirrusCitySouth.asm:64  changeblock 36,  2, $5d
	changeblock_gen2 36, 2, 624, 624, 625, 625, FALSE, FALSE, FALSE, FALSE
	return

@ `IcirrusCityLowerFloorScript` da fonte: o caminho de VOLTA ao estado do map.bin
Unova_IcirrusCitySouth_EventScript_Desce::
	@ maps/IcirrusCitySouth.asm:74  changeblock 16,  4, $50
	changeblock_gen2 16, 4, 515, 614, 515, 615, FALSE, TRUE, FALSE, TRUE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:75  changeblock 18,  4, $51
	changeblock_gen2 18, 4, 616, 616, 617, 617, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:76  changeblock 20,  4, $51
	changeblock_gen2 20, 4, 616, 616, 617, 617, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:77  changeblock 22,  4, $51
	changeblock_gen2 22, 4, 616, 616, 617, 617, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:78  changeblock 24,  4, $51
	changeblock_gen2 24, 4, 616, 616, 617, 617, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:79  changeblock 26,  4, $52
	changeblock_gen2 26, 4, 614, 515, 615, 515, TRUE, FALSE, TRUE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:80  changeblock 18,  2, $49
	changeblock_gen2 18, 2, 515, 515, 608, 608, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:81  changeblock 20,  2, $49
	changeblock_gen2 20, 2, 515, 515, 608, 608, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:82  changeblock 22,  2, $49
	changeblock_gen2 22, 2, 515, 515, 608, 608, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:83  changeblock 24,  2, $49
	changeblock_gen2 24, 2, 515, 515, 608, 608, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:84  changeblock 30,  2, $60
	changeblock_gen2 30, 2, 515, 634, 515, 635, FALSE, TRUE, FALSE, TRUE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:85  changeblock 32,  2, $61
	changeblock_gen2 32, 2, 636, 636, 637, 637, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:86  changeblock 34,  2, $61
	changeblock_gen2 34, 2, 636, 636, 637, 637, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	@ maps/IcirrusCitySouth.asm:87  changeblock 36,  2, $62
	changeblock_gen2 36, 2, 636, 634, 637, 635, FALSE, TRUE, FALSE, TRUE   @ igual ao map.bin: os 4
	return

@ coord_events da fonte: (9,5) (10,5) (29,5) (30,5) (12,4) (13,5) (14,4)
Unova_IcirrusCitySouth_EventScript_GatilhoSobe::
	lock
	goto_if_set FLAG_UNOVA_ICIRRUS_ANDAR_SUPERIOR, Unova_IcirrusCitySouth_EventScript_GatilhoFim
	setflag FLAG_UNOVA_ICIRRUS_ANDAR_SUPERIOR
	call Unova_IcirrusCitySouth_EventScript_Sobe
	special DrawWholeMapView
	release
	end

@ coord_events da fonte: (32,0) (33,0) (34,0) (35,0) (29,8) (30,8) (9,10)
@   (10,10) (4,14)
Unova_IcirrusCitySouth_EventScript_GatilhoDesce::
	lock
	goto_if_unset FLAG_UNOVA_ICIRRUS_ANDAR_SUPERIOR, Unova_IcirrusCitySouth_EventScript_GatilhoFim
	clearflag FLAG_UNOVA_ICIRRUS_ANDAR_SUPERIOR
	call Unova_IcirrusCitySouth_EventScript_Desce
	special DrawWholeMapView
	release
	end

Unova_IcirrusCitySouth_EventScript_GatilhoFim::
	release
	end

Unova_IcirrusCitySouth_EventScript_Placa0::
	msgbox Unova_IcirrusCitySouth_Text_IcirrusCitySignText, MSGBOX_SIGN
	end

Unova_IcirrusCitySouth_EventScript_Npc3::
	msgbox Unova_IcirrusCitySouth_Text_IcirrusCitySouthBuenaText, MSGBOX_NPC
	end

Unova_IcirrusCitySouth_EventScript_Npc4::
	msgbox Unova_IcirrusCitySouth_Text_IcirrusCitySouthFisherText, MSGBOX_NPC
	end

@ `IcirrusCitySouthPokefanMScript` da fonte (decisao 69): o POKEFAN_M tem DOIS
@ textos, e o que escolhe entre eles e a mesma flag do changeblock da boca da
@ caverna. So o texto de ANTES tinha sido importado; o de depois entrou no B3.
Unova_IcirrusCitySouth_EventScript_Npc5::
	goto_if_set FLAG_UNOVA_TWIST_MOUNTAIN_ABERTO, Unova_IcirrusCitySouth_EventScript_Npc5Aberto
	msgbox Unova_IcirrusCitySouth_Text_IcirrusCitySouthPokefanMText, MSGBOX_NPC
	end

Unova_IcirrusCitySouth_EventScript_Npc5Aberto::
	msgbox Unova_IcirrusCitySouth_Text_IcirrusCitySouthPokefanMOpenedText, MSGBOX_NPC
	end


Unova_IcirrusCitySouth_Text_IcirrusCitySignText::
	.string "ICIRRUS CITY"
	.string "\pSky glittering"
	.string "\nwith flowers of"
	.string "\lsnow.$"

Unova_IcirrusCitySouth_Text_IcirrusCitySouthBuenaText::
	.string "If you walk in the"
	.string "\nwetlands, you"
	.string "\pmight surprise"
	.string "\nwild POKéMON into"
	.string "\lpopping out!$"

Unova_IcirrusCitySouth_Text_IcirrusCitySouthFisherText::
	.string "Two legendary"
	.string "\ndragons, awoken at"
	.string "\lthe tower…"
	.string "\pThe stories I"
	.string "\nheard when I was"
	.string "\plittle turned out"
	.string "\nto be true!$"

Unova_IcirrusCitySouth_Text_IcirrusCitySouthPokefanMText::
	.string "There used to be a"
	.string "\ncave here that led"
	.string "\lto TWIST MOUNTAIN."
	.string "\pBut all the"
	.string "\nconstruction"
	.string "\pcaused the"
	.string "\nentrance to"
	.string "\lcollapse…"
	.string "\pThe crews can"
	.string "\nstill get in and"
	.string "\pout through the"
	.string "\nother side, but it"
	.string "\pis a real"
	.string "\ninconvenience for"
	.string "\lus…$"

@ `IcirrusCitySouthPokefanMOpenedText` da fonte, linha 169 de
@ fontes-mapas/bw3g/maps/IcirrusCitySouth.asm. Mesma conversao do resto do
@ arquivo: text/line/para/cont -> .string com "\n", "\p", "\l", e "#" -> "POKé".
Unova_IcirrusCitySouth_Text_IcirrusCitySouthPokefanMOpenedText::
	.string "You're never going"
	.string "\nto believe this!"
	.string "\pA strange looking"
	.string "\nmechanical thing"
	.string "\pcame flying by"
	.string "\nhere and knocked"
	.string "\popen the entrance"
	.string "\nto the mountain!"
	.string "\pI wonder if it was"
	.string "\nsome kind of POKé-"
	.string "\lMON…"
	.string "\pIt's not any I've"
	.string "\never seen before…$"
