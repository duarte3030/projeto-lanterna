Route221_MapScripts::
	.byte 0

Route221_EventScript_SignPalPark::
	msgbox Route221_Text_SignPalPark, MSGBOX_SIGN
	end

Route221_Text_SignPalPark:
	.string "PAL PARK\n"
	.string "Straight ahead.$"

Route221_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_DILLON, Route221_Text_Trainer1Intro, Route221_Text_Trainer1Defeat
	msgbox Route221_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route221_Text_Trainer1Intro:
	.string "Well? Does it look like I'm swimming\ngracefully?\p$"

Route221_Text_Trainer1Defeat:
	.string "I'm finally feeling fatigued...\n$"

Route221_Text_Trainer1Post:
	.string "I may look like I'm swimming\ngracefully, but beneath the surface\pI'm kicking furiously.\n$"

Route221_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_SWIMMER_VANESSA, Route221_Text_Trainer2Intro, Route221_Text_Trainer2Defeat
	msgbox Route221_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route221_Text_Trainer2Intro:
	.string "One thing about Water-type Pokémon:\nThere's a huge variety!\pI'll show you the Water-type Pokémon I\nchose and why I'm so proud of them!\p$"

Route221_Text_Trainer2Defeat:
	.string "I can't boast when I lose...\nI'm so disappointed...\n$"

Route221_Text_Trainer2Post:
	.string "Sure I lost, but watch me! I'll get\ntougher with water Pokémon.\n$"

Route221_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_CORY, Route221_Text_Trainer3Intro, Route221_Text_Trainer3Defeat
	msgbox Route221_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route221_Text_Trainer3Intro:
	.string "I like fishing, no question.\nBut battling? That's what I love!\p$"

Route221_Text_Trainer3Defeat:
	.string "Sploosh!\n$"

Route221_Text_Trainer3Post:
	.string "If you don't know how to fish, you're\nmissing half of life's enjoyment.\pIf you don't know Pokémon...\nYou're missing out on all of it!\n$"


Route221_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_COLLECTOR_IVAN, Route221_Text_Trainer4Intro, Route221_Text_Trainer4Defeat
	msgbox Route221_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route221_Text_Trainer4Intro:
	.string "Are you going to the Pal Park, too?\pFor you, I'm willing to show off my\nprized Pokémon!\p$"

Route221_Text_Trainer4Defeat:
	.string "So? Hot stuff, huh?\nThat's why I'm so proud of my Pokémon!\n$"

Route221_Text_Trainer4Post:
	.string "Pal Park, huh? I wonder what kinds\nof Pokémon you can see there?\n$"

Route221_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_JAKE, Route221_Text_Trainer5Intro, Route221_Text_Trainer5Defeat
	msgbox Route221_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route221_Text_Trainer5Intro:
	.string "They call me an Ace Trainer.\pAllow me to demonstrate the talent\nthat makes me so!\p$"

Route221_Text_Trainer5Defeat:
	.string "I'm burning with jealousy over your\nraw talent!\n$"

Route221_Text_Trainer5Post:
	.string "I think keeping up the effort to\nbetter yourself is a talent in itself.\n$"

Route221_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_SHANNON, Route221_Text_Trainer6Intro, Route221_Text_Trainer6Defeat
	msgbox Route221_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route221_Text_Trainer6Intro:
	.string "Really? So you think you can beat me?\nI'm an Ace Trainer, you do realize?\p$"

Route221_Text_Trainer6Defeat:
	.string "I admit defeat...\n$"

Route221_Text_Trainer6Post:
	.string "Beaten in battle, but not in spirit.\nThat's the mark of a real Ace Trainer.\n$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route221_EventScript_Placa1::
	msgbox Route221_Text_Placa1, MSGBOX_SIGN
	end

Route221_Text_Placa1:
	.string "Pal Park\nA Place for New Beginnings$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
Route221_EventScript_PortaFechada::
	msgbox Route221_Text_PortaFechada, MSGBOX_SIGN
	end

Route221_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
