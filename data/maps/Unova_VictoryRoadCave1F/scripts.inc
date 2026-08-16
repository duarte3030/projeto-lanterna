@ VictoryRoadCave1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@
@ B4 da Obra 2 (changeblock), 15/08/2026. Linhas de metatile geradas por
@ dev_scripts/changeblock_gen2.py (trechos de maps/VictoryRoadCave1F.asm);
@ nenhum id de metatile foi digitado à mão.
@
@ Mecanismo da fonte: a ponte de (16..19, 20..25) tem duas caras. No andar de
@ CIMA (estado estático do map.bin) o jogador anda sobre o tabuleiro; no de
@ BAIXO ele passa por baixo e o meio da ponte vira ÁGUA. Os coord_events de
@ (14,5) e (16,32) descem, e os outros dez sobem. Estado em
@ FLAG_UNOVA_VICTORY_ROAD_ANDAR_INFERIOR. O `.Boulders` da fonte
@ (MAPCALLBACK_TILES) vira MAP_SCRIPT_ON_LOAD, decisão 4 da condutora.
@
@ ARMADILHA DA ÁGUA, e por que os dois sentidos abrem em 24 linhas em vez de 6
@ `changeblock_gen2`: a marca `agua` do changeblock_gen2.py é relativa ao
@ map.bin (estado ESTÁTICO), então só a IDA sairia com `setmetatileinrange` e
@ elevação explícita; a VOLTA sairia como `setmetatile` puro, que PRESERVA a
@ elevação (src/fieldmap.c:474, MapGridSetMetatileIdAt guarda os bits 12-15 de
@ propósito). Quem alternasse os dois estados duas vezes ficaria com o desenho
@ da ponte por cima da elevação da água: tabuleiro bonito, intransitável por
@ IsElevationMismatchAt no meio e surfável nas bordas.
@ Regra aplicada (a mesma do B3 em VillageBridge e VirbankCity, 15/08/2026):
@ comparei os DOIS estados quadrante a quadrante em vez de confiar na marca da
@ ferramenta, e TODO quadrante cuja elevação difere entre eles sai com
@ `setmetatileinrange` e elevação explícita NOS DOIS SENTIDOS. São 12, não 8: os
@ 8 que a ferramenta marca (17..18, 21..24, chão 3 <-> água 1) mais 4 que ela
@ não marca porque não tocam água, (16,22), (16,23), (19,22) e (19,23), que
@ alternam parede elevação 0 <-> passarela elevação 3; deixá-los em
@ `setmetatile` devolveria a borda da ponte andável com elevação 0, que casa com
@ QUALQUER elevação e deixaria o jogador subir da água para a ponte.
@ A ferramenta não foi mexida (a semântica do --demo fica calibrada como está);
@ os valores continuam sendo os dela, só o formato da linha mudou.
@
@ PEDRA (aprovado em 15/08/2026, ver dev_scripts/pedra_buraco_unova.py): o
@ buraco de (11,22) e (32,10) deixou de ser `MB_NON_ANIMATED_DOOR` e virou
@ `MB_MT_PYRE_HOLE`, o comportamento que o motor entende dos DOIS lados: o
@ jogador que pisa CAI (usa o mesmo warp_event que já estava lá) e a pedra que
@ para em cima some por `HandleBoulderFallThroughHole`, que agora também roda o
@ coord_event daquela casa (`RunCoordEventScriptAt`, acrescentado espelhando a
@ função irmã do FRLG). O censo provou que o metatile de porta forçada destes
@ tilesets só existe nas casas de buraco, então mudar o atributo não vaza, e
@ `map.bin` não mudou nem um byte. A pedra fica sumida depois pelo campo `flag`
@ do object_event, que é a MESMA flag da persistência: zero flag nova.

Unova_VictoryRoadCave1F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_VictoryRoadCave1F_EventScript_AoCarregar
	.byte 0

@ `.Boulders` da fonte, linhas 28-46, na mesma ordem.
Unova_VictoryRoadCave1F_EventScript_AoCarregar::
	goto_if_unset FLAG_UNOVA_VICTORY_ROAD_PEDRA_1, Unova_VictoryRoadCave1F_EventScript_AoCarregarPedra2
	call Unova_VictoryRoadCave1F_EventScript_PedraNoBuraco1
Unova_VictoryRoadCave1F_EventScript_AoCarregarPedra2::
	goto_if_unset FLAG_UNOVA_VICTORY_ROAD_PEDRA_2, Unova_VictoryRoadCave1F_EventScript_AoCarregarPonte
	call Unova_VictoryRoadCave1F_EventScript_PedraNoBuraco2
