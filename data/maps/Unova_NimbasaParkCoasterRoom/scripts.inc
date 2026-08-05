@ NimbasaParkCoasterRoom do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NimbasaParkCoasterRoom_MapScripts::
	.byte 0

Unova_NimbasaParkCoasterRoom_EventScript_Placa0::
	msgbox Unova_NimbasaParkCoasterRoom_Text_NimbasaParkCoasterMoveText, MSGBOX_SIGN
	end

Unova_NimbasaParkCoasterRoom_EventScript_Placa1::
	msgbox Unova_NimbasaParkCoasterRoom_Text_NimbasaParkCoasterMoveText2, MSGBOX_SIGN
	end

Unova_NimbasaParkCoasterRoom_EventScript_Placa2::
	msgbox Unova_NimbasaParkCoasterRoom_Text_NimbasaParkCoasterSwitchText, MSGBOX_SIGN
	end

Unova_NimbasaParkCoasterRoom_EventScript_Placa7::
	msgbox Unova_NimbasaParkCoasterRoom_Text_NimbasaParkOldGymText2, MSGBOX_SIGN
	end

Unova_NimbasaParkCoasterRoom_EventScript_Placa8::
	msgbox Unova_NimbasaParkCoasterRoom_Text_NimbasaParkOldGymText2, MSGBOX_SIGN
	end

Unova_NimbasaParkCoasterRoom_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_NIMBASA_1, Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark1SeenText, Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark1BeatenText
	end

Unova_NimbasaParkCoasterRoom_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_NIMBASA_2, Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark2SeenText, Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark2BeatenText
	end

Unova_NimbasaParkCoasterRoom_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_NIMBASA_3, Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark3SeenText, Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark3BeatenText
	end

Unova_NimbasaParkCoasterRoom_EventScript_Npc7::
	msgbox Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark1AfterText, MSGBOX_NPC
	end

Unova_NimbasaParkCoasterRoom_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_GRUNTF_NIMBASA_1, Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark1SeenText, Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark1BeatenText
	end

Unova_NimbasaParkCoasterRoom_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_GRUNTF_NIMBASA_2, Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark2SeenText, Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark2BeatenText
	end

Unova_NimbasaParkCoasterRoom_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_GRUNTF_NIMBASA_3, Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark3SeenText, Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark3BeatenText
	end


Unova_NimbasaParkCoasterRoom_Text_NimbasaParkCoasterMoveText::
	.string "Something moved…$"

Unova_NimbasaParkCoasterRoom_Text_NimbasaParkCoasterMoveText2::
	.string "It sounds like"
	.string "\nsomething heavy"
	.string "\lcrashed…"
	.string "\pA coaster car must"
	.string "\nhave fallen off of"
	.string "\lthe track.$"

Unova_NimbasaParkCoasterRoom_Text_NimbasaParkCoasterSwitchText::
	.string "Oh! There's a"
	.string "\nswitch."
	.string "\pLet's press it!$"

Unova_NimbasaParkCoasterRoom_Text_NimbasaParkOldGymText2::
	.string "N--BASA --TY GY-"
	.string "\nLea--r: E--sa$"

Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark1SeenText::
	.string "I stole this POKé-"
	.string "\nMON years ago, and"
	.string "\pI've been training"
	.string "\nit ever since!"
	.string "\pIt's tough!$"

Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark1BeatenText::
	.string "Don't let it go to"
	.string "\nyour head… but you"
	.string "\pput up a good"
	.string "\nfight…$"

Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark2SeenText::
	.string "Just to warn you,"
	.string "\nI show no mercy!$"

Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark2BeatenText::
	.string "What's the big"
	.string "\nidea? The POKéMON"
	.string "\pI stole was"
	.string "\nuseless!$"

Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark3SeenText::
	.string "It's no use!"
	.string "\nYou're outmatched!$"

Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark3BeatenText::
	.string "So you're a"
	.string "\ntrainer who fights"
	.string "\pfor your POKéMON,"
	.string "\neh?$"

Unova_NimbasaParkCoasterRoom_Text_GruntMNimbasaPark1AfterText::
	.string "You've got to be"
	.string "\nkidding! And I"
	.string "\ptoughened it up so"
	.string "\nmuch, too!$"

Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark1SeenText::
	.string "This used to be a"
	.string "\nroller coaster."
	.string "\pCan you figure out"
	.string "\nhow to get through"
	.string "\lthis place?$"

Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark1BeatenText::
	.string "I get it…$"

Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark2SeenText::
	.string "Okay, it's my"
	.string "\nturn!$"

Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark2BeatenText::
	.string "Plasma! Plasmaaa!$"

Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark3SeenText::
	.string "If I win, give me"
	.string "\nyour POKéMON!$"

Unova_NimbasaParkCoasterRoom_Text_GruntFNimbasaPark3BeatenText::
	.string "What?! What a"
	.string "\njoke!$"
