@ Rt23West do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt23West_MapScripts::
	.byte 0

Unova_Rt23West_EventScript_Npc1::
	msgbox Unova_Rt23West_Text_R23Officer7StopText, MSGBOX_NPC
	end

Unova_Rt23West_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERM_R23_2, Unova_Rt23West_Text_AceTrainerM2R23SeenText, Unova_Rt23West_Text_AceTrainerM2R23BeatenText
	end

Unova_Rt23West_EventScript_Lider12::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_R23_2, Unova_Rt23West_Text_AceTrainerF2R23SeenText, Unova_Rt23West_Text_AceTrainerF2R23BeatenText
	end

Unova_Rt23West_EventScript_Lider13::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERM_R23, Unova_Rt23West_Text_BackpackerMR23SeenText, Unova_Rt23West_Text_BackpackerMR23BeatenText
	end

Unova_Rt23West_EventScript_Lider14::
	trainerbattle_single TRAINER_UNOVA_BACKPACKERF_R23, Unova_Rt23West_Text_BackpackerFR23SeenText, Unova_Rt23West_Text_BackpackerFR23BeatenText
	end

Unova_Rt23West_EventScript_Lider15::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_R23, Unova_Rt23West_Text_PkmnRangerMR23SeenText, Unova_Rt23West_Text_PkmnRangerMR23BeatenText
	end

Unova_Rt23West_EventScript_Lider16::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_R23, Unova_Rt23West_Text_PkmnRangerFR23SeenText, Unova_Rt23West_Text_PkmnRangerFR23BeatenText
	end

Unova_Rt23West_EventScript_Lider17::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_R23, Unova_Rt23West_Text_BattleGirlR23SeenText, Unova_Rt23West_Text_BattleGirlR23BeatenText
	end

Unova_Rt23West_EventScript_Lider18::
	trainerbattle_single TRAINER_UNOVA_VETERANM_R23, Unova_Rt23West_Text_VeteranMR23SeenText, Unova_Rt23West_Text_VeteranMR23BeatenText
	end


Unova_Rt23West_Text_R23Officer7StopText::
	.string "Stop! Ahead lies"
	.string "\nthe path to the"
	.string "\lPOKéMON LEAGUE."
	.string "\pOnly those who"
	.string "\nhave collected"
	.string "\pall 8 POKéMON"
	.string "\nLEAGUE GYM BADGES"
	.string "\lmay enter."
	.string "\pYou cannot pass"
	.string "\nhere unless you"
	.string "\phave the"
	.string "\nLEGENDBADGE.$"

Unova_Rt23West_Text_AceTrainerM2R23SeenText::
	.string "I keep a tally of"
	.string "\nall of the times"
	.string "\pthat I have won or"
	.string "\nlost up until"
	.string "\ptoday. If I battle"
	.string "\nyou, I wonder"
	.string "\pwhich number will"
	.string "\nbe increased.$"

Unova_Rt23West_Text_AceTrainerM2R23BeatenText::
	.string "So my number of"
	.string "\nlosses went up…$"

Unova_Rt23West_Text_AceTrainerF2R23SeenText::
	.string "This is the"
	.string "\nconcerto I perform"
	.string "\pwith my most"
	.string "\nbeloved POKéMON!$"

Unova_Rt23West_Text_AceTrainerF2R23BeatenText::
	.string "Your side is much"
	.string "\nmore in harmony!$"

Unova_Rt23West_Text_BackpackerMR23SeenText::
	.string "You look like an"
	.string "\nopponent who will"
	.string "\phighlight my"
	.string "\nweaknesses.$"

Unova_Rt23West_Text_BackpackerMR23BeatenText::
	.string "Now I see my"
	.string "\nfaults clearly.$"

Unova_Rt23West_Text_BackpackerFR23SeenText::
	.string "A heated battle is"
	.string "\ngood, but get too"
	.string "\phot and you might"
	.string "\nend up getting"
	.string "\lburned!$"

Unova_Rt23West_Text_BackpackerFR23BeatenText::
	.string "Amazing! I think I"
	.string "\ngot a bit singed…$"

Unova_Rt23West_Text_PkmnRangerMR23SeenText::
	.string "I've been waiting"
	.string "\nfor this! Waiting"
	.string "\pfor this very"
	.string "\nmoment!$"

Unova_Rt23West_Text_PkmnRangerMR23BeatenText::
	.string "I had been waiting"
	.string "\nfor such a strong"
	.string "\ptrainer as your-"
	.string "\nself!$"

Unova_Rt23West_Text_PkmnRangerFR23SeenText::
	.string "Oh trainer,"
	.string "\nembarking on the"
	.string "\ppath to VICTORY"
	.string "\nROAD! Won't you"
	.string "\pshow me your true"
	.string "\npower?!$"

Unova_Rt23West_Text_PkmnRangerFR23BeatenText::
	.string "You didn't have to"
	.string "\nshow me quite that"
	.string "\lmuch power…$"

Unova_Rt23West_Text_BattleGirlR23SeenText::
	.string "Your POKéMON must"
	.string "\nbe really some-"
	.string "\pthing if you're"
	.string "\nhere on ROUTE 23!$"

Unova_Rt23West_Text_BattleGirlR23BeatenText::
	.string "Hahaha! POKéMON"
	.string "\nare so much fun!$"

Unova_Rt23West_Text_VeteranMR23SeenText::
	.string "Hey there, future"
	.string "\nchampion!$"

Unova_Rt23West_Text_VeteranMR23BeatenText::
	.string "When someone wins,"
	.string "\ntheir opponent has"
	.string "\lto lose, right?$"
