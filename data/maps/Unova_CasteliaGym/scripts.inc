@ CasteliaGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_CasteliaGym_MapScripts::
	.byte 0

Unova_CasteliaGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_BURGH, Unova_CasteliaGym_Text_BurghGymIntroText, Unova_CasteliaGym_Text_BurghWinLossText, Unova_CasteliaGym_EventScript_Insignia0
	end

Unova_CasteliaGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_CASTELIA
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_CasteliaGym_EventScript_Npc1::
	msgbox Unova_CasteliaGym_Text_CasteliaGymGuyText, MSGBOX_NPC
	end

Unova_CasteliaGym_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_1, Unova_CasteliaGym_Text_HarlequinCasteliaGym1SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym1BeatenText
	end

Unova_CasteliaGym_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_2, Unova_CasteliaGym_Text_HarlequinCasteliaGym2SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym2BeatenText
	end

Unova_CasteliaGym_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_3, Unova_CasteliaGym_Text_HarlequinCasteliaGym3SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym3BeatenText
	end

Unova_CasteliaGym_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_4, Unova_CasteliaGym_Text_HarlequinCasteliaGym4SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym4BeatenText
	end

Unova_CasteliaGym_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_5, Unova_CasteliaGym_Text_HarlequinCasteliaGym5SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym5BeatenText
	end


Unova_CasteliaGym_Text_BurghGymIntroText::
	.string "Hm, my BUG POKé-"
	.string "\nMON have been"
	.string "\pgetting all worked"
	.string "\nup, and what do I"
	.string "\pspy with my little"
	.string "\neye? A trainer"
	.string "\pwho's got me"
	.string "\nscurrying around"
	.string "\lwith excitement!"
	.string "\pI, BURGH, the GYM"
	.string "\nLEADER of CASTELIA"
	.string "\lCITY, accept your"
	.string "\lchallenge!"
	.string "\pLet's get right"
	.string "\nto it!$"

Unova_CasteliaGym_Text_BurghWinLossText::
	.string "Is it over, has"
	.string "\nmy muse abandoned"
	.string "\lme?"
	.string "\pHere, take this"
	.string "\nbadge, I think"
	.string "\lit'll suit you!$"

Unova_CasteliaGym_Text_CasteliaGymGuyText::
	.string "Yo, challenger!"
	.string "\pCASTELIA CITY's"
	.string "\nGYM LEADER is"
	.string "\lcalled BURGH."
	.string "\pHe's a bit of an"
	.string "\noddball, but you'd"
	.string "\pbetter not under-"
	.string "\nestimate his BUG"
	.string "\ltype POKéMON!"
	.string "\pBugs are most"
	.string "\nafraid of FIRE."
	.string "\pThey can also be"
	.string "\ncrushed by ROCKs,"
	.string "\pand FLYING attacks"
	.string "\nwork well too.$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym1SeenText::
	.string "What do you think?"
	.string "\nThis GYM… How"
	.string "\lshould I say?"
	.string "\pIsn't it full of…"
	.string "\nmysterious charms?$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym1BeatenText::
	.string "You've got quite a"
	.string "\nbit of charm your-"
	.string "\lself, don't you?$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym2SeenText::
	.string "You thought you"
	.string "\ncould get through"
	.string "\lhere? Think again!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym2BeatenText::
	.string "My, my! Aren't you"
	.string "\na bit too strong?$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym3SeenText::
	.string "When the cocoon"
	.string "\nopens, the one who"
	.string "\lpops out is moi!"
	.string "\pOn that note, have"
	.string "\na battle with moi!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym3BeatenText::
	.string "I was taking a"
	.string "\nnap!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym4SeenText::
	.string "The one you meet"
	.string "\nat this cocoon is"
	.string "\pnone other than"
	.string "\nme!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym4BeatenText::
	.string "Looks like the"
	.string "\ncocoons brought"
	.string "\lyou to me!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym5SeenText::
	.string "You're just one"
	.string "\nstep away from"
	.string "\pbeing able to"
	.string "\nchallenge BURGH!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym5BeatenText::
	.string "Your battle style"
	.string "\nis almost as"
	.string "\lartistic as BURGH!$"
