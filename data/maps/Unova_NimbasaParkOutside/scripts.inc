@ NimbasaParkOutside do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ >>> B6 Unova, Fase B (portada a mao em 18/08/2026) >>>
@ `.CherenScene` da fonte: `scene_script` SCENE_NIMBASA_PARK_OUTSIDE_CHEREN com
@ `priorityjump`, aqui MAP_SCRIPT_ON_FRAME_TABLE disparando com
@ VAR_UNOVA_NIMBASA_PARK_FORA_CENA em 1 (0x4179, tabela da obra 1; mesmo
@ molde de Unova_UndellaTown/scripts.inc). Var e ALVO REMOTO: quem grava 1 e
@ CasteliaCityStreets.asm/NimbasaParkBasement.asm (fora do escopo desta leva).
@ `.AfterScene` (valor 2, SCENE_NIMBASA_PARK_OUTSIDE_AFTER, o `verbosegiveitem
@ PASS` de uma revisita posterior) NAO entra: fora do pedido desta leva, fica
@ dormant (nada grava 2 hoje; se algum dia gravar, o Blocker/CHEREN abaixo ja
@ ficam escondidos porque o gate usa `>= 2`, entao nao quebra).
@
@ O CHEREN (index novo no fim da lista, localid 8) TEM flag propria na tabela
@ do plano (FLAG_UNOVA_NIMBASA_PARK_FORA_CHEREN, EVENT_NIMBASA_PARK_OUTSIDE_
@ CHEREN da fonte). O NPC "Blocker" (indice 3, localid 4) NAO tem: seu evento
@ de origem (EVENT_NIMBASA_PARK_BLOCKER) nao esta nas 21 flags do plano. Sem
@ flag nova autorizada nesta leva, o Blocker reaproveita
@ FLAG_UNOVA_CENA_JUNIPER (a mesma tecnica 2 de Unova_ChampionsRoom/
@ Unova_UndellaTown/Unova_CasteliaCityStreets etc, "reescreve no proprio
@ ON_TRANSITION"): este mapa vira o NONO consumidor do bit, so pra ESTE
@ objeto. NAO editei os outros 8 arquivos (fora do escopo desta leva,
@ paralela); a contagem "oito mapas participantes" nos comentarios de
@ Unova_ChampionsRoom/scripts.inc fica desatualizada em 1 e precisa de
@ atualizacao de documentacao (nao de logica) por quem tiver esse arquivo
@ liberado.
@ CHEREN nao veio importado: e NPC so desta cena, acrescentado no FIM da
@ lista de object_events (index novo, localid 8), gfx OBJ_EVENT_GFX_RIVAL_
@ BRENDAN_NORMAL (mesmo placeholder ja usado pra CHEREN em
@ Unova_CasteliaCityStreets e Unova_PWTOutside).
@
@ Traducoes e descartes, pela regua do PLANO-OBRAS-UNOVA.md:
@   `playmusic MUSIC_ROCKET_ENCOUNTER` -> `playbgm MUS_ENCOUNTER_MAY` (mesmo
@   tema de encontro padrao ja usado em Unova_UndellaTown); `special
@   FadeOutMusic` + `pause 15` -> `fadeoutbgm 4` + `delay 15`; `playmusic
@   MUSIC_NIMBASA_CITY` (musica normal do mapa) -> `fadedefaultbgm`;
@   `big_step RIGHT` (passo largo do gen 2, sem equivalente) -> `walk_fast_right`
@   (mesma traducao ja registrada em Unova_UndellaTown/scripts.inc:132).
@   `disappear` -> `removeobject` no localid.
@ Rota do jogador conferida contra data/layouts/Unova_NimbasaParkOutside/
@ map.bin: (4,8) -> RIGHT -> (5,8) -> RIGHT -> (6,8), colisao 0 nas tres.
Unova_NimbasaParkOutside_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_NimbasaParkOutside_OnTransition
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Unova_NimbasaParkOutside_OnFrame
	.byte 0

@ Roda ANTES de InitMap() criar os object_events (tecnica 2 do
@ SINNOH-PADRAO.md): reescreve os dois bits toda entrada, porque
@ FLAG_UNOVA_CENA_JUNIPER pode ter ficado ligado por OUTRO mapa na visita
@ anterior.
Unova_NimbasaParkOutside_OnTransition:
	goto_if_eq VAR_UNOVA_NIMBASA_PARK_FORA_CENA, 1, Unova_NimbasaParkOutside_EventScript_TransicaoCena1
	setflag FLAG_UNOVA_NIMBASA_PARK_FORA_CHEREN
	goto_if_ge VAR_UNOVA_NIMBASA_PARK_FORA_CENA, 2, Unova_NimbasaParkOutside_EventScript_TransicaoBlockerFora
	clearflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_NimbasaParkOutside_EventScript_TransicaoCena1::
	clearflag FLAG_UNOVA_NIMBASA_PARK_FORA_CHEREN
	clearflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_NimbasaParkOutside_EventScript_TransicaoBlockerFora::
	setflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_NimbasaParkOutside_OnFrame:
	map_script_2 VAR_UNOVA_NIMBASA_PARK_FORA_CENA, 1, Unova_NimbasaParkOutside_EventScript_CenaCheren
	.2byte 0

@ `.CherenConfrontation` da fonte, palavra a palavra na mesma ordem.
Unova_NimbasaParkOutside_EventScript_CenaCheren::
	lockall
	playbgm MUS_ENCOUNTER_MAY, FALSE
	applymovement LOCALID_PLAYER, Unova_NimbasaParkOutside_Movement_JogadorAvanca
	waitmovement 0
	msgbox Unova_NimbasaParkOutside_Text_NimbasaParkOutsideGruntText, MSGBOX_DEFAULT
	closemessage
	applymovement 4, Unova_NimbasaParkOutside_Movement_GruntFoge
	waitmovement 0
	removeobject 4
	fadeoutbgm 4
	delay 15
	fadedefaultbgm
	turnobject 8, DIR_WEST
	msgbox Unova_NimbasaParkOutside_Text_NimbasaParkOutsideCherenText, MSGBOX_DEFAULT
	closemessage
	applymovement 8, Unova_NimbasaParkOutside_Movement_GruntFoge
	waitmovement 0
	removeobject 8
	setvar VAR_UNOVA_NIMBASA_PARK_FORA_CENA, 3
	releaseall
	end

Unova_NimbasaParkOutside_Movement_JogadorAvanca:
	walk_right
	walk_right
	step_end

Unova_NimbasaParkOutside_Movement_GruntFoge:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end
@ <<< B6 Unova, Fase B <<<

Unova_NimbasaParkOutside_EventScript_Npc3::
	msgbox Unova_NimbasaParkOutside_Text_NimbasaParkOutsideBlockerText, MSGBOX_NPC
	end

Unova_NimbasaParkOutside_EventScript_Npc4::
	goto Unova_NimbasaParkOutside_EventScript_NateRosa

Unova_NimbasaParkOutside_EventScript_Npc5::
	goto Unova_NimbasaParkOutside_EventScript_NateRosa


Unova_NimbasaParkOutside_Text_NimbasaParkOutsideBlockerText::
	.string "Hey! Don't you"
	.string "\nknow the PARK's"
	.string "\ldangerous?"
	.string "\pGo on, get out"
	.string "\nof here!$"

Unova_NimbasaParkOutside_Text_NimbasaParkOutsideNateRosaText::
	.string "...$"

Unova_NimbasaParkOutside_Text_NimbasaParkOutsideGruntText::
	.string "Shoot! I can’t"
	.string "\nbeat you. I’d"
	.string "\pbetter go warn"
	.string "\nthe others!$"

Unova_NimbasaParkOutside_Text_NimbasaParkOutsideCherenText::
	.string "CHEREN: Just as I"
	.string "\nthought, TEAM"
	.string "\pPLASMA’s been"
	.string "\nhiding out here."
	.string "\pI’ll go check out"
	.string "\nthe runway on the"
	.string "\lright side, you"
	.string "\pcan investigate"
	.string "\nthe coaster room."
	.string "\pGood luck,"
	.string "\n{PLAYER}.$"

@ >>> cena importada por dev_scripts/importa_chefes_faltantes.py >>>
Unova_NimbasaParkOutside_EventScript_NateRosa::
	checkplayergender
	goto_if_eq VAR_RESULT, FEMALE, Unova_NimbasaParkOutside_EventScript_NateRosaFeminino
	goto_if_eq VAR_STARTER_MON, 1, Unova_NimbasaParkOutside_EventScript_NATE_SNIVY
	goto_if_eq VAR_STARTER_MON, 0, Unova_NimbasaParkOutside_EventScript_NATE_OSHAWOTT
	goto Unova_NimbasaParkOutside_EventScript_NATE_TEPIG

Unova_NimbasaParkOutside_EventScript_NateRosaFeminino::
	goto_if_eq VAR_STARTER_MON, 1, Unova_NimbasaParkOutside_EventScript_ROSA_SNIVY
	goto_if_eq VAR_STARTER_MON, 0, Unova_NimbasaParkOutside_EventScript_ROSA_OSHAWOTT
	goto Unova_NimbasaParkOutside_EventScript_ROSA_TEPIG

Unova_NimbasaParkOutside_EventScript_NATE_SNIVY::
	trainerbattle_single TRAINER_UNOVA_NATE_SNIVY, Unova_NimbasaParkOutside_Text_NimbasaParkOutsideNateRosaText, Unova_NimbasaParkOutside_Text_NateRosaBeaten
	msgbox Unova_NimbasaParkOutside_Text_NateRosaDepois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_NATE_ROSA
	removeobject LOCALID_UNOVA_NIMBASA_NATE
	removeobject LOCALID_UNOVA_NIMBASA_ROSA
	release
	end

Unova_NimbasaParkOutside_EventScript_NATE_TEPIG::
	trainerbattle_single TRAINER_UNOVA_NATE_TEPIG, Unova_NimbasaParkOutside_Text_NimbasaParkOutsideNateRosaText, Unova_NimbasaParkOutside_Text_NateRosaBeaten
	msgbox Unova_NimbasaParkOutside_Text_NateRosaDepois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_NATE_ROSA
	removeobject LOCALID_UNOVA_NIMBASA_NATE
	removeobject LOCALID_UNOVA_NIMBASA_ROSA
	release
	end

Unova_NimbasaParkOutside_EventScript_NATE_OSHAWOTT::
	trainerbattle_single TRAINER_UNOVA_NATE_OSHAWOTT, Unova_NimbasaParkOutside_Text_NimbasaParkOutsideNateRosaText, Unova_NimbasaParkOutside_Text_NateRosaBeaten
	msgbox Unova_NimbasaParkOutside_Text_NateRosaDepois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_NATE_ROSA
	removeobject LOCALID_UNOVA_NIMBASA_NATE
	removeobject LOCALID_UNOVA_NIMBASA_ROSA
	release
	end

Unova_NimbasaParkOutside_EventScript_ROSA_SNIVY::
	trainerbattle_single TRAINER_UNOVA_ROSA_SNIVY, Unova_NimbasaParkOutside_Text_NimbasaParkOutsideNateRosaText, Unova_NimbasaParkOutside_Text_NateRosaBeaten
	msgbox Unova_NimbasaParkOutside_Text_NateRosaDepois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_NATE_ROSA
	removeobject LOCALID_UNOVA_NIMBASA_NATE
	removeobject LOCALID_UNOVA_NIMBASA_ROSA
	release
	end

Unova_NimbasaParkOutside_EventScript_ROSA_TEPIG::
	trainerbattle_single TRAINER_UNOVA_ROSA_TEPIG, Unova_NimbasaParkOutside_Text_NimbasaParkOutsideNateRosaText, Unova_NimbasaParkOutside_Text_NateRosaBeaten
	msgbox Unova_NimbasaParkOutside_Text_NateRosaDepois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_NATE_ROSA
	removeobject LOCALID_UNOVA_NIMBASA_NATE
	removeobject LOCALID_UNOVA_NIMBASA_ROSA
	release
	end

Unova_NimbasaParkOutside_EventScript_ROSA_OSHAWOTT::
	trainerbattle_single TRAINER_UNOVA_ROSA_OSHAWOTT, Unova_NimbasaParkOutside_Text_NimbasaParkOutsideNateRosaText, Unova_NimbasaParkOutside_Text_NateRosaBeaten
	msgbox Unova_NimbasaParkOutside_Text_NateRosaDepois, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_UNOVA_NATE_ROSA
	removeobject LOCALID_UNOVA_NIMBASA_NATE
	removeobject LOCALID_UNOVA_NIMBASA_ROSA
	release
	end

Unova_NimbasaParkOutside_Text_NateRosaBeaten::
	.string "...!$"

Unova_NimbasaParkOutside_Text_NateRosaDepois::
	.string "......$"
@ <<< cena importada por dev_scripts/importa_chefes_faltantes.py <<<
