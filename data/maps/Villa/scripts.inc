Villa_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Villa_OnFrameTable
	.byte 0

@ >>> B6 Sinnoh S7, onda 5 (18/08/2026): escritor que faltava de
@ VAR_SINNOH_VILLA_ESTADO = 1 >>>
@ O gatilho (5,8) pede == 1 e ninguem gravava esse valor: a cena
@ Villa_EventScript_CoordEvent_DontGoYet era inalcancavel. Na fonte o 1 sai
@ da primeira entrada no mapa, por tabela de frame, nao por cena de fora:
@ res/field/scripts/scripts_init_villa.s:9 `InitScriptGoToIfEqual
@ VAR_VILLA_STATE, 0, 41`, e o script 41 (contagem 1-based da decisao 8) e
@ `Villa_OnFrame_FirstEntry` (scripts_villa.s:1104), cuja primeira linha e
@ `SetVar VAR_VILLA_STATE, 1`. Isso e exatamente o par
@ MAP_SCRIPT_ON_FRAME_TABLE + map_script_2 deste motor.
@ NAO foi pendurado na cena do Resort (ResortArea_CoordEvent_SchoolKidM, o
@ candidato natural) porque a fonte nao poe o setvar la (la ela grava
@ VAR_RESORT_AREA_STATE = 1, que este porte ja faz) e porque a Villa tambem
@ e alcancavel pelo warp comum (18,21) do Resort, sem passar pela cena: pela
@ tabela de frame o 1 entra em qualquer caminho de entrada, como na fonte.
@ Do resto do script 41 (ShowMoney, InitLocalTextListMenu/ShowListMenu do
@ catalogo de moveis, entrega da Table de graca) nada entra: e a mecanica de
@ mobilia, fora do escopo da obra, e a decisao S7 da condutora ja deixou a
@ maquina de visitante/mobilia da Villa ADIADA.
Villa_OnFrameTable:
	map_script_2 VAR_SINNOH_VILLA_ESTADO, 0, Villa_EventScript_FirstEntry
	.2byte 0

Villa_EventScript_FirstEntry::
	setvar VAR_SINNOH_VILLA_ESTADO, 1
	end

@ <<< B6 Sinnoh S7, onda 5 <<<

@ BLOQUEADO (S7, 18/08/2026): Candice/CrasherWake/Cynthia/Fantina (e por
@ tabela, Rival/Counterpart/ProfRowan/Mom/Roark/Gardenia/Maylene/Byron/
@ Volkner/Flint) sao TODOS a mesma maquina de "visitante da Villa"
@ (VAR_RESORT_VILLA_VISITOR + enum VILLA_VISITOR_*, scripts_villa.s:52-90):
@ o motor sorteia/agenda qual lider visita, e SO ele controla quem esta
@ visivel. `grep` por VAR_RESORT_VILLA_VISITOR e VILLA_VISITOR_ em include/
@ e src/ da zero: a maquina inteira nao existe aqui (mesma familia de
@ mecanica ausente que a decisao 3 do plano ja descartou pra GTS/Poketch/
@ Pal Park). Os 4 tiles empilhados em (4,4) (dev_scripts/maquina_sinnoh.json,
@ tiles_empilhados) e os hidden_flag FLAG_HIDE_VILLA_FANTINA/_CRASHER_WAKE/
@ _CANDICE/_CYNTHIA (nenhum dos 4 esta no censo do S1, mesmo buraco do
@ Crasher Wake em Pastoria/Route227) dependem dela. Nao ha var pra alocar
@ (nem endereco de flag) sem a maquina de visitante desenhada por decisao da
@ condutora; volta ao plano (candidato a decisao "descartado" como GTS, ou a
@ ganhar desenho como os acompanhantes da decisao 5).
Villa_EventScript_CoordEvent_Candice::
	end

Villa_EventScript_CoordEvent_CrasherWake::
	end

Villa_EventScript_CoordEvent_Cynthia::
	end

Villa_EventScript_CoordEvent_Fantina::
	end

@ >>> B6 Sinnoh S7: cena da fonte, rotulo Villa_CoordEvent_DontGoYet >>>
@ School Kid M nao faz parte da maquina de visitante (ele e o vendedor fixo
@ do catalogo de moveis, sempre visivel); esta cena e so a fala de primeira
@ visita, independente. O pedido de moveis em si (Villa_OrderForm,
@ InitLocalTextListMenu/ShowListMenu) fica fora, nao e cena de historia.
@ DESVIO DA FONTE, dito, valor a valor (onda 5, 18/08/2026): a fonte deixa
@ este gatilho armado enquanto VAR_VILLA_STATE == 1 e so passa pra 2 em
@ `Villa_DeliverFreeTable` (scripts_villa.s:1477), o fim da entrega da Table
@ de graca. Sem a mecanica de mobilia portada, esse 2 nunca chegaria e a
@ fala "encomende uma Table" ficaria repetindo pra sempre, sem formulario
@ nenhum pra usar. Entao o proprio fecho grava o 2: a cena roda uma vez, com
@ o mesmo valor de corrente da fonte, e desarma sozinha. Quando a mecanica
@ de mobilia ganhar desenho, o setvar volta pra entrega, de onde a fonte o
@ tirou.
Villa_EventScript_CoordEvent_DontGoYet::
	lockall
	applymovement LOCALID_VILLA_SCHOOL_KID_M, Villa_Movement_SchoolKidMWalkOnSpotSouth
	waitmovement 0
	msgbox Villa_Text_DontGoYet, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, Villa_Movement_PlayerWalkNorth
	waitmovement 0
	setvar VAR_SINNOH_VILLA_ESTADO, 2
	releaseall
	end

Villa_Movement_SchoolKidMWalkOnSpotSouth:
	walk_in_place_down
	step_end

Villa_Movement_PlayerWalkNorth:
	walk_up
	step_end

Villa_Text_DontGoYet:
	.string "Whoa, whoa!\n"
	.string "Don't go yet!\p"
	.string "Not until you order a Table from\n"
	.string "this order form!$"

@ <<< B6 Sinnoh S7: cena da fonte <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Villa_EventScript_Placa1::
	msgbox Villa_Text_Placa1, MSGBOX_SIGN
	end

Villa_Text_Placa1:
	.string "{PLAYER} opened the order form.$"

Villa_EventScript_Placa2::
	msgbox Villa_Text_Placa2, MSGBOX_SIGN
	end

Villa_Text_Placa2:
	.string "{PLAYER} opened the order form.$"

Villa_EventScript_Placa3::
	msgbox Villa_Text_Placa3, MSGBOX_SIGN
	end

Villa_Text_Placa3:
	.string "{PLAYER} opened the order form.$"
