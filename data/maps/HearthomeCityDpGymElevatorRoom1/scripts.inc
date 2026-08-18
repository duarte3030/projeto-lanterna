HearthomeCityDpGymElevatorRoom1_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ S5: rotulo da fonte HearthomeCityDPGymElevatorRoom1_CoordEvent_MoveLift.
@ Corpo da fonte e SO `MoveHearthomeGymDPLift` (special nativa em C que move
@ a plataforma giratoria do ginasio eletrico de Hearthome). Nao existe aqui
@ (grep vazio em src/, include/, data/specials.inc) e escrever a mecanica da
@ plataforma e codigo C fora de map.json/scripts.inc, fora do que este
@ executor pode tocar. Descartada sem substituto, regua "specials de
@ mecanica inexistente" do plano; o mesmo vale para a outra sala e para o
@ OnTransition `InitPersistedMapFeaturesForHearthomeGym` (tambem nativo,
@ tambem ausente, mas nao esta na fila como TODO).
HearthomeCityDpGymElevatorRoom1_EventScript_CoordEvent_MoveLift::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

HearthomeCityDpGymElevatorRoom1_EventScript_Placa1::
	msgbox HearthomeCityDpGymElevatorRoom1_Text_Placa1, MSGBOX_SIGN
	end

HearthomeCityDpGymElevatorRoom1_Text_Placa1:
	.string "Question: 3 times 13 is?\nAnswer: {LEFT_ARROW}39 {UP_ARROW}93 {RIGHT_ARROW}33$"

HearthomeCityDpGymElevatorRoom1_EventScript_Placa2::
	msgbox HearthomeCityDpGymElevatorRoom1_Text_Placa2, MSGBOX_SIGN
	end

HearthomeCityDpGymElevatorRoom1_Text_Placa2:
	.string "Correct!\nCongratulations!$"
