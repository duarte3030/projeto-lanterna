Route209LostTower3F_MapScripts::
	.byte 0

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route209LostTower3F_EventScript_PokefanLeonard::
	trainerbattle_single TRAINER_SINNOH_POKEFAN_LEONARD, Route209LostTower3F_Text_PokefanLeonardIntro, Route209LostTower3F_Text_PokefanLeonardDefeat
	msgbox Route209LostTower3F_Text_PokefanLeonardPost, MSGBOX_AUTOCLOSE
	end

Route209LostTower3F_Text_PokefanLeonardIntro:
	.string "I can't explain it...\nBeing here compels me to battle!$"

Route209LostTower3F_Text_PokefanLeonardDefeat:
	.string "Hunh?!\nWhat was I just doing?!$"

Route209LostTower3F_Text_PokefanLeonardPost:
	.string "The desire to do battle lingers on...\pDo such spirits of Pokémon still roam\nwithin these walls?$"

Route209LostTower3F_EventScript_RoughneckKirby::
	trainerbattle_single TRAINER_SINNOH_ROUGHNECK_KIRBY, Route209LostTower3F_Text_RoughneckKirbyIntro, Route209LostTower3F_Text_RoughneckKirbyDefeat
	msgbox Route209LostTower3F_Text_RoughneckKirbyPost, MSGBOX_AUTOCLOSE
	end

Route209LostTower3F_Text_RoughneckKirbyIntro:
	.string "My Pokémon were taken from me...\nTeam Galactic did it...\pEver since, I've never forgiven\ntheir faces...$"

Route209LostTower3F_Text_RoughneckKirbyDefeat:
	.string "Gwaaaaaah!$"

Route209LostTower3F_Text_RoughneckKirbyPost:
	.string "I'm not doing my Pokémon any favors\nby ruining its memory like this...\pI can't be wallowing around forever.\nI gotta move on and turn the page.$"
