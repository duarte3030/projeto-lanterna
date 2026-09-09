@ Battle Tower de Olivine, na Route 40. Decisão 30 do Gui, revista por ele:
@ nada de Frontier de HGSS. O Battle Frontier de Hoenn continua sendo o de
@ Hoenn, e Johto ganha UM prédio, do tamanho da torre simples do Pokémon
@ Crystal: um atendente, uma série de sete lutas, e a recompensa do motor.
@
@ O MOTOR NÃO FOI REIMPLEMENTADO, foi APONTADO PARA CÁ. Tudo que este arquivo
@ faz é chamar os rótulos do saguão de Hoenn, que são o motor de Battle Tower
@ do Emerald (`src/battle_tower.c`, `src/frontier_util.c`): a série já é de
@ SETE lutas (`case 7, ..._WarpToLobbyWon` em
@ `data/maps/BattleFrontier_BattleTowerBattleRoom/scripts.inc`), a recompensa
@ já é fita mais Battle Points (`tower_giveribbons` e `frontier_givepoints`),
@ e o elevador, o corredor e a sala de batalha são os mesmos, compartilhados.
@
@ O QUE O MOTOR JÁ SABIA FAZER SOZINHO, e por isso não custou save nenhuma:
@ `InitTowerChallenge` (`src/battle_tower.c:722`) grava `dynamicWarp` com o
@ mapa E O TILE em que o jogador estava ao começar o desafio, ou seja o saguão
@ de onde ele entrou. É desse campo que sai o ponto de "Continuar" de quem
@ salva no meio da série (`SetContinueGameWarpStatusToDynamicWarp`, chamado por
@ `SaveGameFrontier` em `src/frontier_util.c:2534`). Logo o motor JÁ voltava
@ para o saguão certo em tudo, menos numa linha.
@
@ A LINHA QUE FALTAVA era o `warp` cravado no fim da série, em
@ `BattleFrontier_BattleTowerBattleRoom_EventScript_WarpToLobby`, que mandava
@ para o saguão de Hoenn e ponto. Ela passou a perguntar por
@ `FLAG_TORRE_OLIVINE_EM_DESAFIO`, que este atendente acende e os quatro
@ atendentes de Hoenn apagam. A flag é apelido de `FLAG_UNUSED_0x2180`, então
@ custa ZERO byte de save: o vetor de flags já tinha o bit, sem dono.
@
@ SÓ SINGLES, de propósito. Duplas, multi e multi por cabo continuam existindo
@ e continuam SÓ em Hoenn: a torre de Crystal era uma fila de sete lutas um
@ contra um, e cada modo a mais aqui seria um caminho de volta a mais para
@ testar sem emulador.

Route40_BattleTower_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Route40_BattleTower_OnFrame
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, Route40_BattleTower_OnWarp
	.byte 0

Route40_BattleTower_OnWarp:
	map_script_2 VAR_TEMP_1, 0, Route40_BattleTower_EventScript_PlayerFaceNorth
	.2byte 0

Route40_BattleTower_EventScript_PlayerFaceNorth::
	setvar VAR_TEMP_1, 1
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

@ A tabela de status é a MESMA do saguão de Hoenn, rótulo por rótulo: é ela que
@ paga a fita e os Battle Points ao voltar da sétima luta, que reata o desafio
@ pausado e que trata o "saiu sem salvar".
Route40_BattleTower_OnFrame:
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, 0, BattleFrontier_BattleTowerLobby_EventScript_GetChallengeStatus
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_SAVING, BattleFrontier_BattleTowerLobby_EventScript_QuitWithoutSaving
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_PAUSED, BattleFrontier_BattleTowerLobby_EventScript_ResumeChallenge
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_WON, BattleFrontier_BattleTowerLobby_EventScript_WonChallenge
	map_script_2 VAR_TEMP_CHALLENGE_STATUS, CHALLENGE_STATUS_LOST, BattleFrontier_BattleTowerLobby_EventScript_LostChallenge
	.2byte 0

@ O atendente é o objeto de ÍNDICE 0 do mapa, logo o local id dele é 1, que é o
@ mesmo número de `LOCALID_TOWER_ATTENDANT_SINGLES`. Isso não é coincidência
@ bonita: `..._EventScript_SetAttendantTalkedTo` grava esse número em
@ `VAR_LAST_TALKED` antes de mandar o atendente andar até o elevador, e é por
@ ele que o `applymovement` acha quem tem de andar. Mexer na ordem dos objetos
@ deste mapa quebra a caminhada.
Route40_BattleTower_EventScript_Attendant::
	lock
	faceplayer
	setvar VAR_FRONTIER_FACILITY, FRONTIER_FACILITY_TOWER
	setflag FLAG_TORRE_OLIVINE_EM_DESAFIO
	special SavePlayerParty
	msgbox Route40_BattleTower_Text_Welcome, MSGBOX_DEFAULT
	goto BattleFrontier_BattleTowerLobby_EventScript_AskEnterSinglesChallenge
	end