Unova_VictoryRoadCave1F_EventScript_AoCarregarPonte::
	goto_if_unset FLAG_UNOVA_VICTORY_ROAD_ANDAR_INFERIOR, Unova_VictoryRoadCave1F_EventScript_AoCarregarFim
	call Unova_VictoryRoadCave1F_EventScript_DesceAndar
Unova_VictoryRoadCave1F_EventScript_AoCarregarFim::
	end

@ `VictoryRoadCave1FLowerScript` da fonte: coord_events (14,5) e (16,32).
Unova_VictoryRoadCave1F_EventScript_GatilhoDesce::
	goto_if_set FLAG_UNOVA_VICTORY_ROAD_ANDAR_INFERIOR, Unova_VictoryRoadCave1F_EventScript_GatilhoFim
	call Unova_VictoryRoadCave1F_EventScript_DesceAndar
	setflag FLAG_UNOVA_VICTORY_ROAD_ANDAR_INFERIOR
	special DrawWholeMapView
Unova_VictoryRoadCave1F_EventScript_GatilhoFim::
	end

@ `VictoryRoadCave1FUpperScript` da fonte: coord_events (14,4), (17,32),
@ (31,35), (32,35), (33,35), (34,35), (21,4), (22,4), (5,10) e (6,10).
Unova_VictoryRoadCave1F_EventScript_GatilhoSobe::
	goto_if_unset FLAG_UNOVA_VICTORY_ROAD_ANDAR_INFERIOR, Unova_VictoryRoadCave1F_EventScript_GatilhoFim
	call Unova_VictoryRoadCave1F_EventScript_SobeAndar
	clearflag FLAG_UNOVA_VICTORY_ROAD_ANDAR_INFERIOR
	special DrawWholeMapView
	end

@ maps/VictoryRoadCave1F.asm:39-44 (e 89-94, as mesmas 6 chamadas). A cena abre
@ em 24 linhas porque 12 quadrantes trocam de elevação: explícita, decisão 1.
Unova_VictoryRoadCave1F_EventScript_DesceAndar::
	@ maps/VictoryRoadCave1F.asm:39  changeblock 16, 20, $7e ; bridge top left
	setmetatile 16, 20, 524, TRUE   @ igual ao map.bin
	setmetatile 17, 20, 516, FALSE   @ igual ao map.bin
	setmetatile 16, 21, 582, TRUE   @ igual ao map.bin
	setmetatileinrange 17, 21, 17, 21, 640, FALSE, 1   @ água: elevação explícita 1
	@ maps/VictoryRoadCave1F.asm:40  changeblock 18, 20, $7f ; bridge top right
	setmetatile 18, 20, 516, FALSE   @ igual ao map.bin
	setmetatile 19, 20, 521, TRUE   @ igual ao map.bin
	setmetatileinrange 18, 21, 18, 21, 640, FALSE, 1   @ água: elevação explícita 1
	setmetatile 19, 21, 582, TRUE   @ igual ao map.bin
	@ maps/VictoryRoadCave1F.asm:41  changeblock 16, 22, $82 ; bridge left
	setmetatileinrange 16, 22, 16, 22, 641, TRUE, 0   @ água: elevação explícita 0
	setmetatileinrange 17, 22, 17, 22, 642, FALSE, 1   @ água: elevação explícita 1
	setmetatileinrange 16, 23, 16, 23, 643, TRUE, 0   @ água: elevação explícita 0
	setmetatileinrange 17, 23, 17, 23, 644, FALSE, 1   @ água: elevação explícita 1
	@ maps/VictoryRoadCave1F.asm:42  changeblock 18, 22, $83 ; bridge right
	setmetatileinrange 18, 22, 18, 22, 642, FALSE, 1   @ água: elevação explícita 1
	setmetatileinrange 19, 22, 19, 22, 641, TRUE, 0   @ água: elevação explícita 0
	setmetatileinrange 18, 23, 18, 23, 644, FALSE, 1   @ água: elevação explícita 1
	setmetatileinrange 19, 23, 19, 23, 643, TRUE, 0   @ água: elevação explícita 0
	@ maps/VictoryRoadCave1F.asm:43  changeblock 16, 24, $86 ; bridge bot left
	setmetatile 16, 24, 582, TRUE   @ igual ao map.bin
	setmetatileinrange 17, 24, 17, 24, 640, FALSE, 1   @ água: elevação explícita 1
	setmetatile 16, 25, 525, TRUE   @ igual ao map.bin
	setmetatile 17, 25, 516, FALSE   @ igual ao map.bin
	@ maps/VictoryRoadCave1F.asm:44  changeblock 18, 24, $87 ; bridge bot right
	setmetatileinrange 18, 24, 18, 24, 640, FALSE, 1   @ água: elevação explícita 1
	setmetatile 19, 24, 582, TRUE   @ igual ao map.bin
	setmetatile 18, 25, 516, FALSE   @ igual ao map.bin
	setmetatile 19, 25, 521, TRUE   @ igual ao map.bin
	return

