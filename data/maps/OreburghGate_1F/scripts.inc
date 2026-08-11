OreburghGate_1F_MapScripts::
	.byte 0

OreburghGate_1F_EventScript_Hiker1::
	msgbox OreburghGate_1F_Text_Hiker1, MSGBOX_NPC
	end

OreburghGate_1F_EventScript_Hiker2::
	msgbox OreburghGate_1F_Text_Hiker2, MSGBOX_NPC
	end

OreburghGate_1F_Text_Hiker1:
	.string "This gate connects OREBURGH CITY to\n"
	.string "the routes beyond.\p"
	.string "Watch your step around the ledges.$"

OreburghGate_1F_Text_Hiker2:
	.string "I heard there's good training on the\n"
	.string "routes nearby.\p"
	.string "Might head that way once I catch my\n"
	.string "breath.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghGate_1F_EventScript_Npc1::
	msgbox OreburghGate_1F_Text_Npc1, MSGBOX_NPC
	end

OreburghGate_1F_Text_Npc1:
	.string "Oh! Good golly!\nThat's Oreburgh City's Gym Badge!\pAll right! Now you can use the hidden\nmove Rock Smash on small boulders!$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

OreburghGate_1F_EventScript_PicnickerDiana::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_DIANA, OreburghGate_1F_Text_PicnickerDianaIntro, OreburghGate_1F_Text_PicnickerDianaDefeat
	msgbox OreburghGate_1F_Text_PicnickerDianaPost, MSGBOX_AUTOCLOSE
	end

OreburghGate_1F_Text_PicnickerDianaIntro:
	.string "To celebrate my getting through this\ncave, I'm going to battle you!$"

OreburghGate_1F_Text_PicnickerDianaDefeat:
	.string "Well, I guess losing is something\nto commemorate, too...$"

OreburghGate_1F_Text_PicnickerDianaPost:
	.string "Getting through that cave feels\nlike an adventure.$"

OreburghGate_1F_EventScript_CamperCurtis::
	trainerbattle_single TRAINER_SINNOH_CAMPER_CURTIS, OreburghGate_1F_Text_CamperCurtisIntro, OreburghGate_1F_Text_CamperCurtisDefeat
	msgbox OreburghGate_1F_Text_CamperCurtisPost, MSGBOX_AUTOCLOSE
	end

OreburghGate_1F_Text_CamperCurtisIntro:
	.string "We Trainers will accept challenges\nanywhere! It's what we do.$"

OreburghGate_1F_Text_CamperCurtisDefeat:
	.string "Hmm...\nInsufficiently raised?$"

OreburghGate_1F_Text_CamperCurtisPost:
	.string "Pokémon can appear anywhere in a cave.\nIt's not like the tall grass by roads.$"
