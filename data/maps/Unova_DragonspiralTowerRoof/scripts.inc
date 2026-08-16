@ DragonspiralTowerRoof do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5).
@
@ FONTE: fontes-mapas/bw3g/maps/DragonspiralTowerRoof.asm. Dois coord_events,
@ (8,14) e (9,14), no mesmo fecho. E o climax do arco do dragao: o ZINZOLIN
@ liga o GENESIS PROJECT, a JUNIPER aparece controlada pela MIND LINK, o
@ jogador bate o ZINZOLIN, as tres SOMBRAS o traem em nome do GHETSIS, e o
@ DRAYDEN paga com a DRAGON FANG.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   VAR_UNOVA_DRAGONSPIRAL_TOPO_CENA: 0 = SCENE_DEFAULT, 1 = SCENE_FINISHED.
@
@ EVENT_ da fonte -> FLAG_ da tabela:
@   EVENT_GOT_DRAGON_FANG              -> FLAG_UNOVA_RECEBEU_PRESA_DRAGAO
@   EVENT_DRAYDENS_HOUSE_DRAGON_FANG   -> FLAG_UNOVA_DRAYDEN_CASA_PRESA_DRAGAO
@   EVENT_DRAGONSPIRAL_TOWER_SAGES     -> FLAG_UNOVA_DRAGONSPIRAL_SABIOS
@   EVENT_FINISHED_DRAGONSPIRAL_TOWER  -> FLAG_UNOVA_DRAGONSPIRAL_CONCLUIDA
@   EVENT_OPELUCID_CITY_IRIS           -> FLAG_UNOVA_OPELUCID_IRIS
@   EVENT_DRAYDENS_HOUSE_IRIS          -> FLAG_UNOVA_DRAYDEN_CASA_IRIS
@
@ ELENCO, zero flag nova (janela de save fechada): duas flags TEMPORARIAS
@ recalculadas pelo ON_TRANSITION. O motor limpa os FLAG_TEMP_* em
@ `ClearTempFieldEventData()` (src/overworld.c:893) ANTES do
@ `RunOnTransitionMapScript()` (:909), e os objetos so nascem depois, olhando
@ `template->flagId` (src/event_object_movement.c:2920).
@   FLAG_TEMP_11 = quem ja esta no telhado quando o jogador chega: DRAYDEN,
@                  ZINZOLIN, SOMBRA 1 e o GENESECT desligado. So no estagio 0.
@   FLAG_TEMP_12 = quem entra no meio da cena e por isso NUNCA nasce sozinho:
@                  JUNIPER, SOMBRA 2, SOMBRA 3 e o GENESECT ligado. O
@                  `addobject` cria mesmo com a flag acesa, porque
@                  `TrySpawnObjectEvent` nao consulta flag.
@ Isso tambem substitui o callback `.AppearRoofObjects` de
@ DragonspiralTower6F.asm, que existia so para rearmar este elenco quando o
@ jogador perdia para o ZINZOLIN: aqui o estado e recalculado da var toda vez.
@
@ Ids locais (indice no map.json + 1): 1 = DRAYDEN, 2 = ZINZOLIN,
@ 3 = JUNIPER, 4 = SOMBRA 1, 5 = SOMBRA 2, 6 = SOMBRA 3, 7 = GENESECT
@ desligado, 8 = GENESECT ligado.
@
@ DESCARTADOS: `setlasttalked`, `dontrestartmapmusic`, `reloadmapafterbattle`
@ (cobertos pelo `trainerbattle_no_intro`); `special ReloadSpritesNoPalettes` e
@ `special LoadMapPalettes` (nao existe equivalente e nenhuma palette muda
@ aqui).
@ FADES: `special FadeOutMusic` -> `special Script_FadeOutMapMusic` +
@ `waitstate`; `special FadeOutPalettes` -> `fadescreen FADE_TO_BLACK`;
@ `FadeBlackQuickly` -> `fadescreenspeed FADE_TO_BLACK, 8`; `FadeInQuickly` ->
@ `fadescreenspeed FADE_FROM_BLACK, 8`; `playmapmusic` -> `fadedefaultbgm`.
@ `teleport_to` / `teleport_from` do gen 2 nao tem movimento equivalente: viram
@ SE_WARP_IN + `addobject` e SE_WARP_OUT + `removeobject`, o mesmo idioma que a
@ ChampionsRoomEntrance ja usa. Som igual, animacao de subir e descer nao
@ existe.
@ `follow DRAYDEN, JUNIPER` / `stopfollow` tambem nao existe aqui: a JUNIPER
@ leva o roteiro que o motor de gen 2 daria a ela ao seguir o DRAYDEN, cinco
@ passos para baixo, terminando em (7,13) enquanto ele para em (8,13). Os dois
@ ficam de frente para o jogador quando ele desce para (9,13), que e o que a
@ cena precisa.
@ MUSICA: MUSIC_ROCKET_ENCOUNTER -> MUS_ENCOUNTER_AQUA.
@ ROTAS DO JOGADOR conferidas no map.bin de LAYOUT_UNOVA_DRAGONSPIRAL_TOWER_ROOF:
@ (8,14)->(8,13)->(9,13)->(9,12)->(9,11) e (9,14)->(9,13)->(9,12)->(9,11),
@ depois (9,11)->(9,12)->(9,13); colisao 0 em todos.

