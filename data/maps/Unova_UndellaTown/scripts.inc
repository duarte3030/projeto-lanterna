@ UndellaTown do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ >>> B6 Unova, Obra 1: cena de chegada do MARLON (portada à mão em 15/08/2026) >>>
@ `.UndellaTownMeetMarlon` da fonte: `scene_script` SCENE_DEFAULT com
@ `priorityjump`, que aqui é MAP_SCRIPT_ON_FRAME_TABLE disparando com
@ VAR_UNOVA_UNDELLA_CENA em 0 (mesma tradução de Unova_P2LabEntrance).
@ Roda uma vez só: a própria cena grava 1 (SCENE_UNDELLA_TOWN_CANT_LEAVE).
@
@ MARLON não veio importado: é NPC só desta cena, acrescentado no FIM da lista
@ de object_events do map.json (índice 8, id local 9), parado em (20,8) como na
@ fonte, gfx OBJ_EVENT_GFX_BRAWLY (o mesmo placeholder que o MARLON já usa em
@ Unova_HumilauGym). Esconder sem flag nova: o objeto usa FLAG_UNOVA_CENA_JUNIPER
@ no campo `flag` e o ON_TRANSITION abaixo reescreve o bit a cada entrada
@ (técnica 2 do SINNOH-PADRAO.md; contrato da dependência compartilhada anotado
@ em Unova_ChampionsRoom/scripts.inc).
@
@ Traduções e descartes, pela régua do PLANO-OBRAS-UNOVA.md:
@   `playmusic MUSIC_MARLON_THEME` -> `playbgm MUS_ENCOUNTER_MAY` (tema de
@   encontro padrão das cenas de Unova); `special FadeOutMusic` + `pause 15` ->
@   `fadeoutbgm 4` + `delay 15`; `playmusic MUSIC_LACUNOSA_TOWN` no fim ->
@   `fadedefaultbgm` (volta a música do mapa).
@   `setevent EVENT_MET_MARLON_IN_UNDELLA` DESCARTADO: não tem FLAG_ na tabela
@   do plano e a janela de save está fechada. O que se perde: nada jogável hoje;
@   quem lê esse evento na fonte (HumilauCity.asm, bloqueadores do MARINE TUBE e
@   do ginásio; MarlonsHouse.asm, fala da esposa) ainda é stub gerado aqui, sem
@   nenhum checkevent portado. Quando esses mapas forem escritos, a condição
@   equivalente é VAR_UNOVA_UNDELLA_CENA >= 1, sem precisar de flag.
@ Rota do jogador conferida contra data/layouts/Unova_UndellaTown/map.bin:
@ (25,7) -> (25,8) livre (colisão 0), e o MARLON anda por (21..24,8), tudo livre.
Unova_UndellaTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_UndellaTown_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Unova_UndellaTown_OnFrame
	.byte 0

@ Roda ANTES de InitMap() criar os object_events: o MARLON só nasce enquanto a
@ cena de chegada ainda não rodou (var em 0).
Unova_UndellaTown_OnTransition:
	goto_if_eq VAR_UNOVA_UNDELLA_CENA, 0, Unova_UndellaTown_EventScript_TransicaoEstado0
	setflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_UndellaTown_EventScript_TransicaoEstado0::
	clearflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_UndellaTown_OnFrame:
	map_script_2 VAR_UNOVA_UNDELLA_CENA, 0, Unova_UndellaTown_EventScript_CenaMarlon
	.2byte 0

@ `.UndellaTown_MarlonScene` da fonte, palavra a palavra na mesma ordem.
Unova_UndellaTown_EventScript_CenaMarlon::
	lockall
	applymovement LOCALID_PLAYER, Unova_UndellaTown_Movement_JogadorNaoSai
	waitmovement 0
	fadeoutbgm 4
	delay 15
	playbgm MUS_ENCOUNTER_MAY, FALSE
	turnobject LOCALID_PLAYER, DIR_WEST
	applymovement 9, Unova_UndellaTown_Movement_MarlonChega
	waitmovement 0
	msgbox Unova_UndellaTown_Text_UndellaTownMarlonText, MSGBOX_DEFAULT
	closemessage
	applymovement 9, Unova_UndellaTown_Movement_MarlonSai
	waitmovement 0
	removeobject 9
	setvar VAR_UNOVA_UNDELLA_CENA, 1
	fadeoutbgm 4
	delay 15
	fadedefaultbgm
	releaseall
	end

Unova_UndellaTown_Movement_MarlonChega:
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

