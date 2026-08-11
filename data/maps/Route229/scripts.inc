@ Referencia de treinador de Sinnoh. Ver Pokemon Claude/SINNOH-PADRAO.md.
@ Falas vindas de pret/pokeplatinum, em ingles, como o resto do jogo.

Route229_MapScripts::
	.byte 0

Route229_EventScript_RangerDeshawn::
	trainerbattle_single TRAINER_SINNOH_RANGER_DESHAWN, Route229_Text_RangerDeshawnIntro, Route229_Text_RangerDeshawnDefeat
	msgbox Route229_Text_RangerDeshawnPost, MSGBOX_AUTOCLOSE
	end

Route229_EventScript_AceTrainerFelix::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_FELIX, Route229_Text_AceTrainerFelixIntro, Route229_Text_AceTrainerFelixDefeat
	msgbox Route229_Text_AceTrainerFelixPost, MSGBOX_AUTOCLOSE
	end

Route229_EventScript_AceTrainerDana::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_DANA, Route229_Text_AceTrainerDanaIntro, Route229_Text_AceTrainerDanaDefeat
	msgbox Route229_Text_AceTrainerDanaPost, MSGBOX_AUTOCLOSE
	end

Route229_EventScript_AceTrainerSandra::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_SANDRA, Route229_Text_AceTrainerSandraIntro, Route229_Text_AceTrainerSandraDefeat
	msgbox Route229_Text_AceTrainerSandraPost, MSGBOX_AUTOCLOSE
	end

Route229_EventScript_Pokefan::
	msgbox Route229_Text_Pokefan, MSGBOX_NPC
	end

Route229_Text_RangerDeshawnIntro:
	.string "I work to protect beautiful, natural\n"
	.string "environments.\p"
	.string "My Pokémon are my constant\n"
	.string "companions while I work.$"

Route229_Text_RangerDeshawnDefeat:
	.string "Oh, my gosh!\n"
	.string "My poor Pokémon!$"

Route229_Text_RangerDeshawnPost:
	.string "Everyone can do their part to keep\n"
	.string "nature clean. It doesn't take much.$"

Route229_Text_AceTrainerFelixIntro:
	.string "Welcome to my Pokémon show!$"

Route229_Text_AceTrainerFelixDefeat:
	.string "Did you enjoy the show?\n"
	.string "Super fabulous, wasn't it?$"

Route229_Text_AceTrainerFelixPost:
	.string "I'll be happy to battle you again!\n"
	.string "Let's battle again sometime, yeah?$"

Route229_Text_AceTrainerDanaIntro:
	.string "You're willing to battle?\n"
	.string "Let me see what you have?$"

Route229_Text_AceTrainerDanaDefeat:
	.string "Your love of Pokémon really shows!$"

Route229_Text_AceTrainerDanaPost:
	.string "I grew up together with Felix and\n"
	.string "my team, right from my childhood.\p"
	.string "All our memories, we've always shared\n"
	.string "them.$"

Route229_Text_AceTrainerSandraIntro:
	.string "When eyes meet...\n"
	.string "That's when a battle starts!$"

Route229_Text_AceTrainerSandraDefeat:
	.string "You won't let me win?$"

Route229_Text_AceTrainerSandraPost:
	.string "I suddenly remembered what it was\n"
	.string "like when I had my first battle.\p"
	.string "I wonder why that would be?$"

Route229_Text_Pokefan:
	.string "Were you looking for me? Did you\n"
	.string "miss me? I wish I had a new nugget\l"
	.string "of wisdom to share with you, but\p"
	.string "alas, I don't!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route229_EventScript_Placa1::
	msgbox Route229_Text_Placa1, MSGBOX_SIGN
	end

Route229_Text_Placa1:
	.string "Rt. 229\nResort Area$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route229_EventScript_Npc1::
	msgbox Route229_Text_Npc1, MSGBOX_NPC
	end

Route229_Text_Npc1:
	.string "Were you looking for me?\nDid you miss me?\pI wish I had a new nugget of wisdom\nto share with you, but alas, I don't!\pSo, I'll have to make it up to you\nwith this!$"
