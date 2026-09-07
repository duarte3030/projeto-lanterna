@ Turnback Cave: o sorteio de sala.
@ Gerado por dev_scripts/turnback_cave_sinnoh.py, que explica no topo
@ de onde cada regra saiu (src/scrcmd.c:6089 do pokeplatinum).
@ A porta e warp normal com destino MAP_DYNAMIC; quem decide para onde
@ ela leva e o `setdynamicwarp` que roda no ON_TRANSITION da sala.

TurnbackCave_OnTransitionEntrada::
	setvar VAR_TURNBACK_PILARES_VISTOS, 0
	setvar VAR_TURNBACK_SALAS_VISITADAS, 0
	goto TurnbackCave_Sorteia
	end

TurnbackCave_OnTransitionSala::
	addvar VAR_TURNBACK_SALAS_VISITADAS, 1
	goto TurnbackCave_Sorteia
	end

@ A sala do pilar e a unica que conta pilar. Tres pilares abrem a
@ sala da Giratina, que e a regra 1 do scrcmd.
TurnbackCave_OnTransitionPilar::
	addvar VAR_TURNBACK_SALAS_VISITADAS, 1
	addvar VAR_TURNBACK_PILARES_VISTOS, 1
	goto TurnbackCave_Sorteia
	end

@ Da sala da Giratina so se sai para a entrada.
TurnbackCave_OnTransitionGiratina::
	setdynamicwarp MAP_TURNBACK_CAVE_ENTRANCE, 0
	end

TurnbackCave_Sorteia::
	goto_if_ge VAR_TURNBACK_PILARES_VISTOS, 3, TurnbackCave_ParaGiratina
	goto_if_ge VAR_TURNBACK_SALAS_VISITADAS, 30, TurnbackCave_ParaEntrada
	random 100
	goto_if_lt VAR_RESULT, 25, TurnbackCave_ParaPilar
	switch VAR_TURNBACK_PILARES_VISTOS
	case 1, TurnbackCave_Nivel2
	case 2, TurnbackCave_Nivel3
	goto TurnbackCave_Nivel1
	end

TurnbackCave_ParaGiratina::
	setdynamicwarp MAP_TURNBACK_CAVE_GIRATINA_ROOM, 0
	end

TurnbackCave_ParaEntrada::
	setdynamicwarp MAP_TURNBACK_CAVE_ENTRANCE, 0
	end

TurnbackCave_ParaPilar::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_ROOM, 0
	end

TurnbackCave_Nivel1::
	random 6
	switch VAR_RESULT
	case 0, TurnbackCave_Nivel1Sala0
	case 1, TurnbackCave_Nivel1Sala1
	case 2, TurnbackCave_Nivel1Sala2
	case 3, TurnbackCave_Nivel1Sala3
	case 4, TurnbackCave_Nivel1Sala4
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_1_ROOM_6, 0
	end

TurnbackCave_Nivel1Sala0::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_1_ROOM_1, 0
	end

TurnbackCave_Nivel1Sala1::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_1_ROOM_2, 0
	end

TurnbackCave_Nivel1Sala2::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_1_ROOM_3, 0
	end

TurnbackCave_Nivel1Sala3::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_1_ROOM_4, 0
	end

TurnbackCave_Nivel1Sala4::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_1_ROOM_5, 0
	end

TurnbackCave_Nivel2::
	random 6
	switch VAR_RESULT
	case 0, TurnbackCave_Nivel2Sala0
	case 1, TurnbackCave_Nivel2Sala1
	case 2, TurnbackCave_Nivel2Sala2
	case 3, TurnbackCave_Nivel2Sala3
	case 4, TurnbackCave_Nivel2Sala4
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_2_ROOM_6, 0
	end

TurnbackCave_Nivel2Sala0::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_2_ROOM_1, 0
	end

TurnbackCave_Nivel2Sala1::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_2_ROOM_2, 0
	end

TurnbackCave_Nivel2Sala2::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_2_ROOM_3, 0
	end

TurnbackCave_Nivel2Sala3::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_2_ROOM_4, 0
	end

TurnbackCave_Nivel2Sala4::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_2_ROOM_5, 0
	end

TurnbackCave_Nivel3::
	random 6
	switch VAR_RESULT
	case 0, TurnbackCave_Nivel3Sala0
	case 1, TurnbackCave_Nivel3Sala1
	case 2, TurnbackCave_Nivel3Sala2
	case 3, TurnbackCave_Nivel3Sala3
	case 4, TurnbackCave_Nivel3Sala4
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_3_ROOM_6, 0
	end

TurnbackCave_Nivel3Sala0::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_3_ROOM_1, 0
	end

TurnbackCave_Nivel3Sala1::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_3_ROOM_2, 0
	end

TurnbackCave_Nivel3Sala2::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_3_ROOM_3, 0
	end

TurnbackCave_Nivel3Sala3::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_3_ROOM_4, 0
	end

TurnbackCave_Nivel3Sala4::
	setdynamicwarp MAP_TURNBACK_CAVE_PILLAR_3_ROOM_5, 0
	end