Unova_UndellaTown_Movement_MarlonSai:
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Unova_UndellaTown_Text_UndellaTownMarlonText::
	.string "MARLON: Hey,"
	.string "\n{PLAYER}!"
	.string "\pI'm sure ya got a"
	.string "\ntaste of POKéMON"
	.string "\pbattling on the"
	.string "\nway here!"
	.string "\pBy the way, some"
	.string "\nPOKéMON trainers"
	.string "\pare havin' a"
	.string "\ncontest down on"
	.string "\pROUTE 14, just"
	.string "\nsouth of town."
	.string "\pThere's a prize"
	.string "\nfor anyone who"
	.string "\pcan beat all of"
	.string "\n'em!"
	.string "\pIt should give"
	.string "\nyou some sweet"
	.string "\lexperience!"
	.string "\pAfter that, you"
	.string "\nmay even be ready"
	.string "\pto take on my"
	.string "\nGYM!"
	.string "\pBy the way, the"
	.string "\nMARINE TUBE here"
	.string "\pin town can take"
	.string "\nya right back home"
	.string "\pto HUMILAU CITY"
	.string "\nreal quick!"
	.string "\pCome on by the"
	.string "\nGYM when you're"
	.string "\pready, I'll be"
	.string "\nwaitin' for ya,"
	.string "\l{PLAYER}!$"

@ <<< B6 Unova, Obra 1: cena de chegada do MARLON <<<

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ So dispara com VAR_UNOVA_UNDELLA_CENA ja em 1 (SCENE_UNDELLA_TOWN_CANT_LEAVE):
@ quem grava esse 1 e a cena de chegada do MARLON, portada acima em 15/08/2026.
@ `showemote EMOTE_SHOCK` -> `Common_Movement_ExclamationMark` (mesmo recurso
@ ja usado em Unova_ChampionsRoomEntrance pra emocao de susto/alerta).
@ `big_step LEFT` (passo largo do gen 2, sem equivalente) -> `walk_fast_left`.
Unova_UndellaTown_EventScript_UndellaTownBlockerScript::
	lockall
	applymovement 1, Common_Movement_ExclamationMark
	waitmovement 0
	applymovement 1, Unova_UndellaTown_Movement_BlockerBloqueia
	waitmovement 0
	turnobject 1, DIR_SOUTH
	turnobject LOCALID_PLAYER, DIR_NORTH
	goto_if_unset FLAG_BADGE_UNOVA_HUMILAU, Unova_UndellaTown_EventScript_BlockerSemInsignia
	msgbox Unova_UndellaTown_Text_UndellaTownBlockerText_Safe, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_UndellaTown_Movement_BlockerVolta
	waitmovement 0
	setvar VAR_UNOVA_UNDELLA_CENA, 2
	releaseall
	end

Unova_UndellaTown_EventScript_BlockerSemInsignia::
	msgbox Unova_UndellaTown_Text_UndellaTownBlockerText_Blocked, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_UndellaTown_Movement_BlockerVolta
	applymovement LOCALID_PLAYER, Unova_UndellaTown_Movement_JogadorNaoSai
	waitmovement 0
	releaseall
	end

Unova_UndellaTown_Movement_BlockerBloqueia:
	walk_fast_left
	step_end

Unova_UndellaTown_Movement_BlockerVolta:
	walk_right
	step_end

Unova_UndellaTown_Movement_JogadorNaoSai:
	walk_down
	step_end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_UndellaTown_EventScript_Placa0::
	msgbox Unova_UndellaTown_Text_UndellaReversalSignText, MSGBOX_SIGN
	end

Unova_UndellaTown_EventScript_Placa1::
	msgbox Unova_UndellaTown_Text_UndellaFishingSignText, MSGBOX_SIGN
	end

Unova_UndellaTown_EventScript_Placa2::
	msgbox Unova_UndellaTown_Text_UndellaMarineTubeSignText, MSGBOX_SIGN
	end

Unova_UndellaTown_EventScript_Placa3::
	msgbox Unova_UndellaTown_Text_UndellaTownSignText, MSGBOX_SIGN
	end

Unova_UndellaTown_EventScript_Placa6::
	msgbox Unova_UndellaTown_Text_UndellaLockedDoorText, MSGBOX_SIGN
	end

Unova_UndellaTown_EventScript_Npc0::
	msgbox Unova_UndellaTown_Text_UndellaTownBlockerText_Dangerous, MSGBOX_NPC
	end

Unova_UndellaTown_EventScript_Npc1::
	msgbox Unova_UndellaTown_Text_UndellaTownBugCatcherText, MSGBOX_NPC
	end

