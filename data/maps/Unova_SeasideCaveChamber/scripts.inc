@ SeasideCaveChamber do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 15/08/2026 (B6 Obra 1, bloco A5).
@
@ FONTE: fontes-mapas/bw3g/maps/SeasideCaveChamber.asm. Dois coord_events,
@ (6,9) e (7,9), no mesmo fecho: a PRIMEIRA batalha contra o ZINZOLIN, o
@ telefonema da BIANCA e a explicacao do MARLON sobre a MIND LINK.
@
@ TRADUCAO DO setscene (tabela do PLANO-OBRAS-UNOVA.md):
@   VAR_UNOVA_SEASIDE_CAVE_CAMARA_CENA: 0 = SCENE_DEFAULT, 1 = SCENE_FINISHED.
@
@ O setmapscene REMOTO do fim da cena:
@   `setmapscene R_12_VILLAGE_BRIDGE_GATE, SCENE_FINISHED`
@   -> `setvar VAR_UNOVA_R12_VILLAGE_BRIDGE_PORTAO_CENA, 1`
@   (tabela do PLANO: 0 = SCENE_DEFAULT, 1 = SCENE_FINISHED). E o que libera a
@   ponte para OPELUCID CITY de que o MARLON fala no fim da fala dele.
@
@ ELENCO, zero flag nova (janela de save fechada): os CINCO figurantes desta
@ camara ja estao no mapa quando o jogador chega (a fonte nunca faz `appear`
@ em nenhum deles) e somem juntos no fim. Um gate so, FLAG_TEMP_11, aceso pelo
@ ON_TRANSITION quando a var ja saiu de 0. O motor limpa os FLAG_TEMP_* em
@ `ClearTempFieldEventData()` (src/overworld.c:893) ANTES do
@ `RunOnTransitionMapScript()` (:909), e os objetos so nascem depois, olhando
@ `template->flagId` (src/event_object_movement.c:2920).
@
@ Ids locais (indice no map.json + 1): 1 = ZINZOLIN, 2 = SOMBRA 1,
@ 3 = SOMBRA 2, 4 = CHEREN, 5 = MARLON.
@
@ DESCARTADOS: `setlasttalked`, `dontrestartmapmusic`, `reloadmapafterbattle`
@ (cobertos pelo `trainerbattle_no_intro`); `special ReloadSpritesNoPalettes`
@ (sem equivalente, nenhuma palette muda aqui); `playmusic MUSIC_UNOVA_CAVE`
@ no fim vira `fadedefaultbgm`, porque a faixa da caverna ja e a musica deste
@ mapa.
@ FADES: `special FadeOutMusic` -> `special Script_FadeOutMapMusic` +
@ `waitstate`; `FadeBlackQuickly` -> `fadescreenspeed FADE_TO_BLACK, 8`;
@ `FadeInQuickly` -> `fadescreenspeed FADE_FROM_BLACK, 8`.
@ MUSICA: MUSIC_ROCKET_ENCOUNTER -> MUS_ENCOUNTER_AQUA; MUSIC_CHEREN_THEME ->
@ MUS_ENCOUNTER_BRENDAN. Nenhuma faixa nova foi criada.
@ ROTAS DO JOGADOR conferidas no map.bin de LAYOUT_UNOVA_SEASIDE_CAVE_CHAMBER:
@ (6,9)->(6,8)->(6,7)->(5,7)->(5,6)->(5,5) e (7,9)->(7,8)->(7,7)->(6,7)->
@ (5,7)->(5,6)->(5,5); colisao 0 em todos os quadrantes.

Unova_SeasideCaveChamber_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_SeasideCaveChamber_OnTransition
	.byte 0

Unova_SeasideCaveChamber_OnTransition:
	goto_if_eq VAR_UNOVA_SEASIDE_CAVE_CAMARA_CENA, 0, Unova_SeasideCaveChamber_EventScript_TransicaoFim
	setflag FLAG_TEMP_11