Unova_DragonspiralTowerRoof_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_DragonspiralTowerRoof_OnTransition
	.byte 0

Unova_DragonspiralTowerRoof_OnTransition:
	setflag FLAG_TEMP_12
	goto_if_eq VAR_UNOVA_DRAGONSPIRAL_TOPO_CENA, 0, Unova_DragonspiralTowerRoof_EventScript_TransicaoFim
	setflag FLAG_TEMP_11
Unova_DragonspiralTowerRoof_EventScript_TransicaoFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
Unova_DragonspiralTowerRoof_EventScript_DragonspiralTowerRoofScript1::
	lockall
	applymovement LOCALID_PLAYER, Unova_DragonspiralTowerRoof_Movement_JogadorChegaPelaEsquerda
	waitmovement 0
	goto Unova_DragonspiralTowerRoof_EventScript_DragonspiralTowerRoofScript

Unova_DragonspiralTowerRoof_EventScript_DragonspiralTowerRoofScript2::
	lockall
	applymovement LOCALID_PLAYER, Unova_DragonspiralTowerRoof_Movement_JogadorChegaReto
	waitmovement 0
	@ cai no proximo, como na fonte

Unova_DragonspiralTowerRoof_EventScript_DragonspiralTowerRoofScript::
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	msgbox Unova_DragonspiralTowerRoof_Text_RoofIntro, MSGBOX_DEFAULT
	closemessage
	applymovement 2, Unova_DragonspiralTowerRoof_Movement_ZinzolinSobe
	waitmovement 0
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	playse SE_SHINY
	waitse
	delay 15
	playse SE_SHINY
	waitse
	delay 30
	playse SE_PC_ON
	fadescreen FADE_TO_BLACK
	addobject 8
	turnobject LOCALID_PLAYER, DIR_NORTH
	delay 5
	removeobject 7
	waitse
	fadescreen FADE_FROM_BLACK
	delay 30
	msgbox Unova_DragonspiralTowerRoof_Text_RoofCry, MSGBOX_DEFAULT
	closemessage
	playmoncry SPECIES_GENESECT, CRY_MODE_NORMAL
	waitmoncry
	delay 15
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	turnobject 2, DIR_SOUTH
	msgbox Unova_DragonspiralTowerRoof_Text_RoofPoweredOn, MSGBOX_DEFAULT
	closemessage
	playse SE_WARP_IN
	addobject 5
	waitse
	playse SE_WARP_IN
	addobject 6
	waitse
	playse SE_WARP_IN
	addobject 3
	waitse
	delay 30
	applymovement 1, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox Unova_DragonspiralTowerRoof_Text_RoofJuniperReveal, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_DragonspiralTowerRoof_Movement_DraydenSeAproxima
	waitmovement 0
	delay 30
	applymovement 1, Unova_DragonspiralTowerRoof_Movement_DraydenRecua
	applymovement 3, Unova_DragonspiralTowerRoof_Movement_JuniperSegueDrayden
	waitmovement 0
	turnobject 1, DIR_NORTH
	turnobject 3, DIR_NORTH
	msgbox Unova_DragonspiralTowerRoof_Text_RoofTimeForBattle, MSGBOX_DEFAULT
	closemessage
	applymovement 2, Unova_DragonspiralTowerRoof_Movement_ZinzolinDesce
	waitmovement 0
	msgbox Unova_DragonspiralTowerRoof_Text_RoofStartBattle, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_UNOVA_ZINZOLIN2, Unova_DragonspiralTowerRoof_Text_RoofBattleWin
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	delay 15
	msgbox Unova_DragonspiralTowerRoof_Text_RoofAfterBattle, MSGBOX_DEFAULT
	closemessage
	turnobject 4, DIR_EAST
	turnobject 5, DIR_EAST
	turnobject 6, DIR_EAST
	turnobject 2, DIR_WEST
	msgbox Unova_DragonspiralTowerRoof_Text_RoofBetrayalReveal, MSGBOX_DEFAULT
	closemessage
	applymovement 6, Unova_DragonspiralTowerRoof_Movement_Sombra3Cerca
	waitmovement 0
	turnobject 2, DIR_NORTH
	applymovement 5, Unova_DragonspiralTowerRoof_Movement_Sombra2Cerca
	applymovement 4, Unova_DragonspiralTowerRoof_Movement_Sombra1Cerca
	waitmovement 0
	msgbox Unova_DragonspiralTowerRoof_Text_RoofShadowBetrayal, MSGBOX_DEFAULT
	closemessage
	special Script_FadeOutMapMusic
	waitstate
	fadescreenspeed FADE_TO_BLACK, 8
	delay 15
	playse SE_WARP_OUT
	waitse
	removeobject 4
	removeobject 5
	removeobject 6
	removeobject 8
	delay 15
	fadescreenspeed FADE_FROM_BLACK, 8
	fadedefaultbgm
	delay 15
	msgbox Unova_DragonspiralTowerRoof_Text_RoofZinzolinFreakout, MSGBOX_DEFAULT
	closemessage
	applymovement 2, Unova_DragonspiralTowerRoof_Movement_ZinzolinFoge
	waitmovement 0
	removeobject 2
	delay 30
	applymovement LOCALID_PLAYER, Unova_DragonspiralTowerRoof_Movement_JogadorDesce
	waitmovement 0
	turnobject 3, DIR_EAST
	turnobject 1, DIR_EAST
	msgbox Unova_DragonspiralTowerRoof_Text_RoofJuniperThanks, MSGBOX_DEFAULT
	closemessage
	playse SE_WARP_OUT
	removeobject 3
	waitse
	turnobject LOCALID_PLAYER, DIR_WEST
	msgbox Unova_DragonspiralTowerRoof_Text_RoofDraydenThanks, MSGBOX_DEFAULT
	closemessage
	giveitem ITEM_DRAGON_FANG
	goto_if_eq VAR_RESULT, FALSE, Unova_DragonspiralTowerRoof_EventScript_SemEspacoNaMochila
	setflag FLAG_UNOVA_RECEBEU_PRESA_DRAGAO
	goto Unova_DragonspiralTowerRoof_EventScript_DraydenSeDespede

