@ BURNED TOWER 1F, portado de fontes-mapas/hns/data/maps/BurnedTower_1F.
@ ponytail: FIREBREATHER_NARD e BURGLAR_RICHARDO ainda nao existem como
@ TRAINER_ (zero vaga sobrando, ver PENDENCIAS-JOHTO.md secao "torres e
@ farol"). Cena montada com o nome que os treinadores DEVEM ter. Sprite de
@ overworld trocado porque OBJ_EVENT_GFX_FIREBREATHER e OBJ_EVENT_GFX_BURGLAR
@ nem existem como constante nesta build: NARD virou CAMPER, RICHARDO virou
@ HIKER.
@ Itens usam Common_EventScript_FindItem com FLAG_UNUSED_0x268/0x269 crus
@ (flags.h esta com outro agente).
@ Nao portado, por falta de sprite que esta build nao desenha: EUSINE e MORTY
@ (aqui, como NPC de corredor; o MORTY treinador de ginasio ja existe em outro
@ lugar).
@ 06/08/2026: o rival SILVER ENTROU (terceira batalha, texto do pokecrystal
@ maps/BurnedTower1F.asm). O sprite e OBJ_EVENT_GFX_RED, que esta build
@ desenha fora de qualquer #if; o motivo da escolha esta em
@ data/maps/NewBarkTown/scripts.inc. Time fixo e raio de visao no lugar do
@ coord_event, motivo em data/maps/CherrygroveCity/scripts.inc. Zero var.
@ O buraco pro B1F que no hns so abre depois da batalha do SILVER virou
@ passagem sempre aberta: sem a cena que o abre, nao ha por que trava-lo, e
@ nao dava pra arriscar um setmetatile com ID de tile chutado. O warp para
@ BURNED_TOWER_B1F ja existia no map.json antes desta sessao.
@ Cortado tambem: os dois avisos de estatua (a fonte do hns citava um script
@ de Ruins of Alph que nao existe aqui e nao e meu; conferido contra
@ pcrystal, BurnedTower1F nem tem estatua no original) e os bichos de
@ decoracao (RATICATE/ZUBAT/KOFFING/HOUNDOUR/SLUGMA via
@ OBJ_EVENT_GFX_MON_BASE, que cai no fallback POKE_BALL nesta build).

BurnedTower_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, BurnedTower_1F_OnTransition
	.byte 0

BurnedTower_1F_OnTransition:
	setflag FLAG_HIDE_SILVER_BURNED_TOWER
	goto_if_not_defeated TRAINER_JOHTO_RIVAL_SILVER_2, BurnedTower_1F_EventScript_SilverFim
	goto_if_defeated TRAINER_JOHTO_RIVAL_SILVER_3, BurnedTower_1F_EventScript_SilverFim
	clearflag FLAG_HIDE_SILVER_BURNED_TOWER
BurnedTower_1F_EventScript_SilverFim:
	end

BurnedTower_1F_EventScript_Silver::
	trainerbattle_single TRAINER_JOHTO_RIVAL_SILVER_3, BurnedTower_1F_Text_SilverSeen, BurnedTower_1F_Text_SilverBeaten
	msgbox BurnedTower_1F_Text_SilverAfter, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_SILVER_BURNED_TOWER
	removeobject LOCALID_BURNED_TOWER_1F_SILVER
	release
	end

BurnedTower_1F_EventScript_Nard::
	trainerbattle_single TRAINER_FIREBREATHER_NARD, BurnedTower_Text_NardSeen, BurnedTower_Text_NardBeaten
	msgbox BurnedTower_Text_NardAfter, MSGBOX_AUTOCLOSE
	end

BurnedTower_1F_EventScript_Richardo::
	trainerbattle_single TRAINER_BURGLAR_RICHARDO, BurnedTower_Text_RichardoSeen, BurnedTower_Text_RichardoBeaten
	msgbox BurnedTower_Text_RichardoAfter, MSGBOX_AUTOCLOSE
	end

BurnedTower_Text_NardSeen:
	.string "Don't worry!\p"
	.string "We fire-breathers know the true\n"
	.string "power of fire better than anyone!$"

BurnedTower_Text_NardBeaten:
	.string "Thanks for such a heated battle!$"

BurnedTower_Text_NardAfter:
	.string "The reason this tower's burned is\n"
	.string "that it was hit by lightning.\p"
	.string "The fire I'm breathing is tiny\n"
	.string "in comparison…$"

BurnedTower_Text_RichardoSeen:
	.string "I'm practicing my stealing in the\n"
	.string "BURNED TOWER! Don't try\l"
	.string "this at home!$"

BurnedTower_Text_RichardoBeaten:
	.string "Pfffffffffffffff.$"

BurnedTower_Text_RichardoAfter:
	.string "Maybe a life of crime isn't for\n"
	.string "me…$"

BurnedTower_1F_Text_SilverSeen:
	.string "…… …… ……\p"
	.string "…Oh, it's you.\p"
	.string "I came looking for some legendary\n"
	.string "POKéMON that they say roosts here.\p"
	.string "But there's nothing here!\p"
	.string "Nothing after all the trouble of\n"
	.string "coming to this dump? No way!\p"
	.string "It's all your fault!$"

BurnedTower_1F_Text_SilverBeaten:
	.string "…Humph!\p"
	.string "This is why I hate battling wimps.\p"
	.string "There's no challenge in it.$"

BurnedTower_1F_Text_SilverAfter:
	.string "…Aw, whatever.\p"
	.string "You would never be able to catch a\n"
	.string "legendary POKéMON anyway.$"
