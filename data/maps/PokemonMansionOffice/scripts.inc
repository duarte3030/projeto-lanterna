PokemonMansionOffice_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, PokemonMansionOffice_OnTransition
	.byte 0

@ >>> B6 Sinnoh S7: cena da fonte, PokemonMansionOffice_CoordEvent_BlockStatue >>>
@ Fonte (scripts_pokemon_mansion_office.s:15): GetHour decide se o Policeman
@ bloqueia a estatua (horas 0-1 e 6-23) ou libera (2-5). `gettime` (nao
@ `gettimeofday`, que so da 3 baldes) devolve a hora exata em VAR_0x8000,
@ mesmo precedente de Route209_OnTransition (S5, GetTimeOfDay ali; aqui e
@ GetHour, comando irmao, mesma familia `gettime`).
PokemonMansionOffice_OnTransition:
	gettime
	goto_if_eq VAR_0x8000, 0, PokemonMansionOffice_SetBlockStatue
	goto_if_eq VAR_0x8000, 1, PokemonMansionOffice_SetBlockStatue
	goto_if_le VAR_0x8000, 5, PokemonMansionOffice_SetDontBlockStatue
	goto PokemonMansionOffice_SetBlockStatue
	end

PokemonMansionOffice_SetBlockStatue:
	clearflag FLAG_SINNOH_ESCONDE_POKEMON_MANSION_OFFICE_POLICEMAN
	setvar VAR_SINNOH_MANSAO_ESTATUA_ESTADO, 0
	end

PokemonMansionOffice_SetDontBlockStatue:
	setflag FLAG_SINNOH_ESCONDE_POKEMON_MANSION_OFFICE_POLICEMAN
	setvar VAR_SINNOH_MANSAO_ESTATUA_ESTADO, 1
	end

@ O coord_event so e alcancado com o Policeman ja visivel (flag clara), entao
@ o corpo e so a fala + empurrao, sem clearflag/addobject.
PokemonMansionOffice_EventScript_CoordEvent_BlockStatue::
	lockall
	applymovement LOCALID_POKEMON_MANSION_OFFICE_POLICEMAN, PokemonMansionOffice_Movement_PolicemanFaceWest
	waitmovement 0
	msgbox PokemonMansionOffice_Text_SorryDontTouchStatue, MSGBOX_DEFAULT
	applymovement OBJ_EVENT_ID_PLAYER, PokemonMansionOffice_Movement_PlayerWalkBackFromStatue
	applymovement LOCALID_POKEMON_MANSION_OFFICE_POLICEMAN, PokemonMansionOffice_Movement_PolicemanFaceSouth
	waitmovement 0
	releaseall
	end

PokemonMansionOffice_Movement_PolicemanFaceWest:
	walk_in_place_left
	step_end

PokemonMansionOffice_Movement_PolicemanFaceSouth:
	walk_in_place_down
	step_end

PokemonMansionOffice_Movement_PlayerWalkBackFromStatue:
	walk_left
	step_end

PokemonMansionOffice_Text_SorryDontTouchStatue:
	.string "I'm sorry, but I can't let you touch\n"
	.string "the statue.$"

@ <<< B6 Sinnoh S7: cena da fonte <<<

PokemonMansionOffice_EventScript_Placa1::
	msgbox PokemonMansionOffice_Text_Placa1, MSGBOX_SIGN
	end

PokemonMansionOffice_Text_Placa1:
	.string "It's a very expensive-looking book\non Pokémon.\pWould you like to read it?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PokemonMansionOffice_EventScript_Npc1::
	msgbox PokemonMansionOffice_Text_Npc1, MSGBOX_NPC
	end

PokemonMansionOffice_Text_Npc1:
	.string "Backlot: Hello, hello!\nWelcome to my opulent mansion!\pThere's a lot for me to be proud of\ninside, and outside, of this home...\pBut what makes me the most proud is\nmy trophy garden in the back!\pWhy bother traveling afar when\nPokémon are attracted by my garden?\pThey come to me in hopes of seeing\nthe garden!\pYou're welcome to join them and\nmarvel at my garden!$"

PokemonMansionOffice_EventScript_Placa2::
	msgbox PokemonMansionOffice_Text_Placa2, MSGBOX_SIGN
	end

PokemonMansionOffice_Text_Placa2:
	.string "It's a very expensive-looking Pokémon\nstatue...\p...!\nYou got fingerprints on it...$"
