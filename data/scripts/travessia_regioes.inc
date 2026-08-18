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

@ GALAR, 18/08/2026 (G5 da obra de Galar, decisão 12 do PLANO-OBRAS-GALAR.md)
@
@ Galar entra como sexto destino ATRÁS DE FLAG DE TESTE, para o Gui poder andar
@ na região antes de a fase de conteúdo abrir. A flag é FLAG_GALAR_QA_ANDAR,
@ apelido de FLAG_UNUSED_0x1CFF (faixa de Galar, decisão 6): apelidar UNUSED não
@ mexe em FLAGS_COUNT, então a janela de save continua fechada. Nenhum script a
@ acende; ela se liga pelo menu de debug (Flags & Vars) ou pelo modo de teste.
@
@ A volta existe: WEDGEHURST_05 ganhou um marinheiro (dev_scripts/gente_galar.py,
@ OBJETOS_A_MAO) que chama ESTE MESMO menu, então de Galar se sai para as cinco
@ regiões pelas mesmas regras. Sem ele a viagem seria de mão única.
@
@ O id empilhado é 6, e por isso NENHUM `case` dos cinco portos mudou de número.
@ O último argumento de contagem do `dynmultistack` sobe de 6 para 7, porque ele
@ é o TAMANHO MÁXIMO da lista e não o número de opções visíveis.

Travessia_EventScript_MenuDeDestinos::
	call_if_set FLAG_REGIAO_JOHTO_LIBERADA, Travessia_EventScript_EmpilhaOlivine
	call_if_set FLAG_REGIAO_HOENN_LIBERADA, Travessia_EventScript_EmpilhaSlateport
	@ Kanto é a região onde o jogo começa: o porto dela nunca fica escondido.
	dynmultipush Travessia_Text_Vermilion, 2
	call_if_set FLAG_ELITE_SINNOH_VENCIDA, Travessia_EventScript_EmpilhaVirbank
	call_if_set FLAG_REGIAO_SINNOH_LIBERADA, Travessia_EventScript_EmpilhaCanalave
	call_if_set FLAG_GALAR_QA_ANDAR, Travessia_EventScript_EmpilhaWedgehurst
	dynmultipush Travessia_Text_Sair, 5
	dynmultistack 0, 0, FALSE, 7, FALSE, 0, DYN_MULTICHOICE_CB_NONE
	return

@ A ida para Galar é UMA só, compartilhada pelos cinco portos: `case 6` de cada
@ um aponta para cá, em vez de cada porto ganhar um roteiro igual ao dos outros.
@ (23,18) de WEDGEHURST_05 foi medido no blockdata: colisão 0, elevação 3, sem
@ warp e sem objeto em cima, e o marinheiro fica colado, em (23,17).
Travessia_EventScript_ZarparParaGalar::
	msgbox Travessia_Text_SetSailToGalar, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_GALAR_WEDGEHURST_05, 23, 18
	waitstate
	release
	end

@ O marinheiro do lado de Galar. Mesmo menu, mesmos ids; o `case 6` não aparece
@ aqui porque quem já está em Galar não zarpa para Galar.
Travessia_EventScript_MarinheiroGalar::
	lock
	faceplayer
	msgbox Travessia_Text_GalarWhereTo, MSGBOX_DEFAULT
	call Travessia_EventScript_MenuDeDestinos
	switch VAR_RESULT
	case 0, Travessia_EventScript_GalarParaOlivine
	case 1, Travessia_EventScript_GalarParaSlateport
	case 2, Travessia_EventScript_GalarParaVermilion
	case 3, Travessia_EventScript_GalarParaVirbank
	case 4, Travessia_EventScript_GalarParaCanalave
	msgbox Travessia_Text_GalarComeAgain, MSGBOX_DEFAULT
	release
	end

@ As coordenadas de chegada são as mesmas que os cinco portos já usam entre si
@ (copiadas de data/maps/*/scripts.inc, não escolhidas aqui).
Travessia_EventScript_GalarParaOlivine::
	msgbox Travessia_Text_GalarSetSail, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	waitstate
	release
	end

Travessia_EventScript_GalarParaSlateport::
	msgbox Travessia_Text_GalarSetSail, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SLATEPORT_CITY_HARBOR, 8, 14
	waitstate
	release
	end

Travessia_EventScript_GalarParaVermilion::
	msgbox Travessia_Text_GalarSetSail, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_VERMILION_CITY, 15, 10
	waitstate
	release
	end

Travessia_EventScript_GalarParaVirbank::
	msgbox Travessia_Text_GalarSetSail, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_UNOVA_VIRBANK_PORT, 4, 6
	waitstate
	release
	end

Travessia_EventScript_GalarParaCanalave::
	msgbox Travessia_Text_GalarSetSail, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_CANALAVE_CITY, 17, 49
	waitstate
	release
	end

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

Travessia_EventScript_EmpilhaWedgehurst::
	dynmultipush Travessia_Text_Wedgehurst, 6
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

Travessia_Text_Wedgehurst:
	.string "WEDGEHURST$"

Travessia_Text_Sair:
	.string "EXIT$"

Travessia_Text_GalarWhereTo:
	.string "Welcome to WEDGEHURST, GALAR!\n"
	.string "Where would you like to sail?$"

Travessia_Text_GalarSetSail:
	.string "Setting sail!$"

Travessia_Text_SetSailToGalar:
	.string "Setting sail for WEDGEHURST\n"
	.string "in GALAR!$"

Travessia_Text_GalarComeAgain:
	.string "Come see me whenever you want to\nsail between the regions.$"
