FootstepHouse_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

FootstepHouse_EventScript_Npc1::
	bufferleadmonspeciesname STR_VAR_1
	msgbox FootstepHouse_Text_Npc1, MSGBOX_NPC
	end

FootstepHouse_Text_Npc1:
	.string "Dr. Footstep: Pokémon are quite easy\nfor me to read.\pI need only to see their footprints,\nand their innermost thoughts are\prevealed to me!\pOh?\nYou are skeptical of my claim?\pThen, let your {STR_VAR_1} walk\nin front of me, right here.\pFrom its footprints, I will determine\nhow it feels about you.$"
