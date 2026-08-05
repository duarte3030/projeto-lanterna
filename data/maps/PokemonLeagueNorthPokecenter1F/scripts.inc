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
