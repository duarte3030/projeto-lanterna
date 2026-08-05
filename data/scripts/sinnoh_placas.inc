@ Placa genérica das 425 placas trazidas do pokeplatinum em 05/08/2026.
@
@ No Platinum o campo "script" da placa é um índice numérico dentro do arquivo de
@ scripts do mapa, e o texto mora num banco de mensagens separado. Nada disso
@ atravessa para cá, então importar o texto exigiria portar os bancos de texto
@ inteiros de Sinnoh. Enquanto isso não acontece, toda placa importada aponta
@ para este rótulo único: a placa EXISTE, dá para ler e não trava.
@
@ Substituir por texto próprio mapa a mapa está registrado em
@ PENDENCIAS-NPC-SINNOH.md.

Sinnoh_EventScript_PlacaImportada::
	msgbox Sinnoh_Text_PlacaImportada, MSGBOX_SIGN
	end

Sinnoh_Text_PlacaImportada:
	.string "The lettering has faded with age.$"
