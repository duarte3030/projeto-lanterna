@ Mapa de referencia de Sinnoh. O padrao usado aqui vale para os outros 132:
@ ver Pokemon Claude/SINNOH-PADRAO.md antes de escrever qualquer script novo.
@ Textos vindos de pret/pokeplatinum, em ingles, como o resto do jogo.

TwinleafTown_MapScripts::
	.byte 0

TwinleafTown_EventScript_Guitarist::
	lock
	faceplayer
	msgbox TwinleafTown_Text_Guitarist, MSGBOX_DEFAULT
	release
	end

@ Barry. Antes do inicial ele e quem manda o jogador para SANDGEM; depois,
@ ele ja foi embora e so provoca. Falas do Platinum, twinleaf_town.json e
@ twinleaf_town_player_house_2f.json.
TwinleafTown_EventScript_Rival::
	lock
	faceplayer
	goto_if_set FLAG_SYS_POKEMON_GET, TwinleafTown_EventScript_RivalAfter
	msgbox TwinleafTown_Text_Rival, MSGBOX_DEFAULT
	release
	end

TwinleafTown_EventScript_RivalAfter::
	msgbox TwinleafTown_Text_RivalAfter, MSGBOX_DEFAULT
	release
	end

TwinleafTown_EventScript_TownSign::
	msgbox TwinleafTown_Text_TownSign, MSGBOX_SIGN
	end

TwinleafTown_Text_Guitarist:
	.string "Everyone goes off on adventures,\n"
	.string "and then they gradually grow up...$"

TwinleafTown_Text_Rival:
	.string "Hey, {PLAYER}!\p"
	.string "Did you just see the TV?\n"
	.string "Sure you did!\p"
	.string "PROF. ROWAN's that really important\n"
	.string "guy who studies POKéMON, right?\p"
	.string "That means he must have lots and\n"
	.string "lots of POKéMON.\p"
	.string "So, if we ask him, I bet he'd give\n"
	.string "us some POKéMON!\p"
	.string "We're going to go see PROF. ROWAN\n"
	.string "in SANDGEM TOWN, north of here.\p"
	.string "OK, {PLAYER}? If you're late, I'm\n"
	.string "fining you ¥10 million!$"

TwinleafTown_Text_RivalAfter:
	.string "How do you like that?\n"
	.string "PROF. ROWAN's really nice.\p"
	.string "On TV, he seems so stern and\n"
	.string "scary.$"

TwinleafTown_Text_TownSign:
	.string "TWINLEAF TOWN\n"
	.string "A Town Whose Leaves Are Always Fresh$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TwinleafTown_EventScript_Npc1::
	msgbox TwinleafTown_Text_Npc1, MSGBOX_NPC
	end

TwinleafTown_Text_Npc1:
	.string "It's true that wild Pokémon do attack\npeople sometimes...\pBut, Pokémon also open their hearts\nto you, so you can become friends.$"

TwinleafTown_EventScript_Npc2::
	msgbox TwinleafTown_Text_Npc2, MSGBOX_NPC
	end

TwinleafTown_Text_Npc2:
	.string "Technology just blows me away!\pI mean, now you can play with people\naround the world...wirelessly!$"

TwinleafTown_EventScript_Placa3::
	msgbox TwinleafTown_Text_Placa3, MSGBOX_SIGN
	end

TwinleafTown_Text_Placa3:
	.string "Twinleaf Town\nFresh and Free!$"