Unova_SeasideCaveChamber_EventScript_TransicaoFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
Unova_SeasideCaveChamber_EventScript_SeasideCaveZinzolinScript1::
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	applymovement LOCALID_PLAYER, Unova_SeasideCaveChamber_Movement_JogadorPelaEsquerda
	waitmovement 0
	goto Unova_SeasideCaveChamber_EventScript_SeasideCaveZinzolinScript

Unova_SeasideCaveChamber_EventScript_SeasideCaveZinzolinScript2::
	lockall
	special Script_FadeOutMapMusic
	waitstate
	delay 15
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	applymovement LOCALID_PLAYER, Unova_SeasideCaveChamber_Movement_JogadorPelaDireita
	waitmovement 0
	@ cai no proximo, como na fonte

Unova_SeasideCaveChamber_EventScript_SeasideCaveZinzolinScript::
	turnobject 1, DIR_SOUTH
	msgbox Unova_SeasideCaveChamber_Text_SeasideCaveZinzolinIntro, MSGBOX_DEFAULT
	closemessage
	trainerbattle_no_intro TRAINER_UNOVA_ZINZOLIN1, Unova_SeasideCaveChamber_Text_SeasideCaveZinzolinBeaten
	playbgm MUS_ENCOUNTER_AQUA, FALSE
	msgbox Unova_SeasideCaveChamber_Text_SeasideCaveZinzolinAfter, MSGBOX_DEFAULT
	closemessage
	applymovement 2, Unova_SeasideCaveChamber_Movement_Sombra1
	applymovement 3, Unova_SeasideCaveChamber_Movement_Sombra2
	waitmovement 0
	special Script_FadeOutMapMusic
	waitstate
	fadescreenspeed FADE_TO_BLACK, 8
	delay 15
	playse SE_WARP_OUT
	waitse
	removeobject 1
	removeobject 2
	removeobject 3
	delay 15
	fadescreenspeed FADE_FROM_BLACK, 8
	playbgm MUS_ENCOUNTER_BRENDAN, FALSE
	delay 15
	turnobject LOCALID_PLAYER, DIR_SOUTH
	applymovement 5, Unova_SeasideCaveChamber_Movement_MarlonSeAproxima
	applymovement 4, Unova_SeasideCaveChamber_Movement_CherenSeAproxima
	waitmovement 0
	msgbox Unova_SeasideCaveChamber_Text_SeasideCaveMarlonAfter, MSGBOX_DEFAULT
	closemessage
	applymovement 4, Common_Movement_ExclamationMark
	waitmovement 0
	playse SE_POKENAV_CALL
	waitse
	msgbox Unova_SeasideCaveChamber_Text_SeasideCaveCherenPhone, MSGBOX_DEFAULT
	closemessage
	playse SE_POKENAV_HANG_UP
	waitse
	turnobject 4, DIR_WEST
	turnobject 5, DIR_EAST
	msgbox Unova_SeasideCaveChamber_Text_SeasideCaveCherenLeave, MSGBOX_DEFAULT
	closemessage
	applymovement 4, Unova_SeasideCaveChamber_Movement_CherenSai
	waitmovement 0
	playse SE_DOOR
	waitse
	removeobject 4
	special Script_FadeOutMapMusic
	waitstate
	delay 30
	fadedefaultbgm
	turnobject 5, DIR_NORTH
	msgbox Unova_SeasideCaveChamber_Text_SeasideCaveMarlonExplanation, MSGBOX_DEFAULT
	closemessage
	applymovement 5, Unova_SeasideCaveChamber_Movement_MarlonSai
	waitmovement 0
	playse SE_DOOR
	waitse
	removeobject 5
	setvar VAR_UNOVA_SEASIDE_CAVE_CAMARA_CENA, 1
	@ setmapscene remoto: libera a ponte de VILLAGE BRIDGE
	setvar VAR_UNOVA_R12_VILLAGE_BRIDGE_PORTAO_CENA, 1
	releaseall
	end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_SeasideCaveChamber_Movement_JogadorPelaEsquerda:
	walk_up
	walk_up
	walk_left
	walk_up
	walk_up
	step_end

Unova_SeasideCaveChamber_Movement_JogadorPelaDireita:
	walk_up
	walk_up
	walk_left
	walk_left
	walk_up
	walk_up
	step_end

