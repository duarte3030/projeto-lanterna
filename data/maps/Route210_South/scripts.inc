Route210_South_MapScripts::
	.byte 0

Route210_South_EventScript_AceTrainer::
	msgbox Route210_South_Text_AceTrainer, MSGBOX_NPC
	end

Route210_South_EventScript_Breeder::
	msgbox Route210_South_Text_Breeder, MSGBOX_NPC
	end

Route210_South_EventScript_Rancher::
	msgbox Route210_South_Text_Rancher, MSGBOX_NPC
	end

Route210_South_EventScript_Belle::
	msgbox Route210_South_Text_Belle, MSGBOX_NPC
	end

Route210_South_Text_AceTrainer:
	.string "I'm taking a rest. If I were a\n"
	.string "bird Pokémon, it would be a roost.$"

Route210_South_Text_Breeder:
	.string "I'm walking my Pokémon to keep\n"
	.string "them happy and healthy.$"

Route210_South_Text_Rancher:
	.string "The Pokémon Day Care is just\n"
	.string "down the road in Solaceon.$"

Route210_South_Text_Belle:
	.string "Pa and I raise Miltank here.\n"
	.string "Come say hi anytime.$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route210_South_EventScript_Placa1::
	msgbox Route210_South_Text_Placa1, MSGBOX_SIGN
	end

Route210_South_Text_Placa1:
	.string "Rt. 210\nSolaceon Town$"

Route210_South_EventScript_Placa2::
	msgbox Route210_South_Text_Placa2, MSGBOX_SIGN
	end

Route210_South_Text_Placa2:
	.string "Café Cabin\nFreshly Squeezed Milk$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route210_South_EventScript_Npc1::
	msgbox Route210_South_Text_Npc1, MSGBOX_NPC
	end

Route210_South_Text_Npc1:
	.string "I'm taking a rest. If I were a bird\nPokémon, it would be a roost. Haha!\pUh... You should rest up, too.$"
