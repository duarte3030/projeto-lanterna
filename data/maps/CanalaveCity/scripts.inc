@ Textos vindos de pret/pokeplatinum (res/text/canalave_city.json), em ingles.
@ Rival_Bridge ENTROU em 12/08/2026, com a batalha e os tres times por inicial
@ do jogador (dev_scripts/cena_galactica_sinnoh.py, bloco B6); o
@ FLAG_HIDE_CANALAVE_CITY_RIVAL_BRIDGE do Platinum virou
@ FLAG_GALACTICA_CANALAVE_RIVAL. Counterpart, Prof_Rowan, Sailor e
@ Rival_Library continuam de fora: sao a cena da biblioteca e da explosao dos
@ lagos, que ainda nao foi portada.
@
@ Confirmado nesta leva (S6, 18/08/2026), checando as 3 flags aliasadas pelo
@ censo do S1 contra a fonte: BLOQUEADAS, nao falso pendente.
@ FLAG_SINNOH_ESCONDE_CANALAVE_CITY_COUNTERPART (0x1B0A): CanalaveCity_
@ Counterpart e ramificacao de genero levando o jogador ao Lago Verity, parte
@ do climax "explosao dos lagos" com a contraparte, que abrange varios mapas
@ ao mesmo tempo (nao so Canalave). FLAG_SINNOH_ESCONDE_CANALAVE_CITY_PROF_
@ ROWAN (0x1B0C): CanalaveCity_ProfRowan e mensagem curta de NPC, mas o mesmo
@ climax decide quando ele aparece aqui. FLAG_SINNOH_ESCONDE_CANALAVE_CITY_
@ RIVAL_LIBRARY (0x1B0D): CanalaveCity_RivalLibrary precisa de ITEM_HM04
@ (Strength) e biblioteca de Canalave com escopo escrito, e o proprio plano
@ registra a biblioteca como "continua sem escopo escrito, herdado do ESTADO
@ 0" (PLANO-OBRAS-SINNOH.md, "O que fica de fora"). Os 3 voltam ao plano da
@ condutora antes de qualquer executor escrever a cena.

CanalaveCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CanalaveCity_OnTransition
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ RESOLVIDO SEM CENA NOVA (S6, 18/08/2026). CanalaveCity_CoordEvent_Rival
@ (script 2, var VAR_SINNOH_CANALAVE_ESTADO) e a MESMA batalha que
@ CanalaveCity_EventScript_Rival ja porta abaixo (linha 229): mesmo texto
@ literal (CheckIfYoureReady = CanalaveCity_Text_CenaCheckReady, TrainAt
@ IronIsland = CanalaveCity_Text_CenaIronIsland, os 3 treinadores TRAINER_
@ SINNOH_RIVAL_CANALAVE_CITY_TURTWIG/_CHIMCHAR/_PIPLUP), so que a fonte
@ dispara por coord_event na ponte e o porte de 12/08/2026 trocou pra gatilho
@ de raio de visao (tecnica 3 do SINNOH-PADRAO.md, precedente do rival de
@ Johto) com FLAG_GALACTICA_CANALAVE_RIVAL no lugar da var. Escrever a
@ versao coord_event tambem duplicava a batalha (o jogador enfrentaria o
@ Cedric duas vezes, uma por gatilho). Os 4 coord_events que o S1 tinha
@ plantado em (17,19)-(17,22) apontando pra este rotulo foram REMOVIDOS do
@ map.json nesta leva: apontavam pra um gatilho morto. Fila conta o grupo
@ como resolvido por cena equivalente ja existente.
CanalaveCity_EventScript_CoordEvent_Rival::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

CanalaveCity_EventScript_SailorEldritch::
	lock
	faceplayer
	msgbox CanalaveCity_Text_WhereTo, MSGBOX_DEFAULT
	@ O menu e montado em data/scripts/travessia_regioes.inc e esconde o
	@ destino ainda nao liberado. Os `case` abaixo NAO mudam: o id
	@ empilhado continua sendo o indice antigo da lista.
	call Travessia_EventScript_MenuDeDestinos
	switch VAR_RESULT
	case 0, CanalaveCity_EventScript_SailToOlivine
	case 1, CanalaveCity_EventScript_SailToSlateport
	case 2, CanalaveCity_EventScript_SailToVermilion
	case 3, CanalaveCity_EventScript_SailToVirbank
	@ G5 de Galar: destino 6, atras de FLAG_GALAR_QA_ANDAR. O roteiro e um so,
	@ compartilhado pelos cinco portos (data/scripts/travessia_regioes.inc).
	case 6, Travessia_EventScript_ZarparParaGalar
	msgbox CanalaveCity_Text_ComeAgain, MSGBOX_DEFAULT
	release
	end

