@ Rt13 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt13_MapScripts::
	.byte 0

Unova_Rt13_EventScript_Placa0::
	msgbox Unova_Rt13_Text_R13SignText, MSGBOX_SIGN
	end

Unova_Rt13_EventScript_Placa1::
	msgbox Unova_Rt13_Text_R13UndellaSignText, MSGBOX_SIGN
	end

Unova_Rt13_EventScript_Npc0::
	msgbox Unova_Rt13_Text_R13Blocker1Text, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc1::
	msgbox Unova_Rt13_Text_R13Blocker2Text, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc2::
	msgbox Unova_Rt13_Text_R13Blocker3Text, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Npc3::
	msgbox Unova_Rt13_Text_R13Blocker4Text, MSGBOX_NPC
	end

Unova_Rt13_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_R13, Unova_Rt13_Text_YoungsterR13SeenText, Unova_Rt13_Text_YoungsterR13BeatenText
	end

Unova_Rt13_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_LASS_R13, Unova_Rt13_Text_LassR13SeenText, Unova_Rt13_Text_LassR13BeatenText
	end

Unova_Rt13_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_R13, Unova_Rt13_Text_SchoolKidMR13SeenText, Unova_Rt13_Text_SchoolKidMR13BeatenText
	end

Unova_Rt13_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDF_R13, Unova_Rt13_Text_SchoolKidFR13SeenText, Unova_Rt13_Text_SchoolKidFR13BeatenText
	end


Unova_Rt13_Text_R13SignText::
	.string "GIANT CHASM"
	.string "\pBeware of wild"
	.string "\nPOKéMON!$"

Unova_Rt13_Text_R13UndellaSignText::
	.string "ROUTE 13"
	.string "\pA beachside"
	.string "\nstroll from"
	.string "\pUNDELLA TOWN to"
	.string "\nLACUNOSA TOWN.$"

Unova_Rt13_Text_R13Blocker1Text::
	.string "Hey, watch out!"
	.string "\pWe're in the"
	.string "\nmiddle of a POKé-"
	.string "\lMON battle!$"

Unova_Rt13_Text_R13Blocker2Text::
	.string "PATRAT: Prah!$"

Unova_Rt13_Text_R13Blocker3Text::
	.string "PURRLOIN: Prrr-$"

Unova_Rt13_Text_R13Blocker4Text::
	.string "Stop bothering"
	.string "\nme! I'll battle"
	.string "\pyou when I'm"
	.string "\nfinished.$"

Unova_Rt13_Text_YoungsterR13SeenText::
	.string "You can tell how"
	.string "\nmuch your opponent"
	.string "\lwants to fight by"
	.string "\plooking into their"
	.string "\neyes, don't you"
	.string "\lthink?$"

Unova_Rt13_Text_YoungsterR13BeatenText::
	.string "Wow! I could tell"
	.string "\nyou really wanted"
	.string "\lto win!$"

Unova_Rt13_Text_LassR13SeenText::
	.string "Hey, you! Have you"
	.string "\nseen my cute POKé-"
	.string "\lMON? Take a look!$"

Unova_Rt13_Text_LassR13BeatenText::
	.string "My POKéMON are"
	.string "\ncute even if they"
	.string "\llose!$"

Unova_Rt13_Text_SchoolKidMR13SeenText::
	.string "I'm the strongest"
	.string "\ntrainer in my"
	.string "\lclass!$"

Unova_Rt13_Text_SchoolKidMR13BeatenText::
	.string "I guess I'm not"
	.string "\nthe strongest in"
	.string "\lthe world.$"

Unova_Rt13_Text_SchoolKidFR13SeenText::
	.string "My favorite class"
	.string "\nis math!$"

Unova_Rt13_Text_SchoolKidFR13BeatenText::
	.string "Oh, no!"
	.string "\nHow could I lose?$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ Gruta escondida do BW3G (tier 1). ponytail: la ela reenche
@ todo dia; aqui e uma flag e o item sai uma vez so.
Unova_Rt13_EventScript_Gruta4B8::
	goto_if_set FLAG_UNOVA_GRUTA_R13, Unova_EventScript_GrutaVazia
	setflag FLAG_UNOVA_GRUTA_R13
	goto Unova_EventScript_GrutaTier1
