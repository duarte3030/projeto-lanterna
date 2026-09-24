@ FoothillTown_House5: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 17.7) por dev_scripts/copia_planta_ex.py.

FoothillTown_House5_MapScripts::
	.byte 0

@ Fala do EX condicionada à FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE (0x9E no EX e no vanilla).
FoothillTown_House5_EventScript_AquaM::
	lock
	faceplayer
	goto_if_set FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, FoothillTown_House5_EventScript_AquaMDepois
	msgbox FoothillTown_House5_Text_AquaMAntes, MSGBOX_DEFAULT
	release
	end
FoothillTown_House5_EventScript_AquaMDepois::
	msgbox FoothillTown_House5_Text_AquaMDepois, MSGBOX_DEFAULT
	release
	end

FoothillTown_House5_EventScript_AquaF::
	lock
	faceplayer
	goto_if_set FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, FoothillTown_House5_EventScript_AquaFDepois
	msgbox FoothillTown_House5_Text_AquaFAntes, MSGBOX_DEFAULT
	release
	end
FoothillTown_House5_EventScript_AquaFDepois::
	msgbox FoothillTown_House5_Text_AquaFDepois, MSGBOX_DEFAULT
	release
	end

FoothillTown_House5_Text_AquaMAntes:
	.string "TEAM AQUA sent us here to catch the\n"
	.string "GYARADOS of the lake!$"

FoothillTown_House5_Text_AquaMDepois:
	.string "TEAM AQUA sure messed up by waking\n"
	.string "KYOGRE.\p"
	.string "We decided to leave the TEAM and settle\n"
	.string "down here.$"

FoothillTown_House5_Text_AquaFAntes:
	.string "It’s a bit weird being posted here so\n"
	.string "far from the rest of TEAM AQUA...\p"
	.string "At least the guy I’m here with is nice.$"

FoothillTown_House5_Text_AquaFDepois:
	.string "I’m glad the two of us were sent here.\n"
	.string "We didn’t even know about all the bad\l"
	.string "stuff TEAM AQUA was up to!$"

