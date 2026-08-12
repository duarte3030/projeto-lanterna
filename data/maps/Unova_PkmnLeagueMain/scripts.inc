@ PkmnLeagueMain do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 12/08/2026 (B5): o portao da Elite dos Quatro.
@
@ Medido antes do conserto: os sete warps deste mapa vao para a entrada da Liga,
@ para si mesmo e para as quatro salas da Elite. NENHUM leva ao Campeao. No BW3G
@ quem leva e a estatua do centro (bg_event em 13,11 e 14,11): depois dos quatro
@ ela deixa de falar e vira elevador, `warp CHAMPIONS_ROOM_ENTRANCE, 7, 16`.
@ Aqui as duas estatuas so tinham o texto, entao a sala do Campeao era
@ inalcancavel a pe, com a Elite inteira derrotada.
@
@ Custo: ZERO var e ZERO flag nova. O motor ja grava sozinho a flag "ja perdeu"
@ de cada treinador (TRAINER_FLAGS_START + id), e `goto_if_not_defeated` le ela.
@ Por isso o portao nao precisa de contador de estagio, que e o que costuma
@ comer var em Liga.
@
@ AS PORTAS, acrescentadas mais tarde no mesmo dia, com os tilesets de Unova ja
@ estaveis. No BW3G um MAPCALLBACK_TILES abre a porta de cada sala conforme o
@ membro da Elite cai, e destrava o elevador do centro quando os quatro caem.
@ DE ONDE SAIU CADA METATILE (nada foi chutado): um bloco de gen 2 vale 2x2
@ metatiles nossos, e a tabela (bloco, quadrante) -> metatile do tileset ja
@ convertido esta em `dev_scripts/blockdata_unova.py` (`quad2mt` de tileset_gen2,
@ tileset `pkmn_league` = gTileset_UnovaPkmnLeague). Os `changeblock` da fonte
@ foram resolvidos por essa tabela e comparados tile a tile com o `map.bin`
@ atual: de cada bloco de 4 quadrantes so UM difere, e e so ele que entra aqui.
@ Nenhuma das quatro portas muda colisao (as quatro ja estao com colisao 0 no
@ blockdata), entao isto e o DESENHO da porta abrindo, e o caminho ja existia:
@ os 7 warps deste mapa ja disparavam (100% em valida_warp_tile.py --regiao Unova).
@
@ O tile do centro, (13,13), e o unico que muda comportamento: 844 e
@ MB_NON_ANIMATED_DOOR e 845 e MB_NORMAL. Esse 844 e o warp que aponta para SI
@ MESMO, herdado do BW3G, que hoje faz o jogador levar uma transicao de tela a
@ toa ao pisar no centro da sala. Ele so e trocado depois dos quatro, que e
@ quando a fonte troca; antes disso o incomodo continua, e esta anotado.
@
@ Custo desta parte: ZERO var e ZERO flag. Quem decide e a flag de treinador
@ derrotado do motor, a mesma que o portao da estatua le.
@
@ O SELO, feito em 12/08/2026 pelo B6 (era o item que o B5 deixou anotado aqui).
@
@ `.PkmnLeagueEnter` da fonte: ao subir da entrada, o jogador anda seis passos
@ para o norte, o chao treme e os dois `changeblock` $B9 e $BA fecham a escada de
@ volta. Os numeros vieram da mesma tabela que o B5 usou (`quad2mt` de
@ tileset_gen2, tileset `pkmn_league`), comparados tile a tile com o `map.bin` do
@ disco: dos oito quadrantes dos dois blocos so DOIS diferem, (13,15) e (14,15),
@ os dois indo de mt 803 (colisao 0) para mt 780 (parede). Medido na grade de
@ colisao: a linha 15 so tem aberto 4, 13, 14 e 23, e as colunas 4 e 23 nao
@ chegam na linha 20; entao (13,15) e (14,15) sao o UNICO caminho entre o salao
@ da Elite e a saida. Selar ali fecha a Liga de verdade, que e o que a fonte faz.
@
@ POR QUE ISTO NAO PRENDE O JOGADOR, que e o aceite do B6:
@ 1. o selo so e aplicado enquanto FLAG_UNOVA_LIGA_VENCIDA estiver apagada, e
@    quem a acende e o Hall da Fama (data/maps/Unova_HallOfFame/scripts.inc).
@    Ganhou, a escada volta a existir sozinha, sem `setmetatile` de desfazer:
@    basta a cena nao rodar, porque o estado limpo e o do proprio `map.bin`;
@ 2. a cena inteira que ele fecha entrou no MESMO dia, nos quatro mapas
@    (PkmnLeagueEntrance, PkmnLeagueMain, ChampionsRoomEntrance, ChampionsRoom,
@    HallOfFame). Selar sem ela era o que o B5 se recusou a fazer, e com razao;
@ 3. o selo NAO esta no ON_LOAD, e isso e de proposito. No ON_LOAD ele valeria
@    tambem para quem chega vindo de baixo, que nasce em (13,19)/(14,19), ABAIXO
@    do selo: o jogador entraria ja trancado num corredor de quatro tiles. Quem
@    aplica e a propria cena, DEPOIS de subir o jogador, como na fonte.
@
@ Custo: ZERO var. UMA flag nova, FLAG_UNOVA_LIGA_PORTAO, que e o porteiro da
@ cena (so roda quem subiu da entrada; ver o cabecalho de
@ data/maps/Unova_PkmnLeagueEntrance/scripts.inc), mais a leitura de
@ FLAG_UNOVA_LIGA_VENCIDA, que e do bloco da cena do Campeao.

