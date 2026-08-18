@ QG da Galactica, sala de controle: a batalha contra o Comandante Saturn e as
@ tres maquinas com os Pokemon dos lagos.
@ Texto de pret/pokeplatinum, res/text/galactic_hq_control_room.json.
@ Layout emprestado do Centro Espacial de Mossdeep, 2F.
@
@ ponytail: quem decide se as maquinas ainda estao cheias continua sendo a flag
@ de treinador do Saturn, que o jogo grava de graca. O botao, esse sim, ganhou
@ FLAG_GALACTICA_LAKE_TRIO_FREED: sem ela dava para soltar os tres Pokemon
@ quantas vezes o jogador quisesse. Agora solta uma vez, e depois responde que o
@ console esta morto.
@
@ Saturn reusa TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, que ja existe. Se o
@ jogador tiver batido nele em Valor Cavern antes, esta cena ja nasce vencida.

GalacticHQ_ControlRoom_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
GalacticHQ_ControlRoom_EventScript_CoordEvent_Saturn::
	@ TODO S6: cena da fonte, rotulo GalacticHQControlRoom_CoordEvent_Saturn
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

GalacticHQ_ControlRoom_EventScript_Saturn::
	trainerbattle_single TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, GalacticHQ_ControlRoom_Text_SaturnIntro, GalacticHQ_ControlRoom_Text_WhatMakesYouSoTough, GalacticHQ_ControlRoom_EventScript_SaturnDefeated
	msgbox GalacticHQ_ControlRoom_Text_PressButtonAndFreePokemon, MSGBOX_AUTOCLOSE
	end

GalacticHQ_ControlRoom_EventScript_SaturnDefeated::
	msgbox GalacticHQ_ControlRoom_Text_BossCraftedRedChain, MSGBOX_DEFAULT
	release
	end

GalacticHQ_ControlRoom_EventScript_Charon::
	lock
	faceplayer
	goto_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, GalacticHQ_ControlRoom_EventScript_CharonAfter
	msgbox GalacticHQ_ControlRoom_Text_WhereWouldTheyGo, MSGBOX_DEFAULT
	msgbox GalacticHQ_ControlRoom_Text_WhatAreYouSaying, MSGBOX_DEFAULT
	msgbox GalacticHQ_ControlRoom_Text_ILookForwardToPlan, MSGBOX_DEFAULT
	msgbox GalacticHQ_ControlRoom_Text_BossCanDoWithoutSupport, MSGBOX_DEFAULT
	release
	end

GalacticHQ_ControlRoom_EventScript_CharonAfter::
	msgbox GalacticHQ_ControlRoom_Text_PerhapsAnotherOption, MSGBOX_DEFAULT
	release
	end

GalacticHQ_ControlRoom_EventScript_Button::
	lockall
	goto_if_set FLAG_GALACTICA_LAKE_TRIO_FREED, GalacticHQ_ControlRoom_EventScript_ButtonSpent
	goto_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, GalacticHQ_ControlRoom_EventScript_PressButton
	msgbox GalacticHQ_ControlRoom_Text_AskPressButton, MSGBOX_DEFAULT
	msgbox GalacticHQ_ControlRoom_Text_AlreadyPressedButton, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_ControlRoom_EventScript_PressButton::
	msgbox GalacticHQ_ControlRoom_Text_AskPressButton, MSGBOX_DEFAULT
	msgbox GalacticHQ_ControlRoom_Text_PlayerPressedButton, MSGBOX_DEFAULT
	setflag FLAG_GALACTICA_LAKE_TRIO_FREED
	releaseall
	end

