Route206_South_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S4: cena da fonte >>>
@ Mesma mecanica de Route206_North (portao gemeo da Cycling Road): a fonte
@ forca bicicleta com FLAG_FORCE_BIKING_IN_GATE, que nao existe neste motor.
@ Descartado sem substituto, decisao 3. VAR_TEMP_2 so marca passagem.
Route206_South_EventScript_CoordEvent_OnlyCyclists::
	lockall
	msgbox Route206_South_Text_CyclingRoadFlavor, MSGBOX_SIGN
	setvar VAR_TEMP_2, 1
	releaseall
	end

Route206_South_EventScript_CoordEvent_ClearFlagForceBikingInGate::
	setvar VAR_TEMP_2, 0
	end

Route206_South_Text_CyclingRoadFlavor:
	.string "CYCLING ROAD\n"
	.string "Built for speed on two wheels.$"

@ <<< B6 Sinnoh S4: cena da fonte <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route206_South_EventScript_Npc1::
	msgbox Route206_South_Text_Npc1, MSGBOX_NPC
	end

Route206_South_Text_Npc1:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"

Route206_South_EventScript_Npc2::
	msgbox Route206_South_Text_Npc2, MSGBOX_NPC
	end

Route206_South_Text_Npc2:
	.string "Learn how to shift gears, and you'll\nbe able to ride anywhere.$"

Route206_South_EventScript_Npc3::
	msgbox Route206_South_Text_Npc3, MSGBOX_NPC
	end

Route206_South_Text_Npc3:
	.string "What's a Bicycle without this?\pYou've got to have a Flag!\nIt's a Pokémon Accessory!$"
