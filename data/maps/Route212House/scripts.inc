Route212House_MapScripts::
	.byte 0

Route212House_EventScript_Npc1::
	msgbox Route212House_Text_Npc1, MSGBOX_NPC
	end

Route212House_Text_Npc1:
	.string "If you'd share your shards with me,\nI can teach your Pokémon some moves.\pWould you like me to teach a move?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route212House_EventScript_Npc3::
	msgbox Route212House_Text_Npc3, MSGBOX_NPC
	end

Route212House_Text_Npc3:
	.string "My daddy likes Blue Shards.\pThere are other people who like shards\nin Sinnoh.\pOne person likes Red Shards.\nAnother collects Yellow Shards.$"

Route212House_EventScript_Npc2::
	msgbox Route212House_Text_Npc2, MSGBOX_NPC
	end

Route212House_Text_Npc2:
	.string "My daddy collects shards.\pIf you find any, like in the\nUnderground, please bring them to us.$"

Route212House_EventScript_Placa3::
	msgbox Route212House_Text_Placa3, MSGBOX_SIGN
	end

Route212House_Text_Placa3:
	.string "Red Shards emphasize power.\nBlue Shards are for special effects.\pYellow Shards are for status problems.\pBlue Shards are the ones for me!$"
