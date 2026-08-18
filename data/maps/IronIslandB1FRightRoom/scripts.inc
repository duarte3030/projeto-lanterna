IronIslandB1FRightRoom_MapScripts::
	.byte 0

@ BLOQUEADO (S7, 18/08/2026). A fonte (scripts_iron_island_b*.s) resolve a
@ plataforma inteira com dois specials, InitPersistedMapFeaturesForPlatform
@ Lift (OnTransition) e TriggerPlatformLift (o coord_event), nenhum dos dois
@ existe neste motor (`grep` em include/ e src/ confirma zero ocorrencias).
@ Nao e so o texto/movimento que falta: e a mecanica de plataforma
@ deslizante inteira (estado persistido entre visitas ao andar). "Specials
@ inexistentes descartados com comentario", sem substituto aqui. Volta ao
@ plano.
IronIslandB1FRightRoom_EventScript_CoordEvent_PlatformLift::
	end

@ Treinador do pokeplatinum: time, raio de visao e fala
@ (dev_scripts/treinadores_masmorra_sinnoh.py)

IronIslandB1FRightRoom_EventScript_PicnickerSummer::
	trainerbattle_single TRAINER_SINNOH_PICNICKER_SUMMER, IronIslandB1FRightRoom_Text_PicnickerSummerIntro, IronIslandB1FRightRoom_Text_PicnickerSummerDefeat
	msgbox IronIslandB1FRightRoom_Text_PicnickerSummerPost, MSGBOX_AUTOCLOSE
	end

IronIslandB1FRightRoom_Text_PicnickerSummerIntro:
	.string "May we have a battle, please?\pIt will be something to lighten up this\nboring picnic with.$"

IronIslandB1FRightRoom_Text_PicnickerSummerDefeat:
	.string "We're not going to win if we play\naround like that...$"

IronIslandB1FRightRoom_Text_PicnickerSummerPost:
	.string "I'm going home to play with my\nPokémon!$"
