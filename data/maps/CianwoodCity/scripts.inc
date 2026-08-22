@ CIANWOOD CITY. O SUICUNE que passa correndo e o duelo do EUSINE, portados de
@ fontes-mapas/hns/data/maps/CianwoodCity/scripts.inc em 15/08/2026
@ (EventScript_SuicuneTrigger e os movimentos Suicune1..3 / Eusine1..3, linha a
@ linha). Texto do hns, palavra por palavra; time do hns, com o nivel na curva
@ de Johto (dev_scripts/porta_cenas_johto.py --treinadores).
@
@ O QUE MUDOU em relacao a fonte, e por que:
@
@ 1. O portao. La a cena e o TERCEIRO avistamento do SUICUNE
@    (VAR_SUICUNE_ENCOUNTERS >= 2, alimentada pela Route 36 e pela Route 42, que
@    esta ROM nao tem). Aqui ela e AUTOCONTIDA: acontece uma vez, na primeira
@    vez que o jogador sobe a rua da praia, e por isso a fala do EUSINE
@    ("aquilo nao era o SUICUNE agora ha pouco?") continua verdadeira, porque o
@    jogador acabou de ver.
@ 2. Sprite do EUSINE: OBJ_EVENT_GFX_EUSINE NAO EXISTE nesta build, nem dentro
@    de `#if IS_FRLG` (nao esta no enum de include/constants/event_objects.h).
@    Substituido por OBJ_EVENT_GFX_PSYCHIC_M, que e o homem de capa desta
@    build, na mesma linha das trocas ja feitas em 05/08 (SUPER_NERD ->
@    SCIENTIST_1, JUGGLER -> EXPERT_M). Em batalha, TRAINER_CLASS_PSYCHIC e
@    TRAINER_PIC_PSYCHIC_M pelo mesmo motivo (nao existe MYSTERY_MAN aqui).
@ 3. Sprite do SUICUNE: a fonte usa `OBJ_EVENT_GFX_MON_BASE+SPECIES_SUICUNE`,
@    que aqui e OBJ_EVENT_GFX_SPECIES(SUICUNE). Medido antes de escrever, que e
@    a licao 4.5: SPECIES_SUICUNE TEM bloco OVERWORLD() em
@    src/data/pokemon/species_info/gen_2_families.h, entao o grafico existe e o
@    id nao aponta para o vazio.
@ 4. `playbgm MUS_HG_EUSINE` caiu: a musica nao existe nesta build.
@
@ Os dois objetos sao as vagas que ja existiam (indices 0 e 1, item balls
@ mudas, nas MESMAS coordenadas da fonte), nao objetos novos.
@
@ Nenhum `applymovement` mexe no JOGADOR: so emote (ExclamationMark) e
@ `turnobject`. Isso e de proposito, e e o que separa esta cena do risco
@ descrito na secao 3 do PENDENCIAS-JOHTO.md: movimento roteirizado de NPC nao
@ consulta colisao (src/event_object_movement.c, InitNpcForMovement), mas o do
@ jogador consulta, e caminho bloqueado ali trava o `waitmovement` para sempre.

CianwoodCity_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CianwoodCity_OnTransition
	.byte 0

@ Recalcula tudo a cada entrada no mapa, em vez de confiar no que ficou gravado:
@ o unico estado de verdade e a flag do TRAINER_JOHTO_EUSINE, que o motor grava
@ sozinho quando ele cai. A var existe so porque `coord_event` compara var.
CianwoodCity_OnTransition:
	setflag FLAG_JOHTO_HIDE_CIANWOOD_SUICUNE
	setflag FLAG_JOHTO_HIDE_CIANWOOD_EUSINE
	setvar VAR_JOHTO_CIANWOOD_SUICUNE, 0
	goto_if_defeated TRAINER_JOHTO_EUSINE, CianwoodCity_EventScript_SuicuneFim
	clearflag FLAG_JOHTO_HIDE_CIANWOOD_SUICUNE
	setvar VAR_JOHTO_CIANWOOD_SUICUNE, 1
CianwoodCity_EventScript_SuicuneFim:
	end

