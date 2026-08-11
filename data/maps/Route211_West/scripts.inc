Route211_West_MapScripts::
	.byte 0

Route211_West_EventScript_BirdKeeper::
	msgbox Route211_West_Text_BirdKeeper, MSGBOX_NPC
	end

Route211_West_EventScript_Hiker::
	msgbox Route211_West_Text_Hiker, MSGBOX_NPC
	end

Route211_West_EventScript_NinjaBoy::
	msgbox Route211_West_Text_NinjaBoy, MSGBOX_NPC
	end

Route211_West_Text_BirdKeeper:
	.string "Eterna City is close now.\n"
	.string "Almost through the mountain.$"

Route211_West_Text_Hiker:
	.string "Mt. Coronet splits Sinnoh\n"
	.string "right down the middle.$"

Route211_West_Text_NinjaBoy:
	.string "Heh, you found me. I like to\n"
	.string "hide in the tall grass.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route211_West_EventScript_Placa1::
	msgbox Route211_West_Text_Placa1, MSGBOX_SIGN
	end

Route211_West_Text_Placa1:
	.string "Rt. 211\nMt. Coronet$"

Route211_West_EventScript_Placa2::
	msgbox Route211_West_Text_Placa2, MSGBOX_SIGN
	end

Route211_West_Text_Placa2:
	.string "Rt. 211\nEterna City$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route211_West_EventScript_BirdKeeperAlexandra::
	trainerbattle_single TRAINER_SINNOH_BIRD_KEEPER_ALEXANDRA, Route211_West_Text_BirdKeeperAlexandraIntro, Route211_West_Text_BirdKeeperAlexandraDefeat
	msgbox Route211_West_Text_BirdKeeperAlexandraPost, MSGBOX_AUTOCLOSE
	end

Route211_West_Text_BirdKeeperAlexandraIntro:
	.string "Look at these beautiful wings!$"

Route211_West_Text_BirdKeeperAlexandraDefeat:
	.string "Oh, you!\nI'm going to peck you for that!$"

Route211_West_Text_BirdKeeperAlexandraPost:
	.string "There's a bird Pokémon that can learn\nhuman speech! Did you know that?$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route211_West_EventScript_HikerLouis::
	trainerbattle_single TRAINER_SINNOH_HIKER_LOUIS, Route211_West_Text_HikerLouisIntro, Route211_West_Text_HikerLouisDefeat
	msgbox Route211_West_Text_HikerLouisPost, MSGBOX_AUTOCLOSE
	end

Route211_West_Text_HikerLouisIntro:
	.string "See how Mt. Coronet towers above us.\nI want to be big like that one day!$"

Route211_West_Text_HikerLouisDefeat:
	.string "You loom before me as a giant presence!$"

Route211_West_Text_HikerLouisPost:
	.string "Mt. Coronet has long been known as\nan ancient and mysterious mountain.$"

Route211_West_EventScript_NinjaBoyZach::
	trainerbattle_single TRAINER_SINNOH_NINJA_BOY_ZACH, Route211_West_Text_NinjaBoyZachIntro, Route211_West_Text_NinjaBoyZachDefeat
	msgbox Route211_West_Text_NinjaBoyZachPost, MSGBOX_AUTOCLOSE
	end

Route211_West_Text_NinjaBoyZachIntro:
	.string "ZUBAT! Doesn't that sound like a\nninja bursting from cover?$"

Route211_West_Text_NinjaBoyZachDefeat:
	.string "Oh!\nMy ZUBAT tristars...$"

Route211_West_Text_NinjaBoyZachPost:
	.string "Sowing confusion among the foe is\none way a ninja battles.\pA Pokémon can't overcome its\nconfusion unless it switches out.$"
