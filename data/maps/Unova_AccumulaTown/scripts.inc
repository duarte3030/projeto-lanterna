@ AccumulaTown do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_AccumulaTown_MapScripts::
	.byte 0

Unova_AccumulaTown_EventScript_Placa0::
	msgbox Unova_AccumulaTown_Text_AccumulaTownSignText, MSGBOX_SIGN
	end

Unova_AccumulaTown_EventScript_Npc0::
	msgbox Unova_AccumulaTown_Text_AccumulaTownPokefanMText, MSGBOX_NPC
	end

Unova_AccumulaTown_EventScript_Npc1::
	msgbox Unova_AccumulaTown_Text_AccumulaTownCooltrainerFText, MSGBOX_NPC
	end

Unova_AccumulaTown_EventScript_Npc2::
	msgbox Unova_AccumulaTown_Text_AccumulaTownTeacherText, MSGBOX_NPC
	end

Unova_AccumulaTown_EventScript_Npc3::
	msgbox Unova_AccumulaTown_Text_AccumulaTownYoungsterText, MSGBOX_NPC
	end

Unova_AccumulaTown_EventScript_Npc4::
	msgbox Unova_AccumulaTown_Text_AccumulaTownBlocker1Text, MSGBOX_NPC
	end

Unova_AccumulaTown_EventScript_Npc5::
	msgbox Unova_AccumulaTown_Text_AccumulaTownBlocker2Text, MSGBOX_NPC
	end

Unova_AccumulaTown_EventScript_Npc6::
	msgbox Unova_AccumulaTown_Text_AccumulaTownBlocker3Text, MSGBOX_NPC
	end

Unova_AccumulaTown_EventScript_Npc7::
	msgbox Unova_AccumulaTown_Text_AccumulaTownBlocker4Text, MSGBOX_NPC
	end

Unova_AccumulaTown_EventScript_Npc8::
	goto Unova_AccumulaTown_EventScript_RYOKU1


Unova_AccumulaTown_Text_AccumulaTownSignText::
	.string "ACCUMULA TOWN."
	.string "\pThe fast-growing"
	.string "\ntown!$"

Unova_AccumulaTown_Text_AccumulaTownPokefanMText::
	.string "Back when TEAM"
	.string "\nPLASMA was first"
	.string "\pstarted, they"
	.string "\ntried to recruit"
	.string "\ppeople from our"
	.string "\ntown."
	.string "\pA lot of us got"
	.string "\nswept up in what"
	.string "\lthey were saying."
	.string "\pIt was kind of"
	.string "\nscary, now that I"
	.string "\lthink about it.$"

Unova_AccumulaTown_Text_AccumulaTownCooltrainerFText::
	.string "Have you visited"
	.string "\nthe GYM in"
	.string "\lSTRIATON CITY yet?"
	.string "\pI heard their GYM"
	.string "\nLEADER was taking"
	.string "\pa break, but he"
	.string "\ndecided to come"
	.string "\lback!$"

Unova_AccumulaTown_Text_AccumulaTownTeacherText::
	.string "Oh, what's this?"
	.string "\pYou and your POKé-"
	.string "\nMON somehow res-"
	.string "\lemble each other!$"

Unova_AccumulaTown_Text_AccumulaTownYoungsterText::
	.string "TEAM PLASMA are no"
	.string "\ngood, thanks for"
	.string "\pgetting rid of"
	.string "\nthat guy!$"

Unova_AccumulaTown_Text_AccumulaTownBlocker1Text::
	.string "Man: Hey, you're"
	.string "\nfrom that TEAM"
	.string "\lPLASMA, aren't you?"
	.string "\pYou're probably up"
	.string "\nto no good!$"

Unova_AccumulaTown_Text_AccumulaTownBlocker2Text::
	.string "Woman: Hey, there"
	.string "\nwas a robbery in"
	.string "\pNACRENE CITY just"
	.string "\nrecently, I bet"
	.string "\phe had something"
	.string "\nto do with it!"
	.string "\pMan: That's why"
	.string "\nhe's in such a"
	.string "\phurry! He's trying"
	.string "\nto get away!"
	.string "\pWoman: Someone had"
	.string "\nbetter stop him!$"

Unova_AccumulaTown_Text_AccumulaTownBlocker3Text::
	.string "We won't just let"
	.string "\nTEAM PLASMA come"
	.string "\linto our town like"
	.string "\lthat!$"

Unova_AccumulaTown_Text_AccumulaTownBlocker4Text::
	.string "Hey! What does"
	.string "\nthat TEAM PLASMA"
	.string "\lguy think he's"
	.string "\ldoing?$"

Unova_AccumulaTown_Text_AccumulaTownRyokuIntroText::
	.string "???: Oh dear…"
	.string "\pPlease, you must"
	.string "\nallow me through.$"

@ >>> cena importada por dev_scripts/importa_chefes_faltantes.py >>>
Unova_AccumulaTown_EventScript_RYOKU1::
	trainerbattle_single TRAINER_UNOVA_RYOKU1, Unova_AccumulaTown_Text_AccumulaTownRyokuIntroText, Unova_AccumulaTown_Text_RYOKU1Beaten
	msgbox Unova_AccumulaTown_Text_RYOKU1Depois, MSGBOX_DEFAULT
	release
	end

Unova_AccumulaTown_Text_RYOKU1Beaten::
	.string "Oh dear…$"

Unova_AccumulaTown_Text_RYOKU1Depois::
	.string "RYOKU: I-I must\n"
	.string "retreat! Here,\l"
	.string "take it!$"
@ <<< cena importada por dev_scripts/importa_chefes_faltantes.py <<<
