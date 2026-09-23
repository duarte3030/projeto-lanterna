@ LcUnderseaEntrance: mapa copiado de Pokémon Liquid Crystal.gba (g4m114) por
@ dev_scripts/copia_mapa_rom.py. A ARTE é do hack; o JOGO (warps, NPCs,
@ encontros, treinadores, placas) é NOSSO e está aqui.
@
@ Este é o ÚNICO mapa da Undersea Cavern com MAP_TYPE_UNDERWATER, e é de
@ propósito: `TryDoDiveWarp` (src/field_control_avatar.c:1254) só deixa EMERGIR
@ quando `gMapHeader.mapType == MAP_TYPE_UNDERWATER`. Os outros oito são
@ MAP_TYPE_UNDERGROUND, que é o que a arte pede (caverna com chão, escada e
@ poça) e o que a tabela `sTransitionTypes` de src/fldeff_flash.c já sabe
@ atravessar nos dois sentidos (ROUTE -> UNDERGROUND e UNDERGROUND -> ROUTE).
@
@ Por que `setdivewarp` e não conexão "emerge": a conexão de mergulho leva o
@ jogador para as MESMAS coordenadas x,y no mapa de destino (SetDiveWarp em
@ src/overworld.c:864 chama SetWarpDestination com x e y do mapa atual). A
@ Route 41 é 74x89 e este mapa é 24x36: metade das coordenadas dela cairia fora
@ daqui. Com `setdivewarp` o destino é fixo e medido.

LcUnderseaEntrance_MapScripts::
	map_script MAP_SCRIPT_ON_DIVE_WARP, LcUnderseaEntrance_OnDive
	.byte 0

@ Emergir de qualquer ponto deste mapa devolve o jogador ao mesmo tile de água
@ funda da Route 41 de onde ele mergulhou, (17,85), a cova escura encostada no
@ paredão de Cianwood.
LcUnderseaEntrance_OnDive:
	setdivewarp MAP_ROUTE41, 17, 85
	end

LcUnderseaEntrance_EventScript_TrenchSign::
	msgbox LcUnderseaEntrance_Text_TrenchSign, MSGBOX_SIGN
	end

LcUnderseaEntrance_Text_TrenchSign:
	.string "The sand ends here and the rock\n"
	.string "begins.\p"
	.string "Below this shelf the water is old\n"
	.string "and very, very still.$"
