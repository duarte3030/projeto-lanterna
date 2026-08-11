IronIslandB1FLeftRoom_MapScripts::
	.byte 0

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

IronIslandB1FLeftRoom_EventScript_CamperLawrence::
	trainerbattle_single TRAINER_SINNOH_CAMPER_LAWRENCE, IronIslandB1FLeftRoom_Text_CamperLawrenceIntro, IronIslandB1FLeftRoom_Text_CamperLawrenceDefeat
	msgbox IronIslandB1FLeftRoom_Text_CamperLawrencePost, MSGBOX_AUTOCLOSE
	end

IronIslandB1FLeftRoom_Text_CamperLawrenceIntro:
	.string "Yeah, I like to camp! So what?\nLet's battle!$"

IronIslandB1FLeftRoom_Text_CamperLawrenceDefeat:
	.string "I should've just stuck to\ncamping out here...$"

IronIslandB1FLeftRoom_Text_CamperLawrencePost:
	.string "When I'm with my Pokémon, I can camp\njust about anywhere I want!$"