GalacticHQ_ControlRoom_EventScript_ButtonSpent::
	msgbox GalacticHQ_ControlRoom_Text_ButtonIsDead, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_ControlRoom_EventScript_UxieMachine::
	lockall
	goto_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, GalacticHQ_ControlRoom_EventScript_UxieMachineEmpty
	msgbox GalacticHQ_ControlRoom_Text_UxieIsSealedInside, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_ControlRoom_EventScript_UxieMachineEmpty::
	msgbox GalacticHQ_ControlRoom_Text_UxieWasSealedInside, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_ControlRoom_EventScript_MespritMachine::
	lockall
	goto_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, GalacticHQ_ControlRoom_EventScript_MespritMachineEmpty
	msgbox GalacticHQ_ControlRoom_Text_MespritIsSealedInside, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_ControlRoom_EventScript_MespritMachineEmpty::
	msgbox GalacticHQ_ControlRoom_Text_MespritWasSealedInside, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_ControlRoom_EventScript_AzelfMachine::
	lockall
	goto_if_defeated TRAINER_SINNOH_COMMANDER_SATURN_GALACTIC_HQ, GalacticHQ_ControlRoom_EventScript_AzelfMachineEmpty
	msgbox GalacticHQ_ControlRoom_Text_AzelfIsSealedInside, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_ControlRoom_EventScript_AzelfMachineEmpty::
	msgbox GalacticHQ_ControlRoom_Text_AzelfWasSealedInside, MSGBOX_DEFAULT
	releaseall
	end

GalacticHQ_ControlRoom_Text_SaturnIntro:
	.string "You... You came all the way here\n"
	.string "just to save some Pokémon?\p"
	.string "...Though it's nothing new, I\n"
	.string "can't say I understand our boss...\p"
	.string "Why would he let a kid like you\n"
	.string "come and go freely...?\p"
	.string "We, Team Galactic, take all that\n"
	.string "we need, and eliminate what we do\l"
	.string "not.\p"
	.string "But anyway. You've taken the\n"
	.string "trouble to come. Let me welcome\l"
	.string "you!\p"
	.string "Consider it payback for your\n"
	.string "insulting me at the lake.$"

GalacticHQ_ControlRoom_Text_WhatMakesYouSoTough:
	.string "...Gah!\n"
	.string "What makes you so tough?\p"
	.string "Fine... Do whatever you want with\n"
	.string "those three Pokémon.\p"
	.string "Press the button on that machine\n"
	.string "to set them free.$"

GalacticHQ_ControlRoom_Text_PressButtonAndFreePokemon:
	.string "Press the button and set them\n"
	.string "free. Isn't that why you came?$"

GalacticHQ_ControlRoom_Text_BossCraftedRedChain:
	.string "Our boss crafted a Red Chain from\n"
	.string "crystals he took from the three\l"
	.string "Pokémon.\p"
	.string "That Red Chain is what he needed\n"
	.string "to shackle something on\l"
	.string "Mt. Coronet.\p"
	.string "It's also apparently needed for\n"
	.string "creating something.\p"
	.string "But that's all I know. Who knows\n"
	.string "what he's planning to do up there.$"

GalacticHQ_ControlRoom_Text_WhereWouldTheyGo:
	.string "Charon: Fuhyahya!\p"
	.string "Those Pokémon of the lakes, where\n"
	.string "do you suppose they would go?$"

GalacticHQ_ControlRoom_Text_WhatAreYouSaying:
	.string "Saturn: What are you trying to\n"
	.string "say?$"

GalacticHQ_ControlRoom_Text_ILookForwardToPlan:
	.string "Charon: Nothing.\n"
	.string "Pay it no heed.\p"
	.string "A new world isn't overly\n"
	.string "interesting. What of it?\p"
	.string "If Cyrus is right, then Team\n"
	.string "Galactic will rule that new world.\p"
	.string "That's when it will be\n"
	.string "interesting. A chance to enjoy its\l"
	.string "sweets.\p"
	.string "I surely hope that our visionary\n"
	.string "Cyrus realizes his dream.\p"
	.string "I look forward to whatever our\n"
	.string "beloved leader has planned atop\l"
	.string "Mt. Coronet.$"

