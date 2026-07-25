FloaromaTown_FlowerShop_MapScripts::
	.byte 0

FloaromaTown_FlowerShop_EventScript_Beauty::
	msgbox FloaromaTown_FlowerShop_Text_Beauty, MSGBOX_NPC
	end

FloaromaTown_FlowerShop_EventScript_Lass::
	msgbox FloaromaTown_FlowerShop_Text_Lass, MSGBOX_NPC
	end

FloaromaTown_FlowerShop_EventScript_Breeder::
	msgbox FloaromaTown_FlowerShop_Text_Breeder, MSGBOX_NPC
	end

FloaromaTown_FlowerShop_Text_Beauty:
	.string "The flowers here are grown with so\n"
	.string "much care. Aren't they lovely?$"

FloaromaTown_FlowerShop_Text_Lass:
	.string "TRAINER, please water Berries using\n"
	.string "this SPRAYDUCK watering can.\p"
	.string "Use it to water the soil where you've\n"
	.string "planted Berries.$"

FloaromaTown_FlowerShop_Text_Breeder:
	.string "A single Berry will grow into a plant\n"
	.string "that makes several Berries.\p"
	.string "By planting one, there will be more\n"
	.string "and more Berries in the world.$"
