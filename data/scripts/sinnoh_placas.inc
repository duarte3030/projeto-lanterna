@ Placa genérica das placas trazidas do pokeplatinum em 05/08/2026.
@
@ No Platinum o campo "script" da placa é um índice numérico dentro do arquivo de
@ scripts do mapa, e o texto mora num banco de mensagens separado. Nada disso
@ atravessa para cá: a placa que ainda não teve o texto portado aponta para este
@ rótulo único, e a placa EXISTE, dá para ler e não trava.
@
@ Estado em 11/08/2026, medido: das 680 placas importadas, 424 já têm texto
@ próprio e 256 continuam aqui. `dev_scripts/texto_sinnoh.py` segue a corrente
@ índice -> ScriptEntry -> banco de texto e porta o resto quando der.
@
@ ATENÇÃO: 146 das que continuam apontando para cá NÃO são placa. São item
@ escondido do Platinum, onde placa e item moram no mesmo array `bg_events` e só
@ se distinguem pela faixa do campo `script` (8000 a 8799 é
@ SCRIPT_ID_OFFSET_HIDDEN_ITEMS). Elas ficam de propósito com este texto e NÃO
@ devem ganhar fala: virar item de verdade custa uma flag por item e é decisão
@ do dono do projeto (decisão 13 do ESTADO.md). A lista sai de
@ `python3 dev_scripts/texto_sinnoh.py --itens`.

Sinnoh_EventScript_PlacaImportada::
	msgbox Sinnoh_Text_PlacaImportada, MSGBOX_SIGN
	end

Sinnoh_Text_PlacaImportada:
	.string "The lettering has faded with age.$"
