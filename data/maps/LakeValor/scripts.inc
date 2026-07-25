LakeValor_MapScripts::
	.byte 0

LakeValor_EventScript_Fisherman::
	msgbox LakeValor_Text_Fisherman, MSGBOX_NPC
	end

LakeValor_EventScript_Hiker::
	msgbox LakeValor_Text_Hiker, MSGBOX_NPC
	end

LakeValor_Text_Fisherman:
	.string "The water's deep out there.\n"
	.string "I've heard strange stories about\n"
	.string "this lake.$"

LakeValor_Text_Hiker:
	.string "Lake Valor sure is quiet this\n"
	.string "time of day.$"
