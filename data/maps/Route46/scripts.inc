@ Treinadores de rota de Route46, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

Route46_MapScripts::
	.byte 0

Route46_EventScript_Bailey::
	trainerbattle_single TRAINER_JOHTO_BAILEY, Route46_Text_BaileySeen, Route46_Text_BaileyBeaten
	msgbox Route46_Text_BaileyAfter, MSGBOX_AUTOCLOSE
	end

Route46_EventScript_Ted::
	trainerbattle_single TRAINER_JOHTO_TED, Route46_Text_TedSeen, Route46_Text_TedBeaten
	msgbox Route46_Text_TedAfter, MSGBOX_AUTOCLOSE
	end

Route46_EventScript_Erin::
	trainerbattle_single TRAINER_JOHTO_ERIN, Route46_Text_ErinSeen, Route46_Text_ErinBeaten
	msgbox Route46_Text_ErinAfter, MSGBOX_AUTOCLOSE
	end

Route46_Text_BaileySeen:
	.string "Awright! I'll show you the\n"
	.string "power of mountain POKéMON!$"

Route46_Text_BaileyBeaten:
	.string "Mercy! You showed me your\n"
	.string "power!$"

Route46_Text_BaileyAfter:
	.string "It's over. I don't mind.\n"
	.string "We HIKERS are like that.$"

Route46_Text_TedSeen:
	.string "I'm raising POKéMON too!\p"
	.string "Will you battle with me?$"

Route46_Text_TedBeaten:
	.string "Wha…?$"

Route46_Text_TedAfter:
	.string "I did my best but came up\n"
	.string "short.\p"
	.string "No excuses--I admit I lost.$"

Route46_Text_ErinSeen:
	.string "I raise POKéMON too!\p"
	.string "Will you battle with me?$"

Route46_Text_ErinBeaten:
	.string "Oh, rats!$"

Route46_Text_ErinAfter:
	.string "I've been to many GYMS, but the\n"
	.string "GYM in GOLDENROD is my favorite.\p"
	.string "It's filled with pretty flowers!$"
