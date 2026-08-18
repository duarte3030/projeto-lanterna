Route218_West_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ rotulo da fonte: Route218GateToCanalaveCity_CoordEvent_ScientistM (script
@ 2). LOCALID_ROUTE218_WEST_SCIENTIST_M nasce escondido (flag alias
@ FLAG_SINNOH_ESCONDE_ROUTE_218_GATE_TO_CANALAVE_CITY_SCIENTIST_M, 0x1B71,
@ acesa em data/scripts/new_game.inc; o `setflag` de nascimento FALTAVA e foi
@ posto la em 18/08/2026, senao o `clearflag` daqui nao tinha o que limpar e
@ este comentario era falso) e esta cena revela e some, mesmo molde do rival
@ de Route203. DESVIO DA FONTE, dito: la ele NAO nasce escondido (a cena de
@ scripts_route_218_gate_to_canalave_city.s nao tem ClearFlag, so o SetFlag do
@ fim, e a flag nao esta entre as 112 de scripts_init_new_game.s). Aqui ele
@ nao tem script de clique, entao plantado no corredor do portao antes da hora
@ so viraria obstaculo mudo. Posicao movida
@ de (5,7) fonte pra (4,6): (5,7) cai em parede neste layout (conferido com
@ dev_scripts/valida_mapas_sinnoh.py colisao()), (4,6) e o tile andavel mais
@ perto. Textos identicos (masculino/feminino, res/text/route_218_gate_to_
@ canalave_city.json) viram UM so texto, sem ramo de genero. BufferCounterpart
@ Name vira "BARRY" literal (mesma regra do rival em todo o resto da obra:
@ este motor nao tem nome de rival escolhivel). TurnOnPokedexFormDetection
@ descartada: e o toggle DS de mostrar diferenca de genero na Pokedex, e
@ aqui SpeciesHasGenderDifferences (src/pokemon.c) ja mostra sem toggle.
Route218_West_EventScript_CoordEvent_ScientistM::
	lockall
	clearflag FLAG_SINNOH_ESCONDE_ROUTE_218_GATE_TO_CANALAVE_CITY_SCIENTIST_M
	addobject LOCALID_ROUTE218_WEST_SCIENTIST_M
	applymovement LOCALID_ROUTE218_WEST_SCIENTIST_M, Route218_West_Movement_ScientistMNoticePlayer
	waitmovement 0
	msgbox Route218_West_Text_UpgradeYourPokedex, MSGBOX_DEFAULT
	msgbox Route218_West_Text_DisplayMaleAndFemale, MSGBOX_DEFAULT
	setflag FLAG_SINNOH_ESCONDE_ROUTE_218_GATE_TO_CANALAVE_CITY_SCIENTIST_M
	removeobject LOCALID_ROUTE218_WEST_SCIENTIST_M
	setvar VAR_SINNOH_R218_PORTAO_CANALAVE, 1
	releaseall
	end

Route218_West_Movement_ScientistMNoticePlayer:
	emote_exclamation_mark
	step_end

@ Texto literal de res/text/route_218_gate_to_canalave_city.json (BARRY:
@ nome do rival hardcoded, mesma regra do resto da obra), requebrado.
Route218_West_Text_UpgradeYourPokedex:
	.string "{PLAYER}, long time, no see!\p"
	.string "Oh? You look puzzled.\n"
	.string "You're wondering who I am.\p"
	.string "I'm Professor Rowan's assistant\n"
	.string "and BARRY's father.\p"
	.string "The professor asked that I\n"
	.string "upgrade your Pokédex, you see.\p"
	.string "So I'd chosen this spot on a\n"
	.string "hunch that you'd pass through.\p"
	.string "{PLAYER}, may I have your\n"
	.string "Pokédex for a moment?$"

Route218_West_Text_DisplayMaleAndFemale:
	.string "Let's see... Was I supposed to\n"
	.string "put in the software here...?\p"
	.string "Ka-chunk.\n"
	.string "Ka-chunk!\p"
	.string "All done!\n"
	.string "I've upgraded your Pokédex!\p"
	.string "I should explain how it's been\n"
	.string "upgraded, shouldn't I?\p"
	.string "It can now display images of\n"
	.string "male and female Pokémon.\p"
	.string "OK, I'll leave you to carry on\n"
	.string "with your project for the\l"
	.string "professor...\p"
	.string "...May I also ask you to keep\n"
	.string "an eye on Team Galactic?\p"
	.string "The professor is concerned\n"
	.string "about what happened in\l"
	.string "Jubilife City...\p"
	.string "It's probably nothing to worry\n"
	.string "over! I'll be on my way now.$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

Route218_West_EventScript_Npc1::
	msgbox Route218_West_Text_Npc1, MSGBOX_NPC
	end

Route218_West_Text_Npc1:
	.string "Boy...\nI sure am thirsty...$"
