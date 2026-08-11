SolaceonTownNorthHouse_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SolaceonTownNorthHouse_EventScript_Npc1::
	msgbox SolaceonTownNorthHouse_Text_Npc1, MSGBOX_NPC
	end

SolaceonTownNorthHouse_Text_Npc1:
	.string "Every so often, an Egg will be found\nat the Pokémon Day Care.\pAnd they're found without anyone\nknowing how they got there.\pIt's an enduring mystery.\nIs someone leaving them there?$"

SolaceonTownNorthHouse_EventScript_Npc2::
	msgbox SolaceonTownNorthHouse_Text_Npc2, MSGBOX_NPC
	end

SolaceonTownNorthHouse_Text_Npc2:
	.string "They say no one has ever seen\na Pokémon actually lay an Egg.\pSo, it hasn't been proven that\nPokémon actually lay Eggs.$"