Unova_DragonspiralTowerRoof_EventScript_SemEspacoNaMochila::
	msgbox Unova_DragonspiralTowerRoof_Text_RoofDraydenNoRoom, MSGBOX_DEFAULT
	closemessage
	clearflag FLAG_UNOVA_DRAYDEN_CASA_PRESA_DRAGAO
Unova_DragonspiralTowerRoof_EventScript_DraydenSeDespede::
	msgbox Unova_DragonspiralTowerRoof_Text_RoofDraydenLeave, MSGBOX_DEFAULT
	closemessage
	playse SE_WARP_OUT
	removeobject 1
	waitse
	setflag FLAG_UNOVA_DRAGONSPIRAL_SABIOS
	setflag FLAG_UNOVA_DRAGONSPIRAL_CONCLUIDA
	setflag FLAG_UNOVA_OPELUCID_IRIS
	clearflag FLAG_UNOVA_DRAYDEN_CASA_IRIS
	setvar VAR_UNOVA_DRAGONSPIRAL_TOPO_CENA, 1
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_DragonspiralTowerRoof_Movement_JogadorChegaPelaEsquerda:
	walk_up
	walk_right
	walk_up
	walk_up
	step_end

Unova_DragonspiralTowerRoof_Movement_JogadorChegaReto:
	walk_up
	walk_up
	walk_up
	step_end

