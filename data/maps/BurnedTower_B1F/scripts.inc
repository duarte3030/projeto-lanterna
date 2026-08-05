@ BURNED TOWER B1F, portado de fontes-mapas/hns/data/maps/BurnedTower_B1F.
@ ponytail: RAIKOU, ENTEI e SUICUNE nao tem sprite que esta build desenha
@ (OBJ_EVENT_GFX_RAIKOU/ENTEI/SUICUNE existem no enum mas so tem entrada em
@ object_event_graphics_info_pointers.h dentro de #if IS_FRLG; usar
@ reiniciaria o jogo na tela de titulo). Igual foi feito com Dialga e Palkia
@ no Spear Pillar, a cena virou tres bg_event (sign): sem NPC visivel, so
@ cheiro/grito. No pcrystal original tambem e uma cutscene de "apareceu e
@ sumiu", entao nao perde muito nao ter sprite parado.
@ Pedra de forca portada igual ao padrao vanilla (EventScript_StrengthBoulder
@ + FLAG_TEMP_11, mesma flag que o FieryPath usa pro dele: FLAG_TEMP zera a
@ cada carregamento de mapa, reuso entre mapas diferentes e seguro).
@ Itens usam Common_EventScript_FindItem com FLAG_UNUSED_0x26A/0x26B crus
@ (flags.h esta com outro agente).
@ Nao portado: o cameo do EUSINE aqui embaixo (mesma falta de sprite do 1F) e
@ os quatro bichos de decoracao (KOFFING/MISDREAVUS/MAGMAR via
@ OBJ_EVENT_GFX_MON_BASE, que cai no fallback POKE_BALL nesta build).

BurnedTower_B1F_MapScripts::
	.byte 0

BurnedTower_B1F_EventScript_Raikou::
	lock
	playmoncry SPECIES_RAIKOU, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Raikou, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_EventScript_Entei::
	lock
	playmoncry SPECIES_ENTEI, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Entei, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_EventScript_Suicune::
	lock
	playmoncry SPECIES_SUICUNE, CRY_MODE_NORMAL
	msgbox BurnedTower_B1F_Text_Suicune, MSGBOX_DEFAULT
	waitmoncry
	closemessage
	release
	end

BurnedTower_B1F_Text_Raikou:
	.string "A crackle of static electricity\n"
	.string "runs down your spine…\p"
	.string "Something fast and yellow leaps\n"
	.string "past in a blur. By the time you\l"
	.string "turn, RAIKOU is already gone.$"

BurnedTower_B1F_Text_Entei:
	.string "A wave of heat rolls off the\n"
	.string "scorched pillar…\p"
	.string "You catch a glimpse of ENTEI's\n"
	.string "mane before it vanishes into the\l"
	.string "shadows.$"

BurnedTower_B1F_Text_Suicune:
	.string "A cool mist drifts through the\n"
	.string "basement, though there's no\l"
	.string "water in sight…\p"
	.string "SUICUNE was here. You're sure\n"
	.string "of it.$"
