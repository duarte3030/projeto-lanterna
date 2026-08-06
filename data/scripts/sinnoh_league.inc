@ Mecanica compartilhada das salas da Elite dos Quatro de Sinnoh.
@
@ ponytail: as cinco salas reusam os layouts da Elite de Hoenn, entao os
@ metatiles e as coordenadas de porta de data/scripts/elite_four.inc valem sem
@ mudanca nenhuma. Abrir a porta depois da vitoria e chamada direta de
@ PokemonLeague_EliteFour_SetAdvanceToNextRoomMetatiles, que ja existe.
@
@ A porta de ENTRADA nao e fechada atras do jogador com setmetatile, ao contrario
@ de Hoenn, e NAO PRECISA SER. O paragrafo antigo aqui dizia que isso deixava
@ "voltar uma sala para curar": era falso, e custou uma sessao inteira. O que foi
@ MEDIDO em 06/08/2026, nos dados e no emulador:
@
@  - o tile de entrada (6,13) e o metatile 0x234 do gTileset_EliteFour, e o
@    comportamento dele e MB_NORMAL (0x00). As duas variantes de porta fechada
@    (METATILE_EliteFour_EntryDoor_ClosedTop 0x206 e ClosedBottom 0x20E) tambem
@    sao MB_NORMAL. IsWarpMetatileBehavior (src/field_control_avatar.c) exige
@    porta, escada, escalator ou um dos warps especiais, entao o warp_event 0
@    dessas salas NUNCA dispara por pisar nele: ele so serve de ancora de
@    chegada. Fechar a porta trocaria um tile que nao warpa por outro que
@    tambem nao warpa.
@  - a UNICA saida e a porta da frente, METATILE_EliteFour_OpenDoor_Opening
@    (0x345), que e MB_LADDER (0x60), warp de verdade. E ela so aparece no mapa
@    quando SetAdvanceToNextRoomMetatiles roda, ou seja, depois da vitoria.
@  - prova no emulador: T83.1 e T83.2 em dev_scripts/testes_criticos/
@    83_porta_elite_sinnoh.json.
@
@ Ou seja, o corredor da Elite ja e de mao unica de graca, sem flag e sem var.
@ Nao gaste flag para "consertar" isto.
@
@ "Membro ja derrotado" tambem nao gasta flag: quem responde e a flag propria do
@ treinador (TRAINER_FLAGS_START + id), lida com checktrainerflag.

@ Abre a porta do fundo sem som e sem mover o jogador. Usado no ON_LOAD, para a
@ porta continuar aberta quando o jogador volta para uma sala ja vencida.
SinnohLeague_EventScript_OpenNextDoorSilent::
	setmetatile 6, 1, METATILE_EliteFour_OpenDoor_Frame, FALSE
	setmetatile 6, 2, METATILE_EliteFour_OpenDoor_Opening, FALSE
	setmetatile 0, 2, METATILE_EliteFour_RightSpotlightOff, TRUE
	setmetatile 1, 2, METATILE_EliteFour_LeftSpotlightOff, TRUE
	setmetatile 2, 2, METATILE_EliteFour_RightSpotlightOff, TRUE
	setmetatile 3, 2, METATILE_EliteFour_LeftSpotlightOff, TRUE
	setmetatile 4, 2, METATILE_EliteFour_RightSpotlightOff, TRUE
	setmetatile 8, 2, METATILE_EliteFour_LeftSpotlightOff, TRUE
	setmetatile 9, 2, METATILE_EliteFour_RightSpotlightOff, TRUE
	setmetatile 10, 2, METATILE_EliteFour_LeftSpotlightOff, TRUE
	setmetatile 11, 2, METATILE_EliteFour_RightSpotlightOff, TRUE
	setmetatile 12, 2, METATILE_EliteFour_LeftSpotlightOff, TRUE
	return