@ maps/VictoryRoadCave1F.asm:102-107. Restauração do estado inicial: as 24
@ linhas são `igual ao map.bin`, e por isso mesmo NENHUMA pode ser apagada.
@ As 12 de elevação variável saem em `setmetatileinrange` com elevação
@ explícita, pelo motivo escrito no cabeçalho (setmetatile não desfaz a
@ elevação que a ida deixou).
Unova_VictoryRoadCave1F_EventScript_SobeAndar::
	@ maps/VictoryRoadCave1F.asm:102  changeblock 16, 20, $36 ; bridge top left
	setmetatile 16, 20, 524, TRUE   @ igual ao map.bin
	setmetatile 17, 20, 516, FALSE   @ igual ao map.bin
	setmetatile 16, 21, 582, TRUE   @ igual ao map.bin
	setmetatileinrange 17, 21, 17, 21, 582, TRUE, 0   @ igual ao map.bin, água: elevação explícita 0
	@ maps/VictoryRoadCave1F.asm:103  changeblock 18, 20, $3b ; bridge top right
	setmetatile 18, 20, 516, FALSE   @ igual ao map.bin
	setmetatile 19, 20, 521, TRUE   @ igual ao map.bin
	setmetatileinrange 18, 21, 18, 21, 582, TRUE, 0   @ igual ao map.bin, água: elevação explícita 0
	setmetatile 19, 21, 582, TRUE   @ igual ao map.bin
	@ maps/VictoryRoadCave1F.asm:104  changeblock 16, 22, $3e ; bridge left
	setmetatileinrange 16, 22, 16, 22, 587, FALSE, 3   @ igual ao map.bin, água: elevação explícita 3
	setmetatileinrange 17, 22, 17, 22, 587, FALSE, 3   @ igual ao map.bin, água: elevação explícita 3
	setmetatileinrange 16, 23, 16, 23, 589, FALSE, 3   @ igual ao map.bin, água: elevação explícita 3
	setmetatileinrange 17, 23, 17, 23, 589, FALSE, 3   @ igual ao map.bin, água: elevação explícita 3
	@ maps/VictoryRoadCave1F.asm:105  changeblock 18, 22, $3e ; bridge right
	setmetatileinrange 18, 22, 18, 22, 587, FALSE, 3   @ igual ao map.bin, água: elevação explícita 3
	setmetatileinrange 19, 22, 19, 22, 587, FALSE, 3   @ igual ao map.bin, água: elevação explícita 3
	setmetatileinrange 18, 23, 18, 23, 589, FALSE, 3   @ igual ao map.bin, água: elevação explícita 3
	setmetatileinrange 19, 23, 19, 23, 589, FALSE, 3   @ igual ao map.bin, água: elevação explícita 3
	@ maps/VictoryRoadCave1F.asm:106  changeblock 16, 24, $42 ; bridge bot left
	setmetatile 16, 24, 582, TRUE   @ igual ao map.bin
	setmetatileinrange 17, 24, 17, 24, 582, TRUE, 0   @ igual ao map.bin, água: elevação explícita 0
	setmetatile 16, 25, 525, TRUE   @ igual ao map.bin
	setmetatile 17, 25, 516, FALSE   @ igual ao map.bin
	@ maps/VictoryRoadCave1F.asm:107  changeblock 18, 24, $43 ; bridge bot right
	setmetatileinrange 18, 24, 18, 24, 582, TRUE, 0   @ igual ao map.bin, água: elevação explícita 0
	setmetatile 19, 24, 582, TRUE   @ igual ao map.bin
	setmetatile 18, 25, 516, FALSE   @ igual ao map.bin
	setmetatile 19, 25, 521, TRUE   @ igual ao map.bin
	return