GalacticHQ_ControlRoom_Text_BossCanDoWithoutSupport:
	.string "Saturn: Gramps.\p"
	.string "Our boss can do without your kind\n"
	.string "of moral support.$"

GalacticHQ_ControlRoom_Text_PerhapsAnotherOption:
	.string "Charon: Humph. Saturn and even\n"
	.string "Cyrus fall to a mere child...\p"
	.string "Team Galactic's state of affairs\n"
	.string "is worrying...\p"
	.string "That plan of Cyrus's atop\n"
	.string "Mt. Coronet, too... Who knows if\l"
	.string "it will work.\p"
	.string "...Hmm. Perhaps another option\n"
	.string "needs to be considered.\p"
	.string "One befitting the genius of\n"
	.string "Charon!$"

GalacticHQ_ControlRoom_Text_AskPressButton:
	.string "Press the button and set\n"
	.string "the Pokémon free?$"

GalacticHQ_ControlRoom_Text_PlayerPressedButton:
	.string "{PLAYER} pressed the button and\n"
	.string "set the Pokémon free.$"

GalacticHQ_ControlRoom_Text_ButtonIsDead:
	.string "The machines stand open and empty.\p"
	.string "The button clicks, and nothing\n"
	.string "answers it.$"

GalacticHQ_ControlRoom_Text_AlreadyPressedButton:
	.string "The button does not respond.\n"
	.string "Someone is guarding the console.$"

GalacticHQ_ControlRoom_Text_UxieIsSealedInside:
	.string "UXIE is sealed inside! It appears\n"
	.string "to be suffering, with eyes\l"
	.string "squeezed shut.$"

GalacticHQ_ControlRoom_Text_MespritIsSealedInside:
	.string "MESPRIT is sealed inside! It seems\n"
	.string "to be suffering, with its tail\l"
	.string "twitching.$"

GalacticHQ_ControlRoom_Text_AzelfIsSealedInside:
	.string "AZELF is sealed inside! It appears\n"
	.string "to be suffering, with wracking\l"
	.string "shudders.$"

GalacticHQ_ControlRoom_Text_UxieWasSealedInside:
	.string "It's Team Galactic's sinister\n"
	.string "machine. UXIE had been sealed\l"
	.string "inside it.$"

GalacticHQ_ControlRoom_Text_MespritWasSealedInside:
	.string "It's Team Galactic's sinister\n"
	.string "machine. MESPRIT had been sealed\l"
	.string "inside it.$"

GalacticHQ_ControlRoom_Text_AzelfWasSealedInside:
	.string "It's Team Galactic's sinister\n"
	.string "machine. AZELF had been sealed\l"
	.string "inside it.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

GalacticHQ_ControlRoom_EventScript_Placa1::
	msgbox GalacticHQ_ControlRoom_Text_Placa1, MSGBOX_SIGN
	end

GalacticHQ_ControlRoom_Text_Placa1:
	.string "UXIE is sealed inside! It appears to\nbe suffering, with eyes squeezed shut.$"

GalacticHQ_ControlRoom_EventScript_Placa2::
	msgbox GalacticHQ_ControlRoom_Text_Placa2, MSGBOX_SIGN
	end

GalacticHQ_ControlRoom_Text_Placa2:
	.string "MESPRIT is sealed inside! It seems to\nbe suffering, with its tail twitching.$"

GalacticHQ_ControlRoom_EventScript_Placa3::
	msgbox GalacticHQ_ControlRoom_Text_Placa3, MSGBOX_SIGN
	end

GalacticHQ_ControlRoom_Text_Placa3:
	.string "AZELF is sealed inside! It appears to\nbe suffering, with wracking shudders.$"

GalacticHQ_ControlRoom_EventScript_Placa4::
	msgbox GalacticHQ_ControlRoom_Text_Placa4, MSGBOX_SIGN
	end

GalacticHQ_ControlRoom_Text_Placa4:
	.string "Press the button and set\nthe Pokémon free?$"
