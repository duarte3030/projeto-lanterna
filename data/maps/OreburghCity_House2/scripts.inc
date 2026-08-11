OreburghCity_House2_MapScripts::
	.byte 0

OreburghCity_House2_EventScript_Youngster::
	msgbox OreburghCity_House2_Text_Youngster, MSGBOX_NPC
	end

OreburghCity_House2_EventScript_Pokefan::
	msgbox OreburghCity_House2_Text_Pokefan, MSGBOX_NPC
	end

OreburghCity_House2_Text_Youngster:
	.string "My PIKACHU loves running around\n"
	.string "the house. Watch your step!$"

OreburghCity_House2_Text_Pokefan:
	.string "OREBURGH doesn't get many visitors.\n"
	.string "It's nice to see a new face!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_House2_EventScript_Npc1::
	msgbox OreburghCity_House2_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_House2_Text_Npc1:
	.string "Have you ever seen or heard about\ndifferently colored Pokémon?\pFor instance, a regular PIKACHU has\na yellow body, correct?\pWell, the different-colored PIKACHU\nhas a sort of orange body.$"

OreburghCity_House2_EventScript_Npc2::
	msgbox OreburghCity_House2_Text_Npc2, MSGBOX_NPC
	end

OreburghCity_House2_Text_Npc2:
	.string "You know how Pokémon have different\nnatures like we have personalities?\pI don't think it's surprising to see\nPokémon in different colors.$"

OreburghCity_House2_EventScript_Npc3::
	msgbox OreburghCity_House2_Text_Npc3, MSGBOX_NPC
	end

OreburghCity_House2_Text_Npc3:
	.string "PIKACHU: Pikaaah!$"
