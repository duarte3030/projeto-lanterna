Route218_West_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
Route218_West_EventScript_CoordEvent_ScientistM::
	@ TODO S6: cena da fonte, rotulo Route218GateToCanalaveCity_CoordEvent_ScientistM
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route218_West_EventScript_Npc1::
	msgbox Route218_West_Text_Npc1, MSGBOX_NPC
	end

Route218_West_Text_Npc1:
	.string "Boy...\nI sure am thirsty...$"
