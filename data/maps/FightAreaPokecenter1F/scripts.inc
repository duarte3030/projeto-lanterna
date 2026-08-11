FightAreaPokecenter1F_MapScripts::
	.byte 0

FightAreaPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

FightAreaPokecenter1F_EventScript_Npc1::
	msgbox FightAreaPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

FightAreaPokecenter1F_Text_Npc1:
	.string "The Battle Frontier's as tough as they\nsay...\pNone of the facilities are cakewalks,\nthat's for sure.$"

FightAreaPokecenter1F_EventScript_Npc2::
	msgbox FightAreaPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

FightAreaPokecenter1F_Text_Npc2:
	.string "The best Trainers from around the\ncountry...\pNo, the best Trainers from around\nthe world gather at the Battle Zone.$"

FightAreaPokecenter1F_EventScript_Npc3::
	msgbox FightAreaPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

FightAreaPokecenter1F_Text_Npc3:
	.string "To toughen myself!\nTo toughen my Pokémon!\pFor that alone, I have come!$"
