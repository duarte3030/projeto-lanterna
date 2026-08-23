CanalaveCitySailorEldritchHouse_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CanalaveCitySailorEldritchHouse_OnTransition
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

CanalaveCitySailorEldritchHouse_EventScript_Npc1::
	msgbox CanalaveCitySailorEldritchHouse_Text_Npc1, MSGBOX_NPC
	end

CanalaveCitySailorEldritchHouse_Text_Npc1:
	.string "I'm going to be a Sailor like my\ndaddy!\pHe's a real man among men!\nEven the sea doesn't scare him!\pOh, but a Gym Leader'd be cool, too!\nByron is so awesome!$"

CanalaveCitySailorEldritchHouse_EventScript_Npc2::
	msgbox CanalaveCitySailorEldritchHouse_Text_Npc2, MSGBOX_NPC
	end

CanalaveCitySailorEldritchHouse_Text_Npc2:
	.string "Our boy has too much energy!\n...That's the best way to be!$"

@ ponytail: portao de NPC de cena com a flag RECALCULADA a cada entrada.
@ Acende sempre e so apaga se o marco ja caiu, entao nao depende de
@ linha nenhuma em new_game.inc e save antiga se comporta igual a nova.
CanalaveCitySailorEldritchHouse_OnTransition:
	setflag FLAG_SINNOH_ESCONDE_CANALAVE_CITY_SAILOR_ELDRITCH_HOUSE_SAILOR_ELDRITCH
	call_if_defeated TRAINER_SINNOH_LEADER_BYRON, CanalaveCitySailorEldritchHouse_EventScript_Mostra_CANALAVE_CITY_SAILOR_ELDRITCH_HOUSE_SAILOR_ELDRITCH
	end

CanalaveCitySailorEldritchHouse_EventScript_Mostra_CANALAVE_CITY_SAILOR_ELDRITCH_HOUSE_SAILOR_ELDRITCH::
	clearflag FLAG_SINNOH_ESCONDE_CANALAVE_CITY_SAILOR_ELDRITCH_HOUSE_SAILOR_ELDRITCH
	return
