@ Dreamyard do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@
@ B4 da Obra 2 (changeblock), 15/08/2026. Linhas de metatile geradas por
@ dev_scripts/changeblock_gen2.py (trechos de maps/Dreamyard.asm); nenhum id de
@ metatile foi digitado à mão.
@
@ Mecanismo da fonte: a rampa da coluna x=12 e a mureta de y=0 têm duas caras,
@ andar de cima e andar de baixo. O coord_event de (23,6) sobe e os de (22,6),
@ (23,7) e (24,6) descem. Estado em FLAG_UNOVA_DREAMYARD_ANDAR_SUPERIOR.
@ O `.SetTiles` da fonte APAGA o estado do andar em toda carga de mapa, com o
@ comentário dela mesma: nenhuma batalha ou warp devolve o jogador ao andar de
@ cima, então entrar no mapa sempre começa embaixo. Copiado igual: o clearflag
@ abaixo é da fonte, não invenção, e é o que dispensa reescrever as 9 linhas do
@ andar de baixo no ON_LOAD (o estado estático do map.bin já é esse: as 9 saem
@ marcadas `igual ao map.bin: os 4`).
@
@ Sobre a armadilha da elevação (a que pegou VictoryRoadCave1F e os mapas de
@ água do B3): aqui ela NÃO existe. 28 quadrantes trocam de elevação entre os
@ dois andares (parede 0 <-> chão 3) e ficam com `setmetatile`, que preserva a
@ elevação, de propósito: o map.bin deste mapa só tem elevação 0 e 3 (medido:
@ 1057 e 463 células, ZERO de água), e elevação 0 casa com qualquer outra em
@ IsElevationMismatchAt. Sem um segundo nível para vazar, andar sobre um tile
@ que ficou em 0 é igual a andar sobre um em 3. Não trocar por
@ `setmetatileinrange` sem antes achar água neste mapa.
@
@ PEDRA (aprovado em 15/08/2026, ver dev_scripts/pedra_buraco_unova.py): o
@ buraco de (10,21) deixou de ser `MB_NON_ANIMATED_DOOR` e virou
@ `MB_MT_PYRE_HOLE`, o comportamento que o motor entende dos DOIS lados: o
@ jogador que pisa CAI (usa o mesmo warp_event que já estava lá) e a pedra que
@ para em cima some por `HandleBoulderFallThroughHole`, que agora também roda o
@ coord_event daquela casa (`RunCoordEventScriptAt`, acrescentado espelhando a
@ função irmã do FRLG). O censo provou que o metatile de porta forçada destes
@ tilesets só existe nas casas de buraco, então mudar o atributo não vaza, e
@ `map.bin` não mudou nem um byte. A pedra fica sumida depois pelo campo `flag`
@ do object_event, que é a MESMA flag da persistência: zero flag nova.

Unova_Dreamyard_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_Dreamyard_EventScript_AoCarregar
	.byte 0

@ `.SetTiles` da fonte, linhas 19-27.
Unova_Dreamyard_EventScript_AoCarregar::
	clearflag FLAG_UNOVA_DREAMYARD_ANDAR_SUPERIOR
	goto_if_unset FLAG_UNOVA_DREAMYARD_PEDRA, Unova_Dreamyard_EventScript_AoCarregarFim
	call Unova_Dreamyard_EventScript_PedraNoBuraco
Unova_Dreamyard_EventScript_AoCarregarFim::
	end

@ `DreamyardUpperLevelScript` da fonte: coord_event (23,6).
Unova_Dreamyard_EventScript_GatilhoSobe::
	goto_if_set FLAG_UNOVA_DREAMYARD_ANDAR_SUPERIOR, Unova_Dreamyard_EventScript_GatilhoFim
	call Unova_Dreamyard_EventScript_SobeAndar
	setflag FLAG_UNOVA_DREAMYARD_ANDAR_SUPERIOR
	special DrawWholeMapView
Unova_Dreamyard_EventScript_GatilhoFim::
	end

@ `DreamyardLowerLevelScript` da fonte: coord_events (22,6), (23,7) e (24,6).
Unova_Dreamyard_EventScript_GatilhoDesce::
	goto_if_unset FLAG_UNOVA_DREAMYARD_ANDAR_SUPERIOR, Unova_Dreamyard_EventScript_GatilhoFim
	call Unova_Dreamyard_EventScript_DesceAndar
	clearflag FLAG_UNOVA_DREAMYARD_ANDAR_SUPERIOR
	special DrawWholeMapView
	end

@ maps/Dreamyard.asm:57-65
Unova_Dreamyard_EventScript_SobeAndar::
	changeblock_gen2 10, 0, 635, 627, 627, 627, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 14, 0, 627, 627, 627, 627, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 16, 0, 635, 627, 627, 627, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 18, 0, 635, 627, 627, 627, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 20, 0, 635, 627, 627, 627, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 12, 2, 627, 628, 628, 626, FALSE, FALSE, FALSE, TRUE   @ igual ao map.bin: BD
	changeblock_gen2 12, 4, 628, 633, 627, 628, FALSE, TRUE, FALSE, FALSE
	changeblock_gen2 12, 6, 635, 628, 627, 628, FALSE, FALSE, FALSE, FALSE
	changeblock_gen2 12, 8, 635, 628, 627, 628, FALSE, FALSE, FALSE, FALSE
	return

