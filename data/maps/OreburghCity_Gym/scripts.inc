@ Ginasio de referencia de Sinnoh. Lider com insignia, no padrao usado pelos
@ outros sete. Falas vindas de pret/pokeplatinum.

OreburghCity_Gym_MapScripts::
	.byte 0

OreburghCity_Gym_EventScript_Visitor::
	msgbox OreburghCity_Gym_Text_Visitor, MSGBOX_NPC
	end

OreburghCity_Gym_EventScript_Sign::
	msgbox OreburghCity_Gym_Text_Sign, MSGBOX_SIGN
	end

OreburghCity_Gym_Text_Visitor:
	.string "I came to watch ROARK train. He's\n"
	.string "not battling challengers just yet.$"

OreburghCity_Gym_Text_Sign:
	.string "OREBURGH CITY POKéMON GYM\n"
	.string "Leader: Roark$"

OreburghCity_Gym_EventScript_Roark::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_1, OreburghCity_Gym_EventScript_RoarkDerrotado
	msgbox OreburghCity_Gym_Text_RoarkIntro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_ROARK, OreburghCity_Gym_Text_RoarkDefeat
	msgbox OreburghCity_Gym_Text_RoarkPost, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_1
	@ OS DOIS DEGRAUS QUE FALTAVAM das maquinas de Oreburgh e do Looker de
	@ Jubilife. Na fonte quem grava esses dois valores e a vitoria sobre o
	@ ROARK, em OreburghGym_Roark
	@ (res/field/scripts/scripts_oreburgh_city_gym.s:34-35), logo depois do
	@ GiveBadge. Sem eles o gatilho do rival de Oreburgh (coord_event pedindo
	@ 2) e o do Looker em Jubilife (pedindo 1) eram inalcancaveis: a cidade so
	@ sabia escrever 1 (o youngster) e 3 (o proprio rival).
	@ Valores literais da fonte, decisao 2 do plano.
	setvar VAR_SINNOH_JUBILIFE_LOOKER_ESTADO, 1
	setvar VAR_SINNOH_OREBURGH_ESTADO, 2
	@ A mesma cena da fonte ainda grava VAR_GTS_ACCESS_STATE (descartada,
	@ decisao 3) e VAR_JUBILIFE_CITY_STATE, 3. Este ultimo NAO entra aqui: as
	@ duas cenas de Jubilife (LookerBlockRoute203 e TeamGalactic) ja escrevem
	@ o 3 no arco delas, e escrever aqui tambem armaria a emboscada da
	@ Galactica antes de o jogador voltar a cidade.
	release
	end

OreburghCity_Gym_EventScript_RoarkDerrotado::
	msgbox OreburghCity_Gym_Text_RoarkJaVenceu, MSGBOX_DEFAULT
	release
	end

OreburghCity_Gym_Text_RoarkIntro:
	.string "...$"

OreburghCity_Gym_Text_RoarkDefeat:
	.string "W-what? That can't be!\nMy buffed-up Pokémon!$"

OreburghCity_Gym_Text_RoarkPost:
	.string "...$"

OreburghCity_Gym_Text_RoarkJaVenceu:
	.string "The COAL BADGE is yours.\nKeep digging deeper, challenger!$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

OreburghCity_Gym_EventScript_Npc1::
	msgbox OreburghCity_Gym_Text_Npc1, MSGBOX_NPC
	end

OreburghCity_Gym_Text_Npc1:
	.string "Howdy!\nHow's it going, Champ-to-be?\pThat's what I said to a really\nimpatient boy earlier, too.\pThe Gym Leader is a user of\nRock-type Pokémon.\pWell, listen. Rock-type Pokémon\nreally hate water, all right?\pThey're also weak to Grass-type\nmoves.\pGee, they sure have weaknesses!\pBut don't think it will be easy.\pYou don't get to be a Gym Leader\nwithout covering for weaknesses.\pGoing after a Rock-type Pokémon\nwith a Fire-type Pokémon won't be\peasy, either.\pThat's all the advice I can give.\nThanks for listening!$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

OreburghCity_Gym_EventScript_YoungsterJonathon::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_JONATHON, OreburghCity_Gym_Text_YoungsterJonathonIntro, OreburghCity_Gym_Text_YoungsterJonathonDefeat
	msgbox OreburghCity_Gym_Text_YoungsterJonathonPost, MSGBOX_AUTOCLOSE
	end

OreburghCity_Gym_Text_YoungsterJonathonIntro:
	.string "You avoided the long way around?\nLet's see why you'd do that!$"

OreburghCity_Gym_Text_YoungsterJonathonDefeat:
	.string "Now I understand why you decided to\nbattle with me.$"

OreburghCity_Gym_Text_YoungsterJonathonPost:
	.string "You should go whichever way you\nwant, shortcut or the long way!$"

OreburghCity_Gym_EventScript_YoungsterDarius::
	trainerbattle_single TRAINER_SINNOH_YOUNGSTER_DARIUS, OreburghCity_Gym_Text_YoungsterDariusIntro, OreburghCity_Gym_Text_YoungsterDariusDefeat
	msgbox OreburghCity_Gym_Text_YoungsterDariusPost, MSGBOX_AUTOCLOSE
	end

OreburghCity_Gym_Text_YoungsterDariusIntro:
	.string "Only those who want to win can\nchallenge a Pokémon Gym!$"

OreburghCity_Gym_Text_YoungsterDariusDefeat:
	.string "Gggh...\nThis is humiliating!$"

OreburghCity_Gym_Text_YoungsterDariusPost:
	.string "One day, I'm going to become a tough\nTrainer like you.$"
