@ Ginasio de Sinnoh com interior reaproveitado de Hoenn.

PastoriaCity_Gym_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ S5: os 3 botoes da fonte (rotulos PastoriaGym_BlueButton/GreenButton/
@ YellowButton) so chamam a special nativa `PressPastoriaGymButton`, que
@ move o nivel d'agua/plataformas do labirinto aquatico do ginasio real de
@ Pastoria. Ausente aqui (grep vazio em src/, include/, data/specials.inc),
@ e o comentario do topo do arquivo ja avisa que este ginasio reaproveita
@ interior de Hoenn: nao existe labirinto d'agua para mover. Mesmo caso do
@ MoveHearthomeGymDPLift em HearthomeCityDpGymElevatorRoom1/2. Os SetVar
@ de VAR_TEMP_1/2/3 da fonte tambem saem: sem a special, nada le esses
@ temps neste mapa (conferido, nenhum outro coord_event/script daqui os
@ usa), entao so ficariam soltos sem efeito. Descartado sem substituto.
PastoriaCity_Gym_EventScript_BlueButton::
	end

PastoriaCity_Gym_EventScript_GreenButton::
	end

PastoriaCity_Gym_EventScript_YellowButton::
	end

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

PastoriaCity_Gym_EventScript_Leader::
	lock
	faceplayer
	goto_if_set FLAG_INSIGNIA_SINNOH_4, PastoriaCity_Gym_EventScript_JaVenceu
	msgbox PastoriaCity_Gym_Text_Intro, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_SINNOH_LEADER_WAKE, PastoriaCity_Gym_Text_Defeat
	msgbox PastoriaCity_Gym_Text_Post, MSGBOX_DEFAULT
	setflag FLAG_INSIGNIA_SINNOH_4
	@ Leva final (18/08/2026): fecho da corrente de Pastoria, molde dos fechos
	@ pos-vitoria de Maylene (VeilstoneCity_Gym) e Fantina (HearthomeCity_Gym).
	@ Os tres comandos abaixo sao as tres linhas que a fonte poe aqui
	@ (res/field/scripts/scripts_pastoria_city_gym.s:66-68).
	@
	@ DESVIO DE VALOR, documentado como a condutora pediu: a fonte escreve 3
	@ aqui e so chega a 4 na cutscene `PastoriaCity_OnFrame_ExitGym`
	@ (scripts_pastoria_city.s:524), a cena em que o Wake sai do ginasio atras
	@ do jogador. Essa cutscene NAO foi portada (nao esta no censo do S1 nem em
	@ nenhuma onda desta obra), e nada neste repositorio le o valor 3: `grep`
	@ por VAR_SINNOH_PASTORIA_ESTADO em data/ da so os quatro coord_events de
	@ PastoriaCity (valores 1, 4 e 5) e os escritores 2 e 5 do proprio mapa.
	@ Escrever 3 e depois 4 seria duas linhas com uma sem efeito; escrevemos o
	@ 4 direto, que e o estado em que a corrente da bomba fica ARMADA, e este
	@ comentario e o registro do valor pulado.
	setvar VAR_SINNOH_PASTORIA_ESTADO, 4
	@ Fonte: SetFlag FLAG_HIDE_PASTORIA_CITY_GRUNT_M. O grunt que fica de pe na
	@ cidade antes do ginasio some; quem o traz de volta e a propria cena da
	@ bomba, com `clearflag`+`addobject` na posicao nova.
	setflag FLAG_SINNOH_ESCONDE_PASTORIA_CITY_GRUNT_M
	@ Fonte: SetFlag FLAG_BLOCK_PASTORIA_CITY_CROAGUNK_EVENT. Trava o sorteio
	@ do Croagunk da placa (PastoriaCity_EventScript_CoordEvent_FaceBoard le
	@ com goto_if_set). Quem apaga, na fonte, e scripts_valor_lakefront.s, fora
	@ do escopo desta obra: aqui ela fica acesa a partir daqui.
	setflag FLAG_SINNOH_PASTORIA_CROAGUNK_BLOQUEADO
	release
	end

PastoriaCity_Gym_EventScript_JaVenceu::
	msgbox PastoriaCity_Gym_Text_JaVenceu, MSGBOX_DEFAULT
	release
	end

PastoriaCity_Gym_Text_Intro:
	.string "...$"

PastoriaCity_Gym_Text_Defeat:
	.string "Hunwah!\nIt's gone and ended!How will I say this... I want more!\nI wanted to battle a lot more!$"

PastoriaCity_Gym_Text_Post:
	.string "...$"

PastoriaCity_Gym_Text_JaVenceu:
	.string "The FEN BADGE is already yours.$"

@ Fala de NPC e de placa vinda do pokeplatinum (dev_scripts/texto_sinnoh.py)

PastoriaCity_Gym_EventScript_Npc1::
	msgbox PastoriaCity_Gym_Text_Npc1, MSGBOX_NPC
	end

