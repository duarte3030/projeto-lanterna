EverGrandeCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, EverGrandeCity_OnTransition
	.byte 0

EverGrandeCity_OnTransition:
	call_if_set FLAG_SYS_WEATHER_CTRL, Common_EventScript_SetAbnormalWeather
	end

EverGrandeCity_EventScript_VictoryRoadSign::
	msgbox EverGrandeCity_Text_EnteringVictoryRoad, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_CitySign::
	msgbox EverGrandeCity_Text_CitySign, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_PokemonLeagueSign::
	msgbox EverGrandeCity_Text_EnteringPokemonLeague, MSGBOX_SIGN
	end

EverGrandeCity_EventScript_SetVisitedEverGrande::
	setflag FLAG_VISITED_EVER_GRANDE_CITY
	setvar VAR_TEMP_1, 1
	end

EverGrandeCity_Text_EnteringVictoryRoad:
	.string "ENTERING VICTORY ROAD$"

EverGrandeCity_Text_EnteringPokemonLeague:
	.string "ENTERING POKéMON LEAGUE\n"
	.string "CENTER GATE$"

EverGrandeCity_Text_CitySign:
	.string "EVER GRANDE CITY\p"
	.string "“The paradise of flowers, the sea,\n"
	.string "and POKéMON.”$"

@ >>> Povoamento: os 10 NPCs por cidade (dev_scripts/povoa_cidades.py) >>>
@ Lei do Gui de 07/09/2026: toda cidade do cartucho 1 tem pelo menos 10 NPCs.
@ Bloco GERADO. Para mudar fala ou posicao, edite dev_scripts/povoa_cidades.json
@ e rode `python3 dev_scripts/povoa_cidades.py --aplica`.

EverGrandeCity_EventScript_Povoa1::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa1, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa1:
	.string "VICTORY ROAD is the only way up.\nThere is no shortcut.$"

EverGrandeCity_EventScript_Povoa2::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa2, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa2:
	.string "I have healed here four times\ntoday. I am not going in yet.$"

EverGrandeCity_EventScript_Povoa3::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa3, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa3:
	.string "A city with no houses, only a\ngate and a mountain.$"

EverGrandeCity_EventScript_Povoa4::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa4, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa4:
	.string "The POKéMON LEAGUE takes eight\nbadges and nothing less.$"

EverGrandeCity_EventScript_Povoa5::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa5, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa5:
	.string "ROUTE 128 west is deep water.\nYou surfed it to get here.$"

EverGrandeCity_EventScript_Povoa6::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa6, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa6:
	.string "The cliffs here are the tallest\nin HOENN. Look up.$"

EverGrandeCity_EventScript_Povoa7::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa7, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa7:
	.string "Everyone who reaches this beach\nhas a story worth hearing.$"

EverGrandeCity_EventScript_Povoa8::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa8, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa8:
	.string "Rest before the road.\nInside, there is nowhere to sit.$"

EverGrandeCity_EventScript_Povoa9::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa9, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa9:
	.string "My sister went up this morning.\nI am waiting right here.$"

EverGrandeCity_EventScript_Povoa10::
	lock
	faceplayer
	msgbox EverGrandeCity_Text_Povoa10, MSGBOX_DEFAULT
	release
	end

EverGrandeCity_Text_Povoa10:
	.string "I fish this shore and watch\nchampions walk past. Good life.$"

@ <<< Povoamento: fim do bloco gerado <<<
