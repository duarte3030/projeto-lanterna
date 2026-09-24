@ DewfordTown_Ex3_6: planta copiada do Pokémon Emerald EX v1.0.4 (mapa 3.6) por dev_scripts/copia_planta_ex.py.

DewfordTown_Ex3_6_MapScripts::
	.byte 0

@ Eventos novos do Pokémon Emerald EX (mapa 3.6), reescritos a partir do texto da ROM
@ por dev_scripts/copia_planta_ex.py.
DewfordTown_Ex3_6_EventScript_ExNpc1::
	msgbox DewfordTown_Ex3_6_Text_ExNpc1, MSGBOX_NPC
	end

DewfordTown_Ex3_6_Text_ExNpc1:
	.string "They have POKéBALLS here that make it\n"
	.string "easier to catch POKéMON while FISHING!$"

DewfordTown_Ex3_6_EventScript_ExNpc2::
	msgbox DewfordTown_Ex3_6_Text_ExNpc2, MSGBOX_NPC
	end

DewfordTown_Ex3_6_Text_ExNpc2:
	.string "Do you think that a POTION will help\n"
	.string "with digestion?$"

@ Laterais do Pokémon Emerald EX (decisão 7 do Fable), reescritos do script da ROM.
@ Balcão 1: a loja por insígnia do EX. As flags de insígnia do EX (as 8 de Hoenn do
@ motor dele) viram as FLAG_INSIGNIA_HOENN_1 a 8 nossas, que são as de CONTEÚDO de
@ Hoenn; a de campeão vira FLAG_IS_CHAMPION e a do começo FLAG_ADVENTURE_STARTED.
DewfordTown_Ex3_6_EventScript_Clerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	goto_if_set FLAG_IS_CHAMPION, DewfordTown_Ex3_6_EventScript_Mart0
	goto_if_set FLAG_INSIGNIA_HOENN_8, DewfordTown_Ex3_6_EventScript_Mart1
	goto_if_set FLAG_INSIGNIA_HOENN_7, DewfordTown_Ex3_6_EventScript_Mart2
	goto_if_set FLAG_INSIGNIA_HOENN_6, DewfordTown_Ex3_6_EventScript_Mart3
	goto_if_set FLAG_INSIGNIA_HOENN_5, DewfordTown_Ex3_6_EventScript_Mart4
	goto_if_set FLAG_INSIGNIA_HOENN_4, DewfordTown_Ex3_6_EventScript_Mart5
	goto_if_set FLAG_INSIGNIA_HOENN_3, DewfordTown_Ex3_6_EventScript_Mart6
	goto_if_set FLAG_INSIGNIA_HOENN_2, DewfordTown_Ex3_6_EventScript_Mart7
	goto_if_set FLAG_INSIGNIA_HOENN_1, DewfordTown_Ex3_6_EventScript_Mart8
	goto_if_set FLAG_ADVENTURE_STARTED, DewfordTown_Ex3_6_EventScript_Mart9
	pokemart DewfordTown_Ex3_6_Pokemart_Inicial
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart0::
	pokemart DewfordTown_Ex3_6_Pokemart_0
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart1::
	pokemart DewfordTown_Ex3_6_Pokemart_1
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart2::
	pokemart DewfordTown_Ex3_6_Pokemart_2
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart3::
	pokemart DewfordTown_Ex3_6_Pokemart_3
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart4::
	pokemart DewfordTown_Ex3_6_Pokemart_4
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart5::
	pokemart DewfordTown_Ex3_6_Pokemart_5
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart6::
	pokemart DewfordTown_Ex3_6_Pokemart_6
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart7::
	pokemart DewfordTown_Ex3_6_Pokemart_7
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart8::
	pokemart DewfordTown_Ex3_6_Pokemart_8
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

DewfordTown_Ex3_6_EventScript_Mart9::
	pokemart DewfordTown_Ex3_6_Pokemart_9
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
DewfordTown_Ex3_6_Pokemart_Inicial:
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_0:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_DUSK_BALL
	.2byte ITEM_QUICK_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_RESTORE
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_1:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_MAX_POTION
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_2:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_FULL_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_3:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_ULTRA_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	.2byte ITEM_MAX_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_4:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_HYPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_5:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_BURN_HEAL
	.2byte ITEM_REVIVE
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	.2byte ITEM_SUPER_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_6:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_7:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_8:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_GREAT_BALL
	.2byte ITEM_POTION
	.2byte ITEM_SUPER_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	.2byte ITEM_ESCAPE_ROPE
	.2byte ITEM_REPEL
	pokemartlistend

	.align 2
DewfordTown_Ex3_6_Pokemart_9:
	.2byte ITEM_POKE_BALL
	.2byte ITEM_POTION
	.2byte ITEM_ANTIDOTE
	.2byte ITEM_PARALYZE_HEAL
	.2byte ITEM_AWAKENING
	pokemartlistend

@ Balcão 2: a loja da Dewford do EX (Lure Ball e X itens).
DewfordTown_Ex3_6_EventScript_SpecialtyClerk::
	lock
	faceplayer
	message gText_HowMayIServeYou
	waitmessage
	pokemart DewfordTown_Ex3_6_Pokemart_Specialty
	msgbox gText_PleaseComeAgain, MSGBOX_DEFAULT
	release
	end

	.align 2
DewfordTown_Ex3_6_Pokemart_Specialty:
	.2byte ITEM_LURE_BALL
	.2byte ITEM_X_SPEED
	.2byte ITEM_X_SP_ATK
	.2byte ITEM_X_DEFENSE
	pokemartlistend

