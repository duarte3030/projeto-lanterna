@ Mecanica compartilhada das salas da Elite dos Quatro de Sinnoh.
@
@ ponytail: as cinco salas reusam os layouts da Elite de Hoenn, entao os
@ metatiles e as coordenadas de porta de data/scripts/elite_four.inc valem sem
@ mudanca nenhuma. Abrir a porta depois da vitoria e chamada direta de
@ PokemonLeague_EliteFour_SetAdvanceToNextRoomMetatiles, que ja existe.
@
@ A porta de ENTRADA nao e fechada atras do jogador, ao contrario de Hoenn.
@ Fechar exige VAR_ELITE_4_STATE, que e de Hoenn e nao pode ser reusada sem
@ misturar o progresso das duas Elites, e var nova nao se inventa
@ (Pokemon Claude/SINNOH-PADRAO.md: sobram 23 no jogo inteiro). Efeito colateral:
@ da para voltar uma sala para curar. Aceito de proposito.
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
