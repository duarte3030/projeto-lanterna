@ NEW BARK TOWN. Primeiro encontro com SILVER, o rival de Johto, portado do
@ pokecrystal (maps/NewBarkTown.asm, NewBarkTownRivalScript e os dois textos).
@
@ Sprite: OBJ_EVENT_GFX_RED. Escolhido porque (a) esta build DESENHA esse
@ sprite fora de qualquer #if IS_FRLG (conferido em
@ src/data/object_events/object_event_graphics_info_pointers.h, linha do
@ OBJ_EVENT_GFX_RED, sem #if em volta), (b) nenhum mapa deste repo usava ele,
@ então o rival de Johto não se confunde com ninguém, e (c) OBJ_EVENT_GFX_SILVER
@ só existe dentro de #if IS_FRLG e derruba o jogo. OBJ_EVENT_GFX_RICH_BOY, que
@ é o BARRY de Sinnoh, ficou de fora de propósito para os dois rivais não terem
@ a mesma cara.
@
@ Visibilidade sem var: quem decide se o SILVER está no mapa é o ON_TRANSITION
@ abaixo, que liga FLAG_HIDE_SILVER_NEW_BARK por padrão e só desliga enquanto a
@ cena ainda não aconteceu. Como o motor roda ON_TRANSITION antes de nascerem os
@ objetos, isso substitui a VAR_NEW_BARK_TOWN_STATE do hns sem gastar var.

NewBarkTown_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, NewBarkTown_OnTransition
	.byte 0

NewBarkTown_OnTransition:
	setflag FLAG_HIDE_SILVER_NEW_BARK
	goto_if_set FLAG_SILVER_NEW_BARK_DONE, NewBarkTown_EventScript_SilverFim
	clearflag FLAG_HIDE_SILVER_NEW_BARK
NewBarkTown_EventScript_SilverFim:
	end

NewBarkTown_EventScript_Silver::
	lock
	faceplayer
	msgbox NewBarkTown_Text_Silver1, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_NEW_BARK_TOWN_SILVER, Common_Movement_WalkInPlaceFasterLeft
	waitmovement 0
	msgbox NewBarkTown_Text_Silver2, MSGBOX_DEFAULT
	closemessage
	playse SE_M_HEADBUTT
	applymovement LOCALID_NEW_BARK_TOWN_SILVER, NewBarkTown_Movement_SilverVaiEmbora
	waitmovement 0
	setflag FLAG_SILVER_NEW_BARK_DONE
	setflag FLAG_HIDE_SILVER_NEW_BARK
	removeobject LOCALID_NEW_BARK_TOWN_SILVER
	release
	end

NewBarkTown_Movement_SilverVaiEmbora:
	walk_right
	walk_right
	walk_right
	step_end

NewBarkTown_Text_Silver1:
	.string "……\p"
	.string "So this is the famous ELM\n"
	.string "POKéMON LAB…$"

NewBarkTown_Text_Silver2:
	.string "…What are you staring at?$"