CanalaveCity_EventScript_SailToOlivine::
	msgbox CanalaveCity_Text_SettingSailToOlivine, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_OLIVINE_CITY_PORT_INSIDE, 8, 17
	waitstate
	release
	end

CanalaveCity_EventScript_SailToSlateport::
	msgbox CanalaveCity_Text_SettingSailToSlateport, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_SLATEPORT_CITY_HARBOR, 8, 14
	waitstate
	release
	end

CanalaveCity_EventScript_SailToVermilion::
	msgbox CanalaveCity_Text_SettingSailToVermilion, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_VERMILION_CITY, 15, 10
	waitstate
	release
	end

CanalaveCity_Text_WhereTo:
	.string "Welcome to CANALAVE CITY, SINNOH!\n"
	.string "Where would you like to sail?$"

CanalaveCity_Text_SettingSailToOlivine:
	.string "Setting sail for OLIVINE CITY\n"
	.string "in JOHTO!$"

CanalaveCity_Text_SettingSailToSlateport:
	.string "Setting sail for SLATEPORT CITY\n"
	.string "in HOENN!$"

CanalaveCity_Text_SettingSailToVermilion:
	.string "Setting sail for VERMILION CITY\n"
	.string "in KANTO!$"

CanalaveCity_Text_ComeAgain:
	.string "Come see me whenever you want to\nset sail.$"

CanalaveCity_EventScript_GymSign::
	msgbox CanalaveCity_Text_GymSign, MSGBOX_SIGN
	end

CanalaveCity_EventScript_LibrarySign::
	msgbox CanalaveCity_Text_LibrarySign, MSGBOX_SIGN
	end

CanalaveCity_Text_SailorEldritch:
	.string "Do you wanna set sail?\p"
	.string "You just tell me whenever you\n"
	.string "need to set sail!$"

CanalaveCity_Text_GymSign:
	.string "CANALAVE CITY POKéMON GYM\p"
	.string "The Steel-Type Sturdiness Style!$"

CanalaveCity_Text_LibrarySign:
	.string "CANALAVE LIBRARY$"

CanalaveCity_EventScript_SailToVirbank::
	msgbox CanalaveCity_Text_SettingSailToVirbank, MSGBOX_DEFAULT
	closemessage
	warpsilent MAP_UNOVA_VIRBANK_PORT, 4, 6
	waitstate
	release
	end

CanalaveCity_Text_SettingSailToVirbank:
	.string "Setting sail for VIRBANK CITY\n"
	.string "in UNOVA!$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

CanalaveCity_EventScript_Placa1::
	msgbox CanalaveCity_Text_Placa1, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa1:
	.string "Canalave Library$"

CanalaveCity_EventScript_Placa2::
	msgbox CanalaveCity_Text_Placa2, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa2:
	.string "Canalave City Pokémon Gym\nLeader: Byron\pThe Man with the Steel Body!$"

CanalaveCity_EventScript_Placa3::
	msgbox CanalaveCity_Text_Placa3, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa3:
	.string "Canalave Dock$"

CanalaveCity_EventScript_Placa5::
	msgbox CanalaveCity_Text_Placa5, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa5:
	.string "Sailor Eldritch's House$"

CanalaveCity_EventScript_Placa6::
	msgbox CanalaveCity_Text_Placa6, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa6:
	.string "Harbor Inn\nA Roost for Restless Sailors\p'Enjoy sweet dreams in our\nsumptuous beds!'$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CanalaveCity_EventScript_Npc1::
	msgbox CanalaveCity_Text_Npc1, MSGBOX_NPC
	end

CanalaveCity_Text_Npc1:
	.string "What's up?\nYour clothes look damp.\pMaybe you took the boat to Iron Island\nto get a Hidden Machine, right?$"

CanalaveCity_EventScript_Npc2::
	msgbox CanalaveCity_Text_Npc2, MSGBOX_NPC
	end

CanalaveCity_Text_Npc2:
	.string "My PSYDUCK is very close to me.\nThat makes its Return move powerful!$"