@ O PREMIO DA SERIE, no estilo do Pokemon Crystal (item 8 da fila de bugs do
@ cartucho 1). La a torre pagava um item a cada serie de sete lutas, e o item
@ girava; aqui a roda tem tres casas, Rare Candy, PP Up e Elixir, guardadas em
@ `VAR_TORRE_OLIVINE_PREMIO`, apelido de `VAR_UNUSED_0x41D7`, que custa ZERO
@ byte de save porque o vetor de vars ja tinha a vaga sem dono.
@
@ Ele e CHAMADO de dentro do saguao de Hoenn, logo depois do
@ `frontier_givepoints`, por uma linha unica de `call_if_set`. Nao ha motor novo
@ e nao ha serie propria: a serie de sete e a mesma do Emerald, os Battle Points
@ continuam sendo pagos pelo mesmo `frontier_givepoints`, e o que Johto ganha e
@ o item por cima.
@
@ A roda so gira quando o item ENTRA na mochila. `giveitem` devolve FALSE com a
@ mochila cheia, e nesse caso o jogador ouve que nao ha espaco e continua com o
@ mesmo premio esperando na proxima serie, em vez de perder a vez em silencio.
Route40_BattleTower_EventScript_PagaPremioDaSerie::
	msgbox Route40_BattleTower_Text_PremioDaSerie, MSGBOX_DEFAULT
	compare VAR_TORRE_OLIVINE_PREMIO, 1
	goto_if_eq Route40_BattleTower_EventScript_PremioPPUp
	compare VAR_TORRE_OLIVINE_PREMIO, 2
	goto_if_eq Route40_BattleTower_EventScript_PremioElixir
	giveitem ITEM_RARE_CANDY
	goto_if_eq VAR_RESULT, FALSE, Route40_BattleTower_EventScript_PremioSemEspaco
	setvar VAR_TORRE_OLIVINE_PREMIO, 1
	return

Route40_BattleTower_EventScript_PremioPPUp::
	giveitem ITEM_PP_UP
	goto_if_eq VAR_RESULT, FALSE, Route40_BattleTower_EventScript_PremioSemEspaco
	setvar VAR_TORRE_OLIVINE_PREMIO, 2
	return

Route40_BattleTower_EventScript_PremioElixir::
	giveitem ITEM_ELIXIR
	goto_if_eq VAR_RESULT, FALSE, Route40_BattleTower_EventScript_PremioSemEspaco
	setvar VAR_TORRE_OLIVINE_PREMIO, 0
	return

Route40_BattleTower_EventScript_PremioSemEspaco::
	return

Route40_BattleTower_EventScript_RulesBoard::
	msgbox Route40_BattleTower_Text_RulesBoard, MSGBOX_SIGN
	end

Route40_BattleTower_EventScript_Sailor::
	msgbox Route40_BattleTower_Text_Sailor, MSGBOX_NPC
	end

Route40_BattleTower_EventScript_Girl::
	msgbox Route40_BattleTower_Text_Girl, MSGBOX_NPC
	end

Route40_BattleTower_Text_PremioDaSerie:
	.string "And the TOWER always thanks a seven\n"
	.string "battle streak with something useful.$"

Route40_BattleTower_Text_Welcome:
	.string "Welcome to the BATTLE TOWER of\n"
	.string "OLIVINE.\p"
	.string "Seven TRAINERS are waiting upstairs.\n"
	.string "Beat all seven in a row and the\l"
	.string "record is yours.\p"
	.string "Lose once and the streak is over.$"

Route40_BattleTower_Text_RulesBoard:
	.string "BATTLE TOWER RULES\p"
	.string "Three POKéMON. Seven battles in a\n"
	.string "row. No items from the BAG.\p"
	.string "Every POKéMON must be a different\n"
	.string "kind, and hold a different item.$"

Route40_BattleTower_Text_Sailor:
	.string "The tower was built out here so the\n"
	.string "ships from OLIVINE could see it.\p"
	.string "Seven wins and they sound the horn\n"
	.string "at the port for you.$"

Route40_BattleTower_Text_Girl:
	.string "The BATTLE FRONTIER over in HOENN\n"
	.string "has seven whole facilities.\p"
	.string "We have one tower, and it is enough\n"
	.string "to keep me busy.$"