CianwoodCity_EventScript_SuicuneTrigger::
	lock
	playmoncry SPECIES_SUICUNE, CRY_MODE_NORMAL
	applymovement LOCALID_CIANWOOD_CITY_SUICUNE, CianwoodCity_Movement_Suicune1
	playse SE_LEDGE
	waitse
	playse SE_LEDGE
	waitse
	waitmovement 0
	waitmoncry
	playse SE_PIN
	applymovement OBJ_EVENT_ID_PLAYER, Common_Movement_ExclamationMark
	delay 60
	applymovement LOCALID_CIANWOOD_CITY_SUICUNE, CianwoodCity_Movement_Suicune2
	playse SE_LEDGE
	delay 30
	playse SE_LEDGE
	delay 30
	waitmovement 0
	turnobject OBJ_EVENT_ID_PLAYER, DIR_SOUTH
	applymovement LOCALID_CIANWOOD_CITY_SUICUNE, CianwoodCity_Movement_Suicune3
	playse SE_LEDGE
	delay 30
	playse SE_LEDGE
	delay 30
	waitmovement 0
	delay 30
	setflag FLAG_JOHTO_HIDE_CIANWOOD_SUICUNE
	removeobject LOCALID_CIANWOOD_CITY_SUICUNE
	clearflag FLAG_JOHTO_HIDE_CIANWOOD_EUSINE
	addobject LOCALID_CIANWOOD_CITY_EUSINE
	applymovement LOCALID_CIANWOOD_CITY_EUSINE, CianwoodCity_Movement_Eusine1
	waitmovement 0
	delay 55
	applymovement LOCALID_CIANWOOD_CITY_EUSINE, CianwoodCity_Movement_Eusine2
	waitmovement 0
	msgbox CianwoodCity_Text_EusineSuicune, MSGBOX_DEFAULT
	trainerbattle_no_intro TRAINER_JOHTO_EUSINE, CianwoodCity_Text_EusineBeaten
	msgbox CianwoodCity_Text_EusineAfter, MSGBOX_DEFAULT
	closemessage
	applymovement LOCALID_CIANWOOD_CITY_EUSINE, CianwoodCity_Movement_Eusine3
	waitmovement 0
	setflag FLAG_JOHTO_HIDE_CIANWOOD_EUSINE
	removeobject LOCALID_CIANWOOD_CITY_EUSINE
	setvar VAR_JOHTO_CIANWOOD_SUICUNE, 2
	release
	end

CianwoodCity_Movement_Suicune1:
	jump_in_place_right_left
	jump_in_place_right_left
	face_down
	step_end

CianwoodCity_Movement_Suicune2:
	jump_down
	jump_2_down
	jump_right
	face_up
	step_end

CianwoodCity_Movement_Suicune3:
	jump_2_down
	jump_2_right
	jump_2_right
	jump_2_right
	jump_2_right
	jump_2_right
	step_end

CianwoodCity_Movement_Eusine1:
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	face_right
	step_end

CianwoodCity_Movement_Eusine2:
	face_up
	walk_up
	walk_up
	step_end

CianwoodCity_Movement_Eusine3:
	face_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	walk_fast_down
	step_end

CianwoodCity_Text_EusineSuicune:
	.string "EUSINE: Yo, {PLAYER}.\p"
	.string "Wasn't that SUICUNE just now?\p"
	.string "I only caught a quick glimpse, but\n"
	.string "I thought I saw SUICUNE running on\l"
	.string "the waves.\p"
	.string "SUICUNE is beautiful and grand.\p"
	.string "And it races through towns and\n"
	.string "roads at simply awesome speeds.\p"
	.string "It's wonderful…\p"
	.string "I want to see SUICUNE up close…\p"
	.string "I've decided.\p"
	.string "I'll battle you as a trainer to\n"
	.string "earn SUICUNE's respect!\p"
	.string "Come on, {PLAYER}. Let's battle now!$"

CianwoodCity_Text_EusineBeaten:
	.string "I hate to admit it, but you win.$"

CianwoodCity_Text_EusineAfter:
	.string "You're amazing, {PLAYER}!\p"
	.string "No wonder POKéMON gravitate to you.\p"
	.string "I get it now.\p"
	.string "I'm going to keep searching for\n"
	.string "SUICUNE.\p"
	.string "I'm sure we'll see each other again.\p"
	.string "See you around!$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

