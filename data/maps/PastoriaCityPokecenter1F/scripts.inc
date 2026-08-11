PastoriaCityPokecenter1F_MapScripts::
	.byte 0

PastoriaCityPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCityPokecenter1F_EventScript_Npc1::
	msgbox PastoriaCityPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

PastoriaCityPokecenter1F_Text_Npc1:
	.string "The Great Marsh is vast!\nHow vast is it, you ask?\pTake a look from the Observatory\nand you can see for yourself!$"

PastoriaCityPokecenter1F_EventScript_Npc2::
	msgbox PastoriaCityPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

PastoriaCityPokecenter1F_Text_Npc2:
	.string "Pastoria's Great Marsh was once\na part of the sea.\pThe seawater drained slowly away over\ntime, leaving the huge marshland.\pThat's why they say there are rare\nPokémon that you can only see here.$"
