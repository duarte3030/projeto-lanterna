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
