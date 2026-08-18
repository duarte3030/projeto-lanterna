CelesticTownNorthHouse_MapScripts::
	.byte 0

CelesticTownNorthHouse_EventScript_Npc1::
	msgbox CelesticTownNorthHouse_Text_Npc1, MSGBOX_NPC
	end

CelesticTownNorthHouse_Text_Npc1:
	.string "Where are you from?\p...\pHm, Twinleaf Town, you say.\nIsn't that close to Lake Verity?\pThat lake is said to be home to MESPRIT,\n'The Being of Emotion.'\pThat Pokémon may well be watching\nover you.\pWould you like to know more about\nMESPRIT?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CelesticTownNorthHouse_EventScript_Npc2::
	msgbox CelesticTownNorthHouse_Text_Npc2, MSGBOX_NPC
	end

CelesticTownNorthHouse_Text_Npc2:
	.string "My big sister is studying the myths\nof Sinnoh.\pShe wants to know how people and\nPokémon interacted in the days of\pmyths.\pWere things different back then?\nOr were they the same as now?\pShe says that's the focus of her\nresearch.$"

CelesticTownNorthHouse_EventScript_Placa2::
	msgbox CelesticTownNorthHouse_Text_Placa2, MSGBOX_SIGN
	end

CelesticTownNorthHouse_Text_Placa2:
	.string "It's hard to tell for sure, but it's\nprobably an invaluable scroll.$"

@ >>> B6 Sinnoh S5: grupo de hidden_flag (dev_scripts/maquina_sinnoh.json) >>>
@ Objeto plantado pelo executor S5. Fonte comeca escondida (SetFlag em
@ scripts_init_new_game.s, ver data/scripts/new_game.inc) e so aparece
@ depois de CelesticTownCave_DefeatedCyrus (ClearFlag), cena das ruinas de
@ Celestic que ainda nao existe neste projeto (mapa nao casado). Fica
@ escondida ate essa cena ser construida por uma leva futura.
@ Os ramos FLAG_GAME_COMPLETED e FLAG_FIRST_ARRIVAL_CANALAVE_CITY da fonte
@ nao tem par aqui (Canalave fora do meu escopo; o ramo pos-liga precisava
@ de FLAG_UNLOCKED_DIALGA_PALKIA_SPEAR_PILLAR, mecanica do climax de S6,
@ fora da tabela do plano). Regra dura: flag/var nova NENHUMA. Fica so a
@ fala padrao (CelesticTownNorthHouse_Text_UsingSurfGoPlaces da fonte).
CelesticTownNorthHouse_EventScript_Elder::
	lock
	faceplayer
	msgbox CelesticTownNorthHouse_Text_UsingSurfGoPlaces, MSGBOX_DEFAULT
	release
	end

CelesticTownNorthHouse_Text_UsingSurfGoPlaces:
	.string "Using the move Surf, you'll be able to\ngo to places that were inaccessible.\pYou'd be surprised where you can go.$"
@ <<< B6 Sinnoh S5: grupo de hidden_flag <<<
