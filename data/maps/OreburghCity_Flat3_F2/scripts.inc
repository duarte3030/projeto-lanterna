OreburghCity_Flat3_F2_MapScripts::
	.byte 0

OreburghCity_Flat3_F2_EventScript_Worker::
	msgbox OreburghCity_Flat3_F2_Text_Worker, MSGBOX_NPC
	end

OreburghCity_Flat3_F2_EventScript_SchoolKid::
	msgbox OreburghCity_Flat3_F2_Text_SchoolKid, MSGBOX_NPC
	end

OreburghCity_Flat3_F2_EventScript_Lass::
	msgbox OreburghCity_Flat3_F2_Text_Lass, MSGBOX_NPC
	end

OreburghCity_Flat3_F2_Text_Worker:
	.string "Long shift down in the MINE today.\n"
	.string "Nothing beats coming home to rest.$"

OreburghCity_Flat3_F2_Text_SchoolKid:
	.string "I can see the whole town from my\n"
	.string "window up here!$"

OreburghCity_Flat3_F2_Text_Lass:
	.string "A DUSK BALL works best if you use\n"
	.string "it at night or inside a cave.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_Flat3_F2_EventScript_Npc1::
	msgbox OreburghCity_Flat3_F2_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_Flat3_F2_Text_Npc1:
	.string "Wow... Your Pokémon's eyes are\ntwinkling brightly!\pSeeing that makes me happy!\nHere, I want you to have this!$"

OreburghCity_Flat3_F2_EventScript_Npc2::
	msgbox OreburghCity_Flat3_F2_Text_Npc2, MSGBOX_NPC
	end

OreburghCity_Flat3_F2_Text_Npc2:
	.string "The Oreburgh Mine is operated\nwith the utmost care.\pWe avoid causing any damage to\nthe natural habitats of Pokémon.$"

OreburghCity_Flat3_F2_EventScript_Npc3::
	msgbox OreburghCity_Flat3_F2_Text_Npc3, MSGBOX_NPC
	end

OreburghCity_Flat3_F2_Text_Npc3:
	.string "Coal is carried out of Oreburgh Mine on\na fully automated system.\pMachines do all the work automatically.\nSo, it's all very easy.$"
