@ Menu de destinos do barco que liga as cinco regiões, montado em tempo de
@ execução a partir das flags de progresso. Escrito em 11/08/2026.
@
@ POR QUE ELE EXISTE
@
@ Até aqui os cinco portos ofereciam os quatro destinos desde o primeiro minuto
@ de jogo, e o único portão da travessia inteira era o PASSE TRI de Vermilion:
@ dava para zarpar de Kanto direto para Unova e destruir a curva de nível
@ (Kanto 3-50, Unova 195-255). As três FLAG_REGIAO_*_LIBERADA já estavam
@ reservadas em include/constants/flags.h com o desenho escrito ao lado delas,
@ e nenhum script as lia ou acendia. Este arquivo é esse desenho ligado.
@
@ COMO FUNCIONA, E POR QUE NENHUM PORTO PRECISOU MUDAR O ROTEAMENTO
@
@ `dynmultipush NOME, ID` empilha uma opção com um ID PRÓPRIO, e o
@ `dynmultistack` devolve em VAR_RESULT esse ID, não a linha escolhida
@ (src/scrcmd.c:1884 grava item.id, e Task_HandleScrollingMultichoiceInput em
@ src/script_menu.c grava `gSpecialVar_Result = input`, que é o id da lista).
@ Então os IDs continuam sendo os mesmos índices da antiga
@ MULTI_CINCO_REGIOES_BARCO (0 OLIVINE, 1 SLATEPORT, 2 VERMILION, 3 VIRBANK,
@ 4 CANALAVE, 5 Sair) e todos os `case N` dos cinco portos seguem valendo sem
@ um caractere de diferença. O que muda é só QUAIS opções aparecem.
@
@ MUDA A CONTAGEM DE `DOWN` DOS TESTES. O menu não dá a volta e agora encolhe,
@ então o número de DOWN até um destino deixa de ser o próprio índice: passa a
@ ser a posição dele DENTRO da lista já filtrada. Os roteiros de T4, T6, T8,
@ T10 e T86 foram refeitos junto com esta mudança.
@
@ QUEM ACENDE CADA FLAG
@
@   FLAG_REGIAO_JOHTO_LIBERADA   campeão de Kanto  (PokemonLeague_ChampionsRoom_Frlg)
@   FLAG_REGIAO_HOENN_LIBERADA   Clair, 8a insígnia de Johto (BlackthornCity_Gym)
@   FLAG_REGIAO_SINNOH_LIBERADA  Wallace, campeão de Hoenn (EverGrandeCity_ChampionsRoom)
@   Unova                        FLAG_ELITE_SINNOH_VENCIDA, que a Cynthia já acendia
@
@ Johto é a exceção declarada: esta ROM NÃO tem uma Elite dos Quatro de Johto
@ (a Liga de gen 2 é o mesmo Planalto Índigo de Kanto, que aqui são os mapas
@ PokemonLeague_*_Frlg). O fim de Johto que existe de verdade é a oitava
@ insígnia, então é ela que abre Hoenn. Zero flag nova: as três já estavam
@ reservadas e a de Sinnoh já existia.

Travessia_EventScript_MenuDeDestinos::
	call_if_set FLAG_REGIAO_JOHTO_LIBERADA, Travessia_EventScript_EmpilhaOlivine
	call_if_set FLAG_REGIAO_HOENN_LIBERADA, Travessia_EventScript_EmpilhaSlateport
	@ Kanto é a região onde o jogo começa: o porto dela nunca fica escondido.
	dynmultipush Travessia_Text_Vermilion, 2
	call_if_set FLAG_ELITE_SINNOH_VENCIDA, Travessia_EventScript_EmpilhaVirbank
	call_if_set FLAG_REGIAO_SINNOH_LIBERADA, Travessia_EventScript_EmpilhaCanalave
	dynmultipush Travessia_Text_Sair, 5
	dynmultistack 0, 0, FALSE, 6, FALSE, 0, DYN_MULTICHOICE_CB_NONE
	return

Travessia_EventScript_EmpilhaOlivine::
	dynmultipush Travessia_Text_Olivine, 0
	return

Travessia_EventScript_EmpilhaSlateport::
	dynmultipush Travessia_Text_Slateport, 1
	return

Travessia_EventScript_EmpilhaVirbank::
	dynmultipush Travessia_Text_Virbank, 3
	return

Travessia_EventScript_EmpilhaCanalave::
	dynmultipush Travessia_Text_Canalave, 4
	return

Travessia_Text_Olivine:
	.string "OLIVINE$"

Travessia_Text_Slateport:
	.string "SLATEPORT$"

Travessia_Text_Vermilion:
	.string "VERMILION$"

Travessia_Text_Virbank:
	.string "VIRBANK$"

Travessia_Text_Canalave:
	.string "CANALAVE$"

Travessia_Text_Sair:
	.string "EXIT$"
