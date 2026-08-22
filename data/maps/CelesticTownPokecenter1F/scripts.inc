CelesticTownPokecenter1F_MapScripts::
	.byte 0

CelesticTownPokecenter1F_EventScript_Enfermeira::
	setvar VAR_0x800B, 1
	call Common_EventScript_PkmnCenterNurse
	waitmessage
	waitbuttonpress
	release
	end

CelesticTownPokecenter1F_EventScript_Npc1::
	msgbox CelesticTownPokecenter1F_Text_Npc1, MSGBOX_NPC
	end

CelesticTownPokecenter1F_Text_Npc1:
	.string "Oh? Hm, hm...\nYour Pokémon is quite interesting!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CelesticTownPokecenter1F_EventScript_Npc3::
	msgbox CelesticTownPokecenter1F_Text_Npc3, MSGBOX_NPC
	end

CelesticTownPokecenter1F_Text_Npc3:
	.string "What would compel a young person like\nyou to come somewhere so rustic?\pBe sure to see the cave painting since\nyou're already here.$"

CelesticTownPokecenter1F_EventScript_Npc2::
	msgbox CelesticTownPokecenter1F_Text_Npc2, MSGBOX_NPC
	end

CelesticTownPokecenter1F_Text_Npc2:
	.string "They say this town has been here\nsince Sinnoh was made.$"

@ >>> porta fechada (remove_mapas_cortados.py) >>>
CelesticTownPokecenter1F_EventScript_PortaFechada::
	msgbox CelesticTownPokecenter1F_Text_PortaFechada, MSGBOX_SIGN
	end

CelesticTownPokecenter1F_Text_PortaFechada:
	.string "Fechado. Área em obras.$"
@ <<< porta fechada <<<