Unova_PkmnLeagueMain_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_PkmnLeagueMain_EventScript_Portas
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Unova_PkmnLeagueMain_OnFrame
	.byte 0

Unova_PkmnLeagueMain_OnFrame:
	map_script_2 VAR_TEMP_0, 0, Unova_PkmnLeagueMain_EventScript_Terremoto
	.2byte 0

Unova_PkmnLeagueMain_EventScript_Terremoto::
	goto_if_unset FLAG_UNOVA_LIGA_PORTAO, Unova_PkmnLeagueMain_EventScript_TerremotoFim
	clearflag FLAG_UNOVA_LIGA_PORTAO
	goto_if_set FLAG_UNOVA_LIGA_VENCIDA, Unova_PkmnLeagueMain_EventScript_TerremotoFim
	lockall
	applymovement LOCALID_PLAYER, Unova_PkmnLeagueMain_Movement_Sobe
	waitmovement 0
	playse SE_M_STRENGTH
	setvar VAR_0x8004, 0
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 12
	setvar VAR_0x8007, 3
	special ShakeScreen
	setmetatile 13, 15, 780, TRUE
	setmetatile 14, 15, 780, TRUE
	special DrawWholeMapView
	waitse
	msgbox Unova_PkmnLeagueMain_Text_EscadaSelada, MSGBOX_DEFAULT
	closemessage
	releaseall
Unova_PkmnLeagueMain_EventScript_TerremotoFim::
	end

@ CINCO passos, e nao seis, desde 12/08/2026. A fonte anda seis porque la o
@ jogador nasce em (13,20): o `MB_NON_ANIMATED_DOOR` do tile de chegada fazia
@ `Task_ExitNonAnimDoor` empurrar ele um tile para o sul antes da cena comecar.
@ (13,19) e (14,19) passaram a ser `MB_SOUTH_ARROW_WARP`
@ (dev_scripts/porta_de_saida_unova.py, que explica o porque), a seta nao
@ empurra ninguem, e a partida subiu um tile. Com seis passos a cena terminaria
@ em (13,13), que e o warp que aponta para si mesmo; com cinco ela termina em
@ (13,14), exatamente onde terminava antes, e o selo em (13,15)/(14,15)
@ continua ficando ATRAS do jogador.
Unova_PkmnLeagueMain_Movement_Sobe:
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

Unova_PkmnLeagueMain_Text_EscadaSelada::
	.string "The ground shook, and the stairs\n"
	.string "behind you sealed themselves.\p"
	.string "There is only one way out of the\n"
	.string "POKéMON LEAGUE now: forward.$"

Unova_PkmnLeagueMain_EventScript_Portas::
	call Unova_PkmnLeagueMain_EventScript_ReaplicaSelo
	call_if_defeated TRAINER_UNOVA_E4_GRIMSLEY, Unova_PkmnLeagueMain_EventScript_PortaGrimsley
	call_if_defeated TRAINER_UNOVA_E4_MARSHAL, Unova_PkmnLeagueMain_EventScript_PortaMarshal
	call_if_defeated TRAINER_UNOVA_E4_ELESA, Unova_PkmnLeagueMain_EventScript_PortaElesa
	call_if_defeated TRAINER_UNOVA_E4_COLRESS, Unova_PkmnLeagueMain_EventScript_PortaColress
	goto_if_not_defeated TRAINER_UNOVA_E4_GRIMSLEY, Unova_PkmnLeagueMain_EventScript_PortasFim
	goto_if_not_defeated TRAINER_UNOVA_E4_MARSHAL, Unova_PkmnLeagueMain_EventScript_PortasFim
	goto_if_not_defeated TRAINER_UNOVA_E4_ELESA, Unova_PkmnLeagueMain_EventScript_PortasFim
	goto_if_not_defeated TRAINER_UNOVA_E4_COLRESS, Unova_PkmnLeagueMain_EventScript_PortasFim
	setmetatile 13, 13, 845, FALSE
