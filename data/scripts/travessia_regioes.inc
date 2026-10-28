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

@ CARTUCHO 2, 28/10/2026 (fase 0 do PRD de assets)
@
@ Kanto, Johto, Hoenn e Sinnoh saíram desta branch: são o cartucho 1. O menu
@ ficou com os dois portos do cartucho 2, VIRBANK (id 3) e WEDGEHURST (id 6),
@ mais Sair (id 5). Os ids continuam os mesmos da lista antiga, então nenhum
@ `case` que sobrou mudou de número. Os destinos 0 (OLIVINE), 1 (SLATEPORT),
@ 2 (VERMILION) e 4 (CANALAVE) saíram, com os roteiros de ida de Galar para
@ eles. VIRBANK deixou de depender de FLAG_ELITE_SINNOH_VENCIDA (a Cynthia não
@ existe mais aqui): no cartucho 2 o jogo começa em Unova, então o porto dela
@ aparece sempre. Galar continua atrás de FLAG_GALAR_QA_ANDAR, que é decisão
@ de conteúdo e não desta obra.

Travessia_EventScript_MenuDeDestinos::
	dynmultipush Travessia_Text_Virbank, 3
	call_if_set FLAG_GALAR_QA_ANDAR, Travessia_EventScript_EmpilhaWedgehurst
	dynmultipush Travessia_Text_Sair, 5
	dynmultistack 0, 0, FALSE, 3, FALSE, 0, DYN_MULTICHOICE_CB_NONE
	return

@ A ida para Galar é UMA só: o `case 6` do porto de Virbank aponta para cá.
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
	case 3, Travessia_EventScript_GalarParaVirbank
	msgbox Travessia_Text_GalarComeAgain, MSGBOX_DEFAULT
	release
	end

@ A coordenada de chegada é a mesma que os portos já usavam entre si.
Travessia_EventScript_GalarParaVirbank::
	msgbox Travessia_Text_GalarSetSail, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_UNOVA_VIRBANK_PORT, 4, 6
	waitstate
	release
	end

Travessia_EventScript_EmpilhaWedgehurst::
	dynmultipush Travessia_Text_Wedgehurst, 6
	return

Travessia_Text_Virbank:
	.string "VIRBANK$"

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