CianwoodCity_EventScript_CaveSign::
	lock
	msgbox CianwoodCity_Text_Safari, MSGBOX_SIGN
	closemessage
	release
	end

CianwoodCity_EventScript_CitySign::
	lock
	msgbox CianwoodCity_Text_Sign, MSGBOX_SIGN
	closemessage
	release
	end

CianwoodCity_EventScript_GymSign::
	lock
	msgbox CianwoodCity_Text_GymSign, MSGBOX_SIGN
	closemessage
	release
	end

CianwoodCity_EventScript_Pharmacy::
	lock
	msgbox CianwoodCity_Text_PharmacySign, MSGBOX_SIGN
	closemessage
	release
	end

CianwoodCity_Text_GymSign::
	.string "CIANWOOD CITY POKéMON GYM\p"
	.string "LEADER: CHUCK\p"
	.string "His Roaring Fists Do the Talking$"

CianwoodCity_Text_PharmacySign::
	.string "500 Years of Tradition\p"
	.string "CIANWOOD CITY PHARMACY\p"
	.string "We Await Your Medicinal Queries$"

CianwoodCity_Text_Safari::
	.string "CLIFF EDGE CAVE\n"
	.string "Road to the SAFARI ZONE.$"

CianwoodCity_Text_Sign::
	.string "CIANWOOD CITY\p"
	.string "A Port Surrounded by Rough Seas$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

CianwoodCity_EventScript_PokefanM::
	lock
	faceplayer
	msgbox CianwoodCity_Text_PokefanM, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodCity_Text_PokefanM::
	.string "Boulders to the north of town can\n"
	.string "be crushed.\p"
	.string "They may be hiding something.\p"
	.string "Your POKéMON could use ROCK SMASH\n"
	.string "to break them.$"

CianwoodCity_EventScript_Youngster::
	lock
	faceplayer
	msgbox CianwoodCity_Text_Youngster, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodCity_Text_Youngster::
	.string "If you use FLY, you can get back\n"
	.string "to OLIVINE instantly.$"

CianwoodCity_EventScript_Lass::
	lock
	faceplayer
	msgbox CianwoodCity_Text_Lass, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodCity_Text_Lass::
	.string "CHUCK, the GYM LEADER, spars with\n"
	.string "his fighting POKéMON.$"

@ NPCs devolvidos do hns por dev_scripts/restaura_npcs_johto.py

CianwoodCity_EventScript_Engineer::
	lock
	faceplayer
	msgbox CianwoodCity_Text_Engineer, MSGBOX_DEFAULT
	closemessage
	release
	end

CianwoodCity_Text_Engineer::
	.string "This path is under construction.\n"
	.string "We're getting the new SAFARI ZONE\l"
	.string "up and running!$"

@ >>> Dex completa (dev_scripts/distribui_dex.py) >>>
CianwoodCity_EventScript_DexSuicune::
	lockall
	msgbox CianwoodCity_Text_DexSuicuneIntro, MSGBOX_DEFAULT
	waitse
	playmoncry SPECIES_SUICUNE, CRY_MODE_ENCOUNTER
	delay 30
	waitmoncry
	seteventmon SPECIES_SUICUNE, 50
	setflag FLAG_SYS_CTRL_OBJ_DELETE
	special BattleSetup_StartLegendaryBattle
	clearflag FLAG_SYS_CTRL_OBJ_DELETE
	setvar VAR_LAST_TALKED, LOCALID_DEX_SUICUNE
	specialvar VAR_RESULT, GetBattleOutcome
	call_if_eq VAR_RESULT, B_OUTCOME_WON, CianwoodCity_EventScript_DexSuicuneSome
	call_if_eq VAR_RESULT, B_OUTCOME_CAUGHT, CianwoodCity_EventScript_DexSuicuneSome
	releaseall
	end

CianwoodCity_EventScript_DexSuicuneSome::
	fadescreenswapbuffers FADE_TO_BLACK
	removeobject LOCALID_DEX_SUICUNE
	setflag FLAG_HIDE_DEX_SUICUNE
	fadescreenswapbuffers FADE_FROM_BLACK
	return

CianwoodCity_Text_DexSuicuneIntro:
	.string "SUICUNE appeared!$"

@ <<< Dex completa <<<