Unova_SeasideCaveChamber_Movement_Sombra1:
	walk_fast_right
	walk_fast_up
	walk_fast_up
	face_right
	step_end

Unova_SeasideCaveChamber_Movement_Sombra2:
	walk_fast_left
	walk_fast_up
	walk_fast_up
	face_left
	step_end

Unova_SeasideCaveChamber_Movement_MarlonSeAproxima:
	walk_right
	walk_right
	walk_up
	step_end

Unova_SeasideCaveChamber_Movement_CherenSeAproxima:
	walk_left
	walk_left
	face_up
	step_end

Unova_SeasideCaveChamber_Movement_CherenSai:
	walk_down
	walk_down
	walk_down
	walk_down
	walk_down
	step_end

Unova_SeasideCaveChamber_Movement_MarlonSai:
	walk_down
	walk_down
	walk_down
	walk_right
	walk_down
	walk_down
	step_end

Unova_SeasideCaveChamber_Text_SeasideCaveZinzolinIntro::
	.string "ZINZOLIN: Ah,"
	.string "\n{PLAYER}. I was"
	.string "\lexpecting you."
	.string "\pYou've come to"
	.string "\nstop my plans?"
	.string "\pHa! I'm afraid"
	.string "\nyou're too late,"
	.string "\lchild!"
	.string "\pWhile my SHADOWs"
	.string "\nwere keeping those"
	.string "\lGYM LEADERs busy,"
	.string "\pI've already"
	.string "\nextracted the"
	.string "\pWATER ELEMENT from"
	.string "\nthis pool!"
	.string "\pNow only one"
	.string "\nELEMENT remains"
	.string "\pbefore my master"
	.string "\nplan is complete!"
	.string "\pBut don't think"
	.string "\nI'm just going to"
	.string "\plet you leave"
	.string "\nthat easily."
	.string "\pConsider this"
	.string "\npunishment for"
	.string "\pyour arrogance at"
	.string "\nthe POKéMON WORLD"
	.string "\lTOURNAMENT!$"

Unova_SeasideCaveChamber_Text_SeasideCaveZinzolinBeaten::
	.string "Impossible!$"

Unova_SeasideCaveChamber_Text_SeasideCaveZinzolinAfter::
	.string "ZINZOLIN: What?"
	.string "\nAgain?!"
	.string "\p…not that it"
	.string "\nmatters. I have"
	.string "\lwhat I came for."
	.string "\pAnd by now, I've"
	.string "\nkept you all busy"
	.string "\lfor long enough,"
	.string "\pmy other plan"
	.string "\nshould be finished"
	.string "\las well!"
	.string "\pFarewell, you"
	.string "\nfools!"
	.string "\pSHADOWs! To me!$"

Unova_SeasideCaveChamber_Text_SeasideCaveMarlonAfter::
	.string "MARLON: Hey, that"
	.string "\nwas some nice"
	.string "\lbattlin', {PLAYER}!"
	.string "\pSorry we couldn't"
	.string "\nbe much help."
	.string "\pWe had our hands"
	.string "\nfull with those"
	.string "\lninja fellas."
	.string "\pCHEREN: I'm more"
	.string "\nconcerned with"
	.string "\pwhat he said"
	.string "\nafterward…"
	.string "\pHis other plan…?$"

Unova_SeasideCaveChamber_Text_SeasideCaveCherenPhone::
	.string "Hello? You've"
	.string "\nreached CHEREN."
	.string "\pOh, BIANCA? Wha-"
	.string "\pWait! Slow down!"
	.string "\p… … … …"
	.string "\pI see, I see…"
	.string "\p… … … …"
	.string "\pBut how did-"
	.string "\nNevermind. This"
	.string "\lis a problem…"
	.string "\pI'll meet you"
	.string "\nthere soon.$"

