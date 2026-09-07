@ Texto ÚNICO das portas que ficaram fechadas porque o mapa do outro lado saiu
@ do escopo (a lista `CORTES_DO_GUI` de `dev_scripts/completude.py`, aplicada
@ por `dev_scripts/remove_mapas_cortados.py` no commit 721c77fb63).
@
@ Existe por dois motivos, os dois medidos em 06/09/2026:
@
@ 1. IDIOMA. As 22 placas nasceram com "Fechado. Área em obras." em português,
@    dentro de um jogo que fala inglês do início ao fim. Era a única fala em
@    português que sobrava no jogo, e o Gui a encontrou no playtest, na porta da
@    igreja de Hearthome.
@ 2. REPETIÇÃO. Cada mapa carregava a sua própria cópia da mesma frase. Aqui ela
@    é uma só, e o rótulo de cada mapa aponta para cá.
@
@ Quem lê esta placa está diante de porta cujo destino é TÚMULO de verdade
@ (cabeçalho sem evento, `MAPSEC_NONE`), conferido um a um. Porta cujo destino
@ ainda é mapa vivo NÃO recebe placa: ela é reaberta.
Common_EventScript_PortaFechada::
	msgbox Common_Text_PortaFechada, MSGBOX_SIGN
	end

Common_Text_PortaFechada:
	.string "Closed for renovations.$"

@ Boca de caverna que nenhuma das cinco fontes de Johto abre (hns, GS
@ Chronicles, Liquid Crystal, FireGold e Scorched Silver), medido em 07/09/2026
@ na pergunta 46 do Gui. Frase própria porque a placa de prédio fala em obra,
@ e buraco de pedra não está em obra nenhuma.
Common_EventScript_BocaFechada::
	msgbox Common_EventScript_BocaFechada_Text, MSGBOX_SIGN
	end

Common_EventScript_BocaFechada_Text:
	.string "The cave mouth is blocked by fallen rocks.$"

@ Cais sem barco (07/09/2026, cartucho 1 onda 4). O píer oeste da Battle
@ Frontier embarcava para a praça `TrainerHill_Courtyard`, ao norte da Route 40,
@ que a decisão 29 do Gui tirou do jogo: prédio em Johto não leva a facility de
@ Hoenn, e o caminho valia nos dois sentidos. O tile de embarque continua
@ desenhado e agora explica por que ninguém embarca. Frase própria, e não a
@ placa de obras, pela mesma razão que a boca de caverna tem a dela: píer não
@ está em obra.
Common_EventScript_CaisFechado::
	msgbox Common_Text_CaisFechado, MSGBOX_SIGN
	end

Common_Text_CaisFechado:
	.string "No ferry runs from this berth.$"
