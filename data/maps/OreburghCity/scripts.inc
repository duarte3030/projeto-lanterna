@ Texto vindo de pret/pokeplatinum, em ingles, como o resto do jogo.

OreburghCity_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
OreburghCity_EventScript_CoordEvent_Rival::
	@ TODO S4: cena da fonte, rotulo OreburghCity_CoordEvent_Rival
	end

OreburghCity_EventScript_CoordEvent_Youngster::
	@ TODO S4: cena da fonte, rotulo OreburghCity_CoordEvent_Youngster
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

OreburghCity_EventScript_Rival::
	lock
	faceplayer
	msgbox OreburghCity_Text_Rival, MSGBOX_DEFAULT
	release
	end

OreburghCity_EventScript_Worker::
	msgbox OreburghCity_Text_Worker, MSGBOX_NPC
	end

OreburghCity_EventScript_BattleGirl::
	msgbox OreburghCity_Text_BattleGirl, MSGBOX_NPC
	end

OreburghCity_EventScript_CitySign::
	msgbox OreburghCity_Text_CitySign, MSGBOX_SIGN
	end

OreburghCity_EventScript_GymSign::
	msgbox OreburghCity_Text_GymSign, MSGBOX_SIGN
	end

OreburghCity_Text_Rival:
	.string "Hunh? Oh, it's you! You finally got\n"
	.string "here? You're slow like always.\p"
	.string "But anyway, the GYM LEADER's tough!\n"
	.string "Like, seriously serious!\p"
	.string "Anyway, he's gone off to the coal\n"
	.string "mine. If you want to take him on,\l"
	.string "you'd better go off to the mine!$"

OreburghCity_Text_Worker:
	.string "There's no question. This is hard,\n"
	.string "hard work.\p"
	.string "But working alongside POKéMON...\n"
	.string "it gives me a boost somehow.$"

OreburghCity_Text_BattleGirl:
	.string "Feeling hale and hearty puts a\n"
	.string "smile on my face. And that makes\l"
	.string "me happy.$"

OreburghCity_Text_CitySign:
	.string "OREBURGH CITY\n"
	.string "The Historic Mining Town$"

OreburghCity_Text_GymSign:
	.string "OREBURGH CITY POKéMON GYM\n"
	.string "LEADER: ROARK\p"
	.string "The Cliff Crag Pokémon Gym$"

@ Texto de placa vindo do pokeplatinum (dev_scripts/texto_placas_sinnoh.py)

OreburghCity_EventScript_Placa2::
	msgbox OreburghCity_Text_Placa2, MSGBOX_SIGN
	end

OreburghCity_Text_Placa2:
	.string "Oreburgh City Pokémon Gym\nLeader: Roark\p'Call me Roark the Rock!'$"

OreburghCity_EventScript_Placa3::
	msgbox OreburghCity_Text_Placa3, MSGBOX_SIGN
	end

OreburghCity_Text_Placa3:
	.string "Oreburgh Mining Museum\n'Coal Mining and You!'$"

OreburghCity_EventScript_Placa4::
	msgbox OreburghCity_Text_Placa4, MSGBOX_SIGN
	end

OreburghCity_Text_Placa4:
	.string "Oreburgh Mine\nBeware of Busy Pokémon!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_EventScript_Npc1::
	msgbox OreburghCity_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_Text_Npc1:
	.string "Up ahead there's a huge mountain\nthat towers above everything.\pIt divides Sinnoh into two distinct\nhalves.$"

OreburghCity_EventScript_Npc2::
	msgbox OreburghCity_Text_Npc2, MSGBOX_NPC
	end

OreburghCity_Text_Npc2:
	.string "The Gym Leader went off to work in\nthe mine.$"

OreburghCity_EventScript_Npc3::
	msgbox OreburghCity_Text_Npc3, MSGBOX_NPC
	end

OreburghCity_Text_Npc3:
	.string "Everyone's proud of the mine.\pThey're digging for coal under the\nsea as we speak...\pIt's amazing how they do it!$"

