SolaceonTownPokecenter1F_MapScripts::
	.byte 0

SolaceonTownPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

SolaceonTownPokecenter1F_EventScript_Npc1::
	msgbox SolaceonTownPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

SolaceonTownPokecenter1F_Text_Npc1:
	.string "The Day-Care Man was saying Pokémon\ngrow at different rates.$"

SolaceonTownPokecenter1F_EventScript_Npc2::
	msgbox SolaceonTownPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

SolaceonTownPokecenter1F_Text_Npc2:
	.string "It's quite far from Solaceon Town to\nVeilstone City.\pThere's a café along the way where\nyou can get some rest, though.$"

SolaceonTownPokecenter1F_EventScript_Npc3::
	msgbox SolaceonTownPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

SolaceonTownPokecenter1F_Text_Npc3:
	.string "The Hidden Machine Defog can be found\nin the Solaceon Ruins.\pBut my Pokémon can't learn the hidden\nmove.\pI'm going to give the ruins a miss, this\ntime.$"
