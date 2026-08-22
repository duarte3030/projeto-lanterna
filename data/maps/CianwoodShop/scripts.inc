CianwoodShop_MapScripts::
	.byte 0

CianwoodShop_EventScript_Clerk::
	lock
	faceplayer
	call CianwoodShop_EventScript_Pharmacist
	message gText_HowMayIServeYou
	waitmessage
	pokemart CianwoodShop_Pokemart
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
CianwoodShop_Pokemart:
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REPEL
	pokemartlistend

@ ARCO DO FAROL DE OLIVINE, dev_scripts/arco_farol_johto.py
@ A farmacia de Cianwood. No hns o unico NPC deste mapa E o farmaceutico e nao
@ ha loja; aqui ele ja era balconista de mart quando esta rodada comecou, entao
@ o remedio vem ANTES do balcao e a loja continua existindo. Nada foi tirado.
CianwoodShop_EventScript_Pharmacist::
	goto_if_ne VAR_OLIVINE_CITY_STATE, 3, CianwoodShop_EventScript_SemRemedio
	msgbox CianwoodShop_Text_PharmacistGivePotion, MSGBOX_DEFAULT
	giveitem ITEM_SECRET_POTION
	setvar VAR_OLIVINE_CITY_STATE, 4
	return

CianwoodShop_EventScript_SemRemedio::
	return

CianwoodShop_Text_PharmacistGivePotion:
	.string "Your POKéMON appear to be fine.\p"
	.string "Is something worrying you?\p"
	.string "…\p"
	.string "The LIGHTHOUSE POKéMON is in\n"
	.string "trouble?\p"
	.string "I got it!\n"
	.string "This ought to do the trick.$"
