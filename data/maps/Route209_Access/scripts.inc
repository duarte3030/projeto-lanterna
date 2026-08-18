Route209_Access_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
Route209_Access_EventScript_CoordEvent_Rival::
	@ TODO S5: cena da fonte, rotulo Route209GateToHearthomeCity_CoordEvent_Rival
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route209_Access_EventScript_Npc1::
	msgbox Route209_Access_Text_Npc1, MSGBOX_NPC
	end

Route209_Access_Text_Npc1:
	.string "There's a wrecked stone pillar up\nahead.\pI wonder what it is?\nIt's got me very curious.$"
