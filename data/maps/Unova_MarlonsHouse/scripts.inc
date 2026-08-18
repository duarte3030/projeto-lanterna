@ MarlonsHouse do BW3G (Azure_Keys). Gerado por dev_scripts/importa_unova.py; nao editar a mao.

@ >>> B6 Unova, Fase B (portada a mao em 18/08/2026) >>>
@ `.MeetWife` da fonte: `scene_script` SCENE_DEFAULT com `priorityjump`, aqui
@ MAP_SCRIPT_ON_FRAME_TABLE disparando com VAR_UNOVA_MARLON_CASA_CENA em 0
@ (mesma traducao/molde de Unova_UndellaTown). So uma vez: a propria cena
@ grava 1.
@
@ Decisao da condutora, Fase B do PRD (18/08/2026): a cena entra SEM a
@ entrega de inicial (o inicial desta ROM ja e dado em Nuvema, obra 1). A cena
@ porta a conversa (WifeText_Intro) e o estado (a esposa continua a falar
@ sobre o paradeiro do MARLON conforme VAR_UNOVA_UNDELLA_CENA), e o presente
@ e descartado: `showemote EMOTE_SHOCK` + `WifeText_TakePokemon` +
@ `setscene SCENE_MARLONS_HOUSE_CANT_LEAVE` + os tres `*PokeBallScript` de
@ escolha (yesorno/givepoke/TakeXText/ChoseStarterText1/ReceivedStarterText1)
@ + `WifeDirectionsScript` (TOWN_MAP, `setmapscene HUMILAU_CITY`) saem
@ inteiros, junto com `MarlonsHouseTryToLeaveScript` (so existia pra barrar
@ quem tentava sair sem pokemon: sem essa regra, os 2 coord_events da porta
@ do map.json ficam vazios de proposito, conforme a decisao). `EVENT_GOT_TEPIG`
@ nao e necessaria (decisao explicita). As 3 POKE_BALLs do map.json ficam de
@ decoracao: reaproveitam `LookPokeBallText` da fonte (o texto que ja existia
@ pra bola ja tomada), sem inventar prosa nova.
@ Rota do jogador conferida contra data/layouts/Unova_MarlonsHouse/map.bin:
@ dos dois warps da porta, (5,7)/(4,7) -> UP x3 -> (5,4)/(4,4) -> LEFT -> tudo
@ colisao 0.
Unova_MarlonsHouse_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, Unova_MarlonsHouse_OnFrame
	.byte 0

Unova_MarlonsHouse_OnFrame:
	map_script_2 VAR_UNOVA_MARLON_CASA_CENA, 0, Unova_MarlonsHouse_EventScript_CenaEsposa
	.2byte 0

@ `.WalkUpToWife` da fonte, ate onde a régua permite (sem o presente).
Unova_MarlonsHouse_EventScript_CenaEsposa::
	lockall
	applymovement LOCALID_PLAYER, Unova_MarlonsHouse_Movement_JogadorVaiAteEsposa
	waitmovement 0
	msgbox Unova_MarlonsHouse_Text_WifeText_Intro, MSGBOX_DEFAULT
	closemessage
	setvar VAR_UNOVA_MARLON_CASA_CENA, 1
	releaseall
	end

Unova_MarlonsHouse_Movement_JogadorVaiAteEsposa:
	walk_up
	walk_up
	walk_up
	walk_left
	step_end

@ Fala normal da esposa (fora da cena de chegada). `WifeScript` da fonte,
@ sem os dois ramos que dependiam do presente (checkevent
@ EVENT_GOT_A_POKEMON_FROM_ELM e o WifeText_GetMon de antes da cena, que na
@ pratica nunca reaparece porque o ON_FRAME_TABLE acima ja rodou lockall
@ antes de o jogador conseguir falar com ela). O ramo que sobra usa a mesma
@ traducao ja registrada em Unova_UndellaTown/scripts.inc:24-29 pra
@ `checkevent EVENT_MET_MARLON_IN_UNDELLA` -> VAR_UNOVA_UNDELLA_CENA >= 1.
Unova_MarlonsHouse_EventScript_Npc0::
	lock
	faceplayer
	goto_if_ge VAR_UNOVA_UNDELLA_CENA, 1, Unova_MarlonsHouse_EventScript_EsposaMarlonNoGinasio
	msgbox Unova_MarlonsHouse_Text_WifeFindMarlon, MSGBOX_DEFAULT
	release
	end

Unova_MarlonsHouse_EventScript_EsposaMarlonNoGinasio::
	msgbox Unova_MarlonsHouse_Text_WifeText_MarlonInGym, MSGBOX_DEFAULT
	release
	end

@ As 3 POKE_BALLs ficam de decoracao (presente descartado); reaproveitam
@ `LookPokeBallText` da fonte, que ja dizia isso pra bola ja tomada.
Unova_MarlonsHouse_EventScript_Npc1::
	msgbox Unova_MarlonsHouse_Text_LookPokeBallText, MSGBOX_NPC
	end

Unova_MarlonsHouse_EventScript_Npc2::
	msgbox Unova_MarlonsHouse_Text_LookPokeBallText, MSGBOX_NPC
	end

Unova_MarlonsHouse_EventScript_Npc3::
	msgbox Unova_MarlonsHouse_Text_LookPokeBallText, MSGBOX_NPC
	end

Unova_MarlonsHouse_EventScript_Placa1::
	msgbox Unova_MarlonsHouse_Text_MarlonsHouseFridgeText, MSGBOX_SIGN
	end
@ <<< B6 Unova, Fase B <<<

Unova_MarlonsHouse_Text_MarlonsHouseFridgeText::
	.string "Better not mess"
	.string "\naround in MARLON's"
	.string "\lfridge!$"

Unova_MarlonsHouse_Text_WifeText_Intro::
	.string "Oh, {PLAYER}!"
	.string "\pMARLON was waiting"
	.string "\nfor you until just"
	.string "\la few minutes ago."
	.string "\pHe got a phone"
	.string "\ncall and just left"
	.string "\lall of a sudden."
	.string "\pOf course, he"
	.string "\ndidn’t mention"
	.string "\lwhere he was"
	.string "\lgoing…"
	.string "\pI think he was"
	.string "\nheaded to"
	.string "\lROUTE 22…"
	.string "\pBut it’s dangerous"
	.string "\noutside of town."
	.string "\pThere are wild"
	.string "\nPOKéMON out there,"
	.string "\pYou better not go"
	.string "\nafter him alone.$"

Unova_MarlonsHouse_Text_WifeFindMarlon::
	.string "Did you find"
	.string "\nMARLON?"
	.string "\pMake sure he stays"
	.string "\nout of trouble!$"

Unova_MarlonsHouse_Text_WifeText_MarlonInGym::
	.string "Oh, {PLAYER},"
	.string "\nMARLON came back"
	.string "\linto town."
	.string "\pYou can find him"
	.string "\nat the GYM.$"

Unova_MarlonsHouse_Text_LookPokeBallText::
	.string "It contains one of"
	.string "\nMARLON’s POKéMON!$"
