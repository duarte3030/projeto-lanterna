ContestHallLobby_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

ContestHallLobby_EventScript_Npc1::
	msgbox ContestHallLobby_Text_Npc1, MSGBOX_NPC
	end

ContestHallLobby_Text_Npc1:
	.string "A Pokémon fed Poffins does\nbetter in Visual Evaluations.\pI'd better learn how to cook\ndelicious Poffins at the Poffin House!$"

ContestHallLobby_EventScript_Npc2::
	msgbox ContestHallLobby_Text_Npc2, MSGBOX_NPC
	end

ContestHallLobby_Text_Npc2:
	.string "A Contest has three parts: Visual!\nDance! And Acting!\pThe Contestants get graded in those\ncategories, dohoho!$"

ContestHallLobby_EventScript_Npc3::
	msgbox ContestHallLobby_Text_Npc3, MSGBOX_NPC
	end

ContestHallLobby_Text_Npc3:
	.string "They put up photos of the winners!$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
ContestHallLobby_EventScript_PortaFechada::
	msgbox ContestHallLobby_Text_PortaFechada, MSGBOX_SIGN
	end

ContestHallLobby_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
