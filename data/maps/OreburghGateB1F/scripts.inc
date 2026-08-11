OreburghGateB1F_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghGateB1F_EventScript_Npc1::
	msgbox OreburghGateB1F_Text_Npc1, MSGBOX_NPC
	end

OreburghGateB1F_Text_Npc1:
	.string "Do you see those bumps on the\nground?\pIt feels awesome taking those fast\non a Bicycle.$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

OreburghGateB1F_EventScript_VeteranGrant::
	trainerbattle_single TRAINER_SINNOH_VETERAN_GRANT, OreburghGateB1F_Text_VeteranGrantIntro, OreburghGateB1F_Text_VeteranGrantDefeat
	msgbox OreburghGateB1F_Text_VeteranGrantPost, MSGBOX_AUTOCLOSE
	end

OreburghGateB1F_Text_VeteranGrantIntro:
	.string "I'm a Veteran, yes, but don't you\ndare treat me like a senior citizen!$"

OreburghGateB1F_Text_VeteranGrantDefeat:
	.string "Grrr...\nSo young, and yet so talented!$"

OreburghGateB1F_Text_VeteranGrantPost:
	.string "I'll always remain young at heart.\nNever let them say you're too old!$"
