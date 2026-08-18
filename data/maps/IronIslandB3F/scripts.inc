IronIslandB3F_MapScripts::
	.byte 0

@ BLOQUEADO (S7, 18/08/2026). A fonte (scripts_iron_island_b*.s) resolve a
@ plataforma inteira com dois specials, InitPersistedMapFeaturesForPlatform
@ Lift (OnTransition) e TriggerPlatformLift (o coord_event), nenhum dos dois
@ existe neste motor (`grep` em include/ e src/ confirma zero ocorrencias).
@ Nao e so o texto/movimento que falta: e a mecanica de plataforma
@ deslizante inteira (estado persistido entre visitas ao andar). "Specials
@ inexistentes descartados com comentario", sem substituto aqui. Volta ao
@ plano.
IronIslandB3F_EventScript_CoordEvent_PlatformLift::
	end
