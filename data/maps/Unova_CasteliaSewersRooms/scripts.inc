@ CasteliaSewersRooms do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CasteliaSewersRooms_MapScripts::
	.byte 0

Unova_CasteliaSewersRooms_EventScript_Placa0::
	msgbox Unova_CasteliaSewersRooms_Text_CasteliaSewersSwitchText, MSGBOX_SIGN
	end

Unova_CasteliaSewersRooms_EventScript_Placa1::
	msgbox Unova_CasteliaSewersRooms_Text_CasteliaSewersSwitchText, MSGBOX_SIGN
	end

Unova_CasteliaSewersRooms_EventScript_Placa2::
	msgbox Unova_CasteliaSewersRooms_Text_CasteliaSewersSwitchText, MSGBOX_SIGN
	end

Unova_CasteliaSewersRooms_EventScript_Npc2::
	msgbox Unova_CasteliaSewersRooms_Text_WorkerCasteliaSewersRoomsSeenText, MSGBOX_NPC
	end

Unova_CasteliaSewersRooms_EventScript_Npc3::
	msgbox Unova_CasteliaSewersRooms_Text_JanitorCasteliaSewersRoomsSeenText, MSGBOX_NPC
	end


Unova_CasteliaSewersRooms_Text_CasteliaSewersSwitchText::
	.string "There's a switch."
	.string "\nPress it?$"

Unova_CasteliaSewersRooms_Text_WorkerCasteliaSewersRoomsSeenText::
	.string "Whoooa!$"

Unova_CasteliaSewersRooms_Text_JanitorCasteliaSewersRoomsSeenText::
	.string "Do you know how to"
	.string "\nget through the"
	.string "\lsewers?$"
