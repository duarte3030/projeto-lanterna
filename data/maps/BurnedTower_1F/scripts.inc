@ BURNED TOWER 1F, portado de fontes-mapas/hns/data/maps/BurnedTower_1F.
@ ponytail: FIREBREATHER_NARD e BURGLAR_RICHARDO ainda nao existem como
@ TRAINER_ (zero vaga sobrando, ver PENDENCIAS-JOHTO.md secao "torres e
@ farol"). Cena montada com o nome que os treinadores DEVEM ter. Sprite de
@ overworld trocado porque OBJ_EVENT_GFX_FIREBREATHER e OBJ_EVENT_GFX_BURGLAR
@ nem existem como constante nesta build: NARD virou CAMPER, RICHARDO virou
@ HIKER.
@ Itens usam Common_EventScript_FindItem com FLAG_UNUSED_0x268/0x269 crus
@ (flags.h esta com outro agente).
@ Nao portado, tudo por falta de sprite que esta build nao desenha (nenhuma
@ das tres constantes abaixo existe fora de dentro de outro jogo/#if
@ IS_FRLG, ou nem existe): EUSINE, MORTY (aqui, como NPC de corredor; o
@ MORTY treinador de ginasio ja existe em outro lugar) e o rival SILVER, que
@ tambem exigiria VAR_ECRUTEAK_CITY_STATE (proibida). Ver PENDENCIAS-JOHTO.md
@ secao 3 (Rival) para o SILVER.
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
	.byte 0

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