Unova_SeasideCaveChamber_Text_SeasideCaveCherenLeave::
	.string "CHEREN: This is"
	.string "\nbad…"
	.string "\pMARLON, you remem-"
	.string "\nber we moved that"
	.string "\lthing out of"
	.string "\lyour GYM?"
	.string "\pThe PROF just"
	.string "\ncalled, she says"
	.string "\lit's been taken."
	.string "\pMARLON: What? But"
	.string "\nwe moved that"
	.string "\pthing to the POKé-"
	.string "\nMON LEAGUE!"
	.string "\pNo one other than"
	.string "\nLEAGUE members"
	.string "\pshoulda been able"
	.string "\nto get in there."
	.string "\pCHEREN: That's the"
	.string "\nthing. According"
	.string "\lto the PROF…"
	.string "\pThe only person"
	.string "\nseen entering that"
	.string "\larea…"
	.string "\pwas PROF.JUNIPER…"
	.string "\p…I don't know what"
	.string "\nthis means. I'm"
	.string "\lgoing to meet with"
	.string "\pPROF.BIANCA and"
	.string "\nwe'll figure out"
	.string "\lwhat to do from"
	.string "\lthere."
	.string "\pSorry guys… Take"
	.string "\ncare.$"

Unova_SeasideCaveChamber_Text_SeasideCaveMarlonExplanation::
	.string "MARLON: Well now,"
	.string "\nthat thing's been"
	.string "\lnothing but"
	.string "\ltrouble…"
	.string "\pI guess I'd better"
	.string "\nexplain…"
	.string "\pBack when TEAM"
	.string "\nPLASMA first broke"
	.string "\lup, the POKéMON"
	.string "\pLEAGUE took a"
	.string "\nbunch of stuff"
	.string "\lfrom their labs."
	.string "\pOne of the devices"
	.string "\nthey found got a"
	.string "\plot of the folks"
	.string "\nin the LEAGUE"
	.string "\lreal worried."
	.string "\pIt was this thing"
	.string "\nthat could be used"
	.string "\pto combine a"
	.string "\nperson's mind with"
	.string "\la machine."
	.string "\pThey called it"
	.string "\nthe MIND LINK."
	.string "\pSupposedly, if the"
	.string "\nwrong folks got"
	.string "\lahold of it…"
	.string "\pThey could use it"
	.string "\nto make some kind"
	.string "\lof super weapon."
	.string "\pSo, the LEAGUE"
	.string "\ndecided to hide"
	.string "\lit away."
	.string "\pI was keeping it"
	.string "\nin my GYM for a"
	.string "\lwhile."
	.string "\pGuess they figured"
	.string "\nno one would"
	.string "\psuspect a powerful"
	.string "\nthing like that"
	.string "\pwould be kept in"
	.string "\nour little town."
	.string "\pBut then that girl"
	.string "\nbroke into the GYM"
	.string "\pand stole your"
	.string "\nPOKéDEX…"
	.string "\pI didn't think too"
	.string "\nmuch of it at the"
	.string "\ltime, but I think"
	.string "\pshe may have been"
	.string "\ntrying to take the"
	.string "\lMIND LINK, and"
	.string "\pgrabbed the POKé-"
	.string "\nDEX by mistake."
	.string "\pWe moved it to the"
	.string "\nPOKéMON LEAGUE"
	.string "\lafter that."
	.string "\pBut it looks like"
	.string "\nTEAM PLASMA"
	.string "\pmanaged to snag it"
	.string "\nanyway…"
	.string "\pWell, the PROF's a"
	.string "\nbright girl, I'm"
	.string "\psure she'll figure"
	.string "\nsomething out."
	.string "\pAnyway, you've"
	.string "\ngotten a lot"
	.string "\pstronger since I"
	.string "\nsaw you last!"
	.string "\pI'm impressed!"
	.string "\nYou've almost"
	.string "\pcollected all"
	.string "\neight GYM BADGES"
	.string "\lalready!"
	.string "\pLooks like the"
	.string "\nlast one you're"
	.string "\pmissing is the"
	.string "\nGYM BADGE from"
	.string "\lOPELUCID CITY."
	.string "\pIt's not too far"
	.string "\nfrom here. Just"
	.string "\phead WEST past"
	.string "\nLACUNOSA TOWN, and"
	.string "\pcross the VILLAGE"
	.string "\nBRIDGE."
	.string "\pGood luck,"
	.string "\n{PLAYER}, I'm"
	.string "\lrooting for ya!$"