Unova_UndellaTown_EventScript_Lider2::
	trainerbattle_single TRAINER_UNOVA_FISHER_UNDELLA_1, Unova_UndellaTown_Text_Fisher1UndellaTownSeenText, Unova_UndellaTown_Text_Fisher1UndellaTownBeatenText
	end

Unova_UndellaTown_EventScript_Lider3::
	trainerbattle_single TRAINER_UNOVA_FISHER_UNDELLA_2, Unova_UndellaTown_Text_Fisher2UndellaTownSeenText, Unova_UndellaTown_Text_Fisher2UndellaTownBeatenText
	end

Unova_UndellaTown_EventScript_Npc4::
	msgbox Unova_UndellaTown_Text_UndellaTownFisher3Text, MSGBOX_NPC
	end

Unova_UndellaTown_EventScript_Npc5::
	msgbox Unova_UndellaTown_Text_UndellaTownCooltrainerMText, MSGBOX_NPC
	end


Unova_UndellaTown_Text_UndellaReversalSignText::
	.string "REVERSAL MOUNTAIN"
	.string "\pEnter at your"
	.string "\nown risk!$"

Unova_UndellaTown_Text_UndellaFishingSignText::
	.string "FISHING GURU's"
	.string "\nhouse.$"

Unova_UndellaTown_Text_UndellaMarineTubeSignText::
	.string "MARINE TUBE"
	.string "\pPassage to"
	.string "\nHUMILAU CITY.$"

Unova_UndellaTown_Text_UndellaTownSignText::
	.string "UNDELLA TOWN"
	.string "\pA town of"
	.string "\nrippling waves.$"

Unova_UndellaTown_Text_UndellaLockedDoorText::
	.string "Huh? It's locked…$"

Unova_UndellaTown_Text_UndellaTownBlockerText_Dangerous::
	.string "REVERSAL MOUNTAIN"
	.string "\nis a dangerous"
	.string "\lplace, full of"
	.string "\lwild POKéMON."
	.string "\pYou should at"
	.string "\nleast have a GYM"
	.string "\lBADGE before"
	.string "\pentering a place"
	.string "\nlike this.$"

Unova_UndellaTown_Text_UndellaTownBlockerText_Blocked::
	.string "WAIT!"
	.string "\pREVERSAL MOUNTAIN"
	.string "\nis a dangerous"
	.string "\lplace, full of"
	.string "\lwild POKéMON!"
	.string "\pYou should at"
	.string "\nleast have a GYM"
	.string "\lBADGE before"
	.string "\pentering a place"
	.string "\nlike this.$"

Unova_UndellaTown_Text_UndellaTownBlockerText_Safe::
	.string "REVERSAL MOUNTAIN"
	.string "\nis a dangerous"
	.string "\lplace, full of"
	.string "\lwild POKéMON."
	.string "\pI see you have"
	.string "\nthe WAVEBADGE"
	.string "\pfrom the HUMILAU"
	.string "\nCITY GYM."
	.string "\pBe careful in"
	.string "\nthere!$"

Unova_UndellaTown_Text_UndellaTownBugCatcherText::
	.string "I wanted to learn"
	.string "\nhow to fish for"
	.string "\pPOKéMON, but my"
	.string "\nmom says it's too"
	.string "\ldangerous…$"

Unova_UndellaTown_Text_Fisher1UndellaTownSeenText::
	.string "Okay, good catch!"
	.string "\nMy next catch will"
	.string "\lbe called victory!$"

Unova_UndellaTown_Text_Fisher1UndellaTownBeatenText::
	.string "The victory that"
	.string "\ngot away was"
	.string "\lthiiiis big!$"

Unova_UndellaTown_Text_Fisher2UndellaTownSeenText::
	.string "I'll battle you"
	.string "\nwith my freshly"
	.string "\lcaught POKéMON!$"

Unova_UndellaTown_Text_Fisher2UndellaTownBeatenText::
	.string "I lost it!$"

Unova_UndellaTown_Text_UndellaTownFisher3Text::
	.string "This little beach-"
	.string "\nside town is so"
	.string "\lnice for fishing!"
	.string "\pIf you want to"
	.string "\nlearn to fish,"
	.string "\pgo see the fishing"
	.string "\nguru in town!$"

Unova_UndellaTown_Text_UndellaTownCooltrainerMText::
	.string "The kids at the"
	.string "\nschool put on a"
	.string "\pcontest for POKé-"
	.string "\nMON trainers on"
	.string "\lROUTE 14."
	.string "\pBeat all five"
	.string "\ntrainers, and you"
	.string "\lreceive a prize.$"
