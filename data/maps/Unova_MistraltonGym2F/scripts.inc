@ MistraltonGym2F do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

Unova_MistraltonGym2F_MapScripts::
	.byte 0

Unova_MistraltonGym2F_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_PILOT_MISTRALTON_GYM_4, Unova_MistraltonGym2F_Text_Pilot1MistraltonGym2FSeenText, Unova_MistraltonGym2F_Text_Pilot1MistraltonGym2FBeatenText
	end

Unova_MistraltonGym2F_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_PILOT_MISTRALTON_GYM_5, Unova_MistraltonGym2F_Text_Pilot2MistraltonGym2FSeenText, Unova_MistraltonGym2F_Text_Pilot2MistraltonGym2FBeatenText
	end


Unova_MistraltonGym2F_Text_Pilot1MistraltonGym2FSeenText::
	.string "Can you figure out"
	.string "\nhow to get through"
	.string "\lour GYM?$"

Unova_MistraltonGym2F_Text_Pilot1MistraltonGym2FBeatenText::
	.string "I was beaten!$"

Unova_MistraltonGym2F_Text_Pilot2MistraltonGym2FSeenText::
	.string "My POKéMON are"
	.string "\nstronger than the"
	.string "\pwind! They're my"
	.string "\npride and joy!$"

Unova_MistraltonGym2F_Text_Pilot2MistraltonGym2FBeatenText::
	.string "They may be"
	.string "\nstronger than the"
	.string "\pwind, but they're"
	.string "\nnot as strong as"
	.string "\lyours!$"
