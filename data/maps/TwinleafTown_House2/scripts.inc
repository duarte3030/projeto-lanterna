TwinleafTown_House2_MapScripts::
	.byte 0

TwinleafTown_House2_EventScript_Guitarist::
	msgbox TwinleafTown_House2_Text_Guitarist, MSGBOX_NPC
	end

TwinleafTown_House2_Text_Guitarist:
	.string "I went on an adventure with some\n"
	.string "POKéMON a long time ago.\p"
	.string "It was only to SANDGEM, the next\n"
	.string "town over, though. Good times...$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TwinleafTown_House2_EventScript_Npc1::
	msgbox TwinleafTown_House2_Text_Npc1, MSGBOX_NPC
	end

TwinleafTown_House2_Text_Npc1:
	.string "Did you hear?\pThe Pokémon Professor returned\nto the next town over.\pThey say he was gone for four long\nyears.\pI wonder if he found some amazing\nPokémon while he was gone?$"

TwinleafTown_House2_EventScript_Npc2::
	msgbox TwinleafTown_House2_Text_Npc2, MSGBOX_NPC
	end

TwinleafTown_House2_Text_Npc2:
	.string "Listen, listen, {PLAYER}.\nI want a cute Pokémon!$"
