ResortAreaPokecenter1F_MapScripts::
	.byte 0

ResortAreaPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

ResortAreaPokecenter1F_EventScript_Npc1::
	msgbox ResortAreaPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

ResortAreaPokecenter1F_Text_Npc1:
	.string "Do you know there's a sure way to\nchange the world?\pDo a headstand, and the world turns\nupside down!$"

ResortAreaPokecenter1F_EventScript_Npc2::
	msgbox ResortAreaPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

ResortAreaPokecenter1F_Text_Npc2:
	.string "Wherever you are in the world!\pWhoever it is in the world!\pEveryone knows Pokémon!\nThat's fabulously fantastic!$"
