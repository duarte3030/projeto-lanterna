SolaceonTownPokemonNewsPress_MapScripts::
	.byte 0

SolaceonTownPokemonNewsPress_EventScript_Placa1::
	msgbox SolaceonTownPokemonNewsPress_Text_Placa1, MSGBOX_SIGN
	end

SolaceonTownPokemonNewsPress_Text_Placa1:
	.string "'Weekly Poké Ball Roundup'\nis the featured top story.\pIt's a feature article on new types\nof Poké Balls.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SolaceonTownPokemonNewsPress_EventScript_Npc1::
	msgbox SolaceonTownPokemonNewsPress_Text_Npc1, MSGBOX_NPC
	end

SolaceonTownPokemonNewsPress_Text_Npc1:
	.string "What's up? Did you bring us\nthe Pokémon we needed?$"

SolaceonTownPokemonNewsPress_EventScript_Npc2::
	msgbox SolaceonTownPokemonNewsPress_Text_Npc2, MSGBOX_NPC
	end

SolaceonTownPokemonNewsPress_Text_Npc2:
	.string "The Sinnoh region's newspaper is\ntiny, but it has many fans.\pThat newspaper is printed right\nhere!$"
