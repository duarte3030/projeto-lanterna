TwinleafTown_MainHouse_2F_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ Fonte: scripts_twinleaf_town_player_house_2f.s, TwinleafTownPlayerHouse2F_
@ Rival. O rival entra procurando o jogador, empolgado com a TV do PROF.
@ ROWAN, e sai correndo para esperar la fora. A fonte ramifica em 4 so para
@ escolher de que lado o rival entra/aproxima (North/West/East/South); aqui
@ os 4 gatilhos chamam a MESMA cena (o rival sempre entra pela porta, oeste),
@ que e o unico lado que faz sentido no nosso quarto pequeno.
@
@ Des-empilhamento do tile (2,7) (decisao da condutora de 17/08): RivalNorth
@ e RivalSouth caiam no mesmo tile no gerador. RivalNorth ficou em (2,7);
@ RivalSouth foi para (2,6), vizinho ao norte. Nao da para deslocar para o
@ sul (a fonte pediria (4,7) 1 abaixo do centro): o quarto tem so 8 tiles de
@ altura (y 0-7) e (2,8) fica fora do mapa. (2,6) e o unico vizinho livre.
TwinleafTown_MainHouse_2F_EventScript_CoordEvent_RivalNorth::
	goto TwinleafTown_MainHouse_2F_EventScript_Rival
	end

TwinleafTown_MainHouse_2F_EventScript_CoordEvent_RivalWest::
	goto TwinleafTown_MainHouse_2F_EventScript_Rival
	end

TwinleafTown_MainHouse_2F_EventScript_CoordEvent_RivalEast::
	goto TwinleafTown_MainHouse_2F_EventScript_Rival
	end

TwinleafTown_MainHouse_2F_EventScript_CoordEvent_RivalSouth::
	goto TwinleafTown_MainHouse_2F_EventScript_Rival
	end

TwinleafTown_MainHouse_2F_EventScript_Rival::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_TWINLEAF_TOWN_PLAYER_HOUSE_2F_RIVAL
	addobject LOCALID_TWINLEAF_MAINHOUSE2F_RIVAL
	applymovement LOCALID_TWINLEAF_MAINHOUSE2F_RIVAL, TwinleafTown_MainHouse_2F_Movement_RivalEnter
	waitmovement 0
	msgbox TwinleafTown_MainHouse_2F_Text_ThereYouAre, MSGBOX_DEFAULT
	msgbox TwinleafTown_MainHouse_2F_Text_ProfRowanWouldGivePokemon, MSGBOX_DEFAULT
	applymovement LOCALID_TWINLEAF_MAINHOUSE2F_RIVAL, TwinleafTown_MainHouse_2F_Movement_RivalNoticePC
	waitmovement 0
	msgbox TwinleafTown_MainHouse_2F_Text_IsThisANewPC, MSGBOX_DEFAULT
	msgbox TwinleafTown_MainHouse_2F_Text_WhereWasI, MSGBOX_DEFAULT
	msgbox TwinleafTown_MainHouse_2F_Text_SeeProfRowanAndGetPokemon, MSGBOX_DEFAULT
	applymovement LOCALID_TWINLEAF_MAINHOUSE2F_RIVAL, TwinleafTown_MainHouse_2F_Movement_RivalLeave
	waitmovement 0
	removeobject LOCALID_TWINLEAF_MAINHOUSE2F_RIVAL
	setflag FLAG_SINNOH_ESCONDE_TWINLEAF_TOWN_PLAYER_HOUSE_2F_RIVAL
	setvar VAR_SINNOH_CASA_JOGADOR_RIVAL_ESTADO, 1
	releaseall
	end

	.balign 4, 0
TwinleafTown_MainHouse_2F_Movement_RivalEnter:
	walk_left
	walk_left
	emote_exclamation_mark
	step_end

	.balign 4, 0
TwinleafTown_MainHouse_2F_Movement_RivalNoticePC:
	emote_exclamation_mark
	step_end

	.balign 4, 0
TwinleafTown_MainHouse_2F_Movement_RivalLeave:
	walk_right
	walk_right
	walk_down
	walk_down
	walk_right
	walk_right
	set_invisible
	step_end

TwinleafTown_MainHouse_2F_Text_ThereYouAre:
	.string "{RIVAL}: There you are!$"

TwinleafTown_MainHouse_2F_Text_ProfRowanWouldGivePokemon:
	.string "Hey, {PLAYER}!\n"
	.string "Did you just see the TV? Sure you did!\p"
	.string "Prof. Rowan's that really important\n"
	.string "guy who studies Pokémon, right?\p"
	.string "That means he must have lots and lots\n"
	.string "of Pokémon.\p"
	.string "So, if we ask him, I bet he'd give us\n"
	.string "some Pokémon!$"

TwinleafTown_MainHouse_2F_Text_IsThisANewPC:
	.string "Oh, hey!\n"
	.string "Is this a new PC?!$"

TwinleafTown_MainHouse_2F_Text_WhereWasI:
	.string "{RIVAL}: Uh...\n"
	.string "Where was I?$"

TwinleafTown_MainHouse_2F_Text_SeeProfRowanAndGetPokemon:
	.string "Oh, right, right! We're going to go see\n"
	.string "Prof. Rowan and get some Pokémon.\p"
	.string "I'll be waiting outside.\p"
	.string "OK, {PLAYER}? If you're late, I'm\n"
	.string "fining you ¥10 million!$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

TwinleafTown_MainHouse_2F_EventScript_PC::
	msgbox TwinleafTown_MainHouse_2F_Text_PC, MSGBOX_SIGN
	end

@ E a TV que da o motivo da aventura: e nela que o jogador ouve falar do
@ ROWAN. Fala do Platinum, res/text/twinleaf_town_player_house_2f.json.
TwinleafTown_MainHouse_2F_EventScript_TV::
	msgbox TwinleafTown_MainHouse_2F_Text_TV, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_TV:
	.string "That concludes our special program,\n"
	.string "“Let's Ask PROF. ROWAN!”\p"
	.string "Brought to you by JUBILIFE TV on\n"
	.string "Nationwide Net!\p"
	.string "See you next week, same time,\n"
	.string "same channel!$"

TwinleafTown_MainHouse_2F_Text_PC:
	.string "POKéMON BASICS\p"
	.string "People live alongside POKéMON in\n"
	.string "this world. The people that battle\n"
	.string "POKéMON are called POKéMON Trainers.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

TwinleafTown_MainHouse_2F_EventScript_Placa1::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa1, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa1:
	.string "It's a Wii!\nIt's controlled by a Wii Remote!$"

TwinleafTown_MainHouse_2F_EventScript_Placa2::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa2, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa2:
	.string "{PLAYER} checked the PC.\pPokémon Basics...\pPeople live alongside Pokémon in\nthis world.\pThe people that battle Pokémon are\ncalled Pokémon Trainers.$"

TwinleafTown_MainHouse_2F_EventScript_Placa3::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa3, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa3:
	.string "The X Button\nopens the menu!$"

TwinleafTown_MainHouse_2F_EventScript_Placa4::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa4, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa4:
	.string "Mom bought this TV as a gift.$"

TwinleafTown_MainHouse_2F_EventScript_Placa5::
	msgbox TwinleafTown_MainHouse_2F_Text_Placa5, MSGBOX_SIGN
	end

TwinleafTown_MainHouse_2F_Text_Placa5:
	.string "Mom bought this TV as a gift.$"
