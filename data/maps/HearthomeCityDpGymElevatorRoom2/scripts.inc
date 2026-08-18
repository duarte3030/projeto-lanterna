HearthomeCityDpGymElevatorRoom2_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
HearthomeCityDpGymElevatorRoom2_EventScript_CoordEvent_MoveLift::
	@ TODO S?: cena da fonte, rotulo HearthomeCityDPGymElevatorRoom2_CoordEvent_MoveLift
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

HearthomeCityDpGymElevatorRoom2_EventScript_Placa1::
	msgbox HearthomeCityDpGymElevatorRoom2_Text_Placa1, MSGBOX_SIGN
	end

HearthomeCityDpGymElevatorRoom2_Text_Placa1:
	.string "Question: The first room's answer?\nAnswer: {LEFT_ARROW}2 {UP_ARROW}16 {RIGHT_ARROW}15$"

HearthomeCityDpGymElevatorRoom2_EventScript_Placa2::
	msgbox HearthomeCityDpGymElevatorRoom2_Text_Placa2, MSGBOX_SIGN
	end

HearthomeCityDpGymElevatorRoom2_Text_Placa2:
	.string "Correct!\nCongratulations!$"