@ maps/VictoryRoadCave1F.asm:31 (e 64, dentro do `.Boulder1` do stonetable)
@ ATENCAO: muda warp em (11,22): MB_NON_ANIMATED_DOOR -> MB_CAVE, conferir warp_events
@ Conferido: o warp_event 9 do map.json é (11,22) -> MAP_UNOVA_VICTORY_ROAD_CAVE_1F
@ warp 0, isto é (31,36), a boca norte. É o próprio buraco em que a pedra cai;
@ matar o warp é o efeito querido da cena, não acidente.
Unova_VictoryRoadCave1F_EventScript_PedraNoBuraco1::
	changeblock_gen2 10, 22, 527, 635, 534, 533, FALSE, FALSE, TRUE, FALSE   @ igual ao map.bin: CE, BE, BD
	return

@ maps/VictoryRoadCave1F.asm:35 (e 76, dentro do `.Boulder2` do stonetable)
@ ATENCAO: muda warp em (32,10): MB_NON_ANIMATED_DOOR -> MB_CAVE, conferir warp_events
@ Conferido: o warp_event 10 do map.json é (32,10) -> MAP_UNOVA_VICTORY_ROAD_CAVE_1F
@ warp 0, mesmo destino do outro buraco. Mesmo veredito.
Unova_VictoryRoadCave1F_EventScript_PedraNoBuraco2::
	changeblock_gen2 32, 10, 635, 529, 531, 533, FALSE, FALSE, FALSE, FALSE   @ igual ao map.bin: CD, BE, BD
	return

@ `.Boulder1` e `.Boulder2` do stonetable da fonte (linhas 57-77). Gatilho: os
@ coord_events de (11,22) e (32,10), as casas dos buracos, com var_value que
@ NUNCA casa (VAR_TEMP_0 nasce 0 a cada mapa), pelo idioma do
@ VictoryRoad_1F_Frlg: o jogador que pisa no buraco CAI (MB_MT_PYRE_HOLE, que
@ usa o warp_event que já está lá) e não roda isto; quem roda é só a pedra que
@ parou em cima, via HandleBoulderFallThroughHole. O motor já tocou SE_FALL e
@ tirou a pedra; o `flag` do object_event a mantém sumida depois.
Unova_VictoryRoadCave1F_EventScript_PedraCai1::
	lockall
	msgbox Unova_VictoryRoadCave1F_Text_PedraCaiu, MSGBOX_DEFAULT
	setflag FLAG_UNOVA_VICTORY_ROAD_PEDRA_1
	call Unova_VictoryRoadCave1F_EventScript_PedraNoBuraco1
	special DrawWholeMapView
	releaseall
	end

Unova_VictoryRoadCave1F_EventScript_PedraCai2::
	lockall
	msgbox Unova_VictoryRoadCave1F_Text_PedraCaiu, MSGBOX_DEFAULT
	setflag FLAG_UNOVA_VICTORY_ROAD_PEDRA_2
	call Unova_VictoryRoadCave1F_EventScript_PedraNoBuraco2
	special DrawWholeMapView
	releaseall
	end

Unova_VictoryRoadCave1F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_VICTORY_ROAD_INT_1, Unova_VictoryRoadCave1F_Text_AceTrainerMVictoryRoadCave1FSeenText, Unova_VictoryRoadCave1F_Text_AceTrainerMVictoryRoadCave1FBeatenText
	end

Unova_VictoryRoadCave1F_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_VICTORY_ROAD_INT_2, Unova_VictoryRoadCave1F_Text_AceTrainerFVictoryRoadCave1FSeenText, Unova_VictoryRoadCave1F_Text_AceTrainerFVictoryRoadCave1FBeatenText
	end

Unova_VictoryRoadCave1F_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_VETERANM_VICTORY_ROAD_INT_1, Unova_VictoryRoadCave1F_Text_VeteranMVictoryRoadCave1FSeenText, Unova_VictoryRoadCave1F_Text_VeteranMVictoryRoadCave1FBeatenText
	end

Unova_VictoryRoadCave1F_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_VETERANF_VICTORY_ROAD_INT_1, Unova_VictoryRoadCave1F_Text_VeteranFVictoryRoadCave1FSeenText, Unova_VictoryRoadCave1F_Text_VeteranFVictoryRoadCave1FBeatenText
	end

Unova_VictoryRoadCave1F_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_PSYCHICM_VICTORY_ROAD_INT, Unova_VictoryRoadCave1F_Text_PsychicMVictoryRoadCave1FSeenText, Unova_VictoryRoadCave1F_Text_PsychicMVictoryRoadCave1FBeatenText
	end

