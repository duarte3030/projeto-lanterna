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
