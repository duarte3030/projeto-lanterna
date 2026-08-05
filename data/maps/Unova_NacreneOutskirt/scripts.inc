@ NacreneOutskirt do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_NacreneOutskirt_MapScripts::
	.byte 0

Unova_NacreneOutskirt_EventScript_Placa0::
	msgbox Unova_NacreneOutskirt_Text_NacreneOutskirtSignText, MSGBOX_SIGN
	end

Unova_NacreneOutskirt_EventScript_Npc0::
	msgbox Unova_NacreneOutskirt_Text_NacreneOutskirtYoungsterText, MSGBOX_NPC
	end

Unova_NacreneOutskirt_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_NACRENE_OUTSKIRT, Unova_NacreneOutskirt_Text_YoungsterNacreneSeenText, Unova_NacreneOutskirt_Text_YoungsterNacreneBeatenText
	end

Unova_NacreneOutskirt_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_LASS_NACRENE_OUTSKIRT, Unova_NacreneOutskirt_Text_LassNacreneSeenText, Unova_NacreneOutskirt_Text_LassNacreneBeatenText
	end

Unova_NacreneOutskirt_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_PARASOL_LADY_NACRENE_OUTSKIRT, Unova_NacreneOutskirt_Text_ParasolLadyNacreneSeenText, Unova_NacreneOutskirt_Text_ParasolLadyNacreneBeatenText
	end

Unova_NacreneOutskirt_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_RICH_BOY_NACRENE_OUTSKIRT, Unova_NacreneOutskirt_Text_RichBoyNacreneSeenText, Unova_NacreneOutskirt_Text_RichBoyNacreneBeatenText
	end


Unova_NacreneOutskirt_Text_NacreneOutskirtSignText::
	.string "West to PINWHEEL"
	.string "\nFOREST."
	.string "\pStay on the road!$"

Unova_NacreneOutskirt_Text_NacreneOutskirtYoungsterText::
	.string "There are cops in"
	.string "\nthe forest. They"
	.string "\pwouldn't let me"
	.string "\nthrough!$"

Unova_NacreneOutskirt_Text_YoungsterNacreneSeenText::
	.string "I'm just gonna run"
	.string "\naround! I've got"
	.string "\pthe whole field to"
	.string "\nmyself!$"

Unova_NacreneOutskirt_Text_YoungsterNacreneBeatenText::
	.string "I know… I shouldn't"
	.string "\ntake it all for"
	.string "\lmyself…$"

Unova_NacreneOutskirt_Text_LassNacreneSeenText::
	.string "Hey, trainer! Let's"
	.string "\nhave a refreshing"
	.string "\pbattle and blow"
	.string "\naway all my"
	.string "\ltroubles!$"

Unova_NacreneOutskirt_Text_LassNacreneBeatenText::
	.string "You guys feel like"
	.string "\nan unbeatable"
	.string "\lcombination!$"

Unova_NacreneOutskirt_Text_ParasolLadyNacreneSeenText::
	.string "A woman standing"
	.string "\nalone with a para-"
	.string "\lsol in one hand…"
	.string "\pHi… Please have a"
	.string "\nbattle with me.$"

Unova_NacreneOutskirt_Text_ParasolLadyNacreneBeatenText::
	.string "The parasol can't"
	.string "\nblock defeat…$"

Unova_NacreneOutskirt_Text_RichBoyNacreneSeenText::
	.string "Are you ready to"
	.string "\nexperience a VIP"
	.string "\pPOKéMON battle"
	.string "\nperformance?$"

Unova_NacreneOutskirt_Text_RichBoyNacreneBeatenText::
	.string "My performance"
	.string "\nwasn't up to VIP"
	.string "\lstandards…$"