Unova_VictoryRoadCave1F_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_PSYCHICF_VICTORY_ROAD_INT, Unova_VictoryRoadCave1F_Text_PsychicFVictoryRoadCave1FSeenText, Unova_VictoryRoadCave1F_Text_PsychicFVictoryRoadCave1FBeatenText
	end

Unova_VictoryRoadCave1F_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_HEX_MANIAC_VICTORY_ROAD_INT, Unova_VictoryRoadCave1F_Text_HexManiacVictoryRoadCave1FSeenText, Unova_VictoryRoadCave1F_Text_HexManiacVictoryRoadCave1FBeatenText
	end


@ `VictoryRoadCave1FBoulderFellText` da fonte, uma só para as duas pedras.
Unova_VictoryRoadCave1F_Text_PedraCaiu::
	.string "The boulder fell\n"
	.string "through!$"

Unova_VictoryRoadCave1F_Text_AceTrainerMVictoryRoadCave1FSeenText::
	.string "An ACE TRAINER"
	.string "\nlike me has pride,"
	.string "\lso I won't lose!$"

Unova_VictoryRoadCave1F_Text_AceTrainerMVictoryRoadCave1FBeatenText::
	.string "I couldn't protect"
	.string "\nmy pride! I'm"
	.string "\lmortified!$"

Unova_VictoryRoadCave1F_Text_AceTrainerFVictoryRoadCave1FSeenText::
	.string "Challenging the"
	.string "\nPOKéMON LEAGUE?"
	.string "\pIt's no wonder you"
	.string "\nmight feel a bit"
	.string "\pnervous, but you"
	.string "\njust have to"
	.string "\pbelieve in your"
	.string "\nPOKéMON and do it!$"

Unova_VictoryRoadCave1F_Text_AceTrainerFVictoryRoadCave1FBeatenText::
	.string "Am I really going"
	.string "\nto be alright with"
	.string "\ponly this trifling"
	.string "\npower?$"

Unova_VictoryRoadCave1F_Text_VeteranMVictoryRoadCave1FSeenText::
	.string "You bothered to"
	.string "\ncome all the way"
	.string "\phere? Good! I will"
	.string "\nreward your hard"
	.string "\pwork by battling"
	.string "\nwith all of my"
	.string "\lstrength!$"

Unova_VictoryRoadCave1F_Text_VeteranMVictoryRoadCave1FBeatenText::
	.string "A battle with a"
	.string "\ngood trainer fills"
	.string "\pmy heart with"
	.string "\nwarmth!$"

Unova_VictoryRoadCave1F_Text_VeteranFVictoryRoadCave1FSeenText::
	.string "Hey, since you"
	.string "\nworked so hard to"
	.string "\pget here, how"
	.string "\nabout I be your"
	.string "\lopponent?$"

Unova_VictoryRoadCave1F_Text_VeteranFVictoryRoadCave1FBeatenText::
	.string "Thanks a bunch. It"
	.string "\nwas a lot of fun!$"

Unova_VictoryRoadCave1F_Text_PsychicMVictoryRoadCave1FSeenText::
	.string "You… Who's brought"
	.string "\nyou this far?$"

Unova_VictoryRoadCave1F_Text_PsychicMVictoryRoadCave1FBeatenText::
	.string "It's your reliable"
	.string "\nPOKéMON who've"
	.string "\pbrought you this"
	.string "\nfar, isn't it?$"

Unova_VictoryRoadCave1F_Text_PsychicFVictoryRoadCave1FSeenText::
	.string "I'll use my psychic"
	.string "\npowers to release"
	.string "\pmy POKéMON from"
	.string "\nits POKéBALL!$"

Unova_VictoryRoadCave1F_Text_PsychicFVictoryRoadCave1FBeatenText::
	.string "Well, that didn't"
	.string "\ngo the way I"
	.string "\lwanted it to!$"

Unova_VictoryRoadCave1F_Text_HexManiacVictoryRoadCave1FSeenText::
	.string "You are no ordin-"
	.string "\nary opponent…"
	.string "\pThat is what my"
	.string "\nghost type POKéMON"
	.string "\pis whispering to"
	.string "\nme.$"

Unova_VictoryRoadCave1F_Text_HexManiacVictoryRoadCave1FBeatenText::
	.string "My premonition was"
	.string "\nspot on!$"
