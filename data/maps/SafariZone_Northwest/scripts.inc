SafariZone_Northwest_MapScripts::
	.byte 0

SafariZone_Northwest_EventScript_Man::
	msgbox SafariZone_Northwest_Text_Man, MSGBOX_NPC
	end


@ Eventos novos do Pokémon Emerald EX (mapa 29.0), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
SafariZone_Northwest_EventScript_ExNpc2::
	msgbox SafariZone_Northwest_Text_ExNpc2, MSGBOX_NPC
	end

SafariZone_Northwest_Text_ExNpc2:
	.string "Have you seen any cool POKéMON up\n"
	.string "here?$"

SafariZone_Northwest_EventScript_ExNpc3::
	msgbox SafariZone_Northwest_Text_ExNpc3, MSGBOX_NPC
	end

SafariZone_Northwest_Text_ExNpc3:
	.string "It was hard to climb up here!\p"
	.string "It tok so long, I’m almost out of time in\n"
	.string "my SAFARI GAME!$"

