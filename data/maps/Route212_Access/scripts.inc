Route212_Access_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route212_Access_EventScript_Npc1::
	msgbox Route212_Access_Text_Npc1, MSGBOX_NPC
	end

Route212_Access_Text_Npc1:
	.string "I traveled a long way to take part\nin these Contests.$"

Route212_Access_EventScript_Npc2::
	msgbox Route212_Access_Text_Npc2, MSGBOX_NPC
	end

Route212_Access_Text_Npc2:
	.string "I've given my Pokémon lots of Poffins.\pI'm confident that we'll win our share\nof Contests.$"
