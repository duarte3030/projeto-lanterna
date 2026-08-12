@ PkmnLeagueEntrance do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ Editado a mao em 12/08/2026 (B6): o porteiro da cena do terremoto.
@
@ Traducao do `.PrepareEliteFour` de PkmnLeagueEntrance.asm, que e um
@ MAPCALLBACK_NEWMAP e cuja unica parte que importa aqui e
@ `setmapscene PKMN_LEAGUE_MAIN, SCENE_ELITE_FOUR_ROOM_ENTER`: passar por esta
@ sala e o que arma a cena de entrada da Liga. As outras linhas daquele callback
@ (limpar EVENT_BEAT_ELITE_FOUR_*) sao para o BW3G poder REFAZER a Elite dos
@ Quatro; aqui quem lembra que cada membro caiu e a flag de treinador derrotado
@ do proprio motor, e apaga-la seria apagar o progresso do jogador.
@
@ Zero var. Uma flag, FLAG_UNOVA_LIGA_PORTAO, que a PkmnLeagueMain consome e
@ apaga assim que a cena roda.

Unova_PkmnLeagueEntrance_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_PkmnLeagueEntrance_OnTransition
	.byte 0

Unova_PkmnLeagueEntrance_OnTransition:
	setflag FLAG_UNOVA_LIGA_PORTAO
	end


