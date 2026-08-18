GalacticHq4F_MapScripts::
	.byte 0

@ >>> B6 Sinnoh S1: esqueletos de cena (dev_scripts/maquina_sinnoh.py) >>>
@ DESBLOQUEADO em 18/08/2026 (onda 5): TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_
@ GALACTIC_HQ (2514, id pre-atribuido pela condutora) ja existe. A fonte
@ (scripts_galactic_hq_4f.s) rami fica a aproximacao final por coluna do
@ jogador (X8/X9) so pra escolher o passo de caminhada; sem colisao no NPC
@ colapsa numa aproximacao so, mesma tecnica de Route203/209.
@ `trainerbattle_no_intro` porque a fala de abertura (SpeechWasBigLie /
@ IKnowWhyYoureHere) ja e mostrada a mao ANTES da batalha, igual ao molde
@ de Route209_Access_EventScript_CoordEvent_Rival; o texto de derrota
@ literal do Cyrus (TRMSG_DEFEAT do json da fonte) vira o `lose_text`. O
@ pos-batalha (YouAreIndeedStrong / Master Ball / IMakePowerMyOwn /
@ TakeWarpPanel / sai andando) continua na MESMA cena depois da linha de
@ trainerbattle_no_intro (gotopostbattlescript volta pra ca na vitoria; a
@ derrota o motor resolve sozinho, sem branch de BlackOut manual).
@ Sem CanFitItem para o Master Ball: item unico e raro, mesma simplificacao
@ que Route207_EventScript_CoordEvent_Counterpart ja fez pro VS Seeker.
@ Sem setflag de hide no fecho: conferido na fonte que o hidden_flag do
@ objeto nunca e tocado (ver comentario do map.json); quem impede a cena de
@ repetir e o VAR_SINNOH_QG_4F_ESTADO indo pra 1, que desarma o coord_event
@ (var_value == 0). O Cyrus pode reaparecer visualmente numa nova entrada
@ no mapa depois disso (fiel a fonte, que tem a mesma lacuna).
GalacticHq4F_EventScript_CoordEvent_Cyrus::
	lockall
	applymovement 1, GalacticHq4F_Movement_CyrusNoticePlayer
	waitmovement 0
	msgbox GalacticHq4F_Text_SpeechWasBigLie, MSGBOX_DEFAULT
	applymovement 1, GalacticHq4F_Movement_CyrusWalkToPlayer
	waitmovement 0
	msgbox GalacticHq4F_Text_IKnowWhyYoureHere, MSGBOX_DEFAULT
	@ CONSERTO (onda 5): `setvar VAR_LAST_TALKED` ANTES do trainerbattle, molde
	@ de Route209_Access_EventScript_CoordEvent_Rival. Emboscada por
	@ coord_event nao passa por `faceplayer`, entao VAR_LAST_TALKED ficaria com
	@ o ultimo NPC clicado em qualquer mapa e a batalha amarraria o objeto
	@ errado. Valor literal 1 porque o Cyrus e o unico object_event do mapa
	@ (local id 1 por posicao, sem constante em map_event_ids.h, decisao ja
	@ registrada no map.json).
	setvar VAR_LAST_TALKED, 1
	trainerbattle_no_intro TRAINER_SINNOH_GALACTIC_BOSS_CYRUS_GALACTIC_HQ, GalacticHq4F_Text_CyrusDefeat
	msgbox GalacticHq4F_Text_YouAreIndeedStrong, MSGBOX_DEFAULT
	giveitem ITEM_MASTER_BALL
	msgbox GalacticHq4F_Text_IMakePowerMyOwn, MSGBOX_DEFAULT
	msgbox GalacticHq4F_Text_TakeWarpPanel, MSGBOX_DEFAULT
	applymovement 1, GalacticHq4F_Movement_CyrusLeave
	waitmovement 0
	removeobject 1
	setvar VAR_SINNOH_QG_4F_ESTADO, 1
	releaseall
	end

GalacticHq4F_Movement_CyrusNoticePlayer:
	walk_in_place_down
	step_end

GalacticHq4F_Movement_CyrusWalkToPlayer:
	walk_down
	walk_down
	walk_in_place_down
	step_end

GalacticHq4F_Movement_CyrusLeave:
	walk_up
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

GalacticHq4F_Text_SpeechWasBigLie:
	.string "CYRUS: ...So, you've come.\p"
	.string "You heard my speech, I take it.\n"
	.string "Snicker... A big lie, of course.\p"
	.string "It's true insofar as my intention is\n"
	.string "to create a new world.\p"
	.string "But that world isn't for the likes\n"
	.string "of Team Galactic. I seek an entirely\lnew world solely for myself.$"

GalacticHq4F_Text_IKnowWhyYoureHere:
	.string "I know why you're here. It's about\n"
	.string "UXIE, MESPRIT, and AZELF, right?\p"
	.string "I no longer have any need for them.\n"
	.string "If your heart aches to save them,\lgo right ahead.\p"
	.string "Such pitifully useless emotions...\n"
	.string "I will make you regret paying heed\lto your heart!$"

GalacticHq4F_Text_CyrusDefeat:
	.string "Interesting.\n"
	.string "And quite curious.$"

GalacticHq4F_Text_YouAreIndeedStrong:
	.string "CYRUS: I see.\n"
	.string "You are indeed strong.\p"
	.string "And the basis of your power is your\n"
	.string "compassion toward Pokémon...\p"
	.string "That doesn't matter. I doubt you\n"
	.string "will ever understand my position.\p"
	.string "But I recognize that you are strong\n"
	.string "and courageous to come alone.\lThis is your reward.$"

GalacticHq4F_Text_IMakePowerMyOwn:
	.string "CYRUS: The Master Ball is the\n"
	.string "ultimate Poké Ball.\p"
	.string "But it is not anything that I\n"
	.string "require. I don't make Pokémon my\lfriends or partners.\p"
	.string "Instead, I make the power of\n"
	.string "Pokémon my own.$"

GalacticHq4F_Text_TakeWarpPanel:
	.string "If you wish to save the Pokémon\n"
	.string "from the lakes, take the warp panel\lahead.\p"
	.string "I am off to Mt. Coronet. I will\n"
	.string "ascend to its peak, where I will\lcreate my new world...$"

@ <<< B6 Sinnoh S1: esqueletos de cena <<<

GalacticHq4F_EventScript_Placa1::
	msgbox GalacticHq4F_Text_Placa1, MSGBOX_SIGN
	end

GalacticHq4F_Text_Placa1:
	.string "Team Galactic Report$"
