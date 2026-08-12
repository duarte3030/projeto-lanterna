PokemonLeagueNorthPokecenter1F_MapScripts::
	.byte 0

PokemonLeagueNorthPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

PokemonLeagueNorthPokecenter1F_EventScript_Npc1::
	msgbox PokemonLeagueNorthPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

PokemonLeagueNorthPokecenter1F_Text_Npc1:
	.string "Let me confirm that you are qualified\nto challenge the Pokémon League.\pSo! Let us examine the Gym Badges\nyou gathered from Sinnoh.\pOreburgh City's Coal Badge!\pEterna City's Forest Badge!\pHearthome City's Relic Badge!\pVeilstone City's Cobble Badge!\pPastoria City's Fen Badge!\pCanalave City's Mine Badge!\pSnowpoint City's Icicle Badge!\pAnd...\nSunyshore City's Beacon Badge!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PokemonLeagueNorthPokecenter1F_EventScript_Npc3::
	msgbox PokemonLeagueNorthPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

PokemonLeagueNorthPokecenter1F_Text_Npc3:
	.string "It doesn't matter if the going is slow.\pNor does it matter how many challenges\nit takes.\pI'm never giving up!\nNot until I beat the Elite Four!$"

PokemonLeagueNorthPokecenter1F_EventScript_Npc2::
	msgbox PokemonLeagueNorthPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

PokemonLeagueNorthPokecenter1F_Text_Npc2:
	.string "What is the Pokémon League?\nDon't take my word for it.\pTake the challenge and experience it\nfor yourself!$"

@ Lojas de Sinnoh portadas do pokeplatinum (dev_scripts/mudos_sinnoh.py --lojas-aplica)

PokemonLeagueNorthPokecenter1F_Text_LojaSaudacao:
	.string "Welcome! Take a look around, we've\ngot everything a TRAINER needs.$"

@ loja_comum do Platinum (lista comum), tabela de include/data/mart_items.h
PokemonLeagueNorthPokecenter1F_EventScript_Loja1::
	lock
	faceplayer
	msgbox PokemonLeagueNorthPokecenter1F_Text_LojaSaudacao, MSGBOX_DEFAULT
	pokemart PokemonLeagueNorthPokecenter1F_Pokemart_Loja1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
PokemonLeagueNorthPokecenter1F_Pokemart_Loja1:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

@ loja_especial do Platinum (MART_SPECIALTIES_ID_POKEMON_LEAGUE), tabela de include/data/mart_items.h
PokemonLeagueNorthPokecenter1F_EventScript_Loja2::
	lock
	faceplayer
	msgbox PokemonLeagueNorthPokecenter1F_Text_LojaSaudacao, MSGBOX_DEFAULT
	pokemart PokemonLeagueNorthPokecenter1F_Pokemart_Loja2
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
PokemonLeagueNorthPokecenter1F_Pokemart_Loja2:
	.2byte ITEM_HEAL_BALL
	.2byte ITEM_NET_BALL
	.2byte ITEM_NEST_BALL
	.2byte ITEM_DUSK_BALL
	.2byte ITEM_QUICK_BALL
	.2byte ITEM_TIMER_BALL
	.2byte ITEM_REPEAT_BALL
	.2byte ITEM_LUXURY_BALL
	pokemartlistend
