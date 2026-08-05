@ Rt9 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt9_MapScripts::
	.byte 0

Unova_Rt9_EventScript_Placa0::
	msgbox Unova_Rt9_Text_R9SignText, MSGBOX_SIGN
	end

Unova_Rt9_EventScript_Placa1::
	msgbox Unova_Rt9_Text_R9MallSignText, MSGBOX_SIGN
	end

Unova_Rt9_EventScript_Placa2::
	msgbox Unova_Rt9_Text_R9TubelineSignText, MSGBOX_SIGN
	end

Unova_Rt9_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_BIKER_R9_1, Unova_Rt9_Text_Biker1R9SeenText, Unova_Rt9_Text_Biker1R9BeatenText
	end

Unova_Rt9_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_BIKER_R9_2, Unova_Rt9_Text_Biker2R9SeenText, Unova_Rt9_Text_Biker2R9BeatenText
	end

Unova_Rt9_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_ROUGHNECK_R9_1, Unova_Rt9_Text_Roughneck1R9SeenText, Unova_Rt9_Text_Roughneck1R9BeatenText
	end

Unova_Rt9_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_ROUGHNECK_R9_2, Unova_Rt9_Text_Roughneck2R9SeenText, Unova_Rt9_Text_Roughneck2R9BeatenText
	end


Unova_Rt9_Text_R9SignText::
	.string "ROUTE 9$"

Unova_Rt9_Text_R9MallSignText::
	.string "SHOPPING MALL 9"
	.string "\pWares for serious"
	.string "\nPOKéMON trainers.$"

Unova_Rt9_Text_R9TubelineSignText::
	.string "TUBELINE BRIDGE"
	.string "\nahead."
	.string "\pPassage to"
	.string "\nICIRRUS CITY.$"

Unova_Rt9_Text_Biker1R9SeenText::
	.string "Hey, hey! I'll"
	.string "\ntake care of you!$"

Unova_Rt9_Text_Biker1R9BeatenText::
	.string "My baby lost!$"

Unova_Rt9_Text_Biker2R9SeenText::
	.string "Do you want to"
	.string "\npass through here?"
	.string "\pThen, you must"
	.string "\ngreet me!$"

Unova_Rt9_Text_Biker2R9BeatenText::
	.string "You! What great"
	.string "\nstrength you have!$"

Unova_Rt9_Text_Roughneck1R9SeenText::
	.string "Hey, hey! What's"
	.string "\nwrong? Are you"
	.string "\llost or something?$"

Unova_Rt9_Text_Roughneck1R9BeatenText::
	.string "Beaten down!$"

Unova_Rt9_Text_Roughneck2R9SeenText::
	.string "Join our team!"
	.string "\pActually, I will"
	.string "\nforce you to join"
	.string "\lour team!$"

Unova_Rt9_Text_Roughneck2R9BeatenText::
	.string "Our team doesn't"
	.string "\nneed a trainer who"
	.string "\pis quite that"
	.string "\nstrong!$"
