@ SeasideCave1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_SeasideCave1F_MapScripts::
	.byte 0

Unova_SeasideCave1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_DOCTOR_SEASIDE_CAVE, Unova_SeasideCave1F_Text_SeasideCaveDoctorIntroText, Unova_SeasideCave1F_Text_SeasideCaveDoctorWinText
	end

Unova_SeasideCave1F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_VETERANF_SEASIDE_CAVE, Unova_SeasideCave1F_Text_VeteranFSeasideCave1FSeenText, Unova_SeasideCave1F_Text_VeteranFSeasideCave1FBeatenText
	end

Unova_SeasideCave1F_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_BLACKBELT_SEASIDE_CAVE_1, Unova_SeasideCave1F_Text_BlackbeltSeasideCave1FSeenText, Unova_SeasideCave1F_Text_BlackbeltSeasideCave1FBeatenText
	end

Unova_SeasideCave1F_EventScript_Lider9::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_SEASIDE_CAVE_1, Unova_SeasideCave1F_Text_BattleGirlSeasideCave1FSeenText, Unova_SeasideCave1F_Text_BattleGirlSeasideCave1FBeatenText
	end


Unova_SeasideCave1F_Text_SeasideCaveDoctorIntroText::
	.string "I'm a doctor, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_SeasideCave1F_Text_SeasideCaveDoctorWinText::
	.string "Ah, I see.$"

Unova_SeasideCave1F_Text_VeteranFSeasideCave1FSeenText::
	.string "Let me show you"
	.string "\nthe POKéMON that I"
	.string "\lmet by fate!$"

Unova_SeasideCave1F_Text_VeteranFSeasideCave1FBeatenText::
	.string "The POKéMON that"
	.string "\nyou've met are"
	.string "\pquite formidable,"
	.string "\naren't they?$"

Unova_SeasideCave1F_Text_BlackbeltSeasideCave1FSeenText::
	.string "The path of karate"
	.string "\nis the path of"
	.string "\phumanity… and the"
	.string "\npath of POKéMON!$"

Unova_SeasideCave1F_Text_BlackbeltSeasideCave1FBeatenText::
	.string "Oof! It is not by"
	.string "\nchance that you"
	.string "\lhave won!$"

Unova_SeasideCave1F_Text_BattleGirlSeasideCave1FSeenText::
	.string "Greetings! So…"
	.string "\nshall we do this?$"

Unova_SeasideCave1F_Text_BattleGirlSeasideCave1FBeatenText::
	.string "What an upset!$"