PastoriaCity_Gym_Text_Npc1:
	.string "The Gym Leader Wake... Uh, I mean\nCrasher Wake, is a master of\pWater-type Pokémon.\pI'd say you've got guts if you try\nto face down Water types with Fire-\por Ground-type Pokémon!\pBut that part I'll leave up to you!\nGo and have some good battles!$"

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

PastoriaCity_Gym_EventScript_TuberJacky::
	trainerbattle_single TRAINER_SINNOH_TUBER_JACKY, PastoriaCity_Gym_Text_TuberJackyIntro, PastoriaCity_Gym_Text_TuberJackyDefeat
	msgbox PastoriaCity_Gym_Text_TuberJackyPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_TuberJackyIntro:
	.string "My body isn't the only thing I\nwork on toughening up here.\pI also work on my Pokémon and my\nspirit!$"

PastoriaCity_Gym_Text_TuberJackyDefeat:
	.string "Wow, Trainer! You just might be\ntougher than our Gym Leader!$"

PastoriaCity_Gym_Text_TuberJackyPost:
	.string "Maybe I'll do like Wake,\pI mean, Crasher Wake, and wear\nthe same kind of mask.$"

PastoriaCity_Gym_EventScript_SailorDamian::
	trainerbattle_single TRAINER_SINNOH_SAILOR_DAMIAN, PastoriaCity_Gym_Text_SailorDamianIntro, PastoriaCity_Gym_Text_SailorDamianDefeat
	msgbox PastoriaCity_Gym_Text_SailorDamianPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_SailorDamianIntro:
	.string "I've been around the world, going from\nplace to place training Pokémon.\pIt's this Gym I've chosen to make my\nhome!\pYou can bet it's tough!$"

PastoriaCity_Gym_Text_SailorDamianDefeat:
	.string "You!\nYou're truly top-class tough!$"

PastoriaCity_Gym_Text_SailorDamianPost:
	.string "If you were to go around the world,\nI'm sure you'd meet tougher Pokémon.$"

PastoriaCity_Gym_EventScript_TuberCaitlyn::
	trainerbattle_single TRAINER_SINNOH_TUBER_CAITLYN, PastoriaCity_Gym_Text_TuberCaitlynIntro, PastoriaCity_Gym_Text_TuberCaitlynDefeat
	msgbox PastoriaCity_Gym_Text_TuberCaitlynPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_TuberCaitlynIntro:
	.string "I want to become a strong Trainer\nlike Crasher Wake!$"

PastoriaCity_Gym_Text_TuberCaitlynDefeat:
	.string "Groan...\nYou're too much.$"

PastoriaCity_Gym_Text_TuberCaitlynPost:
	.string "Maybe I'll do like Wake...\pI mean, Crasher Wake, and use\nthe same kinds of Pokémon.$"

PastoriaCity_Gym_EventScript_SailorSamson::
	trainerbattle_single TRAINER_SINNOH_SAILOR_SAMSON, PastoriaCity_Gym_Text_SailorSamsonIntro, PastoriaCity_Gym_Text_SailorSamsonDefeat
	msgbox PastoriaCity_Gym_Text_SailorSamsonPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_SailorSamsonIntro:
	.string "Like the raging sea, I crash down\nand wash away everything before me!\pThat's just how I roll!$"

PastoriaCity_Gym_Text_SailorSamsonDefeat:
	.string "That wave didn't even wash\nmy hands...$"

PastoriaCity_Gym_Text_SailorSamsonPost:
	.string "I'm now becalmed like a waveless\nsea...$"

PastoriaCity_Gym_EventScript_FishermanErick::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_ERICK, PastoriaCity_Gym_Text_FishermanErickIntro, PastoriaCity_Gym_Text_FishermanErickDefeat
	msgbox PastoriaCity_Gym_Text_FishermanErickPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_FishermanErickIntro:
	.string "I've landed the most fish Pokémon\nin the world. I'm next!$"

PastoriaCity_Gym_Text_FishermanErickDefeat:
	.string "Being number one in the world doesn't\nmean a thing...$"

PastoriaCity_Gym_Text_FishermanErickPost:
	.string "I figure I got too wrapped up in\nfishing and neglected training.$"

PastoriaCity_Gym_EventScript_FishermanWalter::
	trainerbattle_single TRAINER_SINNOH_FISHERMAN_WALTER, PastoriaCity_Gym_Text_FishermanWalterIntro, PastoriaCity_Gym_Text_FishermanWalterDefeat
	msgbox PastoriaCity_Gym_Text_FishermanWalterPost, MSGBOX_AUTOCLOSE
	end

PastoriaCity_Gym_Text_FishermanWalterIntro:
	.string "I wield the stupendous power of water!\nDon't think you can win!$"

PastoriaCity_Gym_Text_FishermanWalterDefeat:
	.string "But the kid wins anyway!\nI'm just bowled over!$"

PastoriaCity_Gym_Text_FishermanWalterPost:
	.string "The water rising and falling is tricky,\nbut don't let it annoy you.\pIf you lose sight of yourself, that's\nwhen you're set to lose.$"
