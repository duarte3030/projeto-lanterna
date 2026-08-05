@ VirbankGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_VirbankGym_MapScripts::
	.byte 0

Unova_VirbankGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_ROXIE, Unova_VirbankGym_Text_RoxieGymIntroText, Unova_VirbankGym_Text_RoxieWinLossText, Unova_VirbankGym_EventScript_Insignia0
	end

Unova_VirbankGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_VIRBANK
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_VirbankGym_EventScript_Lider1::
	trainerbattle_single TRAINER_UNOVA_GUITARIST_VIRBANK_GYM_1, Unova_VirbankGym_Text_GuitaristVirbankGym1SeenText, Unova_VirbankGym_Text_GuitaristVirbankGym1BeatenText
	end

Unova_VirbankGym_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_GUITARIST_VIRBANK_GYM_2, Unova_VirbankGym_Text_GuitaristVirbankGym2SeenText, Unova_VirbankGym_Text_GuitaristVirbankGym2BeatenText
	end

Unova_VirbankGym_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_MUSICIAN_VIRBANK_GYM_1, Unova_VirbankGym_Text_MusicianVirbankGym1SeenText, Unova_VirbankGym_Text_MusicianVirbankGym1BeatenText
	end

Unova_VirbankGym_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_MUSICIAN_VIRBANK_GYM_2, Unova_VirbankGym_Text_MusicianVirbankGym2SeenText, Unova_VirbankGym_Text_MusicianVirbankGym2BeatenText
	end


Unova_VirbankGym_Text_RoxieGymIntroText::
	.string "Get ready! I'm"
	.string "\ngonna knock some"
	.string "\lsense outta ya!$"

Unova_VirbankGym_Text_RoxieWinLossText::
	.string "Wait! I was right"
	.string "\nin the middle of"
	.string "\lthe chorus!$"

Unova_VirbankGym_Text_GuitaristVirbankGym1SeenText::
	.string "I'm going to take"
	.string "\nyou down! Prepare"
	.string "\lto be stung!$"

Unova_VirbankGym_Text_GuitaristVirbankGym1BeatenText::
	.string "Gwaaah!"
	.string "\nI was overpowered…$"

Unova_VirbankGym_Text_GuitaristVirbankGym2SeenText::
	.string "Get in my way, and"
	.string "\nI'll knock you"
	.string "\pout! Stay out of"
	.string "\nmy way… and I'll"
	.string "\lknock you out too!$"

Unova_VirbankGym_Text_GuitaristVirbankGym2BeatenText::
	.string "I'm the one who"
	.string "\ngot knocked out!$"

Unova_VirbankGym_Text_MusicianVirbankGym1SeenText::
	.string "Hold it there,"
	.string "\nkid. This is an"
	.string "\lexclusive club.$"

Unova_VirbankGym_Text_MusicianVirbankGym1BeatenText::
	.string "Ah! Come right in!$"

Unova_VirbankGym_Text_MusicianVirbankGym2SeenText::
	.string "I can always be"
	.string "\nhonest with myself"
	.string "\pwhen I'm playing"
	.string "\nthe guitar or"
	.string "\phaving a POKéMON"
	.string "\nbattle!$"

Unova_VirbankGym_Text_MusicianVirbankGym2BeatenText::
	.string "Argh! The happy"
	.string "\ntimes always end"
	.string "\lso quickly!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ jumpstd gymstatue1 do BW3G: nome do mapa + "#MON GYM"
Unova_VirbankGym_EventScript_EstatuaGinasio::
	msgbox Unova_VirbankGym_Text_EstatuaGinasio, MSGBOX_SIGN
	end

Unova_VirbankGym_Text_EstatuaGinasio::
	.string "VIRBANK CITY\n"
	.string "POKéMON GYM$"
