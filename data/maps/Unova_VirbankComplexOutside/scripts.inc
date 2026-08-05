@ VirbankComplexOutside do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VirbankComplexOutside_MapScripts::
	.byte 0

Unova_VirbankComplexOutside_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_VIRBANK_COMPLEX_1, Unova_VirbankComplexOutside_Text_GruntM1VirbankComplexOutsideSeenText, Unova_VirbankComplexOutside_Text_GruntM1VirbankComplexOutsideBeatenText
	end

Unova_VirbankComplexOutside_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_GRUNTM_VIRBANK_COMPLEX_2, Unova_VirbankComplexOutside_Text_GruntM2VirbankComplexOutsideSeenText, Unova_VirbankComplexOutside_Text_GruntM2VirbankComplexOutsideBeatenText
	end

Unova_VirbankComplexOutside_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_GRUNTF_VIRBANK_COMPLEX_1, Unova_VirbankComplexOutside_Text_GruntFVirbankComplexOutsideSeenText, Unova_VirbankComplexOutside_Text_GruntFVirbankComplexOutsideBeatenText
	end

Unova_VirbankComplexOutside_EventScript_Npc8::
	msgbox Unova_VirbankComplexOutside_Text_VirbankComplexOutsideCherenIntroText, MSGBOX_NPC
	end


Unova_VirbankComplexOutside_Text_GruntM1VirbankComplexOutsideSeenText::
	.string "Ha! I bet you"
	.string "\nthought I was a"
	.string "\lworker here!$"

Unova_VirbankComplexOutside_Text_GruntM1VirbankComplexOutsideBeatenText::
	.string "Grrrr…$"

Unova_VirbankComplexOutside_Text_GruntM2VirbankComplexOutsideSeenText::
	.string "I trained myself"
	.string "\nendlessly to get"
	.string "\pjustice for TEAM"
	.string "\nPLASMA! I won't"
	.string "\plose to anyone"
	.string "\nanymore!$"

Unova_VirbankComplexOutside_Text_GruntM2VirbankComplexOutsideBeatenText::
	.string "…But if I lose, I"
	.string "\nwon't be able to"
	.string "\pcarry out my"
	.string "\njustice!$"

Unova_VirbankComplexOutside_Text_GruntFVirbankComplexOutsideSeenText::
	.string "What do you want,"
	.string "\nintruder?!$"

Unova_VirbankComplexOutside_Text_GruntFVirbankComplexOutsideBeatenText::
	.string "Hmph! I missed my"
	.string "\nchance to grab"
	.string "\lyour POKéMON!$"

Unova_VirbankComplexOutside_Text_VirbankComplexOutsideCherenIntroText::
	.string "CHEREN: {PLAYER},"
	.string "\ngood timing."
	.string "\pI've been invest-"
	.string "\nigating this"
	.string "\lCOMPLEX."
	.string "\pIt's as I thought,"
	.string "\nTEAM PLASMA has"
	.string "\pinfiltrated the"
	.string "\nCOMPLEX. They"
	.string "\pmust be after"
	.string "\nsomething…"
	.string "\pI managed to snag"
	.string "\na key to the lift"
	.string "\pthat leads into"
	.string "\nthe facility."
	.string "\pHere, you should"
	.string "\ntake it.$"