@ maps/Dreamyard.asm:73-81. Restauração do estado inicial: as 9 são
@ `igual ao map.bin`, e por isso mesmo NENHUMA pode ser apagada.
Unova_Dreamyard_EventScript_DesceAndar::
	changeblock_gen2 10, 0, 629, 623, 630, 630, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 14, 0, 623, 623, 630, 630, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 16, 0, 629, 623, 630, 630, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 18, 0, 629, 623, 630, 630, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 20, 0, 629, 623, 630, 630, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 2, 623, 624, 625, 626, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 4, 631, 532, 632, 631, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 6, 634, 631, 632, 631, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: os 4
	changeblock_gen2 12, 8, 623, 624, 629, 624, TRUE, TRUE, TRUE, TRUE   @ igual ao map.bin: os 4
	return

@ maps/Dreamyard.asm:25 (e 44, dentro do `.Boulder` do stonetable)
@ ATENCAO: muda warp em (10,21): MB_NON_ANIMATED_DOOR -> MB_NORMAL, conferir warp_events
@ Conferido: o warp_event 2 do map.json é (10,21) -> MAP_UNOVA_DREAMYARD warp 0,
@ isto é (1,16), a boca do mapa. É o próprio buraco em que a pedra cai; matar o
@ warp é o efeito querido da cena, não acidente.
Unova_Dreamyard_EventScript_PedraNoBuraco::
	changeblock_gen2 10, 20, 515, 515, 561, 560, FALSE, FALSE, FALSE, TRUE   @ igual ao map.bin: CE, CD, BD
	return

@ `.Boulder` do stonetable da fonte (maps/Dreamyard.asm:37-46). Gatilho:
@ coord_event de (10,21), a casa do buraco, com var_value que NUNCA casa
@ (VAR_TEMP_0 nasce 0 a cada mapa), pelo idioma do VictoryRoad_1F_Frlg: o
@ jogador que pisa ali CAI (MB_MT_PYRE_HOLE) e não roda isto; quem roda é só a
@ pedra que parou em cima, via HandleBoulderFallThroughHole. O motor já tocou
@ SE_FALL e tirou a pedra; o `flag` do object_event a mantém sumida depois.
Unova_Dreamyard_EventScript_PedraCai::
	lockall
	msgbox Unova_Dreamyard_Text_PedraCaiu, MSGBOX_DEFAULT
	setflag FLAG_UNOVA_DREAMYARD_PEDRA
	call Unova_Dreamyard_EventScript_PedraNoBuraco
	special DrawWholeMapView
	releaseall
	end

Unova_Dreamyard_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_DREAMYARD, Unova_Dreamyard_Text_YoungsterDreamyardSeenText, Unova_Dreamyard_Text_YoungsterDreamyardBeatenText
	end

Unova_Dreamyard_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_DREAMYARD, Unova_Dreamyard_Text_SchoolKidMDreamyardSeenText, Unova_Dreamyard_Text_SchoolKidMDreamyardBeatenText
	end

Unova_Dreamyard_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_DREAMYARD, Unova_Dreamyard_Text_SchoolKidFDreamyardSeenText, Unova_Dreamyard_Text_SchoolKidFDreamyardBeatenText
	end


@ `DreamyardBoulderFellText` da fonte.
Unova_Dreamyard_Text_PedraCaiu::
	.string "The boulder fell\n"
	.string "through!$"

Unova_Dreamyard_Text_YoungsterDreamyardSeenText::
	.string "Shorts and POKé-"
	.string "\nMON! This is the"
	.string "\pultimate"
	.string "\ncombination!$"

Unova_Dreamyard_Text_YoungsterDreamyardBeatenText::
	.string "It's not my POKé-"
	.string "\nMON's fault! It's"
	.string "\pnot my shorts'"
	.string "\nfault either!$"

Unova_Dreamyard_Text_SchoolKidMDreamyardSeenText::
	.string "My POKéMON's"
	.string "\nstrong points!"
	.string "\pYou'll see them if"
	.string "\nyou fight!$"

Unova_Dreamyard_Text_SchoolKidMDreamyardBeatenText::
	.string "Hey! Did you see"
	.string "\nmy POKéMON's strong"
	.string "\lpoints?$"

Unova_Dreamyard_Text_SchoolKidFDreamyardSeenText::
	.string "See my extra-"
	.string "\nordinarily pretty"
	.string "\lPOKéMON!$"

Unova_Dreamyard_Text_SchoolKidFDreamyardBeatenText::
	.string "Ah! Its beauty has"
	.string "\nbeen weakened!$"
