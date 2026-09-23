@ LcNewIslandLab: mapa copiado de Pokémon Liquid Crystal.gba (g4m33) por
@ dev_scripts/copia_mapa_rom.py. A ARTE e do hack; o JOGO e nosso.
@ A sala tem UM warp que dispara, a escada de (12,11), e ela devolve o jogador
@ para a porta da terraco leste do exterior: interior de uma porta so TEM de
@ devolver para o mapa de onde veio (regra 0 do valida_conectividade.py).

LcNewIslandLab_MapScripts::
	.byte 0

LcNewIslandLab_EventScript_SignLab::
	msgbox LcNewIslandLab_Text_SignLab, MSGBOX_SIGN
	end

LcNewIslandLab_Text_SignLab:
	.string "LABORATORY\n"
	.string "Log every reading. Report every\l"
	.string "anomaly. Ask nothing.$"
