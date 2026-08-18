@ Ginasio de Sinnoh com interior reaproveitado de Hoenn.

HearthomeCity_Gym_MapScripts::
	.byte 0

@ Fecho pos-vitoria (onda 4, 18/08/2026): scripts_hearthome_city_gym_leader_
@ room.s da fonte, direto apos GiveBadge/SetTrainerFlag (polimento de time,
@ fora de escopo, decisao 2 do Gui intocada). Tres linhas literais: `SetVar
@ VAR_ROUTE_209_GATE_TO_HEARTHOME_CITY_STATE, 1` (arma os 5 coord_events de
@ Route209_Access_EventScript_CoordEvent_Rival), `SetFlag FLAG_HIDE_
@ HEARTHOME_CITY_ROUTE_209_BLOCKADE` (o objeto do bloqueio ja mora em
@ HearthomeCity/map.json, fora dos meus arquivos desta onda) e `ClearFlag
@ FLAG_HIDE_HEARTHOME_CITY_ROUTE_209_GATE_RIVAL` (revela o rival plantado
@ pelo S5 em Route209_Access).
HearthomeCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_5, HearthomeCity_Gym_EventScript_JaVenceu
	msgbox HearthomeCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_FANTINA, HearthomeCity_Gym_Text_Defeat
	msgbox HearthomeCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_5
	setvar VAR_SINNOH_R209_PORTAO_HEARTHOME, 1
	setflag FLAG_SINNOH_ESCONDE_HEARTHOME_CITY_ROUTE_209_BLOCKADE
	clearflag FLAG_SINNOH_ESCONDE_HEARTHOME_CITY_ROUTE_209_GATE_RIVAL
	release
	end

HearthomeCity_Gym_EventScript_JaVenceu::
	msgbox HearthomeCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

HearthomeCity_Gym_Text_Intro:
	.string "...$"

HearthomeCity_Gym_Text_Defeat:
	.string "You are so fantastically strong.\nI know now why I have lost.$"

HearthomeCity_Gym_Text_Post:
	.string "...$"

HearthomeCity_Gym_Text_JaVenceu:
	.string "The RELIC BADGE is already yours.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

HearthomeCity_Gym_EventScript_Npc1::
	msgbox HearthomeCity_Gym_Text_Npc1, MSGBOX_NPC
	end

HearthomeCity_Gym_Text_Npc1:
	.string "Hey, there!\nHow's it going, Champ-to-be?\pYou must really like hearing me talk.\pIf you want to hear my long spiel again,\njust say, 'Yes!'$"