CanalaveCity_EventScript_Npc3::
	msgbox CanalaveCity_Text_Npc3, MSGBOX_NPC
	end

CanalaveCity_Text_Npc3:
	.string "Welcome to Canalave City, the Canal\nCity!\pIn the old days, this port used to\nbe a hub of cargo transportation.$"

CanalaveCity_EventScript_Npc4::
	msgbox CanalaveCity_Text_Npc4, MSGBOX_NPC
	end

CanalaveCity_Text_Npc4:
	.string "I'm going to study at the library.\pI've taken an interest in the subject\nof time and space.$"

CanalaveCity_EventScript_Npc5::
	msgbox CanalaveCity_Text_Npc5, MSGBOX_NPC
	end

CanalaveCity_Text_Npc5:
	.string "PSYDUCK: Gua?$"

CanalaveCity_EventScript_Npc6::
	msgbox CanalaveCity_Text_Npc6, MSGBOX_NPC
	end

CanalaveCity_Text_Npc6:
	.string "The Gym Leader and Trainers of this Gym\noften go out to Iron Island.\pThey not only train their Pokémon,\nbut they work out as well.$"

CanalaveCity_EventScript_Npc7::
	msgbox CanalaveCity_Text_Npc7, MSGBOX_NPC
	end

CanalaveCity_Text_Npc7:
	.string "Do you wanna set sail?$"

CanalaveCity_EventScript_Placa8::
	msgbox CanalaveCity_Text_Placa8, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa8:
	.string "Canalave City\nCargo Port$"

CanalaveCity_EventScript_Placa9::
	msgbox CanalaveCity_Text_Placa9, MSGBOX_SIGN
	end

CanalaveCity_Text_Placa9:
	.string "The door is tightly shut.\nIt appears impossible to open.$"

@ ponytail: TRES ids, e nao um, porque os tres ramos EXISTEM nesta ROM. Medido
@ antes de escrever: data/maps/SandgemTown_RowanLab/scripts.inc escreve
@ VAR_STARTER_MON com 0, 1 e 2 (grama, fogo, agua) desde 05/08/2026, entao o
@ triangulo de tipos do rival e verdade aqui. O comentario do rival de JOHTO
@ (data/maps/CherrygroveCity/scripts.inc) diz o contrario e esta VELHO: ele foi
@ escrito quando o laboratorio ainda nao escrevia a var, e aponta para
@ SandgemTown_House1, que nao e o laboratorio.
@
@ O nome de cada constante e o inicial DO JOGADOR, nao o do rival: no Platinum o
@ ramo TURTWIG e o que roda quando o jogador tem Turtwig, e o ace daquele time e
@ Infernape (fogo bate grama). Conferido bloco a bloco em trainers.party.
@
@ Gatilho por RAIO DE VISAO (tecnica 3 do SINNOH-PADRAO.md), precedente do rival
@ de Johto: o motor faz exclamacao, aproximacao e memoria de "ja perdeu" de
@ graca. O `switch` roda DEPOIS da aproximacao e antes da batalha.
CanalaveCity_EventScript_Rival::
	lock
	faceplayer
	msgbox CanalaveCity_Text_CenaCheckReady, MSGBOX_DEFAULT
	switch VAR_STARTER_MON
	case 0, CanalaveCity_EventScript_RivalTurtwig
	case 1, CanalaveCity_EventScript_RivalChimchar
	goto CanalaveCity_EventScript_RivalPiplup
	end

CanalaveCity_EventScript_RivalTurtwig::
	trainerbattle_single TRAINER_SINNOH_RIVAL_CANALAVE_CITY_TURTWIG, CanalaveCity_Text_CenaCheckReady, CanalaveCity_Text_CenaIronIsland, CanalaveCity_EventScript_RivalBeaten
	end

CanalaveCity_EventScript_RivalChimchar::
	trainerbattle_single TRAINER_SINNOH_RIVAL_CANALAVE_CITY_CHIMCHAR, CanalaveCity_Text_CenaCheckReady, CanalaveCity_Text_CenaIronIsland, CanalaveCity_EventScript_RivalBeaten
	end

CanalaveCity_EventScript_RivalPiplup::
	trainerbattle_single TRAINER_SINNOH_RIVAL_CANALAVE_CITY_PIPLUP, CanalaveCity_Text_CenaCheckReady, CanalaveCity_Text_CenaIronIsland, CanalaveCity_EventScript_RivalBeaten
	end

