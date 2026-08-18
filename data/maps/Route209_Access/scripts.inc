Route209_Access_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ S5: rotulo da fonte Route209GateToHearthomeCity_CoordEvent_Rival. O
@ gatilho so dispara com VAR_SINNOH_R209_PORTAO_HEARTHOME==1, e quem grava
@ esse 1 (e revela LOCALID_ROUTE209_ACCESS_RIVAL, ClearFlag na fonte) e o
@ script de vitoria do lider de Hearthome (scripts_hearthome_city_gym_
@ leader_room.s / _dp_..., os dois arquivos), fora do meu escopo (decisao 2
@ do Gui: batalha de ginasio/lider fica pro fim).
@ BLOQUEADO: TRAINER_SINNOH_RIVAL_ROUTE_209_TURTWIG / _CHIMCHAR / _PIPLUP
@ nao existem em opponents.h. O objeto do rival ja foi plantado (escondido
@ por FLAG_SINNOH_ESCONDE_HEARTHOME_CITY_ROUTE_209_GATE_RIVAL, setflag em
@ new_game.inc), pronto para quando o executor de treinadores desta onda
@ criar os tres ids e o polimento do ginasio ligar o ClearFlag + SetVar.
Route209_Access_EventScript_CoordEvent_Rival::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route209_Access_EventScript_Npc1::
	msgbox Route209_Access_Text_Npc1, MSGBOX_NPC
	end

Route209_Access_Text_Npc1:
	.string "There's a wrecked stone pillar up\nahead.\pI wonder what it is?\nIt's got me very curious.$"
