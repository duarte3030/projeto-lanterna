@ Rt17 do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_Rt17_MapScripts::
	.byte 0

Unova_Rt17_EventScript_Placa0::
	msgbox Unova_Rt17_Text_R17SignText, MSGBOX_SIGN
	end

Unova_Rt17_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_FISHER_R17_1, Unova_Rt17_Text_Fisher1R17SeenText, Unova_Rt17_Text_Fisher1R17BeatenText
	end

Unova_Rt17_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_FISHER_R17_2, Unova_Rt17_Text_Fisher2R17SeenText, Unova_Rt17_Text_Fisher2R17BeatenText
	end

Unova_Rt17_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SWIMMER_M_R17_1, Unova_Rt17_Text_SwimmerM1R17SeenText, Unova_Rt17_Text_SwimmerM1R17BeatenText
	end

Unova_Rt17_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_SWIMMER_M_R17_2, Unova_Rt17_Text_SwimmerM2R17SeenText, Unova_Rt17_Text_SwimmerM2R17BeatenText
	end

Unova_Rt17_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_SWIMMER_F_R17_1, Unova_Rt17_Text_SwimmerF1R17SeenText, Unova_Rt17_Text_SwimmerF1R17BeatenText
	end

Unova_Rt17_EventScript_Lider10::
	trainerbattle_single TRAINER_UNOVA_SWIMMER_F_R17_2, Unova_Rt17_Text_SwimmerF2R17SeenText, Unova_Rt17_Text_SwimmerF2R17BeatenText
	end

Unova_Rt17_EventScript_Lider11::
	trainerbattle_single TRAINER_UNOVA_DOCTOR_R17, Unova_Rt17_Text_R17DoctorIntroText, Unova_Rt17_Text_R17DoctorWinText
	end


Unova_Rt17_Text_R17SignText::
	.string "ROUTE 17"
	.string "\pWatch for strong"
	.string "\ncurrents!$"

Unova_Rt17_Text_Fisher1R17SeenText::
	.string "I'm showing off"
	.string "\nthe sea to my"
	.string "\lbeloved POKéMON…$"

Unova_Rt17_Text_Fisher1R17BeatenText::
	.string "Wow! How powerful!$"

Unova_Rt17_Text_Fisher2R17SeenText::
	.string "The sounds of"
	.string "\ngently crashing"
	.string "\pwaves… The smell"
	.string "\nof salt in the"
	.string "\pair… And a battle"
	.string "\nwith a trainer!$"

Unova_Rt17_Text_Fisher2R17BeatenText::
	.string "Simply excellent!"
	.string "\nThat's what being"
	.string "\lyoung is about!$"

Unova_Rt17_Text_SwimmerM1R17SeenText::
	.string "I've been taking"
	.string "\non the POKéMON"
	.string "\pGyms all across"
	.string "\nthe world!$"

Unova_Rt17_Text_SwimmerM1R17BeatenText::
	.string "I couldn't defeat"
	.string "\nthem all, but I"
	.string "\plearned a lot, and"
	.string "\nbecame stronger!$"

Unova_Rt17_Text_SwimmerM2R17SeenText::
	.string "We spend our lives"
	.string "\nswimming! Of"
	.string "\pcourse we battle"
	.string "\nwhile swimming,"
	.string "\ltoo!$"

Unova_Rt17_Text_SwimmerM2R17BeatenText::
	.string "I lost, but I'm"
	.string "\nstill cool. Not"
	.string "\pmany people can"
	.string "\nsay they've"
	.string "\pbattled while"
	.string "\nswimming!$"

Unova_Rt17_Text_SwimmerF1R17SeenText::
	.string "Time for an"
	.string "\naquatic battle in"
	.string "\lthe sea!$"

Unova_Rt17_Text_SwimmerF1R17BeatenText::
	.string "I'm just going to"
	.string "\nfloat on by…$"

Unova_Rt17_Text_SwimmerF2R17SeenText::
	.string "Seeing a POKéMON"
	.string "\nuse its best moves"
	.string "\pagainst another"
	.string "\nPOKéMON is really"
	.string "\lan adventure!$"

Unova_Rt17_Text_SwimmerF2R17BeatenText::
	.string "The adventure is"
	.string "\nover already.$"

Unova_Rt17_Text_R17DoctorIntroText::
	.string "I'm a doctor, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_Rt17_Text_R17DoctorWinText::
	.string "Ah, I see.$"