Unova_DragonspiralTowerRoof_Movement_JogadorDesce:
	walk_down
	walk_down
	face_left
	step_end

Unova_DragonspiralTowerRoof_Movement_ZinzolinSobe:
	walk_up
	step_end

Unova_DragonspiralTowerRoof_Movement_ZinzolinDesce:
	walk_down
	step_end

Unova_DragonspiralTowerRoof_Movement_DraydenSeAproxima:
	walk_fast_left
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end

Unova_DragonspiralTowerRoof_Movement_DraydenRecua:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_right
	step_end

@ O que o `follow` do gen 2 faria com a JUNIPER atras do DRAYDEN.
Unova_DragonspiralTowerRoof_Movement_JuniperSegueDrayden:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Unova_DragonspiralTowerRoof_Movement_Sombra1Cerca:
	walk_up
	walk_up
	walk_up
	face_down
	step_end

Unova_DragonspiralTowerRoof_Movement_Sombra2Cerca:
	walk_up
	walk_right
	walk_right
	walk_up
	walk_right
	face_down
	step_end

Unova_DragonspiralTowerRoof_Movement_Sombra3Cerca:
	walk_up
	walk_up
	walk_right
	walk_right
	walk_down
	step_end

Unova_DragonspiralTowerRoof_Movement_ZinzolinFoge:
	walk_fast_right
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_left
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

Unova_DragonspiralTowerRoof_Text_RoofIntro::
	.string "ZINZOLIN: So,"
	.string "\nyou've come to"
	.string "\ltry to stop me?"
	.string "\pHa! Once again,"
	.string "\nyou're too late!"
	.string "\pWhile you were"
	.string "\nbusy dealing with"
	.string "\pmy SAGEs, I've"
	.string "\nextracted the ICE"
	.string "\pELEMENT from atop"
	.string "\nthis tower. Now,"
	.string "\pwith the ELEMENTS"
	.string "\nof FIRE, WATER,"
	.string "\pTHUNDER, and ICE,"
	.string "\nTEAM PLASMA's"
	.string "\pultimate weapon"
	.string "\nwill be unstopp-"
	.string "\lable!$"

Unova_DragonspiralTowerRoof_Text_RoofCry::
	.string "SEEEEEECT!$"

Unova_DragonspiralTowerRoof_Text_RoofPoweredOn::
	.string "ZINZOLIN: That's"
	.string "\nright! What you're"
	.string "\plooking at is the"
	.string "\nend result of TEAM"
	.string "\pPLASMA's efforts"
	.string "\nto create the"
	.string "\lultimate POKéMON!"
	.string "\pBehold, the"
	.string "\nGENESIS PROJECT!"
	.string "\pThe foolish boy"
	.string "\nking tried to have"
	.string "\pthe project shut"
	.string "\ndown, but it was"
	.string "\pcontinued in"
	.string "\nsecret. And now,"
	.string "\pwe will use its"
	.string "\npower to conquer"
	.string "\lUNOVA!"
	.string "\pIt just needs one"
	.string "\nmore final touch."
	.string "\pSHADOWs! To me!$"

