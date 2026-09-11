EcruteakCity_SageOffice2_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EcruteakCity_SageOffice2_OnTransition
	.byte 0

@ >>> Retorno dinamico de predio compartilhado (frente A, 11/09/2026) >>>
@ Este predio tem DUAS entradas de rua: a Bellchime Trail e a ECRUTEAK copiada.
@ Ate a copia de Ecruteak a porta de la nunca disparava, entao a saida
@ cravada em MAP_BELLCHIME_TRAIL nao incomodava ninguem; com a porta
@ funcionando, quem entrasse pela cidade saia na trilha, do outro lado do
@ mapa. O tile de porta virou MAP_DYNAMIC e quem grava a origem e o motor,
@ em SetupWarp. O special e rede para save antiga que tenha sido gravada
@ aqui dentro com retorno velho. Corpo e motivo no bloco "Retorno dos
@ predios que duas regioes dividem", em src/field_specials.c.
EcruteakCity_SageOffice2_OnTransition:
	special DefinirRetornoPredioCompartilhado
	end
@ <<< Retorno dinamico de predio compartilhado <<<
