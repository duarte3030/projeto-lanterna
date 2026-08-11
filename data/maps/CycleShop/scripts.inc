CycleShop_MapScripts::
	.byte 0

CycleShop_EventScript_Caixa::
	lock
	faceplayer
	msgbox CycleShop_Text_Caixa, MSGBOX_DEFAULT
	pokemart CycleShop_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
CycleShop_Pokemart:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

CycleShop_Text_Caixa:
	.string "Welcome! Take a look around, we've\n"
	.string "got everything a TRAINER needs.$"

CycleShop_EventScript_Npc1::
	msgbox CycleShop_Text_Npc1, MSGBOX_NPC
	end

CycleShop_Text_Npc1:
	.string "The manager's gone off to the Team\nGalactic building and hasn't returned.\pI wonder what's holding him up?$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CycleShop_EventScript_Placa1::
	msgbox CycleShop_Text_Placa1, MSGBOX_SIGN
	end

CycleShop_Text_Placa1:
	.string "There is a manual on the latest\nmodel Bicycle.\pThird gear for steering.\nFourth gear for all-out speed!\pChange gears with the B Button for\nexhilarating cycling!$"

CycleShop_EventScript_Placa2::
	msgbox CycleShop_Text_Placa2, MSGBOX_SIGN
	end

CycleShop_Text_Placa2:
	.string "There is a manual on the latest\nmodel Bicycle.\pThird gear for steering.\nFourth gear for all-out speed!\pChange gears with the B Button for\nexhilarating cycling!$"

CycleShop_EventScript_Placa3::
	msgbox CycleShop_Text_Placa3, MSGBOX_SIGN
	end

CycleShop_Text_Placa3:
	.string "There's a catalog from the Hoenn region\non its popular Bikes...\pMach Bike--a folding Bike built solely\nfor blazing speed!\pAcro Bike--a folding Bike designed for\nstunts like jumps and wheelies!$"

CycleShop_EventScript_Placa4::
	msgbox CycleShop_Text_Placa4, MSGBOX_SIGN
	end

CycleShop_Text_Placa4:
	.string "There's a catalog from the Hoenn region\non its popular Bikes...\pMach Bike--a folding Bike built solely\nfor blazing speed!\pAcro Bike--a folding Bike designed for\nstunts like jumps and wheelies!$"
