TurnbackCaveEntrance_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TurnbackCave_OnTransitionEntrada
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TurnbackCaveEntrance_EventScript_Placa1::
	msgbox TurnbackCaveEntrance_Text_Placa1, MSGBOX_SIGN
	end

TurnbackCaveEntrance_Text_Placa1:
	.string "...Past three pillars...\nto the sleeping...\p...before 30 is surpassed...$"

TurnbackCaveEntrance_EventScript_Placa2::
	msgbox TurnbackCaveEntrance_Text_Placa2, MSGBOX_SIGN
	end

TurnbackCaveEntrance_Text_Placa2:
	.string "...Past three pillars...\nto the sleeping...\p...before 30 is surpassed...$"

TurnbackCaveEntrance_EventScript_Placa3::
	msgbox TurnbackCaveEntrance_Text_Placa3, MSGBOX_SIGN
	end

TurnbackCaveEntrance_Text_Placa3:
	.string "...Past three pillars...\nto the sleeping...\p...before 30 is surpassed...$"
