Route209LostTower2F_MapScripts::
	.byte 0

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route209LostTower2F_EventScript_YoungsterOliver::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_OLIVER, Route209LostTower2F_Text_YoungsterOliverIntro, Route209LostTower2F_Text_YoungsterOliverDefeat
	msgbox Route209LostTower2F_Text_YoungsterOliverPost, MSGBOX_AUTOCLOSE
	end

Route209LostTower2F_Text_YoungsterOliverIntro:
	.string "Waah! Ghost! Get away! Eek!\nHelp me, team!$"

Route209LostTower2F_Text_YoungsterOliverDefeat:
	.string "Hey...\nYou're no ghost...$"

Route209LostTower2F_Text_YoungsterOliverPost:
	.string "I had to come to the Lost Tower on\na dare...\pI have to go to the top and use Defog\nthere...$"
