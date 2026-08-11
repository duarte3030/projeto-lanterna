SurvivalAreaNorthHouse_MapScripts::
	.byte 0

SurvivalAreaNorthHouse_EventScript_Npc1::
	msgbox SurvivalAreaNorthHouse_Text_Npc1, MSGBOX_NPC
	end

SurvivalAreaNorthHouse_Text_Npc1:
	.string "If you'd share your Shards with me,\nI can teach some moves.\pWould you like me to teach a move?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SurvivalAreaNorthHouse_EventScript_Npc1::
	msgbox SurvivalAreaNorthHouse_Text_Npc1, MSGBOX_NPC
	end

SurvivalAreaNorthHouse_Text_Npc1:
	.string "I started living here where no one\ncould reach me without using Rock Climb.\pI came because I got sick and tired of\nseeing people.\pBut when I stopped seeing people,\nI began looking forward to visitors.\pWhere one lives can change people and\nPokémon, that's what I'm saying.$"

SurvivalAreaNorthHouse_EventScript_Placa2::
	msgbox SurvivalAreaNorthHouse_Text_Placa2, MSGBOX_SIGN
	end

SurvivalAreaNorthHouse_Text_Placa2:
	.string "Red Shards emphasize power.\nBlue Shards are for special effects.\pYellow Shards are for status problems.\pRed Shards are what I like!$"
