Route222WestHouse_MapScripts::
	.byte 0

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route222WestHouse_EventScript_Npc1::
	msgbox Route222WestHouse_Text_Npc1, MSGBOX_NPC
	end

Route222WestHouse_Text_Npc1:
	.string "PIKACHU: Pikachuu!$"

Route222WestHouse_EventScript_Npc2::
	msgbox Route222WestHouse_Text_Npc2, MSGBOX_NPC
	end

Route222WestHouse_Text_Npc2:
	.string "PIKACHU: Pikachuu!$"

Route222WestHouse_EventScript_Npc3::
	msgbox Route222WestHouse_Text_Npc3, MSGBOX_NPC
	end

Route222WestHouse_Text_Npc3:
	.string "PIKACHU: Pikachuu!$"

Route222WestHouse_EventScript_Npc4::
	msgbox Route222WestHouse_Text_Npc4, MSGBOX_NPC
	end

Route222WestHouse_Text_Npc4:
	.string "PIKACHU: Pikachuu!$"

Route222WestHouse_EventScript_Npc5::
	msgbox Route222WestHouse_Text_Npc5, MSGBOX_NPC
	end

Route222WestHouse_Text_Npc5:
	.string "PIKACHU: Pikachuu!$"

Route222WestHouse_EventScript_Npc6::
	msgbox Route222WestHouse_Text_Npc6, MSGBOX_NPC
	end

Route222WestHouse_Text_Npc6:
	.string "Eehehe! I'm going for the Pokémon\nChampionship with only PIKACHU!$"

@ Treinador de rota do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_rota_sinnoh.py)

Route222WestHouse_EventScript_PokeKidJanet::
	trainerbattle_single TRAINER_SINNOH_POKE_KID_JANET, Route222WestHouse_Text_PokeKidJanetIntro, Route222WestHouse_Text_PokeKidJanetDefeat
	msgbox Route222WestHouse_Text_PokeKidJanetPost, MSGBOX_AUTOCLOSE
	end

Route222WestHouse_Text_PokeKidJanetIntro:
	.string "Bika bikabika!\nPigachu!$"

Route222WestHouse_Text_PokeKidJanetDefeat:
	.string "Pikachu...$"

Route222WestHouse_Text_PokeKidJanetPost:
	.string "Pika...\pI'll need a lot more practice to\nbecome a real PIKACHU...$"
