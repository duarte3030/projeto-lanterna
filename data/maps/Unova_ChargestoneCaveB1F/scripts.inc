@ ChargestoneCaveB1F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_ChargestoneCaveB1F_MapScripts::
	.byte 0

Unova_ChargestoneCaveB1F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_ACE_TRAINERF_CHARGESTONE_2, Unova_ChargestoneCaveB1F_Text_AceTrainerF2ChargestoneSeenText, Unova_ChargestoneCaveB1F_Text_AceTrainerF2ChargestoneBeatenText
	end

Unova_ChargestoneCaveB1F_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_HIKER_CHARGESTONE_2, Unova_ChargestoneCaveB1F_Text_Hiker2ChargestoneSeenText, Unova_ChargestoneCaveB1F_Text_Hiker2ChargestoneBeatenText
	end

Unova_ChargestoneCaveB1F_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_BATTLE_GIRL_CHARGESTONE, Unova_ChargestoneCaveB1F_Text_BattleGirlChargestoneSeenText, Unova_ChargestoneCaveB1F_Text_BattleGirlChargestoneBeatenText
	end

Unova_ChargestoneCaveB1F_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_DOCTOR_CHARGESTONE, Unova_ChargestoneCaveB1F_Text_ChargestoneDoctorIntroText, Unova_ChargestoneCaveB1F_Text_ChargestoneDoctorWinText
	end

Unova_ChargestoneCaveB1F_EventScript_Lider7::
	trainerbattle_single TRAINER_UNOVA_SCIENTISTF_CHARGESTONE, Unova_ChargestoneCaveB1F_Text_ScientistFChargestoneSeenText, Unova_ChargestoneCaveB1F_Text_ScientistFChargestoneBeatenText
	end

Unova_ChargestoneCaveB1F_EventScript_Lider8::
	trainerbattle_single TRAINER_UNOVA_PKMN_RANGERM_CHARGESTONE, Unova_ChargestoneCaveB1F_Text_PkmnRangerMChargestoneSeenText, Unova_ChargestoneCaveB1F_Text_PkmnRangerMChargestoneBeatenText
	end


Unova_ChargestoneCaveB1F_Text_AceTrainerF2ChargestoneSeenText::
	.string "My beloved POKéMON"
	.string "\nwill make their"
	.string "\ldebut!$"

Unova_ChargestoneCaveB1F_Text_AceTrainerF2ChargestoneBeatenText::
	.string "You were the one"
	.string "\nwith the stronger"
	.string "\lpower as a team!$"

Unova_ChargestoneCaveB1F_Text_Hiker2ChargestoneSeenText::
	.string "When I say dig,"
	.string "\nsay, How low?$"

Unova_ChargestoneCaveB1F_Text_Hiker2ChargestoneBeatenText::
	.string "I didn't notice"
	.string "\nthe pitfall!$"

Unova_ChargestoneCaveB1F_Text_BattleGirlChargestoneSeenText::
	.string "Ai! Ai! Ai!"
	.string "\nHi-yaaah!$"

Unova_ChargestoneCaveB1F_Text_BattleGirlChargestoneBeatenText::
	.string "Aww… It was my"
	.string "\nturn next…$"

Unova_ChargestoneCaveB1F_Text_ChargestoneDoctorIntroText::
	.string "I'm a doctor, but"
	.string "\nI'm also a POKé-"
	.string "\lMON trainer."
	.string "\pIf you can defeat"
	.string "\nme in a battle,"
	.string "\lI'll heal your"
	.string "\lPOKéMON.$"

Unova_ChargestoneCaveB1F_Text_ChargestoneDoctorWinText::
	.string "Ah, I see.$"

Unova_ChargestoneCaveB1F_Text_ScientistFChargestoneSeenText::
	.string "I love this place!"
	.string "\nThe electricity"
	.string "\pcharges up my"
	.string "\ninspiration!$"

Unova_ChargestoneCaveB1F_Text_ScientistFChargestoneBeatenText::
	.string "Aha! A lightbulb"
	.string "\nwent off in my"
	.string "\lhead!$"

Unova_ChargestoneCaveB1F_Text_PkmnRangerMChargestoneSeenText::
	.string "I am a POKéMON"
	.string "\nRANGER, here to"
	.string "\pgather up some"
	.string "\nelectric power!$"

Unova_ChargestoneCaveB1F_Text_PkmnRangerMChargestoneBeatenText::
	.string "I still can't draw"
	.string "\nforth my electric"
	.string "\lpowers!$"