Unova_PkmnLeagueMain_EventScript_PortasFim::
	end

@ `.SetTiles` da fonte reaplica $B9/$BA em TODA carga de mapa que nao seja a de
@ entrada (`checkscene; ifequal SCENE_ELITE_FOUR_ROOM_ENTER, .CheckMarshal`), que
@ e o que faz o selo continuar la depois de sair e voltar de uma sala da Elite.
@ Aqui o "e a carga de entrada?" e FLAG_UNOVA_LIGA_PORTAO, que so esta acesa
@ quando o jogador acabou de passar pela PkmnLeagueEntrance; nesse caso quem sela
@ e a cena, DEPOIS de subir o jogador, senao ele nasceria trancado abaixo do selo.
Unova_PkmnLeagueMain_EventScript_ReaplicaSelo::
	goto_if_set FLAG_UNOVA_LIGA_PORTAO, Unova_PkmnLeagueMain_EventScript_SemSelo
	goto_if_set FLAG_UNOVA_LIGA_VENCIDA, Unova_PkmnLeagueMain_EventScript_SemSelo
	setmetatile 13, 15, 780, TRUE
	setmetatile 14, 15, 780, TRUE
	return

Unova_PkmnLeagueMain_EventScript_SemSelo::
	return

@ bloco $C8 da fonte em (10,8)
Unova_PkmnLeagueMain_EventScript_PortaGrimsley::
	setmetatile 11, 8, 811, FALSE
	return

@ bloco $C9 da fonte em (16,12)
Unova_PkmnLeagueMain_EventScript_PortaMarshal::
	setmetatile 16, 12, 811, FALSE
	return

@ bloco $C9 da fonte em (16,8)
Unova_PkmnLeagueMain_EventScript_PortaElesa::
	setmetatile 16, 8, 811, FALSE
	return

@ bloco $C8 da fonte em (10,12)
Unova_PkmnLeagueMain_EventScript_PortaColress::
	setmetatile 11, 12, 811, FALSE
	return

Unova_PkmnLeagueMain_EventScript_Placa0::
	goto Unova_PkmnLeagueMain_EventScript_Estatua
	end

Unova_PkmnLeagueMain_EventScript_Placa1::
	goto Unova_PkmnLeagueMain_EventScript_Estatua
	end

Unova_PkmnLeagueMain_EventScript_Estatua::
	lock
	goto_if_not_defeated TRAINER_UNOVA_E4_GRIMSLEY, Unova_PkmnLeagueMain_EventScript_EstatuaFala
	goto_if_not_defeated TRAINER_UNOVA_E4_MARSHAL, Unova_PkmnLeagueMain_EventScript_EstatuaFala
	goto_if_not_defeated TRAINER_UNOVA_E4_ELESA, Unova_PkmnLeagueMain_EventScript_EstatuaFala
	goto_if_not_defeated TRAINER_UNOVA_E4_COLRESS, Unova_PkmnLeagueMain_EventScript_EstatuaFala
	msgbox Unova_PkmnLeagueMain_Text_EstatuaAbre, MSGBOX_DEFAULT
	closemessage
	warp MAP_UNOVA_CHAMPIONS_ROOM_ENTRANCE, 7, 16
	waitstate
	release
	end

Unova_PkmnLeagueMain_EventScript_EstatuaFala::
	msgbox Unova_PkmnLeagueMain_Text_PkmnLeagueMainStatueText, MSGBOX_DEFAULT
	release
	end

Unova_PkmnLeagueMain_Text_EstatuaAbre::
	.string "The four warriors"
	.string "\nhave all fallen."
	.string "\pThe way to the"
	.string "\nsummit is open!$"


Unova_PkmnLeagueMain_Text_PkmnLeagueMainStatueText::
	.string "Four great"
	.string "\nwarriors form this"
	.string "\lPOKéMON LEAGUE."
	.string "\pTo the southwest"
	.string "\nis one who has"
	.string "\pgreat knowledge of"
	.string "\nthe steel type."
	.string "\pTo the southeast"
	.string "\nis one who"
	.string "\pchannels the power"
	.string "\nof the fighting"
	.string "\ltype."
	.string "\pTo the northwest"
	.string "\nis one who has"
	.string "\pmastered the dark"
	.string "\ntype."
	.string "\pTo the northeast"
	.string "\nis one who shines"
	.string "\pwith the electric"
	.string "\ntype."
	.string "\pIf you can defeat"
	.string "\nthese warriors"
	.string "\pwith your courage"
	.string "\nand wisdom, you"
	.string "\pshall be led to"
	.string "\nthe summit, where"
	.string "\pthe strongest"
	.string "\nCHAMPION awaits.$"
