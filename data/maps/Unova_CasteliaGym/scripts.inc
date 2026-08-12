@ CasteliaGym do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py.
@ Editado a mao em 12/08/2026 (B5): os dois ATALHOS do favo de mel.
@
@ No BW3G o ginasio tem um MAPCALLBACK_TILES que, depois de dois `coord_event`
@ la no fundo, abre buracos no casulo perto da entrada (EVENT_CASTELIA_GYM_OPEN_1
@ e _2, seis `changeblock`). A importacao nao trouxe nem os coord_events nem o
@ callback, entao os buracos nunca abriam.
@
@ ISTO NAO E ENFEITE, e foi medido antes de escrever: cinco dos tiles que esses
@ buracos abrem estao com COLISAO 1 no blockdata de hoje, ou seja sao parede de
@ verdade. Os atalhos compram caminho.
@
@ DE ONDE SAIU CADA NUMERO DE METATILE (nada foi chutado): um bloco de gen 2 vale
@ 2x2 metatiles nossos, e `dev_scripts/blockdata_unova.py` guarda a tabela
@ (bloco, quadrante) -> metatile do tileset ja convertido (`quad2mt` de
@ tileset_gen2, tileset `facility` = gTileset_UnovaFacility). Os seis
@ `changeblock` da fonte foram resolvidos por essa tabela e comparados tile a
@ tile com o `map.bin` atual; so entram aqui os que DIFEREM, que sao seis dos
@ vinte e quatro. Os blocos $75 (8,38) e $76 (12,38) sairam inteiros da lista
@ porque os quatro quadrantes deles ja estao no estado final.
@
@ Custo: ZERO var e DUAS flags, FLAG_UNOVA_CASTELIA_GYM_ATALHO_1 e _2. Flag e nao
@ var porque os dois atalhos sao independentes (da para acender o segundo sem o
@ primeiro), e porque o estado e de 1 bit cada: aberto ou fechado, para sempre.
@ O gatilho dos coord_events e VAR_TEMP_0 valor 0, tecnica 1 do SINNOH-PADRAO.md.
@
@ O ON_LOAD reaplica na entrada do mapa, que e o que faz o buraco continuar
@ aberto depois de sair e voltar; o `special DrawWholeMapView` so aparece no
@ caminho do coord_event, porque no ON_LOAD o mapa ainda vai ser desenhado.

Unova_CasteliaGym_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_CasteliaGym_EventScript_Favo
	.byte 0

Unova_CasteliaGym_EventScript_Favo::
	call_if_set FLAG_UNOVA_CASTELIA_GYM_ATALHO_1, Unova_CasteliaGym_EventScript_AbreAtalho1
	call_if_set FLAG_UNOVA_CASTELIA_GYM_ATALHO_2, Unova_CasteliaGym_EventScript_AbreAtalho2
	end

@ bloco $74 da fonte, em (6,38): buraco da frente e da lateral
Unova_CasteliaGym_EventScript_AbreAtalho1::
	setmetatile 7, 38, 679, FALSE
	setmetatile 7, 39, 682, FALSE
	return

@ blocos $6F (10,36), $73 (10,38) e $72 (2,38) da fonte
Unova_CasteliaGym_EventScript_AbreAtalho2::
	setmetatile 11, 36, 678, FALSE
	setmetatile 11, 37, 679, FALSE
	setmetatile 11, 38, 682, FALSE
	setmetatile 2, 38, 672, FALSE
	return

Unova_CasteliaGym_EventScript_Atalho1::
	lock
	goto_if_set FLAG_UNOVA_CASTELIA_GYM_ATALHO_1, Unova_CasteliaGym_EventScript_AtalhoFim
	setflag FLAG_UNOVA_CASTELIA_GYM_ATALHO_1
	call Unova_CasteliaGym_EventScript_AbreAtalho1
	special DrawWholeMapView
	msgbox Unova_CasteliaGym_Text_AtalhoAberto, MSGBOX_DEFAULT
	release
	end

Unova_CasteliaGym_EventScript_Atalho2::
	lock
	goto_if_set FLAG_UNOVA_CASTELIA_GYM_ATALHO_2, Unova_CasteliaGym_EventScript_AtalhoFim
	setflag FLAG_UNOVA_CASTELIA_GYM_ATALHO_2
	call Unova_CasteliaGym_EventScript_AbreAtalho2
	special DrawWholeMapView
	msgbox Unova_CasteliaGym_Text_AtalhoAberto, MSGBOX_DEFAULT
	release
	end

Unova_CasteliaGym_EventScript_AtalhoFim::
	release
	end

Unova_CasteliaGym_Text_AtalhoAberto::
	.string "A hole opened up"
	.string "\nin the honeycomb"
	.string "\lback near the"
	.string "\lentrance!$"

Unova_CasteliaGym_EventScript_Lider0::
	trainerbattle_single TRAINER_UNOVA_LEADER_BURGH, Unova_CasteliaGym_Text_BurghGymIntroText, Unova_CasteliaGym_Text_BurghWinLossText, Unova_CasteliaGym_EventScript_Insignia0
	end

