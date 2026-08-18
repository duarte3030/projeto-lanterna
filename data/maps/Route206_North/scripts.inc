Route206_North_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
Route206_North_EventScript_CoordEvent_ClearFlagForceBikingInGate::
	@ TODO S?: cena da fonte, rotulo Route206CyclingRoadNorthGate_CoordEvent_ClearFlagForceBikingInGate
	end

Route206_North_EventScript_CoordEvent_OnlyBicycles::
	@ TODO S?: cena da fonte, rotulo Route206CyclingRoadNorthGate_CoordEvent_OnlyBicycles
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route206_North_EventScript_Npc1::
	msgbox Route206_North_Text_Npc1, MSGBOX_NPC
	end

Route206_North_Text_Npc1:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"

Route206_North_EventScript_Npc2::
	msgbox Route206_North_Text_Npc2, MSGBOX_NPC
	end

Route206_North_Text_Npc2:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"
