Route224_MapScripts::
	.byte 0

@ BLOQUEADO (S7, 18/08/2026). LOCALID_MARLEY precisa de FLAG_HIDE_ROUTE_224_
@ MARLEY, que NAO esta no censo do S1 (nao e um dos 247 grupos de
@ hidden_flag; `grep` em dev_scripts/maquina_sinnoh.json confirma zero
@ ocorrencias), mesmo buraco do Crasher Wake em Pastoria/Route227/Villa.
@ Achado extra (nao so este mapa): LOCALID_PROF_OAK, que TEM flag no censo
@ (FLAG_SINNOH_ESCONDE_ROUTE_224_PROF_OAK, 0x1B76), NAO fica mais barato:
@ a fonte so libera ele com `CheckDistributionEvent DISTRIBUTION_EVENT_
@ SHAYMIN` (scripts_route_224.s:8-19), que e Mystery Gift, mecanica
@ descartada pela decisao 3 do plano ("Mystery Gift nao existe aqui"). Sem
@ Mystery Gift a condicao nunca fecha, entao mesmo com endereco de flag o
@ Prof Oak nunca aparece; nao ha cena pra escrever, so o descarte a
@ registrar (mesma familia de FLAG_HIDE_POKECENTER_*/MART_* da decisao 6).
@ Volta ao plano nos dois casos.
Route224_EventScript_CoordEvent_Marley::
	end

Route224_EventScript_Trainer1::
	trainerbattle_single TRAINER_SINNOH_BLACK_BELT_CARL, Route224_Text_Trainer1Intro, Route224_Text_Trainer1Defeat
	msgbox Route224_Text_Trainer1Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer1Intro:
	.string "All right, my Pokémon squad!\nGet out there and kick up a storm!\p$"

Route224_Text_Trainer1Defeat:
	.string "The squad failed to hit its stride...$"

Route224_Text_Trainer1Post:
	.string "Hmm...\p"
	.string "Gazing out over the sea doesn't do a\n"
	.string "thing for toughening up my Pokémon!$"

Route224_EventScript_Trainer2::
	trainerbattle_single TRAINER_SINNOH_VETERAN_ARMANDO, Route224_Text_Trainer2Intro, Route224_Text_Trainer2Defeat
	msgbox Route224_Text_Trainer2Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer2Intro:
	.string "I've seen countless Trainers and\neven more Pokémon!\pSo, what kind of a Trainer are you?\p$"

Route224_Text_Trainer2Defeat:
	.string "I see...\nSimply outstanding.$"

Route224_Text_Trainer2Post:
	.string "I've seen countless Trainers and\n"
	.string "even more Pokémon.\p"
	.string "You're a strong Trainer.\n"
	.string "Moreover, your heart is strong.$"


Route224_EventScript_Trainer3::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_RUBEN, Route224_Text_Trainer3Intro, Route224_Text_Trainer3Defeat
	msgbox Route224_Text_Trainer3Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer3Intro:
	.string "There's something about you...\nYou're not just anybody.\pI challenge you!\p$"

Route224_Text_Trainer3Defeat:
	.string "You're at a different level of\n"
	.string "expertise for sure!$"

Route224_Text_Trainer3Post:
	.string "You've won countless times...\n"
	.string "That has made you very powerful.$"

Route224_EventScript_Trainer4::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_MAXWELL, Route224_Text_Trainer4Intro, Route224_Text_Trainer4Defeat
	msgbox Route224_Text_Trainer4Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer4Intro:
	.string "For some reason I was drawn here,\nand it is here that I met you...\pI want to know what all this means!\p$"

Route224_Text_Trainer4Defeat:
	.string "I see...\p"
	.string "So that's what it means...$"

Route224_Text_Trainer4Post:
	.string "I feel... I feel some sort of a mystic\n"
	.string "presence emanating from here...$"

Route224_EventScript_Trainer5::
	trainerbattle_single TRAINER_SINNOH_PSYCHIC_BRITTNEY, Route224_Text_Trainer5Intro, Route224_Text_Trainer5Defeat
	msgbox Route224_Text_Trainer5Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer5Intro:
	.string "There is nothing here... And yet\nthere is a power lurking...\pWere you drawn by it, as well?\p$"

Route224_Text_Trainer5Defeat:
	.string "The power that slumbers within you...\n"
	.string "It is rather marvelous indeed...$"

Route224_Text_Trainer5Post:
	.string "A place where nothing else exists...\p"
	.string "A place such as that is better suited\n"
	.string "to awaken the power within.$"

Route224_EventScript_Trainer6::
	trainerbattle_single TRAINER_SINNOH_ACE_TRAINER_JAMIE, Route224_Text_Trainer6Intro, Route224_Text_Trainer6Defeat
	msgbox Route224_Text_Trainer6Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer6Intro:
	.string "I constantly analyze Pokémon and\nvarious battles on my laptop.\p$"

Route224_Text_Trainer6Defeat:
	.string "...Things don't always work out\n"
	.string "according to my calculations...$"

Route224_Text_Trainer6Post:
	.string "I had a lot of fun battling with\n"
	.string "you, though.\p"
	.string "I wonder if I can analyze the\n"
	.string "battle data properly?\p"
	.string "I could use a rematch to get\n"
	.string "some additional data.$"

Route224_EventScript_Trainer7::
	trainerbattle_single TRAINER_SINNOH_RUIN_MANIAC_LARRY, Route224_Text_Trainer7Intro, Route224_Text_Trainer7Defeat
	msgbox Route224_Text_Trainer7Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer7Intro:
	.string "I don't care who you are--no one\ninterferes with my treasure hunting!\p$"

Route224_Text_Trainer7Defeat:
	.string "My Pokémon!\n"
	.string "My treasures!$"

Route224_Text_Trainer7Post:
	.string "I heard there's an intriguing stone\n"
	.string "monument around, so I came running.$"

Route224_EventScript_Trainer8::
	trainerbattle_single TRAINER_SINNOH_DRAGON_TAMER_HAYDEN, Route224_Text_Trainer8Intro, Route224_Text_Trainer8Defeat
	msgbox Route224_Text_Trainer8Post, MSGBOX_AUTOCLOSE
	end

Route224_Text_Trainer8Intro:
	.string "My dragon Pokémon chose to become\npowerful here. They sure like it!\p$"

Route224_Text_Trainer8Defeat:
	.string "Your battle style...\n"
	.string "So savage...$"

Route224_Text_Trainer8Post:
	.string "It's been several years since I left\nthe Dragon's Den.\pI've got to say, your Pokémon are\nin the top class for toughness.$"


@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

Route224_EventScript_Placa8::
	msgbox Route224_Text_Placa8, MSGBOX_SIGN
	end

Route224_Text_Placa8:
	.string "The surface is unmarked.\nIt is polished like a mirror.$"