Unova_CasteliaGym_EventScript_Insignia0::
	setflag FLAG_BADGE_UNOVA_CASTELIA
	call Common_EventScript_PlayGymBadgeFanfare
	release
	end

Unova_CasteliaGym_EventScript_Npc1::
	msgbox Unova_CasteliaGym_Text_CasteliaGymGuyText, MSGBOX_NPC
	end

Unova_CasteliaGym_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_1, Unova_CasteliaGym_Text_HarlequinCasteliaGym1SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym1BeatenText
	end

Unova_CasteliaGym_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_2, Unova_CasteliaGym_Text_HarlequinCasteliaGym2SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym2BeatenText
	end

Unova_CasteliaGym_EventScript_Lider4::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_3, Unova_CasteliaGym_Text_HarlequinCasteliaGym3SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym3BeatenText
	end

Unova_CasteliaGym_EventScript_Lider5::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_4, Unova_CasteliaGym_Text_HarlequinCasteliaGym4SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym4BeatenText
	end

Unova_CasteliaGym_EventScript_Lider6::
	trainerbattle_single TRAINER_UNOVA_HARLEQUIN_CASTELIA_GYM_5, Unova_CasteliaGym_Text_HarlequinCasteliaGym5SeenText, Unova_CasteliaGym_Text_HarlequinCasteliaGym5BeatenText
	end


Unova_CasteliaGym_Text_BurghGymIntroText::
	.string "Hm, my BUG POKé-"
	.string "\nMON have been"
	.string "\pgetting all worked"
	.string "\nup, and what do I"
	.string "\pspy with my little"
	.string "\neye? A trainer"
	.string "\pwho's got me"
	.string "\nscurrying around"
	.string "\lwith excitement!"
	.string "\pI, BURGH, the GYM"
	.string "\nLEADER of CASTELIA"
	.string "\lCITY, accept your"
	.string "\lchallenge!"
	.string "\pLet's get right"
	.string "\nto it!$"

Unova_CasteliaGym_Text_BurghWinLossText::
	.string "Is it over, has"
	.string "\nmy muse abandoned"
	.string "\lme?"
	.string "\pHere, take this"
	.string "\nbadge, I think"
	.string "\lit'll suit you!$"

Unova_CasteliaGym_Text_CasteliaGymGuyText::
	.string "Yo, challenger!"
	.string "\pCASTELIA CITY's"
	.string "\nGYM LEADER is"
	.string "\lcalled BURGH."
	.string "\pHe's a bit of an"
	.string "\noddball, but you'd"
	.string "\pbetter not under-"
	.string "\nestimate his BUG"
	.string "\ltype POKéMON!"
	.string "\pBugs are most"
	.string "\nafraid of FIRE."
	.string "\pThey can also be"
	.string "\ncrushed by ROCKs,"
	.string "\pand FLYING attacks"
	.string "\nwork well too.$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym1SeenText::
	.string "What do you think?"
	.string "\nThis GYM… How"
	.string "\lshould I say?"
	.string "\pIsn't it full of…"
	.string "\nmysterious charms?$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym1BeatenText::
	.string "You've got quite a"
	.string "\nbit of charm your-"
	.string "\lself, don't you?$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym2SeenText::
	.string "You thought you"
	.string "\ncould get through"
	.string "\lhere? Think again!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym2BeatenText::
	.string "My, my! Aren't you"
	.string "\na bit too strong?$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym3SeenText::
	.string "When the cocoon"
	.string "\nopens, the one who"
	.string "\lpops out is moi!"
	.string "\pOn that note, have"
	.string "\na battle with moi!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym3BeatenText::
	.string "I was taking a"
	.string "\nnap!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym4SeenText::
	.string "The one you meet"
	.string "\nat this cocoon is"
	.string "\pnone other than"
	.string "\nme!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym4BeatenText::
	.string "Looks like the"
	.string "\ncocoons brought"
	.string "\lyou to me!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym5SeenText::
	.string "You're just one"
	.string "\nstep away from"
	.string "\pbeing able to"
	.string "\nchallenge BURGH!$"

Unova_CasteliaGym_Text_HarlequinCasteliaGym5BeatenText::
	.string "Your battle style"
	.string "\nis almost as"
	.string "\lartistic as BURGH!$"

@ Placas trazidas do BW3G por dev_scripts/importa_placas_unova.py

@ jumpstd gymstatue1 do BW3G: nome do mapa + "#MON GYM"
Unova_CasteliaGym_EventScript_EstatuaGinasio::
	msgbox Unova_CasteliaGym_Text_EstatuaGinasio, MSGBOX_SIGN
	end

Unova_CasteliaGym_Text_EstatuaGinasio::
	.string "CASTELIA CITY\n"
	.string "POKéMON GYM$"
