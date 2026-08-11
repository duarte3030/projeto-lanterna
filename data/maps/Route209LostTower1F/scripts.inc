Route209LostTower1F_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route209LostTower1F_EventScript_Npc1::
	msgbox Route209LostTower1F_Text_Npc1, MSGBOX_NPC
	end

Route209LostTower1F_Text_Npc1:
	.string "This is where spirits rest.\nPlease be quiet and respectful.$"

Route209LostTower1F_EventScript_Npc2::
	msgbox Route209LostTower1F_Text_Npc2, MSGBOX_NPC
	end

Route209LostTower1F_Text_Npc2:
	.string "This is the Lost Tower.\pThere is a persistent fog that thickens\nthe higher you climb.\pIf you can't use the hidden move Defog\nand you have no business here, there\pis no need to go up.$"
