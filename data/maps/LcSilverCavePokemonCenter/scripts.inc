@ LcSilverCavePokemonCenter: mapa copiado de Pokémon Liquid Crystal.gba (g4m95)
@ por dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO é NOSSO.
@ Os dois warps extras do hack (1,5) e (1,3), que lá levavam ao andar de cima e
@ à sala de link, NÃO entraram: os dois tiles são MB_NORMAL nesta cópia e não
@ há andar de cima a ligar.

LcSilverCavePokemonCenter_MapScripts::
	.byte 0

LcSilverCavePokemonCenter_EventScript_Climber::
	msgbox LcSilverCavePokemonCenter_Text_Climber, MSGBOX_NPC
	end

LcSilverCavePokemonCenter_Text_Climber:
	.string "This CENTRE was built for the crews\n"
	.string "who cut the path over the ridge.\p"
	.string "They left. The nurse stayed, and\n"
	.string "so did the kettle.\p"
	.string "Rest up. SILVER CAVE takes a whole\n"
	.string "day if you do it properly.$"
