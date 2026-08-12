StarkMountainOutside_MapScripts::
	.byte 0

@ Treinador do pokeplatinum que os dois scripts irmaos nao alcancam
@ (dev_scripts/treinadores_faltantes_sinnoh.py)

StarkMountainOutside_EventScript_DragonTamerDarien::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_DARIEN, StarkMountainOutside_Text_DragonTamerDarienIntro, StarkMountainOutside_Text_DragonTamerDarienDefeat
	msgbox StarkMountainOutside_Text_DragonTamerDarienPost, MSGBOX_AUTOCLOSE
	end

StarkMountainOutside_Text_DragonTamerDarienIntro:
	.string "My Pokémon and I seek only victory!$"

StarkMountainOutside_Text_DragonTamerDarienDefeat:
	.string "Arrrgh! My Pokémon...$"

StarkMountainOutside_Text_DragonTamerDarienPost:
	.string "I failed my Pokémon!\nI wasn't prepared enough to lead it!\pI don't ever want my precious Pokémon\nto be humiliated again!$"
