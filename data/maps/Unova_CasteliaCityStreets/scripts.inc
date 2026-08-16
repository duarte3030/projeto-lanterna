@ CasteliaCityStreets do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ CHEREN (EVENT_CASTELIA_CITY_CHEREN na fonte) nao veio importado: e um NPC
@ so desta cena, gfx OBJ_EVENT_GFX_RIVAL_BRENDAN_NORMAL (mesmo placeholder ja
@ usado pro CHEREN em Unova_PWTOutside), acrescentado no FIM da lista de
@ object_events (indice 7, local id 7), parado em (10,11).
@ EVENT_CASTELIA_CITY_CHEREN e so campo de esconde-objeto na fonte, sem
@ checkevent/setevent/clearevent em nenhum script; a varredura de flags do
@ PLANO nao o capturou e nao ha flag reservada nesta leva. Zero flag nova:
@ ON_LOAD some com ele usando a propria var da cena (VAR_UNOVA_CASTELIA_RUAS_
@ CENA chega a 2 quando a cena termina).
Unova_CasteliaCityStreets_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, Unova_CasteliaCityStreets_EventScript_AoCarregar
	.byte 0

Unova_CasteliaCityStreets_EventScript_AoCarregar::
	goto_if_ne VAR_UNOVA_CASTELIA_RUAS_CENA, 2, Unova_CasteliaCityStreets_EventScript_AoCarregarFim
	removeobject 7
Unova_CasteliaCityStreets_EventScript_AoCarregarFim::
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ So dispara com VAR_UNOVA_CASTELIA_RUAS_CENA ja em 1 (SCENE_CASTELIA_CHEREN):
@ quem grava esse 1 e Unova_CasteliaGym (`setmapscene CASTELIA_CITY_STREETS,
@ SCENE_CASTELIA_CHEREN` da fonte, logo apos a insignia), corrigido nesta
@ sessao (era a unica linha que faltava pra fechar essa ponte remota).
@
@ `addcellnum PHONE_CHEREN` + `GotCherensNumberText` + `playsound SFX_
@ REGISTER_PHONE_NUMBER` DESCARTADOS: sem sistema de contatos/telefone neste
@ motor (mesma razao de Unova_PWTOutside). O convite ("register my number...")
@ fica no texto, so a confirmacao mecanica sai.
@ `setmapscene NIMBASA_PARK_OUTSIDE, SCENE_NIMBASA_PARK_OUTSIDE_CHEREN` ->
@ setvar na var do mapa alvo (tabela do PLANO).
Unova_CasteliaCityStreets_EventScript_CherenAppears::
	lockall
	fadeoutbgm 4
	delay 15
	playbgm MUS_ENCOUNTER_MAY, FALSE
	applymovement 7, Unova_CasteliaCityStreets_Movement_CherenChega
	waitmovement 0
	turnobject LOCALID_PLAYER, DIR_EAST
	msgbox Unova_CasteliaCityStreets_Text_CasteliaCherenIntroText, MSGBOX_DEFAULT
	closemessage
	msgbox Unova_CasteliaCityStreets_Text_CasteliaCherenNimbasaText, MSGBOX_DEFAULT
	closemessage
	applymovement 7, Unova_CasteliaCityStreets_Movement_CherenSai
	waitmovement 0
	removeobject 7
	clearflag FLAG_UNOVA_NIMBASA_PARK_FORA_CHEREN
	setvar VAR_UNOVA_NIMBASA_PARK_FORA_CENA, 1
	setvar VAR_UNOVA_CASTELIA_RUAS_CENA, 2
	fadeoutbgm 4
	delay 15
	fadedefaultbgm
	releaseall
	end

Unova_CasteliaCityStreets_Movement_CherenChega:
	walk_left
	walk_left
	walk_left
	step_end

Unova_CasteliaCityStreets_Movement_CherenSai:
	walk_right
	walk_right
	walk_right
	step_end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_CasteliaCityStreets_EventScript_Placa0::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaBikeSignText, MSGBOX_SIGN
	end

Unova_CasteliaCityStreets_EventScript_Placa1::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaMassageSignText, MSGBOX_SIGN
	end

Unova_CasteliaCityStreets_EventScript_Placa2::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaGameFreakSignText, MSGBOX_SIGN
	end

Unova_CasteliaCityStreets_EventScript_Placa5::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaConeSignText, MSGBOX_SIGN
	end

Unova_CasteliaCityStreets_EventScript_Npc0::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaconeBuyText, MSGBOX_NPC
	end

