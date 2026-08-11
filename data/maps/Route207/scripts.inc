Route207_MapScripts::
	.byte 0

Route207_EventScript_Cyclist::
	msgbox Route207_Text_Cyclist, MSGBOX_NPC
	end

Route207_EventScript_Camper::
	msgbox Route207_Text_Camper, MSGBOX_NPC
	end

Route207_EventScript_Picnicker::
	msgbox Route207_Text_Picnicker, MSGBOX_NPC
	end

Route207_EventScript_Hiker::
	msgbox Route207_Text_Hiker, MSGBOX_NPC
	end

Route207_Text_Cyclist:
	.string "That slope's too slippery.\n"
	.string "You'll need a Bike to get up.\p"
	.string "There's a Cycle Shop in\n"
	.string "Eterna City if you need one.$"

Route207_Text_Camper:
	.string "I love pitching a tent out here.\n"
	.string "The stars are amazing at night.$"

Route207_Text_Picnicker:
	.string "I packed way too many PokéBlocks\n"
	.string "for this trip. Want to trade?$"

Route207_Text_Hiker:
	.string "Watch your step around here.\n"
	.string "The cave entrance drops off fast.$"

Route207_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_CAMPER_ANTHONY, Route207_Text_Trainer1Intro, Route207_Text_Trainer1Defeat
	msgbox Route207_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer1Intro:
	.string "Go for it, my Pokémon!\n"
	.string "I'll do my best, too!$"

Route207_Text_Trainer1Defeat:
	.string "Oh...\n"
	.string "We lost...$"

Route207_Text_Trainer1Post:
	.string "Dig for Fossils in the Underground.\pThe mining museum might be able to\n"
	.string "bring back the ancient Pokémon!$"

Route207_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_LAUREN, Route207_Text_Trainer2Intro, Route207_Text_Trainer2Defeat
	msgbox Route207_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer2Intro:
	.string "Go do it, my Pokémon!\n"
	.string "I'll work hard, too!$"

Route207_Text_Trainer2Defeat:
	.string "Oh...\n"
	.string "We lost...$"

Route207_Text_Trainer2Post:
	.string "I think we'll visit the TV station in\n"
	.string "Jubilife City next.\pOr maybe we should go to the Global\n"
	.string "Terminal?$"

Route207_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_AUSTIN, Route207_Text_Trainer3Intro, Route207_Text_Trainer3Defeat
	msgbox Route207_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer3Intro:
	.string "I wear shorts the whole year!\n"
	.string "I've got energy to burn!$"

Route207_Text_Trainer3Defeat:
	.string "I couldn't win with just energy...\n"
	.string "Nothing's really that easy!$"

Route207_Text_Trainer3Post:
	.string "Pokémon don't wear clothes.\n"
	.string "I worry about them getting cold.$"

Route207_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_HIKER_JUSTIN, Route207_Text_Trainer4Intro, Route207_Text_Trainer4Defeat
	msgbox Route207_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer4Intro:
	.string "I just got through Mt. Coronet, but\n"
	.string "I've still got energy to burn!$"

Route207_Text_Trainer4Defeat:
	.string "Whoops!\n"
	.string "Taken down easily!$"

Route207_Text_Trainer4Post:
	.string "We need to rest up in Oreburgh City\n"
	.string "before heading to Mt. Coronet again.$"

Route207_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_HIKER_KEVIN, Route207_Text_Trainer5Intro, Route207_Text_Trainer5Defeat
	msgbox Route207_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer5Intro:
	.string "Wahaha!\n"
	.string "Laughter brings good fortune!$"

Route207_Text_Trainer5Defeat:
	.string "Wahahaha! There's nothing that\n"
	.string "I can do but laugh!$"

Route207_Text_Trainer5Post:
	.string "Wahahahaha!\n"
	.string "...Go ahead, laugh at me--the loser!$"

Route207_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_BATTLE_GIRL_HELEN, Route207_Text_Trainer6Intro, Route207_Text_Trainer6Defeat
	msgbox Route207_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route207_Text_Trainer6Intro:
	.string "OK, OK!\n"
	.string "Let's be quick about this!$"

Route207_Text_Trainer6Defeat:
	.string "Oh, yeah? Let's do this again!\n"
	.string "...Oops. I'm out of Pokémon!$"

Route207_Text_Trainer6Post:
	.string "Yup! Good going!\n"
	.string "I like the way you battle!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route207_EventScript_Placa1::
	msgbox Route207_Text_Placa1, MSGBOX_SIGN
	end

Route207_Text_Placa1:
	.string "Rt. 207\nOreburgh City$"

Route207_EventScript_Placa2::
	msgbox Route207_Text_Placa2, MSGBOX_SIGN
	end

Route207_Text_Placa2:
	.string "Rt. 207\nMt. Coronet$"

Route207_EventScript_Placa3::
	msgbox Route207_Text_Placa3, MSGBOX_SIGN
	end

Route207_Text_Placa3:
	.string "Trainer Tips\pPokémon may become immobilized if\nthey are asleep or paralyzed.\pIf it happens to your Pokémon,\nit could be disastrous.\pIf your opponent's Pokémon can't\nmove, it's a big opportunity!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route207_EventScript_Npc1::
	msgbox Route207_Text_Npc1, MSGBOX_NPC
	end

Route207_Text_Npc1:
	.string "That slope's too slippery.\nYou'll need a Bike to get up.\pYou don't have a Bicycle?\nThere's a Cycle Shop in Eterna City.$"
