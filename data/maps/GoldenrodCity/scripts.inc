@ GOLDENROD CITY. Quarta e última batalha contra SILVER, o rival de Johto,
@ portada do pokecrystal (maps/GoldenrodUndergroundSwitchRoomEntrances.asm,
@ UndergroundRivalScene* e textos).
@
@ Mudança de LUGAR, e é a única invenção desta cena: no original a emboscada é
@ lá embaixo, no túnel subterrâneo, mapa
@ GoldenrodUndergroundSwitchRoomEntrances. Este repo tem
@ MAP_GOLDENROD_CITY_UNDERGROUND_SWITCHES, mas ele não é meu nesta tarefa;
@ GoldenrodCity é. O SILVER ficou então em pé na CALÇADA da entrada sul do
@ subterrâneo, em (19,39), de frente para quem vai descer em (21,39). A fala
@ dele ("eu te vi, e vim atrás de você") continua fazendo sentido na rua, que
@ era o requisito para não ter que reescrever o texto.
@
@ Time fixo e raio de visão no lugar do coord_event: motivo em
@ data/maps/CherrygroveCity/scripts.inc. Zero var.

GoldenrodCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GoldenrodCity_OnTransition
	.byte 0

GoldenrodCity_OnTransition:
	setflag FLAG_HIDE_SILVER_GOLDENROD
	goto_if_not_defeated TRAINER_JOHTO_RIVAL_SILVER_3, GoldenrodCity_EventScript_SilverFim
	goto_if_defeated TRAINER_JOHTO_RIVAL_SILVER_4, GoldenrodCity_EventScript_SilverFim
	clearflag FLAG_HIDE_SILVER_GOLDENROD
GoldenrodCity_EventScript_SilverFim:
	end

GoldenrodCity_EventScript_Silver::
	trainerbattle_single TRAINER_JOHTO_RIVAL_SILVER_4, GoldenrodCity_Text_SilverSeen, GoldenrodCity_Text_SilverBeaten
	msgbox GoldenrodCity_Text_SilverAfter, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_HIDE_SILVER_GOLDENROD
	removeobject LOCALID_GOLDENROD_CITY_SILVER
	release
	end

GoldenrodCity_Text_SilverSeen:
	.string "Hold it!\p"
	.string "I saw you, so I tailed you.\p"
	.string "I don't need you underfoot while I\n"
	.string "take care of TEAM ROCKET.\p"
	.string "…Wait a second. You beat me\n"
	.string "before, didn't you?\p"
	.string "That was just a fluke.\p"
	.string "But I repay my debts!$"

GoldenrodCity_Text_SilverBeaten:
	.string "…Why…\n"
	.string "Why do I lose?\p"
	.string "I've assembled the toughest\n"
	.string "POKéMON.\p"
	.string "I didn't ease up on the gas.\p"
	.string "So why do I lose?$"

GoldenrodCity_Text_SilverAfter:
	.string "…I don't understand…\p"
	.string "Is what that LANCE guy said true?\p"
	.string "That I don't treat POKéMON\n"
	.string "properly?\p"
	.string "Love…\p"
	.string "Trust…\p"
	.string "Are they really what I lack?\p"
	.string "Are they keeping me from winning?\p"
	.string "I… I just don't understand.\p"
	.string "But it's not going to end here.\p"
	.string "Not now. Not because of this.\p"
	.string "I won't give up my dream of\n"
	.string "becoming the world's best\l"
	.string "POKéMON trainer!$"
