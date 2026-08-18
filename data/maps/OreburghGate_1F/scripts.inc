OreburghGate_1F_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S4: cena da fonte, rotulo OreburghGate1F_CoordEvent_Hiker >>>
@ O andarilho (LOCALID_OREBURGH_GATE_1F_HIKER_3, ja importado mudo em 7,20)
@ anda ate o jogador e da a HM de Rock Smash na primeira passagem pelo portao.
@ Fonte fala de Poketch de passagem ("That sparkling new Poketch!"); cortado,
@ decisao 3 do plano (mecanica nao existe aqui). O aviso de que precisa de
@ insignia para usar Rock Smash fora de batalha tambem caiu: neste motor o
@ campo e sempre utilizavel (precedente MauvilleCity_House1).
OreburghGate_1F_EventScript_CoordEvent_Hiker::
	lockall
	applymovement LOCALID_OREBURGH_GATE_1F_HIKER_3, OreburghGate_1F_Movement_HikerWalkToPlayer
	applymovement LOCALID_PLAYER, OreburghGate_1F_Movement_PlayerFaceHiker
	waitmovement 0
	msgbox OreburghGate_1F_Text_MakeAGiftOfThisHM, MSGBOX_DEFAULT
	giveitem ITEM_HM_ROCK_SMASH
	setflag FLAG_RECEIVED_HM_ROCK_SMASH
	msgbox OreburghGate_1F_Text_ThatHMContainsRockSmash, MSGBOX_DEFAULT
	setvar VAR_SINNOH_OREBURGH_PORTAO_ANDARILHO, 2
	releaseall
	end

OreburghGate_1F_Movement_PlayerFaceHiker:
	delay_8
	face_up
	step_end

OreburghGate_1F_Movement_HikerWalkToPlayer:
	face_down
	emote_exclamation_mark
	walk_down
	walk_down
	step_end

OreburghGate_1F_Text_MakeAGiftOfThisHM:
	.string "Hmm… You're still a pretty new\n"
	.string "Trainer, aren't you?\p"
	.string "But it's all good! You're a new\n"
	.string "friend of Pokémon!\p"
	.string "So, let me make a gift of this\n"
	.string "Hidden Machine to you!$"

OreburghGate_1F_Text_ThatHMContainsRockSmash:
	.string "That Hidden Machine, or HM for\n"
	.string "short, contains the hidden move\l"
	.string "Rock Smash.\p"
	.string "A Pokémon that knows Rock Smash\n"
	.string "can smash small boulders in the\l"
	.string "field.$"
@ <<< B6 Sinnoh S4: cena da fonte <<<

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
