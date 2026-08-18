@ Texto vindo de pret/pokeplatinum, em ingles, como o resto do jogo.

OreburghCity_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S4: cena da fonte >>>
@ Simplificacao anotada nas duas cenas: a fonte ramifica em 4 (um por tile do
@ gatilho, mesma linha de chegada em Z distintas) e a de baixo ainda anda o
@ JOGADOR por um corredor inteiro ate o ginasio. Colapsado num so caminho, sem
@ tocar o jogador (so NPC anda; nenhum applymovement mexe no jogador, mesma
@ regra de CianwoodCity_EventScript_SuicuneTrigger) para nao arriscar
@ waitmovement travado por colisao nao conferida contra map.bin.

@ rotulo da fonte: OreburghCity_CoordEvent_Youngster
OreburghCity_EventScript_CoordEvent_Youngster::
	lockall
	applymovement LOCALID_OREBURGH_CITY_YOUNGSTER, OreburghCity_Movement_YoungsterNoticePlayer
	waitmovement 0
	msgbox OreburghCity_Text_IllTakeYouToTheGym, MSGBOX_DEFAULT
	applymovement LOCALID_OREBURGH_CITY_YOUNGSTER, OreburghCity_Movement_YoungsterRunToGym
	waitmovement 0
	setvar VAR_SINNOH_OREBURGH_ESTADO, 1
	releaseall
	end

OreburghCity_Movement_YoungsterNoticePlayer:
	emote_exclamation_mark
	step_end

OreburghCity_Movement_YoungsterRunToGym:
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	walk_fast_right
	step_end

@ rotulo da fonte: OreburghCity_CoordEvent_Rival
@ BARRY (LOCALID_OREBURGH_CITY_BARRY, sprite OBJ_EVENT_GFX_RICH_BOY, mesma
@ troca de Route203) esbarra no jogador saindo do ginasio e comenta que vai
@ para Eterna. Nao ha batalha nesta cena na fonte (so em Route203); nenhum
@ TRAINER_SINNOH_* precisa existir aqui.
OreburghCity_EventScript_CoordEvent_Rival::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_OREBURGH_CITY_RIVAL
	addobject LOCALID_OREBURGH_CITY_BARRY
	applymovement LOCALID_OREBURGH_CITY_BARRY, OreburghCity_Movement_BarryRunIntoPlayer
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	msgbox OreburghCity_Text_BigThud, MSGBOX_DEFAULT
	msgbox OreburghCity_Text_EternaCityNextPlaceWithAGym, MSGBOX_DEFAULT
	msgbox OreburghCity_Text_CantGoToRoute207WithoutBicycle, MSGBOX_DEFAULT
	msgbox OreburghCity_Text_NextStopTheEternaGymBadge, MSGBOX_DEFAULT
	applymovement LOCALID_OREBURGH_CITY_BARRY, OreburghCity_Movement_BarryLeave
	waitmovement 0
	setflag FLAG_SINNOH_ESCONDE_OREBURGH_CITY_RIVAL
	removeobject LOCALID_OREBURGH_CITY_BARRY
	setvar VAR_SINNOH_OREBURGH_ESTADO, 3
	releaseall
	end

OreburghCity_Movement_BarryRunIntoPlayer:
	walk_fast_left
	walk_fast_left
	step_end

OreburghCity_Movement_BarryLeave:
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	walk_fast_left
	step_end

OreburghCity_Text_IllTakeYouToTheGym:
	.string "Howdy, Trainer!\p"
	.string "Huh? Uh-oh! You don't have a\n"
	.string "single Gym Badge?\p"
	.string "You'd better do something about\n"
	.string "that! I'll take you to the\l"
	.string "Pokémon Gym.$"

OreburghCity_Text_BigThud:
	.string "Thud!!$"

OreburghCity_Text_EternaCityNextPlaceWithAGym:
	.string "BARRY: Whoops! {PLAYER}!\n"
	.string "You got the Gym Badge, huh?\p"
	.string "Eterna City is the next place\n"
	.string "with a Gym that gives away\l"
	.string "Badges, right?$"

OreburghCity_Text_CantGoToRoute207WithoutBicycle:
	.string "So, yeah, I went to Route 207, but\n"
	.string "you can't go there without a\l"
	.string "Bicycle.\p"
	.string "I made my team battle and\n"
	.string "toughened them up, so it wasn't\l"
	.string "a waste.$"

OreburghCity_Text_NextStopTheEternaGymBadge:
	.string "So, I'm going back to Jubilife\n"
	.string "City. Next stop, the Eterna Gym\l"
	.string "Badge!$"
@ <<< B6 Sinnoh S4: cena da fonte <<<

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