Unova_CasteliaCityStreets_EventScript_Npc1::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaGiveRestText, MSGBOX_NPC
	end

Unova_CasteliaCityStreets_EventScript_Npc2::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaStreetsYoungsterText, MSGBOX_NPC
	end

Unova_CasteliaCityStreets_EventScript_Npc3::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaStreetsTeacherText, MSGBOX_NPC
	end

Unova_CasteliaCityStreets_EventScript_Npc4::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaStreetsLassText, MSGBOX_NPC
	end

Unova_CasteliaCityStreets_EventScript_Npc5::
	msgbox Unova_CasteliaCityStreets_Text_CasteliaStreetsCooltrainerMText, MSGBOX_NPC
	end


Unova_CasteliaCityStreets_Text_CasteliaBikeSignText::
	.string "CASTELIA CYCLES.$"

Unova_CasteliaCityStreets_Text_CasteliaMassageSignText::
	.string "POKéMON massage"
	.string "\nparlor.$"

Unova_CasteliaCityStreets_Text_CasteliaGameFreakSignText::
	.string "GAME FREAK HQ.$"

Unova_CasteliaCityStreets_Text_CasteliaConeSignText::
	.string "Tasty and refresh-"
	.string "\ning! Get your"
	.string "\lCASTELIACONE"
	.string "\ltoday!$"

Unova_CasteliaCityStreets_Text_CasteliaconeBuyText::
	.string "Hi! Welcome to"
	.string "\nCASTELIA CITY!"
	.string "\pHow would you like"
	.string "\nto try a specialty"
	.string "\lCASTELIACONE?"
	.string "\pIt's just ¥100."
	.string "\pYou can buy just"
	.string "\none, or a dozen."
	.string "\pHow about it?$"

Unova_CasteliaCityStreets_Text_CasteliaGiveRestText::
	.string "…zzzzz…"
	.string "\p…wha, huh?"
	.string "\pHey, I'm trying"
	.string "\nto sleep here!"
	.string "\pTake this and go"
	.string "\naway…$"

Unova_CasteliaCityStreets_Text_CasteliaStreetsYoungsterText::
	.string "I've been training"
	.string "\nout in the desert"
	.string "\pto take on the"
	.string "\nGYM!$"

Unova_CasteliaCityStreets_Text_CasteliaStreetsTeacherText::
	.string "Have you tried a"
	.string "\nCASTELIACONE?"
	.string "\pThey're all the"
	.string "\nrage!$"

Unova_CasteliaCityStreets_Text_CasteliaStreetsLassText::
	.string "I love being"
	.string "\nsurrounded by tall"
	.string "\lbuildings!$"

Unova_CasteliaCityStreets_Text_CasteliaStreetsCooltrainerMText::
	.string "Should I change my"
	.string "\nPOKéMON's moves or"
	.string "\lits held items?$"

Unova_CasteliaCityStreets_Text_CasteliaCherenIntroText::
	.string "Oh, excuse me,"
	.string "\nare you {PLAYER}?"
	.string "\pMy name is CHEREN."
	.string "\nI'm a friend of"
	.string "\lthe PROF."
	.string "\pI've been invest-"
	.string "\nigating the recent"
	.string "\pappearances of a"
	.string "\ngroup claiming to"
	.string "\lbe TEAM PLASMA."
	.string "\pThey were a terror"
	.string "\ngroup that was"
	.string "\ldisbanded a few"
	.string "\lyears ago."
	.string "\pOh? You've already"
	.string "\nhad a run-in with"
	.string "\lthem?"
	.string "\pPerhaps you could"
	.string "\nbe of assistance."
	.string "\pHere, register my"
	.string "\nnumber in your"
	.string "\lX-TRANSCIEVER.$"

Unova_CasteliaCityStreets_Text_CasteliaCherenNimbasaText::
	.string "CHEREN: I'm pretty"
	.string "\nknowledgable about"
	.string "\lPOKéMON evolution."
	.string "\pCall me if you"
	.string "\nwant to know how"
	.string "\pto evolve any of"
	.string "\nyour POKéMON."
	.string "\pI'm going to"
	.string "\nNIMBASA CITY."
	.string "\pI've heard reports"
	.string "\nthat TEAM PLASMA"
	.string "\phas been up to"
	.string "\nsomething at the"
	.string "\lold PARK…"
	.string "\pCome and meet me"
	.string "\nif you'd like to"
	.string "\llend a hand.$"
