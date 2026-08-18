@ Roteiro do seletor de capítulo. A tabela, os nomes e todo o efeito moram em
@ src/chapter_jump.c; aqui só ficam os dois menus e o vaivém entre eles, que é a
@ parte que PRECISA ser script (a parada de contexto do multichoice e o
@ `waitstate` do warp só existem no interpretador).
@
@ Entram aqui dois caminhos, com o mesmo roteiro: o item CHAPTER JUMP
@ (src/item_use.c, ItemUseOutOfBattle_ChapterJump) e o seletor automático do
@ jogo novo (src/field_control_avatar.c).
@
@ O menu é o `dynmultistack`, o mesmo do menu do barco em travessia_regioes.inc:
@ a lista é empilhada em C e ele a consome, rolando sozinho quando passa das 6
@ linhas. VAR_RESULT volta com o `id` empilhado, e não com a linha escolhida.

ChapterJump_EventScript_Abrir::
	lockall
ChapterJump_EventScript_MenuDeRegioes::
	special ChapterJump_MontaListaDeRegioes
	@ SEM `waitstate` atrás, e isso é o conserto de 17/08/2026: o próprio
	@ `dynmultistack` já para o contexto (ScrCmd_dynmultichoice chama
	@ ScriptContext_Stop, src/scrcmd.c) e quem o religa é a tarefa do menu,
	@ ao escolher. O `waitstate` extra parava o contexto UMA SEGUNDA VEZ, e aí
	@ não sobrava ninguém para religar: o menu fechava, o jogo ficava travado
	@ para sempre e New Game era injogável. O menu do barco
	@ (data/scripts/travessia_regioes.inc, o modelo deste aqui) nunca teve
	@ waitstate depois do dynmultistack.
	dynmultistack 0, 0, FALSE, 6, FALSE, 0, DYN_MULTICHOICE_CB_NONE
	compare VAR_RESULT, MULTI_B_PRESSED
	goto_if_eq ChapterJump_EventScript_Sair
	copyvar VAR_0x8004, VAR_RESULT

ChapterJump_EventScript_MenuDeCapitulos::
	@ Quem sabe quantas regiões existem é a tabela em C, não este arquivo: o
	@ montador devolve FALSE quando VAR_0x8004 não é região, que é o caso da
	@ última entrada da lista (EXIT, ou START FROM BEGINNING no jogo novo).
	@ Assim acrescentar uma região nunca obriga a mexer aqui.
	specialvar VAR_RESULT, ChapterJump_MontaListaDeCapitulos
	compare VAR_RESULT, FALSE
	goto_if_eq ChapterJump_EventScript_Sair
	@ Mesmo conserto do menu de cima: o dynmultistack já para o contexto sozinho.
	dynmultistack 0, 0, FALSE, 6, FALSE, 0, DYN_MULTICHOICE_CB_NONE
	@ B aqui volta um nível, para a lista de regiões, em vez de fechar tudo:
	@ errar a região é o engano mais provável do seletor.
	compare VAR_RESULT, MULTI_B_PRESSED
	goto_if_eq ChapterJump_EventScript_MenuDeRegioes
	copyvar VAR_0x8005, VAR_RESULT
	@ Acende as flags, cura o time e teleporta. Este special traz um `waitstate`
	@ implícito (data/specials.inc) e termina em warp, então NÃO leva
	@ `releaseall` atrás: carregar o mapa novo já devolve o controle, e é assim
	@ que todo roteiro de warp da ROM termina (ex.: BattleFrontier_BattleDomeCorridor).
	special ChapterJump_AplicaCapitulo
	end

ChapterJump_EventScript_Sair::
	releaseall
	end