OreburghCity_EventScript_Npc4::
	msgbox OreburghCity_Text_Npc4, MSGBOX_NPC
	end

OreburghCity_Text_Npc4:
	.string "Is that guy in front of the Gym\nyour friend?\pHe's sort of twitchy and impatient.$"

OreburghCity_EventScript_Npc5::
	msgbox OreburghCity_Text_Npc5, MSGBOX_NPC
	end

OreburghCity_Text_Npc5:
	.string "These vents exchange the hot air\ndown below with the fresh air outside.\pLooking down them gives me the urge\nto start yelling into 'em! Hello!$"

OreburghCity_EventScript_Npc6::
	msgbox OreburghCity_Text_Npc6, MSGBOX_NPC
	end

OreburghCity_Text_Npc6:
	.string "There's no question. This is hard,\nhard work.\pBut working alongside Pokémon...\nIt gives me a boost somehow.\pHere, take one of these.$"

OreburghCity_EventScript_Npc7::
	msgbox OreburghCity_Text_Npc7, MSGBOX_NPC
	end

OreburghCity_Text_Npc7:
	.string "When I run around with my Running\nShoes on, I'm the center of attention!\p...At least that's what it feels like.\nThere's always someone looking at me.$"

OreburghCity_EventScript_Npc8::
	msgbox OreburghCity_Text_Npc8, MSGBOX_NPC
	end

OreburghCity_Text_Npc8:
	.string "This pile of dirty sand is called\na slag heap.\pIt's the waste from sorting coal.$"

OreburghCity_EventScript_Npc10::
	msgbox OreburghCity_Text_Npc10, MSGBOX_NPC
	end

OreburghCity_Text_Npc10:
	.string "Have you seen the vents?\nThey release steam from down below.$"

OreburghCity_EventScript_Npc11::
	msgbox OreburghCity_Text_Npc11, MSGBOX_NPC
	end

OreburghCity_Text_Npc11:
	.string "TMs are single use only, but HMs\ncan be used over and over.\pIt's tricky trying to decide which\nPokémon should learn what moves.$"

OreburghCity_EventScript_Npc12::
	msgbox OreburghCity_Text_Npc12, MSGBOX_NPC
	end

OreburghCity_Text_Npc12:
	.string "MACHOP: Macho! Chopo!$"

OreburghCity_EventScript_Npc13::
	msgbox OreburghCity_Text_Npc13, MSGBOX_NPC
	end

OreburghCity_Text_Npc13:
	.string "MACHOP: Pigyooh!$"

OreburghCity_EventScript_Npc14::
	msgbox OreburghCity_Text_Npc14, MSGBOX_NPC
	end

OreburghCity_Text_Npc14:
	.string "MACHOP: Gwooh! Gogogooh!$"

OreburghCity_EventScript_Npc15::
	msgbox OreburghCity_Text_Npc15, MSGBOX_NPC
	end

OreburghCity_Text_Npc15:
	.string "Natural time capsules buried many,\nmany years ago...\pThat's what Fossils are.$"

OreburghCity_EventScript_Placa16::
	msgbox OreburghCity_Text_Placa16, MSGBOX_SIGN
	end

OreburghCity_Text_Placa16:
	.string "Oreburgh City\nCity of Energy$"

OreburghCity_EventScript_Placa17::
	msgbox OreburghCity_Text_Placa17, MSGBOX_SIGN
	end

OreburghCity_Text_Placa17:
	.string "Oreburgh City\nCity of Energy$"

OreburghCity_EventScript_Placa18::
	msgbox OreburghCity_Text_Placa18, MSGBOX_SIGN
	end

OreburghCity_Text_Placa18:
	.string "Howdy, Trainer!\pHuh? Uh-oh!\nYou don't have a single Gym Badge?\pYou'd better do something about that!\nI'll take you to the Pokémon Gym.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_EventScript_Npc9::
	msgbox OreburghCity_Text_Npc9, MSGBOX_NPC
	end

OreburghCity_Text_Npc9:
	.string "Chop, chop, MACHOP!\nChop, chop away on rocks! ~{EMOJI_NOTE}$"
