IronRuins_MapScripts::
	.byte 0

@ BLOQUEADO (S7, 18/08/2026), os 7 pontos deste santuario. A fonte
@ (scripts_iceberg_ruins.s e irmas) trava a ativacao de cada ponto em
@ VAR_ICEBERG_RUINS_STATE/VAR_IRON_RUINS_STATE/VAR_ROCK_PEAK_RUINS_STATE
@ (nao e um dos VAR_MAP_LOCAL, e nao esta na tabela de 49 vars do plano; e
@ var interna que so aparece durante o porte, decisao "volta ao plano, entra
@ na tabela em append" da secao de vars) e no special ActivateRegiRuinsDot
@ (com CheckPartyHasFatefulEncounterRegigigas e StartLegendaryBattle pro
@ Regi em si), nenhum dos dois existe neste motor (`grep` em include/ e
@ src/ confirma). "Specials inexistentes descartados com comentario": os 7
@ `SetVar VAR_TEMP_N, 1` sao literais e portaveis, mas sozinhos nao fazem
@ nada sem o special que conta quantos pontos foram ativados e libera a
@ estatua; escrever so o SetVar era esqueleto vazio (ponytail: nao
@ scaffolding sem consumidor). Volta ao plano: precisa de endereco de var
@ nova da condutora e decisao sobre a mecanica do Regi (capturavel? so
@ decorativo?) antes de qualquer cena aqui.
IronRuins_EventScript_DotEast::
	end

IronRuins_EventScript_DotMiddle::
	end

IronRuins_EventScript_DotNorthEast::
	end

IronRuins_EventScript_DotNorthWest::
	end

IronRuins_EventScript_DotSouthEast::
	end

IronRuins_EventScript_DotSouthWest::
	end

IronRuins_EventScript_DotWest::
	end

IronRuins_EventScript_Placa1::
	msgbox IronRuins_Text_Placa1, MSGBOX_SIGN
	end

IronRuins_Text_Placa1:
	.string "Something changed in the air...\pAn indescribable power is emanating\nfrom the Pokémon statue...$"

IronRuins_EventScript_Placa2::
	msgbox IronRuins_Text_Placa2, MSGBOX_SIGN
	end

IronRuins_Text_Placa2:
	.string "Something changed in the air...\pAn indescribable power is emanating\nfrom the Pokémon statue...$"

IronRuins_EventScript_Placa3::
	msgbox IronRuins_Text_Placa3, MSGBOX_SIGN
	end

IronRuins_Text_Placa3:
	.string "Something changed in the air...\pAn indescribable power is emanating\nfrom the Pokémon statue...$"
