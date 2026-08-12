Route219_MapScripts::
	.byte 0

Route219_EventScript_BeachSign::
	msgbox Route219_Text_BeachSign, MSGBOX_SIGN
	end

Route219_Text_BeachSign:
	.string "SANDGEM BEACH\n"
	.string "This way.$"

Route219_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_TUBER_TRENTON, Route219_Text_Trainer1Intro, Route219_Text_Trainer1Defeat
	msgbox Route219_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route219_Text_Trainer1Intro:
	.string "I love my inflatable tube.\nSo I admire jellyfish Pokémon!\p$"

Route219_Text_Trainer1Defeat:
	.string "I'm drifting away...\n$"

Route219_Text_Trainer1Post:
	.string "I wish Professor Rowan would\ngive me a Pokédex.\pBut that old guy looks kind of\nscary.\n$"

Route219_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_TUBER_MARIEL, Route219_Text_Trainer2Intro, Route219_Text_Trainer2Defeat
	msgbox Route219_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route219_Text_Trainer2Intro:
	.string "I can't swim without my inflatable tube.\nBut my Pokémon might be strong!\p$"

Route219_Text_Trainer2Defeat:
	.string "They weren't tough, my Pokémon...\n$"

Route219_Text_Trainer2Post:
	.string "My mommy said that Professor Rowan\nis really kindhearted.$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route219_EventScript_Placa1::
	msgbox Route219_Text_Placa1, MSGBOX_SIGN
	end

Route219_Text_Placa1:
	.string "Rt. 219\nSandgem Beach$"