Unova_DragonspiralTowerRoof_Text_RoofJuniperReveal::
	.string "DRAYDEN: PROF."
	.string "\nJUNIPER!"
	.string "\pJUNIPER: …huh?"
	.string "\nWha… What's"
	.string "\lhappening…?"
	.string "\pWhat am I doing"
	.string "\nhere?"
	.string "\pZINZOLIN: Mwa ha"
	.string "\nha! Thanks to the"
	.string "\pPROF here, I was"
	.string "\nfinally able to"
	.string "\pget my hands on"
	.string "\nthe one piece"
	.string "\pmissing for my"
	.string "\nplan: the MIND"
	.string "\lLINK!"
	.string "\pJUNIPER: Wha…?"
	.string "\pZINZOLIN: It"
	.string "\nmay have taken the"
	.string "\ppower of two of my"
	.string "\nSHADOWs to influ-"
	.string "\lence her mind, but"
	.string "\pwith our dear"
	.string "\nPROF. under my"
	.string "\pcontrol, taking"
	.string "\nthe MIND LINK from"
	.string "\pthe POKéMON LEAGUE"
	.string "\nwas no problem at"
	.string "\lall!"
	.string "\pDRAYDEN: You- You"
	.string "\nvillains!$"

Unova_DragonspiralTowerRoof_Text_RoofTimeForBattle::
	.string "JUNIPER: Ah… I'm"
	.string "\nsorry. I wasn't"
	.string "\lmyself…"
	.string "\pZINZOLIN: A-ha-ha!"
	.string "\nIt's too late!"
	.string "\pYou've already"
	.string "\ngiven me every-"
	.string "\lthing I need!"
	.string "\pNow, before I put"
	.string "\nthe finishing"
	.string "\ptouches on my"
	.string "\nplan, there's just"
	.string "\pone more thing to"
	.string "\ntake care of.$"

Unova_DragonspiralTowerRoof_Text_RoofStartBattle::
	.string "You will not stand"
	.string "\nin my way any"
	.string "\plonger! Prepare to"
	.string "\nfeel the freezing"
	.string "\pvengeance of TEAM"
	.string "\nPLASMA!$"

Unova_DragonspiralTowerRoof_Text_RoofBattleWin::
	.string "I- Impossible!$"

Unova_DragonspiralTowerRoof_Text_RoofAfterBattle::
	.string "ZINZOLIN: …It"
	.string "\nmatters not. With"
	.string "\pthe GENESIS"
	.string "\nPROJECT under my"
	.string "\pcontrol, I am"
	.string "\nunstoppable!$"

Unova_DragonspiralTowerRoof_Text_RoofBetrayalReveal::
	.string "Come SHADOWs! Let"
	.string "\nus prepare the"
	.string "\pfinal stages of"
	.string "\nmy plan!"
	.string "\pI will use the"
	.string "\nGENESIS PROJECT to"
	.string "\pbecome the ruler"
	.string "\nof UNOVA!"
	.string "\pSHADOW: …How"
	.string "\namusing."
	.string "\pZINZOLIN: Wha…?"
	.string "\pSHADOW: You truly"
	.string "\nbelieve you were"
	.string "\pto become a ruler?"
	.string "\pSHADOW: How sad…$"

