@ FoothillTown_FishingDojo: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 17.9) por dev_scripts/copia_planta_ex.py.

FoothillTown_FishingDojo_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 17.9), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
FoothillTown_FishingDojo_EventScript_ExNpc0::
	msgbox FoothillTown_FishingDojo_Text_ExNpc0, MSGBOX_NPC
	end

FoothillTown_FishingDojo_Text_ExNpc0:
	.string "A few years ago I was fishing in the the\n"
	.string "FOOTHILL TOWN POND.\p"
	.string "I got a bite, and a fierce battle\n"
	.string "ensued. After fighting for almost an\l"
	.string "hour I finally pulled my opponent to the\l"
	.string "surface, and when I did...\p"
	.string "IT WAS A MASSIVE GYARADOS!!!\p"
	.string "Before I could even think it attacked\n"
	.string "me with a HYDRO PUMP! I dodged and when\l"
	.string "I looked back it was gone...\p"
	.string "Ever since many have tried to find that\n"
	.string "GYARADOS but none have succeeded...$"

FoothillTown_FishingDojo_EventScript_ExNpc2::
	msgbox FoothillTown_FishingDojo_Text_ExNpc2, MSGBOX_NPC
	end

FoothillTown_FishingDojo_Text_ExNpc2:
	.string "I don’t think these jars will be able to\n"
	.string "hold a GYARADOS.$"


@ Presente do EX (0x8351D62), reescrito: a GOOD ROD, uma vez.
FoothillTown_FishingDojo_EventScript_RodFisherman::
	lock
	faceplayer
	goto_if_set FLAG_RECEIVED_HOENNEX_FOOTHILL_GOOD_ROD, FoothillTown_FishingDojo_EventScript_RodGiven
	msgbox FoothillTown_FishingDojo_Text_TakeRod, MSGBOX_DEFAULT
	giveitem ITEM_GOOD_ROD
	setflag FLAG_RECEIVED_HOENNEX_FOOTHILL_GOOD_ROD
FoothillTown_FishingDojo_EventScript_RodGiven::
	msgbox FoothillTown_FishingDojo_Text_CatchGyarados, MSGBOX_DEFAULT
	release
	end

FoothillTown_FishingDojo_Text_TakeRod:
	.string "With my new SUPER ROD I’ll catch a\n"
	.string "GYARADOS for sure!\p"
	.string "I won’t need this anymore.\n"
	.string "Here take it!$"

FoothillTown_FishingDojo_Text_CatchGyarados:
	.string "I will catch a GYARADOS!$"

