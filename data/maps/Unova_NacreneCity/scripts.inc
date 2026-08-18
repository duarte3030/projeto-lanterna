@ NacreneCity do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ LENORA (EVENT_NACRENE_CITY_LENORA na fonte) ja veio importada como objeto 1
@ (local id 1, gfx OBJ_EVENT_GFX_ROXANNE, parada em 6,8). Mesmo caso da JUNIPER
@ em Unova_FloccesyTown: EVENT_NACRENE_CITY_LENORA e so campo de esconde-
@ objeto (nunca aparece em checkevent/setevent/clearevent), a varredura de
@ flags do PLANO nao o capturou, e nao ha flag reservada nesta leva. Mesma
@ solução de zero flag nova: o objeto usa FLAG_UNOVA_CENA_JUNIPER no campo
@ `flag` do map.json e o ON_TRANSITION abaixo reescreve o bit a cada entrada,
@ guiado pela PRÓPRIA var da cena (VAR_UNOVA_NACRENE_CENA vai a 1 quando a cena
@ termina). `removeobject` dentro da cena cobre o "disappear" imediato.
@ A primeira versão (leva A4 da rodada de 15/08/2026) usava ON_LOAD + removeobject,
@ que é no-op: ON_LOAD roda
@ dentro de InitMap() (src/fieldmap.c:135-140), ANTES de InitObjectEventsLocal()
@ criar os objetos, e removeobject só age em objeto já nascido; a LENORA
@ renascia a cada reentrada no mapa.
Unova_NacreneCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, Unova_NacreneCity_OnTransition
	.byte 0

@ Roda ANTES de InitMap() criar os object_events (técnica 2 do SINNOH-PADRAO.md):
@ a LENORA só nasce enquanto a cena ainda não rodou (var em 0).
@ DEPENDÊNCIA COMPARTILHADA, não mexer aqui sozinho: FLAG_UNOVA_CENA_JUNIPER é o
@ MESMO bit em Unova_NuvemaLab, Unova_P2LabEntrance, Unova_ChampionsRoom,
@ Unova_UndellaTown (MARLON), Unova_CasteliaCityStreets (CHEREN),
@ Unova_FloccesyTown (JUNIPER), Unova_NacreneCity (LENORA) e Unova_PWTOutside
@ (CHEREN e BIANCA). O contrato que faz isso funcionar é "todo mapa que usa o
@ bit o REESCREVE no seu próprio ON_TRANSITION, antes de os objetos nascerem".
@ Quem tirar ou condicionar esta escrita em UM dos oito quebra os outros sete.
@ Mudou um, confira os oito.
Unova_NacreneCity_OnTransition:
	goto_if_eq VAR_UNOVA_NACRENE_CENA, 0, Unova_NacreneCity_EventScript_TransicaoAntesDaCena
	setflag FLAG_UNOVA_CENA_JUNIPER
	end

Unova_NacreneCity_EventScript_TransicaoAntesDaCena::
	clearflag FLAG_UNOVA_CENA_JUNIPER
	end

@ >>> B6 Unova, Obra 1: gatilhos de setscene (dev_scripts/gatilhos_setscene_unova.py) >>>
@ LENORA anda ate o jogador, quatro variantes conforme a fileira em que ele
@ entrou (fonte usa `jump`/fallthrough pro roteiro comum).
Unova_NacreneCity_EventScript_NacreneCityLenoraScript1::
	lockall
	applymovement 1, Unova_NacreneCity_Movement_Lenora1
	waitmovement 0
	goto Unova_NacreneCity_EventScript_NacreneCityLenoraComum

Unova_NacreneCity_EventScript_NacreneCityLenoraScript2::
	lockall
	applymovement 1, Unova_NacreneCity_Movement_Lenora2
	waitmovement 0
	goto Unova_NacreneCity_EventScript_NacreneCityLenoraComum

Unova_NacreneCity_EventScript_NacreneCityLenoraScript3::
	lockall
	applymovement 1, Unova_NacreneCity_Movement_Lenora3
	waitmovement 0
	goto Unova_NacreneCity_EventScript_NacreneCityLenoraComum

Unova_NacreneCity_EventScript_NacreneCityLenoraScript4::
	lockall
	applymovement 1, Unova_NacreneCity_Movement_Lenora4
	waitmovement 0
	@ cai no comum

