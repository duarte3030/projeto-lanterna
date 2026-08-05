@ Pokecenter2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Pokecenter2F_MapScripts::
	.byte 0

Unova_Pokecenter2F_EventScript_Npc0::
	msgbox Unova_Pokecenter2F_Text_Text_TradeReceptionistIntro, MSGBOX_NPC
	end

Unova_Pokecenter2F_EventScript_Npc1::
	msgbox Unova_Pokecenter2F_Text_Text_BattleReceptionistIntro, MSGBOX_NPC
	end

Unova_Pokecenter2F_EventScript_Npc2::
	msgbox Unova_Pokecenter2F_Text_Text_TimeCapsuleReceptionistIntro, MSGBOX_NPC
	end

Unova_Pokecenter2F_EventScript_Npc3::
	msgbox Unova_Pokecenter2F_Text_Text_MysteryGiftDeliveryGuy_Intro, MSGBOX_NPC
	end


Unova_Pokecenter2F_Text_Text_TradeReceptionistIntro::
	.string "Welcome to CABLE"
	.string "\nTRADE CENTER."
	.string "\pYou may trade your"
	.string "\nPOKéMON here with"
	.string "\la friend."
	.string "\pWould you like to"
	.string "\ntrade?$"

Unova_Pokecenter2F_Text_Text_BattleReceptionistIntro::
	.string "Welcome to CABLE"
	.string "\nCLUB COLOSSEUM."
	.string "\pYou may battle a"
	.string "\nfriend here."
	.string "\pWould you like to"
	.string "\nbattle?$"

Unova_Pokecenter2F_Text_Text_TimeCapsuleReceptionistIntro::
	.string "Welcome to CABLE"
	.string "\nCLUB TIME CAPSULE."
	.string "\pYou can travel to"
	.string "\nthe past and trade"
	.string "\lyour POKéMON."
	.string "\pWould you like to"
	.string "\ntrade across time?$"

Unova_Pokecenter2F_Text_Text_MysteryGiftDeliveryGuy_Intro::
	.string "Hello! You're"
	.string "\n{PLAYER}, right?"
	.string "\pI have some-"
	.string "\nthing for you.$"