Unova_DragonspiralTowerRoof_Text_RoofShadowBetrayal::
	.string "ZINZOLIN: Wha-"
	.string "\nWhat are you"
	.string "\pdoing?! Stop this"
	.string "\nat once! Your"
	.string "\lking demands it!"
	.string "\pSHADOW: You fool…"
	.string "\pSHADOW: We only"
	.string "\nserve one king."
	.string "\pSHADOW: The one"
	.string "\ntrue king of TEAM"
	.string "\lPLASMA."
	.string "\pSHADOW: The great"
	.string "\nand mighty"
	.string "\lGHETSIS!"
	.string "\pZINZOLIN: What?!"
	.string "\nGHETSIS?! GHETSIS"
	.string "\lis gone! He's lost"
	.string "\phis mind! That's"
	.string "\nwhy I'm the king"
	.string "\lnow!"
	.string "\pSHADOW: You're"
	.string "\nwrong! GHETSIS"
	.string "\pwill return to"
	.string "\ntake his rightful"
	.string "\pplace as the ruler"
	.string "\nof TEAM PLASMA."
	.string "\pSHADOW: And you"
	.string "\nwere but a pawn in"
	.string "\lour plan."
	.string "\pSHADOW: We must"
	.string "\nthank you for"
	.string "\pfinding the"
	.string "\nGENESIS PROJECT,"
	.string "\pand collecting the"
	.string "\nELEMENTs needed to"
	.string "\lrestore its power."
	.string "\pSHADOW: Thanks to"
	.string "\nyou and the other"
	.string "\pSAGEs, we were"
	.string "\nable to override"
	.string "\pthe security lock"
	.string "\nto activate the"
	.string "\lMIND LINK."
	.string "\pSHADOW: How"
	.string "\nconvenient that"
	.string "\pROOD had a grand-"
	.string "\ndaughter who could"
	.string "\punlock his part of"
	.string "\nthe seal…"
	.string "\pSHADOW: But though"
	.string "\nyou've been of"
	.string "\puse, now that we"
	.string "\nhave the MIND LINK"
	.string "\pand the GENESIS"
	.string "\nPROJECT, you are"
	.string "\pno longer of use"
	.string "\nto us…"
	.string "\pSHADOW: Farewell…"
	.string "\pZINZOLIN: No! You"
	.string "\ncan't do this to"
	.string "\pme! I am your"
	.string "\nking!$"

Unova_DragonspiralTowerRoof_Text_RoofZinzolinFreakout::
	.string "ZINZOLIN: This…"
	.string "\nThis is not"
	.string "\lpossible!"
	.string "\pI am the king of"
	.string "\nTEAM PLASMA!!"
	.string "\p… … … …"
	.string "\pI… I think I'd"
	.string "\nbetter get out of"
	.string "\lhere…$"

Unova_DragonspiralTowerRoof_Text_RoofJuniperThanks::
	.string "JUNIPER: {PLAYER}!"
	.string "\pThat was quite a"
	.string "\nbattle! I'm"
	.string "\limpressed!"
	.string "\pThank you for your"
	.string "\nhelp. I… I'm not"
	.string "\ptruly sure what"
	.string "\nhappened to me…"
	.string "\pMy memories have"
	.string "\nbeen hazy ever"
	.string "\psince the WORLD"
	.string "\nTOURNAMENT."
	.string "\pBut if I've been"
	.string "\nused for those"
	.string "\lSHADOWs' plan…"
	.string "\pThen I'm going to"
	.string "\nput a stop to it!"
	.string "\pSafe travels,"
	.string "\n{PLAYER}.$"

Unova_DragonspiralTowerRoof_Text_RoofDraydenThanks::
	.string "DRAYDEN: Thank you"
	.string "\nfor your help,"
	.string "\l{PLAYER}."
	.string "\pYou handled your-"
	.string "\nself quite well."
	.string "\pI look forward to"
	.string "\nchallenging you in"
	.string "\lmy GYM."
	.string "\pBut before I go,"
	.string "\nI'd like you to"
	.string "\lhave this.$"

Unova_DragonspiralTowerRoof_Text_RoofDraydenNoRoom::
	.string "Oh, it seems you"
	.string "\ndon't have room"
	.string "\lfor it."
	.string "\pI will leave it"
	.string "\nfor you in my"
	.string "\phouse in OPELUCID"
	.string "\nCITY. Stop by and"
	.string "\ppick it up at your"
	.string "\nconvenience.$"

Unova_DragonspiralTowerRoof_Text_RoofDraydenLeave::
	.string "I'm going back to"
	.string "\nmy GYM in OPELUCID"
	.string "\lCITY now."
	.string "\pStop by if you'd"
	.string "\nlike to challenge"
	.string "\pme. I'll be"
	.string "\nI'll be looking"
	.string "\lforward to it.$"
