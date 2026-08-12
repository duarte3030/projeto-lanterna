@ Treinadores de rota de NationalPark_Normal, portados de fontes-mapas/hns por
@ dev_scripts/importa_treinadores_johto.py. Nao editar a mao: rode o script.

NationalPark_Normal_MapScripts::
	.byte 0

NationalPark_Normal_EventScript_Jack::
	trainerbattle_single TRAINER_JOHTO_JACK, NationalPark_Normal_Text_JackSeen, NationalPark_Normal_Text_JackBeaten
	msgbox NationalPark_Normal_Text_JackAfter, MSGBOX_AUTOCLOSE
	end

NationalPark_Normal_EventScript_Beverly::
	trainerbattle_single TRAINER_JOHTO_BEVERLY, NationalPark_Normal_Text_BeverlySeen, NationalPark_Normal_Text_BeverlyBeaten
	msgbox NationalPark_Normal_Text_BeverlyAfter, MSGBOX_AUTOCLOSE
	end

NationalPark_Normal_EventScript_William::
	trainerbattle_single TRAINER_JOHTO_WILLIAM, NationalPark_Normal_Text_WilliamSeen, NationalPark_Normal_Text_WilliamBeaten
	msgbox NationalPark_Normal_Text_WilliamAfter, MSGBOX_AUTOCLOSE
	end

NationalPark_Normal_EventScript_Krise::
	trainerbattle_single TRAINER_JOHTO_KRISE, NationalPark_Normal_Text_KriseSeen, NationalPark_Normal_Text_KriseBeaten
	msgbox NationalPark_Normal_Text_KriseAfter, MSGBOX_AUTOCLOSE
	end

NationalPark_Normal_Text_JackSeen:
	.string "The world of POKéMON is deep.\p"
	.string "There are still lots of things we\n"
	.string "don't know.\p"
	.string "But I know more than you do!$"

NationalPark_Normal_Text_JackBeaten:
	.string "Wha-wha-what?$"

NationalPark_Normal_Text_JackAfter:
	.string "There is a lot to learn.\p"
	.string "For example…\p"
	.string "There are 50 kinds of TMs.\p"
	.string "Traded POKéMON level up faster.$"

NationalPark_Normal_Text_BeverlySeen:
	.string "My POKéMON are simply darling.\p"
	.string "Let me tell you how proud my\n"
	.string "darlings make me.$"

NationalPark_Normal_Text_BeverlyBeaten:
	.string "I can beat you in pride, but…$"

NationalPark_Normal_Text_BeverlyAfter:
	.string "I must say, your POKéMON are quite\n"
	.string "cute, too.$"

NationalPark_Normal_Text_WilliamSeen:
	.string "We adore our POKéMON, even if they\n"
	.string "dislike us.\p"
	.string "That's what being a FAN is about.$"

NationalPark_Normal_Text_WilliamBeaten:
	.string "M-my POKéMON!$"

NationalPark_Normal_Text_WilliamAfter:
	.string "I lost the battle, but my POKéMON win\n"
	.string "the prize for being most lovely.$"

NationalPark_Normal_Text_KriseSeen:
	.string "Hello? Why are you staring at me?\p"
	.string "Oh, a battle?$"

NationalPark_Normal_Text_KriseBeaten:
	.string "…Hmmm…$"

NationalPark_Normal_Text_KriseAfter:
	.string "I thought you were staring at me\n"
	.string "because I'm cute!$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

NationalPark_Normal_EventScript_Lass::
	lock
	faceplayer
	msgbox NationalPark_Normal_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

NationalPark_Normal_Text_Lass::
	.string "Look! Check out my bag!\p"
	.string "I printed out my favorites from my\n"
	.string "POKéDEX and stuck them on my bag.$"

NationalPark_Normal_EventScript_Youngster2::
	lock
	faceplayer
	msgbox NationalPark_Normal_Text_Youngster2, MSGBOX_DEFAULT
	closemessage
	release
	end

NationalPark_Normal_Text_Youngster2::
	.string "I get the other guy's POKéDEX sticker\n"
	.string "if I win.$"

NationalPark_Normal_EventScript_Youngster1::
	lock
	faceplayer
	msgbox NationalPark_Normal_Text_Youngster1, MSGBOX_DEFAULT
	closemessage
	release
	end

NationalPark_Normal_Text_Youngster1::
	.string "I'm playing with stickers I printed\n"
	.string "from my POKéDEX.$"

NationalPark_Normal_Text_Teacher2::
	.string "I take walks in the PARK, but I\n"
	.string "never go into the grass.\p"
	.string "Trainers always want to battle…\p"
	.string "You must have been in many battles.\n"
	.string "Let me heal your POKéMON for you.$"

NationalPark_Normal_EventScript_Teacher2Fala::
	msgbox NationalPark_Normal_Text_Teacher2, MSGBOX_NPC
	end