Unova_NacreneCity_EventScript_NacreneCityLenoraComum::
	msgbox Unova_NacreneCity_Text_NacreneCityLenoraText, MSGBOX_DEFAULT
	closemessage
	applymovement 1, Unova_NacreneCity_Movement_LenoraSai
	waitmovement 0
	removeobject 1
	setvar VAR_UNOVA_NACRENE_CENA, 1
	releaseall
	end

Unova_NacreneCity_Movement_Lenora1:
	walk_left
	walk_left
	walk_left
	step_end

Unova_NacreneCity_Movement_Lenora2:
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Unova_NacreneCity_Movement_Lenora3:
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Unova_NacreneCity_Movement_Lenora4:
	walk_down
	walk_down
	walk_down
	walk_left
	walk_left
	walk_left
	walk_left
	walk_left
	step_end

Unova_NacreneCity_Movement_LenoraSai:
	walk_right
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

@ <<< B6 Unova, Obra 1: gatilhos de setscene <<<

Unova_NacreneCity_EventScript_Placa0::
	msgbox Unova_NacreneCity_Text_NacreneCitySignText, MSGBOX_SIGN
	end

Unova_NacreneCity_EventScript_Placa1::
	msgbox Unova_NacreneCity_Text_NacreneCafeSignText, MSGBOX_SIGN
	end

Unova_NacreneCity_EventScript_Placa2::
	msgbox Unova_NacreneCity_Text_NacreneMuseumSignText, MSGBOX_SIGN
	end

Unova_NacreneCity_EventScript_Placa3::
	msgbox Unova_NacreneCity_Text_NacreneR3SignText, MSGBOX_SIGN
	end

Unova_NacreneCity_EventScript_Npc1::
	msgbox Unova_NacreneCity_Text_NacreneCityLassText, MSGBOX_NPC
	end

Unova_NacreneCity_EventScript_Npc2::
	msgbox Unova_NacreneCity_Text_NacreneCityGentlemanText, MSGBOX_NPC
	end

Unova_NacreneCity_EventScript_Npc3::
	msgbox Unova_NacreneCity_Text_NacreneCityMusicianText, MSGBOX_NPC
	end


Unova_NacreneCity_Text_NacreneCitySignText::
	.string "NACRENE CITY"
	.string "\pA pearl of a"
	.string "\nplace!$"

Unova_NacreneCity_Text_NacreneCafeSignText::
	.string "NACRENE CITY Cafe."
	.string "\pRefresh your body"
	.string "\nand soul!$"

Unova_NacreneCity_Text_NacreneMuseumSignText::
	.string "NACRENE CITY"
	.string "\nMuseum."
	.string "\pWhere the past"
	.string "\ncomes to life!$"

Unova_NacreneCity_Text_NacreneR3SignText::
	.string "ROUTE 3 ahead."
	.string "\pPassage to"
	.string "\nSTRIATON CITY.$"

Unova_NacreneCity_Text_NacreneCityLassText::
	.string "The cafe in town"
	.string "\nserves specialty"
	.string "\pdrinks you can't"
	.string "\nget anywhere else!$"

Unova_NacreneCity_Text_NacreneCityGentlemanText::
	.string "We used to have a"
	.string "\nGYM in the museum,"
	.string "\pbut LENORA has"
	.string "\nretired to run"
	.string "\pthe museum full"
	.string "\ntime.$"

Unova_NacreneCity_Text_NacreneCityLenoraText::
	.string "Hey! I don't"
	.string "\nrecognize you."
	.string "\pYou're not up to"
	.string "\nanything shady,"
	.string "\lare you?"
	.string "\p… … … …"
	.string "\pSorry, we just had"
	.string "\na break in at the"
	.string "\pmuseum. Something"
	.string "\nimportant was"
	.string "\lstolen."
	.string "\pI'm LENORA, I run"
	.string "\nthe museum here in"
	.string "\ptown. We have a"
	.string "\nspecial machine"
	.string "\pthat can revive"
	.string "\nPOKéMON fossils!"
	.string "\pBut it's useless"
	.string "\nwithout that DATA"
	.string "\pDISK that was"
	.string "\nstolen…"
	.string "\pYou should stop by"
	.string "\nif you find out"
	.string "\lanything."
	.string "\pBye now!$"

Unova_NacreneCity_Text_NacreneCityMusicianText::
	.string "NACRENE CITY may"
	.string "\nnot be the biggest"
	.string "\pcity in UNOVA, but"
	.string "\nit's got a"
	.string "\pthriving scene for"
	.string "\nyoung artists.$"
