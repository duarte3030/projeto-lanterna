Villa_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
Villa_EventScript_CoordEvent_Candice::
	@ TODO S?: cena da fonte, rotulo Villa_CoordEvent_Candice
	end

Villa_EventScript_CoordEvent_CrasherWake::
	@ TODO S?: cena da fonte, rotulo Villa_CoordEvent_CrasherWake
	end

Villa_EventScript_CoordEvent_Cynthia::
	@ TODO S?: cena da fonte, rotulo Villa_CoordEvent_Cynthia
	end

Villa_EventScript_CoordEvent_DontGoYet::
	@ TODO S7: cena da fonte, rotulo Villa_CoordEvent_DontGoYet
	end

Villa_EventScript_CoordEvent_Fantina::
	@ TODO S?: cena da fonte, rotulo Villa_CoordEvent_Fantina
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

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
