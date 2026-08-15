@ TOHJO FALLS, sala do GIOVANNI. Duelo de cena portado de
@ fontes-mapas/hns/data/maps/TohjoFalls_GiovanniRoom/scripts.inc em 15/08/2026.
@ Texto do hns, palavra por palavra; time do hns, com o nivel na curva de Johto
@ (dev_scripts/porta_cenas_johto.py --treinadores).
@
@ TRES coisas da fonte NAO entraram, e nenhuma por gosto:
@
@ 1. O gatilho. La a cena so roda para quem tem CELEBI andando atras
@    (`specialvar VAR_RESULT, CheckCelebi`, um `special` do hns que este repo
@    nao tem: nao esta em data/specials.inc). Aqui o portao e o mesmo tipo que
@    o resto de Johto usa, flag de TREINADOR: o GIOVANNI so aparece depois que
@    o ARCHER cai na Torre Radio, que e o momento em que a transmissao pirata
@    do radio (a que a placa desta sala descreve) chama o chefe de volta. Ele
@    chega tarde para a propria organizacao, que e a tragedia do original.
@    ZERO var, ZERO flag de enredo: o ON_TRANSITION recalcula tudo.
@ 2. A entrada e a saida do CELEBI (dois `applymovement OBJ_EVENT_ID_FOLLOWER`
@    com jump, fadescreen e SE_M_TELEPORT). Sem o CELEBI seguidor, esses
@    quadros nao tem quem os execute.
@ 3. `playbgm MUS_HG_RADIO_ROCKET`: a musica nao existe nesta build
@    (include/constants/songs.h nao tem MUS_HG_RADIO_ROCKET nem apelido dela).
@
@ O objeto e a vaga que ja existia (indice 0, em (5,4), item ball muda), nao um
@ objeto novo. De frente para o sul, com raio 3, ele ve quem sobe de (5,7),
@ (5,6) ou (5,5); o jogador entra pelo warp de (5,8). Colisao conferida tile a
@ tile no LAYOUT_TOHJO_FALLS_GIOVANNI_ROOM: os quatro sao chao.
@ OBJ_EVENT_GFX_GIOVANNI DESENHA nesta build (a entrada dele em
@ object_event_graphics_info_pointers.h:734 esta FORA de `#if IS_FRLG`, e
@ graphics/object_events/pics/people/giovanni.png existe).

TohjoFalls_GiovanniRoom_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TohjoFalls_GiovanniRoom_OnTransition
	.byte 0

TohjoFalls_GiovanniRoom_OnTransition:
	setflag FLAG_JOHTO_HIDE_TOHJO_GIOVANNI
	goto_if_not_defeated TRAINER_JOHTO_ROCKET_ARCHER, TohjoFalls_GiovanniRoom_EventScript_GiovanniFim
	goto_if_defeated TRAINER_JOHTO_GIOVANNI, TohjoFalls_GiovanniRoom_EventScript_GiovanniFim
	clearflag FLAG_JOHTO_HIDE_TOHJO_GIOVANNI
TohjoFalls_GiovanniRoom_EventScript_GiovanniFim:
	end

TohjoFalls_GiovanniRoom_EventScript_Giovanni::
	trainerbattle_single TRAINER_JOHTO_GIOVANNI, TohjoFalls_GiovanniRoom_Text_GiovanniIntro, TohjoFalls_GiovanniRoom_Text_GiovanniDefeat
	msgbox TohjoFalls_GiovanniRoom_Text_GiovanniAfter, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_JOHTO_HIDE_TOHJO_GIOVANNI
	removeobject LOCALID_TOHJO_FALLS_GIOVANNI
	release
	end

@ Os dois textos que a fonte mostra em sequencia antes da batalha
@ (Text_GiovanniIntro e Text_GiovanniBeforeBattle) estao emendados aqui com um
@ \p: `trainerbattle_single` so aceita UM texto de abertura, e cortar o segundo
@ perderia fala do hns. Nada foi reescrito.
TohjoFalls_GiovanniRoom_Text_GiovanniIntro:
	.string "GIOVANNI: ...\p"
	.string "I don't know why you have come\n"
	.string "here.\p"
	.string "Anyway, I have to warn you that\n"
	.string "this is not a place for kids like\l"
	.string "you.\p"
	.string "You have a certain look.\n"
	.string "It reminds me of the kid who stood\l"
	.string "in front of me three years ago...\p"
	.string "You have the same eyes...\p"
	.string "...\p"
	.string "I'm on my way to GOLDENROD CITY\n"
	.string "to answer the call and join my team.\l"
	.string "Are you going to get in my way?\p"
	.string "My old associates need me...\n"
	.string "We will not repeat the failure of\l"
	.string "three years ago!$"

TohjoFalls_GiovanniRoom_Text_GiovanniDefeat:
	.string "What in the world are you?$"

TohjoFalls_GiovanniRoom_Text_GiovanniAfter:
	.string "GIOVANNI: How is this possible...?\n"
	.string "The past three years have been a\l"
	.string "waste...?\p"
	.string "How can a kid like you manage to\n"
	.string "destroy my dream once again?\p"
	.string "The precious dream of TEAM ROCKET\n"
	.string "has become little more than an\l"
	.string "illusion...$"

@ Placas trazidas do hns por dev_scripts/importa_placas_johto.py

TohjoFalls_GiovanniRoom_EventScript_Radio::
	msgbox TohjoFalls_GiovanniRoom_Text_RadioObject, MSGBOX_SIGN
	end

TohjoFalls_GiovanniRoom_Text_RadioObject::
	.string "A radio...\n"
	.string "The battery is dead...$"
