@ LentimasOutskirts do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_LentimasOutskirts_MapScripts::
	.byte 0

Unova_LentimasOutskirts_EventScript_Placa0::
	msgbox Unova_LentimasOutskirts_Text_LentimasReversalSignText, MSGBOX_SIGN
	end

Unova_LentimasOutskirts_EventScript_Placa1::
	msgbox Unova_LentimasOutskirts_Text_LentimasLostlornSignText, MSGBOX_SIGN
	end

Unova_LentimasOutskirts_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_SCHOOL_KIDM_OUTSKIRTS, Unova_LentimasOutskirts_Text_SchoolKidMOutskirtsSeenText, Unova_LentimasOutskirts_Text_SchoolKidMOutskirtsBeatenText
	end

Unova_LentimasOutskirts_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_CYCLISTM_OUTSKIRTS, Unova_LentimasOutskirts_Text_CyclistMOutskirtsSeenText, Unova_LentimasOutskirts_Text_CyclistMOutskirtsBeatenText
	end

Unova_LentimasOutskirts_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_CYCLISTF_OUTSKIRTS, Unova_LentimasOutskirts_Text_CyclistFOutskirtsSeenText, Unova_LentimasOutskirts_Text_CyclistFOutskirtsBeatenText
	end

Unova_LentimasOutskirts_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_YOUNGSTER_OUTSKIRTS, Unova_LentimasOutskirts_Text_YoungsterOutskirtsSeenText, Unova_LentimasOutskirts_Text_YoungsterOutskirtsBeatenText
	end

Unova_LentimasOutskirts_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_OUTSKIRTS, Unova_LentimasOutskirts_Text_PkmnRangerMOutskirtsSeenText, Unova_LentimasOutskirts_Text_PkmnRangerMOutskirtsBeatenText
	end

Unova_LentimasOutskirts_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERF_OUTSKIRTS, Unova_LentimasOutskirts_Text_PkmnRangerFOutskirtsSeenText, Unova_LentimasOutskirts_Text_PkmnRangerFOutskirtsBeatenText
	end

Unova_LentimasOutskirts_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_DOCTOR_OUTSKIRTS, Unova_LentimasOutskirts_Text_OutskirtsDoctorIntroText, Unova_LentimasOutskirts_Text_OutskirtsDoctorWinText
	end


Unova_LentimasOutskirts_Text_LentimasReversalSignText::
	.string "REVERSAL MOUNTAIN."
	.string "\pEnter at your"
	.string "\nown risk!$"

Unova_LentimasOutskirts_Text_LentimasLostlornSignText::
	.string "South to"
	.string "\nLOSTLORN FOREST.$"

Unova_LentimasOutskirts_Text_SchoolKidMOutskirtsSeenText::
	.string "I've been training"
	.string "\nto take on the"
	.string "\pGYM. I won't give"
	.string "\nup easily!$"

Unova_LentimasOutskirts_Text_SchoolKidMOutskirtsBeatenText::
	.string "What! My victory"
	.string "\nwas taken away"
	.string "\lfrom me!$"

Unova_LentimasOutskirts_Text_CyclistMOutskirtsSeenText::
	.string "Yahooo! If you"
	.string "\ncall, I'll come"
	.string "\lright away!$"

Unova_LentimasOutskirts_Text_CyclistMOutskirtsBeatenText::
	.string "I'm on fire, baby!"
	.string "\nOn fire!$"

Unova_LentimasOutskirts_Text_CyclistFOutskirtsSeenText::
	.string "Shift gears and"
	.string "\nBob's your uncle!"
	.string "\pYou'll be going"
	.string "\nfull speed in no"
	.string "\ltime!$"

Unova_LentimasOutskirts_Text_CyclistFOutskirtsBeatenText::
	.string "No matter how I"
	.string "\nshift my gears, it"
	.string "\plooks like I'll"
	.string "\nnever match your"
	.string "\lspeed!$"

Unova_LentimasOutskirts_Text_YoungsterOutskirtsSeenText::
	.string "I'm going to over-"
	.string "\nwhelm you with my"
	.string "\lspeed!$"

Unova_LentimasOutskirts_Text_YoungsterOutskirtsBeatenText::
	.string "Roll, roll, roll,"
	.string "\nroll on!$"

Unova_LentimasOutskirts_Text_PkmnRangerMOutskirtsSeenText::
	.string "I'm wandering the"
	.string "\nworld trying to"
	.string "\pfind a place where"
	.string "\nI belong…"
	.string "\pHow about you?$"

Unova_LentimasOutskirts_Text_PkmnRangerMOutskirtsBeatenText::
	.string "I lost… So this"
	.string "\nisn't where I"
	.string "\lbelong either…$"

Unova_LentimasOutskirts_Text_PkmnRangerFOutskirtsSeenText::
	.string "Every day is the"
	.string "\nsame. I get bored"
	.string "\pwhen things don't"
	.string "\nchange, so I don't"
	.string "\lmind battling you!$"

Unova_LentimasOutskirts_Text_PkmnRangerFOutskirtsBeatenText::
	.string "It's been quite"
	.string "\nsome time since"
	.string "\pI've had a POKéMON"
	.string "\nbattle!$"

Unova_LentimasOutskirts_Text_OutskirtsDoctorIntroText::
	.string "I'm a doctor, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_LentimasOutskirts_Text_OutskirtsDoctorWinText::
	.string "Ah, I see.$"