CanalaveCity_EventScript_RivalBeaten::
	msgbox CanalaveCity_Text_CenaIronIsland, MSGBOX_DEFAULT
	setflag FLAG_GALACTICA_CANALAVE_RIVAL
	removeobject LOCALID_CANALAVE_CITY_RIVAL
	release
	end

CanalaveCity_Text_CenaCheckReady:
	.string "CEDRIC: Whoops!\nHey, {PLAYER}!\pYou're going to challenge the Gym\nLeader up past here, eh?\pSomeone should check to see if you're\nready for this challenge!\pThat someone is me!\nWith my brand-new Gym Badge!$"

CanalaveCity_Text_CenaIronIsland:
	.string "CEDRIC: Yeah, yeah, you're just\na bit better than me, as usual.\pBut listen up!\pLet me tell you who's going to take on\nthe Pokémon League and become the\pChampion.\pYou guessed right!\nIt's going to be me!\pAnyway, you should go to Iron Island\nand toughen up some more.\pYeah, train at Iron Island! That's what\nI did before going to the Gym!$"

@ ponytail: tres `call_if_defeated` e nao um, porque o rival tem TRES ids, um
@ por inicial do jogador, e so um deles chega a ser lutado. Quem ja venceu o seu
@ nao ve o rival de novo ao reentrar no mapa.
CanalaveCity_OnTransition:
	call_if_defeated TRAINER_SINNOH_RIVAL_CANALAVE_CITY_TURTWIG, CanalaveCity_EventScript_EsconderRival
	call_if_defeated TRAINER_SINNOH_RIVAL_CANALAVE_CITY_CHIMCHAR, CanalaveCity_EventScript_EsconderRival
	call_if_defeated TRAINER_SINNOH_RIVAL_CANALAVE_CITY_PIPLUP, CanalaveCity_EventScript_EsconderRival
	end

CanalaveCity_EventScript_EsconderRival::
	setflag FLAG_GALACTICA_CANALAVE_RIVAL
	return

@ >>> Lendarios de Sinnoh (dev_scripts/lendarios_sinnoh.py) >>>
CanalaveCity_EventScript_Darkrai::
	lockall
	msgbox CanalaveCity_Text_DarkraiIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_DARKRAI, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_DARKRAI, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_CANALAVE_CITY_DARKRAI
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CanalaveCity_EventScript_DarkraiSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CanalaveCity_EventScript_DarkraiPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
CanalaveCity_EventScript_DarkraiPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_CANALAVE_CITY_DARKRAI
	setflag FLAG_HIDE_DARKRAI_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CanalaveCity_EventScript_DarkraiSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_CANALAVE_CITY_DARKRAI
	setflag FLAG_HIDE_DARKRAI_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox CanalaveCity_Text_DarkraiSome, MSGBOX_DEFAULT
	return

CanalaveCity_Text_DarkraiIntro:
	.string "A shadow with no one to cast it\nstands still by the harbor...$"

CanalaveCity_Text_DarkraiSome:
	.string "DARKRAI melted away into the\ndarkness...$"

CanalaveCity_EventScript_Cresselia::
	lockall
	msgbox CanalaveCity_Text_CresseliaIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_CRESSELIA, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_CRESSELIA, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_CANALAVE_CITY_CRESSELIA
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CanalaveCity_EventScript_CresseliaSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CanalaveCity_EventScript_CresseliaPreso
	releaseall
	end

@ ponytail: so apaga o bicho em VITORIA ou CAPTURA. Fugir, perder ou
@ ser teleportado deixa ele no mapa, senao uma bola errada tira o
@ lendario do save. Mesma regra do LUGIA e do SpearPillar_Dialga.
CanalaveCity_EventScript_CresseliaPreso::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_CANALAVE_CITY_CRESSELIA
	setflag FLAG_HIDE_CRESSELIA_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CanalaveCity_EventScript_CresseliaSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_CANALAVE_CITY_CRESSELIA
	setflag FLAG_HIDE_CRESSELIA_SINNOH
	fadescreenswapbuffers FADE_FROM_BLACK
	msgbox CanalaveCity_Text_CresseliaSome, MSGBOX_DEFAULT
	return

CanalaveCity_Text_CresseliaIntro:
	.string "A crescent glow drifts in from over\nthe sea...$"

CanalaveCity_Text_CresseliaSome:
	.string "The Pokemon flew off somewhere...$"

@ <<< Lendarios de Sinnoh <<<
